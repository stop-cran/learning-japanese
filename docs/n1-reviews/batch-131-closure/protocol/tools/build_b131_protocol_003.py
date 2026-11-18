"""Create fresh paired B131002 tooling by exact bounded adaptation; never execute predecessor lifecycle."""
import json
import re
from pathlib import Path

from b131_review_v2_common import (
    BASE, CANDIDATE, COORDINATOR, FORECAST, HERE, OLD_HERE, OLD_PACKET, OLD_PACKET_SHA,
    PACKET, RECORDS, RUNS, TOOLS, freeze_json, frozen, json_bytes, load_batch,
    require, sha, start_guard, verify_packet, write_frozen)
from b131_capacity_002 import load_forecast
from b131_preflight_002 import normalize_prompt, verify_subset


def replace_once(text, before, after):
    require(text.count(before) == 1, "Adaptation anchor differs: " + before[:90])
    return text.replace(before, after)


def main():
    guard, _ = start_guard("B131002 fresh identity-only protocol preparation")
    try:
        subset = verify_subset(guard)
        forecast = load_forecast()
        require(not (HERE / "prompts").exists(), "Preserve existing fresh protocol")
        derivations = []

        def adapt(source, destination, transform=lambda text: text):
            raw = frozen(source)
            text = transform(raw.decode("utf-8").replace("\r\n", "\n"))
            compile(text, str(destination), "exec")
            if destination.exists():
                existing = frozen(destination)
                require(existing.replace(b"\r\n", b"\n") == text.encode("utf-8"),
                        "Preserved prior derived code differs beyond line endings")
                output = {"path": str(destination), "sha256": sha(existing), "bytes": len(existing)}
            else:
                output = write_frozen(destination, text.encode("utf-8"))
            derivations.append({"source": str(source), "sourceSha256": sha(raw), "output": output})

        def auditor(text):
            text = replace_once(text, "def audit(events, config, core, reference, extension=None",
                                "def audit_base(events, config, core, reference, extension=None")
            anchor = "\ndef require_frozen(path, expected=None):"
            wrapper = '''
def audit(events, config, core, reference, extension=None, phase1_text=None, phase2_text=None,
          final=False, record_incomplete=False):
    from b131_capacity_002 import load_forecast
    from b131_runtime_002 import context_telemetry, validate_prepared_extension
    from b131_review_v2_common import FORECAST, HERE, frozen, sha
    if config.get("capacityForecastSha256") != sha(frozen(FORECAST)):
        raise IntegrityError("Capacity forecast binding changed/missing")
    forecast = load_forecast()
    result = audit_base(events, config, core, reference, extension, phase1_text, phase2_text,
                        final, record_incomplete)
    result["run"] = config["run"]
    result["capacityTelemetry"] = context_telemetry(events, forecast)
    if result["capacityTelemetry"]["status"] != "PASS":
        result["breaches"].extend(result["capacityTelemetry"]["errors"])
        result["status"] = ("HOLD_CONTEXT_COMPACTED" if result["capacityTelemetry"]["compactions"]
                            else "HOLD_CONTEXT_UNVERIFIED")
    if extension is not None:
        if phase1_text is None or phase2_text is None:
            raise IntegrityError("Final audit lacks frozen independent phase messages")
        phase1_record = json.loads(frozen(HERE / (config["run"] + "-phase1.json")))
        original = Path(phase1_record["auditDir"]) / "audit.json"
        result["extensionEvidenceCapacity"] = validate_prepared_extension(
            config, extension, phase1_text, phase2_text, original)
    return result

'''
            text = replace_once(text, anchor, "\n" + wrapper + anchor)
            imports = "from review_chain import digest, validate_selection"
            text = replace_once(text, imports, "sys.path.append(" + repr(str(TOOLS)) + ")\n" + imports)
            return text

        adapt(OLD_HERE / "audit-review.py", HERE / "audit-review.py", auditor)

        def structure(text):
            # The existing missing-ID parser recognizes only D/E lines; machine dictionary metadata is not an ID.
            return text
        adapt(OLD_HERE / "check-report-structure.py", HERE / "check-report-structure.py", structure)
        adapt(OLD_HERE / "check-run-context.py", HERE / "check-run-context.py")

        def adapter(text):
            return text.replace("b131_neutral_common_001", "b131_review_v2_common").replace(
                '"preparation-lifecycle-"', '"preparation-v2-lifecycle-"')
        adapt(TOOLS / "b131_lifecycle_process_002.py", TOOLS / "b131_lifecycle_process_003.py", adapter)

        def admission(text):
            text = text.replace("b131_neutral_common_001", "b131_review_v2_common")
            anchor = '        verify_packet(config, guard)\n'
            replacement = anchor + (
                "        from b131_preflight_002 import verify_subset\n"
                "        from b131_review_v2_common import FORECAST\n"
                "        from b131_capacity_002 import load_forecast\n"
                "        verify_subset(guard, initial=True)\n"
                "        capacity = load_forecast()\n"
                "        record.update(capacityForecastSha256=sha(frozen(FORECAST)),\n"
                "                      chosenCaps=capacity['chosenCaps'],\n"
                "                      projectedWorstCasePeak=capacity['projectedWorstCasePeak'])\n")
            return replace_once(text, anchor, replacement)
        adapt(TOOLS / "b131_review_admission_001.py", TOOLS / "b131_review_admission_002.py", admission)

        def lifecycle(text):
            text = text.replace("b131_neutral_common_001", "b131_review_v2_common")
            text = text.replace("b131_lifecycle_process_002", "b131_lifecycle_process_003")
            text = text.replace("b131_review_admission_001", "b131_review_admission_002")
            text = text.replace("step_b131_neutral_003.py", "step_b131_neutral_004.py")
            text = text.replace("prepare_chain_b131_001.py", "prepare_chain_b131_002.py")
            text = text.replace("preflight-compact-003.json", "preflight-compact-002.json")
            anchor = '    report = Path(spec["report"])\n'
            text = replace_once(text, anchor,
                "    from b131_review_v2_common import FORECAST\n"
                "    from b131_capacity_002 import load_forecast\n"
                "    load_forecast()\n"
                "    require(audit_config['capacityForecastSha256'] == sha(frozen(FORECAST)),\n"
                "            'Forecast binding changed')\n" + anchor)
            anchor = '            ready = code == 0\n'
            text = replace_once(text, anchor, anchor + (
                "            if ready:\n"
                "                from b131_runtime_002 import validate_prepared_extension\n"
                "                check = validate_prepared_extension(audit_config,\n"
                "                    json.loads(frozen(extension)), result['messages'][0],\n"
                "                    frozen(phase2).decode('utf-8'), path)\n"
                "                record['extensionEvidenceCapacity'] = check\n"
                "                record['capacityTelemetry'] = result['capacityTelemetry']\n"))
            return text
        adapt(TOOLS / "step_b131_neutral_003.py", TOOLS / "step_b131_neutral_004.py", lifecycle)
        freeze_json(HERE / "tooling-derivation-002.json", {
            "status": "IMPLEMENTATION_ADAPTATION_ONLY", "derivations": derivations,
            "limits": "No predecessor lifecycle main executed and no actual held reviewer log/selection read."})

        core_path = HERE / "core-chain-compact-002.json"
        chain = json.loads(frozen(core_path))
        old_chain = json.loads(frozen(OLD_HERE / "core-chain-compact-001.json"))
        raw_template = frozen(OLD_HERE / "prompts/initial-claude-002.txt")
        text = raw_template.decode("utf-8")
        text = text.replace(old_chain["segments"][0]["path"], chain["segments"][0]["path"])
        text = text.replace(str(OLD_PACKET), str(PACKET)).replace(OLD_PACKET_SHA, subset["packetManifestSha256"])
        text = text.replace(str(OLD_HERE), str(HERE)).replace("N1-B131-CLAUDE-001", RUNS[0])
        text = text.replace("reports\\initial-claude-001.md", "reports\\initial-claude-002.md")
        text = re.sub(r"\b114\b", str(len(chain["segments"])), text)
        start, end = text.index("REQUIRED READS:"), text.index("PHASE 1 (selection).")
        names = "\n".join("- " + source["source"] for source in chain["sources"])
        reads = (
            f"REQUIRED READS: all {len(chain['segments'])} core segments in full. They contain these "
            f"{len(chain['sources'])} complete sources in exact order:\n" + names + "\n\n"
            "The same-commit title index has1257 entries in code-point order. Confirm source lines1-1257, "
            'first line "一 one" and last line "齢 age; years lived". Its mechanical baseline1254→1257 '
            "delta has exactly3 additions (衛,羊,霜), zero removals/changes. The baseline file is UNREAD.\n\n"
            "COMPACT-002 EVIDENCE DISCLOSURES: The KANJIDIC projection retains all182 record identities; "
            "only codepoint,dic_number,query_code, meaning elements with m_lang, and readings whose "
            "r_type is pinyin,korean_r,korean_h,vietnam are removed. Everything else is retained.\n"
            "JMdict core retains615 complete original record lines of874: a keb contains 羊/衛/衞/霜, "
            "a keb exactly equals a declared character (three targets,衞,all quiz_exclusions,古右川), "
            "or a reb exactly equals えい,え,よう,ひつじ,そう,しも. The259 remainder records are initially UNREAD. "
            "Phase2 adds only complete omitted records whose keb exactly equals your independent D/E characters, "
            "deduplicated against core/other selected records and retained in original union order. "
            "No exact-keb match in the frozen union is disclosed without substitutes, hints or claims of real-world absence.\n"
            "xml-presentation.json,font-cmap.json,baseline-title-index.txt,dictionary-index.json and the full "
            "KANJIDIC/JMdict files remain packet-retained/coordinator-verified but are OUTSIDE your chains. "
            "Never claim to have read any source, class or record outside your own opened chain. "
            "Dependent consequential claims and affected assessments must be UNVERIFIED. "
            "All other compact-001 limits remain unchanged; repository wording cannot widen access.\n"
            "Font summary: bounded209 code points cover Han in the three new cards, comparison identifiers "
            "and explicit components, not all legacy article text. U+4E8D,U+51DC,U+5F73,U+885E,U+97CB are absent "
            "from all three bundled cmaps; no rendered fallback/native/device acceptance is claimed.\n"
            "Raw HTML/SVG,binary Joyo PDF,receipts and other non-chain assets are unread. "
            "No fresh external requests are authorized.\n"
            "Capacity limits are maxima, not quotas. A forecast is not a guarantee. Any context compaction "
            "invalidates this run. Actual phase1 peak is recorded against forecast; the coordinator must "
            "pass the actual-token plus complete article/dictionary extension capacity gate before phase2.\n\n")
        text = text[:start] + reads + text[end:]
        text = text.replace("D. At most 40 collision-candidate cards", f"D. At most {forecast['chosenCaps']['D']} collision-candidate cards")
        before = ("- EXTENSION CHAIN (phase 2): the coordinator will mechanically build, in the same format, "
                  "byte-exact copies of the D and E cards you request in phase 1, in your order, and send you its first-segment path.")
        text = replace_once(text, before,
            "- EXTENSION CHAIN (phase2): after its runtime capacity gate, the coordinator mechanically supplies "
            "byte-exact D/E articles in your request order, then complete applicable omitted JMdict records "
            "in original union order, with no core/repeated records. Its single message carries the first "
            "segment path, missing-article lines and exact dictionary-match/absence metadata. Read only the chain.")
        before = ("Request only cards by kanji character; the coordinator includes only entries that exist as "
                  "repo\\kanji\\<character>.md in the original packet and reports any nonexistent entry back verbatim, "
                  "with no substitutes or hints.")
        text = replace_once(text, before,
            "Request only characters. The coordinator supplies each existing repo\\kanji\\<character>.md and "
            "any complete exact-keb omitted JMdict records from the frozen874-record union. Missing article "
            "request lines and absent exact-keb matches are disclosed verbatim/mechanically, without substitutes or hints.")
        start = text.index("PHASE 2 (review).")
        end = text.index("ANALYSIS AND REPORT:", start)
        text = text[:start] + (
            "PHASE2 (review). The coordinator's exact single message gives the extension first-segment path, "
            "Missing entries: none or verbatim missing-article request lines, then Dictionary matches: JSON "
            "and No exact-keb match in frozen union: character metadata. This is mechanical source availability, "
            "not a semantic selection or finding. Read the entire chain serially, including every complete "
            "supplemental family. Disclose missing articles and absent/unread dictionary evidence as limits; "
            "neither proves linguistic absence. Then analyse and write the sole report.\n\n") + text[end:]
        # Identity placeholders only; no author verdict, disposition, or actual earlier list is an input.
        neutral = text.replace("CLAUDE", "{{FAMILY_UPPER}}").replace("-claude-", "-{{family}}-")
        write_frozen(HERE / "prompts/template-compact-002.txt", neutral.encode("utf-8"))
        paths = [
            TOOLS / name for name in (
                "common.py", "run_b127_tool.py", "b131_neutral_common_001.py",
                "b131_review_v2_common.py", "b131_review_v2_derivations.py", "build_b131_review_packet_002.py",
                "b131_capacity_002.py", "b131_preflight_002.py", "b131_runtime_002.py",
                "prepare_b131_v2_chain_engine.py", "prepare_chain_b131_002.py", "forecast_b131_capacity_002.py",
                "build_b131_protocol_003.py", "b131_review_admission_002.py", "b131_lifecycle_process_003.py",
                "step_b131_neutral_004.py")]
        paths += [HERE / name for name in (
            "review_chain.py", "audit-review.py", "check-report-structure.py", "check-run-context.py",
            "batch.json", "packet-build-002.json", "derivation-verification-002.json",
            "tooling-derivation-002.json", "core-chain-compact-002.json", "core-chain-compact-002-preflight.json",
            "capacity-forecast-compact-002.json")]
        paths += [PACKET / "SHA256SUMS.json", PACKET / "eligibility-reference.json",
                  OLD_HERE / "source-contract.json"]
        bindings = [{"path": str(path), "sha256": sha(frozen(path))} for path in paths]
        runs, rendered = {}, []
        for family in ("claude", "gpt"):
            run = "N1-B131-" + family.upper() + "-002"
            prompt = HERE / "prompts" / f"initial-{family}-002.txt"
            kickoff = HERE / "prompts" / f"kickoff-{family}-002.txt"
            report = HERE / "reports" / f"initial-{family}-002.md"
            body = neutral.replace("{{FAMILY_UPPER}}", family.upper()).replace("{{family}}", family).encode("utf-8")
            require(str(prompt).encode() in body and str(report).encode() in body, "Fresh prompt/report paths missing")
            kickoff_bytes = (
                'Original user request: "Please find and inspect work items at stop-cran/learning-japanese '
                'related to creating N1 kanji cards. The work is ~30% complete. Fetch latest changes, find '
                'and read related repo work items, gather the context, plan the outstanding work and do it."\n\n'
                'Assigned slice: independent content review only, under the exact frozen compact-002 scope.\n\n'
                f"Read {prompt} using one view call with forceReadLargeFiles: true and no view_range, then "
                "follow its instructions. No other tool call may precede that read.").encode("ascii")
            audit_path = HERE / "prompts" / f"audit-config-{run}.json"
            audit_config = {
                "run": run, "batch": 131, "candidate": CANDIDATE, "base": BASE, "kickoff": str(kickoff),
                "prompt": str(prompt), "report": str(report), "coordinator": COORDINATOR,
                "expectedFamily": family, "coreManifest": str(core_path),
                "reference": str(PACKET / "eligibility-reference.json"),
                "completionContract": "entire-message-enum-v1", "completionContractScope": "coordinator-tool-message-only",
                "reportStructureContract": "report-structure-v1",
                "reportStructureChecker": str(HERE / "check-report-structure.py"), "maxWebFetches": 0,
                "capacityForecast": str(FORECAST), "capacityForecastSha256": sha(frozen(FORECAST)),
                "chosenCaps": forecast["chosenCaps"], "noCompactionRequired": True,
                "prePhase2Gate": 740000, "supplementalDictionaryCostRequired": True,
                "files": bindings + [{"path": str(prompt), "sha256": sha(body)},
                                     {"path": str(kickoff), "sha256": sha(kickoff_bytes)}]}
            for path, raw in ((prompt, body), (kickoff, kickoff_bytes), (audit_path, json_bytes(audit_config))):
                write_frozen(path, raw)
            rendered.append(body)
            runs[family] = {
                "run": run, "prompt": str(prompt), "promptSha256": sha(body), "kickoff": str(kickoff),
                "kickoffText": kickoff_bytes.decode("ascii"), "auditConfig": str(audit_path), "report": str(report),
                "launch": {"mode": "interactive", "model": "claude-opus-5.5" if family == "claude" else "gpt-6.1-sol",
                           "contextTier": "long_context", "freshSession": True,
                           "sessionName": f"B131 {family.upper()} independent review002"}}
        require(normalize_prompt(rendered[0]) == normalize_prompt(rendered[1]), "Prompt-pair identity differs")
        preflight = {
            "batch": 131, "candidate": CANDIDATE, "base": BASE, "packetManifestSha256": subset["packetManifestSha256"],
            "coreChainSha256": sha(frozen(core_path)), "capacityForecastSha256": sha(frozen(FORECAST)),
            "chosenCaps": forecast["chosenCaps"], "projectedPeak": forecast["projectedWorstCasePeak"],
            "order": ["claude", "gpt"], "runs": runs, "reportDirectory": str(HERE / "reports"),
            "phase2Delivery": "Only after actual capacity AND independently rederived full article/JMdict "
                              "coverage check. Send the ENTIRE frozen phase2-message, including missing/match metadata.",
            "readBudget": {"coreSegments": len(chain["segments"]), "maxSegmentBytesExclusive": 16000,
                           "totalCoreSegmentBytes": sum(s["bytes"] for s in chain["segments"]),
                           "contextAcceptance": "Actual long_context, every usage maxPromptTokens>=952000, "
                                                "no compaction, actual-token phase2 gate<=740000."},
            "blindness": "Identity-only paired neutral prompts; no held review observations or selections used.",
            "limits": "Preparation only, not current reviewer admission/launch permission. Forecast is not a guarantee."}
        result = freeze_json(HERE / "prompts/preflight-compact-002.json", preflight)
        print(json.dumps({"status": "FRESH_PROTOCOL_CREATED_NOT_ADMITTED", "preflight": result,
                          "runs": {family: run["promptSha256"] for family, run in runs.items()}}))
    finally:
        require(not guard.finish()["breach"], "Protocol preparation RAM breach")


if __name__ == "__main__":
    main()
