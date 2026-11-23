# Batch 148 — initial blind review (reviewer 1)

## Snapshot

- Commit under review: `8408b3a5a52cccea74fe2eaf65601568968b6b26` (batch 148: 絞 継 綱 緊 締 緩 緯 縁 縄 縛 縦 織 繕 繰 罰).
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-148-8408b3a5` (manifest sha256 205a8761…c322ea, as stated in the assignment; not recomputed).
- Reviewer model: Claude (Anthropic), running as a read-only sub-agent. This is a blind review: I did not see the other reviewer's report or the author's rationale.

## Scope

The unit reviewed is the 15 new kanji cards, the 15 stroke files, the 17 word-article link-wrap diffs and the three declared remark edits (修, 張, 慢). Leads (a) to (n) were each judged; see Verdicts and Findings.

Packet files I opened:

| File | Extent |
| --- | --- |
| INSTRUCTIONS.md | full |
| mechanical-checks.md | full |
| evidence\source-metadata.json | full |
| evidence\joyo-pages.md | full |
| evidence\public-source\weblio-{絞,継,綱,緊,締,緩,緯,縁,縄,縛,縦,織,繕,繰,罰}.txt (15 files) | full; later re-grepped for 綱, 縄, 縁, 織, 縦, 締, 罰 |
| evidence\daijisen-heads.txt | full |
| evidence\kanjipedia-outside-readings.json | full |
| evidence\okurigana-scan.txt | full |
| evidence\jmdict-families.xml | part: I extracted every entry id cited on the 15 Metadata lines, plus 1541760, and grepped all `繰…` kebs |
| evidence\jmdict-digest.tsv | part (the 絞 rows) |
| evidence\audits\reading-exposure.txt | most of it: lines 1–40 plus greps for key lines and for 繕/セン |
| evidence\app-code\KanjiReadings.kt | part (outline and lines 44–135) |
| evidence\app-code\Words.kt | outline only |
| titles\kanji-titles.tsv | part (filtered lookups of every kanji cited in prose, exclusions and distractors) |
| snapshot\kanji\ — all 15 new cards | full |
| snapshot\kanji\締.md, 緩.md, 綱.md, 緊.md | full, then re-grepped |
| snapshot\strokes\*.json (15) | all parsed for kanji, strokeCount, stroke ids and source revision; 絞.json printed in full |
| diffs\ (all 20) | full (kanji diffs with context; word diffs as changed lines plus hunk headers) |
| repo\docs\content-format.md | part: heading grep plus lines 86–154 (Kanji card, Quiz authoring, Curated reading questions) |

Not opened:

- evidence\kanjidic2-records.xml. I checked front matter against source-metadata.json instead, plus a live jisho.org KANJIDIC check for 繰.
- evidence\audits\quiz-safety.txt, reading-options.txt, kanji-remarks.json and word-remarks.json. I relied on the mechanical-checks.md summaries and read the three kanji diffs directly.
- snapshot\words\*.md as whole files. The diffs supply the changed lines and their context.
- QuizBuilder.kt and KanjiMeaningMetadata.kt.
- titles\word-titles.tsv.

Public web: jisho.org (KANJIDIC data for 繰: ソウ / く.る, 19 strokes, parts 糸 品 木; on-reading compound 繰糸 ソウシ). I made no other live lookups. All dictionary checks used the pinned JMdict, Daijisen (Weblio) and Kanjipedia extracts in the packet, which is the version the cards cite.

## Verdicts

### Overall (all 15 cards)

| Facet | Verdict |
| --- | --- |
| 1. Correctness | **Minor defects.** Each is a wording or citation slip: 締 (C1, C2, C3), 縄 (C4), 織 (C5), 罰 (C6). Every front-matter field, every reading, every cited JMdict id and gloss I checked, every Joyo-table claim and every mnemonic stroke sum is correct. I found no wrong reading, wrong entry id or wrong homograph. |
| 2. Scoped coverage | **Clean.** Every metadata reading has a row or an explicit source-only/rare qualification (繰 ソウ, 罰 ハツ, 縄 ただ.す). The important family words are present. Two optional gaps: 繰 compounds, and 縦軸's alternative reading (O7). |
| 3. Consistency / quiz safety | **Clean with optional polish.** Titles are unique and distinguishable. Distractors are defensible in both directions. Exclusions are real direct pairs. Every quiz reading has a linked word. Links resolve, section order follows content-format.md, and stroke counts match the cards. See O1–O4. |
| 4. Comprehensibility | **Minor defects** on 締 (C1) and 罰 (C6). The other cards are clear, though long. |

### Per card

| Card | 1 | 2 | 3 | 4 | Notes |
| --- | --- | --- | --- | --- | --- |
| 絞 | ✓ | ✓ | ✓ | ✓ | |
| 継 | ✓ | ✓ | ✓ | ✓ | |
| 綱 | ✓ | ✓ | ✓ | ✓ (O6) | |
| 緊 | ✓ | ✓ | ✓ (O1) | ✓ | |
| 締 | minor (C1, C2, C3) | ✓ | ✓ (O5) | minor (C1) | |
| 緩 | ✓ | ✓ | ✓ | ✓ | |
| 緯 | ✓ | ✓ | ✓ | ✓ | |
| 縁 | ✓ | ✓ | ✓ | ✓ | |
| 縄 | minor (C4) | ✓ | ✓ | ✓ | |
| 縛 | ✓ | ✓ | ✓ (O1) | ✓ | |
| 縦 | ✓ | ✓ (O7) | ✓ | ✓ (O7) | |
| 織 | minor (C5) | ✓ | ✓ | ✓ (O8) | |
| 繕 | ✓ | ✓ | ✓ | ✓ | |
| 繰 | ✓ | ✓ (O9) | ✓ | ✓ | |
| 罰 | minor (C6) | ✓ | ✓ | minor (C6) | |

### Diffs and stroke files

- **17 word diffs: clean.** Each changes exactly one line, and each change is only a link-wrap of the first mention of the new kanji to `../kanji/<k>.md`. For 締め切り, 締め切る and 繰り返す the wrap is `[締](…)め` / `[繰](…)り`, which links only the kanji, as intended. All 17 targets are the intended cards.
- **Dictionary lines:** no diff touches a Dictionary: line. The 綱 and 緯度 diffs touch prose lines only. 威張る has no diff at all, so the three lint warnings stay as context.
- **Remark edits (修, 張, 慢):** each rewrites only the declared sentence, and each link points to the intended card (繕, 緊, 緩). Each resulting sentence is true. Two have optional wording polish (O2, O3).
- **Stroke files: all 15 consistent.** Each has strokeCount equal to both its number of strokes and the card's `strokes:`. Stroke ids run consecutively and the source is KanjiVG revision 70a0b7ae for all 15.

### Leads (a)–(n)

- **(a) 締.** Quizzing し.める is correct: the three linked words are 締める, 締め切り and 締め切る, all しめ-forms; JMdict 1436570, 1594590 and 1594600 confirm this, and Joyo p. 113 lists しめる with 締める, 締め切る and 引き締め. The し.まる label from the automatic alignment is wrong for these words. The card says so, but in learner-facing jargon (C1). The title is fine. The exclusions are real pairs except 限 and 期, which are weak, only transitive via 締め切り (O5). Distractors 紙 店 海 are fine.
- **(b) 絞 / 締 / 緊 / 縛.** 絞 excludes 締, 緊 and 縛. 締 excludes 緊 and 縛. 緊 and 縛 exclude none of the four. So the 緊–縛 pair is excluded on **neither** side, and the lead's premise that every pair is excluded exactly once is not accurate. I judge 緊–縛 safe: "tense; tight; urgent" against "bind; tie up; restrain" is not defensibly interchangeable from either side, though 緊縛 exists (O1). 絞 against 刑 and 殺 is defensible via 絞首刑 and 絞殺; 抽 is defensible via 絞り出す / 抽出 "extract".
- **(c) 綱/縄 and 継/繕.** Distinguishable as titles. Each pair is excluded once (綱→縄, 継→繕), which is sufficient because exclusions are symmetric. Both cards in each pair explain the difference correctly; Daijisen's つな usage note matches the 綱 and 縄 text.
- **(d) 紙 and 終.** Each is wrong but plausible from both sides on every card; neither "paper" nor "end; finish" overlaps any of the eight titles. The repetition is a mild weakness only (O4).
- **(e) 繰.** Correct. Daijisen has no character block. ソウ is honestly labelled source-only (JMdict 繰糸 そうし with re_restr; the Joyo table has only くる). く.る comes from 繰り返す and 繰る, with り and る as okurigana. The title is fine. The exclusions are real direct pairs.
- **(f) 織.** Choosing シキ from 組織 is correct: the Joyo table gives シキ only with 組織, and 組織 is the one linked word. ショク is clearly explained as the reading of most cloth compounds. The kun forms are illustrated correctly (織る, 織り, 織物, 羽織). The exclusions are fine.
- **(g) 罰.** Correct. ばっ.する is explained as sokuon バツ before する. 罰 ばち is JMdict 1478050 "(divine) punishment; curse; retribution" (it carries news1/nf12 priority, so it is a common word). ハツ is source-only. Daijisen's バツ/バチ (慣) and its 罸 note (俗字) are reported accurately. The title and exclusions are fine. Defect C6 is separate.
- **(h) Homographs.** Each card's Metadata ids point at the intended entries:
  - 緩 cites 1183300 ぬるい only to say it is a different word. The card's claim that 緩い is a search-only form there is true; JMdict also notes "usu. written as 緩い" on the "lenient" sense, which the card omits harmlessly.
  - 縁 does not cite 1541760 よし and claims no よし reading.
  - 綱 cites 2179140 こう correctly as a separate entry.
  - No card claims a reading for the wrong homograph.
- **(i) 縁.** The title and the えん/ふち account are correct; Daijisen's four エン senses and examples match. All 17 exclusions are direct overlaps of a displayed title sense, not a transitive clique: 刃 "cutting edge"; 仲 "relations between people"; 運 "luck"; 偶 "chance". Distractors 緑, 縮 and 魚 are fine.
- **(j) 緩.** Titles, labels and JMdict quotes are verified (1214410 and the others). The 16 exclusions are broad but each matches a real gloss of 緩い, 緩やか or 緩慢. 甘 matches "lenient" (甘い); 渋 is the weakest ("sluggish") but still defensible. 緯's イ, its exclusions and its distractors are fine.
- **(k) 縦.** Title and readings are correct. Daijisen's ジュウ (慣) / ショウ (漢) and its kun list are reported accurately. ほしいまま (1908340) and よし (2607700) are correctly called separate words. The exclusions are fine. See O7.
- **(l) 縛 and 縄.** 縛: しば.る and バク are correct, and distractor 専 shares the right-hand shape. 縄: なわ and ジョウ are correct, and the exclusions are fine. See C4.
- **(m) Mnemonics.** All 15 carry the "Modern-shape mnemonic, not etymology" label and a disclaimer. All component statements and the stroke sums I checked are true, for example 繰 = 糸 6 + 品 9 + 木 4 = 19, and 罰 = 罒 5 + 言 7 + 刂 2 = 14. Optional: the 織 wording (O8).
- **(n) Reading audit.** The 9 latent collisions are counted correctly, with 0 production and 0 padded hits. 繰's くり←栗 cannot be drawn, because closer tier-4 candidates fill the single open slot. I found no attested reading that could be drawn as a wrong option.

## Findings

All findings are minor; none is a blocker.

**C1 — 締: tooling jargon and an unverifiable claim in learner prose** (facets 4 and 1; confidence high)
- Location: 締.md L40.
- Claim: "The linked articles teach しめる; the quiz tool labels the stem し.まる for these words, but 締める is しめる."
- Impact: An N5–N4 learner is told about an internal "quiz tool" label they never see. The app code in the packet (KanjiReadings.kt, Words.kt) shows no such word-to-reading alignment, so the sentence is either about authoring tooling or confusing. It also repeats "締める is しめる" from L23.
- Remedy: delete the clause. If the alignment is ever shown to learners, fix the label rather than explaining it on the card.

**C2 — 締: inconsistent statement of what 締 and 切 supply** (facet 1; confidence high)
- Location: 締.md L40 and L50, against words\締める.md (the diff context).
- Claim: L40 says that in 締め切り / 締め切る "締 supplies しめ and 切 … supplies きり and きる".
  - L50 on the same card says 切 supplies き in both words, which is correct, since り and る are okurigana.
  - The linked word article says "締 supplies し … める is okurigana", consistent with KANJIDIC2 し.める.
- Impact: The card contradicts itself and the linked word article about okurigana, which is the very point the cards teach.
- Remedy: "締 supplies し (め is okurigana) and 切 supplies き (り/る are okurigana)."

**C3 — 締: Daijisen paraphrases presented as quoted glosses** (facet 1; confidence medium-high)
- Location: 締.md L25.
- Claim: "The Daijisen character entry gives テイ for "tie up; bind" and "conclude an agreement"…"
- Evidence: Daijisen's text is one Japanese sense, 締めくくって一つにまとめる。約束などを結ぶ。 The two English strings are the author's translations, not JMdict glosses, KANJIDIC2 meanings or card titles. L52 then reuses "conclude an agreement" in quotes.
- Remedy: remove the quotation marks, for example "…gives テイ for binding things together into one and for concluding an agreement…"

**C4 — 縄: Daijisen's variant relation stated backwards** (facet 1; confidence medium-high)
- Location: 縄.md Notes, last bullet.
- Claim: "Daijisen also lists 縄 as a variant of 繩."
- Evidence: weblio-縄.txt has the heading じょう【縄〔繩〕】. Daijisen prints 繩 in brackets as the traditional form of 縄; it does not call 縄 a variant of 繩. The Readings paragraph already says correctly that the Joyo table prints 繩 in brackets.
- Remedy: "Like the Joyo table, Daijisen gives the traditional form 繩 in brackets." Alternatively, delete the bullet.

**C5 — 織: JMdict tag merged into a quoted gloss** (facet 1; confidence high)
- Location: 織.md, Meaning and origin, second bullet.
- Claim: 織豊時代 しょくほうじだい, "historical term Shokuhō period (i.e. the Azuchi-Momoyama period, approx. 1568-1600)".
- Evidence: in JMdict 2205540, "historical term" is a `<misc>` tag. The gloss itself begins "Shokuhō period …".
- Remedy: write `"Shokuhō period (i.e. …)" (historical term)`.

**C6 — 罰: dangling cross-reference and empty Notes bullet; sentence fragment** (facets 1 and 4; confidence high)
- Location: 罰.md, Meaning and origin ("More Daijisen examples are listed at the end of the Notes.") and the last two Notes bullets.
- Claim: the Notes end with "For reference, Daijisen lists further examples of the senses above.", which lists none. The preceding bullet, "Other kanji read バツ, バチ or ハツ; none of them is ever offered as a wrong answer.", has no main verb.
- Impact: the cross-reference promises content that is absent, and the bullet is padding. The fragment reads poorly on a phone. All other cards list the promised examples.
- Remedy: list the Daijisen examples from weblio-罰.txt (罰則 刑罰 厳罰 重罰 賞罰 体罰 / 懲罰 信賞必罰 / 神罰 冥罰), or delete both sentences. Rewrite the fragment as "Other kanji read バツ, バチ or ハツ are never offered as wrong answers."

## Optional

- **O1 (緊, 縛):** the 緊–縛 pair is unexcluded on both sides. I judge it safe; adding 縛 to 緊's exclusions (緊縛 "binding tightly") would be cheap insurance.
- **O2 (張 remark edit):** "[緊](緊.md) is the kanji in 緊張." 緊張 has two kanji. For parallel structure with the rest of the bullet, write: [緊](緊.md), "tense; tight; urgent," is the other kanji in 緊張.
- **O3 (慢 remark edit):** "[緩](緩.md) in 緩慢 has its own kanji card; this does not change the complete word's reading." After the rewrite, the second clause no longer follows. Suggested: "[緩](緩.md), "loosen; slack; lenient," is the other kanji in 緩慢; learn かんまん as a whole word."
- **O4 (distractors):** 紙 "paper" is a distractor on 8 of the 15 cards, and on most 糸-key cards. It is never wrong in itself, but a learner can learn that "paper" is never the answer for these cards. Consider varying it with other 糸-key cards that are not excluded, such as 絵, 給 or 細, where they are not already used.
- **O5 (締):**
  - The exclusions 限 and 期 come only via 締め切り "deadline". They are harmless but transitive; consider dropping them.
  - L51 shows the raw entry id "閉める 1508590" in learner prose; remove the number.
- **O6 (綱 L54):** "海 and 夏 are common starter cards with kun readings like つな" can be read as saying they share つな. Suggested: "with short two-kana kun readings (うみ, なつ)".
- **O7 (縦):**
  - "縦軸 … 縦笛 … 縦糸 … they keep たて": JMdict 1709530 also reads 縦軸 じゅうじく. Consider a parenthetical.
  - "The 経 spelling of 縦 is tagged 'rarely used kanji form'" is clumsy. Suggested: "JMdict also lists 経 as a rarely used spelling of たて."
- **O8 (織 mnemonic):** "音, with a hooked stroke beside it": the remaining element is a 戈-like group of several strokes, not one stroke. Suggested: "with a 戈-like shape beside it".
- **O9 (繰 coverage):** common compounds 繰り越す, 繰り広げる and 繰り上げる are not mentioned. They are not required, but one would show that く.る is productive beyond 繰り返す.

## Limits

- **Tool-call rule:** I kept to one tool call per response and issued no parallel calls. Several single calls were PowerShell commands that printed or filtered a few specific named files, such as the 15 weblio extracts or the 20 diffs. These are targeted opens, not scans; I note them in case the owner reads "one file per call" more strictly.
- **Context compaction:** part of this review (the first six cards and the evidence reading) happened before a context summarisation. I rely on my notes from that phase for 絞, 継, 綱 and 緊, and I re-checked 締, 綱 and 緊 lines directly afterwards.
- **Files not opened:** KANJIDIC2 records were checked via source-metadata.json, not the raw XML. I did not open quiz-safety.txt, reading-options.txt or the remarks JSON; for the meaning-quiz and reading-options results I accept the mechanical-checks summaries (0 errors and 0 problems), apart from my own reading of KanjiReadings.kt.
- **Live checks:** I made one live public check (jisho.org for 繰). Other verification used the pinned packet extracts. Live dictionaries can differ from the 2026-11 snapshots the cards cite.
- **Known packet limits:** the Android JVM tests and the Kotlin reading-audit cross-check were not run. I treated these as packet limits, as instructed.
- **Assumption:** the 締 "quiz tool" sentence (C1) refers to authoring or alignment tooling rather than anything the app displays. If the app does display し.まる for these words, that is a separate, more serious defect outside this card.
