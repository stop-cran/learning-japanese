# Batch 149 confirmation review (Claude)

**Model:** Claude (Anthropic), an Opus-class model. The exact version string is not exposed to me.

## Snapshot

- **Revised snapshot under review:** 06b2db87bfd9f516f313f63101c40f1fe724f40f
- **Snapshot from my first round:** 070b6f694216c7580346cc1b1432519b3284e919

## Scope

I read the following:

- **Packet files, in full:** INSTRUCTIONS.md, CHANGES.md, RESPONSE.md, evidence\README.md, diffs\fix.patch, checks\quiz-safety.txt, checks\reading-options.txt.
- **My first-round report:** reports-149\initial-claude.md, in full.
- **All 15 revised cards, in full:** 翻 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華.
- **Changed word articles:** the changed hunks of words\艶.md and words\芝居.md, plus the surrounding context of words\艶.md.
- **App sources:** evidence\QuizBuilder.kt and evidence\KanjiReadings.kt, in full.
- **checks\reading-exposure.txt:** the header and the sections for 翻, 翼, 舎, 艶, 芝, 芽, 茂, 荘 and 華, plus the totals.
- **checks\link-targets.tsv:** the header, the first rows, and a search for failure markers.
- **Every cited JMdict entry** in evidence\jmdict-cited-entries.xml.
- **The KANJIDIC2 records** for 興 茂 腐 脈 翻 舎, taken from the original packet's evidence.

Every changed hunk was checked against all four facets: meaning, readings, words and examples, and quiz safety.

## Dispositions

- **C1 — RESOLVED.** 荘.md:23 now gives 別荘 べっそう as ベツ + ソウ, with the ツ of 別 becoming a small っ. This is correct, and the link target 別荘 exists.
- **C2 — RESOLVED.** Source labels in the reading tables now follow one convention:
  - "source-only here" marks only rows that have no JMdict example (翼, 脈, 舎, 荘).
  - Rows backed by a JMdict word carry plain "on" or "kun" (翻 ハン, 芝 シ, 芽 めぐむ, 荘 ショウ and チャン, 腐 くさ.す, 華 ケ and ゲ).
  - Each 艶 row states whether it is selected for questions.
  - Two small wording leftovers are listed under Optional.
- **C3 — RESOLVED.** 腐 now uses 豆腐 (JMdict 1450070, "tofu; bean curd") in the フ row and in Common words, and the id is on the Metadata line.
  - 腐敗 ふはい — "decomposition; putrefaction; corruption" is an accurate selection from JMdict 1497870, which spans senses 1 and 2.
  - The author declined my extra tofu clause; that decline is acceptable.
- **C4 — RESOLVED.** 艶 now gives 艶やか つややか — "glossy; sleek; lustrous", a faithful subset of JMdict 2682080 ("glossy (e.g. hair); sleek; shiny; lustrous").
  - The あでやか rows say "usually written in kana". This matches the {word usually written using kana alone} tag on JMdict 1177720.
  - 2682080 is on the Metadata line.
- **C5 — RESOLVED.** The new distractor sets are 芝 田木花, 芽 木土雨, 茂 山川土, 荘 校駅海, 華 月天川 and 舎 道京雨.
  - 犬 is gone, and 芽 and 茂 no longer share a set.
  - None of the 18 option titles can be defended as a correct meaning for its target.
  - quiz-safety.txt reports 3/3 curated meaning options on all 15 cards, with 0 errors and 0 warnings.
  - The section "Quiz options after the fix" below gives my own reasoning from the app source.
- **C6 — RESOLVED.** 翼:33 now reads "list this reading, meaning to help". The misleading quoted English word is gone, and たす.ける stays marked as source-only.
- **O1 — RESOLVED.** 臭:46 and 舎:44 are reworded, and the "Do not merge" sentence in 荘 is deleted. The remaining text is accurate.
- **O2 — RESOLVED.** 艶:35 and 艶:52 now name the overlapping senses: gloss or charm for つや versus showy elegance for あでやか, and sexy or captivating for なまめかしい / なまめく. This is consistent with JMdict 1177680, 1177720, 1177690 and 2708210.
- **O3 — RESOLVED.** The quiz_exclusions now read:
  - 腐: [酸, 甘, 傷]
  - 興: adds 復
  - 茂: [密, 盛, 豊]

  The stated grounds are verified:
  - 甘やかす "to pamper; to spoil" (1213470).
  - 傷む "to be spoiled (e.g. food)" (1432710, sense 2).
  - KANJIDIC2 lists "revive" for 興.
  - 茂る "to grow thickly; … to luxuriate; to be luxurious" (1533740), and KANJIDIC2 "grow thick" and "be luxuriant" for 茂.
  - No exclusion overlaps a curated distractor.
- **O4 — ACCEPTED (declined).** The author's reason holds; nothing in the card is wrong.
- **O5 — RESOLVED.** The new words are:
  - 山脈 "mountain range" (1303190)
  - 動脈 "artery" (1451580)
  - 華やか "bright and beautiful; gorgeous; showy…" (1600990)

  The glosses and ids match JMdict.
