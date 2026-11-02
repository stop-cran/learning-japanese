I reviewed all four batch-007 files: two need one small fix each and two are clean. I made no edits, wrote no files and posted nothing.

**Snapshot:** commit `33e9c9438c912bd701b05dd989114f23a85b08a9`, as given in the task. No uncommitted teaching changes are included. I had no shell, so I could not confirm HEAD myself.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), the only reviewer.
- **Teaching files:** `kanji\柚.md`, `kanji\椿.md`, `words\柚.md` and `words\椿.md`, read in full and checked for correctness, scoped coverage and comprehensibility.
- **Guidance and policy:** `copilot-instructions.md`, `content-structure.instructions.md`, `content-format.md` lines 42–148 and `jlpt-levels.md` lines 1–96.
- **Source evidence:** the complete KANJIDIC2 metadata, all 16 lexical families in `batch-007-jmdict.xml` and all 14 comparison families.
- **Comparison articles:** all 11 kanji (木 由 油 相 春 棒 村 事 香 焼 子) and all 13 words (木 植物 植える 果物 果実 実 花 茶 油 植木 大木 桜 お茶). None were missing.
- **Other checks:** a grep of `confusable-words.md` (no applicable pairs), a check that the new titles are unique, and live Kotobank pages for 柚 and 椿.

**Verdicts:**
- `kanji\柚.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN
- `kanji\椿.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN
- `words\柚.md`: correctness CLEAN; scoped coverage NEEDS FIX; comprehensibility CLEAN
- `words\椿.md`: correctness CLEAN; scoped coverage NEEDS FIX; comprehensibility CLEAN

**Findings:**
1. Minor; scoped coverage (quiz guards); `words\柚.md:8` and `words\椿.md:8`.
   - **Claim and impact:** Both words exclude 木 ("tree; wood") and 植物 ("plant; vegetation") as broader categories, but not 植木 ("garden tree; potted plant"). That term is just as broad, and both articles' own examples show a garden tree: 庭に柚の木を植えました and 庭の椿が咲きました. In the English-to-Japanese quiz, a learner shown "garden tree; potted plant" could reasonably pick 柚 or 椿. All three articles share the `plants` tag, so the automatic choices may well put them together.
   - **Remedy:** Add 植木 to both `quiz_exclusions` lists, or record why it differs from 木.
   - **Evidence:** the actual displayed titles; `content-format.md` (when to add an exclusion).
   - **Confidence:** medium. The ambiguity is mainly in one quiz direction, and the omission may be a deliberate judgement.

**Optional:**
- `kanji\椿.md:43`: the note about 山茶花 さざんか guards against a confusion the card never sets up. 山茶花 contains no 椿, and this card does not say that 山茶 is another spelling (and the Chinese name) of つばき; only the word article explains that. Add that context or drop the line.
- 椿 also names *Toona* (チャンチン, Chinese mahogany) in 香椿 and in one plant-name dictionary. This could be mentioned as recognition-only.
- 字通's (Jitsu's) classification of 柚 as 形声 (phonetic compound with 由 as the sound component) could be cited as one source's view. The current labelled mnemonic and `structure-unclassified` tag are acceptable.
- 柚子 can be read as ゆ + ず (the ス on'yomi of 子, voiced). The current "not freely reusable" wording is acceptable.

**Limits:**
- **Not fetched:** the 晩白柚 and 珍事 Kotobank pages. Those senses rest on the supplied JMdict packet (the 椿事 incident sense is marked "esp. 椿事").
- **Kotobank 柚 page:** confirmed the Daijisen ゆず heading and Jitsu's loom sense (織機のたてまき, ジク).
- **Kotobank 椿 page:** confirmed Seisenban つばき sense 1, including the alternative spelling 山茶.
- **Frozen packets:** I treated them as supplied evidence, not fresh upstream retrieval.
- **Not run:** validation, the app, or any native-speaker or phone check. Phone readability is not measured.
- **Tool calls:** I made exactly one call per response, with no parallel calls or delegation. I can't see the runtime's internals, so I can't confirm there was no hidden overlap.
