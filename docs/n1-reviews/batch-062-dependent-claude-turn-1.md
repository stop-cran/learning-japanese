# Batch 062 — Turn 1 of 2: dependent confirmation for `words\俸給.md`

My original conclusions for `words\俸給.md` still hold: correctness, scoped coverage and comprehensibility are all CLEAN, with no findings. This is a dependent confirmation in the original session, not a new blind review, and it does not make the original review retroactively compliant. Some line numbers in my original report were wrong; corrections are below.

**Snapshot:** Frozen teaching snapshot `38ab6072d2041325142c54cf54be5d126928eb31`. The coordinator reports an empty git diff to evidence HEAD `322e2002b0b8dd84fbb1407cdacd4bee58519211` for runtime teaching and the manifest. I had no git access, so I could not check that independently. No teaching was fixed.

**Scope:**
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`).
- **This turn:** exactly one tool call, `words\俸給.md` lines 1–53. I read the whole file again.
- **Not reread:** the JMdict, KANJIDIC2 and Kotobank evidence and the comparison articles. I relied on what I read in the original review; nothing was fetched again.
- **Not certified yet:** `kanji\給.md` waits for turn 2.

**Verdicts: `words\俸給.md`** — correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **Identity:** 俸給 / ほうきゅう, `kanji: [俸, 給]`, `kango`, title "salary; pay". This matches JMdict 1515280, glossed "salary (esp. public employees); wages; pay". There is no `jlpt` field, so no level is inferred from the kanji.
- **Meaning:** The article links the word to public employees without restricting it to them, and says it also covers company employees. That matches the original Nikkoku Seisen retrieval: 官公吏などの職務… and 一般に、会社などの勤め人に支給する賃金。給料.
- **Examples:**
  - 俸給を受け取っています。(ほうきゅうをうけとっています。) — "I receive a salary."
  - 俸給が上がりました。(ほうきゅうがあがりました。) — "My salary went up."
  - Both are grammatical, and their kana and translations are correct. The を note is accurate.
- **Components:** 俸 contributes salary/stipend and 給 contributes giving/paying. The reading splits as ホウ + キュウ, and the article keeps both long vowels.
- **Comparisons:** 給料, 給与, 月給 and 収入 are linked and accurately distinguished. The article invents no fixed payroll categories and makes no claim about payment interval.
- **Source note:** The JMdict IDs are correct: 1515280 for 俸給; comparisons 1230360 (給料), 1230350 (給与), 1255560 (月給) and 1330790 (収入). The Kotobank Nikkoku link is the page I originally retrieved.
- **Quiz exclusions:** All nine direct pairs remain defensible: 給料, 給与, 月給, 収入, 支給, 支払, 払う, 支払う, 代金. They are pairwise only, not a clique, and the earlier title search found no further guard the evidence requires.
- **Links:** 俸給 → 俸 is at physical line 29 and 俸給 → 給 at line 30. The links from 俸 and 給 back to 俸給 are left for turn 2 or previously retained evidence.

**Findings:** None.

**Corrections to the original report:**
1. **Line citations.** In the original report, the 俸給 → 俸 and 俸給 → 給 links are at lines 29–30, not 30–31. Optional item 3 should cite lines 30–31.
   - Counting from the views I had retained (not freshly reread), the 俸.md → 俸給 links appear to be at lines 23, 36 and 44, not 22, 34 and 40.
   - The rice sentence in 俸.md (optional item 1) appears to be at line 57, not 59.
   - The added bullet in 給.md appears to be physical line 40, not 37. Turn 2 will confirm this.
   - These are citation errors only; the conclusions do not change.
2. **The 140-line claim was false.** Audit 062-P2 is correct: the `docs\content-format.md` range 1261–1405 was 145 inclusive lines, over the 140-line cap. I am not rereading it to cover this up.
3. **Read-discipline violation.** Audit 062-P1 is correct: one response contained two view calls, starting `words\俸給.md` 1–53 and `kanji\給.md` 1–45 together. All assigned source content was still returned.

**Optional:** Unchanged and not adopted. The two items touching this file are:
- naming 給料 as the usual everyday word (not verified as a register claim);
- naming the relationship between the two kanji explicitly.

**Limits:**
- The source evidence is carried over from the original review, not retrieved again.
- The original Kotobank limits still apply:
  - publisher headings that returned only attribution are not verified definitions;
  - the 俸 page was truncated at 5,000 characters;
  - the historical character-page variants and extra readings were not adopted.
- I have no native-speaker, device, phone, rendering, drawing or runtime evidence.
- Larger or live quiz pools are not certified.
- Whether all three files' conclusions together still hold is for turn 2.
