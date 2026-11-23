# Author's statement for the reviewer of `reports-156-hold\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1, G2 and G3 are your report's Findings. O1, O2 and O3 are the
three bullets of your Optional section, in order. Two of your Limits raise questions this revision can answer; they are L1 and L2
below. Your other Limits describe your own method and need no answer. The statement is the author's claim about what changed and
why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files
and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet. Seven kanji
cards changed (乙 亜 仙 伎 伏 伐 伴); the word article 乙 was deleted; the word article 甲乙 is new; the word articles 亜熱帯 and 仁
changed; and the generated `manifest.json` was regenerated. Every other kanji card, every stroke file and every other word article
is unchanged. See `CHANGES.md`. Give a disposition for each of G1-G3, O1-O3, L1 and L2, and judge the other reviews' changes
described below.

## Findings

### G1: the word 乙's reading quiz can offer the attested reading おと as a wrong answer

Author action: **changed**, by your third remedy: the ambiguous prompt is gone. The word article 乙 (`words\乙.md`) is deleted
and replaced by a new word article, 甲乙 こうおつ (`snapshot\words\甲乙.md`). No word quiz is built on the bare written form 乙 any
more. 音's reading is unchanged, and no exclusion was added for it.

- **Why not the client remedy:** `ReadingOptions.build` is app code in a separate repository (kanji-cards-android); this content
  revision cannot change it. The app change is recorded as a follow-up for the batch closure. `evidence\corpus-attested.txt`
  (produced by `evidence\gen_corpus_attested.py`) lists 112 existing words that can still be offered, in their reading quiz, a
  wrong option that JMdict gives as a reading of the word's written form. None is a batch-156 word, and the freeze had 113, the
  extra row being 乙/音 おと.
- **Why not disambiguation:** the author found no content-side way to add sense context to a word's reading question. Replacing
  the word is the remedy available within this content revision.
- **The new word's quizzes:** JMdict's only entry spelled 甲乙 (1280080, in `evidence\jmdict-cited-entries.xml`) has one
  reading, こうおつ. The word-quiz audit at `3c5ef845` (`evidence\word-quiz.txt`) shows:
  - lines 89-92: the reading quiz draws two of the generated look-alikes ごうおつ, こおつ, こうおうつ and こうおず, plus one
    option from a 9-word corpus tier; none is a reading of 甲乙;
  - line 3658: "ATTESTED or too-few-candidate problems: 0" (the freeze had 1, this collision);
  - lines 79-88: the meaning options (curated 丙 plus two from an 8-word tie at score 7).
  Digital Daijisen also gives かるめる, a music term written 上下 or 甲乙 (`evidence\甲乙-daijisen.txt`). No word article is read
  かるめる and it is not a generated look-alike, so it cannot be offered.
- **乙 is still taught:** the kanji card links 甲乙 at `乙.md:23`, `31` and `38`, and still names the word 乙 おつ with its
  JMdict gloss and entry 1182940 (lines 23 and 31). It still teaches おと at lines 10, 33, 42 and 53. No file links
  `words/乙.md`. That article was new in this batch and never published.

`words\甲乙.md` is new text. Please review it in full on all four facets, including the meaning options above and the 甲乙 item
under "Points the author judged acceptable" in `CHANGES.md`.

### G2: 人物 is drawable as a wrong meaning answer for 仁, although 仁 has the sense "human"

Author action: **changed** as you proposed, with three further direct exclusions. `words\仁.md:8` is now `quiz_exclusions: [善,
親切, 優しい, 道徳, 人類, 人間, 人物, 個人, 芯, 中心]`. The article still teaches the "human" sense (line 38).

- 人物 "person; figure; character" is your pair.
- 個人 "individual; private person" is the same kind of overlap with the "human" sense.
- 芯 "core; wick" and 中心 "center; core; focus" overlap the "kernel" sense: JMdict 1595120 and 1424550 both include "core;
  heart" (`evidence\jmdict-cited-entries.xml`).

These are direct sense overlaps with 仁's own JMdict senses (entry 1369620), not a transitive expansion of the ethics words.
Audits at `3c5ef845`:

- **Forward** (`evidence\word-quiz.txt`): line 109 shows the ten exclusions, and line 113 shows 仁's meaning tier is now 1,409
  tied words (1,413 at the freeze).
- **Reverse:** lines 2691-2740 list the 50 existing words whose meaning quiz can draw 仁, the same 50 as at the freeze. None is
  one of the ten excluded words.

Please check that each exclusion rests on a real sense overlap and that no other tied word, or reverse target, makes 仁 a
defensible answer.

### G3: the curated distractor sets of 仙 and 伎 can be rejected by category

Author action: **changed**, and extended to four more cards whose sets had the same pattern. Each old set was concrete objects
(food, animals, containers, materials) set against an abstract target. Six sets changed (line 13), and each card's distractor
sentence now names the three cards with their titles:

- 乙 `[王, 硬, 粗]` (line 58)
- 仙 `[下, 供, 生]` (line 49)
- 伎 `[供, 食, 自]` (line 50)
- 伏 `[起, 座, 伸]` (line 55)
- 伐 `[保, 耕, 育]` (line 56)
- 伴 `[迎, 離, 他]` (line 53)

