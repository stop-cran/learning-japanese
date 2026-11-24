# Confirmation report: correctness facet

**Reviewer:** Claude Sonnet 5.5 (`claude-sonnet-5.5`)
**Snapshot:** 093c66da4c311367affc0a3567b2b9dca06b154d, confirming my findings from 6fb17b33…. I take the snapshot ID from the task text and file names. There is no git here, and `snapshot.txt` still describes 6fb17b33.

## Scope and what I read
- **Read in full this turn:** `followup-diff-1..5`, `followup-revision-1..5`, `followup-facts.txt`, `correction-evidence.txt`, `confirmation-task.txt`, `correction-families.xml`, and `labels.txt`. `labels.txt` is the earlier snapshot's partial label inventory.
- **Source facts** (JMdict, `sources.json` and the families files) come from my earlier full reads of `primary.xml`, `sources.json` and `families-1..7`. I did not re-read them here, apart from `correction-families.xml`.
- **Changed cards covered:**
  - Kanji: 宮 宰 寡 尚 尼 尽.
  - Words: 主宰 大尉 寛大 寡婦 尚 尺度 尼 尽くす.
- **Not re-read:** unchanged cards (宵, 尉, 尺, 神宮 and others), which I did not re-review.
- **Method:** there are no line numbers, so I cite card and section.

## Original findings
| ID | Status | Evidence |
|---|---|---|
| F1 (主宰, vacuous "Reversing who leads whom…" line) | **Resolved** | The sentence is gone from `revision-3`. |
| F2 (主宰, elliptical example 2) | **Resolved** | It is now 雑誌の取材でその劇団の主宰に話を聞いた, and the reading ざっしのしゅざいで… is correct. |
| F3 (尼, bare 尼が…) | **Resolved** | It is now 寺では、尼さんが庭を案内してくれた, and あまさん is correct. |

My optional points are also addressed:
- 宮 title is now "palace; Shinto shrine". This matches JMdict (宮 "shrine"), which I read earlier.
- 宰 no longer says "not a job title".
- 寡 notes now cover やもめ.
- 尼 kanji says "Catholic nun", matching JMdict sense 2.
- 寛大 now explains に and 寛大な.
- 大尉 notes the Navy だいい reading (JMdict 1413030).
- 尺度 now says which sense the examples illustrate.
- 尽くす has an intransitive example with no を.
- All four quiz-safety hypotheses now appear as exclusions: 尚↔じっと, 尚↔且/敬, 主宰↔監督, 尽くす↔注ぐ.

## Regression check of changed passages
**Source facts:**
- 尽 rows match JMdict 1585205 (力ずく/力づく/力尽く with per-spelling readings), 2065420 (納得ずく/納得尽く are なっとくずく; なっとくづく goes with 納得づく only) and 2436480 (suffix "after a noun", usually kana).
- The サン row now matches `quizOnyomi: []`.
- じっと sense 1 is "motionlessly; (be) still", which supports the 尚 contrast.
- 注ぐ sense 4 is "concentrate one's energy… devote to", which supports 力を注ぐ.
- 監督 sense 2 is "director", which supports the 主宰 synonym line.

**Result:** I found no regressions in readings, restricted senses, grammar or scope.

## Verdicts (correctness)
All changed cards are **CLEAN**. That means no actionable defect was established. It does not mean native or corpus verification.

## Remaining actionable issues
**None.**

## Optional ideas (author's discretion)
1. **主宰 example 2:** 取材 (しゅざい) is a near-homophone of しゅさい in a card about homophones. 記事 or インタビュー would avoid the distraction.
2. **主宰 監督 line:** "can also name someone who directs" does not contrast the two. Suggested remedy: "監督 directs a film or team; 主宰 runs the company or group."
3. **寡婦 wording:** JMdict puts "widow; divorced woman not remarried; unmarried woman" in one sense, so "groups both uses with the broader gloss" is loose. The caution against calling a never-married woman 寡婦 is the author's interpretation (`correction-evidence.txt`). I cannot check it in the packet. The "administrative document" sentence in Distinctive meaning now has no example, and the divorce sense has no example.
4. **尽 rows:** the -づ.く row also explains the ず spelling 力ずく. "Write … not 納得尽く" could read "JMdict pairs なっとくづく only with 納得づく".
5. **Unchanged:** 宵 has no register note, and 尽くす shows no に pattern. Kanjipedia-only readings for 宮, 宰, 尚, 尺 and 尽 are still undocumented.

## Limits
- I did not do a fresh whole-deck, device, native, corpus or external-page review.
- Exclusion symmetry ("direct and symmetric") is the author's claim. I did not see the counterpart cards (注ぐ, じっと, 監督, 敬, 且) in the follow-up files, so I could not check their exclusion lists.
- Link targets are unconfirmed. `labels.txt` shows 且, 注ぐ, じっと and 監督 but not kanji 敬, and that file is partial and earlier.
- `labels.txt` still shows the old 宮 label, "palace; imperial shrine". I treated `followup-facts.txt` as the post-revision projection.
- Composed examples are unverified for naturalness.
