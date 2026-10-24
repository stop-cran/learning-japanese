I reviewed the corrected snapshot and confirm the corrections. All five of my initial findings are fixed, the seven added and one removed exclusion each hold up, and I found no new defects. All twenty rows are CLEAN in every cell.

## Snapshot
Corrected commit **4917e82133f4f6e88fd8f4e5409a1109689411ae**; parent **88560e5b110c4e8b78922c8e3efedecbd1c99559**. The receipt says the committed content is clean and that 9 files changed. My file tools can't run Git or check hashes, and I didn't look inside `.git`. Commit, cleanliness and hashes are therefore the author's claims, not mine.

## Scope
- **Model:** claude-opus-5.5 (Claude family).
- **Read completely in this session:**
  - The correction-snapshot receipt and `correction.patch`.
  - All nine changed articles: 逸れる, 揃う, 揃える, 太鼓, 大層, 体積, 体制, 対策 and 大して.
  - `corrective-comparison-reading.txt`: 15 families and 42 senses, which I counted myself. They include 量 はか (2817380) and the sports-ground グランド (1046340).
  - `corrective-existing-reading.txt`: the seven old articles 作る, 量, グランド, ずっと, 楽器, 政府 and 予防.
  - `corrective-public-bodies.txt`: the Daijisen ずっと capture, which the author fetched, not me.
- **Read in part:**
  - Original `public-bodies.txt`, lines 1–16 (逸れる) and 185–215 (対策).
  - `corrected-review-evidence.json`, lines 26600–26700 and 26990–27120 only (the correction section). That section includes the author's comparison of the two reviewers; I didn't use it as evidence.
- **Spot-checked:**
  - TSV rows N2:962–981.
  - The edit lines in the four kanji cards and in 大小.md (lines 5 and 47).
  - The exclusion lines of the ten unchanged new articles. Counting all 19 gives **141 exclusions**, which matches 135 + 7 − 1.
  - The titles and exclusion lists of こしらえる, 準備, 用意, うんと, 大, 立派, 数, 大小 and 防ぐ.
- **Carried over from my initial review (not reread):** the bodies of the ten unchanged new articles, 大小, the four kanji cards, and my earlier kotobank fetch for 対照.
- **Not read:** `review-labels.jsonl`, `review-principals.jsonl`, `selected-families-02` to `-10`, `public-bodies.json`, `kanjipedia.json`, and the rest of the corrected evidence JSON. I read none of the prohibited files and fetched nothing from the web this session.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:962 | 逸れる (new) | Complete reread + Daijisen capture | CLEAN | CLEAN | CLEAN |
| N2:963 | 揃う (new) | Complete reread | CLEAN | CLEAN | CLEAN |
| N2:964 | 揃える (new) | Complete reread | CLEAN | CLEAN | CLEAN |
| N2:965 | 算盤 (new) | Carried over + TSV/算 spot-check | CLEAN | CLEAN | CLEAN |
| N2:966 | 存じる (new) | Carried over + TSV spot-check | CLEAN | CLEAN | CLEAN |
| N2:967 | 存ずる (new) | Carried over + TSV spot-check | CLEAN | CLEAN | CLEAN |
| N2:968 | 損得 (new) | Carried over + TSV/損 spot-check | CLEAN | CLEAN | CLEAN |
| N2:969 | 田んぼ (new; source spelling 田ぼ) | Carried over + TSV spot-check | CLEAN | CLEAN | CLEAN |
| N2:970 | 第一 (new) | Carried over + exclusion-line spot-check | CLEAN | CLEAN | CLEAN |
| N2:971 | 大学院 (new) | Carried over + exclusion-line spot-check | CLEAN | CLEAN | CLEAN |
| N2:972 | 大工 (new) | Carried over + exclusion-line spot-check | CLEAN | CLEAN | CLEAN |
| N2:973 | 体系 (new) | Carried over + exclusion-line spot-check | CLEAN | CLEAN | CLEAN |
| N2:974 | 太鼓 (new) | Complete reread | CLEAN | CLEAN | CLEAN |
| N2:975 | 対策 (new) | Complete reread + original Daijisen capture | CLEAN | CLEAN | CLEAN |
| N2:976 | 大して (new) | Complete reread | CLEAN | CLEAN | CLEAN |
| N2:977 | 対照 (new) | Carried over (incl. my kotobank fetch) | CLEAN | CLEAN | CLEAN |
| N2:978 | 大小 (reused) | Carried over + lines 5/47 spot-check | CLEAN | CLEAN | CLEAN |
| N2:979 | 体制 (new) | Complete reread | CLEAN | CLEAN | CLEAN |
| N2:980 | 体積 (new) | Complete reread | CLEAN | CLEAN | CLEAN |
| N2:981 | 大層 (new) | Complete reread | CLEAN | CLEAN | CLEAN |

