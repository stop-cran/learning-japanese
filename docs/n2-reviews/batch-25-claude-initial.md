**Snapshot:** 7eedeb1589aedfbf26e84aa3d7a700b5930ebec8 (baseline eece75b4b18bec3bcc6a058670e73947555948d4; branch jlpt-n2-kanji; the snapshot file says the worktree was clean). I reviewed committed files only. I had file tools but no Git, so I could not confirm that the files on disk match that commit, or that the 23-file scope and the patch match the commit diff. I relied on the snapshot JSON and the supplied patch.

**Scope:** One reviewer, claude-opus-5.5 (Claude family). I worked alone, made no edits and used no other agents.
- **Read completely:** kanji\骨.md, kanji\麦.md, kanji\黄.md, kanji\鼻.md and kanji\齢.md.
- **Narrow scope:** the 年 distractor line, and the link edits in the "How the kanji combine" lines of the seven word articles (words\骨.md, words\骨折.md, words\小麦.md, words\黄色.md, words\黄色い.md, words\鼻.md and words\年齢.md). I read the full patch.
- **Evidence used:** batch-25.json (all records read), docs\n2-source-snapshot.json (all five kanji are in the N2 set), docs\confusable-words.md, words\年.md, the titles and distractors of comparison cards, Kotobank 齢 and a Jisho search for 黄金.
- **Not reviewed:** stroke drawing paths, manifest.json, validator output, and the unchanged teaching text in 年.md and the seven word articles.
- **Not read (forbidden):** authoring notes, review ledgers, author receipts and other reviewers' output.

**Verdicts:**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 骨 | CLEAN | CLEAN | CLEAN |
| 麦 | CLEAN | CLEAN | CLEAN |
| 黄 | CLEAN | CLEAN | NEEDS FIX (B25-1) |
| 鼻 | CLEAN | CLEAN | CLEAN |
| 齢 | CLEAN | CLEAN | CLEAN |

- **Metadata:** readings, stroke counts, radicals and grades on all five cards match the source record. Stroke counts in the stroke JSON files also match (10, 7, 11, 14, 17).
- **Reading examples:** every example produces the stated reading, including 骨折 こっせつ, 硫黄 いおう, bound こ- in 黄金 こがね, and the explained source-only 齢 とし. I confirmed on Kotobank: Daijisen gives よわい【齢／歯】 with 「―を重ねる」, and Jitsū lists 字訓 とし・よわい.
- **Distractors:** all 15 choices are existing cards with meanings that are clearly wrong for the target.
  - 齢 and 歳 ("years of age") each have three curated distractors, so the default quiz never fills a slot with the other.
  - The 12 cards that still have only two distractors (人, 休, 何, 入, 出, 口, 女, 山, 日, 月, 男, 買) have no meaning overlap with the new titles.
- **年 edit (CLEAN):** adding 牛 "cattle, cow" gives a third wrong option, which stops the quiz from filling in 齢 "age; years lived", an ordinary meaning of 年.
- **Seven word-article edits (CLEAN):** each only adds a link at the kanji's introduction. All targets exist and the `../kanji/` paths are correct. Titles, readings and other metadata are unchanged.

**Findings:**
- **B25-1**
  - **Severity and facet:** Minor; comprehensibility.
  - **Location:** kanji\黄.md:44.
  - **Claim and impact:** "do not replace it with another source reading without checking the expression" relies on unexplained internal jargon and points to readings it never names. Learners cannot act on it.
  - **Remedy:** name the alternatives JMdict lists, こうしょく and おうしょく, with a short note that they are not the everyday reading. Alternatively, delete the clause.
  - **Evidence:** JMdict 1576760 lists the readings きいろ, こうしょく and おうしょく.
  - **Confidence:** high that the sentence is opaque; the learning impact is low.

**Optional:**
- **黄.md:31, 39, 43:** use 黄金 おうごん as the オウ example, or note that it is the more frequent reading. In JMdict, 1181860 おうごん has ichi1/news1/nf09 and 2839304 こがね has only ichi1. That is a priority comparison, not proof that こがね is rare.
- **麦.md:42:** rephrase as "read ばくが, not むぎが". At present the sentence talks about confusing a word with a reading.
- **齢.md:31, 34, 39:**
  - Note that よわい is outside the jōyō reading list (Daijisen marks it ▽).
  - Explain that Jitsū is the kanji dictionary 字通.
  - Consider citing Jitsū's 形声 analysis with 令 as the phonetic.
- **Additional common words (not checked against the pinned source):** 高齢, 麦茶, 鼻血 and 黄身.

**Limits:**
- Git was not available (see Snapshot), and I did not run the validator or manifest build.
- I did not review stroke paths, which came from the repository's stroke converter; I only checked file existence and stroke counts.
- Dictionary evidence was limited to the selected records in batch-25.json, Kotobank for 齢, and the Jisho search, which added nothing beyond JMdict.
- The register of よわい is unverified: Daijisen gives no label, and JMdict has news1/nf20.
- I took quiz fallback behaviour from docs\content-format.md and did not re-check the app's QuizBuilder code.
