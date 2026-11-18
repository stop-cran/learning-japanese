# -*- coding: utf-8 -*-
"""Build a focused follow-up packet for ONE reviewer after a confirmation round. The batch snapshot does not change.

  python n1_followup_packet.py --batch 110 --snapshot 10d79652 --out DIR \
      --instructions FILE --response FILE --report PATH \
      --orig-packet DIR --confirm-packet DIR --prior-report FILE [--prior-report FILE]... \
      --android-repo DIR --android-commit SHA --android-slug OWNER/REPO \
      [--android-file 'PATH|NOTE']... [--compare-rev REV --compare-file PATH ...] [--verify-raw] \
      [--grep NAME=REGEX]... [--tool FILE]... [--check FILE]... [--jm-id N]...

Requires HEAD == snapshot, a clean tracked tree and a non-existent out dir. The batch cards are copied from the working tree
(the same bytes as in the confirmation packet, which is asserted) and checked against the git blobs after CRLF -> LF.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import n1cmds  # noqa: E402
from n1lib import JMDICT_GZ, REPO, load_cards, sha256_file  # noqa: E402

RAW = "https://raw.githubusercontent.com/%s/%s/%s"

EVIDENCE_README = """# Evidence for the follow-up round

Everything here is supplied so that the corrected pool facts in `RESPONSE.md` can be checked against sources, not taken on
trust. Sections 1 to 4 are source material; section 5 is the author's own analysis (claims to verify, not evidence).

## 1. Android client sources (`android\\`)

The reading quiz of the app is built from the Android repository `{slug}` (public) at ONE pinned commit:
`{commit}`. The files below are the exact git blobs of that commit (LF line ends, no edits). The table gives each file's size,
SHA-256, git blob id and the public raw URL where the same bytes can be fetched anonymously
(`{raw_base}/<path>`); "raw check" says whether the author compared the bytes served at that URL with the blob on
{checked_on}. What each file shows (line numbers are of the file in this packet):

{table}
`android\\SOURCES.tsv` has the same table as tab-separated values.

- `android\\call-sites.txt`: `git grep` over every `*.kt` file of the commit for the quiz entry points and pool builders
  (`{call_pattern}`). Files under `src/test` and `src/androidTest` are tests, not production paths.
- `android\\routes.txt`: `git grep` for the `kreading` route of the readings screen (`{route_pattern}`).
{compare}
## 2. Content metadata (`cards-reading-metadata.tsv`)

Every card of the snapshot (the whole shipped content at commit `{snapshot}`), one row per card: kanji, tags,
onyomi, kunyomi, ask-on, ask-kun, distractors, quiz_exclusions; list values are space-separated. "ask-on" and "ask-kun" are what the
app asks (`quizOnyomi` / `quizKunyomi` when the card has them, otherwise the full lists, as `toReadingCard()` does in
`android\\app\\src\\main\\java\\io\\github\\stopcran\\kanji\\data\\ReadingData.kt`). The pools can be rebuilt from the
tags: the N1 stack holds every card tagged `jlpt-n1` to `jlpt-n5`, All every card, Starter every card tagged `starter`.

## 3. Dictionary entries (`jmdict-cited-entries.xml`)

Complete JMdict entries {jm_ids}: 1587610 (嫌 / 厭: いや, や, イヤ) is the attestation of や; 2711110 is the 応 entry whose
おお reading is restricted to a search-only form (not counted as an attested reading). Pinned input `{jm_file}`
(sha256 {jm_sha}). The Digital Daijisen text for 嫌 that your confirmation report cites is in the original packet
(`evidence\\public-source\\`) and at weblio.

## 4. Snapshot (`snapshot\\kanji\\`, `snapshot-identity.txt`)

The 15 cards of commit `{snapshot}` ({snapshot_short} is the reviewed snapshot of your confirmation round). Byte-identical to
the cards in your confirmation packet; `snapshot-identity.txt` lists the git blob id of each.

## 5. Author's analysis (`checks\\`, `evidence\\tools\\`): claims to verify, not evidence

