I found no defects in the four teaching files; every facet of each file is CLEAN. I made one process error during the review, described under Limits.

**Snapshot:** Supplied signed snapshot `2567f5e7b3888f2df3ed560f618341266b471902`, with no uncommitted teaching changes. I had no Git or shell access, so I couldn't confirm the SHA or the working-tree state myself. I reviewed the files as they are on disk in `C:\Users\stop-\n1-kanji-workspace\learning-japanese`.

**Scope:** Reviewer model: Claude Opus 5.5 (`claude-opus-5.5`).
- **Files read in full:**
  - `kanji\俳.md`, which is new and was reviewed completely.
  - `words\俳句.md`, `words\俳優.md` and `kanji\優.md`. In these I reviewed the three changed links and the text closely tied to them; the rest was read as context.
  - The supplied frozen XML: `batch-061-jmdict.xml` (30 entry families), `batch-061-comparison-jmdict.xml` (15 families) and `batch-061-kanjidic2.xml` (7 character records: 句, 借, 人, 俳, 悲, 非, 優).
  - The comparison articles `words\句.md`, `川柳.md`, `役者.md`, `女優.md`, `詩.md`, `詩人.md`, `主役.md` and `演技.md`.
  - The comparison cards `kanji\非.md`, `悲.md`, `借.md`, `芸.md`, `演.md` and `人.md`.
  - The guidance files `.github\copilot-instructions.md`, `content-structure.instructions.md`, `docs\content-format.md` (lines 1–1405) and `docs\jlpt-levels.md` (lines 1–401).
  - The pinned stroke-data SVG `n1-04ff3-70a0b7ae.svg`.
- **Fresh dictionary lookups:** the three assigned Kotobank pages, fetched today.
- **Searches:** the title, distractor and tag lines of the eleven two-distractor cards; kanji titles mentioning haiku, actors or performance; and the relevant rows of `docs\confusable-words.md` (it has none for these words).

**Verdicts:**
- **`kanji\俳.md` (new):**
  - Correctness: CLEAN
  - Scoped coverage: CLEAN
  - Comprehensibility: CLEAN
- **`words\俳句.md`** (changed link on line 25; unchanged context):
  - Correctness: CLEAN
  - Scoped coverage: CLEAN
  - Comprehensibility: CLEAN
- **`words\俳優.md`** (changed link on line 26; unchanged context):
  - Correctness: CLEAN
  - Scoped coverage: CLEAN
  - Comprehensibility: CLEAN
- **`kanji\優.md`** (changed link on line 37; unchanged context):
  - Correctness: CLEAN
  - Scoped coverage: CLEAN
  - Comprehensibility: CLEAN

What I checked:
- **Card metadata matches the source.** The kanji dictionary record for 俳 gives:
  - the on reading ハイ only, with no kun reading;
  - 10 strokes, radical 9 and school grade 6;
  - the meanings "haiku" and "actor".

  The card keeps this metadata exactly. The practice lists offer ハイ only, have an empty kun list, and link the reading's own examples 俳句 and 俳優. The stroke data also has 10 strokes, with 亻 marked as a variant of 人 next to 非.
- **The radical, origin and look-alike notes are handled correctly.**
  - The card explains 亻 as the side form of 人 and keeps 人 as the indexing radical.
  - The memory aid is labelled as a modern-shape mnemonic, not etymology.
  - The card makes no phonetic claim, even though the stroke data and the 字通 kanji dictionary both name 非 as the sound component. Leaving it out is allowed.
  - The notes say 非 does not turn these words into negations.
- **Word identities and readings match the dictionary.** 俳句/はいく is entry 1471900 and 俳優/はいゆう is entry 1471970, split as ハイ+ク and ハイ+ユウ. Their vocabulary levels (N2 and N3) are kept. The haiku rule is described in Japanese morae with exceptions, which matches JMdict and the 日本国語大辞典 entry. Nothing teaches the rarely used 俳徊 spelling, organisation names, the historical わざおぎ reading or extra meanings as metadata.
- **The 優 performer sense is supported.** The kanji dictionary lists "actor" for 優, and the Kotobank encyclopedia notes that 優 alone was used for performers in Chinese usage.
- **All six reciprocal links are present with correct paths:** 俳→俳句, 俳句→俳, 俳→俳優, 俳優→俳, 優→俳優 and 俳優→優.
- **Quiz safety holds within this bounded check.**
  - The existing quiz exclusions 俳句/句, 俳句/詩, 川柳/俳句, 女優/俳優 and 主役/俳優 remain.
  - 役者 and 俳優 share the exact title "actor; actress"; the app already keeps exactly matching titles apart, as the content format describes.
  - 俳's wrong choices (非 "non-; wrong", 悲 "sadness", 借 "borrow, rent") are look-alikes with clearly different meanings. Performance neighbours 優, 芸 and 演 are rightly not used.
  - The title "haiku; actor" is unique among kanji cards.
  - None of the eleven cards that still have only two wrong choices has a meaning that could make "haiku; actor" a defensible answer. 俳 shares no tags with them. These are 人 person, 休 rest, 何 what, 入 enter, 出 go out, 口 mouth, 女 woman, 日 sun/day, 月 moon/month, 男 man and 買 buy.

**Findings:** None.

**Optional:**
- **"haikai" is unexplained:** `words\俳句.md:25` uses the term without defining it. A short gloss such as "humorous linked verse from which haiku developed" would help English readers. Nipponica and 日本国語大辞典 describe haikai this way.
- **"rows" may misdescribe 非:** `kanji\俳.md:27-28` says "two rows of strokes". The two halves of 非 stand side by side, so "two halves" or "two columns" would describe the shape more exactly.
- **Two unlinked mentions in unchanged text:** `words\俳優.md:31` names 役者 without linking its existing article. `kanji\優.md` mentions 俳優 unlinked on lines 22 and 33. Linking either is optional; the required reciprocal links are already in place.
- **Optional phonetic note:** a sourced note could say that 字通 and the stroke data treat 非 as the sound component. Leaving it out is acceptable.

**Limits:**
- **Serial-rule breach:** in one response I wrongly sent three reads of `batch-061-jmdict.xml` at once (lines 150–300, 300–450 and 450–487), which broke the one-call-per-response rule. Every other call was sent on its own, one per response. This affected execution order only, not what was read.
- **Kotobank coverage was partial:**
  - **俳:** the デジタル大辞泉 section shows only its publisher heading, with no definition. 日本国語大辞典 and 字通 gave definitions.
  - **俳句:** デジタル大辞泉 again shows only its heading. I read 日本国語大辞典 and the first part of Nipponica from the saved output (20.9 KB). The rest of the encyclopedia history was not read.
  - **俳優:** across two fetches, only 世界大百科事典 encyclopedia material came through: the modern actor, the Chinese 俳優/優 usage and the historical わざおぎ. No modern dictionary entry was extracted, so the modern meaning rests on JMdict.

  The frozen XML is supplied evidence; the Kotobank pages are my own fresh retrievals.
- **What wasn't run or certified:**
  - I didn't run the validator or the manifest build, and didn't read the app's quiz code. My fallback analysis relies on the documented behaviour.
  - Larger, random or live quiz pools are not covered.
- **No device testing:** no native-speaker or physical-phone evidence was supplied. My reading of the text doesn't certify how glyphs render or how stroke drawing works. A compatible Android build (`f9b59a2` or later) is required, and phone/general-release acceptance is still outstanding.
