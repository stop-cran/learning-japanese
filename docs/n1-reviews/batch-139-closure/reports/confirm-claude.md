# Confirmation report: batch 139

**Snapshot:** commit 3b6f972767928e01261440466899f32df398d7f1. The reviewed snapshot was a47efe9af926316eaa86656033bf6e109f2be697. Reviewer model: Claude (Anthropic).

**Scope:** files I opened, and how deeply.

Confirm packet `confirm-139-claude`:
- Read in full:
  - `INSTRUCTIONS.md`
  - `RESPONSE.md`
  - `diffs\fix.patch`
  - the revised cards `snapshot\kanji\嫁.md`, `嬢.md`, `宣.md` and `峠.md`
  - `snapshot\words\宴会.md`
  - in `evidence\`: `README.md`, `weblio-岬-character.txt`, `QuizBuilder.kt` and `extras-correction.txt`
  - in `checks\`: `quiz-safety.txt`, `link-targets.tsv`, `lint.txt`, `linkplan.txt`, `validate.txt`, `unittest.txt` and `kanji-remarks.txt`
- Read in part:
  - `snapshot\kanji\岬.md`, lines 21–27.
  - `evidence\jmdict-cited-entries.xml`: I extracted all ten entries (1191680, 1694880, 2836096, 2230740, 2216510, 1340820, 2096040, 2842102, 1433030, 1251110).
  - `checks\reading-exposure.txt` and `checks\reading-options.txt`: compared line by line with the original files; I read the changed lines and the tail lines.
- Hashes only: all 15 files in `snapshot\kanji\`. The 11 cards declared unchanged are byte-identical to the original packet.
- Read in full in a follow-up turn: `CHANGES.md` (lines 1-40 and 41-76), `diffs\changed-lines.txt`, `evidence\word-remarks.json`, `checks\budget.txt`, `checks\vocabulary.txt` and `checks\manifest.txt`.
- Read in part in the follow-up: `evidence\meta-scan.txt` (first 8 lines, and the lines matching お嬢, 伝え and 嬢さん); `evidence\QuizBuilder.kt` line 26; `checks\reading-options.txt` line 196.
- Listed but not opened: `KanjiReadings.kt`, `Words.kt`, `meta_scan.py` and `packet-manifest.json`.

Original packet `batch-139-a47efe9a`, read-only:
- `evidence\audits\reading-exposure.txt` and `reading-options.txt`, for the line comparison; `evidence\audits\quiz-safety.txt`, by hash comparison.
- In the follow-up: `mechanical-checks.md` lines 7-9, and `evidence\provenance.json` line 365.
- `evidence\jmdict-families.xml`, programmatically: every entry with a 宣 spelling read with の-.
- `snapshot\kanji\*.md`, for hashes only.

My own `reports-139\initial-claude.md`, as context from round 1.

**Dispositions:**
- **C1 – RESOLVED.** `宣.md:40` now adds "JMdict notes it was originally respectful and is nowadays often used sarcastically." This accurately paraphrases the s_inf of JMdict 2842102, "originally respectful language; nowadays oft. used sarcastically." The row still says the word is not quizzed.
- **C2 – RESOLVED.** `嫁.md:23` now reads "its third sense, which JMdict marks as Kansai dialect, is 'wife.'" JMdict 1191680 sense 3 carries `<dial>Kansai-ben</dial>` and the gloss "wife."
- **O1 – RESOLVED.** The new bullet at `嬢.md:47` matches the JMdict entries:
  - 1694880 お嬢様: sense 1 "(another's) daughter" is polite, and "polite" is attached only to that sense. Sense 2 "young lady (of pampered upbringing)" is a real gloss.
  - 2836096 嬢ちゃん: "young girl; young lady".
  - 2230740 嬢さん じょうさん: "(another's) daughter" and "young lady (esp. of respectable upbringing)". See Optional for a small truncation.
  - 2216510 嬢さん とうさん: honorific and Kansai-ben, "daughter (of a good family)".
  - The Metadata line at line 51 adds all four entry IDs.
- **O2 – RESOLVED.** `宣.md:31` now names のべる, のる and のたまう. This matches the Daijisen line ［訓］のべる のる のたまう, which RESPONSE cites from the original packet's `evidence\public-source\weblio-宣.txt`; I did not reopen that file this round. I checked the JMdict claims directly:
  - In 1340820, 宣べる is a "rarely used kanji form" of 述べる, "to state; to express; to say".
  - 2096040 宣べ伝える is "to proclaim (e.g. gospel)".
  - A scan of the original `jmdict-families.xml` finds only five entries that spell a word with 宣 and read it with の-: 述べる, 宣べ伝える, 宣ふ, 宣わく and 宣う. So 宣べ伝える is the only one with a のべ main spelling, and no entry writes のる with 宣.
  - The Metadata line at line 57 adds 1340820 and 2096040.
- **O3 – RESOLVED.** `words\宴会.md:32-33` now reads "…the kind of gathering. The on readings are / エン + カイ." It reads naturally, and the rest of the article is unchanged. `linkplan.txt` reports 0 problems with 4 declared remark edits.
- **O4 – DECLINE ACCEPTED.** I had already judged the title "mountain pass; peak; climax" acceptable. The card explains the "worst point" sense at line 23.

**岬 limit:** resolved. `evidence\weblio-岬-character.txt` contains the Daijisen character entry `こう【▽岬】 … ［音］コウ（カフ）（漢）［訓］みさき`, with one sense, みさき, and the example 岬角. The ▽ in that headword is the mark this card explains at line 27: the official table does not give 岬 this reading. That supports "outside the official table" for コウ. The file also contains the word entry みさき【岬／▽崎】 "海や湖などに細長く突き出ている陸地" and the word entry さき【崎／▽岬／…】. Together these support `岬.md:23`, `:25` and `:27` as written.

**Other changed hunks:**
- **峠, removal of the 通 and 経 exclusions** (`峠.md:14`, `:48`, `:49`, `:51`). Acceptable.
  - In both directions, "pass through; commute" and "pass through; sutra" are defensibly wrong against "mountain pass; peak; climax". The two titles share only the English word "pass", and the new Notes bullet at line 49 makes that contrast explicit.
  - The paraphrases of 通る and 経る at line 49 are faithful to 1433030 ("to go by; … to pass through") and 1251110 ("to pass; to elapse; … to pass through"). They are not quoted as glosses.
  - The 峠 meaning options still use 3 of 3 curated distractors (岸, 島, 上). Neither 通 nor 経 appears in the fallback list, so the change has no observable effect on any current quiz.
  - `link-targets.tsv` shows that the quoted titles at lines 48-49 equal the target titles.
- **Reading-audit extras** (宗 たっと.ぶ, 宣 の.る). I compared the old and new audit files line by line. The only differences are the lines declared in `extras-correction.txt`: lines 1, 46 and 95 of exposure; lines 1, 37, 72 and 80 of options.
  - The tail counts are unchanged: 0 production hits, 0 padded hits, 11 latent collisions and 1 options problem (岬 さき, latent).

**CHANGES.md check (follow-up):** I checked every claim in `CHANGES.md`. None is false in substance.
- Card changes: claims match `fix.patch`, the hash comparison and `diffs\changed-lines.txt` (嫁 23; 嬢 47, 51; 宣 31, 40, 57; 峠 14, 48-49, 51; 宴会 32).
- Front matter: only 峠 `quiz_exclusions` changed.
- Exclusion rule: `QuizBuilder.kt` line 26 excludes a pair when either card lists the other.
- `checks\quiz-safety.txt`: hash-identical to the original packet's file.
- Checks:
  - `lint.txt`: the same two warnings as the original `mechanical-checks.md` lines 7-9.
  - `unittest.txt`: 436 OK. `validate.txt`: 0 errors.
  - `budget.txt`: a size summary with no error. `vocabulary.txt`: 3201 of 3336.
  - `manifest.txt`: the sha256 is the same before and after the rebuild, and the tree is clean.
  - `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `word-remarks.json`: only the 宴会 entry covers line 32; the other three entries match the edits I verified in round 1.
