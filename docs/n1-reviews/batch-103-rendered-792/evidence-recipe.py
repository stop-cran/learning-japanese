import datetime
import importlib.util
import shutil
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prep792", C / "prepare-batch-103-rendered-792.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
p.check()
shutil.copyfile(C / "prepare-batch-103-rendered-792.py", p.D / "preparation-recipe.py")
shutil.copyfile(C / "preflight-792.ps1", p.D / "preflight-792.ps1.txt")
shutil.copyfile(C / "start-checkpoint-792.py", p.D / "starting-checkpoint-recipe.py")
shutil.copyfile(Path(__file__), p.D / "evidence-recipe.py")
provenance = p.load(p.D / "source-provenance.json")
resources = p.load(p.D / "review-resources.json")
image_scope = p.load(p.D / "original-png-scope.json")
manifest = p.load(p.R / "manifest.json")
assert manifest["contentVersion"] == "38c32a8df5fd6063"
assert not p.git("diff", "--", "manifest.json", "kanji", "words", "strokes", "articles", "tools")
evidence = {
    "schemaVersion": 1, "execution": 792, "batch": "103",
    "recordedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "stage": "rendered-source-and-original-image-dossier-prepared-not-reviewed",
    "startingState": p.load(p.L / "starting-state-792.json"),
    "sourceSnapshot": p.HEAD, "unchangedTeachingSnapshot": p.TEACHING,
    "qualifiedAndroidHead": p.APP,
    "evidenceDirectory": "docs/n1-reviews/batch-103-rendered-792",
    "reviewResources": resources,
    "reviewResourceBytes": sum(r["bytes"] for r in resources),
    "maximumReviewResourceBytes": max(r["bytes"] for r in resources),
    "sourceInputs": provenance["inputs"],
    "sampledLabelCount": 39, "hostUniqueLabels": 36, "nativeUniqueLabels": 33,
    "newNativeLabels": p.load(p.N / "sampled-labels-and-host-delta.json")["newVersusHost789"],
    "completeDictionaryFamilies": provenance["completeFamilies"],
    "originalDistinctFamiliesPreserved": provenance["originalDistinctFamiliesPreserved"],
    "completeRawCharacterRecords": provenance["rawCharacterRecords"],
    "suppliedArticleBodies": provenance["completeSuppliedArticleBodies"],
    "linkedWordArticleCount": provenance["linkedWordArticles"],
    "originalPngScope": 73, "distinctPngByteHashes": image_scope["distinctByteHashes"],
    "hostExactOptionSets": 64, "nativeExactOptionSets": 64,
    "frozenInputHashesAndDecompressedHashesVerified": True,
    "allApplicableFamilySelectionRecomputedAgainstFullFrozenDictionary": True,
    "everySelectedFamilyAndCharacterEqualToFrozenSource": True,
    "allOriginalNativeArtifactIndexHashesVerified": True,
    "xmlRecordAndJsonValueEqualityAfterWhitespaceCompaction": True,
    "resourceArchiveAndWorkspaceBytesRoundTripVerified": True,
    "intendedOriginalSessions": p.SESSIONS,
    "requestedModelsPresentInFreshActualCliCatalog": p.MODELS,
    "actualNewReviewerModels": [],
    "independentReviewersLaunched": 0,
    "originalSessionConfirmationsExecuted": 0,
    "freshVisualInspections": 0,
    "freshLinguisticReview": False,
    "ordinarySenseFallbackSemanticAcceptance": "UNVERIFIED",
    "independentRenderedReviewClosed": False,
    "runtimeChanged": False, "manifestChanged": False,
    "runtimeHashesVerifiedByRegeneratedManifest": 8463,
    "contentVersion": manifest["contentVersion"],
    "manifestSha256": p.sha(p.R / "manifest.json"),
    "validation": {
        "command": "python -B tools\\validate.py; python -B tools\\build_manifest.py; git diff --exit-code -- manifest.json; git diff --check",
        "observedTerminalExitCode": 0,
        "validatorErrors": 0,
        "manifestFiles": 8463,
        "manifestBytesUnchanged": True,
        "sourceIntegrityCheck": "prepare-batch-103-rendered-792.py check",
        "sourceIntegrityCheckPassed": True,
        "fullPythonOrAndroidOrNativeRerun": False,
    },
    "processDiagnostic": {
        "interruptedCommand": "First start-checkpoint-792.py post-write history assertion repeatedly reloaded the full progress file once per historical key.",
        "disposition": "Stopped that owned bounded shell (tool shellId4), corrected to parse once, resumed verification against original immutable backup and saved starting-state receipt. Every original root value verified unchanged; no lost checkpoint or new permission denial.",
        "historyLoss": False,
    },
    "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
    "actualNewPermissionDenials": [],
    "runtimeAccepted": False, "runtimePublished": False,
    "reviewClosed": [], "published": [], "nextBatchStarted": False,
    "publishedAdditions": 129, "remainingAdditions": 1099,
    "lastPublishedCommit": "a38f4cf554300ce34ee65aada79e87b7c9d0319e",
    "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
    "wholeProjectComplete": False,
    "nextAction": "Two SERIAL ORIGINAL-session rendered confirmations using review-resources.json and respective *-review-task.txt.gz (not superseded *-task.txt.gz/bounded-resources.json), all73 original PNGs, exact128 option sets and complete frozen evidence. Verify fresh exact signed heads/clean worktrees/runner ancestry/session/checkpoint/catalog, original sessions and actual models; audit tool/process serialization and actual returned ranges/images before acceptance. No native rerun/publication/104 at that review checkpoint.",
    "limits": [
        "Preparation and exact byte/record equality only; neither source linguistic approval nor independent reviewer access/comprehension.",
        "Complete applicable family selection is bounded to exact sampled characters, linked spellings/primary readings and preserved original batch/comparison IDs, not every compound containing a character.",
        "333 complete families and120 article bodies are supplied as source access, not claimed freshly read or reviewed. Original textual788, HOST789 and native791 evidence inherited.",
        "73 original image files have33 distinct byte hashes; that is not33 proven unique visual states. No new visual inspection, image rescaling, reconstruction or contactsheet substitution.",
        "Superseded ten-resource raw dossier and original preparation prompts retained; reviewers must use the nine compact review-resource files and respective review-task instead.",
        "Compaction drops insignificant XML whitespace/JSON layout only, preserving every supplied record, sense, restriction, flag and JSON value; numbered record lines are not original XML file line numbers.",
        "Native bounded derivation omits only numerical mechanical guard arrays/repeated pool membership, preserving every exact option set/pool/seed/route assertion; immutable originals and omission counts retained.",
        "All existing source/review/process/denial/OOM/phone limitations and publication/combined-main acceptance gates remain unchanged.",
        "No physical phone, native speaker, unrestricted quiz-safety, general-release, whole-set or new batch acceptance.",
    ],
}
p.save(p.S / "execution-792.json", evidence)
print("Execution792 substantive source-and-image preparation evidence saved; no reviewer or publication claimed.")
