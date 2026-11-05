**Snapshot:** Signed frozen SHA `5bfb668dae3b2acd99720d88a15e5fc2feb397ae`, as supplied. I made no edits, fixes, commits or issues. I had no shell, so I could not check HEAD, uncommitted changes, the diff or the signature myself.

**Scope:** Exposed model: Claude Opus 5.5. I read every assigned range, one tool call at a time:
- **Cards and articles:** all of 儀; the four word articles; 辞/式/礼/行; 億/優/倍/人.
- **Frozen sources:** both JMdict files (146 entries in total); all 10 KANJIDIC2 records; the stroke JSON and the pinned SVG at revision 70a0b7ae.
- **Guidance:** the assigned instruction and docs ranges.
- **Quiz:** one search of titles for the 11 fallback candidates, and one search of kanji titles mentioning ceremony, conduct, manners or ritual.
- **Fresh Kotobank fetches:** the five Kotobank URLs (儀, 儀式, 礼儀, 行儀, 地球儀).

**Verdicts:**
- **儀:** correctness CLEAN; scoped coverage NEEDS FIX; comprehensibility CLEAN.
- **お辞儀, 儀式, 礼儀, 行儀** (only the new 儀 link, read in context): all three facets CLEAN.
- **辞, 式, 礼, 行** (only the new Common-words backlink): all three facets CLEAN.
- **Links:** all 8 reciprocal pairs and 16 directed links are present and point to the right files. Each linked reading matches JMdict: おじぎ, ぎしき, れいぎ, ぎょうぎ.

**Findings:**
- **Minor; scoped coverage; `kanji/儀.md:50-52`.**
  - **Claim and impact:** The card says 儀 can follow "a person's name or a personal pronoun". It doesn't say this use is limited to oneself or one's own side and adds humility. A learner could put it after anyone's name, such as a superior's.
  - **Remedy:** Say that it follows nouns for oneself or one's own side, as in 私儀, and has a humble nuance in letters and notices.
  - **Evidence:** The Nikkoku 儀 entry that the card cites (fetched fresh) gives the suffix sense as 自分、または自分の側を示す名詞に付いて… 謙譲の意を添える. Frozen JMdict 1311150 私儀 is also self-referential. JMdict 1224690 is broader: "after a person's name, personal pronoun, etc."
  - **Confidence:** Medium. The sources differ in breadth.

**Checks with no defect:**
- **Metadata:** ギ is the only on reading and the kun list is empty. The ギ practice key has its own table row linking 儀式. 15 strokes, radical 人 (no. 9), grade 8 and the visible 亻 all match the sources.
- **Origin:** The shape mnemonic is clearly labelled as not historical.
- **Meanings:** The "matter; affair" branch and the 地球儀 counterexample are supported. 地球儀 is an Earth-globe model in both JMdict and Nikkoku.
- **Word articles:** 礼義 is only a search form, and the 礼儀 article doesn't teach it. 行儀 is neutral until いい or 悪い adds the judgement. The お prefix and ジ+ギ base are supported by JMdict 1733730. 儀式 includes "service".
- **Quiz:** The curated distractors 億/優/倍 have unrelated titles. None of the 11 fallback titles overlaps.

**Optional:**
- The 行 card's note says "ギョウ is for line/event", which now sits beside 行儀 (conduct). A small tweak would help.
- 義 is the phonetic according to KanjiVG and 字通. The card's unclassified label is still acceptable.
- The source lines on 辞, 式 and 礼 don't list the newly linked words' JMdict entry numbers.

**Limits:**
- Kotobank's デジタル大辞泉 sections returned only headings; the 地球儀 page was cut off after the relevant entry.
- お辞儀 was checked only against the frozen JMdict.
- I didn't check whether 儀 is in the N1 snapshot.
- In larger, random or live quiz pools, 式 ("ceremony; formula") or 祭 ("festival; ritual; worship") could appear as near-synonym answers. This is unverified.
- This is a text-only review: no native-speaker, font, rendering or phone checks. It assumes Android f9b59a2 or later for reading curation.
