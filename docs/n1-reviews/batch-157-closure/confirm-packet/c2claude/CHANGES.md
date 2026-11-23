# Batch 157 revision: what changed from cd5d75d1 to 24201899

Your confirmation report reviewed `cd5d75d1`. The revised snapshot is `24201899`, three first-parent commits later (`81142e4a`, `0daebfba`, `24201899`). The range has no merges. Every commit in it is signed with key 9D94B9D311BD26A7 (`evidence\verify-commit.txt`). No other review round ran between the three confirmation reports and this revision. These changes answer the three confirmation reports only.

- **Changed:**
  - the batch cards 侍, 侯, 俵 and 倫;
  - the word article `words/倫理.md` (front matter only);
  - the ledger `docs/n1-sources/batch-157-progress.json`.
- **Unchanged:**
  - the other six batch cards: 佐 佳 併 侮 俊 俗;
  - the other nine word articles;
  - the reused cards 助 and 理;
  - `tools/`, the JMdict supplement files and every stroke file.
- **Front-matter changes:**
  - new `distractors` on 侍, 侯, 俵 and 倫;
  - 倫理's `quiz_exclusions` drops 仁.
  - No title changed.
- **Distractor sentences:** the four cards' Notes sentences name the new distractors.
- **Generated file:** `manifest.json` is regenerated (contentVersion `b6a770ce2d8d0049`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `kanji/侍.md` | 13 | distractors [父, 母, 子] → [父, 雨, 魚] |
| | 43 | the distractor sentence names 父 (“father”), 雨 (“rain”) and 魚 (“fish”). The clause “they name family members;” is removed. |
| `kanji/侯.md` | 13 | distractors [国, 京, 社] → [女, 国, 金] |
| | 39 | the distractor sentence names 女 (“woman, female”), 国 (“country”) and 金 (“gold, money”) |
| `kanji/俵.md` | 13 | distractors [田, 土, 木] → [田, 車, 本] |
| | 44 | the distractor sentence names 田 (“rice field”), 車 (“car, vehicle”) and 本 (“book, origin”) |
| `kanji/倫.md` | 13 | distractors [力, 事, 名] → [力, 時, 名] |
| | 34 | the 不倫 example now reads “immorality; especially infidelity, an extramarital affair” (was “infidelity; an extramarital affair”) |
| | 38 | the 倫理/不倫 contrast now reads “倫理 is ethics, while Digital Daijisen defines 不倫 as departing from morality, especially a sexual relationship with someone other than one's spouse” (was “ethics versus infidelity”). The sentence “倫 also appears in 五倫 ごりん, “the five Confucian filial-piety relationships.”” is removed. The rest of the line is unchanged. |
| | 40 | the distractor sentence names 時 (“time, hour”) instead of 事 (“matter, affair”) |
| | 42 | Metadata no longer lists JMdict entry 1593605 (五倫). The other entries and links are unchanged. |
| `words/倫理.md` | 8 | quiz_exclusions [道徳, 善, 仁] → [道徳, 善]. Lines 28 and 34 are unchanged: line 28 still gives JMdict's gloss of 仁 as another related moral concept, and line 34 still compares entry 1369620. |
| `docs/n1-sources/batch-157-progress.json` | 55 | 倫理's word-exclusion row is now ["道徳", "善"] |
| | 112, 114, 117, 118 | the `quizAudit` rows for 侍, 侯, 俵 and 倫: the new distractors and their card titles |
| | 127 | `batchAudit` adds “the first confirmation round's fixes” and names manifest `b6a770ce2d8d0049` (was `00777806885a6934`) |
| | 136 | `status` now lists the word exclusions “併用/用途 and 佳作/制作” (倫理/仁 removed) |

## Distractor choices

| Card (title) | At cd5d75d1 | Revised | Revised distractors' card titles |
|---|---|---|---|
| 侍 (samurai; retainer) | 父 母 子 | 父 雨 魚 | father; rain; fish |
| 侯 (marquis; feudal lord) | 国 京 社 | 女 国 金 | woman, female; country; gold, money |
| 俵 (straw bag; bale) | 田 土 木 | 田 車 本 | rice field; car, vehicle; book, origin |
| 倫 (ethics; moral principles) | 力 事 名 | 力 時 名 | power; time, hour; name |

- **Why they changed:** the confirmation reports judged that some sets can be rejected as one category. Examples are the family set on 侍, the nature set on 俵 and the places-and-institutions set on 侯, whose answer is a person's rank. One report also noted that 倫's distractor 事 “matter, affair” sits next to the card's own 不倫 example “affair”. Each revised set mixes categories, and 時 replaces 事.
- **Kept sets:**
  - 佐 (母 友 子 for “aide; assistant”) is kept. All four options name people, so the person category does not single out the answer. The set is not one closed family: 友 is a friend, not a relative.
  - 俊 (安 少 多 for “talented; outstanding”) is kept. All four titles are qualities or amounts, and no one category holds the three distractors without the answer.
  - Please judge both.
- **Starter cards:** every new distractor is a Starter card (`evidence\distractor-use.tsv`, lines 13–15 for 侍, 19–21 for 侯, 27–29 for 俵, and 26 and 30–31 for 倫; the starter tag is in column 4).
  - 雨, 魚, 女, 金, 車, 本 and 時 are new to these cards.
  - 父 (侍), 国 (侯), 田 (俵), 力 and 名 (倫) were already in the card's set.
  - The last column of `distractor-use.tsv` marks the cards that gained each distractor after cd5d75d1.
  - Lines 46–52 list the replaced distractors: 母 and 子 are still used by 佐, while 京, 社, 土, 木 and 事 are no longer used by any batch card.
- **Evidence:**
  - `evidence\distractor-senses.txt` lists every JMdict entry spelled with each single distractor character, including the replaced ones and the rejected candidates.
  - `evidence\prior-distractor-use.tsv` is the same table at cd5d75d1.
- **Titles:** taken from the distractor cards' own front matter. They match the titles in the ledger's `quizAudit` rows.

### Candidates rejected for this revision

`evidence\distractor-use.tsv` lines 67–77 give each reason. 男 is the only candidate ever committed on a card it was rejected for (侍, at `81142e4a`).

| Candidate | For | Reason |
|---|---|---|
| 友 | 侍 | 1539980 sense 2 “accompaniment; companion (e.g. book); complement; accessory”, close to an attendant |
| 手 | 侍 | 1327190 sense 4 “hand; worker; help” names a helper or worker |
| 女 | 侍 | 1344370 すけ “assistance; help; helper”, and the 侍 card's own 内侍 (1582520 “maid of honor; maid of honour; lady-in-waiting”) names a female attendant. 女 is used on 侯 instead. |
| 犬 | 侍 | precautionary: 1258330 sense 2 “squealer; rat; snitch; informer; informant; spy” |
| 足 | 侍 | 1709000 足軽 “common foot soldier (feudal Japan); samurai of the lowest rank” |
| 人 | 侍 | too generic: 1580640 sense 1 “person; someone; somebody” covers any samurai |
| 道 | 倫, 侍 | 1454080 sense 5 “way (of living, proper conduct, etc.); moral principles”; 1498620 武士道 “Bushido” |
| 男 | 侯, 侍 | for 侯: 2843485 sense 3 “baron”, a peerage rank. For 侍: too generic, like 人 (1419990 sense 1 “man; male”). It was committed on 侍 at `81142e4a` and replaced by 雨 in the next commit `0daebfba`, before any review (see Process notes). |
| 子 | 侯 | 2216440 sense 2 “viscount”, a peerage rank |
| 父 | 侯 | precautionary: 1497610 sense 3 “God; Father” could be read as a lord |
| 物 | 俵 | too generic: 1502390 sense 1 “thing; object; article; stuff; substance” |

### Points the author judged acceptable (please check them)

Line numbers are in `evidence\distractor-senses.txt`.

- **On 侍:**
  - **父** (line 101): 1497610 sense 2 “father (e.g. of a discipline); pioneer (e.g. of field of research); founder” and sense 3 “God; Father”. Neither is a samurai or a retainer.
  - **雨** (line 112): 1171900 “rain”, “rainy day; rainy weather” and “the November suit (in hanafuda)”.
  - **魚** (line 117): 1578010 “fish” only.
- **On 侯:**
  - **女** (line 138):
    - 1344370 すけ “assistance; help; helper” (sense 1) and colloquial “babe; chick; broad” (sense 2);
    - 1344930 sense 2 “female lover; girlfriend; mistress”;
    - 2742880 め sense 2 “smaller (of the two); weaker”.
    - None names a lord or a rank. The すけ “helper” sense is why 女 was rejected for 侍 (a retainer serves a lord) but kept for 侯.
  - **国** (line 156): 1592250 sense 5 “province (of Japan)” [historical]. This was already on 侯 at cd5d75d1.
  - **金** (line 164): 1242600 sense 10 “Jin dynasty” [historical], sense 11 “gold general” (a shogi piece, abbreviation), sense 7 “Friday” and sense 12 “testicles” (colloquial).
- **On 俵:**
  - **車** (line 224): 1323080 sense 2 “wheel; castor; caster”.
  - **本** (line 231):
    - 1522150 ほん sense 3 “main; head; principal” and sense 5 “counter for long, thin objects”;
    - 1260670 もと sense 10 “counter for plants or trees”.
    - 俵 ひょう is a counter for sacks (1583390 sense 2), but 本's counter senses are for other objects. The card title is “book, origin”.
- **On 倫:**
  - **時** (line 269): 1315840 sense 3 “chance; opportunity; season” and sense 4 “the times; the age; the day”. Neither is a moral principle.
  - The author did not put 時 on 侍, judging that 侍's component 寺 would make 時 a visual near-match there.

### What the new sets change in the reading quiz (`checks\reading-exposure.txt`)

The earlier output is `evidence\prior-reading-exposure.txt` (at cd5d75d1). Every batch card's three wrong options still come from its curated set, and the fallback is never consulted in the N1 stack, the All stack or the Starter practice session.

| Card (prompt) | At cd5d75d1: outcomes / drawable wrong options (line) | Revised (line) |
|---|---|---|
| 侍 (さむらい) | 4 / 5 (65) | 9 / 7 (65) |
| 侯 (コウ) | 3 / 5 (97) | 9 / 7 (97) |
| 俵 (たわら) | 2 / 4 (146) | 1 / 3 (146) |
| 倫 (リン) | 12 / 7 (160) | 6 / 6 (160) |

- **Latent readings:** the four are unchanged: 佳 けい and えい (lines 31, 34), 侍 かみ (line 68; held by 上 守 神 紙 髪, none of them a distractor) and 俗 しょく (line 130).
- **Totals:** 0 production hits, 0 padded-session hits, 4 latent collisions and 0 one-holder padded hits (lines 168–169), the same as at cd5d75d1.
- **Reading options:** `checks\reading-options.txt` reports 0 problems. Over 100 seeds it saw these numbers of wrong options:
  - 侍: 7 (line 59);
  - 侯: 7 (line 86);
  - 俵: 3 (line 131);
  - 倫: 6 (line 144).
- **Reading options at cd5d75d1:** 5, 5, 4 and 7 for the same four cards (`evidence\prior-reading-options.txt`).

### Word-quiz options (`evidence\word-quiz.txt`)

- **倫理** (block at lines 2076–2094):
  - The exclusions are 道徳 and 善 (line 2078).
  - 仁 “benevolence; compassion” now scores 7, above the last slot (line 2083). It is offered in every 倫理 meaning quiz, together with two of the eleven words tied at score 6 (lines 2084–2094). The tie is unchanged.
  - At the frozen draft a5c6a0ff, 仁 was also above the last slot, with only 道徳 excluded (the earlier confirmation packet's `evidence\freeze-word-quiz.txt`, lines 2069–2087). The first-round fixes added 善 and 仁 to the exclusions; this revision removes 仁 again.
- **Reverse pairs:** 814 at line 2171, up from 813 at line 2170 of `evidence\prior-word-quiz.txt`. The one new pair is 倫理 shown for 仁, at score 7 above the last slot (line 2796), so 倫理 is offered in every 仁 meaning quiz.
- **Other blocks:** no other block changed.
- **Reading quiz:** 121 reverse pairs (line 2986), and no ATTESTED problems (line 3109).

## Checks run on the revised snapshot (outputs in `checks\`)

- **quiz-safety:** 0 errors and 0 warnings. Option lines: 侍 line 8, 侯 line 12, 俵 line 18, 倫 line 20.
- **reading-exposure** and **reading-options:** see above.
- **lint** (`lean\n1_batch_tool.py lint --base e2c25363`): 1 error and 44 warnings, as at cd5d75d1. The error is the pre-existing unknown `phonetic` key in `kanji/語.md`, outside the batch.
- **audit** (`tools\audit_n1_batch.py --batch 157`): exit 0. It reports 10 kanji, 10 new words, 8 changed reused articles, 17 reading dispositions and 27 dictionary families, and the manifest is fresh (`b6a770ce2d8d0049`).
- **budget:** retained 56,739,555 bytes, inflated 57,175,627 and local ZIP 36,459,996 (+19, +19 and +5 bytes from cd5d75d1). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **Other checks:**
  - manifest: rebuilding gives an identical file;
  - diffcheck: clean from the batch base `e2c25363`;
  - validate: 0 errors;
  - unittest: 439 tests OK;
  - vocabulary: 3201/3539;
  - `checks\link-targets.tsv` (written by the packet builder): every link on a changed line and its target.
- **Also in `evidence\`:**
  - `meta-scan.txt`: the same two part-of-run matches as before (佐.md:40 助け, 併.md:39 合わせ);
  - `corpus-attested.txt`, `weblio-不倫.txt` and `Words.kt` (as in the earlier confirmation packet);
  - `verify-commit.txt`.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Process notes

- **No other review rounds:** no review ran on `81142e4a` or `0daebfba`. RESPONSE.md lists the changes made for the other two confirmation reports under “Changes made for the other reviews”.
- **Intermediate 侍 set:** `81142e4a` set 侍's distractors to [父, 男, 魚]. The author then judged 男 too generic, like the rejected 人, and `0daebfba` replaced it with 雨. `diffs\fix.patch` shows only the net change.
- **Ledger refresh:** `24201899` changes only ledger line 127, the audit sentence and manifest version.
- **倫理 line 28:** the comparison with 仁 in the body is kept; only the exclusion is removed.
