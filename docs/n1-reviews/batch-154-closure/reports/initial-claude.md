# Batch 154 initial review — Claude

## Snapshot

- Commit: f8f3db8c9ae7d88d72cdc3d8eaae84c8f736ca5f (batch 154).
- New kanji cards: 随 隠 隣 雄 雷 霧 項 顕 飼 飽 飾 驚 鬼 鮮 黙.
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-154-f8f3db8c`, manifest sha256 12817983e0c88ddba45c5a38130c88ff9770e8eb246f3e5bdadf1bbf135ca3aa. I did not recompute this hash.
- Reviewer: Claude (Anthropic), the first blind reviewer. I worked alone and read-only.

## Scope

Unit under review:

- the 15 new cards in `snapshot\kanji\`;
- the 15 files in `snapshot\strokes\`;
- the remark-only edits to 塊, 微 and 鏡;
- the 19 link-wrap diffs to word articles.

Packet files I opened:

- **INSTRUCTIONS.md:** read in full.
- **mechanical-checks.md:** read in full, as packaged (several sections are truncated).
- **Directory listings, names only (non-recursive):**
  - the packet root;
  - `snapshot\kanji`, `snapshot\strokes`;
  - `evidence`, `evidence\audits`;
  - `diffs`.
- **`snapshot\kanji\` cards:**
  - 随 隠 隣 雄 雷 霧 項 顕 飼 飽 飾 驚 鬼 鮮 黙: read in full.
  - 塊: lines 1–4 and 27–31, in part.
  - 微: lines 61–81, in part.
  - 鏡: lines 45–53, in part.
- **`snapshot\strokes\*.json` (all 15):** parsed in full for stroke count, id sequence, stroke types and source revision. I printed 黙.json raw.
- **`diffs\` (all 22):** I read the hunk headers and every `-`/`+` line. Unchanged context lines were filtered out.
- **evidence\audits\:**
  - kanji-remarks.json: in full.
  - quiz-safety.txt: in full.
  - reading-exposure.txt: in part (the header, the 随 section, and every "unlisted readings attested" / "attested reading … offered by" line plus the totals).
  - reading-options.txt: in part (the header and the 随, 隠 and 隣 sections).
- **evidence\:**
  - source-metadata.json, kanjipedia-outside-readings.json, kanjivg-components.txt and okurigana-scan.txt: in full.
  - kanjidic2-records.xml: parsed in full (readings, nanori, grade, strokes, variants and meanings for every record).
  - `public-source\*` (15 Weblio/Digital Daijisen extracts): in full.
  - jmdict-families.xml: in part. I extracted entries 2526030, 2409100, 1908340, 1589190, 1584890, 2742870, 2836662, 1839950, 1555830, 2163190, 2077780, 1588840, 1170230, 1170890, 1357210, 2868304, 1364440, 1167860, 1263490, 1263510, 2854409, 1668330, 1616130, 2849868, 2866687, 1623650, 1518320, 1560080, 1381820, 1381910, 1431810, 1534930 and 2513990.
  - jmdict-digest.tsv: in part (rows for each batch kanji, mainly the priority-tagged rows).
  - joyo-pages.md: in part (the page headers and the rows for all 15 kanji).
- **titles\:**
  - kanji-titles.tsv: in part (the header plus pattern searches over titles for semantic neighbours, and the titles of every linked, distractor and excluded card).
  - word-titles.tsv: in part (lines containing the batch kanji).
- **repo\docs\content-format.md:** in part (lines 60–150 plus a grep).

Public web pages I inspected: Kanjipedia 黙 (0006748600) and 顕 (0001973800), the live pages.

Not opened:

- evidence\daijisen-heads.txt, evidence\kanjivg-svgs.txt and evidence\app-code\;
- evidence\audits\word-remarks.json (only its name was listed; mechanical-checks reports it empty);
- full `snapshot\words\` files (I relied on the diffs);
- any repo\ card files.

## Verdicts

| Facet | Overall | Per card where it differs |
|---|---|---|
| 1 Correctness | CLEAN | All 15 cards are CLEAN on local evidence. Kanjipedia sense quotations were checked live only for 黙 and 顕; the others match the packet's local evidence but are not independently live-verified (see Limits). |
| 2 Scoped coverage | NEEDS FIX (minor) | 雄 NEEDS FIX (C1); 随 NEEDS FIX (C2); the other 13 are CLEAN. |
| 3 Consistency and quiz safety | CLEAN | — |
| 4 Comprehensibility | CLEAN | — |

What the facet-1 verdict rests on:

- **Front matter:** grade, strokes, radical, on/kun, quizOnyomi and quizKunyomi match source-metadata.json and kanjidic2-records.xml for all 15 cards. 飼 is grade 5 with the grade-5 tag; the other 14 are grade 8.
- **Joyo claims:** each card's "Joyo lists …" sentence matches joyo-pages.md, including the old forms 隨, 隱, 顯 and 默 and the examples cited.
- **Readings tables:**
  - Every rare-form, archaic, poetical, search-only and source-only qualifier matches JMdict. Examples: 随に まにまに; 隣る (archaic); 雷 いかずち (poetical; いかづち search-only); 顕れる (rare form of 現れる); 黙す (formal/literary); 鬼百合 and 飽くまで (usually kana).
  - The source-only rows are KANJIDIC2 readings: 隠 よ.る, 雷 いかづち, 霧 ボウ, 顕 あきらか, 黙 ボク.
  - The outside-the-table (外) claims match kanjipedia-outside-readings.json. They also match the live pages for 黙 (ボク, だんまり, もだす) and 顕 (あきらか, あらわれる).
- **JMdict:** the senses and numbering quoted as supporting exclusions are correct. Examples: 神's fourth sense, archaic "thunder"; 電 as a rare form of 稲妻; 表す's s_inf "esp. 顕す"; 飾る's fourth sense "to be showy"; しじま listing 黙 and 静寂 as rare kanji forms.
- **KANJIDIC2 meanings quoted in exclusion notes:**
  - 寂 "quietly";
  - 卓 "eminent" and "high";
  - 養 "rear";
  - 掲 "display";
  - 華 "showy" and "ostentatious";
  - 雄 "superiority".
- **Mnemonics:** all 15 are labelled as modern-shape mnemonics and not etymology, and make no historical claim. Every component, position and variant statement matches kanjivg-components.txt. For 黙: 黒 has original=黑 with 里 ⊃ 日 at the left; 犬 sits at the right; 灬 has original=火 at the bottom. Every quoted title is exact against kanji-titles.tsv.
- **Stroke files:** all 15 have strokeCount equal to the stroke-array length and to KANJIDIC2, sequential ids, and the same pinned KanjiVG revision 70a0b7ae (matching kanjivg-components.txt).
- **22 diffs:**
  - Each of the 19 word diffs changes exactly one line. Each wraps only the first bare mention of the new kanji in `[X](../kanji/X.md)`, with no other character changed and no Dictionary: line added or removed.
  - The 3 kanji diffs equal the old and new text declared in kanji-remarks.json. The links resolve: 鬼 is "demon; ogre" and 顕 is "evident; reveal", both exact titles. 眼 has no card, so 鏡's remaining sentence is still true. All three passages read naturally.

## Findings

### C1 — 雄 represents ユウ only by a rare word and omits 英雄 and 雄大

- **Severity:** minor. **Facet:** 2 (scoped coverage).
- **Where:** `snapshot\kanji\雄.md:31` (ユウ row), `:38` (Common words).
- **Claim and impact:**
  - The ユウ row and the only Common words entry use 雄勁 ゆうけい "vigorous; powerful". In JMdict, 1839950 has no priority tags. It is also not one of the Joyo examples for ユウ, which are 雄大, 英雄 and 雌雄 (joyo-pages.md, p. 150).
  - 英雄 えいゆう (ichi1, nf07) and 雄大 ゆうだい (ichi1) are the words an English-speaking learner meets first for ユウ, but neither is named anywhere on the card. The 英 exclusion note does not mention 英雄 either, even though it is the most natural link between the two kanji.
  - Listing a no-priority literary word as the card's sole "common" word misdescribes how 雄 is used.
- **Remedy:**
  - Keep 雄勁 as the linked word that establishes the quiz reading.
  - Name 英雄 and 雄大 unlinked in the ユウ row, as 黙 does with 沈黙, or in Notes.
  - Optionally mention 英雄 in the 英 exclusion note.
- **Evidence:** jmdict-digest.tsv (雄 priority rows); jmdict-families.xml 1839950; joyo-pages.md p. 150 row 雄.
- **Confidence:** high.

### C2 — 随 omits 随分 ずいぶん

- **Severity:** minor. **Facet:** 2 (scoped coverage).
- **Where:** `snapshot\kanji\随.md:31–37` (ズイ row and Common words) and the whole card.
- **Claim and impact:**
  - 随分 (JMdict 1372800, ichi1) is a very common everyday word, usually taught around N4. Most learners will have seen 随 first in it.
  - The card never mentions it. It names 随筆, 随意, 随伴, 随行 and 追随.
  - 随時 and 随所 (news1) are also absent, though that is less important.
  - Without 随分, the learner misses the most useful anchor for ズイ.
- **Remedy:** add 随分 ずいぶん ("very; extremely; considerably") unlinked to the ズイ row or a Note. No word article exists for it, so it cannot be linked.
- **Evidence:** jmdict-digest.tsv (随 rows); word-titles.tsv (no 随分 article).
- **Confidence:** high that it is omitted; medium on how much the omission matters.

No other defect is established. On the leads in the brief:

- **(a) Exclusions:**
  - Each listed pair is backed by a shared title word, a KANJIDIC2 meaning, a Kanjipedia or Digital Daijisen sense, or a JMdict spelling or sense, and the card cites that backing.
  - Pairs that are conservative but sourced: 随/準, 随/仕, 隣/町, 鬼/気, 雷/怒, 雷/神, 項/首, and 鮮/乏/希/珍. Over-exclusion here only narrows the option pool. None is a transitive clique without a direct source.
  - The non-excluded pairs named in the brief are all defensibly distinct as displayed titles: 随/追, 隣/側, 隣/境, 雷/鳴, 霧/雲, 霧/曇, 霧/煙, 項/目, 項/欄, 鮮/鋭, 鮮/清, 黙/沈.
  - Title searches found no missing synonym card. There is no card titled ghost, soul, spirit (other than 気), haze or mute.
- **(b) In-batch pairs:** 隠/顕 are clear opposites, and Kanjipedia itself marks 顕 対 隠. The pairs 隠/黙, 雷/霧, 鮮/顕, 随/隣, 雄/鬼 and the three 飠 kanji are all distinguishable from their titles.
- **(c) Distractors:** every distractor is plausible and defensibly wrong in both directions. The curated readings shown in reading-options.txt never coincide with the asked reading.
- **(e) Reading-exposure accounting:** the 8 latent collisions are 隠 お and なまる; 雄 かつ, ゆ and よう; 飼 かい; 飽 あき; 飾 しか. These match the per-kanji lines. None is drawable in the N1, All or Starter pools. okurigana-scan.txt supports いん.ぺい, こも.る, なま.る, らい.こう, あら.わ, だんま.り, もく.する, もく.とう and まま.に.
- **(g) Meaning statements:** the meaning statements I checked against local evidence are true. 飾's line 23 quotes senses 1, 2 and 4 of 飾る without numbering them; the note on line 50 correctly says "fourth sense". This does not contradict anything (see O2).

## Optional

- **O1. 隣 とな.る row.** It uses only the archaic 隣る. The Joyo example is 隣り合う (JMdict 1598830), which appears only in Notes. Showing 隣り合う in the row would give learners a live word for とな.
- **O2. 飾 Meaning section.** It lists three of 飾る's four JMdict senses back to back, skipping sense 3: "to mark; to adorn (e.g. the front page); to grace". A reader may assume 飾る has three senses and then be puzzled by "fourth sense" in the 華 note. A short "among its senses" or a sense number would remove the friction.
- **O3. 黙 coverage.** 暗黙 (ichi1, news1; a Joyo example) and 黙祷 もくとう (news1) are not named. Kanjipedia marks もだす as well as だんまり as outside the table (外), but the もだ.す row does not say so. The row could note it.
- **O4. 黙 distractor 走 "run".** It is semantically far from "be silent; silence", so it does little work. 叫 and 踊 are fine. A noise- or speech-related kanji would be more instructive.
- **O5. 項 mnemonic wording.** The phrasing "頁, a shape, stands on the right" is slightly awkward, for example compared with "the shape 頁 stands on the right".
- **O6. Card density.** The exclusion notes are long, citation-heavy paragraphs on all 15 cards. That is consistent with corpus style, but heavy on a phone.

## Limits

- I am Claude (Anthropic). Every response I made contained exactly one tool call. I know of no response that issued more than one. I used no sub-agents, background jobs or other sessions.
- **Kanjipedia live senses:** I verified them on the live site only for 黙 and 顕. For the other 13 cards, the quoted Kanjipedia senses were checked only for consistency with the packet evidence (outside-reading JSON and the cards' own cited text), not live. Among them, for example:
  - 雷's descriptive and weapon senses;
  - 鬼's 悪神;
  - 飽's 満たされる;
  - 鮮's three senses.

  I therefore do not claim them independently verified; nothing I saw suggests they are wrong.
- daijisen-heads.txt and kanjivg-svgs.txt were not opened. The headword-derived extras were judged from reading-exposure.txt and the public-source extracts. The mnemonics were judged from kanjivg-components.txt, which is derived from the same pinned SVGs.
- **Word diffs:** I viewed the changed lines and hunk headers, not the unchanged context lines. "Passage still reads correctly" was judged from the full changed sentence in each diff.
- **Reading-exposure:** the "3 more one-holder hits for KANJIDIC2 name-only readings" total was not recounted independently. It depends on the app's per-seed padding simulation in app-code, which I did not open.
- I assumed that the Common words section is meant to list word articles that exist in the repo. On that assumption, C1 and C2 ask for unlinked mentions, not new links.
- The JVM content tests and the Kotlin cross-check were not run at this snapshot. That is a known packet limit and is not reported.
