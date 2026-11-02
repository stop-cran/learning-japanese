# N1 kanji pilot: independent initial content review

**Snapshot:** 6855b42fa2c4e4cae6fd01a2697d10ee42011abb. The packet index reports `uncommittedTeaching: false`, and the baseline is 57dcc2aaedd8d6b0f141d5b4c3cb9c13f6f797b2. I did not recompute the packet hashes.

## Scope

- **Reviewer:** Claude Opus 5.5 (claude-opus-5.5). This was a read-only review, with tools used one at a time.
- **Facets reviewed:**
  - All three facets (correctness, scoped coverage and phone comprehensibility) for:
    - the 12 new kanji articles (幹 氏 扱 乃 凹 凸 矛 鷹 彗 漱 栞 莉);
    - the 5 new word articles (乃至 彗星 栞 茉莉花 鷹).
  - The changed passages only, read with their complete bodies, for: うがい, でこぼこ, 凹む, 扱う, 新幹線, 氏, 氏名, 矛盾.
- **Packets read in full, each once, none truncated:**
  - packet-index.json
  - teaching-01 to teaching-05
  - reused-passages.diff
  - dictionary-01 to dictionary-04 (all 56 families)
  - comparisons-01 and comparisons-02
  - metadata-and-offered-keys.json (whole file)
  - external-observations.json
- **One read outside the packets:** a grep of the frontmatter of `words/星.md` in the working tree. It returned `title: star` and no `quiz_exclusions` line. I read it because 彗星.md L27 links to it but it was not in the comparison set. This is working-tree evidence, not an export of the snapshot.
- **Not read:** progress files, ledgers, the draft audit, author notes and other reviews. I made no web fetches.

## Verdicts

Format: correctness / scoped coverage / comprehensibility.

| File | Verdict |
| --- | --- |
| kanji/幹 | CLEAN / CLEAN / CLEAN |
| kanji/氏 | CLEAN / CLEAN / CLEAN |
| kanji/扱 | CLEAN / CLEAN / CLEAN |
| kanji/乃 | CLEAN / CLEAN / CLEAN |
| kanji/凹 | CLEAN / CLEAN / CLEAN |
| kanji/凸 | CLEAN / CLEAN / CLEAN |
| kanji/矛 | CLEAN / CLEAN / CLEAN |
| kanji/鷹 | CLEAN / CLEAN / CLEAN |
| kanji/彗 | CLEAN / CLEAN / CLEAN |
| kanji/漱 | CLEAN / CLEAN / CLEAN |
| kanji/栞 | CLEAN / CLEAN / CLEAN |
| kanji/莉 | CLEAN / CLEAN / CLEAN |
| words/乃至 | CLEAN / **UNVERIFIED** (F1) / CLEAN |
| words/彗星 | CLEAN / CLEAN / CLEAN |
| words/栞 | CLEAN / CLEAN / CLEAN |
| words/茉莉花 | CLEAN / CLEAN / CLEAN |
| words/鷹 | CLEAN / CLEAN / CLEAN |

Changed-passage scope (each reviews only the new link or sentence and how it fits the article):

| File | Change | Verdict |
| --- | --- | --- |
| words/うがい | L24 | CLEAN / CLEAN / CLEAN |
| words/でこぼこ | L15 | CLEAN / CLEAN / CLEAN |
| words/凹む | L25 | CLEAN / CLEAN / CLEAN |
| words/扱う | L24 | CLEAN / CLEAN / CLEAN |
| words/新幹線 | L28 | CLEAN / CLEAN / CLEAN |
| words/氏 | L28 | CLEAN / CLEAN / CLEAN |
| words/氏名 | L27 | CLEAN / CLEAN / CLEAN |
| words/矛盾 | L28 | CLEAN / CLEAN / CLEAN |

The reading-key suitability is a separate verdict. It is **NEEDS a companion prerequisite under issue #1** (see R1), not a text defect.

## What the checks confirmed

- **Metadata matches the source.** Frontmatter on/kun lists, the order of the reading-table rows, stroke counts, radicals, radical numbers and grade tags all match the frozen KANJIDIC2 data for all 12 kanji.
- **Every reading row is covered.** Each on/kun row has either a JMdict- or Kanjipedia-backed word example or a clearly marked source-only disclosure. Examples:
  - 扱 ソウ/キュウ/あつか.る
  - 乃 ノ/アイ
  - 矛 ボウ
  - 彗 エ/ケイ/セイ
  - 漱 シュウ/ス/くちそそ.ぐ
  - 栞 カン
  - 莉 ライ/レイ
- **Dictionary flags are represented correctly.** Usual-kana, rare, search-only, restriction, colloquial and dated labels match the families. Examples:
  - 1469800 乃 search-only
  - 1404100 乃ち rare
  - 1582410 restricts sense 2 to でこぼこ
  - 1254510 穴凹 search-only
  - 1415510 and 1568040 usually written in kana
  - 1577660 漱 rare
  - 2826358 おれ is a special (gikun) reading
  - 1608970 ようよう is restricted to 鷹揚
- **The older 氏 suffix reading is supported.** 山田氏 やまだうじ is backed by the coordinator's Kotobank observations (精選版 日本国語大辞典 [2] and Nipponica).
- **Okurigana boundaries are supported.** The 漱ぐ くちすす-ぐ / すす-ぐ split is backed by the Kanjipedia navigation headings.
- **Shape mnemonics are labelled as non-etymology everywhere.** No origin claims are made.
- **Links are reciprocal** between every kanji and its supporting words, including all eight reused articles.
- **Distractors work.** Each new kanji has three distractors with clearly wrong meanings. The 凹/凸 antonym pair is defensibly wrong.
- **Word quiz exclusions are sound in the forward direction.** Superordinate words are excluded: 鳥 for 鷹, 花 for 茉莉花, and 本/書物/図書/冊子 for 栞. Leaving 星 ("star") out of 彗星's exclusions is defensible, because a comet is not a star in English and the article says so (L23, L27).
- **Examples are natural and translated.**

