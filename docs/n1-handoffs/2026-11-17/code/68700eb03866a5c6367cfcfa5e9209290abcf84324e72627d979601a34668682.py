"""Prepare complete, bounded source rereads without cross-reviewer observations."""
import json
import re
from pathlib import Path

from common import WS, freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from confirm_b132 import INITIALS, OUT, ROOT, REPO, build, clean
from verify_b132_packet import RUNNER
from verify_b132_sources import Git
from verify_b132_teaching_revision import REVISION, PREFIX

OUTPUT = ROOT / "confirmation-sources-001"
SOURCE = WS / "scratch-132" / "source-reconciliation-001"
PROOF = ROOT / "teaching-revision-verification-001" / "verification.json"
PROOF_SHA = "899c61fff8616c48a3de52d15ca9b44cb0646b3c02c2935768b37b2a766d02e5"
ATTRIBUTION = re.compile(r"\b(?:claude|anthropic|opus|sonnet|haiku|gpt|openai|codex)\b", re.I)


def main():
    require(not OUTPUT.exists(), "Preserve previous source preparation")
    proof = json.loads(frozen(PROOF, PROOF_SHA))
    require(proof["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY"
            and proof["candidate"] == REVISION and not proof["reviewAccepted"], "Unverified revision")
    guard, _ = start_guard("B132 confirmation source preparation")
    shared, capture_bindings = [], []

    def supply(name, display, raw):
        require(not ATTRIBUTION.search(raw.decode("utf-8")), "Shared material contains reviewer attribution")
        saved = write_frozen(OUTPUT / name, raw)
        shared.append({"path": saved["path"], "sha256": saved["sha256"], "source": display})
        return saved

    try:
        git = Git(REPO, RUNNER, guard)
        clean(git, REVISION)
        signed = lambda name: git("show", REVISION + ":" + PREFIX + name)
        for name in ("jmdict-exact-families.xml", "jmdict-referenced-families.xml",
                     "kanjidic2-exact-characters.xml", "dictionary-receipt.json", "referenced-receipt.json",
                     "membership.json", "referenced-membership.json"):
            raw = frozen(SOURCE / name)
            require(raw == signed("source/" + name), "Source differs from signed record")
            supply(name, "source-reconciliation-001/" + name, raw)
        captures = []
        for name in ("external-captures.json", "referenced-external-captures.json"):
            captures.extend(json.loads(frozen(SOURCE / name))["captures"])
        selected, omitted = [], []
        for row in captures:
            use = row.get("status") == 200 and (
                row["provider"] == "kotobank" or row["term"] in ("標", "塔"))
            if not use:
                omitted.append({key: row[key] for key in ("term", "provider", "url", "status", "error")
                                if key in row})
                continue
            name = Path(row["extraction"]).name
            raw = frozen(row["extraction"], row["extractionSha256"])
            saved = supply("external/" + name, "source-reconciliation-001/external/" + name, raw)
            selected.append(name)
            capture_bindings.append({
                key: row[key] for key in ("term", "provider", "url", "finalUrl", "capturedAt",
                                         "rawSha256", "extractionSha256", "extractionMethod")
            } | {"supplied": saved, "completeExtract": True})
        original_target = WS / "scratch-132" / "survey-001" / "external" / "墓-kotobank.txt"
        target_raw = frozen(original_target, "0483a4eb6b3ead1f68dbf4084f0d78b8fc7db7e0942f4fcee9dc239f4170332d")
        saved = supply("external/墓-kotobank.txt", "survey-001/external/墓-kotobank.txt", target_raw)
        capture_bindings.append({
            "term": "墓", "provider": "kotobank", "url": "https://kotobank.jp/word/墓",
            "finalUrl": "https://kotobank.jp/word/墓-599723",
            "capturedAt": "2026-11-16T21:55:34.337380+00:00",
            "rawSha256": "d29d7f0854fe9165b8618038b5c2373b21c32729f61cab5f3ff693425eb2a3c5",
            "extractionSha256": sha(target_raw), "supplied": saved, "completeExtract": True,
        })
        pair_raw = signed("pair-dispositions.json")
        pairs = json.loads(pair_raw)
        require(set(pairs) == {"parent", "claimIds", "status", "pairs", "directExclusionsBefore",
                              "directExclusionsAfter", "mechanism", "reviewStatus"}, "Unknown pair schema")
        del pairs["reviewStatus"]
        pairs["representation"] = (
            "Exact signed pair hypotheses except the mixed-reviewer status field is omitted. "
            "The original record remains preserved; these rationales require independent source assessment.")
        pairs["originalSha256"] = sha(pair_raw)
        supply("pair-hypotheses.json", "author-response/pair-hypotheses.json", json_bytes(pairs))
        verification = {key: proof[key] for key in (
            "status", "candidate", "parent", "base", "runtimeEntries", "runtimeChanged",
            "unchangedRuntimeEntries", "sourceFilesRechecked", "manifestSha256", "contentVersion",
            "committedGates", "supplementalReadingKeys", "latentCollisions", "scope", "limits")}
        verification["originalProofSha256"] = PROOF_SHA
        verification["independentSourceVerificationSha256"] = (
            "4f64783f8810d41b778a7ccb2048ca1fc54bcff7c3ed009b20541ddd23b9bc77")
        supply("verification.json", "verification/verification.json", json_bytes(verification))
        for gate in proof["committedGates"]:
            ref = proof["capturedExecutionFiles"]["committed-gates/" + gate + ".log"]
            supply("checks/" + gate + ".log", "committed-checks/" + gate + ".log",
                   frozen(ref["path"], ref["sha256"]))
        presentation = {
            "candidate": REVISION, "scope": "Changed meaning safeguards only; not a new initial review.",
            "dictionaryScope": "All23 exact and5 referenced complete JMdict families, one unchanged overlap "
                               "(27 distinct); all3 complete KANJIDIC2 records. No sense/language/restriction pruning.",
            "externalScope": "Every successful Kotobank reconciliation capture, the whole 標 and 塔 Weblio "
                             "extracts, and the complete original 墓 Kotobank extract. Each supplied extract "
                             "is byte-identical to its frozen full-page extraction, not selected passages.",
            "captures": capture_bindings, "notRereadCaptures": omitted,
            "unchangedOriginalSources": "Other original initial-packet sources, including 墓 Weblio, "
                                        "are not reread in this delta confirmation. Readings are unchanged. "
                                        "Their prior review and explicit limits remain in the own original report.",
            "limits": "Raw HTML, source images/layout and other source captures are not authorized inputs. "
                      "Kotobank 墓塔 returned404; Weblio's machine-generated page is not independent lexical "
                      "evidence. Source gaps must remain explicit. No network refetch occurred.",
            "immutability": "Original64 source files were writable when first handed off. Their unchanged "
                            "bytes were independently verified and subsequently frozen, not retroactively immutable. "
                            "This preparation copies only those now-frozen bytes.",
            "isolation": "No other reviewer's report, findings, selection, audit or model identity is included.",
        }
        supply("presentation.json", "verification/presentation.json", json_bytes(presentation))
        revised = ["kanji/" + char + ".md" for char in "墓標塔埋石暮募川"] + ["words/墓.md"]
        for family, item in INITIALS.items():
            run = "N1-B132-" + family.upper() + "-CONFIRM-001"
            response = {
                "candidate": REVISION,
                "change": "Only two direct precautions, qualified Notes and related citations; generated "
                          "manifest and additive contributor evidence changed. No other teaching or source field changed.",
                "ownPriorItems": ({"O1": "No change; optional structural analysis remains optional.",
                                   "O2": "No change; optional additional common words remain optional."}
                                  if family == "claude" else
                                  {"Q1": "Source gap addressed with independent complete 標/marker records; "
                                          "direct precaution implemented. Verify the pair hypotheses.",
                                   "Q2": "Source gap addressed with independent complete 塔/stone-tower records; "
                                          "direct precaution implemented. Verify restrictions and pair hypotheses."}),
                "acceptance": "Implementation claims only; no presumption of confirmation.",
            }
            response_ref = write_frozen(OUTPUT / (family + "-response.json"), json_bytes(response))
            spec = {
                "run": run, "family": family, "candidate": REVISION, "session": item["session"],
                "revisedSources": revised,
                "additionalSources": [*shared, {"path": response_ref["path"], "sha256": response_ref["sha256"],
                                               "source": "author-response/own-response.json"}],
            }
            if family == "gpt":
                spec.update(basis="adjudicated-initial", priorVerdict="UNVERIFIED")
            path = OUT / (run + "-spec.json")
            freeze_json(path, spec)
            build(path)
        clean(git, REVISION)
        record = {
            "status": "PREPARED_NOT_ADMITTED", "candidate": REVISION, "sharedSources": shared,
            "selectedExternalExtracts": [*selected, "墓-kotobank.txt"],
            "runs": [json.loads(frozen(OUT / ("N1-B132-" + family.upper() + "-CONFIRM-001-preflight.json")))
                     for family in INITIALS],
            "producerSha256": sha(frozen(Path(__file__))), "reviewersLaunched": False,
        }
        print(json.dumps(freeze_json(OUTPUT / "preparation.json", record)))
    finally:
        require(not guard.finish()["breach"], "Dossier preparation RAM breach")


if __name__ == "__main__":
    main()
