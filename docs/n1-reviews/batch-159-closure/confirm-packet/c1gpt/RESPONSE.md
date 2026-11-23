# Author's statement for the reviewer of `b159-review-gpt.md`

This statement answers only the points in YOUR initial report. F1-F5 are your Findings 1-5. O1 is your Optional line. L1-L3 are your three Limits in order: 伯叔 naturalness; manifest and application source; packet hashes and the Git signature.

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

Every stroke file and every other kanji card and word article is unchanged. Give a disposition for each of F1-F5, O1 and L1-L3, and judge the other reviews' changes described below.

## Findings

### F1: 吟味 lacks an exclusion against 試験

Author action: **changed**. `words\吟味.md:8` adds 試験 and 確認 to `quiz_exclusions`. 確認 was added for consistency with the existing exclusion 確かめる; the original packet showed 吟味 drawable in 確認's quiz (its `evidence\audits\word-quiz.txt:1189`), as well as in 試験's (line 1223).

- In `evidence\word-quiz.txt` (revised snapshot), neither reverse pair remains. 吟味's own option set (lines 216-252) is unchanged, because neither word was in it.
- `CHANGES.md` lists the 12 quizzes in which 吟味 can still be drawn (審判, 対照, 批評, 探偵, 断定, 比較, 測定, 研究, 観察, 観測, 評価 and 重視). The author judged that none of them would be glossed "close examination; careful selection". Please check that judgement.

### F2: 吟 excludes only poetry neighbours; 検 overlaps

Author action: **changed**. `kanji\吟.md:14` adds 検 審 査 調 究 研 to `quiz_exclusions`. Line 42 names them with their titles: 検 "inspect; examine; check", 審 "examine; judge; trial", 査 "investigate; inspect", 調 "investigate; tune", 究 "investigate thoroughly" and 研 "polish; study closely". These overlap with the sense of examining something closely, as in 吟味.

- **The sense.** Digital Daijisen gives that sense of 吟 as 「内容を探り確かめる。「吟醸・吟味」」 (sense 4, `evidence\daijisen-kotobank.json`, entry 吟).
- **Other examination neighbours reassessed; not excluded:** 診 "diagnose; examine medically", 偵 "spy; covert investigation", 試 "test; try", 験 "test; verify", 察 "observe; infer", 鑑 "model; appraise" and 覧 "look over; peruse". Each names a narrower activity: medical, covert, trial, observation, appraisal or reading. 験 is the closest call; please judge it.
- **Where the exclusions matter.** 吟's curated distractors 二 自 社 fill all three slots in every shipped pool (`checks\quiz-safety.txt` line 16; `checks\reading-options.txt` line 108). So, as you noted, these exclusions matter only in fallback or custom pools.

### F3: 又's "usually written in kana" reason, and the existing-article-first rule

Author action: **changed**, as your remedy proposed. 又 no longer uses the untagged route. Its support words are the existing kana-headed articles `words\または.md` and `words\また.md`, under point 2 of the rule (`evidence\rule-7058679348.md`).

- **The two supports.**
  - または (entry 1524990) carries ichi1/news1 on both the spelling 又は and the reading. `words\または.md:24` now says "又は, written with [又](../kanji/又.md), is another spelling".
  - また (entry 1524930) carries ichi1/news1 only on the reading, so the ledger records that mapping as untagged, with a note (ledger lines 45-67). `words\また.md:24` now links 又 in "[又](../kanji/又.md) is a recognized spelling".
- **The 又 card.**
  - `kanji\又.md:23` links both articles and says that they are headed in kana and show 又 and 又は as other spellings.
  - Line 30 (the また row) links both. `quizKunyomi` is now [また] (line 12).
  - Line 31 (the また- row) keeps 又聞き and 又貸し as unlinked examples, "Not selected for questions here."
- **Removed from the frozen draft:**
  - `words\又聞き.md`, and its line on `kanji\聞.md`;
  - its ledger mapping and exclusion row;
  - JMdict 1442420 (伝聞) and 2025400 (又ね).
- **Repository audit.** It accepts the kana-headed support through a new `support_spelling()` (`tools\audit_n1_batch.py:60-67`), with five tests (`tools\test_audit_n1_batch.py:129-153`). A mapping's `spelling` is accepted only when:
  - the article is kana-headed;
  - the spelling contains the kanji;
  - the article text shows that spelling.
- **Lint** reports two new warnings on `kanji\又.md`, because または and また cannot list 又 in `kanji:` (`tools\validate.py:504-508` rejects a `kanji:` entry that is not in the headword).

### F4: 叔's justification overlooks the tags on the spellings 叔父 and 叔母

Author action: **wording changed**; the untagged route with 伯叔 is **kept**, with the evaluation you asked for.

