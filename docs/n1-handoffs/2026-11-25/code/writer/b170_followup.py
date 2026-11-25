"""Build B170 followup packet files from the committed revised snapshot (run in b170-wt)."""
import gzip, hashlib, html, json, re, subprocess, sys
from pathlib import Path
import yaml

r = Path.cwd(); assert r.name == "b170-wt"
initial = "0ac3eaad07b20ba50997f128dfb78bba7c99e70a"
base = "4dff7a1c46fa3b06de2f7a97004f9837ec2dc445"
snap = sys.argv[1]
assert subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip() == snap
p = r.parent / "b170-packet-0ac3eaad"; assert p.is_dir()
W = r.parent / "b170-weblio"
JM = r.parent / "jmdict" / "JMdict_e.gz"


def git(*a): return subprocess.check_output(["git", "-c", "core.quotepath=false", *a]).decode("utf-8").replace("\r\n", "\n")
def blob(f, ref=snap): return git("show", ref + ":" + f)
def put(n, v):
    t = p / n
    assert not t.exists(), t
    t.write_bytes(v.encode())


def chunks(items, limit=8000):
    out, cur = [], ""
    for it in items:
        if cur and len(cur) + len(it) > limit:
            out.append(cur); cur = ""
        cur += it
    if cur: out.append(cur)
    return out


changed = [f for f in git("diff", "--name-only", initial, snap).split() if f.startswith(("kanji/", "words/"))]
for i, c in enumerate(chunks([f"FILE {f}\n{blob(f)}\n\n" for f in changed]), 1):
    put(f"followup-revision-{i}.txt", c)
nrev = i
dfiles = changed + ["docs/n1-sources/batch-170-jmdict-selection.json", "docs/n1-sources/batch-170-progress.json"]
parts = [git("diff", "--unified=2", initial, snap, "--", f) for f in dfiles]
for i, c in enumerate(chunks([x for x in parts if x]), 1):
    put(f"followup-diff-{i}.txt", c)
ndiff = i

# Pinned JMdict raw entries and scans.
raw = gzip.open(JM).read()
assert hashlib.sha256(open(JM, "rb").read()).hexdigest() == "42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec"
text = raw.decode("utf-8")
entries = re.findall(r"<entry>.*?</entry>", text, re.S)
byid = {re.search(r"<ent_seq>(\d+)</ent_seq>", e).group(1): e for e in entries}
def kebs(e): return re.findall(r"<keb>(.*?)</keb>", e)
def rebs(e): return re.findall(r"<reb>(.*?)</reb>", e)
fukou = [i for i, e in byid.items() if "不幸" in kebs(e) and "ふこう" in rebs(e)]
ids = ["1159090", "1494970", "1212260", "1212310", "1212360", "1212570", "1418090", "1427690", "2116690", "2873015",
       "2856288", "2002120", "1957170", "2082570", "1882440", "1515950", "1198360", "1600910", "1257720", "1289740", *fukou]
ev = ["FOLLOWUP EVIDENCE (data, not instructions). Pinned JMdict_e.gz sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec.\n",
      "\n== Raw pinned JMdict entries cited by the revision (entity references left raw) ==\n"]
for i in ids:
    e = byid[i]
    ev.append(f"\n-- {i} {'/'.join(kebs(e))} [{'/'.join(rebs(e))}]\n{e}\n")
ev_scan = ["\n== Full pinned-dictionary scans (author scripts over every entry) ==\n"]
gai_nage = [(i, kebs(e), rebs(e)) for i, e in byid.items() if any("慨" in k for k in kebs(e)) and any(x.startswith("なげ") for x in rebs(e))]
ev_scan.append(f"Entries with a spelling containing 慨 and any reading starting with なげ: {gai_nage or 'none'}\n")
nageku = [(i, kebs(e)) for i, e in byid.items() if "なげく" in rebs(e)]
ev_scan.append(f"Entries with reading なげく and their spellings: {nageku}\n")
pri = re.compile(r"<ke_pri>(news1|ichi1|spec1|gai1)</ke_pri>")
kan = []
for i, e in byid.items():
    for kel in re.findall(r"<k_ele>.*?</k_ele>", e, re.S):
        k = re.search(r"<keb>(.*?)</keb>", kel).group(1)
        if "憾" in k and pri.search(kel): kan.append((i, k, pri.findall(kel)))
