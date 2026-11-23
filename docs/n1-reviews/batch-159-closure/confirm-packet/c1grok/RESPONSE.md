# Author's statement for the reviewer of `b159-review-grok.md`

This statement answers only the points in YOUR initial report. F1-F6 are your Findings 1-6. O1-O4 are the four points of your Optional line in order: the obi, 呈's glosses, 居, and 吟味's sense 3. L1-L3 are the first three of your Limits:
- L1: the Joyo PDF and Kanjipedia were not re-fetched;
- L2: the idiom of the 伯叔 and 官吏 examples was not checked;
- L3: other Daijisen character pages were not reopened.

Your last two Limits (pinned versus online JMdict, and not looking outside the packet) describe your method and need no answer.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet.

What changed, in brief (see `CHANGES.md` for every line):
- five batch kanji cards (厘 又 叔 吟 呈) and all nine remaining new word articles;
- the new word 又聞き is deleted, and the frozen line added to 聞 is removed;
- the frozen one-line additions to 太 and 官 changed;
- two existing kana-headed articles, また and または, now link the 又 card;
- the repository audit `tools/audit_n1_batch.py` and its tests;
- the ledger `docs\n1-sources\batch-159-progress.json`;
- the batch's pinned JMdict extract (two entries removed);
- the generated `manifest.json`.

Every stroke file and every other kanji card and word article is unchanged. Give a disposition for each of F1-F6, O1-O4 and L1-L3, and judge the other reviews' changes described below. The largest of those changes, 又's support words (item 1), reverses a point your report judged CLEAN; please review it closely.

## Findings

### F1: 又's sense list "and, or or"

Author action: **changed**.
- `kanji\又.md:23` now quotes the senses one by one: また has senses that include "again," "also," "on the other hand," "and; in addition" and "or; otherwise" (JMdict entry 1524930). 又は means "or; either … or" (entry 1524990).
- The distractor note (line 48) reads: "none means “again,” “also” or “or.”"

### F2: 伯叔's senses and examples

Author action: **changed**.
- **Line 15** gives Digital Daijisen's two numbered senses, (1) older and younger brothers, and (2) the older and younger brothers of one's father or mother, that is, 伯父 and 叔父, one's uncles. It then quotes JMdict's gloss and says: "Both examples below use sense 2."
- **Line 24** is rewritten. 伯 stands for the older and 叔 for the younger: in sense 1 (兄と弟) an older and a younger brother, and in sense 2 a parent's older and younger brothers, 伯父 and 叔父. It keeps JMdict's note on 伯父 and 叔父 (entry 1607070).
- **Line 32** adds: "Neither sense covers aunts (伯母 and 叔母)."
- The title, JMdict's gloss "brothers; one's father's brothers", is unchanged.

### F3: 太后 is not explained in plain terms

Author action: **changed**. `words\太后.md:15` adds a plain-terms sentence from Digital Daijisen: 皇太后 is the empress of the previous emperor, or one who is also the current emperor's birth mother, and 太皇太后 is the empress of the emperor two reigns back.

The Daijisen sections for 太后, 皇太后 and 太皇太后 are in `evidence\daijisen-kotobank.json`. The author kept Daijisen's definitions rather than your suggested "widow" and "grandmother", which Daijisen does not say.

### F4: 太's new 太后 line has no bridge from "thick"

Author action: **changed**. `kanji\太.md:38` adds "(here 太 is added to an honored person's title; it does not mean “thick”)". The source is Digital Daijisen's sense 4 of 太, 「尊い者に添える語。「太公・太后・太閤」」 (`evidence\daijisen-kotobank.json`, entry 太).

### F5: 吟味's "How the kanji combine" does not say which sense of 吟 applies

Author action: **changed**. `words\吟味.md:24` now reads: 吟 "can mean reciting poetry, but here it has its sense of examining contents closely: Digital Daijisen lists 吟味 under that sense of 吟." 味 means taste or savoring. "Reciting a poem and savoring its flavor is the original meaning of 吟味 in both JMdict (sense 4, archaic) and Digital Daijisen (sense 3)."

The Daijisen sense of 吟 is 「内容を探り確かめる。「吟醸・吟味」」 (sense 4, entry 吟 in `evidence\daijisen-kotobank.json`).

### F6: 官吏's second example reads as modern usage, and 官's line lacks "dated"

Author action: **changed**.
- `words\官吏.md:18` is now framed as history: 歴史の本で、汚職をした官吏の話を読みました。 "I read about a corrupt government official in a history book."
- `kanji\官.md:37` adds "(dated)".
- `words\官吏.md:28` already names 公務員, a public employee or civil servant (JMdict entry 1274820), so the modern-word pointer you suggested was already present.

## Optional notes

### O1: "obi" and "kimono section" in 呉服

Author action: **changed**. `words\呉服.md:18` now reads: "I chose an obi, the long sash tied around the waist over a kimono, at the department store's kimono-fabric counter."

