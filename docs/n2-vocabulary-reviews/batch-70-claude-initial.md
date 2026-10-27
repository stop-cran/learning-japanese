# N2 batch 70 review: twenty source rows (N2:1382–1401)

I found three defects. 引き受ける and 引き出す are each missing a quiz exclusion, and 引き分け claims a spelling (引分) that no source in scope records. The other seventeen rows, the 島/比/算 kanji edits, the reused-article baselines and all twenty mappings are CLEAN.

## Snapshot
- **Frozen commit:** `c30ca893b7f9271f6b3b95771a7ee361b9236e9f`. Parent is `c4a3c925334275122926cac9be1e036a13b95d5c`, and `frozen-snapshot.json` says the content is committed only.
- **No Git:** file tools cannot run Git. I did not independently check commit identity, the parent diff, hashes or equivalence. Those are the author's claims, and I relied on `related.patch` and the evidence files.

## Scope
**Model:** claude-opus-5.5 (claude family). Read-only; no agents and no edits.

**Read in full:**
- Rules: `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, and `docs\content-format.md` lines 18–103.
- Source and kanji edits: the TSV header (line 1) and lines 1382–1401 only, `related.patch`, and `kanji\島.md`, `比.md` and `算.md`.
- Private files: `review-mappings.jsonl`, `review-principals.jsonl`, `review-components.jsonl`, `frozen-snapshot.json` and `public-bodies.txt`.
- Older-article renderings: `old-body-inspection-04`, `-10`, `-14` and `-15`.
- All twenty assigned articles, twice.
- Comparison articles: 受け持つ, 割合, 引き出し, だます, しっかり, 降ろす.

**Read in part:**
- `review-evidence.json`, including the explicit baseline quiz additions.
- `family-inspection-01` to `-16`: searched only for entries 1589580, 1601640 and 1386380. Only ENTRY 1589580 (下ろす/降ろす) matched, in `-13`; I read it plus the next few records that the search output showed.
- About 100 comparison articles in `words\` (front matter only), plus targeted searches of the bodies of 汚い, 引く, 日, 分ける, 受付, 意地悪, ブレーキ, 合う, 寄る, 被る, 掛かる, 捕まる, かなり, なかなか, ずいぶん, 寧ろ, 比較 and 掛け算.

**Not read:**
- `review-labels.jsonl` and `supplement-comparison-reading.txt`.
- Old-body renderings 01–03, 05–09, 11–13, 16 and 17.
- `public-bodies.json`, and the capture receipts in `review-evidence.json`.
- `docs\confusable-words.md`, `docs\jlpt-levels.md`, `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`.
- No forbidden ledgers and no `batch-70.json`.

**Web:** one fetch of `weblio.jp/content/引分`. It returned encyclopedia text about 引き分け, not a dictionary spelling entry, so it verifies nothing.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1382 | 半島 | CLEAN | CLEAN | CLEAN | Kango はんとう. Reciprocal link with 島; footer ID 1479770 matches. No exclusion needed. |
| N2:1383 | ハンドル | CLEAN | CLEAN | CLEAN | Blank source spelling kept. Grip, steering wheel and handlebars are taught; the Internet handle is noted for recognition. 柄 exclusion is apt. Footer wording is optional polish (O2). |
| N2:1384 | 日当たり | CLEAN | CLEAN | CLEAN | 日光 and 日差し exclusions are apt. The restricted sense 2 is presented as recognition only. |
| N2:1385 | 日帰り | CLEAN | CLEAN | CLEAN | Exclusions for 旅行, 旅, 往復 and 遠足 are defensible. 帰り is distinct. |
| N2:1386 | 比較的 | CLEAN | CLEAN | CLEAN | Reciprocal link with 比 at ひかくてき; footer ID 1483600 matches. 較 and 的 have no cards and are correctly left unlinked. 寧ろ is contrasted. |
| N2:1387 | 日陰 | CLEAN | CLEAN | CLEAN | 陰 and 影 exclusions are apt. The 陰 kanji has no card. The sense 2 restriction is disclosed. |
| N2:1388 | ぴかぴか | CLEAN | CLEAN | CLEAN | Blank spelling kept; the sourced N2 level was added to a previously unlevelled article. Title, exclusions and assets are unchanged. |
| N2:1389 | 引き受ける | NEEDS FIX | CLEAN | CLEAN | Raw 引受る is recognized as irregular okurigana. See F1. |
| N2:1390 | 引き返す | CLEAN | CLEAN | CLEAN | Raw 引返す is recognized. The source gloss "repeat" is explicitly qualified; older literary senses are not over-taught. |
| N2:1391 | 引き算 | CLEAN | CLEAN | CLEAN | Raw 引算 is recognized. Native-first mixed reading follows 掛け算. Reciprocal link with 算; footer ID 1601610 matches. |
| N2:1392 | 引き出す | NEEDS FIX | CLEAN | CLEAN | N4 level and identity preserved; 引出す is described as search-only. See F3. |
| N2:1393 | 引き止める | CLEAN | CLEAN | CLEAN | Uses the ひきとめる heading, not ひきとどめる. Exclusions are defensible. |
| N2:1394 | 卑怯 | CLEAN | CLEAN | CLEAN | Daijisen's 比興 origin is presented as tentative, not as fact. Exclusions are defensible. |
| N2:1395 | 引き分け | NEEDS FIX | CLEAN | CLEAN | Raw 引分け is recognized. See F2. |
| N2:1396 | 日差し | CLEAN | CLEAN | CLEAN | Raw 陽射 is recognized; its empty dictionary capture is not treated as verification. Exclusions are apt. |
| N2:1397 | 肘 | CLEAN | CLEAN | CLEAN | ひじ, not ちゅう. 肘 is kept in metadata although it has no card. |
| N2:1398 | ピストル | CLEAN | CLEAN | CLEAN | Blank spelling kept. 銃 and 鉄砲 exclusions are apt. |
| N2:1399 | ビタミン | CLEAN | CLEAN | CLEAN | Blank spelling kept. German *Vitamin* origin is supported by Daijisen. |
| N2:1400 | ぴったり | CLEAN | CLEAN | CLEAN | N3 level preserved; the blank ぴたり spelling and gloss are kept. The abrupt-stop use is sourced to Daijisen ぴたり sense 3. Process wording is optional (O1). |
| N2:1401 | 引っ掛かる | CLEAN | CLEAN | CLEAN | Senses 1 and 4 are taught; the other senses are recognition uses tied to their constructions. The だます pairing is borderline (O4). |

**Kanji edits:** CLEAN.
- 島: the トウ reading row now links [半島] はんとう; footer ID 1479770 was already present.
- 比: a ヒ link to 比較的 ひかくてき was added; the footer adds 1483600.
- 算: the subtraction entry (voiced ざん) links 引き算; the footer adds 1601610.
- Existing headers and examples are preserved, and no missing cards were invented (none for 較, 的, 陰, 卑, 怯, 射 or 肘).

**Baseline preservation:** CLEAN. I checked this against the older article texts.
- ぴったり keeps N3, and 引き出す keeps N4.
- ぴかぴか's title, exclusions and image are unchanged; its N2 level is new.
- All the explicit quiz additions are present.

**Mappings:** CLEAN. All 20 match the TSV columns, JMdict entries, selected senses, levels and articles.

## Findings
- **F1** — Medium; Correctness (quiz exclusions); `words\引き受ける.md:9`
  - **Claim/impact:** 受け持つ is missing. Learners could accept either word's title for the other.
  - **Minimal remedy:** add 受け持つ to the exclusions on one of the two articles.
  - **Exact evidence:**
    - JMdict 1601520 sense 1 includes "to take charge of" and "to assume responsibility for".
    - 受け持つ's title (`受け持つ.md:4`) is "take charge of; be responsible for", and its exclusion list (`受け持つ.md:9`) is [担当, 係, 預かる, 責任], with no 引き受ける.
    - Daijisen defines 引き受ける sense 1 using 受け持つ.
    - The article already excludes 担当 ("being in charge").
  - **Confidence:** high.
- **F2** — Low; Correctness (spelling claim); `words\引き分け.md:30-31`
  - **Claim/impact:** the line "引分 is also recorded" is unsupported and could teach a spelling no cited source contains.
  - **Minimal remedy:** delete that clause, or cite a dictionary that records 引分.
  - **Exact evidence:**
    - JMdict 1169120 lists only the spellings 引き分け and 引分け.
    - The Daijisen heading 【引（き）分け】 (`public-bodies.txt:179`) allows only the き to be dropped.
  - **Confidence:** medium.
- **F3** — Low; Correctness (quiz exclusions); `words\引き出す.md:9`
  - **Claim/impact:** 引き出し is missing. Its title "drawer; cash withdrawal" overlaps 引き出す's "withdraw money; pull out", so an English-to-Japanese question could accept either.
  - **Minimal remedy:** add 引き出し to 引き出す's exclusions.
  - **Exact evidence:**
    - 引き出し's title is at `引き出し.md:4`, and it declares no exclusions.
    - The repository excludes similar noun/verb pairs: `貸し出し.md:9` [貸し, 貸す], `終わり.md:9` [終わる] and `話し合い.md:9` [話し合う].
    - This batch edited this exclusion list (adding 下ろす, 降ろす, 出す), so the omission is within its edit.
  - **Confidence:** medium-high.

## Optional
- **O1:** The process wording at `引き出す.md:46` and `ぴったり.md:37-39` is accurate but reads like contributor notes; consider moving it to source notes.
- **O2:** `ハンドル.md:48` says "senses 1-3; additional Internet sense 4". "Source senses 1-2; additional 3-4" would match the mapping.
- **O3:** `引っ掛かる.md:33` calls 引っかかる "another recorded spelling", but JMdict lists it first, with a priority marker. Consider wording that reflects how common it is.
- **O4:** The 引っ掛かる/だます pair is borderline and not established as a defect.
  - For: JMdict sense 4 is "to be deceived".
  - Against: the titles show the difference in voice, and repository practice is mixed. 挟まる/挟む is excluded, but 捕まる/捕まえる is not.
  - はめる ("entrap") is a weaker candidate.
- **O5:** `掛け算.md:29` could link 引き算, and the 比較 article could link 比較的.

## Limits
- **F2 rests on two sources:** JMdict and the Daijisen capture. An exact dictionary page recording 引分 would overturn it; the Weblio fetch returned encyclopedia text, not a dictionary entry.
- **Unread files:** the labels file, the comparison supplement, most family-inspection files, 13 of 17 old-body renderings, the receipts and the docs snapshot JSONs. Exclusion candidates beyond those I examined (about 100 checked by front matter, some read in full) may remain.
- **Partly read comparison bodies:** for 汚い, 引く and 日, I searched the article bodies but did not read them in full.
- **Judgement, not certification:** quiz-exclusion and naturalness verdicts are my reviewer judgement, not native-speaker certification.
- **Unverified author claims:** I executed no hash, equivalence or validator checks.
