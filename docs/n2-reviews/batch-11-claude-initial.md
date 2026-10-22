## Snapshot
586989dc37529aaa66ff39ba9d84d0560f2a244d, committed files only; baseline aa3dabe0903908855a40b15d697fea23ec0ddf0a. I had file tools but no Git, so I could not confirm the commit, the diff, the 60-file scope or the clean worktree. Those rest on the author's word.

## Scope
- **Model:** claude-opus-5.5 (claude family). Worked sequentially with no delegation and no edits.
- **Read in full:**
  - the guidance files (.github\copilot-instructions.md, .github\instructions\content-structure.instructions.md, docs\content-format.md:18-109);
  - all 15 kanji cards (査 栄 根 械 棒 森 植 極 橋 欧 武 歴 殿 毒 比);
  - all 4 new word articles (栄える 極める 欧州 御殿);
  - batch-11.json, with complete records pulled for every consequential claim (1578350, 1173980, 1600620, 1254180, 1591970, 1270560, 1181190).
- **Related edits (narrow scope):** I checked the component-link passages in all 21 named articles and nothing else in them.
- **Also used:**
  - docs\confusable-words.md, which has no rows for 栄, 極, 欧州, 御殿, 決める or 西洋;
  - existing word articles, for distractor and quiz-candidate comparison;
  - Kanjipedia pages kanji/0001577800, kotoba/0001578400 and kotoba/0001580300;
  - the pinned app scorer at kanji-cards-android@8c9713f (Words.kt and WordQuizScreen.kt).
- **Not reviewed:**
  - drawing paths in the stroke JSON files (from the pinned converter);
  - unchanged teaching text in the 21 related articles;
  - the forbidden ledgers and reports, which I did not open.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\査.md | CLEAN | CLEAN | CLEAN |
| kanji\栄.md | NEEDS FIX (B11-01) | NEEDS FIX (B11-01) | CLEAN |
| kanji\根.md | CLEAN | CLEAN | CLEAN |
| kanji\械.md | CLEAN | CLEAN | CLEAN |
| kanji\棒.md | CLEAN | CLEAN | CLEAN |
| kanji\森.md | CLEAN | CLEAN | CLEAN |
| kanji\植.md | CLEAN | CLEAN | CLEAN |
| kanji\極.md | CLEAN | CLEAN | NEEDS FIX (B11-02) |
| kanji\橋.md | CLEAN | CLEAN | CLEAN |
| kanji\欧.md | CLEAN | CLEAN | CLEAN |
| kanji\武.md | CLEAN | CLEAN | CLEAN |
| kanji\歴.md | CLEAN | CLEAN | CLEAN |
| kanji\殿.md | CLEAN | CLEAN | CLEAN |
| kanji\毒.md | CLEAN | CLEAN | CLEAN |
| kanji\比.md | CLEAN | CLEAN | CLEAN |
| words\栄える.md | NEEDS FIX (B11-03) | CLEAN | CLEAN |
| words\極める.md | CLEAN | CLEAN | CLEAN |
| words\欧州.md | CLEAN | CLEAN | CLEAN |
| words\御殿.md | CLEAN | CLEAN | CLEAN |

What came back clean:
- **Metadata:** every stroke count, radical and grade matches batch-11. 極 shows 12 strokes; KANJIDIC2 also lists 13, and the primary value 12 is correct.
- **Distractors:** all 45 are semantically wrong options. Each new kanji has three, plus a useful linked word article.
- **Two-choice fallbacks:** no new synonym risk in any older two-choice kanji card.
- **Related links:** all 21 component-link passages are accurate.

## Findings

### B11-01 — minor; correctness and scoped coverage — kanji\栄.md:34, 36, 50
- **Problem:** The え row says "Source-only reading" (line 34). Line 36 then says that for ヨウ and え "No suitable word example was established in the inspected JMdict snapshot… not recommendations to use this kanji as an everyday spelling of a word."
- **Why it's wrong:** The snapshot holds 見栄 みえ, which the card's own footer cites as entry 1578350 (line 50). The record:
  - priority ichi1, news1, nf20;
  - sense 1 "show; display; pretensions; appearances; ostentation; vanity", restricted to the spellings 見栄 and 見え;
  - the 見栄 spelling is flagged "ateji (phonetic) reading", meaning 栄 is used for its sound え.
