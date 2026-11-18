"""Repair only code-line-ending handling in the preserved B123 producer."""
from pathlib import Path

from common import frozen, require, sha


def main():
    original = Path(__file__).with_name("prepare_b123_revision.py")
    raw = frozen(original)
    text = raw.decode("utf-8")
    for old, new in (
        ('original.decode("utf-8").replace("B122", "B123")',
         'original.decode("utf-8").replace("\\r\\n", "\\n").replace("B122", "B123")'),
        ('test_raw.decode("utf-8").replace("verify_b122_revision", "verify_b123_revision")',
         'test_raw.decode("utf-8").replace("\\r\\n", "\\n").replace("verify_b122_revision", "verify_b123_revision")'),
        ('"sources": [{"path": str(source), "sha256": sha(original)},',
         '"preservedProducer": {"path": str(PRESERVED_PRODUCER), "sha256": PRESERVED_SHA},\n'
         '        "codeOnlyNewlineNormalization": True,\n'
         '        "sources": [{"path": str(source), "sha256": sha(original)},'),
    ):
        require(text.count(old) == 1, f"Missing unique repair anchor: {old}")
        text = text.replace(old, new)
    namespace = {
        "__file__": str(Path(__file__).resolve()),
        "__name__": "b123_revision_producer_repaired",
        "PRESERVED_PRODUCER": original,
        "PRESERVED_SHA": sha(raw),
    }
    exec(compile(text, str(original) + "[code-newline-repair]", "exec"), namespace)
    namespace["main"]()


if __name__ == "__main__":
    main()
