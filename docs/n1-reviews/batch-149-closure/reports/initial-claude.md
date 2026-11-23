# Batch 149: initial blind review (Claude)

## Snapshot

- Commit: 070b6f694216c7580346cc1b1432519b3284e919 (070b6f69), batch 149.
- New kanji cards: 翻 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華.
- Packet manifest sha256: 903d321fda8a6df1f46f014c26896a5516d78fc4ac37a5fd8f896882bc419c38.
- Reviewer model: Claude (Anthropic), an Opus-class model. The exact version string is not exposed to me.
- Role: the first of two blind reviewers. I worked read-only and alone.

## Scope

**Unit reviewed:**
- the 15 new cards in snapshot\kanji\;
- the 15 files in snapshot\strokes\;
- the 17 one-line word diffs in diffs\ and the matching snapshot\words\ articles.

**Deepest facets:** 1 (correctness) and 2 (scoped coverage). I checked every reading and every example word against public dictionaries: JMdict (from the packet), Digital Daijisen (the Weblio extracts) and live Kanjipedia pages. Facets 3 and 4 were covered for every card.

**Packet files opened:**

| File | How it was read |
| --- | --- |
| INSTRUCTIONS.md | In full. The report-contract section was re-read. |
| mechanical-checks.md | In full. |
| Packet root and evidence\ | Non-recursive directory listings only. |
| evidence\source-metadata.json | In full. |
| evidence\joyo-pages.md | In full, plus targeted re-reads of the 華 rows (p. 21) and of the 腐 舎 芽 脈 翼 芝 茂 興 舌 rows. |
| evidence\kanjipedia-outside-readings.json | In full. |
| evidence\daijisen-heads.txt | In full. |
| evidence\okurigana-scan.txt | In full. |
| evidence\kanjivg-components.txt | In full. |
| evidence\kanjidic2-records.xml | In part: extracts of the 15 records (meanings, nanori, readings, radicals). |
| evidence\jmdict-families.xml | In part: every entry id on the 15 Metadata lines, plus 1557640, 2261960 and the comparison entries named below. |
| evidence\jmdict-digest.tsv | In part: the header and family rows for 翼 脈 腐 臨 臭 興 舎 艶 芝 芽 茂 荘 華. |
| evidence\public-source\weblio-*.txt | 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華 in full. weblio-翻 was not opened. |
| evidence\app-code\QuizBuilder.kt | In full. |
| evidence\audits\ | Directory listing. |
| evidence\audits\quiz-safety.txt | In full. |
| evidence\audits\reading-exposure.txt | In part: the header, every "attested reading" line, the full 脈 臭 興 舌 sections, the last 30 lines and the totals. |
| evidence\audits\reading-options.txt | In part: the header, the start of the 翻 section, the 脈 section (lines 35-50), all HIT and section lines, and the last 8 lines. |
| diffs\ (all 17) | Hunk headers and all changed (+/-) lines. Unchanged context lines were not printed. |
| snapshot\kanji\ (all 15) | In full. |
| snapshot\strokes\ (all 15) | Parsed: schemaVersion, source, sourceRevision, strokeCount and the stroke-array length. Path data was not inspected. |
| snapshot\words\ (all 17) | In part: section headings and the wrapped link line of each. 芝居.md lines 1-32. |
| titles\kanji-titles.tsv | In part: filtered queries for every title quoted on the cards, every exclusion and distractor, and near-synonym patterns. |
| titles\word-titles.tsv | In part: grep. |
| repo\docs\content-format.md | In part: lines 86-154 and 108-122, plus a keyword grep. |
| repo\kanji\魅.md | Lines 1-16. |
| rubric\copilot-instructions.md | In part: a keyword grep and lines 96-125. |

Not opened:
- evidence\kanjivg-svgs.txt;
- evidence\audits\extra-readings.json, its scripts, kanji-remarks.json and word-remarks.json (their contents are echoed in the audit command lines and in mechanical-checks.md);
- weblio-翻.txt.

**Public web pages inspected:** live Kanjipedia pages for 臨 (0007216700), 臭 (0003114600), 興 (0002316200), 舌 (0004017300), 舎 (0002971600), 艶 (0000493300), 芝 (0002956700), 荘 (0004228100) and 華 (0000684000).

## Verdicts

### Overall

