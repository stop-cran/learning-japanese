## Snapshot

`6855b42fa2c4e4cae6fd01a2697d10ee42011abb`; **no uncommitted teaching**, as identified by the supplied export/index. Baseline: `57dcc2aaedd8d6b0f141d5b4c3cb9c13f6f797b2`. I did not independently inspect Git state.

**Outcome:** No actionable teaching-text correctness defect established. **Learner-facing reading-key acceptance is not established for seven kanji**; the pinned projection exposes source-only or insufficiently contextualized recognition readings. A narrow companion prerequisite belongs under content issue #1, not a metadata rewrite or expansion of this content task.

## Scope

Independent read-only review of all 12 new kanji articles, all five new word articles, and the changed passages plus integration of eight reused word articles. Correctness, scoped coverage and textual phone comprehensibility were assessed separately. Eleven existing articles were read as comparison context, not reassigned for full review.

Model identity exposed in this session: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`.

**Packets read completely, serially:**

- `packet-index.json`
- `teaching-01.txt`, `teaching-02.txt`, `teaching-03.txt`, `teaching-04.txt`, `teaching-05.txt`
- `dictionary-01.txt`, `dictionary-02.txt`, `dictionary-03.txt`, `dictionary-04.txt`
- `comparisons-01.txt`, `comparisons-02.txt`
- `reused-passages.diff`
- `metadata-and-offered-keys.json`: explicit ranges 1–380, 381–760 and 761–1120; the final range returned through EOF.
- `external-observations.json`

**Omitted or unrecovered truncated ranges: none.** All 56 complete frozen JMdict families were read. No prohibited rationale, audit, progress, adjudication or previous-review material was accessed. No commands, edits, delegation, task creation or publication occurred.

## Verdicts

**CLEAN** means no actionable defect established within the assigned scope, not exhaustive certification. Coverage verdicts below include the reading-key integration finding; they do not imply that the article’s source-only disclosures are incorrect.

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji/幹.md` | CLEAN | CLEAN | CLEAN |
| `kanji/氏.md` | CLEAN | CLEAN | CLEAN |
| `kanji/扱.md` | CLEAN | NEEDS FIX | CLEAN |
| `kanji/乃.md` | CLEAN | NEEDS FIX | CLEAN |
| `kanji/凹.md` | CLEAN | CLEAN | CLEAN |
| `kanji/凸.md` | CLEAN | CLEAN | CLEAN |
| `kanji/矛.md` | CLEAN | NEEDS FIX | CLEAN |
| `kanji/鷹.md` | CLEAN | CLEAN | CLEAN |
| `kanji/彗.md` | CLEAN | NEEDS FIX | CLEAN |
| `kanji/漱.md` | CLEAN | NEEDS FIX | CLEAN |
| `kanji/栞.md` | CLEAN | NEEDS FIX | CLEAN |
| `kanji/莉.md` | CLEAN | NEEDS FIX | CLEAN |
| `words/乃至.md` | CLEAN | CLEAN | CLEAN |
| `words/彗星.md` | CLEAN | CLEAN | CLEAN |
| `words/栞.md` | CLEAN | CLEAN | CLEAN |
| `words/茉莉花.md` | CLEAN | CLEAN | CLEAN |
| `words/鷹.md` | CLEAN | CLEAN | CLEAN |
| `words/うがい.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |
| `words/でこぼこ.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |
| `words/凹む.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |
| `words/扱う.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |
| `words/新幹線.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |
| `words/氏.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |
| `words/氏名.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |
| `words/矛盾.md` — changed-passage scope | CLEAN | CLEAN | CLEAN |

### Basis for the CLEAN text verdicts

The preserved on/kun identities, order, stroke counts and canonical radical indices agree with the supplied metadata. Every metadata reading is either supported by a lexical example or explicitly qualified as source-only/character-dictionary recognition. Modern-shape mnemonics are labelled rather than asserted as etymology.

Important distinctions are handled correctly:

- `kanji/氏.md:28–45` distinguishes modern suffix **し**, native **うじ** and older suffix **-うじ**, without denying clan senses under either reading. JMdict 2101130 senses 1–2 and 1311010 senses 1–2 support the distinction; the supplied inspected Kotobank sections support the older suffix example.
- `kanji/凹.md:28–45` and `kanji/凸.md:28–40` preserve the separate へこむ/くぼむ families and the 凸凹/凹凸 spelling order. JMdict 1582410 restricts its imbalance sense to でこぼこ; the articles retain that restriction.
- `kanji/漱.md:31–36,46` correctly explains **漱ぐ／くちすすぐ**, rather than allocating only すす to 漱 or inventing 口漱ぐ. JMdict 2261070 and the supplied inspected Kanjipedia navigation support that boundary. The separate mouth-rinsing すすぐ family is not inflated into general laundry vocabulary.
- `kanji/彗.md:31` explicitly avoids treating the **せい of 星** in 彗星 as evidence for 彗’s セイ reading.
- `words/乃至.md:15–32`, `words/栞.md:15–32`, `words/茉莉花.md:15–32` and `words/鷹.md:15–32` preserve the selected senses, usual-kana qualifications where applicable, and useful limits on English glosses.

The new word examples have English translations and adequate kana support. They are practically understandable in text, without an established naturalness or translation defect.

All eight reused supports contain actual reciprocal links to their new kanji articles: `words/うがい.md:24`, `words/でこぼこ.md:15`, `words/凹む.md:25`, `words/扱う.md:24`, `words/新幹線.md:28`, `words/氏.md:28`, `words/氏名.md:27`, and `words/矛盾.md:28`. Their integration preserves the existing word identities.

All **36 curated kanji meaning distractors** were checked against their actual supplied titles. Each new kanji has three defensibly wrong options; shared components or readings do not make those meaning labels correct. In particular, neither shared unevenness vocabulary for 凹/凸 nor plant components for 莉 invalidate the selected contrasting labels.

The new word exclusions are defensible **pairwise**:

- 乃至 excludes または, あるいは and それとも because their actual labels overlap its alternative “or” sense—not because they share its numerical-range use.
- 栞 excludes 本, 書物, 図書 and 冊子 because its guidebook sense overlaps the book/booklet labels.
- 茉莉花 excludes the broader 花 label; 鷹 excludes the broader 鳥 label.
- 彗星 does not require exclusion of meteor vocabulary: the complete supplied families distinguish those phenomena.
- 案内’s “guidance” label does not automatically become interchangeable with the guidebook object merely through association with 冊子 or 栞. No transitive exclusion requirement is inferred.

Missing vocabulary JLPT levels were not inferred from kanji levels.

## Findings

### F1 — High: reading-prompt acceptance prerequisite remains unmet

**Facet:** Scoped coverage / reading compatibility.  
**Classification:** Demonstrated projection/disclosure mismatch; consequential unresolved prompt suitability. **Not a finding that the dictionary readings are false.**

The articles carefully distinguish useful vocabulary from source-only recognition information. The pinned app nevertheless offers those source-only readings as study keys. Prose warnings do not filter the projection. Thus correct disclosure in an article is insufficient evidence that its offered quiz keys are suitable learner prompts.

| File and original lines | Projected keys requiring resolution | Precise concern and evidence |
|---|---|---|
| `kanji/扱.md:28–35` | On `そう`, `きゅう` | Both rows explicitly lack an established lexical example here. Supplied Kanjipedia observations support character-reading recognition, not a usable example or its study priority. JMdict 1153440 supports あつかう; 2029490 supports こく. Neither establishes these on-reading prompts. |
| `kanji/乃.md:28–36,42` | On `の`; kun `の`, `なんじ` | On ノ has no separately established lexical example. Kun の is a historical/search-only spelling in JMdict 1469800, not ordinary modern particle orthography. なんじ is explicitly character-dictionary/kanbun recognition, supported by the supplied inspected character heading rather than a retrieved standalone word definition. These require explicit prompt qualification or curation, not an assumption that all are ordinary word readings. |
| `kanji/矛.md:28–30` | On `ぼう` | The article supplies only KANJIDIC2 recognition support for ボウ. JMdict 1531090 supports ム in 矛盾 and 1603450 supports ほこ; neither supplies a ボウ lexical example. |
| `kanji/彗.md:28–32` | On `え`, `けい` | Both are expressly source-only here. The supplied Kanjipedia observations corroborate their character-reading status; JMdict 1566680 establishes スイ in 彗星, not these alternatives. Their inclusion among the first three keys is not justified merely by dictionary recognition. |
| `kanji/漱.md:28–36,42` | On `しゅう`, `す`; kun `くちそそぐ` | All three are explicitly unsupported by an established lexical example in this lesson. JMdict 2033270 supports ソウ, 2261070 supports くちすすぐ, and 1577660 supports rare spelling 漱／うがい. None supplies the disputed forms. |
| `kanji/栞.md:28–29` | On `かん` | カン is corroborated as a character reading, but the article supplies no ordinary compound example. JMdict 1568040 supports しおり. Character-reading validity alone does not settle the suitability of an unqualified カン study prompt. |
| `kanji/莉.md:28–32` | On `らい`, `れい` | Both lack lexical examples here. KANJIDIC2 preserves both; supplied Kanjipedia observations corroborate レイ but do not provide an example. JMdict 1641120 and 1909630 support the plant words using リ, not these additional prompts. |

**Learning impact:** Learners may be tested on a reading the lesson itself presents only as source lookup, without a usable lexical anchor or adequate context for its restricted status. In 漱, the first-three cap also leaves the lexically supported **すすぐ** outside the offered kun keys while retaining unestablished **くちそそぐ**.

**Remedy:** Under content issue **#1**, require an explicit curated-reading compatibility decision before accepting these seven cards’ reading prompts. The narrow companion prerequisite is to distinguish preserved dictionary metadata from readings approved for learner-facing prompting, with necessary contextual qualification for recognition-only material. Preserve metadata identities and order; do not silently drop/reorder entries, invent examples, or regard prose warnings as implemented filtering.

A decision to retain any disputed key must justify its educational use, not merely repeat that a character dictionary lists it. This report does not implement or prescribe a broader quiz feature.

**Confidence:** High for the projection and evidence gap; medium-high for the suitability judgment. Absence of a supplied lexical example is **not** proof that no example exists.

### Explicit assessment of all projected reading sets

| Kanji | Exact supplied projection: on / kun | Assessment |
|---|---|---|
| 幹 | `かん` / `みき` | Defensible lexical support. |
| 氏 | `し` / `うじ` | Defensible; suffix dash deduplication does not create an additional sound. |
| 扱 | `そう, きゅう` / `あつかい, こく` | **Prerequisite required** for on keys. The kun keys have lexical support. Collapsing あつかい/あつかう/あつかる is mechanical deduplication, not lexical verification of あつかる. |
| 乃 | `ない, だい, の` / `の, すなわち, なんじ` | **Prerequisite required** as detailed above. ない has useful lexical support; だい has explicitly dated support in 乃公; すなわち has a documented rare spelling. |
| 凹 | `おう` / `くぼむ, へこむ, ぼこ` | Defensible for recognition; ぼこ is appropriately explained as bound use in 凸凹, not an unrestricted standalone noun. |
| 凸 | `とつ` / `でこ` | Defensible lexical support, including usually-kana でこ. |
| 矛 | `む, ぼう` / `ほこ` | **Prerequisite required** for ぼう; other keys supported. |
| 鷹 | `よう, おう` / `たか` | Defensible lexical support through 放鷹, 鷹揚 and 鷹; no frequency claim inferred. |
| 彗 | `すい, え, けい` / `ほうき` | **Prerequisite required** for え/けい. ほうき is supported as a recognition spelling, not established as preferred orthography. セイ is preserved in metadata but not offered. |
| 漱 | `そう, しゅう, す` / `くちすすぐ, くちそそぐ, うがい` | **Prerequisite required** for the three disputed keys. Rare spelling and recognition status remain relevant even for supported keys. |
| 栞 | `かん` / `しおり` | **Prerequisite required** for かん; しおり supported. |
| 莉 | `り, らい, れい` / none | **Prerequisite required** for らい/れい; リ supported in the plant compounds. |

No additional demonstrated content defects were established.

## Optional

Nonblocking polish: `kanji/彗.md:20,32` could link the existing `words/箒.md` article when prioritizing ordinary broom vocabulary. Its present unlinked spelling guidance is understandable and is not a coverage blocker.

## Limits

- The seven cards’ reading-prompt suitability is **not accepted** by this review. Their accurate text disclosures do not resolve app behavior.
- Public-dictionary observations were **coordinator-supplied evidence**, not my independent live retrieval. No web retrieval was performed.
- Relevant supplied extraction limits remain: the dedicated 乃／なんじ page and both dedicated 漱ぐ word pages yielded copyright text only; usable evidence came from inspected character-page headings/navigation. The 氏 observation relies on the named Japanese-dictionary/encyclopedia sections, not an empty Digital Daijisen heading. The misdirected 乃 URL and unsuitable Weblio 氏 result supply no verification.
- Frozen dictionary families support written forms, readings, flags and senses; they do not independently certify the authored example sentences or establish frequency. No consequential example defect was established.
- The exact export identity and absence of uncommitted teaching are supplied snapshot facts, not independently recomputed hashes or Git verification.
- This is not certification of the repository, an official JLPT syllabus, personal-name readings, or historical derivations.
- **Textual phone comprehensibility only:** no physical-phone, native-speaker, selection/session/article/Back, drawing, stroke-guide execution or all-40-font acceptance evidence was obtained or claimed.