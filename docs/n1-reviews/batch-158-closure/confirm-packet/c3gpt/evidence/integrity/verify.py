#!/usr/bin/env python3
"""Read-only integrity check of this review packet against signed Git objects.

Run from anywhere:  python -B evidence\\integrity\\verify.py [--prior-packet DIR]

It reads only files under this packet (and, with --prior-packet, that packet's snapshot\\ and packet-manifest.json).
It writes nothing.
gpgv, if found, runs with --homedir pointing at a directory that does not exist (gpgv does not create it) and
--keyring pointing at key\\signing-key.gpg, so no GnuPG state is read or written.
Exit status 0 when every check passes (SKIP lines do not fail), 1 otherwise.
"""
import base64
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parents[1]
META = {}
FAILS = []


def report(ok, what):
    tag = "PASS" if ok is True else ("SKIP" if ok is None else "FAIL")
    if ok is False:
        FAILS.append(what)
    print("%s  %s" % (tag, what))


def git_sha(kind, data):
    return hashlib.sha1(b"%s %d\0" % (kind.encode(), len(data)) + data).hexdigest()


def parse_tree(raw):
    entries, i = {}, 0
    while i < len(raw):
        sp = raw.index(b" ", i)
        nul = raw.index(b"\0", sp)
        entries[raw[sp + 1:nul].decode("utf-8")] = (raw[i:sp].decode(), raw[nul + 1:nul + 21].hex())
        i = nul + 21
    return entries


def split_commit(raw):
    """Return (headers, payload, signature): the payload is the object without its gpgsig header."""
    head, sep, body = raw.partition(b"\n\n")
    kept, sig, in_sig, headers = [], [], False, {"parent": []}
    for line in head.split(b"\n"):
        if line.startswith(b"gpgsig "):
            in_sig = True
            sig.append(line[7:])
            continue
        if in_sig and line.startswith(b" "):
            sig.append(line[1:])
            continue
        in_sig = False
        kept.append(line)
        key, _, value = line.partition(b" ")
        if key == b"parent":
            headers["parent"].append(value.decode())
        elif key in (b"tree", b"author", b"committer"):
            headers[key.decode()] = value.decode("utf-8")
    payload = b"\n".join(kept) + sep + body
    return headers, payload, (b"\n".join(sig) + b"\n") if sig else b"", body.split(b"\n", 1)[0].decode("utf-8")


def dearmor(text):
    lines = text.strip().splitlines()
    start = lines.index("") + 1 if "" in lines else 1
    b64 = [ln for ln in lines[start:] if not ln.startswith("-----") and not ln.startswith("=")]
    return base64.b64decode("".join(b64))


def find_gpgv():
    for cand in (shutil.which("gpgv"), r"C:\Program Files\GnuPG\bin\gpgv.exe", r"C:\Program Files (x86)\GnuPG\bin\gpgv.exe",
                 r"C:\Program Files\Git\usr\bin\gpgv.exe"):
        if cand and Path(cand).is_file():
            return cand
    return None


