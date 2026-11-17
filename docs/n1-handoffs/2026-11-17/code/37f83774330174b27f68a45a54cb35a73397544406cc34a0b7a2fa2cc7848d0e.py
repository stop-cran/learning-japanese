"""Persist B120's accepted review and validation evidence without claiming delivery."""
import json
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha, start_guard, write_frozen

CANDIDATE = "c986ae49e844c08afc294d9381c7e486f2c9315d"
INITIAL = "8637cccb25507a1123559041ebba5401203de2db"
MANIFEST_SHA = "000daca2adf350a897a99027de9fda6e310bc18fce6897b69b5e79d10e1a2f29"
SUMMARY_SHA = "985b89011351ab99143beaa14de30c7ac8f5be6c47239b1f3a8a6de63e904810"
REVIEW = WS / "scratch-120" / "review"
GATES = WS / "scratch-120" / "committed-revision-gates-001"
SOURCE_DIR = "docs/n1-sources/batch-120/reconciliation-001"
CARD = "kanji/\u902e.md"
WORD = "words/\u902e\u6355.md"
STROKES = "strokes/\u902e.json"


def verify_closure(provenance):
    require(provenance["reviewedSnapshot"] == CANDIDATE
            and provenance["initialSnapshot"] == INITIAL
            and provenance["publication"] == "PENDING"
            and not provenance["excludedInitialRuns"]
            and not provenance["intermediateRuns"], "Unexpected B120 closure lineage")
    lineage = provenance["reviewLineage"]
    finals = [row for row in lineage if row["finalAcceptance"]]
    initials = [row for row in lineage if row["role"] == "initial"]
    require(len(lineage) == 4 and len(finals) == len(initials) == 2
            and {row["family"] for row in finals} == {"claude", "gpt"}
            and {row["family"] for row in initials} == {"claude", "gpt"}
            and all(row["rawVerdict"] == "UNVERIFIED" and row["snapshot"] == INITIAL for row in initials)
            and all(row["rawVerdict"] == "CONFIRMED" and row["snapshot"] == CANDIDATE
                    and row["confirmationAcceptedOnSnapshot"] and row["priorRun"] is None for row in finals),
            "Both original families must confirm; preserve the UNVERIFIED initials")


def runtime(manifest):
    return {path: digest for entries in manifest.values() if isinstance(entries, dict)
            for path, digest in entries.items()}


def verify_runtime(before, after):
    old, new = runtime(before), runtime(after)
    require(new.keys() - old.keys() == {CARD, STROKES} and old.keys() <= new.keys()
            and {path for path in old if old[path] != new[path]} == {WORD},
            "Unexpected baseline runtime changes")
    require(len(new) == 8702, "Unexpected runtime count")
    return new


