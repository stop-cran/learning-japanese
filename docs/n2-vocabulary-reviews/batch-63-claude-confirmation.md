## Snapshot
- **Corrected commit:** `0daa3c922e51440b61c38aef03f257affe843f19`
- **Parent:** `0cc62d83b0e932b0d0c45e332f9f070a37d2b19c`

These come from `batch-63-correction-snapshot.json`. The review covers committed content only. My file tools can't run Git, hash or working-tree cleanliness checks, and I did not inspect `.git`. Whether the files on disk match the commit, and the hash, manifest and baseline-preservation checks, are author-executed and I have not reproduced them.

## Scope
**Model:** claude-opus-5.5 (Claude family). Read-only: no edits, agents or delegation.

**Read completely in this confirmation phase:**
- `correction-snapshot.json`, the full `correction.patch` and `correction-public.json`.
- Both `correction-families` chunks: 12 complete families, 56 senses (1009410, 1188330, 1189310, 1408810, 1597890, 1599580, 1587850, 1532880, 1607520, 2861111, 1378790, 1212670).
- The full `correction-old-bodies-01.txt`: six complete bodies (なぜなら, 打つ, 作る, 慣れる, いろいろ, 演奏).
- All five changed bodies: `words\為す.md`, `words\生意気.md`, `words\馴れる.md`, `words\なにしろ.md`, `words\何分.md`.
- The TSV header (line 1) and exactly rows N2:1242–1261 (lines 1242–1261).

