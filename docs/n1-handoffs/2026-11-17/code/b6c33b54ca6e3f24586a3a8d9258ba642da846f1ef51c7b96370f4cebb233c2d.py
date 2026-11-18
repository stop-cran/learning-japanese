"""Structural admissibility check for a fresh B134 review report.

Mechanical validity only: it does not adjudicate semantics.
Usage: check_b134_fresh_report.py <family> <revision> <out.json>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
PREP = WS / "scratch-134" / "review" / "fresh-independent-001" / "preparation.json"
VERDICTS = {"CLEAN", "NEEDS FIX", "UNVERIFIED"}
ASSESSMENTS = {"SUPPORTED PRECAUTION", "DISTINCT WITH BASIS", "UNVERIFIED"}
FACETS = ["Correctness", "Scoped coverage", "Consistency and quiz safety", "Comprehensibility"]
CITATION = re.compile(r"[A-Za-z0-9_\-./\\:\u3000-\u9fff]+\.(?:md|json|xml|txt|log|py|csv|tsv|html|svg)(?::\d+(?:[-\u2013]\d+)?)")


def check(family, revision):
    prep = json.loads(PREP.read_text(encoding="utf-8"))
    exclusions = prep["exclusions"]
    upper = family.upper()
    report = WS / "reports-134" / f"fresh-{family}-{revision}.md"
    raw = report.read_bytes()
    text = raw.decode("utf-8")
    errors = []
    headings = [
        f"# Fresh B134 independent review \u2014 N1-B134-FRESH-{upper}-{revision}",
        "## Snapshot", "## Scope and evidence", "## Overall verdict", "## Facet verdicts",
        "## Direct-pair assessment", "## Findings", "## Optional points", "## Limits",
    ]
    lines = text.splitlines()
    found = [l.rstrip() for l in lines if re.match(r"^#{1,2} ", l)]
    if found != headings:
        errors.append({"headings": found})
    sections = {}
    current = None
    for line in lines:
        if line.rstrip() in headings:
            current = line.rstrip()
            sections[current] = []
        elif current:
            sections[current].append(line)

    def body(name):
        return "\n".join(sections.get(name, []))

    if prep["candidate"] not in body("## Snapshot"):
        errors.append("snapshot lacks full candidate id")
    overall = body("## Overall verdict")
    tokens = [v for v in VERDICTS if re.search(r"(?<![A-Z])" + v + r"(?![A-Z])", overall)]
    first = re.search(r"\b(CLEAN|NEEDS FIX|UNVERIFIED)\b", overall)
    verdict = first.group(1) if first else None
    if verdict is None:
        errors.append("overall verdict missing")
    facet_text = body("## Facet verdicts")
    facets = {}
    for facet in FACETS:
        m = re.search(re.escape(facet) + r"[^\n]*?\b(CLEAN|NEEDS FIX|UNVERIFIED)\b", facet_text)
        facets[facet] = m.group(1) if m else None
        if not m:
            errors.append("facet verdict missing: " + facet)

    rows = []
    for line in sections.get("## Direct-pair assessment", []):
        s = line.strip()
        if not s.startswith("|") or re.match(r"^\|\s*:?-{3,}", s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0].strip("` *") == "Character":
            continue
        if len(cells) >= 4 and len(cells[0].strip("` *")) == 1:
            rows.append(cells)
    chars = [r[0].strip("` *") for r in rows if r[0].strip("` *") in exclusions]
    if chars != exclusions:
        errors.append({"pairOrder": chars, "expected": exclusions})
    pair_assessments = {}
    uncited = []
    for r in rows:
        ch = r[0].strip("` *")
        if ch not in exclusions:
            continue
        a = r[2].strip("` *")
        pair_assessments[ch] = a
        if a not in ASSESSMENTS:
            errors.append(f"invalid assessment {ch}: {a}")
        if not CITATION.search(" | ".join(r[3:])):
            uncited.append(ch)
    if uncited:
        errors.append({"rowsWithoutPathLineCitation": uncited})
    for name, prefix, sev in (("## Findings", "F", {"high", "medium", "low"}),
                              ("## Optional points", "O", {"optional"})):
        b = body(name).strip()
        items = re.findall(r"^### " + prefix + r"(\d+): ", b, re.M)
        if b == "None.":
            continue
        if not items:
            errors.append(name + " neither None. nor numbered items")
            continue
        if [int(i) for i in items] != list(range(1, len(items) + 1)):
            errors.append(name + " numbering")
        for chunk in re.split(r"^### " + prefix + r"\d+: ", b, flags=re.M)[1:]:
            for field in ("Facet", "Severity", "Confidence", "Citations", "Evidence",
                          "Required change" if prefix == "F" else "Suggestion"):
                if not re.search(r"(?m)^\W*" + field + r"\W*:", chunk):
                    errors.append(f"{name} item lacks {field}")
            m = re.search(r"(?m)^\W*Severity\W*:\W*(\w+)", chunk)
            if not m or m.group(1).lower() not in sev:
                errors.append(f"{name} invalid severity")
    findings = len(re.findall(r"^### F\d+: ", body("## Findings"), re.M))
    if verdict == "CLEAN" and findings:
        errors.append("CLEAN with findings")
    if verdict == "NEEDS FIX" and not findings:
        errors.append("NEEDS FIX without findings")
    return {
        "report": str(report),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "overallVerdict": verdict,
        "verdictTokensInOverall": sorted(tokens),
        "facets": facets,
        "pairRows": len(chars),
        "pairAssessments": pair_assessments,
        "assessmentCounts": {a: list(pair_assessments.values()).count(a) for a in sorted(ASSESSMENTS)},
        "findings": findings,
        "errors": errors,
        "mechanicallyValid": not errors,
        "scope": "Structural report contract only; not semantic adjudication.",
    }


if __name__ == "__main__":
    family, revision, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    result = check(family, revision)
    data = json.dumps(result, ensure_ascii=False, indent=2).encode("utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "xb") as f:
        f.write(data)
    print(json.dumps({"path": str(out), "sha256": hashlib.sha256(data).hexdigest(),
                      "valid": result["mechanicallyValid"], "verdict": result["overallVerdict"],
                      "errors": result["errors"]}, ensure_ascii=False))
