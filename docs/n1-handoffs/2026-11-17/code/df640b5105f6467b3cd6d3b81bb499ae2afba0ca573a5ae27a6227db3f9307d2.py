"""Audit a nested reviewer session from its events.jsonl.

Records actual model identity, tool-call seriality, packet read coverage, writes and web sources.
The audit never accepts a review; it only documents what the session did.

    python n1_audit.py --session SID --packet PACKET_DIR --report REPORT_PATH --out audit.json [--since ISO]
"""
import argparse
import difflib
import fnmatch
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

STATE = Path(os.path.expanduser("~")) / ".copilot" / "session-state"
WRITE_PAT = re.compile(r"(Set-Content|Add-Content|Out-File|New-Item|Remove-Item|Move-Item|Copy-Item|Rename-Item|"
                       r"\bgit\s+(add|commit|push|checkout|reset|stash|merge|rebase|clean|rm|mv)\b|\btee\b|(?<=\s)>>?\s*[\"'$.\\A-Za-z]|"
                       r"\.write(_text|_bytes)?\(|open\([^)]*[\"'][wa]b?[\"'])", re.I)
ABS_PAT = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:\\[^\"'\s;|<>]+")
RECURSE_PAT = re.compile(r"-Recurse|\brglob\b|os\.walk|\*\*|\bgci\b.*-r\b", re.I)
PATCH_FILE = re.compile(r"^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$", re.M)


def norm(p):
    return str(p).replace("/", "\\").rstrip("\\").lower()


def load(sid):
    path = STATE / sid / "events.jsonl"
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    return rows


