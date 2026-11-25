"""Assemble docs/n1-reviews/batch-NNN-closure from a review packet, prompts, reports and audits.

    python n1_closure.py --batch 109 --packet PACKET_DIR --runs runs.json --out REPO/docs/n1-reviews/batch-109-closure

runs.json:
  {"initialSnapshot": "<sha>", "reviewedSnapshot": "<sha>",
   "runs": [{"id": "initial-claude", "kind": "initial|review|confirm|follow-up|delta-confirm", "family": "Claude", "session": "<id>",
             "snapshot": "<sha>", "requestedModel": "...", "prompt": "<file>", "report": "<file>",
             "audit": "<n1_audit.py json>", "confirms": null | "<run id>"}]}

The README is written by hand; this prints the run table to paste into it.
Initial packets may use the legacy manifest or B112's packet.json plus SHA256SUMS.json.
Flat-packet supporting files are kept byte-exact under packet/captured/ (large XML files
are gzipped); snapshot and corpus copies are represented by their recorded hashes.
Reports retain their original bytes so their hashes agree with raw-byte execution audits.
"""
import argparse
import gzip
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

GITATTR = """*.json text eol=lf
*.md text eol=lf
*.gz binary
# Prompts, diffs and confirmation-packet files keep their captured bytes so the SHA-256 values in the
# provenance records stay verifiable.
prompts/*.txt -text
reports/*.md -text
packet/diffs/*.diff -text
packet/captured/** -text
confirm-packet/** -text
followup-packet/** -text
delta-packet/** -text
round-packet/** -text
supplement/** -text
"""
BIG_EVIDENCE = ("jmdict-families.xml", "kanjidic2-records.xml", "jmdict-digest.tsv")
BIG_CONFIRM = 65536


def lf(b):
    return b.replace(b"\r\n", b"\n")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def gz(b):
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0, compresslevel=9) as g:
        g.write(b)
    return buf.getvalue()


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha(data)


def load_initial_packet(packet):
    legacy = packet / "packet-manifest.json"
    if legacy.is_file():
        return json.loads(legacy.read_text(encoding="utf-8")), None
    raw = (packet / "SHA256SUMS.json").read_bytes()
    checksums = json.loads(raw.decode("utf-8"))
    metadata = (packet / "packet.json").read_bytes()
    if checksums.get("packet.json") != sha(metadata):
        sys.exit("packet.json differs from SHA256SUMS.json")
    pm = json.loads(metadata.decode("utf-8"))
    pm.update({
        "files": {name: {"sha256": digest} for name, digest in checksums.items()},
        "fileCount": len(checksums),
        "changed": pm["snapshotFiles"],
        "builtAt": None,
        "sourceManifest": "SHA256SUMS.json",
        "sourceManifestSha256": sha(raw),
        "note": "Adapted from packet.json and the flat checksum manifest; build time was not recorded. "
                "changed contains the packet's changed-content snapshot, not authoring-ledger changes.",
    })
    return pm, raw


def record_flat_packet(packet, pk, files, raw_manifest):
    hashes = {}
    hashes["packet/SHA256SUMS.json.gz"] = put(pk / "SHA256SUMS.json.gz", gz(raw_manifest))
    for name, info in sorted(files.items()):
        # repo/ is a (possibly CRLF) checkout of the frozen commit and PDFs are public sources; keep hashes only.
        if name.startswith(("snapshot/", "repo/")) or name.lower().endswith(".pdf"):
            continue
        data = (packet / name).read_bytes()
        if sha(data) != info["sha256"]:
            sys.exit("%s differs from SHA256SUMS.json" % name)
        stored = "captured/" + name
        if Path(name).name in BIG_EVIDENCE:
            stored += ".gz"
            data = gz(data)
        hashes["packet/" + stored] = put(pk / stored, data)
    return hashes


