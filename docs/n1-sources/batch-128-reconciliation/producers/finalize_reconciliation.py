import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from extract_reconciliation import CHARACTERS, QUERIES, HashReader, canonical
from recon_common import BASE, HERE, ORIGINAL, PACKET, PARENT, REPO, ROOT, SCRATCH, git, sha, start_guard, write


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
        verified = {}
        for label, tag, identifier in (("jmdict", "entry", "ent_seq"), ("kanjidic2", "character", "literal")):
            info = receipt["dictionaryInputs"][label]
            path = ROOT / "control" / "inputs" / info["filename"]
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    guard.check()
                    digest.update(chunk)
            assert digest.hexdigest() == info["compressedSha256"]
            raw = (PACKET / info["output"]).read_bytes()
            assert sha(raw) == info["outputSha256"]
            expected = {n.findtext(identifier): canonical(n) for n in ET.fromstring(raw).findall(tag)}
            applicable, equal = set(), set()
            with gzip.open(path, "rb") as stream:
                reader = HashReader(stream, guard)
                context = ET.iterparse(reader, events=("start", "end"))
                _, root = next(context)
                for event, node in context:
                    if event != "end" or node.tag != tag:
                        continue
                    key = node.findtext(identifier)
                    match = (bool(QUERIES & {k.text for k in node.findall("k_ele/keb")}) or "ほとり" in {r.text for r in node.findall("r_ele/reb")}) if label == "jmdict" else key in CHARACTERS
                    if match:
                        applicable.add(key)
                    if key in expected:
                        assert canonical(node) == expected[key], (label, key)
                        equal.add(key)
                    node.clear()
                    root.clear()
            assert reader.digest.hexdigest() == info["decompressedXmlSha256"]
            assert applicable == equal == expected.keys()
            verified[label] = {"completeRecords": len(expected), "allSelectorsAndCanonicalRecordsMatchOriginal": True,
                               "compressedSha256": digest.hexdigest(), "decompressedXmlSha256": reader.digest.hexdigest(),
                               "extractedSha256": sha(raw), "canonicalIdentities": sorted(equal)}
        local_admission = json.loads((SCRATCH / "reconciliation-admission-bindings.json").read_text(encoding="utf-8"))
        for value in local_admission["admissionBindings"].values():
            assert sha(Path(value["path"]).read_bytes()) == value["sha256"], value["path"]
        write(PACKET / "source-verification-002.json", verified)
        write(PACKET / "source-receipt-002.json", {
            "parentCommit": PARENT, "publishedBase": BASE,
            "originalReceipt": {"path": "source-receipt.json", "sha256": sha((PACKET / "source-receipt.json").read_bytes())},
            "selectorMembership": {"path": "selector-membership.json", "sha256": sha((PACKET / "selector-membership.json").read_bytes())},
            "verification": {"path": "source-verification-002.json", "sha256": sha((PACKET / "source-verification-002.json").read_bytes())},
            "admissionBindings": local_admission["admissionBindings"],
            "recordCounts": {k: v["completeRecords"] for k, v in verified.items()},
            "producerSha256": sha(Path(__file__).read_bytes()),
        })
        gates_path = SCRATCH / "reconciliation-author-gates-001" / "summary.json"
        gates = json.loads(gates_path.read_text(encoding="utf-8"))
        assert gates["status"] == "PASS" and gates["startingHead"] == PARENT
        manifest = json.loads((REPO / "manifest.json").read_bytes())
        assert sha((REPO / "manifest.json").read_bytes()) == gates["manifestSha256"]
        mapped = {p: v for group in manifest.values() if isinstance(group, dict) for p, v in group.items()}
        history = {}
        for item in git("ls-tree", "-r", "-z", PARENT, "--", "docs/n1-sources/batch-128", "docs/n1-sources/batch-128-progress.json").decode("utf-8").rstrip("\0").split("\0"):
            guard.check()
            meta, path = item.split("\t", 1)
            raw = (REPO / path).read_bytes()
            blob = meta.split()[2]
            assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == blob, path
            history[path] = {"gitBlob": blob, "rawSha256": sha(raw), "bytes": len(raw)}
        write(PACKET / "preserved-history.json", {"parentCommit": PARENT, "allRawBytesMatchParent": True, "files": history})
        for path in sorted(HERE.glob("*.py")):
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
            write(PACKET / "producers" / path.name, path.read_bytes())
        for path in sorted(gates_path.parent.iterdir()):
            if path.is_file():
                write(PACKET / "author-gates-001" / path.name, path.read_bytes())
        for path in sorted(SCRATCH.glob("reconciliation-*-memory-001.json")):
            write(PACKET / "execution-evidence" / path.name, path.read_bytes())
        write(PACKET / "author-evidence.json", {
            "parentCommit": PARENT, "publishedBase": BASE, "authorGates": {"directory": str(gates_path.parent), "summarySha256": sha(gates_path.read_bytes()), "checks": gates["checks"]},
            "manifestSha256": gates["manifestSha256"], "contentVersion": manifest["contentVersion"], "manifestMappedRuntimeEntries": len(mapped),
            "runtimeChangedFromParent": ["kanji/唇.md"], "supportWordAndGeometry": "Must remain raw-byte-identical to parent; separately checked by preservation producer.",
            "sourceVerification": "source-verification-002.json", "fullSelectors": "selector-membership.json",
            "preservedHistory": "preserved-history.json", "originalFilesHashInventoried": len(history),
            "scope": "One bounded B128 reconciliation; no new membership. Two isolated responses; neutral shared source/decision records.",
            "warnings": ["Zero final scoped lint/quiz warnings.", "Two latent hypothetical reading-pool collisions remain outside modeled shipped/restricted-Starter exposure.", "Variant 脣 fallback rendering is not tested; vocabulary remains pilot-stage."],
            "committedEvidence": "Recorded separately in scratch after signing, avoiding self-referential committed IDs.",
        })
        progress = json.loads((REPO / "docs" / "n1-sources" / "batch-128-progress.json").read_text(encoding="utf-8"))
        progress.update({
            "revision": "reconciliation-001", "parentCommit": PARENT, "baseCommit": BASE,
            "status": "local-unreviewed-reconciled-authoring-candidate",
            "supersedesWithoutOverwriting": "batch-128-progress.json",
            "sourceEvidence": "batch-128-reconciliation/source-receipt-002.json",
            "comparisonEvidence": ["batch-128/baseline-gloss-scan.json", "batch-128/baseline-gloss-scan-002.json", "batch-128-reconciliation/pair-dispositions.json"],
            "authorAudit": "batch-128-reconciliation/summary.md", "authorEvidence": "batch-128-reconciliation/author-evidence.json",
            "packetInventory": "batch-128-reconciliation/packet-files.json",
            "completeSourceVerification": "batch-128-reconciliation/source-verification-002.json",
            "runtimeCandidate": {"manifestSha256": gates["manifestSha256"], "contentVersion": manifest["contentVersion"], "manifestMappedRuntimeEntries": len(mapped)},
            "authorGates": {"status": "PASS", "summary": "batch-128-reconciliation/author-gates-001/summary.json", "summarySha256": sha(gates_path.read_bytes()), "committedChecks": "To be bound separately after signing; not claimed in advance."},
            "addedDirectGuards": ["咲", "刃", "郊"], "totalDirectGuards": 17,
        })
        assert progress["accounting"]["publishedPendingRecordsWithCards"] == 257 and progress["accounting"]["undelivered"] == 971
        write(REPO / "docs" / "n1-sources" / "batch-128-progress-reconciliation-001.json", progress)
        files = {p.relative_to(PACKET).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(PACKET.rglob("*")) if p.is_file()}
        write(PACKET / "packet-files.json", {"hashMode": "raw bytes; no normalization", "files": files, "excludes": ["packet-files.json"]})
        print(json.dumps({"records": {k: v["completeRecords"] for k, v in verified.items()}, "packetFiles": len(files) + 1,
                          "inventorySha256": sha((PACKET / "packet-files.json").read_bytes()), "manifestSha256": gates["manifestSha256"], "contentVersion": manifest["contentVersion"]}, ensure_ascii=False))
    finally:
        write(SCRATCH / "reconciliation-finalization-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
