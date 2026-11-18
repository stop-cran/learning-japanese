# Independent review packet: N1 kanji batch 111, candidate 3b30803e

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

Teaching cards for JLPT N1 kanji (community list). Kanji added: 修 句 房 授 敷 旬 標 独 率 節 義 製 評 鏡 養. New word articles: none.
Modified existing files: kanji/価.md kanji/暖.md words/上旬.md words/下旬.md words/中旬.md words/主義.md words/休養.md words/作製.md words/修正.md words/修理.md words/修繕.md words/俳句.md words/冷房.md words/准教授.md words/初旬.md words/助教授.md words/句.md words/句読点.md words/女房.md words/季節.md words/座敷.md words/意義.md words/批評.md words/授業.md words/教授.md words/教養.md words/敷く.md words/敷地.md words/文句.md words/文房具.md words/暖房.md words/望遠鏡.md words/栄養.md words/標本.md words/標準.md words/標識.md words/独り言.md words/独特.md words/独立.md words/独身.md words/率.md words/率直.md words/目標.md words/眼鏡.md words/研修.md words/確率.md words/節.md words/節約.md words/義務.md words/能率.md words/製作.md words/製品.md words/製造.md words/評価.md words/評判.md words/評論.md words/調節.md words/講義.md words/鏡.md words/顕微鏡.md words/風呂敷.md words/養分.md. Audience: an English speaker at roughly JLPT N5-N4 reading on a phone. The format
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
- Verify consequential claims yourself against reputable sources (for example JMdict/Jisho, KANJIDIC2/kanjiapi.dev,
  Weblio/Kotobank dictionaries, NHK or established teaching sources). A search snippet is not verification: inspect the
  actual entry, reading, sense and register. Say what you could not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit 3b30803e; reviewer model as you identify it>
Scope: <files reviewed and the facet you examined deepest>
Verdicts: <for each facet - correctness, scoped coverage, consistency and quiz safety, comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, one line each, per file where they differ>
Findings: <numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence>
Optional: <nonblocking expansion or polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. No finding quota. Separate defects from optional polish and editorial preference.
Severity reflects demonstrated impact on learning; confidence reflects the strength of evidence.
