"""Mechanical structure check for a B115 confirmation report (confirm-structure-v1).

PASS means only that the report follows the frozen confirmation template, that every requested item has exactly one
disposition from the allowed set, that its citations name sources and source-line numbers present in the reviewer's
own chain, and that its verdicts are internally consistent with each other and with the coordinator completion
message. It is not linguistic acceptance.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CONTRACT = "confirm-structure-v1"
CONFIRMATION = ("CONFIRMED", "NEEDS FIX", "UNVERIFIED")
FACET_VERDICTS = ("CLEAN", "NEEDS FIX", "UNVERIFIED")
FACETS = ("Correctness", "Scoped coverage", "Consistency and quiz safety", "Comprehensibility")
FACET_ALIASES = {"Consistency/quiz safety": "Consistency and quiz safety"}
SECTIONS = ("Snapshot", "Scope", "Dispositions", "Verdicts", "Confirmation", "Findings", "Optional", "Limits")
H3_SECTIONS = {"Findings", "Optional"}
DISPOSITIONS = ("PARTIALLY RESOLVED", "NOT RESOLVED", "RESOLVED", "DECLINE ACCEPTED", "DECLINE REJECTED",
                "DISPUTE ACCEPTED", "DISPUTE REJECTED")
ACCEPTING = {"RESOLVED", "DECLINE ACCEPTED", "DISPUTE ACCEPTED"}
FIELDS = {"F": ("Facet", "Severity", "Confidence", "Citations", "Evidence", "Required change"),
          "O": ("Facet", "Severity", "Confidence", "Citations", "Evidence", "Suggestion")}
SEVERITIES = {"F": ("blocker", "major", "minor"), "O": ("optional",)}
LEVELS = ("high", "medium", "low")
DASH = r"\s+[-\u2013\u2014]\s+"
SPEC = r"\d+(?:\s*[-\u2013]\s*\d+)?"


def plain(line):
    return line.replace("**", "").replace("`", "").strip()


def top_level(lines):
    return [line for line in lines if line.strip() and line[:1] not in (" ", "\t")]


def bullet(line):
    """Top-level '- Name: value' (markup-insensitive); None for other lines."""
    match = re.fullmatch(r"[-*] ([^:]+?):\s*(.*)", plain(line))
    return (match[1].strip(), match[2].strip()) if match else None


def keyed(lines, key, errors, where):
    """Exactly one '<key>: value' line, optionally bulleted; returns the value."""
    found = [m[1].strip() for m in (re.fullmatch(r"(?:[-*] )?" + re.escape(key) + r":(.*)", plain(l))
                                    for l in top_level(lines)) if m]
    if len(found) != 1:
        errors.append(f"{where}: expected exactly one '{key}:' line, found {len(found)}")
        return None
    if not found[0]:
        errors.append(f"{where}: '{key}:' is empty")
    return found[0]


def only_keys(lines, keys, errors, where):
    for line in top_level(lines):
        if not re.fullmatch(r"(?:[-*] )?(?:" + "|".join(map(re.escape, keys)) + r"):.*", plain(line)):
            errors.append(f"{where}: unexpected top-level line {line.strip()!r}")


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
    parts = [p.strip() for p in value.split(";")]
    if not parts or not all(parts):
        errors.append(f"{where}: empty citation")
        return
    for part in parts:
        match = re.fullmatch(r"(.+?):(" + SPEC + r"(?:\s*,\s*" + SPEC + r")*)", part)
        if not match:
            errors.append(f"{where}: citation {part!r} is not <source>:<line> or <source>:<first>-<last>")
            continue
        source = match[1].strip().replace("\\", "/")
        if source not in sources:
            errors.append(f"{where}: citation source {source!r} is not in the reviewer's chain")
            continue
        for spec in re.split(r"\s*,\s*", match[2]):
            numbers = [int(n) for n in re.findall(r"\d+", spec)]
            first, last = numbers[0], numbers[-1]
            if not 1 <= first <= last <= sources[source]:
                errors.append(f"{where}: citation {part!r} is outside source lines 1-{sources[source]}")


def items(lines, kind, sources, errors):
    where = "Findings" if kind == "F" else "Optional"
    if [plain(l) for l in lines if l.strip()] == ["None."]:
        return []
    result = []
    for number, (title, body) in enumerate(h3_blocks(lines, errors, where), 1):
        match = re.fullmatch(kind + r"(\d+): (\S.*)", plain(title))
        if not match or int(match[1]) != number:
            errors.append(f"{where}: heading {title!r} must be '{kind}{number}: <short title>'")
        label = f"{where} {kind}{number}"
        fields = {}
        for line in top_level(body):
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
        facet = FACET_ALIASES.get(fields.get("Facet"), fields.get("Facet"))
        fields["Facet"] = facet
        if facet and facet not in FACETS:
            errors.append(f"{label}: facet {facet!r} is not one of {', '.join(FACETS)}")
        if fields.get("Severity") and fields["Severity"] not in SEVERITIES[kind]:
            errors.append(f"{label}: severity {fields['Severity']!r} must be {' or '.join(SEVERITIES[kind])}")
        if fields.get("Confidence") and fields["Confidence"] not in LEVELS:
            errors.append(f"{label}: confidence {fields['Confidence']!r} must be high, medium or low")
        if fields.get("Citations"):
            citations(fields["Citations"], sources, errors, label)
        result.append(fields)
    if not result:
        errors.append(f"{where}: write either the single line 'None.' or numbered items")
    return result


def check(report_text, run, commit, ids, chain, completion):
    errors = []
    lines = report_text.replace("\r\n", "\n").split("\n")
    sources = {record["source"]: record["selectedLines"] for record in chain["sources"]}
    first = next((l for l in lines if l.strip()), "")
    if not re.fullmatch(r"# B115 confirmation [\u2014\u2013-] " + re.escape(run), plain(first)):
        errors.append(f"Line 1 must be '# B115 confirmation \u2014 {run}'")
    if sum(1 for l in lines if l.startswith("# ")) != 1:
        errors.append("Exactly one level-1 heading is allowed")
    headings = [plain(l[3:]) for l in lines if l.startswith("## ")]
    if tuple(headings) != SECTIONS:
        errors.append("Level-2 headings must be exactly, in order: " + "; ".join(SECTIONS))
    if any(re.match(r"#{4,} ", l) for l in lines):
        errors.append("Headings deeper than level 3 are not allowed")
    section, body = None, {}
    for line in lines:
        if line.startswith("## "):
            section = plain(line[3:])
            body.setdefault(section, [])
        elif section is not None:
            body[section].append(line)
            if line.startswith("### ") and section not in H3_SECTIONS:
                errors.append(f"{section}: level-3 headings are not allowed here")
    get = lambda name: body.get(name, [])

    value = keyed(get("Snapshot"), "Commit", errors, "Snapshot")
    if value is not None and commit not in value:
        errors.append(f"Snapshot: Commit must name {commit}")
    keyed(get("Snapshot"), "Model", errors, "Snapshot")
    keyed(get("Scope"), "Chain", errors, "Scope")
    keyed(get("Scope"), "Fetches", errors, "Scope")

    dispositions = {}
    pattern = re.compile(r"[-*] ([FO][1-9]\d?)" + DASH + "(" + "|".join(DISPOSITIONS) + ")" + DASH + r"(\S.*)")
    for line in top_level(get("Dispositions")):
        match = pattern.fullmatch(plain(line))
        if not match:
            errors.append(f"Dispositions: line {line.strip()!r} is not '- <ID> - <DISPOSITION> - <reason>'")
            continue
        if match[1] in dispositions:
            errors.append(f"Dispositions: {match[1]} appears more than once")
        dispositions[match[1]] = match[2]
    if sorted(dispositions) != sorted(ids):
        errors.append("Dispositions: exactly one line is required for each of " + ", ".join(ids))

    facets = {}
    pattern = re.compile(r"(?:[-*] )?([^:]+):\s*(" + "|".join(FACET_VERDICTS) + r")(?:(?:" + DASH
                         + r"|\s*[;(]\s*)(.*))?")
    for line in top_level(get("Verdicts")):
        match = pattern.fullmatch(plain(line))
        facet = FACET_ALIASES.get(match[1].strip(), match[1].strip()) if match else None
        if facet not in FACETS:
            errors.append(f"Verdicts: line {line.strip()!r} is not '<facet>: <CLEAN|NEEDS FIX|UNVERIFIED>'")
            continue
        if facet in facets:
            errors.append(f"Verdicts: {facet} appears more than once")
        facets[facet] = match[2]
    if sorted(facets) != sorted(FACETS):
        errors.append("Verdicts: exactly one line is required for each of " + "; ".join(FACETS))

    confirmation = keyed(get("Confirmation"), "Verdict", errors, "Confirmation")
    basis = [l for l in top_level(get("Confirmation")) if re.fullmatch(r"(?:[-*] )?Basis:.*", plain(l))]
    if len(basis) > 1 or any(not re.fullmatch(r"(?:[-*] )?Basis:\s*\S.*", plain(l)) for l in basis):
        errors.append("Confirmation: at most one nonempty 'Basis:' line is allowed")
    only_keys(get("Confirmation"), ("Verdict", "Basis"), errors, "Confirmation")
    if confirmation is not None and confirmation not in CONFIRMATION:
        errors.append(f"Confirmation: verdict {confirmation!r} is not CONFIRMED, NEEDS FIX or UNVERIFIED")
        confirmation = None

    findings = items(get("Findings"), "F", sources, errors)
    optional = items(get("Optional"), "O", sources, errors)
    limits = 0
    limit_lines = top_level(get("Limits"))
    if [plain(l) for l in limit_lines] != ["None."]:
        for line in limit_lines:
            match = re.fullmatch(r"[-*] L(\d+):\s*(\S.*)", plain(line))
            if not match or int(match[1]) != limits + 1:
                errors.append(f"Limits: expected '- L{limits + 1}: <limit>', found {line.strip()!r}")
                continue
            limits += 1
        if not limits:
            errors.append("Limits: write either the single line 'None.' or numbered limits")

    named = {f.get("Facet") for f in findings}
    open_items = sorted(i for i, d in dispositions.items() if d not in ACCEPTING)
    for facet in named & set(FACETS):
        if facets.get(facet) != "NEEDS FIX":
            errors.append(f"An F item names {facet}, but that facet is not NEEDS FIX")
    defect = bool(findings) or "NEEDS FIX" in facets.values()
    if "NEEDS FIX" in facets.values() and not findings and not open_items:
        errors.append("A facet is NEEDS FIX without any F item or non-accepting disposition")
    if confirmation == "CONFIRMED" and (defect or open_items):
        errors.append("CONFIRMED requires accepting dispositions only, Findings 'None.' and no NEEDS FIX facet")
    if confirmation == "NEEDS FIX" and not (defect or open_items):
        errors.append("NEEDS FIX requires an F item, a NEEDS FIX facet or a non-accepting disposition")
    if confirmation == "UNVERIFIED" and defect:
        errors.append("UNVERIFIED is not allowed with an F item or a NEEDS FIX facet; use NEEDS FIX")
    message = re.sub(r"\r?\n\Z", "", completion) if completion is not None else None
    if message not in CONFIRMATION:
        errors.append("The coordinator completion message is not an exact confirmation verdict")
    elif confirmation and message != confirmation:
        errors.append(f"Completion message {message} differs from the Confirmation verdict {confirmation}")
    return {"contract": CONTRACT, "status": "FAIL" if errors else "PASS", "errors": errors,
            "confirmation": confirmation, "facets": facets, "dispositions": dispositions,
            "nonAccepting": open_items, "findings": len(findings), "optionalPoints": len(optional),
            "limits": limits, "acceptanceLimit": "Structure only; not linguistic acceptance."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("report", "chain-manifest", "audit"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--run", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--ids", required=True, help="Comma-separated required disposition IDs")
    args = parser.parse_args(argv)
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    messages = json.loads(args.audit.read_bytes()).get("messages") or []
    if not args.report.is_file():
        result = {"contract": CONTRACT, "status": "FAIL", "errors": ["Report is absent"]}
    else:
        result = check(args.report.read_bytes().decode("utf-8"), args.run, args.commit, ids,
                       json.loads(args.chain_manifest.read_bytes()), messages[0] if len(messages) == 1 else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
