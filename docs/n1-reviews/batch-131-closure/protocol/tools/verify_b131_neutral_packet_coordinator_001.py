"""Coordinator-independent verification of the frozen B131 neutral review packet.

Read-only. Checks the packet against signed git blobs and frozen coordinator evidence rather
than against the preparer's own build or verification records.
"""
import hashlib
import html
import json
import os
import re
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
TOOLS = WS / "review-tools"
PACKET = WS / "review-packets" / "batch-131-1359b467-compact-001"
WT = WS / "b131-worktree"
CAND = "1359b467e0edee8822c665614d6ca57e42785c4d"
BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
MANIFEST_SHA = "454c924ce460d050d31eedca225b9553d42790a0060df474088e38c7ca049b39"
GATES_DIR = WS / "scratch-131" / "committed-gates-002"
GATES_SUMMARY_SHA = "4fe77b614065913feef4ec8fe310f8720310a09a1d8519c16eb066f60e0684d1"
EXT_DIR = WS / "scratch-131" / "review" / "packet-verification-002" / "external"
CONTRACT_ORIGINAL = WS / "scratch-131" / "review" / "preparation-001" / "source-contract" / "original"
JOYO_PDF = WS / "review-packets" / "_checks-109-fix" / "joyokanjihyo_20101130.pdf"
PREFIX = "docs/n1-sources/batch-131/"
MEMBERS = ["衛", "羊", "霜"]
GATES = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]
JM_FILES = ["jmdict-complete-families.xml", "jmdict-supplemental-families.xml",
            "jmdict-manual-families.xml"]
JM_RESIDUALS = ["jmdict-final-families.xml", "jmdict-final-families-002.xml"]
KD_FILES = ["kanjidic2-target-records.xml", "kanjidic2-comparison-records.xml",
            "kanjidic2-supplemental-comparisons.xml", "kanjidic2-manual-comparisons.xml"]
FORBIDDEN_PATH_TOKENS = ["n1-sources", "n1-reviews", "n1-authoring-notes", "author", "disposition",
                         "scan", "selection", "membership", "adjudicat", "finding"]
BLIND_TERMS = ["pair-disposition", "dispositions", "authored-source-analysis", "author-response",
               "adjudicat", "n1-authoring-notes", "scans-002", "final-query-membership",
               "N1-B131-CLAUDE", "N1-B131-GPT", "local-history-bindings"]

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)
    return bool(condition)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob_id(raw):
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", str(WT), "-c", "core.quotepath=false", *args],
                          check=True, capture_output=True).stdout


