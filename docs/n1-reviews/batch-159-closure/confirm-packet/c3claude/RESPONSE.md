# Author's statement for the reviewer of the confirmation report on `4f8ebea7`

This statement answers only the points in YOUR confirmation report on `4f8ebea7` (the earlier confirmation report named in `INSTRUCTIONS.md`). You confirmed `4f8ebea7`. N1 is the minor wording note in your Findings line (the 叔 exception text in ledger lines 29, 78 and 952). O2 is your comment on the 験 exclusion. LIM is the Limits points that call for an answer.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet.

What changed, in brief (`CHANGES.md` lists every line): the 叔 support article `words\伯叔.md` is replaced by `words\叔母.md`; three lines of `kanji\叔.md`; `kanji\伯.md` is restored to its batch-base text; one line is added to `kanji\母.md`; one sentence each of `words\太后.md` and `words\吟味.md` is split; the ledger is regenerated for these changes, and `manifest.json` is regenerated. Give a disposition for N1, O2 and LIM, and judge the other review's changes described at the end.

## N1: “reported to the owner” and “the tags … belong to the whole-word readings”

Author action: **superseded**. The 叔 exception is withdrawn (see change 1 below), so the sentences you noted are gone:
- line 29 (`selectionReason`) now says: “The 叔 row uses 叔母 (entry 1607100): its spelling carries ichi1/news1, and its reading しゅくぼ, restricted to that spelling, uses シュク; its support mapping explains why the equally tagged 叔父 is not used.”
- line 81 is a `note` (not an `exceptionReason`). It opens: “The spelling 叔母 carries ichi1/news1 (the reading おば also carries ichi1/news1).” It does not say that the tags belong to the whole-word readings.
- line 955 (`status`) no longer mentions a 叔 exception or the owner.

The owner will still be asked on issue #60 whether the published B156 row for 伯 (伯仲), which used the interpretation this batch has now dropped, should be aligned. That question is outside this batch; no batch-159 text depends on it.

## O2: 験 over-exclusion

Author action: **none**. As you note, 験 never competes with the curated 二 自 社 and acts only in fallback or custom pools; the exclusion stays for the sense overlap that another review raised.

## LIM

- **Owner report.** No owner decision is now needed for this batch, so its absence is no longer a limit on the 叔 row.
- **Joyo PDF.** No change: `evidence\joyo\` holds the author's extracts. The 叔 row of p75 and the 叔母 line of p162 are the pages that matter for this revision.

## Changes made for the other review

Another review confirmed every point of `4f8ebea7` except the 叔 row. It held that a disclosed exception awaiting an owner decision is not enough for publication, and asked for the qualifying 叔父 (しゅくふ) fallback or explicit owner acceptance. It also suggested splitting two long sentences. Please judge each change as a reviewer of the revised text.

1. **叔 support: 叔母 (しゅくぼ), entry 1607100.**
   - Under the letter of point 2 (`evidence\rule-7058679348.md`), 叔母 qualifies: the spelling carries ichi1/news1; the reading しゅくぼ is restricted to it, carries no excluded mark and uses シュク; 母 has a card (`evidence\jmdict-cited-entries.xml`).
   - 叔父 (しゅくふ) qualifies in the same way but is not used: 精選版 日本国語大辞典 gives the variant reading しゅくぶ (「( 「しゅくぶ」とも )」) for 叔父 and none for 叔母 (`evidence\daijisen-kotobank.json`, field `nikkoku`). The word reading quiz always shows two generated look-alikes (`evidence\Words.kt` lines 256–268); for しゅくふ, しゅくぶ is one of five, so it would be shown as a wrong option in 4 of 10 pairs (`evidence\reading-lookalikes-c3.txt`). None of しゅくぼ's five look-alikes is recorded.
   - `words\叔母.md` is new. It cites Digital Daijisen 「父母の妹。おば。」 and JMdict sense 1 “aunt”, gives two original examples, and its “Distinctive meaning” section (line 32) says that 叔母 is also read おば (the Joyo special reading, and the reading JMdict tags) and that not every printed 叔母 is pronounced しゅくぼ.
   - `kanji\叔.md` lines 29, 34 and 38: the シュク row leads with the linked 叔母 しゅくぼ, then 叔父 しゅくふ, then the unlinked 伯叔; the Common words line reads “叔母 おば, also しゅくぼ”; the Notes paragraph adds that read with シュク, 叔父 is しゅくふ and 叔母 is しゅくぼ.
   - `words\伯叔.md` is deleted; `kanji\伯.md` is back to its batch-base text; `kanji\母.md:38` adds the 叔母 line.
   - Word quiz (`evidence\word-quiz.txt` lines 70–97): 伯母さん, 親戚 and 親類 are excluded; 0 problems.
2. **Sentence splits.** `words\太后.md:15` (“…the empress of the previous emperor. In a narrower sense, …”) and `words\吟味.md:24` (“…the original meaning of 吟味. Digital Daijisen sense 3 …”). The wording is otherwise unchanged from the text you accepted.
3. **Checks.** Lint has 5 more warnings, all older conditions of `kanji\母.md` and `words\お母さん.md`, which are now in scope because 母 changed (`CHANGES.md`, “Checks”).
