"""Prepare context-bounded confirmations without changing the signed evidence."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from b129_confirmation_presentation import (
    compact_xml, kd_projection, lexical_articles, named_section, pair_projection,
)
from b129_revision_pairs import EXTERNAL_SHA, NOOSE_EXTERNAL_SHA, ORIGINAL
from common import freeze_json, frozen, json_bytes, load_batch, require, sha, start_guard, write_frozen
from confirm_b127 import build, clean
from prepare_b129_confirmations import neutral
from verify_b129_revision_runtime import PREFIX, REPO, REVIEW, RUNNER
from verify_b129_sources import Git

OUTPUT = REVIEW / "confirmation-002-neutral"
PREPARATION_SHA = "582d7eb5d828ea59cac3ab52d7fc526840ff903c3b57185d63ef3d2a0f65ac86"
PROOF_SHA = "3378793385dbd2a8d895f60aab5d01d7d9b5e33dbb50e2d4e4484b7a7b9d3029"


def main():
    require(not OUTPUT.exists(), "Preserve previous preparation")
    prepared = json.loads(frozen(REVIEW / "confirmation-001-preparation.json", PREPARATION_SHA))
    proof = json.loads(frozen(REVIEW / "revision-evidence-proof-001" / "verification.json", PROOF_SHA))
    candidate = prepared["candidate"]
    require(candidate == proof["candidate"] and proof["status"] == "PASS_MECHANICAL_ONLY",
            "Signed source admission differs")
    config = load_batch(129)
    guard, _ = start_guard("B129 bounded complete-entry confirmation preparation")
    git = Git(REPO, RUNNER, guard)
    shared, derivations = [], []

    def save(name, raw, source, derivation=None):
        require(neutral(raw) and all(len(line) <= 13000 for line in raw.splitlines(keepends=True)),
                f"Non-neutral or oversized presentation line: {name}")
        binding = write_frozen(OUTPUT / name, raw)
        shared.append({**binding, "source": source})
        if derivation:
            derivations.append({"output": binding, **derivation})

    def blob(path):
        return git("show", f"{candidate}:{path}")

    try:
        clean(config, candidate)
        spec_path = REVIEW / "confirm" / "N1-B129-CLAUDE-CONFIRM-001-spec.json"
        initial = json.loads(frozen(spec_path))
        pair_source = next(item for item in initial["additionalSources"]
                           if item["source"] == "evidence/reconciliation/pair-dispositions.json")
        pair_raw = frozen(pair_source["path"], pair_source["sha256"])
        table = pair_projection(pair_raw)
        rows = table.pop("rows")
        pair_lines = [json.dumps(table, ensure_ascii=False, separators=(",", ":"))]
        pair_lines.extend(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows)
        save("pair-dispositions.jsonl", ("\n".join(pair_lines) + "\n").encode(),
             "evidence/reconciliation/pair-dispositions.jsonl",
             {"input": pair_source, "method": "Complete semantic projection; only repeated hashes and "
              "complete-record file lists replaced by family IDs. Header followed by one full pair per line."})
        families = set()
        for name in ("jmdict-complete-records.xml", "jmdict-supplement-complete-records.xml",
                     "jmdict-noose-complete-records.xml"):
            raw = blob(PREFIX + name)
            families.update(node.findtext("ent_seq") for node in ET.fromstring(raw).findall("entry"))
            save(name, compact_xml(raw), "evidence/reconciliation/" + name,
                 {"signedPath": PREFIX + name, "signedSha256": sha(raw),
                  "method": "Every complete record, restriction and sense retained; "
                  "canonical XML equality checked, insignificant indentation removed."})
        require(len(families) == 303 and all(set(row["completeJmdictFamilyIds"]) <= families for row in rows),
                "A claimed family is missing from complete current selections")
        for prefix, name in ((ORIGINAL, "kanjidic2-target-records.xml"),
                             (PREFIX, "kanjidic2-complete-records.xml")):
            raw = blob(prefix + name)
            projection, omitted = kd_projection(raw)
            save(name, projection, "evidence/english-readings/" + name,
                 {"signedPath": prefix + name, "signedSha256": sha(raw), "omittedFields": omitted,
                  "method": "Explicit presentation of literal, complete misc metadata, every reading "
                  "with attributes, all nanori and every English meaning in every reading group. "
                  "Non-English meanings and non-reading administrative fields are not presented. "
                  "Full unmodified multilingual records remain in the signed verified packet."})
        captures = json.loads(frozen(REVIEW / "reconciliation-external-001" / "manifest.json",
                                     EXTERNAL_SHA))["captures"]
        captures.append(json.loads(frozen(REVIEW / "reconciliation-noose-external-001" / "manifest.json",
                                         NOOSE_EXTERNAL_SHA)))
        for index, capture in enumerate(captures, 1):
            raw_binding = capture["outputs"]["raw.html"]
            raw = frozen(raw_binding["path"], raw_binding["sha256"])
            receipt_binding = capture["outputs"]["receipt.json"]
            receipt = json.loads(frozen(receipt_binding["path"], receipt_binding["sha256"]))
            character = capture["character"]
            articles, omitted = lexical_articles(raw, receipt["finalUrl"], character)
            require([item["class"] for item in articles] == receipt["selectedArticleClasses"],
                    f"Lexical source coverage differs: {character}")
            author_binding = capture["outputs"]["articles.json"]
            author = json.loads(frozen(author_binding["path"], author_binding["sha256"]))
            text = [f"Complete lexical dictionary entries for {character}\n"
                    "All Daijisen, Nikkoku and Jitsu article elements retained, including all "
                    "senses/examples and image placeholders. Other encyclopedia/topic articles and "
                    "navigation are omitted, not semantically rejected. Images are not inspected.\n"]
            article_bindings = []
            for article in articles:
                matching = [a for a in author if a["id"] == article["id"]
                            and a["class"] == article["class"]]
                require(len(matching) == 1, "Article locator changed")
                body = article["text"].split("\n", 2)[2]
                require(re.sub(r"\s+", "", body) == re.sub(r"\s+", "", matching[0]["text"]),
                        f"Independent full-article extraction disagrees: {character}")
                text.append(f"\nARTICLE ID: {article['id']}\nARTICLE CLASS: {article['class']}\n"
                            + article["text"])
                article_bindings.append({key: value for key, value in article.items() if key != "text"})
            save(f"external-{index:02d}.txt", "".join(text).encode(),
                 f"external-reconciliation/{index:02d}-complete-lexical.txt",
                 {"input": raw_binding, "articles": article_bindings, "omittedArticles": omitted,
                  "method": "Independent raw HTML article-boundary selection and HTMLParser visible-text "
                  "extraction on each complete article; full normalized text independently "
                  "matched author article JSON. No bounded quotation substituted for an entry."})
            guard.check()
        source = REPO.parent / "review-packets" / "batch-129-7c662b37" / "evidence" / "external-snapshots" / "07-extract.txt"
        raw = frozen(source)
        section, bounds = named_section(raw, "Wiktionary\u65e5\u672c\u8a9e\u7248\uff08\u65e5\u672c\u8a9e\u30ab\u30c6\u30b4\u30ea\uff09")
        save("rainbow-wiktionary-japanese.txt", section, "original-source-sections/rainbow-wiktionary-japanese.txt",
             {"input": {"path": str(source), "sha256": sha(raw)}, "sourceLines": bounds,
              "method": "Whole named Japanese Wiktionary section, through the next named-section boundary; "
              "other Weblio dictionaries/encyclopedia sections are retained in the original packet, not repeated."})
        summary_item = next(item for item in initial["additionalSources"]
                            if item["source"] == "verification/signed-correction-summary.json")
        shared.append(summary_item)
        for item in initial["additionalSources"]:
            if item["source"].startswith("committed-checks/"):
                shared.append(item)
        source_notes = {
            "candidate": candidate, "proofSha256": PROOF_SHA,
            "completeCurrentJmdictFamilies": 303,
            "completeFamilyPolicy": "All 302 primary families plus the full one-family supplement "
                "and exact zero-match selection are presented, without gloss filtering. All 80 "
                "families cited by the finite pair table are present. The original, unchanged "
                "selections remain verified within the 539-family union; unrelated old families "
                "are not repeated. The complete original reports remain unchanged.",
            "currentCards": "All three targets, all 28 actual finite counterparts, current curated "
                "options, three separately disclosed borrowed-reading holders and three support "
                "words. Old unchanged guard counterparts are not re-reviewed here.",
            "kanjidicPresentation": "English meaning/all-reading projection, not full multilingual "
                "records. All full records remain verified and unchanged; no translation or "
                "absence-based negative claim about unpresented language fields.",
            "sourceDisagreement": "All three complete primary dictionary works are shown wherever "
                "available for all 29 captures, including the noose-versus-swing disagreement. "
                "Other encyclopedia/topic works remain retained but are not part of this bounded confirmation.",
            "supersededPreparation": "Confirmation 001 was prepared but never admitted or delivered; "
                "its repeated original sources and unrelated encyclopedia text exceeded estimated "
                "remaining context. This is the first confirmation delivery, not a reviewer retry.",
        }
        save("presentation-scope.json", json_bytes(source_notes), "verification/presentation-scope.json")
        sys.path.insert(0, str(REPO.parent / "lean"))
        from n1lib import parse
        cards = set(config["members"]) | {row["pair"][1] for row in rows} | set("\u6a4b\u653b\u8cac")
        for character in config["members"]:
            metadata, _ = parse(blob(f"kanji/{character}.md").decode().replace("\r\n", "\n"))
            cards.update(metadata["distractors"])
        revised = [f"kanji/{character}.md" for character in sorted(cards)]
        revised += ["words/\u8309\u8389\u82b1.md", "words/\u7d79.md", "words/\u8679.md"]
        revised += [PREFIX + name for name in (
            "jmdict-query-membership.json", "supplement-query-membership.json", "noose-source-receipt.json",
            "source-discrepancies-and-limits.json",
        )]
        for path in revised:
            require(neutral(blob(path)), "Revised source leaks other-family provenance")
        originals = [f"evidence/external-snapshots/{index:02d}-extract.txt" for index in (2, 3, 4)]
        originals.append("evidence/external-snapshots/manifest.json")
        runs = []
        for family in ("CLAUDE", "GPT"):
            old_run = f"N1-B129-{family}-CONFIRM-001"
            require(not (REVIEW / "confirm" / f"{old_run}-admission.json").exists()
                    and not (REPO.parent / "reports-129" / f"{old_run}.md").exists(),
                    "Cannot supersede an admitted confirmation")
            spec = json.loads(frozen(REVIEW / "confirm" / f"{old_run}-spec.json"))
            own_response = next(item for item in spec["additionalSources"]
                                if item["source"] == "author-response/current.json")
            spec.update(run=f"N1-B129-{family}-CONFIRM-002", revisedSources=revised,
                        originalSources=originals, additionalSources=[own_response, *shared])
            spec_path = REVIEW / "confirm" / f"{spec['run']}-spec.json"
            freeze_json(spec_path, spec)
            build(spec_path)
            chain = json.loads(frozen(REVIEW / "confirm" / f"{spec['run']}-chain.json"))
            runs.append({"run": spec["run"], "session": spec["session"],
                         "segments": len(chain["segments"]),
                         "chainBytes": sum(row["bytes"] for row in chain["segments"])})
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Presentation preparation RAM guard breached")
    print(json.dumps(freeze_json(REVIEW / "confirmation-002-preparation.json", {
        "candidate": candidate, "status": "PREPARED_NOT_ADMITTED",
        "priorPreparationSha256": PREPARATION_SHA, "proofSha256": PROOF_SHA,
        "runs": runs, "derivations": derivations, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "presentationHelperSha256": sha(frozen(Path(__file__).with_name("b129_confirmation_presentation.py"))),
        "limits": "Bounded complete lexical entries and full current bilingual families. "
                  "Actual context and serial admission remain required; no semantic acceptance.",
    })))


if __name__ == "__main__":
    main()
