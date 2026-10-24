I found five quiz-label and teaching issues, all Minor or Low. None is a major factual or grammar error.

## Snapshot
The frozen commit is `fa390bf5776402ca8a27fac55cb75990d1f37b1d` (parent `618886c128b550c64f52c61ab3e76c98c17436a6`). I reviewed the committed files as they appear in the working tree. I had file tools only, with no Git, so I could not confirm the frozen commit or recompute any hashes.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked alone and edited nothing.
- **Read in full:** the frozen receipt; the three guidance files (`content-format.md` lines 18–126, plus lines 63–90 again); all 20 new articles; the five-file patch; the full 了, 周, 祝, 辺 and 量 kanji files; mapping rows N2:722–741.
- **Evidence file:** I read the rows, the 20 main word records, the list of comparison cards the author checked, all existing card titles and exclusions (lines 26660–28244), the public-dictionary receipts and the quiz declarations.
- **Other cards checked:** the titles and exclusions of existing cards in `words\` that could be confused with the new words. No existing card lists any new word in its exclusions.
- **Web:** Kotobank's Daijisen entry for 重点 confirmed the article. The 住居 lookups returned only encyclopedia text, so they prove nothing.
- **Not read:** the forbidden files; most of the comparison word records (lines 2788–26660); most of the kanji component records (lines 1539–2528); `batch-37-comparisons-compact.txt` beyond line 80.

## Verdicts
Each cell reads correctness / scoped coverage / comprehensibility.

| Article | Verdict |
|---|---|
| 住居 | UNVERIFIED / NEEDS FIX / NEEDS FIX (B37-01) |
| 集金 | NEEDS FIX / CLEAN / CLEAN (B37-04) |
| 集合 | CLEAN / CLEAN / CLEAN |
| 習字 | CLEAN / CLEAN / CLEAN |
| 修繕 | CLEAN / CLEAN / CLEAN |
| 重体 | CLEAN / CLEAN / CLEAN |
| 絨毯 | CLEAN / CLEAN / CLEAN |
| 終点 | NEEDS FIX / CLEAN / CLEAN (B37-02) |
| 重点 | CLEAN / CLEAN / CLEAN |
| 就任 | CLEAN / CLEAN / CLEAN |
| 周辺 | NEEDS FIX / CLEAN / CLEAN (B37-03) |
| 重役 | CLEAN / CLEAN / CLEAN |
| 終了 | NEEDS FIX / CLEAN / CLEAN (B37-05; also side of B37-02) |
| 重量 | CLEAN / CLEAN / CLEAN |
| 重力 | CLEAN / CLEAN / CLEAN |
| 熟語 | CLEAN / CLEAN / CLEAN |
| 祝日 | CLEAN / CLEAN / CLEAN |
| 縮小 | CLEAN / CLEAN / CLEAN |
| 受験 | CLEAN / CLEAN / CLEAN |
| 主語 | CLEAN / CLEAN / CLEAN |

**Kanji edits (了, 周, 辺, 量, 祝):** all CLEAN on all three facets.
- 終了 is linked at リョウ, 重量 at リョウ, 周辺 at シュウ and ヘン, and 祝日 at シュク.
- The dictionary entry IDs (JMdict) were added only where they were missing.
- All existing readings and source qualifications are still there.
- The seven kanji without cards (修, 繕, 絨, 毯, 就, 熟, 縮) appear in the word metadata but are not linked. That is correct.

**Mappings:** 19 are CLEAN on all three facets. N2:722 (住居) is CLEAN / NEEDS FIX / CLEAN. Its note says the "residential address" meaning is kept, but the article never shows it in use (B37-01).
- Dropping the source's "heavyweight boxer" gloss for 重量 is justified.
- The selected and additional senses for 重点 and 重役 match the dictionary records.

## Findings
**B37-01 (Minor): 住居's "address" meaning is never shown in use**
- **Facets:** coverage and comprehensibility.
- **Where:** `words\住居.md` lines 4, 16 and 20–21.
- **Problem:** The title and line 16 say 住居 can mean "address", but the only example (書類に住居の住所を書いてください) puts "address" on 住所. The sentence actually shows 住居 as the home that has an address, which contradicts the claim. A learner could also wrongly start using 住居 where 住所 is correct.
- **Fix:** Either add a sourced example where 住居 itself means the address, or present "address" as a dictionary-only gloss and replace the example. If "address" stays in the title, also consider excluding 宛名 ("addressee; name and address").
- **Evidence:** "address" comes only from the dictionary entry (JMdict 2841455). The author's own Daijisen receipt (evidence line 29236) mentions only dwelling, residence and residing.
- **Confidence:** medium.

**B37-02 (Minor): 終点 and 終了 can appear together in a quiz**
- **Facet:** correctness (quiz labels).
- **Where:** `words\終点.md` lines 9 and 21; `words\終了.md` line 9.
- **Problem:** 終点 ("terminus; final stop") excludes 終わり, 最後 and 末 because their titles say "end". 終了's title "ending; termination" overlaps in the same way. 終点's own example is translated "Where does this train terminate?". The two words share the kanji 終, so the quiz is likely to pick them together.
- **Fix:** Add 終了 to 終点's exclusions. One side is enough.
- **Lower-confidence extra:** 仕舞い ("end; finish") and 端 ("edge; end; tip") follow the same "end" logic.
- **Confidence:** medium-high for 終了.

**B37-03 (Minor): 周辺 can be confused with 郊外**
- **Facet:** correctness (quiz labels).
- **Where:** `words\周辺.md` lines 9 and 16.
- **Problem:** The article teaches 周辺 as including "outskirts", and the dictionary entry (JMdict 1331300) lists "outskirts". The existing 郊外 card is titled "suburbs; outskirts" and has no exclusions. 周辺 excludes the weaker "vicinity" labels (近く, 近所) but not 郊外. 郊外 appears nowhere in the evidence, so the author never compared it.
- **Fix:** Add 郊外 to 周辺's exclusions.
- **Confidence:** medium-high.

**B37-04 (Minor): 集金 can be confused with コレクション**
- **Facet:** correctness (quiz labels).
- **Where:** `words\集金.md` lines 9 and 35.
- **Problem:** "collecting payments" (集金) and "collection; collecting" (コレクション) share "collecting". In ordinary English, "collection" includes collecting money. The existing コレクション card already excludes 集める, 集まる and 集まり on this same wording. The 集金 article itself warns about "the broad English word 'collection'" but declares no exclusion.
- **Fix:** Add コレクション to 集金's exclusions.
- **Confidence:** medium.

**B37-05 (Low): 終了 excludes too much in one place and misses 結論**
- **Facet:** correctness (quiz labels).
- **Where:** `words\終了.md` lines 9, 21 and 37.
- **Problem 1:** The exclusion of 切る (title "cut") has no basis in the titles a learner sees. 切れる ("snap; run out; cut well") is weakly supported at best. These exclusions remove usable wrong answers.
- **Problem 2:** 結論 is titled "conclusion", and in everyday English "conclusion" also means "end". This article translates 終了 as "concludes" on line 21.
- **Fix:** Remove 切る (and possibly 切れる), and consider excluding 結論.
- **Confidence:** medium for 切る; medium-low for 結論.

## Optional
- **集合:** Excluding 学会, 大会 and 打ち合わせ seems generous, but the existing 集会 card does the same.
- **受験 vs 試験 ("examination; test"):** borderline, though the titles do separate taking an exam from the exam itself.
- **熟語 vs 諺 ("proverb; saying"):** English learners often blur "idiom" and "saying".

## Limits
- I could not run Git or verify any hashes.
- Dictionary facts come from the author's evidence file. I did not retrieve them independently.
- Of the public dictionaries, I personally checked only 重点. I could not confirm whether 住居 is actually used alone to mean "address".
- I read most of the comparison word records and kanji component records only in part, and did not use them to check whole records.
- Naturalness of the example sentences is my judgement, not a native-speaker certification.
