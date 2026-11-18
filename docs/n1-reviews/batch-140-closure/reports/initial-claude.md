# Batch 140 blind review — initial reviewer

Reviewer model: Claude (Anthropic), first of the two blind reviewers. Read-only review; the only file written is this report.

## Snapshot

- Commit `28831314c9b8203cf7dd66c4eec16f23ef0fef22` (batch 140).
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-140-28831314`. I did not recompute the packet-manifest.json sha256; I took the packet as given (see Limits).
- New kanji cards: 嵐 巣 帳 幕 幣 序 弁 往 径 徐 従 徴 志 怠 恨.

## Scope

Facets examined deepest: facet 1 (correctness) and facet 2 (scoped coverage). Facets 3 and 4 were covered for all 15 cards and all 24 diffs.

**Read in full:**

- `INSTRUCTIONS.md`
- `mechanical-checks.md`
- All 15 new cards in `snapshot\kanji\`: 嵐 巣 帳 幕 幣 序 弁 往 径 徐 従 徴 志 怠 恨
- `evidence\joyo-pages.md`, read in two ranges that together cover the whole file
- `evidence\source-metadata.json`
- `evidence\kanjipedia-outside-readings.json`
- `evidence\daijisen-heads.txt`
- `evidence\public-source\`: the Weblio Daijisen extracts for all 15 kanji
- `evidence\app-code\QuizBuilder.kt`
- `snapshot\strokes\弁.json`
- All 24 diffs in `diffs\`: every changed line, extracted by script

**Read in part:**

- `evidence\jmdict-digest.tsv`: searched by kanji and by entry id for every card.
- `evidence\jmdict-families.xml`: searched for specific entry ids, with context, for every card's example words. These include 序 1956430, 順序 1342340, 序幕 1345540, 秩序 1422520, 庠序 2254190, ついでに 1008050 and 弁 1512710. They also include はなびら 1194520, みち 1454080, 径 2018930, 徐に 1345580, ひろい 2427730, 従兄弟, 従姉妹, 追従, 従容, 従三位, 徴 2253400, しるし 2663510, 変徴 2829542, 志 シリング 2464210, 恨む and 憾む 2833583.
- All 15 files in `snapshot\strokes\`: every file parsed by script. For each one I checked the strokeCount, the length of the strokes array, the id sequence, the KanjiVG revision and the card's `strokes:` value.
- `evidence\audits\reading-options.txt`: lines 1-76 and a header search.
- `evidence\audits\quiz-safety.txt`: lines 1-12.
- `evidence\audits\reading-exposure.txt`: search for attested, latent and collision lines.
- `titles\kanji-titles.tsv`: searches, including 署, 帳, 幕 and a check that 緩 has no row.
- `snapshot\words\半径.md` lines 22-34 and `snapshot\words\往復.md` lines 26-36, to read the context of the removed remarks.
- `snapshot\kanji\慢.md` lines 74-86.
- `repo\kanji\墓.md` lines 1-16.
- `repo\docs\content-format.md` lines 71-139, plus a search.
- `rubric\`: search only.

**Folders listed non-recursively:** the packet root, `snapshot\`, `snapshot\strokes\`, `diffs\`, `evidence\`, `evidence\public-source\` and `evidence\audits\`.

**Live web:** two jisho.org API lookups.

- 冠 かんむり: JMdict spells it with 冠 only.
- 従三位: じゅさんみ, "second grade of the third rank of honor".

## Verdicts

The new cards and the edits are in good shape. Every reading, example word, gloss, Joyo-table claim, Daijisen or Kanjipedia claim, component statement and stroke count I checked is correct. The only established defects are three minor quiz-safety issues; facets 1, 2 and 4 are clean.

| Facet | Overall | Per card where it differs |
|---|---|---|
| 1 Correctness | CLEAN | — |
| 2 Scoped coverage | CLEAN | — |
| 3 Consistency and quiz safety | NEEDS FIX (minor) | 幣 (C1), 徴 (C2), 帳 and 幕 (C3). The other 11 cards are CLEAN. |
| 4 Comprehensibility | CLEAN | 径 and 弁 have optional polish (O1, O4). |

**Diffs.** All 24 diffs are CLEAN.

- In 21 word diffs, the only change is a link-wrap of the first mention of the new kanji. Each link points to the intended card (`../kanji/<kanji>.md`), and no other text changed.
- 半径 drops only "The missing 径 card does not remove that written character from the word." The passage still reads correctly: "...径 contributes a path or distance across. A radius is half a diameter."
- 往復 drops only "往 is part of the written word even though it has no kanji card here." The passage still reads "[往] contributes going, and [復] returning. This is a paired combination of the two directions: オウ + フク."
- The 慢 bullet now reads "緩 in 緩慢 has no kanji card here yet; this does not change the complete word's reading." This is true: 緩 has no row in `titles\kanji-titles.tsv`, and 怠 now has a card. The singular "word's" agrees with the single word left.

**Stroke files.** All 15 are CLEAN. strokeCount equals the length of the strokes array and the card's `strokes:` value for every file (嵐 12, 巣 11, 帳 11, 幕 13, 幣 15, 序 7, 弁 5, 往 8, 径 8, 徐 10, 従 10, 徴 14, 志 7, 怠 9, 恨 9). Every file has stroke ids running 1..n without gaps, cites KanjiVG CC BY-SA 3.0 and uses revision 70a0b7ae.

**Points (a)-(l) judged independently:**

- **(a) 幣.**
  - The accounts of ぬさ, みてぐら (Daijisen, not in KANJIDIC2) and まい (a separate Daijisen headword and JMdict 2789910) match the evidence.
  - The title "currency; Shinto offering" is accurate.
  - ぜに (a Kanjipedia outside reading) and にきて (a Daijisen ▽ headword) are rare readings that are never quizzed. Leaving them out is acceptable; see O2.
  - The distractors are a real issue: see C1.
- **(b) 従.**
  - The cards' accounts are all verified:
    - ジュウ with 従事, and ショウ with 従容 しょうよう and 追従 ついしょう / ついじゅう
    - ジュ with 従三位 じゅさんみ
    - より and the archaic prefix ひろい, which is JMdict 2427730 "lesser (of equal court ranks)"
    - 従兄弟 and 従姉妹 read いとこ: JMdict marks them gikun, usually kana, with the alternate readings じゅうけいてい and じゅうしまい
  - The title "follow; obey; subordinate" is accurate.
- **(c) 弁.**
  - The old forms are correct: the Daijisen [補説] says senses 1-3 were written 辨, 4-6 辯 and 7-8 瓣. JMdict 1512710 lists 辯, 瓣 and 辨 as out-dated spellings.
  - ヘン, かんむり, わける and あらそう are correctly treated as source-only. JMdict has no 弁 spelling for any of them, and 冠 is the only spelling of かんむり.
  - わきまえる is the Daijisen kun reading.
  - 花弁 read はなびら is JMdict 1194520 and is listed as 難読 (hard to read) in Daijisen.
  - The title omits the bento sense; see O4.
- **(d) 志.** The katakana kun シリング matches JMdict 2464210, where 志 is a search-only form noted as "formerly written as 志". こころざす and こころざし are correct. The name reading じん needs no account, because the cards do not cover nanori.
- **(e) 往.** All verified:
  - 往く is a rare kanji form of 行く, read いく or ゆく.
  - 往古 is a rare form of 古 いにしえ (poetical), also read おうこ.
  - さきに is source-only.
  - 往ぬ いぬ: sense 1 is Kansai dialect, the rest are archaic.
- **(f) 径.** The kun readings are verified:
  - みち: JMdict 1454080 spells it 道, 途, 路, 径.
  - わたり: the 径 entry 2018930.
  - こみち: 径書房 こみちしょぼう.
  - さしわたし and ただちに are qualified as source-only.
  - The title "diameter; path" is accurate.
  - One example is a weak illustration; see O1.
- **(g) 帳 and 幕.** とばり is handled consistently: JMdict spells it 帳 (rarely 帷, 幄 or 幌) and never 幕. 蚊帳 かや and 幕府 バク are correct. For the pairing, see C3.
- **(h) 徴.** The account of チ is right: JMdict 2253400 has the music-degree sense, with 変徴. しるし is JMdict 2663510 "sign; indication; omen". The title's "sign" collides with 署; see C2.
- **(i) Other rare or unquizzed readings.** These are accurate and clearly qualified:
  - 序: ついで, as JMdict 1345470 and ついでに 1008050 (rare kanji forms, usually kana)
  - 巣: ソウ
  - 嵐: ラン
  - 徐: おもむろに, as JMdict 1345580
  - 怠: タイ, with だるい marked usually kana
  - 恨: コン and うらめしい
- **(j) quiz_exclusions.** Each entry is a direct synonym or confusable pair that the card defends in its Notes. 従 (10 entries) and 徴 (10 entries) are broad but not transitive cliques. No defect.
- **(k) Distractors.** All are defensibly wrong, apart from C1 (幣) and the deliberate 署 case (C2).
  - Several are shape-family choices rather than strict look-alikes: 序 with 預, 弁 with 台 and 算, and 志 with 売. Each card's Notes explain the shared component honestly.
- **(l) Reading audits.**
  - The four latent collisions (幣 まい, 弁 とく, 従 ひろい, 志 じん) cannot be drawn in any pool, so no action is needed.
  - The HIT for 幣 まい is the same latent case.
  - In the 幕 マク quiz, the fallback fills two of the three slots. This is a quality note, not a defect; see O3.

## Findings

### C1: 幣's distractors include two near-synonyms of each other and weak look-alikes

- **Severity:** minor.
- **Facet:** 3.
- **Where:** `snapshot\kanji\幣.md` line 13 (`distractors: [中, 内, 南]`) and the line 53 Notes bullet.
- **Claim and impact:**
  - The titles of 中, "middle, inside", and 内, "within, inner", overlap in meaning. Two wrong options that say nearly the same thing let a learner eliminate both together, which weakens the quiz. content-format.md asks for semantically distinct wrong options.
  - The visual link is also thin. The Notes compare 巾's vertical stroke through 冂 with 中's stroke through a box. The card itself then names 常, 帯 and 希 as kanji that "have the same 巾 at the bottom", and those are much closer look-alikes.
- **Remedy:** Replace 中 and 内 (or one of them) with 常 "usual; constant", 帯 "sash; zone" or 希 "hope; rare", and adjust the Notes bullet to match.
- **Evidence:**
  - The card's own line 53.
  - The titles in `titles\kanji-titles.tsv`.
  - The content-format.md distractor rule.
- **Confidence:** high that 中 and 内 overlap in meaning; medium on whether the project treats this as a hard rule.

### C2: 徴's title and 署's title both lead with "sign"

- **Severity:** minor.
- **Facet:** 3.
- **Where:** `snapshot\kanji\徴.md` line 3 (`title: sign; indication; levy`), line 14 (quiz_exclusions, which leaves out 署) and line 56.
- **Claim and impact:**
  - 署 is titled "sign; government office" (kanji-titles.tsv).
  - Line 56 deliberately keeps 署 as "an ordinary wrong option for 徴".
  - When both appear in one meaning quiz, two options begin with the same headword "sign". The learner has to tell them apart by the second gloss alone, which defeats the card's own point that the two "sign"s are different ideas.
  - The tag-ordered fallback can surface either card in the other's quiz.
- **Remedy:** Either add 署 to 徴's quiz_exclusions (the exclusion applies in both directions), or retitle 徴 to lead with a gloss that does not collide, for example "indication; omen; levy".
- **Evidence:**
  - 徴.md lines 3, 14 and 56.
  - kanji-titles.tsv: `署 sign; government office`.
  - QuizBuilder.kt applies exclusions to the direct pair in both directions.
- **Confidence:** medium.

### C3: 帳 and 幕 share the curtain sense but do not exclude each other

- **Severity:** minor.
- **Facet:** 3.
- **Where:**
  - `snapshot\kanji\帳.md` line 14 (quiz_exclusions) and line 50
  - `snapshot\kanji\幕.md` line 14 (quiz_exclusions) and line 60
- **Claim and impact:**
  - Each card's Notes says the other also has a hanging-curtain sense. The 幕 card adds that 帳 "is the usual spelling of とばり".
  - Neither card lists the other in quiz_exclusions.
  - On a 帳 meaning quiz, the fallback can offer "curtain; act of a play; shogunate" as a wrong answer, although the card itself teaches that 帳 means a curtain in とばり and 蚊帳.
  - The titles do not collide, so a careful learner can still pick the title answer. That is why this is minor.
- **Remedy:** Add 幕 to 帳's quiz_exclusions; one side is enough because exclusions apply in both directions. Or accept the current titles as the disambiguation.
- **Evidence:** the two cards' Notes lines above, and JMdict とばり spelled 帳.
- **Confidence:** medium.

## Optional

- **O1 (径, line 28, facet 4).** The example for Daijisen sense 2, "a small path or a shortcut", is 径庭 けいてい, "great difference". That word does not show a beginner the "path" idea. A path word already used elsewhere on the card, such as 小径 or 山径, would illustrate the sense better. 径庭 could stay as a further note.
- **O2 (幣, facet 2).** ぜに (a Kanjipedia outside reading) and にきて (Daijisen ▽和幣) are not mentioned, though the reading audits are given both as extra readings. A short "rare / source-only" clause would make the coverage complete. Leaving them out is not wrong.
- **O3 (幕 reading quiz, facet 3).** For the マク prompt, the curated distractors give only one usable on-reading: 墓 has no quizOnyomi, and 暮 and 募 are both ぼ. The fallback therefore fills two of the three slots. A distractor with a distinct quizzable on-reading would keep the curated set effective.
- **O4 (弁, facet 4).** The title "speech; discern; valve" leaves out the "bento" sense (JMdict 1512710 sense 3), which is the sense of both linked words, 弁当 and お弁当. The Notes do explain this, so it is polish only.
- **O5 (怠, facet 3).** The distractor 治 "govern; heal" brushes against 怠る's dated JMdict sense "to improve (of an illness); to get better". It is still defensibly wrong as a title answer.

## Limits

- **Tool-call discipline.** I made one tool call per response throughout and issued no parallel calls. I used no sub-agents, background jobs or other sessions, and ran no recursive or corpus-wide scans.
- **Shell scripts.** Some single PowerShell calls looped over the files of one folder: the 24 diffs and the 15 stroke files. Each was still one tool call, and I note it for transparency.
- **Live web checks.** I made only two (jisho.org API: 冠 かんむり and 従三位). Every other dictionary check used the packet's pinned JMdict extracts and the Daijisen and Kanjipedia evidence. Live JMdict can differ slightly from the pinned snapshot.
- **Joyo table indentation.** The text extraction in joyo-pages.md loses indentation, so I could not confirm the layout of special-reading rows, such as 蚊帳. I could only confirm that the row text is present.
- **Earlier truncated glosses, now verified.** I checked 秩序 "method" and 序 sense 2 "beginning; start" in the full XML. The 従順 gloss "pliant" was confirmed only from the digest line, and I treat it as low risk.
- **Packet integrity.** I did not recompute the packet-manifest.json hash; I assumed the packet matches the stated manifest.
- **Name readings.** I assumed KANJIDIC2 nanori (name readings) are outside the cards' expected coverage. For this reason, 志 じん, 嵐 ぞれ, 幣 しで and similar readings are not findings.
- **Known limits and context, not findings.** As instructed, the Android JVM tests and the Kotlin reading-audit cross-check that were not run, the localZipBytes variation, and the four Dictionary-line lint warnings on 往復, 従姉妹, 直径 and 通帳 are not reported. No diff touches a Dictionary: line, and I found no defect there.
