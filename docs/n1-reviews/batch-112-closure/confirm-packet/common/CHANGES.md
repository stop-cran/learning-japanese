# Batch 112 revision: what changed from d6ad96eb to 737cb020

Revised snapshot: `737cb0201bb3ca76b327504d95b17e64f1a79869`, a child of the reviewed snapshot
`d6ad96ebf7d0352d54184ed44a382f70e4497f7b`. Nothing is published.

- Eight of the 15 kanji cards changed: 妙, 就, 展, 微, 態, 盤, 診 and 障. The other seven (健, 射, 看, 至, 酸, 離, 響) are
  unchanged, and so are all 15 stroke files, all titles and the three existing cards whose remarks the batch edits (基, 素
  and 鏡). No word article changed in this revision.
- Front matter changed only in `quiz_exclusions` (line 14) of seven cards: 妙, 就, 展, 微, 盤, 診 and 障. Each list only
  gained entries; none was removed. 態's front matter is unchanged. `distractors`, titles, tags and metadata readings are
  unchanged on all 15 cards. No reading row, reading selection or linked example changed.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Links: every link on a changed line resolves to an existing card (22 links, 0 unresolved; see `checks\link-targets.tsv`).
  That table compares only a gloss in quotation marks placed right after a link. The new text gives most counterpart
  titles unquoted after the link, writing "; " as "/" (for example `[技](技.md), skill/technique`); the author's script
  checked all 13 such glosses against the linked card's real `title:` (12 written with "/" and 完's `complete`), and all 13
  match. Two titles are quoted later in the sentence: `"minute, part"` (`微.md:69`) is the full title of 分, and
  `"barrier."` (`障.md:62`) is part of the title of 関, `involve; barrier`.
