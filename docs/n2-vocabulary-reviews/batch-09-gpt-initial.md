## Snapshot: ac708ffd2a4153211b420e63c2b0b8766319342d

**Committed content only, as attested by the frozen receipt.** Recorded parent: `5afbc88a0bc01a38f287973aea878916846ea3b0`.

**Git execution was unavailable.** I reviewed the supplied files against the receipt and patch, but could not independently authenticate the commit, recompute hashes, or verify worktree cleanliness.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Sequential, read-only review without delegation. Read all 19 new articles completely, the actual eight-file related patch and changed passages in context, the narrow 奥さん reuse claim, and mappings N2:162–N2:181. Consulted the required instructions, format documentation, permitted source records, relevant comparison cards and component metadata.

Unchanged teaching on the eight related cards was inspected only for context—not comprehensively reviewed. Other batches, forbidden authoring/review materials, other reviewers’ outputs, and application implementation were excluded.

## Verdicts:

**Four localized quiz-exclusion findings need fixes.** No actionable defect was established in the new articles’ linguistic explanations, source coverage, or comprehensibility. CLEAN below means no actionable defect established within this scope, not exhaustive correctness.

All article paths in this table are under `words\`.

| New article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| おおざっぱ.md | NEEDS FIX | CLEAN | CLEAN |
| 大通り.md | CLEAN | CLEAN | CLEAN |
| オートメーション.md | CLEAN | CLEAN | CLEAN |
| オーバーコート.md | CLEAN | CLEAN | CLEAN |
| おおよそ.md | NEEDS FIX | CLEAN | CLEAN |
| お帰り.md | CLEAN | CLEAN | CLEAN |
| おかけください.md | CLEAN | CLEAN | CLEAN |
| おかげさまで.md | CLEAN | CLEAN | CLEAN |
| おかず.md | CLEAN | CLEAN | CLEAN |
| 拝む.md | CLEAN | CLEAN | CLEAN |
| お代わり.md | NEEDS FIX | CLEAN | CLEAN |
| 補う.md | CLEAN | CLEAN | CLEAN |
| お気の毒に.md | CLEAN | CLEAN | CLEAN |
| 屋外.md | CLEAN | CLEAN | CLEAN |
| 送り仮名.md | CLEAN | CLEAN | CLEAN |
| 元気でね.md | CLEAN | CLEAN | CLEAN |
| 怠る.md | CLEAN | CLEAN | CLEAN |
| 押さえる.md | CLEAN | CLEAN | CLEAN |
| お先に.md | NEEDS FIX | CLEAN | CLEAN |

The correctness findings concern possible multiple defensible quiz answers, not incorrect definitions or examples.

| Related file—changed passages only | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\拝.md`—linked おがむ examples | CLEAN | CLEAN | CLEAN |
| `kanji\補.md`—linked おぎなう examples | CLEAN | CLEAN | CLEAN |
| `kanji\毒.md`—お気の毒に example and citation | CLEAN | CLEAN | CLEAN |
| `words\オーバー.md`—オーバーコート navigation | CLEAN | CLEAN | CLEAN |
| `words\コート.md`—オーバーコート navigation | CLEAN | CLEAN | CLEAN |
| `words\おかげ.md`—おかげさまで navigation | CLEAN | CLEAN | CLEAN |
| `words\気の毒.md`—お気の毒に navigation | CLEAN | CLEAN | CLEAN |
| `words\外.md`—屋外 navigation | CLEAN | CLEAN | CLEAN |

**Reuse:** `words\奥さん.md` is **CLEAN / CLEAN / CLEAN** for the narrow reuse suitability claim. Its current text explicitly teaches おくさん as another person’s wife and as an address form, with `jlpt: 5`. The assertion that neither content nor metadata changed from the parent is **UNVERIFIED independently**; file-only access does not establish historical equality.

**Explicit mappings:** **CLEAN / CLEAN / CLEAN** for source-to-teaching suitability across all 20 assigned rows. In particular:

- N2:166’s **大凡／おおよそ** is explicitly recognized in おおよそ, with rare-kanji spelling distinguished from pronunciation.
- N2:180’s **押える／おさえる** is explicitly taught as an alternative spelling in 押さえる, alongside the relevant holding, seizing and suppression meanings.
- **元気でね is N2:178, reading げんきでね**, between 送り仮名 and 怠る in the supplied exact-row records. The article preserves that identity and teaches the farewell rather than a statement of the speaker’s health.
- The anomalous glosses are appropriately qualified: おかげさまで is not restricted to religious use; 怠る’s illness-improvement sense is marked dated.

No omission was found in primary-spelling kanji metadata. Existing primary written-kanji cards receive substantive links, and the required N2 reciprocal examples for 拝, 補 and 毒 use the articles’ actual readings. Whole-word readings are not promoted into invented constituent readings.

## Findings:

**B09-GPT-01 — Minor; correctness, quiz-label ambiguity.**  
**Location:** `words\おおざっぱ.md:4,9,16–21`; comparison declarations in `words\およそ.md:4,9` and `words\一応.md:4,9`.

