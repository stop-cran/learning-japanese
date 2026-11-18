"""Prepare a fresh, blind, complete-source B134 review within the unchanged budget."""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from run_b134_closure_checks import CANDIDATE, HERE, REPO
from verify_b134_payload import RUNNER
from verify_b134_sources import Git

ROOT = HERE / "review"
DOSSIER = ROOT / "confirmation-dossier-002"
PROOF = ROOT / "reconciliation-verification-001" / "verification.json"
PROOF_SHA = "7ea9e7dde1989b5d1eb71bed3b5789ab77f4e3713277591b4841eeb2b0295da1"
OUT_BASE = ROOT / "fresh-independent-001"

PROMPT_TEMPLATE = """Perform one fresh, independent content review of signed N1 B134 candidate {candidate}.

The user asks: "Please find and inspect work items at stop-cran/learning-japanese related to creating N1 kanji cards. The work is ~30% complete. Fetch latest changes, find and read related repo work items, gather the context, plan the outstanding work and do it." The user later directed: "Please resolve this issue by yourself and continue with the task." This is a read-only review of the revised 紫 card, not implementation, confirmation of a prior report, publication, or approval of the full deck.

Review only what you can establish from the supplied sources in this pass. The snapshot is owner-signed and its exact lineage, byte inventory, complete dictionary-source membership and host checks were mechanically verified. Those facts establish provenance, not semantic correctness. The supplied author-written explanations are not included; derive your own conclusions. No initial reviewer reports or verdicts are supplied. Do not infer consensus.

## Input protocol
1. First call: view this exact prompt at {prompt_path}, one full read with forceReadLargeFiles true and no range. No tool may precede it.
2. Then read all {segment_count} segments of the one chain, in order, beginning at {first_segment}, exactly one view tool call per response. No parallel calls, searches, shell, scripts, external fetches, agents, other files or session/history access. Chain parts give source path, SHA-256 and source-line mapping. The final segment states END OF CHAIN. You may re-view a reached segment.
3. Use only these chain segments as evidence. Cite exact source paths and original source line numbers, never segment numbers. Note the canonical XML presentation and other disclosed transformations. Missing source, omitted image or bounded selector is a limitation, not evidence of absence.
4. After the whole chain, create exactly one report with one Add File operation at {report_path}; then read that file back exactly once. Do not edit it again. Report claims must match evidence read.
5. After readback send one message to coordinator {coordinator_id} containing exactly CLEAN, NEEDS FIX, or UNVERIFIED, optionally one final newline. No report path or other message. Then stop.

## Review scope
- Evaluate the actual revised card, support word, unchanged stroke geometry, exact initial-to-revision card diff, and every direct `quiz_exclusions` counterpart article supplied.
- Assess correctness, N1-level scope, teaching coverage, comprehensibility, ordinary and qualified secondary meanings, quiz safety and reading exposure. Direct guards are symmetric but not transitive. Distinguish shared meaning from related subject, whole-word compound, named work/place/person, historical/register-limited sense, spelling restriction, counter, and homophone. Do not equate precautionary guards with unrestricted synonymy.
- Verify each of the 56 direct excluded pairs from both displayed titles, counterpart card's ordinary secondary senses, candidate's supplied source-positive meanings, and quiz/runtime evidence. State the basis for every row, and be explicit when source evidence is insufficient. Verify curated 古/右/川 independently.
- Check all card metadata and readings, source identity, named readings, whole-word readings, 12-stroke evidence, mnemonic qualification, reciprocal support link and support-word level; distinguish repository checks from native/rendered behavior.
- The supplied source receipt lists complete JMdict families selected by declared exact selectors and complete KANJIDIC2 records for the bounded source set. Record any material evidence gap: do not infer exhaustive historical negatives or complete corpus absence. No source was independently retrieved from the network.
- The contributor comparison records and checker logs are evidence, not verdicts. The 51 Notes-coverage warnings are disclosed; decide whether this is a teaching defect or a mechanical convention limitation based on the actual wording and project rubric. The single latent hypothetical 紫/包 reading collision is not a production-pool hit; preserve that distinction.
- Do not require unrelated edits, expand to other batches, or claim whole-set, Kotlin/native/device, font-rendering, arbitrary/custom/multiple-borrow, publication or linguistic consensus acceptance.

## Report format
Write one Markdown report with exactly these headings, in order:

# Fresh B134 independent review — {run}
## Snapshot
## Scope and evidence
## Overall verdict
## Facet verdicts
## Direct-pair assessment
## Findings
## Optional points
## Limits

Snapshot: full candidate ID and confirmed scope. Scope and evidence: enumerate the chain segments read and disclose source representation and evidence limits. Overall verdict is exactly CLEAN, NEEDS FIX or UNVERIFIED with concise basis. Facet verdicts cover Correctness, Scoped coverage, Consistency and quiz safety, and Comprehensibility, each exactly CLEAN/NEEDS FIX/UNVERIFIED with evidence.

Direct-pair assessment must contain one table row for each of the 56 exclusions, in candidate-card order, with columns `Character | Displayed title | Assessment | Evidence and rationale`. Assessment is SUPPORTED PRECAUTION, DISTINCT WITH BASIS, or UNVERIFIED. Cite sources using `path:line`; every nontrivial row needs evidence opened in this pass. Also report curated options and reading-exposure scope.

Findings and Optional points use consecutive numbered level-3 headings (`F1: ...`, `O1: ...`) and fields: Facet, Severity, Confidence, Citations, Evidence, Required change (findings) / Suggestion (optional). Severity is high, medium or low for findings; optional for optional points. Cite full source paths and line/range. Use the single line `None.` when empty.

An established blocking defect requires NEEDS FIX; do not report an established defect as UNVERIFIED. CLEAN means no material defect established within this bounded review, not exhaustive historical or whole-set approval. Preserve consequential uncertainty as UNVERIFIED. Do not create a finding solely to demand stylistic preference.

Do not communicate any verdict or findings before your sole report and final one-word coordinator message.
"""


