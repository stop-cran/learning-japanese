# Independent review packet: N1 kanji batch 135, candidate 163b384e

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

Teaching cards for JLPT N1 kanji (community list). Kanji added: 博 厳 及 姿 履 巡 弾 彫 恵 憶 我 揚 救 暇 模. New word articles: none.
Modified existing files: words/休暇.md words/博士.md words/博物館.md words/厳しい.md words/厳重.md words/及ぼす.md words/姿.md words/姿勢.md words/履く.md words/巡る.md words/巡査.md words/弾.md words/弾く.md words/弾劾.md words/彫る.md words/彫刻.md words/怪我.md words/恩恵.md words/恵まれる.md words/我々.md words/我慢.md words/揚げる.md words/救う.md words/救助.md words/普及.md words/暇.md words/模倣.md words/模様.md words/知恵.md words/草履.md words/記憶.md words/鷹揚.md. Audience: an English speaker at roughly JLPT N5-N4 reading on a phone. The format
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
- `evidence\joyo-pages.md`: text extracts of the official Joyo kanji table PDF pages the cards cite, plus front matter pp. 2-3 and appendix pp. 162-163
- `evidence\audits\quiz-safety.txt`: full meaning-quiz option simulation for the 15 cards
- `evidence\audits\reading-exposure.txt`: full reading-quiz reachability audit (Python port of the app's reading quiz); its last line counts production hits, padded-session hits and latent collisions
- `evidence\audits\reading-options.txt`: full reading-quiz option tiers and seeded simulation per prompt
- `evidence\app-code\QuizBuilder.kt`: meaning-quiz option builder (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- `evidence\app-code\KanjiReadings.kt`: reading-quiz builder (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- `evidence\app-code\KanjiMeaningMetadata.kt`: meaning metadata used by the quiz (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- `evidence\app-code\Words.kt`: word-article model and kanji-word links (app code at kanji-cards-android commit 4db1297c50984dff29499768b2da7cc30e18d850)
- Verify consequential claims yourself against reputable sources (for example JMdict/Jisho, KANJIDIC2/kanjiapi.dev,
  Weblio/Kotobank dictionaries, NHK or established teaching sources). A search snippet is not verification: inspect the
  actual entry, reading, sense and register. Say what you could not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit 163b384e; reviewer model as you identify it>
Scope: <files reviewed and the facet you examined deepest>
Verdicts: <for each facet - correctness, scoped coverage, consistency and quiz safety, comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, one line each, per file where they differ>
Findings: <numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence>
Optional: <nonblocking expansion or polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. No finding quota. Separate defects from optional polish and editorial preference.
Severity reflects demonstrated impact on learning; confidence reflects the strength of evidence.
