## Snapshot
- **Corrected commit:** `2a0eaee7685c42e869db924831dbb4bb71050e20`, whose parent is `033d125b6c4aa4438587e603296d582f2750195d`.
- **What I compared:** the repository files against the correction patch. The nine article diffs and the packet's added section match what is on disk.
- **Provenance limit:** I did not check that the files on disk equal the commit, the parent link, or any hash. The receipt's hashes, including batch-13.json sha256 `92ddd722…`, are the author's assertions.

## Scope
- **Nine articles read in full:** 回転, 外部, 開放, 概論, 返る, 家屋, 垣根, 関わる, 帰す.
- **Comparison cards read:**
  - ぐるぐる "round and round; winding around"
  - 表面 "surface; outward appearance"
  - 表 "front; outward-facing side"
  - 口 "mouth"
  - 大体 "generally; approximately"
  - 戻す "put back; restore"
  - 宅 "home; residence"
  - 壁 "wall"
  - the 参加 link target, "participation" (it exists and teaches 参加する)
  - 送る frontmatter only, "send; escort", to settle my 送る lead
- **Packet (batch-13.json:14912-16809):**
  - all 16 added families (lines 14916-16675)
  - correctionEvidence (16676-16807)
  - 1535850 戻す (11148) and 1512150 返る (10631) from the original evidence
  - the original copy of 1450320 (9614)
- **Fetched myself:** the Weblio 返る page cited in the article.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 回転 | CLEAN | CLEAN | CLEAN |
| 外部 | CLEAN | CLEAN | CLEAN |
| 開放 | CLEAN | CLEAN | CLEAN |
| 概論 | CLEAN | CLEAN | CLEAN |
| 返る | CLEAN | CLEAN | CLEAN |
| 家屋 | CLEAN | CLEAN | CLEAN |
| 垣根 | CLEAN | CLEAN | CLEAN |
| 関わる | CLEAN | CLEAN | CLEAN |
| 帰す | CLEAN | CLEAN | CLEAN |
| Packet additions | CLEAN | CLEAN | CLEAN |

**Why the nine new quiz exclusions are justified.** In each pair, one card's English title could pass as a correct answer for the other card:
- **回転 / ぐるぐる:** "round and round" overlaps physical "rotation" (JMdict 1004140, sense 1). 回転 already excludes くるくる, so this is consistent.
- **外部 / 表面:** 表面's article says outright that 表面 is "a surface or exterior" (1489880, sense 2 "outside; exterior", at ひょうめん).
- **外部 / 表:** the 表 card teaches "the outside" of a building (1489340, sense 4, at おもて).
- **開放 / 口:** the 口 card teaches 口 as "an opening" (1275640, senses 2 and 11).
- **概論 / 大体:** 大体 also means "outline; main points" (1414470, sense 3), and its card teaches 大体の意味 "the general meaning".
- **返る / 戻す:** 戻す sense 1 is glossed "to return" (1535850). The articles still keep transitive and intransitive verbs distinct.
- **家屋 / 宅 and 住宅:** 宅 is "house; home" (1415750, sense 1) and 住宅 is "residential building" (1334150).
- **垣根 / 壁:** the 壁 card teaches the figurative barrier 言葉の壁 (1509290, sense 2, at かべ).

**返る's new example.** JMdict 1512150 sense 2, "turn over", has no spelling restriction, so writing 返る there is valid. The Weblio page I fetched gives reading かえる. Its sense 1 lists 「裾が―・る」 and is not marked 返る-only, while senses 2-4 are. That supports the Usage line, and the sentence is honestly described as an original illustration.

## Findings
**Reconciling my original findings:**
- **B13-01 (帰す.md:21, citation at :37): resolved.** The article now names 帰す (きす), "end in / attribute to", which matches 2410530 senses 1-2. I accept the receipt's point that the old sentence was limited to one reading, so calling it a "blanket denial" overstated it. The clarification is still useful.
- **B13-02 (返る.md:25-27, 47): resolved.** The garment-hem example covers the turn-over sense, and the construction has a citation.
- **B13-03 (家屋.md:9): resolved.** 住宅 is excluded, and 宅 is also added. Exclusions work both ways, so 住宅's own list needs no change.
- **B13-04 (関わる.md:19, 33): resolved.** "Life-or-death matter" is the right translation. "Someone's survival is at stake" fits 命に関わる.
- **B13-05 (関わる.md:29): resolved.** The link `[参加](参加.md)する` points to an existing card.

**Reconciling my optional leads:**
- **Guest example (帰す:19): withdrawn.** 客を帰す is grammatical, and switching to 客が帰る would change the construction being taught.
- **帰す / 送る: withdrawn as a defect.** "Send; escort" and "send home; send back" can be told apart, and 1402730 has no "send back" or "send home" sense.
- **逃がす for the 解放 cage example: withdrawn.** Having another verb available does not make 解放 wrong.
- **開放 "opening up" (now line 31): resolved.** That wording was removed.
- **"stagk": withdrawn.** It is JMdict's real `stagk` element, not a typo.
- **Adding 垣根 to 根.md's -ね row: still optional.**

**New regressions:** none found.

## Optional
- **返る.md:23-25:** say that the turn-over sense can be written either 返る or 反る. The line telling learners to recognize 反る is followed by an example written with 返る, which may briefly puzzle them.
- **帰す (きす):** could note that it is a literary relative of 帰する (2410530 cross-references 帰する).
- **Packet:** 1221240 and 1450320 each appear twice. The copies are identical, so this is only redundant.
- **根.md:** the -ね row example noted above.

## Limits
- **No Git:** I could not check the commit, parent, tree or hashes, so all identity claims rest on the receipt.
- **JMdict:** I relied on the packet's extracts, not the pinned XML.
- **Weblio:** my fetch confirms the construction but not how often it is used. The exact sentence is not corpus-checked or verified by a native speaker.
- **Quiz overlaps:** these are judgments from reading the cards. I didn't run the app or measure how candidates are drawn.
- **Scope:** I did not re-review the rest of batch 13 or the corpus as a whole.