| Facet | Verdict | Findings |
| --- | --- | --- |
| Correctness | NEEDS FIX | C1, C4, C6 (all minor) |
| Scoped coverage | NEEDS FIX | C3, C4 (minor) |
| Consistency and quiz safety | NEEDS FIX | C2, C5 (minor); no quiz-ambiguity defect found |
| Comprehensibility | NEEDS FIX | C1, plus the unexplained jargon in C2 (minor) |

### Per file (facets in the order correctness / coverage / consistency and quiz safety / comprehensibility)

| File | Correctness | Coverage | Consistency and quiz safety | Comprehensibility |
| --- | --- | --- | --- | --- |
| 翻 | CLEAN | CLEAN | NEEDS FIX (C2: ハン label) | CLEAN |
| 翼 | NEEDS FIX (C6) | CLEAN | CLEAN | CLEAN |
| 脈 | CLEAN | CLEAN | CLEAN | CLEAN |
| 腐 | CLEAN | NEEDS FIX (C3) | NEEDS FIX (C2: くさ.す label) | CLEAN |
| 臨 | CLEAN | CLEAN | CLEAN | CLEAN |
| 臭 | CLEAN | CLEAN | CLEAN | CLEAN |
| 興 | CLEAN | CLEAN | CLEAN | CLEAN |
| 舌 | CLEAN | CLEAN | CLEAN | CLEAN |
| 舎 | CLEAN | CLEAN | NEEDS FIX (C5, weaker case) | CLEAN |
| 艶 | NEEDS FIX (C4) | NEEDS FIX (C4) | NEEDS FIX (C2: unlabelled non-Jōyō kun rows) | CLEAN |
| 芝 | CLEAN | CLEAN | NEEDS FIX (C5; C2: シ label) | CLEAN |
| 芽 | CLEAN | CLEAN | NEEDS FIX (C5; C2: めぐむ label) | CLEAN |
| 茂 | CLEAN | CLEAN | NEEDS FIX (C5) | CLEAN |
| 荘 | NEEDS FIX (C1) | CLEAN | NEEDS FIX (C5; C2: ショウ and チャン labels) | NEEDS FIX (C1) |
| 華 | CLEAN | CLEAN | NEEDS FIX (C5; C2: ゲ label) | CLEAN |
| 17 word diffs | CLEAN | CLEAN | CLEAN | CLEAN |
| 15 stroke files | CLEAN | CLEAN | CLEAN | CLEAN |

### What was verified

**Front matter.** On all 15 cards these match evidence\source-metadata.json and KANJIDIC2:
- grade tag, stroke count, radical and radical number;
- the order of the on and kun lists.

KANJIDIC2 files 舎 under radical 9 (人), which the card follows. Kanjipedia files it under 舌; that is not a defect.

**Quiz readings.** Every selected quiz reading has a Readings row linking a word article:

| Card | Quiz reading | Word article |
| --- | --- | --- |
| 翻 | ホン | 翻訳 |
| 翼 | つばさ | 翼 |
| 脈 | ミャク | 文脈 |
| 腐 | くさ.る | 腐る |
| 臨 | リン | 臨時 |
| 臭 | くさ.い | 臭い |
| 興 | キョウ | 興味 |
| 舌 | した | 舌 |
| 舎 | シャ | 校舎 |
| 艶 | つや | 艶 |
| 芝 | しば | 芝居 |
| 芽 | め | 芽 |
| 茂 | しげ.る | 茂る |
| 荘 | ソウ | 別荘 |
| 華 | カ | 豪華 |

For 芝, the official Jōyō table prints 芝居 under the しば row (joyo-pages.md:315), and 芝生（しばふ） as a special reading. The card's account of the two words is correct.

**Readings, glosses and source claims.** Every reading claim, every example word and every double-quoted gloss was checked against JMdict, Digital Daijisen, Kanjipedia, KANJIDIC2 and the Jōyō extracts. Except as stated in C1, C4 and C6, they are correct. Examples:
- 翻す / 翻る glosses;
- 興す sense 2 "to establish (e.g. a company)" (the basis of the 興/設 exclusion);
- the cherry-blossom sense of 花/華 はな in JMdict 1194500, which has no spelling restriction;
- 荘園 しょうえん/そうえん;
- the senses and name readings that Digital Daijisen gives for 華 (white powder, China, 華甲, は・はる, 華盛頓);
- Kanjipedia's outside readings (華: ゲ and しろい; 舎: セキ, いえ, やど, やどる, おく; 荘: ショウ, おごそか, しもやしき).

