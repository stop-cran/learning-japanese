"""Preserve a context-held review and prepare lossless, blind replacement inputs."""
import json
from pathlib import Path

from b129_confirmation_presentation import canonical, compact_xml
from common import TOOLS, WS, freeze_json, frozen, load_batch, require, sha, start_guard, verify_packet, write_frozen
from prepare_b130_review_tools import derive

ROOT = WS / "scratch-130" / "review"
PACKET_SHA = "b0abe56caa9aff451c87cfc568ffb76bc5141d4d423dc49b069525055426799b"
PREFLIGHT_SHA = "bea713663a932619be79f3d5b2a904fad6793db7c4da48ee91c551224755fc2d"
RUN = "N1-B130-CLAUDE-001"


def bound(path):
    raw = frozen(path)
    return {"path": str(path), "sha256": sha(raw)}


def main():
    preflight = json.loads(frozen(ROOT / "prompts" / "preflight.json", PREFLIGHT_SHA))
    audit_config = json.loads(frozen(preflight["runs"]["claude"]["auditConfig"]))
    pins = {row["path"]: row["sha256"] for row in audit_config["files"]}
    sources = (
        "common.py", "step_b127.py", "prepare-chain.py", "build-prompts-b128-v2.py",
        "b129_confirmation_presentation.py", "prepare_b130_review_tools.py",
    )
    for name in sources:
        frozen(TOOLS / name, pins[str(TOOLS / name)])
    final_path = ROOT / f"{RUN}-final.json"
    final = json.loads(frozen(final_path))
    context = json.loads(frozen(final["context"]["path"], final["context"]["sha256"]))
    structure = json.loads(frozen(final["structure"]["path"], final["structure"]["sha256"]))
    require(final["status"] == "HOLD" and context["status"] == "FAIL" and context["compactions"]
            and structure["status"] == "PASS" and final["evidenceCheck"] is None,
            "Expected the actual context-compacted, unaccepted initial review")
    require(not (ROOT / f"{RUN}-acceptance.json").exists(), "Held review was accepted")
    report = Path(preflight["runs"]["claude"]["report"])
    hold = freeze_json(ROOT / f"{RUN}-hold.json", {
        "batch": 130, "run": RUN, "session": final["session"], "candidate": final["candidate"],
        "status": "HOLD_CONTEXT_COMPACTED", "rawVerdict": structure["overall"],
        "reviewAccepted": False, "finalAcceptance": False,
        "final": bound(final_path), "report": bound(report),
        "context": final["context"], "structure": final["structure"], "finalAudit": final["finalAudit"],
        "reason": "The final context audit found an actual compaction at 766999/952000 tokens. "
                  "Complete read counts and a well-formed report do not override this failure.",
        "quarantine": "Preserve raw execution, report, lists and chains. No findings or comparisons "
                      "from this run may be fed to authors or replacement reviewers, or counted as "
                      "accepted review evidence. GPT001 was not launched.",
    })
    failed = ROOT / "claude-final-execution-001"
    receipt = json.loads((failed / "receipt.json").read_bytes())
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 1
            and receipt["logSha256"] == sha((failed / "output.log").read_bytes())
            and not receipt["cleanupError"] and not receipt["memory"]["breach"],
            "Failed execution receipt differs")
    for name in ("receipt.json", "output.log"):
        (failed / name).chmod(0o444)

    guard, _ = start_guard("B130 lossless replacement preparation")
    try:
        config = load_batch(130)
        original, sums, digest = verify_packet(config, guard)
        require(digest == PACKET_SHA and config["candidate"] == final["candidate"], "Original packet differs")
        target = original.with_name(original.name + "-compact-001")
        require(not target.exists(), "Preserve existing replacement packet")
        replacements, records = {}, {}
        for name, count, tag in (
            ("kanjidic2-records.xml", 192, "character"),
            ("jmdict-families.xml", 519, "entry"),
        ):
            relative = "evidence/" + name
            raw = frozen(original / relative, sums[relative])
            compact = compact_xml(raw)
            require(canonical(compact) == canonical(raw)
                    and compact.count(("<" + tag + ">").encode()) == count,
                    "Complete dictionary records changed")
            require(max(map(len, compact.splitlines())) < 13900, "Record exceeds chain budget")
            replacements[relative] = compact
            records[relative] = {
                "original": {"path": str(original / relative), "sha256": sha(raw), "bytes": len(raw)},
                "presentedSha256": sha(compact), "presentedBytes": len(compact),
                "originalLines": len(raw.splitlines()), "presentedLines": len(compact.splitlines()),
                "records": count, "canonicalSha256": sha(canonical(raw).encode("utf-8")),
                "canonicalEqual": True,
            }
        disclosure = {
            "representation": "Complete XML records with indentation removed and one record per line.",
            "method": "ElementTree canonicalization with strip_text=True; complete ordered elements, "
                      "attributes, languages, readings, meanings, restrictions and secondary senses "
                      "are retained. Canonical before/after XML is identical. No source projection "
                      "or semantic selection, and no new web fetch.",
            "sourcePacketManifestSha256": PACKET_SHA, "files": records,
            "limits": "Line numbers and byte hashes refer to this presentation, not original serialization. "
                      "Original source files remain immutable at the disclosed paths. Compact formatting "
                      "is not evidence of comprehension or freedom from future context compaction.",
        }
        from common import json_bytes
        replacements["evidence/xml-presentation.json"] = json_bytes(disclosure)
        packet = json.loads(frozen(original / "packet.json", sums["packet.json"]))
        packet["dictionaryPresentation"] = "evidence/xml-presentation.json"
        replacements["packet.json"] = json_bytes(packet)
        new_sums = {}
        for relative in sorted(set(sums) | set(replacements)):
            raw = replacements[relative] if relative in replacements else frozen(original / relative, sums[relative])
            write_frozen(target / relative, raw)
            new_sums[relative] = sha(raw)
            guard.check()
        manifest = freeze_json(target / "SHA256SUMS.json", new_sums)
        unchanged = [name for name in sums if name not in replacements]
        require(all(new_sums[name] == sums[name] for name in unchanged), "Unrelated packet bytes changed")
        packet_proof = freeze_json(ROOT / "compact-review-packet-preflight-001.json", {
            "batch": 130, "candidate": config["candidate"], "status": "PASS_PRESENTATION_ONLY",
            "sourcePacket": str(original), "sourcePacketManifestSha256": PACKET_SHA,
            "packet": str(target), "packetManifest": manifest,
            "sameByteFiles": len(unchanged), "changedFiles": sorted(set(sums) & set(replacements)),
            "addedFiles": sorted(set(replacements) - set(sums)), "dictionaries": records,
            "heldReview": hold,
            "blindness": "No author judgments, held findings, prior selected D/E list or prior verdict "
                         "are in the replacement packet. Both fresh families get the same complete "
                         "source presentation and choose their own comparisons.",
        })
    finally:
        require(not guard.finish()["breach"], "Replacement preparation RAM breach")

    common = derive("common.py", "b130_compact_common.py", [
        ('    return WS / "review-packets" / f"batch-{config[\'batch\']}-{config[\'candidate\'][:8]}"',
         '    require(config["batch"] == 130, "Compact packet adapter is limited to B130")\n'
         '    return WS / "review-packets" / f"batch-{config[\'batch\']}-{config[\'candidate\'][:8]}-compact-001"'),
    ])
    chain = derive("prepare-chain.py", "prepare-chain-b130-compact.py", [
        ("from common import", "from b130_compact_common import"),
        ('            for name in ("source-metadata.json",',
         '            add("evidence/xml-presentation.json")\n'
         '            for name in ("source-metadata.json",'),
        ('f"b{n}-initial-v1"', 'f"b{n}-initial-compact-001"'),
        ('"core-chain.json"', '"core-chain-compact-001.json"'),
        ('"core-chain-preflight.json"', '"core-chain-compact-001-preflight.json"'),
        ('"prepare-chain.py"', '"prepare-chain-b130-compact.py"'),
    ])
    lifecycle = derive("step_b127.py", "step_b130_compact.py", [
        ("from common import", "from b130_compact_common import"),
        ("step_b127.py", "step_b130_compact.py"),
        ('"prepare-chain.py"', '"prepare-chain-b130-compact.py"'),
        ('"preflight.json"', '"preflight-compact-001.json"'),
    ])
    prompts = derive("build-prompts-b128-v2.py", "build-prompts-b130-compact.py", [
        ("from common import", "from b130_compact_common import"),
        ("build-prompts-b128-v2.py", "build-prompts-b130-compact.py"),
        ('require(not prompts.exists(), "Prompts already built; preserve them")',
         'require(not (prompts / "preflight-compact-001.json").exists(), "Preserve replacement prompts")'),
        ('"core-chain.json"', '"core-chain-compact-001.json"'),
        ('"core-chain-preflight.json"', '"core-chain-compact-001-preflight.json"'),
        ('"batch.json", "packet-build.json",',
         '"batch.json", "packet-build.json", "compact-review-packet-preflight-001.json",'),
        ('f"N1-B{n}-{label}-001"', 'f"N1-B{n}-{label}-002"'),
        ('f"initial-{key}-001.txt"', 'f"initial-{key}-002.txt"'),
        ('f"kickoff-{key}-001.txt"', 'f"kickoff-{key}-002.txt"'),
        ('f"initial-{key}-001.md"', 'f"initial-{key}-002.md"'),
        ('f"B{n} {name} review 001"', 'f"B{n} {name} review 002"'),
        ('"initial-claude-001.txt"', '"initial-claude-002.txt"'),
        ('"initial-gpt-001.txt"', '"initial-gpt-002.txt"'),
        ('require(not any(reports.iterdir()), "Report directory is not empty")',
         'require(all(not Path(s["report"]).exists() for s in runs.values()), "Preserve existing reports")'),
        ('"template.txt"', '"template-compact-001.txt"'),
        ('"preflight.json"', '"preflight-compact-001.json"'),
    ])
    print(freeze_json(ROOT / "compact-review-tooling-derivation-001.json", {
        "batch": 130, "status": "PREPARATION_ONLY", "packetProof": packet_proof,
        "producer": bound(Path(__file__)), "derivations": [common, chain, lifecycle, prompts],
        "limits": "Fresh admission, launch/context/execution auditing and substantive adjudication "
                  "remain mandatory. No context or other gate is weakened. Initial held evidence "
                  "remains unaccepted. Existing tools, source packet and signed teaching are unchanged.",
    }))


if __name__ == "__main__":
    main()
