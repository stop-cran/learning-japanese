# Batch 159 revision: what changed from 4f8ebea7 to 54b00e0c

The revised snapshot is `54b00e0c`, one commit whose parent is `4f8ebea7`. The range has no merges. Every commit from the reviewed freeze `1a9bb910` through `54b00e0c` is signed with key D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (`evidence\verify-commit.txt`).

This revision answers the confirmation reports on `4f8ebea7`:
- one reviewer confirmed with no findings and one optional note;
- a second reviewer confirmed every point except one (NEEDS FIX): the 叔 support row. Under point 2 of the issue #60 rule, a tagged spelling with an unflagged reading that uses a KANJIDIC2 reading of 叔 qualifies, so the author's exception for the untagged 伯叔 could not be published without the owner's explicit acceptance. The reviewer named the fallback 叔父 (しゅくふ) and added one optional note.

`RESPONSE.md` answers your own report only.

- **Changed:**
  - the 叔 support article: `words/伯叔.md` is deleted and `words/叔母.md` (reading しゅくぼ, JMdict entry 1607100) is added;
  - the batch card `kanji/叔.md`: the シュク Readings row (line 29), the Common words list (lines 33–34) and one Notes paragraph (line 38);
  - the existing card `kanji/伯.md`: restored to its text at the batch base `2787e43b` (the 伯叔 line is removed; `git diff 2787e43b 54b00e0c -- kanji/伯.md` is empty);
  - the existing card `kanji/母.md`: one Common words line added (line 38);
  - the word articles `words/太后.md` (line 15) and `words/吟味.md` (line 24): one long sentence each split in two, with no change of wording otherwise;
  - the ledger `docs/n1-sources/batch-159-progress.json`: the selection statement (line 29), the 叔 support mapping (lines 71–81), the 叔 reciprocal pair (line 186), the changed reused passage (lines 219–221, now 母 instead of 伯), the word-quiz exclusion row (lines 279–283), the 叔 シュク reading row (lines 522–526) and the status (line 955).
- **Unchanged:**
  - the other nine batch cards;
  - the other seven new word articles, and every other existing card or article changed earlier in the batch (太 官 不 味 情 服 贈, また, または);
  - `tools/`, the pinned JMdict selection and extract (still 87 complete families: entries 1607070, 1607100 and 1474270 were already cited by the 叔 card), every stroke file and every other file.
