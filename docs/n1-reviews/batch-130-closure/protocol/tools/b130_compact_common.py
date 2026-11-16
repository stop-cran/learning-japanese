"""Shared helpers for the batch-generic N1 review tooling. Outputs are exclusive and ReadOnly."""
import hashlib
import importlib.util
import json
import re
import stat
import subprocess
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
TOOLS = Path(__file__).resolve().parent
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
GUARD = WS / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
SIGNER = "stop-cran@list.ru"
CHECKS = ("lint", "quiz-safety", "linkplan", "reading-exposure", "unittest",
          "validate", "manifest", "manifest-rebuild", "budget", "vocabulary")
SNAP = "evidence/external-snapshots"
NUMBER_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
                "nineteen", "twenty")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def word(n):
    return NUMBER_WORDS[n] if n < len(NUMBER_WORDS) else str(n)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def readonly(path):
    return not Path(path).stat().st_mode & stat.S_IWRITE


def frozen(path, expected=None):
    path = Path(path)
    data = path.read_bytes()
    require(readonly(path), f"Writable frozen input: {path}")
    require(expected is None or sha(data) == expected, f"Changed input: {path}")
    return data


def write_frozen(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
    path.chmod(stat.S_IREAD)
    require(path.read_bytes() == data, f"Readback mismatch: {path}")
    return {"path": str(path), "sha256": sha(data), "bytes": len(data)}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def freeze_json(path, value):
    return write_frozen(path, json_bytes(value))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def start_guard(label):
    require(sha(GUARD.read_bytes()) == GUARD_SHA, "RAM guard changed")
    resource = load_module("n1_ram_guard", GUARD)
    if resource.available_ram() <= 2 * 1024 ** 3:
        raise MemoryError(f"{label} requires more than 2048 MiB free RAM.")
    guard = resource.RamGuard()
    guard.start()
    return guard, resource


def review_dir(batch):
    return WS / f"scratch-{batch}" / "review"


def load_batch(batch):
    path = review_dir(batch) / "batch.json"
    config = json.loads(frozen(path))
    require(config["batch"] == int(batch), "Batch config mismatch")
    for key in ("candidate", "base", "repo", "gates", "members"):
        require(key in config, f"batch.json lacks {key}")
    require(re.fullmatch(r"[0-9a-f]{40}", config["candidate"]) and re.fullmatch(r"[0-9a-f]{40}", config["base"]),
            "Commit identifiers must be full SHA-1")
    config["configSha256"] = sha(path.read_bytes())
    return config


def git(config, *args):
    return subprocess.check_output(["git", "-c", "core.quotepath=false", "-c", "core.autocrlf=false", *args],
                                   cwd=config["repo"])


def at_commit(config, path):
    return git(config, "show", f"{config['candidate']}:{path}")


def packet_dir(config):
    require(config["batch"] == 130, "Compact packet adapter is limited to B130")
    return WS / "review-packets" / f"batch-{config['batch']}-{config['candidate'][:8]}-compact-001"


def verify_packet(config, guard=None):
    root = packet_dir(config)
    raw = frozen(root / "SHA256SUMS.json")
    sums = json.loads(raw)
    for count, (relative, expected) in enumerate(sums.items()):
        if guard and count % 50 == 0:
            guard.check()
        frozen(root / Path(relative), expected)
    on_disk = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    require(on_disk == sorted([*sums, "SHA256SUMS.json"]), "Packet contains unlisted files")
    return root, sums, sha(raw)
