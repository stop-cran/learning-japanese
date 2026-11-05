Both halves of the frozen lexical file now show all 16 entries, and they confirm my original teaching conclusions. I found no content defect. This step made exactly one tool call: lines 141–275, which returned in full through the closing `</JMdict>` tag.

**Snapshot:** Teaching at ea1dac1a6fd2c452db9cf602442e1f287ff95c67, with no edits. The empty diff since that commit is your evidence; I couldn't check Git myself.

**Scope:** Claude Opus 5.5 (claude-opus-5.5), original session 34dbb43d-2a7f-4fa9-9e45-00c50c1281a1.
- **Fresh in the supervised steps:** two separate reads of `batch-060-jmdict.xml`, one call each — lines 1–140 in the previous step and lines 141–275 in this one.
- **Carried over, not reread here:** the four teaching files, last returned during the failed followup and unchanged since. Also the 35 comparison families, the KANJIDIC2 records, the comparison articles, the guidance files, the SVG and the Kotobank pages.
- **Your evidence, not my lookup:** 亭's membership in the N1 source list.

**The 16 entries:**
- **Lines 1–140:** 1434150 亭午, 1434160 亭主, 1434170 亭主関白, 1554300 料亭, 1756930 旗亭, 1776960 亭々/亭亭, 1893280 池亭, 1916170 旅亭, and the start of 2149880.
- **Lines 141–275:**
  - 2149880 亭主の好きな赤烏帽子 (ていしゅのすきなあかえぼし): a proverb, "even an eccentric head of family must be obeyed"
  - 2418970 知らぬは亭主ばかりなり, also written 知らぬは亭主許り也: an idiom, "the husband is always the last to know"
  - 2559160 勘亭流 (かんていりゅう): Kantei style of calligraphy
  - 2567560 涼亭 (りょうてい): marked archaic; a garden pavilion or gazebo
  - 2589430 亭: see below
  - 2828839 泉亭 (せんてい): arbor facing a spring
  - 2837195 席亭 (せきてい): entertainment hall, or its manager
  - 5454792 石亭 (せきてい): a company name, Sekitei (ryokan)
- **2589430 亭:** the pavilion noun has no reading restriction, so it can be read てい or ちん. The two suffix senses, for pen names of writers and performers and for restaurant names, are restricted to てい.
- **1554300 料亭 (りょうてい):** a noun, "ryotei", explained as a traditional Japanese restaurant, especially a luxurious one.
- **2567560 涼亭:** a separate word with the same kana as 料亭, meaning an archaic garden pavilion. It is not an alternative spelling of the restaurant noun.

**Verdicts:** These match the teaching text as I read it before, so my original verdicts stand.

| File | Correctness | Scoped coverage | Text comprehensibility |
| --- | --- | --- | --- |
| `kanji\亭.md` | CLEAN | CLEAN | CLEAN |
| `words\料亭.md` | CLEAN | CLEAN | CLEAN |
| `kanji\料.md` (added Common words line) | CLEAN | CLEAN | CLEAN |
| `kanji\停.md` (added memory-aid link; no pronunciation claim) | CLEAN | CLEAN | CLEAN |

**Findings:**
- **Content:** none.
- **Process:** two earlier runs broke the serial-read rule and remain on record.
  - **060-P1 (initial review):** two read calls overlapped in one response.
  - **060-P2 (dependent followup):** six read calls went out in one response.

  The two supervised reads in this step and the previous one were each a single authorized call. They do not make those earlier runs compliant after the fact.

**Optional:** none new. Your earlier decisions not to adopt O1, O2, O3 or the KanjiVG 丁 sound-component annotation are unchanged.

**Limits:** The XML is the frozen file supplied with the batch; I fetched nothing from upstream. The teaching-file reads and the comparison and source context are carried over, not reread here. This covers the text only — no native-speaker, phone, font, stroke-drawing, live-quiz, Android, validation or publication checks.
