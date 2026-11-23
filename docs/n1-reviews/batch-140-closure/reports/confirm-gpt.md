Snapshot: `1b24a5f97a396d7121689f3928c7aa500e0054ef`, compared with `28831314c9b8203cf7dd66c4eec16f23ef0fef22`. Reviewer: GitHub Copilot; the underlying model name/version is not exposed to this reviewer.

Scope:

Read all eight revised cards in full, checked every patch hunk against correctness, coverage, consistency/quiz safety and comprehensibility, and examined the post-fix meaning options and all 16 selected reading prompts across all 15 batch cards.

**Confirmation-packet files opened:**

- In full: `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, and `evidence\README.md`.
- In full, including unchanged passages: `snapshot\kanji\帳.md`, `snapshot\kanji\幕.md`, `snapshot\kanji\幣.md`, `snapshot\kanji\弁.md`, `snapshot\kanji\径.md`, `snapshot\kanji\徐.md`, `snapshot\kanji\従.md`, `snapshot\kanji\徴.md`.
- In full: `checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt`, `checks\link-targets.tsv`.
- In full: `evidence\QuizBuilder.kt`, `evidence\KanjiReadings.kt`, `evidence\jmdict-cited-entries.xml`, `evidence\superseded-775debde.txt`.
- `evidence\Words.kt`: source lines 205–302, including the complete `ReadingOptions` implementation; complete bytes also compared with the original copy.
- `evidence\雨.json`: complete structured parse; inspected identity, revision, stroke count, stroke types and endpoints, especially strokes 1–4.
- Last seven lines, or the complete file when shorter: `checks\lint.txt`, `checks\unittest.txt`, `checks\validate.txt`, `checks\budget.txt`, `checks\vocabulary.txt`, `checks\manifest.txt`, `checks\linkplan.txt`, `checks\kanji-remarks.txt`.

**Original-packet context reopened:**

- `snapshot\kanji\帳.md`, `幕.md`, `幣.md`, `弁.md`, `径.md`, `徐.md`, `従.md`, `徴.md` — same prefix throughout; complete text loaded for exact patch replay and selected old/new comparisons.
- `snapshot\kanji\嵐.md`, `巣.md`, `序.md`, `往.md`, `志.md`, `怠.md`, `恨.md` — same prefix throughout; metadata/quiz fields examined in this round, with their original full-card review retained.
- `repo\kanji\中.md`, `repo\kanji\南.md`, `repo\kanji\雨.md`, `repo\kanji\署.md`: metadata inspected; complete text was loaded programmatically.
- `titles\kanji-titles.tsv`: complete structured read for referenced titles and revised-title uniqueness.
- `evidence\kanjidic2-records.xml`: complete parse, with 幣 and 徐 reading records inspected.
- `evidence\jmdict-families.xml`: complete parse for the 幣 spelling/reading check; entry 1345580 inspected directly for 徐に/徐ろに.
- `evidence\audits\quiz-safety.txt`, `evidence\audits\reading-exposure.txt`, `evidence\audits\reading-options.txt`: complete text compared with the revised outputs.
- `evidence\app-code\QuizBuilder.kt`, `evidence\app-code\KanjiReadings.kt`, `evidence\app-code\Words.kt`: complete bytes compared with the confirmation copies; all three copies were identical.
- My own `reports-140\initial-gpt.md`: Findings, Optional and Limits reread.

**Independent public checks this round:** actual entry passages, not search snippets, at [Kanjipedia 幣](https://www.kanjipedia.jp/kanji/0006218900), [Daijisen にきて](https://www.weblio.jp/content/にきて), [弁護士](https://www.weblio.jp/content/弁護士), [小径](https://www.weblio.jp/content/小径), [弁](https://www.weblio.jp/content/弁) and [従](https://www.weblio.jp/content/従).

Dispositions:

- **G1 — RESOLVED** — `幕.md:62` now treats covering-cloth as an unquoted Daijisen explanation; `徐.md:48` likewise unquotes slow, unhurried. The retained wording “end; close” is supported by JMdict 1524750, and “act of a play” occurs in 幕's title. Neither correction changes the underlying meaning.
- **G2 — RESOLVED** — `弁.md:25,55` and `従.md:25,56` compress the introductory inventories and move the more peripheral material after the core teaching. The cap/braiding senses, ancient alliance and archaic prefix no longer precede the reading tables. Independent counts matched 378→341 and 455→342 words before Readings. All reading rows, relevant examples and qualifications remain. This resolves the specific front-loaded exhaustive-catalogue issue; it does not mean the cards are now brief.
- **Optional 1 — RESOLVED** — `幣.md:13,53` replaces 内 with 雨 and supplies a defensible frame/vertical-stroke comparison. The actual 中/南/雨 cards are Starter cards with selected/default on readings チュウ/ジュウ, ナン/ナ and ウ. Their keys remain distinct and fill all three wrong slots in the audited pools. This is a safe compromise, not a claim that the set contains the closest possible look-alikes.
- **Optional 2 — RESOLVED** — `弁.md:25,58` adds 弁護士 べんごし and entry 1512850. The supplied complete entry gives “lawyer; attorney”; the independent Daijisen entry confirms the reading and profession.
- **Optional 3 — RESOLVED** — `徐.md:36` explicitly connects おもむ.ろに with 徐ろに and identifies ろに as okurigana. Pinned KANJIDIC2 and JMdict 1345580 support that explanation and the alternative 徐に spelling.

Verdicts:

- **Correctness: CLEAN** — no new established defect in any changed card.
- **Scoped coverage: CLEAN** — retained reading coverage and qualifications survive the relocation; the new examples and dictionary references are supported.
- **Consistency and quiz safety: CLEAN** — all 15 batch meaning-option sets and all 16 selected reading prompts checked; no demonstrated reachable ambiguity.
- **Comprehensibility: CLEAN** — G2's specific introductory-catalogue issue is resolved; residual paragraph density is optional polish.

The regression checks additionally established:

- Replaying every hunk against the original eight cards reproduced the revised card text exactly. Header differences were confined to the declared 弁 title, 幣 distractors and 帳/徴 exclusions. Metadata readings, quiz selections, tags, radicals and stroke counts were unchanged.
- 帳–幕 has a real shared curtain sense. Adding 幕 to 帳's exclusion list makes the exclusion effective in both directions under `QuizBuilder.excluded`; the two revised Notes agree with that behavior.
- 徴–署 is a direct English-answer confusion involving “sign,” although indication and signing one's name differ. The added exclusion is symmetric in the meaning builder and does not contradict the explanatory distinction.
- 弁's revised title and heading agree. “Bento” is supported by Daijisen's explicit 弁当 sense and fits both linked word articles. The revised title remains unique in the supplied title inventory.
- 径's new 小径 しょうけい example genuinely illustrates a path. JMdict 2859605 supports “path; lane” and the formal/literary label. Moving 径庭 to reference material preserves its correct “great difference” gloss without using it to explain the literal path sense.
- 幣's added ぜに and にきて claims are supported by the actual Kanjipedia and Daijisen entries. In context, “in neither KANJIDIC2 nor JMdict” means not attested there **as readings of 幣 in the pinned data**; it does not deny the separately cited 銭ぜに entry. The supplied complete family and pinned character record support that distinction. Entry 2175880 is correctly added.
- The regrouped 弁 and 従 explanations still match the actual Daijisen sense groupings. Their relocated references retain the relevant historical/register and source-only qualifications.
- All 16 changed-line card-link/title comparisons matched the supplied snapshot/title inventory. No declared distractor was also placed in its target's exclusion list.

**Post-fix quiz review — every batch card:**

| Card | Three wrong meaning options checked | Selected reading prompt(s) checked |
|---|---|---|
| 嵐 | rock; boulder / shore; riverbank / crumble; collapse; demolish | あらし |
| 巣 | fruit; fruition / single; simple / flourish; glory | す |
| 帳 | hat; headgear / width; breadth / sash; zone | チョウ |
| 幕 | grave; tomb / dusk; livelihood / recruit; solicit | マク |
| 幣 | middle, inside / south / rain | ヘイ |
| 序 | wide, spacious / government agency / deposit; entrust | ジョ |
| 弁 | stand, machine counter / leave, elapse / calculate; reckon | ベン |
| 往 | reside, dwell / pour, direct attention / wait, await | オウ |
| 径 | role; duty / he / suspicious; uncanny | ケイ |
| 徐 | surplus / route; course / on foot | ジョ |
| 従 | on foot / law; rhythm / wait, await | したがう |
| 徴 | minute; faint / penetrate; be thorough / virtue; benevolence | チョウ |
| 志 | sell / voice / forget | シ |
| 怠 | begin, start / govern; heal / thought; attention | おこたる; なまける |
| 恨 | limit / silver / pleasant; agreeable | うらむ |

These meaning distractors remain defensibly wrong, including against 弁's expanded title. I considered the reverse semantic comparisons, not just exact title inequality. The meaning audit changed only the 幣 option line and 弁 title line.

Reading safety was checked separately: meaning exclusions are not consulted by the reading builder. That builder protects all metadata on/kun keys and their mutations, deduplicates selected wrong keys, and uses fallback when curated choices do not fill the slots.

- 幣 now has four curated combinations and five possible wrong reading keys across 中/南/雨. Every combination fills the three slots in the audited N1, All and padded Starter pools. Its latent まい candidate therefore remains unreachable there.
- The `reading-options.txt` HIT for 幣 まい is not a demonstrated displayed option: that label ignores already-filled curated slots. The complete exposure audit reports zero production hits, zero padded-session hits and zero one-holder padded hits.
- Four latent collisions remain: 幣まい, 弁とく, 従ひろい and name-reading 志じん. They are not four production failures.
- 幕 still needs two fallback slots because 墓 has no selected on reading and 暮/募 share ボ. 往 can need one, 徐 needs one, 従 needs one, and each 怠 prompt needs one in the full pool. The complete candidate/exposure evidence established no unsafe answer for these prompts.
- The superseded 常/帯/希 audit contains a Starter PAD-HIT, but those are not the revised distractors. I did not attribute that superseded result to this snapshot.

Confirmation: **CONFIRMED** — all five response items are RESOLVED, and no new actionable defect was established.

Findings:

None.

Optional:

For future presentation polish, split the remaining long sense-summary paragraphs in 弁 and 従 into shorter visual units. This is not a new finding or a condition of confirmation.

Limits:

- This was a blind, read-only confirmation. No other reviewer's report, outside author material, repository checkout, agent or session was accessed. No parallel calls, recursive listings, corpus scans or background jobs were used.
- Some initially combined output exceeded the tool's display limit. I did not open its automatically generated spool file; the relevant source files were reread in bounded output.
- The supplied 436-test success and other mechanical summaries were inspected, not independently rerun. Android JVM content tests and the Kotlin reading-audit cross-check remain unrun as declared; their absence is not a finding.
- The reading audits are supplied Python-model outputs checked against the supplied Kotlin source. The pool-building integration itself was not executed. Seed sampling is not exhaustive: for example, it did not observe every analytically drawable fallback key for 幕, 往 or 従. Candidate/reachability analysis, not sampling alone, supports the bounded safety conclusion.
- These audits cannot prove completeness of dictionary attestation, safety under every arbitrary smaller/future pool, every multi-card borrowing combination, or actual device behavior. Some candidate lists are abbreviated, and the simpler options audit does not account for curated-slot saturation. A latent collision is not proof of present exposure.
- No phone rendering, animation or JVM execution was performed. Unchanged word articles and stroke files were not re-reviewed in this round.
- I did not perform a whole-corpus inbound-prose search for the old 弁 title. The revised batch links and title inventory were checked; the author's broader “no other card quotes the old title” statement was not independently established globally.
- Historical commit/publication statements and superseded-tree provenance were not authenticated against Git history; local checks were confined to the authorized packets.
- “CLEAN” and “CONFIRMED” apply to this bounded confirmation, not exhaustive linguistic completeness or a runtime guarantee.
