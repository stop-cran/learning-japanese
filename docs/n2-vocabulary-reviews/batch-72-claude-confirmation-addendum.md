# Batch-72 confirmation addendum (Claude-F-03 residual and principals access)

## Snapshot
- **Commit:** `5398d39999695042b16b4af3c4c42fcad307c889`, parent `ded07a6f4969b3f63f2e62ae73511fade363ead1`, taken from `batch-72-correction-snapshot.json`, which I read first.
- **Content reviewed:** committed content only. The checkout is stated to be unchanged.
- **Git limitation:** my file tools cannot run Git. The clean-checkout and hash checks are the author's, not mine.

## Scope
**Model:** claude-opus-5.5 (family claude). Read-only: no edits, shell, agents or delegation. This is a bounded addendum, not a new full-batch acceptance, so the twenty-row table is not restated.

**Fresh, complete access in this addendum:**
- The correction snapshot, read first.
- `batch-72-review-principals.jsonl`, ranges [1,10] and [11,20]: all 20 families and 39 senses.
- `words\広げる.md` (56 lines) and `words\伝える.md` (43 lines), both read completely.
- `docs\content-format.md` lines 76-101.
- `batch-72-public-bodies.txt`, read completely.
- I fetched both Kotobank pages myself. Each returned the full Seisenban heading. The Digital Daijisen sections showed only their source line, so the Daijisen evidence is still the frozen Weblio capture.

**Inherited, not freshly read here:** the JMdict 1441870 (伝える) glosses and all other articles.

**Correction to the historical report (which stays unchanged):**
- My first confirmation listed all 20 principal families (39 senses) as fresh reads. The authenticated output shows that pass returned only lines 1-15, which hold 15 families and 27 senses.
- The final five were not freshly returned: 冷やす, 響き, 百科事典, 広げる and 広々 (12 senses). My working notes said I had read them before a context break, but I cannot verify that, so I do not rely on it.
- My earlier statement that JMdict 1602370 has no convey or propagate sense came from inherited access. It is now freshly verified.
- I cited the title test as `content-format.md:94`; the correct line is `:95`.

## Findings
**The five newly returned principals**
- **Totals:** 20 families and 39 senses, matching the count I claimed earlier.
- **冷やす 1556770, 百科事典 1602190 and 広々 1602380:** no effect on my earlier dispositions.
- **広げる 1602370:** four senses, none meaning convey, tell, propagate or popularize. This matches the card footer at `広げる.md:54-55`.
- **響き 1602130:** three senses, none meaning influence or effect. So the 響き/影響 and 響き/効果 guards (GPT-F72-02) rest on the frozen Daijisen ひびき sense 5 alone.
  - The disposition is unchanged, because "influence; effect" directly translates ひびき sense 5, defined as 「影響」 with the example 「物価上昇の―」.
  - 響き/効果 stays at medium-low confidence.

**Claude-F-03 residual (広げる/伝える): retained, but on narrower grounds**

I withdraw three of my earlier supporting arguments:
- **The literary citation.** Daijisen sense 6 and Seisenban ③(ロ) both record the dissemination sense. They share a single citation, the 1906 草枕 sentence. That is two dictionary judgments resting on one example. A first-citation example does not show that the sense is rare or archaic today.
- **JMdict lacking a propagate sense.** That is a gap in a single authority.
- **"Conveying need not make something widely known."** That is a difference in breadth, not proof that the meanings never overlap.

I accept that the Japanese meanings genuinely overlap:
- 広げる: Seisenban ③(ロ) 「普及させる」 and Daijisen sense 6 「広い範囲にゆきわたらせる。ひろめる。」.
- 伝える: Seisenban [1]②(ハ) 「広く言い知らせる。次から次へと言いひろめる」.
- Neither dictionary defines either word with the other. The overlap comes only through a shared idea of spreading something widely.

The remaining basis is the title test in `content-format.md:95`, applied to the actual displayed titles:
- **Could "convey; tell" (`伝える.md:4`) be accepted for 広げる?** No. 広げる's dissemination sense means "spread widely; popularize", not passing something to a recipient or telling.
- **Could "spread out; widen; unfold" (`広げる.md:4`) be accepted for 伝える?** No.
  - 伝える's ②(ハ) sense could be translated "spread (the word)", but the title says "spread out". Together with "widen" and "unfold", that reads as physical spreading.
  - The ③(ハ) sense, 振動・熱を伝える, means transmit or propagate, not spread out.
- The English-to-Japanese direction fails the same way.
- **Unlike 響き/影響,** neither title translates an applicable sense of the other word.
- **The synonym rule in `content-format.md:82-83` does not require this guard.** The overlap lies in a secondary sense of each word that neither title shows and neither card teaches.
  - The 広げる card (lines 16-25 and 51-52) teaches widening, unfolding and extending scope.
  - It leaves dissemination to 広める (lines 39-40).

**Status:**
- Low severity, Correctness facet, `words\広げる.md:9`.
- Remedy: remove 伝える from 広げる's exclusions and keep the 広める/伝える guard.
- Confidence drops from medium to **medium-low**: the confirmed meaning overlap means a cautious editor could reasonably keep the guard.
- The 広げる Correctness facet stays NEEDS FIX (low). I did not revisit any other row.

## Limits
- No Git; the hashes are the author's.
- The Kotobank Daijisen sections did not render.
- Both dissemination citations go back to one 1906 example. I consulted no corpus or frequency evidence.
- I did not freshly read JMdict 1441870.
- The title-test judgments are editorial. They are not native-speaker certification or runtime-quiz verification.
