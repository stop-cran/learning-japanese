# Batch 110 confirmation review (Claude)

## Snapshot

- Revised snapshot: commit 10d7965266b69ed81703ab69f20cff873a0526e9 (child of 453af714d56aa573204d477ff863cb4da756b4c3, the snapshot reviewed in round 1).
- Batch 110 kanji: 張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖. Changed word article: words\応援.md.
- Reviewer model: Claude Opus 5.5 (model ID claude-opus-5.5). Same reviewer as the round-1 report reports-110\initial-claude.md.

## Scope

Confirmation packet (`review-packets\confirm-110-10d79652-claude\`):

- INSTRUCTIONS.md, CHANGES.md and RESPONSE.md: read in full.
- Folder listings of the packet and its subfolders: non-recursive only.
- snapshot\kanji\ (all 15 revised cards): read in full.
- snapshot\words\応援.md: read in full.
- diffs\fix.patch: not read directly. Instead I compared all 15 old cards (original packet snapshot\kanji) with the 15 new cards using a token-level script diff. That diff covers the same hunks.
- diffs\changed-lines.txt: not opened.
- evidence\README.md: read in full.
- evidence\joyo\p*.txt (all 14 page extracts): read in full.
- evidence\joyo-p33-utsuwa-pair.png: viewed.
- evidence\joyo-p33-utsuwa.png: not opened.
- evidence\kanjivg\06fc0.svg (激): grep of stroke groups and element attributes only, so partial.
- evidence\kanjivg\05668.svg: not opened.
- evidence\jmdict-cited-entries.xml: read in full as a compact dump.
- evidence\QuizBuilder.kt and evidence\KanjiReadings.kt: read in full.
- evidence\Words.kt: only `ReadingOptions.mutations` and `closeness` (lines 226–251), so partial.
- checks\quiz-safety.txt and checks\reading-options.txt: read in full (reading-options.txt in three ranges).
- checks\link-targets.tsv, checks\lint.txt and checks\jvm*.txt: not opened. I rely on CHANGES.md's statement of 109 links with 0 mismatches, and on my own check that the changed hunks add no links except where stated.

Original packet (`review-packets\batch-110-453af714\`), read-only:

- snapshot\kanji\ (the 15 old cards): read in full by the diff script.
- snapshot\words\応援.md: lines 28–36 only.
- repo\kanji\募.md, 校.md, 料.md and 怪.md: front matter only.
- evidence\public-source\weblio-{暖,嫌,応,激,素,縮}.txt: grep of the 音/訓 lines only.

Other files:

- reports-110\initial-claude.md (my own round-1 report): used as the basis for the dispositions.

Public web: I made no new web lookups in this round. Reading and sense checks rest on the packet's JMdict, KANJIDIC2 and Joyo evidence, plus the public-dictionary checks I made in round 1. Every changed claim I verify below is backed by a packet evidence file.

## Dispositions

- **F1 — RESOLVED.**
  - 器.md:29 now describes the centre as 大 "with no dot", with the image of one big serving bowl. The disclaimer names 口 and 大, and the 犬 link is gone.
  - The new older-form paragraph, 器.md:27, matches Joyo p33: 器（器）, where the bracketed glyph is U+FA38. The pair crop shows the dot only in the bracketed glyph.
- **F2 — RESOLVED.** 価.md:37 now reads "In 価格, 価 is read か and 格 supplies カク." The rest of the paragraph is unchanged and correct.
- **F3 — RESOLVED.**
  - In 激.md:27, the component layout matches KanjiVG 06fc0: 氵 on the left, then 白 above 方, then 攵 on the right.
  - The modern-shape disclaimer covers 白, 方 and 放.
- **F4 — RESOLVED.**
  - 応.md:40 now reads "In 応用, 応 is read オウ and 用 supplies ヨウ."
  - It no longer contradicts the ヨウ row (34) or line 44.
- **F5 — RESOLVED.**
  - The new 嫌 exclusions are [憎, 疑, 怪].
  - 怪.md (title "suspicious; uncanny"; distractors [性, 経, 忙]) does not list 嫌. QuizBuilder `excluded()` is symmetric, so no exclusion is needed on that side.
  - 嫌 now shows the 兼, 験 and 好 titles. These are defensibly wrong in both directions.
  - The added note is accurate.
- **O1 — RESOLVED.**
  - 素.md:39 now marks 素敵 and 素晴らしい as ateji. That matches JMdict 1397350 and 1397300, both tagged ateji.
  - The glosses match, and both IDs were added to the metadata.
- **O2 — RESOLVED.** The text now says "in a few compounds", which is consistent with JMdict 1257320 嫌疑. That entry has no register tag.
- **O3 — RESOLVED.** 縮.md:56 and 騒.md:56 now say that ちり / さい "is not one of the readings above". This is accurate against the metadata.
- **O4 — DECLINE ACCEPTED.**
  - 仮名遣い.md has no stand-alone 仮 that needs a different link target. The existing link resolves to the correct card and is harmless.
  - I did not re-open the article in this round.
- **O5 — RESOLVED.** 応.md:38 now states that まさに is usually written in kana. JMdict 1376640 正に, 2856503 将に and 2856504 当に all carry "usually written using kana alone".
- **O6 (整) — DECLINE ACCEPTED.** JMdict 1376240 整備 gives "maintenance; servicing" and "putting in place; development". The card's gloss is within those senses.
- **O6 (嫌い) — DECLINE ACCEPTED.** JMdict 1257240 sense 1 is "disliking; hating; detesting". The card's "dislike" wording is the same meaning.
- **L1 — RESOLVED.**
  - All 15 cards' Joyo-table claims match the packet's p*.txt extracts. That covers readings, example words, remarks (仮名 かな, 素人), the older form 騒（騷）, and the ⇔ pairs 応える/答える, 基 with 下/元/本, 張る/貼る, 整える/調える, 整う/調う and 暖 with 温.
  - The 器 claim is also corroborated by the page crop.
- **L2 — RESOLVED.** For all 15 cards, the meaning quiz shows three curated distractors with no fallback, according to quiz-safety.txt and QuizBuilder.kt. Every displayed title is defensibly wrong in both directions:
  - 張: 長, 弧, 弱
  - 器: 品, 喜, 奇
  - 素: 組, 毒, 責
  - 応: 広, 庁, 欧
  - 仮: 板, 坂, 返
  - 基: 期, 型, 勘
  - 価: 仮, 西, 化
  - 激: 撃, 滴, 漱
  - 嫌: 兼, 験, 好
  - 縮: 宿, 績, 組
  - 騒: 験, 駐, 掃
  - 統: 充, 練, 紙
  - 級: 吸, 扱, 給
  - 整: 政, 敬, 敗
  - 暖: 暗, 段, 談
- **L3 — RESOLVED.**
  - For every reading prompt in reading-options.txt, the excluded keys cover all metadata readings. Curated options that collide with a valid reading are skipped (for example 長 ちょう, 喜/奇 き, 組 そ, 欧 おう, 段/談 だん).
  - Every prompt reaches three wrong options in all 200 seeds.
  - The one-kana entries in the fallback tiers (お for オウ, そ for ソウ, と for トウ, だ for ダン, げ for ゲン) survive because `mutations()` drops forms shorter than two kana. None of them is a reading of the target kanji, so each is defensibly wrong.
  - The only unlisted reading that can actually be drawn is お for 応 オウ (3 of 200 seeds). KANJIDIC2 lists it only as a nanori (name reading), and Daijisen (weblio-応) gives only オウ and ヨウ as on readings. It is therefore a wrong answer to an on'yomi prompt, which CHANGES.md discloses.
  - わり (張), とも (基) and さい (騒) sit in unreachable lower tiers.

## Verdicts

| Facet | Overall | Per-card differences |
|---|---|---|
| 1. Correctness | CLEAN | none |
| 2. Scoped coverage | CLEAN | none |
| 3. Consistency and quiz safety | CLEAN | none |
| 4. Comprehensibility | CLEAN | 暖 has a minor optional polish point (see Optional) |

Other checks:

- 張, 仮, 統, 整 and 暖 changed only in whitespace; I verified this by token diff.
- The other ten cards' hunks match CHANGES.md and introduce no contradiction with untouched text.
- Removing 募 from 応's exclusions and 校 from 級's, and adding 料 to 素's, is safe:
  - The 募, 校 and 料 cards list none of these batch kanji.
  - Each title is clearly wrong for the other card.
  - The new notes 応.md:61 and 級.md:56 are accurate. JMdict 応じる sense 2 includes applying in response to recruitment.
- 応援.md:32–33 ("Both written characters belong in the word, though 援 does not have a kanji card here.") is correct and consistent with 応.md.

## Confirmation

CONFIRMED

## Findings

None. I found no new established defect in the changed hunks, the changed word article or the post-fix quiz options.

## Optional

1. 暖.md:42 begins "KANJIDIC2 lists it…", and "it" refers to ノン at the end of the previous paragraph. Naming ノン explicitly would read better on a phone. This text is unchanged from round 1.
2. 暖.md:40 mentions the Joyo ⇔温 contrast only for あたたか. The Joyo table attaches it to all four kun readings. This is unchanged text and not wrong, just incomplete.

## Limits

- The Joyo evidence consists of pdfplumber text extracts, not the PDF itself. For 器, the page crop corroborates the extract. For the other cards I trusted the extract.
- The reading-option audit has known limits:
  - It draws from all 1,161 cards, while the app draws only from studied cards.
  - It uses its own random generator, not the app's, and it reports candidate sets rather than exact app draws.
  - quiz_exclusions do not apply to the reading quiz.
  - I judged whether candidates are valid; I did not re-run the simulation.
- I did not read diffs\fix.patch directly. Instead I ran an equivalent old-vs-new token diff of the 15 cards, and for 応援.md I compared the old lines 28–36 with the new text.
- I did not re-run the link and lint checks, so I rely on CHANGES.md and my own reading of the changed hunks.
- I did not re-open words\仮名遣い.md (O4) in this round. The decline is accepted on the basis of my round-1 reading.
- I made no new public-web lookups in this round. JMdict checks used the packet's pinned extract, which may differ slightly from the live JMdict.
