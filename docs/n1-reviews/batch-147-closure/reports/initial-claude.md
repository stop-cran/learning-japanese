# Batch 147 — initial blind review (reviewer 1)

Reviewer model: Claude, an Anthropic model (the exact version string is not exposed to me). I worked alone and read-only, with one tool call per response.

## Snapshot

- Commit `6a2323e759d4e4f2e78bc039c8b9eb8914ac2d0c`, batch 147.
- New kanji cards: 瞬 瞳 矢 砕 礎 秀 秘 稚 稼 稿 穏 穴 笛 粋 糧.
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-147-6a2323e7`, packet-manifest sha256 `39afd4115e2e68d2a09419c16590cdab000fb8351e08f68337903067b660952c` (as given in the request; I did not recompute it).

## Scope

The unit under review:
- the 15 new cards in `snapshot\kanji\`;
- the 15 files in `snapshot\strokes\`;
- the 18 word diffs and the changed lines of `kanji\基.md`, `kanji\密.md` and `kanji\透.md` (21 diffs in total).

Packet files I opened:

| File | How far |
| --- | --- |
| `INSTRUCTIONS.md` | full |
| `mechanical-checks.md` | full |
| `evidence\source-metadata.json` | full (one record, 稚, was re-extracted later) |
| `evidence\kanjidic2-records.xml` | full, by parsing it with PowerShell |
| `evidence\kanjipedia-outside-readings.json` | full |
| `evidence\daijisen-heads.txt` | full |
| `evidence\public-source\weblio-*.txt` (15 files) | full |
| `evidence\jmdict-families.xml` | part: XML-parsed extraction of every entry id cited on the Metadata line of each of the 15 cards, plus a few further ids |
| `evidence\jmdict-digest.tsv` | part (grep for 瞬 and 矢) |
| `evidence\joyo-pages.md` | part (grep for the 15 kanji; I read each kanji's rows) |
| `evidence\audits\reading-exposure.txt` | part: lines 1–60 and 110–192 in full, plus a grep of all "attested", "latent", "padded" and "production" lines and the last 15 lines |
| `evidence\app-code\QuizBuilder.kt` | full |
| `evidence\app-code\KanjiReadings.kt` | full |
| `evidence\app-code\` folder | listed |
| `titles\kanji-titles.tsv` | part (grep for every title quoted or relied on) |
| `snapshot\kanji\` 瞬 瞳 矢 砕 礎 秀 秘 稚 稼 稿 穏 穴 笛 粋 糧 `.md` | each in full |
| `snapshot\strokes\*.json` (15 files) | all parsed in full by script (kanji, strokeCount, number and ids of the strokes, KanjiVG revision, stroke types); `矢.json` also viewed in full |
| `diffs\` (21 files) | every hunk header and every changed line of all 21 |
| `repo\docs\confusable-words.md` | part (lines 40–80 and a grep) |
| `repo\docs\content-format.md` | part (grep for quiz_exclusions) |
| `repo\docs\` folder | listed |

Not opened:
- `evidence\audits\quiz-safety.txt`. I relied on the quiz-safety section of mechanical-checks.md and on titles.tsv instead.
- `evidence\audits\reading-options.txt`, `word-remarks.json`, `kanji-remarks.json`, `kanji_remarks.py` and `evidence\okurigana-scan.txt`.
- The full `snapshot\words\` files (I used the diffs).
- `rubric\`, and `repo\kanji` / `repo\words` beyond titles.tsv.

Public web: two weblio.jp lookups (いとけない, Digital Daijisen and 実用日本語表現辞典 entries); a jisho.org page and a kotobank page returned nothing useful.

## Verdicts

| Facet | Overall | Cards that differ |
| --- | --- | --- |
| 1 Correctness | **Defects found** (2 major, 4 minor) | Defects are on 秀 (C1), 粋 (C2), 稚 (C3), 矢 (C4), 礎 and 砕 (C5). I found no correctness defect on 瞬 瞳 秘 稼 稿 穏 穴 笛 糧 or in the 21 diffs. |
| 2 Scoped coverage | **Clean** | Every metadata reading has a row or a qualified source-only/rare account on all 15 cards. Optional coverage polish is noted for 矢, 秘 and 穏. |
| 3 Consistency and quiz safety | **Minor defects** (C6, C7) | Titles are unique. Every distractor is defensibly wrong in both directions. Links resolve. Stroke files match the front matter. The reading-exposure accounting is correct. The defects are over-broad exclusions on 矢 and 砕 (C6) and an undisclosed functional reason for 穏's distractors (C7). |
| 4 Comprehensibility | **Pass with defects inherited from facet 1** | The mnemonics of 秀 (C1), 粋 (C2) and 矢 (C4) would mislead a learner who looks at the character. The other 12 cards are clear, put the central idea first and explain their jargon. |

The 21 diffs:
- The 15 link-wraps change only the first mention of the kanji, and each points to `../kanji/X.md` for the intended kanji.
- The three word-remark edits (矢印, 砕く, 砕ける) are true: 矢 and 砕 now have cards.
- The three kanji-remark edits (基, 密, 透) are true and read correctly. 透's mnemonic sentence correctly says "秀 is a grain-plant shape 禾 over 乃".
- Verdict: clean.

## Findings (established defects)

### C1 — Major — Facet 1/4 — `snapshot\kanji\秀.md:27`

**Claim and impact.** The modern-shape mnemonic reads: "find 禾, the grain-plant key, at the left and [乃](乃.md) … at the right."

This is false. 秀 is a top-over-bottom character: 禾 sits on top and 乃 below.
- KanjiVG stroke order (`snapshot\strokes\秀.json`) is ㇒㇐㇑㇒㇏ for 禾, then ㇒㇡ for 乃 underneath.
- The 禾 in 秀 is the full-width top form, not a narrow left-hand side form.
- The modified 透 card in this same batch says "秀 is a grain-plant shape 禾 over [乃]".

A learner who looks for a left–right split will not find one. The two cards in the same batch contradict each other.

**Remedy.** Change the sentence to "find 禾, the grain-plant key, at the top and [乃](乃.md) … below it". Adjust the image if needed, for example "one stalk rising above the rest".

**Evidence.** The character's shape; `strokes\秀.json`; `diffs\kanji__透.md.diff`.

**Confidence.** High.

### C2 — Major — Facet 1/4 — `snapshot\kanji\粋.md:33`

**Claim and impact.** The mnemonic names the right part of 粋 as [卒](卒.md), "graduate; finish", and links that card.

The modern shape of 粋 has 卆 on the right: 九 over 十, 4 strokes. It does not contain 卒 (亠, two 人 and 十, 8 strokes).
- The stroke arithmetic shows it: 米 (6) + 卆 (4) = 10, which matches `strokes: 10`. With 卒 the total would be 14.
- `strokes\粋.json` gives ㇔㇒㇐㇑㇒㇔/㇏ for 米, then ㇒㇈㇐㇑ for 卆.

The prompt anticipated this point. The card is wrong as written: it tells the learner to find a shape that is not on the screen. (The 砕 card handles the same 卆 shape correctly as "looks like 九 above 十".)

**Remedy.** Either describe the part as on 砕 ("a part that looks like 九 above 十"), or say "卆, a simplified form of [卒](卒.md)". The second option keeps the link without claiming that 卒 itself appears.

**Evidence.** `strokes\粋.json`; the stroke count in the front matter; comparison with `砕.md:27`.

**Confidence.** High.

### C3 — Minor — Facet 1 — `snapshot\kanji\稚.md:40`

**Claim and impact.** The card says "In 稚い, 稚 writes いとけ and ない is the adjective ending."

But 稚い has only い after the kanji, so 稚 stands for いとけな and い is the okurigana. The ない-ending split applies only to the alternative spelling 稚けない.
- JMdict 2863360 lists 稚い, 幼い, 稚けない and 幼けない.
- Kanjipedia records いとけな.い.
- Daijisen has いとけ‐な・い【▽幼い／▽稚い】.
- Weblio 実用日本語表現辞典 has 幼けない with the alternative spelling 稚い.

This mis-teaches the kanji–kana boundary on the one word the card cites for this reading.

**Remedy.** Write "In 稚い, 稚 writes いとけな and い is the okurigana; JMdict also lists the spelling 稚けない, where 稚 writes いとけ."

**Evidence.** jmdict-families.xml 2863360; kanjipedia-outside-readings.json; weblio-稚.txt; live weblio いとけない page.

**Confidence.** High.

### C4 — Minor — Facet 1 — `snapshot\kanji\矢.md:27` and `:47`

**Claim and impact.**
- Line 27, the mnemonic: "imagine the vertical stroke as the arrow's shaft".
- Line 47: 午, 牛 and 天 "share a long vertical stroke and a crossing bar with 矢".

矢 has no vertical stroke. Its KanjiVG strokes are ㇒ ㇐ ㇐ ㇒ ㇏. The long central stroke (stroke 4) is a left-falling sweep, as in 大. 天 has no vertical stroke either (一 一 ノ ㇏). Only 午 and 牛 have a true vertical stroke.

The distractors are still visually plausible (crossing bars, a 大-like sweep), so the choice is fine. Only the stated reasons are false.

**Remedy.**
- Line 27: "imagine the long sweeping stroke through the middle as the shaft".
- Line 47: "午 and 牛 share a long central stroke and crossing bars with 矢; 天 shares the two bars and the spreading 大-like bottom".

**Evidence.** `strokes\矢.json`.

**Confidence.** High.

### C5 — Minor — Facet 1 — quoted titles that are not the exact titles

The packet rule is that a double-quoted gloss must be a JMdict gloss, a KANJIDIC2 meaning or the exact title of the cited card.

- `礎.md:27` quotes [林](林.md) as "woods". The 林 card's title is "grove; woodland". KANJIDIC2 gives grove and forest, so "woods" is neither.
- `砕.md:49` quotes [滅](滅.md) as "perish; destroy". The title is "perish; destroy; die out". This is a truncated title, which would be harmless if it were not in quotation marks.

**Remedy.** Quote the exact titles, "grove; woodland" and "perish; destroy; die out", or drop the quotation marks.

**Evidence.** `titles\kanji-titles.tsv`.

**Confidence.** High.

### C6 — Minor — Facet 3 — quiz_exclusions taken from word senses, not from the displayed labels (`矢.md:14,46`; `砕.md:14,49`)

**Claim and impact.**
- 矢 ("arrow; wedge") excludes 恋 "romantic love; longing" and 念 "thought; attention", and arguably 方 "direction, method". The card justifies them by the colloquial second sense of the word 矢印, "(romantic) interest", and by "direction".
- 砕 ("smash; crush; break into pieces") excludes 単 "single; simple", 易 "easy" and 簡 "simplicity; brevity", justified by 砕く sense 3 "to simplify". It also excludes 悩 "worry; be troubled", justified by a sense of 砕ける.

`repo\docs\confusable-words.md:45-46` says the ground for an exclusion is "overlapping meanings in the displayed quiz labels". In the kanji meaning quiz, none of these pairs can be defended: no learner could argue that "romantic love; longing" means 矢 "arrow; wedge", or that "easy" means 砕 "smash; crush".

The real direct pairs on 砕 (壊 破 割 崩 倒 滅 粉 細 磨) and on 矢 (印 示 標 符) are fine.

**Impact.** Low for safety, because over-exclusion only narrows the wrong-answer pool. It does, however, record pairs as "confusable" that are not confusable in this quiz, which goes against the documented convention.

**Remedy.** Drop 恋 and 念 from 矢 (and 方 unless "direction" is meant to be defended against "arrow"). Drop 単, 易, 簡 and 悩 from 砕. Or keep them and state in Notes that they are protective word-sense exclusions.

**Evidence.** Card lines 14 and 46/49; titles.tsv; confusable-words.md:45-46 and 74-75.

**Confidence.** Medium. Lines 74-75 do allow secondary senses, but they mean senses that a displayed label can carry.

### C7 — Minor — Facet 3/4 — `snapshot\kanji\穏.md:48`, the stated reason for distractors 木 田 花

**Claim and impact.** The card says 田 and 花 "look plausible because … they belong to the same field-and-plants picture as the mnemonic". That is a weak plausibility reason: 田 and 花 share no component with 穏 and no meaning with it.

The evident reason for the choice is not stated: all three are Starter-tagged cards with kun readings (き/こ-, た, はな). That makes the curated options fill all three wrong slots of the おだやか kun prompt in every pool, including the Starter practice session (`reading-exposure.txt` lines 176-190: "All stack: identical to N1 stack; Starter practice session: identical to N1 stack"). This is exactly what keeps the attested reading やすらか, held by 安, undrawable.

Because this dependency is not disclosed, a future editor could swap a distractor for a non-Starter 禾 kanji (私, 秒, 税). That would reopen the latent collision, as the audit's own risk-class line 183 warns. As meaning-quiz options, "rice field" and "flower" are defensibly wrong against "calm; gentle; peaceful", so there is no correctness problem. The issue is honesty and durability.

**Remedy.** Add one sentence to that bullet: all three are Starter cards with kun readings, so they fill every wrong slot of the おだやか reading question in all pools, which keeps 安's やすらか from appearing as a wrong option.

**Evidence.** `穏.md:48`; `reading-exposure.txt` 176-190; `KanjiReadings.kt` `question()` (curated cards are tried first, one random usable reading each).

**Confidence.** Medium-high.

### Leads (a)–(r) judged with no defect beyond the findings above

- **(a) 瞬**
  - The title "blink; instant" fits.
  - The kun accounts are faithful to the sources: まばた.く, まじろ.ぐ, しばた.く and しばたた.く are outside the table in Kanjipedia; JMdict 1341200 瞬く has sense 2 "to blink (one's eyes)"; 2831001 めたたく is archaic; 2831002 しばたたく is usually written in kana.
  - The exclusions 目 刻 時 間 秒 瞳 are real direct pairs.
  - The distractors 親 験 題 are defensibly wrong.
  - The one-sided exclusion 瞬→瞳 follows the convention.
- **(b) 瞳**
  - ドウ is given as an on reading in Daijisen (慣) and in Joyo p.120 (瞳孔). トウ is outside the table in Kanjipedia, so the source-only label is right.
  - The exclusions 目 and 眺 are right; there is no 眼 card. The distractors 真 着 相 all contain 目.
- **(c) 矢**
  - The title "arrow; wedge" matches JMdict 1537760.
  - シ is shown in Joyo p.64 as 一矢. The card also mentions さ (JMdict 1537760).
  - For the exclusions see C6, and for the distractor reasons see C4.
- **(d) 砕**
  - The mnemonic (卆 looks like 九 over 十; 5+2+2 = 9 strokes) is accurate.
  - The title is good.
  - The exclusions are covered in C6 and the quote in C5. The distractors 究 十 砂 are fine.
- **(e) 礎**
  - The mnemonic (林-like over 疋-like) is accurate apart from the "woods" quote (C5).
  - The title, the exclusions 基 根 底 台 本 元 源 石 and the distractors 研 楽 画 are fine.
  - 礎/基 is excluded.
- **(f) 秀**
  - Apart from C1, the title, the exclusions and the distractors 木 私 秒 are fine.
  - The kun reading ひい.でる and the name reading ほ are correctly sourced (Daijisen; KANJIDIC2 nanori).
- **(g) 秘** — the title, the exclusions 密 玄 私 偵 潜 皮 奥 被 and the distractors are fine.
- **(h) 稚**
  - Apart from C3, the front matter matches source-metadata.json (チ, ジ; いとけない, おさない, おくて, おでる).
  - The title, the exclusions and the distractors are fine.
- **(i) 稼**
  - Citing 禾稼 (かか) from Daijisen when JMdict has no entry is honest and labelled.
  - The title, the 11 exclusions and the distractors are fine.
- **(j) 稿**
  - All 17 JMdict ids check out. わら (藁) and したがき (下書き) are correctly explained as source-only.
  - Joyo p.56 (草稿, 原稿, 投稿; no kun) is quoted correctly.
  - The exclusions are real overlaps with "draft", "writing", "contribution" and "version".
  - 稼/稿 share no sense.
- **(k) 穏**
  - The やす.らか account is accurate: Kanjipedia lists it outside the table, and JMdict 1153690 writes 安らか with 安 only.
  - Joyo (穏和, 穏当, 平穏; おだやか 穏やかだ; the note 安穏 = アンノン) is quoted correctly.
  - The exclusions are real.
  - For the distractors see C7. Not noting 温和 is in Optional.
- **(l) 穴**
  - The mnemonic is accurate: 宀 (3 strokes) over 八 (2) = 5, which KanjiVG confirms.
  - The title, the exclusions 凹 巣 欠 差 窓 (matching senses 2, 3, 4, 5 and 1 of JMdict 1254480) and the distractors 究 突 定 are fine.
  - 穴/秘 has no displayed overlap.
- **(m) 笛**
  - The ジャク statement is properly hedged ("Kanjipedia lists … not taught").
  - The ちゃく claim is exactly JMdict 1437310 (out-dated kana usage).
  - 竹 (6) + 由 (5) = 11 strokes.
  - The title, the exclusion 管 and the distractors 笑 答 筆 are fine.
  - Joyo p.114 (汽笛, 警笛, 牧笛; 笛, 口笛) is quoted correctly.
- **(n) 粋**
  - See C2.
  - The title and the 12 exclusions are fine. The one-sided 粋→秀 follows the convention. The distractors 米 粉 糖 are fine.
  - All 9 JMdict ids check out, including 2848938 粋 すい "essence; the best; cream".
- **(o) 糧**
  - The mnemonic is accurate: 米 (6) + 量 (12) = 18.
  - All 6 JMdict ids check out (2017850 with the stagr かて on sense 2, かりて out-dated; 兵粮 out-dated).
  - The title, the exclusions and the distractors 粗 重 野 (里-like part) are fine.
  - Joyo p.157 (リョウ, ロウ 兵糧, かて) is quoted correctly.
- **(p) Shared distractors**
  - 木, 私, 秒 and 税 on the 禾 cards and 究 on 砕 and 穴 are plausible by shape and defensibly wrong both ways from the displayed titles.
  - The Notes bullets give true shape reasons, except 矢 (C4) and 穏 (C7).
- **(q) Exclusions**
  - Both one-sided exclusions are correct under the symmetric app logic (`QuizBuilder.excluded`).
  - I found no unexcluded pair whose displayed titles let a learner defend a wrong answer. Pairs checked include 稼 against 俸 "salary; stipend" and 賃 "fee; rent", 穏 against 悠 "leisurely; distant", 礎 against 柱 "pillar; post", 粋 against 風, and 糧 against 盛.
- **(r) Reading exposure**
  - The 7 latent collisions are 矢 さ (小 早 然), 秀 ほ, 稚 わく (惑), 稼 うえる (植 芸 飢), 穏 やすらか (安), 穴 しし (肉) and 笛 う (卯).
  - The count of 0 production, 0 padded-session and 0 one-holder hits agrees with the app logic in `KanjiReadings.kt`: curated cards are tried first, with one random usable reading each, and fallback only fills a deficit.
  - The single reading-options "problem" is a false positive for the shipped pools, because 木 田 花 fill all three slots in every pool. It is a real latent dependency (see C7).

## Optional (polish, not defects)

- **O1, `砕.md:25`.** "fine, small" is put in double quotes as Daijisen's sense こまかい. It is a translation, not a JMdict, KANJIDIC2 or title gloss. Use single quotes or no quotes. The same applies if the 秀 card quotes a translation of Daijisen's 最もすぐれている anywhere.
- **O2, 矢 coverage.** Consider naming 無理矢理 むりやり (JMdict 1531030, ichi1/news1/spec1) and 矢張り/矢っ張り (やはり, usually written in kana) as very common words that contain 矢. Today a learner meets them without the card's help.
- **O3, `秘.md:41`.** ひそ.か is shown as a plain kun reading. Kanjipedia marks ひそ.か (and かく.す) as outside the official table; Joyo lists only ひめる; and `daijisen-heads.txt` finds no Daijisen headword spelled 秘か. Labelling the row "kun, outside the official table" would match how the other cards label such rows.
- **O4, 穏.**
  - Line 25 says "Its examples are 穏健, 穏和, 安穏, 不穏 and 平穏". Daijisen also lists 静穏, so write "include" or add 静穏.
  - Line 46 quotes JMdict "穏和"; the entry (1589620) is headed 温和, with 穏和 as an equal-priority (ichi1) second spelling, and has 3 senses. Saying so would help the learner who meets 温和 more often.
- **O5, `穴.md`, the paragraph on JMdict 1254490.** The "usually kana" and colloquial tags sit on senses 1–2 only, not on the whole entry. The entry also has a fourth sense, the counter "hole; notch", which the card's list of senses omits.
- **O6, `diffs\kanji__基.md.diff`.** After the edit, [礎](礎.md) is the only item in that bullet without a quoted title. Adding "cornerstone; foundation" would keep the pattern.
- **O7, words\純粋.md (unchanged line, same paragraph as the link-wrap).** "Keep すい separate from the reading of the independent word 粋 (いき)" sits a little awkwardly next to the new 粋 card. That card notes JMdict 2848938, an independent 粋 read すい. This is outside the diff's change, so it is just a heads-up.

## Limits

- I issued exactly one tool call per response throughout; no parallel calls, sub-agents or background jobs.
- I checked readings and senses mainly against the packet's pinned sources:
  - JMdict, from the families XML for every cited id;
  - KANJIDIC2;
  - the Daijisen extracts in public-source and daijisen-heads;
  - Kanjipedia;
  - the Joyo page extracts.

  Live web verification was limited to weblio's いとけない entries, which confirm C3. Attempts at jisho and kotobank returned nothing usable. I did not do a live check of every word against an outside dictionary, so "verified" in this report means verified against the packet's pinned dictionary data.
- I did not open `quiz-safety.txt` or `reading-options.txt` in full. I relied on the mechanical-checks sections, titles.tsv and `reading-exposure.txt`, and I did not re-run any audit. The judgement in (r) rests on reading the audit output against `KanjiReadings.kt` and `QuizBuilder.kt`.
- I checked the word-article diffs from the diff hunks only, not from the full word files. I assumed that the link-plan and kanji_remarks checks (both OK in mechanical-checks.md) cover lines outside the hunks.
- Assumptions:
  - Over-broad exclusions (C6) are rated Minor rather than Optional, because confusable-words.md ties exclusions to the displayed labels.
  - C1 and C2 are rated Major because a false component statement in the mnemonic is an explicit correctness criterion, and it directly misleads a learner looking at the character.
- The Android JVM tests and the Kotlin cross-check were not run (a known limit of the packet). The localZipBytes variance is not treated as a defect.
