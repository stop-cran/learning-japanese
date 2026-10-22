## Snapshot
`dfe4fb06ebb16b9a224e63b56f23a787b8502880`, committed files only. I had file tools but could not run Git, so the clean worktree, the commit identity and the 63-file scope (baseline `5b47e12b71bd4fdbc818da671cebec910a6e8635`) rest on the author's confirmation.

## Scope
**Model:** claude-opus-5.5 (claude family). I worked sequentially, made no edits and used no sub-agents.

**Governing documents read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-109`.

**Read in full:**
- All 18 assigned pages: kanji 毛, 氷, 永, 汗, 汚, 池, 沈, 河, 沸, 油, 況, 泉, 泊, 波, 泥, and words 汚す, 沈める, 泊める.
- `docs\n2-batch-sources\batch-12.json`: metadata, primaryWords and all wordEvidence records.
- `kanji\川.md`.

**Related passages:**
- The single new component-link line in each of the 24 related word articles.
- Surrounding context wherever a new card relies on that article: 河, 沸く, 波, 泉, 汗, 毛, 毛布, 永遠, 状況, 池 and 油.
- Every link target used by the new cards exists, including 凍る, 長い and 永久.

**Quiz data:** titles and distractors of all 45 distractor targets, older kanji titles that share English words with the new titles, and the older two-distractor cards 水 and 何. For the word quiz: the titles and exclusions of 汚れる, 汚い, 汚染, 土, 沈む, 泊まる, 宿泊, 宿, 下宿, 滞在 and 止める, plus `docs\confusable-words.md`.

**Not reviewed:**
- The 15 stroke files (from the pinned converter; exhaustive path review was not assigned).
- The unchanged bodies of the 24 related articles beyond the passages above.
- `docs\n2-source-snapshot.json`.
- All forbidden ledgers and reports.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\毛 | CLEAN | CLEAN | CLEAN |
| kanji\氷 | CLEAN | CLEAN | CLEAN |
| kanji\永 | CLEAN | CLEAN | CLEAN |
| kanji\汗 | NEEDS FIX | CLEAN | CLEAN |
| kanji\汚 | CLEAN | CLEAN | CLEAN |
| kanji\池 | CLEAN | CLEAN | CLEAN |
| kanji\沈 | CLEAN | CLEAN | CLEAN |
| kanji\河 | CLEAN | CLEAN | CLEAN |
| kanji\沸 | CLEAN | CLEAN | CLEAN |
| kanji\油 | CLEAN | CLEAN | CLEAN |
| kanji\況 | CLEAN | CLEAN | CLEAN |
| kanji\泉 | CLEAN | CLEAN | CLEAN |
| kanji\泊 | CLEAN | CLEAN | CLEAN |
| kanji\波 | CLEAN | CLEAN | CLEAN |
| kanji\泥 | CLEAN | CLEAN | CLEAN |
| words\汚す | NEEDS FIX | CLEAN | CLEAN |
| words\沈める | CLEAN | CLEAN | NEEDS FIX |
| words\泊める | CLEAN | CLEAN | CLEAN |

**Checks that matched the source for all 15 kanji:**
- Readings, primary stroke counts, canonical radicals and radical numbers, and grade tags all match batch-12. `grade-8` follows the repo convention also used by 凍 and 叫.
- The 48 reading rows are 44 JMdict-backed rows and 4 honestly qualified source-only rows (況 まし.て and おもむき; 泥 デ and ニ).
- All 45 distractors point to existing cards whose meanings are wrong for the answer.

**The 川 change is sound.** Its distractors are now [山, 水, 州], and 州 means "state; province". Adding a third distractor removes the risk that the default fallback picks 河 "river; watercourse" as a direct synonym.

## Findings
**B12-01 — Minor — Correctness — `kanji\汗.md:40`**
- **Claim and impact:** "do not simply attach する to the noun 汗" reads as a grammatical ban. JMdict has the suru verb 汗する. A learner who meets it (for example in 額に汗して) would think the dictionary form is wrong.
- **Remedy:** Keep 汗をかく as the everyday expression, and say that 汗する exists but is not the usual everyday way to say "sweat".
- **Evidence:** The Jisho API, which attributes its data to JMdict, returned 汗する / あせする, "to perspire; to sweat", a suru-included intransitive verb. Batch-12 does not contain this entry.
- **Confidence:** Medium. The attestation is established, and the word "simply" partly softens the ban.

**B12-02 — Minor — Correctness — `words\汚す.md:27-28` (with 21-23)**
- **Claim and impact:** The article calls 汚し (よごし) "the conjugation stem". 汚す is a godan verb, so 汚し is only its masu-stem. The article's own form 汚さない does not come from 汚し, and the label invites the mistake 汚しない.
- **Remedy:** Write "masu-stem 汚し (汚します); the negative uses 汚さ (汚さない)", as `words\話す.md:20` already does for 話し.
- **Evidence:** Standard godan conjugation and the article's own forms list.
- **Confidence:** High.

**B12-03 — Minor — Comprehensibility — `words\沈める.md:46-47`**
- **Claim and impact:** "The presence of める does not by itself make this verb about calming a person or quieting a room" hints at a homophone without naming it. Learners cannot tell why calming would come up at all.
- **Remedy:** Name the homophone: 静める/鎮める (しずめる), "calm; quiet; suppress", is a different verb with a different spelling. `words\泊める.md:43-45` already does this for 止める.
- **Evidence:** Jisho (JMdict data) lists しずめる [静める, 鎮める] as a transitive ichidan verb meaning "to quiet… to calm… to suppress", with "esp. 鎮める" on sense 3.
- **Confidence:** Medium-high.

## Optional
These are nonblocking improvements:

1. **`kanji\油.md:43`:** You could give the usual tendency: 油 for oils that are liquid at room temperature, 脂 for animal fat and skin grease. Kotobank's 世界大百科事典 entry for 油 makes this split for fats and oils. The current hedge is defensible because the boundary is not universal.
2. **`kanji\河.md:42`:** You could note that が also appears in 銀河 and 運河, so 氷河 does not look like a one-off voicing. Contrasting ガ with かわ is also an odd framing.
3. **`kanji\沈.md:45`:** "spelling list" should be "reading list".
4. **`kanji\泉.md:41`:** "a defensible river-source meaning" is garbled.
5. **`kanji\況.md:44`:** 況んや is an emphatic expression, not a "situation noun".
6. **汚す and 汚れる word quiz:** They have no exclusion, and English "soil" and "stain" can be intransitive. Repo precedent (止まる/止める, 壊す/壊れる) leaves such pairs unexcluded, so an exclusion is optional.
7. **Larger kanji quizzes only:** some English title words overlap. These are 毛 "down" vs 下 "down, below", and "circumstances" in both 況 and 情. They also include 泊 vs 宿 and 留, 永 vs 久, and 氷 vs 凍. The default quiz is unaffected because each older card has three curated distractors.
8. **Small additions:**
   - The 川 Notes could link 河.
   - 沈める could mention 浮かべる as an antonym.
   - The missing exclusion between 宿泊 and 泊まる predates this batch and is out of scope.

## Limits
- **No Git:** I could not check the diff, worktree state or commit identity.
- **Not reviewed:** stroke drawing paths and `docs\n2-source-snapshot.json`.
- **Unreachable sources:**
  - The Bunka-chō 異字同訓 PDF timed out twice, so the official 油/脂 guidance is unverified. It is only used in an Optional item.
  - EDRDG JMdictDB requires a password.
  - The Jisho HTML search for 汗する returned nothing, so I used the Jisho API instead.
- **Evidence limits:** batch-12 is a selected extraction, not the complete dictionary. These verdicts are not native-speaker certification.
