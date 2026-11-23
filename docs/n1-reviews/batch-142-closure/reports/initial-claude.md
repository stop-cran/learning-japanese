# Batch 142 independent review: initial-claude

## Snapshot

- Reviewer: Claude, an Anthropic model. This is the first blind reviewer, from a different model family. The review was read-only.
- Commit: `9d393a8f7bbf04114668b40f84b67a9a4b2ef7e3`. Packet: `review-packets\batch-142-9d393a8f`.
- New cards (15): 挙 振 挿 掌 推 描 提 揮 揺 操 故 敵 斉 斎 斜.
- Also in scope: 15 stroke files, 24 word link-wrap diffs and the remark edit to `kanji/仮.md`.

## Scope

**Opened in full**
- INSTRUCTIONS.md and mechanical-checks.md
- all 15 `snapshot\kanji\*.md` cards
- source-metadata.json and joyo-pages.md
- all 15 `public-source\weblio-*.txt` extracts
- daijisen-heads.txt and kanjipedia-outside-readings.json
- all 25 diffs (changed lines of the 24 word diffs; the 仮 diff in full)
- audits\quiz-safety.txt, reading-options.txt, kanji-remarks.json and word-remarks.json
- all 15 `snapshot\strokes\*.json`, parsed

**Opened in part or queried**
- jmdict-families.xml: I parsed every entry cited for the 15 kanji, about 220 headwords.
- jmdict-digest.tsv: targeted reading filters.
- reading-exposure.txt: the tail and the 斎 section.
- app-code QuizBuilder.kt, KanjiReadings.kt, Words.kt and KanjiMeaningMetadata.kt: exclusion lines only.
- titles\kanji-titles.tsv: all titles, checked for duplicates and shared segments.
- content-format.md and copilot-instructions.md: grepped for `distractors`/`quizOptions` only.
- Cards 揺, 斎, 操, 斉, 掌, 敵, 斜, 推, 揮, 故 and 描: targeted greps after the full read.

**Not opened**
- the snapshot\words files (I relied on the diffs)
- kanjidic2-records.xml, okurigana-scan.txt and provenance.json
- confusable-words.md
- kanji_remarks.py
- snapshot\kanji\仮.md beyond its diff

**Public-dictionary check**
- I checked every reading and example word against the packet's public-source extracts: Weblio/Digital Daijisen, the Daijisen headword list, Kanjipedia, the Joyo table and JMdict.
- One live jisho.org fetch returned only page chrome and was not used as evidence.

## Verdicts

The facet names are as I recorded them: F1 correctness, F2 scoped coverage, F3 clarity/pedagogy, F4 quiz and format safety.

| File(s) | F1 | F2 | F3 | F4 |
|---|---|---|---|---|
| 挙 振 挿 掌 推 描 提 揮 操 故 敵 斉 斜 | CLEAN | CLEAN | CLEAN | CLEAN |
| 揺 | CLEAN | CLEAN | CLEAN | NEEDS FIX (C1, minor) |
| 斎 | CLEAN | NEEDS FIX (C2, minor) | CLEAN | NEEDS FIX (C1, minor) |
| 15 stroke files | CLEAN | CLEAN | CLEAN | CLEAN |
| 24 word diffs | CLEAN | CLEAN | CLEAN | CLEAN |
| 仮 remark edit | CLEAN | CLEAN | CLEAN | CLEAN |

### What I verified as correct

**Front matter and Joyo data (all 15 cards)**
- Front matter matches source-metadata.json: grade, strokes, radical, on/kun and quiz selections.
- Every Joyo-table row, example, ⇔ contrast and old form (擧 插 搖 齊 齋) matches.
- Every row the table lacks is correctly reported as missing (e.g. no はさむ for 挿, no kun for 掌/斉/斎, no ふるう for 揮).

**Daijisen**
- Character-entry sense counts and examples match for all 15.
- The ▽ headwords on the cards are present in daijisen-heads: 揺 ゆ, よる, あゆく, あよく; 故 え, から, かれ, け; 斎 い, ゆ; 斜め なのめ.

