"""Change only subprocess execution in the frozen lifecycle tool."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen


def main():
    here = Path(__file__).resolve().parent
    source = here / "step_v2.py"
    raw = frozen(source, "bcb51581e1ef18428ad618a65c728337e23351b801cf2b3192e3089edbcdcdd6")
    text = raw.decode("utf-8")
    before = text[text.index("def python(*args):"):text.index("def audit(")]
    newline = "\r\n" if b"\r\n" in raw else "\n"
    after = "from b127_lifecycle_process import python" + newline * 3
    changes = [(before, after), ("step_v2.py", "step_b127.py")]
    for old, new in changes:
        require(old in text and new not in text, "Ambiguous lifecycle substitution")
        text = text.replace(old, new)
    restored = text
    for old, new in reversed(changes):
        restored = restored.replace(new, old)
    require(restored.encode("utf-8") == raw, "Lifecycle changes are not exactly reversible")
    target = here / "step_b127.py"
    compile(text, str(target), "exec")
    binding = write_frozen(target, text.encode("utf-8"))
    print(json.dumps(freeze_json(here.parent / "scratch-127" / "review" / "lifecycle-derivation.json", {
        "source": str(source), "sourceSha256": sha(raw), "target": binding,
        "helper": {"path": str(here / "b127_lifecycle_process.py"),
                   "sha256": sha(frozen(here / "b127_lifecycle_process.py"))},
        "substitutions": [{"before": old, "after": new} for old, new in changes], "reverseExact": True,
        "scope": "Bound subprocess communication and cleanup; preserve all audit, context, selection, "
                 "extension, report structure and acceptance semantics. Route extension creation through "
                 "the existing bounded Git adapter. Historical scripts and reviewer inputs are unchanged.",
    })))


if __name__ == "__main__":
    main()
