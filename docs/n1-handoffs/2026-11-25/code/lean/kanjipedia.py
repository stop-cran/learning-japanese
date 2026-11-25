#!/usr/bin/env python3
"""Kanjipedia (Kanji Kentei) character entries: readings, with the ones marked 外 (outside the official Joyo table).

Usage: python kanjipedia.py [--json OUT] K [K ...]
Prints, per kanji, the entry URL, the on and kun readings, and the readings marked 外, plus a ready --extra argument for
reading_exposure.py / reading_options.py. Pages are cached in cache/kanjipedia/.
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache" / "kanjipedia"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def get(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (re.sub(r"[^0-9A-Za-z]+", "_", url)[-120:] + ".html")
    if f.exists():
        return f.read_text(encoding="utf-8")
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 4:
                raise
            time.sleep(5 * (attempt + 1))
    f.write_text(text, encoding="utf-8")
    time.sleep(1)
    return text


def entry_url(ch):
    q = urllib.parse.quote(ch)
    page = get("https://www.kanjipedia.jp/search?k=%s&kt=1&sk=leftHand" % q)
    for m in re.finditer(r'href="(/kanji/\d{10})"[^>]*>(.*?)</a>', page, re.S):
        if ch in html.unescape(re.sub(r"<[^>]+>", "", m.group(2))) or ("alt=\"%s\"" % ch) in m.group(2):
            return "https://www.kanjipedia.jp" + m.group(1)
    ids = re.findall(r'href="(/kanji/\d{10})"', page)
    if len(set(ids)) == 1:
        return "https://www.kanjipedia.jp" + ids[0]
    return None


def readings(page):
    m = re.search(r'<ul id="onkunList">(.*?)</ul>', page, re.S)
    out = {"on": [], "kun": [], "outside": []}
    if not m:
        return out
    for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.S):
        kind = "on" if 'alt="音"' in li else "kun" if 'alt="訓"' in li else None
        p = re.search(r'<p class="onkunYomi[^"]*">(.*)</p>', li, re.S)
        if not kind or not p:
            continue
        s = p.group(1)
        s = re.sub(r'<span class="txtNormal">(.*?)</span>', r".\1", s)
        # Joyo readings are red; the readings outside the Joyo table follow a 外 icon inside one black span.
        s = re.sub(r'<span style="color:#000000">(.*?)</span>',
                   lambda m: " " + " ".join("※" + t for t in re.split(r"[\s、・,]+", re.sub(r"<[^>]+>", " ", m.group(1))) if t), s, flags=re.S)
        s = re.sub(r'<img[^>]*alt="外"[^>]*>', " ※", s)
        s = re.sub(r"<[^>]+>", " ", s)
        s = html.unescape(s)
        for tok in re.split(r"[\s、・,]+", s):
            if not tok:
                continue
            outside = tok.startswith("※")
            tok = tok.lstrip("※")
            if not tok:
                continue
            out[kind].append(tok)
            if outside:
                out["outside"].append(tok)
    return out


def main(argv):
    out_json, chars = None, []
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--json":
            out_json = args.pop(0)
        else:
            chars.extend(a)
    res = {}
    for ch in chars:
        url = entry_url(ch)
        if not url:
            print("%s: no entry found" % ch)
            res[ch] = None
            continue
        r = readings(get(url))
        res[ch] = dict(r, url=url)
        print("%s %s  on: %s | kun: %s | outside (外): %s" % (ch, url, " ".join(r["on"]) or "-", " ".join(r["kun"]) or "-",
                                                            " ".join(r["outside"]) or "none"))
    extras = ["--extra \"%s=%s\"" % (ch, ",".join(v["outside"])) for ch, v in res.items() if v and v["outside"]]
    print("\nextra args: " + " ".join(extras))
    if out_json:
        Path(out_json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
