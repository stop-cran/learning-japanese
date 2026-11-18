"""Create neutral B131 successors from implementation references; no historical execution."""
import json
from pathlib import Path

from b131_neutral_common_001 import (HERE, TOOLS, WS, freeze_json, frozen, require,
                                     sha, start_guard, write_frozen)


def derive(source, target, changes):
    raw = frozen(source)
    text = raw.decode("utf-8").replace("\r\n", "\n")
    changes_applied = []
    for before, after in changes:
        count = text.count(before)
        require(count > 0, "Missing derivation anchor: " + before[:90])
        text = text.replace(before, after)
        changes_applied.append({"before": before, "after": after, "count": count})
    compile(text, str(target), "exec")
    require("b130" not in text.lower() and "scratch-130" not in text
            and "batch-130" not in text, "Residual predecessor identity in executable")
    return {"source": {"path": str(source), "sha256": sha(raw)},
            "output": write_frozen(target, text.encode("utf-8")), "changes": changes_applied}


def main():
    require(not (HERE / "tooling-derivation.json").exists(), "Preserve derived tooling")
    guard, _ = start_guard("B131 neutral protocol derivation")
    results = []
    try:
        reference = WS / "scratch-130" / "review"
        for name in ("review_chain.py", "audit-review.py", "check-report-structure.py",
                     "check-run-context.py", "test-review-chain.py", "test-report-structure.py",
                     "test-review-audit.py"):
            raw = frozen(reference / name).decode("utf-8")
            changes = [("B130", "B131")] if "B130" in raw else []
            if "b130" in raw:
                changes.append(("b130", "b131"))
            if name == "review_chain.py":
                changes.append(('    for group in ("D", "E"):\n',
                                '    if len({e["character"] for e in entries}) != len(entries):\n'
                                '        errors.append("Duplicate comparison character")\n'
                                '    for group in ("D", "E"):\n'))
            if name == "audit-review.py":
                changes.append(('    config = json.loads(args.config.read_bytes())',
                                '    config = json.loads(require_frozen(args.config))'))
            results.append(derive(reference / name, HERE / name, changes))
            guard.check()
        chain_source = TOOLS / "prepare-chain-b130-compact.py"
        text = frozen(chain_source).decode("utf-8")
        results.append(derive(chain_source, TOOLS / "prepare_chain_b131_001.py", [
            ("b130_compact_common", "b131_neutral_common_001"),
            ("prepare-chain-b130-compact.py", "prepare_chain_b131_001.py"),
            ('WS / "review-chains" / f"b{n}-{args.run}-extension"',
             'records / "chains" / f"b{n}-{args.run}-extension"'),
            ('WS / "review-chains" / f"b{n}-initial-compact-001"',
             'records / "chains" / f"b{n}-initial-compact-001"'),
            ('            for name in ("source-metadata.json",',
             '            add("evidence/baseline-title-index.txt")\n'
             '            add("evidence/font-cmap.json")\n'
             '            for relative in packet["modifiedExisting"]:\n'
             '                add("baseline/" + relative)\n'
             '            for name in ("source-metadata.json",'),
            ('            require(phase1["status"] == "PHASE1_READY"',
             '            require(phase1["session"] and args.run in args.phase1_audit.parts,\n'
             '                    "Phase-1 audit is not stored under this run")\n'
             '            require(phase1["status"] == "PHASE1_READY"'),
        ]))
        lifecycle = frozen(TOOLS / "step_b130_compact.py").decode("utf-8").replace("\r\n", "\n")
        start = lifecycle.index('        source = Path(argument)\n')
        end = lifecycle.index('\n    elif action == "launch":', start)
        old_admission = lifecycle[start:end]
        results.append(derive(TOOLS / "step_b130_compact.py", TOOLS / "step_b131_neutral_001.py", [
            ("b130_compact_common", "b131_neutral_common_001"),
            ("step_b130_compact.py", "step_b131_neutral_001.py"),
            ("prepare-chain-b130-compact.py", "prepare_chain_b131_001.py"),
            ("from b127_lifecycle_process import python",
             "from b131_lifecycle_process_001 import python\nfrom b131_review_admission_001 import observe"),
            (old_admission, '        record = observe(argument, config, spec, record)\n'
                            '        out = records / f"{run}-admission.json"\n'),
            ('    elif action == "launch":\n        admission = binding(records / f"{run}-admission.json")',
             '    elif action == "launch":\n'
             '        admission_path = records / f"{run}-admission.json"\n'
             '        admitted = json.loads(frozen(admission_path))\n'
             '        age = (datetime.datetime.now(datetime.timezone.utc) -\n'
             '               datetime.datetime.fromisoformat(admitted["createdAt"])).total_seconds()\n'
             '        require(admitted["admitted"] is True and 0 <= age < 120,\n'
             '                "Startup observation expired; do not launch against a stale admission")\n'
             '        admission = binding(admission_path)'),
            ('        launch = json.loads(frozen(records / f"{run}-launch.json"))',
             '        launch = json.loads(frozen(records / f"{run}-launch.json"))'),
            ('        require(adjudication["run"] == run and adjudication["report"]["sha256"] == sha(frozen(report)),',
             '        require(adjudication["candidate"] == config["candidate"]\n'
             '                and adjudication["finalSha256"] == sha(frozen(records / f"{run}-final.json"))\n'
             '                and adjudication["claimsAdjudicated"] is True\n'
             '                and adjudication["run"] == run\n'
             '                and adjudication["report"]["sha256"] == sha(frozen(report)),'),
        ]))
        prompt_source = frozen(TOOLS / "build-prompts-b130-attempt004.py")
        prefix = prompt_source.decode("utf-8").replace("\r\n", "\n").split("\ndef main(batch):", 1)[0]
        prefix = prefix.replace("b130_compact_common", "b131_neutral_common_001").replace(
            "build-prompts-b130-attempt004.py", "build_b131_review_prompts_001.py")
        require("B130" not in prefix and "b130" not in prefix, "Predecessor identity in prompt primitives")
        results.append({
            "source": {"path": str(TOOLS / "build-prompts-b130-attempt004.py"), "sha256": sha(prompt_source)},
            "output": write_frozen(TOOLS / "b131_prompt_primitives_001.py", prefix.encode("utf-8")),
            "changes": "Retain only accepted-template value/render functions, never run predecessor main; "
                       "change shared configuration import to B131-only paths."})
        result = freeze_json(HERE / "tooling-derivation.json", {
            "batch": 131, "status": "PREPARATION_ONLY", "derivations": results,
            "producerSha256": sha(frozen(Path(__file__))),
            "limits": "Implementation sources only. No predecessor reports, selections, audit runs, "
                      "adjudications, findings or access grants were imported or executed."})
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Tooling derivation RAM breach")


if __name__ == "__main__":
    main()
