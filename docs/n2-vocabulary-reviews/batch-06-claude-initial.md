## Snapshot
- **Frozen commit:** `4c40b75eb68980ad3744c172f8adac8c32016342` (parent `59801b4d48ce48f27a165f6e9431e6e082bc5fec`). The receipt marks it as clean committed content.
- **My limit:** I have file tools only and cannot run Git. I could not independently confirm the commit, that the tree is clean, or any file hash. I reviewed the files as they are on disk, on the receipt's word that they match the commit.

## Scope
- **Model:** claude-opus-5.5, family claude, in a fresh process. I worked sequentially, edited nothing and used no other agents.
- **Instructions and rules read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md` lines 18-112.
- **Source files read:**
  - The frozen receipt and the related-file patch.
  - The 20 mapping rows in `n2-vocabulary-sources.tsv` (lines 102-121).
  - `batch-06.json`: source rows (lines 12-363), the full dictionary entry families, the comparison families, and the author's notes on outside sources (lines 9043-9097).
- **New articles:** all 16 read in full.
- **Related edits:** the ten changed passages, read in context:
  - Kanji pages 承, 薄, 敬, 裏 and 浮.
  - Word pages 浮く, うっかり, 埋める, 会議 and 写す.
- **Reuse claims:** 浮く, うっかり, 埋める and 討つ (unchanged, still N3).
- **Aliases:** 浮ぶ → 浮かぶ, 受取 → 受け取り, 打合せ → 打ち合わせ.
- **Supporting checks:**
  - Every link and quiz-exclusion target exists, and I read its title.
  - I checked whether the kanji cards exist and their levels.
  - I searched all word titles under `words\` for overlapping English labels.
  - I checked `confusable-words.md` and the exclusion settings on 会合, 務め and 責任.
- **Deliberately not read:** the forbidden notes and review files, and other reviewers' output. I did not search the whole repository.
- **Not covered:** a full review of the unchanged teaching in the ten related files.

## Verdicts
Each row gives correctness / scoped coverage / comprehensibility.

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 浮かぶ | CLEAN | CLEAN | CLEAN |
| 浮かべる | CLEAN | CLEAN | CLEAN |
| 承る | CLEAN | CLEAN | CLEAN |
| 受け取り | CLEAN | CLEAN | CLEAN |
| 受け持つ | CLEAN | CLEAN | CLEAN |
| 薄暗い | CLEAN | CLEAN | CLEAN |
| 薄める | CLEAN | CLEAN | CLEAN |
| 打ち合わせ | NEEDS FIX (B06-01) | NEEDS FIX (B06-03) | CLEAN |
| 打ち消す | CLEAN | NEEDS FIX (B06-04) | CLEAN |
| 映す | CLEAN | CLEAN | CLEAN |
| 写る | CLEAN | CLEAN | CLEAN |
| 映る | CLEAN | CLEAN | CLEAN |
| うどん | CLEAN | CLEAN | CLEAN |
| 有無 | CLEAN | CLEAN | NEEDS FIX (B06-02) |
| 敬う | CLEAN | CLEAN | CLEAN |
| 裏返す | CLEAN | CLEAN | CLEAN |

**Ten related edits: all CLEAN on all three facets.**
- **Kanji pages:**
  - Kanji pages 承, 敬, 薄 and 裏 now link each new word that contains them, at the right reading. 薄 links both 薄暗い and 薄める.
  - Kanji page 浮 adds the reading row う.かべる and links 浮かぶ and 浮かべる.
  - The dictionary entry IDs added to the 薄 and 裏 pages (1475530 and 1550630) are correct.
- **Word pages:**
  - 浮く adds the N2 source and a comparison link to 浮かぶ.
  - うっかり and 埋める add only the N2 source.
  - 会議 now links 打ち合わせ.
  - 写す now links 写る and 映す.

**Four reuse claims: all CLEAN.**
- **浮く:** teaches physical floating (dictionary sense 1) and says plainly that other senses are not taught.
- **うっかり:** teaches inattention (sense 1).
- **埋める:** teaches the うめる reading with senses 1-3. "Fill a seat or vacant position" falls under sense 3 and is covered by 空欄を埋める (fill in the blanks). A seat or vacancy example would be a nice addition; see Optional.
- **討つ:** unchanged, keeps its N3 level, and has the same spelling and reading. It teaches attack, defeat and avenge.

**Three aliases: all CLEAN.**
- **浮ぶ:** taught explicitly at 浮かぶ.md:24-25 as a search-only spelling, which matches the dictionary.
- **受取:** both 受取り and 受取 are taught at 受け取り.md:18, and 受取 is used in the example at line 21.
- **打合せ:** taught at 打ち合わせ.md:18.

**Other checks that came out clean:**
- **Grammar and readings:** spellings, readings, verb classes and transitivity all match the dictionary entries. This includes うすぐらい, うらがえす (with the voiced が), 有 read ウ + 無 read ム, 饂飩 marked rare, and ゆうむ marked outdated.
- **Kanji lists:** every article's kanji list includes every kanji written in it.
- **Missing kanji cards:** 有無 correctly leaves 無 unlinked because 無 has no kanji card.

## Findings
**B06-01: Minor, correctness (quiz metadata). 打ち合わせ.md:9**
- **Problem:** 打ち合わせ excludes 会議 ("meeting; conference") from its quiz choices but not 会合 ("meeting; gathering"). The dictionary's first gloss for 打ち合わせ is "(preparatory) meeting" (batch-06.json:1786). So in a quiz asking for 打ち合わせ, "meeting; gathering" is a reasonable answer. That meets the exclusion rule at content-format.md:95-96. The two words share the kanji 合 and the noun and suru-verb tags, and those shared traits make the app likely to offer them together (content-format.md:81). 会合 already excludes 会議, and the author excluded 会議 here for the same "meeting" overlap. Exclusions are not transitive, so neither existing exclusion covers this pair.
- **Effect on learners:** a question with two arguably correct choices.
- **Fix:** add 会合 to the quiz exclusions on 打ち合わせ.
- **Confidence:** medium.

**B06-02: Minor, comprehensibility. 有無.md:18**
- **Problem:** "It is a noun, not a verb meaning to create something" is a warning about a different word read うむ (生む or 産む, "give birth; produce"). It never names that word, so a learner who doesn't know it can't tell what the sentence is about.
- **Fix:** name it. For example: "Do not confuse it with the verb 生む・産む (うむ), 'give birth; produce.'" Neither word has a card, so plain text with kana is right.
- **Confidence:** high.

**B06-03: Low, scoped coverage (links). 打ち合わせ.md:29**
- **Problem:** "合わせる (あわせる), 'bring together; coordinate'" introduces this parts-of-the-word verb as plain text, but `words\合わせる.md` exists. The same sentence links 打つ. The rule at content-structure.instructions.md:20 and :55 is to link existing cards where they are substantively introduced.
- **Fix:** write it as `[合わせる](合わせる.md)`.
- **Confidence:** high.

**B06-04: Low, scoped coverage (links). 打ち消す.md:36**
- **Problem:** 肯定 (こうてい, "affirmation") is presented as the contrast in the synonyms-and-antonyms section, but it isn't linked. `words\肯定.md` exists with the title "affirmation", and the same section links 否定.
- **Fix:** write it as `[肯定](肯定.md)`.
- **Confidence:** high.

## Optional
None of these are defects.
- **薄める:** the "tone down" meaning in the title is explained (line 17) but has no example. Something like 印象を薄める would help.
- **埋める:** the source gloss mentions filling a seat or vacant position. An example like 欠員を埋める would show it.
- **受け取り:** note that for payments, 領収書 or レシート is now more usual than 受取 for the document. 受取 is common on forms and labels, as in 受取人 (recipient).
- **打ち消す:** mention かき消す as the more common verb for drowning out a voice.
- **浮かぶ / 浮かべる:** mention 思い浮かべる ("picture in one's mind").
- **裏返す:** mention the intransitive partner 裏返る. Optionally link `words\裏.md`.
- **有無.md:43:** the "not a special computer term for every kind of flag" sentence is odd and could be removed.
- **Kanji pages 写, 映 and 有:** these unchanged N4 pages list 写る, 映る, 映す and 有無 as plain text. Those cards now exist, so linking them would be cheap navigation. It isn't required for N4 kanji.
- **出会い ("meeting; encounter"):** it shares "meeting" with 打ち合わせ. "Encounter" makes its meaning clear, so no exclusion is needed.

## Limits
- **Git:** I couldn't run it, so the commit and hashes are not independently verified.
- **Outside dictionary and guide claims:** my own fetches failed.
  - The official 異字同訓 PDF (bunka.go.jp) returned compressed binary I couldn't read.
  - Kotobank and Weblio returned no entry text.
  
  The claims below therefore rest on the author's notes plus my own knowledge, without direct retrieval. They agree with the dictionary entries and with what I know, and I found no defect in them.
  - The official-guide claims about 写る, 映る and 映す: ビデオに写る vs ビデオを映す, and 映る for video playback and live camera display.
  - The Daijisen "document" sense for 受取.
  - The Nipponica history of the name うどん, and its classification as kango.
- **Naturalness of 打ち消す's drown-out example:** the dictionary supports 大きな音が彼の声を打ち消しました (sense 2, "drown out"). I couldn't confirm in a Japanese dictionary how natural it is compared with かき消す.
- **No native speaker:** none of this is native-speaker certification.
- **Scope gap:** I did not comprehensively review the unchanged teaching in the ten related files.
- **Exclusion search:** my search for overlapping titles was by keyword, so other uncurated overlaps may exist.
