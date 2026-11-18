# Batch 140 revision: what changed from 28831314 to 1b24a5f9

Revised snapshot: `1b24a5f97a396d7121689f3928c7aa500e0054ef`. It is reached from the reviewed snapshot
`28831314c9b8203cf7dd66c4eec16f23ef0fef22` by one commit. Nothing is published.

- Eight of the 15 kanji cards changed: 帳, 幕, 幣, 弁, 径, 徐, 従 and 徴. The other seven (嵐, 巣, 序, 往, 志, 怠, 恨)
  are unchanged. No word article, stroke file or existing kanji card changed: the 23 word articles the batch edits, the
  remark edit in 慢 and the 15 stroke files still differ from the published text exactly as in the reviewed snapshot.
- Front matter:
  - 幣 `distractors` changed from `[中, 内, 南]` to `[中, 南, 雨]`.
  - 徴 `quiz_exclusions` gained 署; it is now `[兆, 符, 印, 標, 症, 収, 採, 税, 召, 募, 署]`.
  - 帳 `quiz_exclusions` gained 幕; it is now `[録, 籍, 記, 誌, 冊, 本, 巻, 幕]`. 幕's own `quiz_exclusions` is
    unchanged. The app excludes a pair when either card lists the other (`evidence\QuizBuilder.kt` line 26), so 帳–幕
    and 徴–署 are now excluded in both directions.
  - 弁 `title` changed from `speech; discern; valve` to `speech; discern; valve; bento`; the heading at line 17
    matches.
  - No other title, tag, metadata reading or `distractors` list changed.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). Two cards changed
  length:
  - 弁 went from 73 to 60 lines. Lines 25-39 became one line, 25, and a new Notes bullet is line 55. Reviewed-snapshot
    lines 40-68 are now lines 26-54 (14 earlier), and lines 69-73 are now 56-60 (13 earlier); the Metadata line moved
    from 71 to 58.
  - 従 went from 69 to 61 lines. Lines 25-34 became one line, 25, and a new Notes bullet is line 56. Reviewed-snapshot
    lines 35-64 are now lines 26-55 (9 earlier), and lines 65-69 are now 57-61 (8 earlier).
  - Every other line number is unchanged.
