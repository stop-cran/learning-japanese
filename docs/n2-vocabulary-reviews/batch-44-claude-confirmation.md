All four of my original findings are fixed on the corrected snapshot, and the extra exclusions added on 澄む, スライド and ずらす don't introduce any problems. Nothing actionable remains in scope.

## Snapshot
1ae25de5c02566e0926ecd865142175430c25de8 (parent 519d183f9494ce149cab8317d46d7e3a7c6e41bf, my original snapshot). I reviewed committed content only. I have file tools, not Git, so I read the working-tree files and could not confirm they match this commit. The receipt's hash and equivalence checks were run by the author, not by me.

## Scope
- **Model and session:** claude-opus-5.5 (Claude family), resuming my own initial review session.
- **Read in full for this check:**
  - The correction receipt, the correction patch and the 15-family comparison rendering.
  - The author's capture of the existing comparison articles.
  - All six changed cards: すまない, 澄む, スライド, ずらす, 性質 and 刷る.
- **Grepped and confirmed:**
  - Titles and exclusion lists for どうも, 感謝, 御礼, 礼, 落ち着く, 安心, 変える, 天然 and 活字.
  - Links on kanji\刷.md, 税.md and 清.md.
  - words\姓.md front matter and the six old-word backlinks.
  - docs\n2-vocabulary-sources.tsv rows N2:862–881.
- **Inherited without re-reading:** my original judgments on the 13 unchanged articles.
- **Not read:** batch-44-corrected-review-evidence.json.

## Verdicts
Rows marked R were reassessed against the correction; rows marked I keep my unchanged original judgment.

| Row | Article | Status | Basis | Correctness | Coverage | Comprehensibility |
|---|---|---|---|---|---|---|
| N2:862 | 住まい | new | I | CLEAN | CLEAN | CLEAN |
| N2:863 | すまない | new | R | CLEAN | CLEAN | CLEAN |
| N2:864 | 墨 | new | I | CLEAN | CLEAN | CLEAN |
| N2:865 | 澄む | new | R | CLEAN | CLEAN | CLEAN |
| N2:866 | 澄む (清む alias) | new, shared | R | CLEAN | CLEAN | CLEAN |
| N2:867 | 相撲 | new | I | CLEAN | CLEAN | CLEAN |
| N2:868 | スライド | new | R | CLEAN | CLEAN | CLEAN |
| N2:869 | ずらす | new | R | CLEAN | CLEAN | CLEAN |
| N2:870 | ずらり | new | I | CLEAN | CLEAN | CLEAN |
| N2:871 | 刷る | new | R | CLEAN | CLEAN | CLEAN |
| N2:872 | ずるい | new | I | CLEAN | CLEAN | CLEAN |
| N2:873 | すれ違う | new | I | CLEAN | CLEAN | CLEAN |
| N2:874 | ずれる | new | I | CLEAN | CLEAN | CLEAN |
| N2:875 | 寸法 | new | I | CLEAN | CLEAN | CLEAN |
| N2:876 | 姓 | reuse | I | CLEAN | CLEAN | CLEAN |
| N2:877 | 税関 | new | I | CLEAN | CLEAN | CLEAN |
| N2:878 | 製作 | new | I | CLEAN | CLEAN | CLEAN |
| N2:879 | 制作 | new | I | CLEAN | CLEAN | CLEAN |
| N2:880 | 性質 | new | R | CLEAN | CLEAN | CLEAN |
| N2:881 | 清書 | new | I | CLEAN | CLEAN | CLEAN |

- **Three kanji edits (unchanged):** CLEAN on all three facets.
  - 刷.md:31 and :39 link 刷る under す.る and in Common words.
  - 税.md:30 and :37 link 税関 under ゼイ.
  - 清.md:30 and :41 link 清書 under セイ.
  - 清.md:42 and :49 link 清む to 澄む and state that KANJIDIC2 has no す.む reading.
- **Bounded reuse (姓, unchanged):** CLEAN. It has `jlpt: 2`, and its title, reading and exclusions [名, 名前] are unchanged.
- **Six old-word backlinks (unchanged):** CLEAN. All six links are still present: インク:30, インキ:34, 透き通る:29, 性格:30, 性:28 and 下書き:37.
- **All twenty mappings:** CLEAN. The source rows are unchanged from my original capture.

## Findings
- **F1 (性質 sentence that read as "性質 is things-only"; Minor) — Resolved.** 性質.md:35-36 now says 性格 is not limited to people and 性質 is not limited to things. This matches sense 1, the first example and the Daijisen usage note, and it keeps the qualified overlap rather than splitting people from things.
- **F2 (性質 should exclude 天然; Minor) — Resolved.** 性質.md:9 adds 天然. Both titles carry the English label "nature" (JMdict 1439580:1 also glosses 天然 as "nature").
- **F3 (すまない gratitude exclusions; Minor) — Resolved.** すまない.md:9 adds どうも, 感謝, 御礼 and 礼.
  - Their titles are "thanks; very much", "gratitude; appreciation", "thanks; gratitude" and "thanks; bow".
  - JMdict 1610020:3 includes "thank you". This matches the precedent in 恐縮.md:9.
- **F4 (刷る's bare "print" title overlaps 活字; Minor, low-medium confidence) — Resolved** by the exclusion rather than a retitle.
  - 活字's sense 2 (JMdict 1208300) includes "print", and its example translates 小さい活字 as "small print".
  - The verb-versus-type distinction is unchanged.
- **Other changes the author added, checked for regressions:**
  - 澄む now excludes 落ち着く ("calm down; settle") and 安心 ("peace of mind; relief"). This is supported by sense 3, "become serene… free of worries", which the card teaches. The Buddhist reading あんじん was not relied on. This covers row 866 too, because 清む shares the 澄む card.
  - スライド and ずらす now exclude 変える ("change something"). This is supported by 変える's sense 1, by its meeting-time example, and by スライド's sense 5 ("change with a sliding scale").
  - All additions point to existing articles, and none is excessive or harms the choice pool.
- **New regressions:** none.

## Optional
- 住まい.md:30-31: reword to "do not read 住まい as じゅうきょ."
- 寸法: mention the colloquial "〜という寸法だ" pattern.
- 税関: you could contrast it with the reversed compound 関税 ("tariff").
- 性質.md:34-36 now says twice that 性格 applies to things; you could trim one of the two.

## Limits
- Based on file reads only; I could not run Git or hash checks.
- The comparison and existing-article captures were made by the author. I confirmed the titles and exclusion lists myself, but not the full bodies.
- The thirteen unchanged articles keep my original judgments and were not re-read.
- I made no web fetches, and nothing here is certified by a native speaker.
