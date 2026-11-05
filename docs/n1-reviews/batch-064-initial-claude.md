Snapshot: I was given signed frozen snapshot `400ba5ea60299cf4b77f6f9ffbf66cae8f061db3`. I couldn't check this SHA or the working tree's commit/dirty state because I had no shell or Git tool. So I reviewed the files as they are on disk at that path.

Scope:
- **Reviewer:** Claude Opus 5.5, one reviewer, working read-only. I did not read any other reports or author records.
- **Review files, read in full:** `kanji/偵.md` (1–60), `words/探偵.md` (1–55), and `kanji/探.md` (1–52). In `探.md`, only the changed Common words line (40) was reviewed; the rest was read as context.
- **Context files, read in full:** `停.md`, `低.md`, `値.md`, `人.md`, `刑事.md`, `調査.md`, `調べる.md`, `探る.md`, `警官.md`, `警察.md`, `研究.md`, `検査.md`, `検討.md`, `チェック.md` and `strokes/偵.json`.
- **Guidance read:** both instruction files and the assigned ranges of `content-format.md` and `jlpt-levels.md`.
- **Frozen sources:** all 23 lexical JMdict entries (lines 1–369), all 10 comparison entries (1–274), all 7 KANJIDIC2 records (人, 探, 値, 低, 停, 偵, 貞; 1–492) and the pinned SVG (1–78).
- **Checked by search:** the 11 two-distractor cards (title, tags and distractors), word/kanji titles that overlap in meaning, mentions of 探偵 and 偵, and `confusable-words.md`, which has no matching rows.
- **Fresh Kotobank lookups:** 偵, 探偵 and 刑事, fetched today. These are separate from the frozen XML.

Verdicts:
- **`kanji/偵.md` (new):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words/探偵.md` (new):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`kanji/探.md`, changed line 40:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN. The unchanged context was not judged as part of the change.

What the checks found:
- **偵 metadata:** It matches KANJIDIC2 exactly: 11 strokes, classical radical 9 (人), grade 8, sole on reading テイ and no kun readings. `quizOnyomi: [テイ]` is a correct subset, and its reading row has its own linked example, 探偵. `quizKunyomi: []` is consistent with having no kun readings.
- **Side form:** The facts line explains 人 appearing as 亻 without changing the radical metadata.
- **Mnemonic:** It is labelled as a modern-shape aid and explicitly not etymology. Jitsu calls 偵 a phonetic compound (形声) with 貞 as the sound element. The card makes no phonetic or structural claim and uses `structure-unclassified`, which is acceptable.
- **Jitsu's extra kun readings:** Jitsu gives the historical readings うかがう and とう. They were correctly not added to the metadata, and line 38 correctly says no kun reading is supplied.
- **Stroke data:** The SVG has 11 paths (亻 + 貞, split into 卜 and 貝), and the JSON's `strokeCount` of 11 and stroke order match.
- **Reading allocation:** タン + テイ = たんてい is stated correctly in all three files.
- **探偵 identity:** JMdict 1418380 has a person sense (detective, investigator, sleuth) and a second sense (detective work, secret investigation) that is a noun, a する verb and transitive. The article covers both.
  - Nikkokuseisen ① gives the same two meanings. Its sense ② is a historical spy sense. The article neither adopts that sense nor makes every 探偵 a spy.
  - Nipponica says 探偵 usually means a non-police professional. That supports "often a private investigator" and the hedged contrast with 刑事.
- **Examples:** In 探偵に調査を頼みました, に marks the person asked and を the work requested; the roles and translation are correct. In 探偵小説を読むのが好きです, the construction (の turning 読む into a noun + が好き) and the translation are correct. 私立探偵 and 探偵小説 match JMdict 1311440 and 1418390.
- **Kanji contributions:** 探 (search/probe) and 偵 (investigate what is hidden) are two related ideas that reinforce each other. There is no claim of fixed meaning compartments, and no implication that an investigation succeeds.
- **Word JLPT level:** None is given and none was inferred. The vocabulary baseline only covers N5–N2.
- **Links (two pairs, four directions):** 偵→探偵 (lines 23/36/43), 探偵→偵 (line 29), 探→探偵 (line 40) and 探偵→探 (line 28) are all present. All four point to the correct pages.
- **Kanji quiz choices:** 停 "halt; stopping", 低 "low; lower in height" and 値 "value; price" are clearly different from "spy; covert investigation", including their ordinary meanings. None of the 11 legacy two-distractor cards has a title that could be confused with 偵's: 人, 休, 何, 入, 出, 口, 女, 日, 月, 男 and 買.
- **Word quiz exclusions:** The four exclusions (刑事, 調査, 調べる, 探る) are each justified by an actual overlap with "detective" or "investigate". They act in both directions but only as direct pairs, not as a group.
  - 警官, 警察, 研究, 検査, 検討, チェック, 秘密 and こっそり share a topic but not a title-level meaning, so no missing exclusion is established.

Findings:
1. **Minor; scoped coverage (navigation); `words/刑事.md:28`.** This existing card compares 刑事 with "探偵 (たんてい) … such as a private investigator", but 探偵 is plain text. That card now exists, and this is a substantive comparison, so the link rule (link at the substantive introduction or comparison) applies. Without the link, learners lose the reverse path from the police-detective card to the private-investigator card. It is not one of the required reciprocal pairs.
   - **Remedy:** link `[探偵](探偵.md)` at line 28 (requires authorization, since the brief says no other reused teaching changes).
   - **Evidence:** the search shows the unlinked mention; `探偵.md:34` links to 刑事.
   - **Confidence:** high that the link is missing; low learning impact.

Optional:
- `偵.md:54` could note that 低 also reads テイ (KANJIDIC2), as the note does for 停. The current wording is true; this would just strengthen the look-alike guidance.
- `探偵.md` could gloss the 読むのが好き construction in one line, or add an example of the verb 探偵する.
- Unchanged `探.md` context: its Readings table still says only kun examples are selected, and 探る (line 39) is unlinked. A タン row linked to 探偵 is now possible. Both are outside this batch's change scope.

Limits:
- **Snapshot:** not checked independently, because I had no Git access.
- **Kotobank:**
  - 偵: Daijisen returned only an attribution line; the Jitsu entry came through in full.
  - 探偵: Daijisen and Jitsu were attribution-only; Nikkokuseisen and Nipponica came through.
  - 刑事: Daijisen, Mypedia and Britannica were attribution-only; Nikkokuseisen, Nipponica, Sekai Daihyakka and Jitsu came through.
  - I made no frequency or register claims.
- **Quiz audit:** Only the bounded pool was checked. Kanji cards outside it whose quizzes may fill missing choices from other cards (for example 査 "investigate; inspect", 調, 究) could show 偵 as a fallback choice. That pool is not certified.
- **Native/phone evidence:** none was supplied. These are text-only judgments; they don't certify glyph rendering or stroke drawing for 偵/貞, 停/低/値, 人/亻 or 手/扌. Phone and general-release acceptance remain outstanding, and Android `f9b59a2` or later is required.
- **Tools:** I used one tool call per response throughout.
