# SAME082: confirmation of the 准 distractor change (9ce870d1)

The real edit matches the proposal I accepted, line for line, and nothing else on the card changed. At content level my earlier finding (082-V1, the "imitate; emulate" quiz option) is resolved. It stays unverified at runtime until fresh host and native runs check the actual quiz options on the new content version.

## Snapshot

- **Correction snapshot:** 9ce870d190d5c519d65ed20b118de64371350c0c.
- **Previous snapshot:** cadd1054ff865b7c08fdeaff19f0439a02cf5073.
- **Content version:** d82e7fefe3898a70 (previously 0739a82c9699f031).
- **Model:** Claude Opus 5.5 (claude-opus-5.5). Only `view` was available.

## Scope

**What I read:**
- I read `docs\n1-reviews\batch-082-choice-confirmation-packet.txt` with one view call. There was no truncation notice and no denied access.
- Contents: the full current 准.md (65 lines), 冴.md and 冶.md (67 lines each) and 隼.md (73 lines), the runtime diff (35 lines) and the correction audit (238 lines).
- That totals about 545 numbered lines plus headers, which fits the stated 558. I did not count the packet's own lines.

**What this is based on:**
- My linguistic and source conclusions come from my earlier full-packet reads, not fresh upstream lookups.
- I did no Git or hash verification.
- No new host or native runs, and no screenshots.

## Is the edit correct, with no regressions?

**The change is exactly the one proposed:**
- The diff changes only `kanji/准.md` line 13, from `distractors: [集, 進, 難]` to `distractors: [冴, 冶, 隼]`.
- The only other change is in `manifest.json`: the content version moves from 0739a82c… to d82e7fef…, and the hash entry for 准.md is updated.

**Nothing else on 准 regressed:**
- I compared the current 准.md, line by line, with my cadd1054 reading. Lines 1–12 and 14–65 match: title, level, tags, strokes, radical, ジュン reading with empty kun, quiz keys, prose, mnemonic, readings table, Common words, Notes, links and metadata.
- The look-alike note at lines 58–60 still compares 集, 進 and 難. That is accurate and still useful. Quiz options don't need to match comparison prose.

**The three candidate cards are unchanged.** 冴, 冶 and 隼 have the same SHA256 values as in the previous packet. Each is N1, tagged jlpt-n1, with titles "clear; sharp-minded", "smelt; work metals" and "falcon".

**The new options should all appear.**
- According to the audit, all four meanings are distinct.
- The quiz builder picks options from the selected study level and uses 4 options by default (`QuizViewModel.kt:157` uses the default `count = 4`).
- So in both the N1 and All quizzes, the three listed distractors fill every slot and the tag-similarity fallback (and with it 倣) is never reached. This depends on all three cards being imported with these titles. I accept that as supplied; it is not checked at runtime.

**Hash note, not a finding:** the manifest's hash for 准.md (1465a5c8…) differs from the packet's file SHA256 (fc6907e7…). The previous pair also differed (3a118e5e… against a5aca406…), so the manifest probably hashes in a different way. I could not verify either.

## Verdicts

| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Current `准.md`, all content including line 13 (source level) | CLEAN | CLEAN | CLEAN |
| `准.md:13` at runtime on d82e7fef (actual options shown) | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| `准教授.md`, `教.md:39`, `助教授.md:16` (not changed in this snapshot) | CLEAN | CLEAN | CLEAN |

## Findings

None at content level.

## Status of earlier concerns

- **082-V1 ("imitate; emulate", my earlier finding at `准.md:13`):**
  - Resolved at content level for the default four-option N1 and All quizzes.
  - Unresolved at runtime: the old native result on 0739a82c does not count as acceptance of d82e7fef.
- **What the fix does and does not settle:**
  - The swap avoids the question rather than answering it.
  - The rare 准える "imitate" overlap stays documented: real, but not proven common.
  - The earlier capture showing "imitate; emulate" as an option remains part of the record.
- **My earlier claim that 準's listed distractors (集/清/卒) protect its quiz** is still unverified. It is outside this change.
- **The concern about larger or uncurated quiz pools** is still unresolved.

## Optional

- 准's Notes could mention 冴 and 冶 as shapes that share 冫. This is not required.
- Other cards whose listed distractors fall outside their own level may hit the same fallback. That is a whole-set hypothesis; any fix would be an app change that has not been approved.

## Limits

**Still needed for runtime acceptance, on the current version:**
- fresh host and native runs
- checks that the options shown are exactly 冴, 冶, 隼 plus 准, all with distinct meanings
- new screenshots

**Fonts:** the font scope has grown to 34 Han characters, adding 冴, 冶 and 隼. Fresh renders in all four font families are still pending. The old 31-character renders are historical evidence only. The fonts' missing coverage for 冫, 氵, 辶 and 隼's component 隹 is not evidence of whether they are legible.

**Not covered by the content-level resolution:**
- larger, custom or partial quiz pools
- option counts other than four
- missing candidate imports
- future changes to how the quiz picks options

**Still unresolved from earlier phases:**
- physical phone, native-speaker and learning-effectiveness evidence
- general release and the whole set
- final integration with current main, publication, CI and an immutable ZIP
- all read-depth, OOM, denial and ML Kit limits

Every runtime fact here (code excerpts, audit counts, N1 membership) was supplied to me, not run by me.
