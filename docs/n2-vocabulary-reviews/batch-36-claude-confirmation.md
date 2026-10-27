## Snapshot
- **Corrected commit:** `458105a0a9e6ecb00b0de1a127da4566f49b5bdc`; parent `68a03b7c32e03b23a6aad5ff7edfbde37fa6ea03`. I reviewed committed content only and made no edits.
- **Verification limit:** I had file tools only, so I could not run Git or compute hashes. That leaves several author-receipt claims unchecked: that the files on disk match the commit, all file and evidence hashes, that the evidence copy differs from the original only by the removed quiz rationale, and that the unchanged files really are unchanged.

## Scope
- **Model:** claude-opus-5.5 (Claude family), working sequentially with no delegation.
- **Read in full:**
  - The new receipt and my initial report (`docs\n2-vocabulary-reviews\batch-36-claude-initial.md`).
  - The five-file correction patch.
  - All five changed articles.
  - The new evidence sections (lines 20402–20800: `additionalComparisonEntryFamilies`, `correctionEvidence`, `currentQuizDeclarations`, adjudication).
  - The supplemental families file (dictionary entries 1084000, 1084080 and 1568670).
  - The inspected-cards file (the デモ, 姓 and 止す cards).
- **Also checked:**
  - Dictionary entries 1568640 (lines 1258–1330) and 1568670 (line 14293) in the evidence.
  - The front matter of 姓, 止す, 止める, デモ, 終える and しまう on disk.
  - The rules on how quiz exclusions work (`content-format.md:78-92`).
  - Source rows N2:702–704 and N2:719–721.
- **Public sources:** I fetched Weblio's 洒落る page and got the actual Digital Daijisen text. The 締め切り page again came back without its dictionary text.
- **Carried forward without re-reading:** the fifteen unchanged articles, the four kanji edits and the twenty mappings.
- **Not read:** the other family's reports, the review ledger, the authoring notes, REVIEW.md and `batch-36.json`.

## Verdicts
Each cell is correctness / scoped coverage / comprehensibility.

| Article | Verdict |
|---|---|
| 氏名 | CLEAN / CLEAN / CLEAN |
| 洒落 | CLEAN / CLEAN / CLEAN *(revised from NEEDS FIX)* |
| 集会 | CLEAN / CLEAN / CLEAN *(revised from NEEDS FIX)* |
| 締め切り | CLEAN / CLEAN / CLEAN |
| 締め切る | CLEAN / CLEAN / CLEAN |

- **Fifteen unchanged articles:** I keep CLEAN on all three facets, carried forward from my initial review. I did not inspect them again.
- **Four kanji edits (湿, 弱, 庫, 輪):** I keep CLEAN on all three facets, carried forward.
- **Twenty mappings N2:702–721:** I keep CLEAN on all three facets. I re-read N2:703, N2:719 and N2:721 against the revised text and they are consistent with it.
- **Quiz exclusion counts:** I confirm 17 cards with exclusions and 57 declared entries.
  - The changes are +集会/デモ and −締め切る/止す.
  - The full current list in the evidence tallies to these numbers.

## Findings
**My original findings:**
- **B36-01 (集会 / デモ): resolved.**
  - `集会.md:9` now excludes デモ. Declaring it on one side covers both directions.
  - `集会.md:35` adds an accurate distinction: a protest rally can be both; 集会 doesn't itself mean protest; デモ also has a product-demo sense.
  - The dictionary supports this: 1084000 sense 1 and 1084080 sense 1 are "demonstration, protest", and 1084000 sense 2 is the demo/presentation sense.
  - **Other-choice check:** the remaining uncurated pairs, デモ with 集まり, 会合 or 大会, show no established ambiguity, so no exclusion clique is needed.
- **B36-02 (洒落た): resolved.**
  - `洒落.md:39` now correctly identifies 洒落た as the た-form of the intransitive ichidan verb 洒落る (dictionary entry 1568670), modifying 店, and notes that おしゃれ takes な.
  - I independently confirmed this from the public page. Digital Daijisen gives しゃれる as 動ラ下一 with 洒落 marked 当て字, and sense 2, 気がきいている・あか抜けしている, has the example 「―・れた店を出す」.
  - The citation at `洒落.md:45` is accurate.
  - **Withdrawn:** my initial claim that the verb was absent from the evidence packet was wrong. Entry 1568670 is at evidence line 14293.
- **締め切り notice wording: resolved.** The new hedged sentence at `締め切り.md:29` is accurate and matches the N2:703 note.
- **締め切る / 止す: resolved, and I agree with the removal** (`締め切る.md:9`).
  - In both directions, "stop doing; give up" does not cover closing an opening or closing applications.
  - Exclusions against 止める, 終える and しまう still prevent the overlapping pairs from appearing together.
- **洒落 translation: adopted.** "This is not a joke" at `洒落.md:21` is clearer.
- **締め切り / 締め切る noun–verb exclusion: not adopted; acceptable.** The part-of-speech difference in the titles keeps the two apart.
- **水道 link and 出会い/議会/群れ exclusions: not adopted; they remain optional.** 集会's distinctions already separate it from an encounter, an institution and a crowd.

**The other family's finding (GPT36-01), known to me only from the evidence adjudication:** `氏名.md:33` now links 姓. The target card exists ("surname; family name"), so this is resolved. I missed this navigation gap in my initial review.

**Regressions introduced by the correction:** none established.

## Optional
- **洒落 and な:** dictionary entry 1568640 sense 2 is recorded as a な-adjective. A short note that 洒落な is listed in the dictionary, but 洒落た and おしゃれな are the learner-safe patterns, would help reconcile `洒落.md:39-41`.
- **N2:719 mapping note:** it attributes the style sense to "洒落た constructions"; it could name the related verb 洒落る (entry 1568670).
- **`締め切り.md:29`:** "a closed opening can explain an entry notice" could carry a concrete example, such as 締切 on a door versus 受付締切.
- **Carried over:** the 水道→蛇口 back-link.

## Limits
- **Git and hashes:** see Snapshot.
- **Public dictionaries:** Weblio's 締め切り body still did not extract. The Daijisen claims for 氏名 and 集会 rest on the author's receipts plus my own knowledge.
- **Carried-forward verdicts:** the fifteen articles, four kanji edits and twenty mappings were not re-read; their verdicts depend on the receipt's claim that they are unchanged.
- **No app run:** quiz draws were not executed.
- **No native-speaker certification.**
