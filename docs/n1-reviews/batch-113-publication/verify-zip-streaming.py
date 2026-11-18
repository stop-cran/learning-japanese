"""Verify one exact GitHub ZIP with bounded payload memory and a Windows RAM guard.

Variant of the batch-112 verifier: retains its comparisons, but streams download
hashing and keeps only one chunk, the manifest, and ZIP metadata in memory.
Usage: python -B verify-zip-streaming.py <repo-root> <commit> <new-output-dir>
"""
from __future__ import annotations

import _thread
import ctypes
from ctypes import wintypes
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import threading
import urllib.request
import zipfile

sys.dont_write_bytecode = True
VARIANT = "n1-zipverify-streaming-v1"
CHUNK = 64 * 1024
MIN_FREE = 1024 * 1024 * 1024
SAMPLE_SECONDS = 0.25
EXPORT_IGNORED = {"docs", "tools", ".github"}


class MemoryStatus(ctypes.Structure):
    _fields_ = [
        ("dwLength", wintypes.DWORD),
        ("dwMemoryLoad", wintypes.DWORD),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


class ProcessMemory(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
        (name, ctypes.c_size_t)
        for name in (
            "PeakWorkingSetSize", "WorkingSetSize",
            "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
            "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
            "PagefileUsage", "PeakPagefileUsage",
        )
    ]


kernel = ctypes.WinDLL("kernel32", use_last_error=True)
kernel.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MemoryStatus)]
kernel.GlobalMemoryStatusEx.restype = wintypes.BOOL
kernel.GetCurrentProcess.restype = wintypes.HANDLE
psapi = ctypes.WinDLL("psapi", use_last_error=True)
psapi.GetProcessMemoryInfo.argtypes = [
    wintypes.HANDLE, ctypes.POINTER(ProcessMemory), wintypes.DWORD
]
psapi.GetProcessMemoryInfo.restype = wintypes.BOOL


def available_ram() -> int:
    value = MemoryStatus()
    value.dwLength = ctypes.sizeof(value)
    if not kernel.GlobalMemoryStatusEx(ctypes.byref(value)):
        raise ctypes.WinError(ctypes.get_last_error())
    return value.ullAvailPhys


def peak_working_set() -> int:
    value = ProcessMemory()
    value.cb = ctypes.sizeof(value)
    if not psapi.GetProcessMemoryInfo(
        kernel.GetCurrentProcess(), ctypes.byref(value), value.cb
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    return value.PeakWorkingSetSize


class RamGuard:
    def __init__(self) -> None:
        self.before = available_ram()
        self.minimum = self.before
        self.problem: str | None = None
        self.lock = threading.Lock()
        self.stopped = threading.Event()
        self.thread = threading.Thread(target=self.monitor, daemon=True)

    def check(self) -> None:
        with self.lock:
            free = available_ram()
            self.minimum = min(self.minimum, free)
            if free < MIN_FREE:
                self.problem = f"Free RAM below 1024 MiB: {free / 1024**2:.2f} MiB"
            if self.problem:
                raise MemoryError(self.problem)

    def monitor(self) -> None:
        while not self.stopped.wait(SAMPLE_SECONDS):
            try:
                self.check()
            except Exception as error:
                self.problem = str(error)
                _thread.interrupt_main()
                return

    def start(self) -> None:
        self.check()
        self.thread.start()

    def finish(self) -> dict:
        self.stopped.set()
        if self.thread.ident is not None:
            self.thread.join()
        after = available_ram()
        self.minimum = min(self.minimum, after)
        return {
            "freeRamBeforeBytes": self.before,
            "freeRamAfterBytes": after,
            "minimumObservedFreeRamBytes": self.minimum,
            "peakWorkingSetBytes": peak_working_set(),
            "peakScope": "Verifier Python process, including its monitor thread; not subprocess peaks.",
            "abortThresholdBytes": MIN_FREE,
            "samplingIntervalSeconds": SAMPLE_SECONDS,
            "additionalChecks": "Before each file and each streamed chunk; signal interruption on a sampled breach.",
            "breach": self.problem,
        }


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root)


def stream_hashes(stream, guard, *, capture=False, chunk_size=CHUNK):
    raw_hash = hashlib.sha256()
    text_hash = hashlib.sha256()
    captured = bytearray() if capture else None
    pending = b""
    count = 0
    while chunk := stream.read(chunk_size):
        guard.check()
        count += len(chunk)
        raw_hash.update(chunk)
        if captured is not None:
            captured.extend(chunk)
        block = pending + chunk
        pending = b"\r" if block.endswith(b"\r") else b""
        if pending:
            block = block[:-1]
        text_hash.update(block.replace(b"\r\n", b"\n"))
    text_hash.update(pending)
    return count, raw_hash.hexdigest(), text_hash.hexdigest(), captured


def check_stream_hashing(guard) -> None:
    for data in (b"", b"a\r\nb\r", b"\r\r\n\r\n", b"\x00\xff\r\nz"):
        for size in (1, 2, 7):
            count, raw, text, captured = stream_hashes(
                io.BytesIO(data), guard, capture=True, chunk_size=size
            )
            assert count == len(data) and captured == data
            assert raw == hashlib.sha256(data).hexdigest()
            assert text == hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def download(commit: str, dest: Path, guard, max_compressed: int):
    url = f"https://api.github.com/repos/stop-cran/learning-japanese/zipball/{commit}"
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json", "User-Agent": VARIANT}
    )
    if token := os.environ.get("GH_TOKEN"):
        request.add_unredirected_header("Authorization", f"Bearer {token}")
    digest = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(request, timeout=600) as response, dest.open("xb") as out:
        while chunk := response.read(CHUNK):
            guard.check()
            total += len(chunk)
            assert total <= max_compressed
            digest.update(chunk)
            out.write(chunk)
    assert dest.stat().st_size == total
    return url, digest.hexdigest()


