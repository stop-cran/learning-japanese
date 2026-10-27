20, all final-precard files and public-bodies.json.
- Any complete older `words\` body. Both attempts were interrupted.
- Any `kanji\` file other than the 10 renderings. I did not run a kanji glob.
- `docs\confusable-words.md`, `jlpt-levels.md`, `n2-vocabulary-snapshot.json` and `n2-source-snapshot.json`.
- Any web page.

I did not access the forbidden TSV, batch-87.json, ledgers, notes or other reviewer reports.

**Evidence gaps:**
- I checked comparisons selectively and did not finish. I read all 190 comparison titles and exclusion lists, but no complete comparison body.
- My working notes did not keep the full quiz_exclusions lists for several assigned articles when I read labels 97–190. Those cross-checks are unresolved; see Limits.
- My notes did not keep exact body line numbers for B87-02 and B87-03.

**Public headings that apply.** The capture comes from one dictionary, not from 20 independent sources.

| Word | Heading that applies | Heading(s) set aside |
|---|---|---|
| 夕立 | ゆうだち | — |
| 夕日 | ゆうひ (also written 夕陽) | Secondary reading せきじつ |
| 悠々 | ゆうゆう【悠悠】 | — |
| 有料 | ゆうりょう | — |
| 浴衣 | ゆかた | The よくい heading, a second reading that the article also teaches |
| 湯気 | ゆげ | The separate ゆけ heading |
| 輸血 | ゆけつ | — |
| 輸送 | ゆそう | — |
| 油断 | ゆだん | — |
| ゆでる | ゆでる【茹でる】 | — |
| 湯飲み | ゆのみ | — |
| 緩い | ゆるい | The ぬるい【温い】 heading |
| 溶岩 | ようがん | — |
| 容器 | ようき | — |
| 用語 | ようご | — |
| 要旨 | ようし | — |
| 幼児 | ようじ | The おさなご heading |
| 容積 | ようせき | — |
| 幼稚 | ようち | — |
| 幼稚園 | ようちえん | The trailing image caption |

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1722 夕立 | words\夕立.md | CLEAN | CLEAN | CLEAN | The only JMdict sense matches public sense 1. Public sense 2 is archaic (wind or clouds rising in the evening), which justifies the article's "modern rain sense" wording. The 夕立ち spelling is covered. The broader-term pair 夕立/雨 was not cross-checked (see Limits). |
| N2:1723 夕日 | words\夕日.md | CLEAN | CLEAN | CLEAN | The 夕陽 spelling is covered, and せきじつ is correctly limited to the 夕日 spelling. Guards against 日の入り, 日光, 日差し and 太陽 are adequate. |
| N2:1724 悠々 | words\悠々.md | CLEAN | CLEAN | CLEAN | Teaches senses 1–2 and presents sense 3 (distant, eternal) for recognition only, which suits practical use. The full guard list was returned (line 9). |
| N2:1725 有料 | words\有料.md | CLEAN | CLEAN | CLEAN | The opposite word 無料 is covered. The extra "toll road" sense is distinguished. The warning against 有料なサービス is correct. No guard is needed. |
| N2:1726 浴衣 | words\浴衣.md | UNVERIFIED | CLEAN | CLEAN | Both readings, ゆかた and よくい, are taught, and 寝間着 is guarded. Whether 浴衣 and 着物 ("kimono") need a guard is unresolved. |
| N2:1727 湯気 | words\湯気.md | UNVERIFIED | CLEAN | CLEAN | ゆげ is the only JMdict reading. Filing it as wago with a "native-first mixed" label is acceptable. Guards against 蒸気 and 水蒸気 are unresolved. |
| N2:1728 輸血 | words\輸血.md | CLEAN | CLEAN | CLEAN | It is a noun usable with する, both transitive and intransitive, matching the public entry. No guard is needed against 血, 血液 or 注射. |
| N2:1729 輸送 | words\輸送.md | NEEDS FIX | CLEAN | CLEAN | See B87-01. The transitive する use matches the public entry. |
| N2:1730 油断 | words\油断.md | UNVERIFIED | CLEAN | CLEAN | Part of speech matches. The public origin note is itself hedged, and my reading found no overstated etymology. A guard against 過失 ("negligence") is unresolved. |
| N2:1731 ゆでる | words\ゆでる.md | CLEAN | CLEAN | NEEDS FIX | See B87-02. 茹でる, 煠でる, the うでる reading and sense 2 are covered. Guards against 煮る, 煮える, 沸かす and 沸く are needed and present. |
| N2:1732 湯飲み | words\湯飲み.md | CLEAN | CLEAN | CLEAN | All five spellings are covered, along with its status as a shortening of 湯呑み茶碗. The cited entry ID 2810060 was not checked (see Limits). |
| N2:1733 緩い | words\緩い.md | CLEAN | NEEDS FIX | CLEAN | See B87-03. The guards against "slow" words, なだらか, 甘い and 柔らかい are sound. |
| N2:1734 溶岩 | words\溶岩.md | CLEAN | CLEAN | CLEAN | 熔岩 is marked as a rare spelling. Both meanings are taught: molten lava and the rock it hardens into. Guarding 岩 is justified. |
| N2:1735 容器 | words\容器.md | CLEAN | CLEAN | CLEAN | 包装 is guarded. The 入れ物 guard is redundant because identical titles are deduplicated, but it is harmless. |
| N2:1736 用語 | words\用語.md | UNVERIFIED | CLEAN | CLEAN | Both senses are taught. The guard against 言葉遣い ("wording") is unresolved. |
| N2:1737 要旨 | words\要旨.md | UNVERIFIED | CLEAN | CLEAN | The guard against 要点 ("main point; gist") is unresolved. |
| N2:1738 幼児 | words\幼児.md | UNVERIFIED | CLEAN | CLEAN | Both the general sense and the legal "one year old up to school age" sense are taught. 子, 子供, 児童 and あかちゃん are guarded. The guard against 赤ん坊 ("baby; infant") is unresolved. |
| N2:1739 容積 | words\容積.md | CLEAN | CLEAN | CLEAN | Both "capacity" and "volume" are taught. 定員 and 体積 are guarded. 能力 ("ability; capability") needs no guard. |
| N2:1740 幼稚 | words\幼稚.md | CLEAN | CLEAN | CLEAN | Both the noun and na-adjective senses are taught, and 幼い is guarded. |
| N2:1741 幼稚園 | words\幼稚園.md | CLEAN | CLEAN | CLEAN | The age-3, non-compulsory detail matches the public entry. |

**Related kanji edits and earlier content preserved:** CLEAN for all ten characters (浴, 衣, 湯, 輸, 血, 油, 溶, 岩, 幼 and 児) on correctness, scoped coverage and comprehensibility.
- The patch only adds content:
  - links on existing plain-text mentions (幼児 in 幼, 溶岩 in 溶, 輸送 in 輸, 輸血 in 血);
  - new Common-words lines;
  - JMdict IDs added to Metadata lines.
- Front matter and earlier teaching are unchanged.

**Components:**
- The readings in all 36 component records agree with the articles, for example the ケ reading of 気, the ゆう reading of 夕, and チ for 稚.
- Whether every primary Han character's existing kanji card is linked is UNVERIFIED. This applies to characters such as 器, 稚, 悠, 緩 and 旨, because I never listed the `kanji\` folder.

**Reciprocity:** CLEAN. All 14 required pairs are present in both directions.

**Mappings:** CLEAN on correctness, scoped coverage and comprehensibility for all 20 rows (N2:1722–1741). Each points to the right article and JMdict entry.

| Word | JMdict entry | Selected senses |
|---|---|---|
| 夕立 | 1542820 | 1 |
| 夕日 | 1542750 | 1 |
| 悠々 | 1605700 | 1–2, plus sense 3 for recognition |
| 有料 | 1541690 | 1, plus sense 2 for recognition |
| 浴衣 | 1584990 | 1 |
| 湯気 | 1448600 | 1 |
| 輸血 | 1538810 | 1 |
| 輸送 | 1538850 | 1 |
| 油断 | 1538690 | 1 |
| ゆでる | 1571470 | 1 |
| 湯飲み | 1612130 | 1 |
| 緩い | 1214410 | 1–5 |
| 溶岩 | 1546120 | 1 |
| 容器 | 1545370 | 1 |
| 用語 | 1546270 | 1–2 |
| 要旨 | 1546770 | 1 |
| 幼児 | 1545160 | 1–2 |
| 容積 | 1545420 | 1 |
| 幼稚 | 1545250 | 1–2 |
| 幼稚園 | 1545260 | 1 |

The 緩い mismatch is in the article, not the mapping (B87-03).

## Findings
**B87-01: missing quiz guard between 輸送 and 交通機関**
- **Severity:** Minor. **Facet:** correctness (quiz guard).
- **Files:** `words\輸送.md:4,9` and `words\交通機関.md:4,9`.
- **Problem:**
  - The titles are "transport; transportation" (輸送) and "means of transport; transport system" (交通機関). Neither word excludes the other.
  - In everyday English, "transportation" often means the transport system itself ("public transportation" is 公共交通機関). A learner could reasonably accept either title for either word.
  - 輸送 already guards 交通 ("traffic; transportation"), 航空 ("air transport") and 鉄道 ("rail transport") because their titles overlap on "transport". It is inconsistent not to guard 交通機関.
  - In my full card reading, the 輸送 body contrasts itself with 交通機関 but sets it aside on grammatical-role grounds. The rubric does not allow a blanket part-of-speech exemption. I did not keep the exact line.
- **Fix:** add 交通機関 to 輸送's quiz_exclusions. One side is enough because guards apply both ways.
  - **Possible extra fix (low confidence):** 便 ("transport service; mail", `words\便.md:4`; it only excludes 便り, line 9) overlaps on "transport" in the same way. Consider adding it too.
- **Evidence:**
  - The grep returned the titles and exclusion lines.
  - I could not read the 交通機関 body because the call was interrupted.
- **Confidence:** medium for 交通機関; low for 便.

**B87-02: 十分 in a ゆでる example is misleading**
- **Severity:** Minor. **Facet:** comprehensibility and natural example wording.
- **File:** `words\ゆでる.md`, example block. I did not keep the exact line.
- **Problem:**
  - The example 卵を十分ゆでました uses the kana reading じゅっぷん ("ten minutes").
  - Written as 十分 directly before a verb, a native reader would read じゅうぶん ("thoroughly").
  - The kanji line and its intended reading therefore point in different directions.
- **Fix:** write 卵を10分ゆでました, or use 十分間.
- **Evidence:** my complete reading of the review-cards renderings.
- **Confidence:** medium.

**B87-03: the selected "slow / weak" sense of 緩い is under-taught**
- **Severity:** Minor. **Facet:** scoped coverage.
- **File:** `words\緩い.md`, meaning section. I did not keep the exact line.
- **Problem:**
  - The mapping selects JMdict senses 1–5, which include sense 4, "slow; weak". Waller's gloss is "loose, lenient, slow".
  - Public sense 3 gives the example 流れが緩い ("the current is slow").
  - The article mentions this sense only in a one-line "dictionary also records" note with no example. That treats a selected sense as recognition-only.
  - The guards already assume this sense: 遅い, のろい, ゆっくり and のろのろ.
- **Fix:** add one short taught line with an example, such as 川の流れが緩い.
- **Evidence:** principal record 1214410, mapping row 12 and public lines 165–170.
- **Confidence:** medium.

## Optional
- **湯気:** The "not an unrelated heading read ゆけ" note is accurate; the public ゆけ entry means a mild faint caused by bathing. It is dictionary-meta wording, though, and could be moved to Sources.
- **幼児:** Simplify the double-negative note about "infant" and "baby". For example: "toddler to preschool age; for babies under one, 乳児 is used." There is no 乳児 article, so leave it unlinked.
- **ゆでる:** The guards against 作る and こしらえる (and arguably 料理 and 炊事) look inherited from the cooking group around 煮る and 炊く, not from title overlap. Consider removing them. Low confidence.
- **悠々:** The 広い guard has weak grounds, and I did not check 佚's title.
- **緩い:**
  - The shared word "gentle" with 優しい and 穏やか is a possible overlap. なだらか guards both of them. Low confidence.
  - Optional notes could cover modern 緩い雰囲気 ("laid-back atmosphere") and the 緩い spelling of ぬるい.

## Limits
- **Git:** I could not run Git. The commit, its cleanliness and its hashes are as the author recorded them.
- **Execution:** the two concurrency violations are described under Scope. I read no complete older comparison body.
- **Unresolved guard pairs** (exclusion lists not retained):
  - 湯気 with 蒸気 or 水蒸気;
  - 要旨 with 要点;
  - 浴衣 with 着物;
  - 幼児 with 赤ん坊;
  - 油断 with 過失;
  - 用語 with 言葉遣い, 語 or 言葉.
- **Broader-term pairs treated as no guard needed, but not cross-checked:** 夕立 with 雨, and 容器 with 瓶, 箱 or 袋.
- **Kanji links:** whether kanji cards exist for unlinked Han characters is unverified.
- **湯飲み:** the 2810060 entry and its ぢゃ reading were not checked against a pinned record.
- **Evidence sources:** I fetched no outside pages, and the public capture comes from a single dictionary.
- **What CLEAN means:** no actionable defect was found in the scope I actually read. It is not a native-speaker certification.
