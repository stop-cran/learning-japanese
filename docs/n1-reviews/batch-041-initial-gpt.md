**Snapshot:** `75b4ae840933a9002d07a0bfa549539cea0b2554`, identified by the supplied task as the frozen signed snapshot, with no uncommitted teaching included. Git identity, signature and worktree status could not be independently verified with the permitted tools. No files were changed.

**Scope:** Independent initial read-only review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual phone comprehensibility of the complete `kanji\隼.md` and `words\隼.md`.

Read scope completed:
- Entire `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\jlpt-levels.md`; `docs\content-format.md:42–148`.
- Entire batch-041 input metadata, including all seven raw KANJIDIC2 elements: 集・十・準・鷹・鳥・隼・隹.
- All **574 lines / 25 complete families** across the three frozen JMdict packets: seven main families (隼, ハヤブサ科／隼科, 鷹隼, 稚児隼, 白隼, 隼人瓜／隼人うり, 隼人); eleven comparison families (準, 雀, 鷹, 鳥, 鷲, numeric 十, 集, 速, 隹, Chinese-derived 十／シー, spacecraft はやぶさ); seven support families (英雄, 生き物, 生物／せいぶつ, 生物／なまもの, 動物, 勇者, 鴻鵠).
- Entire comparison cards: `kanji\準.md`, `集.md`, `十.md`, `鷹.md`, `鳥.md`; `words\鷹.md`, `鳥.md`, `動物.md`, `生き物.md`, `生物.md`, `鴻鵠.md`.
- All five specified raw-HTML ranges, inspecting the actual Digital Daijisen, 精選版日本国語大辞典 and Kanjipedia entry bodies.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\隼.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\隼.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review—not exhaustive certification.

**Findings:** None.

The complete sourced reading order, `シュン・ジュン` and `はやぶさ`, is preserved. Explicit `quizOnyomi: []` disables on-reading practice rather than invoking omission’s full-list behavior; `quizKunyomi: [はやぶさ]` has its own row and reciprocal word-card link. JMdict 1478360 supports 隼／はやぶさ and marks the noun usually kana; its katakana reading has `re_nokanji`, consistent with teaching ハヤブサ as a kana spelling rather than a kanji-reading substitution.

The recognition example 鷹隼／ようしゅん is supported by complete JMdict 1914500 and the supplied Japanese dictionary entry. Its archaic flag is correctly localized to that compound. Daijisen and Kanjipedia independently *as dictionary sources* document both character readings; the article does not misclassify ジュン as necessarily name-only or manufacture a lexical example for it.

Daijisen’s bird senses and JMdict support the qualified peregrine-falcon/broader-falcon explanation. The two Japanese examples have appropriate particles, readings, tense and English translations. The native-word classification, katakana qualification, spacecraft boundary and separation of character-level figurative meaning from the taught animal noun are sound.

The 隹-over-cross mnemonic is explicitly modern-shape imagery, not invented etymology. The three supplied kanji distractors have actual labels “standard, conform,” “gather” and “ten,” none an ordinary meaning of 隼. Direct word exclusions cover 鷹’s overlapping falcon sense and the four inspected broader-category labels separately; no transitive protection is assumed. The literary, nonspecific 鴻鵠 comparison does not establish an additional mandatory exclusion. The kanji/word 隼 pair links both ways.

**Optional:** None necessary within the assigned scope.

**Limits:** All required reads returned their complete requested content; no truncations or failed reads occurred. The dictionaries were inspected through supplied frozen XML and saved HTML, **not fresh upstream retrieval**; source authenticity, hashes and currency were not independently verified.

The bounded `docs\confusable-words.md` search returned no matching inventory entries. A scoped glob found no 鷲・雀・勇者・英雄 cards; this was not a repository-wide semantic inventory audit. Unchanged comparison cards were inspected for affected integration, not recertified wholesale.

Comprehensibility verdicts concern text, not rendered tables, native glyphs or physical-phone acceptance. No cmap, Android, current-main, CI or public-ZIP checks were performed. Supplied prior acceptance and inherited 隹 disposition are not fresh batch-041 acceptance; compatible Android `f9b59a2+` and outstanding phone/general-release qualifications remain explicit.

Tool calls were issued singly and awaited; no internal tool overlap was observed. No author evidence/adjudication records, other reviews or prior findings were consulted.
