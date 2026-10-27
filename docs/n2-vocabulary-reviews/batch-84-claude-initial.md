I completed the review: all 20 rows, mappings, components, the three kanji edits and every required evidence range were read. I found six low-severity issues and no blockers.

## Snapshot
04e39de5d1d0055ec6702a224270bffa57e188e6, committed content only (parent bf0edffe59470653020849eb7cbb23614bba9495). File tools can't run Git, so the commit identity, clean status and hash/equivalence checks come from the author's frozen-snapshot.json. I did not verify them myself.

## Scope
- **Model:** claude-opus-5.5 (claude family). I used 74 of the 80 allowed tool calls, one at a time.
- **Instructions:** I read copilot-instructions, content-structure.instructions and content-format.md lines 18–103.
- **Articles:** I read all 20 assigned articles completely, and re-read most of them for line numbers.
- **Kanji and patch:** I read 税.md, 接.md, 材.md and related.patch in full.
- **Private evidence:** I read every required range without truncation: mappings (1–10, 11–20), principals (1–10, 11–20), components (1–15, 16–30), all 291 labels in six ranges, and public-bodies.txt (1–105, 106–210, 211–307).
- **TSV:** only the header [1,1] and rows [1662,1681].
- **Existence checks:** I checked which kanji cards and comparison words exist with two globs: 免, 儲 and 潜 have no cards; 若, 茶 and 苦 do.
- **Comparison bodies:** 寄る, 片寄る, 予算, はっきり and 迷惑.
- **Other:** one title grep of `words\`, and one jisho.org fetch for 寄る.
- **Not read:** the family-inspection, old-body-inspection, supplemental, final-precard and related-kanji-inspection files, review-evidence.json and public-bodies.json. I also did not read the forbidden ledgers or batch-84.json.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1662 | めちゃくちゃ | CLEAN | NEEDS FIX | CLEAN | B84-F01 |
| N2:1663 | めっきり | CLEAN | CLEAN | CLEAN | Possible はっきり guard is optional |
| N2:1664 | めでたい | CLEAN | CLEAN | CLEAN | Naive use goes through おめでたい, matching Daijisen |
| N2:1665 | メニュー | CLEAN | CLEAN | CLEAN | French origin matches Daijisen |
| N2:1666 | めまい | CLEAN | CLEAN | CLEAN | Novel/film titles correctly excluded |
| N2:1667 | 目安 | NEEDS FIX | CLEAN | CLEAN | B84-F05 |
| N2:1668 | 免税 | CLEAN | CLEAN | CLEAN | 免 has no card, so unlinked is correct |
| N2:1669 | 面積 | CLEAN | CLEAN | CLEAN | Possible 地域 guard is optional |
| N2:1670 | 面接 | CLEAN | CLEAN | NEEDS FIX | B84-F02 |
| N2:1671 | 面倒くさい (source 面倒臭い) | NEEDS FIX | CLEAN | CLEAN | B84-F06; spelling, both readings and on-first mixed type are correct |
| N2:1672 | 儲かる | CLEAN | CLEAN | CLEAN | Unexpected-advantage use matches Daijisen sense 2 |
| N2:1673 | 儲ける | CLEAN | CLEAN | CLEAN | 設ける shared origin matches Daijisen |
| N2:1674 | 申し訳ない | CLEAN | CLEAN | CLEAN | Polite-form note matches Daijisen |
| N2:1675 | モーター | CLEAN | CLEAN | CLEAN | |
| N2:1676 | 木材 | CLEAN | CLEAN | CLEAN | Separate きざい heading correctly set aside |
| N2:1677 | 目次 | CLEAN | CLEAN | CLEAN | |
| N2:1678 | 潜る | CLEAN | CLEAN | NEEDS FIX | B84-F03; もぐる (1609715) kept separate from くぐる (1609710) and obsolete むぐる |
| N2:1679 | もしかしたら | CLEAN | CLEAN | CLEAN | |
| N2:1680 | もしかすると | CLEAN | CLEAN | NEEDS FIX | B84-F04 |
| N2:1681 | もたれる | CLEAN | CLEAN | CLEAN | 寄る leaning sense confirmed (JMdict sense 6) |

**Kanji/baseline preservation: CLEAN.** The 税, 接 and 材 edits only add lines (reading links, common-word entries, sorted entry numbers; 材 also turns plain-text 木材 into links). Unrelated teaching and metadata are unchanged.

**Components: CLEAN.**
- Every article's kanji metadata covers the primary written form (面倒くさい = [面,倒]); kana headwords use `[]`.
- Existing cards are linked where the kanji is substantively introduced.
- 免, 儲 and 潜 have no cards, so leaving them unlinked is correct; no links were invented.
- 若, 茶 and 苦 appear only in notes on rare or ateji spellings, so linking them is optional.

**Reciprocity: CLEAN.** 免税/税, 面接/接 and 木材/材 link in both directions.

**Mappings: CLEAN.** All 20 rows match the TSV entry number, selected senses and level 2. 面倒臭い maps to 面倒くさい (entry 1533560). The raw 潜る gloss is preserved.

## Findings
- **B84-F01**; Low; Scoped coverage; words\めちゃくちゃ.md:16-21
  - Claim/impact: the "ruined/wrecked" use (めちゃくちゃになる/にする) appears only as an abstract mention of に "describing a manner or resulting state". There is no example or translation.
  - Remedy: add an example such as 雨で旅行の計画がめちゃくちゃになった ("The rain wrecked our travel plans").
  - Evidence: Daijisen sense 2 「せっかくの集まりを―にする」; TSV raw gloss "messed up, spoiled, wreaked".
  - Confidence: medium.
- **B84-F02**; Low; Comprehensibility; words\面接.md:16-17,22-24
  - Claim/impact: "Do not assume that 面接する by itself always identifies the applicant…" is a confusing double negative. It never says that the interviewer is the usual subject.
  - Remedy: say 面接する is usually said of the interviewer (役員が面接する), while applicants say 面接を受ける.
  - Evidence: Daijisen 「役員が―する」.
  - Confidence: medium-high.
- **B84-F03**; Low; Comprehensibility; words\潜る.md:47-48
  - Claim/impact: the sentence about the source list's "drive" and truncated "go undergroun" exposes source-data errors to learners. It also implies "go underground" isn't taught, though lines 18, 22 and 46 teach it.
  - Remedy: delete the sentence, or reword it to say "drive" is an error for "dive" and that going underground is taught above. The raw fields stay preserved in the mapping.
  - Confidence: high.
- **B84-F04**; Low; Comprehensibility; words\もしかすると.md:39-42
  - Claim/impact: the article quotes "By some chance", but the Meaning section (lines 16-17) never introduces that gloss, so "here" refers to nothing. The すると warning is also obscure.
  - Remedy: add "by some chance" to the line-17 glosses, or delete lines 41-42.
  - Confidence: medium-high.
- **B84-F05**; Low; Correctness (quiz_exclusions); words\目安.md:4,9,20
  - Claim/impact: 予算 ("budget; cost estimate") is a defensible answer for 目安 as a rough cost estimate. 目安 already excludes 見当, 予測 and 推定 for the same "estimate" overlap, and 予算.md has no exclusions.
  - Remedy: add 予算 to 目安's quiz_exclusions.
  - Evidence: 目安 example 「費用の目安」 ("rough guide to the cost"); Daijisen 「費用の目安を立てる」; words\予算.md:4,15.
  - Confidence: medium.
- **B84-F06**; Low; Correctness (quiz_exclusions); words\面倒くさい.md:4,9,19
  - Claim/impact: the article's own example translates 面倒くさい as "a nuisance", which overlaps 迷惑 ("nuisance; inconvenience", words\迷惑.md:4). Both words exclude 面倒, but guards don't carry over, so this pair needs its own.
  - Remedy: add 迷惑 to 面倒くさい's quiz_exclusions.
  - Confidence: medium-low.

## Optional
- Borderline guards to consider: めっきり/はっきり ("distinctly cooler"), 面積/地域 ("area"), めちゃくちゃ/散らかす ("make a mess"; matches the existing 汚い and ぐしゃぐしゃ guards).
- もしかすると example 2 reads more naturally as この道のほうが近道なんじゃないですか.
- In めでたい, translate 決まった as "settled" rather than "arranged", which can suggest an arranged marriage.
- Link 地下 in 潜る and 接近 in 面接; both articles exist.
- In 面倒くさい, note that めんどくさい is common in casual speech.
- Some exclusions are redundant but harmless: 木材→材木 (identical titles already dedupe), もしかしたら/もしかすると→偶然 and たまたま, もたれる→寝る and 頼む.

## Limits
- I couldn't run Git, and I didn't independently run the author's hash checks.
- I didn't read the older-body inspection files. Guard judgments rely on the 291 labels, targeted bodies and a keyword-limited title grep.
- The 寄る leaning sense was confirmed against current JMdict on jisho.org, not the pinned snapshot.
- Unverified in pinned evidence: that めまい's げんうん is a separate JMdict entry, and whether 〜を面接する is standard usage.
- This review doesn't certify native-speaker naturalness.
