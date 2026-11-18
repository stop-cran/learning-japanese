"""Verify the inherited, claim-free B133 fresh Claude bootstrap and freeze its CONFIRM-002 spec."""
import json
from pathlib import Path

from b133_fresh_confirmation import CANDIDATE_002, PLANNED_RUN, binding, observation_path
from common import freeze_json, frozen, require, sha, start_guard, write_frozen
from confirm_b133_v2 import OUT

SESSION = "928ed3cb-7f93-476e-85cb-1b7b6f05f1ef"
BOOTSTRAP = (
    "This is session provisioning only, not a review and not authorization to read evidence. "
    "The N1 coordinator is 2451b10d-02a9-46ab-82d5-d90993f0cb8b. Use no tools, inspect no files, "
    "contact no sessions, and make no changes. Reply READY and stop (an optional task_complete "
    "containing READY is permitted). The coordinator will later deliver the separately admitted "
    "frozen confirmation kickoff directly to this session. This bootstrap supplies no linguistic "
    "or review claims."
)
JMDICT = "docs/n1-sources/batch-133-reconciliation/source/jmdict-complete-families.xml"
EXTRA = ("kanji/水.md", JMDICT)
REPORTS = Path(r"C:\Users\stop-\n1-kanji-workspace\reports-133")
BASIS = (
    "The original reviewer's B133 initial review reported CLEAN with C1-C3 and O1-O4; it was accepted as "
    "evidence only, not as teaching approval. Coordinator adjudication decided 18 direct pair decisions. "
    "Owner-signed revision 110b4ffb6af078eb2adb00645db4c9e0bd6db188, the sole child of freeze ad047ace, "
    "appended 11 qualified quiz exclusions: 鉛 [鉱,遅,円], 滝 [速,声,激,岩,険], 琴 [具,糸,緒]. The original "
    "reviewer's CONFIRM-001 on 110b4ffb (evidence/claude-confirm-001-report.md, accepted with coordinator "
    "adjudication evidence/claude-confirm-001-adjudication.json) confirmed those precautions, C1-C3, O1-O4 "
    "and the 鉛-具 cross-pair, but did not judge the retained distinctions. The coordinator then replaced the "
    "retained 滝-液 distinction with a qualified direct precaution. Owner-signed revision "
    "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30, the sole child of 110b4ffb, appends only 液 to 滝 "
    "quiz_exclusions with one qualified Note and one 液 citation. diffs/fix.patch is the cumulative teaching "
    "delta from ad047ace; diffs/reconciliation-002.patch is the exact second delta; evidence/revision-proof.json "
    "and evidence/revision-proof-002.json are the mechanical boundary, preservation and committed-gate proofs; "
    "evidence/coordinator-dispositions-002.json lists all 18 decisions (12 precautions added, 6 distinctions "
    "retained) and supersedes evidence/coordinator-dispositions.json only for 滝-液. Confirm every one of the "
    "18 decisions on d7d6cff9 against the supplied complete sections and counterpart cards: each added "
    "precaution and its Note, including the new 滝-液 precaution, its wording and its citation; each retained "
    "distinction (鉛-鉄, 鉛-似, 鉛-倣, 琴-機, 琴-線, 琴-索) as not requiring a precaution, judging each "
    "explicitly; and the 鉛-具 cross-pair. Give the C1-C3 and O1-O4 dispositions on d7d6cff9. Also verify "
    "the five JMdict identities newly cited by the reconciliation Notes (1396980, 1404975, 1380440, 1244950, "
    "1343610) against snapshot/" + JMDICT + "; earlier card citations are outside this delta. Sources are "
    "complete named Kotobank publisher sections, not whole pages, layout or images, plus complete JMdict "
    "families; no fresh KANJIDIC2 or whole-JMdict reread and no web access. Precautions are quiz-safety "
    "guards, not synonymy claims. If a supplied source cannot settle a point, say so precisely rather than "
    "inferring."
)


def events_of(session):
    path = Path.home() / ".copilot" / "session-state" / session / "events.jsonl"
    before = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    require(raw.endswith(b"\n") and before.st_size == after.st_size
            and before.st_mtime_ns == after.st_mtime_ns, "Events changed during inspection")
    return raw, [json.loads(line) for line in raw.splitlines()]


