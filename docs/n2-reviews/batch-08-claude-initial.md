## Snapshot
`92300150bee23b62f8c0558f97ddd224d0d48498`, committed files only. I could only read files and could not run Git. So I did not check the commit identity, the clean worktree, the 58-file scope or the diff against baseline `43e664c8994edc45de427bed0d1e4b3fd40b03d0` myself. I relied on the author's confirmation and assumed the files on disk match that commit.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked alone in one sequential pass and edited nothing.
- **Instructions read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-109`.
- **Read completely:** the 15 cards (庫 延 弱 律 復 快 恋 患 悩 憎 戸 承 技 担 拝) and `words\憎む.md`.
- **Evidence read:** all of `docs\n2-batch-sources\batch-08.json` and `docs\n2-source-snapshot.json:1-90`.
- **Related edits (narrow):** I read the component-link passage, with its section context, in each of the 22 word articles. The 延期 and 担当 articles were read in full.
- **Quiz checks:**
  - All 45 distractors against the actual answer meanings.
  - Every new title for exact duplicates.
  - Overlapping meanings among existing kanji titles.
  - The 20 legacy cards that have only two choices.
  - Word titles about hating or disliking, plus the `quiz_exclusions` of 憎む.
- **Stroke files:** for all 15, the `strokeCount` matches the card's stroke count and the KanjiVG revision is the pinned `70a0b7ae…`.
- **Public sources fetched:** ja.wiktionary pages 庫, 承 and こう; the jisho.org word API (a JMdict mirror) for くら and 承ける; kotobank and weblio pages for 恋う.
- **Omissions:**
  - Stroke drawing paths were not reviewed.
  - The unchanged bodies of the 22 word articles were not reviewed.
  - `docs\jlpt-levels.md` was not read, so I did not assess 憎む's lack of a word JLPT level (the field is optional).
  - Forbidden ledgers and reports were not read.
  - Nanori and the old four-level JLPT tags are out of scope.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\庫.md | CLEAN | NEEDS FIX (B08-01) | CLEAN |
| kanji\延.md | CLEAN | CLEAN | CLEAN |
| kanji\弱.md | CLEAN | CLEAN | CLEAN |
| kanji\律.md | CLEAN | CLEAN | CLEAN |
| kanji\復.md | CLEAN | CLEAN | CLEAN |
| kanji\快.md | CLEAN | CLEAN | CLEAN |
| kanji\恋.md | CLEAN | CLEAN | CLEAN |
| kanji\患.md | CLEAN | CLEAN | CLEAN |
| kanji\悩.md | CLEAN | CLEAN | CLEAN |
| kanji\憎.md | CLEAN | CLEAN | CLEAN |
| kanji\戸.md | CLEAN | CLEAN | CLEAN |
| kanji\承.md | CLEAN | NEEDS FIX (B08-02) | CLEAN |
| kanji\技.md | CLEAN | CLEAN | CLEAN |
| kanji\担.md | CLEAN | CLEAN | CLEAN |
| kanji\拝.md | CLEAN | CLEAN | CLEAN |
| words\憎む.md | CLEAN | CLEAN | CLEAN |

What passed without findings:
- **Card data:** every stroke count, radical and number, grade tag, on reading and kun reading matches the KANJIDIC2 record in batch-08.json. 延 correctly uses 8 strokes and mentions the alternative count of 7.
- **Distractors:** each new card has exactly 3, and all 45 are semantically wrong for the answer. No new title exactly duplicates an existing one.
- **Legacy two-choice cards:** none of the 20 is affected.
- **憎む:** it is a transitive godan verb (JMdict 1403440), its forms are correct, and it excludes 嫌う and 嫌い from its quiz. No other word title means "hate" or "dislike".
- **Related edits:** all 22 component-link passages are accurate.

## Findings

**B08-01 · Minor · scoped coverage · `kanji\庫.md:30` (also :40)**
- **Problem:** the row "くら | kun | 庫 くら - storehouse; warehouse" appears as a typical word with no note on its spelling. The word くら is normally written 蔵 or 倉, and くら is not one of 庫's jōyō readings. Note :40 only says that 庫裏 doesn't show くら.
- **Impact:** learners may think 庫 is an ordinary spelling of くら. 復.md:29,38 qualifies its own rare spelling, so the two cards are inconsistent. This conflicts with content-structure.instructions.md:44-45 and :67.
- **Remedy:** keep the row and add: "The word くら is normally written 蔵 or 倉; くら is not a jōyō reading of 庫." Do not add a claim about how often it is used.
- **Evidence:**
  - batch-08.json:735-748 (entry 1592380): `spellingPriority []` for 庫, while the reading carries ichi1/news1/nf10. This alone does not prove rarity.
  - The fetched jisho API lists that entry under 蔵, with spellings 蔵, 倉, 庫 for くら.
  - ja.wiktionary 庫 marks ク and コ as 表内 (in the jōyō table) but くら as not.
- **Confidence:** high on the facts; medium-high that this needs fixing.

**B08-02 · Minor · scoped coverage (affects comprehensibility) · `kanji\承.md:33` and `:45`**
- **Problem:** the row "承ける うける - receive; get" teaches the most ordinary sense with no note that this sense is normally written 受ける, or that う.ける is not a jōyō reading of 承. Note :45 says the row is "not unrestricted spelling substitution across every sense", which suggests 承ける is a normal way to write "receive".
- **Impact:** learners may write 承ける for everyday "receive".
- **Remedy:**
  - Keep the reading and add: "Ordinary receive/get is written 受ける; う.ける is not a jōyō reading of 承. Learn 承ける for recognition."
  - Optionally mention that the entry notes this spelling especially for the grammar sense "be modified by".
- **Evidence:**
  - batch-08.json:3110-3135 (entry 1329590): `spellingInfo []` and `spellingPriority []`. Sense 1 has no restriction.
  - :3295-3296: sense 10, "to be modified by", is the only sense whose note mentions 承ける ("esp. 受ける, 承ける").
  - The jisho API files the entry under 受ける (spellings 受ける, 請ける, 承ける, 享ける, ウケる) and tags sense 10 as Linguistics.
  - ja.wiktionary 承 marks ショウ and うけたまわ-る as 表内, but not う-ける or ジョウ.
- **Confidence:** medium-high.

## Optional
- **O1:** `延.md:43` says "specifically associates" and `承.md:45` says "specifically assigns", but the source only says "esp." That is a tendency, so wording like "notes the use especially with…" would be more accurate.
- **O2:** in `悩.md:45`, "KANJIDIC2's undotted なやみ row" is jargon and needs plainer words.
- **O3:** in the `戸.md:3` title, "house counter" can read as a countertop. "door; counter for households" is clearer.
- **O4:** in bigger quizzes or when the app fills in choices, some existing titles overlap in meaning:
  - 律 and 法 ("law")
  - 復 with 再 ("repeat") and 戻
  - 延 and 伸
  - 恋 and 愛
  - 患 with 病 and 苦
  - 技 and 術
  - 担 with 負 and 運
  - 拝 and 礼 ("bow")
  - 承 and 受

  The current 4-choice quizzes are unaffected; consider mutual exclusions for these pairs.
- **O5:** 恋.md could show the conjugated forms 恋うて and 恋うた, and add a register label if one can be sourced.
- **O6:** 拝 おろがむ could be labelled archaic if sourced. The card already treats it as a reading recorded only by the source.
- **O7:** `弱い.md:24`, `復習.md:23` and `技術.md:24` write on readings in hiragana (cosmetic).

## Limits
- I could not run Git. The commit identity, cleanliness, file scope and exact changed lines in the 22 related articles are taken from the author's confirmation.
- **恋う register is unresolved.** JMdict has no register tag, ja.wiktionary gives no label, and the Nikkoku excerpt is historical. The Daijisen text did not render, and goo failed with a DNS error. I did not treat this as a defect.
- The jōyō status in B08-01 and B08-02 comes from ja.wiktionary's 表内 markers, not the official MEXT table. The jisho API may not be the pinned JMdict version, and the official EDRDG lookup required a password.
- I did not check the made-up example phrases (for example 延べ三日) against a corpus. They look plausible but are not verified as natural.
- I did not review the stroke drawing paths, only stroke counts and source revision.
