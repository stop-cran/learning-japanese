The new 勘定/料金 exclusion is an acceptable conservative quiz safeguard, and I found nothing material missing in this correction. It is neither too broad nor inadequate. My earlier view still stands: the guard wasn't required. Adding it isn't a defect.

**Snapshot:** checkpoint `0b6be1de66c9681b208ee2d27f0253baed4052cc`, packet content version `d19ddd349a584532`.
- Phases 1–3 were serial single `view` calls, none denied:
  - The `.git` file pointed to `auditor-compatibility-isolated/.git/worktrees/learning-japanese`.
  - The worktree HEAD read `ref: refs/heads/n1/resume-after-106-476f429`.
  - That ref read `0b6be1de…`.
- My ref read only shows which commit the branch points to. The signature check is yours; I didn't verify it.
- I can't independently link the packet's content version to that commit.
- No uncommitted state is included.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), dependent follow-up, using only `view`.
- **Phase 4:** I read `followup-850\correction-fee-packet.txt` in one forced read with no range. No truncation notice appeared. I couldn't confirm the 19,514-byte size or any SHA-256 value.
- **Phase 5:** I read my own `followup-849\confirmation-claude.md`. I read no other reviewer report or ledger, and fetched nothing from upstream sources.
- **Earlier material:** I had already seen the earlier packets and my earlier reports in this session. This assessment rests on what I read in phases 4–5.

## 勘定/料金 guard: acceptable conservative safeguard; medium–high confidence
- **Sources:** 勘定 is labelled "reckoning; bill" (`勘定.md`:4). JMdict 1210750 gives 勘定 three senses: counting/reckoning, bill/check/account/payment, and consideration. 料金 is labelled "fee; charge; fare" (`料金.md`:4, 15). JMdict 1554280 gives only fee, charge and fare.
- **Overlap:** The only overlap is in English. A "charge" can be the amount billed, which sits close to 勘定's "bill" sense. That makes the case for a guard weak, but excluding the pair is a reasonable precaution.
- **Not a synonym claim:** 料金 is the rate for a service (`料金.md`:15–20). お勘定 is settling the bill (`勘定.md`:16–21). Neither article's text changed, and the guard only affects quiz choices.
- **Not overly broad:** It removes one wrong choice that scored highly. They share the tags kango, noun and money plus the same type. In the full pool, 料金 still gets other money-related wrong options such as 金融, 奨学金 and 金庫.
- **Trade-off:** It loses a hard-but-fair contrast that I judged useful before. That is an editorial cost, not an error.
- **Independent of other guards:** I didn't base this on 代金 excluding 料金 or 勘定 excluding 代金. Exclusions only block the pair they name.

## Earlier safeguards: intact
- The diff only adds `料金` to the end of 勘定's list (`勘定.md`:9). 計算, 支払う, 給与, 払う and 代金 are all still there.
- 勘 still excludes 感覚 according to the test's check (`Batch107FeeQuizTest.kt`:45). That comes from the supplied test, not from my reading `勘.md` in this packet.

## Selector behaviour and test samples
- **Both directions:** `Words.kt`:175 checks both cards' exclusion lists. 料金 has none of its own (`料金.md` has no line 9 entry), so the guard works in both directions through 勘定's entry alone.
- **Other wrong options:** Line 178 also stops two mutually excluded words from appearing together as wrong options. Test lines 98–103 check that with an unrelated target word: at most one of 勘定 and 料金 appears.
- **Short pools:** With only the two cards, the test expects a single option, the target itself (lines 60–61). This shows a small pool can yield fewer choices.
- **Full and custom pools:** The test expects four distinct options and labels over 20 seeds, in both quiz directions (lines 83–92).
- **Unguarded check:** With the guard removed in memory, the pair does appear together (lines 93–97 and the printed sample). That shows the guard is reachable, not that the meanings are ambiguous.
- **Limits of this evidence:** These are supplied results that I didn't run. The bounded samples don't prove the whole deck is safe.

## Omissions and remedies
- **None material.** If the editorial record explains this guard, it should call it a precaution against the shared English word "charge", not synonymy.

## Still unresolved, not reconsidered
- **定 and 違 reading gaps:** 定's さだ.か and 違's ちが.える, -ちが.える, たが.う and たが.える readings have no rows, and the app offers たが.う with no explanation. These predate batch 107 and don't block it.
- **支払う/支払 pair:** still hard but fair, and unchanged.

## Limits
- I didn't assess native-speaker judgement, rendering, phone behaviour, the merged tree, publication, old app versions (which ignore exclusions) or wider semantic safety.