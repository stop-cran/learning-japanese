# Author's statement for the reviewer of `reports-156-hold\initial-grok.md`

This statement answers only the points in YOUR initial report. X1 is your report's Finding. O1, O2 and O3 are the three bullets
of your Optional section, in order. Two of your Limits raise questions this revision can answer; they are L1 and L2 below. Your
other Limits describe your own method and need no answer. The statement is the author's claim about what changed and why. Verify
each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and
independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet. Seven kanji
cards changed (乙 亜 仙 伎 伏 伐 伴); the word article 乙 was deleted; the word article 甲乙 is new; the word articles 亜熱帯 and 仁
changed; and the generated `manifest.json` was regenerated. Every other kanji card, every stroke file and every other word article
is unchanged. See `CHANGES.md`. Give a disposition for each of X1, O1-O3, L1 and L2, and judge the other reviews' changes
described below.

## Findings

### X1: the word 乙's reading quiz can offer おと, an attested reading of the written form 乙

Author action: **changed**, by a content remedy, not the app remedy you named. The word article 乙 (`words\乙.md`) is deleted and
replaced by a new word article, 甲乙 こうおつ (`snapshot\words\甲乙.md`). No word quiz is built on the bare written form 乙 any
more. As you asked, the おと teaching stays on the kanji card.

- **Why not your remedy:** `ReadingOptions.build` is app code in a separate repository (kanji-cards-android); this content
  revision cannot change it. The app change is recorded as a follow-up for the batch closure. `evidence\corpus-attested.txt`
  (produced by `evidence\gen_corpus_attested.py`) lists 112 existing words that can still be offered, in their reading quiz, a
  wrong option that JMdict gives as a reading of the word's written form. None is a batch-156 word, and the freeze had 113, the
  extra row being 乙/音 おと. One other review rated this collision major and named suppressing the ambiguous prompt as an
  acceptable remedy.
- **The new word's quizzes:** JMdict's only entry spelled 甲乙 (1280080, in `evidence\jmdict-cited-entries.xml`) has one
  reading, こうおつ. The word-quiz audit at `3c5ef845` (`evidence\word-quiz.txt`) shows:
  - lines 89-92: the reading quiz draws two of the generated look-alikes ごうおつ, こおつ, こうおうつ and こうおず, plus one
    option from a 9-word corpus tier; none is a reading of 甲乙;
  - line 3658: "ATTESTED or too-few-candidate problems: 0" (the freeze had 1, this collision);
  - lines 79-88: the meaning options (curated 丙 plus two from an 8-word tie at score 7).
  Digital Daijisen also gives かるめる, a music term written 上下 or 甲乙 (`evidence\甲乙-daijisen.txt`). No word article is read
  かるめる and it is not a generated look-alike, so it cannot be offered.
- **The おと teaching is kept:** `乙.md:10` (kunyomi おと-), `33` (乙子 おとご), `42` (乙女 おとめ) and `53` (old usage for a younger
  brother or sister) are unchanged. The kanji card links 甲乙 at lines 23, 31 and 38, and still names the word 乙 おつ with its
  JMdict gloss and entry 1182940 (lines 23 and 31). No file links `words/乙.md`. That article was new in this batch and never
  published.

`words\甲乙.md` is new text. Please review it in full on all four facets, especially comprehensibility for an N5-N4 reader. Also
judge the meaning options above and the 甲乙 item under "Points the author judged acceptable" in `CHANGES.md`.

## Optional notes

### O1: "This book writes about benevolence in Confucianism" at `仁.md:20-22`

Author action: **changed**. `words\仁.md:22` now reads "This book discusses benevolence in Confucianism." The Japanese line (20)
and its kana (21) are unchanged.

### O2: "either character" in a three-character word at `亜熱帯.md:29`

Author action: **changed**. The sentence now ends "…not the historical origin of any of the three characters."

### O3: "ateji" without a gloss at `仙.md:32`

Author action: **changed**. The セント row now reads "ateji (kanji chosen for their sound, not their meaning)".

## Limits answered

### L1: JMdict 1002570 (お疲れ様) was checked only on jpdb

Author action: **evidence added, and no longer cited**. `evidence\jmdict-cited-entries.xml` holds 1002570 from the pinned JMdict.
Only the deleted word article 乙 cited it, so no revised file cites it.

### L2: the compound-sound-changes article was not in the packet

Author action: **evidence added**. `evidence\compound-sound-changes.md` is the article, unchanged since the freeze. The links are
`伐.md:31` and `words\亜熱帯.md:29` in this packet, and `潜.md:57` and `words\伐採.md:28` in the original packet's `snapshot\`.

- ねっ (ネツ) in 亜熱帯, and ばっ (バツ) in 伐採 (both 伐 lines), are the small-っ change in "Small っ: gemination in a compound"
  (article lines 26-49).
- ぷく (フク) in 潜伏 せんぷく is less well covered. The "Small っ plus /p/" section (lines 51-63) names the h-row to p-row
  change (handakuon-ka, lines 56-57), but its example 失敗 has the /p/ after small っ; in 潜伏 it follows ん. The published 輩
  card (batch 152, `evidence\輩.md:31`) links the article the same way for ぱい in 先輩 せんぱい.

