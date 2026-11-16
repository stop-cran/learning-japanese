import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from recon_common import *


class Articles(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = None
        self.articles = []
        self.ignore = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            assert self.active is None
            self.active = {"id": attrs.get("id"), "class": attrs.get("class"), "parts": []}
        if self.active is not None:
            if tag in ("script", "style"):
                self.ignore += 1
            if tag == "img":
                self.active["parts"].append("[image alt: " + attrs["alt"] + "]" if attrs.get("alt") else "[image without alt text]")

    def handle_endtag(self, tag):
        if self.active is not None:
            if tag in ("script", "style"):
                self.ignore = max(0, self.ignore - 1)
            if tag == "article":
                self.articles.append(self.active)
                self.active = None

    def handle_data(self, data):
        if self.active is not None and not self.ignore and data.strip():
            self.active["parts"].append(data.strip())


guard = start_guard()
try:
    readback = []
    for comparisons in PAIRS.values():
        for ch in comparisons:
            guard.check()
            capture = HERE / "external-pages" / f"{ch}-kotobank.html"
            assert not capture.exists()
            url = "https://kotobank.jp/word/" + urllib.parse.quote(ch)
            request = urllib.request.Request(url, headers={"User-Agent": "N1-author-source-check/129-reconciliation"})
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    raw = response.read()
                    final_url = response.geturl()
            except (urllib.error.URLError, TimeoutError) as error:
                write(HERE / "external-pages" / f"{ch}-failure-001.json", {"url": url, "error": str(error)})
                raise
            write(capture, raw)
            parser = Articles()
            parser.feed(raw.decode("utf8"))
            assert parser.active is None and parser.articles, ch
            articles = []
            for article in parser.articles:
                text = "\n".join(article.pop("parts")) + "\n"
                article["text"] = text
                articles.append(article)
            write(capture.with_suffix(".json"), articles)
            selected = [a for a in articles if set((a["class"] or "").split()) & {"daijisen", "nikkokuseisen", "jitsu"}]
            assert selected, ch
            full = "\n".join(f"===== {ch} / {a['class']} =====\n{a['text']}" for a in selected)
            write(capture.with_suffix(".txt"), full.encode())
            receipt = {"character": ch, "url": url, "finalUrl": final_url,
                       "capturedAt": datetime.now(timezone.utc).isoformat(),
                       "rawSha256": sha(raw), "rawBytes": len(raw), "localRawCapture": str(capture),
                       "allArticleJsonSha256": sha(capture.with_suffix(".json").read_bytes()),
                       "selectedCompleteArticleTextSha256": sha(full.encode()),
                       "selectedArticleClasses": [a["class"] for a in selected],
                       "extraction": "Complete matching Daijisen/Nikkoku/Jitsu article text including all supplied senses and missing-image markers; HTML scripts/styles excluded. All other article JSON and raw HTML retained locally. Not rendered-image acceptance."}
            write(capture.with_name(f"{ch}-receipt.json"), receipt)
            readback.append(full)
            print(json.dumps({"character": ch, "bytes": len(raw), "selectedTextBytes": len(full.encode()),
                              "articles": receipt["selectedArticleClasses"]}, ensure_ascii=False), flush=True)
    write(HERE / "monolingual-complete-readback.txt", "\n".join(readback).encode())
finally:
    write(HERE / "monolingual-memory-001.json", guard.finish())
