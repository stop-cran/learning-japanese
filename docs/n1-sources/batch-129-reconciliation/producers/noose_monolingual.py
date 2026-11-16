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
    ch = "羂索"
    capture = HERE / "external-pages" / f"{ch}-kotobank.html"
    assert not capture.exists()
    url = "https://kotobank.jp/word/" + urllib.parse.quote(ch)
    request = urllib.request.Request(url, headers={"User-Agent": "N1-author-source-check/129-reconciliation"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw, final_url = response.read(), response.geturl()
    write(capture, raw)
    parser = Articles()
    parser.feed(raw.decode("utf8"))
    assert parser.active is None and parser.articles
    for article in parser.articles:
        article["text"] = "\n".join(article.pop("parts")) + "\n"
    write(capture.with_suffix(".json"), parser.articles)
    selected = [a for a in parser.articles if set((a["class"] or "").split()) & {"daijisen", "nikkokuseisen", "jitsu"}]
    assert selected
    full = "\n".join(f"===== {ch} / {a['class']} =====\n{a['text']}" for a in selected)
    write(capture.with_suffix(".txt"), full.encode())
    write(capture.with_name(f"{ch}-receipt.json"), {
        "character": ch, "url": url, "finalUrl": final_url,
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "rawSha256": sha(raw), "rawBytes": len(raw), "localRawCapture": str(capture),
        "allArticleJsonSha256": sha(capture.with_suffix(".json").read_bytes()),
        "selectedCompleteArticleTextSha256": sha(full.encode()),
        "selectedArticleClasses": [a["class"] for a in selected],
        "trigger": "Exact noun explicitly present in complete 索 Nikkoku sense2; resolve noose/rope scope, not a new title search.",
        "extraction": "Complete matching Daijisen/Nikkoku/Jitsu article text including all supplied senses and missing-image markers; all raw HTML and article JSON local only.",
    })
    print(full)
finally:
    write(HERE / "noose-monolingual-memory-001.json", guard.finish())
