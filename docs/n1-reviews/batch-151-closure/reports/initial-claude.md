# Batch 151 initial review (Claude)

## Snapshot

- **Commit:** b624890f8aea8cfb6b5a08ee6beff21df5f8c807 (batch 151; kanji cards 訴 証 詩 詳 誇 誓 誘 謙 謡 譲 護 豆 豪 貢 貴).
- **Packet:** batch-151-b624890f (packet-manifest.json sha256 ca0ee534…1cf1, as stated in the task).
- **Reviewer model:** Claude (Anthropic), first of two blind reviewers. I worked read-only and alone.

## Scope

**Facets examined deepest:** facet 1 (correctness) and facet 2 (scoped coverage). I also covered facets 3 and 4 for all 15 cards and all 29 diffs.

Packet files opened (paths relative to the packet root):

- **Read in full:**
  - INSTRUCTIONS.md and mechanical-checks.md.
  - evidence\: source-metadata.json, joyo-pages.md, kanjipedia-outside-readings.json, daijisen-heads.txt, okurigana-scan.txt, kanjivg-components.txt, and all 15 public-source\weblio-*.txt.
  - snapshot\kanji\: all 15 new cards (訴 証 詩 詳 誇 誓 誘 謙 謡 譲 護 豆 豪 貢 貴).
- **Read in part:**
  - diffs\: all 29 diffs, changed lines plus context.
  - evidence\jmdict-families.xml and evidence\jmdict-digest.tsv: grep for every cited entry id and word.
  - evidence\kanjidic2-records.xml: grep for literals, readings and meanings.
  - evidence\audits\reading-exposure.txt: lines 1-30 and 194-246, plus a grep for the attested, latent, info and summary lines.
  - titles\kanji-titles.tsv and titles\word-titles.tsv: grep for every linked, quoted, exclusion and distractor title.
  - repo\docs\content-format.md: grep, plus lines 100-175.
  - evidence\app-code\KanjiReadings.kt: grep only.
- **Listed only (non-recursive):** the packet top level, its first-level folders and evidence\app-code.
- **Public web:** live Kanjipedia pages for 訴 誘 謙 謡 豪 豆 護 貴 貢 譲 証.

## Verdicts

**Overall:**

- Correctness: NEEDS FIX (minor, 貴 only, C1); CLEAN for the other 14 cards and all 29 diffs.
- Scoped coverage: CLEAN.
- Consistency and quiz safety: CLEAN.
- Comprehensibility: CLEAN.

**Per card:**

- **訴 証 詩 詳 誇 誓 誘 謙 謡 譲 護 豆 豪 貢:** CLEAN on all four facets. Optional polish is listed below for 謙, 護, 誓, 譲, 訴 and 誘.
- **貴:** correctness NEEDS FIX (C1, mnemonic stroke account). Coverage, quiz safety and comprehensibility are CLEAN.

**Diffs:**

- **19 word diffs:** CLEAN. Each is a one-line link-wrap of the first mention, and each link points to the right ../kanji/X.md card. None touches a Dictionary: line, including 民謡, 誓う and 看護婦.
- **10 kanji remark diffs:** CLEAN. Each new link targets an existing card with its exact title: 虚, 舌, 薦, 慮, 貢, 及, 裁, 羊, 我 and 短 ("short"). Each sentence is true at this snapshot and reads naturally.

## Findings

### C1: 貴's mnemonic misses one stroke

- **Severity:** minor.
- **Facet:** 1 (correctness: component and stroke statement).
- **File:** snapshot\kanji\貴.md, modern-shape mnemonic paragraph (Meaning and origin section).
- **Claim and impact:**
  - The mnemonic splits 貴 into 中 on top and 貝 at the bottom, with nothing between them.
  - At the pinned KanjiVG revision, 貴 groups 中 as strokes 1-4, then an ungrouped horizontal stroke 5 (㇐), then 貝 as strokes 6-12.
  - 中 (4) + 貝 (7) = 11 strokes, but the card's front matter says 12.
  - A learner checking the parts against the stroke animation will find a stroke the mnemonic does not account for.
- **Remedy:** describe the top as 中 resting on a horizontal stroke (一), above 貝. The picture can stay the same.
- **Evidence:** evidence\kanjivg-components.txt, entry for 貴 (groups 中 and 貝 with a separate stroke-5 ㇐); 貴.md front matter `strokes: 12`.
- **Confidence:** high.

No blocker or major defect was established.

### Points (a)-(h): checked and not defects

- **(a) Broad exclusion sets.**
  - Every pair is either a real direct synonym or a confusable pair through a shared gloss or kun reading, or at worst a harmless over-exclusion.
  - Over-exclusion only removes candidate options; the app treats exclusions as symmetric and non-transitive, and they affect meaning choices only.
  - The weakest pairs are 誇/功, 誇/凱, 謡/凱, 訴/挙, 誘/艶, 豪/盛 and 豆 with 子, 児, 童, 幼 and 稚. They are tied to the "small" and "child" prefix senses of 豆 (JMdict 1450030) and are defensible as caution.
  - I found no missing exclusion that leaves a correct-looking wrong answer.
- **(b) Close pairs in this batch.** All are distinguishable as answers in both directions from the displayed titles:
  - 謙/譲: excluded on 譲's side; correct, given 謙譲.
  - 詩/謡: excluded on 謡's side.
  - 誇 "pride; boast" vs 豪 "powerful; excelling".
  - 貴 "precious; esteem" vs 豪.
  - 貢 "tribute; contribute" vs 譲 "hand over; yield". This is the closest pair, but its senses are distinct.
  - 証 "evidence; proof" vs 誓 "vow; swear".
