## Snapshot
Frozen commit: **7ffb9fef77051410d247dfde7de6c8315ccb8e6f** (parent bab4b8118ca8674554ea1ffc9cae443f166089ef), committed content only.

I used file tools only and ran no Git commands, so I did not verify the commit, the hashes or the receipt's equivalence claims myself. Those checks were run by the author.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), in a fresh process. Nothing was edited and nothing was delegated.
- **Read in full:**
  - All 20 new articles.
  - The related patch and the mappings, principal-reading, supplemental-comparison (応接), components and labels files.
  - The public-bodies text file. These are author captures, not pages I fetched.
  - kanji\角.md, kanji\接.md and words\成長.md.
- **Read in part:**
  - The changed lines of 清, 掃, 党 and 門, and of the seven link-only old cards.
  - kanji\折.md.
  - The titles and exclusions of 機会, チャンス, 苦心, 一生懸命, 死亡, 緯度 and 熱帯.
  - Some sections of the review-evidence file, including JMdict 2846960 (赤道 read あかみち/あかどう).
- **Also checked with file tools:** every link target, which kanji cards exist (整, 暦 and 脊 have none) and whether any old card's quiz_exclusions name a new card (none do).
- **Not read:** selected-families files 01-18, public-bodies.json, the 131 old full bodies, docs\confusable-words.md, docs\jlpt-levels.md, and the repository's .tsv and snapshot .json files. I used the compact private equivalents instead.
- **Out-of-range read:** a "link" search in content-format.md returned lines outside 18-126 (lines 36 and 933-934).
- **No web fetches.**

## Verdicts
Each row gives correctness / scoped coverage / comprehensibility. All 20 articles are new.

| ID | Article | Verdict |
|---|---|---|
| N2:882 | 青少年 | CLEAN / CLEAN / CLEAN |
| N2:883 | 整数 | CLEAN / CLEAN / CLEAN |
| N2:884 | 清掃 | CLEAN / CLEAN / CLEAN |
| N2:885 | 生存 | CLEAN / NEEDS FIX (F5) / CLEAN |
| N2:886 | 生長 | CLEAN / CLEAN / CLEAN |
| N2:887 | 政党 | CLEAN / CLEAN / CLEAN |
| N2:888 | 生年月日 | CLEAN / CLEAN / CLEAN |
| N2:889 | 性能 | CLEAN / CLEAN / CLEAN |
| N2:890 | 整備 | CLEAN / CLEAN / CLEAN |
| N2:891 | 成分 | CLEAN / CLEAN / CLEAN |
| N2:892 | 性別 | CLEAN / CLEAN / CLEAN |
| N2:893 | 正方形 | CLEAN / CLEAN / CLEAN |
| N2:894 | 正門 | CLEAN / CLEAN / CLEAN |
| N2:895 | 成立 | CLEAN / CLEAN / CLEAN |
| N2:896 | 西暦 | NEEDS FIX (F3) / CLEAN / CLEAN |
| N2:897 | 背負う | CLEAN / CLEAN / CLEAN |
| N2:898 | 赤道 | CLEAN / NEEDS FIX (F4) / CLEAN |
| N2:899 | せっかく | NEEDS FIX (F1, F2) / CLEAN / CLEAN |
| N2:900 | 接近 | CLEAN / CLEAN / CLEAN |
| N2:901 | 接する | CLEAN / CLEAN / CLEAN |

- **Six kanji edits:** CLEAN.
  - 清, 掃, 党, 門 and 接 each have the reciprocal reading-row and Common words examples at the stated readings.
  - The 接 Notes explain the small っ.
  - 角 gives navigation only: a Common words line and a note, with no change to the カク row.
  - The entry lists are updated, and the patch leaves metadata and stroke counts unchanged.
- **Eight old-word edits:** CLEAN.
  - The seven link-only edits are at 青年:31, 小数:28, 誕生日:28, 性:28, 四角:27, 四角い:35 and 門:29.
  - The 成長 comparison acknowledges that 成長 also covers plants and that 生長 has broader and older uses, matching the Daijisen captures.