- **Generated file:** `manifest.json` is regenerated (contentVersion `523a882a9af5a7e3`; was `c459784ce290b1ef`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot. `diffs\changed-lines.txt` has the old and new text of every changed line.

## The 叔 support: 叔母 (しゅくぼ)

The 叔 row now follows the letter of point 2 of the rule (`evidence\rule-7058679348.md`). There is no author's exception left in this row.

- **Qualification.** JMdict entry 1607100 (`evidence\jmdict-cited-entries.xml`): the spelling 叔母 carries ichi1/news1/nf20; the reading おば carries ichi1/news1/news2/nf20/nf30; the reading しゅくぼ is restricted (`re_restr`) to 叔母 and carries no priority tag and no `re_inf` mark; the spelling carries no `ke_inf` mark. しゅくぼ uses シュク, a KANJIDIC2 on reading of 叔, and ボ for 母. The other kanji, 母, has a card. Sense 1: “aunt”, with the note “伯母 can mean older and 叔母 can mean younger than one's parent”.
- **Sources for the meaning.** Digital Daijisen, しゅく‐ぼ【叔母】: 「父母の妹。おば。」; 精選版 日本国語大辞典, しゅく‐ぼ【叔母】: 「〘名詞〙 父母の妹。おば。」, with no variant reading (`evidence\daijisen-kotobank.json`, captured from https://kotobank.jp/word/%E5%8F%94%E6%AF%8D-528307). The Joyo table lists 叔母 おば among the whole-word special readings (`evidence\joyo\p162.txt`) and 伯叔 as its example for シュク (`evidence\joyo\p75.txt`).
- **Why not 叔父 (しゅくふ).** 叔父 (entry 1607070) qualifies in the same way: the spelling has ichi1/news1, and しゅくふ is restricted to it and unflagged. It is not used because 精選版 日本国語大辞典 gives a variant reading: しゅく‐ふ【叔父】「〘名詞〙 ( 「しゅくぶ」とも ) 父母の弟。おじ。」 (`evidence\daijisen-kotobank.json`, from https://kotobank.jp/word/%E5%8F%94%E7%88%B6-528298). The word reading quiz draws two of its generated look-alike readings at random (`evidence\Words.kt`: `ReadingOptions.mutations`, lines 234–246, and `ReadingOptions.build`, lines 256–268, where line 263 takes the first two of the shuffled look-alikes). For しゅくふ the look-alikes are じゅくふ, しゅぐふ, しゅっくふ, しゅくぶ and しゅくぷ, so a 叔父 article would show the attested しゅくぶ as a “wrong” option in 4 of the 10 equally likely draws. The app has no way to exclude a reading option. The look-alikes for しゅくぼ are じゅくぼ, しゅぐぼ, しゅっくぼ, しゅくほ and しゅくぼう; none is a recorded reading (`evidence\reading-lookalikes-c3.txt`, produced by running the word-quiz audit's Python port of `mutations` unchanged; `evidence\word-quiz.txt` line 96, where the audit checks each look-alike against JMdict). 叔母 also matches the 叔 card's title, “uncle or aunt (younger than a parent)”, as well as 叔父 does, and Digital Daijisen's first sense of 叔 cites both: 「１ 父・母の年下のきょうだい。「叔父・叔母」」 (`evidence\daijisen-weblio-叔.txt`, the extract behind `kanji/叔.md:23`).
- **What the article teaches.** `words/叔母.md` teaches the reading しゅくぼ and says plainly, in “Distinctive meaning” (line 32), that 叔母 is also read おば, which is the Joyo special reading and the reading JMdict tags, and that not every printed 叔母 is pronounced しゅくぼ. `words/身体.md` (しんたい, also read からだ) is an existing article that teaches the on reading of a spelling with a common alternative reading.
- **The 叔 card.** The シュク Readings row (line 29) now leads with the linked 叔母 しゅくぼ and gives Digital Daijisen's definition 父母の妹, then 叔父 しゅくふ, then the unlinked 伯叔 はくしゅく (still the Joyo table's example; entry 1474270 is still cited). The Common words line for 叔母 (line 34) links the article: “[叔母](../words/叔母.md) おば, also しゅくぼ — aunt (written 叔母 when younger than one's parent)”. The former 伯叔 Common words line is removed. The Notes paragraph (line 38) adds: “Read with シュク, 叔父 is しゅくふ and 叔母 is しゅくぼ; JMdict restricts these readings to those spellings.”
- **Reciprocal links.** `words/叔母.md` links `../kanji/叔.md` and `../kanji/母.md` (line 24); `kanji/叔.md` links `../words/叔母.md` (lines 29 and 34); `kanji/母.md:38` adds “[叔母](../words/叔母.md) しゅくぼ — aunt (a parent's younger sister)”.
- **伯.** `kanji/伯.md` no longer needs the 伯叔 link and is back to its B158 text. The ledger's changed-reused-passages list names 母 instead of 伯.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `words/伯叔.md` | all | deleted |
| `words/叔母.md` | 1–34 | new article (see above) |
| `kanji/叔.md` | 29 | シュク row: “[叔母](../words/叔母.md) しゅくぼ — aunt; Digital Daijisen defines it as a younger sister of one's father or mother (JMdict entry 1607100); 叔父 しゅくふ — uncle; Digital Daijisen defines it as a younger brother of one's father or mother (JMdict entry 1607070); 伯叔 はくしゅく — brothers; one's father's brothers (JMdict entry 1474270)” |
| | 33–34 | the plain 叔母 line and the 伯叔 line become one linked line (quoted above) |
| | 38 | adds the sentence quoted above |
| `kanji/伯.md` | (old 39) | the 伯叔 line is removed; the file equals its B158 text |
| `kanji/母.md` | 38 | the new 叔母 line, after 母語 |
| `words/太后.md` | 15 | “…皇太后 as the empress of the previous emperor. In a narrower sense, 皇太后 is such an empress…” (was “…previous emperor; in a narrower sense…”) |
| `words/吟味.md` | 24 | “…the original meaning of 吟味. Digital Daijisen sense 3 is…” (was “…the original meaning of 吟味: Digital Daijisen sense 3 is…”) |
| `docs/n1-sources/batch-159-progress.json` | 29 | `selectionReason`: “The 叔 row uses 叔母 (entry 1607100): its spelling carries ichi1/news1, and its reading しゅくぼ, restricted to that spelling, uses シュク; its support mapping explains why the equally tagged 叔父 is not used.” The exception wording is removed. |
| | 71–81 | 叔 mapping: article `words/叔母.md`, primary reading しゅくぼ, entry 1607100, priority tags ichi1/news1; `exceptionReason` is replaced by a `note` (quoted below) |
| | 186 | reciprocal pair 叔 ↔ `words/叔母.md` |
| | 219–221 | changed reused passage: `kanji/母.md` (was `kanji/伯.md`) |
| | 279–283 | word-quiz exclusions: 叔母 → 伯母さん, 親戚, 親類 (was 伯叔 → 兄弟, おじさん, 親戚) |
| | 522–526 | 叔 シュク reading row: “The supported common-word article 叔母 directly uses シュク.”, entry 1607100 |
| | 955 | `status`: “The 后 and 吏 untagged-support exceptions and the kana-headed 又 support remain subject to review.” |

Ledger line 81 (the 叔 `note`) reads, in full:

> The spelling 叔母 carries ichi1/news1 (the reading おば also carries ichi1/news1). The reading しゅくぼ, restricted to 叔母, carries no priority tag and no irregular, rare, outdated, ateji, or gikun mark, and it uses the KANJIDIC2 reading シュク. 叔父 (entry 1607070) qualifies in the same way, with the reading しゅくふ, but it is not used: 精選版 日本国語大辞典 gives しゅくぶ as a variant reading of 叔父, and the reading quiz can generate しゅくぶ from しゅくふ as a look-alike wrong option. Neither Digital Daijisen nor 精選版 日本国語大辞典 gives a variant reading for 叔母 しゅくぼ.

## Quiz options

- **Word quiz, 叔母** (`evidence\word-quiz.txt` lines 70–97).
  - Meaning: no curated options. The reachable options are 父母 “father and mother; parents” and 祖母 “grandmother” (score 8) and the score-7 tier of family nouns (lines 77–93). `quiz_exclusions` removes 伯母さん “aunt” (same meaning), and 親戚 and 親類 “relative; kin” (a broader term that covers an aunt). 親戚 was already excluded by 伯叔; 親類 has the same gloss, so it is excluded too. Exclusion is symmetric (`evidence\Words.kt`).
  - Reading: the JMdict readings of 叔母 are おば and しゅくぼ (line 95). Two wrong options are drawn from the look-alikes listed above, none of them a recorded reading. The third comes from the closeness tier お母さん おかあさん, 伯母さん おばさん and 母親 ははおや (line 97). おばさん is the reading of 伯母さん and 叔母さん, not of the bare spelling 叔母, so it is a wrong option here. おば itself never appears: no word article has the reading おば, and no look-alike of しゅくぼ produces it. The audit reports 0 attested or too-few-candidate problems (line 1436).
  - Reverse direction: 叔母 can appear as a wrong option in other words' quizzes (the reverse section of `evidence\word-quiz.txt`), mostly in family words, whose titles differ from “aunt (a parent's younger sister)”.
- **Word quiz, other words.** 伯叔 is gone from the pool. 太后 and 吟味 keep their front matter, so their option sets are unchanged.
- **Kanji quiz.** `checks\quiz-safety.txt`, `checks\reading-exposure.txt` and `checks\reading-options.txt` are identical to the earlier revision's apart from the header line. No card front matter changed.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `4f8ebea7`, except the numbers named here.

- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0; 87 complete JMdict families; the manifest is fresh (`523a882a9af5a7e3`). The audit checks the 叔 mapping (reading, new article, entry ids in the extract families, the spelling and reading pair, reciprocal links).
- **budget:** retained 56,881,413 bytes, inflated 57,317,485 and local ZIP 36,535,514 (+436 retained bytes from `4f8ebea7`). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety:** 0 errors, 0 warnings. **reading-exposure:** 0 production hits, 0 padded-session hits. **reading-options:** 0 problems.
- **lint:** exit 1 with the same 3 errors as at `4f8ebea7` (on the reused cards 太 and 情, present at the batch base `2787e43b`) and 42 warnings (was 37). The 5 new warnings are on `kanji/母.md` (not in the N1 source index; no quizOnyomi; no quizKunyomi; no Metadata line) and on `words/お母さん.md` (no Dictionary line). They are older conditions of the base files, reported now because 母 is a changed card; the lint scope changed from 伯 to 母.
- **Other checks:**
  - manifest rebuild identical;
  - diffcheck clean from the batch base `2787e43b`;
  - validate 0 errors;
  - unittest 444 tests OK;
  - vocabulary 3201/3539.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Evidence added in this round

- `evidence\daijisen-kotobank.json` adds 叔母 and 叔父, each with its Digital Daijisen and 精選版 日本国語大辞典 sections from the same kotobank page (the 伯叔 entry stays for reference).
- `evidence\reading-lookalikes-c3.txt`: the look-alike readings of しゅくふ and しゅくぼ, produced by running the word-quiz audit's Python port of `ReadingOptions.mutations` unchanged, with the share of draws that include しゅくぶ. The look-alikes can also be derived by hand from `evidence\Words.kt` lines 223–246.
- `evidence\daijisen-weblio-叔.txt`: the Digital Daijisen character entry for 叔 (weblio.jp), cited by `kanji/叔.md` since the reviewed freeze; added here because the 叔 support choice cites its first sense.
- `evidence\jmdict-scan-c3.txt`: the same pinned-JMdict scan as `jmdict-scan-c2.txt` (the JMdict pin did not change); it already covers every spelling containing 叔.