- **The rewritten reason.** Ledger line 78 (`exceptionReason`) now states that the spellings 叔父 (1607070) and 叔母 (1607100) carry ichi1/news1. Their tagged readings are the whole-word readings おじ and おば. The Joyo table lists these as special readings of 叔父 and 叔母 (`evidence\joyo\p75.txt`, and its appendix of whole-word readings, 付表, on `p162.txt`). しゅくふ and しゅくぼ are restricted to those spellings and carry no priority tag.
- **Why 伯叔 is kept.** As you say, しゅくふ and しゅくぼ are unflagged, use シュク, and 父 and 母 have cards. But an article headed 叔父 or 叔母 would teach おじ or おば as its primary reading. Those are not readings of 叔: the card has `kunyomi: []`. An article that taught 叔父 as しゅくふ would teach a learner the less common reading of an everyday word.
- **Precedent.** 伯叔 (1474270) is the Joyo table's only example for シュク. The same choice was accepted in B156 for 伯, where 伯父 and 伯母 were passed over for 伯仲.
- **For learners.** `kanji\叔.md:39` adds the Joyo point: おじ and おば are whole-word special readings, not readings of 叔 alone.

Please judge whether this justification satisfies the untagged route for this row.

### F5: Dictionary lines omit the Digital Daijisen entry link

Author action: **changed**. Line 34 of all nine remaining new word articles now ends with a `[Digital Daijisen, <word>](https://kotobank.jp/word/…)` link: 不吉 伯叔 厘 叙情 吟味 呉服 太后 官吏 贈呈. The tenth article, 又聞き, is deleted (F3).

- The text behind each link is in `evidence\daijisen-kotobank.json`, keyed by word, with the canonical kotobank URL.
- The word articles of earlier batches (B156-B158) also lack this link. That backfill is outside this batch; it will be offered to the owner separately.

## Optional notes

### O1: no merged card warranted; the 后 and 吏 exceptions are supported

Author action: **none**. Two related wording changes from the other reviews are listed below (items 3 and 4).

## Limits answered

### L1: naturalness of the 伯叔 examples

The examples are unchanged. `words\伯叔.md:15` now says that both use Digital Daijisen's sense 2, a parent's brothers, and translates them as uncles. Naturalness remains your judgement.

### L2: manifest and application source not in the packet

Author action: **evidence added**.
- `checks\manifest.txt` shows that rebuilding the manifest at the revised snapshot gives an identical file.
- `checks\audit.txt` reports the manifest fresh (contentVersion `92143d996fc2aff4`).
- The app's quiz code is in `evidence\QuizBuilder.kt` (kanji quizzes) and `evidence\Words.kt` (word quizzes).

### L3: packet hashes do not authenticate the Git signature

Author action: **evidence added**. `evidence\verify-commit.txt` holds `git verify-commit -v` output for the reviewed snapshot `1a9bb910` and the revision `5c04be73`, each with its parent line, and `git log --show-signature` for the batch range `2787e43b..5c04be73`. This is Git's own signature check, not a packet hash.

## Changes made for the other reviews

The other two reviews asked for the changes below. Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **又's sense list** (`kanji\又.md:23`) quotes the senses one by one: "again," "also," "on the other hand," "and; in addition" and "or; otherwise". The distractor note (line 48) says none means "again," "also" or "or." This replaces the frozen "and, or or".
2. **伯叔** (`words\伯叔.md`):
   - line 15 gives Digital Daijisen's two numbered senses, (1) older and younger brothers and (2) a parent's older and younger brothers, 伯父 and 叔父, then JMdict's gloss, and labels both examples as sense 2;
   - line 24 explains how 伯 (older) and 叔 (younger) combine in both senses;
   - line 32 adds that neither sense covers aunts.
3. **太后 and 太.**
   - `words\太后.md:15` adds a plain-terms sentence from Digital Daijisen: 皇太后 is the empress of the previous emperor, or one who is also the current emperor's birth mother, and 太皇太后 is the empress of the emperor two reigns back.
   - `kanji\太.md:38` adds that in 太后, 太 is added to an honored person's title and does not mean "thick" (Daijisen 太 sense 4, 尊い者に添える語).
4. **官吏 and 官.**
   - `words\官吏.md:18` replaces the undated corruption example with one framed as history: 歴史の本で、汚職をした官吏の話を読みました。 "I read about a corrupt government official in a history book."
   - `kanji\官.md:37` adds "(dated)".
5. **吟味's "How the kanji combine"** (`words\吟味.md:24`): here 吟 has its sense of examining contents closely, and Digital Daijisen lists 吟味 under that sense. Reciting a poem and savoring its flavor is the original meaning: JMdict sense 4 (archaic) and Daijisen sense 3.
6. **叔's reason wording.** This is the same change described under F4.
7. **厘** (`kanji\厘.md:42`): 分 ぶ "is the fractional unit ten times larger" (was "the next larger fractional unit"), and 厘 is one-hundredth, including 0.3 mm as one-hundredth of a sun. `words\厘.md:28` says one 分 equals ten 厘.
8. **Optional wording:**
   - `words\呉服.md:18` explains obi ("the long sash tied around the waist over a kimono") and calls 呉服売り場 the department store's kimono-fabric counter;
   - `kanji\呈.md:40` quotes 呈する's JMdict glosses in full (entry 2012430): "to present; to offer," "to show; to display; to exhibit" and "to assume (e.g. a shape)".

Every other changed line is a ledger line that records the same changes, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
