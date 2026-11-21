# Batch 156 — initial review (Claude)

Snapshot: commit c6afa16315d5a88b5045eeb85d429b8f7fd90b1f (c6afa163); reviewer model: Claude (Anthropic), blind first reviewer, read-only.

Scope:
- Examined deepest: facet 1 (correctness) and facet 2 (scoped coverage). Facets 3 and 4 were also covered for all 10 cards, all 10 word articles and both diffs.
- Read in full:
  - INSTRUCTIONS.md
  - snapshot\kanji: 丹 乙 亜 仁 仙 伎 伏 伐 伯 伴 (.md)
  - snapshot\words: 丹念 乙 亜熱帯 仁 仙人 歌舞伎 降伏 伐採 伯仲 同伴 (.md)
  - diffs\kanji__潜.md.diff and diffs\words__伯母さん.md.diff
  - evidence: source-metadata.json, kanjipedia-senses.txt, joyo-pages.md, kanjivg-components.txt, daijisen-word-text.md
  - evidence\public-source\weblio-{丹,乙,亜,仁,仙,伎,伏,伐,伯,伴}.txt
  - evidence\audits: kanji-remarks.json, word-remarks.json, manifest-diff.md
- Read in part:
  - evidence\kanjidic2-records.xml: the 10 records.
  - evidence\jmdict-families.xml: about 45 entries printed. These include 1182940, 1182945, 1182970, 2837087, 2855480, 1576860, 1316400, 2220160, 1416890, 2870834, 1369620, 1599770, 1154990, 1387170, 1075090, 1218320, 1225090, 1193420, 1282940, 1622940, 1500220, 1602650, 1478010, 2107700, 1299200, 1474280, 1607070, 1607100, 1233560, 1478400 and 1874770.
  - evidence\jmdict-digest.tsv: rows grepped by id.
  - Stroke JSONs, compared programmatically with evidence\kanjivg-svgs.txt.
  - mechanical-checks.md: all sections.
  - evidence\audits\word-quiz.txt: each word's forward section; the 仁, 降伏, 伐採 and 同伴 tiers scanned by keyword; the reverse section scanned by keyword and its reading-quiz part read in full.
  - evidence\audits\reading-options.txt and reading-exposure.txt: grep and tails.
  - evidence\app-code\Words.kt: lines 177–261 (ReadingOptions.build).
  - snapshot\kanji\潜.md: grep.
  - titles\word-titles.tsv: grep.
  - packet listing.
- Web:
  - jisho.org search for わざおぎ.

Verdicts:
- Correctness: CLEAN for all 10 cards, all 10 word articles, all 10 stroke files and both diffs.
  - Front matter matches source-metadata and KANJIDIC2: grade, strokes, radical, on and kun readings, and name-reading counts.
  - Joyo, Kanjipedia 外, Daijisen and JMdict claims checked against the evidence matched. These include the JMdict notes quoted for 仙 セント, 伎楽, 技/伎, 亜ぐ, 乙夜, 乙子, 弟/乙 おと, 仁王/二王, 杏仁, 仁 senses, 降服, 伯仲 S2, 歌舞妓, 伏せる/伏す, 調伏, 討つ/伐つ, おじ/おば restrictions and 伴/とも.
  - Stroke files match KanjiVG 70a0b7ae in count, type and start point.
  - Mnemonic component claims match kanjivg-components.txt.
- Scoped coverage: CLEAN. Every Joyo reading and Joyo example of each kanji is present. Source-only readings are either shown or explicitly set aside: 伎 わざおぎ, 伴 とも, 乙 イツ/おと/きのと, 伏 ブク, 伐 ハツ, 伯 ハ/かみ, and the name readings. Each word's central sense is taught, and minor senses are omitted reasonably.
- Consistency and quiz safety: NEEDS FIX for words/乙.md (C1, minor). CLEAN for all other files.
  - The 潜.md and 伯母さん.md diffs each change exactly one line. Their links resolve to the intended cards, and kanji_remarks and link-plan verify report 0 problems.
  - 伯 は HIT (lead e): moot. The three curated cards 自 物 毎 all supply on readings, so the fallback is never reached. reading-exposure reports 0 production or padded hits.
  - The forward and reverse meaning tiers showed no synonym that a learner could pick as a second correct answer. Checks included 丹念↔真剣/丁寧, 降伏↔勝負/提出, 伯仲↔凌駕/勝負 and 同伴↔共同/合同. Needed exclusions such as 丁寧, 匹敵, 熱帯/温帯 and 従う are present or curated.
