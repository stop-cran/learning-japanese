"""Export the blind review packet for batch N from its signed candidate commit, without author adjudication.

Everything is read from the candidate commit (git show / git archive), the author gate logs bound to the
candidate manifest, and the one-time snapshot capture. All named Weblio source sections are extracted.
Usage: python -B build-packet-b128-v2.py <batch>
"""
import html
import json
import re
import sys
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

from common import (CHECKS, SIGNER, SNAP, WS, TOOLS, at_commit, freeze_json, frozen, git, json_bytes, load_batch,
                    packet_dir, require, review_dir, sha, start_guard, word, write_frozen)

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse  # noqa: E402

START = "<!--開始 デジタル大辞泉 -->"
END = "<!--終了 デジタル大辞泉-->"
BLOCK = re.compile(r"<(?:br|/p|/div|/li|/h[1-6]|/tr|/table|/dt|/dd)\b[^>]*>", re.IGNORECASE)
METHOD = (
    "extract-daijisen-v1: decode the response as strict UTF-8; require exactly one '" + START + "' marker "
    "and exactly one later '" + END + "' marker, otherwise AMBIGUOUS and no extract; take the text "
    "strictly between them; delete <script>/<style> elements and HTML comments; collapse each run of "
    "HTML ASCII whitespace (space, tab, LF, CR, FF) to one space; replace each <br>, </p>, </div>, </li>, "
    "</h1-6>, </tr>, </table>, </dt> and </dd> tag with a line break; delete all other tags; decode HTML "
    "character references; strip ASCII spaces at both ends of each line; drop empty lines; join with LF "
    "and end with one LF. All other characters, including non-ASCII spaces and private-use code points, "
    "are kept verbatim."
)
JOYO_PDF = WS / "review-packets" / "_checks-109-fix" / "joyokanjihyo_20101130.pdf"
AUTHOR_ONLY = {"source-receipt.json", "artifact-sha256.json", "selection.json", "evidence-index.json"}


def extract(raw):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return None, f"Response is not strict UTF-8: {error}"
    if text.count(START) != 1 or text.count(END) != 1:
        return None, f"Marker counts start={text.count(START)} end={text.count(END)}; expected exactly one each"
    a, b = text.index(START) + len(START), text.index(END)
    if b <= a:
        return None, "End marker precedes start marker"
    body = text[a:b]
    body = re.sub(r"<script\b.*?</script\s*>", "", body, flags=re.S | re.I)
    body = re.sub(r"<style\b.*?</style\s*>", "", body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"[ \t\n\r\f]+", " ", body)
    body = BLOCK.sub("\n", body)
    body = re.sub(r"<[^>]*>", "", body)
    body = html.unescape(body)
    lines = [line for line in (line.strip(" ") for line in body.split("\n")) if line]
    if not lines:
        return None, "Marked section contains no text"
    return "\n".join(lines) + "\n", None


from b128_external_sources import METHOD as SECTION_METHOD, extract as extract_sections
from source_contract import load as load_source_contract, read as contract_source