The statements on 臭 are correct:
- KANJIDIC2 lists fragrance, be fragrant, glow and be bright among its meanings.
- Kanjipedia gives only におい, くさい・いやなにおい and 悪いうわさ, so it records no glow or bright sense.
- The account that 臭い くさい establishes くさ.い, and that 臭い におい does not, is right.

**Mnemonics.** All 15 are labelled "Modern-shape mnemonic, not etymology". None makes a historical claim, and the titles they quote are exact. Every component, position and stroke statement agrees with kanjivg-components.txt:
- 翻 is 番 plus 羽.
- 翼 is 羽 over 異.
- 脈's right side is compared with 派.
- 興 has 同 in the middle, side pieces, a long horizontal stroke, then 八.
- 舌 is 千 over 口.
- 舎 is 人 + 士 + 口, 2 + 3 + 3 = 8 strokes.
- 艶 is 豊 (strokes 1-13) plus 色 (strokes 14-19).
- 芽 ends with 牙's ㇚ and ㇒.
- 茂 contains 戊, which contains 戈, the same as the right of 戦.
- 荘 contains 壮, whose right side is 士.
- 華 has four horizontals, two short verticals and a final long vertical under the 艹 crown: 3 + 4 + 2 + 1 = 10.

**Word diffs.** Each of the 17 diffs removes one line and adds one line. The only change is wrapping the bare kanji as `[X](../kanji/X.md)`, and every link points to the intended card. No diff touches a Dictionary: line, so the lint warnings on 校舎, 艶 and 翻訳 are unaffected. Every wrapped sentence still reads correctly in its "How the kanji combine" section.

**Stroke files.** All 15 cite KanjiVG revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc. In every file, strokeCount equals the length of the strokes array and the card's `strokes:` value (17 18 10 14 18 9 16 6 8 19 6 8 8 9 10).

**Reading audits, lead (l).** The accounting is correct. I checked the 脈 HIT label in detail:
- For prompt ミャク, the curated cards 目, 手 and 足 supply もく, ぼく, しゅ, ず and そく. They fill all three wrong slots in all 4 outcomes.
- The fallback tier, where ばく sits as a tier-3 candidate, is therefore never consulted. The 100-seed simulation saw only those 5 options.
- The label is an artifact of reading-options.txt scoring the fallback tiers without the curated fill. This is consistent with 0 production hits in reading-exposure.txt.

The 16 latent collisions are either KANJIDIC2 nanori (み さ もろ よし じ き む そ わ) or card-text readings (たすける ばく ことば おく めぐむ すぐれる げ). None is drawable in the N1, All or Starter-session pools, and no one-holder padded hit exists. Listed readings such as 興's コウ, おこる and おこす are protected by the app's full-reading filter (content-format.md:151).

## Findings

There are no blocker or major findings. All six findings are minor.

### C1: wrong description of the small っ in べっそう

- **Severity / facet:** minor; correctness and comprehensibility.
- **Location:** snapshot\kanji\荘.md:23.
- **Claim and impact:** the card says "the reading is ソウ for 荘 and the whole word has a small っ after ベツ". 別荘 is べっそう: ベツ loses its final ツ, which becomes the small っ (べ + っ + そう). A small っ placed after ベツ would give *べつっそう*. A beginner following the sentence literally would misread or misspell the quiz-evidence word.
- **Remedy:** "…the reading is ソウ for 荘; before it, ベツ shortens to べっ (its final ツ becomes a small っ): べっそう."
- **Evidence:** JMdict 1509970 reb べっそう. The card's own rows at lines 31 and 39 show べっそう.
- **Confidence:** high.

### C2: "source-only" is applied inconsistently and never explained

- **Severity / facet:** minor; consistency (facet 3) and comprehensibility (facet 4).
- **Locations:**
  - 翻.md:32
  - 翼.md:33
  - 脈.md:32-33 and 41
  - 腐.md:37 and 45
  - 舎.md:32-34
  - 艶.md:33-36
  - 芝.md:31
  - 芽.md:33
  - 荘.md:32-35
  - 華.md:34 and 43
