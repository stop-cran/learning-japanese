**Snapshot:** I was given `75fbfc7dc734c7ff5d9771fbd5103afd3f3fdc1c`, with no teaching changes since my initial review. I couldn't check this independently because shell and Git weren't available. I made no edits.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), confirming my own initial batch-074 review in the same session. This was not a new initial review, and I did not reread the 182-family JMdict packet.
- **Files read:** I read these six, in full, one call per response:
  - `kanji\兄.md` lines 1–47
  - `kanji\元.md` lines 1–45
  - `words\免れる.md` lines 1–64
  - `words\救助.md` lines 1–35
  - `words\生存.md` lines 1–45
  - `docs\n1-reviews\batch-074-confirmation-jmdict.xml` lines 1–50
- **What I checked:**
  - 兄 and 元 as wrong answers for 免.
  - 免れる against 救助 and 生存: displayed titles, ordinary meanings, grammatical roles, and whether more quiz exclusions are needed.

**Verdicts:**
- **New 免, wrong answers 兄/元:** correctness CLEAN, coverage CLEAN, comprehensibility CLEAN.
  - "older brother" and "origin, former" don't overlap with "exempt; be spared".
  - The 兄 and 元 cards confirm their full meanings, including 元's "former state".
- **New 免れる, compared with 救助/生存:** correctness CLEAN, coverage CLEAN, comprehensibility CLEAN.
  - **救助** (JMdict 1229200): a noun meaning "relief; aid; rescue", and a transitive する-verb. Its title "rescue; relief" names a rescuer's action. 免れる says someone was spared or avoided something, without naming any rescuer.
  - **Possible overlap:** JMdict sense 1 of 免れる includes "to be rescued from". A learner could be drawn toward "rescue; relief", but the roles and parts of speech differ, so both answers aren't equally defensible.
  - **生存** (JMdict 1379230): a noun meaning "existence; being; life; survival", and an intransitive する-verb. Staying alive is different from escaping harm or avoiding a burden. Both the 生存 and 免れる articles say this explicitly (生存 lines 41–42, 免れる lines 48–51).
  - **Conclusion:** leaving out exclusions for these pairs is not a demonstrated defect. Exclusions are pairwise, so 助かる excluding both words doesn't link them. The other two changed links and the 許 example were outside this confirmation and keep their initial verdicts.

**Findings:** None. My initial findings ("None") and optional suggestions are unchanged.

**Optional:** No new suggestions. The earlier four remain:
- the missing JMdict 1533130 citation in `kanji\許.md`
- noting that 勉 and 晩 contain the 免 shape
- an example for 免's dismissal sense
- the 謗りを免れない pattern

**Limits:**
- **Earlier parallel call:** in my initial review, I read 兄 and 元 in a single parallel call. That breach still stands. In this run, every call was serial.
- **Earlier missing evidence:** the original 182-family packet did not include the 救助 and 生存 families. Yet my initial report said they correctly stayed unexcluded, based only on their article text, and I didn't disclose that gap. That conclusion is now confirmed with the supplied families.
- **Supplied JMdict extract:** I relied on the given extract and its stated hash. I did not hash it myself or fetch the families fresh. I inferred nothing about frequency.
- **Still unchecked:**
  - larger or live quiz pools
  - the possible 逃 fallback choice
  - native-speaker review, Android f9b59a2+ or physical-phone checks (text review only)
