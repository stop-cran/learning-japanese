import copy
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from recon_common import *
from pair_records import ROWS


def compact(text):
    return re.sub(r"\s+", "", text)


guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    expected = {(target, other) for target, others in PAIRS.items() for other in others}
    assert {tuple(row["pair"]) for row in ROWS} == expected
    bindings = {tuple(b["pair"]): b for b in json.loads((PACKET / "comparison-bindings.json").read_text(encoding="utf8"))}
    for row in json.loads((PACKET / "frozen-input-bindings.json").read_text(encoding="utf8"))["inputs"]:
        assert sha(Path(row["path"]).read_bytes()) == row["sha256"]
    sources = {}
    for ch in [c for chars in PAIRS.values() for c in chars] + ["羂索"]:
        receipt = json.loads((HERE / "external-pages" / f"{ch}-receipt.json").read_text(encoding="utf8"))
        raw = Path(receipt["localRawCapture"])
        assert sha(raw.read_bytes()) == receipt["rawSha256"]
        assert sha(raw.with_suffix(".json").read_bytes()) == receipt["allArticleJsonSha256"]
        assert sha(raw.with_suffix(".txt").read_bytes()) == receipt["selectedCompleteArticleTextSha256"]
        sources[ch] = receipt
    records = {}
    for folder, filenames in [(ORIGINAL_PACKET, [
        "jmdict-complete-families.xml", "jmdict-supplemental-comparisons-002.xml",
        "jmdict-final-comparisons.xml", "jmdict-additional-families.xml"]), (PACKET, [
        "jmdict-complete-records.xml", "jmdict-supplement-complete-records.xml",
        "jmdict-noose-complete-records.xml"])]:
        for filename in filenames:
            for node in ET.parse(folder / filename).getroot():
                eid = node.findtext("ent_seq")
                digest = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())
                if eid in records:
                    assert records[eid]["canonicalSha256"] == digest
                else:
                    records[eid] = {"canonicalSha256": digest, "completeRecordFiles": []}
                records[eid]["completeRecordFiles"].append(str((folder / filename).relative_to(REPO)).replace("\\", "/"))
    kd = {}
    for node in ET.parse(PACKET / "kanjidic2-complete-records.xml").getroot():
        kd[node.findtext("literal")] = [m.text for m in node.findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
    rows = copy.deepcopy(ROWS)
    for row in rows:
        ch = row["pair"][1]
        binding = bindings[tuple(row["pair"])]
        assert sha((PACKET / "comparison-cards" / f"{ch}.md").read_bytes()) == binding["rawSha256"]
        assert (PACKET / "comparison-cards" / f"{ch}.md").read_bytes() == git("show", f"{PARENT}:kanji/{ch}.md")
        articles = json.loads((HERE / "external-pages" / f"{ch}-kotobank.json").read_text(encoding="utf8"))
        article, = [a for a in articles if row["source"] in a["class"].split()]
        text, quote = compact(article["text"]), compact(row["quote"])
        assert quote in text, (ch, row["source"], row["quote"])
        row["comparison"] = binding
        row["comparisonEnglishMeaningsCompleteKANJIDIC2"] = kd[ch]
        row["sourceEvidence"] = {
            "url": sources[ch]["url"], "articleClass": article["class"],
            "articleId": article["id"], "boundedExcerpt": row.pop("quote"),
            "whitespaceNormalizedExcerptStart": text.index(quote),
            "normalization": "Whitespace removed only for locator matching; raw capture hashes are unchanged.",
            "rawCaptureSha256": sources[ch]["rawSha256"],
            "completeSelectedTextSha256": sources[ch]["selectedCompleteArticleTextSha256"],
        }
        row["completeJmdictFamilies"] = {eid: records[eid] for eid in row.pop("jmdict")}
        row["guardDeclaration"] = ("kanji/" + row["pair"][0] + ".md:quiz_exclusions") if row["guard"] else None
        row["guardSemantics"] = "One direct pair is symmetric by the host OR rule, never transitive; old guards and all curated options retained."
        row["coverage"] = "Complete actual card and complete selected Daijisen/Nikkoku/Jitsu articles read; all English KANJIDIC2 meanings inspected. Claim families read complete with spelling/reading/sense restrictions, not a title-only scan."
    # Keep these discrepancies explicit rather than use missing bilingual evidence as disproof.
    noose = json.loads((HERE / "external-pages" / "羂索-kotobank.json").read_text(encoding="utf8"))
    assert any("わな" in a["text"] for a in noose)
    assert any("ぶらんこ" in a["text"] for a in noose)
    rows[1]["additionalExactNounEvidence"] = {
        "sourceBinding": "external-source-bindings.json:羂索",
        "Nikkoku": "Native noun sense1 is an animal/bird snare; sense2 is the Buddhist cord/noose and figurative bondage, sense3 cross-refers to search. Daijisen explicitly gives the original animal-trap sense before the ritual cord.",
        "Jitsu": "Its separate compound entry instead says ぶらんこ (swing); retained as a consequential discrepancy, not silently harmonised.",
        "bilingual": "Exact spelling 羂索 returned zero complete JMdict families. This is query-negative evidence, not proof the monolingual senses do not exist.",
        "scope": "The whole compound's senses/readings are not all transferred to 索 or 絹; the positive nominal ritual cord under standalone 索 and unresolved broad rope/noose label motivate the precaution.",
    }
    target_bindings = []
    for number, ch in [("02", "絹"), ("04", "虹")]:
        path = ROOT / "review-packets" / "batch-129-7c662b37" / "evidence" / "external-snapshots" / f"{number}-extract.txt"
        target_bindings.append({"character": ch, "path": str(path), "sha256": sha(path.read_bytes()),
                                "url": "https://kotobank.jp/word/" + ch,
                                "scope": "Frozen target extract already read; complete original external captures/source receipts remain locally bound through unchanged original packet."})
    assert "色のついた光の輪" in compact(Path(target_bindings[1]["path"]).read_text(encoding="utf8"))
    write(PACKET / "external-source-bindings.json", {
        "comparisonsAndExactFollowupNoun": sources, "targets": target_bindings,
        "originalPacketInventory": {"path": "docs/n1-sources/batch-129/evidence-inventory-003.json",
                                    "sha256": sha((ORIGINAL_PACKET / "evidence-inventory-003.json").read_bytes())},
        "attribution": "Kotobank hosts Digital Daijisen (Shogakukan), selected Nihon Kokugo Daijiten, and Fukyuban Jitsu (Heibonsha); target 虹 also uses Nipponica. Copyrighted complete captures stay local; only bindings, short attributable excerpts and authored analysis are committed.",
        "readingLimit": "All selected comparison articles were read complete, not all other Kotobank articles, linked related words, source images or rendered glyphs. Unread/missing image glyphs are not guessed.",
    })
    write(PACKET / "pair-dispositions.json", {
        "contract": ["F1", "L1-SILK", "L1-RAINBOW", "L3-ADDITIONAL"], "parent": PARENT,
        "totalPairs": 28, "newDirectGuards": sum(r["guard"] for r in rows),
        "supportedNoncollisionPairs": [r["pair"] for r in rows if not r["guard"]],
        "interpretation": "Conservative broad-label protection is not universal lexical synonymy, a demonstrated current curated collision, historical-gloss disambiguation, or confirmation/publication acceptance.",
        "rows": rows,
    })
    write(PACKET / "reviewer-response-gpt.json", {
        "originalRun": "N1-B129-GPT-001", "originalVerdictUnchanged": "NEEDS FIX",
        "originalReportAndAdjudication": "frozen-input-bindings.json",
        "F1": "Implemented the three direct guards with the coordinator's minor conservative-policy qualification. Preserved Claude's lexical/shape distinction and absence of a demonstrated current curated meaning collision.",
        "L1-SILK": "All four exact pairs read; guard 絡 for raw silk, 緒/線 for independently attested thread, 索 conservatively for its nominal ritual noose/cord and unresolved broad label. Complete exact 羂索 follow-up and zero JMdict match retained, including the Jitsu swing discrepancy.",
        "L1-RAINBOW": "All15 exact pairs read and individually justified direct guards added. The reasons use positive secondary criticism/censure, debate/mockery, attack, disorder, blame, coercion/opposition, noun curve and vessel senses; not title differences, current-option absence, age claims or transitive guards.",
        "L3-ADDITIONAL": "All six actual cards and complete applicable sources inspected. Guard 絹/括 for the independently positive くくり snare noun; guard 虹/缶 for the displayed broad container label and 虹/対,虹/抵 for explicit opposition. No guard for 絹/結 (binding does not establish trapping) or 虹/容 (containment/property is not the vessel noun).",
        "D4": "Confirmed 網 absent from parent signed tree; no fabricated read or new card.",
        "evidence": "pair-dispositions.json contains all28 complete per-pair claim, evidence, both label directions, disposition and guard entries; source query tables retain complete records and zero matches.",
        "remainingQualification": "These are author reconciliations, not a new reviewer verdict. Retain the report's unread-source/model/geometry/font/native/device/old-APK/served-ZIP/arbitrary/custom/multi-borrow limits. Confirmation/publication stay with coordinator.",
    })
    write(PACKET / "reviewer-response-claude.json", {
        "originalRun": "N1-B129-CLAUDE-001", "originalVerdictUnchanged": "qualified CLEAN",
        "originalReportAndAdjudication": "frozen-input-bindings.json",
        "D10": "The description positively says coloured ring of light. Added conservative ring/circle/light guards as coordinator policy, while retaining the narrower distinction between a phenomenon's shape and lexical rainbow meaning; no claim that both initial reviewers agreed.",
        "citationErratum": {"sha256": "cb67d51517dca32ace7a731c5f437d6fea7713fe9bf4fecd6deeccaec4df05bd",
                            "correction": "04-extract.txt:41 -> :42", "originalReportAndAdjudicationEdited": False},
        "O1": "Deferred: no cocoon/silk guard inferred from material origin, source-only readings or 繭糸.",
        "O2": "Retained selective original historical guards. Added only source-grounded exact contract pairs with individual limitations; no blanket deletion, unsupported rarity classification or transitive closure.",
        "O3": "Deferred: no optional 茉 み wording/metadata/practice change.",
        "O4": "Deferred: keep structure-unclassified and expressly invented mnemonics. Missing sound-element image does not verify exact 肙 attribution.",
        "O5": "Deferred: コウ inventory/practice unchanged; no claim it is Joyo-approved.",
        "guSupplement": "Neither initial reviewer read the separate coordinator ぐ check. Original host log omitted グ; later normalised ぐ gave zero production/target-only padded hits and the same six latent collisions, retaining 橋/攻/責 one-additional-holder risks. Revised bounded checker explicitly supplies all18 positive extra target keys, including ぐ, without retrospective reviewer/native/custom/multi-borrow acceptance.",
        "newAudit": "The finite additional comparison source work and dispositions are authored here, not attributed retrospectively to Claude.",
    })
    write(PACKET / "source-discrepancies-and-limits.json", {
        "historicalSemeru": "The target Jitsu source positively gives せめる without enough context to choose attack versus reproach/press. Keep both branches as conservative risks; do not pretend guards resolve the philology.",
        "kuKuri": "Nikkoku explicitly has a snare sense for くくり; complete JMdict2763660 has three senses but no snare. Its complete family and exact spelling/reading predicates are retained.",
        "kensaku": "Exact JMdict 羂索 spelling query is zero. Nikkoku/Daijisen preserve animal trap and Buddhist cord/noose; separate Jitsu compound entry says swing. All complete applicable local captures and the discrepancy are retained.",
        "sourceLayers": "KANJIDIC2 English meanings for 絹/虹 are silk/rainbow, not all supplemental historical character uses. Absence from that list or from priority/Joyo data is not disproof of positive sources. Complete source records preserve other languages, flags and readings without claiming all foreign-language senses translated.",
        "claimReadset": "claim-source-readset.json distinguishes82 complete claim families read from other retained homonyms/example families; supplemental2763660 was read complete separately. All34 selected KANJIDIC2 English-meaning and full-reading inventories were inspected; complete multilingual records retained.",
        "noTransitivity": "All26 new exclusions are direct declarations on the new cards; the host treats either endpoint as a symmetric pair. Neither an existing nor a newly added guard generates another pair.",
        "currentCurated": "All three curated meaning/reading option lists and selected practice readings are unchanged. No new currently curated meaning collision is claimed.",
        "readingLimits": "Bounded host N1/All/Starter target-only padded model plus separately labelled one-additional-holder probe; not arbitrary/custom pools, multiple borrowing, Kotlin/native/device, rendering, whole-set or publication acceptance. No claim that explicit extra source keys appear in card prose merely because the helper prints 'card text'.",
        "unchangedLimits": "No new font/rendering/component/native/device/served-ZIP acceptance. Original font misses, geometry/source limits and six latent reading collisions remain. Deferred 伯33 憶395 撲461 remain deferred. No new word/stroke/support or B130 work.",
        "delivery": "Still258/1228 delivered and970 pending. The three B129 local drafts remain unpublished and are not counted as delivered.",
    })
    print("Composed28 pair entries;", sum(r["guard"] for r in rows), "guards; complete canonical family union", len(records))
finally:
    write(HERE / "compose-memory-001.json", guard.finish())
