# Batch 112 initial content review (Claude)

## Snapshot

- Candidate: d6ad96ebf7d0352d54184ed44a382f70e4497f7b (signed locally, unpublished); base 0320ba4a199432374096360e984b7dc5754dd6bc.
- Packet: C:\Users\stop-\n1-kanji-workspace\review-packets\batch-112-d6ad96eb. SHA256SUMS.json SHA-256 22dc9721a0dc9bd2d4e1e94a4cf7cc74cc4137ac017a435f78a17787089c2288 verified; all 6,392 listed files re-hashed, 0 mismatches.
- Reviewer: single independent blind initial review, first of two serial reviews. Configured model claude-opus-5.5; actual execution-model identity is unverified.
- Read-only. No JVM, Gradle or emulator was run. Nothing was edited, staged, committed or pushed except this report.

## Scope

Read in full:

- REVIEW.md, packet.json, provenance.json and the rubric (copilot-instructions, content-structure instructions, content-format kanji/quiz/curated-reading sections).
- All 15 new kanji cards: 健 妙 射 就 展 微 態 盤 看 至 診 酸 障 離 響.
- The 基, 素 and 鏡 remark changes, and the whole of diffs\existing.diff (611 lines, 44 word articles, 45 link additions).
- All 75 JMdict families in jmdict-families.xml, source-metadata.json (KANJIDIC2), dictionary-index.json and joyo-rows.json (all 15 rows).
- All check outputs except the full body of reading-exposure.txt, which I did not read line by line.

Mechanical cross-checks I ran (Python, read-only):

- Snapshot cards and words equal their repo\ copies after CRLF/LF normalisation (line-ending difference only).
- 372 relative links in the 18 snapshot kanji cards resolve, and every distractor and exclusion target has a card.
- Every word article whose `kanji:` metadata contains a new kanji (3 per kanji, 45 total) links the kanji, and the kanji card links it back. No eligible article is unlinked.
- For all 15 strokes JSON files, the stroke count matches the KanjiVG SVG path count, the card front matter and KANJIDIC2. Per-stroke id/type match and start points are within 0.6 of the SVG `M` coordinates. All use sourceRevision 70a0b7ae.

Comparison context read:

- Titles, exclusions and distractors of all 1,191 kanji cards (overlap scan).
- Bodies of the reused articles where a card claim depended on them: 射す, 事態, plus the How-the-kanji-combine sections of all 44 changed articles via the diff.

Not read or not verified, and consequential:

- The full text of every one of the 44 reused word articles outside the diffed section. I did not re-review existing article content; only the link insertions and the card claims that depend on those articles.
- The reading-exposure.txt detail lines (summary only).
- Weblio/Daijisen public character pages. I did not fetch them; character-sense claims rest on JMdict/KANJIDIC2/Joyo evidence in the packet.

Disclosure: I briefly wrote and immediately deleted C:\Users\stop-\AppData\Local\Temp\jm112.txt (compact JMdict dump). The harness also auto-created a tool-output temp file. No other writes.

## Verdicts

| Facet | Verdict |
| --- | --- |
| Correctness (metadata, readings, glosses, dictionary restrictions, strokes, links) | CLEAN. Polish item F3 only. |
| Scoped coverage (15 cards, 45 links, 3 remark changes, stroke refs) | CLEAN |
| Consistency / quiz safety | NEEDS FIX (F1, F2). |
| Comprehensibility | CLEAN |
| Runtime / Kotlin / phone / custom-pool quiz behaviour | UNVERIFIED (out of scope; see Limits) |

## Findings

### F1. 微 "minute; faint" collides with 分 "minute, part" (NEEDS FIX, moderate; high confidence)

- 微's title uses "minute" (tiny); 分 (N5) is titled "minute, part".
- In an English→kanji or kanji→English meaning quiz, "minute" is a valid reading of either title, and "minute, part" can be read as "a tiny part".
- Neither card excludes the other: 微 excludes [細, 小, 少, 薄, 弱]; 分 has no exclusions.
- 分 is a high-frequency card present in every pool that contains 微.
- Remedy (either):
  - add 分 to 微's quiz_exclusions; or
  - retitle 微 to avoid the homograph, e.g. "tiny; faint" or "slight; faint".

