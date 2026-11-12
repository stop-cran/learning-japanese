# Batch 110 revision: what changed from 10d79652 to 30f2bd7c

Revised snapshot: `30f2bd7c7b57e0d244a1cb86ba51e5b86121d4f8`, a child of the snapshot
`10d7965266b69ed81703ab69f20cff873a0526e9` of your follow-up report. Nothing is published. The change is the mitigation you
named in your follow-up report (F1): remove only いや from 嫌's `quizKunyomi`, update the practice-selection paragraph, and
keep everything else.

## Scope of the change

- **One card, one list.** `kanji\嫌.md` no longer selects いや for kun'yomi questions. Its full lists
  (`onyomi: [ケン, ゲン]`, `kunyomi: [きら.う, きら.い, いや]`), the いや teaching row with both linked word articles, the
  distractors, `quiz_exclusions`, title and tags are unchanged.
- **Two derived lines of `manifest.json`**: the content version and the hash of `kanji/嫌.md`.
- **Nothing else.** The commit changes 2 files (7 insertions, 5 deletions): `diffs\changed-files.txt` is the complete list,
  `diffs\delta.patch` is the exact patch of the card (without the manifest) and `diffs\manifest-delta.patch` is the exact
  patch of the manifest. No other card, no stroke file, no word article, no document and nothing in the Android client
  changed. The other 14 cards in `snapshot\kanji\` are byte-identical to your earlier packets.

## The card, line by line

Line numbers refer to `snapshot\kanji\嫌.md` in this packet (`diffs\changed-lines.txt`: `kanji/嫌.md: 12, 37, 43-45`).

| Line | Before (`10d79652`) | After (`30f2bd7c`) |
| --- | --- | --- |
| 12 | `quizKunyomi: [きら.う, きら.い, いや]` | `quizKunyomi: [きら.う, きら.い]` |
| 37 | The いや row of the `## Readings` table ended `…いやがる — show dislike; seem unwilling |` | It ends `…いやがる — show dislike; seem unwilling; not selected for questions here |` (the same closing words that the ケン row at line 33 already uses) |
| 43 | `Practice selects ゲン, きら.う, きら.い and いや, the readings with linked word articles. ケン is retained from KANJIDIC2 …` | `Practice selects ゲン, きら.う and きら.い, readings with linked word articles. ケン is retained from KANJIDIC2 …` (the ケン sentence is unchanged) |
| 44 | (existing blank line, now line 46) | new blank line |
| 45 | (none) | new paragraph, 62 words (quoted below) |

The new paragraph, line 45:

> いや also has linked word articles but is not selected either: JMdict lists や as a further reading of 嫌, Digital Daijisen
> explains it as a sound change of いや, KANJIDIC2 does not list it, and a question about いや could show や as a wrong
> option. This is a teaching selection, not a claim that いや is invalid, obsolete or rare.

Counted as whitespace-separated tokens, the revised line 43 has 39 words (it had 41) and the new paragraph has 62; both are
within the 100-word guideline for card paragraphs.

## What the change does to the quiz

With `quizOnyomi: [ゲン]` and `quizKunyomi: [きら.う, きら.い]` the card can ask exactly two prompts: ゲン (on) and きらう (kun;
きら.う and きら.い share the stem きら, so they are one card). The prompt いや is gone, so 嫌 has 2 reading prompts instead of 3
(the batch's reading-prompt list has 25 entries instead of 26). The reading-quiz guard still protects いや: wrong options
for 嫌 are checked against the full `onyomi` and `kunyomi` lists, which still contain いや and ケン (the seven excluded keys
are unchanged). `RESPONSE.md` (N4 to N6) gives the details and the anchors.

## Links and titles on the changed lines

Line 37 is the only changed line with links, and the two links are unchanged (only the suffix after them was added).
`checks\link-targets.tsv` lists them: `words/嫌.md` with the title "unpleasant; unwanted" and `words/嫌がる.md` with the title
"show dislike; seem unwilling"; 2 links on changed lines, 0 unresolved or mismatched. Lines 12, 43 and 45 contain no links.

## Gate results before and after

The same gate script was run on both snapshots; the logs of this snapshot are in `checks\` (the check files there have blank
lines removed, except the five plain copies listed in `evidence\README.md`).

| Check | At `10d79652` | At `30f2bd7c` |
| --- | --- | --- |
| lint (`checks\lint.txt`) | 0 error(s), 17 warning(s) | 0 error(s), 17 warning(s); none concerns `kanji/嫌.md` (two concern the word articles 嫌い and 嫌がる, which this delta does not touch) |
| tools unit tests (`checks\unittest.txt`) | Ran 431 tests, OK | Ran 431 tests, OK |
| validate (`checks\validate.txt`) | 0 error(s) | 0 error(s) |
| archive budget (`checks\budget.txt`) | retainedBytes 45175860, inflatedBytes 45447170, localZipBytes 30574988 | retainedBytes 45176219, inflatedBytes 45447529, localZipBytes 30575129 (files 8548, entries 8563 and listeningTaskMediaBytes 5893602 unchanged) |
| vocabulary (`checks\vocabulary.txt`) | Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot | the same |
| manifest rebuild and `git diff --exit-code` (`checks\manifest.txt`) | exit 0, version `eb332dd7994dd3ba` | exit 0, version `18d0f3df4071aa30` (8541 files, as before) |
| quiz safety (`checks\quiz-safety.txt`) | 0 error(s), 0 warning(s) | 0 error(s), 0 warning(s) |
| reading options (`checks\reading-options.txt`) | 0 problem(s) | 0 problem(s); the run now gets `--extra 嫌=や` because the card text names や |
| Android JVM gates (`checks\jvm.txt`, `checks\jvm-readings.txt`) | BUILD SUCCESSFUL | BUILD SUCCESSFUL |
| reading exposure, scan of every card (`checks\reading-exposure.txt`) | 888 prompts, 331 collisions, 19 whole-stack hits, 13 Starter-session-only hits; 0 production hits, 1 padded-session hit, 5 latent collisions | 887 prompts, 330 collisions, 19 whole-stack hits, 12 Starter-session-only hits; 0 production hits, 0 padded-session hits, 5 latent collisions |
| real Kotlin runs against the pinned Android commit, compared with the Python analysis (`checks\kotlin-vs-exact.txt`) | 52 whole-stack, 26 Starter-session and 32 small-pool prompts; 0 problem(s); 0 HIT; 1 PAD-HIT; 4 NOTE | 50 whole-stack, 25 Starter-session and 26 small-pool prompts; 0 problem(s); 0 HIT; 0 PAD-HIT; 3 NOTE |

The 19 whole-stack hits and 12 Starter-session-only hits of the scan are leads of the author's heuristic scan on other
cards of the content; they are not part of this batch's scope and `RESPONSE.md` (D5) says how the author treats them.
`diffs\checks-vs-followup.diff` (the four plain copies that your follow-up packet also had) and
`diffs\reading-options-vs-confirm.diff` (`reading-options.txt`, which only your confirmation packet had) show every
difference between the five plain copies of this packet and the earlier packets' copies; `evidence\README.md` explains
each kind of difference. The other check files are compared in the table above.