The new card excludes 大体 and ざっと but not **およそ** or **一応**. Their displayed labels—“approximately; generally” and “tentatively; roughly; just in case”—retain defensible answers for the broad/rough treatment taught here. Conversely, “rough; broad-brush” can reasonably describe their general or rough-treatment meanings. Contextual distinctions between the Japanese constructions do not resolve an uncontextualized meaning quiz.

**Minimal remedy:** Add direct exclusions for およそ and 一応 on おおざっぱ. Existing exclusions through おおよそ, 大体 or ざっと are not transitive.

**Evidence:** Complete families in `docs\n2-vocabulary-batch-sources\batch-09.json`: JMdict **1412950:1** (“rough [estimate, summary, etc.]; broad; general”), **1523450:1–2** (“roughly; approximately; generally”), and **1161170:1** (“more or less; roughly; after a fashion”). This is a label safeguard, not a claim of unrestricted substitution. **Confidence: medium-high.**

**B09-GPT-02 — Minor; correctness, unprotected approximation answers.**  
**Location:** `words\おおよそ.md:4,9,16–19`; `words\ばかり.md:4,8,15–22`; `words\程度.md:4,9,16–23`.

The extensive exclusion list omits **ばかり** and **程度**, although both have ordinary numerical-approximation uses. A question showing either comparison word can therefore offer おおよそ’s “approximately; outline” as a defensible alternative to its own title. The different placement—おおよそ十分 versus 十分程度／一時間ばかり—does not distinguish context-free meaning choices.

**Minimal remedy:** Add ばかり and 程度 directly to おおよそ’s `quiz_exclusions`.

**Evidence:** Pinned JMdict **1415050:1** establishes おおよそ’s approximation sense. The comparison articles explicitly teach the corresponding quantity constructions. Independently retrieved [Jisho ばかり entry](https://jisho.org/search/%E3%81%B0%E3%81%8B%E3%82%8A) gives sense 2 “approximately; about”; the [actual 程度 record](https://jisho.org/api/v1/search/words?keyword=%E7%A8%8B%E5%BA%A6) gives ていど and “about; approximately” following a number. Neither endpoint declares the missing pairs. **Confidence: high.**

**B09-GPT-03 — Minor; correctness, ordinary secondary sense omitted from quiz protection.**  
**Location:** `words\お代わり.md:4–9,15–16,26–30`; comparison header `words\代わり.md:2–9`.

Neither card declares an exclusion. Although the existing 代わり article focuses on substitution, its lexical family also contains the food-and-drink meaning represented by the new label **“another helping; refill.”** Thus the new label can be a defensible alternative answer for 代わり. This conclusion does not follow merely from their shared character or derivational relationship.

**Minimal remedy:** Add `quiz_exclusions: [代わり]` to お代わり; retain the useful comparison link and existing titles.

**Evidence:** The complete pinned families distinguish **1612800:1** お代わり from **1590770:4** 代わり. The latter explicitly lists “another helping; second helping; seconds; refill,” notes **“usu. as お～”**, and cross-references お代わり. “Usually” is a qualification, not a spelling or reading restriction excluding the underlying card. **Confidence: high.**

**B09-GPT-04 — Minor; correctness, overlapping invitation labels.**  
**Location:** `words\お先に.md:4,9,16–25`; `words\どうぞ.md:4–9,15–18,32`.

お先に excludes several before/ahead words but not **どうぞ**, whose title is **“please; go ahead.”** The new article explicitly teaches the listener-first invitation translated “Please, go ahead.” Without a sentence distinguishing priority from general permission, that label is a reasonable answer for お先に. Neither endpoint protects the pair.

**Minimal remedy:** Add どうぞ directly to お先に’s exclusions. No change to the departure teaching is necessary.

**Evidence:** Pinned JMdict **1002280:2** supplies “ahead”; **1189130:2** supplies “(go) ahead” when giving permission or accepting a request. The inspected cards explicitly demonstrate the overlapping invitation interpretation. This does not assert equivalence in the leaving-first formula or every use of どうぞ. **Confidence: high.**

## Optional:

None.

## Limits:

Snapshot identity, hashes, cleanliness and the unchanged-reuse history remain receipt-attested rather than independently Git-verified. No files were edited.

Main JMdict and KANJIDIC2 evidence came from the supplied extracted records; I did not independently reconstruct or hash-check the underlying downloads. Author inspection receipts were treated as assertions, not independent retrieval. I independently fetched the four cited Kotobank pages for 御蔭様, 送り仮名, 押える and 怠る, and the Jisho records cited above. Supplemental native-dictionary retrieval for 代わり was inconclusive; B09-GPT-03 rests on the complete pinned JMdict family and its explicit prefix qualification.

Selected dictionary families are not the whole dictionary, and omission was not treated as evidence of absence. Quiz consequences use the supplied symmetric, nontransitive exclusion contract, not an application execution. This review does not establish corpus frequency, native-speaker certification, or an official modern JLPT syllabus.
