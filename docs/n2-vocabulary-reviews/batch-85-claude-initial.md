## Snapshot
**36f7c0c4bdb997b4d2939cb191ee6cfe43a58cdb** (parent 2d4524abd2a54dd70692950f443230d2d0a1204f). I reviewed committed content only. My file tools cannot run Git, so I could not check that the working tree matches this commit. I also could not check that `batch-85-related.patch` matches the committed diff. The author's Git, hash and equivalence checks were not repeated by me.

## Scope
**Model:** claude-opus-5.5 (Claude family). This is the same blind reviewer session, finished without further tools. It is not a fresh independent review. I received no other reviewer's report and no author quiz rationale.

**Execution limits**
- **First attempt:** after the snapshot read I sent three views at once. The monitor stopped the run, and that attempt produced no review.
- **Serial continuation:** about 49 calls completed one at a time. Then I sent two requests together: a reread of `盛る.md` lines 14–58 and a mapping grep for 1696. Both were interrupted and neither completed. My 盛る judgments rely on the earlier complete article read, the earlier mapping read, and a completed line-pin grep.

**Complete reads**
- Frozen snapshot JSON.
- `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md` lines 18–103.
- TSV header (line 1) and rows 1682–1701 only.
- Mappings 1–10 and 11–20.
- Principals 1–10 and 11–21, including restrictions, flags, POS and one-based senses.
- Components 1–17 and 18–34.
- Labels 1–45, 46–90, 91–135 and 136–179. I used these only as navigation, not as evidence about word bodies.
- `batch-85-related.patch`, `kanji\燃.md` and `kanji\缶.md`.
- All twenty assigned articles.
- `public-bodies.txt` lines 1–408.
- Two older articles: `words\注ぐ.md` and `words\初め.md`.