**Partly read:**
- `corrected-review-evidence.json`: one targeted search only, which incidentally showed the author's disposition text for N2-63-02/03.
- Title and exclusion lines of comparison articles in `words\`: だって, だから, なぜ, なさる, 致す, する, やる, 行う, 何々, 鳴らす, いろいろ, 演奏.

**Inherited from my initial full reads, not reread:**
- The 15 unchanged word bodies.
- The kanji cards 仲, 並 and 極.
- The related patch.
- The four compact derivatives, which are no longer on the allowlist.

**Omissions:**
- No full read of the large corrected derivative.
- No fresh live fetch.
- Older bodies read in full across both phases: only 打つ, 作る and 慣れる (initial) plus these six (三 of which overlap), not the 151-body union.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1242 | words\仲良し.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1243 | words\慰める.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1244 | words\亡くす.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1245 | words\なぐる.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1246 | words\為す.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1247 | words\謎謎.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1248 | words\なだらか.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1249 | words\懐かしい.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1250 | words\撫でる.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1251 | words\斜め.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1252 | words\なにしろ.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1253 | words\何々.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1254 | words\何分.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1255 | words\生意気.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1256 | words\並木.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1257 | words\倣う.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1258 | words\鳴らす.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1259 | words\生る.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1260 | words\馴れる.md | Full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1261 | words\南極.md | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |

**Reciprocal pairs (inherited, CLEAN).** All three are checked at the actual whole-word readings, with a reading-row example, a Common words link and a footer entry ID:

| Pair | Reading-row example | Common words | Footer ID |
|---|---|---|---|
| 仲 / 仲良し (なかよし) | 仲.md:31 | 仲.md:38 | 1426100 (仲.md:46) |
| 並 / 並木 (なみき) | 並.md:31 | 並.md:43 | 1599640 (並.md:50) |
| 極 / 南極 (なんきょく) | 極.md:28 | 極.md:44 | 1460180 (極.md:55) |

The word-side links are substantive and the kanji headers are preserved. The correction patch touches no kanji files.

**Kanji and baseline preservation:**
- CLEAN on content, inherited.
- Existing component cards are linked; missing cards (為, 慰, 懐, 撫, 斜, 倣, 馴, 謎, 殴) are not invented. Primary metadata is not expanded for body variants.
- N4 慣れる is unchanged. Its body, reread here in the old-body chunk, still cites only 1212670 sense 1.
- The patch changes no titles, readings, levels, identities, kanji bodies, baseline exclusions or original guards. Hash-level confirmation is author-executed.

**Mappings: 20/20 CLEAN.**
- The TSV rows I reread match the initial judgments.
- Selected senses: なだらか 1,2; なにしろ 1,2; 何々 1-3; 何分 2,3; 馴れる 3; 南極 1,2; all others sense 1.
- Additional senses: 1498290:2, 1322400:2, 1599580:4,5, 1189310:1, 1532880:2,3.

## Findings
**B63-C-01 / N2-63-01 (shared) — RESOLVED.**
- 為す.md:24-26 now separates the modern potential なせる ("can do") from the fixed phrase Xのなせる業, described as an older resultative construction. Line 49 adds the Kotobank link.
- This fits classical grammar: なす 已然形 + perfect/continuative り 連体形. It also fits the 天のなせるわざ / 大自然のなせるわざ examples I saw in my initial Weblio fetch.
- No regression: examples, conjugations, title and exclusions are unchanged.
- Confidence: high.

**B63-C-02 — RESOLVED.**
- 生意気.md:29-30 now reads native なま plus on readings イ/キ, which is accurate.
- `type: wago` at line 6 is kept, following the existing kun-first mixed-word convention (content-format.md:63).
- No regression.

**B63-C-03 — RESOLVED.**
- 馴れる.md:36-37 now attributes only the "getting used to" sense to the existing article. That matches 慣れる.md, which says "not necessarily… becoming highly skilled" and cites 1212670 sense 1 only.
- Lines 38-39 describe the dictionary's spelling preferences, not the older article, and match 1212670: senses 1-2 esp. 慣れる, sense 3 esp. 馴れる.
- No regression.

**B63-C-04 — WITHDRAWN as actionable; now a non-blocking difference in guard preference.**
- 打つ: 1408810:11 ("to do; to carry out; to play; to perform; to engage in") is unmarked and matches 為す's title, "do; carry out" (為す.md:4), nearly word for word. With a context-free title prompt, keeping 打つ out as a distractor is defensible. I concede this one.
- 作る: the overlap is only 1597890:14 "commit (a sin)" against 2861111 "commit". That is in neither actual title (作る "make; prepare"), so the guard is weaker. At most it is harmless extra caution, not a defect.
- Confidence that neither is actionable: medium-high.

**N2-63-02 (なにしろ / なぜなら guard, なにしろ.md:9) — SUPPORTED. My initial review missed this.**
- 1188330:2 includes "because; since; for; after all".
- なぜなら's actual title is "the reason is; because".
- なにしろ already guarded だって ("because; but; even; too"), and だって.md:9 itself guards なぜなら. Leaving なぜなら out was therefore an inconsistency.
- No regression. Confidence: high.

**N2-63-03 (何分 / なぜなら guard, 何分.md:9) — SUPPORTED as a direct, conservative guard.**
- 1189310:3 has "after all".
- The body (何分.md:16-24) teaches introducing a circumstance offered as a reason.
- 何分 already guarded だって.
- I am not inferring this pair through なにしろ.
- Confidence: medium. The competition rests on English labels: "after all" versus "because".

**Regressions:** none found in the five changed bodies or the patch.

**New actionable defects:** none.

## Optional
- **何々 / いろいろ** (何々.md:9): keep the guard, with weaker confidence. 1587850:3 "various things; this and that" partly overlaps the unspecified-listing sense 1599580:2, but variety is not the same as a placeholder.
- **鳴らす / 演奏** (鳴らす.md:9): a thin but conservative guard. 演奏 is limited to musical performance, while 鳴らす covers sounding in general. Shared topic alone wouldn't justify it; leaving it is harmless.
- **何々 example punctuation:** the clearly labelled placeholder demonstration is acceptable; this is polish only.
- **為す versus なさる ("do (honorific)") and 致す ("do humbly"):** neither is guarded. That is consistent with the baseline, where する has no exclusions against them, and the register qualifiers in their titles tell the answers apart. Not a defect; low confidence.
- **作る calibration:** the remaining mild disagreement under B63-C-04 is kept as a preference, not a finding.

## Limits
- **Kotobank analysis:** the なす + り analysis on Kotobank and the Seisenban Nihon Kokugo Daijiten agreement come from the author's paraphrased receipt, not my own retrieval. My support is that receipt, standard classical grammar and my initial Weblio examples.
- **Single source:** all 20 public captures are Digital Daijisen via Weblio, one source. Kotobank overlaps Daijisen and adds only Seisenban.
- **何分 raw gloss:** the TSV gloss "what minute? / how many minutes?" contradicts the row's kanji, reading and entry (1189310). I followed the entry; I can't establish what the list compiler intended.
- **Older-body depth:** I read only a few older bodies in full; other exclusion judgments rely on titles and exclusion lines. This is not an exhaustive audit for missing guards.
- **Not claimed:** Git, hash, manifest or index checks; live quiz draws; measured frequency; native-speaker certification.
- **Deferred:** the batch-61 飛ぶ/飛行 and 止まる/止む debt.
