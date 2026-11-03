All ten screenshots are visually comprehensible, and I found no missing or misleading glyphs; there are no new findings. The only notable artefact is that the sideways-scrolled readings table cuts off the left column, so コウ and ゴウ both show as "ウ" in that one frame.

**Snapshot:**
- Frozen tracked content `ed1109fab7c61d0458edb4ba3e6d0cee3f1045a8`; the teaching is unchanged from `1133566c7a738c2f13b4b67afc4974fcba834c19`. Both hashes are as supplied; I could not check Git (no shell).
- One untracked, non-runtime file, `N1Batch039NativeTest.kt`, is accounted for. I am not claiming the whole worktree is clean.
- I made no independent check of image bytes, hashes or dimensions; the view tool may resize images.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), the same session as the initial and confirmation reviews. This is a dependent visual confirmation, not a blind textual review.
- **Reads, made one at a time:** the task prompt; my two archived reports (`batch-039-initial-claude.md` and `batch-039-confirmation-claude.md`); lines 195–244 of the fixture `N1Batch039NativeTest.kt`; and exactly the ten attempt-2 PNGs.
- **Inherited without rereading:** textual correctness, scoped coverage and source findings from my earlier reports.

**Fixture check (lines 195–244):**
- Line 214 reads `await("Common words")`, followed by `section("Common words")` on line 215, which matches the stated one-line diff.
- This is static code only. It is not evidence that the native run happened.

**Verdicts:**
- **Inherited from my earlier reports (not reassessed here):** correctness and scoped coverage are CLEAN for all three articles. My original origin finding remains withdrawn as a defect; the historical explanation is optional.
- **Fresh visual comprehensibility, bounded to what the screenshots show:**
  - `kanji\鴻.md` (mnemonic, look-alikes and source-only-readings screens): CLEAN.
  - `words\鴻.md` (example and components screens): CLEAN.
  - `words\鴻鵠.md` (attested-phrase, reading-boundary and components screens): CLEAN.
- **Four font families (font-pairs fixture screen):**
  - Gothic, Mincho, Textbook and Brush each render 鴻, 鵠, 紅 and 鳴 as distinct glyphs.
  - The left components are clearly different: 氵+工 in 鴻, 告 in 鵠, 糸 in 紅 and 口 in 鳴. All four contain a visible 鳥 except 紅, as the on-screen caption states.
  - Changes in typeface do not hide these distinctions. This screen is a test fixture, not a production card.

**Findings:** none.

**What is visible in each screen:**
- **Mnemonic screen:**
  - The mnemonic about 江 beside 鳥 and its disclaimer ("not a historical or phonetic rule") render in full.
  - The readings table first shows コウ and ゴウ. The right-hand "Typical words" column is cut off at the edge, and a "Scroll sideways to read all columns" hint is shown.
- **Look-alikes screen:**
  - The notes on 紅, 鳴 and 島 render in full, as do 糸, 工, 口 and 山.
  - The おおとり note shows real glyphs for 大鳥, 鳳 and 鵬, plus the 鳳凰 link and 大トリ. Nothing renders as a missing-glyph box.
- **Source-only-readings screen:**
  - This frame is scrolled sideways, so the left column is cut off. Both on-reading rows display only "ウ", and おおとり shows as "おとり".
  - The ゴウ qualification ("Qualified source-only reading… Not selected for questions") and the おおとり recognition-only row are fully readable.
  - The ひしくい and おおがり rows are below the visible area.
  - The unscrolled mnemonic screenshot shows コウ and ゴウ in full, so this is a scroll-position artefact, not a content defect.
- **鴻 word screens:**
  - Both example sentences, their kana readings and translations render, including the less common kanji 鑑 and 雁.
  - The components, synonyms and reading-boundary sections render in full, covering おおとり, おおがり, ヒシクイ and ガチョウ.
  - The dictionary links at the very bottom are cut off by the screen edge.
- **鴻鵠 screens:**
  - 鵠 renders clearly in the title and the body.
  - 鴻鵠の志 (こうこくのこころざし) and its proverb explanation are readable.
  - The コウ/コク component explanation, the long-vowel boundary for こうこく, and the 偉大 and 鷹揚 contrasts are all visible.
- **Selection screen:**
  - It shows "N1 · 71 cards" and "0 due, 10 new". Drawing and Readings are locked behind the meaning-quiz requirement.
  - A still image does not prove queue or navigation behaviour.

**Optional (cosmetic, not defects):**
- **Line wraps:** several kana words break across lines, such as "ひしく / い", "く / ぐい" and "コ / ク". They remain readable.
- **Table width:** the readings table needs sideways scrolling, and a partly scrolled frame can hide the on-reading prefixes.
- **Carried over from my confirmation report:** the hedged phonetic-origin sentence, the 偉大 quiz-guard hypothesis and the 鳳凰 hypothesis remain nonblocking.

**Limits:**
- **Earlier process issues preserved:** in the confirmation session I made one call containing both a glob and a view (a breach of the one-call rule). In that session I also cited `content-structure` lines 40–47 instead of the actual origin-rule lines 50–55, and relied on my earlier full reading for the origin rule. In this session every call was made serially.
- **What the images cannot show:** they cover only bounded viewport regions, not whole tables or whole articles. They do not prove navigation, reciprocal links, system-back behaviour, the Room database keys, glyph-probe hashes or queue behaviour; those operational claims are as supplied.
- **Not retested:** I did not re-run any meaning, reading or drawing session.
- **Not accepted here:** this does not amount to physical-phone, native-speaker, current-main, CI, public-ZIP or publication acceptance. A compatible Android build `f9b59a2` or later is required, and phone/general-release acceptance remains outstanding, though that is not a veto on owner testing.
