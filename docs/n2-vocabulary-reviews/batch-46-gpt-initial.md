## Snapshot: 97436ec4589201838df1b398046729a2c43d57fe; committed content only

**Two localized correctness fixes are needed:** a missing quiz exclusion for せめて/くらい, and incorrect stem terminology in 攻める. No source-identity or scoped-coverage defect was established.

The frozen receipt reports parent `4f7e8067dbb8368fec49766c2e66dc581abf58a1` and clean committed content. **File tools cannot execute Git:** I could not independently verify the commit, parent relationship, worktree cleanliness, hashes, or correspondence between the readable files and that commit. The review is conditional on the supplied frozen receipt.

## Scope: GPT-6.1 Sol; independent, read-only review

Actual model: **GPT-6.1 Sol**, ID `gpt-6.1-sol`, family `gpt`. No delegation or file edits.

I completely read all nineteen new articles, reused せっせと for its claimed coverage and level-only change, the three related kanji cards, seven link-only old articles, and the supplied related patch. I additionally read **94 existing comparison articles**, including every declared exclusion target in the nineteen new cards. Unrelated baseline teaching was not treated as newly authored material.

Evidence inspected included the required instructions and format passages; allowed level/source documentation; all twenty assigned TSV mappings and blind mapping records; thirty component records; 268 title/exclusion records; twenty complete principal families covering 36 selected senses; all twenty-two selected-family renderings, whose declared union is 432 families/1068 senses; and all twenty-two captured public-source receipts/bodies. I used the compact blind derivatives, not the prohibited author-rationale source file. Forbidden authoring notes, review outputs, private inputs, and other reviewers’ conclusions were not read.

## Verdicts: individual articles, mappings, and related changes

**CLEAN** means no actionable defect established within the actual scope—not exhaustive correctness or native-speaker certification. Correctness includes quiz-answer fairness and grammatical terminology. “Source mapping” assesses the explicit selection and preservation/qualification of raw fields, not the accuracy of every raw source gloss.

| Mapping | Article/status | Correctness | Scoped coverage | Comprehensibility | Source mapping |
|---|---|---|---|---|---|
| N2:902 | せっせと — reused | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:903 | 接続 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:904 | 瀬戸物 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:905 | ぜひとも — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:906 | 迫る — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:907 | ゼミ — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:908 | せめて — new | **NEEDS FIX — F01** | CLEAN | CLEAN | CLEAN |
| N2:909 | 攻める — new | **NEEDS FIX — F02** | CLEAN | CLEAN | CLEAN |
| N2:910 | セメント — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:911 | 栓 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:912 | 前後 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:913 | 洗剤 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:914 | 全集 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:915 | 全身 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:916 | 扇子 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:917 | 専制 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:918 | 先々月 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:919 | 先々週 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:920 | 先祖 — new | CLEAN | CLEAN | CLEAN | CLEAN |
| N2:921 | 先端 — new | CLEAN | CLEAN | CLEAN | CLEAN |

The mapping judgments preserve the important qualifications: N2:902 has blank raw spelling/gloss fields; N2:919 has a blank raw gloss; N2:908 explicitly selects adverb **1006570**, while its raw “offense, method of attack” gloss belongs to separate noun 攻め手 **1675160**. 接続 appropriately explains connecting services rather than equating every connection with a passenger transfer; 前後 does not promote raw “throughout” into an unrestricted translation. No compiler intention was inferred.

Primary written-kanji metadata retains missing-card characters, existing component links are substantive, and kana-primary ぜひとも recognizes 是非とも/是非共 without adding unwritten primary metadata. Quiz review considered complete titles, ordinary secondary senses, reverse declarations, and exclusions between other choices. Beyond F01, I did not establish another missing or unsupported excess guard requiring a change.

**Related changes, assessed separately:**