As you suggested, 仙 and 伎 each take a 亻 card (供). 伏, 伐 and 伴 each take one too (伸, 保, 他). The author's checks found no
new distractor synonymous with its target. `CHANGES.md` ("Distractor choices") gives the principle, the candidates rejected during the fix (父 for 仙, 達 and 行
for 伎), the pairs the author judged acceptable, and the reading-quiz effect. `evidence\distractor-senses.txt` and
`evidence\distractor-use.tsv` hold the evidence. For the recheck you asked for:

- **Both meaning directions:** each candidate was checked against every JMdict entry spelled with that character alone and
  against the target's `quiz_exclusions`.
- **Curated reading slots and fallback reachability:** `checks\reading-exposure.txt` and `checks\reading-options.txt` show them.
  仙 and 伎 now use curated options only in all three pools, because their distractors are Starter cards.
- **Totals:** the last two lines of `checks\reading-exposure.txt` (188-189) match the freeze: 0 production, 0 padded-session and
  0 one-holder hits, and 10 latent collisions.

Please check that no new distractor is a defensible meaning answer for its target.

## Optional notes

### O1: shorten or move audit-oriented explanations off the main learner path

Author action: **not changed**. The cards keep the layout adopted in batch 149 and used since: short reading bullets, one reason
per excluded group and one distractor sentence. A layout change would affect every N1 card, not only this batch, so it belongs in
a separate project-wide decision. The distractor sentences changed in this revision are one sentence each.

### O2: explain specialist English such as "epigone" and "ateji"

Author action: **changed**.
- `亜.md:31` glosses 亜流 as "(inferior) imitator; poor imitation"; "epigone" is gone.
- `仙.md:32` now reads "ateji (kanji chosen for their sound, not their meaning)".

### O3: "This book discusses benevolence in Confucianism" at `仁.md:22`

Author action: **changed** to your wording. The Japanese line (20) and its kana (21) are unchanged.

## Limits answered

### L1: the compound-sound-changes article was not in the packet, so four link destinations were UNVERIFIED

Author action: **evidence added**. `evidence\compound-sound-changes.md` is the article, unchanged since the freeze. The links are
`伐.md:31` and `words\亜熱帯.md:29` in this packet, and `潜.md:57` and `words\伐採.md:28` in the original packet's `snapshot\`.

- ねっ (ネツ) in 亜熱帯, and ばっ (バツ) in 伐採 (both 伐 lines), are the small-っ change in "Small っ: gemination in a compound"
  (article lines 26-49).
- ぷく (フク) in 潜伏 せんぷく is less well covered. The "Small っ plus /p/" section (lines 51-63) names the h-row to p-row
  change (handakuon-ka, lines 56-57), but its example 失敗 has the /p/ after small っ; in 潜伏 it follows ん. The published 輩
  card (batch 152, `evidence\輩.md:31`) links the article the same way for ぱい in 先輩 せんぱい.

Please judge whether the 潜 link is adequate.

### L2: お疲れ様 (1002570) was absent from the local XML

Author action: **evidence added, and no longer cited**. `evidence\jmdict-cited-entries.xml` holds 1002570 from the pinned JMdict.
Only the deleted word article 乙 cited it, so no revised file cites it.

## Changes made for the other reviews

Both other reviews reported the same collision as G1, as a minor finding, and made some optional notes; one could not verify a
sense stated in the new 甲乙 article. Please judge each change below as a reviewer of the revised text, not only as an answer to
your own notes.

1. **`words\仁.md:38`:** now reads: "JMdict also gives the senses "human", "kernel" and, in biology, "nucleolus"; only the kernel
   sense, the seed inside a fruit, can also be read にん." It was "…the senses "human" and "kernel"; the kernel sense, the seed
   inside a fruit, can also be read にん." Check it against entry 1369620: senses 1, 2 and 4 are restricted to じん, and sense 3
   "kernel" has no restriction.
2. **`words\亜熱帯.md:29`:** "…not the historical origin of any of the three characters" (was "either character").
3. **Not changed: the 伯 "HIT は" line in `checks\reading-options.txt:131`.** One review called it a conservative over-report, as
   your "Additional adjudications" also found. The tool is workspace tooling and its output is unchanged.
   `checks\reading-exposure.txt:150` and `165` show that the curated cards 自, 物 and 毎 fill all three wrong slots and that は
   cannot be drawn. A note in the tool output is recorded as a tooling follow-up.
4. **Evidence for another review's limit:** `evidence\wazaogi-scan.txt` (produced by `evidence\wazaogi_scan.py`) checks the 伎
   card's unchanged "JMdict has no entry read わざおぎ" (line 34) against the pinned `JMdict_e.gz`. No entry has that reading, and
   none has a reading that starts with わざお.
5. **`words\甲乙.md`, lines 16, 18-20 and 25:** another review could not verify a sense the new article stated. At `395f5364`
   the Meaning paragraph also said that in a contract 甲 labels the first party and 乙 the second, so 甲乙 can name both parties
   together, and the first example was a contract sentence. Neither JMdict 1280080 nor Digital Daijisen
   (`evidence\甲乙-daijisen.txt`: １ 第一と第二, ２ 二つのものの間の優劣) gives that sense, so `3c5ef845` removes the sentence. The
   first example is now 姉妹の演奏は、甲乙を争う出来ばえだった。, built on Daijisen's example phrase 甲乙を争う出来ばえ, and line 25
   says both examples use the relative-merit sense. `CHANGES.md` ("Process notes") quotes the removed text. Line 39 still gives
   the JMdict senses of 甲 and 乙 on their own.

No other hunk exists: every changed line is one of the changes above, part of the new 甲乙 article, or the regenerated
`manifest.json`.
