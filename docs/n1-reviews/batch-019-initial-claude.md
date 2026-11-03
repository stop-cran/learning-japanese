**Snapshot:** commit `3e2bf34ee3b9621cbaec8713f2b157fdeb74c764`. Committed content only; no uncommitted teaching was included.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), a single blind initial reviewer.
- **Guidance read in full:** `.github\copilot-instructions.md` lines 1–160 and 161–218, `content-structure.instructions.md`, `docs\content-format.md` lines 42–148 and `docs\jlpt-levels.md` lines 1–110.
- **Teaching files read in full:** `kanji\蚊.md` and `words\蚊.md`, covering correctness, scoped coverage and comprehensibility.
- **Metadata:** all of `batch-019-input-metadata.json`.
- **Dictionary packets, every line returned:**
  - `jmdict.xml` lines 1–200, 201–400, 401–600, 601–800 and 801–999.
  - `comparisons-jmdict.xml` lines 1–200 and 201–312.
  - `notes-jmdict.xml` lines 1–186.
  - `supplement-jmdict.xml` lines 1–200 and 201–366.
- **Comparison cards read in full:** kanji 文, 枚, 改, 虫 and 蛍; words 虫, 蛍 and 刺す.
- **Confusable pairs:** a scoped search of `confusable-words.md` for 蚊, 虫 and "mosquito" found no entries.
- **Web sources:** the Kotobank 蚊 page (raw HTML from character 64000 onward) and the Kotobank 飛蚊症 page.

**Verdicts:**
- `kanji\蚊.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\蚊.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

What I checked:

- **Metadata:** the card matches KANJIDIC2 exactly. Readings are ブン and か (in that order), with grade 8, 10 strokes, radical 142 and JLPT 1.
- **Readings and allocation:**
  - Digital Daijisen's character entry for 蚊 gives the on reading ブン and the kun reading か. It lists 飛蚊症 under ブン and 蚊柱 and 家蚊 under か. It marks 蚊帳 かや as a hard-to-read word.
  - Selecting only か for quizzes (`quizKunyomi [か]`, `quizOnyomi []`) is defensible. JMdict 1626600 tags 飛蚊症 as a medical term.
  - The claim that 飛蚊症 is a symptom, not an actual mosquito, is supported by the Nihon Kokugo Daijiten (Seisenban) definition: things appear to fly before the eyes like mosquitoes or threads.
- **Word article:**
  - JMdict 1196540 supports か, plus katakana カ (a kana-only form).
  - The original N2 level (`jlpt: 2`) is preserved.
  - Both example sentences and their translations are natural.
  - Saying に marks the source of the bite in the passive agrees with the 刺す article (actor in a passive sentence) and JMdict 1306470 sense 2.
  - Both changed links resolve: `../kanji/蚊.md` and `虫.md` (the word article).
- **Shape comparison and mnemonic:** 枚 and 改 both have the four-stroke 攵 on the right, which has a slanting top. 文 in 蚊 has a dot and a horizontal stroke on top. The mnemonic is labelled as not etymology and makes no claim about the origin of the pronunciation.
- **Quiz:** the three wrong-answer labels ("sentence, writing", "counter for thin flat objects", "revise; reform") cannot reasonably be taken to mean "mosquito". With three supplied, the default four-choice quiz needs no fallback choices. Excluding 虫 from 蚊 is justified because a mosquito is an insect/bug. "firefly" versus "mosquito" needs no exclusion.

**Findings:** none.

**Optional:**
1. In `words\蚊.md`, "一匹 (いっぴき), 'one'" could say "one (small creature)".
2. 蚊帳 かや appears in both files without saying that its reading belongs to the whole word, so it should not be split by character. Daijisen marks it as hard to read.

**Limits:**
- **Daijisen 飛蚊症 text:** the body was not extracted; only the heading appeared, so the compound's meaning rests on the Seisenban entry. The two gaiji numbering images in the 蚊 character entry were not rendered, but the surrounding text was readable.
- **"Not かあ" note:** the kanji card's statement that ordinary modern か is not pronounced かあ is unsourced. It is low-stakes and qualified, and I found no evidence against it.
- **Confusable pairs:** I only searched `confusable-words.md`, not the full inventory.
- **Phone and native checks:** this was a textual review only. It gives no fresh native, phone, Android, combined-main, CI or public ZIP evidence.
- **Process deviation:** I sent one pair of reads together (`content-structure.instructions.md` and `content-format.md`), contrary to the one-call rule. Every other call was serial. The deviation affected order, not content.
