"""Freeze complete, byte-bound sources for the original reviewers' confirmations."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from confirm_b134 import INITIALS, clean
from prepare_b134_reconciliation_captures import extract, extractor_type
from run_b134_closure_checks import CANDIDATE, HERE, ORDER, REPO
from verify_b134_payload import RUNNER
from verify_b134_sources import Git

ROOT = HERE / "review"
SOURCE = ROOT / "reconciliation-verification-001" / "verification.json"
SOURCE_SHA = "7ea9e7dde1989b5d1eb71bed3b5789ab77f4e3713277591b4841eeb2b0295da1"
GATES = ROOT / "reconciliation-gate-verification-001" / "verification.json"
GATES_SHA = "7b0e846ede88b4a5350df16b58df0c4461e4ba83fc0208f006d65c3951170787"
PREFIX = "docs/n1-sources/batch-134-reconciliation-001/"


def canonical_xml(raw, tag, key):
    root = ET.fromstring(raw)
    identities, lines = [], []
    for node in root:
        require(node.tag == tag and node.findtext(key), "Unexpected complete record")
        identities.append(node.findtext(key))
        lines.append(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True))
    require(len(identities) == len(set(identities)), "Duplicate complete record")
    result = (f"<{root.tag}>\n" + "\n".join(lines) + f"\n</{root.tag}>\n").encode("utf-8")
    require(ET.canonicalize(raw, strip_text=True) == ET.canonicalize(result, strip_text=True),
            "Lossless canonical presentation changed a source field")
    return result, identities


def main(revision):
    require(re.fullmatch(r"[0-9]{3}", revision), "Use a three-digit preserved preparation revision")
    OUT = ROOT / ("confirmation-dossier-" + revision)
    require(not OUT.exists(), "Preserve the previous confirmation dossier")
    proof = json.loads(frozen(SOURCE, SOURCE_SHA))
    gates = json.loads(frozen(GATES, GATES_SHA))
    candidate = proof["candidate"]
    require(proof["status"] == gates["status"] == "PASS" and gates["candidate"] == candidate,
            "Verification proofs differ")
    sources, capture_bindings, transformations = [], [], []
    guard, _ = start_guard("B134 complete confirmation dossier")
    try:
        git = Git(REPO, RUNNER, guard)
        clean(git, candidate, True)

        def signed(name):
            raw = git("show", f"{candidate}:{name}")
            require(raw == (REPO / name).read_bytes(), "Snapshot differs")
            return raw

        def add(name, raw):
            require(name not in {row["source"] for row in sources}, "Duplicate dossier source")
            if not raw.endswith(b"\n"):
                transformations.append({
                    "source": name, "originalSha256": sha(raw), "sha256": sha(raw + b"\n"),
                    "transformation": "One final LF added for chain framing; every original byte retained.",
                })
                raw += b"\n"
            ref = write_frozen(OUT / "sources" / name, raw)
            sources.append({"source": name, "path": ref["path"], "sha256": ref["sha256"]})

        def add_json(name, value):
            add(name, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

        for kind, filename, tag, key in (
                ("jmdict", "jmdict-complete-families.xml", "entry", "ent_seq"),
                ("kanjidic2", "kanjidic2-complete-characters.xml", "character", "literal")):
            original = signed(PREFIX + filename)
            raw, identities = canonical_xml(original, tag, key)
            name = "evidence/jmdict-families.xml" if kind == "jmdict" else "evidence/kanjidic2-records.xml"
            require(len(identities) == proof["sources"][kind]["records"], "Record count changed")
            add(name, raw)
            transformations.append({
                "source": name, "originalPath": PREFIX + filename, "originalSha256": sha(original),
                "sha256": sha(raw), "records": len(identities), "identities": identities,
                "transformation": "Complete canonical XML, one original record per line. All fields, "
                                  "attributes, restrictions and order retained; formatting only, no projection.",
            })
        for char, digest in proof["comparisons"].items():
            raw = signed(f"kanji/{char}.md")
            require(sha(raw) == digest, "Verified comparison changed")
            add(f"repo/kanji/{char}.md", raw)
        for name in ("receipt.json", "query-membership.json", "comparison-index.json"):
            add("evidence/reconciliation-" + name, signed(PREFIX + name))

        response_raw = signed(PREFIX + "dispositions.md")
        response = response_raw.decode("utf-8").replace("\r\n", "\n")
        marker = "The exact source selectors,"
        require(response.count(marker) == 1, "Author-response framing changed")
        intro, body = response.split(marker, 1)
        require("UNVERIFIED" in intro and "NEEDS FIX" in intro, "Unexpected response introduction")
        neutral = (
            "B134 author response: neutral confirmation presentation\n\n"
            f"Signed source: {PREFIX}dispositions.md\nCommit: {candidate}\n"
            f"Original SHA-256: {sha(response_raw)}\n"
            "Only the introductory paragraph naming the initial reviewers and their verdicts is "
            "omitted here to avoid conveying another reviewer's verdict. All technical response "
            "text below is retained, with CRLF normalized to LF. This is the author's proposal, "
            "not coordinator or reviewer acceptance.\n\n" + marker + body)
        add("evidence/author-response.txt", neutral.encode("utf-8"))
        transformations.append({
            "source": "evidence/author-response.txt", "originalSha256": sha(response_raw),
            "omittedPrefixSha256": sha(intro.encode("utf-8")),
            "technicalBodySha256": sha((marker + body).encode("utf-8")),
            "transformation": "Neutral introduction plus exact complete technical body; original signed file retained.",
        })

        for batch, char in ((134, "紫"), (129, "絹")):
            filename = "external-capture-bindings.json" if batch == 134 else "external-source-bindings.json"
            binding_path = f"docs/n1-sources/batch-{batch}/{filename}"
            bindings_raw = signed(binding_path)
            for row in json.loads(bindings_raw)["captures"]:
                if row["character"] != char or (char == "絹" and row["provider"] != "kotobank"):
                    continue
                html_path = Path(row["localRawCapture"])
                text_path = Path(row.get("localTextCapture", str(html_path.with_suffix(".txt"))))
                html, text = html_path.read_bytes(), text_path.read_bytes()
                require(sha(html) == row["rawSha256"] and len(html) == row["rawBytes"]
                        and sha(text) == row["textSha256"], "Pinned complete native capture changed")
                name = f"evidence/native-{char}-{row['provider']}-extract.txt"
                add(name, text)
                capture_bindings.append({**row, "source": name, "bindingPath": binding_path,
                    "bindingSha256": sha(bindings_raw),
                    "scope": "Complete previously captured text, not a new HTTP verification; images/layout omitted."})
        parser_type = extractor_type()
        kon_path = ROOT / "reconciliation-captures-001" / "index.json"
        kon = json.loads(frozen(kon_path, "18a06c432531ccf700d3042b75319c6e3ec4909edd51ce094477c5881a7337a0"))
        for row in kon["captures"]:
            html = Path(row["source"]["path"]).read_bytes()
            require(sha(html) == row["source"]["sha256"], "Kon capture changed")
            text, images = extract(html, parser_type)
            require(text == frozen(row["text"]["path"], row["text"]["sha256"])
                    and images == json.loads(frozen(row["images"]["path"], row["images"]["sha256"])),
                    "Kon complete extraction differs")
            stem = Path(row["source"]["path"]).stem
            name = f"evidence/native-{stem}-extract.txt"
            add(name, text)
            add("evidence/native-" + stem + "-images.json", frozen(row["images"]["path"]))
            capture_bindings.append({**row, "sourceName": name,
                                     "method": "Complete extraction independently reproduced from pinned HTML."})
        native = HERE / "reconciliation-external-001"
        seki_raw = (native / "隻-kotobank.receipt.json").read_bytes()
        seki = json.loads(seki_raw)
        html = (native / "隻-kotobank.html").read_bytes()
        text, images = extract(html, parser_type)
        require(sha(html) == seki["htmlSha256"] == "6b4caf6e6285cc68ba85485a3fd273a18c8498066106cef937ccaa5627c8bc11"
                and len(html) == seki["htmlBytes"] and seki["httpStatus"] == 200
                and text == (native / "隻-kotobank.txt").read_bytes()
                and sha(text) == seki["textSha256"] == "e44872afe1afcb0ab5f468d1bf2d85bd64f8954b630e753f29bec64f1295fbb5"
                and len(text.splitlines()) == seki["textLines"]
                and images == json.loads((native / "隻-kotobank.images.json").read_bytes())
                and len(images) == seki["imageCount"], "Seki complete native extraction differs")
        add("evidence/native-seki-extract.txt", text)
        add("evidence/native-seki-images.json", (native / "隻-kotobank.images.json").read_bytes())
        add("evidence/native-seki-receipt.json", seki_raw)
        capture_bindings.append({**seki, "source": "evidence/native-seki-extract.txt",
                                 "method": "Complete extraction independently reproduced from pinned HTML."})
        add_json("evidence/native-capture-provenance.json", capture_bindings)
        add_json("evidence/source-presentation.json", transformations)

        for name in ORDER:
            for suffix in ("json", "log"):
                key = "reconciliation-committed-001/" + name + "." + suffix
                ref = gates["evidence"][key]
                add("checks/" + name + "." + suffix, frozen(ref["path"], ref["sha256"]))
        add_json("evidence/coordinator-verification.json", {
            "candidate": candidate, "initialSnapshot": CANDIDATE,
            "sourceProof": {"path": str(SOURCE), "sha256": SOURCE_SHA},
            "gateProof": {"path": str(GATES), "sha256": GATES_SHA},
            "sources": proof["sources"], "predicates": proof["predicates"],
            "zeroMatches": proof["zeroMatches"], "originalRecordOverlap": proof["originalRecordOverlap"],
            "runtimeEntries": proof["runtimeEntries"], "unchangedRuntimeEntries": proof["unchangedRuntimeEntries"],
            "manifestSha256": proof["manifestSha256"], "contentVersion": proof["contentVersion"],
            "groups": gates["groups"], "logParsing": gates["logParsing"],
            "scope": "Mechanical verification only; source completeness does not adjudicate author claims.",
            "limits": [proof["limits"], gates["limits"], "Original candidate and aborted/stale runs remain retained.",
                       "Full KD records are supplied, not a field projection.",
                       "Only the complete Kotobank capture is selected for the new silk/cloth claim; "
                       "the separate Weblio silk capture is not supplied here or credited as reviewer reading."],
        })
        basis = (
            "Your initial report remains the original adjudicated evidence, not teaching approval. "
            "Reassess your own findings, optional points, consequential D/E uncertainties and limitations "
            "against the actual signed descendant. No other reviewer's report or verdict is supplied. "
            "The complete technical author response includes shared comparison work; its decisions are "
            "hypotheses, not required outcomes. C1 concerns the purple-tinged dark-blue attribution and "
            "qualified direct purple/navy precaution, not universal hue synonymy. C2 concerns removing "
            "the unsupported elapsed-time guard and independently assessing the retained historical "
            "noblewoman rationale for the hall/building card. The shared source request also covers all "
            "D1-D20 and the L3 classic/material/thread/fiber/cotton/wife comparisons; neither compound "
            "status nor a different short title by itself settles a pair. Self-contained learner wording "
            "was requested without dropping source qualifications. The invented non-etymological mnemonic "
            "and unclassified structure tag are unchanged. Historical ツツム remains unresolved; distinguish "
            "its meaning precaution from the latent reading collision. Do not equate any current guarded "
            "pair with unrestricted synonymy or infer historical negatives from the bounded selection. "
            "All 194 complete JMdict families, all 37 complete KD records, all 36 comparison articles, "
            "and complete selected native extracts are supplied. XML is canonicalized losslessly, not "
            "raw original slices. Confirm only if consequential claims are resolved; otherwise report "
            "the remaining defect or uncertainty. Host gates do not establish native/device, arbitrary "
            "pools, rendered fonts, whole-set or publication acceptance.")
        specs = {}
        for family in ("claude", "gpt"):
            spec = {
                "family": family, "run": f"N1-B134-{family.upper()}-CONFIRM-{revision}",
                "session": INITIALS[family]["session"], "candidate": candidate, "teachingChange": True,
                "scope": ["紫"], "revisedSources": ["kanji/紫.md"], "additionalSources": sources,
                "basis": "adjudicated-initial", "priorVerdict": INITIALS[family]["verdict"], "basisText": basis,
            }
            specs[family] = freeze_json(OUT / (family + "-spec.json"), spec)
        clean(git, candidate, True)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Dossier RAM breach")
    print(json.dumps(freeze_json(OUT / "dossier.json", {
        "status": "PREPARED_NOT_ADMITTED", "candidate": candidate, "specs": specs,
        "sources": sources, "sourceBytes": sum(Path(row["path"]).stat().st_size for row in sources),
        "sourceCount": len(sources), "transformations": transformations, "memory": memory,
        "producerSha256": sha(Path(__file__).read_bytes()),
    })))


if __name__ == "__main__":
    main(sys.argv[1])