Please judge whether the 潜 link is adequate for a beginner who follows it.

## Changes made for the other reviews

The other two reviews reported the same collision as X1 and three further findings, plus some optional notes; one could not
verify a sense stated in the new 甲乙 article. Please judge each change below as a reviewer of the revised text, not only as an
answer to your own notes.

1. **仁/人物 (major finding):** 人物 "person; figure; character" was drawable as a wrong meaning answer for 仁, although the
   article teaches 仁's "human" sense. `words\仁.md:8` is now `quiz_exclusions: [善, 親切, 優しい, 道徳, 人類, 人間, 人物, 個人, 芯,
   中心]`. The four new entries are:
   - 人物 and 個人 "individual; private person", for the "human" sense;
   - 芯 "core; wick" and 中心 "center; core; focus", for the "kernel" sense (JMdict 1595120 and 1424550 include "core; heart").

   In `evidence\word-quiz.txt`, line 109 shows the ten exclusions and line 113 shows 仁's meaning tier is now 1,409 tied words
   (1,413 at the freeze). The reverse audit (lines 2691-2740) lists the 50 existing words whose meaning quiz can draw 仁, the same
   50 as at the freeze; none is one of the ten excluded words.
2. **`words\仁.md:38`:** now reads: "JMdict also gives the senses "human", "kernel" and, in biology, "nucleolus"; only the kernel
   sense, the seed inside a fruit, can also be read にん." It was "…the senses "human" and "kernel"; the kernel sense, the seed
   inside a fruit, can also be read にん." Check it against entry 1369620: senses 1, 2 and 4 are restricted to じん, and sense 3
   "kernel" has no restriction.
3. **Distractor plausibility (minor finding on 仙 and 伎, extended to four more cards):** each old set was concrete objects
   (food, animals, containers, materials) set against an abstract target, so a learner could reject the options by category. Six
   sets changed (line 13), and each card's distractor sentence now names the three cards with their titles:
   - 乙 `[王, 硬, 粗]` (line 58)
   - 仙 `[下, 供, 生]` (line 49)
   - 伎 `[供, 食, 自]` (line 50)
   - 伏 `[起, 座, 伸]` (line 55)
   - 伐 `[保, 耕, 育]` (line 56)
   - 伴 `[迎, 離, 他]` (line 53)

   `CHANGES.md` ("Distractor choices") gives the principle, the candidates rejected during the fix, the pairs the author judged
   acceptable, and the reading-quiz effect. `evidence\distractor-senses.txt` and `evidence\distractor-use.tsv` hold the evidence.
   Please check that no new distractor is a defensible meaning answer for its target, and that none adds an attested-reading
   collision (`checks\reading-exposure.txt`, `checks\reading-options.txt`).
4. **`亜.md:31`:** 亜流 is glossed "(inferior) imitator; poor imitation", without "epigone".
5. **Not changed:**
   - **The 伯 "HIT は" line** in `checks\reading-options.txt:131`. One review called it a conservative over-report; your last
     Limit also found that は cannot be drawn. The tool is workspace tooling and its output is unchanged;
     `checks\reading-exposure.txt:150` and `165` show that the curated cards 自, 物 and 毎 fill all three wrong slots and that は
     cannot be drawn. A note in the tool output is recorded as a tooling follow-up.
   - **Card layout:** one review suggested shortening, or moving off the main learner path, long exclusion reasons, repeated
     "none means …" distractor sentences and repeated mnemonic disclaimers. The cards keep the layout adopted in batch 149 and
     used since: short reading bullets, one reason per excluded group and one distractor sentence. A layout change would affect
     every N1 card, not only this batch.
6. **Evidence for another review's limit:** `evidence\wazaogi-scan.txt` (produced by `evidence\wazaogi_scan.py`) checks the 伎
   card's unchanged "JMdict has no entry read わざおぎ" (line 34) against the pinned `JMdict_e.gz`. No entry has that reading, and
   none has a reading that starts with わざお.
7. **`words\甲乙.md`, lines 16, 18-20 and 25:** another review could not verify a sense the new article stated. At `395f5364`
   the Meaning paragraph also said that in a contract 甲 labels the first party and 乙 the second, so 甲乙 can name both parties
   together, and the first example was a contract sentence. Neither JMdict 1280080 nor Digital Daijisen
   (`evidence\甲乙-daijisen.txt`: １ 第一と第二, ２ 二つのものの間の優劣) gives that sense, so `3c5ef845` removes the sentence. The
   first example is now 姉妹の演奏は、甲乙を争う出来ばえだった。, built on Daijisen's example phrase 甲乙を争う出来ばえ, and line 25
   says both examples use the relative-merit sense. `CHANGES.md` ("Process notes") quotes the removed text. Line 39 still gives
   the JMdict senses of 甲 and 乙 on their own.

No other hunk exists: every changed line is one of the changes above, part of the new 甲乙 article, or the regenerated
`manifest.json`.