- `diffs\fix.patch` is the exact patch from `28831314` to `1b24a5f9`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`, with the target's
  real `title:`.
- The Metadata lines. The author's writing rule for these cards is that the Metadata line lists the JMdict entry of
  every word the card names. The two words newly named by this revision have their entries added: 弁護士 (弁 line 58,
  entry 1512850) and 銭, named for the reading ぜに (幣 line 57, entry 2175880). 小径, now the example at 径 line 28,
  was already named and listed. `evidence\meta-scan.txt`, made by `evidence\meta_scan.py`, finds no word without its
  entry. The script checks every run of Japanese script that has at least two characters, contains a kanji and exactly
  matches a JMdict kanji spelling. It does not check words written only in kana, single-kanji words such as 銭, or
  words that appear only inside a longer word. It lists the last kind separately: 24 of them, the same 24 as at the
  reviewed snapshot. Only the line numbers of seven of them changed, all in 弁 and 従, because those lines moved.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 帳 | 14, 50 | Line 14: `quiz_exclusions: [録, 籍, 記, 誌, 冊, 本, 巻, 幕]` (幕 added). Line 50 now ends `this card's title keeps to the book sense, and 幕 is also kept out of this card's quiz options.` (it ended `keeps to the book sense.`). |
| 幕 | 60, 62 | Line 60 now ends `is the usual spelling of とばり, so the two are kept out of each other's quiz options.` (it ended `is the usual spelling of とばり.`). Line 62: `overlap the senses "act of a play," "covering cloth" and "end; close" that 幕 and its word carry;` now reads `overlap the senses "act of a play" and "end; close" that 幕 and its word carry, and the covering-cloth sense in the Daijisen entry;`. The rest of line 62 is unchanged. Support: 幕's title (`snapshot\kanji\幕.md` line 3) and `evidence\jmdict-cited-entries.xml`, entry 1524750 (幕; sense 4 "end; close"). |
| 幣 | 13, 31, 53, 57 | Line 13: `distractors: [中, 南, 雨]` (内 removed, 雨 added). Line 31: `Its kun readings are ぬさ and みてぐら;` now reads `Its kun readings in that entry are ぬさ and みてぐら;`, and before the closing sentence it adds `Two more readings are in neither KANJIDIC2 nor JMdict: [Kanjipedia's character entry](https://www.kanjipedia.jp/kanji/0006218900) also lists ぜに, a word for money that JMdict writes 銭, and another Daijisen headword reads 幣 as にきて, cloth hung on a sakaki branch as an offering to the gods, also written 和幣 or 幣帛.` Line 53: `[内](内.md), "within, inner," and [南](南.md), "south," are also built on 冂.` now reads `[雨](雨.md), "rain," has a vertical stroke running down from its top bar through the middle of 冂, and [南](南.md), "south," is also built on 冂.` Line 57 (Metadata): entry 2175880 is added after 2789910. Support: the original packet's `evidence\kanjipedia-outside-readings.json` (幣: kun ぜに, ぬさ, みてぐら; the URL above) and `evidence\daijisen-heads.txt` line 16 (`にき‐て【 ▽ 和 ▽ 幣／幣 ＝ 帛／ ▽ 幣】`); `evidence\jmdict-cited-entries.xml`, entry 2175880 (銭 ぜに); `evidence\雨.json`, the repository's KanjiVG stroke data for 雨. |
| 弁 | 3, 17, 25, 55, 58 | Lines 3 and 17: the title and heading gain `; bento`. Line 25 replaces reviewed-snapshot lines 25-39, the eleven-bullet list of Daijisen senses for ベン and the paragraph after it, with one paragraph: `The Daijisen character entry gives eleven senses for ベン, in a few main groups: telling things apart and settling them, as in 弁償 …; a packed meal, as in 駅弁 …; speaking and arguing, as in 弁解 …, and a dialect, as in 東北弁 …; and a petal or a valve, as in 花弁 かべん, "petal," and 安全弁 あんぜんべん, "safety valve." A common everyday word from the speaking group is 弁護士 べんごし, which JMdict glosses "lawyer; attorney." The Daijisen supplementary note says the discerning, settling and packed-meal senses were originally written 辨, the speaking senses 辯 and the petal and valve senses 瓣. It gives only the kun reading わきまえる and lists 花弁 (はなびら) among words with a hard-to-guess reading. All eleven senses, with an example each, are listed at the end of the Notes.` The glosses elided here are unchanged from the reviewed snapshot. Line 55 is a new Notes bullet, `For reference, the eleven Daijisen senses of ベン, one example each: …`, holding all eleven senses with the examples and glosses of the old list (弁別, 雄弁, 武弁 with its formal-or-literary mark, 合弁 and 弁髪 are glossed there). Line 58 (Metadata; line 71 before): entry 1512850 is added, and 1513120 moves before it. Support: `evidence\jmdict-cited-entries.xml`, entry 1512850 (弁護士); the original packet's `repo\kanji\筋.md` and `repo\kanji\納.md`, line 3, for published four-part titles. |
| 径 | 28, 60 | Line 28: the example for the sense "a small path or a shortcut" was `径庭 けいてい, "great difference," also written 逕庭;` and is now `小径 しょうけい, "path; lane," which JMdict marks formal or literary;`. Line 60, the reference bullet: 小径 is removed from it, and it now ends `捷径 しょうけい, "shortcut; expedient," and 径庭 けいてい, "great difference," also written 逕庭.` Support: `evidence\jmdict-cited-entries.xml`, entry 2859605 (小径). |
| 徐 | 36, 48 | Line 36: `JMdict also spells it 徐ろに.` now reads `JMdict also spells it 徐ろに, the spelling that KANJIDIC2's おもむ.ろに reflects, with ろに as okurigana.` Line 48: `overlap the sense "slow, unhurried" that 徐 carries` now reads `overlap the slow, unhurried sense that 徐 carries`. |
| 従 | 25, 56 | Line 25 replaces reviewed-snapshot lines 25-34, the six bullets of Daijisen senses for ジュウ and the paragraph on ショウ, ジュ and the kun readings, with one paragraph: `The Daijisen character entry gives six senses for ジュウ, among them obeying, as in 服従 …; being engaged in a task, as in 従事 …; and a starting point in time, as in 従来 …. For ショウ its senses include following along, as in 追従 …, and for ジュ it gives a court rank just below the main one, as in 従三位 …. A separate headword じゅう uses 従 as a noun for what is secondary; JMdict glosses it "subordinate; secondary; junior; incidental." The other senses, the Daijisen kun readings and more examples are listed at the end of the Notes.` The glosses elided here are unchanged from the reviewed snapshot. Line 56 is a new Notes bullet, `For reference, the other Daijisen senses: …`, holding the remaining senses and examples (従軍, 主従, 従弟, 合従, 従容), the sentence on the kun readings したがう, したがえる and より, and the sentence on the archaic prefix ひろい, all as worded before. |
| 徴 | 14, 56 | Line 14: `quiz_exclusions: [兆, 符, 印, 標, 症, 収, 採, 税, 召, 募, 署]` (署 added). Line 56 now ends `so [署](署.md), "sign; government office," is also kept out of this card's quiz options.` (it ended `remains an ordinary wrong option for 徴.`). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter (16 kanji cards: the 15 new ones and 慢; 25 word articles): 0 errors, 4 warnings, all on word
  articles whose Dictionary line cites no JMdict entry id (往復, 従姉妹, 直径, 通帳). The same four warnings were
  reported at the reviewed snapshot (the original packet's `mechanical-checks.md` lines 7-11); no word article changed.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage
  pilot). `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt` and `kanji-remarks.txt`: the word-article link plan (23 changed word files, 23 added links, 2 declared
  remark edits, 0 problems) and the check that existing kanji cards are unchanged apart from the declared remark edit
  in 慢 (1 modified, 0 problems). The declarations are unchanged from the original packet's `evidence\audits\`.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine), so there is no `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether
  the gloss quoted after the link equals that title.