def main(batch):
    config = load_batch(batch)
    out = packet_dir(config)
    record_path = review_dir(batch) / "packet-build.json"
    require(not out.exists() and not record_path.exists(), "Packet already built; preserve it")
    candidate, base, members, n = config["candidate"], config["base"], config["members"], config["batch"]
    signature = git(config, "log", "-1", "--format=%G?|%GS|%ae|%ce|%P", candidate).decode().strip().split("|")
    require(signature[0] == "G" and SIGNER in signature[1] and signature[2] == signature[3] == SIGNER,
            f"Candidate is not signed and committed by the owner: {signature}")
    require(signature[4] == base, "Base is not the candidate's sole parent")
    guard, _ = start_guard("Packet export")
    temporary = review_dir(batch) / f"packet-export-{candidate[:8]}.tar"
    require(not temporary.exists(), "Stale export archive")
    files = {}

    def put(relative, data):
        require(relative not in files, f"Duplicate packet file: {relative}")
        files[relative] = data

    try:
        changed = {}
        for line in git(config, "diff", "--name-status", "--no-renames", base, candidate).decode().splitlines():
            status, path = line.split("\t", 1)
            changed[path] = status
        runtime = [f"{folder}/{c}.{ext}" for folder, ext in (("kanji", "md"), ("strokes", "json")) for c in members]
        added_words = sorted(p for p, s in changed.items() if s == "A" and p.startswith("words/"))
        modified = sorted(p for p, s in changed.items() if s == "M" and p.startswith("words/"))
        sources_dir = f"docs/n1-sources/batch-{n}/"
        allowed_added = set(runtime) | set(added_words)
        require(all(s in "AM" for s in changed.values()), f"Unexpected change kind: {changed}")
        require({p for p, s in changed.items() if s == "A" and not p.startswith("docs/n1-sources/")} == allowed_added,
                "Added runtime files differ from the batch members")
        require({p for p, s in changed.items() if s == "M" and not p.startswith("docs/n1-sources/")}
                <= set(modified) | {"manifest.json", "docs/n1-authoring-notes.md"}, "Unexpected modified file")
        require("manifest.json" in changed, "Manifest not rebuilt")
        require(not added_words, "New word articles need an explicit packet contract")
        cards = {c: at_commit(config, f"kanji/{c}.md") for c in members}
        linked = []
        for c in members:
            linked += re.findall(r"\]\(\.\./words/([^)]+\.md)\)", cards[c].decode("utf-8"))
        unchanged = sorted({f"words/{w}" for w in linked} - set(modified))
        for relative in unchanged:
            require(at_commit(config, relative) == git(config, "show", f"{base}:{relative}"), relative)
        for relative in runtime + modified:
            guard.check()
            put(f"snapshot/{relative}", at_commit(config, relative))
        git(config, "-c", "core.autocrlf=false", "archive", "--format=tar", f"--output={temporary}", candidate,
            "--", "kanji", *modified, *unchanged)
        kanji_count = 0
        with tarfile.open(temporary, "r|") as archive:
            for entry in archive:
                guard.check()
                if entry.isdir():
                    continue
                path = PurePosixPath(entry.name)
                require(entry.isfile() and len(path.parts) == 2 and ".." not in path.parts
                        and path.parts[0] in {"kanji", "words"} and path.suffix == ".md", f"Archive entry {path}")
                put(f"repo/{path}", archive.extractfile(entry).read())
                kanji_count += path.parts[0] == "kanji"
        temporary.unlink()
        require(kanji_count == config["expectedKanji"], f"Kanji count {kanji_count} != {config['expectedKanji']}")
        for relative in [p for p in runtime if p.endswith(".md")] + modified:
            require(files[f"repo/{relative}"] == files[f"snapshot/{relative}"], relative)
        manifest_data = at_commit(config, "manifest.json")
        put("repo/manifest.json", manifest_data)
        for relative in ("docs/content-format.md", "docs/jlpt-levels.md"):
            put(f"repo/{relative}", at_commit(config, relative))
        for relative in (".github/copilot-instructions.md", ".github/instructions/content-structure.instructions.md"):
            put(f"rubric/{Path(relative).name}", at_commit(config, relative))
        diff = git(config, "diff", "--no-color", base, candidate, "--", *modified)
        put("diffs/existing.diff", diff)
        wrappers = 0
        for line in diff.decode("utf-8").splitlines():
            for c in members:
                count = line.count(f"](../kanji/{c}.md)")
                wrappers += count if line.startswith("+") and not line.startswith("+++") else 0
                wrappers -= count if line.startswith("-") and not line.startswith("---") else 0
        require(wrappers > 0, "No link wrapper added")

        source_contract = load_source_contract(config, lambda path: at_commit(config, path)) \
            if "sourceContract" in config else None

        def source(name):
            if source_contract is not None:
                return contract_source(source_contract, name)
            return at_commit(config, sources_dir + name)

        evidence = json.loads(source("evidence-index.json"))
        selection = json.loads(source("selection.json"))
        require(selection["order"] == members, "Selection order differs from batch.json")
        for name, expected in evidence["outputs"].items():
            require(sha(source(name)) == expected, f"Evidence hash mismatch: {name}")
        source_jm, source_kd = source("jmdict-families.xml"), source("kanjidic2-records.xml")
        entries = ET.fromstring(source_jm).findall("entry")
        dictionary_index = evidence["dictionaryQueryEntries"]
        ids = {e.findtext("ent_seq") for e in entries}
        require(len(ids) == len(entries) == evidence["completeDictionaryEntries"]
                and ids == {i for v in dictionary_index.values() for i in v}, "Dictionary families incomplete")
        put("evidence/jmdict-families.xml", source_jm)
        put("evidence/kanjidic2-records.xml", source_kd)
        for name in ("joyo-rows.json", "shape-evidence.json"):
            put(f"evidence/{name}", source(name))
        for char in members:
            name = f"{ord(char):05x}.svg"
            put(f"evidence/kanjivg/{name}", source(f"kvg/{name}"))
        put(f"evidence/{JOYO_PDF.name}", JOYO_PDF.read_bytes())
        index = {r["kanji"]: r for r in json.loads(at_commit(config, "docs/n1-sources/source-index.json"))}
        require([index[c]["sourceRow"] for c in members] == selection["sourceRows"], "Source rows differ")
        put("evidence/source-metadata.json", json_bytes(
            {c: {**index[c]["metadata"], "sourceRow": index[c]["sourceRow"]} for c in members}))
        put("evidence/dictionary-index.json", json_bytes(dictionary_index))
        snapshot = json.loads(at_commit(config, "docs/n1-source-snapshot.json"))
        put("evidence/provenance.json", json_bytes({
            "candidate": candidate, "base": base, "pinnedInputs": snapshot["inputs"], "familyCount": len(entries),
            "sourceScope": "Complete families for all queries in dictionary-index.json. Empty exact queries do not "
                           "prove impossibility.",
            "serialization": (source_contract["method"] if source_contract is not None else
                              "Complete JMdict families copied byte for byte from committed batch evidence. "
                              "Not byte-identical compressed-source slices. No author observations or adjudication."),
            "originalExtractionHashes": {"jmdict": sha(source_jm), "kanjidic2": sha(source_kd)},
            "explicitSourceContract": config.get("sourceContract"),
            "sourceNormalization": (source_contract["method"] if source_contract is not None else None),
            "kanjivgRevision": "70a0b7ae0c18ceb5cb358274b029cce0234a43bc", "joyoPdfSha256": sha(JOYO_PDF.read_bytes()),
            "publicCharacterSources": {c: f"https://www.weblio.jp/content/{c}" for c in members},
            "dictionaryAttribution": snapshot["dictionaryAttribution"],
            "kanjivgAttribution": snapshot["kanjivgAttribution"],
        }))
        gates = Path(config["gates"])
        manifest_sha = sha(manifest_data)
        gate_receipts = {}
        for name in CHECKS:
            actual_name = config.get("gateNames", {}).get(name, name)
            receipt = json.loads((gates / f"{actual_name}.json").read_bytes())
            require(receipt["gate"] == actual_name, f"Gate identity differs: {actual_name}")
            log = (gates / f"{actual_name}.log").read_bytes()
            require(receipt["exitCode"] == 0 and receipt["logSha256"] == sha(log)
                    and not receipt["memory"]["breach"], f"Gate {name} failed or changed")
            if name in ("manifest", "manifest-rebuild"):
                require(receipt["manifestSha256"] == manifest_sha, f"Gate {name} ran on another manifest")
            put(f"checks/{name}.txt", log)
            gate_receipts[name] = sha((gates / f"{actual_name}.json").read_bytes())
        titles = []
        kanji_files = sorted((k for k in files if k.startswith("repo/kanji/")), key=lambda k: ord(Path(k).stem))
        for relative in kanji_files:
            fm, _ = parse(files[relative].decode("utf-8").replace("\r\n", "\n"))
            titles.append(f"{Path(relative).stem} {fm['title']}")
        put("evidence/title-index.txt", ("\n".join(titles) + "\n").encode("utf-8"))
        metadata = []
        for char in members:
            relative = f"snapshot/kanji/{char}.md"
            fm, _ = parse(files[relative].decode("utf-8").replace("\r\n", "\n"))
            metadata.append({"card": char, "source": relative, "sha256": sha(files[relative]),
                             "distractors": fm["distractors"], "quiz_exclusions": fm["quiz_exclusions"]})
        reference = json_bytes({"newCards": members, "otherRequiredCards": [], "cards": metadata})
        put("eligibility-reference.json", reference)

        record = json.loads(frozen(review_dir(batch) / "snapshots" / "fetch-record.json"))
        require(record["candidate"] == candidate, "Snapshot capture belongs to another candidate")
        snapshots = []
        for result in record["results"]:
            entry = {k: result.get(k) for k in ("index", "citedUrl", "memberPage", "requestUrl",
                                                "fetchStartedUtc", "fetchCompletedUtc")}
            entry["citedBy"] = [{"card": c["card"], "line": c["line"], "cardSha256": c["cardSha256"]}
                                for c in result["citedBy"]]
            for cited in result["citedBy"]:
                require(sha(files[cited["card"]]) == cited["cardSha256"], "Cited card changed")
            i = result["index"]
            if result["outcome"] != "FETCHED":
                entry.update(status="FAILED", reason=result.get("error"), response=None, extract=None)
                snapshots.append(entry)
                continue
            raw = frozen(result["raw"]["path"], result["raw"]["sha256"])
            put(f"{SNAP}/{i:02d}-response.html", raw)
            entry.update(finalUrl=result["finalUrl"], httpStatus=result["status"],
                         contentType=result["headers"].get("Content-Type"),
                         response={"path": f"{SNAP}/{i:02d}-response.html", "sha256": sha(raw), "bytes": len(raw)})
            text, problem = extract_sections(raw, result["finalUrl"], sorted({PurePosixPath(item["card"]).stem for item in result["citedBy"]} | ({result["memberPage"]} if result.get("memberPage") else set())))
            if problem or result["status"] != 200:
                entry.update(status="AMBIGUOUS", reason=problem or f"HTTP status {result['status']}", extract=None)
            else:
                data = text.encode("utf-8")
                put(f"{SNAP}/{i:02d}-extract.txt", data)
                entry.update(status="SUPPLIED", extract={"path": f"{SNAP}/{i:02d}-extract.txt", "sha256": sha(data),
                                                         "bytes": len(data), "lines": text.count("\n")})
            snapshots.append(entry)
        put(f"{SNAP}/manifest.json", json_bytes({
            "snapshotSet": f"B{n} supplied external snapshots",
            "scope": record["scope"], "candidate": candidate, "extractionMethod": SECTION_METHOD, "snapshots": snapshots}))
        supplied = sum(s["status"] == "SUPPLIED" for s in snapshots)

        manifest = json.loads(manifest_data)
        words = len(modified)
        packet = {
            "batch": n, "candidate": candidate, "base": base, "newKanji": members, "newWords": [],
            "modifiedExisting": modified, "modifiedWords": modified, "supportingUnchanged": unchanged,
            "snapshotFiles": {p: changed[p] for p in runtime + modified},
            "sourceRows": selection["sourceRows"], "linkWrappers": wrappers,
            "wordProseChanges": config.get("wordProseChanges", []),
            "sourceKanjiArticles": kanji_count, "exportedWordArticles": words + len(unchanged),
            "completeDictionaryEntries": len(entries), "manifestContentVersion": manifest["contentVersion"],
            "manifestSha256": manifest_sha, "titleIndexLines": len(titles), "titleIndexFirst": titles[0],
            "titleIndexLast": titles[-1], "externalSnapshotsSupplied": supplied,
            "blinding": "No author design, adjudication, comparison notes, rejected candidates, reviewer findings, "
                        "probes, progress ledger, commit message or session history.",
            "publication": "Signed local review freeze only; not pushed or review-closed.",
        }
        put("packet.json", json_bytes(packet))
        support = (f" The unchanged {', '.join(Path(u).stem for u in unchanged)} article(s) are supporting evidence."
                   if unchanged else " No unchanged supporting word article is linked from the new cards.")
        prose_note = ("\nDeclared word prose changes (also assess their correctness): "
                      + json.dumps(config["wordProseChanges"], ensure_ascii=False) + "\n") \
            if config.get("wordProseChanges") else ""
        put("REVIEW.md", f"""# Independent B{n} review packet

Snapshot: {candidate}
Base: {base}

Review {word(len(members))} new kanji cards, their canonical stroke JSON, and {word(wrappers)} link
wrappers across {word(words)} existing word articles.{support} No word article or other
existing-kanji edit is added. Both independent reviewers receive the same snapshot,
rubric and source access, working serially.
{prose_note}
## Contract

Assess correctness, scoped coverage, consistency/quiz safety and comprehensibility
separately, using CLEAN, NEEDS FIX or UNVERIFIED with evidence, severity, confidence,
source-line citations and limits. CLEAN is bounded absence of an established defect,
not exhaustive correctness. There is no finding quota.

Read complete applicable dictionary families and actual comparison cards.
Preserve restrictions, sense-local flags and ordinary secondary meanings.
Exclusions are direct symmetric pairs, not transitive cliques. Shared topics
or different titles alone do not settle ambiguous English answers.
Separate metadata readings from quiz selections and mnemonic shapes from history.

The run-specific instruction file controls access, phases, fetch limits and
the sole report write. Its chain-only rules govern wider suggestions in the
copied repository guidance. No content edits, shell, agents, JVM/emulator,
device work, author rationale or progress-ledger access is permitted.

## Evidence and limits

snapshot has {word(2 * len(members) + words)} changed teaching/geometry files. repo/kanji has all
{kanji_count:,} same-commit cards. repo/words has the changed and supporting articles only,
not the complete word corpus. The neutral title index is mechanical extraction,
not a collision-candidate list.

{word(len(entries)).capitalize()} complete dictionary families retain their flags. Metadata and cached
Joyo rows are sourced evidence, not a fresh linguistic or PDF-glyph review.
evidence/external-snapshots holds raw cited-source responses fetched once at packet
build, with complete neutral source extracts ({supplied} supplied responses); a failed or
ambiguous page is recorded without any substitute. Each section keeps its source label;
different dictionaries are not one unified entry. Raw SVGs, raw responses and the
binary PDF are outside chain-only access and remain unread.

The ten supplied logs are host/static evidence, not native acceptance.
Reading exposure is an existing Python model of bounded pools, not arbitrary
custom pools, multiple borrowed cards, Kotlin or physical-phone acceptance.
Historical installed-APK references are not current device observations; compatibility is not claimed.
Local archive budgets are not an exact served GitHub ZIP check.

B{n} scoped lint covers its {word(len(members))} cards and {word(words)} words. No earlier
review verdict or exception is imported as evidence for B{n}.
""".encode("utf-8"))
        guard.check()
        for relative, data in files.items():
            write_frozen(out / Path(relative), data)
        sums = {k: sha(files[k]) for k in sorted(files)}
        written = write_frozen(out / "SHA256SUMS.json", json_bytes(sums))
        memory = guard.finish()
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise
    result = {"packet": str(out), "candidate": candidate, "base": base, "files": len(sums),
              "packetManifestSha256": written["sha256"], "members": members, "modifiedWords": modified,
              "supportingUnchanged": unchanged, "linkWrappers": wrappers, "snapshotsSupplied": supplied,
              "snapshotStatuses": [(s["index"], s["status"], s.get("reason")) for s in snapshots],
              "gateReceipts": gate_receipts, "gateSourceNames": config.get("gateNames", {}),
              "sourceContract": config.get("sourceContract"), "batchConfigSha256": config["configSha256"],
              "builder": {"path": str(TOOLS / "build-packet-b128-v2.py"), "sha256": sha((TOOLS / "build-packet-b128-v2.py").read_bytes()),
                          "extractorSha256": sha((TOOLS / "b128_external_sources.py").read_bytes())},
              "memory": memory}
    freeze_json(record_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
