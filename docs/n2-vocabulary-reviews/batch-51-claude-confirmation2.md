I found no new defects in correction2, and all five of my earlier findings (B51-F1–F3, B51-C1, B51-C2) are resolved.

## Snapshot
- **Commit:** `0a2b27a7c7a86ac430f1ef367f5a0928607b8aba`; parent `0e73b4e0028a0bb74940f2dbdc10e7890bb24ef9`. Both come from correction2-snapshot.json. Its "committed content only" and "clean" flags are the author's checks.
- **Changed files listed:** `words/たちまち.md`, `words/ためらう.md`, `docs/n2-vocabulary-sources.tsv`.
- **Limitation:** file tools can't run Git, hashes or cleanliness checks, and I didn't look in `.git`. I assume the working-tree files I read match that commit.

## Scope
**Model:** claude-opus-5.5 (Claude family). Read-only throughout: no edits, agents or delegation.

**Read in full this turn:**
- correction2-snapshot.json and correction2.patch, including the one TSV note change.
- words\たちまち.md and words\ためらう.md.
- followup-comparison-reading.txt: the five complete families 1001400, 1005190, 1164040, 1275250 and 1609210.
- followup-existing-reading.txt: the five full old bodies 一度に, おどおど, 効力, 一斉 and さっさと.
- For comparison: words\妥当.md, 有効.md, 急速.md and どんどん.md.

