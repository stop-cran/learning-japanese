**Snapshot:** `ad2a00e2028444fc42e599a538d6e5eddd629fea`, as identified by the task; no uncommitted teaching included. Read-only review; no changes made.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), independently reviewing correctness, scoped coverage and textual phone comprehensibility of complete `kanji\虎.md` and `words\虎.md`.

Completed all prescribed instruction/format/level ranges, complete input metadata—including raw KANJIDIC2 elements for 虎・劇・酔—and both complete frozen dictionary packets: **115 + 21 = 136 families**, inspecting spellings, readings, restrictions, senses and flags. XML reads covered lines 1–2306 and 1–731 serially, in explicit ranges of at most 200 lines, without returned truncation. Completed all nine comparison cards: kanji 劇・鳥・風; words 動物・猫・酔っ払い・酔う・動物園・見る. Consulted `docs\confusable-words.md` by scoped search and confirmed 虎’s membership in the frozen community list.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\虎.md` | CLEAN | CLEAN | CLEAN |
| `words\虎.md` | NEEDS FIX | CLEAN | CLEAN |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification.

The kanji preserves the complete source readings コ／とら and their order. Selected とら has a defensible whole-word allocation and useful reciprocal word link; unselected コ is supported by divided こ‐けつ dictionary headings. 虎猫／とらねこ respects JMdict’s reading restrictions. Radical 141, stroke count, grade and explicitly labelled modern-shape mnemonic agree with the inspected evidence without asserting an unverified origin.

Both animal sentences, their readings and translations are natural and correct. N3 vocabulary placement remains independent of N1 kanji placement. The three curated kanji labels—“drama; play,” “bird,” and “wind; style”—are not defensible meanings of 虎, including its colloquial drunk-person sense.

**Findings:**

**Minor; correctness—quiz ambiguity; `words\虎.md:1–9`, `words\酔っ払い.md:4,9`.** Neither header excludes the direct 虎／酔っ払い pair. For an uncontextualized Japanese-to-English question showing 虎, both its intended “tiger” label and the competing “a drunk; drunkenness” label offer a defensible interpretation: 虎 also means a drunk person. The article’s animal-only scope does not supply context to the quiz.

**Remedy:** Add a direct `quiz_exclusions` declaration for this pair on either card, preserving the existing 酔っ払い／酔う exclusion. Do not infer protection through 酔う or extend exclusions indiscriminately to animal-category comparisons.

**Evidence:** `batch-030-jmdict.xml:26–31`, entry 1267610 sense 2, marks the drunk-person meaning colloquial; `batch-030-comparisons-jmdict.xml:292–315`, entry 1372660 sense 1, supplies “drunk person” and “(a) drunk.” Independently retrieved [Nikkoku’s とら【虎】 entry](https://kotobank.jp/word/%E8%99%8E-493416), noun [1]④, explicitly defines it as 酔っぱらい／泥酔者. The exclusion contract is `docs\content-format.md:133–148`. **Confidence: high.** This is an inherited header omission exposed by the requested comparison audit, not a defect caused by the component-link edit.

**Optional:** None.

**Limits:** Snapshot identity and the link-only baseline diff are task-supplied, not independently Git-verified. Required file/range reads matched the stated lengths; none remained incomplete or truncated. Confusable-word inventory inspection was partial, by scoped search.

The XML and KANJIDIC2 records are supplied frozen evidence, not fresh upstream downloads. I independently fetched and inspected the relevant Kotobank bodies for 虎 and 虎穴, corroborating the coordinator-supplied facts; I did not inspect the preserved raw HTML or verify its hashes. Empty 虎 Digital Daijisen/Jitsu headings were not treated as evidence.

Comprehensibility assessment is textual only. Supplied font coverage and inherited native evidence were not independently reproduced; fresh batch-030 Android, physical-phone, combined-main, CI and public-ZIP acceptance remain outstanding. Larger quizzes and fallback algorithms are not certified. All tool calls were issued individually and awaited; no internal tool overlap was observed, and unavailable process evidence is not claimed.
