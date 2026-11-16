"""Prepare isolated original-family confirmations of the verified B125 reconciliation-002 candidate."""
import json
import re
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha, write_frozen
from confirm_v2 import build, clean

SCRATCH = WS / "scratch-125"
REVIEW = SCRATCH / "review"
CANDIDATE = "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
PARENT = "49d0b00d438969b157e739360f8639c6a9b0d950"
PROOF_SHA = "ab5977465cacf873bd565e2761a1bafbdfcc1d044c8bf7ae06a7f214660e196d"
TOOLING_SHA = "0630da7d1d0b3097b8614d7ec5fbb49e52e77e7983934d03a506855b78665163"
COMMITTED_SUMMARY_SHA = "f79fef485ccd994ab77d720d03c9a444a54f9c23354e129df3e48d9035837aba"
CAPTURE_DIR = SCRATCH / "reconciliation-002-source-captures-001"
CAPTURE_RECEIPT_SHA = "22806123d130640b2b1b771a399195191a2287cc560fb67e644d76c85c68832e"
CAPTURES = {"凌": "ryo.html", "占": "sen.html", "侵": "shin.html"}
R1 = "docs/n1-sources/batch-125-reconciliation/"
R2 = "docs/n1-sources/batch-125-reconciliation-002/"
GUARDS = "犯冒害攻撃入損痛討略戦患病毒破触違突徹凌占"
DISTRACTORS = "寝進掃"
DISPOSITION_IDS = {*(f"Q{i}" for i in range(1, 14)), "F1-討", "F1-痛"}
REVIEWERS = {
    "claude": ("094f79c1-7820-4520-9bd9-d799aaff7525", "N1-B125-CLAUDE-001",
               "014417a41f60fd3e8d7ebe4520de5ac46825eb7d3120a910da395ea214c7ab95"),
    "gpt": ("63aefa5e-b5f3-4d20-bf2e-0b26ec19dc95", "N1-B125-GPT-002",
            "7fd68d65752071da9a10f32c869ab09d591eb228b8da8c4a4146f5ad1b7fa38a"),
}
PROVENANCE = re.compile(r"\bclaude\b|\bgpt\b|NEEDS FIX|CONFIRMED", re.I)
SUMMARY_KEYS = ("batch", "candidate", "parent", "originalCandidate", "signature", "addedDirectGuards",
                "dispositionsSha256", "sourceReceiptSha256", "manifestSha256", "contentVersion",
                "runtimeEntries", "gates", "integrityReceipts")


def shared_is_neutral(raw):
    return not PROVENANCE.search(raw.decode("utf-8"))


def response_is_isolated(family, raw):
    other = {"claude": "gpt", "gpt": "claude"}[family]
    return not re.search(rf"\b{other}\b", raw.decode("utf-8"), re.I)


def lf_derivative(raw):
    """Chain inputs must end in LF; append exactly one so the original is derivative[:-1]."""
    require(not raw.endswith(b"\n"), "Capture already ends with LF")
    raw.decode("utf-8")
    return raw + b"\n"


def neutral_summary(proof):
    summary = {key: proof[key] for key in SUMMARY_KEYS}
    summary["changedFiles"] = [p for p in proof["changedFiles"] if not p.endswith("-response-002.md")]
    summary["captures"] = [{key: item[key] for key in ("character", "url", "sha256", "bytes")}
                           for item in proof["captures"]]
    summary.update(
        omittedFromChangedFiles="Family-specific author responses; each family receives only its own.",
        status="PASS_MECHANICAL_ONLY", semanticAcceptance=False, sourceProofSha256=PROOF_SHA,
        limits="Verified signed bytes, exact delta, bound complete captures and twenty host gate "
               "receipts only. Author dispositions are proposals for independent evaluation; no "
               "semantic harmlessness, review confirmation or publication acceptance is implied.")
    return summary


def exclusions(card):
    front = card.decode("utf-8").split("---", 2)[1]
    parse = lambda key: "".join(re.search(rf"(?m)^{key}: \[(.*)\]\r?$", front)[1].split(", "))
    return parse("quiz_exclusions"), parse("distractors")


