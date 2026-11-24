**Needs fixes before quiz sign-off.** Four direct meaning exclusions are missing from the supplied data, and the 満悦 card omits JMdict’s usage note that ご満悦 is the usual form. All 16 required reciprocal navigation pairs are present.

**Snapshot:** `dc46cc08608fa8714a68a36af77fb9ebd1b8fa37`, based on `894d30525e87a394b0b5a6de9767d2d1084b6ed3`. No uncommitted changes were identified in the packet; the worktree was not inspected.

**Scope:** One blind, read-only reviewer, GPT-6.2 Sol (`gpt-6.2-sol`). Read `kanji-1..4.txt`, `words-1..3.txt`, `changed.txt`, and `comparison-words.txt` in full. Checked `primary.xml`, `sources.json`, all eight `families-*.jsonl` files, `quiz.txt`, and `labels.txt` against `rubric.txt`. Reviewed meaning and reading quiz safety, cross-card consistency, navigation, evidence, and scoped teaching coverage—not idiomaticity or publication acceptance.

**Verdicts** are correctness / scoped coverage / comprehensibility, in that order. **C** = CLEAN, **N** = NEEDS FIX, **U** = UNVERIFIED. CLEAN applies only to the assigned facets.

| New kanji | Verdict | Mapped word | Verdict |
|---|---|---|---|
| 忍 | C/C/C | 忍ぶ（しのぶ） | N/N/C |
| 忠 | C/C/C | 忠実（ちゅうじつ） | N/N/C |
| 恒 | N/C/C | 恒例（こうれい） | C/N/C |
| 恭 | C/U/C | 恭しい（うやうやしい） | C/U/C |
| 悦 | C/N/C | 満悦（まんえつ） | C/N/C |
| 悼 | N/C/C | 追悼（ついとう） | N/N/C |
| 惨 | C/C/C | みじめ（みじめ）, reused | C/C/C |
| 惰 | C/C/C | 怠惰（たいだ） | C/C/C |
| 愁 | N/N/C | 郷愁（きょうしゅう） | C/N/C |
| 愚 | C/C/C | 愚か（おろか） | C/N/C |

The changed hunks of **実, 例, 満, 追, 郷, 怠** are each C/C/C. The eight older comparison words—**我慢, 隠れる, 習慣, 丁寧, 満足, 弔問, 懐かしい, 馬鹿**—each support their existing direct quiz exclusion; no separate whole-card verdict is implied.

**Findings**

| Severity / facet | Location and evidence | Exact remedy |
|---|---|---|
| Moderate · meaning quiz · high confidence | `words/忍ぶ.md:8,15`: 潜る displays “dive; get underneath; **hide**” in `labels.txt`, overlapping the taught hiding sense of 忍ぶ (JMdict `1467450`, sense 1). Its existing exclusions for 隠れる and 隠す do not protect this pair. | Add `潜る` to 忍ぶ’s `quiz_exclusions` and synchronize the audit. |
| Moderate · meaning quiz · high confidence | `words/忠実.md:8,15`: ねっしん displays “enthusiastic; **devoted**.” “Devoted” is an explicit gloss of 忠実 (`1012210`) and is taught in its duty sense. | Add `ねっしん` to 忠実’s direct exclusions and synchronize the audit. |
| Moderate · meaning quiz · high confidence | `kanji/悼.md:14` and `kanji/愁.md:14`: both cards teach grief; 悼む (`1446980`) and the lament sense of 愁える (`1588580`) share “grieve,” “mourn,” and “lament.” The common exclusions 哀 and 悲 do not protect 悼–愁. | Declare `悼`–`愁` as a direct pair. Keep the teaching distinction between death-focused mourning and the broader sorrow or worry of 愁. |
| Moderate · meaning quiz · medium confidence | `words/追悼.md:8,26`: 嘆く displays “lament; **grieve**; sigh.” Its ordinary use for grieving a death makes it a plausible competing label for 追悼. 嘆く’s exclusions for 悲しむ and 悔やむ do not protect this pair. | Add `嘆く` to 追悼’s direct exclusions and synchronize the audit. |
| Moderate · scoped coverage · high confidence | `words/満悦.md:15–22,30`: JMdict `1526740` explicitly says “usu. as ご満悦.” The card leads with bare 満悦する and describes ご only as a polite prefix, so learners miss which form to expect. | Say that JMdict gives ご満悦 as the usual form and lead with that example. Keep 満悦する as valid; the recorded Daijisen check supports it. |
| Minor · reading and spelling · high confidence | `kanji/恒.md:33,41` presents 常に as the unqualified spelling, while `sources.json` records Kanjipedia’s outside-standard-use `つね.に` for 恒. `kanji/愁.md:33,41` calls 愁い a second spelling but leaves out JMdict `1540740`’s sense-local preferences. | For 恒, teach 常に as the ordinary spelling and identify 恒＋に as outside standard use, not a quiz reading. For 愁, say JMdict particularly associates 愁い with grief and 憂い with worry; these are preferences, not exclusive rules. |
| Minor · evidence record · high confidence | `quiz.txt:93–102` calls 満悦 an “untagged” exception even though `1526740` has `news2`, `spec2`, and `nf37` on both spelling and reading. | Call it a **no qualifying preferred-tier spelling** exception, preserve the raw tags, and distinguish it from genuinely untagged 恭しい. This corrects the record, not the choice of word. |
| Minor · evidence navigation · high confidence | Several in-text dictionary claims are supported by the packet but not traceable from their article citations. | In `words/忍ぶ.md:15,30–32`, cite JMdict `2126560` and `1321590`; in `words/郷愁.md:30–32`, cite `1200550`; in `words/愚か.md:30–32`, cite `2832535`. Link the Daijisen **character** headings explicitly where invoked at `words/忠実.md:22` (実 sense 4), `words/恒例.md:22` (例 sense 3), and `words/追悼.md:22` (追 sense 4). `sources.json` records those exact headings as checked by the author. |

**Counts and navigation:** Ten selected source rows map to ten distinct word articles: nine new and one N2 reuse. The batch affects 26 articles total: 19 new and seven edited. Verified both relative-link directions and the actual word reading for all 16 required pairs: ten involving the new kanji, plus 実–忠実, 例–恒例, 満–満悦, 追–追悼, 怠–怠惰, and 郷–郷愁. 惨 links to the existing `みじめ.md`; its kana identity, N2 level, `kanji: []`, and five exclusions are preserved. All 25 new-kanji metadata readings have a table row, including qualified source-only rows. The ten offered keys match the projection: six on and four kun, with no duplicate within those ten. The 30 fixed meaning distractor slots showed no competing label. The packet lists 54 new-kanji and 46 new-word direct exclusions before the fixes above.

**Optional:** Give 忍ぶ one short usage note distinguishing the fixed 人目を忍ぶ from the transitive “hide something” in 隠す or 忍ばせる. The existing examples need not be replaced.

**Limits:** The 113 supplied JMdict families support the checks above, but do not establish the author’s exhaustive priority scans or issue #60 eligibility for 恭しい and 満悦. `sources.json` records the author’s Daijisen, Kanjipedia, and standard-use checks; no external page, native-speaker, or device verification was performed. The quiz simulation and lint are author-reported, including eight inherited reading-row errors on 例, 実, and 満 and 17 substring-only citation matches. The packet does not establish whole-deck or manifest integration, or word-reading option safety: before sign-off, verify that bare 忠実 does not present the valid alternate reading まめ as wrong without a sense or context cue.