- `quiz-safety.txt` differs from the original packet's `evidence\audits\quiz-safety.txt` only in two lines: the 幣 line
  (9), whose options are now `middle, inside | south | rain` (they were `middle, inside | within, inner | south`), and
  the 弁 line (13), which shows the new title. 0 errors, 0 warnings. 帳's and 徴's curated distractors still fill all
  three wrong slots of their meaning questions, so their options are unchanged.

### Reading audits

`reading-exposure.txt` and `reading-options.txt` were rerun with the same `--extra` input as at the freeze (it already
included ぜに and にきて for 幣). Apart from line 1 (the command), the only differences from the original packet's
`evidence\audits\` files are the 幣 block, where curated 雨 (う) replaces 内 (ない, だい), and the 弁 heading, which shows
the new title.

- `reading-exposure.txt` line 252: 0 production hits, 0 padded-session hits, 4 latent collisions, as at the freeze;
  line 253: 0 one-holder padded hits, 0 more for KANJIDIC2 name-only readings. The 幣 block starts at line 68: 中, 南
  and 雨 are all Starter cards, so the curated options fill all three wrong slots of the ヘイ question in every pool,
  including a Starter practice session that borrows 幣.
- `reading-options.txt` line 228: 1 problem, the HIT label at line 73 (幣 まい, offered by 埋, 妹, 枚, 毎 and 米), the
  same one reported at the freeze. This tool does not model curated slots that are already filled;
  `reading-exposure.txt`, which models the actual pools, finds まい not drawable.
- An earlier local version of this fix used the distractors `[常, 帯, 希]` for 幣. None of them is a Starter card, so
  in a Starter practice session the fallback filled the ヘイ question and could offer まい: one padded-session hit.
  That version was replaced before this packet was built; `evidence\superseded-775debde.txt` holds its audit lines.