def additional(path, source):
    return {"path": str(path), "source": source, "sha256": sha(frozen(path))}


def main():
    config = load_batch(125)
    clean(config, CANDIDATE)
    require(git(config, "rev-parse", f"{CANDIDATE}^").decode().strip() == PARENT, "Unexpected parent")
    proof = json.loads(frozen(REVIEW / "reconciliation-002-independent-proof.json", PROOF_SHA))
    require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE and proof["parent"] == PARENT
            and proof["reviewAccepted"] is False and proof["confirmationAccepted"] is False,
            "Independent verification is not a pass on this candidate")
    tooling = json.loads(frozen(REVIEW / "confirm" / "tooling-preflight.json", TOOLING_SHA))
    require(tooling["status"] == "PASS_PREPARATION_ONLY" and tooling["exitCode"] == 0,
            "Confirmation tooling preparation missing")
    for item in tooling["derivations"]:
        frozen(Path(item["output"]["path"]), item["output"]["sha256"])
    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    card = blob("kanji/侵.md")
    require(exclusions(card) == (GUARDS, DISTRACTORS), "Card guards or distractors changed")
    r2 = json.loads(blob(R2 + "dispositions.json"))
    require(sha(blob(R2 + "dispositions.json")) == proof["dispositionsSha256"]
            and sha(blob(R2 + "source-receipt.json")) == proof["sourceReceiptSha256"],
            "Verified disposition or receipt changed")
    rows = r2["unchanged"] + r2["revisions"]
    require({row["id"] for row in rows} == DISPOSITION_IDS and len(rows) == len(DISPOSITION_IDS)
            and all(row["status"] == "direct_guard" and row["endpoint"] == "侵" for row in rows)
            and {row["other"] for row in rows} <= set(GUARDS), "Finite disposition inventory changed")
    neutral = REVIEW / "confirmation-001-neutral"
    require(not neutral.exists(), "Preserve existing neutral sources")
    summary_path = neutral / "verification-summary.json"
    freeze_json(summary_path, neutral_summary(proof))
    shared = [additional(summary_path, "verification/signed-correction-summary.json")]
    gate_dir = SCRATCH / "reconciliation-002-committed-gates-001"
    frozen(gate_dir / "summary.json", COMMITTED_SUMMARY_SHA)
    logs = {row["gate"]: row["logSha256"] for row in proof["gates"]["committed"]}
    require(set(logs) == set(CHECKS), "Committed gate set differs")
    shared.append(additional(gate_dir / "summary.json", "committed-checks/summary.json"))
    for gate in CHECKS:
        frozen(gate_dir / f"{gate}.log", logs[gate])
        shared.append(additional(gate_dir / f"{gate}.log", f"committed-checks/{gate}.log"))
    receipt_path = CAPTURE_DIR / "capture-receipt.json"
    receipt = json.loads(frozen(receipt_path, CAPTURE_RECEIPT_SHA))
    declared = {item["character"]: item for item in proof["captures"]}
    require(set(declared) == set(CAPTURES), "Capture inventory changed")
    derivations, capture_sources = [], []
    for char, name in CAPTURES.items():
        original = frozen(CAPTURE_DIR / name, declared[char]["sha256"])
        row = next(item for item in receipt["captures"] if item["sha256"] == declared[char]["sha256"])
        require(row["status"] == 200 and row["finalUrl"] == row["url"] == declared[char]["url"],
                "Capture receipt mismatch")
        stem = name.removesuffix(".html")
        derived = write_frozen(neutral / "external-snapshots" / f"{stem}-response-plus-lf.html",
                               lf_derivative(original))
        label = f"evidence/external-snapshots/reconciliation-002/{stem}-response-plus-lf.html"
        derivations.append({"character": char, "url": row["url"], "label": label,
                            "original": {"path": str(CAPTURE_DIR / name), "sha256": sha(original),
                                         "bytes": len(original)},
                            "derivative": derived})
        capture_sources.append(additional(Path(derived["path"]), label))
    derivation_path = neutral / "capture-derivatives.json"
    freeze_json(derivation_path, {
        "batch": 125, "candidate": CANDIDATE, "captures": derivations,
        "transformation": "Complete HTTP response bytes followed by exactly one appended LF, because "
                          "read-chain inputs must end in LF. Removing that final byte restores the "
                          "original capture exactly; no other byte is changed.",
        "retention": "Complete captures remain local and are not redistributed in published archives.",
    })
    shared.append(additional(derivation_path, "evidence/reconciliation-002-capture-derivatives.json"))
    shared.append(additional(receipt_path, "evidence/reconciliation-002-capture-receipt.json"))
    shared.extend(capture_sources)
    revised = ["kanji/侵.md", "words/侵入.md"]
    revised += [f"kanji/{char}.md" for char in sorted(set(GUARDS + DISTRACTORS))]
    revised += ["docs/n1-sources/batch-125/jmdict-selected-records.xml",
                "docs/n1-sources/batch-125/kanjidic2-selected-records.xml"]
    revised += [R1 + name for name in ("dispositions.json", "source-receipt.json", "jmdict-records.xml",
                                       "kanjidic2-records.xml")]
    revised += ["docs/n1-sources/batch-125-supplement/jmdict-records.xml",
                "docs/n1-sources/batch-125-supplement/kanjidic2-records.xml"]
    revised += [R2 + "dispositions.json", R2 + "source-receipt.json"]
    originals = ["evidence/external-snapshots/01-extract.txt", "evidence/external-snapshots/manifest.json"]
    for raw in [*(blob(path) for path in revised), *(frozen(Path(item["path"])) for item in shared)]:
        require(shared_is_neutral(raw), "Cross-review material in shared evidence")
    freeze_json(REVIEW / "confirmation-001-source-adjudication.json", {
        "batch": 125, "candidate": CANDIDATE, "status": "READY_FOR_INDEPENDENT_CONFIRMATIONS",
        "verificationSha256": PROOF_SHA, "neutralSummary": additional(summary_path, "summary"),
        "captureDerivatives": additional(derivation_path, "derivatives"),
        "implementedDirectPairs": sorted(row["other"] for row in rows),
        "openPairs": [],
        "disclosedUnassessed": "Kanji Pedia records a separate 侵 appearance sense with a reading "
                               "outside its standard-reading mark, absent from frozen KANJIDIC2 and "
                               "the card; no current deck title presents that sense.",
        "limits": "Fifteen author direct-guard dispositions are proposals for each original family to "
                  "evaluate against the full selected evidence and the actual runtime delta. Neither "
                  "initial acceptance nor this preparation approves publication.",
    })
    prepared = []
    for family, (session, original_run, acceptance_sha) in REVIEWERS.items():
        run = f"N1-B125-{family.upper()}-CONFIRM-001"
        acceptance = REVIEW / f"{original_run}-acceptance.json"
        accepted = json.loads(frozen(acceptance, acceptance_sha))
        require(accepted["run"] == original_run and accepted["reviewAccepted"] is True,
                "Original review not accepted")
        response = blob(R2 + f"{family}-response-002.md")
        require(sha(response) == proof["responses"][family] and response_is_isolated(family, response),
                "Family response changed or not isolated")
        response_path = neutral / f"response-{family}.md"
        write_frozen(response_path, response)
        spec = {
            "batch": 125, "run": run, "family": family, "candidate": CANDIDATE, "session": session,
            "acceptance": {"path": str(acceptance), "sha256": acceptance_sha},
            "revisedSources": revised, "originalSources": originals,
            "additionalSources": [additional(response_path, "author-response/current.md"), *shared],
        }
        path = REVIEW / "confirm" / f"{run}-spec.json"
        freeze_json(path, spec)
        build(path)
        prepared.append(run)
    print(json.dumps({"runsPrepared": prepared, "reviewersLaunched": False, "candidate": CANDIDATE}))


if __name__ == "__main__":
    main()
