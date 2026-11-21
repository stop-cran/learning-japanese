# Independent review packet: N1 kanji batch 153, candidate cdab83b3

You are one of several independent reviewers from different model families. You will not see the other reviewers'
reports or the author's rationale, and you must not look for them. Work alone, serially and read-only.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your own
  report to the one path you are given in your assignment. Do not start other agents, sessions or background jobs.
  Make one tool call at a time; read large files in ranges rather than all at once.
- **Blind.** This packet is your complete local evidence set. Do not open any other path on this machine (in particular
  no repository checkouts, no `docs\n1-reviews`, no `docs\n1-sources\batch-*`, no `docs\n1-authoring-notes.md`, no other
  packets or reports). Public web sources are allowed and encouraged for verification.
- **Scope.** The files in `snapshot\` are the unit under review. `repo\` is a read-only export of the rest of the
  content at the same commit, for checking links, titles, readings, exclusions and consistency; it is context, not
  further scope. `diffs\` shows how modified existing files changed.

## What the batch is

Teaching cards for JLPT N1 kanji (community list). Kanji added: 酌 酔 酢 醜 釈 釣 鈴 銃 銭 鎖 鐘 鑑 附 陥 陰. New word articles: none.
Modified existing files: kanji/属.md words/図鑑.md words/日陰.md words/欠陥.md words/解釈.md words/酌む.md words/酔う.md words/酔っ払い.md words/酢.md words/醜い.md words/金銭.md words/釣り.md words/釣り合う.md words/釣る.md words/鈴.md words/銃.md words/鎖.md words/鐘.md words/鑑賞.md words/附属.md words/陰.md. Audience: an English speaker at roughly JLPT N5-N4 reading on a phone. The format
contract is `repo\docs\content-format.md`; the review contract is `rubric\copilot-instructions.md`.

## Facets (cover all four; your assignment names the one to examine deepest)

1. **Correctness.** Front matter against the pinned metadata (`evidence\source-metadata.json`, `evidence\kanjidic2-records.xml`);
   every reading claim; word readings, types, senses, register and restrictions against complete JMdict families
   (`evidence\jmdict-families.xml`, `evidence\jmdict-digest.tsv`) and independent public sources; example sentences
   (grammar, naturalness, translation, kana); mnemonics labelled as mnemonics; no unsupported etymology; every
   comparison claim in Notes and Synonyms is true.
2. **Scoped coverage.** For each kanji, are the readings and the common usage it needs for N1 study present or explicitly
   qualified (every metadata reading has a row; source-only or rare readings are marked as such; important words from the
   dictionary families are not wrongly omitted or misdescribed)? Do not demand every related word.
3. **Consistency and quiz safety.** Links resolve to the intended cards; each declared kanji of each word has a card link where
   a card exists; titles are unique and unambiguous as quiz answers; `distractors` are plausible wrong answers that cannot also
   be correct; `quiz_exclusions` cover real synonym or confusable pairs (see `repo\docs\confusable-words.md`); `quizOnyomi`
   and `quizKunyomi` are selected from the metadata and each has a linked word example; tags, levels, section order, headings.
4. **Comprehensibility.** Clear to a beginner on a phone: central idea first, jargon explained, kana where needed,
   contrastive natural examples, mnemonic concrete and honest, no wall of text, no padding.

Treat `mechanical-checks.md` as the output of automatic checks, not as a verdict on any facet.

## Evidence

- `evidence\provenance.json`: pinned dictionary inputs and hashes. Pinned data may differ from today's online dictionaries;
  say so when it matters.
- `evidence\public-source\`: retrieved public dictionary text (coordinator retrieval, not your independent lookup).
- `evidence\joyo-pages.md`: text extracts of the official Joyo kanji table PDF pages the cards cite, plus front matter pp. 2-3
- `evidence\audits\quiz-safety.txt`: full meaning-quiz option simulation for the 15 cards
- `evidence\audits\reading-exposure.txt`: full reading-quiz reachability audit (Python port of the app's reading quiz); its first lines give the command, the --extra readings and their provenance, and its last line counts production hits, padded-session hits and latent collisions
- `evidence\audits\reading-options.txt`: full reading-quiz option tiers and seeded simulation per prompt; its first lines give the command and the --extra readings. Its HIT label ignores slots already filled by curated distractors
- `evidence\audits\kanji_remarks.py`: the script behind the kanji card edits mechanical check: it compares kanji\ at the candidate with the base commit and allows only the 15 new cards plus declared remark-only edits to existing cards (1 card in this batch, with 1 remark edit: 属; see kanji-remarks.json)
- `evidence\audits\kanji-remarks.json`: the declared old-to-new remark edits to existing kanji cards that the kanji card edits check allows (1 remark edit in this batch, on 属, rewriting the clause that said 附 in 附属 had no card yet into a link to the new 附 card)
- `evidence\audits\word-remarks.json`: the declared old-to-new remark edits to existing word articles that the link plan verify check allows (2 remark edits in this batch: 附属 drops the sentence that 附 has no card yet, and 酌む drops the sentence that there is no 酌 kanji card, now that this batch adds both)
- `evidence\app-code\QuizBuilder.kt`: meaning-quiz option builder (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- `evidence\app-code\KanjiReadings.kt`: reading-quiz builder (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- `evidence\app-code\KanjiMeaningMetadata.kt`: meaning metadata used by the quiz (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- `evidence\app-code\Words.kt`: word-article model and kanji-word links (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- `evidence\kanjipedia-outside-readings.json`: Kanjipedia (kanjipedia.jp) on and kun readings for the 15 kanji (JSON generated from the coordinator text retrieval), with the readings Kanjipedia marks as outside the official table and each page URL (coordinator retrieval)
- `evidence\daijisen-heads.txt`: Digital Daijisen headwords on Weblio for the cards' kanji-plus-okurigana forms and for each kanji alone, with marks for readings outside the official table (coordinator retrieval; each line gives the page URL and the raw-HTML sha256 prefix)
- `evidence\okurigana-scan.txt`: JMdict kanji-plus-okurigana headwords whose reading stem is not among the card's kun readings, used to find extra readings for the exposure audit
- `evidence\audits\extra-readings.json`: the per-kanji extra readings from Kanjipedia and Digital Daijisen (character on/kun lists and headwords) that the gate runner passes to the two reading audits, together with the okurigana-scan readings; the first lines of each audit file list the full --extra set actually passed
- `evidence\audits\make_extras.py`: the script that builds extra-readings.json and kanjipedia-outside-readings.json from the coordinator retrievals
- `evidence\kanjivg-components.txt`: KanjiVG component groups (element, position, stroke range) and stroke types for the 15 kanji at the pinned KanjiVG revision 70a0b7ae that the stroke files use; each entry gives the raw-file URL and sha256. Use it to check the mnemonics' component statements
- `evidence\kanjivg-svgs.txt`: the 15 raw KanjiVG SVG files behind kanjivg-components.txt, concatenated, each with its URL and sha256
- `evidence\audits\kanjivg_report.py`: the script that generates kanjivg-components.txt and kanjivg-svgs.txt from the pinned SVG files
- Verify consequential claims yourself against reputable sources (for example JMdict/Jisho, KANJIDIC2/kanjiapi.dev,
  Weblio/Kotobank dictionaries, NHK or established teaching sources). A search snippet is not verification: inspect the
  actual entry, reading, sense and register. Say what you could not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit cdab83b3; reviewer model as you identify it>
Scope: <files reviewed and the facet you examined deepest>
Verdicts: <for each facet - correctness, scoped coverage, consistency and quiz safety, comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, one line each, per file where they differ>
Findings: <numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence>
Optional: <nonblocking expansion or polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. No finding quota. Separate defects from optional polish and editorial preference.
Severity reflects demonstrated impact on learning; confidence reflects the strength of evidence.
