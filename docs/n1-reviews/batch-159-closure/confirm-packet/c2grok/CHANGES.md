# Batch 159 revision: what changed from 5c04be73 to bad899ea

The revised snapshot is `bad899ea`. The range `5c04be73..bad899ea` has five commits and no merges:
- `4f8ebea7`, “N1 B159: apply second-round review fixes” (parent `5c04be73`);
- `54b00e0c`, “N1 B159: apply third-round review fixes” (parent `4f8ebea7`);
- `f85ff382`, “N1 B159: apply a third-round review note” (parent `54b00e0c`);
- `0ba7df63`, “N1 B159: correct the ledger's lint warning count” (parent `f85ff382`);
- `bad899ea`, “N1 B159: correct the ledger's reading-options note” (parent `0ba7df63`).

Every commit from the reviewed freeze `1a9bb910` through `bad899ea` is signed with key D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (`evidence\verify-commit.txt`). `diffs\fix.patch` and `diffs\changed-lines.txt` show the combined change from `5c04be73`; the intermediate snapshots `4f8ebea7`, `54b00e0c`, `f85ff382` and `0ba7df63` are not in this packet.

This revision answers the confirmation reports made since `5c04be73`:
- on `5c04be73`, two reviewers (one of them you) confirmed with no findings, each with optional notes; a third reviewer found two points only partly resolved (NEEDS FIX) and added one optional note;
- `4f8ebea7` answered those reports. On it, one reviewer confirmed with one optional note, and the third reviewer confirmed every point except the 叔 support row (NEEDS FIX), described below. You did not review `4f8ebea7`;
- `54b00e0c` answers the reports on `4f8ebea7`;
- `f85ff382` applies one optional note from a confirmation report on `54b00e0c`: the new 叔母 line on `kanji/母.md` gives the usual reading おば first, as the 叔 card does;
- `0ba7df63` answers a confirmation report on `f85ff382`, which found that the ledger's lint statement (line 948) still gave the warning count from before `kanji/母.md` entered the lint scope (see “The new statement against the lint output” below);
- `bad899ea` applies an optional note of a confirmation report on `0ba7df63`: the ledger's reading-options statement (line 953) named only one of the two informational notes in `checks\reading-options.txt` (see “The new reading-options statement” below).

`RESPONSE.md` answers your own report on `5c04be73` only.

- **Changed:**
  - the 叔 support article: `words/伯叔.md` is deleted and `words/叔母.md` (reading しゅくぼ, JMdict entry 1607100) is added;
  - the batch card `kanji/叔.md`: the シュク Readings row (line 29), the Common words list (lines 33–34) and one Notes paragraph (line 38);
  - the batch card `kanji/吟.md`: one front-matter line (14) and one Notes line (42);
  - the existing card `kanji/伯.md`: restored to its text at the batch base `2787e43b` (the 伯叔 line is removed; `git diff 2787e43b bad899ea -- kanji/伯.md` is empty);
  - the existing card `kanji/母.md`: one Common words line added (line 38);
  - the word articles `words/太后.md` (line 15) and `words/吟味.md` (line 24), one body line each;
  - the ledger `docs/n1-sources/batch-159-progress.json`: the selection statement (line 29), the 叔 support mapping (lines 71–81), the 叔 reciprocal pair (line 186), the changed reused passage (lines 219–221, now 母 instead of 伯), the word-quiz exclusion row for the 叔 support word (lines 279–283), the 吟 kanji-exclusion row (lines 429–430), the 叔 シュク reading row (lines 522–526), the lint check note (line 948), the quiz-safety check note (line 950), the reading-options check note (line 953) and the status (line 955).
- **Unchanged:**
  - the other eight batch cards, and the 吟 card's title, readings, distractors and tags;
  - the other seven new word articles, and every other existing card or article changed earlier in the batch (太 官 不 味 情 服 贈, また, または);
  - `tools/`, the pinned JMdict selection and extract (still 87 complete families: entries 1607070, 1607100 and 1474270 were already cited by the 叔 card), every stroke file and every other file.