- **All twenty mappings:** CLEAN.
  - Senses are selected faithfully.
  - 背負う selects senses 1-3 and recognizes sense 4 (しょう) separately.
  - せっかく is kana-primary and recognizes 折角.
  - 政党 corrects the source's "(member of)" gloss.
  - 赤道 あかみち/あかどう is confirmed as a separate JMdict entry, 2846960.

## Findings
- **F1 (Medium; correctness/quiz; せっかく.md:4,9).**
  - **Claim:** the title "with effort; a valuable opportunity" overlaps four existing titles that the card does not exclude:
    - 一生懸命, "with utmost effort"
    - 苦心, "painstaking effort; taking pains"
    - 機会, "opportunity"
    - チャンス, "chance; opportunity"
  - **Evidence:**
    - JMdict 1596090 sense 1 is "at great pains", and sense 2 is "valuable; long-awaited".
    - The author already excludes 努力, 手間 and 苦労 for this effort overlap.
    - 苦心 itself excludes 努力, 手間, 苦労 and 一生懸命.
    - No old card excludes せっかく.
  - **Impact:** a quiz question can include a wrong choice that a learner could reasonably defend.
  - **Remedy:** add 苦心, 一生懸命, 機会 and チャンス to せっかく's quiz_exclusions.
  - **Confidence:** high for 苦心 and 一生懸命; medium-high for 機会 and チャンス.
- **F2 (Low; correctness/character association; せっかく.md:30-32).**
  - **Claim:** the article glosses 折 as "folding/occasion" and 角 as "corner/angle", and calls the pairing not a demonstrated etymology.
  - **Evidence:** the cited Daijisen (author capture, 折角 noun sense 1) traces the word to the Han-shu anecdote "鹿の角を折る", meaning to break a horn. That is where 骨を折ること comes from. kanji\折.md:20,30-31 gives "break", and kanji\角.md:3 gives "horn".
  - **Remedy:** gloss the parts as break + horn, mention that classical anecdote, and keep the advice to learn the modern word whole.
  - **Confidence:** medium.
- **F3 (Low; correctness/quiz; 西暦.md:9,39-40).**
  - **Claim:** 時代 ("era; period") and 年代 ("era; period of years") are excluded because of the "Common Era" ambiguity, but 世紀 ("century; era") is not.
  - **Evidence:** 世紀 itself excludes 時代 and 年代 for that same "era" sense.
  - **Remedy:** add 世紀.
  - **Confidence:** medium.
- **F4 (Low; coverage/links; 赤道.md:33-35).**
  - **Claim:** the main comparisons 緯度 and 熱帯 are left unlinked, although both have cards.
  - **Rule:** content-structure.instructions.md:20,55 and content-format.md:933.
  - **Remedy:** link both.
  - **Confidence:** high.
- **F5 (Low; coverage/links; 生存.md:36).**
  - **Claim:** the contrast word 死亡 ("death") has a card but is left unlinked.
  - **Remedy:** link it.
  - **Confidence:** high.

## Optional
- 正方形.md:22: the 一辺 note is not used by any example. Add an example such as 一辺が五センチの正方形, or remove the note.
- 接する.md:26-27: 二つの面を接する is a made-up phrase. Daijisen's attested 軒を接する or ひざを接する would be safer.
- 成立: mention 成立させる, for example 交渉を成立させる.
- 背負う: note that しょう is also used for carrying, and add the collocation 責任を背負う.
- 生存: add a recognition note for the alternative reading せいそん.
- 角.md Notes: align the wording with F2.
- The broad exclusion lists are backed by secondary senses or English ambiguity, so they are not defects. This covers 接する (23 items), 清掃↔集まり, 生存↔いる/ある/居る/人命, and 整備↔設備/こしらえる.

## Limits
- No Git or hash checks of my own.
- No fresh public retrievals. The Daijisen evidence is the author's capture.
- I did not read selected-families files 01-18 or the 131 old bodies.
- The naturalness of the examples is my judgement, not a native-speaker certification. In particular, 二つの面を接する and 会社が成立する were not checked against a source.
