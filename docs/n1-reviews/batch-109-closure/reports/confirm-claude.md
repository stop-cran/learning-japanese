# Batch 109 confirmation report: reviewer of initial-claude.md

## Snapshot

- Revised snapshot: a3e0610a7566c20f2bd2ae019617623d6eab7b01. Its parent is the reviewed snapshot 0a20f4bf2415d6b4d20644f518990e8c938259b1.
- Reviewer model: Claude Opus 5.5 (model ID claude-opus-5.5). It is the same reviewer that wrote reports-109\initial-claude.md.
- Work was serial: one tool call per response, read-only, and the only write is this file.

## Scope

**Confirmation packet** (`confirm-109-a3e0610a-claude\`):
- INSTRUCTIONS.md: read in full.
- RESPONSE.md: read in full.
- CHANGES.md: read in full.
- evidence\QuizBuilder.kt: read in full.
- checks\quiz-safety.txt: read in full, covering all 15 cards and the fallback list.
- checks\link-targets.tsv: read in full (36 links).
- diffs\fix.patch: read in full, in three consecutive ranges covering all 13 card diffs.
- The 13 changed cards in snapshot\kanji\ (影 摩 攻 撃 撮 掲 擦 括 抵 弧 抗 催 促): each read in full.
- Read in part, by grep:
  - evidence\README.md
  - evidence\jmdict-cited-entries.xml: entries 1590145, 1592730, 1279170, 1253590, 1253620, 1951490 and 1383160
  - evidence\joyo\p144.txt (摩) and evidence\joyo\p62.txt (擦, 撮)
  - evidence\kanjivg\064ae.svg, 06700.svg, 063b2.svg and 066f7.svg: the element tree only
- Not opened:
  - snapshot\kanji\批.md and 択.md. Both are unchanged; I read them in round 1, and their quiz options are checked here from quiz-safety.txt.
  - diffs\changed-lines.txt, which is superseded by reading fix.patch in full.

**Original packet** (`batch-109-0a20f4bf\`, read-only), read in part by grep:
- evidence\kanjidic2-records.xml: every literal and meaning line.
- evidence\public-source\weblio-攻.txt, weblio-撮.txt, weblio-弧.txt and weblio-催.txt: the Digital Daijisen character entry line.
- mechanical-checks.md: the fallback list.

**Own initial report** (reports-109\initial-claude.md): not reopened this round. I used my recorded F1–F5 and O1–O10 findings.

**Public web:** not used this round. The pinned evidence covered every new claim. My round-1 jisho.org checks of example words still apply, because no example word changed except 抗がん剤, which is checked here against JMdict 1951490.

## Dispositions

- **F1: RESOLVED.**
  - 影.md:13 now has distractors [景, 英, 京]. The displayed options are "scenery | English; outstanding | capital". None of them is a defensible meaning of 影.
  - 英 is an エイ sound-alike with no shadow, image or light sense.
  - 影.md:14 excludes [映, 形, 像, 象, 光, 跡]. None of these overlaps a distractor.
  - Notes 影.md:45 and 48 match JMdict 1590145: sense 1 "shadow; silhouette; figure; shape", sense 2 "reflection; image", sense 4 "light (stars, moon)" and sense 5 "trace".
- **F2: RESOLVED.**
  - 括.md:14 adds 包 and 囲.
  - The bullet at 括.md:45 is accurate, and the quoted titles match (link-targets.tsv).
- **F3: RESOLVED.** The paragraph at 摩.md:36 no longer contradicts the rows.
  - Joyo p. 144 lists only マ for 摩 (摩擦, 摩天楼) and no kun reading.
  - "マ plus the verb する" matches JMdict 1982610.
  - さする is marked kana-usual and す.る is marked rarely used kanji form, consistent with rows 33–34.
  - The 研 bullet (摩.md:46) matches JMdict 1592730 (研摩 is a rarely used kanji form) and KANJIDIC2 摩 ("polish, grind").
- **F4: RESOLVED.**
  - Joyo p. 62 lists 擦 as サツ (擦過傷, 摩擦), する (擦る, 擦り傷) and すれる (擦れる, 靴擦れ), with no こする.
  - 擦.md:23, 35 and 38 now qualify こす.る as the kana-usual spoken verb and do not present it as a recommended spelling.
- **F5: RESOLVED.**
  - KanjiVG 06700 (最) and 066f7 (曷) mark the top as 日 with kvg:original="曰".
  - In 063b2, 掲's right-hand part is 曷 with kvg:variant="true", made of 日 above 匂.
  - The new wording "a wide 日-like box (曰)" (撮.md:25, 掲.md:25) is accurate and readable for a beginner, and the misleading link to 日 is gone from 掲.
- **O1: DECLINE ACCEPTED.** I had said no change was needed.
- **O2 (title): DECLINE ACCEPTED.** Daijisen 抵 sense 2 is 突き当たる (抵触), and KANJIDIC2 has "reach, touch". "collide" is defensible, if weak.
- **O2 (link): RESOLVED.** 抵.md:23 links 大抵 to words/たいてい.md, which resolves (title "usually; most").
- **O3 (older): RESOLVED.** The extract confirms the Daijisen 弧 entry order: １ ゆみ (桑弧), ２ 弓なりに湾曲した線. The new wording at 弧.md:23 is exact.
- **O3 (弱 framing): DECLINE ACCEPTED.** 弧.md:42 claims only that 弓 is at the left, which is true for 引, 弱 and 強.
- **O4: RESOLVED.** 抗.md:23 now reads 抗がん剤 (also written 抗癌剤). JMdict 1951490 lists both forms with the reading こうがんざい.
- **O5: DECLINE ACCEPTED.** 速 "fast" stays defensibly wrong for "urge; prompt", and 促.md:43 draws the contrast.
- **O6 (集): DECLINE ACCEPTED.** It is defensibly wrong, and 催.md:45 contrasts it with 催.
- **O6 (催/促): RESOLVED.**
  - 催.md:14 has quiz_exclusions [促].
  - The Daijisen extract confirms 催 sense １ うながす。せきたてる (催促), which supports the 催.md:44 note.
- **O7: RESOLVED.** 攻.md:44 and 撃.md:42 now say "Both characters concern attacking". That is true for both (KANJIDIC2 攻 "attack", 撃 "attack").
- **O8: DECLINE ACCEPTED.** 催.md:31 already labels もよう.す "Source-only here … Not selected for practice."
- **O9: DECLINE ACCEPTED.** It is pre-existing and out of the batch's scope.
- **O10: RESOLVED.** 抵.md:14 has quiz_exclusions [抗, 反, 対], with no overlap with distractors [低, 底, 抱]. The bullet at 抵.md:42 is accurate.
- **L1: RESOLVED.**
  - In QuizBuilder.kt, options come from the curated distractors in order. A candidate is skipped if either card excludes the target or an already chosen option. Tag-similar or random cards are added only when fewer than three curated distractors survive.
  - quiz-safety.txt shows every batch card filling 3/3 from its curated list. My F2 impact, and likewise O6 and O10, was therefore a latent fallback-path risk, not a live risk in the default options. Fallback happens if a curated card is excluded or missing from the card list passed to the builder.
  - The added exclusions remain correct as direct-title-overlap protection and have no visible cost. Nothing remains open; see Limits for one assumption.

## Verdicts

The four facet verdicts are the same for all 15 cards; no card differs.

- **Correctness:** CLEAN. Every new or changed claim checks against the pinned JMdict entries, the Joyo pages, the KanjiVG records, KANJIDIC2 and the Daijisen extracts:
  - KANJIDIC2 meanings cited by the new exclusion notes: 摩 polish/grind, 攻 criticize/polish, 撃 defeat.
  - JMdict senses: 攻撃 sense 2 "criticism; censure"; 責める sense 2 "to urge; to press; to pester"; 撃退 "repelling; driving back"; 撃破 "defeating; crushing".
  - Daijisen 撮 sense １ つまんで取る.
- **Scoped coverage:** CLEAN. The 摩 and 擦 readings are now qualified against the Joyo table, and no coverage was lost.
- **Consistency and quiz safety:** CLEAN for all 15 cards, including the unchanged 批 and 択.
  - The default options shown have no defensible correct alternative.
  - No exclusion overlaps a distractor.
  - The validator reports 0 errors.
  - The 11-card fallback list is identical to the original packet, so the new exclusions cause no regression.
  - All 36 links on changed lines resolve, and the quoted titles match.
- **Comprehensibility:** CLEAN. The new wording uses plain English: "doubled consonant sound", "older Chinese-derived (Go-on) reading", and the Joyo table explained as "the official list of standard-use readings".

## Confirmation

CONFIRMED.

## Findings

None.

## Optional

1. **掲.md:25:** the mnemonic still says "holding a sign up toward the sun". It is harmless because the text now calls the shape "日-like", but "holding a sign up high" would avoid reintroducing 日.
2. **摩.md:45–46:** the 研磨/研摩 spelling fact appears in both the 磨 bullet and the new 研 bullet. One mention would be enough.
3. **促.md:42:** the 催 bullet does not mention that 催 and 促 are now kept apart in quiz options (the exclusion is declared on 催.md:14 and is symmetric). Parity only; 催 is not in 促's curated list, so there is no visible effect.
4. **擦.md:43:** the Common words line for 擦る こする lacks the "usually written in kana" note that the table row and paragraph now carry.

## Limits

- **QuizBuilder input:** I assumed the `all` list passed to QuizBuilder.options is the full card corpus. If the app passes a filtered deck, for example one JLPT level, curated distractors outside it would trigger fallback more often. The added exclusions would then matter more; they are correct either way.
- **No live web check:** I did no live web lookup this round. JMdict, Joyo and KanjiVG claims were checked against the pinned extracts in the packet, and Daijisen claims against the weblio extracts from the original packet. The README notes that online JMdict may differ slightly.
- **Joyo extracts:** the Joyo text extracts come from pdfplumber. I did not open the PDF itself; the extract layout (kanji, then reading, then examples) was unambiguous for 摩, 擦 and 撮.
- **Unchanged cards:** I did not reopen 批.md, 択.md or my initial report. Only quiz options and cross-card consistency were rechecked for 批 and 択.
