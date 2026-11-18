# Batch 141 revision: what changed from a92d134a to 65b47299

Revised snapshot: `65b47299831240115de12f5c9c5f0f6ed0e2065d`. It is reached from the reviewed snapshot
`a92d134afd93566ba705b586daf8d7969c683a5f` by one commit. Nothing is published.

- Four of the 15 new kanji cards changed: 懐, 懸, 扇 and 抽. The other eleven (悔, 悟, 惑, 惜, 愉, 慎, 慮, 慰, 憧, 憩,
  拡) are unchanged. The existing card 張 changed again, within its declared remark edit. Two word articles changed
  beyond their link wrap: 悔しい and 悔やむ. The other 19 word articles and all 15 stroke files are unchanged from the
  reviewed snapshot.
- No front matter changed: no title, tag, metadata reading, `distractors` or `quiz_exclusions` list. The meaning and
  reading quiz options are therefore unchanged (see "Checks" below).
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. Two cards changed length:
  - 懐 went from 70 to 73 lines. Reviewed-snapshot line 66 became lines 66-69; reviewed-snapshot lines 67-70 are now
    lines 70-73 (3 later), so the Metadata line moved from 68 to 71.
  - 扇 went from 61 to 62 lines. Reviewed-snapshot line 57 became lines 57-58; reviewed-snapshot lines 58-61 are now
    lines 59-62 (1 later), so the Metadata line moved from 59 to 60.
  - Every other line number is unchanged.
