"""Use B134's actual proof graph, not B133's differently shaped companion."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import frozen, require, sha, write_frozen, freeze_json
source = HERE / "tools" / "packet-builder-b134-004.py"
raw = frozen(source)
text = raw.decode().replace('"complete-record-trial-002"', '"complete-record-trial-003"')
before = ('        companion = gates["capturedInputs"]["full-runtime/summary.json"]\n'
          '        put("checks/full-runtime-summary.json", frozen(companion["path"], companion["sha256"]))')
after = '''        baseline_manifest_raw = blob("manifest.json", BASE)
        baseline_manifest = json.loads(baseline_manifest_raw)
        groups = {}
        for group, values in manifest.items():
            if not isinstance(values, dict):
                continue
            old_values = baseline_manifest[group]
            require(isinstance(old_values, dict), "Runtime group shape differs")
            if group != "files":
                require(values == old_values, "Non-files group changed")
            groups[group] = {"baseline": len(old_values), "candidate": len(values),
                             "unchanged": sum(k in values and values[k] == v for k, v in old_values.items())}
        require(len(groups) == 9 and sum(g["baseline"] for g in groups.values()) == 8745
                and sum(g["candidate"] for g in groups.values()) == 8747, "Runtime companion count mismatch")
        put("checks/full-runtime-summary.json", json_bytes({
            "candidate": CANDIDATE, "base": BASE, "groups": groups,
            "baselineManifestSha256": sha(baseline_manifest_raw), "candidateManifestSha256": sha(manifest_raw),
            "gateProofSha256": PROOFS["gate-verification-002/verification.json"],
            "source": "Direct signed candidate/base manifest groups; neutral derivative, not a signed author producer.",
            "gateFullRuntime": gates["fullRuntime"], "gatePreservation": gates["preservation"]}))
'''
require(before in text, "Runtime anchor differs")
binding = write_frozen(HERE / "tools" / "packet-builder-b134-005.py", text.replace(before, after).encode())
measure = HERE / "tools" / "measure-and-adapt-b134-001.py"
measure_raw = measure.read_bytes()
measure.chmod(0o444)
mt = measure_raw.decode().replace('"complete-record-trial-002"', '"complete-record-trial-003"')
mt = mt.replace('        write_frozen(PREP / "tools" / name, text.encode())',
                '        path = PREP / "tools" / name\n'
                '        if path.exists():\n'
                '            require(frozen(path) == text.encode(), "Existing derived tool differs")\n'
                '        else:\n'
                '            write_frozen(path, text.encode())')
mt = mt.replace('    write_frozen(PREP / "tools" / "chain_b134_initial.py", text.encode())',
                '    path = PREP / "tools" / "chain_b134_initial.py"\n'
                '    if path.exists():\n'
                '        require(frozen(path) == text.encode(), "Existing chain tool differs")\n'
                '    else:\n'
                '        write_frozen(path, text.encode())')
mb = write_frozen(HERE / "tools" / "measure-and-adapt-b134-002.py", mt.encode())
freeze_json(HERE / "packet-runtime-correction-005.json", {
    "source": {"path": str(source), "sha256": sha(raw)}, "output": binding,
    "measurementSource": {"path": str(measure), "sha256": sha(measure_raw)}, "measurementOutput": mb,
    "reason": "B134 proof has direct fullRuntime/preservation objects, not a full-runtime captured file. Build a disclosed neutral nine-group derivative from exact manifests. Preserve both failed trials and resource receipts."})
