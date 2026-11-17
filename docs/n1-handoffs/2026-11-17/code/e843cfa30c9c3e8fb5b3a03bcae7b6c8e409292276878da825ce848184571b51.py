"""Preserve prior dictionary tool returns without refetching or copying author analysis."""
import json
from pathlib import Path

from common import WS, freeze_json, require, sha, write_frozen

AUTHOR = "3fb8a285-ebf3-456e-89ed-5e4b77b0f0a1"
CALLS = {
    "標": "call_KIdNhCY04l3qADdFJDh0U3Lz",
    "紀": "call_fpo9UGZt3pVJWxdi1t5jYaBE",
    "鏡": "call_Dma9QxEmJA6dA8lrlwfb2Kvc",
    "限": "call_1Pf6Lq0WPrmklU2SgdWWsw5S",
    "境": "call_kViMtDAQX6dC79iqycntjXBm",
    "界": "call_MOXVbWP3NSiaPQu6RSDXKgng",
}


def main():
    output = WS / "scratch-123" / "review" / "reconciliation-source-captures-001"
    require(not output.exists(), "Preserve the existing capture")
    events = Path.home() / ".copilot" / "session-state" / AUTHOR / "events.jsonl"
    source = events.read_bytes()
    require(source.endswith(b"\n"), "Incomplete event prefix")
    starts, results = {}, {}
    for raw in source.splitlines(keepends=True):
        event = json.loads(raw)
        data = event.get("data", {})
        call = data.get("toolCallId")
        if call not in CALLS.values():
            continue
        kind = event.get("type")
        if kind == "tool.execution_start":
            require(call not in starts and data["toolName"] == "web_fetch",
                    "Duplicate or unexpected source call")
            starts[call] = (event, raw)
        elif kind == "tool.execution_complete":
            require(call not in results and data["success"] is True,
                    "Duplicate or unsuccessful source result")
            require(isinstance(data["result"]["content"], str), "Unexpected source content")
            results[call] = (event, raw)
    require(starts.keys() == results.keys() == set(CALLS.values()), "Source calls incomplete")
    records = []
    for number, (character, call) in enumerate(CALLS.items(), 1):
        start, start_raw = starts[call]
        result, result_raw = results[call]
        content = result["data"]["result"]["content"].encode("utf-8")
        url = start["data"]["arguments"]["url"]
        require(content.startswith(f"Contents of {url}:".encode("utf-8")),
                "Result URL does not match requested source")
        prefix = f"{number:02d}-{character}"
        records.append({
            "character": character, "url": url, "callId": call,
            "startedAt": start["timestamp"], "completedAt": result["timestamp"],
            "request": write_frozen(output / f"{prefix}-request-event.json", start_raw),
            "result": write_frozen(output / f"{prefix}-result-event.json", result_raw),
            "content": write_frozen(output / f"{prefix}-tool-result.txt", content),
            "sourceLabel": f"external-sources/{prefix}-tool-result.txt",
            "limits": "Verbatim previously returned web_fetch text, not raw HTML or a claim "
                      "of a complete page. Any truncation notice remains unchanged.",
        })
    script = Path(__file__)
    script.chmod(0o444)
    print(json.dumps(freeze_json(output / "provenance.json", {
        "batch": 123, "status": "CAPTURED", "authorSession": AUTHOR,
        "eventPrefixBytes": len(source), "eventPrefixSha256": sha(source),
        "sources": records, "newNetworkRequests": 0,
        "scriptSha256": sha(script.read_bytes()),
        "scope": "Only original tool requests and successful source-return events; "
                 "no author prose, other review, adjudication or verdict is copied.",
    })))


if __name__ == "__main__":
    main()