- **(c) Distractors.** Every one is defensibly wrong in both directions. 舌 is not used anywhere. 舞, 笛 and 茶 against "Noh chanting", 劇 and 琴 against "poem; poetry", and 芋 against "bean; pea" are plausible but clearly wrong. 譲's 食, 行 and 来 are wrong but weak (see Optional).
- **(d) Reading labels.**
  - Every label is supported by KANJIDIC2, Joyo p. pages in joyo-pages.md, Daijisen or Kanjipedia (live pages match for 11 kanji):
    - 証's あか.す and しるし;
    - 誓's ゼイ from 弘誓 ぐぜい (JMdict 1872960);
    - 誘's いざな.う and おび.く (Kanjipedia 外);
    - 豆's まめ- prefix and たかつき (Kanjipedia 外);
    - 豪's えら.い from 豪い (JMdict 1155780, rarely used kanji form), with コウ and つよい marked 外;
    - 貢's ク from 年貢 ねんぐ (JMdict 1468630);
    - 貴's たかい, あて and むち;
    - 譲's せめる (Kanjipedia ③).
  - **護/看護婦:** JMdict 1213870 marks 看護婦 an obsolete term, with an xref to 看護師. The reading ゴ in it is current and unaffected, and the card states the status and points to 看護師. This is a sound basis (see Optional).
- **(e) Reading-exposure accounting.** It is correct:
  - 3 latent collisions (詳 よし, 譲 せめる, 貴 ぎ), none drawable in the N1, All or Starter pools;
  - 2 info lines for name-only readings drawable only in a Starter session (豆 ま, 豪 ご);
  - 0 production, padded or one-holder hits.

  The okurigana-scan extras are passed correctly. 謙's name reading ゆずる does not collide, because 謙 quizzes only ケン.
- **(f) Mnemonics.**
  - All 15 are labelled "Modern-shape mnemonic, not etymology" and disclaim any historical formation.
  - All quoted titles are exact.
  - The component statements match kanjivg-components.txt, except 貴 (C1) and the incomplete but non-arithmetic description of 謙 (Optional).
- **(g) Meaning statements.** All match JMdict or Kanjipedia (live). For example:
  - 訴: さばきを求めて申し出る and 同情を求める.
  - 証: あかす。あかしをたてる。また、あかし。しるし, with 類 徴.
  - 詩: うた, from JMdict 1193180 sense 3.
  - 詳: JMdict 1351730 sense 2 "well-informed (about)".
  - 誇: 誇らしい, JMdict 1267730.
  - 誓: 弘誓.
  - 謡: ③ うたい。能のうたい.
  - 護: 看護婦 and 看護師.
  - 豆: prefix senses, and ② たかつき.
  - 豪: ④ 豪太剌利の略, and えら (JMdict 2229640).
  - 貢: ク and 年貢.
  - 貴: ③ 相手への敬意を表す語.
- **(h) Remark edits.** True, correctly linked and natural.

## Optional

1. **謙:** the mnemonic names 八, ⺕ and two vertical strokes for 兼. KanjiVG also has stroke 10 (一) and strokes 16-17 (㇒ ㇏). There is no arithmetic claim, so this is not wrong, but adding "plus a horizontal stroke and two sweeping strokes at the bottom" would make it complete.
2. **護:** ゴ is quizzed through 看護婦, which JMdict marks as an obsolete term. The card handles this honestly. A future word article for 保護 or 看護師 would be a more current basis.
3. **誓:** the Readings table lists ゼイ after ちか.う. content-format.md has no ordering rule, but grouping the on readings (セイ, ゼイ) before the kun reading would read more naturally.
4. **Coverage polish:**
   - 訴: 告訴 (a Joyo example) and 起訴 or 控訴 are not mentioned.
   - 誘: 誘拐 and おびき出す or おびき寄せる are not mentioned; the second would illustrate おび.く.
   - 誓: 宣誓 is not mentioned.

   None is required.
5. **譲:** the distractors 食 "eat, food", 行 "go" and 来 "come" are correct but easy to eliminate. A verb with closer semantics, such as 奪 or 受, would make the question more useful.
6. **縫 diff:** it is −2/+1 lines. It replaces a wrapped bullet with one line and drops the clause "this does not change the complete word's reading." It is still a remark-only edit; noting it for transparency.

## Limits

- **Not opened:**
  - evidence\audits\: quiz-safety.txt, reading-options.txt, kanji-remarks.json and extra-readings.json;
  - evidence\kanjivg-svgs.txt and snapshot\strokes\*.json. I checked the mnemonics against kanjivg-components.txt only; the stroke files were not validated individually beyond the mechanical checks.
  - The full snapshot\words articles beyond the diff context, the rubric, confusable-words.md and most of app-code.
- **Live checks:**
  - I did not fetch the live Kanjipedia pages for 詩, 詳, 誇 or 誓. I relied on the packet's public-source extracts, daijisen-heads.txt and kanjipedia-outside-readings.json.
  - I did not check JMdict online. I relied on the packet's pinned JMdict extract.
- **Assumptions:**
  - Over-exclusion is harmless, because exclusions only shrink the option pool.
  - The remark edits' declared old and new texts are as shown in the diffs.
- **Packet limits (not reported):** the Android JVM tests and the Kotlin cross-check were not run.
- **Tool use:** every response contained exactly one tool call.
