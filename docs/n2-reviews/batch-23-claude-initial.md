## Snapshot
The frozen commit is **ba36c794cd3cff027e3b1bf8c6a7c6f2de800dd8**, against baseline 5297e4f594f6587cb1d48abfb4e271cea3e83e10. I treated the review as covering committed files only. Because I could not run Git, I could not confirm that the files on disk are identical to that commit. I relied on the snapshot JSON's statement that the worktree is clean.

## Scope
- **Model:** claude-opus-5.5, Claude family.
- **Read completely:** the 15 kanji cards (述 逆 造 郊 郵 量 針 鈍 鉄 鉱 銅 鋭 録 門 防), `words\鈍い.md` and `words\鉱石.md`.
- **Read as instructed:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-109`.
- **Read in `batch-23.json`:** the metadata, primaryWords, most wordEvidence records, newWordArticles and quizSafeguards.
- **Related edits:** I checked every link line in the 19 links-only articles in context, and read 鋭い, 門 and 針 in full. All link targets exist.
- **Quiz checks:**
  - All 45 distractor assignments are existing cards with semantically wrong meanings.
  - I swept word titles for overlaps with 鈍い and 鉱石, and grepped `confusable-words.md` (only CW036 is relevant).
  - I checked the 13 older cards that have only two distractors for synonym risk via tag-based fallback.
- **Omissions:**
  - The 15 stroke files were not reviewed.
  - Unchanged text in the 19 articles was not reviewed.
  - I only partly read the comparison records at `batch-23.json` lines 4910-6868. I confirmed their entry IDs and the しくしく senses.
  - I did not inspect `docs\n2-source-snapshot.json`.
  - I did not read any forbidden ledgers or other reviewers' output.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 述, 逆, 造, 郊, 郵, 量, 針, 鈍, 鉄, 鉱, 銅, 鋭, 録, 防 (14 cards) | CLEAN | CLEAN | CLEAN |
| 門 | **NEEDS FIX** | CLEAN | CLEAN |
| 鈍い (word) | CLEAN | CLEAN | CLEAN |
| 鉱石 (word) | CLEAN | CLEAN | CLEAN |

Strokes, grade, radical, radical number, on'yomi and kun'yomi match the KANJIDIC2 data on all 15 cards.

## Findings
**B23-R-01 — Minor — Correctness — `kanji\門.md:32` and `:42`**
- **Claim:** The と row gives "門 と - shutter; window shutter" as a typical word. Line 42 calls shutter "the unmarked applicable sense", which teaches learners to write 門 for a door or shutter.
- **Evidence:**
  - JMdict 1266970 (`batch-23.json:1249-1325`, and jisho.org) leaves sense 2 "shutter" unrestricted, so the author followed the pinned source.
  - デジタル大辞泉 (kotobank), と【戸／▽門】: sense 1, the sliding or hinged fitting, is explicitly marked （戸）. The 門 spelling only covers sense 2 (entrance, archaic citation) and sense 3 (water passage or strait).
  - The ▽ mark shows と is a non-Jōyō reading of 門.
  - 日本国語大辞典 restricts only the strait sense to 門, so the two Japanese dictionaries are not fully aligned.
  - JMdict (via jisho) lists 鳴門 なると, a common word meaning a strait with roaring tides, which uses 門 as と.
- **Minimal remedy, either:**
  - change the row to the 門-specific senses, for example "門 と - (archaic) entrance; narrows", noting that the modern door/shutter と is written 戸; or
  - use 鳴門 なると as the example, after adding its source record.

  Revise line 42 to match.
- **Confidence:** medium.

## Optional
- **逆:** 莫逆 ばくげき is correct; both dictionaries use it as the main headword. However, it is literary (from 荘子) and has the variant ばくぎゃく. 逆鱗 げきりん, as in 逆鱗に触れる, is a better-known ゲキ example.
- **門:** 門出 かどで or 門松 かどまつ would be more familiar examples of かど. These would need source records.
- **鉱石.md:** it could link to `words\石.md` and `words\採掘.md` ("mining"), which both exist.

## Limits
- I had no Git execution, so I could not check the committed state or diff the 19 related articles. Instead I inspected every link passage in them.
- Stroke drawing paths were not reviewed.
- My overlap check of word-quiz candidates used keyword sweeps, not every title. Substring hits such as そろそろ "slowly", 厚い "thick" and ずけずけ "bluntly" are not real equivalences. Larger quizzes that rely on fallback were not simulated.
- B23-R-01 rests on a disagreement between dictionaries.
- The jisho.org results may come from a newer JMdict release than the pinned snapshot.
- None of this is native-speaker certification of example naturalness.
