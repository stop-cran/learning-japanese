# Batch 154 confirmation review — Claude

Snapshot: commit e5c945d6d3f83b97145100528e448747424fded5 (reviewed snapshot f8f3db8c). Reviewer: Claude (Anthropic), the same blind reviewer as in the initial round, working alone and read-only.

Scope:
- **This packet:**
  - INSTRUCTIONS.md, RESPONSE.md, CHANGES.md and evidence\README.md: read in full.
  - Revised cards 随, 隣, 雄, 飽, 飾 and 黙: read in full. 項: lines 18–30 (the only hunk is line 25).
  - diffs\fix.patch: every hunk header and every changed `-`/`+` line. Removed lines that start with "--" were filtered out by my grep. I judged the revised Joyo lines directly instead.
  - checks\: quiz-safety.txt and link-targets.tsv in full; reading-options.txt in full (all 15 prompts plus the total); reading-exposure.txt (totals line only).
  - evidence\: QuizBuilder.kt and daijisen-aku.txt in full. jmdict-cited-entries.xml: every headword, reading, priority, misc, s_inf and gloss line of all 21 entries.
  - Not opened: meta-scan.txt, KanjiMeaningMetadata.kt, KanjiReadings.kt and Words.kt (all four unchanged copies per README).
- **Original packet (read-only):**
  - joyo-pages.md: rows for ユウ (雄), モク/だまる (黙), ズイ (随), 飽, かざる and となる (隣).
  - kanjivg-components.txt: the 項 block.
  - titles\kanji-titles.tsv: rows for 追 辺 側 英 暗 沈 逮, plus a title-pattern search for side, beside, near, neighbo, adjac, vicinit, next, border, follow, accompan, hero, grand, magnific, silen, tacit and very.
  - repo\kanji\追.md, 辺.md and 側.md: front-matter title, kunyomi and distractors.
  - repo\kanji\釈.md: lines 36–43.
- **My initial report:** read in full.
- **Public web:** the Weblio / Digital Daijisen 飽く page, fetched live. Its [補説] matches evidence\daijisen-aku.txt.

Dispositions:
- **C1 - RESOLVED.**
  - `雄.md:39-40` add 英雄 えいゆう "hero; heroine; great person" (JMdict 1174680 sense 1, verbatim) and 雄大 ゆうだい "grand; magnificent; majestic" (1542540, the first three of its five glosses).
  - `雄.md:45` names 雄大, 英雄 and 雌雄. That matches joyo-pages.md:723, "ユウ 雄大，英雄，雌雄".
  - The Metadata ids add 1174680, 1542540 and 1312940. 雄勁 still establishes the quiz reading.
  - The declined sub-remedy, 英雄 in the 英 note, was optional. The author's reason is sound: a shared compound is not a shared meaning.
- **C2 - RESOLVED.**
  - `随.md:38` adds 随分 ずいぶん "very; considerably" and the kana note. JMdict 1372800 sense 1 contains "very" and "considerably" and carries "word usually written using kana alone".
  - The Metadata ids add 1372800.
  - Not adding 随時 and 随所 is acceptable. I had flagged them as less important.
- **O1 - RESOLVED.**
  - `隣.md:32` leads with 隣り合う となりあう "to adjoin each other; to sit side by side". That is JMdict 1598830 verbatim, and it is the Joyo example: joyo-pages.md:815 reads "となる 隣り合う".
  - The row then gives 隣る as archaic, which matches JMdict 2163190 misc "archaic".
  - `隣.md:41` is consistent with the row and drops nothing true.
- **O2 - RESOLVED.** `飾.md:23` now numbers senses 1, 2 and 4. All three are verbatim from JMdict 1357210, which has four senses. This agrees with the "fourth sense" in the 華 bullet at `飾.md:50`.
- **O3 - RESOLVED.**
  - `黙.md:34` adds the Kanjipedia 外 marking for もだす. I checked it live in round 1.
  - `黙.md:39-40` add 沈黙 and 暗黙. Both glosses are verbatim leading glosses of 1431810 and 1154700.
  - `黙.md:44` matches joyo-pages.md:667, "モク 黙殺，暗黙，沈黙".
  - Not adding 黙祷 is justified. In JMdict 1535010 the keb 黙祷 has no ke_pri; only 黙とう has news1 and nf22.
- **O4 - DECLINE ACCEPTED.** 走 "run" is clearly wrong in both directions. Distractor difficulty is an editorial preference, not a defect.
- **O5 - RESOLVED.**
  - `項.md:25` now reads "頁 stands on the right: a horizontal stroke and a left-falling stroke over 貝 … made of 目 … over 八".
  - KanjiVG 09805 agrees: stroke 4 is ㇐ and stroke 5 is ㇒, and 貝 covers strokes 6–12 with 目 on top and 八 at the bottom.
  - All four links resolve to exact titles (link-targets.tsv).
