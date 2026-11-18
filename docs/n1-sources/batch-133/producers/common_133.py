import gzip
import hashlib
import importlib.util
import json
import os
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
REPO = ROOT / "b133-worktree"
HERE = Path(__file__).resolve().parent
PACKET = REPO / "docs" / "n1-sources" / "batch-133"
BASE = "6858fcfb069cc56a195c3f6ed938f92f657fe96b"
GUARD = ROOT / "scratch-115" / "confirm" / "ram-guard" / "verify-zip-streaming.py"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}
ACTIVE = None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(data, bytes):
        data = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)


def normalized(path):
    return path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")


def start_guard():
    global ACTIVE
    assert os.environ["N1_REPO"] == str(REPO)
    assert sha(GUARD.read_bytes()) == GUARD_SHA
    spec = importlib.util.spec_from_file_location("ramguard_b133", GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.available_ram() > 2 * 1024**3, "Admission requires >2 GiB free"
    ACTIVE = module.RamGuard()
    ACTIVE.start()
    return ACTIVE


def stop_child(process):
    if process is None or process.poll() is not None:
        return
    for action in (process.terminate, process.kill):
        action()
        deadline = time.monotonic() + 10
        while process.poll() is None and time.monotonic() < deadline:
            try:
                process.wait(timeout=min(0.1, max(0.001, deadline - time.monotonic())))
            except subprocess.TimeoutExpired:
                pass
        if process.poll() is not None:
            return
    raise subprocess.TimeoutExpired(process.args, 20)


def git(*args):
    process = subprocess.Popen(["git", "-c", "core.quotepath=false", *args], cwd=REPO,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        while True:
            try:
                out, err = process.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                if ACTIVE:
                    ACTIVE.check()
        if process.returncode:
            raise RuntimeError(err.decode("utf-8", "replace"))
        return out
    finally:
        stop_child(process)


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        data = self.stream.read(size)
        self.digest.update(data)
        return data


def records(source, guard):
    name, compressed, decompressed, tag = INPUTS[source]
    path = ROOT / "control" / "inputs" / name
    assert sha(path.read_bytes()) == compressed
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        parser = ET.iterparse(reader, events=("start", "end"))
        _, root = next(parser)
        for event, node in parser:
            if event == "end" and node.tag == tag:
                yield node
                node.clear()
                root.clear()
    assert reader.digest.hexdigest() == decompressed


def xml_output(path, tag, nodes):
    root = ET.Element(tag)
    root.extend(nodes)
    original = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in root}
    assert len(original) == len(root)
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    write(path, raw)
    assert original == {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
    return {"sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": original}
