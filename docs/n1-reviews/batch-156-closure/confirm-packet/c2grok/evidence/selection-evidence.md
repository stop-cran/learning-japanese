# Word selection for the 乙, 仙 and 伯 rows: the rule and the sources

Every quotation below is verbatim. Check it against the named source; this file is a convenience, not evidence of its own.

## 1. The selection rule (issue #60, the remaining-rows proposal)

Source: https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7058679348 (B156 is the first batch under
it). Points 2 and 3 of its list "From B156: a supporting word article per kanji, new unless a suitable one exists":

> 2. **Choice of word.** I first check whether an existing article, including a kana-headed one, already teaches a suitable
> word, checking its spelling, reading and senses; if so, it is linked instead of adding one. Otherwise I take a word from
> the pinned JMdict, preferring a spelling with one of JMdict's common-word tags (news1, ichi1, spec1, gai1); where none
> exists, an untagged word may be used with a justification reviewed for that row. In either case the spelling and reading
> must have no irregular, rare, outdated, ateji or gikun mark. Its reading must use one KANJIDIC2 reading of the kanji, and
> its other kanji must already have cards or join the same batch. A word that shows the kanji's main meaning is preferred.
> The tags guide the choice; they are not evidence of frequency.
> [...]
> Rows outside the first group are decided one by one when they come up; a row with no defensible word is set aside and
> reported.
>
> 3. **Whole-word and sound-changed readings.** The cards of 伯 戯 撲 皇 眼 邪 also link their existing articles in the
> meaning or common-words text and explain the reading (a whole-word reading, or the sound change in 天皇 てんのう), as 鏡
> does for 眼鏡. Those words are not attached to a reading row and give no quizzed reading, so each of the six also gets a
> word under point 2, normally a new article.

("The first group" is the survey line "a tagged word whose other kanji have cards".)

## 2. What the JMdict priority tags mean

Source: the DTD comment on `ke_pri` in the pinned `JMdict_e.gz` (sha256
42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec).

> - news1/2: appears in the "wordfreq" file compiled by Alexandre Girardi from the Mainichi Shimbun. [...] Words in the
>   first 12,000 in that file are marked "news1" and words in the second 12,000 are marked "news2".
> - ichi1/2: appears in the "Ichimango goi bunruishuu", Senmon Kyouiku Publishing, Tokyo, 1998. [...]
> - spec1 and spec2: a small number of words use this marker when they are detected as being common, but are not included
>   in other lists.
> - gai1/2: common loanwords, based on the wordfreq file.
> - nfxx: [...] (The entries with news1, ichi1, spec1, spec2 and gai1 values are marked with a "(P)" in the EDICT and
>   EDICT2 files.)
>
> The reason both the kanji and reading elements are tagged is because on occasions a priority is only associated with a
> particular kanji/reading pair.

So the proposal's list (news1, ichi1, spec1, gai1) is JMdict's "(P)" set without spec2.

## 3. The official Joyo kanji table (2010)

`evidence\joyo\p<N>.txt` holds the text of each page used here (PDF page numbers; the printed page number is one higher).

- p. 19, 乙: `オツ 乙種，甲乙 乙女（おとめ）`: one reading, オツ; examples 乙種 and 甲乙; 乙女 with its reading in brackets.
- p. 94, 仙: `セン 仙骨，仙人，酒仙`.
- p. 97, 早: `ソウ 早朝，早晩，早々に 早乙女（さおとめ）`.
- p. 126, 伯: `ハク 伯仲，画伯 伯父（おじ）` / `伯母（おば）`.
- p. 162, the appendix (付表) of whole-word readings: `さおとめ 早乙女`, `おとめ 乙女`, `おじ` for 叔父 and 伯父, `おば` for
  叔母 and 伯母 (in the extracted text the two spellings sit on the lines above and below the reading). Its head note:
  "※以下に挙げられている語を構成要素の一部とする熟語に用いてもかまわない。"
- p. 3, note 13 of the table's preface: "「付表」には，いわゆる当て字や熟字訓など，主として１字１字の音訓としては挙げにくいものを語の形で掲げた。"
  (The appendix gives, as whole words, mainly ateji and jukujikun: readings that are hard to give character by
  character.)

## 4. Candidate words

`evidence\candidates.md` lists, for 乙, 仙 and 伯, every pinned-JMdict entry whose kanji form contains the kanji and carries
a priority tag on that form, plus the untagged entries named in `RESPONSE.md`, with the tags, readings, first glosses,
whether each other kanji has a card and whether a word article exists. `evidence\cands.py` is the script that produced it;
it needs the author's JMdict path module (n1lib), which is not included, so it is here to be read, not run. The complete
entries are in `evidence\jmdict-cited-entries.xml`.

## 5. Dictionary entries for the 乙 row

- Digital Daijisen, character entry 乙 (`evidence\weblio-乙.txt`): under 〈オツ〉, sense 2 "順位で、第二位。「乙種」"; under
  ［難読］ (hard-to-read words) it lists "早乙女 (さおとめ)".
- Digital Daijisen, 乙種, 乙種合格, 甲種, 丙種 and 種 (`evidence\weblio-<word>.txt`).
- Kanjipedia, 乙 (https://www.kanjipedia.jp/kanji/0000578500; `evidence\kanjipedia-乙.txt`), meaning ②:
  "物事の順位の二番目。「乙種」".
