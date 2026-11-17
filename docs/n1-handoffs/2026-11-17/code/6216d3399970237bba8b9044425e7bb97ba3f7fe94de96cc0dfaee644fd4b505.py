"""Write one user message that a reviewer session received, byte-exact (UTF-8), to a file.

    python n1_prompts.py --session SID --list
    python n1_prompts.py --session SID --index 2 --out prompts\\confirm-claude.txt

The text is the event's `content` field (what the coordinator sent), not the runtime-wrapped
`transformedContent`. The SHA-256 printed here equals the `userMessages` hash in n1_audit.py output.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

SESSIONS = Path(r"C:\Users\stop-\.copilot\session-state")


def messages(session):
    found = []
    with open(SESSIONS / session / "events.jsonl", encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "user.message":
                found.append((e.get("timestamp") or "", e["data"].get("content") or "", e["data"].get("delivery")))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--index", type=int)
    ap.add_argument("--out")
    a = ap.parse_args()
    found = messages(a.session)
    if a.list or a.index is None:
        for i, (ts, content, delivery) in enumerate(found):
            data = content.encode("utf-8")
            print("%d  %s  %-9s %5d chars  %s  %s" % (i, ts, delivery, len(content), hashlib.sha256(data).hexdigest()[:16],
                                                    content[:60].replace("\n", " ")))
        return 0
    if not a.out:
        sys.exit("--out is required with --index")
    out = Path(a.out)
    if out.exists():
        sys.exit("refusing to overwrite %s" % out)
    ts, content, _ = found[a.index]
    data = content.encode("utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print("%s  %d chars  sha256 %s -> %s" % (ts, len(content), hashlib.sha256(data).hexdigest(), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