def sources():
    gpt001 = json.loads(frozen(OUT / "N1-B133-GPT-CONFIRM-001-spec.json"))
    gpt002 = json.loads(frozen(OUT / "N1-B133-GPT-CONFIRM-002-spec.json"))
    claude001 = json.loads(frozen(OUT / "N1-B133-CLAUDE-CONFIRM-001-spec.json"))
    require(set(claude001["revisedSources"]) <= set(gpt001["revisedSources"])
            and {row["source"] for row in claude001["additionalSources"]}
            <= {row["source"] for row in gpt001["additionalSources"]}, "Claude 001 sources not covered")
    revised = [*gpt001["revisedSources"], *EXTRA]
    later = {row["source"]: row for row in gpt002["additionalSources"]}
    acceptance = json.loads(frozen(OUT / "N1-B133-CLAUDE-CONFIRM-001-acceptance.json"))
    additional = [*gpt001["additionalSources"],
                  *(later[name] for name in ("evidence/coordinator-dispositions-002.json",
                                             "evidence/revision-proof-002.json", "diffs/reconciliation-002.patch")),
                  {"source": "evidence/claude-confirm-001-report.md", **binding(acceptance["report"]["path"],
                                                                                acceptance["report"]["sha256"])},
                  {"source": "evidence/claude-confirm-001-adjudication.json",
                   **binding(acceptance["adjudication"]["path"], acceptance["adjudication"]["sha256"])}]
    require(len(revised) == len(set(revised))
            and len(additional) == len({row["source"] for row in additional}), "Duplicate source")
    for row in additional:
        frozen(row["path"], row["sha256"])
        require("gpt" not in row["source"].lower(), "Other-family report supplied")
    return revised, additional


def main():
    guard, _ = start_guard("B133 fresh Claude bootstrap and spec")
    try:
        observation = json.loads(frozen(observation_path()))
        raw, events = events_of(SESSION)
        starts = [event["data"] for event in events if event["type"] == "session.start"]
        users = [event["data"]["content"] for event in events if event["type"] == "user.message"]
        messages = [event["data"] for event in events if event["type"] == "assistant.message"]
        calls = [event for event in events if event["type"] == "tool.execution_start"]
        model = observation["telemetry"]["contextProfile"]["selectedModel"]
        require(len(starts) == 1 and starts[0]["sessionId"] == SESSION and starts[0]["selectedModel"] == model
                and starts[0]["contextTier"] == "long_context", "Fresh inherited family or tier differs")
        require(users == [BOOTSTRAP] and len(messages) == 1 and messages[0]["content"] == "READY"
                and not messages[0].get("toolRequests") and not calls
                and not any("compaction" in event["type"] for event in events),
                "Bootstrap did more than claim-free readiness")
        usage = [event["data"]["usage"] for event in events if event["type"] == "session.usage_record"]
        require(len(usage) == 1 and usage[0]["model"] == model, "Unverified actual bootstrap model")
        original = Path.home() / ".copilot" / "session-state" / observation["originalSession"] / "events.jsonl"
        with original.open("rb") as stream:
            require(sha(stream.read(observation["events"]["bytes"])) == observation["events"]["sha256"],
                    "Original accepted-review context prefix changed")
        prefix = write_frozen(OUT / (PLANNED_RUN + "-bootstrap-events.jsonl"), raw)
        revised, additional = sources()
        report = REPORTS / (PLANNED_RUN + ".md")
        require(not report.exists(), "Report destination exists")
        spec = {
            "family": "claude", "run": PLANNED_RUN, "session": SESSION, "candidate": CANDIDATE_002,
            "teachingChange": True, "scope": ["琴", "鉛", "滝"], "revisedSources": revised,
            "additionalSources": additional, "basis": "adjudicated-initial", "priorVerdict": "CLEAN",
            "basisText": BASIS, "originalSession": observation["originalSession"],
            "contextObservation": binding(observation_path()),
        }
        require("your own" not in BASIS.lower() and "B132" not in BASIS, "Misattributed basis")
        spec_binding = freeze_json(OUT / (PLANNED_RUN + "-spec.json"), spec)
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Bootstrap verifier RAM breach")
    print(json.dumps(freeze_json(OUT / (PLANNED_RUN + "-bootstrap.json"), {
        "run": PLANNED_RUN, "session": SESSION, "originalSession": observation["originalSession"],
        "status": "VERIFIED_BOOTSTRAP_NOT_REVIEW_ADMISSION", "model": starts[0]["selectedModel"],
        "contextTier": starts[0]["contextTier"], "inputTokens": usage[0]["inputTokens"],
        "maxPromptTokens": usage[0]["maxPromptTokens"], "prefix": prefix, "spec": spec_binding,
        "revisedSources": len(revised), "additionalSources": len(additional), "memory": memory,
        "scope": "Inherited actual model/tier, one READY bootstrap, no tools or claim evidence. Original "
                 "observed context prefix preserved. The spec widens the original Claude scope to all 18 "
                 "decisions because the fresh context removes the measured capacity reason for excluding the "
                 "retained distinctions. Fresh admission, exact kickoff, complete chain, final execution audit "
                 "and substantive adjudication remain required; this is not confirmation or delivery.",
        "producer": binding(Path(__file__)),
    }, ), ensure_ascii=False))


if __name__ == "__main__":
    main()
