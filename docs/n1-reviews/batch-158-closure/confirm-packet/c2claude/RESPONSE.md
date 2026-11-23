# Author's statement for the reviewer of `b158-confirm-reports\claude.md`

This statement answers only the points in YOUR confirmation report on 6605a8b0. F1 is your Finding 1, and O1 is your Optional
note. Two of your Limits raise points this packet can answer; they are L1 and L2 below. Your other Limits describe your own method and
need no answer. The statement is the author's claim about what changed and why. Verify each claim against the revised text in
`snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as
evidence. Line numbers refer to the revised files in this packet. Only `words\升.md` (two body lines), the ledger
`docs\n1-sources\batch-158-progress.json` (one line), the pinned JMdict selection and extract (one added entry) and the
regenerated `manifest.json` changed. Every batch kanji card and every other word article is unchanged since 6605a8b0. See
`CHANGES.md`. Give a disposition for each of F1, O1, L1 and L2.

## Findings

### F1: the word 升 excludes 腰掛け although the titles no longer overlap

Author action: **kept, with the reason now stated on the article**. You offered two remedies: keep the exclusion with a stated
reason, or remove it. The author kept it.

- **Why it is kept:** the article still teaches JMdict 1346290 sense 2, “box (seating at a theatre, etc.)”, with 升席 at line 15.
  A learner who has read that sense could take 腰掛け “seat; bench” as a correct answer for 升. The exclusion only removes 腰掛け
  from 升's options and 升 from 腰掛け's options; it adds no wrong option anywhere.
- **Where the reason is:** `words\升.md:28`, at the end of the Synonyms paragraph: 腰掛け is a seat or bench (JMdict entry
  1288370); in its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench. Line 34 adds 1288370
  to the compared entries. `evidence\jmdict-cited-entries.xml` now holds entry 1288370.
- **Why the article and not the ledger:** the ledger's word-exclusion row for 升 (`docs\n1-sources\batch-158-progress.json`,
  lines 327–338) lists the exclusions copied from the front matter, without reasons, like every other row. The Synonyms
  paragraph already compares 箱 and 容器, and it is the text the learner sees.
- **Why 腰掛け differs from 席, 座席 and 客席:** your report noted that the author left 席, 座席 and 客席 unexcluded. The difference
  is reachability, not meaning. `evidence\Words.kt` lines 197–199 score a candidate as 2 per shared tag, plus 1 for the same type
  and 1 for a shared kanji.
  - 腰掛け is type wago with the tags wago, noun, furniture and posture: score 5 against 升. That is the last-slot score, with
    668 tied words (`evidence\word-quiz.txt`, block from line 1690), so without the exclusion 腰掛け could be drawn.
  - 席, 座席 and 客席 are type kango and share only the tag noun: score 2, below the last slot, so they are never offered.
  - The author judged that a sense-2 overlap is worth guarding where the word can actually be drawn. Please say whether you
    accept this, or still prefer removing 腰掛け.

## Optional note

### O1: split the 偏見.md:28 sentence about 意見

Author action: **not changed**. Each of the ten B158 word articles has a one-paragraph Synonyms section, and `words\偏見.md:28`
follows that pattern. The 升 sentence above was also folded into its existing paragraph for the same reason. The app wraps a
long paragraph on a phone; the 意見 sentence is the last sentence of the paragraph and stands on its own.

## Limits answered

### L1: the added JMdict entries were not verified as complete and unmodified

Author action: **evidence pointer**. The extract `docs\n1-sources\batch-158-jmdict.xml` is written by
`tools\extract_n1_jmdict.py --pin continuation`. Its `--check` mode checks the input's SHA-256 against the pin, re-extracts
every selected entry from the pinned input and requires the committed extract to be byte-identical. The author ran it at
ccc046bb; `evidence\jmdict-check.txt` holds the command, both hashes and the result, “Verified 87 complete JMdict families”.
`checks\audit.txt` also reports 87 complete JMdict families. `evidence\jmdict-cited-entries.xml` holds the same complete
entries; you can compare any of them with today's online JMdict, which may differ slightly from the pinned file.

### L2: the claim that no candidate written with 升 carries a qualifying tag was not verified

Author action: **new evidence**. `evidence\jmdict-entries-with-升.txt` lists every entry of the pinned JMdict (same input hash as
in `evidence\jmdict-check.txt`) with 升 in any written form: 19 entries, with the priority markers of each written form and
reading, sense 1 glosses, and the qualifying markers of the issue #60 rule (news1, ichi1, spec1, gai1). None of the 19 has a
qualifying marker. 1346290 升 ます is the only entry with any marker (news2, nf37 and spec2). The author made the list with a
one-off scan of the pinned file; it is not a repository tool.
