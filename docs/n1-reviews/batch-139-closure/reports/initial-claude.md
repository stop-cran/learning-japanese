# Batch 139 blind review: first reviewer (Claude)

## Snapshot

- Reviewer model: Claude (Anthropic), working as an independent, read-only, blind first reviewer.
- Commit: a47efe9af926316eaa86656033bf6e109f2be697 (batch 139).
- Kanji cards: 嫁 嬢 宗 宜 宣 宴 寂 密 審 尋 屈 属 岬 峠 崩.
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-139-a47efe9a`. I did not recompute the manifest sha256; I took 95f5b71e… from the brief.

## Scope

Under review:

- the 15 new cards in `snapshot\kanji\`;
- the 15 stroke files in `snapshot\strokes\`;
- the 20 modified word articles, which I reviewed through `diffs\`.

Packet files I opened:

- `INSTRUCTIONS.md`: in full.
- `mechanical-checks.md`: in full.
- Top-level packet listing (not recursive).
- `evidence\source-metadata.json`: in full.
- `evidence\joyo-pages.md`: in full (pp. 2, 3, 16, 21, 34, 42, 71, 73, 83, 86, 87, 94, 101, 120, 141, 145).
- `evidence\daijisen-heads.txt`: in full.
- `evidence\kanjipedia-outside-readings.json`: in full.
- `evidence\okurigana-scan.txt`: in full.
- `evidence\public-source\weblio-<k>.txt` for all 15 kanji: in full. These are short extracts. The 岬 extract holds no Daijisen block; see Limits.
- `evidence\jmdict-families.xml`: in part. I extracted by ent_seq every entry id cited in the Metadata lines of all 15 cards, plus a few more (2842102, 2835838, 1360430, and searches for さむしい and みそか).
- `evidence\jmdict-digest.tsv`: in part (the header and the 嫁 rows).
- `evidence\kanjidic2-records.xml`: in part (the records for 岬 峠 崩 属 審 尋 屈 密). For the other seven cards I compared the front matter with `source-metadata.json` only.
- `evidence\audits\reading-exposure.txt`: in part (first 40 lines, the key summary lines, and the 宗, 寂 and 岬 sections).
- `evidence\audits\word-remarks.json`: in full.
- `evidence\audits\reading-options.txt` and `evidence\audits\quiz-safety.txt`: not opened directly. I used their tails as reproduced in `mechanical-checks.md`.
- `snapshot\kanji\*.md`: all 15, in full, with line numbers.
- `snapshot\strokes\*.json`: all 15, parsed in full by script. I checked the kanji, strokeCount, the length of the strokes array, ids 1..n, 16 points per stroke, the source revision, and agreement with each card's `strokes:`.
- `snapshot\words\宴会.md`: in part (lines 24–34). I reviewed the other 19 word articles through their diffs only.
- `diffs\*.diff`: all 20. I read the changed and hunk lines of each, and the 宴会 diff in full.
- `titles\kanji-titles.tsv`: in part (lookups of specific kanji, and the line count).
- `repo\docs\content-format.md`: in part (lines 71–138, the kanji-card and quiz-authoring rules, plus a heading grep).
- `repo\kanji\具.md` and `repo\kanji\押.md`: in part (front matter).
- `evidence\app-code\` and `evidence\audits\kanji_remarks.py`: not opened.

Public sources:

- I fetched the live Weblio page for 岬 (https://www.weblio.jp/content/岬), first 5,000 characters only. It showed the 実用日本語表現辞典 block, not the Daijisen character block.
- Otherwise my public-dictionary check rests on the packet's archived JMdict, KANJIDIC2 and Digital Daijisen (Weblio) extracts, which I read entry by entry.

## Verdicts

The verdicts are the same for every card except where noted.

| Facet | Overall | Per-card differences |
| --- | --- | --- |
| 1. Correctness | PASS with minor findings | 宣: C1 (register of のたまう). 嫁: C2 (dialect tag on the "wife" sense). 岬: PASS, but one Daijisen character-entry claim is unverified (see Limits). |
| 2. Scoped coverage | PASS | 嬢: optional O1. 宣: optional O2. |
| 3. Consistency and quiz safety | PASS | none |
| 4. Comprehensibility | PASS | none |

The stroke files are CLEAN. All 15 match their cards.

The 20 word diffs are CLEAN:

- Each one wraps exactly the first plain mention of the new kanji in a link to `../kanji/<k>.md`, and every target is one of the 15 new cards.
- 秘密 links only 密; 秘 stays plain and has no card (it is absent from `kanji-titles.tsv`).
- The four remark edits match `word-remarks.json` exactly. In 宴会, 崩す and 崩れる the deleted sentence is now false, because the card exists.
- 附属's "附 has no card yet." is true: 附 is absent from `kanji-titles.tsv`.
- 附属's rewritten line now links 属, and the surrounding sentences still read correctly.

### Per-card checks

All front matter matches the metadata. Every quoted JMdict gloss, Joyo row and example I traced is exact.

- **嫁**:
  - Front matter matches; the Joyo p.21 and Daijisen claims hold.
  - 嫁ぐ (dated), 再嫁 (formal or literary) and 許嫁 (gikun) are correct.
  - Distractors 好 妨 姓 and exclusions 妻 婦 婚 are sound.
  - Mnemonic: 女 + 家 = 13 strokes, true.
- **嬢**:
  - ジョウ only in the Joyo table (令嬢, 愛嬢, お嬢さん); the むすめ row is correctly marked outside the table.
  - 御嬢さん is a search-only spelling, as stated.
  - Distractors 娯 妙 始 are sound.
- **宗**:
  - Joyo p.73 (シュウ, ソウ) and Daijisen (シュウ marked 慣, ソウ marked 漢; むね, たっとぶ) are correct.
  - The むね row correctly says JMdict writes 旨 first.
  - Mnemonic: 宀 + 示 = 8 strokes, true.
  - Exclusions 主 祖 are defensible: 宗主 and 祖宗.
- **宜**:
  - Only ギ is in the Joyo table.
  - よろしい and よろしく are usually written in kana in JMdict.
  - むべ and うべ are archaic.
  - 宜い is a rare spelling of よい.
  - The title "suitable; proper; good" is fine.
  - Distractors 且 組 査 are look-alikes and defensibly wrong.
- **宴**:
  - Joyo p.16, うたげ (poetical) and えん (formal or literary) are all correct.
  - Exclusions are reasonable; 党 shares the English word "party".
- **寂**:
  - Joyo p.71 shows ジャク, セキ, さび, さびしい and さびれる.
  - 寂然 has both readings, and its second sense is restricted to じゃくねん.
  - 寂しい is read さびしい or さみしい. さむしい is a Daijisen ▽ headword only; JMdict has no さむしい, which matches the card.
- **密**:
  - The four Daijisen senses and examples are exact.
  - JMdict 1612520 密か has only ひそか, so "no entry for みそか spelled 密か" is true. 秘か and 窃か are listed, and 密やか is "quiet; still; surreptitious."
  - The みっ assimilation examples are correct.
  - 秘 has no card.
  - Mnemonic: 宀 + 必 + 山 = 11 strokes.
- **審**:
  - Every gloss of the 18 cited JMdict entries is exact. That includes つまびらか: listed after 詳らか, usually kana, obsolete kana つばひらか. It also includes つぶさに, spelled 具に and in other ways but not with 審.
  - 具's card does carry つぶさ.に.
  - Mnemonic: 宀 + 番 = 15 strokes, and 番 = 釆 + 田, true.
- **尋**:
  - Daijisen gives four senses (尋訪 is the compound absent from JMdict), and its ひろ headword gives 5 or 6 shaku (1.515 m or 1.816 m), as the card says.
  - 千尋 is せんじん, with ちひろ restricted to that spelling.
  - The Joyo rows and the ⇔ 訪ねる comparison are correct.
  - Mnemonic: ヨ + 工 + 口 + 寸 = 12 strokes.
- **屈**:
  - The four Daijisen senses are correct. 屈強 is also written 倔強 (rare).
  - かがまる comes from Daijisen and is absent from KANJIDIC2.
  - こごむ and くぐむ (obsolete kana) for 屈む, and こごめる for 屈める, are correct.
  - The Joyo examples are exact.
  - Mnemonic: 尸 + 出 = 8 strokes.
- **属**:
  - On ショク: Daijisen marks ゾク 呉 and ショク 漢. The ショク senses with 属文, 属望 and 属目 are correct, and the note that the second sense is interchangeable with 嘱 is right.
  - 属する しょくする is a separate formal or literary entry, 2410030, with 嘱する first.
  - On さかん: 雅楽属 うたのさかん carries the historical tag. Daijisen word sense 3 gives 主典(さかん), and JMdict 2249730 marks 主典 さかん archaic.
  - On つく and やから: neither is in Daijisen or JMdict with 属, and both are correctly marked "source-only here". 輩 is derogatory and 族 poetical.
  - Grade 5 matches both KANJIDIC2 and Daijisen.
- **岬**:
  - さき is a KANJIDIC2 nanori. JMdict 1297220 さき lists 崎 first and 岬 second, and Daijisen さき【崎／▽岬／▽埼】 matches the ▽ claim.
  - 岬角 (rare; the anatomy sense) and 岬湾 (rare) are correct.
  - The Notes shape comparisons are true: the right part of 岬 is 田 with its middle vertical extended below, and 押 has the same right part.
  - Distractors 山 田 中 are look-alikes and defensibly wrong.
- **峠**:
  - It is a kokuji according to both KANJIDIC2 and Daijisen's [補説].
  - The Daijisen origin (a sound change of たむけ, because travellers made offerings to 道祖神) is reported as Daijisen's account, not as the card's own claim.
  - Both Daijisen senses and the example sentence are exact.
  - The title "mountain pass; peak; climax" matches KANJIDIC2 and JMdict sense 2. "Peak" is not exclusive, and 頂 is correctly excluded.
  - Mnemonic: 山 + 上 + 下 = 9 strokes.
- **崩**:
  - The -くず.れ suffix row (山崩れ やまくずれ, with no rendaku) is correct, and so are 崩れ (1640640), 総崩れ and 値崩れ.
  - 潰崩 is archaic and listed after 壊崩. 崩御 is honorific.
  - 雪崩 is gikun or jukujikun, and is a special reading on Joyo p.141.
  - Mnemonic: 山 + two 月 = 11 strokes.

Facet 3:

- Every quizOnyomi or quizKunyomi reading has a table row with a linked word.
- The titles are unique.
- Every distractor and exclusion target exists in `kanji-titles.tsv`.
- The exclusions are direct pairs grounded in shared displayed senses or co-occurring compounds. Some are broad: 員 and 般 for 属, 均 and 替 for 崩, 私 for 密, 旬 and 経 for 峠. They only shrink the pool, and none creates a hazard.
- Sections and headings follow `content-format.md`.

## Findings

Established defects. Both are minor; I found nothing blocking.

### C1: 宣, the のたまう register is incomplete

- **Severity:** minor.
- **Facet:** 1 (correctness: register) and 4.
- **Location:** `snapshot\kanji\宣.md:40`.
- **Claim and impact:** The のたま.う row glosses 宣う as "to say; to be pleased to say (honorific; usually written in kana)". JMdict entry 2842102 adds that it was originally respectful language but is nowadays often used sarcastically. Without that note, a learner may think のたまう is a usable polite verb, when in modern use it is usually ironic ("deigns to say", "has the gall to say").
- **Remedy:** append "originally respectful; now often used sarcastically" to the row.
- **Evidence:** `evidence\jmdict-families.xml`, entry 2842102.
- **Confidence:** high.

### C2: 嫁, the dialect tag on the "wife" sense is omitted

- **Severity:** minor.
- **Facet:** 1 (correctness: register).
- **Location:** `snapshot\kanji\嫁.md:23`.
- **Claim and impact:** "its third sense is 'wife.'" In JMdict's 嫁 よめ entry that third sense is tagged Kansai-ben. The card mentions the register tags of the other words in the same paragraph (dated, formal or literary, gikun), so leaving this one out makes "wife" look like an unmarked standard sense. The usage うちの嫁 is widespread but still regionally marked or contested.
- **Remedy:** "its third sense, which JMdict marks as Kansai dialect, is 'wife.'"
- **Evidence:** the `evidence\jmdict-families.xml` entry for 嫁 よめ, which the card cites.
- **Confidence:** high on the tag. Its pedagogical weight is moderate.

## Optional

These are polish suggestions, not defects.

- **O1 (嬢, coverage):** consider one Notes line on お嬢様 おじょうさま and 嬢ちゃん じょうちゃん, and on 嬢さん, which JMdict also reads とうさん as a Kansai honorific. These are frequent learner-facing forms; the card covers only お嬢さん, 令嬢, 愛嬢 and a few others.
- **O2 (宣, coverage):** `宣.md:31` says "only のたまう is a KANJIDIC2 reading" without naming the other Daijisen kun readings (のべる and のる). Naming them, with the note that JMdict has 宣べる only as a rare spelling, would make the sentence self-contained.
- **O3 (宴会 word article, pre-existing wording):** lines 31–33 now end "The first character specifies the kind of gathering: エン + カイ." The colon makes the readings look like the "kind of gathering". This wording predates the batch (the diff only removed the following sentence), so it is not a defect of this batch. A small rewrite would help: "…the kind of gathering. The on readings are エン + カイ."
- **O4 (峠 title):** "peak" may suggest a summit to some learners. It is sourced from KANJIDIC2 and JMdict sense 2, and 頂 is excluded, so it is acceptable. "pass; crisis point" would be an alternative if the title is ever revisited.

## Limits

- **Reviewer conduct.** I am Claude. I made exactly one tool call per response, as far as I know; I am not aware of any response with more than one. I used no sub-agents or background jobs, and I did not look for the other reviewer's report or the author's rationale.
- **Not run.** Android JVM tests and the Kotlin cross-check were not run at this snapshot. That is a known limit of the packet, and I do not report it.
- **Spilled tool output.** The harness saved two tool outputs to temp files on its own: my stroke-file listing and the second page of the live Weblio fetch. I did not open those files. I re-ran the stroke check in compact form instead.
- **岬's Daijisen character entry is unverified.** The packet's Weblio extract and my first live fetch show only the 実用日本語表現辞典 block. So I could not verify three claims: that the character entry has one sense (みさき), that its example is 岬角, and the card's description of the Daijisen word entry みさき. The heads file does confirm the headwords こう【▽岬】, さき【崎／▽岬／▽埼】 and みさき, so I treat these claims as plausible but unverified.
- **KANJIDIC2 for seven cards.** For 嫁, 嬢, 宗, 宜, 宣, 宴 and 寂 I checked the front matter against `source-metadata.json` and did not reopen `kanjidic2-records.xml`.
- **Quoted glosses for kanji without cards.** I assumed that 秘 "secret" (`密.md`) and similar glosses come from KANJIDIC2 meanings, which are not in the packet's records for those kanji.
- **Reading-audit leads, latent only.**
  - 宗 し: a KANJIDIC2 name-only reading. Drawing it on the シュウ prompt is harmless, because it is never a correct answer and is a real reading of the character, so it is not a defect.
  - 岬 さき offered by 先: the reading-options label HIT is latent. The curated 山 田 中 fill every distractor slot in every shipped pool.
  - The other "attested reading … offered by" collisions: I did not examine each line. The audit counts 11 latent collisions and 0 production or padded-session hits, and I accepted that count.
- **"Card text" provenance labels.** I assumed that "card text" in the audit's provenance labels means the --extra input source, not the card prose.
- **Live public dictionaries.** Apart from the one Weblio fetch, I did not check the live Jisho, Kotobank or Kanjipedia sites. My dictionary verification uses the archived JMdict, KANJIDIC2 and Daijisen extracts in the packet, which I read entry by entry.
