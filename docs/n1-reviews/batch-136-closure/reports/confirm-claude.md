Snapshot: commit 7a525b065ee613535c71d559bfc4ce0aea00beb1 (child of the reviewed snapshot 420a6669). Reviewer: Claude (Anthropic model family). This is the confirmation round of my initial report.

Scope:

| File | How deeply |
| --- | --- |
| confirm packet: `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md` | in full |
| `diffs\fix.patch` | in full |
| `evidence\README.md`, `evidence\jmdict-cited-entries.xml` (all 6 entries), `evidence\QuizBuilder.kt` | in full |
| `evidence\KanjiReadings.kt` | lines 1-200: the reading-quiz builder and queue |
| `evidence\kanjivg\09759.svg` | element and position lines only |
| `evidence\Words.kt` | not opened; the mutation list was not needed |
| `checks\link-targets.tsv`, `checks\quiz-safety.txt` | in full |
| `checks\reading-exposure.txt` | in part: line 1 and lines 10-22, 92-110, 246-256, 355-364 |
| `checks\reading-options.txt` | in part: line 1 and lines 86-99, 224-234, 326-330 |
| revised `snapshot\kanji\` 炊 端 粗 請 駄 and `snapshot\words\透明.md` | in full |

The other checks files (`lint.txt`, `unittest.txt`, `validate.txt`, `budget.txt`, `vocabulary.txt`, `manifest.txt`) were not opened; I rely on CHANGES.md's summary of them.

I also compared both reading audits and quiz-safety.txt line by line with the original packet's `evidence\audits\` copies. From the original packet I read:
- line 6 of `evidence\public-source\weblio-` for 膨, 駄, 納, 炊, 粗 and 脱 (the Daijisen character entry), plus a grep of weblio-膨 for ホウ;
- a count of においうま, 荷負い馬 and はした in `jmdict-families.xml` and `jmdict-digest.tsv`.

From my own earlier work I reused:
- `reports-136\initial-claude.md`, which was this session's own output;
- the line 6 of weblio-端 that I read earlier in this session.

Public web: I re-read Weblio Daijisen 致す (おこす and おくす headwords). A jisho.org search for においうま was attempted; it only redirected to におい, so it proved nothing.

Dispositions:
- **C1 - RESOLVED.**
  - `炊.md:23` now says JMdict marks the second sense as Kansai dialect and names standard 煮る にる. `炊.md:50` now says "the Kansai-dialect sense of 炊く."
  - Pinned JMdict 1596830 sense 2 carries `<dial>Kansai-ben</dial>` and `<xref>煮る</xref>`. Entry 1322540 is 煮る にる, "to boil; to simmer; to stew; to seethe."
  - The 煮る link resolves (link-targets.tsv), and 1322540 was added to line 52. The 沸, 飯, 蒸 exclusion is kept.
  - Nothing else in the card body presents a general "boil" sense for the verb. The kanji title "cook rice; boil" is unchanged; see Optional.
- **O1 - RESOLVED.**
  - `駄.md:31` adds the Daijisen kun reading においうま, confirmed by line 6 of weblio-駄 (［訓］ においうま).
  - "No JMdict entry has" it: the pinned 駄 family (jmdict-families.xml, jmdict-digest.tsv) contains neither においうま nor 荷負い馬.
  - Not adding Kanjipedia の.せる is consistent with the stated Daijisen-based rule, and Daijisen does not list it.
  - My suggestion of non-ateji ダ examples was already met: 駄作 (l.29), 駄菓子 (l.31) and 駄目 (l.39).
- **O2 - DECLINE ACCEPTED.**
  - Line 6 of weblio-膨 shows Daijisen ［音］ ボウ（慣） and ［訓］ ふくらむ ふくれる only. ホウ appears only in the Wiktionary block, marked 表外.
  - The author's premise correction is right: Daijisen itself lists 炊 かしぐ, 粗 ほぼ and 納 いれる. So only 脱 タツ was a Kanjipedia-sourced mention, and my O2 comparison misattributed the source.
  - JMdict 1011000 has 膨よか only as a rarely used kanji form of ふくよか.
- **O3 - RESOLVED.**
  - `端.md:33` adds はした. This matches line 6 of weblio-端 (［訓］ はし は はた はした, with word groups only for はし, は and はた). JMdict 2590770 is 端 / 端た はした, sense 1 "fraction; odd sum"; it is added to l.65.
  - Declining the はた example is correct: 井戸端 and 炉端 are read ばた and belong under the existing -ばた row, which has 道端. My suggestion was misplaced.
  - Not adding はじめ is acceptable: it is only a Daijisen ［名のり］ name reading and a Kanjipedia outside reading.
- **O4 - DECLINE ACCEPTED.** I raised no defect. The card's account of ノウ, ナ, ナン and トウ matches Daijisen (line 6 of weblio-納). Adding a ノウ word article is new scope.
- **O5 - RESOLVED.**
  - `粗.md:42` now says JMdict marks the noun as usually written in kana in the "flaw or fault" sense. JMdict 1586730 sense 2 ("flaw (esp. of a person); fault; defect") carries "word usually written using kana alone."
  - Not mentioning fish-bone アラ is acceptable, because the card does not teach that sense.
- **O6 - RESOLVED.** `炊.md:25` now quotes the full gloss of JMdict 1299440 exactly.
- **O7 - DECLINE ACCEPTED.** This was polish only. Both distractor sets remain defensibly wrong in both directions, and changing them would re-open two clean quiz audits.
- **O8 - DISPUTE ACCEPTED.**
  - KanjiReadings.kt lines 110-112: each curated distractor adds one usable reading first. The closeness-tiered fallback only adds while `chosen.size < count - 1`.
  - For 端 はし, 新, 山 and 短 always supply three non-excluded readings (reading-exposure l.98, "fallback is never consulted"; reading-options l.98, 6 distinct options = the 6 curated readings at l.88-90).
  - For 致 いたす, 話, 買 and 学 do the same (exposure l.251; options l.226-228 and l.233, 4 distinct options).
  - So 起's おこす cannot be offered in the audited pools, and the card sentence I suggested would be false.
- **O9 - DECLINE ACCEPTED.**
  - い, a KANJIDIC2 name-only reading of 炊, can still be drawn on the スイ on-prompt in the N1 and All stacks (exposure l.18). It is shown as an on option, which 炊 does not have, so it is a defensible wrong answer.
  - The 吹 and 八 fallbacks are unchanged and safe.
- **O10 - DECLINE ACCEPTED.** No change was needed; every exclusion is a real direct pair.
- **O11 - DECLINE ACCEPTED.**
  - A uniform placement rule (first occurrence inside the "How the kanji combine" section) is a defensible convention. Under that rule 鉢多羅 is the correct first hit.
  - Content-format.md requires only that the kanji is linked. I did not re-read all 34 articles to confirm that the rule is applied uniformly (see Limits).
- **LD - DISPUTE ACCEPTED.**
  - My initial report read "6 / 4 wrong options seen over 100 seeds" as draw frequencies. They are counts of distinct options, and they equal exactly the curated readings.
  - In reading-options.txt, "HIT (can be drawn)" flags membership in a fallback tier, not an observed draw.
  - The two audits therefore agree with each other and with KanjiReadings.kt: there are 0 production hits (exposure l.363), and はじめ and おこす cannot be drawn (l.107, l.254).

Verdicts:

| Facet | Verdict | Basis |
| --- | --- | --- |
| Correctness | CLEAN | All changed claims verified against the pinned JMdict entries, the Daijisen extracts and KanjiVG 静 (青 `kvg:position="left"`, 争 right). The new 請 l.54 statement is correct; the old one, which I missed in my initial round, was wrong. |
| Scoped coverage | CLEAN | Daijisen kun readings はした (端) and においうま (駄) are now mentioned. |
| Consistency and quiz safety | CLEAN | Front matter is unchanged, so the meaning and reading options for all 15 cards are unchanged. quiz-safety.txt reports 0 errors and 0 warnings, every wrong option is distinct from its card's title, and no exclusion is also a distractor. All 9 links on changed lines resolve with equal titles. QuizBuilder.kt skips excluded and duplicate-title options, so every meaning item has exactly one correct option. |
| Comprehensibility | CLEAN | The additions are short and plain. |

The 透明 word-article deletion is correct: it removes a sentence made false by the new 透 card, and nothing else changed.

Confirmation: CONFIRMED.

Findings: none.

Optional:
1. `炊.md:3`: the title "cook rice; boil" is unchanged. Next to the new l.23, which marks the verb's "boil" sense as Kansai, a learner may wonder why "boil" is in the title. The title is defensible as a KANJIDIC2-style kanji meaning (compare 煮炊き). A half-sentence noting that the kanji's "boil" sense is broader than the standard verb would remove the tension. This is editorial only.
2. CHANGES.md says checks\quiz-safety.txt is "identical" to the original packet's copy. Its content is identical, but the file lacks one trailing blank line (57 vs 58 lines, 4554 vs 4556 bytes). This is immaterial.

Limits:
- **Model and process:** Claude (Anthropic). Every response contained exactly one tool call; I am not aware of any parallel calls. No sub-agents and no recursive listings.
- **Audits cover only three pools:** the reading audits are the author's Python ports. I checked their logic against KanjiReadings.kt lines 91-116 and QuizBuilder.kt, but did not run the Kotlin code. The JVM content tests and the Kotlin cross-check were not run; this is a known packet limit. The audits model only the N1 stack, the All stack and the Starter practice session. Other pool compositions (custom stacks, or pools where a curated distractor card is absent) are shown only as "risk class" lines and are not production-verified.
- **"No JMdict entry has においうま":** verified only within the pinned 駄 family extracts, not the full pinned JMdict. I assume an entry spelled 荷負い馬 without 駄 would be irrelevant to the card's claim. The jisho.org lookup was inconclusive.
- **Placement rule (O11):** not verified across all 34 word articles; I read only their diff hunks.
- **Sources:** Daijisen claims were checked against the packet's weblio extracts, assumed to reflect the live pages, except 致す, which I re-read live. JMdict claims were checked against the pinned entries; online JMdict may differ slightly.
- **Unchanged cards:** the ten unchanged cards and the 33 unchanged word-article diffs were not re-read in full. They are byte-unchanged according to CHANGES.md and fix.patch, and my initial verdicts stand.
- **Lint and other check outputs:** not opened; I rely on CHANGES.md's summary.
