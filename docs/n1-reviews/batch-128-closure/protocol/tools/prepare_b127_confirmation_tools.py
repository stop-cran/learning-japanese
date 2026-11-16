"""Derive the unchanged confirmation protocol with B127's bounded process helper."""
import json
from pathlib import Path

from b127_lifecycle_process import python
from common import WS, freeze_json, frozen, load_module, require, sha, write_frozen

SOURCE = WS / "scratch-125" / "review" / "confirm"
OUTPUT = WS / "scratch-127" / "review" / "confirm"
PREFLIGHT_SHA = "0630da7d1d0b3097b8614d7ec5fbb49e52e77e7983934d03a506855b78665163"
ENGINE_SHA = "a7a5cbc435295a99caa6be9680b6ed2caf1090df9ced8ace17a48c0210432305"


def main():
    producer = frozen(Path(__file__))
    previous = json.loads(frozen(SOURCE / "tooling-preflight.json", PREFLIGHT_SHA))
    require(previous["status"] == "PASS_PREPARATION_ONLY" and previous["exitCode"] == 0,
            "Predecessor confirmation fixtures did not pass")
    require(not OUTPUT.exists(), "Preserve existing confirmation tooling")
    selected = [item["output"] for item in previous["derivations"]]
    require({Path(item["path"]).name for item in selected} == {
        "audit-confirm.py", "check-confirm-structure.py", "renderer.py",
        "test-audit-confirm-isolated.py", "test-confirm-structure.py",
    }, "Incomplete confirmation protocol")
    derivations = []
    for item in selected:
        source = Path(item["path"])
        original = frozen(source, item["sha256"])
        require(b"B127" not in original, "Ambiguous batch substitution")
        derived = original.replace(b"B125", b"B127")
        require(derived.replace(b"B127", b"B125") == original, "Nonreversible substitution")
        compile(derived, source.name, "exec")
        derivations.append({
            "source": item,
            "output": write_frozen(OUTPUT / source.name, derived),
            "reverseExact": True,
            "soleDelta": "B125 to B127; production protocol and all fixture assertions unchanged",
        })
    tools = Path(__file__).resolve().parent
    source = tools / "confirm_v2.py"
    original = frozen(source, ENGINE_SHA)
    before = b'    done = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")'
    newline = b"\r\n" if b"\r\n" in original else b"\n"
    after = newline.join([
        b"    from b127_lifecycle_process import python",
        b"    code, stdout, stderr = python(*command[2:])",
        b"    done = subprocess.CompletedProcess(command, code, stdout, stderr)",
    ])
    require(original.count(before) == 1 and after not in original, "Final subprocess anchor changed")
    derived = original.replace(before, after)
    require(derived.replace(after, before) == original, "Nonreversible engine derivation")
    compile(derived, "confirm_b127.py", "exec")
    engine = write_frozen(tools / "confirm_b127.py", derived)
    helper = tools / "b127_lifecycle_process.py"
    engine_derivation = {
        "source": {"path": str(source), "sha256": ENGINE_SHA},
        "output": engine,
        "helper": {"path": str(helper), "sha256": sha(frozen(helper))},
        "reverseExact": True,
        "soleDelta": "Final audit capture uses the existing 0.1-second communication and bounded "
                     "cleanup helper; all confirmation admission, chain and audit semantics retained.",
        "before": before.decode("ascii"),
        "after": after.decode("ascii"),
    }
    renderer = load_module("b127_confirmation_renderer", OUTPUT / "renderer.py")
    renderer.self_test()
    code, stdout, stderr = python("-m", "unittest", "discover", "-s", OUTPUT, "-p", "test-*.py")
    log = write_frozen(OUTPUT / "tooling-tests.txt", (stdout + stderr).encode("utf-8"))
    result = {
        "batch": 127,
        "status": "PASS_PREPARATION_ONLY" if code == 0 else "HOLD",
        "sourcePreflight": {"path": str(SOURCE / "tooling-preflight.json"), "sha256": PREFLIGHT_SHA},
        "derivations": derivations,
        "engineDerivation": engine_derivation,
        "exitCode": code,
        "tests": log,
        "rendererChecks": 3,
        "producer": {"path": str(Path(__file__)), "sha256": sha(producer)},
        "limits": "Preparation only. No candidate, confirmation, publication or semantic acceptance. "
                  "Build and final run through run_b127_tool.py for bounded Git. Admission uses "
                  "scoped_confirmation_admission.py and a fresh complete status snapshot; the "
                  "historical unscoped admit and derive commands are not used.",
    }
    print(json.dumps(freeze_json(OUTPUT / "tooling-preflight.json", result)), flush=True)
    print(stdout + stderr, flush=True)
    require(code == 0, "Confirmation protocol regression suite failed")


if __name__ == "__main__":
    main()
