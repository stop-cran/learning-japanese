# B116 confirmation — N1-B116-CONSTITUTION-CONFIRM-003

## Snapshot
Commit: 2b81b65b52ef8daa2c8690bd240371656545d1ef
Model: runtime-reported Claude Opus 5.5; execution-model identity is not independently verifiable within this pass

## Scope
Chain: segments 1-45 of n1-b116-constitution-confirm-003, each read once in order with no re-views; the kickoff instruction file was viewed once at the start as authorized. Scoped card: 憲 (revised snapshot read in full, with the be498245 original, fix.patch, changed-lines, link-targets, all ten checks, QuizBuilder.kt, 51 Daijisen character-entry excerpts, comparison-english-meanings.json, JMdict cited entries and 42 counterpart cards). 監 and 督 were read as context only.
Fetches: none

## Dispositions
- O1 - RESOLVED - Daijisen 令 sense 2 records おきて/のり ("rule; law") with 条令・法令, and KANJIDIC2 lists "laws" for 令 (confirm-packet/evidence/character-definition-令.txt:13; confirm-packet/evidence/comparison-english-meanings.json). The revised 憲 now declares 令 in quiz_exclusions (confirm-packet/snapshot/kanji/憲.md:14) and explains the rule/decree comparison (confirm-packet/snapshot/kanji/憲.md:78-82). This settles the previously UNVERIFIED direct 憲/令 pair.
- O2 - RESOLVED - Daijisen 管 sense 5 is 担当の範囲を取り締まる, the same 取り締まる wording as 憲 sense 3 (confirm-packet/evidence/character-definition-管.txt:16; original-packet/evidence/external-snapshots/01-extract.txt:9). 管 is now a declared direct exclusion (confirm-packet/snapshot/kanji/憲.md:14), and the Notes qualify the regulating comparison without equating pipes, supervision and a constitution (confirm-packet/snapshot/kanji/憲.md:91-97).
- O3 - RESOLVED - The card now states that KANJIDIC2 records のり as a name reading, not in its on/kun list, while Daijisen lists it as kun (confirm-packet/snapshot/kanji/憲.md:49-52). This matches KANJIDIC2's nanori のり (original-packet/evidence/kanjidic2-records.xml:73-75) and Daijisen ［訓］のり (original-packet/evidence/external-snapshots/01-extract.txt:5). No practice reading was added.
- O4 - DECLINE ACCEPTED - The mnemonic is explicitly labeled as a selective modern-shape aid naming landmarks (宀, a 罒-shaped block, 心), not a stroke decomposition or historical claim (confirm-packet/snapshot/kanji/憲.md:32-36). The stroke JSON is unchanged and supplies the full 16-stroke animation (original-packet/snapshot/strokes/憲.json:1). The omitted middle bars are an optional polish, not a defect.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: All four points are RESOLVED or DECLINE ACCEPTED. Every new 憲 claim is supported by the supplied entries. The rule/legal-text uses of 例 式 格 度 程 定 章 match those Daijisen entries: 例 2, 式 1/4, 格 3 and キャク, 度 2 and ト, 程 1, 定 3, 章 4. Agreements, precepts and directives (約 2, 訓 2/4), order senses (令 1-2, 勅 1, 命 2), regulating and governing uses (管 5, 治, 御 2-3, 統 2, 理 4, 政 1), police (警 3) and the historical-official use (守 2) also check out. The English-makeup guards for 体 質 性 構 are honestly qualified. All 24 new exclusions resolve to existing cards (link-targets 0 unresolved), none overlaps distractors 寄 害 寒, and lint, validate and quiz-safety pass with unchanged curated options and an unchanged reading quiz. Rechecking my prior D/E dispositions against the new full entries, the remaining unguarded candidates (基 権 兵 刑 党 数 府 庁 署 局 省 系 義 正 標 案 議 罪 犯 判 軍 民) carry foundation, power/rights, military, punishment, party, number, institution, lineage/system, righteousness, correctness, mark, proposal, deliberation, offense, judgment or populace senses, not a law, constitution or regulating-official meaning that would make either displayed title defensible for the other. No consequential claim remains unresolved within this text and host-model scope.

## Findings
None.

## Optional
None.

## Limits
- L1: No network fetch was made. All Daijisen character entries are coordinator-retrieved bounded excerpts with response hashes; I relied on them as quoted text but did not independently re-fetch them.
- L2: Raw KanjiVG SVGs, the binary Joyo PDF and full Weblio HTML responses were not read. Stroke and Joyo claims rest on the unchanged stroke JSON, the shape-evidence tree and the cached Joyo text rows.
- L3: The reading-exposure and quiz-safety outputs are host-side Python models of the N1, All and Starter pools. They do not establish caller-built or multi-borrow pools, Kotlin execution, native/device acceptance or compatibility with the older installed APK 5c000bd, which predates quiz_exclusions. QuizBuilder.kt was read as code, not executed.
- L4: The 監 and 督 revisions were read only as context and are not adjudicated here. Whether other existing cards outside those read declare reciprocal exclusions with 憲 was not exhaustively checked; the declared 憲-side list suffices for every pair assessed.
- L5: The unguarded-candidate dispositions rely on the supplied Daijisen excerpts, KANJIDIC2 English meanings and counterpart cards. Other dictionaries or rare historical senses were not consulted.
- L6: The original external-snapshot manifest still records its earlier-candidate card locator (line 84, card SHA 98c4f800...). It is provenance for the fetched URL, not a line reference into the revised card.