**Read in part this turn:**
- followup-review-evidence.json, the `confirmationFollowup` section only: lines 25260–25300 and 25600–25825. I didn't read the JSON copy of the families at 25300–25600; the .txt rendering covers them.
- principal-reading.txt:38–50 and 152–162.
- The N2:1006 TSV row in full. For the other nineteen rows I only checked by pattern that all twenty are batch 51, draft, `words/`.
- Line checks of `kanji\畳.md`, `kanji\線.md`, `kanji\袋.md`, and of 成立's title and exclusions.
- Title searches across `words\` for instant/sudden/at once/immediately/quick/rapid/hesitate/timid.

**Fresh retrieval:** the jisho API page for 急速. It is JMdict-derived, but its version isn't the pinned snapshot.

**Carried over without rereading:**
- 例える, 溜まる, 溜める and だらしない: full rereads at the first confirmation; unchanged since.
- The other thirteen articles: full reads in the initial review; unchanged.
- The full bodies of all three kanji cards.

**Never fully read in any round:** family-inspection-01 to 10 and public-bodies.json.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1002 | 助かる (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1003 | 但し (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1004 | 畳む (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1005 | 立ち止まる (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1006 | たちまち (new) | Fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1007 | 建つ (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1008 | 発つ (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1009 | 脱線 (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1010 | 妥当 (new) | Fresh full view; unchanged since 1st correction | CLEAN | CLEAN | CLEAN |
| N2:1011 | 例える (new) | Carried over from 1st-confirmation reread | CLEAN | CLEAN | CLEAN |
| N2:1012 | 頼もしい (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1013 | 足袋 (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1014 | ダブル (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1015 | だます (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1016 | 溜まる (new) | Carried over from 1st-confirmation reread | CLEAN | CLEAN | CLEAN |
| N2:1017 | ダム (new) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1018 | ため息 (new; source 溜息) | Carried over from initial review | CLEAN | CLEAN | CLEAN |
| N2:1019 | ためらう (new) | Fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1020 | 溜める (new) | Carried over from 1st-confirmation reread | CLEAN | CLEAN | CLEAN |
| N2:1021 | だらしない (new) | Carried over from 1st-confirmation reread | CLEAN | CLEAN | CLEAN |

**Mappings: CLEAN.**
- All twenty rows N2:1002–1021 are present: batch 51, draft, `words/<word>.md`.
- In `n2-vocabulary-sources.tsv:1006`, only `source_note` changed. Entry 1288480, senses `1,2`, empty additional senses and the identity note are unchanged.
- The new note is accurate. Each claim matches the current guards and the 一斉 title and body, and it resolves my earlier optional point about a stale note.
- The packet's `sourceNote` (evidence line 100) is identical to the TSV text.

**Kanji reciprocity: CLEAN** (line checks; full bodies carried over).
- `畳.md`: たた.む row at 30, Common words 39, note 44, source 1356780 at 47.
- `線.md`: セン row with 脱線 at 30, entry at 45, source 1416560 at 53.
- `袋.md`: whole-word たび (足袋) row at 33, entry 41, note 48, and 1404920 in the final list at 50.

**Baseline preservation: CLEAN.**
- Correction2 changes only the three listed files.
- The old-article titles I checked (一度に, おどおど, さっさと, 一斉, 有効, 急速, どんどん) are unchanged in the current tree.

**First-round corrections: all eleven still in place.** `currentQuizDeclarations` (evidence 25639–25780) still contains:
- たちまち: すっと, 一瞬
- 妥当: 成立, 適する, 立つ
- 溜まる and 溜める: 重なる
- ためらう: ぐずぐず
- だらしない: ぐしゃぐしゃ, だらだら
- 例える: 例え

**Guard count:** my own sum is 105 across 18 cards, matching the author's figure.

## Findings
**Earlier findings, all resolved:**
- **B51-F1 (例え):** still in 例える's current list, confirmed from the evidence packet.
- **B51-F2 (一瞬):** still in たちまち.md:9.
- **B51-F3 (1404920 citation):** present at 袋.md:50.
- **B51-C1 (たちまち/一度に):**
  - Fixed at たちまち.md:9.
  - The pair is justified: 1609210:1 is the bare gloss "all at once", which 1288480:2 also uses. 一度に's title is an unqualified "all at once", and たちまち.md:43 explicitly teaches that rendering.
- **B51-C2 (ためらう/おどおど):**
  - Fixed at ためらう.md:9.
  - The pair is justified: 1001400:1 includes "hesitantly". おどおど's title and body cover hesitant behaviour, e.g. "The boy hesitantly gave his name."
  - My earlier failed fetch is superseded by the author's capture.

**Author-adopted たちまち/さっさと guard: accepted, not excessive.**
- 1005190:1 ("quickly; promptly; immediately; without delay…") and 1288480:1 ("…immediately; right away; at once") share "immediately".
- たちまち already guards すぐに, 直ちに, 早速 and すっと, all of which さっさと also guards.
- The two words differ (deliberate manner versus sudden result), but a learner could plausibly accept either title for either word. The cost is one fewer distractor.
- No ためらう/さっさと guard is needed: "without hesitation" is an antonym.

**Declined candidates: both accepted.**
- **一斉:**
  - 1164040's "all at once" sits beside "simultaneous", i.e. acting together. 1288480:2 sits beside "suddenly".
  - 一斉's title carries the "simultaneous" qualifier, and たちまち.md:43–45 contrasts the two explicitly.
- **効力:**
  - 1275250:1 and the old body teach legal force and efficacy (contracts, rules, substances). 妥当 teaches soundness of judgement.
  - The only link is the English "valid/validity". Unlike さっさと, there is no shared dictionary meaning.

**Regressions: none.** Both lists are valid single-line YAML with no duplicates or self-entries, and every entry names an existing article title.

**New actionable findings:** none.

## Optional
- **たちまち/急速 ("rapid"):** たちまち's own prose uses "rapid result" (たちまち.md:25) and "rapid change" (:37). Its entry is 1228890; I checked it via the jisho API, which gives "rapid (e.g. progress)" only. 急速.md also separates pace from abrupt onset. A conservative guard, or rewording たちまち's prose, would be harmless. どんどん ("rapidly; one after another") is a weaker case. Neither is established as a defect.
- **妥当/効力:** the "valid/validity" wording leaves a small residual risk. A guard would be harmless but isn't required.

## Limits
- Git, hash and cleanliness checks were run by the author only.
- There was no live quiz rendering and no native-speaker certification.
- The おどおど and さっさと evidence comes from author captures, not my own retrievals.
- The jisho API page is not the pinned dictionary snapshot.
- My first round missed 一度に and おどおど even though their titles were among those I read. This turn's title searches focused only on the two changed cards, so other unguarded pairs may remain.