def record_confirm(out, specs, git_derived=()):
    """Keep what the confirmation round was shown, byte for byte, except the snapshot cards.

    The cards under snapshot/ are the Git blobs at the revised commit, so only their hashes are kept (in the
    stored manifests). Files under a git_derived prefix are raw `git cat-file` output at published commits and
    are kept as hashes only too. A file identical in every packet is stored once under common/. Any other file
    whose bytes were already stored for another packet (under any path) is recorded in sameAs instead of being
    copied again.
    """
    packets = {}
    for spec in specs:
        name, _, folder = spec.partition("=")
        folder = Path(folder)
        raw = (folder / "packet-manifest.json").read_bytes()
        packets[name] = (folder, json.loads(raw.decode("utf-8")), raw)
    names = sorted(packets)
    skip = ("snapshot/",) + tuple(git_derived)
    union = sorted({p for _, m, _ in packets.values() for p in m["files"] if not p.startswith(skip)})
    root = out / "confirm-packet"
    layout = {"common": [], **{n: [] for n in names}}
    same_as, seen, gzipped = {n: {} for n in names}, {}, []
    for path in union:
        digests = {n: packets[n][1]["files"].get(path, {}).get("sha256") for n in names}
        common = len(set(digests.values())) == 1 and None not in digests.values()
        for n in (names[:1] if common else names):
            if digests[n] is None:
                continue
            data = (packets[n][0] / path).read_bytes()
            if sha(data) != digests[n]:
                sys.exit("%s/%s differs from its own manifest" % (n, path))
            where = "common" if common else n
            if not common and digests[n] in seen:
                same_as[n][path] = seen[digests[n]]
                continue
            target = path
            if len(data) >= BIG_CONFIRM and not path.endswith(".gz"):
                target, data = path + ".gz", gz(data)
                gzipped.append("%s/%s" % (where, target))
            put(root / where / target, data)
            seen.setdefault(digests[n], "%s/%s" % (where, target))
            layout[where].append(path)
    for n in names:
        put(root / n / "packet-manifest.json", packets[n][2])
    prov = {"schemaVersion": 1, "note": "Files identical in every packet are stored under common/; the rest under the "
            "packet's name, except that a file whose bytes were already stored for another packet is listed in sameAs "
            "(packet path -> stored copy under confirm-packet/). snapshot/ cards are the Git blobs at the revised "
            "commit and are not copied; their hashes are in each packet-manifest.json (snapshotBlobs and files).",
            "layout": layout,
            "sameAs": {n: v for n, v in same_as.items() if v},
            **({"gzipped": {"files": gzipped, "note": "Files of %d bytes or more are stored gzipped (mtime 0, level 9) "
                "with .gz appended; the recorded SHA-256 values are of the uncompressed bytes the reviewer saw."
                % BIG_CONFIRM}} if gzipped else {}),
            **({"gitDerived": {"prefixes": list(git_derived), "note": "Files under these prefixes are raw `git "
                "cat-file` output (commit, tree or blob objects) at published commits; only their hashes are kept, "
                "in each packet-manifest.json."}} if git_derived else {}),
            "packets": {n: {k: v for k, v in packets[n][1].items() if k != "files"} | {
                "manifestSha256": sha(packets[n][2]), "fileSha256": {p: m["sha256"] for p, m in packets[n][1]["files"].items()}}
                for n in names}}
    put(root / "provenance.json", (json.dumps(prov, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return {n: len(v) for n, v in layout.items()} | {"sameAs": sum(len(v) for v in same_as.values())}


def record_followup(out, folder, dirname="followup-packet"):
    """Keep a follow-up or delta round's packet byte for byte, except the snapshot cards.

    The cards under snapshot/ are the Git blobs at the reviewed commit, so only their hashes are kept (in the stored
    manifest). Every other file is verified against the manifest before it is stored.
    """
    folder = Path(folder)
    raw = (folder / "packet-manifest.json").read_bytes()
    manifest = json.loads(raw.decode("utf-8"))
    root = out / dirname
    stored = 0
    for path, info in sorted(manifest["files"].items()):
        if path.startswith("snapshot/"):
            continue
        data = (folder / path).read_bytes()
        if sha(data) != info["sha256"]:
            sys.exit("follow-up packet %s differs from its own manifest" % path)
        put(root / path, data)
        stored += 1
    put(root / "packet-manifest.json", raw)
    return {"filesStored": stored, "manifestSha256": sha(raw), "candidate": manifest["candidate"],
            "androidCommit": manifest.get("androidCommit"), "fileCount": manifest["fileCount"]}


def record_rounds(out, specs, initial_files, initial_meta):
    """Keep later full review rounds' packets as differences from the initial packet.

    A later round packet is built by the same tool at a later candidate commit. Files whose bytes equal the initial
    packet's file at the same path are recorded by hash only; repo/ and snapshot/ are Git blobs at the round's
    candidate and are folded into hashes; every other file is verified against the round's manifest and stored
    (titles and large evidence gzipped) unless an earlier round already stored the same bytes. The manifest is kept as
    its differences from the initial packet's manifest, with the SHA-256 of the round's raw manifest.
    """
    root = out / "round-packet"
    rounds, seen = {}, {}
    for spec in specs:
        name, _, folder = spec.partition("=")
        folder = Path(folder)
        raw = (folder / "packet-manifest.json").read_bytes()
        m = json.loads(raw.decode("utf-8"))
        stored, same, ctx, earlier = {}, [], [], {}
        for path, info in sorted(m["files"].items()):
            if path.startswith(("repo/", "snapshot/")) or path.lower().endswith(".pdf"):
                ctx.append("%s:%s" % (path, info["sha256"]))
                continue
            if initial_files.get(path, {}).get("sha256") == info["sha256"]:
                same.append(path)
                continue
            if info["sha256"] in seen:
                earlier[path] = seen[info["sha256"]]
                continue
            data = (folder / path).read_bytes()
            if sha(data) != info["sha256"]:
                sys.exit("round packet %s: %s differs from its own manifest" % (name, path))
            target = path
            if Path(path).name in BIG_EVIDENCE or path.startswith("titles/"):
                target += ".gz"
                data = gz(data)
            stored["round-packet/%s/%s" % (name, target)] = put(root / name / target, data)
            seen[info["sha256"]] = "round-packet/%s/%s" % (name, target)
        delta = {k: v for k, v in m.items() if k != "files" and initial_meta.get(k) != v}
        delta["filesChanged"] = {p: i for p, i in sorted(m["files"].items()) if initial_files.get(p) != i}
        delta["filesRemoved"] = sorted(p for p in initial_files if p not in m["files"])
        delta["keysRemoved"] = sorted(k for k in initial_meta if k != "files" and k not in m)
        put(root / name / "manifest-delta.json", (json.dumps(delta, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
        rounds[name] = {
            "candidate": m["candidate"], "base": m["base"], "builtAt": m.get("builtAt"), "fileCount": m["fileCount"],
            "changed": m.get("changed"), "manifestSha256": sha(raw),
            "filesSameAsInitialPacket": len(same), "filesStored": stored, "filesSameAsEarlierRound": earlier,
            "gitBlobsAggregateSha256": sha("\n".join(ctx).encode("utf-8")), "gitBlobFiles": len(ctx)}
    put(root / "provenance.json", (json.dumps({
        "schemaVersion": 1,
        "note": "Each later full review round's packet, stored as differences from the initial packet. "
                "manifest-delta.json lists the round manifest's entries that differ from the initial packet's "
                "manifest (filesChanged, filesRemoved, keysRemoved and changed top-level keys); manifestSha256 is the SHA-256 of "
                "the round's raw packet-manifest.json. Files equal to the initial packet's file at the same path are "
                "not stored again, nor are files an earlier round already stored (filesSameAsEarlierRound); repo/ "
                "and snapshot/ are Git blobs at the round's candidate and are kept as hashes only.",
        "rounds": rounds}, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return {n: {"candidate": r["candidate"], "filesStored": len(r["filesStored"]),
                "filesSameAsInitialPacket": r["filesSameAsInitialPacket"], "manifestSha256": r["manifestSha256"]}
            for n, r in rounds.items()}


def record_supplement(out, folder):
    """Keep, byte for byte, the small read-only supplement a reviewer was given beside the packet."""
    folder = Path(folder)
    stored = {}
    for f in sorted(p for p in folder.rglob("*") if p.is_file()):
        rel = f.relative_to(folder).as_posix()
        stored[rel] = put(out / "supplement" / rel, f.read_bytes())
    return {"files": len(stored), "fileSha256": stored}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--packet", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--confirm-packet", action="append", default=[], help="NAME=DIR of a confirmation packet")
    ap.add_argument("--followup-packet", help="DIR of a follow-up packet")
    ap.add_argument("--delta-packet", help="DIR of a delta confirmation packet")
    ap.add_argument("--supplement", help="DIR of a read-only supplement shown to a reviewer beside the packet")
    ap.add_argument("--round-packet", action="append", default=[],
                    help="NAME=DIR of a later full review round's packet, stored as differences from --packet")
    ap.add_argument("--git-derived", action="append", default=[],
                    help="confirm-packet path prefix whose files are raw Git object output (git cat-file) at "
                         "published commits; kept as hashes only")
    a = ap.parse_args()
    out, packet = Path(a.out), Path(a.packet)
    if out.exists():
        sys.exit("refusing to overwrite %s" % out)
    spec = json.loads(Path(a.runs).read_text(encoding="utf-8"))
    pm, flat_manifest = load_initial_packet(packet)
    out.mkdir(parents=True)
    (out / ".gitattributes").write_text(GITATTR, encoding="utf-8", newline="\n")

    # packet record: instructions, mechanical checks, diffs, evidence (big files gzipped), reduced manifest
    pk = out / "packet"
    hashes = {}
    if flat_manifest is not None:
        hashes = record_flat_packet(packet, pk, pm["files"], flat_manifest)
    else:
        for name in ("INSTRUCTIONS.md", "mechanical-checks.md"):
            hashes["packet/" + name] = put(pk / name, lf((packet / name).read_bytes()))
        for f in sorted((packet / "diffs").glob("*.diff")):
            hashes["packet/diffs/" + f.name] = put(pk / "diffs" / f.name, f.read_bytes())
        for f in sorted((packet / "evidence").iterdir()):
            if f.is_dir():
                for g in sorted(f.glob("*")):
                    data = lf(g.read_bytes())
                    if len(data) >= BIG_CONFIRM and not g.name.endswith(".gz"):
                        hashes["packet/evidence/%s/%s.gz" % (f.name, g.name)] = put(
                            pk / "evidence" / f.name / (g.name + ".gz"), gz(data))
                    else:
                        hashes["packet/evidence/%s/%s" % (f.name, g.name)] = put(
                            pk / "evidence" / f.name / g.name, data)
            elif f.name in BIG_EVIDENCE:
                hashes["packet/evidence/%s.gz" % f.name] = put(pk / "evidence" / (f.name + ".gz"), gz(f.read_bytes()))
            else:
                hashes["packet/evidence/" + f.name] = put(pk / "evidence" / f.name, lf(f.read_bytes()))
    files = pm["files"]
    keep = {k: v for k, v in files.items() if not k.startswith(("repo/kanji/", "repo/words/"))}
    ctx = sorted("%s:%s" % (k, v["sha256"]) for k, v in files.items() if k.startswith(("repo/kanji/", "repo/words/")))
    reduced = {k: pm[k] for k in pm if k != "files"}
    reduced["files"] = keep
    reduced["repoContextExport"] = {
        "files": len(ctx),
        "aggregateSha256": sha("\n".join(ctx).encode("utf-8")),
        "note": "repo/kanji and repo/words are byte copies of those folders at the candidate commit; hashes are folded into one aggregate."}
    hashes["packet/packet-manifest.json.gz"] = put(
        pk / "packet-manifest.json.gz", gz(json.dumps(reduced, ensure_ascii=False, indent=1).encode("utf-8")))

    runs_out, table = [], []
    for run in spec["runs"]:
        rid = run["id"]
        prompt = Path(run["prompt"]).read_bytes()
        report = Path(run["report"]).read_bytes()
        audit = json.loads(Path(run["audit"]).read_text(encoding="utf-8"))
        audit_b = (json.dumps(audit, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
        ps = put(out / "prompts" / (rid + ".txt"), prompt)
        extra = {}
        for item in run.get("extraPrompts", []):
            extra[item["name"]] = put(out / "prompts" / item["name"], Path(item["file"]).read_bytes())
        rs = put(out / "reports" / (rid + ".md"), report)
        as_ = put(out / "scope-audits" / (rid + ".json"), audit_b)
        models = [m["model"] for m in audit["actualModels"]]
        reqs = sum(m["apiRequests"] for m in audit["actualModels"])
        w = audit["window"]
        runs_out.append({
            "key": rid, "phase": run["kind"], "family": run["family"], "session": run["session"],
            "requestedModel": run.get("requestedModel"), "actualModels": models, "apiRequests": reqs,
            "firstEvent": w["first"], "lastEvent": w["last"], "snapshot": run["snapshot"],
            "confirms": run.get("confirms"),
            "toolCalls": audit["toolCalls"]["total"], "maxToolCallsInFlight": audit["toolCalls"]["maxInFlight"],
            "flags": audit["flags"], "promptSha256": ps, "steeringPromptSha256": extra or None,
            "reportSha256": rs, "scopeAuditSha256": as_})
        table.append("| `%s` | %s | `%s` | %s-%s | %d | %d | %d |" % (
            rid, ", ".join(models), run["snapshot"][:8], (w["first"] or "")[11:19], (w["last"] or "")[11:19],
            reqs, audit["toolCalls"]["total"], audit["toolCalls"]["maxInFlight"]))

    prov = {
        "schemaVersion": 1, "batch": a.batch, "members": pm["newKanji"],
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "initialSnapshot": spec["initialSnapshot"], "reviewedSnapshot": spec["reviewedSnapshot"],
        "packet": {"candidate": pm["candidate"], "base": pm["base"], "builtAt": pm["builtAt"],
                   "fileCount": pm["fileCount"], "changed": pm["changed"],
                   "manifestSha256": (sha(flat_manifest) if flat_manifest is not None else
                                      sha(json.dumps(pm, ensure_ascii=False, sort_keys=True).encode("utf-8"))),
                   "manifestFormat": "flat-sha256" if flat_manifest is not None else "legacy-canonical-json",
                   "titlesSha256": {k.split("/")[-1]: v["sha256"] for k, v in files.items() if k.startswith("titles/")},
                   "recordedFileSha256": hashes},
        "runsInChronologicalOrder": runs_out}
    if a.confirm_packet:
        stored = record_confirm(out, a.confirm_packet, tuple(a.git_derived))
        prov["confirmPacketFilesStored"] = stored
    if a.followup_packet:
        prov["followupPacket"] = record_followup(out, a.followup_packet)
    if a.delta_packet:
        prov["deltaPacket"] = record_followup(out, a.delta_packet, "delta-packet")
    if a.supplement:
        prov["supplement"] = record_supplement(out, a.supplement)
    if a.round_packet:
        prov["roundPackets"] = record_rounds(out, a.round_packet, files, pm)
    put(out / "provenance.json", (json.dumps(prov, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print("closure written:", out)
    print("| Run | Actual model | Snapshot | Window (UTC) | API requests | Tool calls | Max in flight |")
    print("|---|---|---|---|---|---|---|")
    print("\n".join(table))
    return 0


if __name__ == "__main__":
    sys.exit(main())
