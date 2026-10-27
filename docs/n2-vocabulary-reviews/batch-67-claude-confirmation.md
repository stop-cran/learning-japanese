# Batch 67 corrected-snapshot confirmation (rows N2:1322–N2:1341)

## Snapshot
- **Corrected commit:** `0aed71b4df27a66ad8a0b6fe6c82530e8dba3682`
- **Parent:** `82e2764231c6146414d806551d1db63670d9191a`
- Committed content only, taken from `batch-67-correction-snapshot.json`, which was read first.
- My file tools cannot run Git, hash or cleanliness checks, and I did not look in `.git`. The commit, parent and hashes are what the author recorded; I did not check them myself.

## Scope
**Model:** claude-opus-5.5 (Claude family), resuming the same session. Read-only: no edits, agents or delegation.

**Read in full this session:**
- `correction-snapshot.json` and the whole `correction.patch`.
- All 22 assigned content files (the 18 word articles and the 4 kanji cards), as they stand now.
- The 3 compact files: mappings (20 records), principals (18 families) and components (27 records).
- Both correction chunks, which ended cleanly:
  - Families: 11 families, 35 senses.
  - Older articles: 千切る, 傑作, むかむか, 回る, 概論, タイプ, 種類, 一種.
- `words\場所.md`, `words\磨く.md` and `kanji\気.md`.
- The TSV header (line 1) and lines 1322–1341. These lines are exactly N2:1322–N2:1341 and match the mappings field by field: IDs, articles, levels, selected and additional senses, blank fields, and notes.

**Read in part:**
- `correction-completed-inspection.json`: lines 1–80 only (the receipt header).
- Searches of `docs\content-format.md` and `.github\*` for the mixed-reading and quiz-exclusion rules.
- The titles and exclusions of 17 comparison words.

**Not read:**
- `corrected-review-evidence.json`.
- `docs\n2-vocabulary-snapshot.json`, `docs\n2-source-snapshot.json`, `docs\confusable-words.md`, `docs\jlpt-levels.md`.
- No new web pages were fetched.

**Carried over from the original session, not re-checked now:**
- How the articles line up with the captured Daijisen text (from `public-bodies.txt`).
- The `frozen-snapshot.json` and `related.patch` contents, and the unchanged kanji headers.
- The full read of `kanji\計.md`.
- Which component kanji cards exist.
- Older exclusions pointing at these words from other articles, e.g. きびきび→はきはき and 測定→計る.
- The earlier Kotobank and Jisho fetches.
- The four full comparison articles read originally: 払う, タイプ, 始め, 初め.

