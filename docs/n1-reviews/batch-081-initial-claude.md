**Snapshot:** b7bf953d137251f179a57128bb84bd70a37737c8, using only the supplied packet. I did no independent Git, hash or upstream checks.

**Scope:** Reviewer model: Claude Opus 5.5 (claude-opus-5.5). I read `control\batch-081-initial-packet.txt` in one `view` call with `forceReadLargeFiles=true` and no range, and made no further reads. There was no truncation marker. The tool showed no line or byte count, so the 2288-line, 121246-byte size is unconfirmed.

Reviewed:
- `kanji\冶.md`, lines 1–67
- `words\冶金.md`, lines 1–54
- the added bullet at `kanji\金.md:39`

I also checked the nine comparison bodies, the diff, the JMdict entries (25 occurrences; 24 distinct, with 1536310 appearing twice), the five KANJIDIC2 records, the stroke file, the metadata JSON, the instructions and the supplied dictionary observations.

**Verdicts:**

| File | Correctness | Scoped coverage | Text comprehensibility |
| --- | --- | --- | --- |
| `kanji\冶.md` | CLEAN | CLEAN | CLEAN |
| `words\冶金.md` | CLEAN | CLEAN | CLEAN |
| `kanji\金.md:39` bullet | CLEAN | CLEAN | CLEAN |

**Findings:** None. Basis for each check:

- **Metadata:** The readings keep the source order, ヤ then い.る. Only ヤ is selected (`quizOnyomi: [ヤ]`) and its row has its own 冶金 link. `quizKunyomi` is explicitly empty. Grade 8, 7 strokes and radical 冫 (no. 15) all match KANJIDIC2 and the KanjiVG stroke file, and the card distinguishes 冫 from 氵 (radical 水).
- **い.る row (lines 38–43):** It is clearly marked as source-only. It does not invent a word written 冶る, treats 鋳る as a separate spelling, and makes no frequency or register claim.
- **Mnemonic and structure:** The mnemonic is labelled as an invented memory aid, not history or sound. The `structure-unclassified` tag does not deny a phonetic component. N1 is labelled as a community list, and 冶金 has no invented word level.
- **Related words:**
  - 陶冶 is given as figurative cultivation, matching JMdict 1655600 sense 1.
  - 鍛冶 is read かじ as a whole word (JMdict marks this reading gikun/jukujikun). No ジ is added to 冶's readings, and the separate reading たんや is noted.
- **冶金.md:**
  - It is described as the technical field, not money, gold, alchemy or simply melting.
  - 製錬 and 精錬 are presented as related processes. The training sense is limited to 精錬 and is not mentioned.
  - The noun is not used as a する verb, which matches JMdict.
  - Both example sentences are original, and their kana, particles, ている forms and English are correct. The "action + object" explanation is labelled as an aid, not word history.
- **Wrong kanji choices:** The titles of 治 ("govern; heal"), 台 ("stand, machine counter") and 始 ("begin, start") do not overlap with 冶's meanings, including their ordinary secondary senses. The supplied word labels ("metal", "melt or dissolve something", "melt; dissolve") are distinct from "metallurgy", so no direct exclusion is shown to be needed.
- **Links:** All four directions are present (冶↔冶金 and 金↔冶金), with the reading やきん.

**Optional (nonblocking):**
- `冶.md:38`: the phrases "inspected families" and "source-only… lookup information" are author jargon; plainer wording would read better on a phone.
- `冶.md:52–58`: could note that JMdict marks 鍛治 as an irregular spelling, which relates to the 冶/治 confusion. Could also say that たんや uses the regular ヤ reading.
- `冶金.md:45–46`: could mention that 錬金術 also has a "money-making" sense (JMdict 1559970 sense 2).
- `金.md:39`: could add "(technical)" for N5 learners.
- `冶.md:64`: could give the KANJIDIC2 version (2026-306).

**Limits:**
- No independent Git or upstream verification. The Kotobank observations were supplied by the coordinator, not retrieved by me.
- There is no evidence on native naturalness, fonts or drawing, the UI or phone, live random-quiz pools, or learning effectiveness.
- I did not check title uniqueness across all cards, whether the linked 女.md exists, or 始's raw KANJIDIC2 record (it isn't in the packet).
- If 溶 ("melt; dissolve") appears as a fallback quiz choice, it might look plausible for 冶. This is an unconfirmed hypothesis.
