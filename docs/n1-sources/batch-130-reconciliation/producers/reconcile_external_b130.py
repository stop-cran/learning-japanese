import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from b130_common import HERE, REPO, sha, start_guard, write
from survey_b130 import PageText

LOCAL = HERE / "reconciliation-001" / "external"
OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
guard = start_guard()
captures = []
try:
    for ch in "音信城":
        url = "https://kotobank.jp/word/" + urllib.parse.quote(ch)
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            chunks = []
            while True:
                guard.check()
                chunk = response.read(65536)
                if not chunk:
                    break
                chunks.append(chunk)
            raw, final_url = b"".join(chunks), response.url
        path = LOCAL / (ch + "-kotobank.html")
        write(path, raw)
        parser = PageText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(parser.parts).encode("utf-8")
        write(path.with_suffix(".txt"), text)
        captures.append({
            "character": ch, "url": url, "finalUrl": final_url,
            "capturedAt": datetime.now(timezone.utc).isoformat(),
            "rawSha256": sha(raw), "rawBytes": len(raw), "textSha256": sha(text),
            "localRawCapture": str(path),
            "identityStatus": "Captured; substantive entry identity and body require author inspection.",
        })
        print(json.dumps(captures[-1], ensure_ascii=False), flush=True)
    write(OUT / "external-capture-bindings.json", {
        "captures": captures, "completeCapturesCommitted": False,
        "copyrightBoundary": "Complete external responses stay local; only bindings, short attributable excerpts and original analysis may be committed.",
        "transformation": "Complete HTML retained locally and PageText script/style-free extraction; mixed dictionaries remain separately attributed. Image glyphs are not inferred.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
finally:
    write(LOCAL / "memory-001.json", guard.finish())
