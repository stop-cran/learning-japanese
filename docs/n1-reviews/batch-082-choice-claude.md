# SAME082 runtime-choice reconciliation (proposal not applied)

The concern I flagged as optional is now a real, low-severity issue at `准.md:13`: the hand-picked quiz distractors never appear in the N1 quiz. The proposed swap to `[冴, 冶, 隼]` is justified and needs no corrections. It closes the issue in principle, but no host or native run has tested it yet.

## Snapshot

- **Signed snapshot:** cadd1054ff865b7c08fdeaff19f0439a02cf5073.
- **Packet hash (as supplied, not checked by me):** d5d27086…d9a8.
- **Earlier evidence:** visual HEAD 276df595, teaching snapshot b6bcc8f1, Android test build 1c1b7bf4 on production baseline f9b59a2.
- **Model:** Claude Opus 5.5 (claude-opus-5.5). Only `view` was available.

## Scope

**What I read:**
- I read `docs\n1-reviews\batch-082-choice-reconciliation-packet.txt` with one view call. There was no truncation notice and no denied access.
- The packet contained 12 complete sources: the cards 准, 倣, 冴, 冶 and 隼; the word articles 冴える, 冶金 and 隼; the eleven JMdict entries; the four KANJIDIC2 records; and the source-evidence and runtime-investigation JSON files.
- The embedded files add up to about 1535 numbered lines plus headers, which fits the stated 1561. I did not count the packet's own lines.

**What I did not do:**
- No Git, upstream or hash verification.
- No fresh dictionary lookups. The Kotobank observation came from the coordinator, not from my own retrieval.
- Nothing new was run: no host or native tests, no screenshots.

## How the default N1 quiz chooses wrong options

This is proven from the supplied production code excerpts.

- **Only cards in the selected study set are eligible.** `QuizViewModel.kt:91,97` builds the quiz from that set alone. In the N1 set, that means N1 cards only.
- **Hand-picked distractors outside that set are dropped.** `QuizBuilder.kt:24` keeps a listed distractor only if it is in that pool. 集 is N4 and 進 and 難 are N3, so none of them can appear in the N1 quiz.
- **The empty slots are filled by tag similarity.** `QuizBuilder.kt:25–26` adds cards sharing the most tags with 准, in shuffled order.
  - 准 has the tags jlpt-n1, grade-8 and structure-unclassified. 倣 has exactly the same three, so it is in the most-preferred group.
  - So "imitate; emulate" is a structurally favoured choice, not a one-off. How often it appears depends on how many cards share all three tags, which I could not establish.

## Is "imitate; emulate" actually wrong for 准?

The meaning overlap is real but involves rare spellings. Rare is not the same as invalid.

**Evidence for overlap:**
- JMdict entry 1341500 lists 准える as a "rarely used kanji form" of なぞらえる. Its second sense includes "to imitate" and "to pattern after", and the word is usually written in kana.
- 准じる and 准ずる are also rare kanji forms. Their senses (correspond to, follow) are close to 准's "quasi" meaning.
- Daijisen's 准 entry gives なぞらえる as its kun label. The excerpt shown is 「主たるものになぞらえる。準ずる。」
- KANJIDIC2's Spanish meanings include "imitar".

**Evidence against treating it as a main sense:**
- KANJIDIC2's English meanings are only quasi-, semi- and associate.
- Nothing establishes "imitate" as a common standalone sense of 准.

**Conclusion:** "imitate; emulate" is not clearly wrong for 准, but it is not proven to be a common sense either. That is enough to mean the default quiz can present a debatable wrong option. The cause is proven; how much it affects learners is not.

## Is the proposed swap justified?

Yes. Each of the three replacements is clearly wrong in meaning and plausible in shape:

| Option | Meaning shown | Other senses in sources | Overlap with 准? | Shape similarity |
|---|---|---|---|---|
| 冴 | clear; sharp-minded | clear or vivid, alert, skilful, upbeat, intensely cold (old) | None with rank, approval or model-after | Same 冫 on the left, different right side |
| 冶 | smelt; work metals | melting; 陶冶 can mean training or cultivation | None with 准's senses | Same 冫, 台 on the right instead of 隹 |
| 隼 | falcon | broader falcon use; a figurative "brave person" sense (Kanjipedia, recognition only) | None | Shares 隹; has 十 below and no 冫 on the left |