### F2. 就 "take a position; undertake" collides with 企 "plan; undertake" and 承 "accept; undertake" (NEEDS FIX, moderate; high confidence)

- Same English head word "undertake" on three cards. 企 is also N1 (jlpt-n1), so it lands in the same level pool.
- 就's exclusions [着, 付, 任, 定, 成, 始, 去, 発, 学] omit both.
- Lower but real overlap: 担 "shoulder; take on" and 職 "employment; post" (就職 is one of 就's own example words). 位 "rank; position" vs "take a position" is weak.
- Remedy: add at least 企 and 承 (consider 担 and 職) to 就's quiz_exclusions, or rephrase 就's second gloss so "undertake" is not shared.

### F3. 態 Notes: "separate 態 entries read てい, なり and ざま" (polish, minor; high confidence)

- In JMdict, those families are headed by 体 (てい), 形 (なり) and 様 (ざま), with 態 only as an alternative or rare spelling.
- They are not 態 entries in their own right, so the wording overstates their status.
- Suggested wording: "態 also appears as a less common alternative spelling in the dictionary families of 体 (てい), 形 (なり) and 様 (ざま)."

## Optional

- **O1. 障 "obstruct; hinder" vs 関 "involve; barrier".**
  - 障's own body speaks of barriers, and 障害/障子 draw on a barrier or partition association. 障 excludes only [害, 防].
  - Medium confidence that a learner would accept 関's "barrier".
  - Consider adding 関.
- **O2. Weaker meaning overlaps, likely acceptable but worth a glance:**
  - 展 "unfold; expand" vs 敷 "spread; lay out" (展's body says "spreading out").
  - 妙 "strange; exquisite" vs 技/腕 "skill" (JMdict 妙 sense 3 is skill/knack, but the card does not title it so).
- **O3. 態 タイ in grammatical "voice" (受動態 etc.)** is not mentioned. This is not a defect for N1 scope; it is an optional enrichment.

Items reviewed and found sound (not findings):

- **射 さ.す.** The card is transparent that Joyo lists only シャ/いる, and the 射す article supports the reading.
- **態 on 事態.** The card's "attention to events developing" matches the 事態 article ("especially one that has developed"); the article separately carries JMdict's negative-connotation note.
- **Restriction labels.** These stay attached to the correct entries:
  - 看護婦 is marked deprecated/dated.
  - 乃至 and 算盤 are usually written in kana.
  - 微か and 態と are usually written in kana, and 態と is a rare kanji form.
  - 神妙 しんびょう is an out-dated kana reading.
  - 射つ is a rare form in the 撃つ family.
  - 基盤 is an irregular form for "circuit board".
- **基/素/鏡 remark changes.** These narrowly update "no card yet" wording and are correct.
- **Mnemonics.** All 15 are labelled modern-shape mnemonics; no invented etymology or constituent readings.

## Limits

- The packet's validate (0 errors), lint (0 errors, 8 warnings for missing or ID-less Dictionary lines in 看板, 看護婦, 算盤, 診る, 響き, 響く, 眼鏡, 鏡), links (45 pairs, 0 problems), unit tests (431 OK), manifest and quiz-safety (0 errors) outputs are mechanical evidence, not linguistic proof.
- The Python reading audit models only N1/All pools and Starter with a single borrowed target. Not verified:
  - custom or caller-built pools;
  - multi-borrow Starter;
  - actual Kotlin draw behaviour and fallback level-pool behaviour;
  - native execution and phone acceptance.
- The older installed APK (5c000bd) predates quiz_exclusions, so F1/F2-type exclusions would not protect it. Its compatibility is unverified.
- F1 and F2 are judgments about English-title ambiguity for learners, not runtime-reproduced quiz failures.