- **Generated file:** `manifest.json` is regenerated (contentVersion `18c1f24ea8d2caf8`; was `92143d996fc2aff4` at `5c04be73`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot. `diffs\changed-lines.txt` has the old and new text of every changed line.

## The 叔 support: 叔母 (しゅくぼ)

At `5c04be73`, the 叔 row used the untagged 伯叔 and said that no candidate qualifies through a reading of 叔. Another review held that this is wrong under the letter of point 2 of the issue #60 rule (`evidence\rule-7058679348.md`): a tagged spelling qualifies when its reading uses a KANJIDIC2 reading of the kanji and carries no excluded mark; the reading itself need not be tagged. `4f8ebea7` kept 伯叔 as an author's exception reported to the owner; the same reviewer then asked for the qualifying fallback, or for the owner's explicit acceptance before publication. `54b00e0c` follows the letter of point 2. There is no author's exception left in this row.

- **Qualification.** JMdict entry 1607100 (`evidence\jmdict-cited-entries.xml`): the spelling 叔母 carries ichi1/news1/nf20; the reading おば carries ichi1/news1/news2/nf20/nf30; the reading しゅくぼ is restricted (`re_restr`) to 叔母 and carries no priority tag and no `re_inf` mark; the spelling carries no `ke_inf` mark. しゅくぼ uses シュク, a KANJIDIC2 on reading of 叔, and ボ for 母. The other kanji, 母, has a card. Sense 1: “aunt”, with the note “伯母 can mean older and 叔母 can mean younger than one's parent”.
- **Sources for the meaning.** Digital Daijisen, しゅく‐ぼ【叔母】: 「父母の妹。おば。」; 精選版 日本国語大辞典, しゅく‐ぼ【叔母】: 「〘名詞〙 父母の妹。おば。」, with no variant reading (`evidence\daijisen-kotobank.json`, captured from https://kotobank.jp/word/%E5%8F%94%E6%AF%8D-528307). The Joyo table lists 叔母 おば among the whole-word special readings (`evidence\joyo\p162.txt`) and 伯叔 as its example for シュク (`evidence\joyo\p75.txt`).
- **Why not 叔父 (しゅくふ).** 叔父 (entry 1607070) qualifies in the same way: the spelling has ichi1/news1, and しゅくふ is restricted to it and unflagged. It is not used because 精選版 日本国語大辞典 gives a variant reading: しゅく‐ふ【叔父】「〘名詞〙 ( 「しゅくぶ」とも ) 父母の弟。おじ。」 (`evidence\daijisen-kotobank.json`, from https://kotobank.jp/word/%E5%8F%94%E7%88%B6-528298). The word reading quiz draws two of its generated look-alike readings at random (`evidence\Words.kt`: `ReadingOptions.mutations`, lines 234–246, and `ReadingOptions.build`, lines 256–268, where line 263 takes the first two of the shuffled look-alikes). For しゅくふ the look-alikes are じゅくふ, しゅぐふ, しゅっくふ, しゅくぶ and しゅくぷ, so a 叔父 article would show the attested しゅくぶ as a “wrong” option in 4 of the 10 equally likely draws. The app has no way to exclude a reading option. The look-alikes for しゅくぼ are じゅくぼ, しゅぐぼ, しゅっくぼ, しゅくほ and しゅくぼう; none is a recorded reading (`evidence\reading-lookalikes-c3.txt`, produced by running the word-quiz audit's Python port of `mutations` unchanged; `evidence\word-quiz.txt` line 96, where the audit checks each look-alike against JMdict). 叔母 also matches the 叔 card's title, “uncle or aunt (younger than a parent)”, as well as 叔父 does, and Digital Daijisen's first sense of 叔 cites both: 「１ 父・母の年下のきょうだい。「叔父・叔母」」 (`evidence\daijisen-weblio-叔.txt`, the extract behind `kanji/叔.md:23`).
- **What the article teaches.** `words/叔母.md` teaches the reading しゅくぼ and says plainly, in “Distinctive meaning” (line 32), that 叔母 is also read おば, which is the Joyo special reading and the reading JMdict tags, and that not every printed 叔母 is pronounced しゅくぼ. `words/身体.md` (しんたい, also read からだ) is an existing article that teaches the on reading of a spelling with a common alternative reading.
- **The 叔 card.** The シュク Readings row (line 29) now leads with the linked 叔母 しゅくぼ and gives Digital Daijisen's definition 父母の妹, then 叔父 しゅくふ, then the unlinked 伯叔 はくしゅく (still the Joyo table's example; entry 1474270 is still cited). The Common words line for 叔母 (line 34) links the article: “[叔母](../words/叔母.md) おば, also しゅくぼ — aunt (written 叔母 when younger than one's parent)”. The former 伯叔 Common words line is removed. The Notes paragraph (line 38) adds: “Read with シュク, 叔父 is しゅくふ and 叔母 is しゅくぼ; JMdict restricts these readings to those spellings.” Its earlier sentence, that おじ and おば are whole-word special readings and not readings of 叔 alone, is unchanged.
- **Reciprocal links.** `words/叔母.md` links `../kanji/叔.md` and `../kanji/母.md` (line 24); `kanji/叔.md` links `../words/叔母.md` (lines 29 and 34); `kanji/母.md:38` adds “[叔母](../words/叔母.md) おば, also しゅくぼ — aunt (a parent's younger sister)”.
- **伯.** `kanji/伯.md` no longer needs the 伯叔 link and is back to its B158 text. The ledger's changed-reused-passages list names 母 instead of 伯.
- **B156.** The published B156 row for 伯 (伯仲, kept because the tags of 伯父 and 伯母 belong to the whole-word readings おじ and おば) is not changed by this batch. `evidence\b156-selection.json` is an excerpt of that ledger. Whether B156 should be aligned with the letter of point 2 is a question for the owner, outside this batch.

Ledger line 81 (the 叔 `note`, which replaces the former `exceptionReason`) reads, in full:

> The spelling 叔母 carries ichi1/news1 (the reading おば also carries ichi1/news1). The reading しゅくぼ, restricted to 叔母, carries no priority tag and no irregular, rare, outdated, ateji, or gikun mark, and it uses the KANJIDIC2 reading シュク. 叔父 (entry 1607070) qualifies in the same way, with the reading しゅくふ, but it is not used: 精選版 日本国語大辞典 gives しゅくぶ as a variant reading of 叔父, and the reading quiz can generate しゅくぶ from しゅくふ as a look-alike wrong option. Neither Digital Daijisen nor 精選版 日本国語大辞典 gives a variant reading for 叔母 しゅくぼ.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `words/伯叔.md` | all | deleted |
| `words/叔母.md` | 1–34 | new article (see above) |
| `kanji/叔.md` | 29 | シュク row: “[叔母](../words/叔母.md) しゅくぼ — aunt; Digital Daijisen defines it as a younger sister of one's father or mother (JMdict entry 1607100); 叔父 しゅくふ — uncle; Digital Daijisen defines it as a younger brother of one's father or mother (JMdict entry 1607070); 伯叔 はくしゅく — brothers; one's father's brothers (JMdict entry 1474270)” (伯叔 was first and linked) |
| | 33–34 | the plain “叔母 おば” line and the 伯叔 line become one linked line (quoted above) |
| | 38 | adds the sentence quoted above |
| `kanji/吟.md` | 14 | `quiz_exclusions` [詩, 歌, 謡, 句, 検, 審, 査, 調, 究, 研] → [詩, 歌, 謡, 句, 検, 審, 査, 調, 究, 研, 験] |
| | 42 | the list of examining neighbours adds 験 (“test; verify”): “…究 (“investigate thoroughly”), 研 (“polish; study closely”) and 験 (“test; verify”) overlap with the sense of examining something closely, as in 吟味.” |
| `kanji/伯.md` | (old 39) | the 伯叔 line is removed; the file equals its B158 text |
| `kanji/母.md` | 38 | the new 叔母 line, after 母語: “[叔母](../words/叔母.md) おば, also しゅくぼ — aunt (a parent's younger sister)” |
| `words/太后.md` | 15 | the last sentences now read: “In plain terms, Digital Daijisen describes 太皇太后 as the empress of the emperor two reigns back and 皇太后 as the empress of the previous emperor. In a narrower sense, 皇太后 is such an empress who is also the current emperor's birth mother.” (your optional note on “or one who is also”) |
| `words/吟味.md` | 24 | the last sentences now read: “Both sources mark poetry recitation as the original meaning of 吟味. Digital Daijisen sense 3 is reciting a poem and savoring its flavor, and JMdict sense 4 (archaic) is “reciting and appreciating traditional poetry”.” (your optional note on “savoring” in both sources) |
| `docs/n1-sources/batch-159-progress.json` | 29 | `selectionReason`: two rows (后 吏) take the untagged route; “The 叔 row uses 叔母 (entry 1607100): its spelling carries ichi1/news1, and its reading しゅくぼ, restricted to that spelling, uses シュク; its support mapping explains why the equally tagged 叔父 is not used.” The 叔 entry in the untagged list is removed. |
| | 71–81 | 叔 mapping: article `words/叔母.md`, primary reading しゅくぼ, entry 1607100, priority tags ichi1/news1; `exceptionReason` is replaced by a `note` (quoted above) |
| | 186 | reciprocal pair 叔 ↔ `words/叔母.md` |
| | 219–221 | changed reused passage: `kanji/母.md` (was `kanji/伯.md`) |
| | 279–283 | word-quiz exclusions: 叔母 → 伯母さん, 親戚, 親類 (was 伯叔 → 兄弟, おじさん, 親戚) |
| | 429–430 | the 吟 kanji-exclusion row adds 験 (generated from the front matter) |
| | 522–526 | 叔 シュク reading row: “The supported common-word article 叔母 directly uses シュク.”, entry 1607100 |
| | 948 | `mechanicalChecks.n1Lint`: the warning count is corrected (see “The new statement against the lint output” below) |
| | 950 | `mechanicalChecks.quizSafety`: corrected (see “Correction to the earlier statements” below) |
| | 953 | `mechanicalChecks.readingOptions`: names both informational notes (see “The new reading-options statement” below) |
| | 955 | `status`: “The 后 and 吏 untagged-support exceptions and the kana-headed 又 support remain subject to review.” (叔 is no longer listed) |

## 吟 and 験

Another review asked to exclude 験 (“test; verify”), because Digital Daijisen's first sense of 験, 証拠によって確かめる, overlaps 吟's taught sense 内容を探り確かめる. `kanji/吟.md:14` adds 験 to `quiz_exclusions`, and line 42 names it with its title. The curated meaning distractors 二 自 社 are unchanged (`checks\quiz-safety.txt` line 16). The exclusion check is symmetric (`evidence\QuizBuilder.kt` line 26). Adding 験 therefore removes 験 as a fallback meaning option for 吟, keeps 吟 out of 験's fallback meaning options, and stops 吟 and 験 from appearing together as wrong options for a third card (line 30). 験's own curated distractors are unaffected. Reading questions do not use `quiz_exclusions`: they exclude only the target's own readings (`evidence\KanjiReadings.kt` lines 80–88 and 100).

## Correction to the earlier statements

The `5c04be73` packet's CHANGES.md (under “Points the author judged acceptable”) and one RESPONSE said that 吟's curated distractors 二 自 社 “fill all three slots in every shipped pool”, citing `checks\quiz-safety.txt` line 16 and `checks\reading-options.txt` line 108. The old ledger quiz-safety note said that each card's curated distractors fill all three wrong options of its meaning and reading questions. Both statements were wrong for 吟's reading question.

- **Meaning question.** The statements hold. 二 “two”, 自 “self, oneself” and 社 “company, shrine” have distinct titles, and none is excluded, so they fill all three wrong options (`checks\quiz-safety.txt` line 16; `evidence\QuizBuilder.kt` lines 26–34). The 吟 `quiz_exclusions`, including 験, therefore matter only in fallback or custom pools.
- **Reading question (ギン).** The statements are wrong. 二 offers ニ or ジ, 自 offers ジ or シ, and 社 offers シャ. Each curated card gives one random reading, and a repeated reading is dropped (`evidence\KanjiReadings.kt` lines 100 and 110). In one of the four outcomes, 二 and 自 both show ジ, and the closeness fallback fills the open slot (line 111). `checks\reading-exposure.txt` lines 138–150 report “deficit 0/1: the fallback fills the open slots”: 61 drawable wrong options in the N1 and All stacks (4 curated, 57 fallback) and 27 in Starter practice sessions (4 curated, 23 fallback). `checks\reading-options.txt` lines 108–119 list the 57 tier-3 fallback keys and see 19 wrong options over 100 seeds. The totals at the end of `checks\reading-exposure.txt` report 0 production and 0 padded-session hits. `checks\quiz-safety.txt` line 17 (“wrong options from distractors 3/3”) counts the three curated cards; it does not model the shared ジ.
- **The other nine cards.** Their curated options fill all three wrong slots of every reading prompt in every outcome; the fallback is never consulted (`checks\reading-exposure.txt`).
- **Ledger line 950** now says this: the meaning questions are filled by the curated distractors; for 吟's ギン prompt, the fallback fills the open slot in one of four outcomes, with no exposure hit.

The card's distractors are unchanged: the fallback options are readings of other cards, the audit finds no hit, and existing cards also rely on fallback options (`checks\quiz-safety.txt` lines 22–33 list 11 existing cards whose curated distractors fill only two of three slots).

## Quiz options

- **Word quiz, 叔母** (`evidence\word-quiz.txt` lines 70–97).
  - Meaning: no curated options. The reachable options are 父母 “father and mother; parents” and 祖母 “grandmother” (score 8) and the score-7 tier of family nouns (lines 77–93). `quiz_exclusions` removes 伯母さん “aunt” (same meaning), and 親戚 and 親類 “relative; kin” (a broader term that covers an aunt). Exclusion is symmetric (`evidence\Words.kt`).
  - Reading: the JMdict readings of 叔母 are おば and しゅくぼ (line 95). Two wrong options are drawn from the look-alikes listed above, none of them a recorded reading. The third comes from the closeness tier お母さん おかあさん, 伯母さん おばさん and 母親 ははおや (line 97). おばさん is the reading of 伯母さん and 叔母さん, not of the bare spelling 叔母, so it is a wrong option here. おば itself never appears: no word article has the reading おば, and no look-alike of しゅくぼ produces it. The audit reports 0 attested or too-few-candidate problems (line 1436).
  - Reverse direction: 叔母 can appear as a wrong option in other words' quizzes (the reverse section of `evidence\word-quiz.txt`), mostly in family words, whose titles differ from “aunt (a parent's younger sister)”.
- **Word quiz, other words.** 伯叔 is gone from the pool. 太后 and 吟味 keep their front matter, so their option sets are unchanged.
- **Kanji quiz.** `checks\quiz-safety.txt`, `checks\reading-exposure.txt` and `checks\reading-options.txt` are identical to the `5c04be73` outputs apart from the header line. 吟's meaning options are still 二 自 社.

## The new statement against the lint output

At `5c04be73` and `4f8ebea7` the lint reported 37 warnings, and ledger line 948 said: “Of the 37 warnings, 35 are on reused cards and words.” At `54b00e0c`, `kanji/母.md` (four warnings) and `words/お母さん.md` (one warning) entered the lint scope and the count became 42, but the ledger sentence was not updated. `0ba7df63` changes it to: “Of the 42 warnings, 40 are on reused cards and words. They report a missing N1 source-index entry, quiz reading list or Metadata line, or a missing Dictionary line or one that cites no JMdict entry id; B159 changes none of these fields, because it only adds or links one Common words line on each of those cards and does not change those word articles.” The rest of the statement is unchanged.

- `checks\lint.txt` ends “3 error(s), 42 warning(s)”. Two warnings are on `kanji/又.md` (the また examples または and また). The other 40 are on eight reused cards and twelve reused word articles:
  - 28 on the cards 不 味 太 官 情 服 母 贈: “not in the N1 source index; source comparison skipped” (8), “no quizOnyomi” (8), “no quizKunyomi” (8) and “no Metadata: line” (4: 不 味 服 母);
  - 12 on the word articles お母さん 不潔 不規則 不運 味 和服 太る 太鼓 官庁 服 洋服 調味料: “no Dictionary: line” (5: お母さん 味 太る 服 洋服) and “Dictionary: line cites no JMdict entry id” (7).
- `evidence\reused-lint-diff.txt` (new) shows everything B159 changes in those 20 files, from the batch base `2787e43b` to `bad899ea`: seven cards gain one Common words line each, the existing 贈呈 line on `kanji/贈.md` gains a link, and none of the twelve word articles changes.

## The new reading-options statement

Ledger line 953 (`mechanicalChecks.readingOptions`) said: “lean reading_options.py with the same --extra list: 0 problems. The only informational note is 呉 ぐ, a KANJIDIC2 name-only reading offered by 供, 具, 工 and 求.” `bad899ea` changes it to: “lean reading_options.py with the same --extra list: 0 problems. Two informational notes concern KANJIDIC2 name-only readings that the tool marks as drawable from the fallback: 吉 き on the キツ prompt, offered by 28 cards (among them 気, 期 and 記), and 呉 ぐ on the ゴ prompt, offered by 供, 具, 工 and 求. On both prompts the curated options fill all three wrong slots in every outcome, so the fallback is never consulted, and reading_exposure.py lists both readings among the latent collisions.”

- `checks\reading-options.txt` has two informational notes (“info (can be drawn)”): line 74, on 吉's キツ prompt, for き, offered by 28 cards; and line 147, on 呉's ゴ prompt, for ぐ, offered by 供 具 工 求. Both notes are in the reading-options output of every round since the reviewed freeze `1a9bb910`; only the ledger sentence left out 吉 き.
- `checks\reading-exposure.txt` lines 82 and 175: on both prompts the curated options fill all three wrong slots in every outcome, and the fallback is never consulted. Lines 88 and 178 say that き and ぐ cannot be drawn in the N1 stack, All stack or Starter practice session pool; they are among the 10 latent collisions counted on line 186.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `5c04be73`, except the numbers named here. `checks\link-targets.tsv` is not a check output: the packet builder writes it for the changed lines of this packet's range only, so it differs between packets by design. In this packet it lists the 9 links on the changed lines of `5c04be73..bad899ea`, all resolved.

- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0; 87 complete JMdict families; the manifest is fresh (`18c1f24ea8d2caf8`). The audit checks the 叔 mapping (reading, new article, entry ids in the extract families, the spelling and reading pair, reciprocal links).
- **budget:** retained 56,881,426 bytes, inflated 57,317,498 and local ZIP 36,535,519 (+606 retained bytes from `5c04be73`). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety:** 0 errors, 0 warnings. **reading-exposure:** 0 production hits, 0 padded-session hits, 0 one-holder padded hits and the same 10 latent collisions. **reading-options:** 0 problems.
- **lint:** exit 1 with the same 3 errors as at `5c04be73` (on the reused cards 太 and 情, present at the batch base `2787e43b`) and 42 warnings (was 37). The 5 new warnings are on `kanji/母.md` (not in the N1 source index; no quizOnyomi; no quizKunyomi; no Metadata line) and on `words/お母さん.md` (no Dictionary line). They are older conditions of the base files, reported now because 母 is a changed card; the lint scope changed from 伯 to 母. Ledger line 948 now gives these counts.
- **Other checks:**
  - manifest rebuild identical;
  - diffcheck clean from the batch base `2787e43b`;
  - validate 0 errors;
  - unittest 444 tests OK;
  - vocabulary 3201/3539.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Evidence added since the `5c04be73` packet

- `evidence\daijisen-kotobank.json` adds 叔母 and 叔父, each with its Digital Daijisen and 精選版 日本国語大辞典 sections from the same kotobank page (the 伯叔 entry stays for reference).
- `evidence\reading-lookalikes-c3.txt`: the look-alike readings of しゅくふ and しゅくぼ, produced by running the word-quiz audit's Python port of `ReadingOptions.mutations` unchanged, with the share of draws that include しゅくぶ. The look-alikes can also be derived by hand from `evidence\Words.kt` lines 223–246.
- `evidence\daijisen-weblio-叔.txt`: the Digital Daijisen character entry for 叔 (weblio.jp), cited by `kanji/叔.md` since the reviewed freeze; added here because the 叔 support choice cites its first sense.
- `evidence\b156-selection.json`: an excerpt of the published B156 ledger (`docs/n1-sources/batch-156-progress.json`): its status, its selection statement and its 伯 support row.
- `evidence\KanjiReadings.kt`: the app's kanji reading-question builder (`KanjiReadingQuiz`), from kanji-cards-android commit `91e1d4b578859f7bfb582f7b9c6acf48c6ca6a75` (Git blob `492a43c315816fbdf2079ee8c0bb05c731136b5c`).
- `evidence\app-code-SOURCES.json`: the pinned Android commit with the Git blob id, raw URL and web URL of each app file. `KanjiReadings.kt`, `QuizBuilder.kt` (blob `47ce071b…`) and `Words.kt` (blob `9c8b2c82…`) in this packet match the listed blobs (`git hash-object --no-filters` on the raw bytes; the files keep their CRLF line ends).
- `evidence\verify-commit.txt`: `git verify-commit -v` for every commit from `1a9bb910` through `bad899ea`, and `git log --show-signature` for `2787e43b..bad899ea`.
- `evidence\reused-lint-diff.txt`: everything B159 changes in the 20 reused files with lint warnings (see “The new statement against the lint output”).
- `evidence\jmdict-scan-c6.txt`: the same pinned-JMdict scan as `jmdict-scan-c1.txt` in the `5c04be73` packet (the JMdict pin did not change); it covers every spelling containing 叔.