**JMdict: spot-checked claims, all exact**
- 挙げる: 11 senses, sense 8 a dated term.
- 挙る: search-only under あがる; also a separate こぞる entry.
- 挙って: uk.
- 振る: 12 senses.
- 振り仮名: forms as stated.
- ぶる 振る: uk.
- 振れる: sense 1 restricted to 振れる and 震れる.
- 揮う: untagged; 振う: io.
- 挿す: 5 senses.
- 挿む: untagged in 挟む; 挾む: oK.
- 手のひら: たなごころ and しょう restricted to 掌.
- 掌る: rK under 司る; 仙人掌: rK.
- 推す sense 4: slang.
- 推し進める: a spelling of 押し進める.
- 描く: sense 2 restricted to えがく.
- 絵かき: listed first, [fam].
- 描寫: oK.
- 提灯: forms as stated; ていとう: a rare term.
- 堤出 and 手堤: search-only.
- 揺る: 淘る and 汰る oK.
- 揺さ振る: rK.
- 揺籃: search-only under ゆりかご.
- 揺り動かす: 揺 writes ゆ, so the "source-only" うご.く row is correct.
- 故い: rK.
- 元/旧/故: もと.
- 故障: 4 senses.
- 殊更/故: 故 marked oK.
- 敵 あだ: correctly "source-only". The あだ entry is spelled 仇 寇 讐 賊, and あだをうつ is restricted to 仇を討つ.
- かたき sense 3: "spouse", archaic.
- 斉しい, 斉える and 斉う: rK.
- 等しく/斉しく/均しく: as stated.
- 均整/均斉, 整斉/斉整 and 斎行/斉行: as stated.
- 書斉: search-only.
- 斎 forms:
  - 忌み/斎み/忌/斎 いみ
  - 斎 とき
  - 祝い/祝/斎
  - 忌む/斎む/諱む, with sense 2 restricted
  - 斎く and 斎う
  - 物忌み has no 斎 spelling, so the ものいみ row is correctly source-only.
  - 斎王 さいおう and 斎宮 さいぐう: historical terms.
- 斜め: 斜 marked io, 傾 oK, なのめ ok.
- 斜交 しゃこう versus 斜交い はすかい: as stated.
- 斜 はす/しゃ, entry 2085880.

**Kanjipedia**
- The 外 readings cited (こぞる, すげる, ものいみ for 斉, かなう, はす and others) match the extract.

**Exclusions**
- The claims that pairs are "kept out of each other's quiz options" hold even where only one card declares the pair. `QuizBuilder.kt:26` checks both directions: `excluded(a,b) = b.kanji in a.quizExclusions || a.kanji in b.quizExclusions`, and `Words.kt:177` does the same.

**Titles**
- No duplicate titles.
- Each shared title segment is addressed in that card's Notes: raise (育 養), wave (波), infer and recommend (察 勧), draw (引), submit (屈), command and display (令 命 掲), reason and former (由 旧).

**Strokes**
- All 15 stroke files are KanjiVG revision 70a0b7ae with viewBox 0 0 109 109.
- `kanji` matches the filename, and `strokeCount` equals the number of strokes and the card's stroke count.
- First-stroke types are plausible: 挙 ㇔, 扌 cards ㇐, 掌/敵/斉/斎 ㇑a, 斜 ㇒.

**Diffs**
- Each of the 24 word diffs changes exactly one line. The only change is wrapping the new kanji in `[X](../kanji/X.md)`; the text is unchanged.
- Kanji without cards are correctly left unlinked: 薦 in 推薦 and 郷 in 故郷.
- The 仮 edit matches kanji-remarks.json. The 振 title quoted, "wave; swing; allocate", matches the titles file, and 遣 still has no card.

**Mechanical checks and quiz audits**
- Lint reports 0 errors and validate reports 0 errors; there are 439 unit tests.
- quiz-safety: 3/3 curated wrong options for every prompt.
- reading-exposure: 0 production hits, 0 padded hits.
- The single "HIT" in reading-options (斎, unlisted い offered by 以/位/...) is not drawable in practice. reading-exposure shows the curated 海 毎 買 fill all three slots in every pool, so the fallback is never used. It is latent only.

## Findings

### C1: meaning-quiz distractors for 揺 and 斎 are unrelated starter kanji

- **Severity:** minor
- **Facet:** F4 quiz and format safety
- **Where:**
  - `snapshot\kanji\揺.md` front-matter distractors 入 見 休, and Notes line 56
  - `snapshot\kanji\斎.md` front-matter distractors 海 毎 買, and Notes line 61
