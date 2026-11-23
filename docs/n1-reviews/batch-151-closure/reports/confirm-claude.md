# Batch 151 confirmation review (Claude)

Snapshot: commit 15441514ec9a0a3835921e2031f7d79bec6c8920 (reviewed snapshot was b624890f). Reviewer model: Claude (Anthropic), running as GitHub Copilot; the exact model version is not exposed to me. I am the same reviewer who wrote `reports-151\initial-claude.md`. I worked alone and read-only, apart from writing this file.

Scope:
- **Read in full:**
  - INSTRUCTIONS.md, CHANGES.md, RESPONSE.md and my initial report.
  - `diffs\fix.patch` (178 lines), `diffs\changed-lines.txt` and `evidence\README.md`.
  - The nine revised cards in `snapshot\kanji\`: 誓 誘 謙 譲 護 豆 豪 貢 貴.
  - `evidence\QuizBuilder.kt` and `evidence\distractor-trials.txt`.
  - The KanjiVG group structure of `evidence\kanjivg\08b19.svg` (謙) and `08cb4.svg` (貴), with path data stripped.
  - `checks\quiz-safety.txt`, `checks\reading-options.txt` (all 15 sections), `checks\link-targets.tsv`, `checks\lint.txt`, `checks\validate.txt`, `checks\unittest.txt` and `checks\kanji-remarks.txt`.
- **Read in part:**
  - `evidence\KanjiReadings.kt`, lines 1-151: ReadingKey, ReadingCard, KanjiReadingQuiz and the start of the queue.
  - `checks\reading-exposure.txt`: the header, the 訴/証/詩 sections, the whole 譲 section and the summary lines.
  - `evidence\jmdict-cited-entries.xml`: the complete entries 1266440 (呼ぶ) and 1357030 (譲る).
  - In the original packet: a listing of its top level and the 縫 diff.
- **Searched:** a grep of the revised cards for "declaring", "declares" and "example word".
- **Not opened:** the six unchanged cards (訴 証 詩 詳 誇 謡); they are covered only through the quiz checks.
- **Web:** one jisho.org fetch for 譲る returned only page chrome and verified nothing.

Dispositions:
- **C1 - RESOLVED.** `貴.md:25` now says 中 "sits at the top on a horizontal stroke 一", with 貝 at the bottom. KanjiVG `08cb4.svg` groups 中 as strokes 1-4 (口 1-3 and 丨 4), has an ungrouped ㇐ as stroke 5, and groups 貝 as strokes 6-12 (目 6-10 and 八 11-12). That makes 12 strokes, which matches `strokes: 12`. The picture sentence still fits.
- **O1 - RESOLVED.** `謙.md:25` now reads "八 … at its top, then a horizontal stroke, the shape ⺕, two vertical strokes 丨 and two final sweeping strokes." In `08b19.svg`, 兼 has a variant 八 as strokes 8-9, ㇐ as stroke 10, ⺕ as 11-13, 丨 as 14 and 丨 as 15, then ㇒ and ㇏ as 16-17. With 言 as strokes 1-7, the total is 17 and every stroke is accounted for.
- **O2 - DECLINE ACCEPTED.** 看護婦 remains the only word article with 護. The card states its obsolete status, the JMdict cross-reference to 看護師 (1928100) and the Joyo example 保護 (`護.md:23,31,37`). Adding a new word article is a reasonable deferral beyond this batch's scope, and my point was optional.
- **O3 - RESOLVED.** `誓.md:31-33` now lists セイ, then ゼイ, then ちか.う. The row texts are byte-identical to before (patch hunk), and the front matter is unchanged.
- **O4 - DECLINE ACCEPTED.** This was optional coverage polish. Scoped coverage was clean, and adding sourced claims at confirmation stage only enlarges the review surface.
- **O5 - RESOLVED.** The set I suggested was not used, but the point (closer, more useful distractors than 食 行 来) is addressed.
  - **New set:** `譲.md:13` lists 買 話 読. The prose at `譲.md:57` is true: JMdict 1357030 sense 4 is "to sell", and 話 and 読 both have the radical 言, as 譲 does.
  - **Why 奪 and 受 were rejected:** I checked the author's reason against the app code. `KanjiReadingQuiz.question` takes curated readings only from cards in the pool (`byKanji[it]`). A Starter "Practice more" session contains only Starter cards plus borrowed ones. Non-Starter curated cards such as 奪, 受, 拾, 借 and 握 are therefore missing there, and the fallback fills the open slots. If the session also borrows 攻 or 責, the fallback can offer せめる, a reading attested for 譲 that is outside its metadata, so `excludedKeys` does not block it.
  - **Trials:** `distractor-trials.txt` shows exactly that one-holder hit (攻 and 責) for all six sets that contain 奪, 受, 拾, 借 or 握. It shows none for 買 話 読, whose three cards are all tagged starter (`reading-exposure.txt`, 譲 section).
- **O6 - DECLINE ACCEPTED.** The original 縫 diff shows that the dropped clause ("this does not change the complete word's reading") qualified "It has no kanji card here yet". Once 裁 is linked, the qualification has nothing left to qualify. `kanji-remarks.txt` reports the edit as a declared, remark-only change.

Verdicts:
- **Correctness: CLEAN.** I checked every changed hunk:
  - 誘:51: JMdict 1266440 sense 3 is "to invite" (pinned entry), and 1266440 is added to the Metadata line (line 59).
  - 誘:45: the exclusion list (line 14) and the bullets (lines 47-55) both name 13 cards.
  - 謙:25 and 貴:25: both match KanjiVG.
  - 譲:57: true.
  - The "example word" rewording on 護:23,51, 豆:23, 豪:23,52, 貢:23,46 and 貴:23 is accurate.
  - 誓: the rows were only reordered.
- **Scoped coverage: CLEAN.** The revision removes no reading, word or sense.
- **Consistency and quiz safety: CLEAN.**
  - **Links:** all 19 links on changed lines resolve. Every quoted gloss on a changed line equals its target title (`link-targets.tsv`). No "declaring word" remains in any batch card; "declares the … pair" in 詩:50 and 謙:50 is a different, still correct use.
  - **Meaning options (QuizBuilder):** `excluded()` is symmetric and also checked between the chosen options. Curated distractors are tried first, then tag-similar cards.
    - In `quiz-safety.txt`, all 15 cards show three curated wrong titles, and none of them is a correct meaning. 譲 now shows buy | talk, speak | read. Buy is the opposite of 譲る's "to sell", not a sense of 譲. 買 is not in 譲's exclusions (売 and 販 are), so no exclusion overlaps a distractor.
    - 誘 losing 訪: "visit; call on" is not a meaning of 誘 ("invite; tempt"), and "invite; tempt" is not a meaning of 訪. The pair is safe in both directions. In full pools, 誘's curated 攻 舞 握 fill every slot anyway.
  - **Reading options:** 譲's kun prompt ゆずる now draws only かう, はなす or はなし, and よむ. None of them is a reading of 譲, and 0 fallback is used in the N1, All and Starter pools. The other 14 prompts are unchanged (`reading-options.txt`: 0 problems; `reading-exposure.txt`: 0 production, padded or one-holder hits, with the same 3 latent collisions). 誓's tier-3 candidates include さそう (誘), which is harmless as a wrong option for ちかう.
- **Comprehensibility: CLEAN.**
  - The 謙 and 貴 stroke descriptions stay short and readable on a phone.
  - "Example word" is clearer for a beginner than "declaring word".
  - The 譲 distractor rationale is one plain sentence.

Confirmation: CONFIRMED

Findings: none.

Optional:
1. **"Example word" in two senses:** `護.md:23` and `豪.md:23` now use "The example word X" (the linked article) and "A Joyo example word is Y" in the same paragraph. A beginner could read 保護 and 豪雨 as equally "the" example. "The Joyo table also gives Y as an example" would separate the two. This is purely editorial.
2. **Strength of 話 and 読 as distractors:** they are still easy to eliminate by meaning; their pull is visual, through the shared 言. This is acceptable given the documented exposure constraint, and I am not raising it as a defect.

Limits:
- **Not verified on the live web:** JMdict and KanjiVG. I relied on the pinned extracts in `evidence\`. My one web fetch (jisho.org) returned no entry content.
- **Not re-read:** the six unchanged cards (訴 証 詩 詳 誇 謡) and the unchanged word articles. My initial review covered them; this round I checked them only through `quiz-safety.txt`, `reading-options.txt` and `reading-exposure.txt`.
- **What the audits cannot show:**
  - `quiz-safety.txt` reports the full-pool option lines only. It cannot show which titles the tag fallback draws for meaning questions in a Starter session that borrows a card whose curated distractors are not Starter cards, as happens for 誘. I did not enumerate the Starter titles. 訪 is unlikely to be a Starter card, but I did not confirm that.
  - The reading audits depend on the completeness of the `--extra` list of attested readings.
- **Not opened:** `KanjiReadings.kt` beyond line 151 (queue scheduling) and `Words.kt` (`ReadingOptions.mutations`). I treated the mutation behaviour as described.
- **Not run:** the Android JVM tests that read the real content (author's statement).
- **Not checked:** I did not open 訪.md, so I could not check whether 訪 still lists 誘 in its own exclusions. Either way the pair stays safe.
- **Tool use:** every response contained exactly one tool call. I used no sub-agents or background jobs, and I read no paths outside the allowed set.