| Surface/change | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\接.md` — 接続 at セツ and in Common words | CLEAN | CLEAN | CLEAN |
| `kanji\戸.md` — 瀬戸物 at と within 瀬戸 and in Common words | CLEAN | CLEAN | CLEAN |
| `kanji\専.md` — 専制 at セン and in Common words | CLEAN | CLEAN | CLEAN |
| `words\繋ぐ.md` — link to 接続 | CLEAN | CLEAN | CLEAN |
| `words\コンクリート.md` — link to セメント | CLEAN | CLEAN | CLEAN |
| `words\少なくとも.md` — link to せめて | CLEAN | CLEAN | CLEAN |
| `words\せっけん.md` — link to 洗剤 | CLEAN | CLEAN | CLEAN |
| `words\責める.md` — link to 攻める | CLEAN | CLEAN | CLEAN |
| `words\先週.md` — link to 先々週 | CLEAN | CLEAN | CLEAN |
| `words\再来月.md` — link to 先々月 | CLEAN | CLEAN | CLEAN |
| `words\せっせと.md` — level-only addition `jlpt: 2` | CLEAN | CLEAN | CLEAN |

All three required word/kanji pairs have useful reciprocal links at the actual readings. The supplied patch shows only link changes in the seven old articles and only the level addition in せっせと; their existing teaching and earlier declared levels are preserved.

## Findings: two localized defects

**F01 — Medium severity; quiz correctness; high confidence**

**Location:** `words\せめて.md:4,9`; counterpart `words\くらい.md:4,9`.

The new exclusion list omits **くらい**, whose ordinary minimum-request use can overlap the complete label **“at least; even just (minimum wish).”** For example, 名前くらい教えてください can ask someone to *at least tell their name*, closely overlapping the request illustrated at `words\せめて.md:20`. This is not a claim that the particle and adverb are universally interchangeable.

**Evidence:** The complete pinned family **1154340**, reproduced in `batch-46-selected-families-03.txt:41–46`, explicitly includes “at least” in sense 2 without an archaic or rare restriction. Principal family **1006570** specifies desire/hope. The actual くらい article identifies the particle family, not the separate rank noun. Neither article directly excludes the other, and their complete titles differ, so exact-title deduplication does not protect them. Their shared exclusions involving だけ do not establish this pair: exclusions are nontransitive under `docs\content-format.md:85–96`.

**Impact:** When both cards are eligible, the new minimum-wish label can remain a defensible alternative for くらい in a meaning quiz.

**Minimal remedy:** Add exact word ID `くらい` to せめて’s `quiz_exclusions`. One declaration protects the pair symmetrically; no baseline article expansion is required.

**F02 — Low severity; grammatical terminology; high confidence**

**Location:** `words\攻める.md:30–31`.

“攻 supplies the native **stem せ**” confuses the written kanji/okurigana boundary with the verb-stem boundary. The ichidan stem is **せめ**, not せ.

**Evidence:** Complete principal family **1279130** identifies せめる as ichidan. The article’s own correct forms at line 26—攻めます, 攻めて, 攻めない—retain せめ. Thus the spelling division is **せ｜める**, whereas the conjugational division is **せめ｜る**. Line 31 correctly explains the conjugation, limiting the practical impact but leaving the preceding terminology inaccurate.

**Minimal remedy:** Replace “native stem せ” with wording such as **“攻 is read せ here, with める written as okurigana.”** Preserve the correct conjugation explanation and forms.

## Optional: none

## Limits: snapshot binding and source-retrieval qualifications

Independent Git/hash/equivalence verification remains **UNVERIFIED**. Author-executed receipts and inspection counts were not presented as my checks; in particular, I do not adopt the author’s claimed 113-old-body inspection scope. Not every article represented by the 268 labels was read in full.

The twenty-two public bodies are author captures, not fresh reviewer retrievals. The explicit せっせと and 先々週 extraction failures provide no public-definition verification; 扇子’s captured おうぎ reference alone does not establish all folding-fan details. Those judgments also use the complete pinned principal records.

Fresh retrievals were supplementary: initial くらい pages mixed identities or redirected; the subsequent Kotobank 位 particle heading was inspected. A JLPT Sensei request returned a CAPTCHA and supplied no evidence. **F01 relies on the complete pinned particle record and the actual articles, not retrieval success or an irrelevant heading.** No live quiz execution or manifest verification was performed.