- **O6 — RESOLVED.** 脈絡 is named on 脈 (1528470, "logical connection…"), and 臨床 is added to 臨 as "clinical (e.g. trial)". That gloss is a faithful shortening of 1555640, "clinical (e.g. pathology, training, trial)".
- **O7 — ACCEPTED (declined).** content-format defines no Metadata field for this, so the decline is correct.
- **O8 — RESOLVED.** 脈:32 and 翻:42 now attribute the "outside the Jōyō readings" marking only to Kanjipedia.
- **O9 — RESOLVED.** The exclusion notes on 華 翻 舎 荘 臨 艶 are now bullets. Their content is the same as the old paragraphs.
- **O10 — ACCEPTED (declined).** This was optional polish, and leaving it out introduces no defect.
- **O11 — RESOLVED.** 芝居.md:27 now quotes "turf; lawn," consistently.
- **O12 — ACCEPTED (noted).** This was informational only; 脈's distractors 目 手 足 are unchanged and still valid.

## Quiz options after the fix

This section is my own reasoning from QuizBuilder.kt and KanjiReadings.kt, cross-checked with the audits.

**Meaning mode.** Curated distractors are taken first. A pair is dropped if either card lists the other in quiz_exclusions, and titles must be unique.

- 芝 (turf; lawn) shows rice field / tree, wood / flower.
- 芽 (bud; sprout) shows tree, wood / earth, soil / rain.
- 茂 (overgrown; lush) shows mountain / river / earth, soil.
- 荘 (villa; manor; solemn) shows school / station / sea, ocean.
- 華 (flower; splendor; showiness) shows moon, month / heaven, sky / river.
- 舎 (house; lodging; hut) shows road, way / capital / rain.

None of these collides with its target. The pairs closest in meaning are 華 and 花 (not used) and 芝 with 花 ("flower" is not "lawn"); neither is a defensible correct answer. The new exclusions (腐 酸甘傷, 興 復, 茂 密盛豊) remove only fallback candidates and leave the curated sets intact. The other nine cards' meaning options are unchanged from the first round and still pass.

**Reading mode.** Each curated card contributes one reading of the prompted kind. The excluded keys are the target's readings plus their mutations.

| Card | Prompt | Distractor readings |
| --- | --- | --- |
| 荘 | ソウ | 校 コウ/キョウ, 駅 エキ, 海 カイ |
| 舎 | シャ | 道 ドウ/トウ, 京 キョウ/ケイ/キン, 雨 ウ |
| 華 | カ | 月 ゲツ/ガツ, 天 テン, 川 セン |
| 芝 | しば | 田 た, 木 き/こ, 花 はな |
| 芽 | め | 木 き/こ, 土 つち, 雨 あめ/あま/さめ |
| 茂 | しげる | 山 やま, 川 かわ, 土 つち |

- No option equals the target's reading or its voiced, long-vowel or small-っ form. For 華, ゲツ and ガツ are not the excluded keys げ or が.
- Every distractor card holds a reading of the prompted kind, and each set holds three distinct readings, so the curated cards fill all three slots in every outcome.
- reading-exposure.txt agrees for the N1 stack, the All stack and the Starter practice session.
- Replacing 京 with 駅 on 荘 removes the earlier キョウ/キョウ overlap with 校, which could leave a slot open. As a result, the KANJIDIC2 name-only reading そ, which reading-options.txt still lists as "info (can be drawn)" in the full-pool fallback tiers, is now never reached in any shipped pool: the curated cards always fill all three slots.
- The only "problem" in reading-options.txt is 脈's ばく. It was present in the first round and is unchanged by this fix, and the card documents it as a source-only reading.

## Findings

No new findings. Checking every changed hunk against the four facets found no regressions.

## Optional

- **Label spelling.** 腐:33 now spells the label "kun suffix", while the unchanged 臭:33 spells it "kun (suffix)". Pick one spelling.
- **Mixed wording in 腐.** The 腐 reading rows mix "not selected" and "not selected for questions here". Unifying them would match 艶's rows.
- **Weak distractors.** 舎's 雨 (rain) and 華's set 月 天 川 are valid but weak as distractors. Place or flower fields such as 家-like or 草-like starter cards would be more plausible. This is cosmetic only.

## What the audits cannot show

- **Live app behaviour.** The audits reimplement the selection logic in Python. They do not run the Kotlin code on Android or the JVM, so RNG and order effects are modelled, not observed.
- **ReadingOptions.mutations.** The audits assume this list is complete; I did not verify Words.kt.
- **Content outside the pools.** The audits cover only the shipped pools: the N1 stack, the All stack, and the Starter practice session. Future content, or custom smaller pools (the "risk class" lines), could still surface latent name-only readings such as 荘 そ or 舎 さ.
- **Distractor plausibility.** Whether a distractor is a good teaching choice is outside what the audits measure.

## Limits

- **Parallel tool calls:** in one response I issued TWO tool calls in parallel: a view of initial-claude.md lines 330–380 and a powershell listing of the packet's evidence, checks, diffs and snapshot folders. Every other response used exactly one call.
- **Tests:** no JVM or Android tests were run, because no JDK was available.
- **reading-exposure.txt:** I did not read the sections for 脈, 腐, 臨, 臭, 興 and 舌 in this round. Those cards' distractors are unchanged, and the file's totals show 0 production hits.
- **checks\link-targets.tsv:** I read only the header and the first rows, and searched the 26 rows for missing or broken markers; there were none. I did not inspect every row.
- **Words.kt:** not read.
- **Web sources:** no public web sources were needed. Every gloss check was made against the JMdict and KANJIDIC2 extracts in the packets.
- **Other material:** I did not consult the other reviewer's report or any author material beyond the packet.

## Verdicts

- **Meaning:** PASS
- **Readings:** PASS
- **Words and examples:** PASS
- **Quiz safety:** PASS

## Confirmation

**CONFIRMED.** All of C1–C6 are resolved. The O1–O12 dispositions are accepted or resolved, and the fix introduces no new defects.