- **Small risks, all acceptable:**
  - 隼 also reads ジュン, but the meaning quiz shows only meanings, so that doesn't matter here.
  - 冶's "training" sense (via 陶冶) is not its displayed meaning, and 准 doesn't mean training.
  - 准's mnemonic pictures 隹 as a bird, so 隼 "falcon" is a tempting but wrong choice, which is what a distractor should be.
- **All three would be used.** All three are N1 cards with distinct titles. That means three valid listed distractors fill every slot in both the N1 and All quizzes, so the fallback (and with it 倣) is never reached.
- **Nothing else changes.** Readings, title, prose, links and app code stay as they are. The existing look-alike note about 集/進/難 at lines 58–60 is still accurate and can stay.
- **Remaining conditions:** 冴, 冶 and 隼 must actually be in the synced N1 data with these titles. This has not been checked at runtime.

## Verdicts

**Current snapshot (cadd1054):**

| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `准.md` title, prose and readings | CLEAN | CLEAN | CLEAN |
| `准.md:13` quiz distractors (default N1 quiz) | NEEDS FIX | NEEDS FIX | CLEAN |
| `准教授.md`, `教.md:39`, `助教授.md:16` | CLEAN (unchanged from my earlier review) | CLEAN | CLEAN |

**Proposed `distractors: [冴, 冶, 隼]`:**

| Basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Content and source review | CLEAN | CLEAN | CLEAN |
| Runtime acceptance | UNVERIFIED | UNVERIFIED | UNVERIFIED |

## Findings

**1. Hand-picked distractors never reach the N1 quiz.**
- **Severity:** low.
- **Facet:** correctness and scoped coverage of the quiz options.
- **Location:** `kanji\准.md:13`.
- **Problem:** in the default N1 quiz, 集, 進 and 難 are never offered. The fallback can show "imitate; emulate", which overlaps a documented (rare-spelling) meaning of 准. A learner could be marked wrong for a defensible choice, though the target title is still the best answer.
- **Remedy:** the proposed one-line change to `[冴, 冶, 隼]`. No other changes are needed.
- **Evidence:** `QuizViewModel.kt:91,97`, `QuizBuilder.kt:24–26`, the captured options (whale, imitate; emulate, quasi-; associate rank, crown; peerless), JMdict 1341500/1341510/1341520, Daijisen's なぞらえる, and KANJIDIC2 "imitar".
- **Confidence:** high that the mechanism works this way; moderate on the semantic impact.

## How my earlier concerns now stand

- **"imitate; emulate" (my visual-report Optional 1):** upgraded from a low-risk hypothesis to Finding 1. The proposal resolves it in principle for the default N1 and All quizzes. At runtime it is unresolved until the change is applied and retested.
- **A wrong assumption in my original review:** I said 準's hand-picked distractors (集/清/卒) protect its default quiz. That assumed listed distractors are always used, and they are not when they fall outside the selected level. I now treat that claim as unverified.
- **The broader concern about larger, uncurated quiz pools** is outside this proposal and still unresolved.

## Optional

- 准's Notes could mention 冴 and 冶 as shapes that share 冫. This is not required.
- Other cards whose listed distractors are all outside their own level probably fall back the same way. That is a whole-set and app-design question, and a hypothesis here, not a finding.

## Limits

- The proposal is not applied. After the edit, the following are still needed:
  - fresh host and native runs
  - checks that the actual options shown are exactly 冴, 冶, 隼 plus 准
  - new screenshots
- The earlier native test passing does not show that only one option is correct.
- All runtime facts (code excerpts, captured options, N1 membership) were supplied to me, not run by me.
- Still unresolved from before:
  - physical phone, native speaker and learning effectiveness
  - final integration, publication and CI
  - general release
  - the whole set
  - larger or custom quiz pools and any future change to how options are chosen
- All read-depth, OOM, denial and ML Kit limits from earlier phases still apply.