{checks}{tools}"""


def git_bytes(repo, *args):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=repo, capture_output=True)
    if p.returncode:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.decode("utf-8", "replace")))
    return p.stdout


def git_text(repo, *args):
    return git_bytes(repo, *args).decode("utf-8")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "n1-followup-packet"}), timeout=60) as r:
        return r.read()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--batch", required=True)
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--instructions", required=True)
    ap.add_argument("--response", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--orig-packet", required=True)
    ap.add_argument("--confirm-packet", required=True)
    ap.add_argument("--prior-report", action="append", default=[])
    ap.add_argument("--android-repo", required=True)
    ap.add_argument("--android-commit", required=True)
    ap.add_argument("--android-slug", required=True)
    ap.add_argument("--android-file", action="append", default=[], help="PATH|NOTE (PATH relative to the Android repo root)")
    ap.add_argument("--compare-rev")
    ap.add_argument("--compare-file", action="append", default=[])
    ap.add_argument("--call-pattern", default=r"KanjiReadingQuiz\.|ReadingOptions\.|padCandidates\(|\.borrowable\(|toReadingCard\(\)")
    ap.add_argument("--route-pattern", default="kreading")
    ap.add_argument("--verify-raw", action="store_true")
    ap.add_argument("--tool", action="append", default=[])
    ap.add_argument("--check", action="append", default=[], help="FILE copied to checks\\<name>; NAME=FILE renames it")
    ap.add_argument("--check-note", action="append", default=[])
    ap.add_argument("--tool-note", action="append", default=[])
    ap.add_argument("--jm-id", action="append", default=[])
    a = ap.parse_args()

    repo = Path(a.repo)
    snap = git_text(repo, "rev-parse", a.snapshot).strip()
    head = git_text(repo, "rev-parse", "HEAD").strip()
    if snap != head:
        raise SystemExit("snapshot %s is not HEAD %s" % (snap, head))
    dirty = [l for l in git_text(repo, "status", "--porcelain", "--untracked-files=no").split("\n") if l.strip()]
    if dirty:
        raise SystemExit("tracked changes present: %s" % dirty[:5])
    out = Path(a.out)
    if out.exists():
        raise SystemExit("packet dir exists: %s" % out)

    conf = Path(a.confirm_packet)
    cm = json.loads((conf / "packet-manifest.json").read_text(encoding="utf-8"))
    if cm["candidate"] != snap:
        raise SystemExit("confirmation packet is for %s, not %s" % (cm["candidate"], snap))
    members = cm["members"]

    android = Path(a.android_repo)
    acommit = git_text(android, "rev-parse", a.android_commit).strip()
    if subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=android, capture_output=True,
                      text=True).stdout.strip():
        raise SystemExit("Android checkout has tracked changes")

    out.mkdir(parents=True)

    # snapshot cards: same bytes as the confirmation packet, and the recorded blobs after CRLF -> LF
    ident = ["commit %s" % snap, "tree %s" % git_text(repo, "rev-parse", snap + "^{tree}").strip(),
             "parent %s" % git_text(repo, "rev-parse", snap + "^").strip(), ""]
    for k in members:
        data = (repo / "kanji" / (k + ".md")).read_bytes()
        packed = (conf / "snapshot" / "kanji" / (k + ".md")).read_bytes()
        if data != packed:
            raise SystemExit("snapshot card %s differs from the confirmation packet" % k)
        lf = data.replace(b"\r\n", b"\n")
        want = git_text(repo, "rev-parse", "%s:kanji/%s.md" % (snap, k)).strip()
        if blob_id(lf) != want or cm["snapshotBlobs"]["snapshot/kanji/%s.md" % k] != want:
            raise SystemExit("blob mismatch for %s" % k)
        write(out / "snapshot" / "kanji" / (k + ".md"), data)
        ident.append("kanji/%s.md\t%s" % (k, want))
    write(out / "snapshot-identity.txt", "\n".join(ident) + "\n")

    # Android sources
    ev = out / "evidence"
    rows, tsv = [], ["path\tbytes\tsha256\tgit blob id\traw URL\traw check\tnote"]
    raw_base = (RAW % (a.android_slug, acommit, "")).rstrip("/")
    checked_on = n1cmds.now_utc()[:10]
    for spec in a.android_file:
        path, _, note = spec.partition("|")
        data = git_bytes(android, "show", "%s:%s" % (acommit, path))
        bid = git_text(android, "rev-parse", "%s:%s" % (acommit, path)).strip()
        if blob_id(data) != bid:
            raise SystemExit("blob id mismatch for %s" % path)
        url = "%s/%s" % (raw_base, path)
        if a.verify_raw:
            served = fetch(url)
            check = "identical" if served == data else "DIFFERENT"
            if served != data:
                raise SystemExit("raw URL serves different bytes for %s" % path)
        else:
            check = "not checked"
        write(ev / "android" / Path(path), data)
        win = "android\\" + path.replace("/", "\\")
        rows.append("- `%s` (%d bytes, sha256 `%s`, blob `%s`, raw check: %s): %s" % (
            win, len(data), sha256_bytes(data), bid, check, note))
        tsv.append("\t".join([path, str(len(data)), sha256_bytes(data), bid, url, check, note]))
    write(ev / "android" / "SOURCES.tsv", "\n".join(tsv) + "\n")

    call = git_bytes(android, "grep", "-n", "-E", a.call_pattern, acommit, "--", "*.kt").decode("utf-8")
    prefix = acommit + ":"
    body = "".join(l[len(prefix):] + "\n" if l.startswith(prefix) else l + "\n" for l in call.splitlines())
    write(ev / "android" / "call-sites.txt",
          "git grep -n -E '%s' %s -- '*.kt'\n(paths relative to the repository root)\n\n%s" % (a.call_pattern, acommit, body))
    route = git_bytes(android, "grep", "-n", a.route_pattern, acommit, "--", "*.kt").decode("utf-8")
    write(ev / "android" / "routes.txt",
          "git grep -n %s %s -- '*.kt'\n(paths relative to the repository root)\n\n%s" % (
              a.route_pattern, acommit, "".join(l[len(prefix):] + "\n" if l.startswith(prefix) else l + "\n" for l in route.splitlines())))

    compare = ""
    if a.compare_rev:
        rev = git_text(android, "rev-parse", a.compare_rev).strip()
        lines = ["Blob comparison of the reading-quiz sources between `%s` (a) and the pinned commit `%s` (b)." % (rev, acommit),
                 "same = identical bytes; different = see compare patch.", ""]
        for path in a.compare_file:
            ra = subprocess.run(["git", "rev-parse", "%s:%s" % (rev, path)], cwd=android, capture_output=True, text=True)
            rb = git_text(android, "rev-parse", "%s:%s" % (acommit, path)).strip()
            same = ra.returncode == 0 and ra.stdout.strip() == rb
            lines.append("%s\t%s" % ("same" if same else "different", path))
        names = [a.compare_rev[:8], acommit[:8]]
        write(ev / "android" / ("compare-%s-to-%s.txt" % tuple(names)), "\n".join(lines) + "\n")
        write(ev / "android" / ("compare-%s-to-%s.patch" % tuple(names)),
              git_bytes(android, "diff", "--no-color", "-U3", rev, acommit, "--", *a.compare_file))
        compare = ("- `android\\compare-%s-to-%s.txt` and `.patch`: whether the files that build the reading pools differ between `%s` "
                   "(the commit of the phone build mentioned in the author's statement) and the pinned commit, and the exact patch. "
                   "Context for one statement of limits only.\n" % (names[0], names[1], rev))

    # content side
    kc, _ = load_cards()
    head_row = "kanji\ttags\tonyomi\tkunyomi\task-on\task-kun\tdistractors\tquiz_exclusions"
    trs = [head_row]
    for k in sorted(kc):
        fm, _body = kc[k]

        def lst(key, default=None):
            v = fm.get(key, default)
            if v is None:
                v = []
            return " ".join(v) if isinstance(v, (list, tuple)) else str(v)
        on = fm.get("onyomi", [])
        kun = fm.get("kunyomi", [])
        ask_on = fm["quizOnyomi"] if "quizOnyomi" in fm else on
        ask_kun = fm["quizKunyomi"] if "quizKunyomi" in fm else kun
        trs.append("\t".join([k, lst("tags"), lst("onyomi"), lst("kunyomi"),
                              " ".join(ask_on or []), " ".join(ask_kun or []), lst("distractors"), lst("quiz_exclusions")]))
    write(out / "evidence" / "cards-reading-metadata.tsv", "\n".join(trs) + "\n")
    jm_ids = sorted(set(a.jm_id), key=int)
    if jm_ids:
        write(ev / "jmdict-cited-entries.xml", n1cmds.jmdict_xml(jm_ids))

    # author analysis
    (out / "checks").mkdir()
    check_notes = ""
    for spec in a.check:
        name, sep, path = spec.partition("=")
        if not sep:
            name, path = Path(spec).name, spec
        if not Path(path).is_file():
            raise SystemExit("missing check file %s" % path)
        shutil.copy2(path, out / "checks" / name)
    for n in a.check_note:
        check_notes += "- %s\n" % n
    (ev / "tools").mkdir(parents=True, exist_ok=True)
    tool_notes = ""
    for f in a.tool:
        if not Path(f).is_file():
            raise SystemExit("missing tool file %s" % f)
        shutil.copy2(f, ev / "tools" / Path(f).name)
    for n in a.tool_note:
        tool_notes += "- %s\n" % n

    (ev / "README.md").write_text(EVIDENCE_README.format(
        slug=a.android_slug, commit=acommit, raw_base=raw_base, checked_on=checked_on, table="\n".join(rows) + "\n",
        call_pattern=a.call_pattern, route_pattern=a.route_pattern, compare=compare,
        snapshot=snap, snapshot_short=snap[:8], jm_ids=", ".join(jm_ids) or "none",
        jm_file=JMDICT_GZ.name, jm_sha=sha256_file(JMDICT_GZ),
        checks=("`checks\\`:\n" + check_notes + "\n") if check_notes else "", tools=("`evidence\\tools\\`:\n" + tool_notes) if tool_notes else ""),
        encoding="utf-8")

    shutil.copy2(a.instructions, out / "INSTRUCTIONS.md")
    shutil.copy2(a.response, out / "RESPONSE.md")

    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "packet-manifest.json":
            files[p.relative_to(out).as_posix()] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    (out / "packet-manifest.json").write_text(json.dumps({
        "kind": "follow-up", "batch": a.batch, "candidate": snap, "members": members, "builtAt": n1cmds.now_utc(),
        "androidRepository": a.android_slug, "androidCommit": acommit, "confirmationPacket": a.confirm_packet,
        "originalPacket": a.orig_packet, "priorReports": a.prior_report, "report": a.report,
        "snapshotBlobs": {"snapshot/kanji/%s.md" % k: cm["snapshotBlobs"]["snapshot/kanji/%s.md" % k] for k in members},
        "fileCount": len(files), "files": files}, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(v["bytes"] for v in files.values())
    print("follow-up packet %s: %d files, %.2f MB; android files %d (raw check: %s)" % (
        out, len(files), total / 1e6, len(a.android_file), "verified" if a.verify_raw else "skipped"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