def text_of(res):
    if isinstance(res, dict):
        c = res.get("content")
        if isinstance(c, str):
            return c
        return json.dumps(res, ensure_ascii=False)
    return "" if res is None else str(res)


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True)
    ap.add_argument("--packet", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--out")
    ap.add_argument("--since", help="ignore events before this ISO timestamp (for a later round in the same session)")
    ap.add_argument("--until", help="ignore events after this ISO timestamp")
    ap.add_argument("--also-read", action="append", default=[],
                    help="extra read-only directory or file the reviewer may read in this round (repeatable)")
    a = ap.parse_args()

    packet = Path(a.packet)
    pnorm = norm(packet)
    report_norm = norm(a.report)
    extra_norms = [norm(p) for p in a.also_read]
    extra_reads = set()
    rows = load(a.session)
    if a.since:
        rows = [e for e in rows if e["timestamp"] >= a.since]
    if a.until:
        rows = [e for e in rows if e["timestamp"] <= a.until]
    if (packet / "packet-manifest.json").is_file():
        manifest = json.loads((packet / "packet-manifest.json").read_text(encoding="utf-8"))
        pfiles = list(manifest["files"].keys())
        pfiles.append("packet-manifest.json")
    else:
        # B112+ packets bind files in a flat {relative path: sha256} SHA256SUMS.json instead.
        pfiles = list(json.loads((packet / "SHA256SUMS.json").read_text(encoding="utf-8")).keys())
        pfiles.append("SHA256SUMS.json")
    file_norm = {norm(packet / f): f for f in pfiles}

    start = next((e for e in rows if e["type"] == "session.start"), None)
    users = [e for e in rows if e["type"] == "user.message"]
    usage = [e["data"]["usage"] for e in rows if e["type"] == "session.usage_record"]
    models = Counter((u.get("model"), u.get("responseModel")) for u in usage)
    totals = {k: sum(int(u.get(k) or 0) for u in usage)
              for k in ("inputTokens", "outputTokens", "cacheReadTokens", "cacheWriteTokens", "reasoningTokens")}
    totals["costMultiplierSum"] = round(sum(float(u.get("cost") or 0) for u in usage), 3)

    starts, completes = {}, {}
    order = []
    for e in rows:
        if e["type"] == "tool.execution_start":
            starts[e["data"]["toolCallId"]] = e
            order.append(e["data"]["toolCallId"])
        elif e["type"] == "tool.execution_complete":
            completes[e["data"]["toolCallId"]] = e

    # seriality: sweep start/complete events in time order
    marks = []
    for cid, s in starts.items():
        marks.append((s["timestamp"], 1, cid))
        c = completes.get(cid)
        marks.append((c["timestamp"] if c else s["timestamp"], 0, cid))
    marks.sort(key=lambda m: (m[0], m[1]))
    inflight = max_inflight = overlaps = 0
    live = set()
    overlap_groups = []
    for ts_, kind, cid_ in marks:
        if kind == 1:
            live.add(cid_)
            inflight += 1
            if inflight > 1:
                overlaps += 1
                names = sorted(starts[x]["data"]["toolName"] for x in live)
                overlap_groups.append({"at": ts_, "tools": names})
            max_inflight = max(max_inflight, inflight)
        else:
            live.discard(cid_)
            inflight -= 1

    counts = Counter(s["data"]["toolName"] for s in starts.values())
    outside, writes, web, shell, mcp = set(), [], [], [], []
    view_cov = {}   # file key -> {"full": bool, "ranges": [], "truncated": bool}
    grep_only, shell_touch = set(), set()
    shell_dirs, corpus_scans = set(), []
    flags = []

    def packet_key(path):
        n = norm(path)
        if n in file_norm:
            return file_norm[n]
        return None

    def classify_path(path):
        n = norm(path)
        if n == report_norm:
            return "report"
        if n == pnorm or n.startswith(pnorm + "\\"):
            return "packet"
        if any(n == e or n.startswith(e + "\\") for e in extra_norms):
            return "extra"
        return "outside"

    for cid in order:
        s = starts[cid]
        d = s["data"]
        tool, args = d["toolName"], d.get("arguments") or {}
        c = completes.get(cid)
        res = text_of(c["data"].get("result")) if c else ""
        ok = bool(c and c["data"].get("success"))
        if tool == "view":
            path = args.get("path", "")
            kind = classify_path(path)
            if kind == "outside":
                outside.add(path)
            elif kind == "extra":
                extra_reads.add(path)
            key = packet_key(path)
            if key:
                f = packet / key
                cov = view_cov.setdefault(key, {"ranges": [], "fullViews": 0, "truncated": False, "ok": False})
                cov["ok"] = cov["ok"] or ok
                vr = args.get("view_range")
                if vr:
                    cov["ranges"].append([int(vr[0]), int(vr[1])])
                else:
                    try:
                        total = len(f.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n"))
                    except OSError:
                        total = 0
                    got = len(res.replace("\r\n", "\n"))
                    if total and got >= 0.97 * total:
                        cov["fullViews"] += 1
                    else:
                        cov["truncated"] = True
        elif tool in ("grep", "glob", "rg"):
            for p in as_list(args.get("paths")) or [""]:
                if p:
                    kind = classify_path(p)
                    if kind == "outside":
                        outside.add(p)
                    elif kind == "extra":
                        extra_reads.add(p)
                    key = packet_key(p)
                    if key:
                        grep_only.add(key)
                    elif kind == "packet":
                        n = norm(p)
                        under = [fk for fn, fk in file_norm.items() if fn.startswith(n + "\\")]
                        grep_only.update(under)
                        if len(under) > 500:
                            corpus_scans.append({"tool": tool, "path": p, "files": len(under)})
        elif tool == "apply_patch":
            body = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
            targets = [m.group(1).strip() for m in PATCH_FILE.finditer(body)]
            for t in targets or [None]:
                writes.append({"tool": tool, "path": t, "ok": ok,
                               "allowed": bool(t) and norm(t) == report_norm})
        elif tool in ("create", "edit"):
            writes.append({"tool": tool, "path": args.get("path"), "ok": ok,
                           "allowed": norm(args.get("path", "")) == report_norm})
        elif tool in ("powershell", "bash", "shell"):
            cmd = args.get("command", "")
            toks = ABS_PAT.findall(cmd)
            recursive = bool(RECURSE_PAT.search(cmd))
            for t in toks:
                t = t.rstrip(".,)`")
                kind = classify_path(t)
                if kind == "outside":
                    outside.add(t)
                    continue
                if kind == "extra":
                    extra_reads.add(t)
                    continue
                if "*" in t or "?" in t:
                    pat = norm(t)
                    hits = [fk for fn, fk in file_norm.items() if fnmatch.fnmatchcase(fn, pat)]
                    shell_touch.update(hits)
                    continue
                key = packet_key(t)
                if key:
                    shell_touch.add(key)
                else:
                    n = norm(t)
                    if n == pnorm or n.startswith(pnorm + "\\"):
                        shell_dirs.add(t)
                        if recursive:
                            under = [1 for fn in file_norm if fn.startswith(n + "\\")]
                            corpus_scans.append({"tool": tool, "path": t, "files": len(under), "recursive": True})
            wr = bool(WRITE_PAT.search(cmd))
            shell.append({"command": cmd if len(cmd) <= 400 else cmd[:400] + "...", "writeLike": wr})
        elif tool in ("web_fetch",):
            web.append({"tool": tool, "url": args.get("url"), "ok": ok})
        elif tool in ("web_search",):
            web.append({"tool": tool, "query": args.get("query"), "ok": ok})
        elif tool not in ("report_intent", "task_complete", "sql", "ask_user"):
            mcp.append({"tool": tool, "args": json.dumps(args, ensure_ascii=False)[:200]})

    # per-file coverage
    cov_rows = {}
    for f in pfiles:
        v = view_cov.get(f)
        status = "none"
        if v:
            fp = packet / f
            nlines = 0
            try:
                nlines = len(fp.read_text(encoding="utf-8", errors="replace").splitlines())
            except OSError:
                pass
            covered = set()
            for lo, hi in v["ranges"]:
                covered.update(range(lo, (hi if hi > 0 else nlines) + 1))
            if v["fullViews"] and not v["truncated"]:
                status = "full"
            elif nlines and len(covered & set(range(1, nlines + 1))) >= nlines:
                status = "full (ranges)"
            elif v["ranges"] or v["fullViews"]:
                status = "partial"
            else:
                status = "partial (truncated)"
        elif f in grep_only:
            status = "grep/glob only"
        elif f in shell_touch:
            status = "shell"
        cov_rows[f] = status

    groups = [("snapshot/kanji", "snapshot/kanji/"), ("snapshot/strokes", "snapshot/strokes/"),
              ("snapshot/words", "snapshot/words/"), ("diffs", "diffs/"), ("checks", "checks/"),
              ("evidence (top level)", None), ("evidence/public-source", "evidence/public-source/"),
              ("evidence/kanjivg", "evidence/kanjivg/"),
              ("titles", "titles/"), ("rubric", "rubric/"), ("repo/docs + README", None),
              ("repo/kanji (context)", "repo/kanji/"), ("repo/words (context)", "repo/words/")]
    summary = {}
    for name, prefix in groups:
        if name == "evidence (top level)":
            fs = [f for f in pfiles if f.startswith("evidence/") and "/" not in f[len("evidence/"):]]
        elif name == "repo/docs + README":
            fs = [f for f in pfiles if f.startswith("repo/docs/") or f == "repo/README.md"]
        else:
            fs = [f for f in pfiles if f.startswith(prefix)]
        c = Counter(cov_rows[f] for f in fs)
        entry = {"files": len(fs), **{k: v for k, v in sorted(c.items())}}
        if name.startswith(("snapshot", "diffs", "evidence", "checks")):
            entry["notFullyRead"] = sorted(f for f in fs if cov_rows[f] not in ("full", "full (ranges)"))[:60]
        summary[name] = entry
    root_status = {f: cov_rows[f] for f in ("INSTRUCTIONS.md", "mechanical-checks.md", "REVIEW.md", "packet.json",
                                            "SHA256SUMS.json") if f in cov_rows}

    # final message vs report file
    final, final_src = None, None
    for e in rows:
        d = e["data"]
        if e["type"] == "assistant.message" and not d.get("toolRequests") and d.get("content"):
            final, final_src = d["content"], "assistant.message"
        elif e["type"] == "tool.execution_start" and d.get("toolName") == "task_complete":
            s = (d.get("arguments") or {}).get("summary")
            if s:
                final, final_src = s, "task_complete.summary"
    rp = Path(a.report)
    report_bytes = rp.read_bytes() if rp.is_file() else None
    report_text = (report_bytes.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
                   if report_bytes is not None else None)
    fm = {"finalMessageChars": len(final or ""), "reportFile": str(rp), "reportExists": report_text is not None,
          "reportChars": len(report_text or ""), "reportBytes": len(report_bytes or b""),
          "reportSha256": hashlib.sha256(report_bytes).hexdigest() if report_bytes is not None else None}
    if final and report_text is not None:
        a1 = re.sub(r"\s+", " ", final).strip()
        b1 = re.sub(r"\s+", " ", report_text).strip()
        fm["finalSource"] = final_src
        fm["finalEqualsReport"] = a1 == b1
        fm["finalContainsReport"] = b1 in a1
        if a1 != b1:
            fm["similarity"] = round(difflib.SequenceMatcher(None, a1[:20000], b1[:20000], autojunk=False).quick_ratio(), 4)

    if max_inflight > 1:
        flags.append("overlapping tool calls: max in flight %d (%d overlapping starts)" % (max_inflight, overlaps))
    rec_scans = [c for c in corpus_scans if c.get("recursive")]
    if rec_scans:
        flags.append("recursive shell commands over packet directories: %d" % len(rec_scans))
    if outside:
        flags.append("paths outside the packet and report: %d" % len(outside))
    bad_w = [w for w in writes if not w["allowed"]]
    if bad_w:
        flags.append("create/edit outside the report path: %d" % len(bad_w))
    wl = [s for s in shell if s["writeLike"]]
    if wl:
        flags.append("write-like shell commands: %d (review them)" % len(wl))
    if mcp:
        flags.append("other tools used: %s" % sorted({m["tool"] for m in mcp}))
    if not fm["reportExists"]:
        flags.append("report file missing")

    ts = [e["timestamp"] for e in rows if e.get("timestamp")]
    audit = {
        "reviewAccepted": False,
        "note": "Records model identity and read scope only; it does not accept a review.",
        "session": a.session,
        "selectedModel": start["data"].get("selectedModel") if start else None,
        "reasoningEffort": start["data"].get("reasoningEffort") if start else None,
        "window": {"first": ts[0] if ts else None, "last": ts[-1] if ts else None},
        "userMessages": [{"timestamp": u["timestamp"], "chars": len(u["data"].get("content", "")),
                          "sha256": hashlib.sha256(u["data"].get("content", "").encode("utf-8")).hexdigest()}
                         for u in users],
        "actualModels": [{"model": m, "responseModel": r, "apiRequests": n} for (m, r), n in models.items()],
        "usageTotals": totals,
        "toolCalls": {"total": len(starts), "byTool": dict(counts.most_common()), "maxInFlight": max_inflight,
                      "overlappingStarts": overlaps, "overlaps": overlap_groups[:40]},
        "corpusScans": corpus_scans,
        "shellDirectories": sorted(shell_dirs),
        "packetCoverage": summary,
        "rootFiles": root_status,
        "outsidePaths": sorted(outside),
        "alsoReadAllowed": sorted(a.also_read),
        "alsoReadPaths": sorted(extra_reads)[:300],
        "alsoReadCount": len(extra_reads),
        "writes": writes,
        "shellCommands": shell,
        "web": web,
        "otherTools": mcp,
        "final": fm,
        "flags": flags,
    }
    out = json.dumps(audit, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
    print("session %s model(s) %s api=%d tools=%d maxInFlight=%d" % (
        a.session[:8], [m["model"] for m in audit["actualModels"]], len(usage), len(starts), max_inflight))
    for name, ent in summary.items():
        print("  %-24s %s" % (name, {k: v for k, v in ent.items() if k != "notFullyRead"}))
    for f in flags:
        print("  FLAG:", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
