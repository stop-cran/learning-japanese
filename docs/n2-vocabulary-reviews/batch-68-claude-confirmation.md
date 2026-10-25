I completed the confirmation review. Committed content only. The corrections resolve all five of my original findings and I found no regressions in the changed text. Two new low-severity defects remain, both present since the original snapshot: a stale wago note on the N2:1345 mapping, and 甚だしい missing a guard against 非常に and 極.

## Snapshot
- Corrected commit: **2776efdbf960a682f258bc60141d0983c1727612**
- Parent: **fc23c8b22dc373e0a087e4ee7f09b550a50d870f**
- I can't run Git, hash or cleanliness checks, so these are taken from correction-snapshot.json. I did not inspect `.git`. The author's hashes and equivalence checks were not checked independently.

## Scope
**Model:** claude-opus-5.5 (family claude). No edits, agents or delegation.

**Read completely in the corrected snapshot:**
- correction-snapshot.json and correction.patch.
- The mappings, principals and components JSONL files (20 / 20 / 31 records).
- All six corrective chunks: three family chunks (37 families: 10+12+15) and three older-body chunks (21 articles: 7+7+7), each read through to the end.
- All 24 assigned files: the 20 word articles and `kanji\肌.md`, `kanji\羽.md`, `kanji\根.md`, `kanji\放.md`.
- `words\着.る.md` was not the file name; the file read was `words\着る.md`.
- `docs\n2-vocabulary-sources.tsv` line 1 and lines 1342–1361 only.

