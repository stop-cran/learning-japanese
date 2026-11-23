# Batch 136: first blind review (Claude)

Reviewer model: Claude (Anthropic model family). This is the first of two blind reviews.

## Snapshot

- Commit: 420a6669a2f1dafcc3a237e8b8604ff8cbc4201e (batch 136).
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-136-420a6669`. The packet-manifest.json sha256 given in the task is 440ba2029aafbef24a1be4e90195bb8c673691fec29b8df228a0e963b6b7df58; I did not re-hash it.
- Unit under review:
  - the 15 new cards in `snapshot\kanji\` (炊 焦 異 端 筋 粗 納 脱 膨 致 請 透 鉢 隔 駄);
  - the 15 files in `snapshot\strokes\`;
  - the 34 one-line diffs in `diffs\` to existing word articles.

## Scope

Packet files I opened, and how much of each I read:

| File | Read |
| --- | --- |
| `INSTRUCTIONS.md` | in full |
| `mechanical-checks.md` | in full |
| `evidence\source-metadata.json` | in full |
| `evidence\joyo-pages.md` | in full |
| `evidence\daijisen-heads.txt` | in full |
| `evidence\kanjipedia-outside-readings.json` | in full |
| `evidence\audits\reading-options.txt` | in full (330 lines) |
| `evidence\audits\quiz-safety.txt` | in part: the head, plus a grep for errors, warnings and the per-kanji lines (58 lines; 0 errors, 0 warnings) |
| `evidence\audits\reading-exposure.txt` | in part: the head, the summary lines and every "attested reading ... offered by" line |
| `evidence\kanjidic2-records.xml` | in full, through a script (grade, strokes, radical, on, kun, nanori, meanings) |
| `evidence\jmdict-families.xml` | in part: every entry cited by the 15 cards, extracted by ent_seq |
| `evidence\jmdict-digest.tsv` | in part: targeted rows |
| `evidence\public-source\weblio-*.txt` (all 15) | in part: the character entry and the leading headwords of each |
| `snapshot\kanji\*.md` (15) | in full |
| `snapshot\strokes\*` (15) | in full, through a script (strokeCount and the length of the stroke array) |
| `diffs\*` (34) | in full: the changed lines and their context |
| `titles\kanji-titles.tsv` | in full, through a script |
| `repo\docs\content-format.md` | in part: lines 71-139 (Kanji card, Quiz authoring, Curated reading questions), plus a grep for headings |
| `repo\kanji\` 線 且 起 初 吹 八 | in part: the front-matter and reading lines |
| `rubric\copilot-instructions.md` | in part: a grep only |

I also took non-recursive listings of the packet's top level and its subfolders.

Not opened:
- `evidence\okurigana-scan.txt`
- `evidence\app-code\`
- `titles\word-titles.tsv`
- the full text of the 34 word articles; I read only their diff hunks.

Public web source: Weblio Digital Daijisen, the 致す page, which confirms the headwords おこ・す and おく・す 【▽遣す／▽致す】 with the meaning よこす.

## Verdicts

| Facet | Overall | Cards that differ |
| --- | --- | --- |
| 1. Correctness | CLEAN, with one minor defect | 炊: NEEDS FIX (C1) |
| 2. Scoped coverage | CLEAN | none; optional notes for 駄, 膨, 端, 納 and 粗 |
| 3. Consistency and quiz safety | CLEAN | none |
| 4. Comprehensibility | CLEAN | none |

- Stroke files: CLEAN. Each strokeCount and stroke-array length equals the card's stroke count: 炊 8, 焦 12, 異 11, 端 14, 筋 12, 粗 11, 納 10, 脱 11, 膨 16, 致 10, 請 15, 透 10, 鉢 13, 隔 13, 駄 14.
- The 34 diffs: CLEAN. Each changes exactly one line and wraps a bare mention of the new kanji as `[X](../kanji/X.md)`. Every target is the right kanji card, nothing else changes, and every passage still reads correctly.

What I verified for every card:
- **Front matter** against source-metadata.json and KANJIDIC2: grade, strokes, radical, on and kun lists, quizOnyomi and quizKunyomi.
  - The grade-6 tags on 異, 筋 and 納 and the grade-8 tags on the other twelve match KANJIDIC2.
- **Titles:** all 196 double-quoted card titles in the 15 cards match kanji-titles.tsv exactly, and no two titles are duplicates.
- **Glosses:** every quoted JMdict gloss matches the cited entry in jmdict-families.xml. Quotes that are prefixes of a longer gloss are accurate, not invented.
- **Official Joyo table:** every claim about it matches joyo-pages.md (rows, examples, bracketed forms, appendix). This includes:
  - 駄 has only a ダ row, with no タ row;
  - 請 has no ショウ row.
- **Daijisen claims** match the weblio extracts and daijisen-heads.txt. This includes:
  - the five タン senses of 端 and its kun groups はし, は and はた;
  - 請 セイ (漢), シン (唐), ショウ (呉);
  - 鉢 ハチ (呉), ハツ (漢);
  - タ for the footwear words of 駄;
  - the senses of 致 and the headwords おこす and おくす.
- **Mnemonics:** every card labels its mnemonic as modern-shape and makes no historical claim. Every component and stroke statement I checked is true:
  - 秀 is 禾 over 乃;
  - 鉢 is 金 + 本;
  - 室 and 倒 contain 至;
  - 端 has 立 at the left and 山 at the top right.
- **Readings cited from other cards** are confirmed by the repo cards:
  - 線 すじ;
  - 且 ショ, ソ, ショウ;
  - 起 お.こす;
  - 初 はじ.め;
  - 吹 スイ;
  - 八 ハチ, ハツ.
- **Quiz readings:** each quizOnyomi and quizKunyomi reading has a Readings row with a linked word.
- **Section order and headings** follow content-format.md.

## Findings

### C1: 炊く's dialect sense is presented as general Japanese (minor; facet 1)

- **Location:** `snapshot\kanji\炊.md`, line 23, and the Notes at line 50.
- **What the card says:**
  - Line 23: "JMdict glosses the verb 炊く 'to cook (grains, e.g. rice)' and, in a second sense, 'to boil; to simmer; to stew; to seethe.'"
  - Line 50 uses the same sense to justify excluding 沸: "JMdict's 炊く also has 'to seethe.'"
- **What JMdict says:** in the pinned entry 1596830, sense 2 is tagged as Kansai-ben dialect and cross-references 煮る. Sense 3 is internet slang for "to get angry."
- **Impact:** an English-speaking learner will take "boil; simmer; stew" as an ordinary meaning of 炊く. In standard Japanese it means cooking rice or grains; the wider "simmer" use is regional, mainly Kansai. The quote is accurate, but leaving out the register tag misdescribes the sense. The 沸 exclusion itself is harmless and can stay.
- **Remedy:** label the second sense as Kansai dialect, for example: "and, in Kansai dialect, 'to boil; to simmer; to stew' (standard Japanese uses 煮る)." Adjust the wording at line 50 to match.
- **Evidence:** the `jmdict-families.xml` entry 1596830 (sense 2 carries the dialect tag ksb and the xref 煮る); line 23 of the card.
- **Confidence:** high.

No other established defects.

## Optional

These are polish and design remarks, not defects.

### Coverage and readings

- **O1, 駄:**
  - The only quizzed on-reading is タ. That reading is outside the official table and limited to footwear words such as 下駄 and 雪駄.
  - The main reading ダ is not quizzed because its only word article, 無駄, is an ateji spelling.
  - The card is open about this, and content-format.md allows it.
  - The card could also mention:
    - the outside readings the evidence records: Kanjipedia の.せる, and the Daijisen kun reading においうま shown in the weblio extract;
    - a ダ example that is not ateji, such as 駄作 or 駄菓子 (both are examples in the official table).
- **O2, 膨:** the card does not mention Kanjipedia's outside readings ホウ and ふくよか. The cards for 炊, 粗, 納 and 脱 do mention theirs (かしぐ, ほぼ, いれる, タツ), so a one-line note would keep the cards consistent.
- **O3, 端:**
  - The はた row's example 端から はたから ("from outside", usually kana) is weak. The card itself quotes Daijisen's 道端, and 井戸端 or 炉端 would be clearer examples of はた/ばた.
  - The card does not mention はした (in the Daijisen kun list and in Kanjipedia) or the name reading はじめ. A one-line mention would explain why はじめ can appear as a wrong option on the はし prompt (see O8).
- **O4, 納:**
  - ノウ, the main reading (納入, 収納), has no word article, so the quizzed on-reading is ナッ through 納得.
  - The card's account of ノウ, ナ, ナン and トウ is accurate and openly qualified; I found no defect.
  - A ノウ word article would let ノウ be quizzed later.
- **O5, 粗:**
  - The noun 粗 あら ("flaw; fault") is listed under the あら.い row, while the あら- row says "no word article yet."
  - JMdict 1586730 combines the noun and prefix senses, gives fish bones (アラ) as sense 1 and marks the noun as usually written in kana.
  - Line 42 explains the relationship, but a note that the noun is usually written in kana would help a learner.
- **O6, 炊:** the 雑炊 quote is a shortened prefix of its JMdict gloss. It is accurate; consider ending it with an ellipsis or quoting the full gloss.

### Quiz design

- **O7, 脱 and 致 distractors:**
  - The distractors are 飲 読 聞 for 脱 and 話 買 学 for 致. They are semantically distinct, plausible English verb labels, and none overlaps either card's displayed title or ordinary secondary senses, in either direction. So they are acceptable meaning-quiz distractors.
  - As look-alikes they are weak. For 脱, look-alikes such as 説, 税 or 鋭 exist, which would make harder reading-quiz options.
- **O8, reading-audit HITs:**
  - The two HITs are はじめ on 端's はし prompt (taken from 初) and おこす on 致's いたす prompt (taken from 起). Both are defensibly wrong:
    - はじめ is only a name reading of 端 (Daijisen 名のり) and an outside reading in Kanjipedia;
    - おこす is an archaic Daijisen headword that the 致 card itself explains.
  - The 致 card's Notes say that none of 話, 買 and 学 is read おこす. That is true, but the reading quiz's fallback pool could still show 起's おこす. Saying so would make the card fully transparent.
- **O9, 炊 and 鉢 options:**
  - The distractors 吹 (also read スイ) and 八 (also read ハチ/ハツ) are skipped as excluded keys, so the curated slots fall back safely.
  - い is a KANJIDIC2 name-only reading of 炊. reading-exposure.txt says it can be offered on the スイ prompt (through 以 and others; 11 of 100 seeds). An on-reading prompt asks for スイ, so い is a defensible wrong answer; low risk.
- **O10, quiz_exclusions:** every pair raised in lead (g) has real overlap with a displayed title or an ordinary sense:
  - 異 with 差 ("difference") and 変 ("strange");
  - 端 with 刃 ("blade; cutting edge") and 梢 ("branch tip");
  - 筋 with 系 and 統 ("lineage") and 理 ("reason");
  - 請 with 企 and 就 ("undertake") and 問;
  - 致 with 因 ("cause") and 及 ("reach");
  - 膨 with 太 (KANJIDIC2 "get fat");
  - 駄 with 履 (footwear) and 劣;
  - 隔 with 挟 ("hold between");
  - 透 with 明 ("clear").

  They are direct pairs, not transitive cliques. Some are generous, but generous exclusions only remove options, so none is a defect.

### Diffs

- **O11, 鉢 article:** the wrap gives "[鉢](../kanji/鉢.md)多羅 はったら", so the link splits the word 鉢多羅 next to its transcription. It is correct as a first-mention link, but linking an earlier stand-alone 鉢, if there is one, would read more cleanly.

## Limits

- **Model:** Claude (Anthropic).
- **Tool calls:** every response contained exactly one tool call; I am not aware of having issued parallel calls. I used no sub-agents, background jobs, other sessions or recursive scans.
- **Diffs:** I read only the diff hunks, not the full word articles. "First mention" is verified within each diff's context, not across each whole article.
- **Reading audits disagree on drawability:**
  - reading-options.txt says the HITs はじめ (端) and おこす (致) can be drawn through the full-pool fallback (about 4 to 6 of 100 seeds).
  - reading-exposure.txt, which models the production pools, reports 0 production hits and 17 latent collisions, plus the い name reading of 炊.
  - I did not read evidence\app-code\ to settle which model is right. I judged every one of these readings defensibly wrong on the merits, so the disagreement does not change my verdict.
- **Web checks:** I checked one live page (Weblio Daijisen 致す). Other Daijisen claims were checked against the packet's weblio extracts, which I assume reflect the live pages. JMdict claims were checked against the pinned jmdict-families.xml, which may differ slightly from the online JMdict.
- **Not run:** the Android JVM content tests and the Kotlin cross-check of the reading audit; this is a known limit of the packet.
- **Membership:** batch membership and community-list JLPT levels were not reviewed. For example, KANJIDIC2 gives 異 the old JLPT level 2.
- **Assumption:** the coverage rule requires rows only for readings in the metadata (source-metadata.json and KANJIDIC2). So readings found only in Daijisen or Kanjipedia (for example 駄 においうま or 膨 ホウ) are treated as optional notes, not defects.
