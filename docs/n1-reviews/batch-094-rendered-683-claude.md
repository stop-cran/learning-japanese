# Batch 094 rendered confirmation: 削 / 削る / 削除 / 除 — one low-severity quiz exclusion needed

The articles and rendered screens hold up, but one quiz pair needs fixing. In real word-quiz output, 削る ("shave; pare; cut down") appears next to 縮める ("shorten; reduce; shrink"), and the two meanings overlap on "reduce" (detail in Findings). The fix is to add 縮める to the quiz exclusions in `words\削る.md`. Everything else is CLEAN within this bounded scope.

## Snapshot
- Signed content: HEAD 577eb626. Native full archive 18ad4bed. Teaching snapshot 4089e881 (unchanged since my confirmation). Content version eeae47753a460f72.
- This is a dependent confirmation in my original session, not a fresh blind review.

## Scope
- **Model and session:** claude-opus-5.5, session edf22897-9f87-4a3b-b20f-4c2fd839013a.
- **Text read:** chunks 683-01 through 683-12, each read whole with no ranges. They include:
  - my two earlier reports and the native receipt;
  - the full current articles 削, 削る, 削除, 除 and 縮める;
  - the two JMdict entries 1298090 (削る) and 1337570 (縮める);
  - the quiz rules section of `docs/content-format.md` (lines 152–177);
  - all 64 kanji pool records (indices 0–63);
  - all 384 word guard records (indices 0–383);
  - the mapping from contact sheets to original screenshots.
- **Images viewed:** font panels 1–5 and contact sheets 01–20, all decoded. I did not open any original screenshot individually.
- **Read-order breach:** panels 1 and 2 were requested together in one response, which breaks the one-view-per-response rule. Everything after that was read one at a time.

## Verdicts

| Item | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| `kanji\削.md` | CLEAN | CLEAN | CLEAN |
| `words\削る.md` | **NEEDS FIX** (Low: quiz metadata only; the teaching text is correct) | CLEAN | CLEAN |
| `words\削除.md` | CLEAN | CLEAN | CLEAN |
| `kanji\除.md` line 41 | CLEAN | CLEAN | CLEAN |

**Bounded rendered and quiz checks**

| Check | Verdict | What I saw |
|---|---|---|
| Rendering of the four articles | CLEAN | All four articles display fully. |
| Reading tables | CLEAN | Left- and right-scrolled captures together show every cell, including 斫る. |
| Links and System Back | CLEAN | All three link pairs and six directions are captured. |
| Quiz screens | CLEAN | The N1 selection screen, meaning question and feedback, and the curated さく/けずる reading questions all display correctly. |
| Drawing | CLEAN | Trace, graded feedback and recall feedback screens display correctly. |
| Kanji meaning choices | CLEAN | All 64 pool records and the default labels 弐 "two (formal numeral)", 乏 "scarce; lacking" and 刑 "criminal punishment" are clearly wrong answers for "shave; sharpen; pare". |
| Word-quiz pairing | **NEEDS FIX** | The 削る/縮める pair (see Findings). |

## Findings

1. **Low; quiz correctness; `words\削る.md:9`. Proved under the repo's own exclusion rule.**
   - **Claim and impact:** the production builder puts 縮める ("shorten; reduce; shrink") alongside 削る ("shave; pare; cut down") in guard records 7, 15, 23, 31, 135, 143, 151 and 159 (pool All, seeds 7 and 15, both quiz directions). A learner could reasonably accept either answer for either word:
     - JMdict gives 削る sense 2 as "to cut down (budget, expenses, staff, time); to curtail; to reduce".
     - The 削る article teaches cutting a budget or time.
     - The 縮める article teaches shortening meeting time (会議の時間を縮めました) and condensing text.
     - Both words already exclude 減らす, so the repo already treats a "reduce" overlap as exclusion-worthy.
     - A learner who correctly reads 削る as "reduce" could be marked wrong.
   - **Remedy:** append 縮める to the quiz exclusions in `words\削る.md` (or add 削る to 縮める's list). No prose or title changes.
   - **Confidence:** medium. The correct answer's "shave; pare" is still distinctive, so this is a fairness problem, not a correctness collapse.
   - **Not warranted:** 縮む ("shrink; contract") is intransitive and has no "cut/reduce" sense. 圧縮 ("compression; condensing") does not overlap 削除 ("deletion; erasure").

## Reconciliation
- **削除/省く hypothesis:** resolved, as before. The 省く guard is confirmed in records 256–383.
- **削る/除く and 削る/外す:** resolved and confirmed in records 0–255.
- **My original claim that the exclusions cover the real overlaps:** further withdrawn. Besides 除く and 外す, I also missed 縮める.
- **All earlier optional polish:** unchanged and still optional.
- **Out-of-scope hypothesis, not a finding:** 除く ("remove; exclude") appears beside 取り出す ("take out; pick out; retrieve"). The overlap is weak and 除く is not assigned to this batch.

## Optional
- In the 削 meaning paragraph, the 削る link breaks across lines as "削 / る". Cosmetic.
- 削.md's common-words line glosses 削る as "shave; sharpen; cut down", while the 削る title is "shave; pare; cut down". Consistency only.

## Limits
- **Image scale:** contact sheets are reduced, but the text was legible, so I opened no originals.
- **Contact-sheet labels:** Japanese file names show as empty boxes in the sheet labels. That is an artifact of the sheet generator; the chunk 12 mapping resolves them.
- **Fonts:** the Textbook font panel falls back to a different font for 斫, 刂, 氵 and 阝.
- **Handwriting:** drawing was "Graded by stroke shapes only (handwriting model not available)", so ML Kit handwriting recognition is not certified. The trace screen also shows a "Downloading the handwriting model" message.
- **Screenshots vs. transitions:** the images show where each link ends up, not the tap itself; the transitions rely on the receipt.
- **Sample size:** the 64 pool records and 384 guard records are bounded samples. They do not prove that random fallback is safe in every case.
- **Not done:** no fresh full 121-family review; no upstream, Git or signature verification; no reviewer-run native tests. No physical phone, general release, whole-set acceptance or publication claim. The evidence comes from a test-only emulator build, not the latest app main. Only bounded textual closure is recommended, and only after the 縮める exclusion is added.