**Searches**
- A glob confirming which kanji and word cards exist.
- A grep of `kanji\紅.md` for 紅葉 (line 40). I did not read the whole card.
- A targeted grep of `words\` titles for selected English tokens (52 hits).
- A grep of the `quiz_exclusions` lines in 49 named word files (33 had such a line).
- A grep pinning line numbers for the findings.

**Not inspected**
- `batch-85-review-evidence-v2.json`.
- `family-inspection-01` to `13` and `old-body-inspection-01` to `19`.
- `related-kanji-inspection-01`.
- The three `final-precard-*` files and `public-bodies.json`.
- `docs\confusable-words.md`, `docs\jlpt-levels.md`, `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`.
- Complete dictionary families for comparison words, and older articles other than 注ぐ and 初め.
- No web pages were fetched.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1682 | words\モダン.md | NEEDS FIX | CLEAN | CLEAN | F3: no quiz guard against おしゃれ or スマート, which share "stylish" |
| N2:1683 | words\餅.md | CLEAN | CLEAN | CLEAN | 餅 has no kanji card and is correctly unlinked |
| N2:1684 | words\もったいない.md | CLEAN | CLEAN | CLEAN | Senses 1 and 2 taught; guards 無駄, 惜しい, 贅沢 |
| N2:1685 | words\モデル.md | NEEDS FIX | CLEAN | NEEDS FIX | F1: wrong particle role in モデルにする |
| N2:1686 | words\元々.md | NEEDS FIX | CLEAN | CLEAN | F4: no guard against 初め, which shares "outset"; げんげん not imported |
| N2:1687 | words\物置.md | CLEAN | CLEAN | CLEAN | Guards 倉庫 and 小屋; translation polish in Optional |
| N2:1688 | words\物語る.md | CLEAN | CLEAN | CLEAN | Senses 1 and 2 supported by the public capture |
| N2:1689 | words\物差し.md | CLEAN | CLEAN | CLEAN | Nを物差しにする is correct; 定規 guarded |
| N2:1690 | words\物凄い.md | NEEDS FIX | CLEAN | CLEAN | F2: unsupported claim that もの intensifies; 凄 has no card, as stated |
| N2:1691 | words\モノレール.md | CLEAN | CLEAN | CLEAN | — |
| N2:1692 | words\紅葉.md (もみじ) | CLEAN | CLEAN | CLEAN | One-sentence change only; title, reading こうよう and guard [葉] preserved; maple and foliage both taught |
| N2:1693 | words\揉む.md | CLEAN | CLEAN | CLEAN | 揉 has no card and is unlinked; possible over-guard in Optional |
| N2:1694 | words\燃やす.md | CLEAN | CLEAN | CLEAN | もす is correctly assigned to 燃す |
| N2:1695 | words\催し.md | CLEAN | CLEAN | CLEAN | 催 has no card; possible over-guard 機能 |
| N2:1696 | words\盛る.md | CLEAN | NEEDS FIX | CLEAN | F5: selected sense 3 framed as a side note; title leads with unselected slang |
| N2:1697 | words\問答.md | CLEAN | CLEAN | CLEAN | Noun and する-verb; guards 会話, 議論, 論争 |
| N2:1698 | words\やかましい.md | CLEAN | CLEAN | CLEAN | Senses 1, 3, 4 (+2) match the public capture; 静か.md exists |
| N2:1699 | words\夜間.md | CLEAN | CLEAN | CLEAN | Sunset-to-sunrise definition supported; よま not imported |
| N2:1700 | words\薬缶.md | CLEAN | CLEAN | CLEAN | Medicine-brewing origin supported; 釜 guarded; sense 2 metadata question in Limits |
| N2:1701 | words\役者.md | CLEAN | CLEAN | CLEAN | Same title as 俳優 (deduplicated); sense-2 guards are justified |

**Kanji and baseline preservation: CLEAN.** The patch only adds 燃やす to `kanji\燃.md` (reading row and Common words; its ID 1582900 was already in the metadata). It only adds 薬缶 and ID 1605370 to `kanji\缶.md`. The note in 燃.md that もす belongs to 燃す is correct. `kanji\紅.md` is untouched, and its line 40 still links 紅葉 as こうよう.

**Components: CLEAN.** Links go to cards that exist (元, 物, 置, 語, 差, 紅, 葉, 燃, 問, 答, 夜, 間, 薬, 缶, 役, 者). Characters without cards (揉, 凄, 餅, 催, 盛, 喧, 勿) are not linked, and no cards are invented. I noticed no problem with the kanji metadata on the twenty articles.

**Reciprocity: CLEAN.** Both new pairs (燃 and 燃やす, 缶 and 薬缶) link in both directions. The existing 紅 and 紅葉 pair is preserved.

**Mappings: CLEAN.** All twenty mappings agree with the TSV rows. For 紅葉, the mapping follows the preserved こうよう entry (1578780) and adds もみじ senses 2857870:1 and 2. The article does not merge the two families.

## Findings
**B85-F1 — Moderate; correctness and comprehensibility; words\モデル.md:28**
- **Claim:** "モデルにする means to use something as a model; に identifies the model being used." In XをモデルにするX, を marks X, the thing used as the model; に marks the role モデル. The article gives no XをモデルにするX example, so learners may produce *Xにモデルにする.
- **Remedy:** "In XをモデルにするX, を marks the person or thing used as the model and に marks the role", with an example such as 実在の人物をモデルにした小説.
- **Evidence:** line 28. 物差し.md in the same batch correctly teaches Nを物差しにする.
- **Confidence:** high.

**B85-F2 — Minor; correctness (formation versus etymology); words\物凄い.md:29**
- **Claim:** 物 "contributes the もの element, which intensifies" 凄い. The public capture's sense 3, 何となく恐ろしい, points to the prefix もの- meaning "somehow" or "vaguely". It does not support intensification. The stronger modern sense of the word is a separate matter from how it was formed.
- **Remedy:** describe it neutrally: 物 writes the prefix もの-, and 物凄い should be learned as one word that is stronger than すごい today. Remove the "intensifies" claim.
- **Confidence:** medium.

**B85-F3 — Minor; correctness (quiz guards); words\モダン.md:9 (also :4, :16)**
- **Claim:** モダン's title "modern; stylish" shares "stylish" with おしゃれ.md:4 ("stylish; dressing up") and スマート.md:4 ("stylish; slender; deft"). Neither side lists a guard. Either word could appear as a valid-looking wrong choice. The repository already guards this overlap elsewhere: スマート.md:9 excludes おしゃれ.
- **Remedy:** add おしゃれ and スマート to モダン's `quiz_exclusions`.
- **Confidence:** medium-high. I did not read the older おしゃれ and スマート articles.

**B85-F4 — Minor; correctness (quiz guards); words\元々.md:9 (also :4, :17)**
- **Claim:** "originally; from the outset" overlaps 初め.md:4 ("beginning; outset"). 初め also teaches 初めは as "at first", contrasting with later. 初め.md has no `quiz_exclusions`, and 元々 guards only 本来 and 元.
- **Remedy:** add 初め to 元々's `quiz_exclusions`.
- **Confidence:** medium. Whether 最初 needs a guard is unchecked.

**B85-F5 — Minor; scoped coverage (selected versus additional senses); words\盛る.md:4, :24, :28**
- **Claim:** selected sense 3, administering medicine or poison, appears only as "The dictionary also records…" at line 28. That wording makes a selected sense sound like a side note. Meanwhile the title's "exaggerate" comes from additional sense 6, which line 24 calls slang but not additional recognition.
- **Required remedy:** reword line 28 as a taught meaning, ideally with an example such as 毒を盛る, and label line 24 as additional recognition.
- **Optional:** swap "exaggerate" in the title for a selected-sense gloss.
- **Evidence:** the earlier mapping read (selected 1, 2, 3; additional 6) and the public もる capture (sense 3 薬剤を調合する…毒を飲ませる; sense 6 俗に…大げさに言う). Other lines check out: the 注ぐ/つぐ cross-reference at line 44 matches 注ぐ.md, and the さかる entry is not imported.
- **Confidence:** medium.

## Optional
- **words\物置.md:21:** "There are tools in the garden shed" fits Nに Nがあります better than "The tools are…".
- **words\元々.md:21:** "She has always liked cooking" is more natural than "has liked cooking from the outset".
- **Possible over-guards** (title-based, low to medium confidence, nonblocking):
  - 物凄い→ずっと, and possibly なかなか, from inheriting a whole list of intensifiers.
  - 揉む→問答, which seems to rely only on the chain through 議論.
  - 催し→機能, unless the 催し article uses the English word "function".
  - モデル→種類 and →標本, which look weak.
  - 盛る→与える is justified by the administering sense.

## Limits
- **Interrupted reread:** my 盛る conclusions do not depend on the interrupted reread or mapping grep. I cannot confirm from memory whether the article already has a sense-3 example.
- **Quiz guards:** I did not read older articles or complete dictionary families for comparison words beyond 注ぐ and 初め. F3, F4 and the over-guard points rest on titles and exclusion lines. The title search used selected English words only, so I am not certifying the quiz guards as complete. For example, I did not search "rice cake", "cake" or "train" titles, and I did not check whether 最初 has an article.
- **薬缶 sense 2:** the mapping's source note calls sense 2 (bald head) recognized, but the mapping's additional senses omit it, while the article only distinguishes it. This metadata consistency is unresolved.
- **紅葉:** a sentence that was already in the article refers to an earlier source row pairing こうよう with maple. The TSV restriction stopped me checking it.
- **Uncovered material:**
  - I read `kanji\紅.md` only by grep, not as a full card.
  - I did not inspect the private evidence-v2, family-inspection, old-body-inspection or pre-card files, or the docs snapshots.
- **Single authority:** the public captures come from one dictionary, and its sense numbering differs from pinned JMdict.
- **No Git:** I could not verify that the committed content matches the patch.
- **Scope of verdicts:** CLEAN means no actionable defect found within this scope. It is not a native-speaker certification.
