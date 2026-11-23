# Batch 146: confirmation review (reviewer 1, Claude)

Snapshot: commit 5e61ef074618251796ad971f99736e5663f36df6 (5e61ef07), revised from the reviewed snapshot 38833c7f. Reviewer model: Claude (Anthropic model family); the exact version is not exposed to me.

Scope:
- This packet:
  - `INSTRUCTIONS.md`, `CHANGES.md` and `RESPONSE.md`: in full.
  - `diffs\fix.patch`: in full, all 158 lines.
  - Revised cards 煮 熟 牧 玄 甚 癖 益 盛 睡: each read in full, with line numbers.
  - `checks\quiz-safety.txt`, `checks\link-targets.tsv`, `evidence\README.md`, `evidence\QuizBuilder.kt` and `evidence\kanji-remarks.json`: in full.
  - `checks\reading-options.txt`: the command, every card header and its "unlisted" and "note" lines, then the 甚 癖 益 盛 sections in full.
  - `checks\reading-exposure.txt`: the head and the last 30 lines (the 眺 and 睡 sections and the summary).
  - `evidence\KanjiReadings.kt`: grep only, for the stem, key and distinct logic (lines 25–59).
- My initial report `reports-146\initial-claude.md`: in full.
- Original packet, read-only:
  - `evidence\public-source\weblio-牧.txt` (the Daijisen 牧 entry);
  - grep of `evidence\joyo-pages.md` for 牧 and 甚;
  - grep of `evidence\jmdict-families.xml` for 手癖 and 難癖.
