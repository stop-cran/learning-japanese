I've finished the confirmation review. Three of my five initial findings (B56-Q1, Q3, Q5) are fixed in the correction. I accept the author's reasons for declining the other two and withdraw them. I found no regressions and no new defects.

# Batch-56 corrected-snapshot confirmation review

## Snapshot
- **Corrected commit:** `bee40f02c2313d736a8c8f1f726b417056466260`.
- **Parent:** `3e67155e0a83c666b61719eca7eb3377fd649ce9`.
- I reviewed committed content only. File tools can't run Git, hashes or cleanliness checks, so those are author-run, and I did not inspect `.git`.

## Scope
**Model:** claude-opus-5.5 (claude family), read-only, no agents or delegation.

**Read completely this turn:**
- `correction-snapshot.json` (first).
- `correction.patch`.
- `reconciliation-comparison-reading.txt`: I counted 21 families and 58 senses.
- `correction-existing-reading.txt`: 14 old bodies (苦心, ぺちゃんこ, 生産, 役, 役割, 務め, 勤め, 勤める, 関係, 接続, 通信, 渋滞, 魅力, 繋ぐ).
- `correction-public-reading.txt`: the あで, えん and つや headings.
- The six changed articles: 作る, 努める, 潰す, 潰れる, 詰まる, 艶.
- The five unchanged articles: 繋がり, 繋がる, 繋げる, 務める, 伝わる.
- TSV rows N2:1102–1121.

**Targeted checks this turn:**
- `kanji\詰.md` and `kanji\造.md`: frontmatter plus lines 31/33/39/41/47.
- The five new guard targets and the 勉/力 kanji cards exist.
- Guard lists on the changed and target cards.
- `quiz_distractors` conflicts.
- Titles and guards on deverbal noun/verb pairs, used as precedent.

**Inherited from my initial review, not reread:** 付ける (×2), 漬ける, 突っ込む, 綱, 粒, つまずく, 積む, 爪, and the 造/詰 kanji teaching. These rest on my initial complete article reads plus the principals/mappings/components JSONL and the captured public text. My initial guard judgments for them used titles and guard searches, with one complete extra old body (ぺちゃんこ) and no family-inspection renderings.

**Not read:** `corrected-review-evidence.json` (not required this turn) and the forbidden ledgers. `principal-reading.txt` was absent in the initial turn; that was a prompt limitation, not a lost read. The author's counts (144 families/565 senses, 106 old bodies) are not my reads.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1102 | 作る (reused; raw 造る) | Changed; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1103 | 付ける (reused; raw 着ける) | Unchanged; inherited complete initial read | CLEAN | CLEAN | CLEAN |
| N2:1104 | 付ける (reused; raw 点ける) | Unchanged; inherited complete initial read | CLEAN | CLEAN | CLEAN |
| N2:1105 | 漬ける (reused; raw 浸ける) | Unchanged; inherited initial association review | CLEAN | CLEAN | CLEAN |
| N2:1106 | 伝わる | Unchanged; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1107 | 突っ込む | Unchanged; inherited complete initial read | CLEAN | CLEAN | CLEAN |
| N2:1108 | 務める | Unchanged; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1109 | 努める | Changed; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1110 | 綱 | Unchanged; inherited complete initial read | CLEAN | CLEAN | CLEAN |
| N2:1111 | 繋がり | Unchanged; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1112 | 繋がる | Unchanged; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1113 | 繋げる | Unchanged; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1114 | 粒 (reused; level-only) | Unchanged; inherited initial read | CLEAN | CLEAN | CLEAN |
| N2:1115 | 潰す | Changed; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1116 | 潰れる | Changed; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1117 | つまずく | Unchanged; inherited complete initial read | CLEAN | CLEAN | CLEAN |
| N2:1118 | 詰まる | Changed; complete reread | CLEAN | CLEAN | CLEAN |
| N2:1119 | 積む (reused; level-only) | Unchanged; inherited initial read | CLEAN | CLEAN | CLEAN |
| N2:1120 | 爪 | Unchanged; inherited complete initial read | CLEAN | CLEAN | CLEAN |
| N2:1121 | 艶 | Changed; complete reread | CLEAN | CLEAN | CLEAN |

**Reciprocal kanji – CLEAN.**
- `詰.md:33` (つ.まる row) and `詰.md:41` (Common words) link 詰まる.
- `造.md:31` and `造.md:39` link `[造る](../words/作る.md)` with alias context.
- Baseline frontmatter is intact, and the correction made no kanji changes.

