## Snapshot: 3e67155e0a83c666b61719eca7eb3377fd649ce9; committed content only

**Three actionable findings:** two missing quiz-exclusion pairs and one minor component-link gap. The twenty source associations, identity corrections, narrow reuse edits, and edited 造/詰 passages otherwise pass this scoped review.

Parent: `1544e108e7c7d25df19edbbd93f37a07c9576305`. I read `frozen-snapshot.json` first. File tools cannot execute Git, so the commit association and clean-worktree status remain supplied snapshot assertions, not independently executed Git checks.

## Scope: GPT-6.1 Sol — gpt-6.1-sol; family gpt

Read-only review, without agents, delegation, or edits.

I completely read all fourteen new articles, all five reused articles, `related.patch`, and both edited kanji cards. Reuse judgments concern the assigned source associations and changed passages—not whole-article reauthoring of 漬ける, 粒, or 積む. I also completely read thirteen other relevant kanji cards: 作, 付, 伝, 突, 込, 務, 努, 勉, 力, 着, 点, 粒, 積.

Evidence read included:

- Both required instruction files; `docs\content-format.md:18–126`; the permitted confusable-word and JLPT-policy documents; both repository source-snapshot documents; and only the assigned twenty TSV mappings.
- Complete compact mappings, twenty-one principal-family records, twenty-nine component records, and 289 label/exclusion records.
- All eight family-inspection renderings and the supplemental rendering—the supplied 139-family/557-sense union, including the twenty principal families/99 senses and corrected 務める family.
- All twenty captured public lexical bodies, plus the blind derivative’s relevant provenance, twenty inspection receipts, declarations, and baseline guard additions. I did not read the entire large derivative or redundant `principal-reading.txt`/`public-bodies.json` renderings.
- **Seventy-six additional old word articles completely:** every old target of the new/added exclusions, plus 縄, 苦心, 直通, 間接, ぺちゃんこ, 光る, 輝く, 滑る, and 造船. This is my actual comparison-body scope, not the author’s reported 102 reads.

Fresh usable dictionary reads were Kotobank’s 精選版日本国語大辞典 entries for 続ける and 苦心, and complete relevant Jisho results for 苦心 and ぺちゃんこ. Prohibited ledgers, author rationale, other reviewers’ reports, and unassigned private files were not accessed.

## Verdicts: twenty source rows

Here, **correctness includes quiz-choice ambiguity**, while **scoped coverage includes required component links**. CLEAN means no actionable defect established within the stated scope.

| Source row | Exact article association | Article scope | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1102 | 造る → `words\作る.md` | Reused; retain N5 | CLEAN | CLEAN | CLEAN |
| N2:1103 | 着ける → `words\付ける.md` | Reused; retain N5 | CLEAN | CLEAN | CLEAN |
| N2:1104 | 点ける → `words\付ける.md` | Reused; retain N5 | CLEAN | CLEAN | CLEAN |
| N2:1105 | 浸ける → `words\漬ける.md` | Reused, unchanged N4 | CLEAN | CLEAN | CLEAN |
| N2:1106 | 伝わる → `words\伝わる.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1107 | 突っ込む → `words\突っ込む.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1108 | 務める → `words\務める.md` | New N2; corrected identity | CLEAN | CLEAN | CLEAN |
| N2:1109 | 努める → `words\努める.md` | New N2 | **NEEDS FIX** | **NEEDS FIX** | CLEAN |
| N2:1110 | 綱 → `words\綱.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1111 | 繋がり → `words\繋がり.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1112 | 繋がる → `words\繋がる.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1113 | 繋げる → `words\繋げる.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1114 | 粒 → `words\粒.md` | Reused; N2 level-only addition | CLEAN | CLEAN | CLEAN |
| N2:1115 | 潰す → `words\潰す.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1116 | 潰れる → `words\潰れる.md` | New N2 | **NEEDS FIX** | CLEAN | CLEAN |
| N2:1117 | つまずく → `words\つまずく.md` | New kana-primary N2 | CLEAN | CLEAN | CLEAN |
| N2:1118 | 詰まる → `words\詰まる.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1119 | 積む → `words\積む.md` | Reused; N2 level-only addition | CLEAN | CLEAN | CLEAN |
| N2:1120 | 爪 → `words\爪.md` | New N2 | CLEAN | CLEAN | CLEAN |
| N2:1121 | 艶 → `words\艶.md` | New N2 | CLEAN | CLEAN | CLEAN |

**Mappings — CLEAN for all twenty assigned rows.** The selected and additional one-based senses support the practical teaching presented. In particular:

- **務める:** raw `1240825` contains only 勤める; teaching `2872052:1` is correctly identified as an identity correction, not a same-family alias. 努める correctly rejects the copied employment gloss while retaining it as raw source data.
- **点ける:** `1610400:1` is a separate entry cross-referenced to `1495770:13`. Preserving primary 付ける and recording the additional identity is appropriate.
- **着ける:** the seat-belt fastening/wearing and boat-alongside examples support the selected recognition scope. The article does not authorize every spelling for every family sense.
- **浸ける:** the unchanged soaking example covers the assigned source; 漬ける-only pickling is not transferred to 浸ける.
- Usually-kana, rare, outdated, and alternate-reading recognition is appropriately distinguished from primary spelling and measured frequency. Added meanings are not individually presented as independently sourced N2 senses.

