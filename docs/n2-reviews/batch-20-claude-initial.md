# Snapshot
`adaf3b4c7349e9d7ecb1360b91e9cd85d1ae20ac` (committed files only). The snapshot JSON gives baseline `799bf28ae8fbc48c1af8e80b797bcb2ebfd57a2f`, `clean: true`, 57 files in scope, 16 teaching pages, 21 related passages and manifest version `d4046e2f36729f9e`. I could not run Git, so I could not confirm that the working tree matches this commit, the 57-file scope, or that the 21 related edits only added links.

# Scope
- **Model:** claude-opus-5.5 (Claude family). I worked sequentially, did not delegate and edited nothing. I did not read any of the forbidden ledgers, reports or other reviewers' output.
- **Instructions read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, and `docs\content-format.md:18-109`.
- **Assigned pages:** all 16 read completely (the 15 kanji cards and `words\蒸す.md`).
- **Source checks:** I compared every card against its `batch-20.json` record (metadata, primary words, and the word evidence for each example) and checked the 蒸す comparison entries.
- **Quiz checks:** all 45 distractor assignments, the 蒸す exclusions, `docs\confusable-words.md`, neighbouring word titles, and older cards with synonym-like titles or only two distractors.
- **Related edits:** all 21 linked passages, checked in their section context.
- **Not reviewed:** stroke drawing paths, the manifest and index files, validator runs, unchanged text in the 21 articles outside the linked passages, and other pages except where used for comparison.

# Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\蒸.md | CLEAN | CLEAN | CLEAN |
| kanji\蔵.md | CLEAN | CLEAN | CLEAN |
| kanji\薄.md | CLEAN | CLEAN | CLEAN |
| kanji\虫.md | CLEAN | CLEAN | CLEAN |
| kanji\血.md | CLEAN | CLEAN | CLEAN |
| kanji\衣.md | CLEAN | CLEAN | CLEAN |
| kanji\袋.md | CLEAN | CLEAN | NEEDS FIX |
| kanji\被.md | CLEAN | CLEAN | CLEAN |
| kanji\装.md | CLEAN | CLEAN | CLEAN |
| kanji\裏.md | CLEAN | CLEAN | CLEAN |
| kanji\補.md | CLEAN | CLEAN | CLEAN |
| kanji\複.md | CLEAN | CLEAN | CLEAN |
| kanji\角.md | CLEAN | CLEAN | CLEAN |
| kanji\触.md | CLEAN | CLEAN | CLEAN |
| kanji\訓.md | CLEAN | CLEAN | CLEAN |
| words\蒸す.md | CLEAN | CLEAN | CLEAN |

**What was confirmed:**
- **Metadata:** every reading, stroke count, radical and number, and grade tag matches the source.
- **Source-only readings:** the qualifications for 蔵 おさ.める/かく.れる, 袋 ダイ, and 訓 おし.える/よ.む are accurate and honest.
- **Flags:** the rare and usually-kana flags match the source: 被う, かぶる (senses 1–3), かぶせる, 訓ずる and 秘蔵 ひそう.
- **Verb details:** transitivity and conjugation class are correct for 蒸す, 蒸れる, 蒸らす, 薄める, 薄まる, 薄らぐ, 薄れる, 補う, 触る and 触れる.
- **Distractors:** all 45 exist and are semantically wrong for their targets.
- **蒸す:** the exclusions 暑い, じめじめ and じとじと are justified. The 日本国語大辞典 entry for む・す, sense [1], itself describes the humid heat as 「じとじとする」.
- **Related passages:** all 21 are accurate and consistent with the new cards, and every link target exists.

# Findings
**F-01 · Minor · Comprehensibility (homograph) · kanji\袋.md:30, 44**
- **Claim:** The タイ row gives 布袋 ふたい ("cloth bag") as the typical word, and the note mentions only the alternative reading ぬのぶくろ. It leaves out the separate homograph 布袋 ほてい (Hotei, the pot-bellied god of contentment), which is the best-known reading of this spelling and the base of 布袋腹 ほていばら and 布袋葵 ほていあおい.
- **Impact:** Learners may read 布袋 as ふたい where real texts mean ほてい.
- **Remedy:** Add one clause to line 44 saying the same spelling is also the separate word ほてい, Hotei. Alternatively, switch to a better-known タイ word such as 有袋類 ゆうたいるい ("marsupial"), which would need a new evidence record.
- **Evidence:**
  - `batch-20.json:3496`: JMdict entry 1690870 has readings ぬのぶくろ and ふたい, the gloss "cloth bag", and no priority flags.
  - Jisho API (JMdict data): a separate entry `布袋-1` reads ほてい, glossed "Hotei; Budai; god of contentment…".
  - Kotobank: the 布袋 headword is read ホテイ, and the 日本国語大辞典 entry ふ‐たい sense [2] points to ほてい.
  - The ほてい entry is not in the selected evidence file; it comes only from these public dictionary lookups.
- **Confidence:** high that the homograph exists and is omitted; medium on how much it matters.

# Optional
- **O-01 · kanji\裏.md:30, 37:** JMdict also has a separate common entry, 裏面 うらめん ("back side; reverse; B side"). A note that this spelling is often read うらめん would help, but the card's りめん (news1) is correct.
- **O-02 · kanji\訓.md:29, 43:** 家訓 かきん is attested and the card discloses かくん, but JMdict lists かくん first and Kotobank's headword reading is かくん. Consider saying that かくん is the headword reading.
- **O-03 · kanji\補.md:11:** The distractor 被 is titled "cover; incur", and one JMdict gloss of 補う is "to cover (a shortage, loss…)". The overlap is weak because "incur" and the target title "supplement; make good" separate them, but 複 would be a cleaner distractor that looks similar.
- **O-04 · words\蒸す.md:8, ~47–51:** ほかほか ("warmly steaming") shares the English word "steam". The body already explains the difference; an exclusion would be optional extra safety.
- **O-05 · words\訓練.md:~31 (unchanged text, outside scope):** It writes the on readings in hiragana (くん + れん). This is pre-existing; no action is requested.

# Limits
- Without Git, I could not diff against the baseline or confirm the commit, the 57-file scope, or that the 21 related edits only added links.
- Stroke drawing paths, the manifest, the validator and app quiz runs were not checked; stroke counts were compared only with the source metadata.
- The card's negative claim that no 袋 word read だい exists is a bounded scan by the author, which I did not repeat.
- **Larger or fallback kanji quizzes (no defect):** a quiz of more than four choices could still pair near-synonyms:
  - 蔵 "storehouse; keep in storage" with 庫 "storehouse"
  - 衣 "clothing; garment" with 服 "clothing"
  - 複 "multiple; compound" with 倍 "multiple; double"
  - 触 "touch; contact" with 接 "touch; join"

  All of these cards have three curated distractors, so the default four-choice quiz is safe. Older cards with only two distractors have no synonym risk with the new titles.
- I did not run the app's word-quiz candidate scoring; quiz ambiguity was judged by meaning.
- The public lookups (Jisho API, Kotobank) may differ from the pinned snapshot.
- Teaching sentences were checked for grammar and sense only; this is not a native-speaker check of naturalness or frequency.
