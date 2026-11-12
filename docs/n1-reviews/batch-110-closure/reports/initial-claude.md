# Batch 110 blind review: initial reviewer (Claude)

## Snapshot

- Commit under review: `453af714d56aa573204d477ff863cb4da756b4c3` (batch 110).
- Kanji: 張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖.
- Reviewer: Claude Opus 5.5 (model ID `claude-opus-5.5`), the first blind reviewer. I worked read-only and alone, with one tool call per step and no sub-agents.
- Deepest emphasis: facet 1 (correctness) and facet 2 (scoped coverage). All four facets were covered for all 15 cards and all 93 word-article diffs.

## Scope

Packet root: `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-110-453af714`

| File | How read |
| --- | --- |
| `INSTRUCTIONS.md` | In full |
| `mechanical-checks.md` | In full. The quiz-simulation section is truncated at its start, so the 張, 器 and 素 option lines are absent (see Limits). |
| `rubric\copilot-instructions.md` | In full |
| `repo\docs\content-format.md` | In part: lines 1–190 (kanji card fields, quiz authoring, reading questions, word article fields), plus a targeted search for link and "How the kanji combine" rules |
| `snapshot\kanji\` 張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖 `.md` (15) | Each in full. 嫌.md and the 激.md lines 20–32 were re-read with line numbers. |
| `snapshot\strokes\器.json` | In full: stroke order and centre component |
| `snapshot\strokes\` the other 14 `.json` | In part: parsed `kanji` and `strokeCount` (仮6 価8 器15 基11 嫌13 張11 応7 整16 暖13 激16 級9 素10 統12 縮17 騒18; all correct) |
| `evidence\source-metadata.json` | In full |
| `evidence\kanjidic2-records.xml` | In part: queried the 15 batch records (on, kun, nanori) out of 179 |
| `evidence\jmdict-families.xml` | In part: first 40 lines, then targeted queries of about 60 entries (listed under Findings evidence) |
| `evidence\jmdict-digest.tsv` | In part: header only |
| `evidence\provenance.json` | In full |
| `evidence\public-source\weblio-<k>.txt` (15) | All in full (Digital Daijisen character blocks) |
| `diffs\words__*.md.diff` (93) | All 93 parsed in full by a script (changed lines compared after removing the link markup). Five were read in full by eye: 仮名遣い, 好き嫌い, 整備, 片仮名, 物騒. |
| `titles\word-titles.tsv` | In part: queried for the 15 kanji |
| `titles\kanji-titles.tsv` | In part: keyword and kanji queries (嫌, 怪, 疑, 憎, 扱, 吸, 給 and others) |
| `repo\kanji\扱.md` | In part: lines 1–20 (front matter, to check the 級 Notes claim about キュウ and the grade-8 tag convention) |
| Non-recursive listings | Packet root, `snapshot`, `evidence`, `evidence\public-source`, `rubric`, `diffs`, `titles` |

Public web sources I inspected:

- Jisho API entries for まさに (JMdict 正に, 当に, 将に).
- joyokanji.info 異字同訓 page (from the 2014 Agency for Cultural Affairs report).
- The bunka.go.jp Joyo-table PDF: it was fetched, but the content is compressed binary that could not be read as text.

## Verdicts

| Facet | Overall | Cards that differ |
| --- | --- | --- |
| 1. Correctness | **DEFECTS** | 器 (major: false component in the mnemonic); 価, 激, 応 (minor). The other 11 cards are CLEAN on everything I could verify. Claims that cite the Joyo-table PDF's examples and "⇔" contrasts are UNVERIFIED for all cards (see Limits). |
| 2. Scoped coverage | **CLEAN** | None. Every KANJIDIC2 reading has a row or an explicit qualification, including 張 -は.り/-ば.り, 応 -ノウ/ヨウ/あた.る/まさに, 仮 かり-, 価 ケ, 騒 うれい, 暖 ノン, and 級's nanori しな. There is one optional coverage note for 素. |
| 3. Consistency and quiz safety | **CLEAN with one minor defect** | 嫌: 怪 is not excluded (minor). For 張, 器 and 素 the displayed-option simulation was not available, so their distractors were judged from front matter and titles only. |
| 4. Comprehensibility | **DEFECTS (minor)** | 器 (the mnemonic sends the learner to look for a shape that is not there), 価 (the reading explanation contradicts itself), 応 (one sentence denies a reading the card lists). The others are CLEAN. |
| Word-article diffs (93) | **CLEAN** | All 93 are as intended (details below). |

Per-card summary:

| Card | Facet 1 | Facet 2 | Facet 3 | Facet 4 |
| --- | --- | --- | --- | --- |
| 張 | CLEAN* | CLEAN | CLEAN (simulation not visible) | CLEAN |
| 器 | **DEFECT (F1)** | CLEAN | CLEAN (simulation not visible) | **DEFECT (F1)** |
| 素 | CLEAN* | CLEAN (optional O1) | CLEAN (simulation not visible) | CLEAN |
| 応 | **DEFECT (F4)** | CLEAN | CLEAN | DEFECT (F4) |
| 仮 | CLEAN* | CLEAN | CLEAN | CLEAN |
| 基 | CLEAN* | CLEAN | CLEAN | CLEAN |
| 価 | **DEFECT (F2)** | CLEAN | CLEAN | DEFECT (F2) |
| 激 | **DEFECT (F3)** | CLEAN | CLEAN | CLEAN |
| 嫌 | CLEAN* | CLEAN | **DEFECT (F5)** | CLEAN |
| 縮 | CLEAN* | CLEAN | CLEAN | CLEAN (optional O3) |
| 騒 | CLEAN* | CLEAN | CLEAN | CLEAN (optional O3) |
| 統 | CLEAN* | CLEAN | CLEAN | CLEAN |
| 級 | CLEAN* | CLEAN | CLEAN | CLEAN |
| 整 | CLEAN* | CLEAN | CLEAN | CLEAN |
| 暖 | CLEAN* | CLEAN | CLEAN | CLEAN |

\* The Joyo-table example lists and "⇔" contrast notation cited on the card are UNVERIFIED.

### What was verified as correct (facet 1 and 2 detail)

**Front matter**

- Grade, strokes, radical, onyomi and kunyomi match both `source-metadata.json` and the KANJIDIC2 records exactly for all 15 cards.
- The grade-8 cards (嫌, 騒) use the `grade-8` tag, consistent with `repo\kanji\扱.md`.
- Stroke JSON counts match the metadata.

**Daijisen (Weblio extracts)**

These card claims match the extracts:

- 応: オウ（呉） and ヨウ（漢）; いらえる is listed.
- 激: ゲキ（慣）; the 戟 substitute sense for 刺激; the separate prefix げき.
- 嫌: ケン（漢） and ゲン（呉）; senses and examples 嫌悪, 嫌煙, 嫌疑, 機嫌, 嫌気, 嫌味.
- 級: kun しな.
- 暖: ノン（唐）; 難読 暖簾 and 暖気(のんき).
- 素: もと and もとより; 難読 素人.
- 基: 基督 as 難読; the counter and chemistry senses.
- 張: the counter senses.
- 縮: 難読 縮緬.
- 騒: 難読 潮騒.
- 仮: 〈ケ〉 仮病 and 虚仮.
- 価: no ケ.
- 騒: no うれい.

**JMdict (pinned families file)**

Every one of these card claims checked out:

| Kanji | Entry | Claim confirmed |
| --- | --- | --- |
| 基 | き 2182840 | chemistry group; counter for installed objects |
| 基 | もとい 2219600 | – |
| 基 | 基督 1042520 | ateji and rarely used kanji form; usually kana |
| 基 | 基因 | rarely used form of 起因 (1223720) |
| 基 / 素 | もと 1260670 | senses 5 and 6 restricted to 元; counters restricted to 本; 素 and 基 are listed spellings |
| 素 | す 2069220 | – |
| 素 | そ 1621290 | white silk; prime; principle |
| 素 | 素より | rarely used form of 元より |
| 素 | 素直 | sense set |
| 縮 | 縮む 1337560 | ちじむ variant |
| 縮 | 縮緬 1337650 | usually kana |
| 縮 | 恐縮 1236740 | including the archaic sense |
| 統 | 統べる 1449660 | 総べる a rarely used form |
| 激 | 急劇, 劇しい, 劇痛 | rarely used forms |
| 激 | 刺戟 | rarely used form |
| 激 | 激する 2247700 | "to intensify" |
| 激 | 激 げき 2670200 | prefix |
| 仮 | 虚仮 1776150 | usually kana |
| 仮 | 仮 け 1187280 | Buddhist term |
| 仮 | 仮寝 | – |
| 仮 | 仮名 かな / かめい | – |
| 嫌 | いや 1587610 | interjection usually kana |
| 嫌 | 嫌い 1257240 | – |
| 価 | か 2827787 | valence |
| 価 | あたい 1581630 | spellings 値 and 価 |
| 価 | (whole family) | no word reads 価 as ケ (繭価 けんか is 繭けん + 価か) |
| 騒 | (whole family) | no word reads 騒 as うれい |
| 騒 | 潮騒 1428700 | – |
| 級 | 級 1919590 | – |
| 級 | 級長 1230150 | dated term |
| 級 | 級の木 in しなのき 1950420 | usually kana |
| 暖 | 暖気 のんき | rarely used kanji form of 呑気 1600560; usually kana |
| 暖 | 暖簾 1419890 | usually kana |
| 暖 | 暖か 2081300 | also written 温か |
| 器 | 器 き 2109010 / うつわ 1218880 | – |
| 器 | 大器 | – |
| 応 | 応える 1179810 | – |

**Online JMdict (Jisho)**

- 応 まさに: JMdict gives 正に (1376640; its sense notes say "also written as 将に" and "as まさに...べき; also written as 当に") plus separate entries 当に and 将に. The card's claim at 応.md:36 is therefore correct.

**級 Notes, line 46**

- 吸, 扱 and 給 all have the on reading キュウ: 扱's metadata lists `[ソウ, キュウ]` in `repo\kanji\扱.md`.

**Quiz readings**

- Every quizOnyomi and quizKunyomi value has a Readings row with a linked word article.
- Unselected readings are explained in their rows: 嫌 ケン (no 嫌悪 or 嫌疑 article yet), 応 こた.える, 整 ととの.える, and others.
- Word-title coverage: the 93 modified word articles are exactly the repo words containing the 15 kanji, and each card links its words.

### Word-article diffs (93)

- **88 diffs:** a single changed line that becomes the old line exactly once the one new link is unwrapped. Each new link has the label `X` and target `../kanji/X.md`, where X is a batch kanji contained in that word's title. In each, the link is the first bare mention in its "How the kanji combine" passage.
- **仮名遣い, 好き嫌い, 片仮名:** these are also pure single link-wraps. The kanji appeared earlier only inside an existing word link ([仮名](仮名.md), [嫌い](嫌い.md)), so the new link is the first bare mention. This is acceptable; see optional O4 for 仮名遣い.
- **整備:** two lines change. The 整 link-wrap, and "Read セイ + ビ; 整 has no card here, but remains part of the spelling and metadata." becomes "Read セイ + ビ." The passage still reads correctly.
- **物騒:** one line. The 騒 link-wrap, plus removal of "騒 has no card yet." The passage still reads correctly.
- Nothing else changed in any diff. Every diff has a single hunk, and no Dictionary: line or front matter is touched.

## Findings

### F1. 器 mnemonic describes a component the modern character does not have (major)

- **Facets:** 1 (correctness), 4 (comprehensibility)
- **Location:** `snapshot\kanji\器.md:25`
- **Claim on the card:** "find four 口 … around a centre shape that resembles [犬](犬.md), 'dog.' Imagine four mouths crowded around a dog's food bowl…"
- **Problem:** the modern standard (Joyo) 器 has 大 in the centre, with no dot; its 15 strokes are four 口 (12) plus 大 (3).
  - The packet's own `snapshot\strokes\器.json` has `strokeCount: 15`, and its centre strokes are 一, ノ, ㇏, which is 大.
  - The 犬-centred shape is the traditional 16-stroke form (CJK compatibility U+FA38 器).
- **Why it matters:** the card calls this a "modern-shape mnemonic", but the shape described is not the modern shape. A learner told to look for a dog will not find the dot, and the image teaches the wrong glyph. The link to 犬 reinforces the error. This breaks the rule that component statements must be true.
- **Remedy:** describe the centre as [大](大.md), "big", and rebuild the image (for example, four mouths around one big serving vessel). Keep the "memory aid only" disclaimer, change "口 or 犬" to "口 or 大", and replace the link.
- **Confidence:** high.

### F2. 価 readings paragraph wrongly says 価 supplies both か syllables of かかく (minor)

- **Facets:** 1, 4
- **Location:** `snapshot\kanji\価.md:35`
- **Claim on the card:** "In 価格, 格 supplies カク, so 価 is か in both syllables of かかく."
- **Problem:** 価格 かかく is 価 = か + 格 = かく. 価 supplies only the first か. The sentence contradicts its own first clause and would confuse a beginner about the reading split.
- **Remedy:** "In 価格, 価 supplies the first か and 格 supplies カク."
- **Confidence:** high.

### F3. 激 mnemonic misplaces 放 (minor)

- **Facet:** 1 (component statement)
- **Location:** `snapshot\kanji\激.md:25`
- **Claim on the card:** "氵 … at the left, 白 … at the top right and [放](放.md) … below it."
- **Problem:** in modern 激, the right part is 敫: 白 sits over 方 in the middle column, and 攵 stands at the far right at full height. Only 方 is below 白. 放 (方 + 攵) is not a unit "below" 白; its two halves are split by 白. A learner looking for 放 under 白 will not find it.
- **Remedy:** for example, "氵 at the left, 白 over 方 in the middle, and 攵 at the far right (方 and 攵 together make 放, 'release')". The image can stay. Keep the disclaimer.
- **Confidence:** moderate-high.

### F4. 応 paragraph denies that ヨウ is a reading of 応, contradicting its own table (minor)

- **Facets:** 1, 4
- **Location:** `snapshot\kanji\応.md:38`
- **Claim on the card:** "In 応用, 用 supplies ヨウ, which is why ヨウ appears in the word without being a reading of 応."
- **Problem:** the same card has a ヨウ row (KANJIDIC2 lists ヨウ as an on reading). Later in the same paragraph it says "KANJIDIC2 and the Daijisen character entry list ヨウ, the 漢 reading". The Daijisen extract confirms ヨウ（漢）. The intended point is that the ヨウ in 応用 belongs to 用, but as written the clause states a falsehood about 応.
- **Remedy:** "In 応用, 用 supplies ヨウ; 応 itself is read オウ here, even though ヨウ is also listed as a rare on reading of 応."
- **Confidence:** high.

### F5. 嫌 quiz: 怪 "suspicious; uncanny" is a "suspicion" confusable but is not excluded (minor)

- **Facet:** 3 (quiz safety and consistency)
- **Location:** `snapshot\kanji\嫌.md:14` (`quiz_exclusions: [憎, 疑]`) and Notes line 51.
- **Problem:** 嫌's title is "dislike; suspicion". The card excludes 疑 ("doubt; suspect") precisely because it "overlaps the Daijisen sense of suspecting". 怪 has the title "suspicious; uncanny" (`titles\kanji-titles.tsv:445`) and is also JLPT N1 (as is 嫌, line 329), so it can appear in the same pool.
  - With 嫌 as the prompt, an option "suspicious; uncanny" is a near-synonym trap for "suspicion".
  - With 怪 as the prompt, "dislike; suspicion" is a defensible-looking wrong answer.
  - The card applies its exclusion rationale to 疑 but not to the equally direct 怪 overlap.
- **Remedy:** add 怪 to 嫌's `quiz_exclusions` (and the reciprocal on 怪 if the project requires reciprocity), and mention it in the Notes exclusion sentence. Alternatively, record why 怪 is safe.
- **Confidence:** moderate. It depends on whether the distractor sampler can draw 怪 for 嫌; the simulation lines I could see do not settle it.

## Optional

- **O1 (素, coverage polish):** the ス row and paragraph do not mention the two most frequent everyday ス words, 素晴らしい すばらしい and 素敵 すてき (neither has a repo word article). A one-line unlinked mention would help an N5–N4 reader recognise ス in words they already know. It is not required by the scoped-coverage rule.
- **O2 (嫌, wording):** "in some older compounds suspecting it" (嫌.md:23). 嫌疑 is current formal and legal vocabulary, not old, so "in some formal compounds" is more accurate.
- **O3 (縮.md:52, 騒.md:50, wording):** "It is read as a whole word, with 縮 as ちり" and "with 騒 as さい" both say whole-word and then split the word. Suggest "an irregular reading: 縮 is read ちり only in this word" (and likewise for 騒 さい).
- **O4 (diff `words\仮名遣い.md`):** the new link sits inside "the contracted [仮](../kanji/仮.md)名 unit". It renders as a link on half of a unit that the sentence says to learn whole. It is harmless, but the link could go on the first standalone mention instead, or the sentence could be left unlinked there.
- **O5 (応.md:36):** the まさに row could add that JMdict marks まさに as usually written in kana, so a learner does not expect 応に.
- **O6 (trivial glosses):**
  - The 整 paragraph says "maintenance or putting in place", while the 整備 title is "maintenance; putting in order".
  - The 嫌 table glosses 嫌い "disliked; dislike", while JMdict sense 1 is "disliking; hating; detesting". Aligning these is optional.

## Limits

- **Joyo table (2010) PDF:** the bunka.go.jp PDF returned compressed binary that I could not read as text, and no text mirror was available (the Wikisource URL I tried returned 404).
  - The following are therefore UNVERIFIED, though plausible and consistent with my background knowledge: each card's claims about the table's example words, the "⇔" contrast notation (張/貼, 応える/答える, 基 もと ⇔ 下/元/本, 価/値, 暖か/温か, 整/調) and the remarks-column items (応 反応/順応 ハンノウ/ジュンノウ; 素 素人; 仮 仮名).
  - joyokanji.info (the 2014 異字同訓 report) independently confirms that こたえる（応・答） is an official 異字同訓 pair.
  - I did not count these as defects.
- **Quiz simulation:** `mechanical-checks.md` is truncated at the beginning of the simulation section (it starts mid-word, "ptions from distractors…"). I could not see the displayed options for 張, 器 and 素. For those three, facet 3 is judged from the front-matter distractors and quiz_exclusions against `kanji-titles.tsv`, not from displayed options.
- **Version differences:** JMdict checks used the pinned families file. Where a card's claim depends on entries outside the family file (まさに 当に and 将に), I used live JMdict through Jisho; minor version drift is possible.
- **Example sentences:** I checked each card's example sentences (grammar, kana, naturalness, translation) once while reading the cards in full and found no defects. They were not re-checked against external corpora.
- **Out of scope:** I did not inspect the stroke path geometry beyond 器 and the stroke counts. I did not open `rubric\agents\*.agent.md`, the remainder of `content-format.md` (lines 191–1419), or repo word articles beyond the diffs.
- **Assumption:** headings and section order were judged against the convention shared by all 15 cards and the existing corpus (`## Meaning and origin`, `## Readings`, `## Common words`, `## Notes`, then metadata and evidence lines), because content-format.md lines 1–190 do not spell out kanji body headings.