- **Claim and impact:** the reading-type label has no stable meaning across the batch:
  1. **The stated reason varies.** On 翼:33, 脈:32-33, 舎:32-34 and 荘:34 the label rests on "no checked JMdict word example". The same label sits on rows that do cite a JMdict example:
     - 芝 シ: 芝蘭 2832743;
     - 芽 めぐむ: 芽ぐむ 1197720;
     - 荘 ショウ: 荘園 しょうえん 1402100;
     - 腐 くさ.す: 腐す;
     - 華 ゲ: 蓮華 1559210;
     - 翻 ハン: 2833260.
  2. **Two mahjong counters are labelled differently.** Both have JMdict entries, yet 翻 ハン is "on (source-only)" while 荘 チャン is "on, compound/counter only" (荘.md:33).
  3. **艶's non-Jōyō readings carry no label.** The Jōyō table gives 艶 only エン and つや. Its four further KANJIDIC2 kun readings (なま.めかしい, あで.やか, つや.めく, なま.めく) are labelled plain "kun", identical to つや. Equally non-Jōyō KANJIDIC2 kun readings on other cards (腐 くさ.す, 荘 ほうき) are labelled "source-only".
  4. **The label is spelled five ways:**
     - "kun (source-only)";
     - "kun, source-only";
     - "on, source-only compound reading";
     - "kun (source-only; Digital Daijisen and Kanjipedia)";
     - "on, compound/counter only".

  No card explains the term, which is jargon for an N5-N4 reader. A learner cannot tell whether a labelled reading is non-Jōyō, rare, or merely missing from the reviewed JMdict set. The rubric's "qualified source-only explanation" (rubric\copilot-instructions.md:108-109) presupposes one meaning. Quiz behaviour is unaffected: the quiz lists are correct.
- **Remedy:**
  - Pick one plain-English convention, for example "outside the Jōyō table; not quizzed", and put the reason in the row text.
  - Apply it uniformly, including 艶's four kun rows and 荘 チャン / 翻 ハン.
  - Optionally add a one-line gloss of the convention.
- **Evidence:** the Readings rows cited above; the joyo-pages.md rows; the KANJIDIC2 readings; the JMdict ids listed.
- **Confidence:** high that the label is inconsistent; medium on severity.

### C3: 豆腐 omitted from the 腐 card

- **Severity / facet:** minor; scoped coverage.
- **Location:** snapshot\kanji\腐.md:31 (the フ row) and the Common words section.
- **Claim and impact:** 豆腐 とうふ "tofu; bean curd" is in the reviewed 腐 family:
  - JMdict 1450070, priority ichi1, news1, nf14;
  - jmdict-digest.tsv.

  It is by far the most frequent word in which a learner meets 腐, and it shows フ (as ふ) in everyday vocabulary. It is also the natural contrast to the card's "rot; decay; spoil", because the word does not mean spoiled food. The card gives only 腐敗 for フ, plus 陳腐 in the prose, and never mentions 豆腐. A learner who already knows 豆腐 gets no help reconciling it with the title.
- **Remedy:** add 豆腐 とうふ, "tofu; bean curd" (JMdict 1450070), to the フ row or to Common words. Add one clause that the word does not mean spoiled tofu.
- **Evidence:** jmdict-digest.tsv row 腐/1450070; a search of 腐.md finds no 豆腐.
- **Confidence:** high that it is omitted; medium that it reaches "important".

### C4: 艶やか shown only as あでやか

- **Severity / facet:** minor; correctness and scoped coverage.
- **Location:** snapshot\kanji\艶.md:34 (also Notes line 51).
- **Claim and impact:** the あで.やか row presents 艶やか only as あでやか, "glamorous; fascinatingly elegant", and the card never mentions つややか. JMdict 2682080 records the same written form 艶やか read つややか, "glossy (e.g. hair); sleek; shiny; lustrous". That is the card's own title sense. JMdict 1177720 (あでやか) is marked as usually written in kana. A learner who meets 艶やかな髪 is led to the wrong reading and the wrong sense.
- **Remedy:** in the あで.やか row or the Notes, say: "The same spelling 艶やか is also read つややか, 'glossy (e.g. hair); sleek; shiny; lustrous' (JMdict 2682080); in the glamorous sense, あでやか is usually written in kana." Add 2682080 to the Metadata line.
- **Evidence:** jmdict-digest.tsv rows 艶/1177720 and 艶/2682080; the JMdict misc tag on 1177720 (checked in jmdict-families.xml).
- **Confidence:** high.

### C5: implausible Starter-level distractors on the 艹 cards (and 舎)

