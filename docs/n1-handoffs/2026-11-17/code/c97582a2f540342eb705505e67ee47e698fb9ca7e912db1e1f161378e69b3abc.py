"""Capture additive character evidence for the nine held B123 comparisons."""
import datetime
import json
import urllib.request
from pathlib import Path

from common import WS, TOOLS, freeze_json, load_module, require, sha, start_guard, write_frozen

CHARACTERS = "\u672c\u50cf\u56f2\u65b9\u5ea6\u8a08\u6e2c\u91cf\u7406"
OUTPUT = WS / "scratch-123" / "review" / "open-pair-sources-001"


def main():
    require(not OUTPUT.exists(), "Preserve existing acquisition; no silent repeat")
    fetch = load_module("b123_source_request", TOOLS / "fetch-snapshots.py")
    extract = load_module("b123_source_extract", TOOLS / "build-packet.py")
    guard, _ = start_guard("B123 held-comparison source capture")
    records = []
    try:
        for char in CHARACTERS:
            guard.check()
            url = f"https://www.weblio.jp/content/{char}"
            requested = fetch.request_url(url)
            started = datetime.datetime.now(datetime.timezone.utc).isoformat()
            request = urllib.request.Request(
                requested, headers={"User-Agent": fetch.USER_AGENT, "Accept-Encoding": "identity"})
            with urllib.request.urlopen(request, timeout=60) as response:
                require(response.status == 200, f"HTTP failure for {char}: {response.status}")
                chunks, size = [], 0
                while chunk := response.read(64 * 1024):
                    guard.check()
                    size += len(chunk)
                    require(size <= 4 * 1024**2, f"Oversized source: {char}")
                    chunks.append(chunk)
                raw = b"".join(chunks)
                final_url = response.geturl()
            raw_ref = write_frozen(OUTPUT / f"{char}-raw.html", raw)
            text, error = extract.extract(raw)
            require(error is None and text, f"Ambiguous source for {char}: {error}")
            records.append({
                "character": char, "url": url, "requestUrl": requested, "finalUrl": final_url,
                "startedAt": started,
                "completedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "raw": raw_ref,
                "extract": write_frozen(OUTPUT / f"{char}-daijisen.txt", text.encode("utf-8")),
            })
        memory = guard.finish()
        require(not memory["breach"], "Source acquisition RAM breach")
        print(json.dumps(freeze_json(OUTPUT / "provenance.json", {
            "batch": 123, "candidate": "047970a055903c0337d73823288695938648dd1d",
            "sources": records, "extractionMethod": extract.METHOD, "memory": memory,
            "extractor": {"path": str(TOOLS / "build-packet.py"),
                          "sha256": sha((TOOLS / "build-packet.py").read_bytes())},
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "A new explicit raw acquisition, separate from the preceding web_fetch previews. "
                      "Those preview payloads were not present in the local event log. No claim of "
                      "byte identity to them, no rewriting of earlier sources, and no linguistic "
                      "acceptance is implied. Complete marked Daijisen sections only; other "
                      "dictionaries on each page are excluded.",
        }), ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
