## Snapshot
**329ee65a6b15e20d59cf3426b50dc51aafecd408**, committed content only. The parent is df77fa114378d784594fb5189cf8b65485a3b75e. My file tools cannot run Git, so the commit, the parent, the hashes and the clean-content claim are author-reported. I did not verify them.

## Scope
- **Model:** claude-opus-5.5 (claude family). No agents, no edits, no web fetches.
- **Guidance:** `.github\copilot-instructions.md`, the content-structure instructions, `docs\content-format.md:18-103`, and a grep of `docs\confusable-words.md` (entry CW088 covers 直す/治す).
- **TSV:** the header and rows N2:1222–1241, read directly.
- **Private files read in full:** frozen-snapshot, related.patch, review-mappings, review-principals, review-components, review-labels, public-bodies.txt.
- **Private files read in part:** review-evidence.json:1-80; family-inspection-01:1-60, -10:54-110 and -12:52-60. I found these ranges with grep on the exact permitted file paths, never on the directory.
- **Articles:**
  - All 17 new articles, in full.
  - `words\泊める.md` and `words\長い.md`, in full.
  - Kanji cards 採, 線, 永, 仲 and 泊, in full.
  - Comparison bodies: ずるずる, だらだら, 伸びる, 綿, 選ぶ.
  - Front matter of 身, 直す, 治る, 内容, 物質, 外科, 医学, 線, 捕まる, 捕まえる.
  - A title keyword grep across `words\`, and a glob of `kanji\` to check which cards exist.
- **Not read:** supplement-inspection-01..03, the sports and extra comparison files, public-bodies.json, the rest of the family chunks, `docs\n2-vocabulary-snapshot.json`, `docs\n2-source-snapshot.json` and `docs\jlpt-levels.md`.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility. C = CLEAN, NF = NEEDS FIX.

| Row | Article | Verdict |
|---|---|---|
| N2:1222 泊める | 泊める.md (reused; only `jlpt: 2` added) | C / C / C |
| N2:1223 ともかく | ともかく.md | C / C / C |
| N2:1224 捕える | 捕える.md | C / C / C |
| N2:1225 取り入れる | 取り入れる.md | C / C / C |
| N2:1226 取り消す | 取り消す.md | C / C / C |
| N2:1227 取り出す | 取り出す.md | C / C / C |
| N2:1228 採る | 採る.md | C / C / C |
| N2:1229 捕る | 捕る.md | C / C / C |
| N2:1230 トレーニング | トレーニング.md | C / C / C |
| N2:1231 丼 | 丼.md | C / C / C |
| N2:1232 内科 | 内科.md | C / C / C |
| N2:1233 内線 | 内線.md | C / C / C |
| N2:1234 ナイロン | ナイロン.md | **NF** (B62-02) / C / C |
| N2:1235 治す | 治す.md | C / C / C |
| N2:1236 永い | 長い.md | C / C / C |
| N2:1237 仲直り | 仲直り.md | C / C / C |
| N2:1238 長引く | 長引く.md | **NF** (B62-01) / C / C |
| N2:1239 中身 | 中身.md | C / C / C |
| N2:1240 中味 | 中身.md | C / C / C |
| N2:1241 中指 | 中指.md | C / C / C |

- **Kanji edits 採, 線, 永, 仲:** CLEAN. Each has a link in the reading row at the actual reading (と.る, セン, なが.い via 長い.md, なか), a Common words link and the matching footer ID. Headers are preserved.
- **Unchanged 泊 pair:** CLEAN. 泊 links 泊める (と.める, entry 1474860), and 泊める links back to 泊.
- **Component links:** All existing component cards are linked from the word side. The missing 捉, 兎, 穫, 丼 and 身 cards are not linked or invented.
- **Baseline preservation:** CLEAN. 泊める keeps its body; 長い keeps N5, its title and `[長]`.
- **Mappings:** CLEAN on all three facets. All 20 match the TSV and the principal records (entry numbers, senses, restrictions; 直す sense 4 is "usu. written as 治す").

## Findings
**B62-01 — `words\長引く.md` is missing two quiz exclusions**
- **Severity:** Minor. **Facet:** quiz_exclusions omission.
- **Location:** `words\長引く.md:9`.
- **Claim and impact:** The title "drag on; be prolonged" overlaps ずるずる "dragging on" and だらだら "dragging on". A learner could reasonably accept either as the answer. Neither side declares the pair, yet weaker 引っ張る is excluded.
- **Remedy:** Add `ずるずる, だらだら` to 長引く's quiz_exclusions.
- **Evidence:** ずるずる.md:4 and :21 (話し合いがずるずる続いた). だらだら.md:4 and :20 (会議がだらだら続いた). `docs\content-format.md` gives the "reasonably accept either title" rule.
- **Confidence:** Medium-high.

**B62-02 — `words\ナイロン.md` gives the wrong reading for 綿**
- **Severity:** Minor. **Facet:** reading correctness.
- **Location:** `words\ナイロン.md:28`.
- **Claim and impact:** The line says "[綿](綿.md) (わた) is cotton" in a comparison of materials. The linked article teaches cotton the material as **めん**, and わた as the separate plant/padding word. This contradicts the link target.
- **Remedy:** Change `(わた)` to `(めん)`.
- **Evidence:** 綿.md:3, 16, 20 and 37.
- **Confidence:** High.

## Optional
- **取り出す and 選ぶ/採る:** "pick out" overlaps with choosing. Daijisen's sense 2 for 取り出す is 「多くの中から選び出す」. Consider an exclusion; this is borderline.
- **長い.md:** Could add an example for 永い (such as 永い年月) that shows the ながい reading explicitly.
- **Overlap only through the English word:** 中身 and 物質 share "substance"; 内科 and 薬/医学 share "medicine". Neither is an established pair.
- **採る excludes 入れる:** This is weak but defensible through sense 6 (letting in light).

## Limits
- I could not run Git.
- All 20 public captures come from one source (Daijisen via Weblio), and I did no fresh retrieval.
- I read only parts of the family and supplement evidence, so my reads do not cover the full 246-family union the author inspected.
- The quiz-overlap scan was a title grep plus selected article bodies, so it is not exhaustive.
- Example naturalness is my own judgment, not a native speaker's.
- I did not read either snapshot JSON in `docs\` or `docs\jlpt-levels.md`.