- `reading-options.txt` line 196: the 岬 さき HIT, offered by 先.
- `provenance.json` line 365: supports the claim that `jmdict-families.xml` holds every JMdict family that writes a batch kanji.
- `meta-scan.txt`: reports 0 whole-run gaps and 34 part-of-run matches, and lists the three new ones (お嬢 in お嬢様 at 嬢:47; 伝え and 伝える in 宣べ伝える at 宣:31).

Two wording inaccuracies, neither a defect in shipped content:
- `CHANGES.md` says 1531190 (嬢:51) and 1896840 (峠:51) "move before" the new IDs. In `fix.patch` they stay where they were, at the end of the old list, and the new IDs are appended after them.
- In the 宴会 row, "this revision changes only the colon" understates the edit: the colon becomes a full stop and "The on readings are" is added. The table gives the exact text, so nothing is hidden.

**Verdicts:**
- Correctness: CLEAN (all 15 cards; changed hunks in 嫁, 嬢, 宣, 峠 and 宴会 verified against the JMdict entries)
- Scoped coverage: CLEAN
- Consistency and quiz safety: CLEAN
  - The post-fix meaning options for all 15 cards in `quiz-safety.txt` are unchanged from round 1, and I judged them defensibly wrong then. The checks report 0 errors.
  - The reading-quiz audits show no production or padded-session hits. The 宗 し and 岬 さき collisions remain latent.
- Comprehensibility: CLEAN. `宣.md:31` is denser than before but still readable.

**Confirmation:** CONFIRMED

**Findings:** none new.

**Optional:**
- `嬢.md:47` quotes the second gloss of 嬢さん じょうさん as "young lady". The JMdict gloss is "young lady (esp. of respectable upbringing)". The truncation drops a qualifier, but the quoted text is still the start of a real gloss. It is polish, not a defect.

**Limits:**
- The audits simulate option draws and string collisions only. They cannot judge whether a displayed title is semantically defensible as a wrong answer; I judged that by reading the titles in `quiz-safety.txt`.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run at this revision (known packet limit).
- I did not re-verify public web pages this round. The JMdict claims rest on the pinned entries in the packet. The 岬 Daijisen claims rest on the packet's re-extraction, which I did not compare against the live page.
- I read `CHANGES.md` only in a follow-up turn, after the first version of this report. The first version did not read it: an earlier combined read spilled to a temp file that I did not open.
- The confirm packet holds no stroke files and no word articles other than 宴会. So the claim that the 15 stroke files and the other 19 word articles are unchanged rests on `fix.patch` being the complete patch.
- I cannot confirm the two part-of-run matches that `meta-scan.txt` reports as gone (嬢さん inside お嬢さん and inside 御嬢さん), or the earlier count of 33: the original packet has no meta-scan output to compare.
- Execution limits: every response made exactly one tool call; no parallel calls were issued.