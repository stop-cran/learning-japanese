**Snapshot:** 27e252daa091e21c907ff6799818f6b2da74c7aa, using only the packet's signed snapshot and frozen-draft diff. The two new articles' SHA-256 values are 45ea30bf… and ee7f12d1….

**Scope:** I reviewed the new `kanji\勁.md` (lines 1–47) and `words\雄勁.md` (lines 1–37). I checked them against:
- the 49 existing comparison bodies;
- 9 member and 28 comparison JMdict entries, which make 36 distinct families because 1236070 appears in both sets;
- the KANJIDIC2 records for 勁, 雄, 強, 剛, 力, 勢, 功, 劾 and 剖;
- the KanjiVG SVG, the generated stroke JSON and the reading code in `KanjiReadings.kt`;
- four archived Digital Daijisen texts (勁, 雄勁, 勁草, 雄) and their receipts.

There are no changed reused passages. The model is Claude Opus 5.5 (`claude-opus-5.5`). I used one `view` call with `forceReadLargeFiles=true` and made no further reads.

**Verdicts:**
- **勁.md:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- **雄勁.md:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.

**Findings:** None proved.

**Key checks that passed:**
- **Reading metadata:** KANJIDIC2 gives on [ケイ] and kun [つよ.い], in that order, and the card keeps them. The quiz lists select [ケイ] for on'yomi and nothing for kun'yomi.
- **Offered reading question:** Using `quizReadings`, the only question offered is on'yomi with match key けい, which `display()` shows as ケイ. No kun'yomi question is offered. The full list still keeps つよい from being used as a wrong answer for this kanji.
- **Reading table:** The ケイ row links 雄勁 as its own example.
- **The 勁い spelling:** It matches JMdict 1236070, where 勁い is marked as a search-only form. The card advises using 強い and does not call the documented つよい reading invalid. The link to 強い is described as spelling guidance, not as a word written with 勁.
- **How ゆうけい divides:** ユウ + ケイ comes from character evidence, not kana substrings: Daijisen gives 雄 ［音］ユウ and 勁 ［音］ケイ, lists 雄勁 under 勁, and splits the heading as ゆう‐けい【雄×勁】.
- **Level and grade:** The card marks N1 as a community list. 雄勁 has no inferred word level. Grade 9 is explained as name-use metadata, which matches Daijisen's ［人名用漢字］ label.
- **雄勁 grammar and example:** It is a noun and na-adjective in both JMdict (adj-na, n) and Daijisen (名・形動). 雄勁な筆跡 (ゆうけいなひっせき, "vigorous handwriting") is attested in Daijisen, and 筆跡 is read ひっせき. The な attachment and polite 雄勁です are correct.
- **Meaning:** The article explains that 雄 and 勁 both contribute strength. It says this is a meaning aid, not etymology, and rules out a male-only reading.
- **Comparisons:** The 力強い comparison separates its reassuring sense, which matches JMdict 1554940 sense 2.
- **Shape data:** Radical 力 (no. 19) on the right, 9 strokes, 巠 on the left; the KanjiVG data and generated paths agree. The mnemonic is labelled as a modern-shape aid with no claim about a sound component.
- **Quiz choices:** The displayed labels match the actual cards. The wrong choices 功, 劾 and 剖 have clearly different meanings. The four kanji pairs and six word pairs that keep near-synonyms apart are defensible and don't overlap the wrong choices.
- **Links:** The one required two-way link pair, 勁 and 雄勁, works in both directions with the correct reading ゆうけい. No existing (baseline) cards were edited, and 雄 is listed in the word's kanji metadata without needing a card.

**Hypotheses (not proved defects):**
- **雄勁 vs 活気 ("liveliness; vigor"):** These might appear together as word-quiz choices; both are tagged kango and noun, which the fallback selection may favour. The shared English word "vigor" overlaps. However, 活気 means liveliness of an atmosphere, while 雄勁 means force of expression. Low impact; confidence low.
- **雄勁 vs もりもり ("heartily; full of vigor"):** "Full of vigor" loosely echoes Daijisen's 力がみなぎっていること for 雄勁, but the もりもり label leads with eating ("heartily"). Low impact; confidence low.

**Optional:**
- **Hedge two lines:** 勁.md:23 and :31 present art and prose without the "especially" hedge used at line 38 and in 雄勁.md:33. Adding "characteristically" would make them consistent.
- **Title wording:** The 雄勁 title "vigorous style (art; prose)" reads like a noun for a style. JMdict glosses the word as "vigorous; powerful". Something like "vigorous; powerful (esp. art, prose)" would be closer.
- **Gloss for 雄 (雄勁.md:21):** "Imposing" could be replaced with Daijisen sense 2, 勇ましく強い ("brave and strong").
- **"Search-only" (勁.md:32):** Briefly explaining this JMdict term would help learners.
- **"Practiced as けい" (勁.md:34):** The visible reading label is probably ケイ. The answer-option label code was not in the packet.
- **Extra example:** 勁草 was archived and could be added as a recognition example.

**Limits:**
- **Read completeness:** No truncation marker appeared, and the final section (`docs\jlpt-levels.md`) ended at its declared line 23. I did not separately confirm the 5,129-line count.
- **No independent sources:** I did no Git or upstream checking. The Daijisen texts are the coordinator's extractions.
- **Fonts:** No font cmap data was in the read text. Font coverage, native-speaker review, stroke-drawing, rendered-UI and physical-phone checks were not available.
- **Not covered:** Live quiz pools (default N1, All, custom) and future-pool safety are not certified, and nothing here measures learning effectiveness.
