I found four minor defects across four articles, all metadata, link or comparison-wording issues. No core definitions are wrong, and the kanji edits, the どきどき reuse and all twenty mappings check out.

## Snapshot
d4f6a3e42f752c696ecaa808ea08e7a1b3eb4e00 (parent 32ac78a1c12f9ea2813b8075036347ac7893f93f), committed content only. File tools can't run Git, so the snapshot hashes, equivalence checks and the lower-level check are as the author reported them; I didn't verify them.

## Scope
**Model:** claude-opus-5.5 (claude family).

**Read in full:**
- The three instruction files, with docs\content-format.md lines 18-103.
- related.patch.
- All 19 new articles, words\どきどき.md and kanji\灯.md, 油.md, 童.md, 溶.md.
- The mappings, principals, components and labels JSONL files.
- public-bodies.txt.
- The TSV header and rows N2:1182-1201.

**Read in part:**
- Bodies or headers of comparison articles: 役, 入口, 避ける, ストーブ, 酸っぱい, 丸い, and the titles of 係, 務め, 勤め, 義務, 役割, 交替, 番, 担当, 苦情, 玄関.
- The family-inspection, support and extra files, only through targeted record searches: 石油, オイル, 宜しく, the 退く families, 避ける, 交代, 役, 役割, 油, 合わせる, 混合, plus the first 60 lines of chunk 01.

**Not read:**
- review-evidence.json and public-bodies.json (I read the .txt rendering).
- Every inspection record I didn't target.
- docs\n2-vocabulary-snapshot.json, docs\n2-source-snapshot.json, docs\confusable-words.md and docs\jlpt-levels.md.

**No web fetches.**

## Verdicts
Cells are correctness / scoped coverage / comprehensibility.

| Row | Article | Verdict |
|---|---|---|
| N2:1182 | words\当日.md | CLEAN / CLEAN / CLEAN |
| N2:1183 | words\投書.md | NEEDS FIX (F1) / CLEAN / CLEAN |
| N2:1184 | words\登場.md | CLEAN / CLEAN / CLEAN |
| N2:1185 | words\どうせ.md | CLEAN / CLEAN / CLEAN |
| N2:1186 | words\どうぞよろしく.md | CLEAN / CLEAN / CLEAN |
| N2:1187 | words\灯台.md | CLEAN / CLEAN / CLEAN |
| N2:1188 | words\盗難.md | CLEAN / CLEAN / CLEAN |
| N2:1189 | words\当番.md | NEEDS FIX (F2) / CLEAN / CLEAN |
| N2:1190 | words\等分.md | CLEAN / CLEAN / CLEAN |
| N2:1191 | words\透明.md | CLEAN / CLEAN / CLEAN |
| N2:1192 | words\灯油.md | NEEDS FIX (F4) / CLEAN / CLEAN |
| N2:1193 | words\東洋.md | CLEAN / CLEAN / CLEAN |
| N2:1194 | words\童話.md | CLEAN / CLEAN / CLEAN |
| N2:1195 | words\通り掛かる.md | CLEAN / CLEAN / CLEAN |
| N2:1196 | words\溶かす.md | CLEAN / CLEAN / CLEAN |
| N2:1197 | words\尖る.md | NEEDS FIX (F4) / CLEAN / CLEAN |
| N2:1198 | words\どきどき.md (reused; only `jlpt: 2` added) | CLEAN / CLEAN / CLEAN |
| N2:1199 | words\溶く.md | CLEAN / CLEAN / CLEAN |
| N2:1200 | words\退く.md | NEEDS FIX (F3) / CLEAN / CLEAN |
| N2:1201 | words\特殊.md | CLEAN / CLEAN / CLEAN |

- **N2:1186 どうぞよろしく:** the public lookup returned no dictionary text, so this relies on JMdict and the existing 宜しく card.
- **N2:1198 どきどき:** the existing body covers JMdict senses 1 and 2.

**Kanji edits (灯/油/童/溶): CLEAN.**
- Headers are unchanged.
- All six pairs link at the right reading rows and in Common words: 灯台/灯油 on 灯, 灯油 on 油, 童話 on 童, and 溶かす/溶く on 溶.
- Footer entry IDs match: 灯 adds 1448730 and already had 1448760; 油 adds 1448760; 童 adds 1454000; 溶 already had 1546040 and 1546050.
- The word sides link every existing kanji. No cards were invented for 透, 尖 or 殊.

**Baseline preservation: CLEAN.** どきどき's identity, reading, title, exclusions and body are unchanged.

**Mappings: CLEAN.** All 20 TSV rows match the mapping and principal records. 退く's raw source gloss ("retreat") actually fits しりぞく better, but the article handles that explicitly.

## Findings
**F1 — Minor; quiz metadata; words\投書.md:4, 9, 38; medium confidence**
- **Claim:** the title includes "written complaint", and 苦情 is titled "complaint; grievance; objection". `quiz_exclusions: [手紙]` doesn't guard 苦情, so either word could look correct when the other is the prompt. The article itself compares the two at line 38.
- **Remedy:** add 苦情 to the exclusions.

**F2 — Minor; quiz metadata; words\当番.md:4, 9; medium confidence for 役, low-medium for 義務**
- **Claim:** 当番 already excludes 務め ("duty; responsibility"), 勤め and 係. It omits 役 ("role; duty"), which overlaps the same way. 義務 ("duty; obligation") overlaps in title too, and 務め itself excludes both 義務 and 役.
- **Remedy:** add 役; consider 義務.

**F3 — Minor; correctness; words\退く.md:38; medium-high confidence**
- **Claim:** "避ける (さける) concerns avoiding or moving clear of something." In JMdict entry 1583260, the "move out of the way" sense (4) and "avoid physical contact" sense (1) are restricted to the よける reading; さける covers avoiding situations. The existing 避ける card says the same.
- **Remedy:** limit さける to avoiding situations, or name よける for physically moving clear.

**F4 — Minor; linking; high confidence**
- **Claim:** existing word cards are mentioned without links:
  - 丸い at words\尖る.md:40
  - 酸っぱい at words\尖る.md:46
  - ストーブ at words\灯油.md:24-25
- **Remedy:** link each at that mention.

## Optional
- **登場:** "entrance on stage" shares the English word "entrance" with 入口 and 玄関. This is a low-confidence pair, so it isn't listed as a finding.
- **どうせ, line 36:** "Calling someone どうせ…" could be reworded as "Saying どうせ about someone's efforts…".
- **Possible additions:**
  - 灯台下暗し for 灯台.
  - 昔話 and おとぎ話 for 童話.
  - 通りがかり for 通り掛かる.
  - のく as another reading of 退く sense 1, and どける/どかす as its transitive counterparts.

## Limits
- I didn't independently re-run the pinned lower-level check, the hash checks or the equivalence checks.
- All 19 successful public lookups come from one dictionary service (Digital Daijisen via weblio). The どうぞよろしく lookup returned no dictionary text.
- Most family-inspection records weren't read, so other overlapping secondary senses could exist.
- The quiz-exclusion calls, F1 and F2 especially, are judgment-based.
- This is not a native-speaker check.
