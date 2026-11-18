"""Exclusive immutable successors for fresh GPT004; no reviewer execution or old observations."""
import difflib
import json
from pathlib import Path

from b131_review_v4_common import (
    CORE, DEFAULT_PREFLIGHT, FORECAST, HERE, IMMUTABLE_BINDINGS, POLICY, PRIOR, TELEMETRY_SHA,
    TOOLS, accepted_prerequisite, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen)
from b131_capacity_003 import PROFILES, load_forecast, verify_neutral_telemetry
from b131_preflight_004 import (
    derive_prompt, neutral_inputs, path_inventory, verify_protocol, verify_subset)


def once(text, before, after):
    require(text.count(before) == 1, "Successor anchor differs: " + before[:100])
    return text.replace(before, after)


def main():
    require(not HERE.exists(), "Preserve every existing preparation;004 root must be new")
    guard, _ = start_guard("B131 GPT004 neutral successor preparation")
    try:
        telemetry = verify_neutral_telemetry()
        prerequisite = accepted_prerequisite()
        frozen(TOOLS / "step_b131_neutral_006.py",
               "b7bb9866b6ba1cfde4899bdd8563d17fbdbd953f6911c1872e56e406a9340df7")
        frozen(TOOLS / "b131_lifecycle_process_005.py",
               "4d736933523257498450ff2f9bd877eb498749c7a78d78bacd5a3755668e5b06")
        derivations = []

        def copy(source, destination, transform=None):
            raw = frozen(source)
            output = raw if transform is None else transform(raw.decode("utf-8").replace("\r\n", "\n")).encode("utf-8")
            if destination.suffix == ".py":
                compile(output.decode("utf-8"), str(destination), "exec")
            result = write_frozen(destination, output)
            derivations.append({"source": str(source), "sourceSha256": sha(raw), "output": result})
            guard.check()
            return result

        def migrate(text):
            for before, after in (
                ("b131_review_v3_common", "b131_review_v4_common"),
                ("b131_capacity_002", "b131_capacity_003"),
                ("b131_runtime_003", "b131_runtime_004"),
                ("b131_preflight_003", "b131_preflight_004"),
                ("prepare_chain_b131_003", "prepare_chain_b131_004"),
                ("b131_review_admission_003", "b131_review_admission_004"),
                ("preflight-compact-003.json", "preflight-compact-004.json")):
                text = text.replace(before, after)
            return text

        for name in ("batch.json", "derivation-verification-002.json", "review_chain.py",
                     "core-chain-compact-002.json", "check-report-structure.py"):
            copy(PRIOR / name, HERE / name)
        freeze_json(POLICY, {
            "status": "PREDECLARED_FAMILY_SPECIFIC_CAPACITY", "profiles": PROFILES,
            "startupGate": 700000, "forecastSha256": IMMUTABLE_BINDINGS[4][1],
            "neutralTelemetrySha256": TELEMETRY_SHA, "forecastUnchanged": True,
            "gptHeadroom": {"compactionTriggerEstimate": 737600, "prePhase2Gate": 710000,
                            "marginBelowEstimatedTrigger": 27600},
            "formula": "lastInputTokens +7000 +complete article/JMdict source/header cost +30000 <=family gate",
            "scope": "Exact supported limits; mixed/unknown limits HOLD. Forecast coefficients, caps, sources "
                     "and startup worst-case unchanged. GPT003 remains HOLD and cannot resume.",
            "limits": "Neither capacity forecast nor estimated compaction trigger is a guarantee."})
        verify_subset(guard, initial=True)
        freeze_json(HERE / "sequential-prerequisite-004.json", prerequisite)

        def extension(text):
            text = migrate(text).replace("-extension-003", "-extension-004")
            return once(text, "phase2_gate(events, forecast, cost)", 'phase2_gate(events, forecast, cost, "gpt")')
        copy(TOOLS / "prepare_chain_b131_003.py", TOOLS / "prepare_chain_b131_004.py", extension)

        def runtime(text):
            text = migrate(text)
            text = once(text, "def context_telemetry(events, forecast):",
                        "def context_telemetry(events, forecast, family=None):")
            text = once(text, "observed = telemetry(events, forecast)",
                        "observed = telemetry(events, forecast, family)")
            text = once(text, '    require(config["capacityForecastSha256"]',
                        '    from b131_capacity_003 import validate_capacity_config\n'
                        '    validate_capacity_config(config)\n'
                        '    require(config["capacityForecastSha256"]')
            text = once(text, 'context_telemetry(events, forecast)["status"]',
                        'context_telemetry(events, forecast, config["expectedFamily"])["status"]')
            return once(text, "phase2_gate(events, forecast, cost)",
                        'phase2_gate(events, forecast, cost, config["expectedFamily"])')
        copy(TOOLS / "b131_runtime_003.py", TOOLS / "b131_runtime_004.py", runtime)

        def audit(text):
            text = migrate(text)
            text = once(text, "from b131_capacity_003 import load_forecast",
                        "from b131_capacity_003 import load_forecast, validate_capacity_config")
            text = once(text, "    forecast = load_forecast()\n",
                        "    validate_capacity_config(config)\n    forecast = load_forecast()\n")
            return once(text, "context_telemetry(events, forecast)",
                        'context_telemetry(events, forecast, config["expectedFamily"])')
        copy(PRIOR / "audit-review.py", HERE / "audit-review.py", audit)
        def admission(text):
            text = migrate(text)
            anchor = "    report_readiness = validate_report_destination(spec)\n    request_path = Path(argument)"
            return once(text, anchor,
                "    report_readiness = validate_report_destination(spec)\n"
                "    from b131_review_v4_common import DEFAULT_PREFLIGHT\n"
                "    from b131_preflight_004 import verify_prerequisite\n"
                "    verify_prerequisite(json.loads(frozen(DEFAULT_PREFLIGHT)))\n"
                "    request_path = Path(argument)")
        copy(TOOLS / "b131_review_admission_003.py", TOOLS / "b131_review_admission_004.py", admission)
        copy(TOOLS / "b131_lifecycle_process_005.py", TOOLS / "b131_lifecycle_process_006.py",
             lambda text: migrate(text).replace("preparation-v3-lifecycle-", "preparation-v4-lifecycle-"))

        def step(text):
            text = migrate(text).replace("step_b131_neutral_006", "step_b131_neutral_007").replace(
                "b131_lifecycle_process_005", "b131_lifecycle_process_006")
            text = text.replace("<claude|gpt>", "<gpt>")
            text = once(text, '    spec = preflight["runs"][key]\n',
                        '    require(key == "gpt", "Fresh004 is GPT-only; accepted Claude003 is retained")\n'
                        '    spec = preflight["runs"][key]\n')
            start = text.index('        order = preflight["order"]')
            end = text.index('        record = observe(', start)
            text = (text[:start] + "        from b131_preflight_004 import verify_protocol\n"
                    "        verify_protocol(preflight)\n" + text[end:])
            text = once(text, "from b131_capacity_003 import load_forecast",
                        "from b131_capacity_003 import load_forecast, validate_capacity_config")
            text = once(text, "    load_forecast()\n",
                        "    load_forecast()\n    validate_capacity_config(audit_config)\n")
            require('f"{run}-context-{path.parent.name}.json"' in text
                    and 'f"{run}-structure-{path.parent.name}.json"' in text,
                    "Preserve coordinator006 audit-specific output names")
            return text
        copy(TOOLS / "step_b131_neutral_006.py", TOOLS / "step_b131_neutral_007.py", step)
        helper = frozen(TOOLS / "b131_lifecycle_process_006.py").decode("utf-8")
        require('"PYTHONPATH": str(TOOLS)' in helper, "Preserve coordinator child import fix")
        for before, after, label in (
            (TOOLS / "step_b131_neutral_005.py", TOOLS / "step_b131_neutral_006.py", "coordinator-step006"),
            (TOOLS / "b131_lifecycle_process_004.py", TOOLS / "b131_lifecycle_process_005.py", "coordinator-adapter005"),
            (TOOLS / "step_b131_neutral_006.py", TOOLS / "step_b131_neutral_007.py", "fresh-step007")):
            diff = "".join(difflib.unified_diff(
                frozen(before).decode("utf-8").splitlines(True),
                frozen(after).decode("utf-8").splitlines(True), fromfile=before.name, tofile=after.name))
            write_frozen(HERE / (label + ".diff"), diff.encode("utf-8"))
        checker = '''"""Exact model/long-context/no-compaction checker; only the supplied audited snapshot."""
import json
import sys
from pathlib import Path
from b131_capacity_003 import load_forecast, telemetry
from b131_review_v4_common import sha

def check(path):
    raw = Path(path).read_bytes()
    result = telemetry([json.loads(line) for line in raw.decode("utf-8").splitlines()], load_forecast())
    return {**result, "status": "PASS" if result["status"] == "PASS" else "FAIL",
            "events": str(path), "eventsSha256": sha(raw)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Expected one audited events path")
    result = check(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["status"] == "PASS" else 1)
'''
        compile(checker, "check-run-context.py", "exec")
        write_frozen(HERE / "check-run-context.py", checker.encode("utf-8"))

        def controls(text):
            text = migrate(text).replace("validation-002", "validation-004").replace(
                '["runs"]["claude"]', '["runs"]["gpt"]').replace("claude-fabricated", "gpt-fabricated")
            text = text.replace("b131_lifecycle_process_004.py", "b131_lifecycle_process_006.py")
            text = text.replace('{"contextTier": "long_context"}',
                                '{"contextTier": "long_context", "selectedModel": "gpt-6.1-sol"}')
            text = text.replace("952000", "922000").replace('{"maxPromptTokens": 922000}',
                                                         '{"maxPromptTokens": 922000, "inputTokens": 500000}')
            text = text.replace("bound = 740000", "bound = 710000")
            text = text.replace('"PASS_PAIRED_PROTOCOL"', '"PASS_IDENTITY_BOUND_GPT004"')
            start = text.index("        left, right = ", text.index("def test_prompt_pair_identity_and_nonidentity"))
            end = text.index("\n    def test_complete_preflight", start)
            text = (text[:start] + '''        spec = self.prompts["runs"]["gpt"]
        self.assertEqual(preflight.verify_prompt_identity(spec)["status"], "PASS_IDENTITY_ONLY")
        with patch.object(preflight, "derive_prompt", return_value=frozen(spec["prompt"]) + b"\\nextra hint"):
            with self.assertRaisesRegex(ValueError, "beyond"):
                preflight.verify_prompt_identity(spec)
''' + text[end:])
            return text
        copy(PRIOR / "test-controls-004.py", HERE / "test-controls-004.py", controls)
        freeze_json(HERE / "tooling-derivation-004.json", {
            "derivations": derivations, "neutralCapacity": telemetry, "sequentialPrerequisite": prerequisite,
            "preservedFixes": ["coordinator step006 audit-specific context/structure names",
                               "coordinator adapter005 child PYTHONPATH"],
            "notUsed": "No GPT003 events/audit/phase1 message; no Claude findings/report/adjudication."})
        source = neutral_inputs()
        report = HERE / "reports" / "review-gpt-004" / "initial-gpt-004.md"
        report.parent.mkdir(parents=True)
        spec = {**source, "run": "N1-B131-GPT-004", "report": str(report),
                "prompt": str(HERE / "prompts" / "initial-gpt-004.txt"),
                "kickoff": str(HERE / "prompts" / "kickoff-gpt-004.txt"),
                "auditConfig": str(HERE / "prompts" / "audit-config-N1-B131-GPT-004.json"),
                "launch": {"mode": "interactive", "model": "gpt-6.1-sol", "contextTier": "long_context",
                           "freshSession": True, "sessionName": "B131 GPT independent review004"}}
        prompt = derive_prompt(spec)
        spec["promptSha256"] = sha(prompt)
        spec["kickoffText"] = source["kickoffText"].replace(source["prompt"], spec["prompt"])
        write_frozen(spec["prompt"], prompt)
        write_frozen(spec["kickoff"], spec["kickoffText"].encode("ascii"))
        names = (
            "common.py", "run_b127_tool.py", "b131_review_v2_common.py", "b131_review_v3_common.py",
            "b131_review_v4_common.py", "b131_review_v2_derivations.py", "b131_capacity_002.py",
            "b131_capacity_003.py", "b131_preflight_002.py", "b131_preflight_003.py", "b131_preflight_004.py",
            "prepare_chain_b131_004.py", "b131_runtime_004.py", "b131_review_admission_004.py",
            "b131_lifecycle_process_006.py", "step_b131_neutral_007.py", "build_b131_gpt004.py",
            "test_b131_gpt004.py", "verify_b131_gpt004.py")
        paths = [TOOLS / name for name in names]
        paths += [HERE / name for name in (
            "batch.json", "derivation-verification-002.json", "review_chain.py", "core-chain-compact-002.json",
            "audit-review.py", "check-run-context.py", "check-report-structure.py", "test-controls-004.py",
            "capacity-policy-004.json", "tooling-derivation-004.json", "sequential-prerequisite-004.json")]
        paths += [path for path, _ in IMMUTABLE_BINDINGS] + [POLICY]
        paths += [Path(spec[key]) for key in ("prompt", "kickoff")]
        bindings = [{"path": str(path), "sha256": sha(frozen(path))} for path in dict.fromkeys(paths)]
        config = json.loads(frozen(source["auditConfig"]))
        config.update(run=spec["run"], prompt=spec["prompt"], kickoff=spec["kickoff"], report=spec["report"],
                      expectedFamily="gpt", contextProfile=PROFILES["gpt"],
                      capacityPolicySha256=sha(frozen(POLICY)), files=bindings,
                      reportStructureChecker=str(HERE / "check-report-structure.py"))
        freeze_json(spec["auditConfig"], config)
        forecast = load_forecast()
        preflight = {"batch": 131, "preparationVersion": "004", "order": ["gpt"], "runs": {"gpt": spec},
                     "sequentialPrerequisite": prerequisite, "capacityPolicySha256": sha(frozen(POLICY)),
                     "capacityForecastSha256": IMMUTABLE_BINDINGS[4][1],
                     "chosenCaps": forecast["chosenCaps"], "projectedPeak": forecast["projectedWorstCasePeak"],
                     "readBudget": {"coreSegments": 66, "totalCoreSegmentBytes": 874263,
                                    "contextProfile": PROFILES["gpt"], "startupGate": 700000},
                     "limits": "No permission to admit/launch now. GPT003 is not resumed or reclassified. "
                               "Accepted Claude003 is retained as opaque sequential prerequisite."}
        protocol = verify_protocol(preflight)
        inventory = path_inventory(preflight)
        readiness = freeze_json(HERE / "path-readiness-004.json", {
            "status": "PASS", "protocol": protocol, "inventory": inventory,
            "creationOrder": "Actual unique exclusive-create/readback/delete probe BEFORE preflight freeze."})
        preflight["pathReadiness"] = readiness
        result = freeze_json(DEFAULT_PREFLIGHT, preflight)
        memory = guard.finish()
        require(not memory["breach"], "GPT004 build RAM breach")
        print(json.dumps(freeze_json(HERE / "runset-build-004.json", {
            "status": "PREPARED_GPT004_NOT_ADMITTED", "preflight": result, "pathReadiness": readiness,
            "memory": memory, "neutralTelemetry": telemetry, "unchangedForecast": IMMUTABLE_BINDINGS[4][1]})))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