- Comprehensibility: CLEAN. One optional wording polish is listed under Optional.

Findings:
- C1 — minor — Consistency and quiz safety — words/乙.md:3 (reading: おつ).
  - Claim and impact: the word 乙's reading quiz can show 音 (おと) as a wrong option, but おと is an attested reading of the written form 乙 (JMdict 2837087 弟/乙 おと, archaic "younger brother/sister"). The 乙 kanji card teaches おと (乙.md:10, 33, 42, 53; 乙女 おとめ). A learner who knows 乙 = おと would face a "wrong" option that is a genuine reading of the prompt.
    - How it gets drawn: ReadingOptions.build takes 2 generated look-alikes (おうつ, おず) plus 1 corpus option from the top closeness tier. That tier is ≥3 and holds 129 words, including 音 おと (same length, same first kana).
    - Frequency: roughly 1 in 129 quizzes.
    - The audit itself flags this ("ATTESTED corpus readings: 音 (おと)"; "ATTESTED or too-few-candidate problems: 1").
  - Remedy:
    - Preferred: in the app, make ReadingOptions.build skip corpus readings that JMdict attests for the target's written form.
    - Otherwise: record it as an accepted known risk in the batch notes. The quiz answer おつ is unambiguous for this article's sense, and the incidence is low.
  - Evidence:
    - evidence\audits\word-quiz.txt:133–137
    - evidence\app-code\Words.kt:250–261
    - jmdict-families.xml entry 2837087
  - Confidence: high that it can be drawn. Medium on severity, because I did not verify whether the reading-quiz screen also shows the English meaning.

Optional:
- O1 — words/仁.md:20–21. The example sentence この本は、儒教の仁について書いています。 has an English line built on "This book writes about…", which is unnatural. Suggest "This book is about benevolence (仁) in Confucianism." or "This book discusses …".
- O2 — words/仁.md. JMdict 1369620 S4 "nucleolus" (biology) is not mentioned. This is acceptable for N1 scope, but a one-clause note beside the S3 "kernel" sense would complete the sense list. Not a defect.
- O3 — The 伯 reading-options "HIT は" line in mechanical-checks is a conservative over-report, because the fallback is never reached. A note in the tool output would spare later reviewers the check.

Limits:
- The 伎 card says "JMdict has no entry read わざおぎ". This is a whole-dictionary claim that the families file cannot prove, because it holds only entries containing 伎. A jisho.org search for わざおぎ returned no exact word match and split the query into わ + ざおぎ. That supports the claim, but jisho is not the pinned JMdict build. Confidence: medium-high.
- Glosses of entries outside the families file and digest rows I grepped were not checked against the pinned JMdict: 入念 1466670, 甲 1578730, 降参 1282860, 互角 1268820, 歌舞 1778760, 植林 1357390, 単独 1417780 and お疲れ様 1002570. 同伴者 1453280 "companion" was confirmed in jmdict-digest.tsv.
- I did not read the 仁 meaning tier (1413-way tie) line by line. I scanned it by English and kanji keyword, as I did the large 降伏, 伐採 and 同伴 tiers and the reverse pairs.
- I did not open repo\docs (content-format.md, confusable-words.md). Section order was judged by consistency across the 10 articles, together with lint and validate reporting 0 errors.
- I did not open WordQuizViewModel.kt, so I did not confirm whether the reading-quiz prompt shows the meaning (affects C1 severity).
- Known non-issues, not reported per the assignment: the 潜る lint warning, the JVM/Kotlin tests that were not run, localZipBytes jitter, the meta-scan fragments and the unlisted example words.
- Process: one tool call per response throughout; no parallel calls and no sub-agents. Several individual PowerShell calls combined multiple read-only commands, for example the packet listing and the diffs plus remark JSONs. Two keyword scans wrote oversized output to the tool's own temp file. I did not open those files; I reran with narrower filters.