- **Claim and impact:** The authors chose these distractors for their reading shape:
  - 揺: いれる / みる / やすめる rhyme with ゆれる.
  - 斎: カイ / マイ / バイ rhyme with サイ.

  But quiz-safety.txt shows the same three cards also supply the meaning question's wrong answers:
  - 揺 "shake; sway; waver" is offered against "enter, put in", "see, look" and "rest".
  - 斎 "purification; abstinence; study room" is offered against "sea, ocean", "every, each" and "buy".

  These are N5/N4 starter titles that an N1 learner knows on sight, so the meaning question can be solved by elimination without knowing 揺 or 斎. content-format.md:106 requires distractors to be "plausible wrong options". These are not unsafe: the audits show no collisions. They are weak.

  The Notes describe the choice accurately ("not similar in shape ... These three cards supply this card's wrong answers"), so this is not a correctness error.
- **Remedy:** Prefer distractors that are plausible for both question types, or at least not trivially eliminable for meaning.
  - 揺: shape neighbours the card already names, such as 採 and 稲, or a kun-verb ending in -る from N1/N2 cards.
  - 斎: neighbours the card already names, such as 対, 票 or 示, or an N1/N2 カイ/マイ/バイ/サイ-type card instead of 海 毎 買.
  - Rerun quiz-safety and the reading-exposure audits after the change.

  If the batch convention deliberately allows rhyme-based starter distractors, record that and downgrade this to optional.
- **Evidence:** quiz-safety.txt (the 揺 and 斎 lines); reading-options.txt (curated 入 見 休 / 海 毎 買); content-format.md:106.
- **Confidence:** medium. This is a judgement on plausibility; the facts are certain.

### C2: 斎 summary of Daijisen さい【斎】 omits pen names

- **Severity:** minor
- **Facet:** F2 scoped coverage (with F1 precision)
- **Where:** `snapshot\kanji\斎.md:32`
- **Claim and impact:** The card says the Daijisen さい【斎】 entry "also follows names of studios and rooms". The Daijisen extract says the suffix follows 居室の名や文人などの雅号, that is, room names and the pen names of literati and artists.

  Pen-name use (e.g. 北斎) is the use an N1 learner most often meets, and the card drops it. The summary is incomplete rather than wrong.
- **Remedy:** Change the sentence to read "... a Buddhist noun that also follows the names of studies and rooms and the pen names of writers and artists". Optionally add 北斎 ほくさい as an illustration if a source in the packet supports it.
- **Evidence:** evidence\public-source\weblio-斎.txt / daijisen-heads.txt (さい【斎】 entry: 居室の名や文人などの雅号に添えて用いる).
- **Confidence:** high.

## Optional

- **O1 (斉:36):** The サイ row's headword is 斎行, followed by "also spelled 斉行". This is accurate: JMdict 2798990 lists 斎行 first. On 斉's own table, though, leading with a 斎 spelling could reinforce the 斉/斎 mix-up the card warns about at line 27. Consider "斉行 さいこう (JMdict heads it 斎行)".
- **O2 (掌):** Daijisen also has たなそこ (▽手底/▽掌), which the card does not mention. The card says it does not list every reading, so this is fine. A one-clause mention would complete the Daijisen kun set alongside たなうら.
- **O3 (操):** The distractors 品 and 木 are the card's own components ("goods, refinement", "tree, wood"). This is defensible as a visual lure, but it is weak for meaning, the same pattern as C1. No action is needed unless C1 is acted on.
- **O4 (斎, reading-options.txt):** The coarse reading-options audit reports "1 problem(s)" for 斎 い. The pool-aware reading-exposure audit shows it cannot be drawn. Consider teaching reading_options.py to honour curated-slot fill, so this false HIT stops appearing in future batches.

## Limits

- I followed the one-tool-call-per-response rule throughout. No sub-agents were used.
- **Rule breach:** one PowerShell call mistakenly ran a recursive listing (`Get-ChildItem -Recurse -Depth 2` on `repo` and `rubric`). Its output overflowed to a Temp file. I did not open that file and did not use its contents beyond the visible directory-name preview.
- Android JVM tests were not run. This is a known packet limit; the unit-test result is taken from mechanical-checks.md.
- The word snapshots (`snapshot\words\*.md`) were judged from their diffs only, kanjidic2-records.xml was not opened directly, and KANJIDIC2 claims were checked through source-metadata.json and the audit files.
- I did not reread the prompt file after the initial read, and the facet labels above come from my notes.
- The live web check (jisho.org) returned no usable content. Public-dictionary verification relies on the packet's public-source extracts plus JMdict.
