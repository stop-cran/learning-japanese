"""Derive the binary fix while preserving the frozen source's line endings."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen
from derive_b127_candidate_v2 import HELPER, SOURCE_SHA


def main():
    here = Path(__file__).resolve().parent
    source = here / "prepare_b127_candidate.py"
    target = here / "prepare_b127_candidate_v2.py"
    raw = frozen(source, SOURCE_SHA)
    newline = b"\r\n" if b"\r\n" in raw else b"\n"
    require(newline == b"\n" or raw.count(b"\n") == raw.count(b"\r\n"), "Mixed source line endings")

    def encoded(text):
        return text.encode("utf-8").replace(b"\n", newline)

    before_loop = '''        for path, expected in current.items():
            raw = (REPO / Path(path)).read_bytes()
            binary = Path(path).parts[0] in {"images", "audio", "listeningTaskImages", "listeningTaskAudio"}
'''
    after_loop = '''        for path, (expected, binary) in runtime_entries(manifest).items():
            raw = (REPO / Path(path)).read_bytes()
'''
    changes = [(encoded("def main():"), encoded(HELPER + "def main():")),
               (encoded(before_loop), encoded(after_loop))]
    result = raw
    for before, after in changes:
        require(result.count(before) == 1 and after not in result, "Ambiguous binary-fix substitution")
        result = result.replace(before, after, 1)
    restored = result
    for before, after in reversed(changes):
        require(restored.count(after) == 1, "Ambiguous reverse substitution")
        restored = restored.replace(after, before, 1)
    require(restored == raw, "Binary-fix reverse proof failed")
    compile(result, str(target), "exec")
    binding = write_frozen(target, result)
    print(json.dumps(freeze_json(here.parent / "scratch-127" / "review" / "candidate-verifier-v2-derivation.json", {
        "source": str(source), "sourceSha256": SOURCE_SHA, "target": binding,
        "reverseExact": True, "sourceNewline": repr(newline),
        "reason": "Use manifest sections, not directory spellings, to identify binary task audio/images.",
        "preservedFailures": ["scratch-127/review/bind-signed-candidate-001",
                              "scratch-127/review/derive-candidate-verifier-v2-001"],
        "priorDerivationFailure": "LF-only substitution did not match the frozen CRLF source. No target was written.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })))


if __name__ == "__main__":
    main()
