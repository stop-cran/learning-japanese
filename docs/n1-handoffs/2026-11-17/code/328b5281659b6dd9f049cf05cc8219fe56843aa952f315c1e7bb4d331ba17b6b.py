"""Coordinator mechanical verification of the B134 revision-002 descendant of 355cccb.

Usage: verify-b134-revision002.py FULL_COMMIT NEW_REVIEW_OUTPUT_DIRECTORY
Checks lineage/signing, exact change scope, the 紫 card delta and runtime preservation.
It is not semantic adjudication, reviewer confirmation, closure or publication acceptance.
"""
import json
import re
import sys
from pathlib import Path

from common import freeze_json, require, sha, start_guard, write_frozen
from run_b134_closure_checks import HERE, REPO, validate_lineage
from verify_b134_payload import RUNNER, runtime_entries
from verify_b134_sources import Git, ORIGIN

REVIEWED = "355cccb840d22e7313e79f234eb93d1367e00352"
TARGET = "kanji/\u7d2b.md"
ADDED = ["\u6fc3", "\u98df"]
COMPARISONS = [f"kanji/{c}.md" for c in ADDED]
OLD_COUNT = 56
EVIDENCE_PREFIX = re.compile(r"docs/n1-sources/batch-134-[a-z0-9-]+/")
FULL = re.compile(r"[0-9a-f]{40}")


def split_card(text):
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    require(lines[0] == "---", "Card lacks front matter")
    end = lines.index("---", 1)
    fields, order = {}, []
    for line in lines[1:end]:
        key, sep, value = line.partition(":")
        require(sep and key.strip() and key.strip() not in fields, f"Bad front matter line: {line}")
        fields[key.strip()] = value.strip()
        order.append(key.strip())
    body = "\n".join(lines[end + 1:])
    sections, current = {}, "__lead__"
    sections[current] = []
    for line in body.split("\n"):
        if line.startswith("## "):
            current = line
            require(current not in sections, f"Duplicate section: {line}")
            sections[current] = []
        sections[current].append(line)
    return fields, order, {k: "\n".join(v) for k, v in sections.items()}


def listing(value):
    require(value.startswith("[") and value.endswith("]"), f"Unexpected list syntax: {value}")
    inner = value[1:-1].strip()
    return [item.strip() for item in inner.split(",")] if inner else []


def bullets(section):
    found, current = [], None
    for line in section.split("\n")[1:]:
        if line.startswith("- "):
            current = [line]
            found.append(current)
        elif line.startswith("  ") and current is not None:
            current.append(line)
        else:
            current = None
    return ["\n".join(b) for b in found]


def check_card_delta(old_text, new_text):
    old_fields, old_order, old_sections = split_card(old_text)
    new_fields, new_order, new_sections = split_card(new_text)
    require(old_order == new_order, "Front-matter key order or inventory changed")
    require({k: v for k, v in old_fields.items() if k != "quiz_exclusions"}
            == {k: v for k, v in new_fields.items() if k != "quiz_exclusions"},
            "Front matter changed beyond quiz_exclusions")
    old_ex, new_ex = listing(old_fields["quiz_exclusions"]), listing(new_fields["quiz_exclusions"])
    require(len(old_ex) == OLD_COUNT == len(set(old_ex)), "Unexpected prior exclusion inventory")
    require(len(new_ex) == len(set(new_ex)) == OLD_COUNT + len(ADDED)
            and set(new_ex) == set(old_ex) | set(ADDED) and not set(ADDED) & set(old_ex),
            "Exclusions are not exactly the prior set plus 濃/食")
    distractors = set(listing(new_fields["distractors"]))
    require(not distractors & set(ADDED), "Added exclusion is also a curated distractor")
    require(list(old_sections) == list(new_sections), "Section inventory or order changed")
    changed = [k for k in old_sections if old_sections[k] != new_sections[k]]
    require(set(changed) <= {"## Notes"}, f"Sections beyond Notes changed: {changed}")
    old_b, new_b = bullets(old_sections["## Notes"]), bullets(new_sections["## Notes"])
    require(all(b in new_b for b in old_b), "A prior Notes bullet was removed or altered")
    added = [b for b in new_b if b not in old_b]
    joined = "\n".join(added)
    require(all(c in joined for c in ADDED), "New Notes do not explain both 濃 and 食 precautions")
    return {"priorExclusions": len(old_ex), "exclusions": len(new_ex),
            "appendedInOrder": new_ex == old_ex + ADDED, "changedSections": changed,
            "priorNotesBullets": len(old_b), "addedNotesBullets": len(added),
            "addedNotesChars": len(joined)}