## Verdicts
Read-basis key:
- **A:** full current article
- **M:** mapping plus the exact TSV row
- **P:** complete principal family
- **C:** component records
- **X:** correction chunk evidence (family plus full older article)
- **D:** Daijisen judgment carried over from the original session

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1322 | words\生える.md | A, M, P1378490, C生, D | CLEAN | CLEAN | CLEAN |
| N2:1323 | words\はがす.md | A, M, P1600670, C剥/剝, X1389020+千切る, D (剥がす; raw 剥す lookup returned 404) | CLEAN | CLEAN | CLEAN |
| N2:1324 | words\ばからしい.md | A, M, P1612910, X1253840+傑作, D | CLEAN | CLEAN | CLEAN |
| N2:1325 | words\秤.md | A, M, P1474220, C秤, D | CLEAN | CLEAN | CLEAN |
| N2:1326 | words\計る.md | A, kanji 量 card, M, P1600650, C量/計, D | CLEAN | CLEAN | CLEAN |
| N2:1327 | words\計る.md | A, kanji 測 card, M, P1600650, C測/計, D | CLEAN | CLEAN | CLEAN |
| N2:1328 | words\吐き気.md | A, M, P1444120, C気/吐/嘔, full 気.md and 場所.md, X1012330+むかむか, D | CLEAN | CLEAN | CLEAN |
| N2:1329 | words\はきはき.md | A, M, P1010090, D | CLEAN | CLEAN | CLEAN |
| N2:1330 | words\掃く.md | A, kanji 掃 card, M, P1399760, C掃, full 磨く.md, D | CLEAN | CLEAN | CLEAN |
| N2:1331 | words\歯車.md | A, M, P1313350, C歯/車, D | CLEAN | CLEAN | CLEAN |
| N2:1332 | words\バケツ.md | A, M, P1098340, C馬/穴/尻, D | CLEAN | CLEAN | CLEAN |
| N2:1333 | words\挟まる.md | A, kanji 挟 card, M, P1236840+1600740, C挟/挾, Kotobank (carried over) | CLEAN | CLEAN | CLEAN |
| N2:1334 | words\挟む.md | A, kanji 挟 card, M, P1600740 | CLEAN | CLEAN | CLEAN |
| N2:1335 | words\はしご.md | A, M, P1436480, C梯/階/子, X1604300+回る, D | CLEAN | CLEAN | CLEAN |
| N2:1336 | words\はじめに.md | A, M, P1307520, C始/初, 始め/初め articles (carried over), X1204520+概論; no Daijisen text exists | CLEAN | CLEAN | CLEAN |
| N2:1337 | words\はじめに.md | Same as N2:1336; the raw gloss is blank | CLEAN | CLEAN | CLEAN |
| N2:1338 | words\はじめまして.md | A, M, P1625780, C初/始, D | CLEAN | CLEAN | CLEAN |
| N2:1339 | words\斜.md | A, M, P2085880 (both はす and しゃ), C斜, D | CLEAN | CLEAN | CLEAN |
| N2:1340 | words\外れる.md | A, M, P1203310, C外, D | CLEAN | CLEAN | CLEAN |
| N2:1341 | words\パターン.md | A, M, P1101600, X1075940/1328890/1163170 + タイプ/種類/一種, D | CLEAN | CLEAN | CLEAN |

**Edited kanji cards: CLEAN.**
- 量 and 測: the はか.る row and Common words both link the displayed 量る or 測る to `words\計る.md`, and each footer cites 1600650.
- 掃: the は.く row and Common words link 掃く; the footer cites 1399760.
- 挟: the はさ.まる row and Common words link 挟まる; the footer cites 1236840. The はさ.む link to 挟む and its footer entry 1600740 are kept.
- The correction patch does not touch any kanji card, so the headers are as they were.

**Kanji–word pairs in both directions: CLEAN.**
- 掃く links to 掃 and explains that 掃 writes は before く.
- 挟まる links to 挟 and explains that it writes はさ before まる.
- 計る links to [測] and [量] in sentences that explain when each spelling is used.
- 挟む links to 挟.
- No cards were invented for the kanji without one (吐, 秤, 斜, 剥, 梯); 吐, 秤 and 斜 are still listed in the articles' kanji metadata.

**Existing content preserved: CLEAN.** 計る still has jlpt 3, primary kanji 計, and its original title and body. はきはき only gained jlpt 2. 挟む only gained jlpt 2 and the 挟まる link, and its exclusions are unchanged. The correction changed only the 8 new articles.

**Mappings: CLEAN.** 20 rows map to 18 articles. Two rows share 計る and two share はじめに, and the additional senses match.

## Findings
**My original findings:**

