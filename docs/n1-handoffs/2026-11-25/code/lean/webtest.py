# -*- coding: utf-8 -*-
import sys, urllib.request, urllib.parse, re, html, gzip, hashlib
k = sys.argv[1]
url = "https://www.weblio.jp/content/" + urllib.parse.quote(k)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "ja,en;q=0.8"})
raw = urllib.request.urlopen(req, timeout=30).read()
print("bytes", len(raw), hashlib.sha256(raw).hexdigest()[:16])
t = raw.decode("utf-8", "replace")
# find dictionary blocks
for m in re.finditer(r'<div class="kijiWrp">', t):
    seg = t[m.start(): m.start() + 3500]
    text = re.sub(r"<[^>]+>", " ", seg)
    text = html.unescape(re.sub(r"\s+", " ", text))
    print("----", text[:420])
    break
heads = re.findall(r'<h2 class="midashigo[^>]*>.*?</h2>', t, re.S)
print("n h2:", len(heads))
for h in heads[:6]:
    print(html.unescape(re.sub(r"<[^>]+>", "", h))[:100])
i = t.find("デジタル大辞泉")
print("daijisen idx", i)
txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", txt)))
j = txt.find("デジタル大辞泉")
print(txt[max(0, j - 300): j + 500])
