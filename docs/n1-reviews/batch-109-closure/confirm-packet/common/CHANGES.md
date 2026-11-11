# Batch 109 revision: what changed from 0a20f4bf to a3e0610a

Revised snapshot: `a3e0610a7566c20f2bd2ae019617623d6eab7b01`, a child of the reviewed snapshot
`0a20f4bf2415d6b4d20644f518990e8c938259b1`. Nothing is published.

- 13 kanji cards changed. 批 and 択 are unchanged. No word article, stroke file or title changed.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Every quoted title in the new text was checked by script against the linked card's real `title:` (107 links, 0 mismatches).

| Card | Changed lines | Change |
| --- | --- | --- |
| 催 | 14, 44 | New `quiz_exclusions: [促]`. The 促 note now says the Digital Daijisen character entry lists うながす, "to urge," as the first sense of 催, so 促 is kept out of the quiz options. |
| 促 | 14, 23, 45, 47 | `quiz_exclusions` gains 責. "geminate consonant" is replaced by "doubled consonant sound". New 責 bullet: the verb 責める can also mean "to urge; to press; to pester" (JMdict 1383160 sense 2); links `words/責める.md`. Metadata adds JMdict 1383160. |
| 摩 | 14, 36, 46, 50-51 | `quiz_exclusions` gains 研. The readings paragraph is rewritten around the official Joyo kanji table (マ is the only table reading; no kun reading; the three kun readings are kept for recognition; 摩する, 摩る さする and 摩る す.る are qualified). New 研 bullet (研磨, JMdict 1592730). New `Usage evidence:` line (Joyo PDF p. 144). |
| 擦 | 23, 35, 38, 52-53 | こする is "usually written in kana"; 擦過傷 is "the formal term"; the こす.る row is qualified; the readings paragraph states the Joyo-table readings (サツ, す.る, す.れる; not こす.る or こす.れる). New `Usage evidence:` line (Joyo PDF p. 62). |
| 括 | 14, 45 | `quiz_exclusions` gains 包 and 囲. New bullet: they share the word "enclose" with this card's title. |
| 弧 | 23 | "an older sense of 'bow'" is replaced by: Daijisen lists "bow" (ゆみ) as its first sense and the curved line as its second. |
| 抵 | 14, 23, 42 | `quiz_exclusions` gains 反 and 対. The 抵当 gloss is shortened to "mortgage; security". 大抵 is linked to the existing `words/たいてい.md`. New 反/対 bullet. The title "resist; collide" is unchanged. |
| 抗 | 23 | 抗癌剤 becomes 抗がん剤 (also written 抗癌剤). |
| 撮 | 23, 25 | The Daijisen sense is described as its first sense (no "older"). Mnemonic: 最 is "a wide 日-like box (曰) above 取". |
| 影 | 13-14, 34, 45-46, 48 | Distractor 形 is replaced by 英. `quiz_exclusions` becomes [映, 形, 像, 象, 光, 跡]. "older Chinese-derived (Go-on) reading ヨウ". The 形 bullet is extended; new 英 bullet; new 像/象/光/跡 bullet (secondary senses of かげ in JMdict 1590145). |
| 攻 | 14, 44, 48-49 | `quiz_exclusions` gains 研 and 批. The wording of the shared-sense bullet about 撃 (line 44) changed; it no longer says "hitting at a target". New 研 bullet (KANJIDIC2 "polish"; Daijisen みがく and 専攻). New 批 bullet (KANJIDIC2 "criticize"; JMdict 1279170 sense 2 "criticism; censure"). |
| 撃 | 14, 42, 44, 47 | `quiz_exclusions` gains 敗. The wording of the shared-sense bullet about 攻 (line 42) changed the same way. New 敗 bullet (KANJIDIC2 撃 lists "defeat"; 撃退 and 撃破). Metadata adds JMdict 1253590 and 1253620. |
| 掲 | 14, 25, 44 | `quiz_exclusions` gains 刷. Mnemonic: "a variant of 曷 at the right, drawn as a wide 日-like box (曰) above 匂" (the link to the 日 card is removed). The 刊/置 bullet gains 刷 and the JMdict 1250600 sense "to publish; to print; to carry". |

## Quiz mechanics the changes rely on

- `tools\validate.py` rules (all pass): `quiz_exclusions` has no duplicates, no self, every entry has a card, and **no
  entry may also be one of the same card's `distractors`**.
- The app's `QuizBuilder` is in `evidence\QuizBuilder.kt`: options are the curated `distractors` in order; any candidate
  that is excluded against the target or an already chosen option is skipped; `excluded(a, b)` is true if **either**
  card lists the other, so a pair needs to be listed on one side only (the repository lists each pair once). Only when
  fewer than three curated distractors survive are other cards added (tag-similar first).
- `checks\quiz-safety.txt` prints the four options now shown for each card.
