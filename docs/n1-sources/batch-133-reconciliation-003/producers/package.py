import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write
from notes import PARENT, REL


def main():
    guard = start_guard()
    try:
        packet = REPO / REL
        assert not packet.exists() and git("rev-parse", "HEAD").decode().strip() == PARENT
        for directory in ("author-gates-001", "author-preservation-001"):
            assert json.loads((OUT / directory / "summary.json").read_bytes())["status"] == "PASS"
        sources = json.loads((OUT / "source-bindings.json").read_bytes())
        write(packet / "before-滝.md", (OUT / "before-滝.md").read_bytes())
        write(packet / "after-滝.md", (REPO / "kanji" / "滝.md").read_bytes())
        write(packet / "teaching.diff", git("diff", "--no-ext-diff", PARENT, "--", "kanji/滝.md"))
        decision = OUT.parent / "review" / "claude-confirm-002-adjudication-001.json"
        assert sha(decision.read_bytes()) == "8bba057dd162f4e32c8fa6e0c9243692643dc312fd2e4d2d8548ae1fe2ccf326"
        write(packet / "source" / decision.name, decision.read_bytes())
        write(packet / "source" / "source-bindings.json", (OUT / "source-bindings.json").read_bytes())
        for key in ("log", "receipt"):
            original = Path(sources["preparationFailure"][key]["path"])
            write(packet / "source" / "preparation-failure" / original.name, original.read_bytes())
        write(packet / "source" / "bounded-excerpts.json", {
            "publisher": "小学館 精選版 日本国語大辞典", "url": sources["url"],
            "captureSha256": sources["coordinatorCapture"]["sha256"],
            "completeSectionsSha256": sources["completeSections"]["sha256"],
            "definitions": sources["boundedDefinitions"],
            "scope": "Bounded attributable definition excerpts only; exact line ranges refer to the full frozen coordinator extraction. Complete historical examples and the separate modern-brand publisher section stay local and hash-bound."
        })
        write(packet / "supersession.json", {
            "supersedes": "Only the 滝水 water-from-a-waterfall gloss in 滝 Meaning and the 液 Note rationale, plus the same withdrawn ground in GPT-CONFIRM-001 adjudication 987fb5f9.",
            "correction": "Nikkoku 滝 [2] explicitly abbreviates たきすい, a sake sold in Edo's Kanda; たきみず and ろうすい are distinct waterfall-water readings.",
            "retained": "滝-液 precaution and every other earlier exclusion, distinction, metadata/practice reading, distractor, word, mnemonic, stroke and unrelated line.",
            "historicalRecords": "Original batch-133, reconciliation-001/002, source-only packet and all review verdicts/records remain untouched, including superseded statements.",
            "reviewStatus": "Earlier confirmations/verdicts preserved; new cumulative-delta confirmation remains coordinator-owned. No closure or publication."
        })
        write(packet / "pair-disposition.json", {
            "pair": ["滝", "酒"], "decision": "ADD_QUALIFIED_DIRECT_PRECAUTION",
            "basis": "Nikkoku 滝 [2] -> reading-specific たきすい【滝水】, the named historical sake; actual 酒 title 'alcohol; sake' and full article include alcoholic drink.",
            "directions": {
                "alcoholSakeForWaterfall": "The historical abbreviated drink sense can admit the broad alcohol/sake label, independently of other guards.",
                "waterfallRapidsForAlcohol": "The primary displayed waterfall/rapids label does not mean alcohol. This is a conservative direct secondary-sense guard, not universal synonymy or an assertion that all alcohol is a waterfall."
            },
            "scope": "Append 酒 after 液 only on 滝; direct symmetric exclusion, no transitivity/counterpart edit. The historical abbreviated sense is not taught as modern/generic alcohol.",
            "counterpartBeforeSha256": sha((OUT / "counterpart-酒.md").read_bytes())
        })
        for directory, target in (("author-gates-001", "author-gates"), ("author-preservation-001", "author-preservation")):
            for path in sorted((OUT / directory).iterdir()):
                guard.check()
                if path.is_file():
                    write(packet / target / path.name, path.read_bytes())
        for path in sorted(OUT.glob("*.py")):
            guard.check()
            write(packet / "producers" / path.name, path.read_bytes())
        originals = [(OUT.parent / name, name) for name in
                     ("common_133.py", "run_133_gates.py", "check_reading_133.py", "bounded_launch_133.py")]
        originals += [(OUT.parent / "teaching-reconciliation-002" / "reconcile.py", "reconciliation-002-reconcile.py"),
                      (Path(sources["extractor"]["path"]), "extract_takisui.py")]
        for path, name in originals:
            guard.check()
            write(packet / "producers" / "original" / name, path.read_bytes())
        write(packet / "provenance.json", {
            "parent": PARENT, "decisionSha256": sha(decision.read_bytes()),
            "sourceBindingsSha256": sha((OUT / "source-bindings.json").read_bytes()),
            "authorGatesSummarySha256": sha((OUT / "author-gates-001" / "summary.json").read_bytes()),
            "manifestSha256": sha((REPO / "manifest.json").read_bytes()),
            "scope": "Exactly one card: append 酒, correct the two reading-conflating glosses, add the qualified historical sake Note and one 滝水 citation; preserve all other lines/runtime/earlier evidence.",
            "preservation": "Reuse only frozen reconciliation-002 preserve() through an explicitly bound wrapper; new exact whole-file transformation and direct parent d7d6cff9. No original plan/draft/evidence rewriting.",
            "runners": "gates.py and sign.py are byte-identical copies of reconciliation-002 parameterized by this directory's notes.py; unmodified original ten CHECKS/run_gate retain original creation-base lint/linkplan.",
            "preparationFailure": "Original prepare.py and its failed log/receipt preserved unchanged. prepare_successor.py verifies partial copies and normalizes runtime text only before exact-transform comparison; no source bytes or failed evidence overwritten.",
            "gatePhase": "Serial author gates before signing on the exact packaged runtime; run all ten again on the signed child, retaining committed-phase receipts locally to avoid self-reference.",
            "readingScope": "Metadata/practice readings unchanged. たきすい/たきみず/ろうすい are compound word readings, not new independent 滝 reading keys.",
            "limits": "Not reviewer closure, arbitrary/custom/multiple-borrow pools, Kotlin/native/device, rendering, whole-set or publication acceptance.",
            "delivered": 268, "remaining": 960
        })
        inventory = {}
        for path in sorted(packet.rglob("*")):
            guard.check()
            if path.is_file():
                inventory[str(path.relative_to(packet)).replace("\\", "/")] = {"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
        write(packet / "inventory.json", {"files": inventory, "selfExcluded": True})
        print(json.dumps({"status": "PASS", "files": len(inventory) + 1,
                          "inventorySha256": sha((packet / "inventory.json").read_bytes())}))
    finally:
        write(OUT / "package-memory.json", guard.finish())


if __name__ == "__main__":
    main()
