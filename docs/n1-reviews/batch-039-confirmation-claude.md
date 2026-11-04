The revised snapshot introduces no regression. The added 鴻鵠–鶴 quiz exclusion is supported by Daijisen, and I am withdrawing my original 鴻 origin finding as a defect and keeping it only as optional. One process breach to disclose: in my second response I issued two tool calls (a glob and a view of my own report) instead of one.

**Snapshot:** revised `1133566c7a738c2f13b4b67afc4974fcba834c19`, compared with the original `9b21ba549417d25c54183a37e4f5cc35a2689638`. Both hashes are as supplied; I could not check Git (no shell). There are no uncommitted teaching changes. When I read `words\鴻鵠.md` at the revised snapshot, line 8 was the only change from what I reviewed initially, which matches the supplied diff.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the same session as the initial review. This is a dependent confirmation, not a blind initial review.
- **Reads made now:**
  - my own report, `docs\n1-reviews\batch-039-initial-claude.md` (I did not read the other reviewer's report or the author's ledgers);
  - all of `words\鴻鵠.md`, `words\鶴.md` and `kanji\鴻.md`;
  - `docs\content-format.md` lines 128–148;
  - `content-structure.instructions.md` lines 40–47;
  - the supplied Kanjipedia 鴻鵠 page (lines 45–99) and Daijisen おおとり page (lines 1755–1810).
- **Range note:** lines 40–47 of the instructions cover kanji front matter, readings and quiz curation, not the origin rule (item 4), which sits later in the file. For item 4 I relied on the full text I read in the initial session, which was also restated in this session's context. I did not reread that section in a new range.
- **Not reread:** the full JMdict packets and the other unchanged comparison cards. Those checks are inherited from the initial review, not fresh.

**Verdicts:**
- **`words\鴻鵠.md` (changed):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`kanji\鴻.md` (original finding):** scoped coverage is revised from NEEDS FIX to CLEAN; the item moves to Optional. Correctness and comprehensibility stay CLEAN. The file itself is unchanged.

**Findings:** none new.

**The added 鶴 exclusion:**
- **Overlap is real:** Daijisen's おおとり entry (大鳥／鵬／鳳), sense 1, defines the word as "コウノトリ・ツル・ハクチョウなど、大形の鳥の総称" (a general term for large birds such as storks, cranes and swans). A crane is therefore a direct example of the large birds in 鴻鵠's title.
- **Kanjipedia agrees:** it defines 鴻鵠 as "大形の鳥。大きい鳥。" (a large bird).
- **Quiz risk:** with the prompt "large birds; great person", a learner could reasonably pick 鶴 ("crane (bird)"). That meets the content-format rule that an exclusion is warranted when either title could reasonably be accepted for either word.
- **Mechanics:** the exclusion works in both directions and only for this pair. It does not exclude 鶴 from 鴻, so it does not turn 鴻鵠 into a synonym of 鶴 or imply they can replace each other in text.
- **Format:** the front matter is a valid inline list, 鶴 exists, the entry is not repeated, does not point to itself, and there are no `quiz_distractors` it could overlap.

**Reconciling my original items:**
- **鴻 origin finding (Minor, scoped coverage): withdrawn as a defect.**
  - The content-structure rule allows a labelled modern-shape mnemonic plus `structure-unclassified` when no historical analysis is adopted.
  - The disclaimer "This is a memory aid… not a historical or phonetic rule" grammatically refers to the memory aid. It does not deny that 鴻 has a sound component.
  - The mnemonic still shows 江 itself, and the card links Kanjipedia, which gives the sourced 形声 explanation.
  - Nothing in the text is wrong, and declining to adopt a single-source historical claim is a permitted choice, so the learning impact does not reach an actionable defect.
  - I do not regard this as an unresolved disagreement. The improvement remains optional (see below).
- **偉大 quiz guard: optional, nonblocking.** 偉大 is a な-adjective glossed "great; outstanding". 鴻鵠 is a literary noun for a great person. The labels overlap only partly, and that remains an untested hypothesis, not a defect.
- **Full proverb with reading: optional, nonblocking.**
- **"Phoenix" in English translations: optional, nonblocking.**

**Regression check:** none. The only change is one front-matter line, and the body text is identical to what I reviewed initially.

**Optional:**
- **鴻 card:** a hedged sentence such as "Kadokawa Shinjigen (via Kanjipedia) explains 江 as the sound component (コウ)" would help learners remember the selected reading コウ. It is not required.
- **鳳凰 hypothesis:** 鳳凰 ("Chinese phoenix; fenghuang") is a mythical bird, sense 2 of Daijisen's おおとり, and JMdict 2834550's literal gloss uses "phoenixes". A quiz overlap with 鴻鵠 is weaker than with 鶴 because 鳳凰 is a specific mythical name and the article explicitly rejects the phoenix reading. I am not claiming it is a defect.

**Limits:**
- **Process breach:** I made two tool calls in one response (the glob and the view of my own report), contrary to the one-call rule. Every other step was serial.
- **Inherited checks:** the full dictionary packets and unchanged comparison articles were checked in the initial review, not reread now.
- **Supplied sources only:** I used only the saved Kanjipedia and Daijisen pages and fetched nothing independently.
- **Text only:** this is a textual review. No native app, viewport, Android, phone, CI or publication acceptance is inferred, and those remain pending.