| ID | Status | Evidence | Notes |
|---|---|---|---|
| B67-F01 (吐き気 reading type) | Resolved | `words\吐き気.md`: line 8 adds the `mixed-reading` tag; lines 29–32 say け is an on reading and the word mixes native 吐き with on-reading け | Matches the 気 component record (ケ is an on reading). I accept keeping `type: wago`: 場所.md describes `wago` as covering native-first mixed words, and `content-format.md:63` requires `kango` only for on-first words. I drop my earlier "reconsider wago" suggestion. The Go-on label isn't needed. |
| B67-F02 (挾まる) | Resolved | Sentence deleted (formerly `words\挟まる.md:29`) | JMdict 1236840 lists only 挟まる. Deleting the line doesn't claim the spelling is impossible. |
| B67-F03 (パターン quiz exclusions) | Resolved | `words\パターン.md:9` adds タイプ, 種類 and 一種 | タイプ: high confidence. 種類: medium-high ("type" vs "kind", and the article's own example "several types"). 一種: medium, accepted because its title "a kind; a sort" overlaps パターン's "type" directly, not because 種類 already excludes 一種. |
| B67-F04 (挟まる/挟む) | Resolved | `words\挟まる.md:9` | Exclusions work both ways, so one side is enough; 挟む's existing list is unchanged. |
| B67-F05 (author-facing notes) | Resolved | `words\斜.md:42-43` now explains the はすに横切る phrase; the notes in `words\はじめに.md` are gone | しゃ is no longer called invalid. |
| Optional: はしご transitivity | Resolved | `words\はしご.md:23-24` | Now says both transitive and intransitive uses exist, matching 1436480:3. |
| Optional: はがす wording | Resolved | `words\はがす.md:27` | The irregular-okurigana note for 剥す is kept. |
| Optional: 計.md doesn't link 計る | Deferred, agreed | — | The gap predates this batch, and the card isn't among this batch's kanji edits. |
| Optional: links from 生, 外 and 当たる; 吐き気 collocation; はきはき second sense | Agreed, not needed | — | None of these is a correctness defect. |
| Optional: 掃く/磨く | Withdrawn | Full 磨く.md: "polish; brush teeth", and it says it is "not a general translation for every use of English 'brush'" | 床を磨く (polish or scrub the floor) and 床を掃く (sweep the floor) are different actions. |
| Optional: 容器/コップ | Not a problem | Carried-over glob: コップ.md exists, 容器.md doesn't | バケツ mentions 容器 without a link, so nothing is broken. |

**New quiz exclusions from the other reviewer's findings, judged independently:**
- **はがす/千切る: agree, medium-high.** はがす's dictionary family (1600670) includes "to tear off", as does 千切る's second sense. はがす.md:39 still says peeling need not tear the material.
- **ばからしい/傑作: agree, medium.** ばからしい (1612910) is glossed "absurd; laughable"; 傑作's second sense is "absurd (e.g. blunder)", marked jocular and dated. Neither article suggests the words can replace each other.
- **吐き気/むかむか: agree, high.** むかむか's first sense and title both say "nauseated".
- **はしご/回る: agree, medium.** 回る's article teaches 町の店を回りました ("went around the shops"), which matches its sense of making the rounds (1604300:3).
- **はじめに/概論: agree, high.** Both titles contain "introduction".

**Regressions:** none. Each changed file has one `quiz_exclusions` key, every target exists, and there are no self-references or duplicates. Titles, identities, readings, levels and kanji metadata are unchanged.

**New actionable defects:** none.

## Optional
- `words\はしご.md:30`: "at the source reading はしご" is the one source-related phrase left. Something like "at the reading はしご" would read better for learners.
- `words\斜.md:42-43` slightly repeats the Meaning section. It is accurate, so this is fine as is.
- Outside this batch: the older articles タイプ and 一種 don't exclude each other. A later quiz audit could check that; the exclusions in this batch don't create a requirement for it.

## Limits
- I could not verify the commit, hashes or working-tree cleanliness. The kanji headers being unchanged relies on the original `related.patch` and on the correction patch not touching them.
- I did not read `corrected-review-evidence.json` and read only the first 80 lines of `correction-completed-inspection.json`.
- All captured dictionary text comes from one source, Digital Daijisen via Weblio, read in the original session. The raw 剥す lookup returned 404, and はじめに has no public dictionary text; its row rests on JMdict and the spelling guidance cited in 始め.md. I fetched nothing new.
- Quiz-exclusion checking is bounded. I read the full articles of 14 comparison words or kanji: 払う, タイプ, 始め, 初め and 計 originally; the 8 chunk articles, 場所, 磨く and 気 now. For others I saw titles and exclusions only. I treated 吐き気/酔う ("get motion sick") as a related topic rather than a competing answer.
- This review does not include a full container or cleaning audit, frequency data, live quiz draws or native-speaker certification. The batch-61 quiz backlog is still deferred and was not assessed.