- Public web: Weblio / Digital Daijisen 煮凝り, read in part (the headword and the definition).
- Not opened:
  - the unchanged cards 狂 狭 献 環 盾 眺 and 潔 (their quiz options were judged from `checks\` and the titles);
  - `Words.kt`, `meta-scan.txt`, `lint.txt` and the other check logs.
- Not present: `evidence\jmdict-cited-entries.xml`, which README describes as "(none)", is not in the folder.

Dispositions:
- C1 - RESOLVED.
  - 甚.md l.35 and l.37 now say 甚 writes はなは, with だしい (甚だしい) and だ (甚だ) as okurigana.
  - This matches KANJIDIC2 はなは.だ and はなは.だしい.
  - The aligner wording is gone from l.41.
  - See new Finding 1 for a leftover inconsistency on l.34 and l.41.
- C2 - RESOLVED.
  - 甚 l.33 and 癖 l.33 are now plain `on`.
  - "Source-only" remains only on 狭 コウ, 献 たてまつ.る and 玄 くろ.い, where no ordinary word exists.
- C3 - RESOLVED.
  - 益 l.43: 益体 = ヤク + タイ, and only 益荒男 is a whole-word reading.
  - This matches the Daijisen headword やく‐たい【益体】, which I checked in round 1.
- C4 - RESOLVED.
  - 煮 l.39: 煮凝り = に + こごり, and only 煮麺 is a whole-word reading.
  - Now verified live: the Digital Daijisen headword is 「に‐こごり【煮▽凝り／煮▽凍り】」.
- C5 - RESOLVED.
  - 熟 l.51 now names only 熟語 as linked and calls 熟練 and 熟慮 "examples without word articles", which is accurate.
  - Not re-linking 語 and 練 in this sentence is acceptable, because both are already linked on l.41 and in the Notes (l.52, l.54).
- C6 - RESOLVED. 玄 l.34 says "two-stroke lid". 亠 is 2 strokes: 2 + 3 = 5, matching the front matter.
- C7 - RESOLVED.
  - 癖 l.37 says "often becomes ぐせ".
  - 手癖 てくせ/てぐせ and 難癖 なんくせ match the pinned JMdict entries.
  - "ペキ after the small っ" is accurate.
  - "the 潔 card links back here" is true: the 潔 remark is now "[癖](癖.md) supplies ヘキ in 潔癖." (kanji-remarks.json).
- C8 - DECLINE ACCEPTED, for the title only. The other parts of C8 are resolved.
  - Resolved parts:
    - The kana ぼくどう and ぼくよう were added (l.53).
    - 治 御 官 司 導 were removed from `quiz_exclusions` (l.14, 12 kanji remain), and l.54 explains why.
  - Why the title is defensible:
    - Daijisen sense ② of 牧 is 「人々を治め導く。「牧師・牧民」」, which is the pastoral, shepherding-people sense.
    - The Joyo table's ボク examples include 牧師.
    - English "pastor" literally means a shepherd of a flock.
    - It remains a compound-derived gloss rather than a KANJIDIC2 meaning, but that is an editorial choice, not an error.
  - Quiz safety:
    - The 牧 prompt always fills all three slots from 歌 山 雨 (QuizBuilder adds curated distractors first, and quiz-safety shows 3/3). The five removed kanji therefore never appear as 牧's options.
    - When 治, 御, 官, 司 or 導 is the target, 牧's title is not a defensible meaning of that kanji.
    - 僧, 坊 and 師 stay excluded, which is consistent with "pastor".
- C9 - RESOLVED.
  - 盛 l.36 links only 盛り under さか.る.
  - l.37 links 盛ん under さか.ん and says it shares the stem さか.
  - l.39 has no aligner text, and l.43 is consistent with it.
  - The stem claim matches the app: `KanjiReadings.kt` l.28–29 and l.59 collapse readings that share a stem into one reading card.
- O1 - RESOLVED. A grep of all 15 revised cards finds no "align", "repo's" or "the repo" left (煮 l.36, 甚 l.37/41, 盛 l.39 and 睡 l.37 are clean).
- O2 - DECLINE ACCEPTED. It was optional. 牧 was fixed; the unglossed kana in the Notes of 狭, 狂 and 癖 are further examples and are polish only.
- O3 - DECLINE ACCEPTED. やしゃご for 玄孫 is an optional extra.
- O4 - DECLINE ACCEPTED. The 狭霧 line is not wrong; the request was wording polish.
- O5 - DECLINE ACCEPTED. The audit label "card text" is still applied to the --extra readings (for example いたい for 甚 in reading-options l.134). It has no effect on the counts and does not affect the content.
- O6 - DECLINE ACCEPTED. 環 and 鳴 use "ring" in clearly different senses.
- O7 - DECLINE ACCEPTED. A learner is unlikely to choose 相 "mutual; aspect" for 眺.
- O8 - DECLINE ACCEPTED. Extra exclusions only narrow the option pool; they cannot create a wrong key.
- O9 - DECLINE ACCEPTED. The 眺める link is correct as written.

Verdicts:
- Correctness: NEEDS FIX for 甚 (Finding 1, minor). The other eight changed cards are CLEAN.
- Scoped coverage: CLEAN.
- Consistency and quiz safety: NEEDS FIX for 甚, on text consistency only (Finding 1). Quiz mechanics are CLEAN for all 15 cards:
  - Meaning prompts: every card's three wrong options come from its curated distractors. The titles in quiz-safety.txt are not defensible as correct answers, and that file reports 0 errors.
  - The 牧 exclusion change only matters when 牧 is offered as a fallback option for 治, 御, 官, 司 or 導, and 牧's title is wrong for each of them.
  - Reading prompts: no metadata changed. reading-options reports 0 problems, and reading-exposure reports 0 production or padded hits, with the same 10 latent collisions as before.
  - Links: all 22 links on changed lines resolve, and every quoted gloss matches the target title.
- Comprehensibility: CLEAN. There is minor polish under Optional.

Confirmation: NEEDS FIX. Every RESPONSE item is RESOLVED or DECLINE ACCEPTED, but one minor new defect was established (Finding 1). It is tightly coupled to the C1 fix.

Findings:
1. Minor. Facets: consistency and correctness, with comprehensibility affected. File: `kanji\甚.md` l.34–35 and l.41.
   - **Claim:**
     - l.41 says "Practice selects はなは.だ, the reading in the linked word article 甚だしい". The same paragraph says the Joyo table shows "はなはだしい with 甚だしい".
     - The revised l.35 and l.37 say that in 甚だしい, 甚 writes はなは and だしい is okurigana. That is the KANJIDIC2 form はなは.だしい, not はなは.だ, which is 甚だ.
     - So the card now attributes 甚だしい to two different readings. It also files the 甚だしい link on the はなは.だ row (l.34).
     - The old l.41 justified this with "which the repo's aligner labels by its stem". The revision removed that justification but added no replacement.
     - l.35 also no longer says why はなは.だしい is "not selected separately".
     - The same pattern was fixed for 盛 in C9 and is explained in 煮 l.36 ("shares the stem に with に.る").
   - **Impact:** the card has an internal contradiction in the paragraph that teaches the okurigana boundary. The quiz key is unaffected: the app's `stem()` collapses はなは.だ and はなは.だしい into one reading card.
   - **Remedy:**
     - l.35: "…where 甚 writes はなは and だしい is okurigana; it shares the stem はなは with はなは.だ, so it is not selected separately".
     - l.41: "Practice selects はなは.だ; the linked word article 甚だしい shares its stem はなは."
     - Alternatively, move the 甚だしい link to the はなは.だしい row, as was done for 盛ん. The C9 approach of keeping a link on the selected row is not available here, because 甚だ has no article.
   - **Evidence:**
     - joyo-pages.md l.498–499: separate はなはだ (甚だ) and はなはだしい (甚だしい) rows;
     - KANJIDIC2 はなは.だ and はなは.だしい;
     - 甚.md l.35, l.37 and l.41;
     - KanjiReadings.kt l.28–29 and l.59.
   - **Confidence:** high that the text is inconsistent.

Optional:
- 盛 l.37 glosses 盛ん twice: "thriving; active; "prosperous; flourishing; thriving; successful"". "Thriving" appears twice. Keep the title gloss, or introduce the quote with "JMdict:".
- 牧 l.54: "All twelve kanji named in the last two bullets are kept out", but the same bullet then names five more kanji. Literally, 17 kanji are named. "The nine above and these three" would avoid the miscount.
- 牧 l.26 labels the 牧師 sense "Govern", while the title calls it "pastor". "Govern and guide people" would match Daijisen 「治め導く」 and connect it to the title.

Limits:
- **Execution:** every assistant response contained exactly one tool call. I issued no parallel calls and used no sub-agents. I wrote only this report file.
- **Unchanged cards:** I did not reopen 狂 狭 献 環 盾 眺 or 潔. Their quiz options were judged from quiz-safety.txt, reading-options.txt and their titles, together with my round-1 reading.
- **Quiz mechanics:** QuizBuilder.kt was read in full, but only part of KanjiReadings.kt (the stem, key and distinct logic) and none of Words.kt. I did not rerun any audit or simulation.
- **What the audits cannot show:**
  - whether a fallback title is semantically defensible as a correct answer for some other target (I reasoned this only for 牧 and the five removed kanji);
  - behaviour in the Android JVM tests and the Kotlin cross-check, which were not run;
  - learner-facing rendering on a phone.
- **"Pastor":** I did not check the title against other learner dictionaries; the decline is judged on Daijisen, Joyo and English usage.
- **Sources:** JMdict facts come from the pinned extracts in the original packet. Live JMdict may differ.
- **Model:** the reviewer model is self-identified; the exact model version is not available to me.
