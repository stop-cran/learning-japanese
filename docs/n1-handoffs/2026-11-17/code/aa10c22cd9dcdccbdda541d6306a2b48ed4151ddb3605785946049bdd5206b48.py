"""Adapt final accepted B133 implementations; no reviewer execution."""
import json
import re
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
PREP = ROOT / "neutral-preparation-001"
OLD = WS / "scratch-133" / "review" / "neutral-preparation-004" / "successor-002"
sys.path.insert(0, str(WS / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard, write_frozen

PINS = {
    "source-proof-002.json": "f3a80ee569a1bfd4f452e3f413a6377f5d01cac665e978dfc3e6db722c809393",
    "payload-proof-001.json": "ec47228ee313a82d872e7235f6f4a6b048737f24254d26405418c840dbd65d1a",
    "gate-verification-002/verification.json": "1caed56d80a213605d59eac6cc7ecc69829083cbdaa606b684edd77fb9162694",
    "packet-verification-001/verification.json": "fb95e655419fe9ecc0465ac565fb309397fb8843c22362b08cf5a1feda4d478a",
}
BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
RUNNER_SHA = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
DERIVATIONS = []


def load(path):
    return json.loads(frozen(path))


def main():
    guard, _ = start_guard("B134 final serial protocol derivation")
    try:
        selected = load(PREP / "selected-packet-001.json")
        HERE = Path(selected["root"])
        PROTOCOL = HERE / "protocol-001"
        require(not PROTOCOL.exists() and selected["caps"], "Protocol exists or capacity HOLD")
        caps = selected["caps"]
        build = load(HERE / "packet-build.json")
        forecast = load(HERE / "capacity-measurement-001.json")
        chain = load(HERE / "core-chain-001.json")
        sums = load(HERE / "packet" / "SHA256SUMS.json")
        for n, d in PINS.items():
            proof = json.loads(frozen(ROOT / n, d))
            require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE
                    and proof["base"] == BASE and not proof["memory"]["breach"], "Coordinator proof differs")
        frozen(WS / "review-tools" / "verify_b134_packet.py",
               "d6a5b90ccb0bfe6bb1f4299dea4821e4dda2bc8349575ecbe02ef82f3e82974d")
        for name in ("capacity004.py", "capacity004_units.py"):
            write_frozen(HERE / "tools" / name, frozen(PREP / "tools" / name))

        def transformed(path):
            raw = frozen(path)
            text = raw.decode().replace("\r\n", "\n")
            for before, after in (
                (str(OLD), str(HERE)), ("b133", "b134"), ("B133", "B134"),
                ("scratch-133", "scratch-134"),
                ('ROOT / "neutral-preparation-004" / "successor-002"',
                 'ROOT / "neutral-preparation-001" / "projected-successor-001"'),
                ('"protocol-003"', '"protocol-001"'), ("audit-configs-004", "audit-configs-001"),
                ("audit-configs-003", "audit-configs-001"),
                ("ad047ace020579f81bde250ac948b9a4cb597887", CANDIDATE),
                ("6858fcfb069cc56a195c3f6ed938f92f657fe96b", BASE),
                ("03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb", RUNNER_SHA),
                ("dee789f5d8d6f547c9bd8616a5f9b28bd584028703ac05b9ddec63d9fe6f82e4",
                 sha(frozen(HERE / "packet" / "SHA256SUMS.json"))),
                ("f54ea59e3c10ba539ab110df523740bf9c58da108a7f5e4e990688ed98554146",
                 sha(frozen(HERE / "core-chain-001.json"))),
                ("e09ee3f384183b22d540812bb23001f8b48cfabd30fec1bd2d9037c2f536881a",
                 sha(frozen(HERE / "capacity-measurement-001.json"))),
                ('"batch": 133', '"batch": 134'),
                ("step-b134-002.py", "step-b134-001.py"),
                ("run-step-b134-002.ps1", "run-step-b134-001.ps1"),
                ("test-synthetic-protocol-b134-002.py", "test-synthetic-protocol-b134-001.py"),
            ):
                text = text.replace(before, after)
            return raw, text

        def emit_from(path, name, text=None):
            raw, default = transformed(path)
            binding = write_frozen(PROTOCOL / name, (default if text is None else text).encode())
            DERIVATIONS.append({"source": str(path), "sha256": sha(raw), "output": binding})
            return binding

        names = ("b133_common.py", "b133_capacity.py", "b133_runtime.py",
                 "prepare-extension-b133-001.py", "audit-review-b133-001.py",
                 "check-report-structure-b133-001.py")
        for name in names:
            emit_from(OLD / "protocol-003" / name, name.replace("b133", "b134"))
        raw, parser = transformed(OLD / "protocol-003" / "review_chain_with_optional.py")
        parser = parser.replace('{"D": 10, "E": 5}', repr(caps))
        units = {("K:" + Path(r["source"]).stem if "/kanjidic2-full-records/" in r["source"]
                  else r["source"]): r["source"] for r in forecast["optionalUnits"]}
        a = parser.index("OPTIONAL_UNITS = ")
        b = parser.index("\n\n\ndef validate_selection", a)
        parser = parser[:a] + "OPTIONAL_UNITS = " + repr(units) + parser[b:]
        emit_from(OLD / "protocol-003" / "review_chain_with_optional.py", "review_chain_with_optional.py", parser)

        prompts = {}
        text = frozen(OLD / "prompts-003" / "initial-claude-001.txt").decode()
        text = text.replace(str(OLD), str(HERE)).replace("B133", "B134").replace("prompts-003", "prompts-001")
        text = text.replace("ad047ace020579f81bde250ac948b9a4cb597887", CANDIDATE)
        text = text.replace("6858fcfb069cc56a195c3f6ed938f92f657fe96b", BASE)
        text = text.replace("dee789f5d8d6f547c9bd8616a5f9b28bd584028703ac05b9ddec63d9fe6f82e4",
                            sha(frozen(HERE / "packet" / "SHA256SUMS.json")))
        text = re.sub(r"69(?= (?:core )?segments)", str(len(chain["segments"])), text)
        text = text.replace("segment 69 ends", f"segment {len(chain['segments'])} ends")
        text = re.sub(r"(?m)^C:\\Users\\stop-\\.*\\chains\\core-001\\01-[a-f0-9]+\.txt$",
                      lambda _: chain["segments"][0]["path"], text)
        a, b = text.index("REQUIRED READS:"), text.index("PHASE 1 (selection).")
        disclosure = frozen(HERE / "DISCLOSURE-001.txt").decode()
        text = text[:a] + ("REQUIRED READS: all core segments, in full and order:\n"
            + "\n".join("- " + n for n in build["coreSources"]) + "\n\n" + disclosure
            + f"\nMeasured first passing caps: D<={caps['D']}/E<={caps['E']}; maxima, not quotas.\n\n") + text[b:]
        text = text.replace("D. At most 10", f"D. At most {caps['D']}")
        text = text.replace("E. At most 5", f"E. At most {caps['E']}")
        head = "ELIGIBILITY REFERENCE (exact bytes of the packet's eligibility-reference.json: mechanically extracted original frontmatter, in card order):\n"
        a = text.index(head) + len(head)
        b = text.index("END ELIGIBILITY REFERENCE", a)
        text = text[:a] + frozen(HERE / "packet" / "eligibility-reference.json").decode() + text[b:]
        for before, after in (
            ("each of the three new cards", "the one new card"),
            ("each of the three support-article changes", "the one support-article change"),
            ("one per-card data row for the one new card", "one per-card data row for the one new card"),
            ("O1..O86", "O1..O62"),
        ):
            text = text.replace(before, after)
        lines = text.splitlines(keepends=True)
        first_card = next(i for i, line in enumerate(lines) if line.startswith("| 琴 |"))
        last_card = next(i for i, line in enumerate(lines) if line.startswith("| 滝 |"))
        lines[first_card:last_card + 1] = [
            "| 紫 | <紫-correctness-verdict> | <紫-coverage-verdict> | <紫-consistency-verdict> | <紫-comprehensibility-verdict> | <紫-evidence> |\n"]
        text = "".join(lines)
        require(not any(s in text for s in ("515", "83 KANJIDIC", "three new cards", "three support", "琴.md", "鉛.md", "滝.md")),
                "Stale B133 prompt constants")
        require(chain["segments"][0]["path"] in text and disclosure in text, "Prompt binding/disclosure differs")
        for family in ("claude", "gpt"):
            body = text if family == "claude" else text.replace("CLAUDE", "GPT").replace("-claude-", "-gpt-")
            prompt = HERE / "prompts-001" / f"initial-{family}-001.txt"
            kickoff = frozen(OLD / "prompts-003" / f"kickoff-{family}-001.txt").decode("ascii")
            kickoff = kickoff.replace(str(OLD), str(HERE)).replace("prompts-003", "prompts-001")
            report = HERE / "reports-001" / f"review-{family}-001" / f"initial-{family}-001.md"
            report.parent.mkdir(parents=True, exist_ok=False)
            require(len(body.encode()) <= 40000, "Instruction exceeds bootstrap contract")
            prompts[family] = {"run": f"N1-B134-{family.upper()}-001",
                "prompt": write_frozen(prompt, body.encode()),
                "kickoff": write_frozen(HERE / "prompts-001" / f"kickoff-{family}-001.txt", kickoff.encode("ascii")),
                "kickoffText": kickoff, "report": str(report),
                "launch": {"mode": "interactive", "model": "claude-opus-5.5" if family == "claude" else "gpt-6.1-sol",
                           "contextTier": "long_context", "freshSession": True,
                           "sessionName": f"B134 {family.upper()} independent review 001"}}

        sys.path.insert(0, str(PROTOCOL))
        from b134_common import validate_report_destination
        from b134_capacity import PROFILES, startup_bound
        bindings = [{"path": str(p), "sha256": sha(frozen(p))}
                    for p in list(PROTOCOL.glob("*.py")) + list((HERE / "tools").glob("*.py"))
                    + [HERE / "core-chain-001.json", HERE / "capacity-measurement-001.json",
                       HERE / "packet" / "SHA256SUMS.json", HERE / "packet" / "eligibility-reference.json",
                       HERE / "DISCLOSURE-001.txt"]]
        bindings += [{"path": str(ROOT / n), "sha256": d} for n, d in PINS.items()]
        for family, spec in prompts.items():
            config = {"run": spec["run"], "batch": 134, "candidate": CANDIDATE, "base": BASE,
                "kickoff": spec["kickoff"]["path"], "prompt": spec["prompt"]["path"], "report": spec["report"],
                "coordinator": "2451b10d-02a9-46ab-82d5-d90993f0cb8b", "expectedFamily": family,
                "coreManifest": str(HERE / "core-chain-001.json"),
                "reference": str(HERE / "packet" / "eligibility-reference.json"),
                "completionContract": "entire-message-enum-v1", "completionContractScope": "coordinator-tool-message-only",
                "reportStructureContract": "report-structure-v1",
                "reportStructureChecker": str(PROTOCOL / "check-report-structure-b134-001.py"),
                "capacityForecastSha256": sha(frozen(HERE / "capacity-measurement-001.json")),
                "contextProfile": PROFILES[family], "maxWebFetches": 0,
                "files": bindings + [spec["prompt"], spec["kickoff"]]}
            spec["auditConfig"] = freeze_json(HERE / "audit-configs-001" / f"audit-{family}-001.json", config)
            spec["reportReadiness"] = validate_report_destination(spec)
            spec["startupEstimate"] = startup_bound(forecast, family, len(frozen(config["prompt"])))
        preflight = freeze_json(HERE / "audit-configs-001" / "preflight.json", {
            "status": "PASS_STATIC_FORECAST_NOT_REVIEWER_ADMISSION", "batch": 134, "candidate": CANDIDATE,
            "base": BASE, "order": ["claude", "gpt"], "runs": prompts,
            "coreManifestSha256": sha(frozen(HERE / "core-chain-001.json")),
            "capacityMeasurementSha256": sha(frozen(HERE / "capacity-measurement-001.json"))})

        raw, step = transformed(OLD / "protocol-003" / "step-b133-004.py")
        step = re.sub(r'PREFLIGHT_SHA = "[a-f0-9]+"', 'PREFLIGHT_SHA = "' + preflight["sha256"] + '"', step)
        a, b = step.index("PROOFS = {"), step.index("\n\n\ndef now")
        step = step[:a] + "PROOFS = " + repr(PINS) + step[b:]
        step = step.replace('"PYTHONIOENCODING": "utf-8",', '"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",')
        step_binding = emit_from(OLD / "protocol-003" / "step-b133-004.py", "step-b134-001.py", step)
        raw, wrapper = transformed(OLD / "protocol-003" / "run-step-b133-005.ps1")
        wrapper = wrapper.replace(r"neutral-preparation-004\successor-002\protocol-003\step-b134-004.py",
                                  r"neutral-preparation-001\projected-successor-001\protocol-001\step-b134-001.py")
        wrapper = wrapper.replace("1710b0b378224f45cb84397eac02e946e428455131d3e79d87a1b51dae9b9bfd",
                                  step_binding["sha256"])
        wrapper = wrapper.replace("$env:PYTHONIOENCODING", "$env:PYTHONUTF8 = '1'\n$env:PYTHONIOENCODING", 1)
        emit_from(OLD / "protocol-003" / "run-step-b133-005.ps1", "run-step-b134-001.ps1", wrapper)
        test_map = {
            "final-test-synthetic-protocol-b133-002.py": "test-synthetic-protocol-b134-001.py",
            "final-test-b133-focused-controls-001.py": "test-b134-focused-controls-001.py",
            "final-test-b133-lifecycle-controls-001.py": "test-b134-lifecycle-controls-001.py"}
        for old, new in test_map.items():
            raw, test = transformed(OLD / "protocol-003" / old)
            test = test.replace(
                "| 琴 | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | synthetic |\n"
                "| 鉛 | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | synthetic |\n"
                "| 滝 | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | synthetic |",
                "| 紫 | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | synthetic |")
            test = test.replace("self.assertEqual(proof[\"verifiedJmdictFamilies\"], 515)",
                                "self.assertEqual(proof[\"verifiedJmdictFamilies\"], 399)")
            test = test.replace("self.assertEqual(proof[\"verifiedKanjidicRecords\"], 83)",
                                "self.assertEqual(proof[\"verifiedKanjidicRecords\"], 59)")
            test = test.replace("9ecbdbb9d2c0f90c1de9c1a4088a78655bb531f715e74ae07002ad797dcf9ebd",
                                PINS["packet-verification-001/verification.json"])
            test = test.replace("range(11)", "range(26)").replace("lines[:10]", "lines[:25]")
            emit_from(OLD / "protocol-003" / old, new, test)
        freeze_json(HERE / "protocol-derivation-001.json", DERIVATIONS)
        print(json.dumps({"preflight": preflight, "step": step_binding,
                          "limits": "No reviewer launched. Actual observations and semantic adjudication remain mandatory."}))
    finally:
        require(not guard.finish()["breach"], "Protocol derivation RAM breach")


if __name__ == "__main__":
    main()
