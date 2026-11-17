"""Fetch each cited B127 character source once, serially, without selected excerpts."""
import datetime
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from common import freeze_json, load_batch, require, sha, start_guard, write_frozen
import verify_b127_sources as sources

PATTERN = re.compile(r"https?://[^\s)>\]]*(?:weblio|daijisen|kotobank|kanjipedia)[^\s)>\]]*", re.I)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) learning-japanese-review-snapshot/1.0"


def request_url(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, urllib.parse.quote(parts.path, safe="/%"),
                                    parts.query, ""))


def main():
    config = load_batch(127)
    out = sources.HERE / "snapshots"
    require(not out.exists(), "Preserve existing snapshot attempt")
    guard, _ = start_guard("B127 cited-source capture")
    sources.ACTIVE_GUARD = guard
    results = []
    try:
        sources.clean()
        raw_card = sources.blob(f"kanji/{sources.MEMBER}.md")
        citations, targets = [], {}
        for number, line in enumerate(raw_card.decode("utf-8").splitlines(), 1):
            for url in PATTERN.findall(line):
                citations.append({"card": f"snapshot/kanji/{sources.MEMBER}.md", "cardSha256": sha(raw_card),
                                  "line": number, "url": url})
                targets.setdefault(request_url(url), {"citedUrl": url, "memberPage": None})
        page = request_url(f"https://www.weblio.jp/content/{sources.MEMBER}")
        targets.setdefault(page, {"citedUrl": None, "memberPage": sources.MEMBER})
        require(len(targets) == 3, "Unexpected cited-source set")
        for index, (url, target) in enumerate(targets.items(), 1):
            guard.check()
            entry = {"index": index, **target, "requestUrl": url,
                     "fetchStartedUtc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     "citedBy": [item for item in citations if request_url(item["url"]) == url]}
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    chunks, count = [], 0
                    while chunk := response.read(65536):
                        guard.check()
                        count += len(chunk)
                        require(count <= 4 * 1024**2, "Cited source exceeds bounded response allowance")
                        chunks.append(chunk)
                    body = b"".join(chunks)
                    entry.update(status=response.status, finalUrl=response.geturl(), headers=dict(response.headers.items()))
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                entry.update(outcome="FAILED", error=repr(error))
            else:
                entry.update(outcome="FETCHED", raw=write_frozen(out / "raw" / f"{index:02d}-raw.bin", body))
            entry["fetchCompletedUtc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            results.append(entry)
        sources.clean()
    finally:
        memory = guard.finish()
        sources.ACTIVE_GUARD = None
    require(not memory["breach"], "Cited-source capture breached RAM limit")
    record = freeze_json(out / "fetch-record.json", {
        "batch": 127, "candidate": config["candidate"], "urlPattern": PATTERN.pattern,
        "scope": "Every cited Kanjipedia/Kotobank/Weblio/Daijisen source in the new card plus its Weblio "
                 "character page, each distinct URL fetched once. Raw responses retained in full locally.",
        "citations": citations, "userAgent": USER_AGENT, "results": results, "memory": memory,
        "script": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
    })
    print(json.dumps({"record": record, "results": [(r["index"], r["outcome"], r.get("status")) for r in results]}))


if __name__ == "__main__":
    main()
