import difflib
import json
import re
from pathlib import Path
from recon_common import *
from run_gates import CHECKS

guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    prepared = json.loads((HERE / "manifest-preparation-001" / "summary.json").read_text(encoding="utf8"))
    manifest_raw = (REPO / "manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    assert sha(manifest_raw) == prepared["manifestSha256"]
    teaching = {}
    patch = []
    for ch in ("絹", "虹"):
        rel = f"kanji/{ch}.md"
        old, new = git("show", f"{PARENT}:{rel}"), (REPO / rel).read_bytes()
        a, b = old.replace(b"\r\n", b"\n").decode(), new.replace(b"\r\n", b"\n").decode()
        old_line = re.search(r"^quiz_exclusions:.*$", a, re.M).group()
        new_line = re.search(r"^quiz_exclusions:.*$", b, re.M).group()
        restored = b.replace(new_line, old_line, 1)
        insertions = []
        al, bl = a.splitlines(keepends=True), restored.splitlines(keepends=True)
        for opcode, i1, i2, j1, j2 in difflib.SequenceMatcher(None, al, bl, autojunk=False).get_opcodes():
            if opcode != "equal":
                assert opcode == "insert"
                assert all(line.startswith("- ") for line in bl[j1:j2])
                insertions.extend(bl[j1:j2])
        assert len(insertions) == {"絹": 1, "虹": 3}[ch]
        teaching[rel] = {"rawBeforeSha256": sha(old), "rawAfterSha256": sha(new),
                         "runtimeBeforeSha256": sha(a.encode()), "runtimeAfterSha256": sha(b.encode()),
                         "oldExclusionLine": old_line, "newExclusionLine": new_line,
                         "addedNoteLines": len(insertions), "allOriginalBodyTextPreserved": True,
                         "CRLFBefore": old.count(b"\r\n"), "CRLFAfter": new.count(b"\r\n")}
        patch.extend(difflib.unified_diff(a.splitlines(keepends=True), b.splitlines(keepends=True),
                                          fromfile=PARENT + ":" + rel, tofile="candidate:" + rel))
    write(PACKET / "teaching-diff.patch", "".join(patch).encode())
    write(PACKET / "teaching-change-receipt.json", {
        "parent": PARENT, "runtimeChanges": teaching,
        "manifest": {"rawBeforeSha256": sha(git("show", f"{PARENT}:manifest.json")),
                     "rawAfterSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"]},
        "learnerScope": "Only ordered exclusion suffixes and four new note bullets on the two new cards. 茉, all strokes, all baseline cards and all three existing support wrappers unchanged.",
        "proseException": "None. Do not edit the two inherited CRLF prose blobs or any original B129 packet file.",
        "diffNormalization": "Human-readable diff normalises CRLF to LF; raw hashes separately bind actual bytes.",
    })
    producers = {}
    for path in sorted(HERE.glob("*.py")):
        compile(path.read_text(encoding="utf8"), str(path), "exec")
        raw = path.read_bytes()
        name = "producers/" + path.name
        write(PACKET / name, raw)
        producers[name] = sha(raw)
    for name in ("b129_common.py", "extract_b129.py"):
        path = AUTHOR / name
        raw = path.read_bytes()
        write(PACKET / "producers" / name, raw)
        producers["producers/" + name] = sha(raw)
    tool_names = ["n1_batch_tool.py", "n1lib.py", "quiz_safety.py", "n1_linkplan.py", "reading_exposure.py"]
    tools = {str((ROOT / "lean" / n)): sha((ROOT / "lean" / n).read_bytes()) for n in tool_names}
    for n in ("validate.py", "build_manifest.py", "check_content_budget.py", "grammar_vocabulary.py"):
        tools[str(REPO / "tools" / n)] = sha((REPO / "tools" / n).read_bytes())
    write(PACKET / "validation-plan.json", {
        "parent": PARENT, "batchScopeBase": BASE,
        "baseDistinction": "Lint/linkplan use original B129 introduction base20fda42f; reconciliation direct-child admission/signing uses7c662b37. No changed teaching support or prose exception is needed.",
        "commands": {name: ["python", "-B", *map(str, args)] for name, args in CHECKS.items()},
        "serialGateOrder": list(CHECKS), "preservation": "preserve.py after each complete serial gate run",
        "plannedAuthorDirectories": [str(HERE / "author-gates-001"), str(HERE / "author-preservation-001")],
        "plannedCommittedDirectories": [str(HERE / "committed-gates-001"), str(HERE / "committed-preservation-001")],
        "snapshotBinding": "Final local handoff, outside the Git tree, binds actual author/committed receipts by SHA256 to the signed tree/commit and this self-excluding packet inventory. This plan is not a claim that prospective checks already passed.",
        "process": {"N1_REPO": str(REPO), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1",
                    "ramGuardSha256": GUARD_SHA, "admitFreeGiBAbove": 2, "abortFreeGiBBelow": 1,
                    "sampleSeconds": 0.25, "childWaitMaxSeconds": 0.1, "cleanupMaxSecondsPerStage": 10},
        "producerHashes": producers, "toolHashes": tools,
        "reading": "All18 explicit positive extra target keys, including ぐ, are passed to the bounded host model. Complete original/new family union is canonical-equality checked before deduplication.",
        "limits": "Serial/static host evidence does not confer linguistic, native/device, arbitrary/custom/multi-borrow, rendered-font, whole-set or publication acceptance.",
    })
    readme = """# B129 reconciliation-001

Parent: `7c662b37c647a9b300278abe2e3079fe57f09f83`. Original batch introduction base: `20fda42f7b456889ae4ef82650dde227a139917c`.

This additive author packet resolves the finite F1/L1-SILK/L1-RAINBOW/L3-ADDITIONAL contract: 28 exact pairs, 26 individually qualified direct guards, and two supported bounded noncollision dispositions (絹/結 and 虹/容). It does not relabel GPT's initial NEEDS FIX or Claude's qualified CLEAN verdict, or replace confirmation/publication.

`pair-dispositions.json` binds each actual complete comparison card, strongest secondary evidence, both displayed-label directions and disposition. The three F1 guards protect broad ring/circle/light descriptions; they do not establish unrestricted lexical synonymy or an actual collision in the unchanged three curated meaning options. Original exclusions, ordered metadata, selected practice readings and curated options are preserved. No new word/stroke/support is introduced; all three wrappers remain byte-identical.

`complete-source-receipt.json` and query-membership tables bind pinned compressed/decompressed inputs, complete reserialized JMdict/KANJIDIC2 records, exact predicates, output hashes, canonical equality and zero matches. The くくり follow-up retains its complete three-sense family despite the monolingual positive snare sense being absent from JMdict. Exact 羂索 yields zero bilingual matches; complete monolingual sources retain the trap/Buddhist-cord and Jitsu swing discrepancy. These are not raw XML slices or frequency-filtered fragments.

`external-source-bindings.json` binds all complete local captures and attributable bounded excerpts. Copyrighted raw HTML, all-article JSON and complete monolingual text remain local. Missing image glyphs are not guessed. `claim-source-readset.json` explicitly distinguishes the complete claim families read from other retained homonyms/examples; it is not a claim to have translated every language in the full character records.

`reviewer-response-gpt.json` and `reviewer-response-claude.json` are separate author responses. The citation erratum changes 04-extract.txt:41 to :42 without editing either original report/adjudication. Neither initial reviewer read the separate coordinator ぐ supplement. The original host log omitted グ; its later check gave zero production/target-only padded hits and the same six latent collisions, retaining 橋/攻/責 one-additional-holder risks. The revised checker supplies all18 positive explicit extra keys; its generic 'card text' label is not literal card-prose provenance.

`teaching-change-receipt.json`, `teaching-diff.patch` and `changed-file-inventory.json` delimit the exact change. `evidence-inventory-001.json` self-excludes and hashes every other file in this new packet; it is additive to the unchanged original B129 final inventory003, not a rewrite of it. All older sources, scans, reports, failed attempts, inventories and CRLF dispositions remain frozen. No new prose exception applies.

`validation-plan.json` records actual producers/tools, serial commands, RAM/cleanup constraints and new scratch directories. The final external handoff will bind actual author and exact signed-snapshot gate/preservation receipts, manifest hash/version, signature and cleanliness without a self-referential commit/inventory hash.

JMdict/KANJIDIC2 data: EDRDG, https://www.edrdg.org/ ; source terms and attribution: https://www.edrdg.org/edrdg/licence.html . Monolingual attributions and bounded citations are recorded per source. Complete external captures are not redistributed here.

This remains unpublished B129 author work. Delivered membership remains258/1228 (970 pending); local drafts are not delivered. No reviewer launch, push, publication or B130 work. Preserve all original native/device/font/geometry/whole-set/custom/multi-borrow and source-image limitations.
"""
    write(PACKET / "README.md", readme.encode())
    names = {str(p.relative_to(REPO)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()}
    prefix = str(PACKET.relative_to(REPO)).replace("\\", "/") + "/"
    names.update({prefix + "changed-file-inventory.json", prefix + "evidence-inventory-001.json",
                  "kanji/絹.md", "kanji/虹.md", "manifest.json"})
    write(PACKET / "changed-file-inventory.json", {
        "parent": PARENT, "paths": sorted(names),
        "modifiedInheritedPaths": ["kanji/絹.md", "kanji/虹.md", "manifest.json"],
        "allOtherPaths": "New additive packet files only; original packet/reports/scans/supports unchanged.",
        "selfReference": "Paths include this file and the self-excluding final inventory; all other packet hashes reside in that final inventory.",
    })
    files = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes()) for p in sorted(PACKET.rglob("*")) if p.is_file()}
    write(PACKET / "evidence-inventory-001.json", {
        "packet": "batch-129-reconciliation-001", "parent": PARENT,
        "selfExcluded": "evidence-inventory-001.json",
        "additiveTo": {"path": "docs/n1-sources/batch-129/evidence-inventory-003.json",
                       "sha256": sha((ORIGINAL_PACKET / "evidence-inventory-003.json").read_bytes())},
        "files": files,
    })
    print("Final new packet:", len(files), "other files; inventory", sha((PACKET / "evidence-inventory-001.json").read_bytes()),
          "; manifest", sha(manifest_raw), manifest["contentVersion"])
finally:
    write(HERE / "finalize-memory-001.json", guard.finish())
