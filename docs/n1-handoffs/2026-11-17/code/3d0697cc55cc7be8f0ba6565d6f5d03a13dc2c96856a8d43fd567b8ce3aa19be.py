"""Preserve the failed fresh-review attempt without treating it as review evidence."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

ROOT = WS / "scratch-134" / "review"
FAILED = ROOT / "fresh-independent-001"
ORIGINAL = ROOT / "neutral-preparation-001" / "projected-successor-001"
OUT = ROOT / "fresh-independent-001-rejection"
SESSION = "73081d97-2224-47e3-a8de-113e7dd1d7a2"


def identities(raw, child, key):
    root = ET.fromstring(raw)
    values = [node.findtext(key) for node in root.findall(child)]
    require(values and all(values) and len(values) == len(set(values)),
            "Missing or duplicate dictionary identities")
    return set(values)


def main():
    require(not OUT.exists(), "Preserve the previous rejection receipt")
    guard, _ = start_guard("B134 failed fresh-review evidence")
    try:
        preparation = frozen(
            FAILED / "preparation.json",
            "dcda377f17fe94f9678b547d000f8de8b8bae4f680e66a50a5a187d4362700c8",
        )
        chain_raw = frozen(
            FAILED / "chain.json",
            "6a81c496f08e0ff96bd07f59e32c81bae974a84ad920c1c590867941626f57d2",
        )
        chain = json.loads(chain_raw)
        source_names = {row["source"] for row in chain["sources"]}
        original_sums = json.loads(frozen(
            ORIGINAL / "packet" / "SHA256SUMS.json",
            "12cabfd9f51797c02f77c9513ad5ae6fe7f57aeceb6d180bf3cf24baf6c5c13e",
        ))
        omissions = {}
        for filename, child, key in (
            ("jmdict-families.xml", "entry", "ent_seq"),
            ("kanjidic2-records.xml", "character", "literal"),
        ):
            name = "evidence/" + filename
            original = identities(frozen(ORIGINAL / "packet" / name, original_sums[name]),
                                  child, key)
            supplied = identities(frozen(FAILED / "sources" / name), child, key)
            omissions[name] = {
                "originalRecords": len(original),
                "suppliedRecords": len(supplied),
                "sharedRecords": len(original & supplied),
                "omittedOriginalIdentities": sorted(original - supplied),
            }
        response = frozen(FAILED / "sources" / "evidence" / "author-response.txt")
        require("evidence/author-response.txt" in source_names
                and b"B134 author response" in response, "Author-response failure changed")
        missing_required = [name for name in (
            "repo/kanji/古.md", "repo/kanji/右.md", "repo/kanji/川.md",
            "evidence/title-index.txt",
        ) if name not in source_names]
        event_path = Path.home() / ".copilot" / "session-state" / SESSION / "events.jsonl"
        event_raw = event_path.read_bytes()
        require(event_raw.endswith(b"\n"), "Incomplete event line")
        events = [json.loads(line) for line in event_raw.splitlines()]
        starts = [row["data"] for row in events if row["type"] == "session.start"]
        usages = [row["data"]["usage"] for row in events
                  if row["type"] == "session.usage_record"]
        compactions = [row for row in events if row["type"].startswith("session.compaction")]
        calls = [row["data"] for row in events if row["type"] == "tool.execution_start"]
        require(len(starts) == 1 and starts[0].get("contextTier") is None
                and usages and {row.get("maxPromptTokens") for row in usages} == {200000}
                and compactions, "Observed runtime failure changed")
        report = WS / "reports-134" / "fresh-claude-001.md"
        require(not report.exists(), "A report exists and needs separate preservation")
        event_ref = write_frozen(OUT / "events.jsonl", event_raw)
        result = {
            "status": "REJECTED_PREPARATION_AND_LAUNCH_NOT_CARD_VERDICT",
            "session": SESSION,
            "candidate": json.loads(preparation)["candidate"],
            "preparationSha256": sha(preparation),
            "chainSha256": sha(chain_raw),
            "eventSnapshot": event_ref,
            "eventCount": len(events),
            "selectedModel": starts[0].get("selectedModel"),
            "contextTier": starts[0].get("contextTier"),
            "observedMaxPromptTokens": sorted({row["maxPromptTokens"] for row in usages}),
            "actualPeakInputTokens": max(row["inputTokens"] for row in usages),
            "compactions": [{"type": row["type"], "timestamp": row["timestamp"],
                             "success": row["data"].get("success"),
                             "tokenLimit": row["data"].get("tokenLimit")} for row in compactions],
            "toolCounts": {name: sum(row["toolName"] == name for row in calls)
                           for name in sorted({row["toolName"] for row in calls})},
            "authorResponseSha256": sha(response),
            "dictionaryOmissions": omissions,
            "missingRequiredSources": missing_required,
            "reportExists": False,
            "decision": "No admissible review, verdict, delivery credit, or publication. "
                        "The stopped session is not to be resumed as an independent reviewer. "
                        "Fresh immutable preparation and a new explicitly long-context identity "
                        "require verified runtime admission before core reads.",
            "limits": "Post-failure observation, not a retroactive admission. "
                      "Packet inclusion does not prove a particular leaked source was read.",
            "producerSha256": sha(Path(__file__).read_bytes()),
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach during rejection capture")
    result["memory"] = memory
    print(json.dumps(freeze_json(OUT / "rejection.json", result)))


if __name__ == "__main__":
    main()
