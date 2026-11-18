"""Build neutral B129 review inputs from the independently admitted signed tree."""
import copy
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, json_bytes, load_module, require, sha, start_guard, write_frozen
from source_query_union import selects
from verify_b129_payload import BASE, HERE, MEMBERS, PREFIX, REPO, RUNNER, LINK_HELPER, LINK_HELPER_SHA
from verify_b129_sources import Git, SCAN_HELPER, SCAN_SHA
from b129_source_schema import verify_scan

JOYO_SHA = "cc740aed34751e40831e4ab526408401667a428cefcf0fdd0212848eb31d67cb"
JOYO_ROWS = {
    "\u7d79": ("46", "\u7d79\n\u30b1\u30f3 \u7d79\u5e03\uff0c\u4eba\u7d79\n\u304d\u306c \u7d79\uff0c\u8584\u7d79"),
    "\u8679": ("121", "\u8679\n\u306b\u3058 \u8679"),
}


def query_index(records, selections):
    queries = sorted({query if selection["mode"] == "union" else "exact-keb:" + query
                      for selection in selections for query in selection["queries"]})
    require(all(selection["mode"] in {"union", "exact"} for selection in selections),
            "Unsupported neutral query mode")
    result = {query: sorted((identity for identity, node in records.items()
                            if selects(node, "entry", identity, "union", [query])), key=int)
              for query in queries}
    require({identity for identities in result.values() for identity in identities} == set(records),
            "Neutral query index omits a complete family")
    return result


def intermediate_rows(original):
    return [{"kanji": row["kanji"], "path": row["path"],
             "baselineGitBytesSha256": row["baselineBytesSha256"],
             "title": row["title"], "meanings": row["completeMeanings"]}
            for row in original["rows"]]