def main():
    META.update(json.loads((HERE / "integrity.json").read_text(encoding="utf-8")))
    args = sys.argv[1:]
    prior_packet = Path(args[args.index("--prior-packet") + 1]) if "--prior-packet" in args else None
    chain = META["chain"]
    print("Packet: %s" % PACKET.name)
    print("Chain (newest first): %s" % " -> ".join(c[:8] for c in chain))

    print("\n== 1. Commit objects")
    commits = {}
    for sha in chain:
        raw = (HERE / "commits" / (sha + ".commit")).read_bytes()
        report(git_sha("commit", raw) == sha, "commits\\%s.commit hashes to %s" % (sha, sha))
        headers, payload, sig, subject = split_commit(raw)
        commits[sha] = headers
        print("      tree %s; parent %s; subject: %s" % (headers["tree"], ",".join(headers["parent"]) or "-", subject))
        print("      committer %s" % headers.get("committer", "?"))
        if sig:
            report((HERE / "commits" / (sha + ".payload")).read_bytes() == payload
                   and (HERE / "commits" / (sha + ".sig")).read_bytes() == sig,
                   "%s.payload and %s.sig are the object split at its gpgsig header" % (sha[:8], sha[:8]))
        else:
            report(None, "%s has no gpgsig header" % sha[:8])

    print("\n== 2. Parent chain")
    for child, parent in zip(chain, chain[1:]):
        report(commits[child]["parent"] == [parent], "%s has exactly one parent, %s" % (child[:8], parent[:8]))

    print("\n== 3. Signatures (gpgv, key from %s)" % META["key"]["publicUrl"])
    asc = (HERE / "key" / "signing-key.asc").read_text(encoding="ascii")
    key = (HERE / "key" / "signing-key.gpg").read_bytes()
    report(dearmor(asc) == key, "key\\signing-key.gpg is the dearmored key\\signing-key.asc (asc sha256 %s)"
           % hashlib.sha256(asc.encode("ascii")).hexdigest())
    gpgv = find_gpgv()
    home = HERE / "no-such-gnupg-home"
    if gpgv is None:
        report(None, "gpgv not found; run: gpgv --keyring <abs>\\key\\signing-key.gpg commits\\<sha>.sig commits\\<sha>.payload")
    elif home.exists():
        report(None, "%s exists; gpgv skipped to stay read-only" % home)
    else:
        for sha in chain:
            sig = HERE / "commits" / (sha + ".sig")
            if not sig.exists():
                report(None, "%s unsigned; no gpgv run" % sha[:8])
                continue
            r = subprocess.run([gpgv, "--homedir", str(home), "--keyring", str(HERE / "key" / "signing-key.gpg"),
                                str(sig), str(HERE / "commits" / (sha + ".payload"))], capture_output=True)
            err = r.stderr.decode("utf-8", "replace")
            ok = r.returncode == 0 and "Good signature" in err and META["key"]["fingerprint"] in err.replace(" ", "")
            report(ok, "gpgv: %s Good signature by %s (exit %d)" % (sha[:8], META["key"]["fingerprint"], r.returncode))
            if not ok:
                print("      " + err.strip().replace("\n", "\n      "))
        report(not home.exists(), "gpgv left no home directory behind")

    print("\n== 4. Tree objects")
    trees = {}
    for commit, paths in META["trees"].items():
        for path, tsha in paths.items():
            raw = (HERE / "trees" / (tsha + ".tree")).read_bytes()
            report(git_sha("tree", raw) == tsha, "%s:%s tree %s" % (commit[:8], path or "/", tsha))
            trees[(commit, path)] = parse_tree(raw)
        report(paths[""] == commits[commit]["tree"], "%s root tree matches the signed commit's tree header" % commit[:8])
        for path, tsha in paths.items():
            if path:
                parent, _, name = path.rpartition("/")
                report(trees[(commit, parent)].get(name) == ("40000", tsha),
                       "%s: %s is entry '%s' of %s" % (commit[:8], path, name, parent or "/"))

    def blob_sha(commit, rel):
        parent, _, name = rel.rpartition("/")
        entry = trees.get((commit, parent), {}).get(name)
        return entry[1] if entry else None

    print("\n== 5. manifest.json")
    manifests = {}
    for commit in META["manifests"]:
        raw = (HERE / "manifest" / (commit[:8] + ".manifest.json")).read_bytes()
        report(git_sha("blob", raw) == blob_sha(commit, "manifest.json"),
               "manifest\\%s.manifest.json is blob manifest.json of signed tree %s" % (commit[:8], commit[:8]))
        m = json.loads(raw.decode("utf-8"))
        manifests[commit] = m
        rest = {k: v for k, v in m.items() if k not in ("schemaVersion", "contentVersion")}
        cv = hashlib.sha256(json.dumps(rest, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
        report(cv == m["contentVersion"], "%s contentVersion %s recomputed (tools\\build_manifest.py algorithm)"
               % (commit[:8], m["contentVersion"]))
        for folder in ("kanji", "words"):
            in_tree = {folder + "/" + n for n, (mode, _) in trees[(commit, folder)].items() if mode != "40000"}
            in_man = {k for k in m["files"] if k.startswith(folder + "/")}
            report(in_tree == in_man, "%s: manifest lists exactly the %d files of %s/ in the signed tree"
                   % (commit[:8], len(in_tree), folder))
    if len(manifests) == 2:
        old, new = (manifests[c] for c in META["manifests"])
        changed = sorted("%s[%s]" % (sec, k) for sec in set(old) | set(new) if isinstance(new.get(sec, old.get(sec)), dict)
                         for k in set(old.get(sec, {})) | set(new.get(sec, {})) if old.get(sec, {}).get(k) != new.get(sec, {}).get(k))
        print("      entries that differ %s -> %s: %s" % (META["manifests"][0][:8], META["manifests"][1][:8],
                                                         ", ".join(changed) or "none"))
        print("      contentVersion %s -> %s" % (old["contentVersion"], new["contentVersion"]))

    bm = HERE / "blobs" / "tools" / "build_manifest.py"
    if bm.exists():
        report(git_sha("blob", bm.read_bytes()) == blob_sha(META["fix"], "tools/build_manifest.py"),
               "blobs\\tools\\build_manifest.py is tools/build_manifest.py of signed tree %s" % META["fix"][:8])

    def bind_snapshot(root, commit, label):
        files = sorted(p for p in (root / "snapshot").rglob("*") if p.is_file())
        report(len(files) > 0, "%s: %d snapshot file(s) found" % (label, len(files)))
        man = manifests.get(commit, {}).get("files", {})
        for p in files:
            rel = p.relative_to(root / "snapshot").as_posix()
            raw = p.read_bytes()
            lf = raw.replace(b"\r\n", b"\n")
            want = blob_sha(commit, rel)
            how = "raw bytes" if git_sha("blob", raw) == want else ("after CRLF->LF" if git_sha("blob", lf) == want else None)
            report(want is not None and how is not None, "%s: snapshot\\%s is blob %s of signed tree %s (%s)"
                   % (label, rel.replace("/", "\\"), want, commit[:8], how or "MISMATCH"))
            if rel in man:
                report(hashlib.sha256(lf).hexdigest() == man[rel], "%s: manifest sha256 of %s matches" % (label, rel))

    print("\n== 6. This packet's snapshot\\ against the signed tree %s" % META["fix"][:8])
    bind_snapshot(PACKET, META["fix"], "this packet")
    if prior_packet:
        prior = json.loads((prior_packet / "packet-manifest.json").read_text(encoding="utf-8"))["candidate"]
        print("\n== 6b. Prior packet %s snapshot\\ against the signed tree %s" % (prior_packet.name, prior[:8]))
        if (prior, "") in trees:
            bind_snapshot(prior_packet, prior, "prior packet")
        else:
            report(False, "no trees for %s" % prior)

    print("\n== 7. App code (%s @ %s)" % (META["app"]["repository"], META["app"]["commit"]))
    src = json.loads((HERE / "app-code" / "SOURCES.json").read_text(encoding="utf-8"))
    for f in src["files"]:
        raw = (HERE / "app-code" / Path(f["path"])).read_bytes()
        report(git_sha("blob", raw) == f["blobSha"], "app-code\\%s is blob %s" % (f["path"].replace("/", "\\"), f["blobSha"]))
    for name, rel in (("QuizBuilder.kt", "core/src/main/kotlin/io/github/stopcran/kanji/core/quiz/QuizBuilder.kt"),
                      ("Words.kt", "core/src/main/kotlin/io/github/stopcran/kanji/core/words/Words.kt")):
        ev = PACKET / "evidence" / name
        if ev.exists():
            report(ev.read_bytes() == (HERE / "app-code" / Path(rel)).read_bytes(),
                   "evidence\\%s is byte-identical to app-code\\%s" % (name, rel.replace("/", "\\")))

    print("\n== 8. Python ports (author tools outside both repositories)")
    ports = json.loads((HERE / "ports" / "SOURCES.json").read_text(encoding="utf-8"))
    for f in ports["files"]:
        report(hashlib.sha256((HERE / "ports" / f["name"]).read_bytes()).hexdigest() == f["sha256"],
               "ports\\%s sha256 %s" % (f["name"], f["sha256"]))

    print("\n%d check(s) failed." % len(FAILS) if FAILS else "\nAll checks passed.")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