**Baseline preservation – CLEAN.**
- 作る keeps its primary spelling 作る, reading つくる, title "make; prepare", N5 and kanji [作]. Its only change is guard 生産 on line 9.
- 付ける, 漬ける, 粒 and 積む were not touched by the correction.
- The patch keeps the initial baseline-addition record (4 作る, 2 付ける) separate from the current one (5 作る, 2 付ける).

**Mappings – CLEAN.** I reread all twenty TSV rows. The associations, levels, teaching IDs, senses and notes match my initial review, including:
- 2872052 as an identity correction for 務める.
- 1610400 kept as an additional ID for 点ける.
- Soaking-only sense for 浸ける.
- Senses 1/3/7 for 着ける.

Byte identity is the author's claim; I could not check it.

## Findings
**B56-Q1 (作る/生産): resolved.**
- Fix: `作る.md:9` now guards 生産.
- Basis: 1378990:1 is n/vs/vt "production, manufacture", and the old 生産 body teaches 車を生産 and 米を生産 and names 作る as the broader verb.
- The homograph 2092600 せいざん "live birth" is not conflated with せいさん.

**B56-Q2 (繋がり vs 繋がる/繋げる/繋ぐ): withdrawn.**
- 1251870:1 is a noun only, and the 繋がり body states it is "the **connection itself**". The three verb titles are predicates.
- The repository precedent matches the author's decline:
  - 始まり/始まる, 集まり/集まる and 決まり/決まる are unguarded, because their titles differ in form.
  - 流れ/流れる ("flow"), 終わり/終わる ("end") and 働き/働く ("work") are guarded because their English titles coincide.
- The 関係/接続 edges come from their する uses and do not carry over to 繋がり.

**B56-Q3 (努める/苦心): resolved.**
- Fix: `努める.md:9` now guards 苦心.
- Basis: 1244530:1 glosses "pains, hard work, effort". The old 苦心 body says "working or thinking hard to accomplish something difficult". That is a direct meaning overlap, not one inferred from the shared neighbours 努力/一生懸命.

**B56-Q4 (務める/役割; optional 役/務め): withdrawn.**
- 役割 (1538000), 役 (1537970) and 務め (1240810) name the role or duty itself.
- Their old bodies use separate verbs to perform it (役割を果たす, 務めを果たす, 役を演じる).
- 務める's own body teaches 役を務める as a pairing (role + verb), not as a substitute.
- The 勤め/勤める guard rests on titles that overlap in "work", not on a rule that same-root words always need a guard.

**B56-Q5 (潰れる/ぺちゃんこ, plus the 潰す extension): resolved.**
- Fix: `潰れる.md:9` and `潰す.md:9` now guard ぺちゃんこ.
- Basis: 2009680:1 "crushed flat, flattened, squashed" against 1433830:1 and 1433820:1 "smash, crush, flatten".
- The old ぺちゃんこ body contains 空き缶をぺちゃんこにつぶした, matching 潰す's 空き缶を潰しました.

**Optional suggestions the author adopted, all correct:**
- **艶 (`艶.md:24`, `艶.md:40`):**
  - The つや heading's sense 3, おもしろみ・味わい「芸に艶が出る」, supports "expressive charm in a performance", as does 1177680:3.
  - No sexuality sense was added. The えん headings and 1615260 are a separate reading.
  - The guards and the "senses 1-3" dictionary line are unchanged.
- **詰まる/渋滞 (`詰まる.md:9`):** supported by 1335570:1–2 against 1226480:2 "blocked/clogged" and by the old 渋滞 body's "backed up".
- **勉/力 links (`努める.md:29-30`):** both kanji cards exist and the primary kanji stays [努]. GPT's N2-56-GPT-03 made the same observation.

**Regression check – none found.**
- All five targets exist, with no self-guards and no duplicates within any list.
- No reverse declarations were added on 生産, 苦心, ぺちゃんこ or 渋滞.
- The only distractor involving a new target is 生活→生産, which is unrelated to the 作る/生産 guard.

**New findings:** none.

## Optional
- **伝わる/通信:** still weak and not required. 1433330 names the communicating activity; 1441900 is something being conveyed. This is the same noun-versus-predicate reasoning as Q2.
- **突/込 backlinks for 突っ込む:** still optional.

## Limits
- The patch being the complete diff, the unchanged TSV/snapshot bytes, the hashes and manifest determinism are all author-run checks or author claims.
- For the eight inherited rows, CLEAN is bounded: their guard judgments rest on titles, guard searches and principal families, not on complete comparison families or old bodies.
- All lexical evidence comes from the author's captures from one dictionary service. I made no fresh web retrievals.
- I ran no runtime quiz draws, can't give native-speaker certification, and draw no model ranking from the reviewers' unequal inspection depth.
