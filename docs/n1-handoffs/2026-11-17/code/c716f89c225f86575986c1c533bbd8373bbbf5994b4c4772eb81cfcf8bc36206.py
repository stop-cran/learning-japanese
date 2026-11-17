"""Rebuild blind B134 review inputs from the signed reconciliation and original packet."""
import difflib
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
OLD = ROOT / "neutral-preparation-001" / "projected-successor-001"
PACKET_SRC = OLD / "packet"
RECON_PROOF = ROOT / "reconciliation-verification-001" / "verification.json"
GATE_PROOF = ROOT / "reconciliation-gate-verification-001" / "verification.json"
DOSSIER = ROOT / "confirmation-dossier-002"
RECON_DIR = "docs/n1-sources/batch-134-reconciliation-001"
REPO = WS / "b134-worktree"
BASE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
CANDIDATE = "355cccb840d22e7313e79f234eb93d1367e00352"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
OWNER = "stop-cran@list.ru"
OUT = ROOT / "fresh-independent-002"
FULL = OUT / "complete-record-trial-004"
FINAL = OUT / "projected-successor-004"
EXPECTED = {
    RECON_PROOF: "7ea9e7dde1989b5d1eb71bed3b5789ab77f4e3713277591b4841eeb2b0295da1",
    GATE_PROOF: "7b0e846ede88b4a5350df16b58df0c4461e4ba83fc0208f006d65c3951170787",
    DOSSIER / "dossier.json": "ef4e5a31469233ef10db7a86a555f8ae65e428d32e1b87991c0672d1d09013a9",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    result = subprocess.run(["git", "-C", str(REPO), *args], check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout


def blob(rev, path):
    return git("show", f"{rev}:{path}")


def canon(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def read_lines(path):
    raw = path.read_bytes()
    root = ET.fromstring(raw)
    lines = raw.splitlines(keepends=True)
    require(len(lines) == len(root) + 2 and lines[0].strip().startswith(b"<")
            and lines[-1].strip().startswith(b"</"), f"Unexpected XML line framing: {path}")
    return root, lines[1:-1]


def merge_xml(left_raw, right_raw, tag, record_tag, identity):
    left = ET.fromstring(left_raw)
    right = ET.fromstring(right_raw)
    require(left.tag == right.tag == tag, f"Unexpected {tag} root")
    left_lines = [canon(node).encode("utf-8") + b"\n" for node in left]
    right_lines = [canon(node).encode("utf-8") + b"\n" for node in right]
    require(len(left_lines) == len(left) and len(right_lines) == len(right), "Record framing mismatch")
    selected, records, conflicts, overlap = [], {}, [], []
    for origin, root, lines in (("original", left, left_lines), ("supplemental", right, right_lines)):
        for node, raw in zip(root, lines):
            key = node.findtext(identity)
            require(node.tag == record_tag and key and raw.endswith(b"\n"), "Invalid source record")
            canonical = canon(node)
            if key in records:
                require(records[key][0] == canonical, f"Canonical-equality conflict: {key}")
                overlap.append(key)
                continue
            records[key] = (canonical, origin)
            selected.append(raw)
    out = f"<{tag}>\n".encode() + b"".join(selected) + f"</{tag}>\n".encode()
    require(len(ET.fromstring(out)) == len(records), "Merged union framing failed")
    return out, {"originalRecords": len(left), "supplementalRecords": len(right),
                 "canonicalEqualOverlap": len(overlap), "uniqueRecords": len(records),
                 "overlapIdentities": sorted(overlap, key=str), "sha256": sha(out)}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def copy_packet():
    require(not FULL.exists() and not FINAL.exists(), "fresh-independent-002 outputs already exist; preserve and stop")
    for path, digest in EXPECTED.items():
        raw = path.read_bytes()
        require(sha(raw) == digest, f"Proof hash mismatch: {path}")
    proof = json.loads(RECON_PROOF.read_text(encoding="utf-8"))
    gate = json.loads(GATE_PROOF.read_text(encoding="utf-8"))
    require(proof["status"] == gate["status"] == "PASS"
            and proof["candidate"] == gate["candidate"] == CANDIDATE
            and proof["initialSnapshot"] == BASE, "Signed proof lineage mismatch")
    status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
    identity = git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
    require(not status and identity == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}",
            "Candidate is not the clean signed child")
    OUT.mkdir(parents=True, exist_ok=True)
    FULL.mkdir()
    shutil.copytree(PACKET_SRC, FULL / "packet")
    for path in (FULL / "packet").rglob("*"):
        if path.is_file():
            path.chmod(0o666)
    return identity


def build():
    identity = copy_packet()
    packet = FULL / "packet"
    recon = json.loads(RECON_PROOF.read_text(encoding="utf-8"))
    gateproof = json.loads(GATE_PROOF.read_text(encoding="utf-8"))
    dossier = json.loads((DOSSIER / "dossier.json").read_text(encoding="utf-8"))
    original_manifest = json.loads((packet / "repo" / "manifest.json").read_text(encoding="utf-8"))

    # Bind the actual signed target and its parent without exposing author response material.
    card_path = "kanji/紫.md"
    old_card = blob(BASE, card_path)
    new_card = blob(CANDIDATE, card_path)
    old_support = blob(BASE, "words/紫.md")
    new_support = blob(CANDIDATE, "words/紫.md")
    require(new_support == old_support, "Support article identity/content unexpectedly changed")
    write(packet / "baseline" / "kanji" / "紫.md", old_card)
    write(packet / "baseline" / "words" / "紫.md", old_support)
    write(packet / "snapshot" / "kanji" / "紫.md", new_card)
    write(packet / "snapshot" / "words" / "紫.md", new_support)
    write(packet / "repo" / card_path, new_card)
    candidate_manifest = blob(CANDIDATE, "manifest.json")
    base_manifest = blob(BASE, "manifest.json")
    write(packet / "repo" / "manifest.json", candidate_manifest)
    write(packet / "baseline" / "manifest.json", base_manifest)
    card_diff = "".join(difflib.unified_diff(
        old_card.decode("utf-8").splitlines(keepends=True),
        new_card.decode("utf-8").splitlines(keepends=True),
        fromfile=f"{BASE}:{card_path}", tofile=f"{CANDIDATE}:{card_path}"))
    write(packet / "diffs" / "reconciliation-card.diff", card_diff.encode("utf-8"))
    binding = {
        "status": "SIGNED_RECONCILIATION_CONTENT_BINDING_NOT_SEMANTIC_ACCEPTANCE",
        "base": BASE, "candidate": CANDIDATE, "cardPath": card_path,
        "baseCardSha256": sha(old_card), "candidateCardSha256": sha(new_card),
        "baseManifestSha256": sha(base_manifest), "candidateManifestSha256": sha(candidate_manifest),
        "candidateManifestContentVersion": json.loads(candidate_manifest)["contentVersion"],
        "supportPath": "words/紫.md", "baseSupportSha256": sha(old_support),
        "candidateSupportSha256": sha(new_support), "supportUnchanged": True,
        "exactCardDiffSha256": sha(card_diff.encode("utf-8")),
        "candidateSignature": identity,
    }
    write(packet / "evidence" / "signed-reconciliation-binding.json",
          (json.dumps(binding, ensure_ascii=False, indent=2) + "\n").encode())
    frontmatter = new_card.decode("utf-8").split("---", 2)[1]
    exclusion_line = next(line for line in frontmatter.splitlines()
                          if line.startswith("quiz_exclusions:"))
    exclusion_value = exclusion_line.split(":", 1)[1].strip()
    exclusions = [item.strip() for item in exclusion_value.strip("[]").split(",") if item.strip()]
    write(packet / "eligibility-reference.json", (
        json.dumps({"newCards": ["紫"], "otherRequiredCards": [], "cards": [{
            "distractors": ["古", "右", "川"],
            "quiz_exclusions": exclusions
        }]}, ensure_ascii=False, indent=2) + "\n").encode())

    # Merge complete record unions, rejecting any overlap that is not full canonical equality.
    original_jm = (packet / "evidence" / "jmdict-families.xml").read_bytes()
    original_kd = (packet / "evidence" / "kanjidic2-records.xml").read_bytes()
    supp_jm = blob(CANDIDATE, f"{RECON_DIR}/jmdict-complete-families.xml")
    supp_kd = blob(CANDIDATE, f"{RECON_DIR}/kanjidic2-complete-characters.xml")
    merged_jm, jm_stats = merge_xml(original_jm, supp_jm, "JMdict", "entry", "ent_seq")
    merged_kd, kd_stats = merge_xml(original_kd, supp_kd, "kanjidic2", "character", "literal")
    write(packet / "evidence" / "jmdict-original-union-399.xml", original_jm)
    write(packet / "evidence" / "jmdict-supplemental-194.xml", supp_jm)
    write(packet / "evidence" / "jmdict-families.xml", merged_jm)
    write(packet / "evidence" / "kanjidic2-original-union-59.xml", original_kd)
    write(packet / "evidence" / "kanjidic2-supplemental-37.xml", supp_kd)
    write(packet / "evidence" / "kanjidic2-complete-union.xml", merged_kd)
    write(packet / "evidence" / "kanjidic2-records.xml", merged_kd)

    # Keep both exact selection sources; the neutral derivative deliberately excludes recommendations.
    source_provenance = (packet / "evidence" / "source-selection-provenance.json").read_bytes()
    supp_receipt = json.loads(blob(CANDIDATE, f"{RECON_DIR}/receipt.json"))
    supp_membership = json.loads(blob(CANDIDATE, f"{RECON_DIR}/query-membership.json"))
    neutral_receipt = {k: v for k, v in supp_receipt.items()
                       if k not in {"comparisonCharacters", "outputs", "producerSha256"}}
    neutral_receipt["reviewCandidate"] = CANDIDATE
    neutral_receipt["sourceSnapshot"] = BASE
    neutral_receipt["excludedFields"] = [
        "comparisonCharacters", "outputs", "producerSha256",
        "dispositions and author-response content",
    ]
    write(packet / "evidence" / "reconciliation-query-receipt-neutral.json",
          (json.dumps(neutral_receipt, ensure_ascii=False, indent=2) + "\n").encode())
    write(packet / "evidence" / "reconciliation-query-membership.json",
          (json.dumps(supp_membership, ensure_ascii=False, indent=2) + "\n").encode())
    write(packet / "evidence" / "source-selection-provenance-original.json", source_provenance)
    merged_provenance = {
        "status": "COMPLETE_SELECTION_PROVENANCE_DERIVATIVE_NOT_REVIEW_INSTRUCTION",
        "reviewCandidate": CANDIDATE, "originalSelections": json.loads(source_provenance),
        "supplementalReceipt": "evidence/reconciliation-query-receipt-neutral.json",
        "supplementalMembership": "evidence/reconciliation-query-membership.json",
        "supplementalSourceSnapshot": BASE,
        "originalPredicateCount": 182, "supplementalPredicateCount": 140,
        "originalZeroMatchPredicates": json.loads(source_provenance)["zeroMatchQueries"],
        "supplementalZeroMatchPredicates": [
            key for key, count in neutral_receipt["countsIncludingZero"].items() if count == 0
        ],
        "completeRecordUnions": {"jmdict": jm_stats, "kanjidic2": kd_stats},
        "notIncluded": ["author response", "reports/verdicts", "report-derived assertions",
                        "pair dispositions/reasons", "scan matches", "comparison recommendation list"],
        "limits": "Exact search selection provenance only; historical search source snapshot is parent, not an instruction to select comparisons.",
    }
    write(packet / "evidence" / "source-selection-provenance-merged.json",
          (json.dumps(merged_provenance, ensure_ascii=False, indent=2) + "\n").encode())

    # Bind the complete native captures and final committed host gate evidence; never copy author response.
    source_map = {row["source"]: row for row in dossier["sources"]}
    omitted = {"evidence/author-response.txt", "evidence/reconciliation-comparison-index.json"}
    copied = []
    for source, row in source_map.items():
        if source in omitted:
            continue
        if source.startswith("evidence/native-") or source.startswith("checks/"):
            raw = (DOSSIER / "sources" / source).read_bytes()
            require(sha(raw) == row["sha256"], "Dossier source hash mismatch: " + source)
            target = packet / "reconciliation" / source
            write(target, raw)
            copied.append({"source": source, "packetPath": target.relative_to(packet).as_posix(),
                           "sha256": sha(raw), "bytes": len(raw)})
    require(len([x for x in copied if x["source"].startswith("evidence/native-")]) >= 10,
            "Complete native capture set missing")
    require(len([x for x in copied if x["source"].startswith("checks/")]) == 20,
            "Final committed ten host gates incomplete")
    write(packet / "evidence" / "supplemental-capture-and-gate-inventory.json",
          (json.dumps({"sourceDossierSha256": EXPECTED[DOSSIER / "dossier.json"],
                       "copied": copied,
                       "omitted": sorted(omitted),
                       "limits": "Native capture bytes and signed committed gate receipts/logs only; no author response, report, verdict or semantic conclusion."},
                      ensure_ascii=False, indent=2) + "\n").encode())

    # Preserve the coordinator's signed source proofs as integrity bindings only.
    proofs = {
        "reconciliationVerification": {"path": str(RECON_PROOF), "sha256": EXPECTED[RECON_PROOF]},
        "reconciliationGateVerification": {"path": str(GATE_PROOF), "sha256": EXPECTED[GATE_PROOF]},
        "confirmationDossier": {"path": str(DOSSIER / "dossier.json"),
                                "sha256": EXPECTED[DOSSIER / "dossier.json"]},
    }
    write(packet / "evidence" / "source-proof-bindings.json",
          (json.dumps({"candidate": CANDIDATE, "base": BASE, "proofs": proofs,
                       "limits": "Integrity bindings only; do not treat confirmation material as a blind review packet."},
                      indent=2) + "\n").encode())

    # Generate complete full-record KD units before deciding whether to project.
    kd_root = ET.fromstring(merged_kd)
    kd_lines = merged_kd.splitlines(keepends=True)[1:-1]
    require(len(kd_root) == len(kd_lines) == kd_stats["uniqueRecords"], "KD union framing")
    units = []
    for node, raw in zip(kd_root, kd_lines):
        literal = node.findtext("literal")
        dest = packet / "evidence" / "kanjidic2-full-records" / f"{literal}.xml"
        write(dest, raw)
        units.append({"literal": literal, "path": dest.relative_to(packet).as_posix(),
                      "sha256": sha(raw), "bytes": len(raw)})
    write(packet / "evidence" / "kanjidic2-full-unit-index.json",
          (json.dumps({"records": units, "count": len(units)}, ensure_ascii=False, indent=2) + "\n").encode())

    # Freeze full record trial inventory and write its exact source list.
    original_core = json.loads((OLD / "core-chain-001.json").read_text(encoding="utf-8"))
    core_names = [r["source"] for r in original_core["sources"]]
    core_names[core_names.index("evidence/jmdict-families.xml")] = "evidence/jmdict-families.xml"
    core_names[core_names.index("evidence/kanjidic2-review-projection.xml")] = "evidence/kanjidic2-records.xml"
    for name in [
        "diffs/reconciliation-card.diff", "evidence/signed-reconciliation-binding.json",
        "evidence/source-selection-provenance-merged.json",
        "evidence/reconciliation-query-receipt-neutral.json",
        "evidence/reconciliation-query-membership.json",
        "evidence/supplemental-capture-and-gate-inventory.json",
        "evidence/source-proof-bindings.json",
        "evidence/kanjidic2-full-unit-index.json",
    ]:
        core_names.append(name)
    for row in copied:
        core_names.append("reconciliation/" + row["source"])
    for char in "古右川":
        name = f"repo/kanji/{char}.md"
        if name not in core_names:
            core_names.append(name)
    # Include the parent and signed target support snapshots and signed target article.
    for name in ("baseline/kanji/紫.md", "baseline/words/紫.md",
                 "snapshot/kanji/紫.md", "snapshot/words/紫.md"):
        if name not in core_names:
            core_names.append(name)
    full_files = {p.relative_to(packet).as_posix(): p.read_bytes()
                  for p in packet.rglob("*") if p.is_file()}
    require(all(name in full_files for name in core_names), "Required full-core source absent")
    write(FULL / "core-sources-001.json",
          (json.dumps({"candidate": CANDIDATE, "base": BASE, "sources": core_names},
                      ensure_ascii=False, indent=2) + "\n").encode())
    write(FULL / "complete-record-summary-001.json",
          (json.dumps({"status": "COMPLETE_RECORD_INPUTS_BUILT_BEFORE_PROJECTION",
                       "jmDict": jm_stats, "kanjidic2": kd_stats,
                       "coreSources": len(core_names), "packetFiles": len(full_files),
                       "candidate": CANDIDATE, "base": BASE,
                       "proofHashes": {str(k): v for k, v in EXPECTED.items()},
                       "excludedDossierMaterial": sorted(omitted),
                       "limits": "No semantic review; no reviewer launched."},
                      ensure_ascii=False, indent=2) + "\n").encode())
    sums = {p.relative_to(packet).as_posix(): sha(p.read_bytes())
            for p in sorted(packet.rglob("*")) if p.is_file() and p.name != "SHA256SUMS.json"}
    write(packet / "SHA256SUMS.json", (json.dumps(sums, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"fullRoot": str(FULL), "records": {"JMdict": jm_stats, "KANJIDIC2": kd_stats},
                      "coreSources": len(core_names), "packetFiles": len(full_files),
                      "supplementalCapturesAndGates": len(copied)}, ensure_ascii=False))


if __name__ == "__main__":
    build()