def verify(root: Path, commit: str, out_dir: Path, guard) -> dict:
    sys.path.insert(0, str(root / "tools"))
    from build_manifest import build_manifest
    from check_content_budget import (
        CONTENT_FOLDERS, MAX_COMPRESSED, MAX_ENTRIES,
        MAX_INFLATED, MAX_RETAINED, MAX_TASK_MEDIA,
    )

    assert git(root, "rev-parse", "HEAD").decode().strip() == commit
    expected = build_manifest(root)
    assert expected == json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    guard.check()
    check_stream_hashing(guard)
    archive_path = out_dir / f"zipball-{commit[:12]}.zip"
    url, archive_sha = download(commit, archive_path, guard, MAX_COMPRESSED)
    assert archive_path.stat().st_size <= MAX_COMPRESSED
    tree = git(root, "ls-tree", "-r", "-z", "--name-only", commit).decode("utf-8")
    tree_names = {n for n in tree.split("\0") if n and n.split("/")[0] not in EXPORT_IGNORED}
    binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    expected_hashes = {}
    for section, entries in expected.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                expected_hashes.setdefault(name, []).append((section in binary, digest))

    with zipfile.ZipFile(archive_path) as archive:
        rows = archive.infolist()
        names = [row.filename for row in rows]
        assert len(names) == len(set(names)) and len(names) <= MAX_ENTRIES
        roots = {name.split("/")[0] for name in names}
        assert len(roots) == 1, roots
        prefix = roots.pop() + "/"
        assert prefix.endswith(commit[:7] + "/"), prefix
        payload_names = set()
        inflated = retained = task_media = verified = 0
        manifest_bytes = None
        for row in rows:
            guard.check()
            parts = PurePosixPath(row.filename).parts
            assert not row.filename.startswith(("/", "\\")) and "\\" not in row.filename
            assert all(p not in {".", ".."} and ":" not in p for p in parts)
            assert not stat.S_ISLNK(row.external_attr >> 16)
            assert not row.flag_bits & 1
            assert row.filename.startswith(prefix)
            if row.is_dir():
                assert row.file_size == 0
                continue
            name = row.filename[len(prefix):]
            assert name and name.split("/")[0] not in EXPORT_IGNORED, name
            assert inflated + row.file_size <= MAX_INFLATED
            pieces = name.split("/")
            wanted = name == "manifest.json" or len(pieces) == 2 and (
                pieces[0] in CONTENT_FOLDERS or pieces[0] == "images" and name.endswith(".webp"))
            if wanted:
                limit = (150 * 1024 if pieces[0] in {"images", "task-images"} else
                         512 * 1024 if pieces[0] in {"audio", "task-audio"} else 2 * 1024 * 1024)
                assert row.file_size <= limit, name
            with archive.open(row) as stream:
                count, raw_hash, text_hash, captured = stream_hashes(
                    stream, guard, capture=name == "manifest.json"
                )
            assert count == row.file_size
            inflated += count
            payload_names.add(name)
            if wanted:
                retained += count
                if pieces[0] in {"task-audio", "task-images"}:
                    task_media += count
            assert inflated <= MAX_INFLATED
            assert retained <= MAX_RETAINED and task_media <= MAX_TASK_MEDIA
            if name == "manifest.json":
                manifest_bytes = captured
            for is_binary, digest in expected_hashes.get(name, []):
                assert (raw_hash if is_binary else text_hash) == digest, name
                verified += 1
        assert payload_names == tree_names, sorted(payload_names ^ tree_names)[:10]
        assert set(expected_hashes) <= payload_names
        assert verified == sum(len(v) for v in expected_hashes.values())
        assert manifest_bytes is not None and json.loads(manifest_bytes) == expected
        assert bytes(manifest_bytes) == git(root, "show", f"{commit}:manifest.json")
        assert git(root, "rev-parse", "HEAD").decode().strip() == commit
        guard.check()
        return {
            "verifierVariant": VARIANT,
            "baseVerifier": "docs/n1-reviews/batch-112-publication/verify-zip.py",
            "streamHashBoundaryChecks": "12 cases passed, including CRLF across chunks and final lone CR.",
            "commit": commit,
            "url": url,
            "sha256": archive_sha,
            "manifestEqual": True,
            "contentVersion": expected["contentVersion"],
            "manifestSha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "manifestBytesEqualGitBlob": True,
            "verifiedRuntimeHashes": verified,
            "zipEntries": len(rows),
            "zipFiles": len(payload_names),
            "compressedBytes": archive_path.stat().st_size,
            "inflatedBytes": inflated,
            "retainedBytes": retained,
            "listeningTaskMediaBytes": task_media,
            "zipNamesEqualExportedTree": True,
            "allPublishingBudgetsPassed": True,
            "contributorEvidenceExcluded": True,
            "perFileLimitsAndSafePathsPassed": True,
            "pendingChecks": [],
        }


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("The verifier must run with assertions enabled.")
    root, commit, output = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    output.mkdir(parents=True, exist_ok=False)
    guard = RamGuard()
    try:
        guard.start()
        receipt = verify(root, commit, output, guard)
        memory = guard.finish()
        assert not memory["breach"] and memory["minimumObservedFreeRamBytes"] >= MIN_FREE
        receipt["memory"] = memory
        receipt["verifierSha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, indent=2))
    except (Exception, KeyboardInterrupt) as error:
        failure = {
            "verifierVariant": VARIANT,
            "status": "FAILED; no verification receipt",
            "error": repr(error),
            "memory": guard.finish(),
        }
        (output / "failure.json").write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2), file=sys.stderr)
        raise
