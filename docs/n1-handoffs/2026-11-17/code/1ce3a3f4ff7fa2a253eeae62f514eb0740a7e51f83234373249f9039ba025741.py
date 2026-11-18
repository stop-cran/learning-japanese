"""Capture, once, raw responses for every Weblio/Daijisen/Kotobank/Kanjipedia URL cited in batch N's new cards plus each
member's Weblio character page. Failures are recorded and nothing is supplied in their place. No filtering or
annotation happens here; extraction happens in build-packet.py.

Usage: python -B fetch-snapshots-b128.py <batch>
"""
import datetime
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

from common import freeze_json, load_batch, review_dir, sha, at_commit, start_guard, write_frozen, TOOLS, require

URL_PATTERN = re.compile(r"https?://[^\s)>\]]*(?:weblio|daijisen|kotobank|kanjipedia)[^\s)>\]]*", re.IGNORECASE)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) learning-japanese-review-snapshot/1.0"


def request_url(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, urllib.parse.quote(parts.path, safe="/%"),
                                    parts.query, ""))


def main(batch):
    config = load_batch(batch)
    out = review_dir(batch) / "snapshots"
    if out.exists():
        raise FileExistsError("Preserve the existing capture; no silent re-fetch")
    guard, _ = start_guard("Snapshot capture")
    try:
        citations, targets = [], {}
        for char in config["members"]:
            data = at_commit(config, f"kanji/{char}.md")
            for number, line in enumerate(data.decode("utf-8").split("\n"), 1):
                for url in URL_PATTERN.findall(line):
                    citations.append({"card": f"snapshot/kanji/{char}.md", "cardSha256": sha(data),
                                      "line": number, "url": url})
                    targets.setdefault(request_url(url), {"citedUrl": url, "memberPage": None})
        for char in config["members"]:
            url = request_url(f"https://www.weblio.jp/content/{char}")
            targets.setdefault(url, {"citedUrl": None, "memberPage": None})
            if targets[url]["memberPage"] is None:
                targets[url]["memberPage"] = char
        results = []
        for index, (url, target) in enumerate(targets.items(), 1):
            guard.check()
            started = datetime.datetime.now(datetime.timezone.utc).isoformat()
            entry = {"index": index, **target, "requestUrl": url, "fetchStartedUtc": started,
                     "citedBy": [c for c in citations if request_url(c["url"]) == url]}
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
                    entry.update(status=response.status, finalUrl=response.geturl(),
                                 headers=dict(response.headers.items()))
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                entry.update(fetchCompletedUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                             outcome="FAILED", error=repr(error))
                results.append(entry)
                continue
            entry["fetchCompletedUtc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            entry.update(outcome="FETCHED", raw=write_frozen(out / "raw" / f"{index:02d}-raw.bin", body))
            results.append(entry)
        memory = guard.finish()
        script = (TOOLS / "fetch-snapshots-b128.py").read_bytes()
        record = {"batch": config["batch"], "candidate": config["candidate"], "urlPattern": URL_PATTERN.pattern,
                  "scope": "Every cited Weblio/Daijisen/Kotobank/Kanjipedia URL in the new cards, then each member's "
                           "https://www.weblio.jp/content/<kanji> page; each distinct request fetched once.",
                  "citations": citations, "userAgent": USER_AGENT, "results": results, "memory": memory,
                  "script": {"path": str(TOOLS / "fetch-snapshots-b128.py"), "sha256": sha(script)}}
        written = freeze_json(out / "fetch-record.json", record)
        print({"record": written["sha256"],
               "results": [(r["index"], r.get("memberPage"), r["outcome"], r.get("status")) for r in results]})
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