def main(source_path, source_sha, payload_path, payload_sha, evidence_path, evidence_sha):
    proofs = [json.loads(frozen(path, digest)) for path, digest in (
        (source_path, source_sha), (payload_path, payload_sha), (evidence_path, evidence_sha))]
    source_proof, payload, evidence = proofs
    candidate = source_proof["candidate"]
    require(all(proof["batch"] == 129 and proof["base"] == BASE
                and proof["candidate"] == candidate and proof["status"] == "PASS"
                and not proof["memory"]["breach"] for proof in proofs),
            "Proofs do not bind the same admitted candidate")
    require(payload["sourceProof"]["sha256"] == source_sha
            and evidence["sourceProof"]["sha256"] == source_sha
            and evidence["payloadProof"]["sha256"] == payload_sha
            and evidence["findings"] == [], "Candidate evidence remains unresolved")
    for name in ("batch.json", "source-contract", "source-contract.json",
                 "coordinator-candidate-verification.json"):
        require(not (HERE / name).exists(), f"Preserve existing review input: {name}")
    frozen(LINK_HELPER, LINK_HELPER_SHA)
    helper = load_module("b129_neutral_contract_helper", LINK_HELPER)
    frozen(SCAN_HELPER, SCAN_SHA)
    scan_helper = load_module("b129_intermediate_scan_helper", SCAN_HELPER)
    guard, _ = start_guard("B129 neutral source contract")
    git = Git(REPO, RUNNER, guard)
    signed, outputs = {}, {}

    def blob(name, revision=candidate):
        return git("show", f"{revision}:{name}")

    def source(name):
        raw = blob(PREFIX + name)
        signed[PREFIX + name] = sha(raw)
        return raw

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate changed during review preparation")

    try:
        clean()
        for name, digest in evidence["signedInputs"].items():
            require(sha(blob(name)) == digest, f"Admitted source changed: {name}")
            guard.check()
        tools = json.loads(source("tool-bindings.json"))
        require(tools["environment"]["N1_REPO"] == str(REPO), "Lean tools target another worktree")
        for name, digest in tools["leanTools"].items():
            require(Path(name).name == name and sha((WS / "lean" / name).read_bytes()) == digest,
                    f"Executed lean helper changed: {name}")
        jm = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]
                                   if record["input"] == "n1-implementation-JMdict_e.gz"], "entry", "ent_seq")
        kd = helper.merge_records([blob(record["path"]) for record in source_proof["sourceRecords"]
                                   if record["input"] == "n1-planning-kanjidic2.xml.gz"], "character", "literal")
        require(len(jm) == 252 and set(kd) == set(MEMBERS) | set(source_proof["packetComparisonCards"]),
                "Admitted source union changed")
        rows = json.loads(source("source-rows.json"))
        facts = json.loads(frozen(source_proof["facts"]["path"], source_proof["facts"]["sha256"]))
        scans = []
        for member, row in zip(payload["members"], rows):
            char = member["kanji"]
            require(char == row["kanji"], "Source-row order differs")
            original = json.loads(source(f"scans/{char}.json"))
            baseline = intermediate_rows(original)
            previous = original
            for directory in ("scans-003", "scans-004"):
                raw = source(f"{directory}/{char}.json")
                current = json.loads(raw)
                result = verify_scan(current, baseline, row["metadata"]["meanings"],
                                     member["metadata"]["title"], BASE, scan_helper, previous)
                scans.append({"kanji": char, "path": PREFIX + f"{directory}/{char}.json",
                              "sha256": sha(raw), **result})
                previous = current
        for filename, tag, records in (
            ("jmdict-families.xml", "JMdict", [jm[key] for key in sorted(jm, key=int)]),
            ("kanjidic2-records.xml", "kanjidic2",
             [kd[char] for char in MEMBERS] + [kd[key] for key in sorted(set(kd) - set(MEMBERS))]),
        ):
            root = ET.Element(tag)
            root.extend(copy.deepcopy(node) for node in records)
            outputs[filename] = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        outputs["selection.json"] = json_bytes({
            "order": MEMBERS, "sourceRows": [row["sourceRow"] for row in rows]})
        font = json.loads(source("stroke-font-evidence.json"))
        require(font["members"] == [
            {"kanji": entry["kanji"], "strokeCount": entry["strokeCount"],
             "strokeSha256": entry["strokeSha256"], "svgSha256": entry["svgSha256"],
             "kanjivgBlob": entry["svgGitBlob"]} for entry in payload["generatedGeometry"]],
            "Geometry evidence differs from reproduced payload")
        require(font["fonts"] == evidence["bundledFontEvidence"]
                and font["converterSha256"] == payload["converterSha256"],
                "Font or converter evidence changed")
        shapes = []
        for row, geometry in zip(rows, payload["generatedGeometry"]):
            char = row["kanji"]
            filename = f"{ord(char):05x}.svg"
            svg = source("kanjivg/" + filename)
            require(sha(svg) == geometry["svgSha256"], "SVG changed")
            outputs["kvg/" + filename] = svg
            shapes.append({
                "kanji": char, "revision": font["kanjivgRevision"],
                "gitBlobSha1": geometry["svgGitBlob"], "sha256": sha(svg),
                "sourcePath": "kanji/" + filename, "canonicalStrokes": geometry["strokeCount"],
                "groups": [dict(node.attrib) for node in ET.fromstring(svg).iter("{http://www.w3.org/2000/svg}g")],
                "bundledFonts": {"files": font["fonts"]},
                "scope": "Reproduced geometry and bounded font cmaps, not rendered/native/device acceptance.",
            })
        outputs["shape-evidence.json"] = json_bytes(shapes)
        joyo_raw = (WS / "scratch-111" / "joyo-pages.json").read_bytes()
        require(sha(joyo_raw) == JOYO_SHA, "Pinned Joyo cache changed")
        pages = json.loads(joyo_raw)
        joyo_rows = []
        for char in MEMBERS:
            matches = []
            if char in JOYO_ROWS:
                page, text = JOYO_ROWS[char]
                require(text in pages[page], f"Pinned Joyo text differs: {char}")
                matches.append({"printedPage": int(page), "extract": text})
            else:
                require(not any(char == line.strip() for text in pages.values() for line in text.splitlines()),
                        "Unexpected standalone member row in Joyo cache")
            joyo_rows.append({"kanji": char, "matches": matches})
        outputs["joyo-rows.json"] = json_bytes({
            "cacheSha256": JOYO_SHA, "rows": joyo_rows,
            "scope": "Pinned cached text, not fresh PDF glyph inspection. An empty exact-row match "
                     "is a cache observation, not evidence that a reading or usage is invalid.",
        })
        outputs["evidence-index.json"] = json_bytes({
            "outputs": {name: sha(raw) for name, raw in outputs.items()},
            "completeDictionaryEntries": len(jm),
            "dictionaryQueryEntries": query_index(jm, facts["jmdictSelections"]),
        })
        pending = {row["kanji"] for row in json.loads(blob("docs/n1-sources/source-index.json"))
                   if row["statusAtFreeze"] == "pending"}
        represented = lambda revision: {
            Path(name).stem for name in json.loads(blob("manifest.json", revision))["files"]
            if name.startswith("kanji/")}
        before, after = represented(BASE), represented(candidate)
        require(len(pending) == 1228 and len(pending & before) == 258
                and len(pending & after) == 261 and after - before == set(MEMBERS)
                and len(after) == 1251, "Source membership accounting differs")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Review-contract RAM breach")
    outputs_written = {name: write_frozen(HERE / "source-contract" / name, raw)
                       for name, raw in outputs.items()}
    contract = freeze_json(HERE / "source-contract.json", {
        "batch": 129, "candidate": candidate, "base": BASE, "files": outputs_written,
        "signedSources": signed,
        "method": "Complete signed records independently re-streamed from pinned original inputs. "
                  "Duplicate identities merged only after structural equality; parsed/reserialized XML, "
                  "not raw source slices. All declared predicates retained, including zero-match queries. "
                  "Neutral outputs exclude author judgments.",
        "dictionaryVerification": {"path": source_path, "sha256": source_sha},
        "tool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
    })
    config = freeze_json(HERE / "batch.json", {
        "batch": 129, "candidate": candidate, "base": BASE, "members": MEMBERS,
        "repo": str(REPO), "expectedKanji": 1251,
        "gates": str(Path(evidence_path).parent / "committed"),
        "sourceContract": {"path": contract["path"], "sha256": contract["sha256"]},
    })
    print(json.dumps(freeze_json(HERE / "coordinator-candidate-verification.json", {
        "batch": 129, "candidate": candidate, "base": BASE, "status": "PASS",
        "sourceProof": {"path": source_path, "sha256": source_sha},
        "payloadProof": {"path": payload_path, "sha256": payload_sha},
        "evidenceProof": {"path": evidence_path, "sha256": evidence_sha},
        "sourceContract": contract, "batchConfig": config, "intermediateScans": scans,
        "leanToolBindings": tools["leanTools"], "manifestSha256": payload["manifestSha256"],
        "contentVersion": payload["contentVersion"], "sourceMembersPublishedBeforeBatch": 258,
        "sourceMembersInCandidate": 261, "gates": evidence["gates"], "memory": memory,
        "limits": "Mechanical candidate admission, not independent linguistic review or publication.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 7, "Usage: prepare_b129_review_contract.py SOURCE SHA PAYLOAD SHA EVIDENCE SHA")
    main(*sys.argv[1:])
