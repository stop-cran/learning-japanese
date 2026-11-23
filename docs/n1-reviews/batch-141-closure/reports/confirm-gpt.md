Snapshot: 65b47299831240115de12f5c9c5f0f6ed0e2065d, compared with a92d134afd93566ba705b586daf8d7969c683a5f. Reviewer: OpenAI ChatGPT, GPT family; the exact deployed model identifier is not exposed to me.

Scope:

Independent confirmation, read-only except this report. Paths below are relative to the confirmation packet unless explicitly labelled otherwise.

- Read in full: `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`.
- Read every revised article in full: `snapshot\kanji\懐.md`, `snapshot\kanji\懸.md`, `snapshot\kanji\扇.md`, `snapshot\kanji\抽.md`, `snapshot\kanji\張.md`, `snapshot\words\悔しい.md`, `snapshot\words\悔やむ.md`.
- Evidence read in full: `evidence\README.md`, `evidence\jmdict-cited-entries.xml`, `evidence\QuizBuilder.kt`, `evidence\word-remarks.json`, `evidence\kanji-remarks.json`. Read `evidence\KanjiReadings.kt` lines 1–220; relevant symbol matches and lines 210–273 of `evidence\Words.kt`; lines 1–5 of `evidence\meta-scan.txt` (the complete file was loaded programmatically).
- Checks read in full: `checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt`, `checks\link-targets.tsv`, `checks\linkplan.txt`, `checks\kanji-remarks.txt`, `checks\lint.txt`, `checks\unittest.txt`, `checks\validate.txt`.
- Original packet: fully loaded the old `snapshot\kanji\懐.md`, `懸.md`, `扇.md`, `抽.md`, `張.md` and `snapshot\words\悔しい.md`, `悔やむ.md` for exact in-memory patch reconstruction. Loaded the other eleven original kanji files for front-matter inspection: `snapshot\kanji\悔.md`, `悟.md`, `惑.md`, `惜.md`, `愉.md`, `慎.md`, `慮.md`, `慰.md`, `憧.md`, `憩.md`, `拡.md`. Additionally read original 悟 lines 23–27, 惑 lines 49–53 and 慮 lines 51–55 to check Optional 1. Unchanged bodies were not completely re-reviewed this round.
- Original packet: fully parsed `titles\kanji-titles.tsv` for the relevant title and absence checks; parsed `evidence\kanjidic2-records.xml` and inspected 抽's reading record. Byte-read `evidence\app-code\QuizBuilder.kt`, `KanjiReadings.kt`, `Words.kt` for equality with the confirmation copies. Compared the complete original `evidence\audits\quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt` with their revised counterparts.
- Read my own `reports-141\initial-gpt.md` in full. No other review report was opened.

Independent checks reproduced all seven revised files from their original text plus the supplied patch, verified unchanged front matter on all five changed kanji files, verified all nine changed-line links and their quoted titles against actual packet targets/title-index entries, and confirmed that each G1 word revision is exactly its declared sentence deletion. Meaning-audit output is identical; both reading audits are identical after their command lines. All three supplied app-source copies are byte-identical to their originals.

Public sources inspected as actual entries/articles, not merely snippets:

