import ctypes
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common_132 import HERE, REPO, git, sha, start_guard, write

OUT = Path(__file__).resolve().parent
PARENT = "2e618b38ae5b420f7a1fe6783268093348367c51"
REVIEW = HERE / "review"


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        git("verify-commit", "HEAD")
        fields = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%GF%n%G?", "HEAD").decode().splitlines()
        assert fields == ["Roman Konstantinovskiy", "stop-cran@list.ru", "Roman Konstantinovskiy",
                          "stop-cran@list.ru", "D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "G"]
        expected = {
            "teaching-reconciliation-admission-001/admission.json": "af57b88047fb2d87be36be1df6770555067fc3f8a5e00492288c89cfc8f82b26",
            "source-reconciliation-adjudication-001.json": "fe39f460ee226aaa4753756c7d5d074111cb4ff31839f89a867b95092755d1df",
            "source-reconciliation-verification-001.json": "4f64783f8810d41b778a7ccb2048ca1fc54bcff7c3ed009b20541ddd23b9bc77",
            "source-reconciliation-freeze-001.json": "41b27f638aa6e31e54be7c40bba3f2fd215bbc339f78cfd66670e059b3f66a93",
        }
        for path, digest in expected.items():
            assert sha((REVIEW / path).read_bytes()) == digest, path
        freeze = json.loads((REVIEW / "source-reconciliation-freeze-001.json").read_bytes())
        assert freeze["status"] == "UNCHANGED_BYTES_FROZEN" and len(freeze["files"]) == 64
        get_attrs = ctypes.windll.kernel32.GetFileAttributesW
        get_attrs.argtypes = [ctypes.c_wchar_p]
        get_attrs.restype = ctypes.c_uint32
        for item in freeze["files"]:
            guard.check()
            path = Path(item["path"])
            assert sha(path.read_bytes()) == item["sha256"]
            attrs = get_attrs(str(path))
            assert attrs != 0xffffffff and attrs & 1, str(path)
        raw = git("show", "HEAD:kanji/墓.md")
        assert (REPO / "kanji" / "墓.md").read_bytes() == raw
        write(OUT / "before-墓.md", raw)
        write(OUT / "admission.json", {"candidate": PARENT, "identity": fields, "inputs": expected,
              "previousSourceFreeze": "Previously writable handoff and four reused captures were frozen later by coordinator; no retroactive immutability asserted.",
              "sourceFilesHashAndReadonlyChecked": 64, "producerSha256": sha(Path(__file__).read_bytes())})
        print(json.dumps({"admitted": True, "parent": PARENT, "sourceFiles": 64}))
    finally:
        write(OUT / "admission-memory.json", guard.finish())


if __name__ == "__main__":
    main()