def finalize():
    config = load_batch(120)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-120-closure"
    require(config["candidate"] == INITIAL and config["members"] == ["\u902e"], "Batch changed")
    require(git(config, "rev-parse", "HEAD").decode().strip() == CANDIDATE
            and git(config, "show", "-s", "--format=%P", CANDIDATE).decode().strip() == INITIAL
            and git(config, "show", "-s", "--format=%G?|%ae|%ce", CANDIDATE).decode().strip()
            == "G|stop-cran@list.ru|stop-cran@list.ru", "Signed reconciliation changed")
    require(not git(config, "diff", "--name-only") and not git(config, "diff", "--cached", "--name-only"),
            "Tracked files changed since confirmation")
    untracked = git(config, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")
    require(all(not p or p.startswith("docs/n1-reviews/batch-120-closure/") for p in untracked),
            "Unrelated untracked files")
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    verify_closure(provenance)
    guard, _ = start_guard("B120 closure evidence")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(closure / path, digest)
            guard.check()
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        manifest_raw = blob(CANDIDATE, "manifest.json")
        require(sha(manifest_raw) == MANIFEST_SHA, "Confirmed manifest changed")
        manifest = json.loads(manifest_raw)
        current = verify_runtime(json.loads(blob(config["base"], "manifest.json")), manifest)
        require(blob(CANDIDATE, STROKES) == blob(INITIAL, STROKES)
                and blob(CANDIDATE, WORD) == blob(INITIAL, WORD), "Stroke or wrapper changed")
        for path in (CARD, WORD, STROKES):
            require(sha(blob(CANDIDATE, path).replace(b"\r\n", b"\n")) == current[path],
                    f"Runtime manifest binding differs: {path}")
        index = json.loads(blob(CANDIDATE, "docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
        present = {Path(path).stem for path in current if path.startswith("kanji/")}
        require(len(pending) == 1228 and len(pending & present) == 250, "Membership mismatch")
        summary_raw = frozen(GATES / "summary.json", SUMMARY_SHA)
        summary = json.loads(summary_raw)
        require(summary["startingHead"] == CANDIDATE and summary["base"] == config["base"]
                and summary["status"] == "PASS" and summary["cleanBeforeAndAfter"]
                and summary["manifestSha256"] == MANIFEST_SHA
                and set(summary["checks"]) == set(CHECKS), "Wrong committed gate summary")
        artifacts = {"gates/summary.json": summary_raw}
        for name in CHECKS:
            raw, log = frozen(GATES / f"{name}.json"), frozen(GATES / f"{name}.log")
            receipt = json.loads(raw)
            memory = receipt["memory"]
            require(receipt["gate"] == name and receipt["exitCode"] == 0
                    and receipt["logSha256"] == sha(log) and not memory["breach"]
                    and memory["freeRamBeforeBytes"] > 2 * 1024**3
                    and memory["minimumObservedFreeRamBytes"] > 1024**3,
                    f"Failed or changed gate: {name}")
            if name in ("manifest", "manifest-rebuild"):
                require(receipt["manifestSha256"] == MANIFEST_SHA, "Gate manifest differs")
            if name == "manifest-rebuild":
                require(receipt["manifestReproducible"], "Manifest rebuild differed")
            if name == "reading-exposure":
                require(all(text.encode() in log for text in
                            ("\u902e", "\u30c0\u30a4", "\u30c6\u30a4", "\u304a\u3088\u3076")),
                        "Supplemental readings absent from exposure check")
            artifacts[f"gates/{name}.json"], artifacts[f"gates/{name}.log"] = raw, log
            guard.check()
        bindings_raw = blob(CANDIDATE, f"{SOURCE_DIR}/bindings.json")
        bindings = json.loads(bindings_raw)
        for name, ref in bindings["packetFiles"].items():
            raw = blob(CANDIDATE, f"{SOURCE_DIR}/{name}")
            require(sha(raw) == ref["sha256"] and len(raw) == ref["bytes"],
                    f"Signed source binding differs: {name}")
        for name, ref in bindings["externalEvidence"].items():
            raw = frozen(Path(ref["path"]), ref["sha256"])
            require(len(raw) == ref["bytes"], f"External evidence length differs: {name}")
            artifacts[f"external-evidence/{name}{Path(ref['path']).suffix}"] = raw
        artifacts["source-bindings.json"] = bindings_raw
        for name in ("coordinator-candidate-verification.json", "coordinator-revision-verification-001.json",
                     "coordinator-revision-verification-002.json", "coordinator-runtime-glyph-check.json",
                     "source-contract.json"):
            artifacts[f"verification/{name}"] = frozen(REVIEW / name)
        glyph = json.loads(artifacts["verification/coordinator-runtime-glyph-check.json"])
        require(sha(Path(glyph["rareHanSource"]).read_bytes()) == glyph["rareHanSourceSha256"],
                "RareHan source ranges changed")
        glyph_files = {}
        for path in (CARD, WORD):
            raw = blob(CANDIDATE, path)
            hits = sorted({ord(c) for c in raw.decode() if any(a <= ord(c) <= b for a, b in glyph["ranges"])})
            require(not hits, f"Revised runtime needs RareHan assessment: {path}")
            glyph_files[path] = {"signedBlobSha256": sha(raw), "rareHanCodePoints": hits}
        artifacts["verification/revised-glyph-check.json"] = (
            json.dumps({**glyph, "candidate": CANDIDATE, "files": glyph_files}, ensure_ascii=False, indent=2)
            + "\n").encode()
        for folder in ("neutral-dispositions-001", "english-source-display-001"):
            for path in sorted((REVIEW / folder).iterdir()):
                if path.is_file():
                    artifacts[f"derivations/{folder}/{path.name}"] = frozen(path)
        for name in ("finalize_b120.py", "test_finalize_b120.py", "record_publication.py",
                     "test_record_publication.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        artifacts["protocol/run-committed-revision-checks.py"] = frozen(
            WS / "scratch-120" / "run-committed-revision-checks.py",
            "3adf43a5a3390868ae387652026c781e21de9df59382b04bbbcc28a8a93b98c6")
        for name, raw in artifacts.items():
            write_frozen(closure / name, raw)
        ledger = {
            "schemaVersion": 1, "batch": "120", "baseCommit": config["base"], "initialSnapshot": INITIAL,
            "reviewedSnapshot": CANDIDATE, "membership": config["members"], "sourceRows": [1080],
            "status": "textual-review-closed-publication-pending", "drafted": config["members"],
            "reviewClosed": config["members"], "published": [], "runtimePublished": False,
            "accounting": {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 249,
                           "reviewClosedPendingRecordsWithCards": 250, "n2Placements": 6,
                           "publishedN1Additions": 243, "undelivered": 979, "notStarted": 978,
                           "overallN1TaskComplete": False},
            "declaringWords": {"\u902e": ["\u902e\u6355"]}, "requiredLinkPairs": 1, "newWordArticles": 0,
            "runtimeCandidate": {"contentVersion": manifest["contentVersion"], "manifestSha256": MANIFEST_SHA,
                                 "runtimeEntries": len(current)},
            "review": {"status": "closed-with-disclosed-limits", "finalRuns": provenance["finalRuns"],
                       "closure": "../n1-reviews/batch-120-closure/provenance.json",
                       "closureProvenanceSha256": sha(provenance_raw), "remainingActionableFindings": [],
                       "remainingConsequentialClaims": [], "historicalReportsPreserved": True,
                       "identity": "Independent UNVERIFIED initials, reconciled and confirmed serially "
                                   "by the original Claude and GPT reviewers."},
            "sourceEvidence": {"initial": "batch-120/source-receipt.json",
                               "reconciliation": "batch-120/reconciliation-001/bindings.json"},
            "limits": ["Bounded textual and host review, not exhaustive linguistic or arbitrary-pool acceptance.",
                       "No new Kotlin, native, phone, installed-APK or fallback-rendering acceptance.",
                       "Publication, CI and exact served ZIP remain pending; review closure is not delivery.",
                       "Original UNVERIFIED reports, source qualifications and latent custom-pool risks remain preserved."]
        }
        freeze_json(closure / "validation-provenance.json", {
            "batch": 120, "candidate": CANDIDATE, "reviewClosureSha256": sha(provenance_raw),
            "recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING"})
        print(json.dumps(freeze_json(repo / "docs" / "n1-sources" / "batch-120-progress.json", ledger)))
    finally:
        require(not guard.finish()["breach"], "Closure RAM guard breached")


if __name__ == "__main__":
    finalize()