**Kanji edits and baseline preservation:**

| Edited surface | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\造.md` alias links | CLEAN | CLEAN | CLEAN |
| `kanji\詰.md` reciprocal additions | CLEAN | CLEAN | CLEAN |

造’s `つく.る` example and Common words entry link to primary 作る with explicit alias context (`造.md:31,39`). 詰 has the linked `つ.まる` example and Common words entry (`詰.md:33,41`), reciprocated substantively at `words\詰まる.md:32`.

The supplied patch preserves both kanji cards’ baseline metadata. It also preserves the primary identities, readings, titles, easier levels, and primary-kanji arrays of 作る/付ける; leaves 漬ける unchanged; and adds only `jlpt: 2` to 粒/積む. 粒’s existing guards are retained, not newly adjudicated.

## Findings: three actionable defects

**N2-56-GPT-01 — Moderate; correctness / quiz ambiguity**

**Locations:** `words\努める.md:4,9,16`; `words\苦心.md:4,9,16–19`.

The direct **努める–苦心** pair is unguarded. The complete titles are “strive; make an effort” and “painstaking effort; taking pains.” 苦心’s body explicitly teaches working or thinking hard to accomplish something difficult; its する use makes “make an effort” a defensible answer, not merely a shared effort-related topic. Neither article declares the other. Their shared exclusions through 努力 or 一生懸命 do not close this pair because exclusions are nontransitive.

**Minimal remedy:** add `苦心` to 努める’s exclusions, or the reverse declaration—one direct edge suffices.

**Exact evidence:** pinned `1240820:1` includes “try hard,” “work hard,” “strive,” and “make an effort.” The complete [Jisho 苦心 entry](https://jisho.org/api/v1/search/words?keyword=%E8%8B%A6%E5%BF%83) supplies “hard work; effort,” with noun/intransitive-する POS; [精選版日本国語大辞典](https://kotobank.jp/word/%E8%8B%A6%E5%BF%83-483477) describes efforts to accomplish something successfully. The pairwise rule is `docs\content-format.md:85–98`.

**Confidence:** high for the missing edge and lexical overlap; no claim that a particular live question was observed.

**N2-56-GPT-02 — Moderate; correctness / quiz ambiguity**

**Locations:** `words\潰れる.md:4,9,16–20`; `words\ぺちゃんこ.md:4,14–19`.

The direct **潰れる–ぺちゃんこ** pair is unguarded. “Be crushed; go out of business” and “squashed flat” overlap directly in the physical sense. The old article defines ぺちゃんこ as flattened or crushed down and illustrates bread squashed under a box; 潰れる illustrates a box crushed by weight. These are matching physical outcomes, not simply members of a destruction category. ぺちゃんこ has no reverse exclusion.

**Minimal remedy:** add `ぺちゃんこ` to 潰れる’s exclusions, or declare the reverse pair. Do not infer additional edges transitively.

**Exact evidence:** pinned `1433830:1` covers being crushed or losing shape. The complete [Jisho ぺちゃんこ family](https://jisho.org/api/v1/search/words?keyword=%E3%81%BA%E3%81%A1%E3%82%83%E3%82%93%E3%81%93) gives “crushed flat; flattened; squashed; flat-topped” in sense 1; its other senses do not remove that overlap. Different titles therefore do not provide exact-title deduplication.

**Confidence:** high.

**N2-56-GPT-03 — Minor; scoped coverage / component navigation**

**Location:** `words\努める.md:29`.

The substantive introduction of the rare spellings **勉める and 力める** leaves both existing component cards unlinked. Their recognition-only qualification is accurate; the gap is navigation, not lexical correctness.

**Minimal remedy:** link 勉 and 力 at this introduction, following the existing character-link pattern. Keep primary `kanji: [努]`; no variant metadata expansion or reciprocal-card redesign is required.

**Exact evidence:** both `kanji\勉.md` and `kanji\力.md` exist and were read completely; pinned `1240820` records both rare spellings. `.github\instructions\content-structure.instructions.md:20–21,55–56` requires substantive links to existing cards.

**Confidence:** high.

## Optional: none

## Limits: provenance and bounded review

The twenty supplied endpoint captures are **one dictionary service’s captured bodies**, not twenty independent dictionaries or fresh reviewer retrievals. I separated relevant lexical headings from unrelated/homographic material. Inspection counts, hashes, and equivalence checks remain author-executed assertions; I did not execute them.

Fresh Weblio requests for 続ける and ぺちゃんこ did not provide usable lexical verification, and Kotobank’s ぺちゃんこ request returned 404. Those results were not treated as evidence. Successful alternative reads resolved the relevant comparisons. In particular, 精選版日本国語大辞典’s 続ける sense ④ documents connecting things, so I did not reject the 繋げる/続ける guard from its short title alone. Likewise, つるつる’s complete old body and dictionary record include shine; its 艶 guard was not dismissed as mere texture association.

The 289 labels were not 289 full-body reads. Unread comparisons—including 粒’s five retained guard targets—are not certified. No repository-wide synonym audit, live-app quiz execution, measured-frequency study, native-speaker certification, or independent historical-etymology verification is claimed. No consequential unresolved teaching claim remains identified within the reviewed scope.
