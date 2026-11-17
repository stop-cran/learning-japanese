"""Specialize the preceding preparation without altering its verified evidence."""
import json
import sys
from pathlib import Path

FILES = Path(__file__).resolve().parent
ROOT = Path(r"C:\Users\stop-\n1-kanji-workspace")
sys.path.insert(0, str(ROOT / "review-tools"))
from common import freeze_json, frozen, require, sha, write_frozen
from prepare_b126_publication_tools_v2 import replace

BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
PUBLICATION = "c12af4c508ba7d2f82d92d86569b83e8ad4204f1"


def main():
    prior = json.loads(frozen(FILES / "b133-preparation-001" / "prepared.json"))
    original = frozen(FILES / "prepare-b133-author.py", prior["toolSha256"])
    text = original.decode("utf-8").replace("\r\n", "\n")
    deferred = "B131 left 皇 and 桜 for separate packets because of unresolved native/secondary senses; its notSelected/deferred records apply."
    require(text.count(deferred) == 1, "Deferred scope anchor differs")
    text = text.replace(deferred, "RETAINED_DEFERRED_SCOPE")
    start = text.index("        substitutions = {")
    end = text.index("\n        kickoff_text =", start)
    text = text[:start] + "        substitutions = KICKOFF_REPLACEMENTS" + text[end:]
    changes = {
        "B131": "B132", "B132": "B133", "B133": "B134",
        "b132": "b133", "b133": "b134",
        "scratch-132": "scratch-133", "scratch-133": "scratch-134",
        "batch-132": "batch-133", "batch-133": "batch-134",
        "6858fcfb069cc56a195c3f6ed938f92f657fe96b": BASE,
        "902d6021214aaf28f8bdf41b9920b0d76a79b83c": PUBLICATION,
        "n1-published-membership-6858fcfb.json": "n1-published-membership-e17cb97c.json",
        "268": "271", "262": "265", "960": "957", "133": "134",
    }
    text = replace(text, changes).replace("RETAINED_DEFERRED_SCOPE", deferred)
    kickoff_changes = {
        "B132": "B133", "B133": "B134", "b132": "b133", "b133": "b134",
        "scratch-132": "scratch-133", "scratch-133": "scratch-134",
        "batch-132": "batch-133", "batch-133": "batch-134",
        "6858fcfb069cc56a195c3f6ed938f92f657fe96b": BASE,
        "902d6021214aaf28f8bdf41b9920b0d76a79b83c": PUBLICATION,
        "6932902315": "6937922786",
        "n1-published-membership-6858fcfb.json": "n1-published-membership-e17cb97c.json",
        "268 of 1,228": "271 of 1,228", "960 remain": "957 remain",
        "They contain 墓-specific facts": "They contain 琴/鉛/滝-specific facts",
        "including 嵐 (嵐), 琴 (琴), 紫 (紫), 詩 (詩/詩人), 鉛 (鉛筆), 矢 (矢印) and 滝 (滝)":
            "including 嵐 (嵐), 紫 (紫), 詩 (詩/詩人) and 矢 (矢印)",
        "Recent one-card batches leave substantial work outstanding. Evaluate a practical multi-card subset, approximately 5-10 if complete evidence fits one independent review context, rather than defaulting to one.":
            "B133 delivered three cards; its complete review core measured 1,152,852 UTF-8 bytes before extension and prompt overhead. Select a practical small multi-card subset only if complete source and comparison evidence fits the independent review budget; split on actual complexity, not a row-count target. This byte measurement is not a tokenizer count.",
    }
    table = json.dumps(kickoff_changes, ensure_ascii=True, indent=4)
    table = "\n".join("        " + line if i else line for i, line in enumerate(table.splitlines()))
    text = text.replace("KICKOFF_REPLACEMENTS", table)
    require('ROOT / "b133-worktree", ROOT / "b134-worktree"' in text
            and 'from verify_b133_packet import RUNNER' in text
            and '"271 of 1,228"' in text and BASE in text
            and "B134 AUTHORING ONLY" in text, "Preparation derivation differs")
    compile(text, "prepare-b134-author.py", "exec")
    result = write_frozen(FILES / "prepare-b134-author.py", text.encode("utf-8"))
    print(freeze_json(FILES / "b134-preparation-derivation-001.json", {
        "sourceSha256": sha(original), "successor": result,
        "changes": changes, "kickoffChanges": kickoff_changes,
        "scope": "Same membership, prior-delivery, signature, isolation and resource checks; "
                 "actual B133 delivery constants and bounded next-batch suggestions only.",
    }))


if __name__ == "__main__":
    main()