- New evidence in this packet is everything under `evidence\`: the complete JMdict entries cited by the new text
  (1375720 成就, 1409160 体/態 てい, 1410750 様/態 ざま, 1528490 妙, 1615650 軽微 and 2138450 形/態 なり; only 1615650 is not
  already in the original packet's `evidence\jmdict-families.xml`), the Joyo table page extracts of the eight changed cards
  in `evidence\joyo\` (pages 74 就, 81 障, 86 診, 103 態, 115 展, 129 盤, 131 微 and 146 妙; context only, since no reading
  changed) and the app's `QuizBuilder.kt`. `evidence\README.md` describes each file. All other evidence stays in the
  original packet.

| Card | Changed lines | Change |
| --- | --- | --- |
| 妙 | 14, 67-69 | Line 14: `quiz_exclusions` gains 技 and 腕 and now reads `quiz_exclusions: [奇, 変, 美, 優, 微, 若, 珍, 技, 腕]` (it ended at 珍). Lines 67-69 are a new Notes bullet: `- JMdict also gives the word 妙 みょう a skill or cleverness sense, which overlaps [技](技.md), skill/technique, and [腕](腕.md), arm/skill. These direct comparisons are excluded from meaning choices too.` The skill sense is sense 3 of JMdict 1528490, "cleverness; adroitness; knack; skill", already cited in the Metadata line (line 76). Lines 23-25, which teach the skillful sense, are unchanged. |
| 就 | 14, 74-82 | Line 14: `quiz_exclusions` gains 企, 承, 担, 職, 位, 了, 完 and 済 and now reads `quiz_exclusions: [着, 付, 任, 定, 成, 始, 去, 発, 学, 企, 承, 担, 職, 位, 了, 完, 済]` (it ended at 学). Lines 74-78 are a new bullet: `- "Undertake" also appears in the titles of [企](企.md), plan/undertake, and [承](承.md), accept/undertake. [担](担.md), shoulder/take on, overlaps taking on a responsibility. [職](職.md), employment/post, and [位](位.md), rank/position, overlap the position sense. These comparisons are also excluded; the complete words still differ in use.` Lines 79-82 are a new bullet: `- The completion side shown by 成就 also overlaps [了](了.md), completion/settling, [完](完.md), complete, and [済](済.md), settle/finish. They are excluded from meaning choices as well; this does not make 就 a substitute for those characters in their own words.` The completion sense taught at lines 29-31 (成就 じょうじゅ, JMdict 1375720) and the ジュ row (line 43) are unchanged. |
| 展 | 14, 66-67 | Line 14: `quiz_exclusions` gains 敷 and now reads `quiz_exclusions: [開, 広, 伸, 張, 延, 示, 観, 見, 転, 敷]` (it ended at 転). Lines 66-67 are a new bullet: `- Spreading something out flat also overlaps [敷](敷.md), spread/lay out. That direct meaning comparison is excluded too.` |
| 微 | 14, 65-71, 80 | Line 14: `quiz_exclusions` gains 分 and 軽 and now reads `quiz_exclusions: [細, 小, 少, 薄, 弱, 分, 軽]` (it ended at 弱). Lines 65-67 are a new bullet: `- A slight degree also overlaps [軽](軽.md), lightweight/slight; both characters appear in 軽微 けいび, slight or insignificant. That direct comparison is excluded too, without claiming that 微 means light in weight.` 軽微 けいび is JMdict 1615650, glossed "slight; little; insignificant". Lines 68-71 are a new bullet: `- Here English "minute" means tiny, not the unit of time associated with [分](分.md). That card's title is "minute, part"; the shared English spelling is excluded from meaning choices without treating the Japanese meanings as interchangeable.` Line 80: the JMdict id list of the Metadata line now ends `1260660, 1590290 and 1615650.` (it ended `1260660 and 1590290.`). The title `minute; faint` is unchanged. |
| 態 | 62-63 | The Notes bullet now reads `- JMdict also lists 態 as an additional spelling in the entries headed by 体 (てい), 形 (なり) and 様 (ざま).` (it read `- Dictionaries also have separate 態 entries read てい, なり and ざま.`). In JMdict 1409160, 2138450 and 1410750 the first kanji form is 体, 形 or 様 and 態 is the second; the 態 form carries no information tag. The three ids were already in the Metadata line (line 71). The next line (64), `They are not alternate pronunciations to insert into 態度 or 状態;`, is unchanged. |
| 盤 | 14, 63-65 | Line 14: `quiz_exclusions` gains 乗 and now reads `quiz_exclusions: [板, 皿, 台, 基, 岩, 乗]` (it ended at 岩). Lines 63-65 are a new bullet: `- English "board" here is a flat object, not boarding a vehicle as in [乗](乗.md), ride/board. The shared English spelling is excluded from meaning choices; it is not a shared Japanese meaning.` |
| 診 | 14, 58-59 | Line 14: `quiz_exclusions` gains 査 and now reads `quiz_exclusions: [察, 調, 試, 見, 観, 判, 査]` (it ended at 判). Lines 58-59: the overlap bullet now begins `- [察](察.md), [調](調.md), [試](試.md) and [査](査.md) have examination or investigation meanings;` (it began `- [察](察.md), [調](調.md) and [試](試.md) have examination or investigation meanings;`). The rest of the bullet, from `[見](見.md) and [観](観.md) overlap looking` (line 59) to line 61, and the medical-specific text at lines 23-27 and 43-44 are unchanged. |
| 障 | 14, 61-63 | Line 14: `quiz_exclusions` gains 関 and now reads `quiz_exclusions: [害, 防, 関]` (it read `[害, 防]`). Lines 61-63: the overlap bullet gains `The barrier sense also overlaps [関](関.md), whose title includes "barrier."` before its unchanged closing sentence, `These direct meaning comparisons are excluded from choices, not treated as identical in every compound.` The barrier and partition text at lines 28-30 is unchanged. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on 18 kanji cards (the 15 batch cards and 基, 素 and 鏡, the three existing cards the batch
  also edits) and 59 word articles: 0 errors, 8 warnings. All 8 are on word articles and are of two kinds: 5 say the
  Dictionary line cites no JMdict entry id (看板 算盤 診る 響き 響く) and 3 say there is no Dictionary line (看護婦 眼鏡 鏡).
  The output is the same as the original packet's `checks\lint.txt`, and no word article changed.