- **O6 - DECLINE ACCEPTED.** I had already noted that this matches corpus style. It is a corpus-wide editorial choice.
- **L1 - DISPUTE ACCEPTED.** My assumption was wrong. Unlinked Common words bullets are established: `repo\kanji\釈.md:40-41` lists 釈放 and 会釈 unlinked. I did not recount the claimed 1,812 bullets on 1,003 cards. The pattern itself is verified, and the placement of the C1 and C2 fixes is consistent with it.

Verdicts:
- **Correctness: CLEAN.** Every new quotation matches its source:
  - JMdict glosses, sense numbers, kana and archaic marks: against jmdict-cited-entries.xml.
  - Joyo examples: against joyo-pages.md.
  - The Digital Daijisen [補説] 「あく」は文章語的な表現: against evidence and the live Weblio page. The English paraphrase is faithful: 共通語 is rendered "standard Japanese", 一般に「あきる」を用い as "generally uses あきる".
  - The 頁 stroke description: against KanjiVG.
  - "the 追 card lists お.う", "the 辺 card lists あた.り" and "the 側 card lists そば": against the repo front matter.
- **Scoped coverage: CLEAN.** C1, C2 and O3 are covered. No changed card now omits a core word.
- **Consistency and quiz safety: CLEAN.**
  - **New pairs:** 随/追 ("follow; at will" vs "chase; pursue"; 追う sense 1 includes "to follow after"), 隣/辺 ("next door; adjoining" vs "vicinity; edge"; 辺り sense 1 "(in the) neighbourhood… nearby") and 隣/側 ("side"; そば sense 1 includes "(place) right next to" and "beside").
    - Each is a defensible direct overlap at title level. It is conservative, but it only narrows the option pool.
    - Each pair is declared once. None is a curated distractor of either card: 追's distractors are 近/週/返, 辺's are 返/込/道 and 側's are 内/右/左.
  - **App mechanics:** QuizBuilder's `excluded()` checks both directions, so 随 is now also kept out of 追's fallback options, and 隣 out of 辺's and 側's.
  - **Meaning options:** for all 15 cards, the post-fix options in quiz-safety.txt are unchanged and each remains defensibly wrong.
    - 隣: 遠/奥/裏. 裏 "reverse side; lining" is not "next door", and it is unaffected by excluding 側.
    - 随: 逆/離/導.
    - 鮮: two of its three curated cards supply no usable on reading, so its reading prompt fills two slots from the fallback. This is unchanged from the freeze.
  - **Title search:** it found no further unexcluded title synonym for the new words. 逮 "arrest; chase" vs 随: "chase" is not "follow", and no 逮 sense means follow.
  - **Reading options:** reading-options.txt shows 0 problems. Every curated reading differs from the prompt key (ズイ, となり, ユウ, あきる, かざる, だまる and the unchanged cards). The 8 latent collisions are unchanged.
- **Comprehensibility: CLEAN.** The new rows are long but parse cleanly on a phone.
  - On 隣:32, the em-dash-delimited gloss inside the sentence reads correctly.
  - The 飽 Japanese quotation carries an English paraphrase.
  - On 黙:44, "Kanjipedia also lists だんまり" now reads naturally after the もだす 外 note.

Confirmation: CONFIRMED

Findings: none

Optional: none

Limits:
- **Tool calls:** In one response I issued two grep calls at once. Both were read-only searches of titles\kanji-titles.tsv; the second repeated part of the first. This breaks the one-tool-call-per-response rule. Every other response contained exactly one tool call. I used no sub-agents, background jobs or other sessions.
- **Not verified:**
  - The "1,812 unlinked bullets on 1,003 cards" count (L1). I checked the pattern only, on 釈.md.
  - Live JMdict and live Kanjipedia in this round. I relied on the pinned evidence and my round-1 live check of Kanjipedia 黙.
  - The official Joyo PDF directly. I relied on joyo-pages.md.
- **Not run:** the Android JVM content tests and the app's reading-quiz code (KanjiReadings.kt and Words.kt were not opened). Reading-option safety is judged from reading-options.txt's simulation (100 seeds), which cannot prove the absence of rare seeds or pool configurations outside the audit.
- **Not reviewed in this round:** meta-scan.txt; the unchanged 8 cards, beyond their quiz options.
- **What the audits cannot show:** quiz-safety.txt shows only the curated-first option set for each target card. It does not show fallback fills when a batch card appears as a wrong option for some other target. I reasoned about that from QuizBuilder's two-way exclusion check and from title searches, not from an exhaustive simulation.
