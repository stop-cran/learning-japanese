# Author's statement for the reviewer of `reports-145\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 to C10 and O1 to O9 are your report's own labels.
The statement is the author's claim about what changed and why. Verify each claim against the revised text in
`snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers refer to
the revised cards in this packet; other line numbers refer to the named file in the original packet unless stated.
Eight new cards (漫 漬 潜 濁 瀬 災 炎 為), the existing card 暑 and the word article 湧く changed; see `CHANGES.md`. No
front matter changed in any card. Give a disposition for each of C1 to C10 and O1 to O9.

## Findings

### C1: 漫 lists すず where Daijisen prints すずろ

Author action: **changed** as you proposed. `漫.md:46` now says Daijisen's entry also lists すずろ and そぞろ. The
reading audits' `--extra` input for 漫 had the same truncation; it was corrected and the audits were rerun (see
`CHANGES.md`).

### C2: 暑 says 炎 names fire rather than weather heat

Author action: **changed**. `暑.md:49` (the declared remark edit; `evidence\kanji-remarks.json` is updated) now reads
`炎, "flame," mainly names fire, but in 炎天 and 炎暑 it also means blazing heat, so the 炎 card keeps 暑 out of its
meaning choices.` `炎.md:57` now says the 暑 card notes that 炎 mainly names fire. Verify the new wording is true and
that the pair of statements is consistent.

### C3: 浪漫 should be given as ロマン

Author action: **changed**. `漫.md:30` now gives ロマン as a JMdict ateji spelling whose reading ろうまん is only a
rarely used kana form (JMdict 1147940).

### C4: 濁 implies ジョク is a table reading without an example

Author action: **changed** as you proposed. `濁.md:46` now says the table does not list ジョク, that KANJIDIC2 lists it
and that Kanjipedia marks it as outside the table.

### C5: 為 "first sense" and "for the same doing"

Author action: **changed** as you proposed. `為.md:23` says JMdict glosses it (no "first sense"); `為.md:25` lists ため
among the kun readings without "for the same doing".

### C6: 為 never says the table gives no kun reading

Author action: **changed**. `為.md:44` adds `The table lists no kun reading for 為; な.す and the other kun readings are
outside the table.` The suggested "and are usually written in kana" was not added because that claim is not cited in
the packet. Verify the sentence is true and sufficient.

### C7: 防災 gloss

Author action: **changed**. `災.md:25` quotes "protection against disaster" (JMdict 1520360).

### C8: 漬物 headword

Author action: **changed**. `漬.md:41` says the entry is 漬物 (JMdict 1433700), with 漬け物 as another spelling and
漬けもの as "search-only kanji form".

### C9: 原潜 gloss with the tag inside the quotes

Author action: **changed** as you proposed. `潜.md:30` reads JMdict "nuclear submarine," tagged "abbreviation."

### C10: Daijisen paraphrases in double quotes (災 and 為)

Author action: **changed**. `災.md:25` and `為.md:25` now present the Daijisen わざわい and ため descriptions as
unquoted paraphrases.

## Optional

- **O1 (炎 "and"): applied.** `炎.md:57`.
- **O2 (為 checker sentence): applied.** `為.md:42` now reads `な.る and な.す share the stem な, so this card claims only
  what the linked word supports`.
- **O3 (漬 stagk): applied.** `漬.md:23` is plain English; the `spec1` tag note after 浸かる (`漬.md:39`) was removed too.
- **O4 (瀬 年の瀬): not applied.** Optional extra example; the card's reading coverage is complete without it.
- **O5 (漫 漫才): not applied.** Same reason.
- **O6 (滑 Kanjipedia wording): not applied.** The line is accurate as written.
- **O7 (滞 Notes wording): not applied.** The exclusion is symmetric and functionally correct.
- **O8 (為 exclusions 業 and 理): not applied.** Exclusions only remove options; none creates an ambiguity.
- **O9 (瀬戸物 diff): not applied.** It matches the link-wrap rule.

## Process notes

- `e07ab312` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `845aefbb`.
- The checks in `checks\` were run on the committed revision.