def check_inventory(changes, existed):
    """changes: [(status, path)] for REVIEWED..commit; existed(path) -> bool at REVIEWED."""
    by_path = dict((p, s) for s, p in changes)
    require(len(by_path) == len(changes), "Duplicate changed path")
    require(by_path.get(TARGET) == "M" and by_path.get("manifest.json") == "M",
            "Card or manifest not modified")
    rest = {p: s for p, s in by_path.items() if p not in (TARGET, "manifest.json")}
    prefixes = {EVIDENCE_PREFIX.match(p).group(0) if EVIDENCE_PREFIX.match(p) else None for p in rest}
    require(rest and None not in prefixes and len(prefixes) == 1,
            "Contributor evidence is missing or outside one batch-134 source directory")
    prefix = prefixes.pop()
    require(all(s == "A" for s in rest.values()) and not existed(prefix.rstrip("/")),
            "Contributor evidence is not purely additive in a new directory")
    return prefix, sorted(rest)


def check_manifest_delta(old, new):
    before, after = runtime_entries(old), runtime_entries(new)
    require(before.keys() == after.keys(), "Runtime paths added or removed")
    require({p for p in before if before[p] != after[p]} == {TARGET},
            "Runtime changes exceed the revised card")
    other_old = {k: v for k, v in old.items() if not isinstance(v, dict) and k != "contentVersion"}
    other_new = {k: v for k, v in new.items() if not isinstance(v, dict) and k != "contentVersion"}
    require(other_old == other_new, "Non-runtime manifest fields changed beyond contentVersion")
    return {"runtimeEntries": len(after), "contentVersion": new.get("contentVersion")}


def parse_name_status(raw):
    parts = raw.split(b"\0")
    require(parts[-1] == b"", "Unterminated name-status")
    parts = parts[:-1]
    require(len(parts) % 2 == 0, "Odd name-status output")
    return [(parts[i].decode(), parts[i + 1].decode("utf-8")) for i in range(0, len(parts), 2)]


def main(commit, output):
    require(FULL.fullmatch(commit) and commit != REVIEWED, "Use the full signed descendant identity")
    require(output.parent == HERE / "review" and not output.exists(), "Use a new B134 review output")
    guard, _ = start_guard("B134 revision-002 coordinator verification")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == commit
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Signed revision checkout is not clean at the commit")

        clean()
        git("merge-base", "--is-ancestor", REVIEWED, commit)
        rows = [r for r in git("log", "--reverse", "--format=%H|%P|%G?|%GF|%ae|%ce",
                                f"{REVIEWED}..{commit}").decode().splitlines() if r]
        bodies = [git("show", "-s", "--format=%B", r.split("|")[0]) for r in rows]
        depth = validate_lineage(rows, bodies, REVIEWED, commit)
        changes = parse_name_status(git("diff", "--no-renames", "--name-status", "-z",
                                        REVIEWED, commit, "--"))

        def existed(path):
            return bool(git("ls-tree", "--name-only", REVIEWED, "--", path).strip())

        prefix, evidence_paths = check_inventory(changes, existed)
        blob = lambda name, ref=commit: git("show", f"{ref}:{name}")
        signed = {p: blob(p) for _, p in changes}
        require(all((REPO / p).read_bytes() == raw for p, raw in signed.items()),
                "Working bytes differ from signed blobs")
        card = check_card_delta(blob(TARGET, REVIEWED).decode("utf-8"), signed[TARGET].decode("utf-8"))
        manifest = check_manifest_delta(json.loads(blob("manifest.json", REVIEWED)),
                                        json.loads(signed["manifest.json"]))
        comparisons = {}
        for name in COMPARISONS:
            old, new = blob(name, REVIEWED), blob(name)
            require(old == new, f"Comparison card changed: {name}")
            comparisons[name] = sha(new)
        clean()
        bindings = {"snapshot/" + p: write_frozen(output / "snapshot" / p, raw) for p, raw in signed.items()}
        result = {
            "batch": 134, "status": "PASS", "reviewed": REVIEWED, "commit": commit,
            "lineageDepth": depth, "evidencePrefix": prefix, "evidencePaths": evidence_paths,
            "signedFiles": {p: sha(raw) for p, raw in signed.items()}, "card": card,
            "manifest": manifest, "unchangedComparisonCards": comparisons, "bindings": bindings,
            "verifierSha256": sha(Path(__file__).read_bytes()),
            "limits": "Mechanical scope/lineage/runtime only; no semantic adjudication, gate execution, "
                      "reviewer confirmation, closure, integration or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Revision verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output / "verification.json", result), ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]).resolve())
