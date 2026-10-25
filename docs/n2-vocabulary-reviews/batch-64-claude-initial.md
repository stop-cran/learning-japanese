# N2 batch 64 review: rows N2:1262–1281

I found two small problems. 憎らしい gives a "darling" meaning in its title that the article never explains or shows in an example. 憎い and 憎らしい also list なかなか as a quiz exclusion even though it shares no meaning with either word. Everything else checked out within the evidence I read.

## Snapshot
The frozen commit is **9eb5a046068bdf31aed69a6bdb6f505bc81a39b6** (parent 4aa1a5697e98ae51e93a740f68ec817b817703be). I reviewed committed content only. My file tools can't run Git, so the commit, hash and equivalence checks are the author's records from frozen-snapshot.json. I did not run them myself.

## Scope
- **Model:** claude-opus-5.5 (claude family). No agents, delegation or edits.
- **Guidance read:** .github\copilot-instructions.md, content-structure.instructions.md and docs\content-format.md:18-103.
- **Assigned files read in full:**
  - all twenty words\ articles;
  - related.patch;
  - kanji\憎.md, kanji\課.md and the unchanged kanji\鈍.md.
- **Private files read in full:**
  - review-mappings, review-principals, review-components and review-labels (all 158 labels);
  - public-bodies.txt;
  - family-inspection-09.txt (suffix 2772730, のろい 2838553).
- **Private files read in part:**
  - review-evidence.json, lines 1-80 and 2355-2700;
  - family-inspection-01.txt, record 1149830 only.
- **TSV:** the header and rows 1262–1281 only.
- **Older articles read in full:** におい, 臭い, 働き, 労働 and なかなか.
- **Web fetches:**
  - kotobank 日時 and 匂う (Nihon Kokugo Daijiten), both relevant;
  - Weblio 臭う and kotobank 臭う failed (boilerplate or an unrelated page).
- **Not read:**
  - family chunks 02–08 and old-body chunks 01–11;
  - both supplement chunks and both schedule files;
  - public-bodies.json and the rest of review-evidence.json;
  - docs\n2-vocabulary-snapshot.json, docs\n2-source-snapshot.json, confusable-words.md and jlpt-levels.md.

## Verdicts
Each row shows the article, the dictionary sense mapping and three cells: correctness / scoped coverage / comprehensibility. In a mapping, the senses before "+" are selected and the senses after it are additional.

| Row | Article | Mapping | Correctness | Coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1262 | words\なんとなく.md | 1599730:1 | CLEAN | CLEAN | CLEAN |
| N2:1263 | words\なんとも.md | 1188690:1,2 | CLEAN | CLEAN | CLEAN |
| N2:1264 | words\ナンバー.md | 1090860:1+2 | CLEAN | CLEAN | CLEAN |
| N2:1265 | words\南米.md | 1460570:1 | CLEAN | CLEAN | CLEAN |
| N2:1266 | words\南北.md | 1460600:1+2 | CLEAN | CLEAN | CLEAN |
| N2:1267 | words\煮える.md | 1322490:1 | CLEAN | CLEAN | CLEAN |
| N2:1268 | words\匂う.md | 1599780:1,2+3,4 | CLEAN | CLEAN | CLEAN |
| N2:1269 | words\逃がす.md | 1450320:1+2 | CLEAN | CLEAN | CLEAN |
| N2:1270 | words\憎い.md | 1403390:1+2 | **NEEDS FIX** (B64-CL-02) | CLEAN | CLEAN |
| N2:1271 | words\憎む.md (reused) | 1403440:1 | CLEAN | CLEAN | CLEAN |
| N2:1272 | words\憎らしい.md | 1403450:1+2 | **NEEDS FIX** (B64-CL-02) | CLEAN | **NEEDS FIX** (B64-CL-01) |
| N2:1273 | words\にこにこ.md (reused) | 1091130:1, empty source gloss kept | CLEAN | CLEAN | CLEAN |
| N2:1274 | words\濁る.md | 1415960:1,3+2,4 | CLEAN | CLEAN | CLEAN |
| N2:1275 | words\虹.md | 1463740:1 | CLEAN | CLEAN | CLEAN |
| N2:1276 | words\日時.md | 1464110:1+2 | CLEAN | CLEAN | CLEAN |
| N2:1277 | words\日用品.md | 1464910:1 | CLEAN | CLEAN | CLEAN |
| N2:1278 | words\日課.md | 1463860:1 | CLEAN | CLEAN | CLEAN |
| N2:1279 | words\日程.md | 1464300:1 | CLEAN | CLEAN | CLEAN |
| N2:1280 | words\鈍い.md (reused) | 1582430:1,2,4+3,5, distinct from のろい 2838553 | CLEAN | CLEAN | CLEAN |
| N2:1281 | words\入社.md | 1466260:1 | CLEAN | CLEAN | CLEAN |

