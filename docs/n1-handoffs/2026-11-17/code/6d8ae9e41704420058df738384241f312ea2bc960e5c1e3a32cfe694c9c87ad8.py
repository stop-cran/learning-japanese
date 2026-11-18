"""Preserve the failed B127 verifier and fix only runtime binary classification."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
SOURCE_SHA = "cbdd80904c022055038bf428c5c1d47099e8a91ca1754c02837cdbddb3910b3d"
HELPER = '''def runtime_entries(manifest):
    binary_sections = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    return {path: (digest, section in binary_sections)
            for section, entries in manifest.items() if isinstance(entries, dict)
            for path, digest in entries.items()}


'''


def main():
    source = HERE / "prepare_b127_candidate.py"
    target = HERE / "prepare_b127_candidate_v2.py"
    raw = frozen(source, SOURCE_SHA)
    changes = [
        ("def main():", HELPER + "def main():"),
        ("        for path, expected in current.items():\n",
         "        for path, (expected, binary) in runtime_entries(manifest).items():\n"),
        ('            binary = Path(path).parts[0] in {"images", "audio", "listeningTaskImages", "listeningTaskAudio"}\n', ""),
    ]
    text = raw.decode("utf-8")
    for before, after in changes:
        require(text.count(before) == 1, "Ambiguous v2 substitution")
        text = text.replace(before, after, 1)
    restored = text
    removed = changes[-1][0]
    anchor = '            raw = (REPO / Path(path)).read_bytes()\n'
    require(restored.count(anchor) == 1, "Ambiguous removed-line anchor")
    restored = restored.replace(anchor, anchor + removed, 1)
    for before, after in reversed(changes[:-1]):
        require(restored.count(after) == 1, "Ambiguous reverse substitution")
        restored = restored.replace(after, before, 1)
    require(restored.encode("utf-8") == raw, "Unexpected v2 changes")
    compile(text, str(target), "exec")
    binding = write_frozen(target, text.encode("utf-8"))
    print(json.dumps(freeze_json(HERE.parent / "scratch-127" / "review" / "candidate-verifier-v2-derivation.json", {
        "source": str(source), "sourceSha256": SOURCE_SHA, "target": binding,
        "changes": changes, "reverseExact": True,
        "reason": "Manifest section names are not filesystem directory names: listeningTaskAudio "
                  "maps to task-audio and listeningTaskImages to task-images. Binary payloads must "
                  "be hashed raw, as tools/build_manifest.py does.",
        "manifestBuilderSha256": "e15e104e463566fce38d3406b52980d362295d4f8840e260aa8d1196c115767f",
        "preservedFailure": "scratch-127/review/bind-signed-candidate-001",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })))


if __name__ == "__main__":
    main()
