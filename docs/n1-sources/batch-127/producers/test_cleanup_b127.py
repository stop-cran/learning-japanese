import json
import subprocess
from unittest.mock import Mock, patch
import b127_common as common
import run_b127_gates as runner
from b127_common import HERE, sha, write

out = HERE / "cleanup-check-001"
assert not out.exists()
out.mkdir()
results = []


def receipt(name):
    return json.loads((out / (name + ".json")).read_text())


runner.CHECKS["synthetic-success"] = ["-c", "print('synthetic success')"]
runner.run_gate("synthetic-success", out, None)
assert receipt("synthetic-success")["exitCode"] == 0
results.append("real child success and receipt")

runner.CHECKS["synthetic-exit7"] = ["-c", "raise SystemExit(7)"]
try:
    runner.run_gate("synthetic-exit7", out, None)
except RuntimeError:
    assert receipt("synthetic-exit7")["exitCode"] == 7
else:
    raise AssertionError("nonzero child accepted")
results.append("real nonzero child rejected with receipt")

real_start = runner.start_guard


def interrupting_guard():
    guard = real_start()
    guard.check = Mock(side_effect=RuntimeError("synthetic guard interruption"))
    return guard


runner.CHECKS["synthetic-interrupt"] = ["-c", "import time; time.sleep(20)"]
with patch.object(runner, "start_guard", interrupting_guard):
    try:
        runner.run_gate("synthetic-interrupt", out, None)
    except RuntimeError as error:
        assert str(error) == "synthetic guard interruption"
        row = receipt("synthetic-interrupt")
        assert row["childExitCodeAfterCleanup"] is not None
        assert row["activeError"] == "synthetic guard interruption"
    else:
        raise AssertionError("interruption accepted")
results.append("real live child terminated on synthetic guard interruption")

runner.CHECKS["synthetic-cleanup-error"] = ["-c", "pass"]
with patch.object(runner, "stop_child", side_effect=OSError("synthetic cleanup failure")):
    try:
        runner.run_gate("synthetic-cleanup-error", out, None)
    except OSError:
        row = receipt("synthetic-cleanup-error")
        assert row["exitCode"] == 0 and row["cleanupError"] == "synthetic cleanup failure"
    else:
        raise AssertionError("cleanup failure swallowed")
results.append("cleanup error after exited child retains receipt")

child = Mock(args=["synthetic-stuck"])
child.poll.return_value = None
with patch.object(common.time, "monotonic", side_effect=[0, 11, 12, 23]):
    try:
        common.stop_child(child)
    except subprocess.TimeoutExpired:
        pass
    else:
        raise AssertionError("stuck post-kill child accepted")
assert child.terminate.call_count == 1 and child.kill.call_count == 1
results.append("stuck child exhausts bounded terminate and kill deadlines")

child = Mock(args=["synthetic-timeout"])
child.poll.return_value = None
child.wait.side_effect = subprocess.TimeoutExpired(child.args, 0.1)
with patch.object(common.time, "monotonic", side_effect=[0, 0.01, 11]):
    try:
        common.wait_for_exit(child, 10)
    except subprocess.TimeoutExpired:
        pass
    else:
        raise AssertionError("wait deadline ignored")
assert child.wait.call_count == 1 and child.wait.call_args.kwargs["timeout"] <= 0.1
results.append("each exceptional wait remains at most 0.1 seconds")

write(out / "summary.json", {
    "status": "PASS", "cases": results,
    "commonHelperSha256": sha((HERE / "b127_common.py").read_bytes()),
    "runnerSha256": sha((HERE / "run_b127_gates.py").read_bytes()),
    "testSha256": sha(open(__file__, "rb").read()),
    "limits": "Serial synthetic immediate-child checks, including deterministic fake stuck processes; not descendant-process cleanup acceptance.",
})
print(json.dumps({"status": "PASS", "cases": results}))