def main(revision):
    require(re.fullmatch(r"[0-9]{3}", revision), "Use a three-digit review revision")
    root = ROOT / ("fresh-independent-" + revision)
    require(not root.exists(), "Preserve existing fresh-review preparation")
    dossier = json.loads(frozen(DOSSIER / "dossier.json",
        "ef4e5a31469233ef10db7a86a555f8ae65e428d32e1b87991c0672d1d09013a9"))
    proof = json.loads(frozen(PROOF, PROOF_SHA))
    require(proof["candidate"] != CANDIDATE and proof["status"] == "PASS"
            and dossier["candidate"] == proof["candidate"], "Verified candidate differs")
    source_rows = dossier["sources"]
    evidence = {}
    for row in source_rows:
        raw = frozen(row["path"], row["sha256"])
        evidence[row["source"]] = raw
    require("repo/kanji/紫.md" not in evidence, "Duplicate target")
    guard, _ = start_guard("B134 fresh independent review preparation")
    try:
        git = Git(REPO, RUNNER, guard)
        candidate = proof["candidate"]
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout changed")

        def blob(name, commit=candidate):
            return git("show", f"{commit}:{name}")

        sources = []

        def add(name, raw):
            require(name not in {row["source"] for row in sources}, "Duplicate source: " + name)
            if not raw.endswith(b"\n"):
                raw += b"\n"
            ref = write_frozen(root / "sources" / name, raw)
            sources.append({"source": name, "path": ref["path"], "sha256": ref["sha256"],
                            "bytes": ref["bytes"], "lines": len(raw.splitlines())})

        # Preserve the verified complete source and review packet bytes exactly.
        for name, raw in evidence.items():
            add(name, raw)
        for name, commit in (("snapshot/kanji/紫.md", candidate),
                             ("baseline/kanji/紫.md", CANDIDATE),
                             ("snapshot/words/紫.md", candidate),
                             ("baseline/words/紫.md", candidate),
                             ("snapshot/strokes/紫.json", candidate)):
            path = name.split("/", 1)[1]
            add(name, blob(path, commit))
        add("diffs/紫-reconciliation.diff",
            git("diff", "--no-color", CANDIDATE, candidate, "--", "kanji/紫.md"))
        raw_card = blob("kanji/紫.md")
        match = re.search(rb"^quiz_exclusions:\s*\[([^\]]*)\]\s*$",
                          raw_card.split(b"---", 2)[1], re.M)
        require(match is not None, "Revised direct exclusions are unavailable")
        exclusions = [item.decode("utf-8").strip() for item in match.group(1).split(b",")]
        require(len(exclusions) == len(set(exclusions)) == 56, "Unexpected direct guard count")
        for char in exclusions:
            name = f"repo/kanji/{char}.md"
            if name not in {row["source"] for row in sources}:
                add(name, blob(f"kanji/{char}.md"))
        require(all(f"repo/kanji/{char}.md" in {r["source"] for r in sources}
                    for char in exclusions), "A direct exclusion article is missing")

        rubric = (ROOT / "neutral-preparation-001" / "projected-successor-001" /
                  "packet" / "rubric" / "copilot-instructions.md").read_bytes()
        add("rubric/copilot-instructions.md", rubric)
        formatting = (ROOT / "neutral-preparation-001" / "projected-successor-001" /
                      "packet" / "repo" / "docs" / "content-format.md").read_bytes()
        # The complete content-format guide is already in the original packet; retain it whole.
        add("rubric/content-format.md", formatting)
        jlpt = (ROOT / "neutral-preparation-001" / "projected-successor-001" /
                "packet" / "repo" / "docs" / "jlpt-levels.md").read_bytes()
        add("rubric/jlpt-levels.md", jlpt)

        sys.path.insert(0, str(ROOT / "neutral-preparation-001" / "projected-successor-001" /
                              "protocol-001"))
        from review_chain_with_optional import build_chain
        from b134_runtime import verify_chain

        chain_sources = [(row["source"], frozen(row["path"], row["sha256"]), None)
                         for row in sources]
        chain_path = root / "chain.json"
        chain = build_chain(chain_sources, root / "segments", chain_path, guard,
                            "B134 fresh independent review " + revision)
        verify_chain(chain, chain_sources)
        for family in ("claude", "gpt"):
            run = "N1-B134-FRESH-" + family.upper() + "-" + revision
            report = WS / "reports-134" / ("fresh-" + family + "-" + revision + ".md")
            prompt = root / (family + "-prompt.txt")
            text = PROMPT_TEMPLATE.format(candidate=candidate, run=run, prompt_path=prompt,
                                          report_path=report,
                                          coordinator_id="2451b10d-02a9-46ab-82d5-d90993f0cb8b",
                                          first_segment=chain["segments"][0]["path"],
                                          segment_count=len(chain["segments"]))
            write_frozen(prompt, text.encode("utf-8"))
            kickoff = ("First read the complete prompt at " + str(prompt) +
                       " using one full view call with forceReadLargeFiles true and no range. "
                       "No other tool call may precede that read.").encode("ascii")
            write_frozen(root / (family + "-kickoff.txt"), kickoff)
        max_prompt = max(len((root / (f + "-prompt.txt")).read_bytes()) for f in ("claude", "gpt"))
        from b134_confirmation_capacity import confirmation_cost
        cost = confirmation_cost(chain)
        estimated = 80000 + cost["tokens"] + max_prompt + 12000 + 30000
        require(estimated < 700000, f"Fresh review forecast exceeds fixed gate: {estimated}")
        result = {
            "status": "PREPARED_NOT_LAUNCHED", "candidate": candidate,
            "chain": {"path": str(chain_path), "sha256": sha(frozen(chain_path)),
                      "segments": len(chain["segments"]), "sources": len(sources),
                      "payloadBytes": cost["payloadBytes"], "chainBytes": cost["chainBytes"],
                      "forecastTokens": cost["tokens"]},
            "exclusions": exclusions, "completeCounterpartCards": len(exclusions),
            "models": {"claude": "claude-opus-5.5", "gpt": "gpt-6.1-sol"},
            "promptBytes": max_prompt, "bootstrapTokens": 80000, "driftTokens": 12000,
            "reportReserveTokens": 30000, "startupGate": 700000,
            "conservativeStartupForecast": estimated,
            "reviewOrder": ["claude", "gpt"], "gptRequiresAcceptedClaudeEvidence": True,
            "independence": "Fresh separate reviewer sessions; no original reports, verdicts or author response in evidence chain.",
            "scope": "All 56 direct guard articles, complete verified source records, revised/baseline card and support, "
                     "stroke geometry, exact teaching diff, source receipts and committed gates.",
            "limits": [proof["limits"], "Forecast is conservative, not actual token telemetry.",
                       "Fresh reviewers are new session identities in the same model families, not the original session IDs.",
                       "No reviewer has been admitted or delivered a report."],
            "producerSha256": sha(Path(__file__).read_bytes()),
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Fresh review preparation RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(root / "preparation.json", result)))


if __name__ == "__main__":
    main(sys.argv[1])