- **Impact:** 見栄 is a common everyday spelling of a common word, so the qualification is false for え. Learners also miss the best-known え word.
- **Separate point:** ヨウ really has no example. In 栄耀 えよう (1173980, obsolete kana usage), え belongs to 栄 and よう to 耀.
- **Remedy:** Fill the え row with "見栄 みえ - show; vanity (ateji: 栄 used for its sound)". Keep the source-only qualification for ヨウ alone.
- **Evidence:** batch-11.json:740-785 (1578350); batch-11.json:~790 (1173980).
- **Confidence:** high.

### B11-02 — minor; comprehensibility — kanji\極.md:34-36, 48
- **Problem 1, the marker:** Only き.まる (line 36) is marked "(outside-Joyo reading)". Kanjipedia's 極 page lists the Jōyō readings as キョク, ゴク, きわめる, きわまる and きわみ, and marks both きめる and きまる as 外 (outside the table). So the unmarked き.める row (34) reads as if it were standard, though it is as non-Jōyō as き.まる. The same goes for -ぎ.め and きわ.まり, which are not among the five Jōyō readings.
- **Problem 2, line 48:** It says "that JMdict entry also lists 決める". Entry 1254180 lists 決める first and 極める second, both unflagged. The wording makes 極める sound primary, and unlike line 49 it gives no "not the usual everyday spelling" qualification. I am not claiming rarity from missing priority tags: 極める has no spelling priority, but the reading きめる does.
- **Remedy:** Mark the non-Jōyō rows consistently, or replace the per-row marker with one note listing the five Jōyō readings. Reword line 48 to "that entry's first-listed spelling is 決める".
- **Evidence:**
  - https://www.kanjipedia.jp/kanji/0001577800 (readings and 外 marks);
  - kotoba/0001580300, whose word list marks △極まる(き－まる) and △極め(きめ) but 極める(きわ－める) without △;
  - batch-11.json:2709-2711 (entrySpellings ["決める","極める"]).
- **Confidence:** high for the marker inconsistency; medium for the impact of the wording.

### B11-03 — minor; correctness (quiz metadata) — words\栄える.md:8
- **Problem:** The Japanese→English quiz shows only the written form 栄える, with no reading.
- **How the clash happens:** 輝く (words\輝く.md:4,8: "shine; sparkle; glow", tags wago, verb, intransitive, light; it excludes only 光る) ties at the top score of 7 with about 35 candidates. It is therefore picked in roughly 3 of every 35 栄える questions (about 8%).
- **Why that's a defect:** Under the はえる reading, "shine; glow" is a correct meaning for that written form. JMdict 1600620 lists the 栄える spelling unflagged with ichi2, and sense 1 is "to shine; to glow". The app teaches that meaning itself at kanji\栄.md:33 and words\栄える.md:43-45. content-format.md:95 requires an exclusion when a learner could reasonably accept either title.
- **Remedy:** Add 輝く to quiz_exclusions. 光る scores 5, is never selected, and is optional.
- **Evidence:**
  - Words.kt at 8c9713f: score = 2 per shared tag, +1 same type, +1 shared kanji; candidates are shuffled, sorted by score, and the top three taken;
  - WordQuizScreen.kt: the prompt is `word.word` only;
  - batch-11.json:~1066 (1600620).
- **Confidence:** medium-high.

**Checked and cleared:** 極める vs 決める. 決める's tags share only "wago" with 極める, so it scores 3 and is never selected. 極める.md:46-49 already separates the きめる reading.

## Optional
These are nonblocking:
- **欧州:** 西洋 "the Western world" ties at score 7. The overlap with "Europe" (JMdict 1181190) is borderline, so an exclusion is optional. 西洋 has no exclusion with ヨーロッパ either. ヨーロッパ's identical title "Europe" is deduplicated automatically.
- **御殿:** could mention the figurative 〜御殿 "luxurious mansion" use.
- **極:** could add a homograph note for 極まる きわまる vs きまる.
- **歴とした:** "genuine" is not a JMdict gloss (those are accepted, fully-fledged, clear, respectable), though it is reasonable.

## Limits
- **Git:** none available. The commit identity, the diff against the baseline, the exact 60-file scope and the clean worktree were not verified.
- **Stroke data:** the 15 stroke files' drawing paths were not reviewed; they are attributed to the pinned converter.
- **Quiz analysis:** relies on the pinned Words.kt and WordQuizScreen.kt (8c9713f). Current or exclusion-aware app versions may score differently.
- **batch-11.json:** this is selected evidence, not the full JMdict. An omitted spelling there was not treated as absence from the dictionary.
- **Naturalness:** invented collocations such as 部長殿 are plausible but not certified by a native speaker, and attestation does not prove frequency.
- **Related articles:** the unchanged parts of the 21 articles were not reviewed.
- **Forbidden files:** the ledgers and other reviewers' output were not read.
