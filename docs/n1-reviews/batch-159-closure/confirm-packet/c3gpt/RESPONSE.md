# Author's statement for the reviewer of the confirmation report on `4f8ebea7`

This statement answers only the points in YOUR confirmation report on `4f8ebea7` (the earlier confirmation report named in `INSTRUCTIONS.md`). F4 is the finding you kept open for publication (NEEDS FIX). OPT is your Optional line (long sentences in 太后 and 吟味). L2 and L3 are the two Limits you marked PARTIALLY RESOLVED. You marked F2 and the earlier OPT (ledger reading-option statement) RESOLVED and accepted the 太后 and 吟味 changes; the text behind them is unchanged in this revision, apart from the sentence splits described under OPT.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet.

What changed, in brief (`CHANGES.md` lists every line): the 叔 support article `words\伯叔.md` is replaced by `words\叔母.md`; three lines of `kanji\叔.md`; `kanji\伯.md` is restored to its batch-base text; one line is added to `kanji\母.md` (in `f85ff382`, that line gives the usual reading おば first); one sentence each of `words\太后.md` and `words\吟味.md` is split; the ledger is regenerated for these changes, and `manifest.json` is regenerated. Give a disposition for F4, OPT, L2 and L3, and judge the other review's note described at the end.

## F4: 叔 support and point 2

Author action: **changed**. The author's exception is withdrawn. The 叔 row now follows the letter of point 2 with a qualifying tagged spelling, so no owner acceptance is needed for it.

- **The choice: 叔母 (しゅくぼ), entry 1607100**, not 叔父 (しゅくふ), entry 1607070. You named 叔父 as the fallback; both qualify in the same way under point 2 (`evidence\rule-7058679348.md`):
  - the spelling carries ichi1/news1 (`evidence\jmdict-cited-entries.xml`);
  - the シュク reading (しゅくぼ, しゅくふ) is restricted to that spelling and carries no irregular, rare, outdated, ateji or gikun mark;
  - the other kanji (母, 父) has a card.
- **Why 叔母 and not 叔父.** 精選版 日本国語大辞典 gives a variant reading for 叔父: しゅく‐ふ【叔父】「〘名詞〙 ( 「しゅくぶ」とも ) 父母の弟。おじ。」. Its 叔母 entry, しゅく‐ぼ【叔母】「〘名詞〙 父母の妹。おば。」, gives none, and neither does Digital Daijisen for either word (`evidence\daijisen-kotobank.json`, fields `daijisen` and `nikkoku`, from the kotobank pages named there).
  - The word reading quiz always draws two generated look-alike readings when at least two exist (`evidence\Words.kt` lines 256–268, especially line 263; the generator is `mutations`, lines 234–246).
  - For しゅくふ, the five look-alikes are じゅくふ, しゅぐふ, しゅっくふ, しゅくぶ and しゅくぷ. So a 叔父 article would offer the attested しゅくぶ as a wrong option in 4 of the 10 equally likely pairs (`evidence\reading-lookalikes-c3.txt`). The app has no reading-option exclusion.
  - For しゅくぼ, the look-alikes are じゅくぼ, しゅぐぼ, しゅっくぼ, しゅくほ and しゅくぼう, none of them a recorded reading.
  - 叔母 fits the 叔 card's title, “uncle or aunt (younger than a parent)”, and Digital Daijisen's first sense of 叔, 「父・母の年下のきょうだい。「叔父・叔母」」 (`evidence\daijisen-weblio-叔.txt`), as well as 叔父 does.
- **What the learner sees.**
  - `words\叔母.md` teaches しゅくぼ. Its “Distinctive meaning” section (line 32) says that 叔母 is also read おば, that the Joyo table lists おば as the special reading, that JMdict tags おば and not しゅくぼ, and that not every printed 叔母 is pronounced しゅくぼ.
  - `kanji\叔.md`: the シュク Readings row (line 29) leads with the linked 叔母 しゅくぼ; the Common words line (34) reads “叔母 おば, also しゅくぼ”; the Notes paragraph (line 38) adds that read with シュク, 叔父 is しゅくふ and 叔母 is しゅくぼ, restricted to those spellings.
  - 伯叔 stays in the シュク row as the Joyo table's example (unlinked; entry 1474270 is still cited). Its article is deleted, and `kanji\伯.md` is back to its batch-base text.
- **Ledger.** Line 81 is now a `note` (not an `exceptionReason`), quoted in full in `CHANGES.md`; it records why 叔父 is not used. Line 29 counts two untagged-route rows (后 吏) and describes the 叔 row as qualifying. Line 955 (`status`) no longer mentions a 叔 exception.
- **Quiz safety.** `evidence\word-quiz.txt` lines 70–97: 伯母さん (same meaning), 親戚 and 親類 (“relative; kin”) are excluded; the corpus wrong reading comes from お母さん, 伯母さん (おばさん) and 母親. おばさん is not a reading of the bare spelling 叔母, and no article has the reading おば. The audit reports 0 problems (line 1436).
- **B156.** The published B156 row for 伯 (伯仲) used the interpretation you objected to here. This batch does not change B156. The author will ask the owner on issue #60 whether B156 should be aligned; that question does not affect this batch.

Please judge whether 叔母 (しゅくぼ) satisfies point 2 and whether the reason for preferring it to 叔父 (しゅくふ) holds. If you hold that 叔父 must be used, say why.

## OPT: long sentences in 太后 and 吟味

Author action: **changed**, as you suggested; no wording change otherwise.
- `words\太后.md:15`: “…and 皇太后 as the empress of the previous emperor. In a narrower sense, 皇太后 is such an empress who is also the current emperor's birth mother.” (was “…previous emperor; in a narrower sense, …”).
- `words\吟味.md:24`: “Both sources mark poetry recitation as the original meaning of 吟味. Digital Daijisen sense 3 is reciting a poem and savoring its flavor, and JMdict sense 4 (archaic) is …” (was “…original meaning of 吟味: Digital Daijisen sense 3 …”).

## L2: manifest freshness

Author action: **none**. The manifest is still evidenced by `checks\manifest.txt` (rebuild identical) and `checks\audit.txt` (fresh, `18c1f24ea8d2caf8`). The packet's `snapshot\` holds only the batch cards and the changed files, so the manifest cannot be rebuilt from the packet; this remains a transcript.

## L3: Git object and key authenticity

Author action: **evidence extended**. `evidence\verify-commit.txt` now covers `1a9bb910`, `5c04be73`, `4f8ebea7`, `54b00e0c` and `f85ff382` (each `git verify-commit -v` with its parent line) and `git log --show-signature` for the batch range. As you note, this is the author's transcript; the packet cannot authenticate the signing key independently.

## The other review's note

Another review confirmed `4f8ebea7` with one minor note on the 叔 exception text: it said the exception was “reported to the owner” before the owner had been asked, and that “the tags in those entries belong to the whole-word readings” understated the spelling tags. That text is gone with the exception. The new ledger `note` (line 81) says “The spelling 叔母 carries ichi1/news1 (the reading おば also carries ichi1/news1)”. Please judge the replacement text as a reviewer of the revised snapshot.