**Additional reads:**
- Full older bodies: `words\非常に.md`, `words\極.md`, `words\ド.md`, `words\逆.md`.
- Title, tag and exclusion lines for あまり, あんまり, 大変, 過剰 and 激しい.
- Title scans in `words\` for competitors on each changed facet.
- `docs\content-format.md` lines 78–96, plus a grep for its tag and type rules.
- I fetched Kotobank 罰点-602843 myself this turn.

**Partial or omitted:**
- corrected-review-evidence.json: only grep hits plus lines around 82, 36670–36710, 37100–37130 and 40815–40850.
- Not read at all: correction-completed-inspection.json, the original 31 family/body chunks, the labels file and public-bodies.json.
- Not reread this turn: public-bodies.txt, frozen-snapshot.json and related.patch.
- No live quiz draws.

**Judgments inherited from my initial review and not re-derived here:**
- The mixed-reading convention: on-first readings are kango (台所, 毎朝), native-first are wago (場所). Those bodies were not reread.
- The Seisenban ばつ-602173 fetch.
- The 鉢多羅 note in 鉢.
- The 花火 and 羽 baseline comparison against the original related.patch.
- The content judgments on unchanged 鉢, 発揮, 発電, 発売 and 花嫁. Their full current bodies were reread.

## Verdicts
"Reread" below means a complete reread in the corrected snapshot.

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1342 | words\肌着.md | Reread; full 着る; family 1476500; components | CLEAN | CLEAN | CLEAN |
| N2:1343 | words\果たして.md | Reread; patch; さすが family and body | CLEAN | CLEAN | CLEAN |
| N2:1344 | words\鉢.md | Reread (unchanged); 鉢多羅 judgment inherited | CLEAN | CLEAN | CLEAN |
| N2:1345 | words\ばつ.md | Reread; family 2197150; both Seisenban pages | CLEAN | CLEAN | CLEAN |
| N2:1346 | words\発揮.md | Reread (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1347 | words\バック.md | Reread; patch; corrective families and bodies | CLEAN | CLEAN | CLEAN |
| N2:1348 | words\発射.md | Reread; patch; 撃つ and 打つ families | CLEAN | CLEAN | CLEAN |
| N2:1349 | words\発想.md | Reread; 案 family and body | CLEAN | CLEAN | CLEAN |
| N2:1350 | words\発電.md | Reread (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1351 | words\発売.md | Reread (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1352 | words\派手.md | Reread; オーバー family and body | CLEAN | CLEAN | CLEAN |
| N2:1353 | words\話し合い.md | Reread; 話, 話す and 論じる families and bodies | CLEAN | CLEAN | CLEAN |
| N2:1354 | words\話しかける.md | Reread; 言い出す and しゃべる families and bodies | CLEAN | CLEAN | CLEAN |
| N2:1355 | words\話し中.md | Reread; 忙しい family and body | CLEAN | CLEAN | CLEAN |
| N2:1356 | words\甚だしい.md | Reread; corrective families; 非常に and 極 bodies | NEEDS FIX | CLEAN | CLEAN |
| N2:1357 | words\花火.md | Reread; only `jlpt: 2` added | CLEAN | CLEAN | CLEAN |
| N2:1358 | words\花嫁.md | Reread (unchanged) | CLEAN | CLEAN | CLEAN |
| N2:1359 | words\放れる.md | Reread; full 離れる body in chunk 3 | CLEAN | CLEAN | CLEAN |
| N2:1360 | words\羽.md | Reread; family 1171680 (sense 5 restricted to 羽根) | CLEAN | CLEAN | CLEAN |
| N2:1361 | words\ばね.md | Reread; 春 family and body | CLEAN | CLEAN | CLEAN |

ばつ is CLEAN only for its qualified wording. The historical type is still unverified (see Limits).

**Edited kanji cards: all CLEAN.** The correction did not change them, and all four headers are preserved.
- 肌: はだぎ is in Readings (line 32) and Common words (line 37), with footer 1476500.
- 羽: the 羽根 note links to `words\羽.md` and states the hanetsuki restriction (line 43), with footer 1171680.
- 根: the 羽根 はね alias (line 43) links to `words\羽.md`. It makes no literal-root claim and adds no new character reading. Footer 1171680.
- 放: still N3. The はな.れる row is at line 33 and 放れる is in Common words at line 40, with footer 1516540.

**Primary and alias reciprocal pairs: CLEAN.**
- 肌 ↔ 肌着 はだぎ
- 羽 ↔ 羽 はね
- 根 ↔ 羽根 はね, pointing to the stable `words\羽.md`
- 放 ↔ 放れる はなれる

**Baseline preservation: CLEAN.**
- 花火 gains only N2.
- 羽 keeps N3, its title, reading, kanji, tags, `[翼]` exclusion and the original feather, wing and counter passages.
- `teachingSpelling: 羽根` respects sense 5's spelling restriction.

**Mappings:**
- All 20 associations are CLEAN: IDs, paths, selected and additional senses, reuse levels and blank raw fields all match the TSV.
- The N2:1345 provenance note is NEEDS FIX (B68-OPUS-06).

## Findings
**My original findings**

- **B68-OPUS-01 (fullwidth ｘ): resolved.** `ばつ.md:18` now recognizes ｘ for the cross-mark word and keeps the エックス letter reading distinct. The gloss stays blank.
- **B68-OPUS-02 (ばつ word type): resolved as a teaching claim.**
  - Lines 25–28 say the kango grouping is provisional, "not a verified etymology." The `etymology-uncertain` tag is allowed, since word tags are free (content-format.md:65 and 77).
  - Seisenban ばつ-602173 (「ばってん（罰点）」からできた語か) and 罰点-602843 (「…語源は「罰」「罰点」かといわれる」) both hedge, which matches the article.
  - The bare `type: kango` field carries no qualification by itself; the tag and body mitigate that.
- **B68-OPUS-03 (ばね/春): resolved.** I agree no ばね/泉 guard is needed: 泉's title, "spring; source of water", already tells the two apart.
- **B68-OPUS-04 (話し中/忙しい): resolved.** The physically-moving-phone line is gone, and line 29 is accurate.
- **B68-OPUS-05 (甚だしい/過剰): resolved.**

**My original miss on 発射/打つ:** I accepted the 打つ comparison in the initial review. F05 is right: 1408810 has no shooting sense and shooting is 撃つ (1253570). The current line 25 is accurate, and dropping the 打つ guard is correct.

**Author additions (F03–F11):**
- I concur with:
  - 果たして/さすが and 発想/案.
  - 派手/オーバー, on the exaggerated-behavior facet only.
  - 話し合い/話/話す/論じる and 話しかける/言い出す/しゃべる.
  - バック/下がる/背/バッグ, plus 返す/賛成 as context-specific guards.
  - 甚だしい/あんまり/大変.
- 甚だしい/あまり is borderline: あまり's title is "not very; not much", so the guard rests only on its secondary affirmative-excess sense. It is defensible, and the cost of over-excluding is low.
- The 放れる departure-を explanation (lines 21–22) keeps the verb intransitive and matches 離れる. The "moving backwards" wording and the 着る link with stem き → ぎ (肌着.md:23–24) are both correct.

**Regressions:** none found in the 13 changed articles.

**New: B68-OPUS-06** — low severity; mapping/provenance facet; high confidence.
- Location: `docs\n2-vocabulary-sources.tsv:1345`, the identical N2:1345 note in review-mappings.jsonl, and corrected-review-evidence.json around line 82.
- Claim: the note still says "Required wago field is disclosed as a practical kana-word grouping…", but the article is now provisional kango. The provenance contradicts the content. Learners don't see it.
- Remedy: change the note to "provisionally grouped as kango following the tentative 罰点 connection; tagged etymology-uncertain."

**New: B68-OPUS-07** — low severity; Correctness facet (quiz guard); moderate confidence.
- Location: `words\甚だしい.md:9`.
- Claim: 甚だしい ("extreme; excessive") teaches the adverb 甚だしく at line 17. 非常に ("extremely", no exclusions) and 極 ("very; extremely") share its `degree` tag, which makes them likely distractors (content-format.md:81). A learner could reasonably accept "extremely" for 甚だしい, which meets the test at content-format.md:95. The added あまり edge rests on weaker overlap.
- Remedy: add 非常に and 極 to 甚だしい's `quiz_exclusions`. A one-sided declaration covers both directions.

## Optional
- ばつ.md:18 says "Dictionaries also record…", but only JMdict 2197150 is shown recording ｘ. Consider "JMdict records…".
- Deferred, no objection: the Xも甚だしい pattern; the 羽 N3 counter-provenance wording and an extra hanetsuki gloss; a 話し合う note.
- Possible guards that are weaker than B68-OPUS-07:
  - 甚だしい/ド ("extreme; very; emphatic prefix") and 甚だしい/超過.
  - バック/逆 (shared token "reverse"); 逆 itself already says it is not literal backward movement.
- Not established: 話し中/会話, 派手/豪華/贅沢/大層, 発想/連想/見当.

## Limits
- All public text comes from one authority, Digital Daijisen via Weblio. Raw ｘ returned エックス, and raw 話合い and 話中 returned empty results.
- The two Seisenban pages are my own fetches with no saved hashes.
- The historical origin and type of ばつ remain unverified; only the hedged claim is verified.
- Guard checks rely on title scans plus the bodies I actually read. They are not exhaustive, and there were no live quiz draws.
- There is no native-speaker or frequency certification.
- Inherited batch-61 quiz debt is deferred.
- The partial evidence and inspection reads listed under Scope may contain author reasoning I did not see.
