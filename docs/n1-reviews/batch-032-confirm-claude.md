The original finding is resolved: the revised `words\鶏.md` now excludes 鳥 alongside 鶏肉, and the two new links introduce no regressions.

**Snapshot:** I compared the original snapshot `2cbbb0b836a5a2363a175a0df7cd14f12c5f99fc` with the revised snapshot `23ce40fee3aea6718d56958c2b9f24e5d813bac7`. No uncommitted teaching was included. This checks only the changed passages; it is not a new blind review.

**Scope:**
- **Reviewer:** Claude Opus 5.5, the same session as the original review.
- **Read for this check, one call at a time:**
  - my archived original report (`docs\n1-reviews\batch-032-initial-claude.md`)
  - the correction diff (`control\batch-032-correction.diff`)
  - the whole current `words\鶏.md`, `words\鳥.md`, `words\鳴く.md` and `words\肉.md`
  - JMdict entries 1252990 (lines 95–144), 1253020 (174–213) and 1430250 (302–344)
  - `content-format.md` lines 120–148 and `content-structure.instructions.md` lines 15–22
- **Not reread:** `kanji\鶏.md` and `words\鶏肉.md` are not in the diff. My original review of them still stands. I did not reread all 131 dictionary families.

**Verdicts (changed scope only):**
- **`words\鶏.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
  - The new exclusion list `[鶏肉, 鳥]` uses the allowed inline-list format with existing, non-repeated IDs.
  - The two new links, to the 鳴く and 肉 articles, point to existing articles. The surrounding descriptions match those articles: 鳴く as "make an animal call", and 肉 as on-reading にく for meat.
  - The rest of the article is the same as at the original snapshot.
- **`kanji\鶏.md`:** unchanged; my original verdicts (all three facets CLEAN) still apply.
- **`words\鶏肉.md`:** unchanged; my original verdicts (all three facets CLEAN) still apply.

**Findings:** none new.

**Original finding reconciliation:**
- **Status:** resolved.
- **Original finding:** `words\鶏.md:8` lacked a 鳥 exclusion (Minor; quiz metadata).
- **Fix:** line 8 now reads `quiz_exclusions: [鶏肉, 鳥]`.
- **Why the pair is justified:**
  - JMdict 1430250 gives 鳥/とり a second sense, "bird meat (esp. chicken meat)". This sense is marked "esp. 鶏" and is not restricted to one spelling.
  - The `words\鳥.md` article (lines 39–41) teaches that とり can mean chicken meat in food contexts.
  - English "chicken" can also mean the food, so 鳥 is a defensible answer for the "chicken" label.
- **Effect:** the format contract says one declaration excludes the pair in both directions (lines 133–136). This also covers the reverse case, where "bird" could reasonably be chosen for 鶏.
- **Scope of the guard:** it is a single direct pair. It does not imply 鳥 and 鶏肉 must be excluded, and it does not require editing the reused 鳥, 肉 or 鶏肉 articles.

**Optional:**
- **Adopted:** linking 鳴く from the 鶏 examples, plus a new 肉 link.
- **Still optional:**
  - link 飼う
  - link the now-existing 鶏 article from `words\鶏肉.md`
  - note that 雄鶏/雌鶏 are usually written in kana (おんどり/めんどり)
  - plainer wording for the 酉 zodiac sentence
  - existing 鳥 kanji and word cards mention 鶏 without linking it
  - a kanji quiz larger than four choices could pair "chicken" with 鳥 "bird"

  None of these shows a consequential defect within scope.

**Limits:**
- I didn't count file lines myself. Every file returned fully, including its end, and the lengths look consistent with 48/42/41/36 lines.
- I did not check app behaviour for the exclusion.
- This was a text-only review. Font/native rendering, physical-phone, latest-main, fresh Android, CI and public-ZIP checks are still outstanding. A compatible Android build `f9b59a2` or later is required.
- I have no process records beyond my own one-at-a-time calls.
