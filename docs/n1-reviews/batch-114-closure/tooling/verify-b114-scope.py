"""Verify B114 source membership and exact preservation of baseline runtime files."""
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(r"C:\Users\stop-\n1-kanji-workspace\rollout-recovered\learning-japanese")
SCRATCH = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-114")
BASE = "0485c873d2ac636373c7bdf739df97ff66f9160f"
FREEZE = "8c2bdc27e5d556e639a4d0e9239ae5f2009c400f"
FIX = "1c2b2c6a6658fa968f724657868ccae1eb61b198"


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-c", "core.quotepath=false",
                                    "-C", str(REPO), *args])


def main():
    selection = json.loads((SCRATCH / "selection.json").read_bytes())
    members = selection["order"]
    assert len(members) == len(set(members)) == 15
    rows = json.loads((REPO / "docs/n1-sources/source-index.json").read_bytes())
    pending = {r["kanji"]: r for r in rows if r["statusAtFreeze"] == "pending"}
    assert len(pending) == 1228
    assert [pending[c]["sourceRow"] for c in members] == selection["sourceRows"]
    head = git("rev-parse", "HEAD").decode().strip()
    assert git("merge-base", head, FIX).decode().strip() == FIX
    expected = {f"{folder}/{c}.{ext}": "A" for c in members
                for folder, ext in (("kanji", "md"), ("strokes", "json"))}
    expected.update({f"words/{w}.md": "M" for ws in selection["declared"].values() for w in ws})
    assert len(expected) == 45
    actual = {}
    for row in git("diff", "--name-status", BASE, head, "--", "kanji", "words", "strokes",
                   "articles", "counters", "grammar", "scenes", "images", "listening", "audio",
                   "curriculum", "listening-tasks", "task-audio", "task-images").decode().splitlines():
        status, path = row.split("\t")
        actual[path] = status
    assert actual == expected, (actual, expected)
    changed = git("diff", "--name-only", FREEZE, FIX, "--", "kanji").decode().splitlines()
    assert set(changed) == {f"kanji/{c}.md" for c in "寮症碁穀穫魅"}
    for path in expected:
        blob = git("show", head + ":" + path)
        assert (REPO / path).read_bytes().replace(b"\r\n", b"\n") == blob, path
    kanji = {p.stem for p in (REPO / "kanji").glob("*.md")}
    assert len(kanji) == 1221
    assert len(list((REPO / "words").glob("*.md"))) == 5083
    present = set(pending) & kanji
    assert len(present) == 231 and len(set(pending) - kanji) == 997
    assert set("保案派第策結") <= present
    old = json.loads(git("show", BASE + ":manifest.json"))
    raw = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(raw)
    assert manifest == json.loads(git("show", head + ":manifest.json"))
    assert manifest["contentVersion"] == "1531e050487c8a64"
    added, modified, removed = [], [], []
    for section in old:
        if not isinstance(old[section], dict):
            if section != "contentVersion":
                assert manifest[section] == old[section], section
            continue
        before, after = old[section], manifest[section]
        added.extend(path for path in after if path not in before)
        removed.extend(path for path in before if path not in after)
        modified.extend(path for path in before if path in after and before[path] != after[path])
    assert not removed and set(added) == {p for p, st in expected.items() if st == "A"}
    assert set(modified) == {p for p, st in expected.items() if st == "M"}
    assert sum(len(v) for v in manifest.values() if isinstance(v, dict)) == 8664
    print(json.dumps({
        "status": "PASS", "head": head, "base": BASE, "freeze": FREEZE, "fix": FIX,
        "sourceRows": selection["sourceRows"], "members": members,
        "baselineRuntimeFilesChanged": modified, "newRuntimeFiles": added,
        "otherBaselineRuntimeFilesAndManifestHashesPreserved": True,
        "teachingEqualsSignedFix": True, "kanjiArticles": len(kanji), "wordArticles": 5083,
        "sourceMembership": {"totalPendingAtFreeze": 1228, "present": 231, "absent": 997,
                             "priorN2Placements": 6, "presentN1Additions": 225},
        "contentVersion": manifest["contentVersion"], "runtimeEntries": 8664,
        "manifestWorkingSha256": hashlib.sha256(raw).hexdigest(),
        "publication": "Not established by this local check.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