- **Severity / facet:** minor; consistency and quiz safety.
- **Location:** front-matter `distractors:` (line 13) and the Notes distractor sentence of:

  | Card | Title | Distractor options shown |
  | --- | --- | --- |
  | 芝 | turf; lawn | dog / stone / mountain |
  | 芽 | bud; sprout | dog / mountain / water |
  | 茂 | overgrown; lush | dog / mountain / water |
  | 荘 | villa; manor; solemn | dog / sun, day / rain |
  | 華 | flower; splendor; showiness | dog / moon, month / water |
  | 舎 (weaker case) | house; lodging; hut | rain / tree, wood / mountain |

- **Claim and impact:** content-format.md:106 requires "plausible wrong options", and :111 asks for three curated options. These are N5 pictograph titles with no semantic link to the targets:
  - 芽 and 茂 display an identical option set.
  - "dog" appears on 5 of the 15 cards, "mountain" on 4 and "water" on 4 (quiz-safety.txt).

  Every N1 learner knows these titles, so all three can be eliminated without knowing the target kanji. The meaning question on these cards then tests almost nothing, and the repetition teaches "dog is never right". This is not an ambiguity defect: every option is defensibly wrong in both directions, against both the displayed titles and their ordinary senses. The other cards use options from a related field, for example:
  - 翼: bird / fish / insect;
  - 舌: mouth / ear / foot;
  - 腐: bake / wash / boil.
- **Remedy:** replace one to three options per card with titles from the same field that are clearly different and not excluded. Examples:
  - for 芽, 茂, 芝 and 華: 葉 "leaf", 稲 "rice plant", 植 "plant; put in the ground", 株 "share; stump; rooted plant";
  - for 荘 and 舎: 村 "village".

  Then re-run the exclusion and quiz-safety checks.
- **Evidence:** quiz-safety.txt lines for the six cards; content-format.md:106 and :111-115; titles from kanji-titles.tsv.
- **Confidence:** medium. The rule is qualitative, and the choice may be a deliberate corpus convention.

### C6: double-quoted “help” on the 翼 card is not a real gloss

