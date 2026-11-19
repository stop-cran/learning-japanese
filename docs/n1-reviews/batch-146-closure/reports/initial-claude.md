# Batch 146 — independent blind review (initial, reviewer 1)

Reviewer model: Claude (Anthropic model family). This is a blind, read-only review. I did not look at the other reviewer's report or at the author's rationale.

## Snapshot

- Commit: `38833c7f58bdd2406dbb808c6b2a74257ef29f12` (batch 146).
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-146-38833c7f` (packet-manifest.json sha256 d51bc2fb…5c88, as stated in the assignment; I did not recompute it).
- Unit under review:
  - the 15 new kanji cards 煮 熟 牧 狂 狭 献 玄 環 甚 癖 益 盛 盾 眺 睡;
  - their 15 stroke files;
  - the 23 link-wrap diffs of word articles;
  - the declared one-sentence remark edit in `kanji/潔.md`.

## Scope

Files opened, and how much of each I read:

- `INSTRUCTIONS.md`: in full.
- `mechanical-checks.md`: in full, with each section truncated as the packet itself truncates it.
- `evidence\source-metadata.json`: in full.
- `evidence\kanjidic2-records.xml`: in part. I filtered it to the literal, grade, stroke count, classical radical, ja_on/ja_kun and nanori lines of every record.
- `evidence\joyo-pages.md`: in full.
- `evidence\public-source\weblio-*.txt` (all 15): in full.
- `evidence\okurigana-scan.txt`, `evidence\daijisen-heads.txt`, `evidence\kanjipedia-outside-readings.json`: in full.
- `evidence\jmdict-families.xml`: in part. I queried by entry id every JMdict id cited in the 15 cards, plus 1529360 and the other ids the leads name.
- `evidence\jmdict-digest.tsv`: in part (the header and the rows for 煮 and 熟).
- `evidence\audits\quiz-safety.txt`: in full.
- `evidence\audits\kanji-remarks.json`: in full.
- `evidence\audits\reading-exposure.txt`: in part. I read:
  - the command and the header;
  - the sections for 煮, 熟, 牧, 狂, 狭, 玄, 環, 甚, 癖, 益 and 盛, and the end of 睡;
  - every "attested reading" line;
  - the summary tail.
- `evidence\audits\reading-options.txt`: in part (the command, the start of the 煮 section, the 玄 section and the tail).
- `snapshot\kanji\*.md`, the 15 new cards: in full.
- `snapshot\kanji\潔.md`: in part (lines 25–60, which hold the changed line and its context).
- `snapshot\strokes\*.json` (15 files): every file was parsed to compare kanji, strokeCount, stroke count and id sequence with the front matter. I printed 煮.json in full.
- `snapshot\words\`: I listed the folder. Of the 23 articles, I opened only `矛盾.md`, and only the lines matching 盾/story/spear. I judged the other 22 articles from their diffs.
- `diffs\` (24 files): I read the hunk headers and every changed `+`/`-` line of all 24 diffs.
- `titles\kanji-titles.tsv`: programmatic lookups.
  - Titles of every new card, distractor, exclusion and cross-referenced card.
  - A check that titles are unique (no duplicates).
  - A shared-English-word scan of the 15 new titles against the whole file.
- `repo\docs\content-format.md`: in part (a heading grep, plus lines 86–154: Kanji card, Quiz authoring and Curated reading questions).
- Not opened:
  - `evidence\app-code\*`;
  - `rubric\*`;
  - `titles\word-titles.tsv`;
  - `evidence\audits\kanji_remarks.py`;
  - `packet-manifest.json`;
  - `evidence\provenance.json`;
  - `repo\docs\confusable-words.md`;
  - every file in `repo\kanji` and `repo\words`.

Public web, inspected directly:

- Weblio / Digital Daijisen `益体` (headword `やく‐たい【益体】`).
- Weblio `煮凝り`, in part. The headword line was not captured, so I fell back on morphology for this item; see C4.

I also fetched a kotobank URL whose id I had guessed. It redirected to an unrelated entry and was discarded.

## Verdicts

Overall, by facet:

| Facet | Overall verdict |
| --- | --- |
| 1. Correctness | Defects found: 1 major (C1), 1 moderate (C2), several minor (C3–C9). |
| 2. Scoped coverage | Acceptable, with one labelling defect that also misstates coverage (C2). |
| 3. Consistency and quiz safety | CLEAN for the quiz mechanics. One minor title/exclusion-basis issue (C8). |
| 4. Comprehensibility | Acceptable, with minor issues (C7, C9 and optional polish). |

The checks behind these verdicts:

- **Front matter:** all 15 cards match KANJIDIC2 and source-metadata (grade, strokes, radical, on/kun order, quiz lists).
- **Stroke files:** all 15 have strokeCount equal to the front matter, a matching number of strokes, sequential ids, and KanjiVG revision 70a0b7ae.
- **Diffs:**
  - All 23 word diffs change exactly one line. Each wraps the first bare mention of the new kanji as a link to `../kanji/<k>.md`, and changes nothing else.
  - In `眺める` the link wraps only 眺 inside the word "眺める". It renders correctly.
  - The 潔 diff is the declared edit. It matches kanji-remarks.json exactly, the sentence is true, and the paragraph still reads correctly.

Per card where it differs from the overall verdict:

| Card | F1 Correctness | F2 Coverage | F3 Consistency/quiz | F4 Comprehensibility |
| --- | --- | --- | --- | --- |
| 煮 | minor C4 | OK | OK | OK (jargon, optional) |
| 熟 | minor C5 | OK | OK | OK |
| 牧 | OK | OK | minor C8 | minor (C8: no kana for 牧童/牧羊) |
| 狂 | OK | OK | OK | OK (kana, optional) |
| 狭 | OK | OK | OK | OK (optional 狭霧 wording) |
| 献 | OK | OK | OK | OK |
| 玄 | minor C6 | OK (optional やしゃご) | OK | OK |
| 環 | OK | OK | OK | OK |
| 甚 | **major C1**, C2 | C2 | OK | C1 is confusing |
| 癖 | C2, minor C7 | C2 | OK | minor C7 |
| 益 | minor C3 | OK | OK | OK |
| 盛 | minor C9 | OK | OK | minor C9 |
| 盾 | OK | OK | OK | OK |
| 眺 | OK | OK | OK | OK |
| 睡 | OK | OK | OK | OK (jargon, optional) |
| 潔 (edit) | OK | n/a | OK | OK |

Leads (a)–(r), judged independently. Unless noted, I found no defect.

**(a) 煮**

- The title is fine, and 沸/炊 are direct "boil" pairs. The one-sided 煮→熟 exclusion is enough, because exclusions are symmetric (content-format.md l.117).
- 熟 does carry にる/にえる in Daijisen, so the pair is real.
- 火 水 肉 are wrong in both directions.
- Defect: the 煮凝り claim (C4).

**(b) 熟**

- The exclusions are direct overlaps; 技 and 腕 share "skill".
- 語 木 田 are fine.
- Defect: the "linked words" sentence (C5).

**(c) 牧**

- 歌 山 雨 are fine.
- The ま/まい/もく collisions are latent and correctly accounted.
- Issue: "pastor" and the exclusions that rest on the govern sense (C8).

**(d) 狂**

- The card does not list ふ.れる. It is not in KANJIDIC2; it comes from Kanjipedia only, and JMdict 2433680 has it usually in kana.
- The latent ふれる/触 collision is accounted.
- The exclusions and 犬 気 風 are fine.

**(e) 狭**

- 狭い and 狭苦しい are accurate. 苦しい is a correct part-of-run match.
- The exclusions are fine, せ/瀬・背 is latent, and 道 室 店 are fine.

**(f) 献**

- The kun labelling is accurate (たてまつ.る is source-only, with ささげる/まつる explained).
- The exclusions are fine, and 猫 独 状 are fine.

**(g) 玄**

- The title and exclusions are fine, and 率 畜 玉 are fine.
- Defect: the mnemonic's stroke statement (C6).

**(h) 環**

- The remark about 琴 (王王 at the top) is true.
- The title and exclusions are fine.
- The reading prompt uses 2 of its 3 curated options because 琴 has no reading that can be offered. Fallback fills the third slot, and the audit reports no problem.

**(i) 甚**

- Defects: C1 and C2.
- じ/路 and いたい/痛 are latent only.
- 甘 匹 基 are fine.

**(j) 癖**

- Defects: C2 and C7.
- The 14 exclusions are broad but harmless (see Optional).
- 疲 痛 療 are fine.

**(k) 益**

- The exclusions are defensible. 利 and 享 share "benefit", and 得 shares "gain".
- よう is latent only.
- 皿 雨 魚 are fine.
- Defect: C3.

**(l) 盛**

- The account of 盛る is accurate. The separate さかる entry is JMdict 1379730, and the card cites it.
- The 13 exclusions are defensible overlaps.
- もり/守・森 is counted for both prompts, correctly.
- 山 海 店 are plausible but wrong. The Notes justify their plausibility, not their Starter status, which is enough.
- Defect: C9.

**(m) 盾**

- All accurate, including 楯突く/盾突く (1610710: 盾突く is a plain variant) and the 矛盾 story attribution.

**(n) 眺**

- All accurate.

**(o) 睡**

- I verified each written form against JMdict:

  | Written form | JMdict entry | Tag | Card says |
  | --- | --- | --- | --- |
  | 睡る | 1529390 | none | a written form (correct) |
  | 睡い | 1529330 | none | a written form (correct) |
  | 睡り | 1529370 | "rarely used kanji form" | rare (correct) |

- 睡眠, 熟睡, 午睡 and 昏睡 are accurate.
- 眠 and 寝 are the right exclusions, and 真 着 直 are fine.

**(p) Shared distractors and Starter cards**

- All are acceptable. Sharing a distractor across cards is not a defect.

**(q) Shared English words between titles**

- The scan of all 1,442 titles found these shared words not covered by an exclusion:
  - 牧/挙 and 牧/畝 "raise";
  - 環/鳴 "ring";
  - 盛/食 "food";
  - 眺/仰 and 眺/捜 "look";
  - 献/縮 "contract" (a stem artefact of the scan).
- Each is a clearly different sense, so none lets a learner defend a wrong answer (see Optional for 環/鳴).

**(r) Reading-exposure accounting**

- 10 lines make 9 distinct pairs; もり/守・森 is printed once for each 盛 prompt. The count is correct.
- I found no attested reading that is drawable.
- 玄's name reading けん is absent from the "unlisted" list. That is consistent with it being excluded as the unvoiced counterpart of げん: the reading-options tier list for 玄 omits けん.
- One labelling issue is noted under Optional.

## Findings

### C1 — 甚: the okurigana of 甚だしい is misstated (major; facet 1, also 4)

- **File:** `snapshot\kanji\甚.md` line 37.
- **Claim:** "In 甚だしい, 甚 writes はなはだ and しい is okurigana, the kana ending that follows the kanji. The repo's alignment labels this はなはだ as はなは.だ …"
- **Why it is wrong:**
  - The spelling 甚だしい has だしい in kana, so 甚 writes only はなは and the okurigana is だしい.
  - The same holds for the adverb 甚だ: はなは + だ.
  - KANJIDIC2 records exactly this: はなは.だ and はなは.だしい.
  - The card's own sentence presents the correct aligner label as a mislabel ("labels this はなはだ as はなは.だ").
  - Line 41 repeats the framing: "which the repo's aligner labels by its stem".
- **Impact:** a learner is taught the wrong kanji/kana boundary for the quizzed word, in the very paragraph that explains okurigana.
- **Remedy:** "In 甚だしい, 甚 writes はなは and だしい is okurigana; in the adverb 甚だ, 甚 writes the same はなは and だ is okurigana. KANJIDIC2 lists this reading as はなは.だ and the longer form as はなは.だしい." Then drop the "aligner labels by its stem" wording on line 41.
- **Evidence:** KANJIDIC2 record for 甚; JMdict 1592750 (甚だしい) and 1278390 (甚だ); the visible spelling.
- **Confidence:** high.

### C2 — 甚 ジン and 癖 ヘキ are labelled "source-only here" although they are official readings with common words (moderate; facets 1–2)

- **Files:**
  - `snapshot\kanji\甚.md` line 33: `| ジン | on, source-only here | 甚大 …`
  - `snapshot\kanji\癖.md` line 33: `| ヘキ | on, source-only here | 性癖 … 悪癖 …`
- **How the batch uses the label:** elsewhere in the batch, "source-only" marks a reading for which no ordinary word exists:
  - 献 line 47: "there is no ordinary word here where 献 writes たてまつ.る; the reading is source-only";
  - 玄 line 42 (くろ.い);
  - 狭 line 40 (コウ).
- **Why it is wrong here:** both readings have rows in the official Joyo table and common words.
  - ジン is the Joyo on reading, with 甚大, 激甚 and 幸甚 (the card itself says so on line 41). 甚大 is JMdict 1370040 news2/spec2.
  - ヘキ is the Joyo on reading, with 習癖, 病癖 and 潔癖. 潔癖 (1254470) and 性癖 (1375510) are news2/spec2.
  - Other Joyo readings in the batch that lack a word article are labelled plain "on" (益 ヤク, 盛 セイ/ジョウ, 眺 チョウ, 盾 たて is "kun").
- **Impact:** the label tells the learner that a standard, productive reading exists only in sources. It contradicts the cards' own Joyo paragraphs and is inconsistent within the batch.
- **Remedy:** change both Type cells to plain `on`. Keep "no word article yet, not selected for questions here".
- **Evidence:** joyo-pages.md (甚 and 癖 rows); JMdict 1370040, 1254470 and 1375510; the label usage in 献, 玄 and 狭.
- **Confidence:** high.

### C3 — 益: 益体 is wrongly called an unsplittable whole-word reading (minor; facet 1)

- **File:** `snapshot\kanji\益.md` line 43.
- **Claim:** "In 益体 and 益荒男 ますらお … the whole word has its own reading, so they are not split into per-kanji readings."
- **Why it is wrong:**
  - 益体 やくたい is a regular on-on compound: 益 = ヤク + 体 = タイ.
  - The Digital Daijisen headword is `やく‐たい【益体】` (checked live on Weblio), with the morpheme split marked.
  - The card itself, in its Meaning section, uses 益体 as the Daijisen example of the reading ヤク.
  - 益荒男 ますらお is correctly described.
- **Impact:** a self-contradiction that hides a second ヤク example.
- **Remedy:** "In 益体 やくたい, 益 supplies ヤク and 体 supplies タイ. 益荒男 ますらお has a whole-word reading and is not split."
- **Evidence:** JMdict 2870538; Weblio/Daijisen 益体.
- **Confidence:** high.

### C4 — 煮: 煮凝り is wrongly called an unsplittable whole-word reading (minor; facet 1)

- **File:** `snapshot\kanji\煮.md` line 39.
- **Claim:** "煮凝り にこごり … and 煮麺 にゅうめん … are whole-word readings that Daijisen lists among hard-to-read compounds; they are not split among their kanji."
- **Why it is wrong:**
  - 煮凝り splits regularly: 煮 = に (as in 煮る) + 凝り = こごり (the noun of 凝る こごる).
  - Being listed as 難読 is not the same as having a whole-word reading.
  - Only 煮麺 にゅうめん is irregular.
- **Remedy:** limit the whole-word statement to 煮麺. Say that in 煮凝り, 煮 writes に and 凝り is こごり.
- **Evidence:** JMdict entry cited on the card; daijisen-heads.txt (難読 listing).
- **Confidence:** medium-high. I did not capture the Daijisen headword line live.

### C5 — 熟: "linked words" includes words that are not linked (minor; facet 1)

- **File:** `snapshot\kanji\熟.md` line 51.
- **Claim:** "The other kanji in the linked words are 語 (ゴ) in 熟語, 練 (レン) in 熟練 and 慮 (リョ) in 熟慮".
- **Why it is wrong:** only 熟語 is linked. Line 38 itself says 熟練 and 熟慮 have no word article yet.
- **Related gap:** 練 has a card (title "practice; refine") but is not linked, although 語 is not linked either.
- **Remedy:** "The other kanji in the linked word 熟語 is [語](語.md) (ゴ). In the other examples, [練](練.md) supplies レン in 熟練 and 慮 (no card yet) supplies リョ in 熟慮."
- **Confidence:** high.

### C6 — 玄: the mnemonic miscounts the cap (minor; facet 1, component statement)

- **File:** `snapshot\kanji\玄.md` line 34.
- **Claim:** "a small character with a cap stroke on top of a twisted loop below it".
- **Why it is wrong:** the top element 亠 is two strokes (a dot and a horizontal), and 2 + 3 (幺) = 5 strokes. The stroke file shows strokes 1–2 forming the cap.
- **Remedy:** "a two-stroke lid 亠 on top of a twisted loop".
- **Confidence:** high.

### C7 — 癖: overgeneralized sound statements and one misleading cross-reference (minor; facets 1 and 4)

- **File:** `snapshot\kanji\癖.md` line 37.
- **Problems:**
  - "Joined to another word, くせ is voiced to ぐせ" is presented as a rule. In the same paragraph, 難癖 is read なんくせ (unvoiced), and JMdict gives 手癖 as both てくせ and てぐせ.
  - "ヘキ is voiced to ペキ": ぺ is a semi-voiced (handakuten, p-) sound. In 潔癖 the change is the gemination plus p-sound けっ+ぺき, not voicing.
  - "the [潔](潔.md) card links this word": the 潔 card does not link the word 潔癖, which has no article. It mentions 潔癖 and, after this batch, links the 癖 card.
- **Remedy:**
  - Write "often voiced to ぐせ (口癖 くちぐせ, 酒癖 さけぐせ); 難癖 なんくせ keeps くせ, and 手癖 has both てくせ and てぐせ."
  - Write "ヘキ becomes ペキ after the small っ".
  - Write "the 潔 card links back to this card for 潔癖".
- **Evidence:** JMdict 1461100, 1699540, 1254470 and 1663290.
- **Confidence:** high.

### C8 — 牧: "pastor" in the title, and exclusions based on undisplayed senses (minor; facet 3, also 4)

- **File:** `snapshot\kanji\牧.md`, front matter (title and quiz_exclusions) and the Notes.
- **Claim:** the title is "pasture; raise livestock; pastor".
- **Problem with the title:**
  - "Pastor" is the meaning of 牧師 (師 supplies the person). 牧 alone does not mean pastor.
  - KANJIDIC2 gives 牧 the meanings breed, care for, shepherd, feed and pasture. Daijisen's second sense is governing or guiding people.
  - The title therefore teaches a meaning of the compound as a meaning of the character.
- **Problem with the exclusions:**
  - 治, 御, 官, 司 and 導 are justified by the undisplayed "govern people" sense.
  - content-format.md l.122 says to author pairs only "from evidence about the actual displayed labels and ordinary meanings".
  - The over-exclusion causes no learner harm. It only narrows the fallback pool.
- **Smaller point:** the Notes give 牧童 and 牧羊 without kana or a gloss (line 53).
- **Remedy:**
  - Replace "pastor" with "shepherd" (a KANJIDIC2 meaning), or with "tend (flocks)".
  - Then keep only the exclusions that overlap the displayed title.
  - Add ぼくどう and ぼくよう.
- **Confidence:** medium. Titles are an editorial judgement.

### C9 — 盛: 盛ん is filed under さか.る, while the さか.ん row says it has no example (minor; facets 1 and 4)

- **File:** `snapshot\kanji\盛.md` lines 36, 37 and 39.
- **What the card does:**
  - The さか.る row links 盛ん さかん.
  - The さか.ん row (the KANJIDIC2 reading that exactly matches 盛ん) shows the same word but says "no separate aligned example". Line 39 explains this by the repo's alignment.
- **Why it is a problem:**
  - The okurigana of 盛ん is ん, so per KANJIDIC2 the reading 盛 has there is さか.ん, not さか.る.
  - The quiz key is unaffected, because both share the stem さか and the app treats a shared stem as one reading card.
  - The learner-facing table, however, misattributes the reading and explains the choice with tool jargon.
- **Remedy:**
  - Link 盛ん on the さか.ん row.
  - Keep 盛り on the さか.る row.
  - If the validator needs a link on the selected さか.る row, 盛り already supplies it.
  - Drop the alignment explanation.
- **Confidence:** medium-high.

## Optional

- **Implementation jargon in learner text:** "the repo's aligner/alignment" in 煮 l.36, 甚 l.37/41, 盛 l.39 and 睡 l.37 (昏睡). Rephrase in dictionary terms or omit.
- **Kanji without kana in Notes:**
  - 狭: 狭窄, 狭小, 狭軌, 狭心症;
  - 狂: 狂人, 狂乱, 発狂, 狂喜, 狂態, 酔狂, 狂言;
  - 癖: 習癖, 病癖, 奇癖, 手癖;
  - 牧: 牧童, 牧羊.
- **玄 l.30:** JMdict 1263440 玄孫 also has the everyday reading やしゃご. Consider adding it.
- **狭 l.29/44:** 狭霧 is called "not split among its kanji" but serves as the example of the prefix reading さ (さ + ぎり). Say "さ + ぎり (霧, voiced)" instead.
- **reading-exposure.txt provenance:** it labels ふれる (狂) and いたい (甚) "card text". Neither reading appears in those cards; they come from the --extra list (Kanjipedia / okurigana scan). This is an audit-label imprecision with no effect on the counts.
- **環 / 鳴:** 環 "ring; loop; surround" and 鳴 "animal call; ring" share "ring" in different senses. There is no realistic ambiguity in either direction; an exclusion is optional.
- **眺 / 相:** the distractor 相 "mutual; aspect" carries the English "aspect", which can mean "outlook; view". A learner is very unlikely to pick it, but 省 or 県 alone are safer.
- **癖 exclusions:** 風 "wind; style", 様 "manner" and 柄 "handle; pattern; nature" are loose overlaps with "habit; peculiarity". They are harmless, but not strictly direct pairs.
- **眺める word diff:** the link covers only 眺 within "眺める" (`[眺](../kanji/眺.md)める`). It is correct, but the 眺め article style (link on the bare kanji) is slightly cleaner.

## Limits

- **Execution:** every assistant response contained exactly one tool call. I issued no parallel calls and used no sub-agents.
- **Temporary files, disclosed:**
  - I briefly created a helper `jm_tmp.py` in `reports-146\` and deleted it.
  - I briefly wrote `x.py` to `%TEMP%` and deleted it; Test-Path confirmed the deletion.
  - No other file outside the report path was written. I later piped helper scripts via stdin instead.
- **Word snapshots:** I judged the 23 word-article changes from their diffs. Apart from a grep of 矛盾.md, I did not reread the full articles.
- **Material not opened:** I did not open app-code, the rubric or word-titles.tsv. Quiz behaviour is taken from content-format.md and the packet's audits.
- **Public-web verification:**
  - I inspected live only Weblio/Daijisen 益体 (in full) and 煮凝り (in part).
  - All other dictionary checks used the pinned JMdict/KANJIDIC2 extracts and the packet's Weblio/Joyo/Kanjipedia extracts.
  - Live dictionaries may differ from the pinned snapshots.
- **Known limits of the packet, not reported:** the Android JVM tests and the Kotlin cross-check were not run, and localZipBytes varies.
- **Assumption, "source-only":** I took "source-only" to mean "no ordinary word writes this reading with this kanji", as 献 l.47 defines it in the batch.
- **Assumption, けん for 玄:** I took the reading-options tier omissions (for example, けん for 玄) to reflect the app's protected-key handling, not missed collisions.