### O2: 呈's compressed glosses

Author action: **changed**. `kanji\呈.md:40` quotes 呈する's JMdict glosses in full (entry 2012430): "to present; to offer," "to show; to display; to exhibit" and "to assume (e.g. a shape)".

### O3: 居 overlaps 呈 only in the English word "present"

Author action: **not changed**; the author agrees that 居 is not a second defensible answer.

### O4: 吟味's JMdict sense 3 (a game abbreviation) is not cited

Author action: **not changed**; the author agrees, and the cited senses are unchanged.

## Limits answered

### L1: the Joyo PDF and Kanjipedia were not re-fetched

Author action: **evidence added** for the Joyo table. `evidence\joyo\` has the text of each cited page of the official PDF, with its sha256:
- p157 and p136: 厘 and 分;
- p145: 又;
- p75 and p162: 叔, and the appendix of whole-word readings (付表);
- p78: 叙;
- p34: 吉;
- p52: 后;
- p154: 吏;
- p41: 吟;
- p112: 呈;
- p51: 呉.

Kanjipedia data is unchanged and is in the original packet, `evidence\public-source\kanjipedia.json`.

### L2: the idiom of the 伯叔 examples and 官吏 example 2

The 伯叔 examples are unchanged but are now labeled as sense 2 (F2). 官吏 example 2 is replaced (F6). Naturalness remains your judgement.

### L3: other Digital Daijisen pages were not reopened

Author action: **evidence added**. `evidence\daijisen-kotobank.json` holds the Digital Daijisen sections from kotobank.jp (fetched 2026-11-23) for:
- the nine words;
- the kanji 又 吏 太 吟 叙 呈;
- 皇太后 and 太皇太后.

The nine word articles now link these entries on line 34 (item 3 below).

## Changes made for the other reviews

The other two reviews asked for the changes below. Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **又's support words.** Both other reviews found that "usually written in kana" is not one of the marks that point 2 of the rule excludes (irregular, rare, outdated, ateji, gikun). They also noted that the rule (`evidence\rule-7058679348.md`) first checks for an existing article, "including a kana-headed one".
   - **The new supports.** 又 is now supported by the existing kana-headed articles `words\または.md` and `words\また.md`, not the untagged new word 又聞き.
     - または (entry 1524990) carries ichi1/news1 on both the spelling 又は and the reading.
     - For また (entry 1524930), only the reading carries ichi1/news1, so the ledger records the 又 spelling as untagged, with a note (ledger lines 45-67).
     - 又 and 又は are the Joyo table's examples (`evidence\joyo\p145.txt`).
   - **The 又 card.** `kanji\又.md:23` and line 30 link both articles; `quizKunyomi` is [また] (line 12).
   - **また and または.** `words\また.md:24` and `words\または.md:24` link the 又 card.
   - **Removed.** `words\又聞き.md` and its line on `kanji\聞.md` are removed. 又聞き and 又貸し remain unlinked examples on the また- row (line 31).
   - **Audit and lint.** The repository audit accepts the kana-headed support through a new `support_spelling()` (`tools\audit_n1_batch.py:60-67`), with five tests. lint reports two new warnings on `kanji\又.md`, because a kana-headed article cannot list 又 in `kanji:` (`tools\validate.py:504-508`).
2. **叔's reason wording.**
   - **Ledger line 78** now says that the spellings 叔父 and 叔母 carry ichi1/news1, but their tagged readings are the whole-word readings おじ and おば, and the Joyo table lists those as special readings of 叔父 and 叔母. The シュク readings しゅくふ and しゅくぼ carry no priority tag. An article headed 叔父 or 叔母 would teach おじ or おば.
   - **The route.** It is unchanged: 伯叔 with an untagged justification.
   - **For learners.** `kanji\叔.md:39` adds that 伯叔 is the Joyo table's only example for シュク, and that おじ and おば are whole-word special readings, not readings of 叔 alone.
3. **Digital Daijisen links** on line 34 of all nine new word articles, as point 4 of the rule requires.
4. **吟味 excludes 試験 and 確認** (`words\吟味.md:8`). JMdict 1243390 sense 1 includes "testing", and 吟味 was drawable in 試験's quiz. 確認 was added for consistency with the existing exclusion 確かめる. `CHANGES.md` lists the 12 quizzes in which 吟味 can still be drawn.
5. **吟 excludes 検 審 査 調 究 研** (`kanji\吟.md:14`; the reason, with their titles, is at line 42). They overlap with examining something closely. `CHANGES.md` explains why 診 偵 試 験 察 鑑 覧 are not excluded.
6. **厘.**
   - `kanji\厘.md:42`: 分 ぶ "is the fractional unit ten times larger" (was "the next larger fractional unit"), and 厘 is one-hundredth, including 0.3 mm as one-hundredth of a sun (JMdict entries 1502850 and 1555420).
   - `words\厘.md:28` says one 分 equals ten 厘.

Every other changed line is a ledger line that records the same changes, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
