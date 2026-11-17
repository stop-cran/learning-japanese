import importlib.util
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from common_134 import HERE, sha, start_guard, write

OUT = HERE / "reconciliation-external-001"
SOURCE = HERE.parent / "scratch-133" / "source-reconciliation-001" / "gather.py"
assert sha(SOURCE.read_bytes()) == "ba6dc1168c63c0495aac7c6837fb6602844b9cf107e34482236e222eb31da31a"
spec = importlib.util.spec_from_file_location("prior_b133_extractor", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
url = "https://kotobank.jp/word/" + urllib.parse.quote("隻")
guard = start_guard()
receipt = {"requestedUrl": url, "character": "隻", "startedAt": datetime.now(timezone.utc).isoformat(),
           "timeoutSeconds": 20, "totalDeadlineSeconds": 45, "maxBytes": 3 * 1024**2}
try:
    deadline = time.monotonic() + 45
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        chunks, size = [], 0
        while True:
            guard.check()
            if time.monotonic() >= deadline:
                raise TimeoutError("Capture exceeded total deadline")
            chunk = response.read(65536)
            if not chunk:
                break
            size += len(chunk)
            if size > 3 * 1024**2:
                raise ValueError("Capture exceeded byte limit")
            chunks.append(chunk)
        raw = b"".join(chunks)
        receipt.update(finalUrl=response.geturl(), httpStatus=response.status)
    write(OUT / "隻-kotobank.html", raw)
    parser = module.Extractor()
    parser.feed(raw.decode("utf-8"))
    text = parser.text().encode()
    write(OUT / "隻-kotobank.txt", text)
    write(OUT / "隻-kotobank.images.json", parser.images)
    receipt.update(status="complete-capture", htmlSha256=sha(raw), htmlBytes=len(raw),
                   textSha256=sha(text), textLines=len(text.decode().splitlines()),
                   imageCount=len(parser.images), extractorSha256=sha(SOURCE.read_bytes()),
                   limits="Text excludes script/style/noscript; image bytes, CSS visibility and layout not inspected.")
except (OSError, ValueError, UnicodeError, urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
    receipt.update(status="FAILED", errorType=type(error).__name__, error=str(error))
    if isinstance(error, urllib.error.HTTPError):
        body = error.read(3 * 1024**2)
        write(OUT / "隻-kotobank.failed-response.html", body)
        receipt["failedResponseSha256"] = sha(body)
    raise
finally:
    receipt["completedAt"] = datetime.now(timezone.utc).isoformat()
    write(OUT / "隻-kotobank.receipt.json", receipt)
    write(OUT / "memory.json", guard.finish())
