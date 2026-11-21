# Author's statement for the reviewer of `reports-156-hold\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 is your report's Finding and O1-O3 are your Optional notes.
Two of your Limits raise questions this revision can answer; they are L1 and L2 below. Your other Limits describe your own method
and need no answer. The statement is the author's claim about what changed and why. Verify each claim against the revised text in
`snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as
evidence. Line numbers refer to the revised files in this packet. Seven kanji cards changed (乙 亜 仙 伎 伏 伐 伴); the word article
乙 was deleted; the word article 甲乙 is new; the word articles 亜熱帯 and 仁 changed; and the generated `manifest.json` was
regenerated. Every other kanji card, every stroke file and every other word article is unchanged. See `CHANGES.md`. Give a
disposition for each of C1, O1-O3, L1 and L2, and judge the other reviews' changes described below.

## Findings

### C1: the word 乙's reading quiz can offer 音 おと, an attested reading of the written form 乙

Author action: **changed**, by a content remedy different from the two you named. The word article 乙 (`words\乙.md`) is deleted
and replaced by a new word article, 甲乙 こうおつ (`snapshot\words\甲乙.md`). No word quiz is built on the bare written form 乙 any
more.

- **Why not your preferred remedy:** `ReadingOptions.build` is app code in a separate repository (kanji-cards-android); this
  content revision cannot change it. The app change is recorded as a follow-up for the batch closure.
  `evidence\corpus-attested.txt` (produced by `evidence\gen_corpus_attested.py`) lists 112 existing words that can still be
  offered, in their reading quiz, a wrong option that JMdict gives as a reading of the word's written form. None is a batch-156
  word, and the freeze had 113, the extra row being 乙/音 おと.
- **Why not an accepted known risk:** both other reviews reported the same collision, one of them as major. That review named
  suppressing the ambiguous prompt as an acceptable remedy.
- **The new word's quizzes:** JMdict's only entry spelled 甲乙 (1280080, in `evidence\jmdict-cited-entries.xml`) has one
  reading, こうおつ. The word-quiz audit at `395f5364` (`evidence\word-quiz.txt`) shows:
  - lines 89-92: the reading quiz draws two of the generated look-alikes ごうおつ, こおつ, こうおうつ and こうおず, plus one
    option from a 9-word corpus tier; none is a reading of 甲乙;
  - line 3658: "ATTESTED or too-few-candidate problems: 0" (the freeze had 1, this collision);
  - lines 79-88: the meaning options (curated 丙 plus two from an 8-word tie at score 7).
  Digital Daijisen also gives かるめる, a music term written 上下 or 甲乙 (`evidence\甲乙-daijisen.txt`). No word article is read
  かるめる and it is not a generated look-alike, so it cannot be offered.
- **乙 is still taught:** the kanji card links 甲乙 at `乙.md:23`, `31` and `38`, and still names the word 乙 おつ with its
  JMdict gloss and entry 1182940 (lines 23 and 31). It still teaches おと at lines 10, 33, 42 and 53. No file links
  `words/乙.md`. That article was new in this batch and never published.
- **Your severity question** (whether the reading screen also shows the English meaning) no longer affects this batch, because no
  reading quiz shows bare 乙. If you want to check it for the 112 listed words, `WordQuizViewModel.kt` is in the original
  packet's `evidence\app-code\`.

`words\甲乙.md` is new text. Please review it in full on all four facets, including the meaning options above and the 甲乙 item
under "Points the author judged acceptable" in `CHANGES.md`.

## Optional notes

### O1: the 仁 example's English "This book writes about…"

Author action: **changed**. `words\仁.md:22` now reads "This book discusses benevolence in Confucianism.", one of your two
suggestions; both other reviews made the same note. The Japanese line (20) and its kana (21) are unchanged.

### O2: 仁's "nucleolus" sense is not mentioned

Author action: **changed**. `words\仁.md:38` now reads: "JMdict also gives the senses "human", "kernel" and, in biology,
"nucleolus"; only the kernel sense, the seed inside a fruit, can also be read にん." Check it against entry 1369620 in
`evidence\jmdict-cited-entries.xml`: senses 1, 2 and 4 are restricted to じん, and sense 3 "kernel" has no restriction.

### O3: the 伯 "HIT は" line in reading-options is a conservative over-report

Author action: **not changed**. The tool is workspace tooling outside this repository, and its output at `395f5364` is unchanged:
`checks\reading-options.txt:131` still prints the HIT line. `checks\reading-exposure.txt:150` shows that 伯's curated cards 自, 物
and 毎 fill all three wrong slots in every pool, and line 165 shows that は cannot be drawn in the N1 stack, All stack or Starter
practice session. `CHANGES.md` (the `reading-options.txt` bullet) gives this explanation for later reviewers. A note in the tool
output is recorded as a tooling follow-up for the batch closure.

## Limits answered

### L1: "JMdict has no entry read わざおぎ" was checked only through jisho.org

Author action: **evidence added**; `伎.md:34` is unchanged. `evidence\wazaogi-scan.txt` (produced by `evidence\wazaogi_scan.py`)
scans the pinned `JMdict_e.gz`. Its sha256 `42bd8fbc…` is the `jmdictSha256` in the original packet's
`evidence\provenance.json`. Of 219,135 entries, 0 have the reading わざおぎ and 0 have any reading that starts with わざお. The only
entry spelled 伎 alone is 1225090 (わざ, ぎ).

### L2: glosses of eight entries were not checked against the pinned JMdict

Author action: **evidence added**. `evidence\jmdict-cited-entries.xml` holds all eight entries from the pinned JMdict: 1466670,
1578730, 1282860, 1268820, 1778760, 1357390, 1417780 and 1002570. Seven of them, all but 1002570, were already in the original
packet's `evidence\jmdict-families.xml`, with the same spellings, readings and glosses; that file only expands JMdict's entity
codes into words. 1002570 was absent from it. The text that cites them is unchanged, with two exceptions: 1578730 (甲) is now also
cited by the new 甲乙 article, and 1002570 (お疲れ様) was cited only by the deleted word article 乙, so no revised file cites it.

## Changes made for the other reviews

The other two reviews reported three findings (one is the same collision as C1) and some optional notes. Please judge each change
below as a reviewer of the revised text, not only as an answer to your own notes.

1. **仁/人物 (major finding):** 人物 "person; figure; character" was drawable as a wrong meaning answer for 仁, although the
   article teaches 仁's "human" sense. `words\仁.md:8` is now `quiz_exclusions: [善, 親切, 優しい, 道徳, 人類, 人間, 人物, 個人, 芯,
   中心]`. The four new entries are:
   - 人物 and 個人 "individual; private person", for the "human" sense;
   - 芯 "core; wick" and 中心 "center; core; focus", for the "kernel" sense (JMdict 1595120 and 1424550 include "core; heart").

   The forward audit (`evidence\word-quiz.txt:109`) shows the ten exclusions, and line 113 shows 仁's meaning tier is now
   1,409 tied words (1,413 at the freeze). The reverse audit (lines 2691-2740) lists the 50 existing words whose meaning quiz can
   draw 仁, the same 50 as at the freeze. None of them is one of the ten excluded words. Please check that each exclusion rests on
   a real sense overlap and that no other tied word, or reverse target, makes 仁 a defensible answer.
2. **Distractor plausibility (minor finding on 仙 and 伎, extended to four more cards):** each old set was concrete objects
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
   collision (`checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt`).
3. **Wording:**
   - `亜.md:31`: 亜流 is glossed "(inferior) imitator; poor imitation", without "epigone".
   - `仙.md:32`: "ateji (kanji chosen for their sound, not their meaning)".
   - `words\亜熱帯.md:29`: "any of the three characters" (was "either character").
4. **Not changed:** one review suggested moving long exclusion reasons and distractor sentences off the main learner path. The
   cards keep the layout adopted in batch 149 and used since: short reading bullets, one reason per excluded group and one
   distractor sentence. A layout change would affect every N1 card, not only this batch.

No other hunk exists: every changed line is one of the changes above, part of the new 甲乙 article, or the regenerated
`manifest.json`.
