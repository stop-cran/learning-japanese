# Batch 150: confirmation review (reviewer 1)

```text
Snapshot: 7e3c101b84848bd7a342cb1f44a421cd0f6f73e6 (revision of 2dd9d46b). Reviewer: Claude (Anthropic), Claude-family model running as a GitHub Copilot agent; the exact model version is not shown to me.

Scope:
- Read in full: INSTRUCTIONS.md, CHANGES.md, RESPONSE.md, diffs\fix.patch, evidence\README.md, evidence\QuizBuilder.kt, evidence\meta-scan.txt, checks\quiz-safety.txt and checks\link-targets.tsv.
- Read all 10 changed cards in full at the revised snapshot: 蒔 薦 虚 融 街 衝 裁 裸 視 覧.
- Read in part:
  - evidence\KanjiReadings.kt, lines 45–135 (ReadingCard, excludedKeys, question).
  - checks\reading-exposure.txt: header, plus the 葬, 蒔 and 蓄 sections in full.
  - checks\reading-options.txt: header, the 葬–虚 sections in full, and every per-card prompt, note, check, simulation and total line.
  - evidence\jmdict-cited-entries.xml: entries 1454080 (みち), 1456890 (突く/衝く) and 1371170 (推薦).
  - Original packet, read-only: evidence\public-source\weblio-虚.txt (the 邪心 line); evidence\kanjivg-components.txt (融 and 覧); evidence\kanjivg-svgs.txt (覧 strokes 8–11).
  - My initial report, reports-150\initial-claude.md.
- grep checks: "card text" in checks\ (0 hits; all 16 extra-reading labels now read "--extra list"); 苗|布|捜|径|攻 in the revised cards.
- Live web: Kanjipedia 薦 (0004112600) and 虚 (0001436100), meaning lists read.
- Not opened: unchanged cards 葬 蓄 衆 裂 覆, Words.kt, diffs\changed-lines.txt, and checks other than those listed above.

Dispositions:
- C1 - RESOLVED - Both audit outputs now label every passed extra reading "(--extra list)", and grep finds 0 "card text" hits in checks\. The second line of each output names the sources of the extras: Kanjipedia 外, Daijisen kun and heads, and okurigana-scan.txt. Counts and collisions are unchanged (4 KANJIDIC2 name-only latent collisions, 0 problems).
- O1 - RESOLVED - 虚.md:23 now attributes each wording to its source. Live Kanjipedia ③ reads 邪心をもたない。すなお。「謙虚」, and the packet's Weblio extract 〈キョ〉6 reads 邪心を持たない。「虚心／謙虚」. Both match.
- O2 - RESOLVED - 薦.md:47 no longer quotes a gloss. JMdict 1371170 has <xref>推奨</xref> on its only sense, so "see-also cross-reference" is exact. 薦.md:49 quotes こも。敷物。しとね。, which matches live Kanjipedia ② character for character. The English "(straw mat; floor covering; a mat to sit or lie on)" is a fair gloss.
- O3 - RESOLVED - 径 was added to 街.md:14, and the bullet at 街.md:48 covers it. JMdict 1454080 has the spellings 道, 途, 路 and 径, and its sense 1 is "road; path; street; lane; passage" (exact). The link target's title is "diameter; path", quoted exactly. The count reads eight, and all eight exclusions are covered by bullets. 径 is not among the distractors (橋 庭 池).
- O4 - RESOLVED - 攻 was added to 衝.md:14 and to the bullet at 衝.md:48. JMdict 1456890 includes the spelling 衝く, has "to hit" in sense 2 and "to attack" in sense 4 (both exact), and has no spelling restriction on those senses. The title "attack; go on the offensive" is quoted exactly. The count reads eleven and is complete. 攻 is not among the distractors (走 止 回).
- O5 - DECLINE ACCEPTED - 転's title "turn; roll" names neither covering nor overturning. 覆's quiz is filled entirely by its curated 開 拾 投 (quiz-safety.txt), and exclusion is symmetric in QuizBuilder. So the only exposure is 覆 appearing as a fallback option on 転's own quiz, where "cover; overturn" is distinguishable from "turn; roll".
- O6 - DECLINE ACCEPTED - A grave is a place, not burial or a funeral. My original point was optional.
- O7 - DECLINE ACCEPTED - Common words is scoped coverage, and 衝 is not misdescribed. Adding words would add new sourced claims at the confirmation stage.
- O8 - DECLINE ACCEPTED - Same reason for 虚: the card is accurate as scoped.
- O9 - DECLINE ACCEPTED - Same reason for 覧 and 裂.
- O10 - RESOLVED - Both shape-only descriptions agree with KanjiVG:
  - 融.md:25: 鬲 is 一 (stroke 1) over 口 (2–4) over a taller 冂 frame (5–6), with 4 strokes inside (7–10).
  - 覧.md:25: in the SVG, stroke 8 is a slant (㇒) and stroke 9 a horizontal (㇐) starting at the slant and running right. Stroke 10 is a further horizontal below, outside any group.
  - Giving no meaning is the right choice: a meaning would be an etymological claim that the mnemonic disclaims.
- O11 - RESOLVED - 裸.md:25 is now a single coherent image: a fruit whose "clothing", its peel, is stripped until it stands bare.
- O12 - DECLINE ACCEPTED - okurigana-scan.txt is mechanical evidence. Its parses are now labelled "--extra list", and the header of each audit names their source, which was the substance of my point.

Verdicts:
- Correctness: CLEAN. Every changed claim checked true against the JMdict entries, live Kanjipedia, the Weblio extract and KanjiVG.
- Scoped coverage: CLEAN. No change alters a card's scoped coverage.
- Consistency and quiz safety: CLEAN.
  - Links and quoted titles: all 19 links on changed lines resolve, and I checked every curly-quoted title by hand against link-targets.tsv.
  - Exclusion lists: every "These N cards" count equals its list, and every exclusion has a bullet. No exclusion is also a distractor.
  - The added pairs, 街/径 and 衝/攻, are real direct pairs.
  - The removed pairs, 蒔/苗, 裁/布 and 視/捜 plus 覧/捜, give no two-answer risk in either direction. "seedling; young plant" vs "sow seeds", "cloth; distribute" vs "judge; cut out cloth", and "search; look for" vs "look at; regard as" / "look over; peruse" are each distinguishable.
  - The batch cards' own meaning quizzes are filled 3/3 by their curated distractors, so 苗, 布 and 捜 cannot appear on them.
- Comprehensibility: CLEAN. The new shape descriptions and the 裸 image are concrete and readable. The 覧 mnemonic sentence is long (see Optional).

Confirmation: CONFIRMED

Findings: none

Optional:
1. 覧.md:25 now packs 臣, 𠂉, its stroke description, the extra horizontal and 見 into one sentence. On a phone, a reader may attach "one more horizontal stroke below it" to 臣 rather than to 𠂉. Splitting it would help, for example: "… beside the small shape 𠂉 (…). One more horizontal stroke sits below 𠂉, and 見 … sits underneath."
2. 視.md:49 and 覧.md:50 justify 仰 by reasoning alone ("to look up at something is itself to look at it"), without a source. That is acceptable for a title-to-title overlap; this note is editorial only.

Limits:
- Tool discipline: one tool call per response throughout; no parallel calls, sub-agents, background jobs, recursive listings or corpus scans.
- Meaning-quiz options, all 15 cards:
  - quiz-safety.txt shows each card's 3 curated distractors filling every slot, and I agree that each set is wrong in both directions. QuizBuilder.kt confirms that curated distractors are tried first and that exclusion is symmetric (a in b's list or b in a's).
  - The exclusion changes therefore affect only:
    - the fallback quizzes of other cards: 苗, 布, 捜, 径 and 攻, and the 11 listed existing cards that fall back;
    - which wrong options may appear together.
  - The audit does not show those other cards' quizzes. My judgement about them rests on the QuizBuilder code and the titles, not on runs.
  - The 11 fallback cards (人 休 何 入 出 口 女 日 月 男 買) have titles that none of the 15 batch titles could also answer.
- Reading-quiz options:
  - No reading list, quizOnyomi, quizKunyomi or distractors list changed, and KanjiReadings.kt never reads quiz_exclusions. So the reading prompts are unaffected by this revision. checks\reading-options.txt reports 0 problems, and the curated readings I spot-checked collide with no reading of any target.
  - What the audits cannot show:
    - readings attested in a source but absent both from the metadata and from the --extra list;
    - whether the app at runtime builds ReadingCard.on/kun exactly from the metadata lists (the Android JVM content tests were not run, as at the freeze);
    - learner confusion between near-homophones that the app's key and mutation rules treat as distinct.
- Not verified live:
  - Digital Daijisen (I used the packet's Weblio extract);
  - today's online JMdict (I used the pinned extracts);
  - the English sense of しとね ("a mat to sit or lie on"), which comes from my own knowledge of standard dictionaries.
- Not reopened:
  - the unchanged cards 葬 蓄 衆 裂 覆, beyond their quiz-safety and reading-options lines;
  - Words.kt;
  - the titles TSV. I took the titles of 苗, 布 and 捜 from the old card text in fix.patch.
```