## Findings

### F1: Reverse-direction quiz ambiguity for 乃至

- **Severity:** consequential but unverified, not a demonstrated defect.
- **Facet:** scoped coverage.
- **Location:** words/乃至.md L4, L8, read against words/または.md L4, あるいは.md L4/L9 and それとも.md L4/L9.
- **Claim:**
  - 乃至 correctly excludes または, あるいは and それとも.
  - However, 乃至's title "from ... to; or" contains "or". If the app applies `quiz_exclusions` only one way, a または/あるいは/それとも prompt could show "from ... to; or" as a "wrong" option, and that option is arguably correct (JMdict 1469810 sense 2 "or"; 1524990, 1586850 and 1007010 "or").
  - A weaker version exists for 冊子 (1298530 "booklet; pamphlet") against 栞 "guidebook" (1568040 sense 2).
- **Existing evidence points both ways:** あるいは and それとも exclude または, but または has no exclusions. That suggests either symmetric application or existing tolerance of this overlap.
- **Remedy:**
  1. Confirm whether exclusions are applied symmetrically.
  2. If they are not, add 乃至 to the exclusions of または, あるいは and それとも as a narrow companion change. Optionally do the same for 冊子 with 栞.
- **Confidence:** medium.

### R1: Several offered reading keys are source-only

This is a reading-compatibility issue, separate from text correctness.

- **Location:** metadata-and-offered-keys.json, projection section.
- **The keys are valid character-dictionary recognition data** (KANJIDIC2, plus Kanjipedia where cited). Each card's teaching also discloses them as source-only.
- **They are unsuitable as study prompts.** These keys have no lexical example and are disclosed as source-only:
  - 扱 on そう, きゅう (both of its on keys)
  - 乃 on の
  - 彗 on え, けい
  - 漱 on しゅう, す
  - 漱 kun くちそそぐ
  - 矛 on ぼう
  - 栞 on かん (its only on key)
  - 莉 on らい, れい
- **乃 has a duplicate key:** の appears as both an on key and a kun key, so a reading prompt can't tell them apart (乃.md L36 acknowledges this).
- **The first-three cutoff swaps a supported reading for an unsupported one:**
  - 漱 drops すす.ぐ, which has a lexical example (JMdict 2827411; 漱.md L34), and keeps the source-only くちそそぐ.
  - 乃 drops アイ and 彗 drops セイ. Both drops are harmless.
- **乃 kun なんじ** is backed only by a Kanjipedia character gloss. It is defensible for recognition but weak as a study prompt.
- **Remedy:** a narrow companion prerequisite under content issue #1 (curated reading work). It should be a per-card curated study-key designation that leaves metadata order and identity untouched and excludes source-only keys from quiz prompting. This review is not the place to extend the content task to implement it.
- **Still to decide:** whether the pilot accepts source-only keys as quiz prompts. Nothing in the inputs settles that.
- **Confidence:** high on the facts. The acceptability call belongs to the owner.

No demonstrated correctness defects were found.

## Optional polish (none blocking)

- **彗.md L32:** link [箒](../words/箒.md), since the article already recommends that spelling.
- **漱.md:** add 夏目漱石 (なつめそうせき) as the most familiar place learners meet ソウ. Optionally add ゆすぐ, which JMdict 2827411 also records.
- **彗星.md L31:** name the homophone 水星 (すいせい, "Mercury") explicitly.
- **扱.md L45:** the sentence about しごく not establishing あつか.る reads oddly. Consider removing it.
- **Meta wording aimed at authors rather than learners:**
  - "source-only" and "search-only" are not glossed for learners in most cards.
  - The wording "preserved KANJIDIC2 reading list" (幹.md L41) is meta.
  - The wording "retains its primary でこぼこ identity" (凸.md L39) is meta.
- **幹.md L40:** the contrast notes don't mention the 草 distractor.
- **栞 quiz exclusions:** 案内 ("guidance") is not excluded. That is defensible, because guidance is not a guidebook (1154860 has no guidebook sense), but it is a borderline pair.

## Limits

- **Unverified claims:**
  - Whether the app applies quiz exclusions symmetrically (F1).
  - The "kanbun usage" wording for 乃 なんじ (乃.md L34). The dedicated Kanjipedia page returned only copyright text.
  - The exact phrase 稲を扱く. Only a paraphrase of a rice-stripping example is supplied.
  - Whether link targets such as 姓.md and 至.md exist, and how frontmatter `kanji: [茉, …]` behaves without a 茉 article. I didn't check either.
- **Dictionary access:** I relied on the coordinator's paraphrases for Kanjipedia and Kotobank and fetched nothing myself. The supplied JMdict families are complete. The 星 check used working-tree frontmatter, not an export.
- **No phone, device or native-speaker evidence:**
  - This was a text-only comprehensibility review.
  - Long three-column tables could be hard to read on a phone, but I could not test that.
  - Native app selection, sessions, article display, Back navigation, drawing and acceptance across all 40 fonts were not assessed.
- **Overall scope:** CLEAN means no actionable defect was established within the assigned scope. It does not certify exhaustive correctness, and it does not treat the source list as an official JLPT syllabus.