- `diffs\fix.patch` is the exact patch from `a92d134a` to `65b47299`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`, with the target's
  real `title:`.
- The Metadata lines are unchanged. The revision names no word that the cards did not already name: 抽斗, 抽出し and
  抽き出し are forms of JMdict 1601650, which 抽's Metadata line already lists, and 懸念 (けねん, けんねん) is JMdict
  1257720, which 懸's Metadata line already lists. `evidence\meta-scan.txt` finds no word without its entry; apart from
  line 1 (the command) it is identical to the reviewed snapshot's output.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| words\悔しい | 25 | The sentence `There is no 悔 card in the current collection.` is removed. The line now reads `[悔](../kanji/悔.md) supplies the regret/frustration association in the native adjective くやしい. The dictionary also records 口惜しい as a rare kanji spelling.` |
| words\悔やむ | 28 | The sentence `No 悔 kanji card is currently available.` is removed. The line now reads `[悔](../kanji/悔.md) carries a regret association, here in the native verb くやむ; む is the ending. 悔む is another dictionary spelling of the same word.` |
| 抽 | 34, 36 | Line 34, the ひき- row: the example `抽き出し ひきだし` is now `抽斗 ひきだし`, and `marks 抽き出し and 抽斗 as rarely used kanji forms` now reads `marks 抽斗 and 抽き出し as rarely used kanji forms`; the rest of the row is unchanged. Line 36: the sentence `In 抽き出し, 抽 writes ひ, き is okurigana, the kana ending that follows the kanji, and だし follows; JMdict also lists 抽出し as a search-only spelling, and Daijisen lists 抽斗 ひきだし as a hard-to-read word.` is replaced by `In 抽斗, 抽 writes ひき and 斗 writes だし; Daijisen lists 抽斗 ひきだし as a hard-to-read word. JMdict also lists 抽出し, where 抽 writes ひき, 出 writes だ and し is okurigana, the kana ending that follows the kanji, as a search-only spelling. In the rarely used spelling 抽き出し, 抽 writes only ひ and き is okurigana; KANJIDIC2 lists ひき- for 抽 but no verb reading ひ.く.` Support: `evidence\jmdict-cited-entries.xml`, entry 1601650 (forms 引き出し and 引出し; 抽き出し and 抽斗 marked rarely used; 抽出し and 抽匣 search-only; reading ひきだし); the original packet's `evidence\kanjidic2-records.xml` (抽: チュウ, ひき-) and `evidence\public-source\weblio-抽.txt` line 6 (`［ 難読 ］ 抽斗 ( ひきだし )`). |
| 張 | 59 | The first Notes bullet ended `and [威](威.md), "intimidate; authority; dignity," is the other kanji in 威張る. 緊 in 緊張 does not have a kanji card yet.` and now ends `[威](威.md), "intimidate; authority; dignity," is the other kanji in 威張る, and [拡](拡.md), "expand; enlarge; widen," is the other kanji in 拡張. 緊 in 緊張 does not have a kanji card yet.` Against the published text (base `466b7b28`), the whole remark edit replaces `and [威](威.md), "intimidate; authority; dignity," is the other kanji in 威張る. 緊 in 緊張 and 拡 in 拡張 do not have kanji cards yet.` with the new ending above. `evidence\kanji-remarks.json` declares exactly that replacement. |
| 懸 | 46, 56 | Line 46 ended `In 懸念, 懸 supplies ケ and 念 supplies ネン.` and now ends `In 懸念, 懸 supplies ケ and 念 supplies ネン; JMdict lists けねん first and also the reading けんねん, where 懸 supplies ケン.` Line 56: `The other kanji in the common words are` now reads `The other kanji in the common word are` (the section lists only 一生懸命). Support: `evidence\jmdict-cited-entries.xml`, entry 1257720 (懸念; readings けねん, けんねん). |
| 懐 | 66-69 | Reviewed-snapshot line 66, one "For reference" bullet with all the extra Daijisen examples, is split into four bullets with the same examples and glosses in the same order: line 66 `For reference, more Daijisen examples of the first カイ sense, holding a thought in one's heart:` 懐疑 … 本懐; line 67 `More examples of the second カイ sense, wrapping and holding something inside:` 懐石 and 懐胎; line 68 `More examples of the fourth カイ sense, the bosom of one's clothing:` 懐剣, 懐紙, 懐炉 and 胸懐; line 69 `A Daijisen example with ふところ is 懐刀 …` (it was `A ふところ example is 懐刀 …`). The sense names repeat the list at lines 27-30. Support: the original packet's `evidence\public-source\weblio-懐.txt` line 6, the Daijisen character entry (the extract has spaces between words): its sense １ lists 懐疑, 懐旧, 懐古, 感懐, 述懐, 所懐, 素懐, 坦懐, 追懐, 抱懐 and 本懐; sense ２ lists 懐石, 懐胎 and 懐妊; sense ３ lists 懐柔; sense ４ lists 懐剣, 懐紙, 懐中, 懐炉 and 胸懐; and 〈 ふところ （ぶところ）〉 lists 懐刀, 懐手 and 内懐. |
| 扇 | 57-58 | Reviewed-snapshot line 57 is split before `Under おうぎ`: line 57 keeps the セン examples (銀扇 … 扇情, also spelled 煽情) and line 58 is a new bullet `Under おうぎ, Daijisen gives 扇形 …`, continuing with the 団扇 sentence exactly as before. No word changed. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter (16 kanji cards: the 15 new ones and 張; 28 word articles): 0 errors, 2 warnings, both on
  word articles whose Dictionary line cites no JMdict entry id (扇風機, 威張る). The same two warnings were reported at
  the reviewed snapshot (the original packet's `mechanical-checks.md`).
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage
  pilot). `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt`: the word-article link plan: 21 changed word files, 21 expected and 21 added link pairs, **2 declared
  remark edits** (it was 0), 0 problems. The two declarations are in `evidence\word-remarks.json`: each removes exactly
  the stale sentence quoted above.
- `kanji-remarks.txt`: existing kanji cards are unchanged apart from the declared remark edit in 張 (1 modified, 15 of
  15 new cards present, 0 problems). The declaration, updated for the 拡 clause, is `evidence\kanji-remarks.json`.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine), so there is no `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether
  the gloss quoted after the link equals that title.
- `quiz-safety.txt` is identical to the original packet's `evidence\audits\quiz-safety.txt`: 0 errors, 0 warnings.

### Reading audits

`reading-exposure.txt` and `reading-options.txt` were rerun with the same `--extra` input as at the freeze. Apart from
line 1 (the command), both are identical to the original packet's `evidence\audits\` files, because no front matter
changed.

- `reading-exposure.txt` line 256: 0 production hits, 0 padded-session hits, 5 latent collisions, as at the freeze;
  line 257: 0 one-holder padded hits, 0 more for KANJIDIC2 name-only readings.
- `reading-options.txt` line 230: 0 problems.

## Process notes

- `65b47299` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `a92d134a`.
- The checks in `checks\` were run on the committed revision.