**Kanji cards and other checks:**
- **憎 edit: CLEAN.**
  - 憎い (にくい) and 憎らしい (にくらしい) appear in the reading row and in Common words.
  - Footer IDs 1403390 and 1403450 are present, and the header is preserved.
  - The existing 憎/憎む pair is intact (footer 1403440).
- **課 edit: CLEAN.** 日課 (にっか) is in the カ row and Common words, the footer has 1463860, and the header is unchanged.
- **Unchanged 鈍: CLEAN.** It links 鈍い under にぶ.い with footer 1582430. のろい 2838553 is a separate entry; chunk 09 confirms it is a different identity.
- **Baseline preservation (憎む, にこにこ, 鈍い): CLEAN.** The patch adds only `jlpt: 2`. Bodies, identities, readings, titles and exclusions are unchanged.
- **Mappings: all twenty CLEAN** for correctness, coverage and comprehensibility. They match the TSV rows.
- **Kanji links:**
  - Every existing card is linked from the word side: 何, 南, 米, 北, 逃, 憎, 日, 時, 用, 品, 課, 程, 入 and 社.
  - 煮, 匂, 濁 and 虹 have no cards. They are correctly left unlinked but still listed in the metadata.

## Findings
**B64-CL-01** — Minor; definition/comprehensibility
- **Location:** words\憎らしい.md:4, 12, 19-24
- **Claim:** The title says "ironically darling", but the only non-hostile example (line 20, 憎らしいほど上手) shows grudging admiration, not affection. "Darling" is only mentioned in passing at line 23, with no explanation or example. "Ironically darling" is also unidiomatic English, and it diverges from 憎い's "admirable" even though both articles teach the same admiring use.
- **Impact:** Learners get a title meaning the body never shows.
- **Remedy:** Either retitle to match what the body teaches (for example "hateful; (ironically) annoyingly good"), or add one attested affectionate example with a one-line explanation.
- **Evidence:** JMdict 1403450 sense 2 "(speaking ironically) darling"; Daijisen 憎らしい ② 「気にさわるほどすばらしい」.
- **Confidence:** medium.

**B64-CL-02** — Low; quiz_exclusions (excess)
- **Location:** words\憎い.md:9 and words\憎らしい.md:9
- **Claim:** なかなか ("quite; not readily"; its body teaches degree and "not readily") shares no meaning with "hateful; ironically admirable/darling". The only link is the collocation なかなか憎い. content-format.md:91 requires exclusions to come from actual overlapping meaning, and the two identical lists look like a copied clique.
- **Impact:** A legitimate distractor is suppressed in both quiz directions.
- **Remedy:** Remove なかなか from both lists.
- **Evidence:** labels title "quite; not readily"; words\なかなか.md.
- **Confidence:** medium-high.

No missing exclusions were established. I checked 日課 against 働く/働き/労働, 日程 against カレンダー/定期, 逃がす against 逃げる, 入社 against 勤める/出勤, and 煮える against 焼ける.

## Optional
These are non-blocking suggestions:
- **濁る:** add an example for the selected moral-impurity sense (sense 3), such as 濁った世の中; it is currently explained in prose only.
- **Exclusions on 憎い/憎らしい:** 良い and いい are weak but defensible.
- **Exclusions on 匂う and なんとも:**
  - 匂う's 光る, 輝く, 怪しい and 疑わしい are defensible because the article teaches the glow and suspicion uses.
  - 非常 on なんとも is a marginal guard.
- **Kana spellings:** note that the admiring use of 憎い is often written ニクい or にくい.
- **逃がす:** say that 逃す (のがす) is the more usual verb for missing a chance.
- **匂う:** note that 臭い can also be read におい.

## Limits
- I could not run Git. The hash, equivalence and lower-level TSV no-match checks were run by the author, not by me.
- All twenty public captures come from one source (Digital Daijisen via Weblio). My only independent support is the two kotobank pages (Nihon Kokugo Daijiten):
  - 日時 ② confirms the elapsed-time sense.
  - 匂う ③ and ⑨ support the classical "glow" use and the "something seems fishy" use.
- Not confirmed:
  - the modern "literary" register label for 匂う's glow sense;
  - the spelling 臭う for the suspicion use (both 臭う fetches failed).
- I did not read family chunks 02–08, any old-body chunk or the supplements. My exclusion judgments rely on the 158 label titles and exclusions plus five older bodies I read in full, not full-body coverage.
- Naturalness judgments are not a native-speaker certification.
