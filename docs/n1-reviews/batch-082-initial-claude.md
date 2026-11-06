**Snapshot:** b6bcc8f144cd781917abdb2ca510f663d1339a56, as given in the packet. I did not check it against Git or upstream myself.

**Scope:** Claude Opus 5.5 (claude-opus-5.5). I made one `view` call on `control\batch-082-initial-packet.txt` with forceReadLargeFiles=true and no view_range. It returned no truncation notice and ended with the "MECHANICAL SCOPE AND ACCEPTANCE LIMITS" section, so no ranges needed recovering. The output had no line numbers, so I could not confirm the 3,084-line count myself.

I read:
- all 17 comparison bodies, including `kanji\准.md` (lines 1–65) and `words\准教授.md` (lines 1–62);
- the diff, which matches the two new files, `教.md:39` and `助教授.md:16`;
- 37 dictionary family occurrences (36 distinct);
- seven raw KANJIDIC2 character records;
- the input metadata, the stroke JSON and the instruction excerpts;
- two dictionary observations supplied by the coordinator. I did not fetch these myself.

I used no other files, reports or author adjudication.

**Verdicts:** "CLEAN" here means I found no actionable defect. It does not mean everything is proven correct.

| Item | Correctness | Scoped coverage | Text comprehensibility |
| --- | --- | --- | --- |
| `kanji\准.md` | CLEAN | CLEAN | CLEAN |
| `words\准教授.md` | CLEAN | CLEAN | CLEAN |
| `kanji\教.md:39` (added bullet) | CLEAN | CLEAN | CLEAN |
| `words\助教授.md:16` (added link) | CLEAN | CLEAN | CLEAN |

**Basis:**

*`kanji\准.md`*
- **Metadata (lines 2–12):** The raw KANJIDIC2 record supports 10 strokes, radical 冫 (no. 15), grade 8, on ジュン and no kun readings. The stroke JSON also has 10 strokes. The quiz selection (ジュン only, kun disabled) has its own row with a linked 准教授 example. The card adds no readings from other dictionaries and doesn't deny them.
- **Meaning (lines 22–28):** It covers both the associate-rank sense and the approval sense (批准 ひじゅん, entry 1483390, "ratification"). That matches Daijisen. Line 28 correctly warns that not every 准 compound is a rank.
- **Relation to 準 (lines 51–57):** The shape contrast is correct (氵 and 十 in 準, 冫 in 准). No spelling swaps are suggested: 準備, 基準 and 批准 have no alternate 准/準 spelling in their entries. 準教授 is listed in 2178020 as an unflagged second spelling, which the card notes, while teaching 准教授 as the current title.
- **Mnemonic (lines 30–32):** It is labelled as a modern-shape mnemonic, not etymology. `structure-unclassified` is kept without denying a phonetic component. N1 is described as a community list.
- **Distractors 集/進/難:** Their titles are gather, advance and difficult. Their ordinary secondary senses (collect, concentrate, progress, trouble) don't overlap with "quasi-; associate rank" or with approval. The shape notes in lines 58–60 are accurate.

*`words\准教授.md`*
- The reading じゅんきょうじゅ, noun-only use and ジュン + キョウ + ジュ allocation match the dictionary data. 准 is correctly treated as a modifier on the head 教授, with 教 = teaching and 授 = imparting.
- The April 2007 replacement of 助教授 matches the Nipponica observation. 助教 and 助手 are kept as separate roles, and 先生 is presented as broader.
- It explicitly rejects 准教授する, the "half professor" reading, automatic promotion and exact international equivalence.
- Both example sentences, their kana, particles and English are accurate and natural. They are not presented as attested quotations.
- The quiz exclusion of 助教授 is the necessary direct pair. Titles such as 教授, 講師 and 助手 differ in actual meaning, not just wording, so I found no further pair that needs excluding.

*Changed reused passages*
- The `教.md:39` bullet uses the correct link (`../words/`), reading and gloss.
- `助教授.md:16` links to `准教授.md` correctly from within `words\`, with the reading.

*Links*
- Mapped pairs: 准↔准教授 (`准.md:23,38,46` and `准教授.md:29`) and 教↔准教授 (`教.md:39` and `准教授.md:30`).
- Navigation between the titles: 准教授→助教授 (line 37) and 助教授→准教授 (line 16).

**Findings:** None proven.

**Optional:**
1. **Quiz hypothesis (unproven).** `準.md:20` itself teaches "semi-, quasi-, or associate," so in an uncurated, larger-pool 準 quiz, 准's title could be a defensible answer. The default four-choice quiz uses 準's curated 集/清/卒, so the default quiz is unaffected.
2. `准.md:38` could also list 批准 as a ジュン example. 准看護師 (current) or 准尉 could also illustrate the rank branch.

**Limits:**
- I did no independent Git or upstream verification. The Kotobank and Nipponica material was supplied evidence.
- I could not check that the title is unique across all cards, or the existence of a 授 card.
- I have no evidence on native-speaker naturalness, font, stroke drawing, UI, phone display, live quiz behaviour or learning effectiveness.
