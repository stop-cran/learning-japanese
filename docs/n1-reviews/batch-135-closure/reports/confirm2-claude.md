# Batch 135 — confirmation round 2 (Claude)

**Snapshot:** commit fb236071b6355b28423581c96a35a8ca1084a193. Reviewer: Claude (Anthropic), working alone and read-only. I did not see any other reviewer's report or any author material outside the packet.

**Scope:** files opened and how deeply. Paths are under `review-packets\`.

- **Packet `confirm2-135-claude\`**
  - Read in full: `INSTRUCTIONS.md`, `RESPONSE.md` and `diffs\fix.patch` (90 lines).
  - Not opened: `CHANGES.md`. `fix.patch` and `diffs\changed-lines.txt` gave me every changed line directly.
  - Read in full: `diffs\changed-lines.txt`.
  - Read in full: the four changed cards `snapshot\kanji\彫.md`, `巡.md`, `履.md` and `救.md`. I had read 巡 earlier in this session at 2ef25d33, and the patch shows its three changed lines.
  - `evidence\`:
    - Read in full: `README.md`, `daijisen-彫る.txt` and `jmdict-cited-entries.xml`.
    - `kanjivg\05468.svg` (周), `05186.svg` (円) and `09ad8.svg` (高): component groups only.
    - Not opened: `joyo\p110.txt`.
  - `checks\`:
    - Read in full: `quiz-safety.txt` (all 15 cards' meaning lines and the 0-error summary), `link-targets.tsv`, `lint.txt`, `unittest.txt`, `validate.txt`, `manifest.txt` and `vocabulary.txt`.
    - `reading-exposure.txt`: read in part. Lines 1–4, 125–215 (the 巡, 弾 and 彫 blocks) and 394–401 (the summary).
    - `reading-options.txt`: read in part. A grep of every card header, every HIT line, every simulation line and the problem count, which covers all 15 cards.
  - Listed (non-recursive): the packet root, `diffs`, `evidence`, `checks`, `evidence\joyo` and `evidence\kanjivg`.
- **Original packet:** `rubric\copilot-instructions.md`, grep only.
- **Earlier packets and my earlier reports:** facts carried over from this session's earlier rounds, not reopened.
- **Public web:** the jisho.org entry for 彫る (JMdict 1427950).

**Dispositions:**

- **CO1 – RESOLVED.** 巡's distractors are now `[川, 道, 見]` (`巡.md:13`).
  - Kun prompt めぐる: the wrong options are かわ, みち and one of みる, みえる or みせる. That is 3 outcomes and 5 drawable options, all from curated cards. The fallback is never used in the N1 stack, the All stack or the Starter session (`reading-exposure.txt` 144–152).
  - The options can no longer be told apart by shape alone, and none of the three verbs is a reading of 巡.
  - The ジュン prompt offers セン, ドウ or トウ, and ケン (4 options).
  - The meaning options "river | road, way | see, look" are all clearly wrong for "go around; patrol; tour".
  - `巡.md:49` honestly says 見 is not a look-alike. The quoted titles match exactly (`link-targets.tsv`).
  - The author's reason for not choosing a look-alike holds: it must be a starter card that fills every Starter slot. I accept it.
- **CO2 – RESOLVED.** `履.md:36` now reads "the voiced form of サウ, which is the historical spelling of ソウ, the on reading of 草".
  - The clause is now unambiguous.
  - It matches the Daijisen extracts I verified last round: 草 is ソウ（サウ）, and 草履 is ぞう‐り〔ザウ‐〕.
  - The rest of the line is unchanged.
- **CO3 – RESOLVED.** Both sentences now state facts about the three cards named as distractors, not about what the quiz will output. Both facts are true:
  - `救.md:49`: 敬 is ケイ, キョウ or うやまう; 球 is キュウ or たま; 教 is キョウ, おしえる or おそわる. None of them is グ, ク or たすける.
  - `巡.md:37`: 川, 道 and 見 have no reading まわる.
  - The new 彫 paragraph (`彫.md:41`) follows the same pattern, and its fact is also true: 円, 高 and 見 have no reading える or えり.

**Verdicts:**

- **Correctness: CLEAN.** I verified the new 彫 paragraph and Notes bullet against the Daijisen extract, JMdict 2265620, live JMdict 1427950 and KanjiVG. The 履, 巡 and 救 hunks are true.
- **Scoped coverage: CLEAN.** 彫 now covers える and えり as readings outside KANJIDIC2 and outside the official table. Its metadata is unchanged.
- **Consistency and quiz safety: CLEAN.** Details:
  - All 15 cards have three distinct, defensibly wrong meaning options (`quiz-safety.txt`: 0 errors, 0 warnings).
  - No new distractor is also an exclusion.
  - `link-targets.tsv` shows 9 of 9 links resolve, with exact titles.
  - `reading-exposure.txt` shows 0 production hits, 0 padded-session hits and 0 one-holder padded hits. It also shows 26 latent collisions, which no pool can draw.
  - The only `reading-options.txt` problem is the 巡 まわる superset HIT, which `reading-exposure` shows cannot be drawn.
- **Comprehensibility: CLEAN.**

**Confirmation:** CONFIRMED. CO1, CO2 and CO3 are all RESOLVED, and I found no new actionable defect in the changed hunks or in the post-fix quiz options for any of the 15 cards.

**Findings:** none.

These are the hunks I checked for new defects, with the evidence for each:

- **`彫.md:13`: distractors `[円, 高, 見]`.**
  - Meaning options are "yen, circle | high, expensive | see, look". None is a correct answer for "carve; engrave; sculpt", and none appears in the exclusions `[刻, 削, 像]`.
  - Reading prompt チョウ: エン, コウ and ケン, all curated in every pool.
  - Reading prompt ほる: 13 curated options. 円 gives まるい, まる, まど, まどか or まろやか; 高 gives たかい, たか, -だか, たかまる or たかめる; 見 gives みる, みえる or みせる.
  - Old exposure fixed: える (from 得 or 選) and えり (from 領) can no longer be drawn in any pool or with any single borrowed holder card (`reading-exposure.txt` 190–211). The comparison audit at 2ef25d33 showed that the Starter session could reach them before this change.
- **`彫.md:41`: the える and えり paragraph.**
  - The Daijisen headword え・る〔ゑる〕【▽彫る】 has first sense 彫刻する。ほりつける (`daijisen-彫る.txt`), so the English "to carve; to engrave" is a fair rendering.
  - Daijisen's ▽ mark does mean a reading the official table does not list.
  - JMdict 2265620 has 彫り and 彫, read ほり, and えり marked "out-dated or obsolete kana usage", with the glosses "carving; engraving". The card's quote is exact.
  - KANJIDIC2 lists ほ.る and -ぼ.り only (card metadata), so "outside both KANJIDIC2 and the official table" is true.
- **`彫.md:52`: the new Notes bullet.**
  - KanjiVG confirms the components:
    - 周 has a 冂 frame (marked as a variant form) holding 吉, which is 士 over 口.
    - 円 has 冂.
    - 高 has 冋, which is 冂 with 口 inside, at the bottom.
  - The kun readings of 見 (み.る, み.える, み.せる) do all end in る.
  - The quoted titles are exact.
- **`彫.md:55`:** JMdict 2265620 is added, and the Daijisen 彫る link is added.
- **`巡.md:13`, `:37` and `:49`, `履.md:36`, `救.md:49`:** checked under the dispositions above. None of these hunks contradicts unchanged text in the same card:
  - 巡 keeps 達 as a look-alike in its Notes.
  - 彫 keeps 周, 影 and 掘 in its look-alike bullet, and its mnemonic still uses 周 correctly.

**Optional:**

1. **彫 line 41 could also cite JMdict's own entry for 彫る (1427950).** That entry is already cited in the card's metadata. Live JMdict (via jisho.org) lists える as an "out-dated or obsolete kana usage" reading of 彫る, with sense 1 "to carve; to engrave; to sculpt; to chisel". The card's quoted "to carve; to engrave" is therefore also a real JMdict gloss.
   - The paragraph could say that JMdict, like Daijisen, records える for 彫る, not only えり for 彫り.
   - The current text is not wrong.
   - I checked this against today's online JMdict, not the pinned file, so the pinned file may differ slightly.
2. **One ほる option is a suffix with a visible dash.** One of the 13 possible ほる options is "-だか" (from 高's -だか). Like "-たち" in the previous round, the dash gives it away as a suffix. It is only one possible option, the other two slots are verb- or noun-shaped, and this is not a defect.

**Limits:**

- **Audits are not the app.** The audits are Python ports of the Kotlin quiz code. The JVM tests and the Kotlin cross-check of the reading audit were not run for this revision. My conclusions about which options can be drawn come from the audit output and from reading `KanjiReadings.kt` and `QuizBuilder.kt` in the earlier rounds. I did not re-read the app sources in this packet; `README.md` says they are the same builders.
- **Partial reads.** I read only the 巡, 弾 and 彫 blocks and the summary of `reading-exposure.txt`. For the other twelve cards I relied on the summary lines, which show 0 hits, and on the 0 problems besides 巡 reported in `reading-options.txt`. Per `evidence\README.md`, only the 巡 and 彫 blocks changed since 2ef25d33.
- **Other files not opened.** I did not open `joyo\p110.txt` (彫's Joyo row) or the `reading-exposure-2ef25d33.txt` comparison file. The 彫 Joyo row, チョウ and ほる, is unchanged text that I reviewed in round 1.
- **Other Daijisen ▽ headwords.** I did not search Daijisen for ▽ headwords of the other 14 kanji. The author states the same gap.
- **Execution rules.** I made exactly one tool call in every response this round. I did not notice any parallel calls.
