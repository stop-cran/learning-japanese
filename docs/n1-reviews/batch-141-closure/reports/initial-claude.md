# Batch 141 initial review — Claude

## Snapshot

- Commit: a92d134afd93566ba705b586daf8d7969c683a5f (batch 141).
- New kanji cards: 悔 悟 惑 惜 愉 慎 慮 慰 憧 憩 懐 懸 扇 抽 拡.
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-141-a92d134a`. I did not recompute the sha256 of `packet-manifest.json`; I took the packet as delivered.
- Reviewer: Claude (Anthropic model family), first of two blind reviewers. The review was read-only. The only file written is this report.

## Scope

Packet files opened (all read-only):

- `INSTRUCTIONS.md`: full.
- `mechanical-checks.md`: full.
- `evidence\source-metadata.json`: full.
- `evidence\joyo-pages.md`: full, read in ranges.
- `evidence\public-source\weblio-*.txt`, all 15: full. I later re-searched `weblio-慎.txt` (for 愼 and つつし) and `weblio-抽.txt` (for 抽斗 and ひき).
- `evidence\jmdict-digest.tsv`: in part (lines 1-60, plus a filter on priority tags across the whole file).
- `evidence\jmdict-families.xml`: in part. I extracted these entries by id or headword:
  - 悔: 1664840, 1585740, 2856283, 1200450, 1592350, 2853797.
  - 惜: 1382300, 1382280, 1577210, 2032380, 1697220, 1645830, 1687620, 1531540, plus the file head (1010130, 1150290, 1150880).
  - 悟 and 惑: 悟る, 悟り, 戸惑う, 惑う, 惑わす, both 思惑 entries, 惑, 惑星, 惑い, 眩惑, 蠱惑, 惑乱, 悟道, 大悟, 頓悟, 覚悟.
  - 愉 and 慎: 楽しい, 楽しむ, 楽しみ (their 愉 forms), 愉悦, 愉楽, 愉快, 慎ましい, 慎む, 慎み, 謹慎, 戒慎.
  - 慮, 慰, 憧 and 憩: 慮る, 慮り, 遠慮, 無慮, 顧慮, 叡慮, 慰む, 慰め, 慰み, 弔慰, 慰撫, 憧れる, 憧憬, 憩い, 憩う, 小憩, 休憩.
  - 懐: 懐, all three 懐く entries, 懐ける, 手懐ける, 懐う, 懐中, 述懐, 懐手, 内懐, 懐炉, 坦懐, 懐かしい, 懐かしむ, 所懐, 素懐, 感懐, 胸懐.
  - 懸: 一生懸命, 一所懸命, 掛ける (truncated), 掛かる, 命懸け, 懸想, 懸隔, 懸垂, 懸崖, 懸絶, 筧, 鈴懸, 架ける, 架かる, 賭ける.
  - 抽, 扇 and 拡: 引き出し, 抜きん出る, 抽選, 抽出, 抽象, 扇, 扇ぐ, 扇形, 扇子, 扇風機, 扇動, 扇情, 広がる, 広げる, 広める, 拡張, 拡充, 拡散.
- `evidence\kanjidic2-records.xml`: full. I parsed it for readings, name readings (nanori), meanings and stroke counts.
- `evidence\audits\quiz-safety.txt`: full.
- `evidence\audits\reading-exposure.txt`: in part (every "attested" line and the last 12 lines).
- `evidence\audits\kanji-remarks.json` and `evidence\audits\word-remarks.json`: full.
- `evidence\app-code\`: a search of all four files for exclusion and fallback logic. I read lines 26 and 177/199 of `QuizBuilder.kt` and `Words.kt`.
- `diffs\`: all 22 diffs. The 張 diff was read in full; for the 21 word diffs I read every changed line.
- `snapshot\kanji\`: all 15 new cards in full. Some cards I opened twice, the second time from line 17 onward.
- `snapshot\kanji\張.md`: only through its diff hunk (lines 56-62).
- `snapshot\words\`: all 21 files.
  - I searched all 21 for "card", "collection" and "currently".
  - I read the context around the changed line (2 lines before, 5 after) in 悔しい, 悔やむ, 慰める, 憧れる, 懐かしい, 扇ぐ, 扇子, 扇風機, 抽象, 迷惑, 考慮 and 拡大.
  - For the other 9 articles I relied on the full changed line in the diff.
- `snapshot\strokes\*.json`, all 15: parsed for keys and stroke count. I did not inspect the paths visually.
- `titles\kanji-titles.tsv`: header, every cited title (about 180 lookups) and a uniqueness check of the 15 new titles.
- Directory listings, one folder at a time with no recursion: the packet root, `evidence`, `diffs`, `evidence\public-source`, `evidence\audits`, `evidence\app-code`, `rubric`, `titles`, `snapshot`, `snapshot\words` and `snapshot\strokes`.

Not opened:
- `evidence\daijisen-heads.txt`, `evidence\kanjipedia-outside-readings.json`, `evidence\okurigana-scan.txt` and `evidence\provenance.json`.
- `evidence\audits\reading-options.txt` and `evidence\audits\kanji_remarks.py`.
- `titles\word-titles.tsv`.
- `repo\docs\content-format.md`, `repo\docs\confusable-words.md` and the rubric files.
- Every other `repo\` file.

Public web: one fetch of the jisho.org kanji page for 抽 (KANJIDIC2 data: kun reading ひき-, meanings "pluck, pull, extract, excel").

## Verdicts

Overall:

| Facet | Verdict |
| --- | --- |
| 1. Correctness | Defect: C1 (two word articles) and C2 (抽). All 15 kanji cards are otherwise correct as far as I could verify. |
| 2. Scoped coverage | Clean |
| 3. Consistency and quiz safety | Clean for the cards. C1 also creates a contradiction inside two word articles. |
| 4. Comprehensibility | Clean, except C2 (抽 ひき- explanation) and the C1 contradiction. |

Per card or file, where it differs from clean:

- **悔しい.md and 悔やむ.md (word diffs):** facets 1 and 3 have a defect (C1).
- **抽:** facets 1 and 4 have a minor defect (C2).
- **All other cards and diffs are clean on all four facets:** 悔 悟 惑 惜 愉 慎 慮 慰 憧 憩 懐 懸 扇 拡, the other 19 word diffs and the 張 remark edit.

### What I verified

**Front matter**
- Grade, strokes, radical and number, on and kun lists match `source-metadata.json` and the KANJIDIC2 records for all 15 cards.
- 拡 is grade 6; the other 14 are grade 8.
- 扇 uses radical 戶 (no. 63). 抽 and 拡 use 手 (no. 64). The rest use 心 (no. 61).
- Every quizOnyomi and quizKunyomi reading has a linked word article.
- All 15 stroke files have the expected keys, and their stroke counts equal the card counts: 9, 10, 12, 11, 12, 13, 15, 15, 15, 16, 16, 20, 10, 8 and 8.

**Joyo table claims**
- Every reading row, example, bracketed form and ⇔ contrast the cards cite matches `joyo-pages.md`:
  - 悔: the bracketed variant.
  - 慎 and 懐: 愼 and 懷.
  - 拡: 擴.
  - 憧: the ドウケイ remark.
  - 懸: the contrasts 掛ける/架ける/賭ける and 掛かる/架かる.
  - 慎: the contrast 謹む.
- The "not in the table" statements are correct for:
  - 懐: エ, なず.ける, いだ.く, おも.う.
  - 拡: コウ and the three kun readings.
  - 抽: ひき-.
  - 憧: no separate rows for トウ and ドウ.
  - 慎: つつ.ましい and つつし.

**Daijisen claims**
- Each card's account matches the weblio extract:
  - Number of senses, examples and kun lists.
  - 悔: ケ in 懺悔.
  - 惜: シャク with 不惜身命, and 可惜 listed as hard to read (難読).
  - 慎: 愼 in brackets.
  - 憩: 憇 as a popular variant (俗字), and 憩息 as the compound absent from JMdict.
  - 懐: the ほほ entry.
  - 懸: ケ as a customary reading (慣), and 懸樋 and 鈴懸 as hard to read.
  - 扇: あおぐ and あおる; 煽 can replace 扇 in the incite sense.
  - 抽: ぬきんでる and ぬく; 抽斗 as hard to read.
  - 拡: marked as a grade-6 school kanji.

**JMdict claims**
Every tag and gloss I checked matches the pinned entries:
- 悔 and 惜:
  - 悔悛 is listed after 改悛.
  - 懺悔: Christianity and Buddhism field tags, plus the さんげ note.
  - お悔やみ is polite.
  - 口惜しい is a rare form of 悔しい, and くちおしい is dated.
  - 可惜 is usually written in kana, reads あったら and has the form 惜.
  - 愛惜 also reads あいじゃく.
  - 不惜身命 is a Buddhist yojijukugo.
- 悟 and 惑:
  - 覚る and 覚り are rare forms.
  - 大悟 also reads だいご.
  - 思惑 is ateji, and しわく is a Buddhist term.
  - 惑 わく is "klesha".
  - 途惑う is a rare form.
- 愉 and 慎:
  - 愉しい, 愉しむ and 愉しみ are rare forms.
  - 慎ましい is usually written in kana.
  - 慎しみ uses irregular okurigana.
  - 謹む sits in the 慎む entry, and "to be reverent" is restricted to 謹む.
- 慮 and 慰:
  - 慮る lists おもんばかる first; 慮り lists おもんぱかり first.
  - 遠慮's last sense is marked "orig. meaning".
  - 弔慰 is formal or literary.
  - 慰む has the sense "to trifle with".
- 憧 and 憩:
  - 憬れる is a rare form and 憧憬れる is search-only; 憧憬 lists どうけい first.
  - 憩 is listed alone as a form of 憩い, and 息う is a rare form.
  - 休けい is search-only, and 小憩 is listed before 少憩.
- 懐:
  - 懐く なつく is usually written in kana; 懐く いだく is formal or literary, with 抱く listed first.
  - 手なずける is listed first.
  - 懐う is search-only.
- 懸:
  - 一所懸命's second sense is a historical term.
  - 掛ける senses are usually written in kana.
  - 懸かる is a rare form of 掛かる.
  - 命がけ is listed first.
  - 筧 is listed first for 懸樋.
  - 鈴懸 is usually written in kana, with 篠懸 a rare form.
- 扇, 抽 and 拡:
  - 扇ぐ has the second sense "to incite" and the form 煽ぐ.
  - おおぎ is irregular kana.
  - In 扇形, "sector" is restricted to せんけい.
  - 抽き出し and 抽斗 are rare forms; 抽出し is search-only.
  - 抽んでる is a rare form, and 抽籤 is a rare form.
  - 拡がる and 拡げる carry no tag.
  - There is no 拡める; 広める and 弘める exist.
  - 拡張 has the computing sense "escape; ESC".

**Titles cited in prose**
- About 70 cited titles of other cards are exact, including:
  - Shape and component titles: 梅 毎 慣 海, 五 口 語, 或-free 域, 昔 借 籍, 兪-free 輸, 真, 虎 劇 膚, 寸 封, 童, 舌-free 話 活 自 息 鼻, 十 衣 壊, 県 系 恩 忘, 戸 羽 房 肩 雇, 由 宙 油 押 届, 広 払 拝 底.
  - Exclusion-target titles.
  - Titles of the other kanji in each word: 覚 迷 快 重 考 遠 休 子 風 機 一 生 命 象 充 大 張 不.
- The kanji that cards say have no card really have none: 舌, 兪, 或, 謹, 憬, 懺, 煽, 吾 and 緊.
- The 15 new titles are each unique in `kanji-titles.tsv`.

**Mnemonics**
- All 15 are labelled "Modern-shape mnemonic, not etymology" and disclaim historical formation.
- Every component placement and stroke sum is true: 忄3+毎6, 忄3+五4+口3, 或8+心4, 忄3+昔8, 忄3+兪9, 忄3+真10, 虍6+思9, 尉11+心4, 忄3+童12, 舌6+自6+心4, 忄3+十2+罒5+衣6, 県9+系7+心4, 戸4+羽6, 扌3+由5 and 扌3+広5.
- The reading side-notes are true: 五 ゴ, 真 シン, 昔 セキ, 童 ドウ, 宙 チュウ, 県 ケン/か.ける, 壊 カイ/エ, and 広 has the kun readings that 拡 lists.

**Quiz safety**
- `quiz-safety.txt` reports 0 errors and 0 warnings.
- Exclusions apply in both directions (`QuizBuilder.excluded`), so 休, which is filled from fallback options, cannot draw 憩.

### The brief's leads (a)–(l)

- **(a) 懐:** No defect.
  - カイ and エ are handled correctly; エ is source-only and the parallel with 壊 is true.
  - ふところ and its seven Daijisen senses, なつかしむ, なつく (usually kana), なつける, なずける (via 手懐ける), いだく (formal or literary, 抱く first), おもう (search-only 懐う) and ほほ (archaic Daijisen entry, not KANJIDIC2) are all accurate.
  - The title is supported by the KANJIDIC2 meanings "bosom; become attached to" and by なつかしい.
  - うだく (archaic), なずく and なづく (obsolete kana for なつく), ゆかしい and the name reading かね need no account. かね is a latent collision with 金 that no quiz pool can draw.
- **(b) 憧:** No defect.
  - ショウ (漢) and ドウ (慣) match Daijisen; トウ is correctly labelled source-only.
  - 憧憬 has both readings, with JMdict's order どうけい then しょうけい stated correctly.
  - The older form あくがれる needs no account.
  - The title "long for; yearn; admire" is a verb phrase. It cannot reasonably be confused with 久 "a long time" or 長 "long, chief".
- **(c) 懸:** No defect.
  - ケ (慣) with 懸念 and 懸想 matches the Joyo table and Daijisen.
  - かける and かかる beside 掛ける and 掛かる (rare form) are stated accurately.
  - The 一生懸命 sound changes, and がけ by rendaku in 命懸け, are correct.
  - へだたる and かかり need no account; the "far apart" sense is covered by 懸隔.
- **(d) 慮:** No defect. Both KANJIDIC2 kun spellings are treated correctly (おもんぱく.る as source-only), the ば/ぱ variants follow JMdict's order, and the name reading ぜ needs no account.
- **(e) 慎:** No defect.
  - Each kun reading is accurate: つつし is an honest source-only stem, and the つつ + ましい split is correct.
  - 謹む is in the same entry, with "to be reverent" restricted to it.
  - つつましやか, つつむ, つつみ and the four name readings need no account. みつ is a latent collision with 密 that no quiz pool can draw.
- **(f) 悔 and 惜:** No defect.
  - 悔: カイ with 後悔, くいる with 悔い, and ケ in 懺悔 are all accurate. The card says both readings of 懺悔 voice ケ to げ, which is true. The audit's け test is the latent collision with 毛, not drawable.
  - 惜: セキ, おしむ (all five senses quoted correctly), シャク, あたら and あったら are all accurate.
- **(g) 扇:** No defect.
  - おうぎ and おおぎ (irregular kana) are handled correctly.
  - 扇ぐ is honestly described as supporting no KANJIDIC2 reading.
  - あおる is attributed to Daijisen; 扇子 (子 read ス) and 扇風機 (ふう → ぷう after ん) are right.
  - おだてる needs no account.
  - "incite" is supported by 扇動, 扇情 and 扇ぐ's second sense.
- **(h) 抽 and 拡:**
  - 抽: see C2. ぬく and ぬきんでる are accurate; ひく and ちゅうだい need no account.
  - 拡: コウ is source-only. The three kun readings are accurately described against the Joyo table (absent) and JMdict (広がる and 広げる are the headwords; there is no 拡める).
- **(i) Other unquizzed readings:** Each is presented accurately and marked "not selected for questions": 悟 さと.る and さとり, 惑 まど.う, 愉 たの.しい and たの.しむ (rare forms of 楽しい and 楽しむ), 慰 イ and なぐさ.む, 憩 いこ.い and いこ.う. 愉's name reading ゆう needs no account.
- **(j) quiz_exclusions:** Each pair has a stated real overlap, such as a shared compound or a JMdict gloss. Some are generous (慎–議 rests on the shared English word "deliberate"; 懐–心; 憧–偉). Generosity only removes options and creates no quiz risk, so I report no defect.
- **(k) Distractors:**
  - All are visual look-alikes that share a component, and none overlaps the target title in meaning in either direction.
  - 悟's distractor 口 is a component rather than a whole look-alike, but it is plausible and unambiguous.
  - 惜's distractors 憎 "hate; detest" and 慣 do not overlap "begrudge". 恨, "resent; grudge", is the closer meaning and is excluded.
- **(l) Reading audits:** The 5 latent collisions (悔 け/毛 twice, 慎 みつ/密, 懐 かね/金, 扇 おう/凹…) cannot be drawn in the N1 stack, the All stack or a Starter practice session. The four prompts with 2 of 3 curated distractors (慮, 慰, 憧, 懐) are filled by fallback options, and no hit is reported. No defect.

## Findings

### C1: two word articles still say there is no 悔 card, beside the new link to it

- **Severity:** Established defect, moderate.
- **Facets:** 1 and 3.
- **Where:** `snapshot\words\悔しい.md:25` and `snapshot\words\悔やむ.md:28` (diffs `words__悔しい.md.diff` and `words__悔やむ.md.diff`).
- **Claim:** Each line now begins with `[悔](../kanji/悔.md)`. The unchanged rest of the same line still says:
  - 悔しい: "There is no 悔 card in the current collection."
  - 悔やむ: "No 悔 kanji card is currently available."
- **Impact:**
  - In this snapshot those sentences are false.
  - They contradict the link right next to them.
  - Learners will be confused.
  - This breaks the brief's requirement that each remaining sentence is true and the passage still reads correctly.
- **Why the checks missed it:** "link plan verify" checks only the link-wrap, and the batch declares no word remarks (`word-remarks.json` = `[]`). So nothing checked the stale sentence.
- **Remedy:**
  - Delete those two sentences, or replace them with something like "Its kanji card covers the other readings."
  - Declare both as remark edits in `word-remarks.json`, as was done for the 張 remark.
  - I searched all 21 changed articles for "card", "collection" and "currently". No other article has a stale "no card" statement.
- **Evidence:** The diff lines and the snapshot lines quoted above. `titles\kanji-titles.tsv` now lists 悔.
- **Confidence:** High.

### C2: 抽's ひき- row is illustrated with a word where 抽 writes only ひ

- **Severity:** Established, minor.
- **Facets:** 1 and 4.
- **Where:** `snapshot\kanji\抽.md`: the Readings table row ひき- (line 32) and the paragraph below it (line 35).
- **Claim:**
  - The row for the KANJIDIC2 prefix reading ひき- gives 抽き出し as its example.
  - The paragraph then says "In 抽き出し, 抽 writes ひ, き is okurigana."
  - With that segmentation, 抽き出し illustrates ひ(く), not ひき-. So the row does not show its own reading, and the explanation contradicts the row label.
  - The forms in which 抽 itself stands for ひき are 抽斗 (抽 = ひき, 斗 = だし) and 抽出し (抽 = ひき, 出し = だし). Both are in the same JMdict entry, 1601650 (抽斗 is a rare form, 抽出し is search-only), and Daijisen lists 抽斗 ひきだし as hard to read.
  - The card mentions both forms only as side notes.
- **Impact:** A learner is told the reading is ひき- and then shown a segmentation in which 抽 is ひ. That is confusing, and it misrepresents what the ひき- entry means.
- **Remedy:** Use 抽斗 ひきだし as the row's example and say "抽 writes ひき, 斗 writes だし". Alternatively, keep 抽き出し but explain that ひき- is the reading used when 抽 stands for ひき, as in 抽出し and 抽斗.
- **Evidence:**
  - JMdict 1601650 (forms 引き出し, 引出し, 抽き出し [rarely used], 抽斗 [rarely used], 抽出し [search-only], 抽匣 [search-only]).
  - `weblio-抽.txt` line 6 ("［難読］抽斗 (ひきだし)").
  - KANJIDIC2 抽: チュウ, ひき-.
  - jisho.org 抽.
- **Confidence:** Medium-high.

## Optional

- **O1. 張.md Notes, first bullet.** The edited sentence "緊 in 緊張 does not have a kanji card yet." is true (緊 has no title row). The bullet could now also name [拡](拡.md), "expand; enlarge; widen," as the other kanji in 拡張, alongside 主, 出 and 威. This is polish, not required.
- **O2. 悔.** JMdict 悔過 けか (2865883) shows ケ unvoiced. It could illustrate ケ more directly than 懺悔, where ケ is always voiced to げ. Optional.
- **O3. 懸 Notes, first bullet.** It says "the common words" (plural), but the section lists only 一生懸命. 抽, 慎 and others use the singular "the common word". This is wording only.
- **O4. 慎.** つつましやか, the adjectival form of 慎ましい, and 要慎 (a form of 用心) are omitted. That is acceptable under scoped coverage; mention only if wanted.
- **O5. 懸念.** The digest records that it also reads けんねん. The card gives only けねん, which is the standard reading; a short mention is optional.

## Limits

- **Tool-call discipline:** I made exactly one tool call per response and no parallel calls. Several PowerShell commands combined multiple reads of packet files into one call.
- **Temp file:** One PowerShell output was too large and was automatically saved by the tool runtime to a temp file outside the packet. I did not open that file; I re-read the cards with `view` instead.
- **Files I did not open:** `daijisen-heads.txt`, `kanjipedia-outside-readings.json`, `okurigana-scan.txt`, `reading-options.txt`, `kanji_remarks.py`, `word-titles.tsv` and `repo\docs\content-format.md`.
  - Section order and headings were judged against the uniform structure of the 15 cards and against the clean lint and validate results in `mechanical-checks.md`, not against the format document directly.
  - Daijisen claims were checked against `public-source\weblio-*.txt`, not `daijisen-heads.txt`.
- **Partially read word articles:** I read 9 of the 21 only through the changed line in the diff (休憩, 愉快, 慎重, 惜しい, 一生懸命, 覚悟, 遠慮, 拡充, 拡張). Each change there is a link-wrap of a complete sentence whose wording I checked.
- **JMdict sources:** I relied on the pinned JMdict extract in the packet. The only live public check was jisho.org for 抽. Glosses quoted from entries I did not extract (for example 拡大 1205200 and 憂慮) were taken as consistent with the digest. The 掛ける entry was truncated in my output after about 15 senses, but the cited senses were visible.
- **Stroke files:** I checked only the stroke counts and keys, not the stroke order or shapes.
- **Known packet limits, not findings:** The Android JVM tests and the Kotlin cross-check were not run, and the budget byte count varies slightly between runs.
- **Assumption for C1:** I assume the stale "no 悔 card" sentences fall within the "remaining sentence is true" check that the brief puts in scope, even though the 悔 cards themselves are new.
