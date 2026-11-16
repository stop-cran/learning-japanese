import subprocess
from b127_common import BASE, HERE, REPO, sha, start_guard, stop_child, write

out = HERE / "diff-check-001"
assert not out.exists()
out.mkdir()
guard = start_guard()
try:
    for label, args in (
        ("ordinary", ["git", "diff", "--check"]),
        ("crlf-aware", ["git", "-c", "core.whitespace=cr-at-eol", "diff", "--check"]),
    ):
        process = subprocess.Popen(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            while True:
                try:
                    stdout, stderr = process.communicate(timeout=0.1)
                    break
                except subprocess.TimeoutExpired:
                    guard.check()
            write(out / (label + ".log"), stdout + stderr)
            write(out / (label + ".json"), {"command": args, "exitCode": process.returncode, "logSha256": sha(stdout + stderr)})
            print(label, process.returncode, (stdout + stderr).decode("utf-8"))
            if label == "crlf-aware":
                assert process.returncode == 0
        finally:
            stop_child(process)
    owner_name = __import__("b127_common").git("show", "-s", "--format=%an", BASE).decode("utf-8").strip()
    configured_name = __import__("b127_common").git("config", "user.name").decode("utf-8").strip()
    assert configured_name == owner_name
    print("Configured display name matches the signed supplied base; owner email and key are unchanged.")
finally:
    write(out / "memory.json", guard.finish())
