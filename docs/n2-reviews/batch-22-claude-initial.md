## Snapshot
I reviewed frozen commit `e02823f4e2628344b9ba4fd896fde675e6bce08d` (baseline `95dcb10075d23a934e6ea2c801e27c71ff2de777`). I read only the committed files. I had file tools but could not run Git, so I could not diff or confirm the tree myself; I relied on the snapshot's record of a clean worktree.

## Scope
- **Model:** claude-opus-5.5, claude family.
- **Read completely:**
  - The 15 new kanji cards: 賞 賢 贈 超 跡 踊 軍 軒 軟 軽 輪 輸 辛 農 辺.
  - The two new word articles: `words\超過.md` and `words\軟らかい.md`.
  - The required instruction files and `docs\content-format.md` lines 18–109.
- **Checked against `batch-22.json`:**
  - The source metadata for all 15 kanji.
  - The dictionary record behind every example on the cards.
  - The quiz-safeguard notes and the limits on how the quiz lists were curated.
- **Quiz checks:**
  - Titles of the existing kanji cards used as distractors.
  - Existing cards that still have only two distractors (the app adds a third, so synonyms there would matter).
  - Existing word titles and their quiz exclusion lists.
  - The relevant lines of `docs\confusable-words.md`.
- **Related edits:** each new link line in the 22 link-only word articles, in context. I fully reread only `words\柔らかい.md`, `words\軒.md` and `words\辺り.md`.
- **Not covered:**
  - The drawing paths in the 15 stroke files.
  - The rest of the unchanged text in the 22 link-only articles.
  - Any baseline diff.
  - The manifest and generated files.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 賞 | CLEAN | CLEAN | CLEAN |
| 賢 | CLEAN | CLEAN | CLEAN |
| 贈 | CLEAN | CLEAN | CLEAN |
| 超 | CLEAN | CLEAN | CLEAN |
| 跡 | NEEDS FIX | CLEAN | CLEAN |
| 踊 | CLEAN | CLEAN | CLEAN |
| 軍 | CLEAN | CLEAN | CLEAN |
| 軒 | CLEAN | CLEAN | CLEAN |
| 軟 | CLEAN | CLEAN | CLEAN |
| 軽 | CLEAN | CLEAN | CLEAN |
| 輪 | CLEAN | CLEAN | CLEAN |
| 輸 | CLEAN | CLEAN | CLEAN |
| 辛 | CLEAN | CLEAN | CLEAN |
| 農 | CLEAN | CLEAN | CLEAN |
| 辺 | CLEAN | CLEAN | CLEAN |
| 超過 | CLEAN | CLEAN | CLEAN |
| 軟らかい | CLEAN | NEEDS FIX | CLEAN |

## Findings
**B22-C-01: the 跡 card wrongly rules out the reading そくせき for 足跡**
- **Severity:** Minor.
- **Facet:** correctness.
- **Location:** `kanji\跡.md:41`.
- **Claim:** The note says "Do not use the on reading セキ to pronounce this example." This deletes a reading the source supports for the same written word. Learners may wrongly reject 足跡 read as そくせき.
- **Evidence:**
  - JMdict entry 1581330 (`batch-22.json:4636-4710`) lists two readings, あしあと and そくせき.
  - そくせき is restricted only to the kanji spelling 足跡 and carries no rarity flag.
  - Weblio's copy of Japanese Wiktionary lists 足跡【そくせき】 meaning "歩いたあとに残る足の形" (footprint).
- **Fix:** Reword the note to: "Here 足跡 is read あしあと (足 あし + 跡 あと). The kanji spelling also has the dictionary reading そくせき."
- **Confidence:** High.

**B22-W-01: 軟らかい lacks quiz exclusions that the other spelling already has**
- **Severity:** Minor.
- **Facet:** scoped coverage (quiz curation).
- **Location:** `words\軟らかい.md:8`.
- **Claim:**
  - The existing article `words\もちもち.md:8` excludes 柔らかい, and so does `words\もこもこ.md:8`.
  - 軟らかい is a second spelling of the same word, but its exclusion list includes neither もちもち nor もこもこ.
  - Exclusions are not transitive, so the protection given to 柔らかい does not carry over to 軟らかい.
- **Impact:** A もちもち quiz can show "soft; pliant" as a distractor. The もちもち article itself says "soft but elastic" and mentions "supple skin", so a learner could reasonably pick it. The repository already blocked this same meaning ("soft; flexible") for 柔らかい.
- **Evidence:**
  - 柔らかい and 軟らかい are the same JMdict entry, 1605630.
  - `content-format.md` says exclusions apply both ways but not transitively.
  - The quiz-safeguard notes in `batch-22.json` never mention もちもち or もこもこ.
- **Fix:** Add もちもち to the list. Add もこもこ too, to match the existing pair.
- **Confidence:** Medium for もちもち. Low–medium for もこもこ: its JMdict glosses are "fluffy; lumpy; bulging", and its article says it can mean lumpiness rather than softness.

**Checked with no defect:**
- **Card metadata:** For all 15 kanji, readings, primary stroke counts, radicals and grade tags match KANJIDIC2. 辺 correctly keeps the primary count of 5.
- **Examples:** All examples use the reading the card indicates. Spelling and reading restrictions are respected; for example, 賞める is labelled as the rare spelling, つらい and ほとり are noted as usually written in kana, and いくさ's "archaic" flag is limited to its second sense.
- **Distractors:**
  - All 45 are existing cards whose meanings are wrong for the target. Same-radical picks (足 for 跡, 指 for 輪, the antonym 重 for 軽, 豊 for 農) still have clearly different answer meanings.
  - Close existing meanings never sit in each other's distractor lists. Examples: 宇 "eaves", 兵 "troops", 伝 "convey", 鳴 "ring", 舞 "dance", 越/過 "exceed", 柔 "soft", 際 "edge".
  - No existing card lists a new kanji as a distractor.
  - The 13 older cards with only two distractors (人 休 何 入 出 口 女 山 年 日 月 男 買) have meanings unrelated to the new ones.
- **Word articles:** Every card links at least one useful word article. The exclusions for 超過 are adequate.

## Optional
- **超過:** Consider excluding あんまり ("not very; excessively"). Its "excessively" shares wording with "excess", but its meaning is degree, so this is low risk.
- **輸:** The example 輸入 しゅにゅう for the シュ reading could carry an "uncommon" label. The note already says the dictionary does not measure frequency, and I did not verify whether シュ is an official jōyō reading.
- **軽:** 軽忽 could mention its literary register; the dictionary sets no priority flag, which does not by itself prove rarity.
- **軍:** The いくさ row could mention that 戦 is the usual spelling. The source does not establish this.

## Limits
- I could not run Git, so I did not diff against the baseline. I did not confirm independently that the 22 related articles changed only by links or that no existing kanji or stroke file changed.
- I did not review the drawing paths in the 15 stroke files; they come from the pinned converter.
- `batch-22.json` contains selected dictionary records, not the full dictionary. I did not verify frequencies, so "usual" claims are not established.
- jisho.org's web page and goo returned no usable content, and the kotobank result was an encyclopedia article, not the dictionary sense. These are coverage limits, not evidence either way.
- I did not test the quiz at runtime; quiz risks above are judged from meaning, not observed failures.
- This is not a native-speaker check of naturalness.
