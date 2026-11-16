import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from b131_common import HERE, sha, start_guard, write
from survey_b131 import CHARS, PageText

OUT = HERE / "external-003"
guard = start_guard()
captures = []
try:
    for ch in CHARS:
        for provider, prefix in (("kotobank", "https://kotobank.jp/word/"), ("weblio", "https://www.weblio.jp/content/")):
            url = prefix + urllib.parse.quote(ch)
            path = OUT / f"{ch}-{provider}.html"
            try:
                with urllib.request.urlopen(url, timeout=30) as response:
                    raw, final = response.read(), response.url
                write(path, raw)
                parser = PageText()
                parser.feed(raw.decode("utf8"))
                text = ("\n".join(parser.parts) + "\n").encode()
                write(path.with_suffix(".txt"), text)
                captures.append({"character": ch, "provider": provider, "url": url, "finalUrl": final,
                    "capturedAt": datetime.now(timezone.utc).isoformat(), "localRawCapture": str(path),
                    "rawSha256": sha(raw), "rawBytes": len(raw), "textSha256": sha(text)})
            except (OSError, UnicodeError) as error:
                captures.append({"character": ch, "provider": provider, "url": url, "error": repr(error)})
            guard.check()
    write(OUT / "bindings.json", {"captures": captures, "fullCapturesLocalOnly": True})
    print(captures)
finally:
    write(OUT / "memory.json", guard.finish())