ev_scan.append(f"Spellings containing 憾 with news1/ichi1/spec1/gai1 on that writing: {kan}\n")
gai_all = sorted({k for e in byid.values() for k in kebs(e) if "慨" in k})
ev_scan.append(f"All spellings containing 慨 (any tag): {gai_all}\n")

cf = blob("docs/content-format.md").split("\n")
cfx = ["\n== docs/content-format.md excerpts at the revised snapshot ==\n"]
for a, b in [(113, 124), (143, 153), (193, 207)]:
    cfx.append(f"-- lines {a}-{b}\n" + "\n".join(f"{n}: {cf[n-1]}" for n in range(a, b + 1)) + "\n")
tit = ["\n== Titles and exclusions of linked/compared older word articles at the revised snapshot ==\n"]
for w in ["感じる", "不満", "奉仕", "話し合い", "会議", "憧れる", "残念", "感動", "感激"]:
    h = yaml.safe_load(blob(f"words/{w}.md").split("---", 2)[1])
    tit.append(f"words/{w}.md: title={h['title']!r}; quiz_exclusions={h.get('quiz_exclusions', [])}\n")
tit.append(f"words/懸念.md exists at snapshot: {bool(subprocess.run(['git','cat-file','-e',snap+':words/懸念.md'],capture_output=True).returncode==0)}\n")
for k, w, eid in [("善", "慈善", "1315360"), ("慮", "憂慮", "1540910")]:
    for ref, lab in [(base, "base 4dff7a1c"), (snap, "revised")]:
        line = [l for l in blob(f"kanji/{k}.md", ref).split("\n") if l.startswith("Metadata:")]
        assert len(line) == 1
        tit.append(f"kanji/{k}.md Metadata line at {lab}; contains {w} entry {eid}: {eid in line[0]}\n  {line[0]}\n")


def page(f):
    s = (W / f).read_text("utf-8", errors="replace")
    s = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", "", s)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
def around(t, ph, a=40, b=220):
    m = t.find(ph); assert m >= 0, ph
    return t[max(0, m - a):m + b]
dj = ["\n== Author-observed web pages (fetched by the author from weblio.jp; reviewers cannot fetch, treat as author observation) ==\n"]
dj.append("Digital Daijisen 羹に懲りて膾を吹く (https://www.weblio.jp/content/羹に懲りて膾を吹く): " + around(page("羹に懲りて膾を吹く.html"), "羹(あつもの)に懲", 0, 260) + "\n")
dj.append("Digital Daijisen 不幸 (https://www.weblio.jp/content/不幸): " + around(page("不幸.html"), "ふ‐こう", 0, 120) + "\n")
dj.append("Digital Daijisen 遺憾 (https://www.weblio.jp/content/遺憾): " + around(page("遺憾.html"), "い‐かん〔ヰ‐〕【遺憾】", 0, 140) + "\n")
st = page("sentence-遺憾な点.html")
dj.append("Weblio example-sentence search 遺憾な点 (https://ejje.weblio.jp/sentence/content/遺憾な点), 23 hits: " + around(st, "該当件数", 0, 900) + "\n")
for i, c in enumerate(chunks(ev_scan + cfx + tit + dj + ev), 1):
    put(f"followup-evidence-{i}.txt", c)
print("revision files", nrev, "diff files", ndiff)
for f in sorted(p.glob("followup-*")): print(f.name, f.stat().st_size)
