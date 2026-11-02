# N1 kanji pilot: bounded confirmation of my initial review

**Snapshot:** teaching 6855b42fa2c4e4cae6fd01a2697d10ee42011abb, unchanged. The coordinator reports an empty teaching diff since my initial review and an unchanged Android snapshot (2bc0234bffcb3c4a0cbafde80367d24d2638a93a). I did not verify either statement myself.

## Scope

- **Reviewer:** Claude Opus 5.5 (claude-opus-5.5). This was read-only, with tools used one at a time. I made no edits, ran no commands, delegated nothing and read no other review.
- **Files read, each once, in full:**
  - `docs\n1-reviews\pilot-initial-claude.md` (my original report, left untouched)
  - `docs\n1-reviews\pilot-claude-confirmation-evidence.txt`
- **Where the evidence comes from:** all of the new evidence is coordinator-supplied. That covers the app source and test excerpts, the JVM test run and its XML reports, the Kanjipedia follow-up fetches, and the statements about validator, link and import behaviour. I retrieved nothing independently in this session: no web fetches, no source reads and no test runs.
- **Not done:** I did not repeat the full-packet review and I do not certify one. This confirmation covers only F1, R1 and the limits named in the evidence file.

## Verdicts

Format: correctness / scoped coverage / comprehensibility.

- **words/乃至:** CLEAN / **CLEAN** / CLEAN. Scoped coverage changes from UNVERIFIED because F1 is withdrawn.
- **All other files, including the eight reused articles in changed-passage scope:** unchanged from my initial report.
- **Reading-key suitability:** still NEEDS a companion prerequisite under issue #1 (R1), kept separate from text correctness.

## Findings and dispositions

### F1: reverse-direction quiz ambiguity for 乃至 — withdrawn

- **Evidence (coordinator-supplied):** `Words.kt` L170–187 defines `excluded(a,b) = b.word in a.quizExclusions || a.word in b.quizExclusions`. It applies this between the target and each candidate, and between candidates already chosen and each new candidate. `curatedDistractors` also checks both directions.
- **Tests (coordinator-supplied):**
  - `WordsTest` L177–191 checks one-sided exclusions in both directions.
  - L194–209 checks exclusions between distractors in either selection order.
  - L212–222 checks that exclusions are not transitive.
  - The reported results are 22 of 22 `WordsTest` tests passing, 3 of 3 `RealContentTest` and 1 of 1 `RareHanTest`.
- **Effect:** with symmetric exclusion, 乃至's one-sided `quiz_exclusions: [または, あるいは, それとも]` already stops "from ... to; or" appearing as an option when または, あるいは or それとも is the prompt. The weaker 冊子/栞 variant is also covered by 栞's exclusion of 冊子. No companion change to the comparison articles is needed.
- **Caveat:** I read the code and test excerpts quoted in the evidence file, not the source files. These are JVM tests, not device evidence.

### Limit: 稲を扱く example (扱.md L33) — resolved

The coordinator's retrieval of Kanjipedia kotoba/0000072100 reports the heading 扱く こ-く and the example 稲を―く. Filling in the headword gives 稲を扱く, so the collocation is attested, not invented.

### Limit: 乃 なんじ "kanbun usage" wording (乃.md L34) — partially resolved

- The coordinator's retrieval of Kanjipedia kanji/0004473200 shows sense 2 glossing なんじ as おまえ ("you"), with 乃(なんじ) in the word navigation. That supports the reading and gloss as character-dictionary recognition material.
- The card defines kanbun and limits the reading to recognition, so the teaching makes no overclaim.
- The specific "kanbun" register label still has no direct dictionary source. This is low severity and needs no fix.

### Limit: link targets and 茉 metadata — resolved, with one note

- **至:** it is plain text in 乃至.md, not a link, so nothing can be broken. The evidence cites L23; my export showed 乃至.md L24.
- **姓:** the evidence says `words/氏名.md` L35 links the unchanged baseline article `words/姓.md`, and that `tools/validate.py` and the pilot audit checked relative link targets at the frozen draft. The evidence does not separately address `kanji/氏.md` L43's link to the kanji article 姓.md. I accept it as covered by the validator statement, which I did not run myself.
- **茉:** listing 茉 in 茉莉花's written-kanji metadata is required by the canonical format. The coordinator reports that `RealContentTest` imported the actual pilot without skips.
- **Line-number note (minor):** the evidence's line numbers differ slightly from my exports (乃至 L23 against L24; 氏名 L35 against the 姓 link I saw at L33). The difference doesn't affect the disposition.

### R1: source-only reading keys — unresolved, remains a companion prerequisite under issue #1

- **What holds:** the metadata itself remains valid recognition data. It comes from KANJIDIC2, plus Kanjipedia where cited, and each card discloses the source-only readings correctly.
- **What still needs a decision is acceptable prompting.** The coordinator confirms that 12 projected source-only keys still enter the pilot queue:
  - 扱 そう, きゅう
  - 乃 の (on)
  - 彗 え, けい
  - 漱 しゅう, す, くちそそぐ
  - 矛 ぼう
  - 栞 かん
  - 莉 らい, れい
- **漱:** the lexically supported すすぐ is still cut by the first-three limit.
- **One sub-claim withdrawn:** I had said 乃's の appearing as both an on and a kun key cannot be told apart. The coordinator says `KanjiReadings.kt` keeps separate reading kinds, so identical kana across kinds is not a duplicate-answer defect within one question. Whether on-reading の is suitable as a study prompt remains part of R1.
- **Required prerequisite (still open):** separate the preserved dictionary metadata from the readings accepted for learner prompting. That includes treatment of recognition-only material and actual compatibility with how keys are transported and queued.
- **Not claimed:** I am not claiming any metadata deletion, reordering or app fix. A missing example does not prove a reading false.

## Optional

The polish items from my initial report stand unchanged and none blocks:

- link 箒 from 彗.md;
- add 夏目漱石 (and optionally ゆすぐ) to 漱.md;
- name 水星 in 彗星.md;
- reword or remove the しごく sentence at 扱.md L45;
- gloss or reduce meta wording such as "source-only" and "search-only";
- add a 草 contrast note in 幹.md;
- the 栞/案内 pair remains borderline.

## Limits

- **Second-hand evidence:** everything new here is coordinator-supplied. I did not independently fetch Kanjipedia, read `Words.kt`, `WordsTest.kt`, `ReadingData.kt` or `KanjiReadings.kt`, or run the tests or the validator.
- **No device evidence:** the JVM test passes are not native device or phone evidence. Native selection, sessions, article display, Back navigation, drawing, acceptance across all 40 fonts and phone rendering have not occurred and are not certified.
- **Not certified:** no fresh full-packet review, no publication, and no native-speaker or physical-phone comprehensibility check.
- **Earlier limits still apply:** the 星 frontmatter check used the working tree, not an export.