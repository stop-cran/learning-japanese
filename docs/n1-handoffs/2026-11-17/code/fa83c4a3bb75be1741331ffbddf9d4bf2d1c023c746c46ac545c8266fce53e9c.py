"""Fix the generated reading literals, retaining failed verifier/test artifacts."""
import json
import os
import subprocess
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen


def main():
    tools = Path(__file__).resolve().parent
    source = tools / "verify_b123_revision.py"
    original = frozen(source)
    old = r'("\\u7bc4", "\\u30cf\\u30f3", "\\u306e\\u308a", "\\u3059\\u3059\\u3080")'
    new = r'("\u7bc4", "\u30cf\u30f3", "\u306e\u308a", "\u3059\u3059\u3080")'
    text = original.decode("utf-8")
    require(text.count(old) == 1, "Expected exactly one escaped-reading tuple")
    repaired = text.replace(old, new)
    require(repaired.replace(new, old) == text, "Unexpected repair delta")
    compile(repaired, "verify_b123_revision_v2.py", "exec")
    records = [write_frozen(tools / "verify_b123_revision_v2.py", repaired.encode("utf-8"))]
    tests = []
    inputs = [{"path": str(source), "sha256": sha(original)}]
    for name in ("test_verify_b123_revision_sources", "test_verify_b123_revision"):
        path = tools / f"{name}.py"
        raw = frozen(path)
        inputs.append({"path": str(path), "sha256": sha(raw)})
        updated = raw.replace(b"verify_b123_revision", b"verify_b123_revision_v2")
        target = name + "_v2"
        tests.append(target)
        records.append(write_frozen(tools / f"{target}.py", updated))
    command = [sys.executable, "-B", "-m", "unittest", "-q", *tests]
    run = subprocess.run(command, cwd=tools, capture_output=True,
                         env={**os.environ, "PYTHONIOENCODING": "utf-8",
                              "PYTHONDONTWRITEBYTECODE": "1"})
    review = WS / "scratch-123" / "review"
    log = write_frozen(review / "b123-revision-tool-tests-v2.log", run.stdout + run.stderr)
    require(run.returncode == 0, (run.stdout + run.stderr).decode("utf-8"))
    result = freeze_json(review / "b123-revision-tooling.json", {
        "batch": 123, "status": "PASS", "sourceFiles": inputs, "derivedFiles": records,
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "repair": "Exactly one reading tuple changed from literal backslash-u text to Unicode "
                  "escapes; tests changed only their target module imports/patch references.",
        "preservedAttempts": ["revision-tooling-preparation-001", "revision-tooling-preparation-002"],
        "command": command, "testLog": log, "testsPassed": 7,
        "limits": "Preparation only; no author-worktree execution, linguistic acceptance or "
                  "complete source-selection verification. Read actual revision schema and runner before use.",
    })
    print((run.stdout + run.stderr).decode("utf-8"))
    print(json.dumps(result))


if __name__ == "__main__":
    main()
