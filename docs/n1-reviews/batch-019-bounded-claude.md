**Snapshot:** commit `3e2bf34ee3b9621cbaec8713f2b157fdeb74c764`. No teaching diff and no uncommitted teaching.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the original batch 019 review session. This is a bounded confirmation, not a second blind initial review.
- **Files read, one call at a time:**
  - my original report, `docs\n1-reviews\batch-019-initial-claude.md`, read in full;
  - `words\蚊.md` lines 18–30;
  - `kanji\蚊.md` lines 28–46.
- **Web source:** the Kotobank 蚊 page, raw HTML window from character 70000 (3,500 characters). This is the start of the Seisenban entry. I did not fetch it again from 64000; the Daijisen window there was already in my original read.
- **Not reopened:** the dictionary packets, comparison cards, guidance and other reports.

**Verdicts:** unchanged.
- `kanji\蚊.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\蚊.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:** none.

**Reconciliation of original observations:**

1. **Unsourced "ordinary modern か is not かあ" (`kanji\蚊.md:44`): withdrawn as a limitation. Not a defect, and no unresolved claim remains.**
   - **Modern headings are short:** Seisenban's heading is か【蚊】 (〘名詞〙, the Diptera family 蚊科), and Daijisen's is also か【蚊】. JMdict 1196540 gives か and カ.
   - **The long form is historical:** Seisenban's supplementary note (補助注記) cites ancient sound glossaries. 新訳華厳経音義私記 writes 加安 (カア), and 金光明最勝王経音義 writes 加阿. The note concludes the word "is thought to have been pronounced as a long カー."
   - **The card is consistent with this:** its wording ("ordinary modern") is correctly limited to the present-day short form. The cited Daijisen URL supports the modern reading.
   - **Possible addition (not required):** the historical long pronunciation is out of scope (no historical reconstruction), so the card does not need to mention it. If the authors want a pinpoint source, they could add the same page's Seisenban note.
   - **Confidence:** high.
2. **Optional 1, gloss 一匹 "one" more explicitly (`words\蚊.md:21`): withdrawn.**
   - The sentence already says "The counter for this small creature is 匹". The example at line 19 also shows 一匹 counting a mosquito. In that context "one" is clear, and the change is not needed for any facet.
   - **Confidence:** high.
3. **Optional 2, whole-word 蚊帳 かや (`words\蚊.md:30`; `kanji\蚊.md:37`): optional, retained as nonblocking.**
   - Both files present 蚊帳 かや only as a complete word with a gloss. Neither splits the reading by character, and the reading table does not list 蚊帳 under か.
   - No incorrect allocation is stated, and the stated scope does not require explaining the irregular 帳→や part.
   - Pointing out that Daijisen marks the word as hard to read remains a possible polish, not a requirement.
   - **Confidence:** high that this is not a defect.

**Optional:**
- Note that the reading かや belongs to the whole word 蚊帳.
- Pinpoint the Seisenban note on the historical long pronunciation, without making it part of the teaching.

**Limits:**
- **No fresh Daijisen extraction:** I did not re-extract the 64000 window. The Daijisen evidence relied on here comes from my original read in the same session.
- **Unrendered images:** the gaiji images on the page were still not rendered. They do not affect the cited text.
- **Text only:** this confirmation gives no fresh native, phone, Android, combined-main, CI or publication evidence.
- **Historical process deviation preserved:** my initial review sent one pair of reads together (`content-structure.instructions.md` and `content-format.md`). This serial confirmation cannot make that earlier run fully serial. All five calls in this confirmation were sequential.
