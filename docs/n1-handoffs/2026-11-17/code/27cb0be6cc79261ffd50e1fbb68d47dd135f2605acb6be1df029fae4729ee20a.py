"""Freeze review-preparation deliverables, exact commands and execution evidence."""
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
PREP = ROOT / "neutral-preparation-001"
HERE = PREP / "projected-successor-001"
sys.path.insert(0, str(HERE / "protocol-001"))
from b134_common import frozen, require, sha, freeze_json, write_frozen, start_guard, validate_report_destination

BRIEF = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b134-review-preparation-kickoff.txt")


def load(path):
    return json.loads(frozen(path))


def main():
    guard, _ = start_guard("B134 freeze neutral preparation handoff")
    try:
        require(sha(BRIEF.read_bytes()) == "361aef9b6db7906548549a047bf6512c2e843076d0b1ba6ae9fb6e9c8c93255f",
                "Authoritative brief changed")
        frozen(ROOT / "review-preparation-admission-001.json",
               "2409b05e2949727f98dd00ae83b890c4ea0e4fbd450cf92e0bb54f83f5f48859")
        write_frozen(PREP / "authoritative-brief-001.txt", BRIEF.read_bytes())
        executions = []
        for directory in ROOT.iterdir():
            if not directory.is_dir() or directory == PREP:
                continue
            receipt_path = directory / "receipt.json"
            if not receipt_path.exists():
                continue
            receipt_raw = receipt_path.read_bytes()
            receipt = json.loads(receipt_raw)
            if (not directory.name.startswith("b134-lifecycle-execution-")
                    and not any(str(PREP).lower() in str(arg).lower() for arg in receipt["command"])):
                continue
            log = (directory / "output.log").read_bytes()
            require(sha(log) == receipt["logSha256"] and not receipt["memory"]["breach"]
                    and receipt["cleanupError"] is None
                    and receipt["runnerSha256"] == "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283",
                    "Execution binding/resource failure")
            for path in directory.rglob("*"):
                if path.is_file():
                    path.chmod(0o444)
            executions.append({"path": str(receipt_path), "sha256": sha(receipt_raw),
                "exitCode": receipt["exitCode"], "command": receipt["command"],
                "logSha256": receipt["logSha256"],
                "minimumObservedFreeRamBytes": receipt["memory"]["minimumObservedFreeRamBytes"],
                "interpretation": "PASS" if receipt["exitCode"] == 0 else "PRESERVED_FAILED_ATTEMPT_NOT_A_PASS"})
        # Child checkers run via -c/import adapters; bind their actual known receipts too.
        controller = load(HERE / "controller-validation-001.json")
        for row in controller["wrapperRejections"]:
            raw = frozen(row["receipt"]["path"], row["receipt"]["sha256"])
            receipt = json.loads(raw)
            frozen(Path(row["receipt"]["path"]).parent / "output.log", receipt["logSha256"])
        execution_binding = freeze_json(HERE / "execution-bindings-001.json", {
            "executions": executions, "wrapperRejections": controller["wrapperRejections"],
            "limits": "Includes failures honestly. Final freeze/verifier execution receipts are separate because they complete after this snapshot."})
        preflight = load(HERE / "audit-configs-001" / "preflight.json")
        forecast = load(HERE / "capacity-measurement-001.json")
        full = load(PREP / "complete-record-trial-003" / "complete-record-capacity-001.json")
        complete = load(HERE / "complete-verification-001.json")
        wrapper = HERE / "protocol-001" / "run-step-b134-001.ps1"
        handoff = f"""B134 NEUTRAL PREPARATION: VERIFIED STATIC FORECAST, NOT REVIEW ADMISSION

FINAL ROOT
{HERE}
Use only protocol-001\\run-step-b134-001.ps1 -> step-b134-001.py,
audit-configs-001 and prompts-001 under this final root.
All earlier trials, helpers and failed receipts are preserved, not executable deliverables.

BOUNDARIES
No teaching assessment or edits, comparison selection for a reviewer, reviewer launch,
delegation, commit, push, publication or next batch. Governing issue #60 was read.
Candidate ba80afffc20a72d31be68b355b6f90aab36a5726; sole parent
e17cb97c53ca4e3193dae5e11b52ba517fe86e76. Clean signed snapshot independently rechecked.
Actual later coordinator packet proof fb95e655419fe9ecc0465ac565fb309397fb8843c22362b08cf5a1feda4d478a
is pinned in every audit config and the controller before live reviewer admission.
The authoritative assignment and admission are hash-bound; copied brief is in the parent directory.

COUNTS AND COMPLETE SOURCES
{complete['packetFiles']} packet files plus SHA256SUMS; original full-record trial has {complete['fullTrialFiles']}.
One new card 紫, pending row831, title purple; violet, and strokes\\紫.json.
One unchanged-identity existing words\\紫.md, full before/after, exactly one reciprocal wrapper.
1261 baseline and1262 candidate kanji articles; every candidate article is independently requestable.
8745 baseline /8747 candidate runtime entries in all nine manifest groups.
7888 unchanged baseline files; non-files groups unchanged. Complete runtime summary is a
disclosed neutral direct-manifest derivative, NOT an invented signed author companion file.
Manifest2a3373ec1a529cfcd8f1b1bc5686915e4335facc62a1f593b94ed26914273a77;
contentVersion6b34f159e96c078c. Published remains271/1228,957 remaining; draft is not delivery.

All399 complete JMdict families, every field, remain in core. All182 predicates,
full original selection/query provenance and zero matches are in the core.
Four complete signed original selections, canonical-equal union399 JMdict/59 KD,
all deduplication exact on complete-record canonical equality. No semantic trimming.
All59 KD records retain order in the prescribed projection: drop only codepoint,
dic_number,query_code, non-English m_lang meanings and pinyin/korean_r/korean_h/vietnam
readings. All other fields/attributes, literal/radical/all misc/Japanese readings/
English meanings/nanori retained. Sixteen unauthorized-change rejection controls passed.
Full originals remain in the packet and source-contract. Full KD file is NOT authorized
as a whole-file read;59 complete original record units, one per literal, are requestable.
Three complete derived-index optional units: xml-presentation,font-cmap,dictionary-index.
All62 whole optional units were individually requested, built, byte-audited and budgeted.
Largest optional unit13983 <=20000 shared allowance, envelopes included.
Necessary evidence that cannot fit prevents review closure: no partial chain/message,
truncation, substitution, ignored request, reselection or fictional read.
Full candidate title index plus exact one-line deletion delta represents entire baseline;
both original full indices remain local. Do not claim a fictional raw-baseline read.
Two complete reused B132-survey Kotobank/Weblio extracts preserve actual URLs/dates/hashes,
all named Weblio sections and complete Kotobank body. No new retrieval claimed.
Raw HTML remains local; missing historical glyph images are unavailable, not reconstructed.
No author analysis, pair dispositions/reasons, scan matches or earlier review material in inputs.

MEASURED CAPACITY FORECAST, NOT ACTUAL TOKEN MEASUREMENTS
Complete-record core was built and measured FIRST: {full['coreSources']} sources/
{full['coreSegments']} segments/{full['coreSegmentBytes']} bytes; core forecast {full['coreTokens']}.
D25/E10 startup{full['trials'][0]['startupPeak']} exceeds700000 by{full['trials'][0]['excess']}.
For full KD only, the inherited B133 capacity004 full-kd coefficient is conservatively1.0.
Therefore the exact prescribed B133004 projection/derived-index fallback was applied.
Final core {forecast['coreSources']} sources/{forecast['coreSegments']} segments/
{forecast['coreSegmentBytes']} bytes; payload{forecast['coreCost']['payloadBytes']},
envelopes{forecast['coreCost']['envelopeBytes']}; core forecast{forecast['coreTokens']}.
Largest segment{forecast['maxSegmentBytes']} bytes (<16000), complete sources in order.
D/E | maximum article bytes | article forecast incl envelopes | optional | startup | outcome
"""
        for row in forecast["trials"]:
            handoff += (f"D{row['caps']['D']}/E{row['caps']['E']} | {row['articleUpper']['payloadBytes']} | "
                        f"{row['articleUpper']['tokens']} | 20000 | {row['startupPeak']} | "
                        f"{'PASS_ESTIMATE' if row['passes'] else 'HOLD'}\n")
        handoff += f"""Chosen first passing pair D<=25/E<=10, maxima not quotas; startup625929,
74071 forecast headroom. Identical rubric/source access and disclosure for both families.
Article bound is selection-independent largest additive article+solo-envelope costs in
disjoint eligibility groups; no comparisons suggested. D eligible1219/E eligible39.
B131 coefficients x1.10: docs.354,jlpt.374,cards.502,evjson.522,extract.446,
JMdict.543,titleidx.531; KD projection.715; optional full KD.60; envelopes.574.
Every JSON, all diffs/checks use evjson. Bootstrap80000 includes instructions;
report30000; optional20000; selected max extension172913 incl optional reserve.
Actual model/long_context, exact maxPromptTokens telemetry, zero compaction and whole
core audit remain mandatory. Pre-phase2 lastInputTokens+7000+actual selected extension
forecast+30000 <=740000 Claude /710000 GPT, otherwise HOLD without sending phase2.
Nominal windows alone never authorize a run. Forecast passes are not runtime measurements.

SERIAL PROTOCOL AND EXACT RUNNABLE COMMANDS
$w = '{wrapper}'
pwsh -NoProfile -File $w -Action admit -Model claude -InputPath '<absolute-fresh-request.json>'
pwsh -NoProfile -File $w -Action launch -Model claude -SessionId '<actual-session-id>' -InputPath '<actual-admission.json>'
pwsh -NoProfile -File $w -Action phase1 -Model claude -SessionId '<actual-session-id>'
pwsh -NoProfile -File $w -Action final -Model claude -SessionId '<actual-session-id>'
pwsh -NoProfile -File $w -Action accept -Model claude -InputPath '<absolute-frozen-adjudication.json>'
Only after Claude is accepted and no reviewer active, repeat with -Model gpt using
fresh full status/roster observations and actual new GPT session ID. No retries,
confirmations or changed-candidate authorization here. Controllers never launch/message.
Fresh admission request JSON has exactly statusPath,rosterPath,observedAt. Paths absolute;
observation UTC timezone-aware and age<120s, rechecked after expensive verification.
Complete get_sessions_status and list_sessions_and_chats snapshots: unique equal IDs/counts;
all non-coordinator sessions idle and not running, no unknown/busy sessions. RAM>2GiB;
actual report directories absent outputs, empty/writable exclusive create/readback tested.
Admission is not a reservation. Coordinator launches only after those checks.
Phase1 full core read, then independently selected complete D/E/O lines, including
'D: none','E: none','O: none' when empty. Coordinator mechanically prepares extension;
send ENTIRE frozen returned phase2-message unchanged to the SAME reviewer only after gates.
Only exact full view chain reads in order, single report create/readback and two coordinator
messages; no shell/search/web/agents/parallel/out-of-chain sources. Reached segment rereads allowed.
Completion is the bare verdict enum only. Mechanical validity is never semantic acceptance.
Frozen adjudication JSON: candidate,run,finalSha256,reportSha256,claimsAdjudicated:true,
verdict,claimChecks; each claimCheck nonempty claim/evidence/disposition. Adjudicate every
material claim/ambiguity and match report verdict/hash. Accepted NEEDS FIX/UNVERIFIED review
is not teaching acceptance. Actual final report directories remain empty and writable.

EXACT PAIRED KICKOFFS
"""
        for family, spec in preflight["runs"].items():
            validate_report_destination(spec)
            handoff += (f"\n{family.upper()} {spec['run']}\nlaunch = {json.dumps(spec['launch'])}\n"
                f"prompt = {spec['prompt']['path']}\nprompt SHA256 = {spec['prompt']['sha256']}\n"
                f"instruction bytes = {spec['prompt']['bytes']} (within80000 bootstrap)\n"
                f"kickoff = {spec['kickoff']['path']}\nkickoff SHA256 = {spec['kickoff']['sha256']}\n"
                f"report (absent) = {spec['report']}\nEXACT KICKOFF STRING (no trailing newline):\n"
                + spec["kickoffText"] + "\n")
        handoff += """
CHANGES FROM ACCEPTED B133004 PRECEDENT
B134-only identities/candidate/base/counts/paths, one target/support and two reused captures.
D25/E10 now first passing (B133 usedD10/E5); parser/tests/prompts use actual chosen caps.
59 KD originals+3 derived-index units, not83+3; all399 JMdict, not515.
Complete source-selection provenance is explicitly a separate in-core source, even though
derived xml-presentation/index are optional. Exact one-line baseline delta, not three.
Full runtime summary is generated from exact signed manifests because B134 coordinator
proof shape is direct fullRuntime/preservation objects, unlike B133's captured companion.
Final B133 step004/wrapper005/auditor/checker/runtime implementations retained with new
B134 bindings. Capacity004 helper filenames retained solely for arithmetic compatibility
inside the new isolated directory; KD59 invariant adapted. PYTHONUTF8=1 explicit in wrapper
and controller children. No new source-reduction mechanism or relaxed runtime gate.

VALIDATION AND RESOURCES
Independent complete originals/source selections/candidate/base/packet/chain byte verification.
16 projection rejection controls. Seven inherited synthetic controls, eight focused controls,
six optional controls; full synthetic admit/launch-observation/phase1/final/accept, real guarded
report checker, exclusive report create/readback, four final mutation rejections, all five
actual wrapper action rejections. All62 optional units individually tested; independent
five-pair arithmetic/envelope bounds and exact both-family phase2 capacity boundaries passed.
Actual extension-preparer over-allowance call rejected BEFORE any partial chain/preflight/
message. Readiness rejects existing output/nonempty/readonly directories; E10 passes/E11 rejects.
Fake observations never authorize a live review. No actual reviewer launched.
Pinned runner52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283;
RAM guard46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84.
python-B,UTF8,no-bytecode; admit>2GiB; sample.25s/abort<1GiB; child waits<=.1s;
terminate/kill<=10s each, own child only. Peaks cover verifier Python, not descendants.
Preserved failed attempts: initial prefix, writable reused survey capture, B133-shaped runtime
companion assumption and consequent capacity run before a valid packet; all corrected in new
helpers/trials. No failed receipt is represented as passing. Earlier failed trial sources remain.

LIMITATIONS (UNALTERED)
Author-gates-001:38 'not mentioned in Notes' quiz warnings, superseded; author-gates-002 and
committed-gates-001:0 warnings. Eleven pre-existing fallback cards remain noted.
Reading model:0 production/0 padded-session hits; latent smaller-pool 紫/包 collision for
historicalつつむ not drawable in checked pools; historical scope unresolved.
All three cmaps contain紫/components; search-only茈 U+8308 absent in all3; bounded
cmap checks are not rendered fallback acceptance. 字通11 strokes versus pinned KD/KanjiVG12.
Invented non-etymological mnemonic. Default diff--check flagsCRLF; CR-at-EOL-aware check passes.
verify_committed_bytes_134.py/check_reading_134.py read scratch-134 inputs; coordinator rechecked.
No arbitrary/custom/multiple-borrow pool,Kotlin/native/device,rendering,whole-set or publication
acceptance. Published count remains271/1228,957 remaining.

PRIMARY SHA256 BINDINGS
"""
        key_paths = [
            HERE / "packet" / "SHA256SUMS.json", HERE / "core-chain-001.json",
            HERE / "capacity-measurement-001.json", HERE / "audit-configs-001" / "preflight.json",
            HERE / "protocol-001" / "step-b134-001.py", wrapper,
            PREP / "complete-record-trial-003" / "source-contract" / "contract.json",
            HERE / "complete-verification-001.json", HERE / "controller-validation-001.json",
            HERE / "optional-validation-001.json", HERE / "readiness-and-hold-validation-001.json",
            HERE / "execution-bindings-001.json"]
        for path in key_paths:
            handoff += str(path) + "\n  " + sha(frozen(path)) + "\n"
        write_frozen(HERE / "COORDINATOR-HANDOFF-001.txt", handoff.encode())
        # Freeze only this preparation's files; actual report directories stay writable/empty.
        manifest = {}
        for path in PREP.rglob("*"):
            if path.is_file():
                path.chmod(0o444)
                manifest[path.relative_to(PREP).as_posix()] = sha(frozen(path))
                guard.check()
        binding = freeze_json(PREP / "PREPARATION-SHA256SUMS-001.json", manifest)
        print(json.dumps({"preparationManifest": binding, "handoff": {
            "path": str(HERE / "COORDINATOR-HANDOFF-001.txt"),
            "sha256": sha(frozen(HERE / "COORDINATOR-HANDOFF-001.txt"))},
            "executionBindings": execution_binding, "files": len(manifest)}))
    finally:
        require(not guard.finish()["breach"], "Handoff freeze RAM breach")


if __name__ == "__main__":
    main()
