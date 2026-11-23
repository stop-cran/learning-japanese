# Independent review packet: N1 kanji batch 159, candidate 1a9bb910

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

Teaching cards for JLPT N1 kanji (community list). Kanji added: 厘 又 叔 叙 吉 后 吏 吟 呈 呉. New word articles: 不吉 伯叔 厘 又聞き 叙情 吟味 呉服 太后 官吏 贈呈.
Modified existing files: kanji/不.md kanji/伯.md kanji/味.md kanji/太.md kanji/官.md kanji/情.md kanji/服.md kanji/聞.md kanji/贈.md. Audience: an English speaker at roughly JLPT N5-N4 reading on a phone. The format
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
- `evidence\audits\reading-exposure.txt`: full output of the reading quiz exposure check
- `evidence\audits\reading-options.txt`: full output of the reading quiz options check
- `evidence\audits\meta-scan.txt`: JMdict-spelled words mentioned in the new cards whose entry id is not cited on the card
- `evidence\audits\corpus-attested.txt`: corpus-wide reachable attested options in the word reading quiz
- `evidence\audits\word-quiz.txt`: word reading quiz audit for the 10 new words (where each new word is shown as an option and which options each gets)
- `evidence\audits\distractor-use.tsv`: curated meaning distractors of the batch cards, with every card that uses them
- `evidence\audits\distractor-senses.txt`: JMdict single-character senses of every curated distractor
- `evidence\audits\okurigana-scan.txt`: JMdict scan of okurigana and kana spellings that write each new kanji, grouped by reading
- `evidence\public-source\kanjipedia.json`: Kanjipedia (Kanken) readings, including readings outside the joyo table, for the new kanji
- `evidence\selection\support-selection.json`: the batch selection policy statement and each kanji's support word with its JMdict entry ids, priority tags and, for the four untagged-route rows, the recorded exception reason (excerpt of the batch ledger)
- `evidence\selection\batch-159-jmdict-selection.json`: the JMdict entry ids recorded for the batch
- `evidence\selection\selection-order.tsv`: frozen source rows 1-153 with grade, Joyo or name-use class and whether a card existed at the batch base, showing that the batch is the first ten Joyo rows without a card
- `evidence\selection\rule-7058679348.md`: the issue #60 comment that sets the support-word selection rule (qualifying tags, the untagged route and its conditions)
- Verify consequential claims yourself against reputable sources (for example JMdict/Jisho, KANJIDIC2/kanjiapi.dev,
  Weblio/Kotobank dictionaries, NHK or established teaching sources). A search snippet is not verification: inspect the
  actual entry, reading, sense and register. Say what you could not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit 1a9bb910; reviewer model as you identify it>
Scope: <files reviewed and the facet you examined deepest>
Verdicts: <for each facet - correctness, scoped coverage, consistency and quiz safety, comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, one line each, per file where they differ>
Findings: <numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence>
Optional: <nonblocking expansion or polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. No finding quota. Separate defects from optional polish and editorial preference.
Severity reflects demonstrated impact on learning; confidence reflects the strength of evidence.
