"""Mechanical structure check for a B115 initial-review report (report-structure-v1).

PASS means only that the report follows the frozen template, that its citations name sources and
source-line numbers present in the reviewer's own chains, and that its verdicts are internally
consistent with the coordinator completion message. It is not linguistic acceptance.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CONTRACT = "report-structure-v1"
ENUM = ("CLEAN", "NEEDS FIX", "UNVERIFIED")
FACETS = ("Correctness", "Scoped coverage", "Consistency/quiz safety", "Comprehensibility")
SECTIONS = ("Overall verdict", "Facet verdicts", "Segments read", "Phase-1 D/E lists",
            "D/E cards read", "Per-card results", "Findings", "Optional points", "Limits")
H3_SECTIONS = {"Facet verdicts", "Findings", "Optional points"}
DE_HEADER = ("ID", "Character", "Displayed title", "Related new card(s)", "Reason", "Disposition")
CARD_HEADER = ("Card",) + FACETS + ("Evidence",)
FIELDS = {"F": ("Facet", "Severity", "Confidence", "Citations", "Evidence", "Required change"),
          "O": ("Facet", "Severity", "Confidence", "Citations", "Evidence", "Suggestion")}
LEVELS = ("high", "medium", "low")
LABEL = re.compile(r"\s+\[[DE][1-9]\d?\]$")


def plain(line):
    return line.replace("**", "").strip()


def bullet(line):
    """Top-level '- Name: value' (markup-insensitive); None for indented or other lines."""
    if line[:1] in (" ", "\t"):
        return None
    match = re.fullmatch(r"[-*] ([^:]+?):\s*(.*)", plain(line))
    return (match[1].strip(), match[2].strip()) if match else None


def keyed(lines, key, errors, where):
    """Exactly one '<key>: value' line, optionally bulleted; returns the value."""
    found = [m[1].strip() for m in (re.fullmatch(r"(?:[-*] )?" + re.escape(key) + r":(.*)", plain(l))
                                    for l in lines) if m]
    if len(found) != 1:
        errors.append(f"{where}: expected exactly one '{key}:' line, found {len(found)}")
        return None
    if not found[0]:
        errors.append(f"{where}: '{key}:' is empty")
    return found[0]


def verdict(lines, errors, where):
    value = keyed(lines, "Verdict", errors, where)
    if value is not None and value not in ENUM:
        errors.append(f"{where}: verdict {value!r} is not CLEAN, NEEDS FIX or UNVERIFIED")
        return None
    return value


def table(lines, header, errors, where):
    """Return data rows of the single table in a section, or None when there is no table."""
    indexes = [i for i, line in enumerate(lines) if line.strip().startswith("|")]
    if not indexes:
        return None
    if indexes != list(range(indexes[0], indexes[-1] + 1)):
        errors.append(f"{where}: table rows must be contiguous (one table only)")
    rows = [[cell.strip() for cell in lines[i].strip().strip("|").split("|")] for i in indexes]
    if tuple(plain(c) for c in rows[0]) != header:
        errors.append(f"{where}: table header must be | {' | '.join(header)} |")
        return []
    if len(rows) < 2 or len(rows[1]) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", c) for c in rows[1]):
        errors.append(f"{where}: second table row must be a separator row")
        return []
    body = []
    for number, row in enumerate(rows[2:], 1):
        if len(row) != len(header):
            errors.append(f"{where}: row {number} has {len(row)} cells, expected {len(header)}")
            continue
        cells = [plain(c) for c in row]
        if not all(cells):
            errors.append(f"{where}: row {number} has an empty cell")
        body.append(cells)
    return body


def h3_blocks(lines, errors, where):
    blocks, current = [], None
    for line in lines:
        if line.startswith("### "):
            current = (line[4:].strip(), [])
            blocks.append(current)
        elif current is None:
            if line.strip():
                errors.append(f"{where}: text before the first level-3 heading: {line.strip()!r}")
        else:
            current[1].append(line)
    return blocks


def citations(value, sources, errors, where):
    parts = [p.strip().strip("`").strip() for p in value.replace("`", "").split(";")]
    if not parts or not all(parts):
        errors.append(f"{where}: empty citation")
        return 0
    for part in parts:
        match = re.fullmatch(r"(.+):(\d+)(?:\s*[-–]\s*(\d+))?", part)
        if not match:
            errors.append(f"{where}: citation {part!r} is not <source>:<line> or <source>:<first>-<last>")
            continue
        source = match[1].strip().replace("\\", "/")
        first = int(match[2])
        last = int(match[3]) if match[3] else first
        if source not in sources:
            errors.append(f"{where}: citation source {source!r} is not in the reviewer's chains")
        elif not 1 <= first <= last <= sources[source]:
            errors.append(f"{where}: citation {part!r} is outside source lines 1-{sources[source]}")
    return len(parts)


def items(lines, kind, sources, errors):
    where = "Findings" if kind == "F" else "Optional points"
    content = [plain(l) for l in lines if l.strip()]
    if content == ["None."]:
        return []
    result = []
    for number, (title, body) in enumerate(h3_blocks(lines, errors, where), 1):
        match = re.fullmatch(kind + r"(\d+): (\S.*)", title)
        if not match or int(match[1]) != number:
            errors.append(f"{where}: heading {title!r} must be '{kind}{number}: <short title>'")
        label = f"{kind}{number}"
        fields = {}
        for line in body:
            if not line.strip() or line[:1] in (" ", "\t"):
                continue
            pair = bullet(line)
            if not pair or pair[0] not in FIELDS[kind]:
                errors.append(f"{label}: unexpected top-level line {line.strip()!r}")
                continue
            if pair[0] in fields:
                errors.append(f"{label}: duplicate field {pair[0]}")
            fields[pair[0]] = pair[1]
        for name in FIELDS[kind]:
            if not fields.get(name):
                errors.append(f"{label}: missing or empty field {name}")
        if fields.get("Facet") and fields["Facet"] not in FACETS:
            errors.append(f"{label}: facet {fields['Facet']!r} is not one of {', '.join(FACETS)}")
        severity = fields.get("Severity")
        if severity and (severity not in LEVELS if kind == "F" else severity != "optional"):
            errors.append(f"{label}: severity {severity!r} must be "
                          + ("high, medium or low" if kind == "F" else "optional"))
        if fields.get("Confidence") and fields["Confidence"] not in LEVELS:
            errors.append(f"{label}: confidence {fields['Confidence']!r} must be high, medium or low")
        if fields.get("Citations"):
            citations(fields["Citations"], sources, errors, label)
        result.append(fields)
    if not result:
        errors.append(f"{where}: write either the single line 'None.' or numbered items")
    return result


def phase2_missing(text):
    lines = text.replace("\r\n", "\n").split("\n")
    if len(lines) >= 2 and lines[1] == "Missing entries: none":
        return []
    return [m[1] for m in (re.match(r"([DE][1-9]\d?) ", l) for l in lines[2:]) if m]


def check(report_text, run, core, extension, reference, phase1, phase2_text, completion):
    errors = []
    text = report_text.replace("\r\n", "\n")
    lines = text.split("\n")
    sources = {}
    for record in core["sources"] + extension["sources"]:
        sources[LABEL.sub("", record["source"])] = record["selectedLines"]
    first = next((l for l in lines if l.strip()), "")
    if not re.fullmatch(r"# B115 initial review [—–-] " + re.escape(run), first.strip()):
        errors.append(f"Line 1 must be '# B115 initial review — {run}'")
    if sum(1 for l in lines if re.match(r"# ", l)) != 1:
        errors.append("Exactly one level-1 heading is allowed")
    headings = [l[3:].strip() for l in lines if l.startswith("## ")]
    if tuple(headings) != SECTIONS:
        errors.append("Level-2 headings must be exactly, in order: " + "; ".join(SECTIONS))
    section, body = None, {}
    for line in lines:
        if line.startswith("## "):
            section = line[3:].strip()
            body.setdefault(section, [])
        elif section is not None:
            body[section].append(line)
            if line.startswith("### ") and section not in H3_SECTIONS:
                errors.append(f"{section}: level-3 headings are not allowed here")
    get = lambda name: body.get(name, [])

    overall = verdict(get("Overall verdict"), errors, "Overall verdict")
    facets = {}
    blocks = h3_blocks(get("Facet verdicts"), errors, "Facet verdicts")
    if tuple(title for title, _ in blocks) != FACETS:
        errors.append("Facet verdicts: level-3 headings must be exactly, in order: " + "; ".join(FACETS))
    for title, block in blocks:
        facets[title] = verdict(block, errors, f"Facet {title}")
        keyed(block, "Basis", errors, f"Facet {title}")

    keyed(get("Segments read"), "Core chain", errors, "Segments read")
    keyed(get("Segments read"), "Extension chain", errors, "Segments read")

    entries = phase1["entries"]
    missing = phase2_missing(phase2_text)
    lists = get("Phase-1 D/E lists")
    for group in ("D", "E"):
        value = keyed(lists, group, errors, "Phase-1 D/E lists")
        expected = [e for e in entries if e["label"][0] == group]
        if value is None:
            continue
        if not expected:
            if value.lower() != "none":
                errors.append(f"Phase-1 D/E lists: {group} must be 'none'")
            continue
        labels = re.findall(r"\b" + group + r"[1-9]\d?\b", value)
        if sorted(set(labels)) != sorted(e["label"] for e in expected) or len(labels) != len(expected):
            errors.append(f"Phase-1 D/E lists: {group} line must list each sent {group} ID once")
        for entry in expected:
            if entry["character"] not in value:
                errors.append(f"Phase-1 D/E lists: {group} line lacks {entry['label']} {entry['character']}")
    value = keyed(lists, "Missing entries", errors, "Phase-1 D/E lists")
    if value is not None:
        if not missing and value.lower() != "none":
            errors.append("Phase-1 D/E lists: Missing entries must be 'none'")
        if missing and sorted(set(re.findall(r"\b[DE][1-9]\d?\b", value))) != sorted(missing):
            errors.append("Phase-1 D/E lists: Missing entries must name exactly the missing IDs")

    expected_rows = [(e["label"], e["character"]) for e in entries if e["label"] not in missing]
    de = table(get("D/E cards read"), DE_HEADER, errors, "D/E cards read")
    if de is None:
        if expected_rows or [plain(l) for l in get("D/E cards read") if l.strip()] != ["None read."]:
            errors.append("D/E cards read: a table row is required for every D/E card read"
                          if expected_rows else "D/E cards read: write the single line 'None read.'")
    elif [(r[0], r[1]) for r in de] != expected_rows:
        errors.append("D/E cards read: rows must be exactly the read D/E IDs and characters, in phase-1 order")

    cards = table(get("Per-card results"), CARD_HEADER, errors, "Per-card results") or []
    names = [row[0] for row in cards]
    if sorted(names) != sorted(reference["newCards"]) or len(set(names)) != len(names):
        errors.append("Per-card results: exactly one row for each new card is required")
    for row in cards:
        for facet, cell in zip(FACETS, row[1:5]):
            if cell not in ENUM:
                errors.append(f"Per-card results: {row[0]} {facet} cell {cell!r} is not a verdict")
            elif cell == "NEEDS FIX" and facets.get(facet) != "NEEDS FIX":
                errors.append(f"Per-card results: {row[0]} is NEEDS FIX for {facet}, but that facet is not")
            elif cell == "UNVERIFIED" and facets.get(facet) == "CLEAN":
                errors.append(f"Per-card results: {row[0]} is UNVERIFIED for {facet}, but that facet is CLEAN")

    findings = items(get("Findings"), "F", sources, errors)
    optional = items(get("Optional points"), "O", sources, errors)
    named = {f.get("Facet") for f in findings}
    for facet in FACETS:
        if facets.get(facet) == "NEEDS FIX" and facet not in named:
            errors.append(f"Facet {facet} is NEEDS FIX but no F item names it")
        if facet in named and facets.get(facet) != "NEEDS FIX":
            errors.append(f"An F item names {facet}, but that facet is not NEEDS FIX")

    limits = 0
    for line in get("Limits"):
        if not line.strip() or line[:1] in (" ", "\t"):
            continue
        match = re.fullmatch(r"[-*] L(\d+):\s*(\S.*)", plain(line))
        if not match or int(match[1]) != limits + 1:
            errors.append(f"Limits: expected '- L{limits + 1}: <limit>', found {line.strip()!r}")
            continue
        limits += 1
    if not limits:
        errors.append("Limits: at least one numbered limit is required")

    values = [facets.get(f) for f in FACETS]
    derived = ("NEEDS FIX" if "NEEDS FIX" in values else "UNVERIFIED" if "UNVERIFIED" in values
               else "CLEAN") if all(values) else None
    if overall and derived and overall != derived:
        errors.append(f"Overall verdict {overall} does not follow from the facet verdicts ({derived})")
    message = re.sub(r"\r?\n\Z", "", completion) if completion is not None else None
    if message not in ENUM:
        errors.append("The coordinator completion message is not an exact verdict")
    elif overall and message != overall:
        errors.append(f"Completion message {message} differs from the overall verdict {overall}")
    return {"contract": CONTRACT, "status": "FAIL" if errors else "PASS", "errors": errors,
            "overall": overall, "facets": facets, "findings": len(findings),
            "optionalPoints": len(optional), "limits": limits, "deRows": len(de or []),
            "acceptanceLimit": "Structure only; not linguistic acceptance."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("report", "core-manifest", "extension", "reference", "phase1-list", "phase2-message", "audit"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from review_chain import validate_selection
    reference = json.loads(args.reference.read_bytes())
    phase1 = validate_selection(args.phase1_list.read_bytes().decode("utf-8"), reference)
    audit = json.loads(args.audit.read_bytes())
    messages = audit.get("messages") or []
    if not phase1["valid"]:
        result = {"contract": CONTRACT, "status": "FAIL", "errors": ["Phase-1 list is invalid"]}
    elif not args.report.is_file():
        result = {"contract": CONTRACT, "status": "FAIL", "errors": ["Report is absent"]}
    else:
        result = check(args.report.read_bytes().decode("utf-8"), args.run,
                       json.loads(args.core_manifest.read_bytes()), json.loads(args.extension.read_bytes()),
                       reference, phase1, args.phase2_message.read_bytes().decode("utf-8"),
                       messages[-1] if len(messages) == 2 else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
