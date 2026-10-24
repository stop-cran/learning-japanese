## Snapshot
The frozen commit is `97436ec4589201838df1b398046729a2c43d57fe` (parent `4f7e8067dbb8368fec49766c2e66dc581abf58a1`). The receipt marks the content as clean committed content. My file tools cannot run Git, so I read working-tree files and treated them as that commit. Hash and equivalence results are the author's checks, not mine.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), read-only, no delegation.
- **Instructions read:** `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md:18-126`.
- **Articles read completely:** all 19 new articles, reused `せっせと`, the kanji cards `接`, `戸` and `専`, and the seven link-only cards. I also read these comparison cards in full: `支配`, `トップ`, `せめて` targets and `全集` neighbours.
- **Evidence read:**
  - Mappings, components, principal families (20 families, 36 senses), the related patch, and all 268 labels.
  - Rows N2:902–921 of `n2-vocabulary-sources.tsv`; they match the JSONL.
  - All public bodies, plus targeted complete records from the 22 selected-family files: 責める, 攻め手, ゼミナール, 親, 頂上, 点, 末, 結果, 一緒, 一斉, 逆, 逆さ and 祖.
- **Not read:** the rest of the 432-family union, `n2-vocabulary-snapshot.json`, `n2-source-snapshot.json`, and all forbidden files.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility.

| ID | Article | Status | Correct. | Coverage | Compr. |
|---|---|---|---|---|---|
| N2:902 | せっせと | reused, level only | CLEAN | CLEAN | CLEAN |
| N2:903 | 接続 | new | CLEAN | CLEAN | CLEAN |
| N2:904 | 瀬戸物 | new | CLEAN | CLEAN | CLEAN |
| N2:905 | ぜひとも | new | CLEAN | CLEAN | CLEAN |
| N2:906 | 迫る | new | CLEAN | CLEAN | CLEAN |
| N2:907 | ゼミ | new | NEEDS FIX (F2) | CLEAN | CLEAN |
| N2:908 | せめて | new | CLEAN | CLEAN | CLEAN |
| N2:909 | 攻める | new | CLEAN | CLEAN | CLEAN |
| N2:910 | セメント | new | CLEAN | CLEAN | CLEAN |
| N2:911 | 栓 | new | CLEAN | CLEAN | CLEAN |
| N2:912 | 前後 | new | CLEAN | CLEAN | NEEDS FIX (F5) |
| N2:913 | 洗剤 | new | CLEAN | CLEAN | CLEAN |
| N2:914 | 全集 | new | NEEDS FIX (F4) | CLEAN | CLEAN |
| N2:915 | 全身 | new | CLEAN | CLEAN | CLEAN |
| N2:916 | 扇子 | new | CLEAN | CLEAN | CLEAN |
| N2:917 | 専制 | new | NEEDS FIX (F3) | CLEAN | CLEAN |
| N2:918 | 先々月 | new | CLEAN | CLEAN | CLEAN |
| N2:919 | 先々週 | new | CLEAN | CLEAN | CLEAN |
| N2:920 | 先祖 | new | CLEAN | CLEAN | CLEAN |
| N2:921 | 先端 | new | NEEDS FIX (F1) | CLEAN | CLEAN |

**Kanji edits (CLEAN):** each word is added to its reading row, the Common words list and a note.
- `接.md` lines 30, 43, 52: 接続 at セツ.
- `戸.md` lines 31, 38, 46: 瀬戸物 at と, in the place name 瀬戸.
- `専.md` lines 28, 34, 40: 専制 at セン.

**Seven link-only edits (CLEAN):** the targets exist and the text is unchanged.
- `繋ぐ.md:29`, `コンクリート.md:28`, `少なくとも.md:36`, `せっけん.md:25`, `責める.md:35`, `先週.md:25`, `再来月.md:26`.

**Reused level (CLEAN):** the patch adds `jlpt: 2` to `せっせと`, which had no previous level. No easier level was overwritten, and JMdict 2008620 sense 1 is covered.

**Mappings (CLEAN, all 20):**
- Source fields are preserved.
- The N2:908 raw gloss ("offense, method of attack") belongs to 攻め手 1675160. The article handles this explicitly and does not change the source ID.
- Blank glosses at N2:902 and N2:919 are preserved.
- Selected senses match the principal families.
- ぜひとも has `kanji: []` and recognises its written aliases.

## Findings
- **F1 · minor · quiz exclusions · `words\先端.md:9,45`**
  - **Claim:** 先端 does not exclude トップ. Its title is "tip; leading edge", and line 45 says the word "identifies a leading position". トップ's title is "top; leading position" (`トップ.md:4`). JMdict 1388110 sense 2 gives "forefront; vanguard; leading edge". 頂上 ("summit; top") is already guarded, so トップ is at least as confusable.
  - **Remedy:** add トップ to the exclusions.
  - **Confidence:** medium.
- **F2 · minor · quiz exclusions · `words\ゼミ.md:1-9,15,34-36`**
  - **Claim:** ゼミ has no exclusions. The article calls a ゼミ a "small-group university class" and says "A ゼミ can be a 授業". 授業's title is "class, lesson", so learners could accept either. For comparison, 講演 already guards 講義.
  - **Remedy:** add 授業.
  - **Confidence:** medium.
- **F3 · minor · quiz exclusions · `words\専制.md:1-9,15,21`**
  - **Claim:** 専制 is defined as "autocratic or despotic control" and "autocratic rule". 支配's title is "rule; domination; control" and it is not guarded.
  - **Remedy:** add 支配.
  - **Confidence:** medium-low.
- **F4 · minor · quiz exclusions · `words\全集.md:4,9,16`**
  - **Claim:** the title includes "collected series" and line 16 says "edition or series". シリーズ's title is "series" and it is not guarded.
  - **Remedy:** add シリーズ.
  - **Confidence:** medium-low.
- **F5 · minor · comprehensibility/implied sense · `words\前後.md:57`**
  - **Claim:** the sentence "Do not translate every 前後 as … 'throughout'" implies that some 前後 does mean "throughout". That comes only from the raw N2:912 gloss. None of JMdict senses 1–8 or the Daijisen capture supports it, and the article never mentions the source.
  - **Remedy:** identify "throughout" as an unsupported raw-source gloss, or drop it and keep the reversed-order warning.
  - **Confidence:** medium.

## Optional
- **Kanji links (non-N2 cards):** 前後 could be linked at `kanji\前.md:28`, 扇子 at `子.md:32`, and 先祖 at `祖.md:22,33,39`.
- **Wording to clarify:**
  - `ゼミ.md:29` "inventing an English spelling" could say it comes from German *Seminar*, not English seminar (セミナー).
  - `前後.md:40` "not read まえあと" could become "always ぜんご".
  - `ぜひとも.md:45` "weather-prediction adverb" is cryptic.
- **Smaller notes:**
  - `専制.md:17` "can take する" could say that use is uncommon.
  - 攻める could consider guarding 戦う ("fight; compete").
  - `再来月.md:26` leaves 先月 unlinked; this was already the case before the batch.

## Limits
- I could not run Git.
- Public bodies are the author's captures, not fresh fetches. The せっせと and 先々週 captures are empty, and the 扇子 body is only "おうぎ". JMdict families are the support for those three.
- I read only targeted comparison families, not the full 432 families/1068 senses. That leaves other missing guards possible. The author-inspected scope of 113 old bodies is not mine.
- JMdict's "at most" gloss for せめて is not taught; I judged that acceptable from Daijisen sense 1.
- This review is not a native-speaker certification.
