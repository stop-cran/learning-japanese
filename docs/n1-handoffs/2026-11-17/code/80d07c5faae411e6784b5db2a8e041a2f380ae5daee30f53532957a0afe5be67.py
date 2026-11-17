import json
import runpy
import subprocess
import sys
import time
from pathlib import Path
from common_134 import start_guard, stop_child


def bounded_run(*popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs):
    if input is not None:
        if kwargs.get("stdin") is not None:
            raise ValueError("stdin and input cannot both be supplied")
        kwargs["stdin"] = subprocess.PIPE
    if capture_output:
        if kwargs.get("stdout") is not None or kwargs.get("stderr") is not None:
            raise ValueError("capture_output conflicts with stdout/stderr")
        kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen(*popenargs, **kwargs)
    deadline = None if timeout is None else time.monotonic() + timeout
    first = True
    try:
        while True:
            if deadline is not None and time.monotonic() >= deadline:
                raise subprocess.TimeoutExpired(process.args, timeout)
            wait = 0.1 if deadline is None else min(0.1, max(0.001, deadline - time.monotonic()))
            try:
                stdout, stderr = process.communicate(input=input if first else None, timeout=wait)
                break
            except subprocess.TimeoutExpired:
                first = False
                GUARD.check()
        if check and process.returncode:
            raise subprocess.CalledProcessError(process.returncode, process.args, output=stdout, stderr=stderr)
        return subprocess.CompletedProcess(process.args, process.returncode, stdout, stderr)
    finally:
        stop_child(process)


GUARD = start_guard()
subprocess.run = bounded_run
try:
    args = sys.argv[1:]
    if args[0] == "-m":
        sys.argv = args[1:]
        runpy.run_module(args[1], run_name="__main__", alter_sys=True)
    else:
        sys.argv = args
        sys.path.insert(0, str(Path(args[0]).resolve().parent))
        runpy.run_path(args[0], run_name="__main__")
finally:
    print("\nB134 bounded launcher memory:", json.dumps(GUARD.finish()))