- **Severity / facet:** minor; correctness (the packet's double-quote rule).
- **Location:** snapshot\kanji\翼.md:33.
- **Claim and impact:** the row says "Kanjipedia and Digital Daijisen list “help”". Both sources are Japanese:
  - Digital Daijisen gives ［訓］つばさ たすける and sense ４「力を添えて助ける」(翼賛).
  - "help" is not a KANJIDIC2 meaning of 翼, which are wing, plane and flank.
  - It is not a JMdict gloss of a cited entry.

  The quoted English word is a translation, presented as if a source printed it. The learning impact is small, but the double-quoted gloss is not real.
- **Remedy:** "Kanjipedia and Digital Daijisen list the reading たすける (to help, as in 翼賛)", without quotation marks. Alternatively, quote the Japanese 助ける.
- **Evidence:** weblio-翼.txt; the KANJIDIC2 record for 翼.
- **Confidence:** high.

## Optional

These are not defects. They are polish suggestions and editorial preferences.

**O1. Author-facing wording in learner prose.**
- 臭.md:46: "Do not use the noun 臭い (におい) to justify that selection."
- 舎.md:44: "Do not use 田舎 (いなか) to justify a reading of 舎."

These are editorial instructions. Rephrase them as learner guidance, for example "臭い read におい is the noun 'smell'; the quiz uses くさい."

**O2. 艶.md:51, "JMdict confirms both readings of 艶めく, with different senses".** The senses overlap. JMdict 1177700 つやめく sense 2 is "to look alluring; to be sexy; to be seductive", which is close to なまめく (2708210). The つや.めく row (line 35) shows only "be glossy; glisten". Consider "with overlapping senses" and add the alluring sense to the row.

**O3. Possible exclusions, all low risk.** Each pair could only meet through another card's fallback, because these cards' curated distractors fill 3/3.
- 腐/甘: "spoil" in 腐's title against 甘 "sweet; pamper". This is the same English-homograph logic the batch already uses for 臨/顔 "face" and 艶/符 "charm".
- 腐/傷: "damage"; 傷む also means to go bad.
- 興/復: "revival" against "restore; repeat".
- 茂/豊: "lush" against "bountiful; abundant".

**O4. Weak but harmless exclusions.** The pairs judged one by one are otherwise direct and do not form a clique.
- 臨/写 rests only on the copying sense (臨写/臨書), which the displayed title "face (a situation); attend" does not carry.
- 脈/糸 and 興/昇 are loose.

Keeping these exclusions only removes options, so they need no change. The other pairs named in the leads are justified by displayed or ordinary senses:
- 艶/符 (KANJIDIC2 lists "charm" for 艶);
- 臨/冒 ("brave danger" against "face");
- 翻/波 and 翻/飛 (KANJIDIC2 "wave"; JMdict 翻る "to fly");
- 興/設 (興す "to establish");
- 興/起 (Jōyō prints 興る ⇔ 起こる and 興す ⇔ 起こす).

**O5. Coverage extras.** These are words that appear as Jōyō examples or are common in the family; they are not required.
- 脈: 山脈, 動脈 (Jōyō examples; ichi1), 静脈.
- 華: 華やか (ichi1; the Jōyō はな example, which would show はな better than standalone 華 はな), 中華 (ichi1).
- 芽: 芽生える and 新芽 (Jōyō examples).
- 茂: 茂み (a Jōyō example) and 生い茂る.
- 艶: 色艶 (a Jōyō example) and 艶々.

**O6. Metadata ids with no matching word on the card.**
- 脈.md:47 lists 1528470 (脈絡).
- 臨.md:44 lists 1555640 (臨床).

Neither word appears in the card text. Name the words or drop the ids.

**O7. Formatting consistency.** The Metadata line comes in three formats:
- 翻 翼 脈 腐 臨: `[KANJIDIC2](…); [JMdict](…), entries …; [Jōyō…]`;
- 臭 興 舌 舎 艶: `[KANJIDIC2](…), [JMdict](…wiki…)`;
- 芝 芽 茂 荘 華: `[KANJIDIC2](…), 2026-11-02 snapshot. JMdict entries …`.

The Notes on 芝 芽 茂 荘 華 are bullet lists, while the other cards use prose. content-format.md sets no rule; harmonizing would still help.

**O8. 脈.md:32, "KANJIDIC2 and Kanjipedia record this outside the Jōyō readings".** KANJIDIC2 has no Jōyō marking per reading; it simply lists すじ. Attribute the "outside" marking only to the source that prints it.

**O9. The 華 and 翻 Notes paragraphs that justify the exclusions** (for example the ten-card paragraph in 華's Notes) are dense for an N5-N4 phone reader. Consider shortening them or moving the rationale to the editorial evidence.

**O10. 興: the Jōyō contrast.** One clause could explain the 興る/起こる and 興す/起こす contrast that the Jōyō table prints with ⇔, for example: 興 is for rising or reviving enterprises; 起 is for physical rising and events.

**O11. 芝居.md:27 (a word article; the passage was pre-existing).** It quotes 芝 as "grass; turf" and now links to the card titled "turf; lawn". Aligning the quote with the title would avoid an apparent mismatch.

**O12. 脈's ばく option is safe but fragile.** ばく is safe only because 目, 手 and 足 always fill the three slots. If a curated option is ever removed or excluded, the tier-3 fallback could offer ばく (Kanjipedia's outside reading バク). Keep this in mind for any later edit.

## Limits

- **Joyo p. 157 extract:** the extract (cited by 臨) is truncated, and the 臨 rows are not visible. I verified the readings リン and のぞむ through KANJIDIC2, the Weblio Daijisen extract and the live Kanjipedia page.
- **翻:** weblio-翻.txt was not opened. 翻's Jōyō rows (p. 144), its KANJIDIC2 readings, the Kanjipedia outside reading ハン and every JMdict gloss it quotes were checked. The card cites Digital Daijisen only on its Metadata line.
- **Mnemonics:** I checked the stroke and component statements against kanjivg-components.txt only. I did not open the raw SVGs (kanjivg-svgs.txt) or the stroke path data.
- **Word articles:** read only around the changed line (headings, the link line, and 芝居 lines 1-32). Each diff changes exactly one line, so I treated the rest as out of scope.
- **Not run (known packet limit):** the JVM content tests and the Kotlin reading cross-check.
- **Live web pages** (Kanjipedia) may differ from the pinned packet data. Where I relied on them, they agreed with the packet.
- **Assumptions:**
  - "Plausible" in content-format.md:106 means semantically related enough to require knowledge of the target. C5 rests on this reading.
  - I took the batch's intended meaning of "source-only" to be "outside the Jōyō table and not quizzed". C2 reports the deviations from any single meaning.
- **Tool use:** exactly one tool call per response throughout. No parallel calls, sub-agents, recursive listings or corpus scans. Title checks used titles\*.tsv. The only file written is this report.
