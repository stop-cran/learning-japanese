#!/usr/bin/env python3
"""Build a delta-confirmation packet.

A reviewer who already read snapshot BASE (confirmation and follow-up packets) checks a small revision SNAPSHOT.
The packet carries only what changed, byte-checked against the earlier packets, plus the regenerated analysis
outputs and the author's statements for the round. Earlier packets are only read, never modified.
"""
import argparse
import difflib
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import n1cmds
from n1_confirm_packet import changed_line_ranges, git_bytes, git_text, link_table
from n1_followup_packet import blob_id, sha256_bytes, write
from n1lib import JMDICT_GZ, KANJIDIC_GZ, REPO, load_cards, sha256_file


def unified(old, new, old_name, new_name):
    return "".join(l + "\n" for l in difflib.unified_diff(
        old.splitlines(), new.splitlines(), old_name, new_name, n=2, lineterm=""))


def nonblank(text):
    return [l.rstrip() for l in text.splitlines() if l.strip()]


def metadata_tsv(kc):
    rows = ["kanji\ttags\tonyomi\tkunyomi\task-on\task-kun\tdistractors\tquiz_exclusions"]
    for k in sorted(kc):
        fm, _body = kc[k]

        def lst(key):
            v = fm.get(key)
            if v is None:
                v = []
            return " ".join(v) if isinstance(v, (list, tuple)) else str(v)
        on = fm.get("onyomi", [])
        kun = fm.get("kunyomi", [])
        ask_on = fm["quizOnyomi"] if "quizOnyomi" in fm else on
        ask_kun = fm["quizKunyomi"] if "quizKunyomi" in fm else kun
        rows.append("\t".join([k, lst("tags"), lst("onyomi"), lst("kunyomi"),
                               " ".join(ask_on or []), " ".join(ask_kun or []), lst("distractors"), lst("quiz_exclusions")]))
    return "\n".join(rows) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--batch", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--instructions", required=True)
    ap.add_argument("--response", required=True)
    ap.add_argument("--changes", required=True)
    ap.add_argument("--evidence-readme", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--confirm-packet", required=True)
    ap.add_argument("--followup-packet", required=True)
    ap.add_argument("--orig-packet", required=True)
    ap.add_argument("--prior-report", action="append", default=[])
    ap.add_argument("--check", action="append", default=[], help="NAME=FILE: log text without blank lines to checks\\NAME.txt")
    ap.add_argument("--plain-check", action="append", default=[], help="NAME=FILE: byte copy to checks\\NAME (keeps line numbers)")
    ap.add_argument("--tool", action="append", default=[], help="FILE that must equal the follow-up packet's copy")
    ap.add_argument("--evidence", action="append", default=[], help="NAME=FILE: byte copy to evidence\\NAME")
    ap.add_argument("--jm-id", action="append", default=[])
    a = ap.parse_args()

    repo = Path(a.repo)
    snap = git_text(repo, "rev-parse", a.snapshot).strip()
    base = git_text(repo, "rev-parse", a.base).strip()
    head = git_text(repo, "rev-parse", "HEAD").strip()
    if snap != head:
        raise SystemExit("snapshot %s is not HEAD %s" % (snap, head))
    if subprocess.run(["git", "merge-base", "--is-ancestor", base, snap], cwd=repo).returncode:
        raise SystemExit("snapshot does not descend from base")
    dirty = [l for l in git_text(repo, "status", "--porcelain", "--untracked-files=no").split("\n") if l.strip()]
    if dirty:
        raise SystemExit("tracked changes present: %s" % dirty[:5])
    out = Path(a.out)
    if out.exists():
        raise SystemExit("packet dir exists: %s" % out)

    conf, fup, orig = Path(a.confirm_packet), Path(a.followup_packet), Path(a.orig_packet)
    cm = json.loads((conf / "packet-manifest.json").read_text(encoding="utf-8"))
    fm = json.loads((fup / "packet-manifest.json").read_text(encoding="utf-8"))
    if cm["candidate"] != base or fm["candidate"] != base:
        raise SystemExit("earlier packets are for %s / %s, not %s" % (cm["candidate"], fm["candidate"], base))
    members = fm["members"]
    if members != cm["members"]:
        raise SystemExit("member lists differ between the earlier packets")
    fup_manifest_sha = sha256_file(fup / "packet-manifest.json")
    cf_blob = git_text(repo, "rev-parse", "%s:docs/content-format.md" % snap).strip()
    cf_copy = (orig / "repo" / "docs" / "content-format.md").read_bytes().replace(b"\r\n", b"\n")
    if blob_id(cf_copy) != cf_blob:
        raise SystemExit("the original packet's content-format.md is not the snapshot's")

    status = git_text(repo, "diff", "--name-status", "--no-renames", base, snap)
    changed = {}
    for line in status.splitlines():
        st, _, path = line.partition("\t")
        changed[path] = st
    allowed = {"manifest.json"} | {"kanji/%s.md" % k for k in members}
    if set(changed) - allowed:
        raise SystemExit("changes outside the batch cards and the manifest: %s" % sorted(set(changed) - allowed))
    if any(s != "M" for s in changed.values()):
        raise SystemExit("added or deleted files in the revision: %s" % changed)

    out.mkdir(parents=True)
    ident = ["commit %s" % snap, "tree %s" % git_text(repo, "rev-parse", snap + "^{tree}").strip(),
             "parent %s" % git_text(repo, "rev-parse", snap + "^").strip(), "base %s" % base, ""]
    changed_cards, unchanged_cards, snapshot_blobs, base_blobs = [], [], {}, {}
    for k in members:
        rel = "kanji/%s.md" % k
        data = (repo / rel).read_bytes()
        want = git_text(repo, "rev-parse", "%s:%s" % (snap, rel)).strip()
        if blob_id(data.replace(b"\r\n", b"\n")) != want:
            raise SystemExit("working-tree bytes of %s do not match the snapshot blob" % k)
        old_blob = git_text(repo, "rev-parse", "%s:%s" % (base, rel)).strip()
        old_fup = (fup / "snapshot" / "kanji" / (k + ".md")).read_bytes()
        old_conf = (conf / "snapshot" / "kanji" / (k + ".md")).read_bytes()
        if old_fup != old_conf or blob_id(old_fup.replace(b"\r\n", b"\n")) != old_blob \
                or cm["snapshotBlobs"]["snapshot/kanji/%s.md" % k] != old_blob:
            raise SystemExit("earlier packets disagree about the base card %s" % k)
        write(out / "snapshot" / "kanji" / (k + ".md"), data)
        snapshot_blobs["snapshot/kanji/%s.md" % k] = want
        base_blobs["snapshot/kanji/%s.md" % k] = old_blob
        if want == old_blob:
            if data != old_fup:
                raise SystemExit("unchanged card %s differs in bytes from the earlier packets" % k)
            unchanged_cards.append(k)
            ident.append("kanji/%s.md\t%s" % (k, want))
        else:
            changed_cards.append(k)
            ident.append("kanji/%s.md\t%s\tchanged since base (base blob %s)" % (k, want, old_blob))
    if sorted(changed_cards) != sorted(Path(p).stem for p in changed if p.startswith("kanji/")):
        raise SystemExit("changed cards disagree with git diff: %s" % changed_cards)
    write(out / "snapshot-identity.txt", "\n".join(ident) + "\n")

    d = out / "diffs"
    d.mkdir()
    write(d / "delta.patch", git_bytes(repo, "diff", "--no-color", base, snap, "--", ".", ":(exclude)manifest.json"))
    write(d / "manifest-delta.patch", git_bytes(repo, "diff", "--no-color", base, snap, "--", "manifest.json"))
    write(d / "changed-files.txt", "".join("%s\t%s\n" % (s, p) for p, s in sorted(changed.items())))
    u0 = git_text(repo, "diff", "--no-color", "-U0", base, snap, "--", ".", ":(exclude)manifest.json")
    ranges = changed_line_ranges(u0)
    write(d / "changed-lines.txt", "Changed line numbers on the revised (new) side, by file.\n" +
          "".join("%s: %s\n" % (p, ", ".join(r)) for p, r in sorted(ranges.items())))

    c = out / "checks"
    c.mkdir()
    table, n_links, n_bad = link_table(repo, snap, ranges)
    write(c / "link-targets.tsv", table)
    print("links on changed lines: %d, unresolved or mismatched: %d" % (n_links, n_bad))
    if n_bad:
        raise SystemExit("link targets need attention")
    for spec in a.check:
        name, _, path = spec.partition("=")
        if not Path(path).is_file():
            raise SystemExit("missing check file %s" % path)
        body = n1cmds.read_log(path)
        if "unit" in name.lower():
            body = "\n".join(body.split("\n")[-3:])
        write(c / (name + ".txt"), body.strip() + "\n")
    followup_diffs, confirm_diffs = [], []
    for spec in a.plain_check:
        name, _, path = spec.partition("=")
        if not Path(path).is_file():
            raise SystemExit("missing check file %s" % path)
        shutil.copy2(path, c / name)
        new_text = Path(path).read_text(encoding="utf-8")
        if (fup / "checks" / name).is_file():
            followup_diffs.append(unified((fup / "checks" / name).read_text(encoding="utf-8"), new_text,
                                          "followup-packet/checks/" + name, "checks/" + name))
        elif (conf / "checks" / name).is_file():
            confirm_diffs.append(unified("\n".join(nonblank((conf / "checks" / name).read_text(encoding="utf-8"))),
                                         "\n".join(nonblank(new_text)),
                                         "confirmation-packet/checks/%s (blank lines removed)" % name,
                                         "checks/%s (blank lines removed)" % name))
    write(d / "checks-vs-followup.diff", "".join(followup_diffs))
    write(d / "reading-options-vs-confirm.diff", "".join(confirm_diffs))

    ev = out / "evidence"
    ev.mkdir()
    kc, _ = load_cards()
    new_tsv = metadata_tsv(kc)
    old_rows = {l.split("\t")[0]: l for l in (fup / "evidence" / "cards-reading-metadata.tsv").read_text(encoding="utf-8").splitlines()[1:]}
    new_rows = {l.split("\t")[0]: l for l in new_tsv.splitlines()[1:]}
    if set(old_rows) != set(new_rows):
        raise SystemExit("metadata rows cover different cards")
    differing = sorted(k for k in new_rows if new_rows[k] != old_rows[k])
    if differing != sorted(changed_cards):
        raise SystemExit("metadata rows differ for %s, changed cards are %s" % (differing, changed_cards))
    write(ev / "cards-reading-metadata.tsv", new_tsv)
    jm_ids = sorted(set(a.jm_id), key=int)
    if jm_ids:
        xml = n1cmds.jmdict_xml(jm_ids)
        if xml != (fup / "evidence" / "jmdict-cited-entries.xml").read_bytes():
            raise SystemExit("JMdict extract differs from the follow-up packet's copy")
        write(ev / "jmdict-cited-entries.xml", xml)
    for spec in a.evidence:
        name, _, path = spec.partition("=")
        if not name or not Path(path).is_file() or ".." in name:
            raise SystemExit("bad --evidence %s" % spec)
        dst = ev / Path(name.replace("\\", "/"))
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)

    tool_sha = {}
    for f in a.tool:
        name = Path(f).name
        theirs = fup / "evidence" / "tools" / name
        if not theirs.is_file() or theirs.read_bytes() != Path(f).read_bytes():
            raise SystemExit("tool %s differs from the follow-up packet's copy" % name)
        tool_sha[name] = {"sha256": sha256_file(f), "bytes": Path(f).stat().st_size}

    def sized(p):
        return "%d bytes, sha256 `%s`" % (p.stat().st_size, sha256_file(p))
    check_table = "".join("- `checks\\%s` (%s)\n" % (p.name, sized(p)) for p in sorted(c.iterdir()))
    tool_table = "".join("- `%s` (%d bytes, sha256 `%s`)\n" % (n, v["bytes"], v["sha256"]) for n, v in sorted(tool_sha.items()))
    readme = Path(a.evidence_readme).read_text(encoding="utf-8")
    for token, value in {"@@BASE@@": base, "@@BASE8@@": base[:8], "@@SNAP@@": snap, "@@SNAP8@@": snap[:8],
                         "@@FOLLOWUP_MANIFEST_SHA@@": fup_manifest_sha, "@@CHECK_TABLE@@": check_table,
                         "@@TOOL_TABLE@@": tool_table, "@@JMDICT_FILE@@": JMDICT_GZ.name,
                         "@@JMDICT_SHA@@": sha256_file(JMDICT_GZ), "@@KANJIDIC_FILE@@": KANJIDIC_GZ.name,
                         "@@KANJIDIC_SHA@@": sha256_file(KANJIDIC_GZ), "@@CONTENT_FORMAT_BLOB@@": cf_blob}.items():
        readme = readme.replace(token, value)
    if "@@" in readme:
        raise SystemExit("unreplaced token in the evidence README")
    write(ev / "README.md", readme)

    shutil.copy2(a.instructions, out / "INSTRUCTIONS.md")
    shutil.copy2(a.response, out / "RESPONSE.md")
    shutil.copy2(a.changes, out / "CHANGES.md")

    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "packet-manifest.json":
            files[p.relative_to(out).as_posix()] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    (out / "packet-manifest.json").write_text(json.dumps({
        "kind": "delta-confirmation", "batch": a.batch, "candidate": snap, "base": base, "members": members,
        "changed": changed_cards, "unchangedMembers": unchanged_cards, "builtAt": n1cmds.now_utc(),
        "followupPacket": a.followup_packet, "followupManifestSha256": fup_manifest_sha,
        "confirmationPacket": a.confirm_packet, "originalPacket": a.orig_packet, "priorReports": a.prior_report,
        "report": a.report, "snapshotBlobs": snapshot_blobs, "baseBlobs": base_blobs, "toolSha256": tool_sha,
        "contentFormatBlob": cf_blob,
        "fileCount": len(files), "files": files}, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(v["bytes"] for v in files.values())
    print("delta packet %s: %d files, %.2f MB; changed %s; unchanged %d" % (
        out, len(files), total / 1e6, ",".join(changed_cards), len(unchanged_cards)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
