"""Bind the actual correction producers and handoff in a new verifier revision."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).parent


def derive(source, target, substitutions):
    raw = frozen(HERE / source)
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode()
    changes = []
    for before, after, expected in substitutions:
        before, after = (value.replace("\n", newline) for value in (before, after))
        require(text.count(before) == expected, f"Ambiguous substitution in {source}: {before[:60]}")
        text = text.replace(before, after)
        changes.append({"before": before, "after": after, "count": expected})
    reverse = text
    for change in reversed(changes):
        require(reverse.count(change["after"]) == change["count"], "Reverse substitution count differs")
        reverse = reverse.replace(change["after"], change["before"])
    require(reverse.encode() == raw, "Source bytes not recovered")
    compile(text, str(HERE / target), "exec")
    binding = write_frozen(HERE / target, text.encode())
    return {"source": source, "sourceSha256": sha(raw), "output": binding,
            "substitutions": changes, "reverseExact": True}


def main():
    helper = derive("b129_correction_evidence.py", "b129_correction_evidence_v2.py", [
        ("from common import require, sha", "from common import frozen, require, sha", 1),
        ('        require(raw == source("producers/" + signed) and sha(raw) == digest,\n'
         '                "Replacement executed producer is not byte-equal to the original signed producer")',
         '        expected = source("producers/" + signed)\n'
         '        old = b"assert head == BASE"\n'
         '        new = (\'assert head == "\' + ORIGINAL + \'"\').encode()\n'
         '        require(expected.count(old) == 1, "Original author-admission check differs")\n'
         '        expected = expected.replace(old, new)\n'
         '        if local == "preserve_b129_correction.py":\n'
         '            require(expected.count(b"evidence-inventory-002.json") == 2,\n'
         '                    "Original inventory references differ")\n'
         '            expected = expected.replace(b"evidence-inventory-002.json", b"evidence-inventory-003.json")\n'
         '        require(raw == expected and sha(raw) == digest,\n'
         '                "Executed correction producer differs beyond the verified bounded adaptation")', 1),
        ('    return {\n        "record": PREFIX + CORRECTION,',
         '    handoff_path = scratch / "handoff-002.json"\n'
         '    handoff_raw = frozen(handoff_path, "6f559a2a11f3e729424c27afa1dfcb60588a60bc98d9d07e979b40cccb3e064d")\n'
         '    handoff = json.loads(handoff_raw)\n'
         '    require(handoff["candidate"] == candidate and handoff["base"] == BASE\n'
         '            and handoff["supersededCandidate"] == ORIGINAL\n'
         '            and handoff["correction"]["sha256"] == sha(source(CORRECTION))\n'
         '            and handoff["finalInventory"]["sha256"] == sha(source(INVENTORY))\n'
         '            and handoff["manifestSha256"] == payload["manifestSha256"], "Handoff differs")\n'
         '    for group in handoff["exactReplacementSnapshotEvidence"].values():\n'
         '        directory = Path(group["directory"])\n'
         '        require(directory.parent == scratch, "Unexpected handoff evidence path")\n'
         '        for name, digest in group["files"].items():\n'
         '            require(Path(name).name == name and sha((directory / name).read_bytes()) == digest,\n'
         '                    "Handoff evidence bytes changed")\n'
         '        require(group["summarySha256"] == group["files"]["summary.json"], "Handoff summary differs")\n'
         '    for name, digest in handoff["producerBindings"].items():\n'
         '        require(Path(name).name == name and sha((scratch / name).read_bytes()) == digest,\n'
         '                "Handoff producer binding differs")\n'
         '    previous = handoff["previousHandoff"]\n'
         '    require(Path(previous["path"]) == scratch / "handoff-001.json"\n'
         '            and sha(Path(previous["path"]).read_bytes()) == previous["sha256"], "Prior handoff changed")\n'
         '    return {\n'
         '        "handoff": {"path": str(handoff_path), "sha256": sha(handoff_raw)},\n'
         '        "record": PREFIX + CORRECTION,', 1),
        ('"The unchanged preservation producer checks inventory 002. "\n'
         '                                      "This verifier independently checks the complete superseding inventory 003."',
         '"Both the correction preservation producer and this verifier check final inventory 003. "\n'
         '                                      "Producer changes are exactly the original-candidate author admission and two inventory references."', 1),
    ])
    helper_sha = helper["output"]["sha256"]
    old_helper_sha = sha(frozen(HERE / "b129_correction_evidence.py"))
    verifier = derive("verify_b129_evidence_v3.py", "verify_b129_evidence_v4.py", [
        ("import b129_correction_evidence as correction",
         "import b129_correction_evidence_v2 as correction", 1),
        (f'CORRECTION_HELPER_SHA = "{old_helper_sha}"',
         f'CORRECTION_HELPER_SHA = "{helper_sha}"', 1),
        ('            verify_summary(summary, mode, candidate, payload["manifestSha256"], runner_sha, common_sha)\n'
         '            bindings = helper.gate_bindings(directory, config, payload["manifestSha256"], runner_sha, guard)',
         '            executed_runner_sha = (runner_sha if mode == "author" else\n'
         '                                   sha((SCRATCH / "run_b129_correction_gates.py").read_bytes()))\n'
         '            verify_summary(summary, mode, candidate, payload["manifestSha256"], executed_runner_sha, common_sha)\n'
         '            bindings = helper.gate_bindings(directory, config, payload["manifestSha256"], executed_runner_sha, guard)', 1),
        ('preservation["evidenceInventorySha256"] == signed[PREFIX + "evidence-inventory-002.json"]',
         'preservation["evidenceInventorySha256"] == signed[PREFIX + "evidence-inventory-003.json"]', 1),
        ('preservation["producerSha256"] == signed[PREFIX + "producers/preserve_b129_all.py"]',
         'preservation["producerSha256"] == sha((SCRATCH / "preserve_b129_correction.py").read_bytes())', 1),
    ])
    print(freeze_json(WS / "scratch-129" / "review" / "evidence-v4-derivation.json", {
        "helper": helper, "verifier": verifier,
        "scope": "Bind the actual correction-only producer changes and handoff002; "
                 "retain exact serial gate commands, hashes, inventory and historical evidence.",
    }))


if __name__ == "__main__":
    main()
