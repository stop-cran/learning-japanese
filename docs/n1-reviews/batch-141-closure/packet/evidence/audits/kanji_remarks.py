"""Verify kanji/ changes against BASE: only the batch's new cards are added,
and every modified existing card equals its BASE text with exactly the
declared old->new replacements (line endings normalized).

usage: python kanji_remarks.py REPO BASE REMARKS_JSON K [K ...]
"""
import json, subprocess, sys
from pathlib import Path

repo, base, remarks_path, chars = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4:]


def git(*args):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=repo, capture_output=True)
    return p.returncode, p.stdout.decode("utf-8")


remarks = {}
for it in json.loads(Path(remarks_path).read_text(encoding="utf-8")):
    remarks.setdefault(it["file"], []).append((it["old"], it["new"]))

status = {}
_, out = git("diff", "--name-status", "--no-renames", base, "--", "kanji")
for line in out.splitlines():
    if line.strip():
        st, rel = line.split("\t", 1)
        status[rel] = st
_, out = git("ls-files", "--others", "--exclude-standard", "--", "kanji")
for rel in out.splitlines():
    if rel.strip():
        status[rel.strip()] = "A?"

problems = 0
expected_new = {f"kanji/{k}.md" for k in chars}
for rel in sorted(expected_new):
    if not status.get(rel, "").startswith("A"):
        print(f"MISSING NEW CARD: {rel} (status {status.get(rel, 'unchanged')})")
        problems += 1
edits = 0
for rel, st in sorted(status.items()):
    if rel in expected_new:
        continue
    if st != "M":
        print(f"UNEXPECTED {st}: {rel}")
        problems += 1
        continue
    if rel not in remarks:
        print(f"UNDECLARED EDIT: {rel}")
        problems += 1
        continue
    _, old = git("show", f"{base}:{rel}")
    old = old.replace("\r\n", "\n")
    new = (repo / rel).read_bytes().decode("utf-8").replace("\r\n", "\n")
    for r_old, r_new in remarks[rel]:
        if old.count(r_old) != 1 or r_old in new:
            print(f"REMARK NOT APPLICABLE: {rel}")
            problems += 1
        else:
            old = old.replace(r_old, r_new)
            edits += 1
    if old != new:
        print(f"NOT REMARK-ONLY: {rel}")
        problems += 1
    else:
        print(f"OK remark-only edit: {rel}")
for rel in sorted(set(remarks) - set(status)):
    print(f"REMARK FILE UNCHANGED: {rel}")
    problems += 1
print(f"new cards: {sum(1 for r in status if r in expected_new)}/{len(expected_new)}; "
      f"modified existing cards: {sum(1 for r, s in status.items() if r not in expected_new)}; "
      f"declared remark edits applied: {edits}; problems: {problems}")
sys.exit(1 if problems else 0)