- `unittest.txt`: 431 tests, OK. `validate.txt`: 0 errors. `budget.txt`: content archive budgets met. `vocabulary.txt`:
  vocabulary coverage check passes (2122 of 2431 reviewed prompts, stage pilot). `manifest.txt`: `manifest.json`
  regenerated (8601 files) and committed.
- The Android app's JVM tests were not run for this revision, so there is no `jvm.txt`. JVM and emulator work is held, as
  the original packet's `REVIEW.md` (line 71) says for the reviewed snapshot.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether
  a gloss quoted right after the link equals that title.
- `quiz-safety.txt` and `reading-exposure.txt`: see the next section.

## Quiz mechanics the changes rely on

- The repository validator's rules (all pass; `validate.txt`: 0 errors): `quiz_exclusions` has no duplicates, no self,
  every entry has a card, and no entry may also be one of the same card's `distractors`.
- Meaning quiz: the app's `QuizBuilder` is in `evidence\QuizBuilder.kt` (Android checkout at commit `10d98d0`, which
  contains `2edbf36` "Honor explicit kanji meaning pair exclusions"). `excluded(a, b)` (line 26) is true if **either** card
  lists the other, so a pair needs to be listed on one side only (the repository lists each pair once). `tryAdd` (lines
  28-32) skips any candidate excluded against the target or against an option already chosen (line 30). The curated
  `distractors` that are present in the pool passed in as `all` are tried first, in order (line 34); then the other cards
  of that pool, shuffled and ordered by the number of shared tags (lines 35-36). The field's documented contract is in the
  original packet's `repo\docs\content-format.md`, lines 102-107 (curated and fallback choices, All, level and custom pools;
  symmetric, not transitive; an excluded card is never restored; meaning choices only) and lines 109-112 (older APKs do not
  enforce the field).
- `checks\quiz-safety.txt` prints the four meaning options shown for each of the 15 cards in the full pool (the first
  option is the correct title). The changed cards are at lines 3 (妙), 8 (就), 11 (展), 13 (微), 15 (態), 17 (盤), 24 (診)
  and 29 (障). Every one of the 15 cards still shows its three curated distractors. The "reading ... wrong options from
  distractors N/3" lines under each card count curated slots for the reading prompts, not the options themselves. Lines
  38-49 list 11 existing cards outside this batch (人 休 何 入 出 口 女 日 月 男 買) whose options use the tag-similar
  fallback; they are not part of this review and none of them is in a new pair. The output is the same as the original
  packet's `checks\quiz-safety.txt`: no title, distractor or shown option changed.
- So in the full pool the new exclusions change no option shown for any card: no new pair joins a card to one of its own
  curated distractors, and no card lists both members of a new pair as distractors (see the scan below). They act on
  fallback candidates, which a card draws when fewer than three of its curated distractors are usable, for example in a
  pool that lacks some of them; and, being symmetric, they act on the counterparts' questions as well.
- Reading quiz: `quiz_exclusions` affect only the meaning quiz (`content-format.md` line 107). No reading, reading
  selection, distractor or title changed in this revision, so no input of the reading prompts changed.
  `checks\reading-exposure.txt` (the author's audit of the N1 and All stack pools and the Starter practice session) is the
  same as the original packet's copy; line 236 reads 0 production hits, 0 padded-session hits and 11 latent collisions.
  No `reading-options.txt` is supplied, as for the original packet.
- Exclusion changes in this revision: 16 new pairs, each declared once, on the batch card's side: 妙/技, 妙/腕, 就/企,
  就/承, 就/担, 就/職, 就/位, 就/了, 就/完, 就/済, 展/敷, 微/分, 微/軽, 盤/乗, 診/査 and 障/関. The 16 counterpart cards are
  unchanged; the original packet's `repo\kanji\` holds all 1,191 cards of the reviewed snapshot, and only the eight cards
  above differ from it. Author's script over all 1,191 cards at the revised snapshot: no counterpart lists its batch card
  in `quiz_exclusions` or `distractors`; no batch card lists a counterpart in `distractors`; no card lists both members of
  a new pair in `distractors`; every counterpart has three `distractors`. No exclusion was added between two counterparts.
