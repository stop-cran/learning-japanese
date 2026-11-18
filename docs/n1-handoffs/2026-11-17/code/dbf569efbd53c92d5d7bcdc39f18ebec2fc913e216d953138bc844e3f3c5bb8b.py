"""Verify actual preparation, preserve synthetic isolation, freeze the bounded handoff."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, load_module, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUNTIME = ROOT / "authorization-runtime-002" / "b134_authorized_confirmation_v1.py"
RUNTIME_SHA = "65956a69b4f0c0cf4849228f8a554cd9c6d13afefdcf4a1427682cfea24964a1"
frozen(RUNTIME, RUNTIME_SHA)
m = load_module("b134_authorized_handoff_validation", RUNTIME)
t = m.legacy


def small(ref):
    return {key: ref[key] for key in ("path", "sha256")}


def main():
    require(sha((HERE / RUNTIME.name).read_bytes()) == RUNTIME_SHA, "Tested source differs")
    require(m.AUTH["sha256"] == "4d69ed0c6e0476b38bba3e22b31b959178d417d8b1ecfaa7d29221660da167cb",
            "Authorization pin changed")
    active = {"status": "PREPARATION_READY_NOT_ADMITTED", "producer": t.ref(RUNTIME),
              "authorization": m.AUTH, "source_user_message": m.SOURCE, "scopeHold": m.HOLD,
              "publicationAccepted": False, "actualReviewerAdmissionPerformed": False,
              "runOrder": ["claude", "gpt"], "families": {}}
    old_kickoffs = {}
    for family in ("claude", "gpt"):
        path = ROOT / f"authorized-{family}-confirmation-002" / "preflight.json"
        record, config, spec, chain = t.preflight(path)
        raw = (Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl").read_bytes()
        m.verify_retained_prefix(record, raw)
        context = t.context(t.parse_events(raw), family, record["session"], record["dossierBound"])
        old_record, old_config, _, _ = m.old_preflight(family)
        old_kickoffs[family] = frozen(old_config["kickoff"]).decode("utf-8")
        require(not Path(config["report"]).exists(), "Actual reviewer report must not exist yet")
        active["families"][family] = {
            "run": record["run"], "rawEventSession": record["session"],
            "preflight": t.ref(path), "request": record["spec"], "config": record["config"],
            "chain": record["chain"], "prompt": t.ref(config["prompt"]), "kickoff": t.ref(config["kickoff"]),
            "kickoffText": frozen(config["kickoff"]).decode("utf-8"), "reportDestination": config["report"],
            "sources": len(chain["sources"]), "segments": len(chain["segments"]),
            "contextForecastNotMeasurement": context, "continuation": spec["continuation"],
        }
    # Bind the actual original parent tool's target namespace, rather than guessing
    # that raw event session UUIDs are interchangeable with desktop targets.
    parent_events = (Path.home() / ".copilot" / "session-state" / t.COORDINATOR / "events.jsonl")
    targets = {family: [] for family in old_kickoffs}
    for line in parent_events.open(encoding="utf-8"):
        if "send_session_message" not in line:
            continue
        event = json.loads(line)
        if event.get("type") != "assistant.message":
            continue
        for call in event.get("data", {}).get("toolRequests", []):
            if str(call.get("name", "")).removeprefix("functions.") != "send_session_message":
                continue
            args = call.get("arguments", {})
            for family, kickoff in old_kickoffs.items():
                if args.get("message") == kickoff:
                    targets[family].append({"parentTarget": args["session_id"],
                                            "priorToolCallId": call["toolCallId"],
                                            "priorParentEventId": event["id"]})
    for family in targets:
        require(len(targets[family]) == 1, "Original parent target is not uniquely bound: " + family)
        active["families"][family]["observedParentTransport"] = targets[family][0]
    tests = ROOT / "authorization-controls-execution-004"
    receipt_raw = (tests / "receipt.json").read_bytes()
    receipt = json.loads(receipt_raw)
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
            and receipt["cleanupError"] is None and not receipt["memory"]["breach"]
            and receipt["runnerSha256"] == "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
            and sha((tests / "output.log").read_bytes()) == receipt["logSha256"],
            "Final guarded control receipt/log mismatch")
    synthetic = list(HERE.glob("synthetic-*/claude-accept/acceptance.json"))
    synthetic += list(HERE.glob("synthetic-*/gpt-accept/acceptance.json"))
    require(synthetic and all(json.loads(p.read_bytes())["producer"]["sha256"] != RUNTIME_SHA for p in synthetic),
            "A synthetic acceptance claims the selected actual producer")
    active["controls"] = {"methodsPassed": 8, "execution": str(tests),
                           "receiptSha256": sha(receipt_raw), "logSha256": receipt["logSha256"],
                           "syntheticAcceptanceIsolationChecked": len(synthetic)}
    freeze_json(HERE / "active-artifacts.json", active)
    write_frozen(HERE / "HANDOFF.txt", (HERE / "HANDOFF-template.txt").read_bytes())
    names = ["authorization-continuation-prep-001", "authorization-runtime-001", "authorization-runtime-002",
             "authorized-claude-confirmation-001", "authorized-claude-confirmation-002",
             "authorized-gpt-confirmation-001", "authorized-gpt-confirmation-002",
             "authorization-capture-execution-001",
             "authorization-stage-execution-001", "authorization-stage-execution-002",
             "authorization-claude-prepare-execution-001", "authorization-claude-prepare-execution-002",
             "authorization-gpt-prepare-execution-001", "authorization-gpt-prepare-execution-002",
             "authorization-controls-execution-001", "authorization-controls-execution-002",
             "authorization-controls-execution-003", "authorization-controls-execution-004"]
    files = {}
    for name in names:
        folder = ROOT / name
        require(folder.is_dir() and not folder.is_symlink(), "Unexpected evidence root")
        for path in sorted(folder.rglob("*")):
            require(not path.is_symlink(), "Unexpected linked evidence")
            if path.is_file():
                path.chmod(0o444)
                files[str(path)] = sha(frozen(path))
    inventory = freeze_json(HERE / "frozen-files.json", {
        "status": "PREPARATION_ONLY_NOT_ADMISSION_OR_REVIEW_ACCEPTANCE",
        "files": files, "excludes": ["this inventory", "currently-running final sealing receipt/log"],
        "selectedProducer": active["producer"], "authority": m.AUTH,
        "syntheticResultsAreNotActualProof": True,
    })
    require(all(sha(frozen(path)) == digest for path, digest in files.items()), "Final inventory changed")
    print(json.dumps({"handoff": t.ref(HERE / "HANDOFF.txt"),
                      "activeArtifacts": t.ref(HERE / "active-artifacts.json"),
                      "inventory": small(inventory), "files": len(files), "families": {
                          f: {"target": v["observedParentTransport"]["parentTarget"],
                              "preflight": v["preflight"], "sources": v["sources"], "segments": v["segments"],
                              "lastInput": v["contextForecastNotMeasurement"]["lastInputTokens"],
                              "dossierBound": v["contextForecastNotMeasurement"]["dossierBound"],
                              "forecast": v["contextForecastNotMeasurement"]["forecast"],
                              "limit": v["contextForecastNotMeasurement"]["limit"]}
                          for f, v in active["families"].items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
