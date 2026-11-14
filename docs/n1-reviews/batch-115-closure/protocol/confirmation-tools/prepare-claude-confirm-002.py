"""Prepare the single authorized fresh confirmation; no reviewer or delivery probe."""
import datetime
import difflib
import hashlib
import importlib.util
import io
import json
import stat
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPTS = HERE / "prompts"
REPO = HERE.parent.parent / "rollout-recovered" / "learning-japanese"
OLD_RUN = "N1-B115-CLAUDE-CONFIRM-001"
RUN = "N1-B115-CLAUDE-CONFIRM-002"
COMMIT = "206f98936307a77937fb38346299af11044af761"
BASE = "f36cd819dcf6ac8b4a3ee8ee29b6e750cd6f09ab"
SENTENCE = ("A response that calls web_fetch must contain, in its own public text, the URL and the reason; "
            "a call with empty public text is a breach.")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bound(path, expected=None):
    path = Path(path)
    data = path.read_bytes()
    assert not path.stat().st_mode & stat.S_IWRITE, path
    assert expected is None or sha(data) == expected, path
    return data


def freeze(path, data):
    with path.open("xb") as stream:
        stream.write(data)
    path.chmod(stat.S_IREAD)
    return {"path": str(path), "sha256": sha(data), "bytes": len(data)}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    guard_module = load("confirm002_guard", HERE / "ram-guard" / "verify-zip-streaming.py")
    assert guard_module.available_ram() >= 2 * 1024**3, "Below preparation startup floor"
    guard = guard_module.RamGuard()
    guard.start()
    try:
        old = json.loads(bound(PROMPTS / f"audit-config-{OLD_RUN}.json",
                              "148857bd4bc43a41e4967fe73fe5740836f48358f1cbd65052979ad699100759"))
        for item in old["files"]:
            guard.check()
            bound(item["path"], item["sha256"])
        chain = json.loads(bound(old["chainManifest"]))
        assert len(chain["segments"]) == 25
        for segment in chain["segments"]:
            guard.check()
            bound(segment["path"], segment["sha256"])
        packet_path = next(Path(f["path"]) for f in old["files"]
                           if Path(f["path"]).name == "packet-manifest.json")
        packet = json.loads(bound(packet_path))
        for relative, item in packet["files"].items():
            guard.check()
            bound(packet_path.parent / relative, item["sha256"])
        git = lambda *args: subprocess.check_output(["git", "-c", "core.quotepath=false", *args], cwd=REPO)
        assert git("rev-parse", "HEAD").decode().strip() == COMMIT
        assert not git("status", "--porcelain")
        assert git("show", "-s", "--format=%G?", COMMIT).decode().strip() == "G"
        assert sha(git("cat-file", "commit", COMMIT)) == "c634f1bd5bc4a8fc774db6e76d210d036eff4c7b85eb9dc84a681c0dcb0e8a9e"
        assert sha(git("diff", "--no-color", "--binary", BASE, COMMIT)) == "4c016f3544ef8ace083b0eb4753b8ec4b12ca80131e61397f4f5a0225b594bda"
        assert sha(bound(packet_path.parent / "diffs" / "fix.patch")) == "eedd3585d6860f0011c48be42931453ab85d74ce834efe90d76aa4ccbb681ba6"

        fixtures = load("confirm002_fixtures", HERE / "test-audit-confirm.py")

        class EmptyAnnouncement(fixtures.Fixture):
            def test_empty_public_fetch_text_is_void(self):
                self.call("web_fetch", {"url": "https://example.org/fixture"}, text="")
                self.assertVoid("same-response URL", final=False)

        suite = unittest.defaultTestLoader.loadTestsFromModule(fixtures)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(EmptyAnnouncement))
        output = io.StringIO()
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
        test_log = freeze(HERE / "confirm-002-fabricated-tests.txt", output.getvalue().encode("utf-8"))
        assert result.wasSuccessful() and result.testsRun == 13, output.getvalue()

        replacements = [
            (OLD_RUN, RUN),
            (old["report"], str(HERE.parent.parent / "reports-115" / "confirm-claude-002.md")),
            (old["prompt"], str(PROMPTS / "confirm-claude-115-002.txt")),
        ]
        original = bound(old["prompt"])
        revised = original
        changes = []
        for before, after in replacements:
            count = revised.count(before.encode("utf-8"))
            assert count > 0
            revised = revised.replace(before.encode("utf-8"), after.encode("utf-8"))
            changes.append({"before": before, "after": after, "occurrences": count})
        rule = [line for line in revised.splitlines(keepends=True)
                if line.startswith(b"5. Up to three optional web_fetch")]
        assert len(rule) == 1 and rule[0].endswith(b"\n")
        line = rule[0]
        newline = b"\r\n" if line.endswith(b"\r\n") else b"\n"
        revised = revised.replace(line, line[:-len(newline)] + b" " + SENTENCE.encode() + newline, 1)
        restored = revised.replace(b" " + SENTENCE.encode(), b"", 1)
        for before, after in reversed(replacements):
            restored = restored.replace(after.encode("utf-8"), before.encode("utf-8"))
        assert restored == original and revised.count(SENTENCE.encode()) == 1
        assert not Path(replacements[1][1]).exists()
        prompt = freeze(Path(replacements[2][1]), revised)
        kickoff_data = bound(old["kickoff"]).replace(old["prompt"].encode("utf-8"),
                                                   prompt["path"].encode("utf-8"))
        assert not kickoff_data.endswith((b"\r", b"\n"))
        kickoff = freeze(PROMPTS / "kickoff-claude-115-002.txt", kickoff_data)
        config = dict(old, run=RUN, report=replacements[1][1], prompt=prompt["path"], kickoff=kickoff["path"])
        config["files"] = [
            {"path": prompt["path"], "sha256": prompt["sha256"]} if f["path"] == old["prompt"] else
            {"path": kickoff["path"], "sha256": kickoff["sha256"]} if f["path"] == old["kickoff"] else dict(f)
            for f in old["files"]
        ]
        config_file = freeze(PROMPTS / f"audit-config-{RUN}.json",
                             (json.dumps(config, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        diff = freeze(HERE / "confirm-002-prompt.diff", "".join(difflib.unified_diff(
            original.decode("utf-8").splitlines(keepends=True),
            revised.decode("utf-8").splitlines(keepends=True), fromfile=old["prompt"],
            tofile=prompt["path"])).encode("utf-8"))
        guard.check()
    finally:
        memory = guard.finish()
    assert memory["breach"] is None
    record = {
        "run": RUN, "decisionSourceToolCallId": "toolu_01G7KGdcahpRRvBq12HWSVW8",
        "decisionOrigin": "Coordinator decision; not represented as a new human instruction.",
        "preparedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "candidate": COMMIT, "base": BASE, "originalPromptSha256": sha(original),
        "identityReplacements": changes, "prospectiveClarification": SENTENCE,
        "exactReversalVerified": True, "chainManifest": old["chainManifest"],
        "chainSegments": 25, "packet": str(packet_path.parent), "packetFiles": len(packet["files"]),
        "prompt": prompt, "kickoff": kickoff, "auditConfig": config_file, "diff": diff,
        "fabricatedTests": test_log, "fabricatedTestsPassed": result.testsRun,
        "generatorSha256": sha(bound(Path(__file__))), "memory": memory,
        "reviewerLaunched": False, "syntheticSessionOrDeliveryProbe": False,
        "quarantinedOutputReadOrUsed": False,
    }
    preflight = freeze(PROMPTS / f"preflight-{RUN}.json",
                       (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"prompt": prompt, "kickoff": kickoff, "auditConfig": config_file,
                      "preflight": preflight, "tests": result.testsRun, "memory": memory}, indent=2))


if __name__ == "__main__":
    main()
