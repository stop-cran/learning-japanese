The five guards are justified quiz safeguards, and I don't think 勘定/料金 needs one. The 定 and 違 reading gaps are real but older, and batch 107 doesn't make them blocking.

**Snapshot:** checkpoint `bfd617ab00c75b9f7a74decd865f1f813b0eabed`, packet content version `db93cd80ee101b73`.
- Phases 1–3 were serial single `view` calls, none denied:
  - The `.git` gitdir pointed to `auditor-compatibility-isolated/.git/worktrees/learning-japanese`.
  - The worktree HEAD read `ref: refs/heads/n1/resume-after-106-476f429`.
  - That ref read `bfd617ab…`.
- My ref read establishes only which commit the branch points to. It does not check the signature; whether this is the signed checkpoint rests on your statement.
- I can't independently link the packet's content version to that commit.
- No uncommitted state is included.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), dependent follow-up, `view` only.
- Phase 4 read the follow-up packet in one forced read with no range and no truncation notice. I couldn't confirm its 71,442-byte size or any SHA-256.
- Phase 5 read my own `initial-claude.md`. I read no other reviewer report or ledger, and nothing was freshly fetched upstream.
- Earlier in this session I read the original common packet, the 03f68e8 correction packet and my own unaccepted 03f68e8 follow-up. I treated that attempt as not accepted and reassessed from the phase-4 material. I flag below the one place where I rely on earlier material.

**How the guards work (`Words.kt`:175-178, 197):** exclusions block the named pair only, in both directions. They don't extend to synonyms of either word. A guard only matters if the two cards can meet, which depends on the tag/type/kanji score in lines 189-191. The sampled output is a few seeds. The test file in the packet adds checks over 10–20 seeds; I didn't run it.

## Direct pairs
1. **勘/感覚 (`words/勘.md`:9): Justified conservative safeguard; medium–high confidence.**
   - JMdict 1212330 gives 感覚 "sense / sensation / feeling / intuition". JMdict 1210590 gives 勘 "perception / intuition / the sixth sense".
   - So "intuition; hunch" is defensible for 感覚, and "sense" is defensible for 勘 ("the sixth sense").
   - The words share tags `kango` and `noun` and the same type, so the score (5) is high enough for them to meet.
   - This is not a synonym claim. 感覚.md:16-21 teaches bodily sensation, and the guard leaves that text unchanged.
   - It resolves the hypothesis in my original report.
2. **勘定/支払う: Justified safeguard; medium confidence.**
   - 勘定 sense 2 in JMdict 1210750 is "payment (of a bill); settlement (of an account)", marked as a する-noun.
   - English to Japanese: given the prompt "pay", a learner can reasonably pick 勘定 (かんじょう). The reverse direction is weaker but still possible.
   - Shared tags (money) and type give them a moderate score.
   - 勘定.md:29 already contrasts the two words in its text, so this is not a synonym claim.
3. **勘定/給与: Justified only as a conservative safeguard against the shared word "pay"; low–medium confidence that it is needed.**
   - 給与 means wages or provision (JMdict 1230350, `給与.md`:4, 16). 勘定 never means wages.
   - The "allowance" gloss in 勘定 sense 3 means making allowance for something ("consideration/allowance"), not a money allowance. It doesn't support this guard.
   - The risk is a learner reading 給与's "pay; …" label as 勘定's payment-of-a-bill sense.
   - They share kango, noun, suru-verb and money plus the same type (score 9), so they are likely to meet. That makes the guard effective, not overly broad.
   - Any editorial record must call this a quiz safeguard, not 給与 ≈ 勘定. Both articles correctly make no such claim. I didn't see the ledger.
4. **勘定/払う (new): Justified safeguard; medium confidence.**
   - The packet confirms 払う's title is "pay" (`払う.md`:4; test line 50). JMdict 1501620 sense 1 is "to pay (e.g. money, bill)".
   - It's the same "pay" risk as 支払う.
   - Their score is lower (only `money` is shared; wago vs kango), so they are mainly at risk in custom pools. The unguarded control shows the problem pairing can happen.
   - This closes the 払う gap I raised in the unaccepted 03f68e8 follow-up.