- Digital Daijisen via Weblio: [懐](https://www.weblio.jp/content/懐), [扇](https://www.weblio.jp/content/扇), [懸念](https://www.weblio.jp/content/懸念), [抽斗](https://www.weblio.jp/content/抽斗), relevant headwords and sense sections.
- Kanjipedia: [〈抽斗〉・△抽き出し](https://www.kanjipedia.jp/kotoba/0004740200) and its [notation/readings explanation](https://www.kanjipedia.jp/include/popup_kotoba.html), both in full.
- Shogakukan's [“知ってる？熟字訓『抽斗』の読み方と由来”](https://dime.jp/genre/1284226/), article text, particularly the explicit discussion of 斗 and whole-word readings. Its [LINE republication](https://news.line.me/detail/oa-atdime/00c12720f3e4) was inspected only through initial HTML metadata identifying the canonical article.

Dispositions:

- **G1 — RESOLVED** — The two obsolete availability sentences are gone, the useful explanations and working 悔 links remain, and both exact deletions are declared in `evidence\word-remarks.json`. Independently compared the complete old/new word files; `checks\linkplan.txt` also records two declared remark edits and zero problems.
- **Optional 1 — RESOLVED** — 懐's former single inventory is now four labelled groups, and 扇's on/kun reference material is separated. Live Daijisen supports the new 懐 sense groupings. I accept retaining the other optional passages. The author's correction is fair: 悟:25 is a sense paragraph rather than a separately labelled reference inventory; my earlier wording was imprecise.
- **Optional 2 — DECLINE ACCEPTED** — Keeping explicit mnemonic and practice-selection qualifications is reasonable and protects learners from treating a memory aid as etymology or an unquizzed reading as invalid. Acceptance does not depend on the author's unverified collection-wide occurrence counts.
- **Optional 3 — RESOLVED** — Agreement with the no-expansion recommendation requires no edit. Unchanged metadata and the rerun reading-option evidence establish no new requirement to teach name readings or enumerate the historical extras.

Verdicts:

- **Correctness: NEEDS FIX** — 抽:34–36 introduces G2. No other changed hunk has an established correctness defect.
- **Scoped coverage: CLEAN** — Metadata coverage is preserved; no new necessary omission established.
- **Consistency and quiz safety: CLEAN** — No new unsafe option established for any batch card in the supplied audits. G1's navigation contradiction is resolved. This does not certify every possible reduced/custom pool.
- **Comprehensibility: CLEAN** — The revised grouping improves navigation through the reference material. G2 is a factual reading-attribution error, not merely a preference about wording.

Changed-hunk review:

- **悔しい / 悔やむ:** deletion-only fixes; no surrounding contradiction or new linguistic claim introduced.
- **張:59:** the new 拡 link exists, its quoted title is exact, and the 拡張 decomposition is correct. 緊 remains absent from the title index and the two named original-packet card locations.
- **懐:66–69:** examples and glosses remain in order. The new first/second/fourth カイ classifications match Daijisen's actual numbered lists, including 胸懐 under its fourth list.
- **扇:57–58:** the split preserves the examples and the distinction between おうぎがた, せんけい and whole-word うちわ; no regression established.
- **懸:46,56:** the singular “common word” matches the section. Pinned JMdict entry 1257720 supports the added けんねん variant and the corresponding ケン attribution; its irregular-kana flag motivates the optional qualification below, not another established defect.
- **抽:34,36:** rare/search-only spelling flags and the drawer sense match entry 1601650, and the statement about the pinned KANJIDIC2 reading list is true. The new per-character split of 抽斗 is not: see G2.

Post-fix quiz review covered all forty-five displayed meaning distractors, in both semantic directions, and all sixteen selected reading prompts:

| Card | Reading prompt(s) reviewed | New option defect established |
|---|---|---|
| 悔 | くやむ; くやしい | None |
| 悟 | ゴ | None |
| 惑 | ワク | None |
| 惜 | おしい | None |
| 愉 | ユ | None |
| 慎 | シン | None |
| 慮 | リョ | None |
| 慰 | なぐさめる | None |
| 憧 | あこがれる | None |
| 憩 | ケイ | None |
| 懐 | なつかしい | None |
| 懸 | ケン | None |
| 扇 | セン | None |
| 抽 | チュウ | None |
| 拡 | カク | None |

`QuizBuilder.kt` applies exclusions symmetrically, including between wrong options, without transitive expansion. None of these revisions changes an exclusion, distractor, title or quiz-reading selection. The reading builder excludes all metadata readings of both kinds plus generated sound variants, then uses curated readings before closeness-ranked fallback.

The four full-pool fallback cases remain 慮／リョ, 慰／なぐさめる, 憧／あこがれる and 懐／なつかしい; their listed reachable alternatives establish no additional valid answer. The exposure audit still reports zero production/padded non-name hits and five latent collisions, not five shipped wrong-answer defects. 愉's name-only ゆう is not an ordinary on/kun answer. G2 affects an unquizzed explanation, so these audit results do not detect or excuse it.

Confirmation: **NEEDS FIX** — All four response items are accepted/resolved, but the revision introduces G2.

Findings:

**G2 — Minor; correctness; `snapshot\kanji\抽.md:34–36` (explicit false attribution at line 36).**

The revision now says: “In 抽斗, 抽 writes ひき and 斗 writes だし,” and uses that compound as the ひき- row's example. This incorrectly turns a special whole-word reading into a regular character-by-character explanation.

Kanjipedia marks **〈抽斗〉** as a special whole-word spelling, while marking the transparent **△抽き出し** differently. Its notation guide explains that these readings are not obtained by reading each character through its individual on/kun. Shogakukan's inspected article explicitly states that **斗 cannot be read だし** and identifies 抽斗 as 熟字訓, read as a unit.

The packet's JMdict entry proves that the rare spelling 抽斗 is read ひきだし and means “drawer”; it provides no per-character alignment. KANJIDIC2's independent listing of ひき- for 抽 does not justify inventing a だし reading for 斗 in this explanation.

**Impact:** a beginner is taught a false decomposition in a section specifically explaining which sounds each kanji supplies. This is newly introduced by the revision, not a re-raised initial point.

**Remedy:** retain 抽斗 as a rare whole-word spelling read ひきだし, explicitly without the proposed character split. Illustrate ひき- separately with a transparent spelling and its existing rarity/search-only qualification, or qualify the metadata reading as lacking a verified ordinary example here. Do not remove the sourced metadata reading merely because this example is unsuitable.

**Evidence:** revised lines 34–36 and `diffs\fix.patch`; entry 1601650 in `evidence\jmdict-cited-entries.xml`; the inspected Kanjipedia entry/notation guide and Shogakukan article linked in Scope.

**Confidence:** high.

Optional:

- At 懸:46, consider adding “marked irregular kana in JMdict” after けんねん. The current source-attributed statement is true, but that small qualification would better distinguish it from the standard けねん already used in the reading table.

Limits:

- Exact model/version is unavailable. I did not consult another reviewer, other packets, checkouts, sessions or unprovided author material.
- The packet supplies the snapshot identities and complete-diff claim. I verified patch-to-snapshot consistency, not Git objects or the entire repository tree. The author's global stale-availability scan and collection-wide convention counts cannot be independently confirmed without prohibited corpus scans; neither is needed for the dispositions.
- This is a changed-hunk confirmation with full reads of the seven revised articles, not a fresh full-body review of all unchanged cards or stroke geometry.
- The meaning audit shows the supplied full-pool options, not all fallback choices for arbitrary reduced pools. Reading audits model the stated N1/All, Starter and one-holder borrowing cases against a finite metadata/dictionary/extra-reading inventory. They cannot prove that every possible historical/name reading has been found, validate prose-level character alignment, or certify every future/custom pool.
- Seed sampling alone is not exhaustive. I inspected the audit's candidate/reachability explanations and Kotlin option-building code, but did not independently execute the Python ports or JVM app tests. The supplied 436-test “OK” and validation/lint outputs are recorded evidence, not tests I reran.
- No on-device rendering or learner testing was performed. Public dictionary checks targeted revised consequential claims; unchanged rare examples retain the first-round review's verification limits.
- One oversized web return exceeded the tool display limit; I used bounded follow-up extracts and did not open its generated temporary file. All tool calls were serial, one per tool-using response; no agents, background jobs, recursive listings or corpus scans were used. Only this designated report was intentionally written.