**対策 (row 975):** I've moved correctness from my initial UNVERIFIED to CLEAN. The original Daijisen capture (`public-bodies.txt:191-201`) does show たい‐さく【対策】, 読み方 たいさく, ［名］(スル), then sense 1 with 「―を立てる」「―を練る」. That supports the article's hedged sentence at lines 41–43. This rests on the author's capture, not a fresh retrieval of my own.

**Four kanji edits: CLEAN, unchanged.**
- 算 keeps the source-only そろ row (line 31), the separate whole-word そろばん row (line 32) and the caveat (line 34).
- 損 has ソン/損得 at lines 30 and 40; 照 has ショウ/対照 at lines 30 and 39.
- 層 has ソウ/大層 at lines 28, 35 and 41.

**大小 preservation: CLEAN.** Only `jlpt: 2` (line 5) and the citation (line 47) were added. Leaving the old explanation as it was is correct under the preservation rule.

**Mappings: CLEAN, unchanged.**
- The raw source spelling 田ぼ and its normalization note are intact.
- 存ずる's raw gloss is still blank.
- The extra senses 1596700:2 (算盤) and 1406140:2 (存じる) are still recorded separately from the selected senses.
- The selections and draft status are unchanged.

## Findings
**My initial findings:**
- **B49-01 (揃う/揃える): resolved.** 揃う.md:9 now excludes 揃える, and one listing covers both directions.
- **B49-02 (太鼓/楽器): resolved.** 太鼓.md:9 now excludes 楽器, matching how 楽器 already excludes specific instruments (笛, ピアノ and others). This is a precaution against the broad "musical instrument" label, not a claim that the two words mean the same.
- **B49-03 (大層/ずっと): resolved by removal at 大層.md:9.** I withdraw my claim that the list was copied from うんと; a similar-looking list doesn't show how it was drafted.
  - ずっと's title is "the whole time; much more", and Daijisen's sense 1 is comparative (はるかに).
  - 大層 sense 1 is an absolute "very".
  - うんと ("a lot; very much") still excludes ずっと, which is reasonable because うんと is also used in comparisons. Any remaining overlap is small.
- **B49-04 (逸れる): resolved at 逸れる.md:23–26 and 50.** The new example 話が脇道へそれる, its kana, translation and explanation of へ match Daijisen sense 2 (`public-bodies.txt:9`). No を pattern is needed, and I withdraw that optional suggestion.
- **B49-05 (太鼓 reference to an invisible list): resolved at 太鼓.md:35–37.**
- **My earlier optional suggestions:** 体制/政府 and 対策/予防 were adopted. The 大して/大層 register wording was polished at 大して.md:45–46 and now matches 大層.md:44.

**Three additions my initial review did not catch.** I checked each on its own evidence and agree with all three:
- **揃える/作る:** 揃える already excluded こしらえる ("make; prepare; fabricate"), and 作る's title is "make; prepare". JMdict 揃える sense 2 includes "to prepare".
- **体積/量:** the 量 article teaches "quantity, amount, volume". JMdict 量 sense 1 includes "volume, capacity", and both words carry a measurement tag. The separate はか family plays no role here.
- **大層/グランド:** both titles contain "grand" (グランド entry 1046840: "grand; large"). The sports-ground entry 1046340 plays no role.

**Other new exclusions:** the precautionary 体制/政府 and 対策/予防 pairs overlap on regime/government and countermeasure/precaution. Neither is excessive.

**New actionable defects:** none.

## Optional
None.

## Limits
- I ran no Git, cleanliness or hash checks myself.
- The 対策 (スル) label and the Daijisen ずっと text come from captures the author made. My own earlier fetches didn't return the 対策 Daijisen text, so that is a retrieval limit, not evidence either way.
- The ten unchanged articles, 大小 and the kanji cards rest on my initial reading plus spot-checks. That initial reading covered only one of the ten family files and mostly the front matter of existing articles, and it missed three exclusions. Other missing exclusions are therefore possible.
- I didn't check that the corrected evidence packet matches the author's source file.
- Whether two words need an exclusion is an editorial judgment. I didn't test the live quiz, and none of this certifies how a native speaker would judge naturalness.
