## Snapshot: 77ffbe55d56c925eba2343f9be59b9dcb2daf843; committed content only

Parent: `b5684c408f12489418a9bb3c4626b6067e7015b8`.

**Two actionable quiz-metadata findings:** an unprotected softness overlap in the reused ふわふわ article, and excessive exclusions in 風呂敷. The former is **pre-existing, not a regression from adding `jlpt: 2`**. No actionable lexical-teaching or mapping defect was established in the other source rows.

The supplied receipt identifies this as clean committed content. I could not independently execute Git to verify that assertion. No files were changed.

## Scope: gpt-6.1-sol; family gpt

Independent, read-only review; serial reads, no agents, delegation, concurrent work, or other reviewer input.

Read completely:
- All nineteen assigned articles; `batch-75-related.patch`; required repository instructions and `docs\content-format.md:18–103`.
- All **20 mappings, 19 principal families/35 senses, 18 component records, and 188 comparison labels**, using complete bounded JSONL ranges. Restrictions, flags, inherited POS, raw fields, and one-based sense selections were included.
- The TSV header at physical line 1 and **only rows 1482–1501**; both permitted source-snapshot JSON files.
- All fifteen older-body renderings: **123 complete articles**, including the pre-change ふわふわ. Also read current `次第`, `意志`, `崩す`, and `覚悟`, and reread current bodies consequential to the findings.
- Complete comparison-family renderings 01–02 (**54 family records**), plus complete targeted families returned in rendering 08:118–155, 09:1–105, and 10:55–85. Incidental partial records at range boundaries were not counted as complete families.
- The complete six-sense 次第 supplement; all twenty public captures in both `public-bodies.txt` and their JSON receipt.
- Existing component cards 下、切、増、名、舞、風、火、分、解, including their bodies and levels. Also fetched [語源由来辞典’s 風呂 entry](https://gogen-yurai.jp/furo/), which supports treating its historical derivation as disputed.

The twenty frozen lexical captures are **Digital Daijisen through Weblio—one authority**, not twenty independent dictionaries. Applicable readings/headings were separated from character headings, historical readings, and unrelated homographs.

**Coverage boundaries:** I did not inspect all 315 prepared comparison families/780 senses or every labelled article body. `review-evidence.json` was read only through line 130; the complete compact derivatives supplied the required records. `docs\confusable-words.md` received a partial read, not a complete-document read. Prohibited ledgers, author quiz rationale, scripts/checks, and reviewer reports were not read. Prepared material and author-executed checks were not counted as reviewer inspection.

## Verdicts:

Here, **Correctness includes quiz-answer validity and exclusion metadata**. CLEAN means no actionable defect established within this review, not exhaustive correctness.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1482 踏切 | `words\踏切.md` | CLEAN | CLEAN | CLEAN | Railway-crossing teaching is clear; other selected senses are recognition. Pinned starting-line wording is distinguished from public takeoff usage. |
| N2:1483 麓 | `words\麓.md` | CLEAN | CLEAN | CLEAN | Applicable ふもと mountain/hill-base identity; not body-part “foot” or every bottom. |
| N2:1484 増やす | `words\増やす.md` | CLEAN | CLEAN | CLEAN | Transitive godan, object marking, 増える contrast, and increase-by quantity are adequately taught. |
| N2:1485 殖やす | `words\増やす.md` | CLEAN | CLEAN | CLEAN | Separately assessed: same entry1602880 and reading; rare spelling explicitly retained without an absolute subject-matter restriction. |
| N2:1486 blank spelling; フライパン | `words\フライパン.md` | CLEAN | CLEAN | CLEAN | Blank source spelling preserved; cookware noun and instrumental で are clear. |
| N2:1487 blank spelling; ブラウス | `words\ブラウス.md` | CLEAN | CLEAN | CLEAN | Garment meaning and 着る construction are natural; care/style claims are qualified. |
| N2:1488 blank spelling; ぶらさげる | `words\ぶらさげる.md` | CLEAN | CLEAN | CLEAN | Stable kana identity preserved; ぶら下げる, transitive ichidan behavior, and hanging/carrying constructions are taught. |
| N2:1489 blank spelling; ブラシ | `words\ブラシ.md` | CLEAN | CLEAN | CLEAN | Correctly a tool noun, not an adjective inferred from source “brushy”; electrical use is contextual recognition. |
| N2:1490 blank spelling; プラスチック | `words\プラスチック.md` | CLEAN | CLEAN | CLEAN | Material usage and プラスティック recognition are sound; properties are not universalized. |
| N2:1491 blank spelling; プラットホーム | `words\プラットホーム.md` | CLEAN | CLEAN | CLEAN | Railway lead plus practical public extensions; no fabricated pinned sense numbers. |
| N2:1492 blank spelling; フリー | `words\フリー.md` | CLEAN | CLEAN | CLEAN | Six selected uses are differentiated; price, independence, availability, and substance-free recognition are not conflated. |
| N2:1493 振り仮名 | `words\振り仮名.md` | CLEAN | CLEAN | CLEAN | Source spelling, usual kana spelling, annotation function, and attachment are explicit. |
| N2:1494 blank spelling; プリント | `words\プリント.md` | CLEAN | CLEAN | CLEAN | Printing/copy and handout senses; noun versus をプリントする; photographic/textile recognition. |
| N2:1495 振舞う | `words\振舞う.md` | CLEAN | CLEAN | CLEAN | Source identity retained; 振る舞う taught; behavior versus hospitality participants and godan forms are clear. |
| N2:1496 blank spelling; ブローチ | `words\ブローチ.md` | CLEAN | CLEAN | CLEAN | Brooch ornament, not the separate broach-tool homograph; no unnecessary gemstone requirement. |
| N2:1497 blank spelling; プログラム | `words\プログラム.md` | CLEAN | CLEAN | CLEAN | Event plan, booklet, and computing uses distinguished; actual ソフト and 次第 secondary meanings considered. |
| N2:1498 風呂敷 | `words\風呂敷.md` | NEEDS FIX | CLEAN | CLEAN | Cloth teaching is sound; 包み／包む exclusions exceed demonstrated ambiguity. **B75-GPT-02**. |
| N2:1499 blank spelling; ふわふわ | `words\ふわふわ.md` | NEEDS FIX | CLEAN | CLEAN | All three selected senses covered; pre-existing direct ソフト overlap remains unguarded. **B75-GPT-01**. |
| N2:1500 噴火 | `words\噴火.md` | CLEAN | CLEAN | CLEAN | Volcanic noun/intransitive-suru construction; no required flame or arbitrary anger meaning. |
| N2:1501 分解 | `words\分解.md` | CLEAN | CLEAN | CLEAN | Mechanical, analytical, chemical, and factorization uses; both transitivity patterns for the first two senses are acknowledged. |

**Mappings, assessed separately:** correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN** for all twenty. Source IDs, readings, blank spellings, teaching entries, article targets, and one-based selections agree with the assigned TSV rows. 殖やす remains a separately indexed mapping to the shared 増やす article. All 35 principal senses are selected across the nineteen families; empty additional-sense fields were not populated by inference. More briefly presented recognition uses and public extensions were not independently assigned N2 or attributed to compiler intent.

**Reused-header change:** correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**. Comparing the complete old rendering, current article, and patch supports preservation of identity, reading, title, type, kanji, tags, exclusions, image reference/description, and body. The only shown change is `jlpt: 2`. B75-GPT-01 concerns that preserved baseline, not a newly introduced change.

**Components and reciprocal links:** correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**. Primary written-kanji metadata is complete, including characters without cards. Existing substantive links cover 切、増、名、舞、風、火、分、解; the alternative ぶら下げる also links 下. Their existing levels are N5 下・名・火・分, N4 切・風, and N3 増・舞・解. No primary source character has an existing N2 card, so **no new scoped reciprocal N2 pair or required kanji-card edit was established**. Missing cards were not invented.

## Findings:

**B75-GPT-01 — Moderate; correctness, quiz validity; pre-existing baseline issue.**

**Location:** `words\ふわふわ.md:9,18–30`; `words\ソフト.md:4,8–29`.

The word quiz can offer **“soft”** for ふわふわ even though that is an applicable selected meaning. ふわふわ’s exclusions omit ソフト, and ソフト declares no reciprocal exclusion. This is a direct softness overlap, not a conclusion inherited through 柔らかい or another intermediate card. ソフト’s additional software meaning does not remove its adjective sense.

**Impact:** a defensible meaning can appear as a supposedly wrong answer; exact-title deduplication does not protect the differently worded titles.

**Minimal remedy:** declare the direct ふわふわ／ソフト pair on either endpoint, as a separately authorized baseline correction. Preserve the existing lexical identity and sourced level.

**Exact evidence:** principal JMdict **1113060, sense 2** explicitly includes “soft; fluffy; spongy”; complete comparison family **1075500, sense 1** includes “soft; gentle; mild.” The current articles teach those applicable meanings.

**Confidence:** high.

**B75-GPT-02 — Minor; correctness, excessive quiz exclusions.**

**Location:** `words\風呂敷.md:9,16–20,38–41`; `words\包み.md:4,16–21`; `words\包む.md:4,15–19,36–39`.

The exclusions of **包み** and **包む** are not supported by the inspected applicable meanings. The displayed titles are respectively **“bundle; wrapped package”** and **“wrap; bundle,”** while 風呂敷 names the **wrapping cloth**, not the package or wrapping action. Its own explanation and whole example correctly maintain that distinction.

This judgment considers the complete つつみ and つつむ families, including secondary senses; it is not a blanket noun/verb exemption. Neither family supplies the cloth-object meaning. Sharing a wrapping event—or an exclusion between 包み and 包む—does not establish either direct pair with 風呂敷.

**Impact:** valid contrasting choices are unnecessarily removed, potentially shrinking the available quiz pool.

**Minimal remedy:** remove 包み and 包む from 風呂敷’s exclusions while retaining the useful body comparisons. This does not imply removing their own mutual guard.

**Exact evidence:** JMdict **1500150, sense 1** identifies a furoshiki/wrapping cloth/cloth wrapper; **1515340, complete senses 1–2** identify a package and a counter; **1584060, complete senses 1–4** cover wrapping, enveloping, concealing, and giving money in an envelope. The frozen Daijisen **ふろしき** heading likewise defines the cloth.

**Confidence:** high.

## Optional:

For プログラム, an attested transitive **プログラムする** example could make selected sense 3’s productive verb use more explicit. This is nonblocking expansion: the existing noun-centered examples already distinguish the three practical referents.

## Limits:

File tools could not execute Git. Commit identity, clean-worktree status, hashes, and compact-rendering equivalence therefore remain **supplied receipt assertions**, not independently executed reviewer checks.

Not all prepared comparison families or labelled bodies were inspected; this is not whole-corpus quiz certification. The findings above use complete consequential records and actual bodies, rather than treating uninspected material as absent.

The public captures verify applicable lexical headings, not every teaching claim, frequency assertion, or example collocation. Naturalness judgments here are not native-speaker or corpus certification. The image reference and description were checked for preservation; the image binary/render was not inspected.