class Blobs:
    def __init__(self):
        self.proc = subprocess.Popen(["git", "-C", str(WT), "cat-file", "--batch"],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def get(self, rev, path):
        self.proc.stdin.write(f"{rev}:{path}\n".encode("utf-8"))
        self.proc.stdin.flush()
        header = self.proc.stdout.readline().split()
        if len(header) == 2 and header[1] == b"missing":
            return None
        size = int(header[2])
        data = self.proc.stdout.read(size)
        self.proc.stdout.read(1)
        return data

    def close(self):
        self.proc.stdin.close()
        self.proc.wait(timeout=30)


def ls(rev, prefix):
    out = git("ls-tree", "-r", "-z", "--name-only", rev, "--", prefix)
    return [p.decode("utf-8") for p in out.split(b"\0") if p]


def readonly(path):
    return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_READONLY)


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def frontmatter(raw):
    text = raw.decode("utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.index("\n---", 4)
    fields = {}
    for line in text[4:end].split("\n"):
        match = re.match(r"^([A-Za-z_]+):\s?(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def flow_list(value):
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    inner = value[1:-1].strip()
    return [unquote(item) for item in inner.split(",")] if inner else []


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


class TextCollector(HTMLParser):
    def __init__(self, body_only):
        super().__init__(convert_charrefs=True)
        self.body_only, self.in_body, self.skip, self.parts, self.alts = body_only, not body_only, 0, [], []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "img":
            alt = dict(attrs).get("alt")
            if alt:
                self.alts.append(alt)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag == "body" and self.body_only:
            self.in_body = False

    def handle_data(self, data):
        if self.in_body and not self.skip:
            self.parts.append(data)


def norm(text):
    return re.sub(r"\s+", "", text)


LABEL = re.compile(r"\[image alt: (.*?)\]|\[image without alt text\]")


def extract_body(extract_text):
    lines = extract_text.split("\n")
    body, alts = [], []
    for index, line in enumerate(lines):
        if (index == 0 and line.startswith("Source: ")) or (index == 1 and line.startswith("URL: ")):
            continue
        if line.startswith("Weblio source section: "):
            continue
        alts.extend(match.group(1) for match in LABEL.finditer(line) if match.group(1) is not None)
        body.append(LABEL.sub("\n", line))
    return body, alts


def main(out_path):
    out = Path(out_path)
    if out.exists():
        raise SystemExit("Output must be absent")
    result = {"batch": 131, "candidate": CAND, "base": BASE, "packet": str(PACKET),
              "tool": {"path": __file__, "sha256": sha(Path(__file__).read_bytes())}}

    # 1. Packet manifest and ReadOnly state.
    manifest_raw = (PACKET / "SHA256SUMS.json").read_bytes()
    check(sha(manifest_raw) == MANIFEST_SHA, "Packet manifest hash differs")
    listed = json.loads(manifest_raw)
    disk = {p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()}
    check(disk - {"SHA256SUMS.json"} == set(listed), "Packet disk files differ from manifest")
    bad_hash = [name for name, digest in listed.items()
                if (PACKET / name).is_file() and sha((PACKET / name).read_bytes()) != digest]
    writable = sorted(name for name in disk if not readonly(PACKET / name))
    check(not bad_hash, f"Listed hashes differ: {bad_hash[:5]}")
    check(not writable, f"Writable packet files: {writable[:5]}")
    bad_paths = sorted(name for name in listed
                       if any(token in name.lower() for token in FORBIDDEN_PATH_TOKENS))
    check(not bad_paths, f"Forbidden packet paths: {bad_paths[:5]}")
    result["manifest"] = {"sha256": sha(manifest_raw), "listed": len(listed), "diskFiles": len(disk),
                          "hashMismatches": len(bad_hash), "writable": len(writable),
                          "forbiddenPaths": bad_paths}
    check(len(listed) == 1332, "Expected 1332 listed packet files")

    # 2. Signed clean candidate.
    head = git("rev-parse", "HEAD").decode().strip()
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    meta = git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CAND).decode().strip()
    check(head == CAND and not status, "Candidate checkout is not clean at candidate")
    check(meta == f"{BASE}|G|{FINGERPRINT}|stop-cran@list.ru|stop-cran@list.ru",
          "Candidate parent/signature/identity differs")
    result["candidateGit"] = {"head": head, "clean": not status, "meta": meta}

    blobs = Blobs()
    try:
        # 3. Teaching mirrors against signed blobs.
        mapping = {}
        for name in listed:
            parts = name.split("/", 1)
            if parts[0] == "repo":
                mapping[name] = (CAND, parts[1])
            elif parts[0] == "snapshot":
                mapping[name] = (CAND, parts[1])
            elif parts[0] == "baseline":
                mapping[name] = (BASE, parts[1])
        mapping["rubric/copilot-instructions.md"] = (CAND, ".github/copilot-instructions.md")
        mapping["rubric/content-structure.instructions.md"] = (
            CAND, ".github/instructions/content-structure.instructions.md")
        mirror_mismatch = [name for name, (rev, path) in mapping.items()
                           if blobs.get(rev, path) != (PACKET / name).read_bytes()]
        check(not mirror_mismatch, f"Packet mirrors differ from signed blobs: {mirror_mismatch[:5]}")
        cand_kanji = {p for p in ls(CAND, "kanji/") if p.endswith(".md")}
        base_kanji = {p for p in ls(BASE, "kanji/") if p.endswith(".md")}
        packet_kanji = {n[len("repo/"):] for n in listed if n.startswith("repo/kanji/")}
        check(packet_kanji == cand_kanji and len(cand_kanji) == 1257 and len(base_kanji) == 1254,
              "Complete same-commit kanji article set differs")
        changes = [line.split("\t") for line in
                   git("diff", "--name-status", BASE, CAND, "--", "kanji", "strokes", "words")
                   .decode("utf-8").splitlines()]
        added = sorted(path for status_code, path in changes if status_code == "A")
        modified = sorted(path for status_code, path in changes if status_code == "M")
        other = [row for row in changes if row[0] not in ("A", "M")]
        expected_added = sorted([f"kanji/{c}.md" for c in MEMBERS] + [f"strokes/{c}.json" for c in MEMBERS])
        check(added == expected_added and not other, "Candidate teaching additions differ")
        check(all(p.startswith("words/") for p in modified) and len(modified) == 4,
              "Candidate modified words differ")
        snap = sorted(n[len("snapshot/"):] for n in listed if n.startswith("snapshot/"))
        check(snap == sorted(expected_added + modified), "Snapshot scope differs from actual teaching diff")
        check(sorted(n[len("baseline/"):] for n in listed if n.startswith("baseline/")) == modified,
              "Baseline support scope differs")
        check(sorted(n[len("repo/"):] for n in listed if n.startswith("repo/words/")) == modified,
              "Repo word scope differs")
        result["teaching"] = {"mirrored": len(mapping), "mismatches": mirror_mismatch,
                              "candidateKanji": len(cand_kanji), "baselineKanji": len(base_kanji),
                              "added": added, "modifiedWords": modified}

        # 4. Exact wrapper diff.
        diff = git("diff", "--no-color", BASE, CAND, "--", "words")
        check(diff == (PACKET / "diffs" / "existing.diff").read_bytes(), "Wrapper diff differs from git")
        result["diffEqualsGit"] = diff == (PACKET / "diffs" / "existing.diff").read_bytes()

        # 5. Complete canonical source records.
        def records(names, tag, key):
            union, counts, conflicts = {}, {}, []
            for name in names:
                raw = blobs.get(CAND, PREFIX + name)
                check(raw == (CONTRACT_ORIGINAL / name).read_bytes(),
                      f"Contract original copy differs: {name}")
                root = ET.fromstring(raw)
                rows = [node for node in root if node.tag == tag]
                counts[name] = {"records": len(rows), "sha256": sha(raw),
                                "otherChildren": sorted({n.tag for n in root if n.tag != tag})}
                for node in rows:
                    identity = node.findtext(key)
                    form = canonical(node)
                    if identity in union and union[identity] != form:
                        conflicts.append(identity)
                    union.setdefault(identity, form)
            return union, counts, conflicts

        def packet_records(name, root_tag, tag, key):
            text = (PACKET / "evidence" / name).read_bytes().decode("utf-8")
            lines = text.split("\n")
            if lines and lines[-1] == "":
                lines.pop()
            ok = lines[0] == f"<{root_tag}>" and lines[-1] == f"</{root_tag}>"
            forms = {}
            for line in lines[1:-1]:
                node = ET.fromstring(line)
                ok = ok and node.tag == tag
                identity = node.findtext(key)
                ok = ok and identity not in forms
                forms[identity] = canonical(node)
            return forms, ok, len(lines)

        jm, jm_counts, jm_conflicts = records(JM_FILES, "entry", "ent_seq")
        residuals = {}
        for name in JM_RESIDUALS:
            raw = blobs.get(CAND, PREFIX + name)
            check(raw == (CONTRACT_ORIGINAL / name).read_bytes(), f"Residual copy differs: {name}")
            residuals[name] = {"records": len(ET.fromstring(raw)), "sha256": sha(raw)}
            check(len(ET.fromstring(raw)) == 0, f"Residual not empty: {name}")
        kd, kd_counts, kd_conflicts = records(KD_FILES, "character", "literal")
        pjm, pjm_ok, pjm_lines = packet_records("jmdict-families.xml", "JMdict", "entry", "ent_seq")
        pkd, pkd_ok, pkd_lines = packet_records("kanjidic2-records.xml", "kanjidic2", "character", "literal")
        check(not jm_conflicts and not kd_conflicts, "Conflicting duplicate source records")
        check(len(jm) == 874 and len(kd) == 182, "Source union counts differ")
        check(pjm_ok and pkd_ok, "Compact files are not one complete record per line")
        check(pjm == jm, "Packet JMdict records are not canonical-equal to signed selections")
        check(pkd == kd, "Packet KANJIDIC2 records are not canonical-equal to signed selections")
        comparisons = set(kd) - set(MEMBERS)
        check(set(MEMBERS) <= set(kd) and len(comparisons) == 179, "KANJIDIC2 targets/comparisons differ")
        presentation = json.loads((PACKET / "evidence" / "xml-presentation.json").read_bytes())
        for name, count, lines in (("jmdict-families.xml", 874, pjm_lines),
                                   ("kanjidic2-records.xml", 182, pkd_lines)):
            raw = (PACKET / "evidence" / name).read_bytes()
            claim = presentation["files"][name]
            check(claim["records"] == count and claim["sha256"] == sha(raw) and claim["bytes"] == len(raw)
                  and claim["lines"] == lines, f"Presentation claim differs: {name}")
        result["sources"] = {"jmdictFamilies": len(jm), "kanjidicRecords": len(kd),
                             "comparisonRecords": len(comparisons), "jmdictSelections": jm_counts,
                             "kanjidicSelections": kd_counts, "residuals": residuals,
                             "duplicateConflicts": jm_conflicts + kd_conflicts,
                             "packetJmdictCanonicalEqual": pjm == jm,
                             "packetKanjidicCanonicalEqual": pkd == kd,
                             "oneRecordPerLine": pjm_ok and pkd_ok}

        # 6. Complete title indices rebuilt from frontmatter.
        def index(rev, paths):
            rows, problems = [], []
            for path in paths:
                fields = frontmatter(blobs.get(rev, path))
                stem = path[len("kanji/"):-len(".md")]
                if not fields or unquote(fields.get("kanji", "")) != stem or "title" not in fields:
                    problems.append(path)
                    continue
                rows.append((stem, f"{stem} {unquote(fields['title'])}"))
            return [line for _, line in sorted(rows, key=lambda row: [ord(c) for c in row[0]])], problems

        for name, rev, paths, count in (("baseline-title-index.txt", BASE, base_kanji, 1254),
                                        ("title-index.txt", CAND, cand_kanji, 1257)):
            expected, problems = index(rev, sorted(paths))
            actual = (PACKET / "evidence" / name).read_bytes().decode("utf-8").splitlines()
            differ = [i for i, (a, b) in enumerate(zip(actual, expected)) if a != b]
            check(not problems and actual == expected and len(actual) == count,
                  f"Title index differs: {name} problems={problems[:3]} first={differ[:3]}")
            result.setdefault("titleIndices", {})[name] = {"lines": len(actual), "equalRebuilt": actual == expected}

        # 7. Eligibility reference equals actual frontmatter.
        eligibility = json.loads((PACKET / "eligibility-reference.json").read_bytes())
        for card in eligibility["cards"]:
            raw = blobs.get(CAND, f"kanji/{card['card']}.md")
            fields = frontmatter(raw)
            check(card["sha256"] == sha(raw) and card["distractors"] == flow_list(fields["distractors"])
                  and card["quiz_exclusions"] == flow_list(fields["quiz_exclusions"]),
                  f"Eligibility reference differs: {card['card']}")
        check([c["card"] for c in eligibility["cards"]] == MEMBERS and not eligibility["otherRequiredCards"],
              "Eligibility card scope differs")

        # 8. Geometry inputs.
        font = json.loads((PACKET / "evidence" / "font-cmap.json").read_bytes())
        shapes = json.loads((PACKET / "evidence" / "shape-evidence.json").read_bytes())
        for row in font["members"]:
            svg_name = f"{ord(row['kanji']):05x}.svg"
            svg = (PACKET / "evidence" / "kanjivg" / svg_name).read_bytes()
            stroke = (PACKET / "snapshot" / "strokes" / f"{row['kanji']}.json").read_bytes()
            check(svg == blobs.get(CAND, PREFIX + "kanjivg/" + svg_name) and sha(svg) == row["svgSha256"]
                  and git_blob_id(svg) == row["kanjivgBlob"] and sha(stroke) == row["strokeSha256"],
                  f"Geometry evidence differs: {row['kanji']}")
        check(all(s["svgGitBlob"] == next(r["kanjivgBlob"] for r in font["members"] if r["kanji"] == s["kanji"])
                  for s in shapes), "Shape evidence blob ids differ")
        check(font["members"] and len(font["codePoints"]) == 209, "Font scope differs")
        check((PACKET / "evidence" / "font-cmap.json").read_bytes()
              == blobs.get(CAND, PREFIX + "stroke-font-evidence-002.json"), "Font evidence differs from signed blob")
        pdf = (PACKET / "evidence" / "joyokanjihyo_20101130.pdf").read_bytes()
        check(pdf == JOYO_PDF.read_bytes(), "Joyo PDF differs from pinned local copy")
        result["geometry"] = {"members": len(font["members"]), "codePoints": len(font["codePoints"]),
                              "joyoPdfSha256": sha(pdf)}

        # 9. Committed gate logs and receipts.
        summary_raw = (GATES_DIR / "summary.json").read_bytes()
        check(sha(summary_raw) == GATES_SUMMARY_SHA, "Committed gate summary differs")
        for gate in GATES:
            receipt = (GATES_DIR / f"{gate}.json").read_bytes()
            log = (GATES_DIR / f"{gate}.log").read_bytes()
            parsed = json.loads(receipt)
            check(receipt == (PACKET / "checks" / f"{gate}.json").read_bytes()
                  and log == (PACKET / "checks" / f"{gate}.txt").read_bytes()
                  and parsed.get("exitCode") == 0 and parsed.get("logSha256") == sha(log),
                  f"Gate evidence differs: {gate}")
        result["gates"] = {"count": len(GATES), "summarySha256": sha(summary_raw)}

    finally:
        blobs.close()

    # 10. External captures: identity, fidelity, Kotobank completeness, Weblio reproduction.
    sys.path.insert(0, str(TOOLS))
    from b128_external_sources import extract as external_extract
    ext_manifest = json.loads((PACKET / "evidence" / "external-snapshots" / "manifest.json").read_bytes())
    external = []
    for item in ext_manifest["snapshots"]:
        response = (PACKET / item["response"]["path"]).read_bytes()
        extract_raw = (PACKET / item["extract"]["path"]).read_bytes()
        original = (EXT_DIR / f"{item['character']}-{item['provider']}.html").read_bytes()
        check(response == original and sha(response) == item["response"]["sha256"]
              and sha(extract_raw) == item["extract"]["sha256"], f"External capture differs: {item['index']}")
        reproduced, problem = external_extract(response, item["finalUrl"], [item["character"]])
        reproduction_equal = problem is None and reproduced.encode("utf-8") == extract_raw
        check(reproduction_equal, f"External extract not reproduced: {item['index']}")
        whole = TextCollector(body_only=False)
        whole.feed(response.decode("utf-8"))
        whole_text = norm("".join(whole.parts))
        lines, alts = extract_body(extract_raw.decode("utf-8"))
        unmatched = [line for line in lines for piece in line.split("\n")
                     if norm(piece) and norm(piece) not in whole_text]
        all_alts = {norm(html.unescape(a)) for a in whole.alts}
        missing_alts = [a for a in alts if norm(a) not in all_alts]
        check(not unmatched and not missing_alts, f"External extract fidelity: {item['index']}")
        row = {"index": item["index"], "character": item["character"], "provider": item["provider"],
               "rawEqualsCoordinatorCopy": response == original, "reproduced": reproduction_equal,
               "lines": len(lines), "unmatched": unmatched[:5], "missingAlts": missing_alts[:5]}
        if item["provider"] == "kotobank":
            body = TextCollector(body_only=True)
            body.feed(response.decode("utf-8"))
            body_text = norm("".join(body.parts))
            extract_text = norm("".join(LABEL.sub("", line) for line in lines))
            row["completeBodyEqual"] = body_text == extract_text
            if body_text != extract_text:
                at = next((i for i, (a, b) in enumerate(zip(body_text, extract_text)) if a != b),
                          min(len(body_text), len(extract_text)))
                row["divergence"] = {"at": at, "body": body_text[at:at + 60], "extract": extract_text[at:at + 60],
                                     "bodyLength": len(body_text), "extractLength": len(extract_text)}
            check(row["completeBodyEqual"], f"Kotobank complete body differs: {item['index']}")
        else:
            body = TextCollector(body_only=True)
            body.feed(response.decode("utf-8"))
            body_text = norm("".join(body.parts))
            row["weblioCoverage"] = round(len(norm("".join(LABEL.sub("", l) for l in lines))) / max(1, len(body_text)), 4)
            row["sections"] = [l[len("Weblio source section: "):]
                               for l in extract_raw.decode("utf-8").split("\n")
                               if l.startswith("Weblio source section: ")]
        external.append(row)
    result["external"] = external

    # 11. Blinding keyword scan outside copied repository/source material.
    hits = []
    for name in sorted(listed):
        if name.startswith(("repo/", "snapshot/", "baseline/", "evidence/external-snapshots/0",
                            "evidence/kanjivg/", "checks/")) or name.endswith(".pdf"):
            continue
        text = (PACKET / name).read_bytes().decode("utf-8", errors="replace")
        for term in BLIND_TERMS:
            for match in re.finditer(re.escape(term), text, re.IGNORECASE):
                hits.append({"file": name, "term": term,
                             "context": text[max(0, match.start() - 60):match.end() + 60]})
    result["blindingKeywordHits"] = hits

    result["failures"] = failures
    result["status"] = "PASS" if not failures else "FAIL"
    result["limits"] = ("Mechanical packet equality, canonical source equality, extract fidelity and "
                        "path/keyword blinding checks only; no linguistic, rendered, native or review acceptance.")
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with open(out, "xb") as handle:
        handle.write(raw)
    os.chmod(out, stat.S_IREAD)
    print(json.dumps({"status": result["status"], "failures": failures, "sha256": sha(raw),
                      "blindingKeywordHits": len(hits)}, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
