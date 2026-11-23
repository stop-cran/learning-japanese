# Author's statement for the reviewer of `reports-146\confirm-gpt.md`

This statement answers only the points in YOUR confirmation report on `872d6502`: G3 (reported as partially resolved) and your
Finding 1. The statement is the author's claim about what changed and why. Verify each claim against the revised text in
`snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Line numbers refer to the revised
card. Give a disposition for each of G3 and Finding 1. Your other dispositions (G1, G2, O-A, O-B, O-C) were RESOLVED or
DECLINE ACCEPTED and are not re-asked, but report any new, established defect in the one changed card.

### G3: 牧 exclusions of 牛, 馬 and 羊

Author action: **applied.** 牛 馬 羊 are removed from `quiz_exclusions` in `牧.md:14`, together with 草, which is the same
kind of scene word ("grass; weeds"). `牧.md:53` now says that these four belong to the scene but are animals and plants, not
meanings of 牧, so they are not excluded. 畜 養 育 農 野 stay excluded because their labels ("livestock; domestic animals",
"nourish; raise; adopt", "grow up; raise", "agriculture; farming", "open field") name or closely paraphrase the first sense,
"graze and keep livestock" / "pasture; meadow; grazing land". Check whether you agree about those five.

### Finding 1: removal of the governance exclusions

Author action: **applied.** 治 御 官 司 導 are restored to `quiz_exclusions` (`牧.md:14`), and `牧.md:54` now says why: the
"govern" and official senses are taught in `牧.md:26-27`, and the displayed labels of those five cards ("govern; heal",
"honorific; govern", "government official", "take charge; official; preside", "guide; conduct") give them. 僧 坊 師 stay as the
labels related to "pastor". The list has 13 entries (the freeze list of 17 without 牛 馬 羊 草). Please check the 13-entry list
against the rule in `content-format.md` (displayed labels and ordinary meanings) and `QuizBuilder.kt:24-36`, and say whether any
of the 13 is still not defensible or any other pair is still missing.

## Process notes

- `09e376bd` is the only commit in this round. No other card changed; `quiz-safety`, `reading-exposure` and `reading-options`
  were rerun and are unchanged in result.
- The previous Claude confirmation (snapshot `872d6502`, CONFIRMED) accepted the 12-entry list; a fresh Claude agent will check
  this revision after you.