5. **勘定/代金 (new): Justified; high confidence. This is the strongest of the money guards.**
   - JMdict 1411790 gives 代金 "price, cost, charge, payment, **bill**, fee". 勘定 sense 2 gives "**bill**, check".
   - So "reckoning; bill" is a defensible answer for 代金, and "payment due" is a defensible answer for 勘定 (amount to settle). Either direction can be argued.
   - They share kango, noun and money plus type (score 7).
   - They overlap only in the bill sense. 代金 is the sum owed for goods (`代金.md`:16, 33), while お勘定 is settling the bill. This is not full synonymy.

## 勘定/料金: no direct exclusion needed; optional. Medium confidence.
- 料金's label is "fee; charge; fare" (`料金.md`:4). JMdict 1554280 gives only fee/charge/fare.
- **料金 shown in Japanese, answers in English:** "reckoning; bill" isn't a defensible meaning. 料金 is a rate charged for a service, not the bill or a reckoning, and JMdict gives neither.
- **勘定 shown in Japanese, answers in English:** "fee; charge; fare" is not in 勘定's JMdict senses, and "reckoning; bill" fits better. A learner could associate "charge" with a bill, but the intended answer is clearly better.
- **English prompts:** each label points to its own word. "Fare" and "fee" don't describe 勘定.
- Their score (7: kango, noun and money plus type) means they will often meet. That gives a hard but fair contrast, not two equally right answers.
- 代金 excluding 料金 (`代金.md`:9) and 勘定 excluding 代金 don't imply a 勘定/料金 guard, because exclusions only block the named pair.
- The test file (line 109) records this pair as deliberately unguarded.

## 支払う/支払 (unchanged)
- Both directions sample together ("pay" vs "payment"; しはらう vs しはらい), and JMdict 1310300 and 1594480 keep the verb and noun separate.
- The English word "pay" is ambiguous only in that the noun means wages, which 支払 doesn't mean. 支払う is the best answer.
- Hard but fair. It already existed before this batch and isn't blocking. Low–medium confidence.
- Optional for the owner: retitle 支払う "to pay", or exclude the pair. This is outside batch 107.

## Legacy reading gaps (real, older than this batch, not blocking)
- **The rule versus what is checked:**
  - The authoring instruction (`content-structure` lines 43-45) requires a reading row for every kun'yomi entry.
  - The validator enforces that only for N5/N4 cards.
  - The narrower curated check (format line 128) covers only explicit `quizKunyomi` selections, and neither card has one.
- **定 (N3):**
  - `さだ.か` (line 10) has no row (rows are lines 30-33).
  - さだ.める, さだ.まる and さだ.か share the stem さだ, so the app offers only `[さだ.める]` (`KanjiReadings.kt`:29, 59; host output). さだ.か is never asked, so this is only a gap in the article's explanations.
  - Remedy: add a row such as 定か さだか "certain", marked as needed. This entry is from my own knowledge, not the packet.
- **違 (N3):** ちが.える, -ちが.える, たが.う and たが.える have no rows. Lines 28 and 46 explain the selection only in general terms, which doesn't meet the per-reading rule.
  - The app actually offers `[ちが.う, たが.う]`. たが.う is a real reading with no priority tags (JMdict 2109290), so it is asked without any explanation in the article. That is actionable.
  - Minimal remedy: add `quizKunyomi: [ちが.う]` (older APKs ignore it), or add a たが.う row marked uncommon/literary.
  - Rows or rarity notes for the other three readings would close the authoring gap.
- **Batch 107's part:** it changed only the Common words bullets (定:41, 違:40). It touched no metadata or reading rows. So it didn't create or worsen these gaps, and they don't block it.
- I don't call these articles clean. My original CLEAN verdicts on 定 and 違 cover only the batch-107 changes.

## Updated verdicts
- `words/勘.md` and `words/勘定.md`: correctness, scoped coverage and text comprehensibility are CLEAN within this scope.
- The other four articles are unchanged since my original report.
- The only actionable items are the older 違 たが.う gap (and the 定 さだ.か documentation gap) for later remediation.
- There are no new defects, and no material omission among the five guards.

## Limits
- Not checked:
  - 直感/直観 cards or any other card titled "intuition" or "payment"
  - 会計's current exclusions (I know 会計 excludes 勘定 only from the original packet read earlier)
  - the editorial ledger wording
- The test output is a bounded sample, not proof that no ambiguous pair exists anywhere in the deck.
- Native-speaker judgment, rendering, phone behaviour, the merged tree, publication and old-APK behaviour are not assessed.