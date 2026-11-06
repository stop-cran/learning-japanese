## Snapshot

Supplied signed snapshot: `0f7f20e93b1e20cbc9943011e9ac69b20f75086e`. Signature, Git contents and worktree state were **not independently verified**.

Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`; no delegation or other reviewers’ reports consulted.

## Scope

Read the entire assigned packet in **one `view` call**, using `forceReadLargeFiles=true` without `view_range`. The response exposed the packet through its final bounded inventory, with no truncation indication; no recovery reads were needed. The supplied resource is identified as 218,080 bytes/5,364 lines; those counts were not independently measured.

Fresh review covered:

- Complete NEW `kanji\冠.md`, lines 1–55.
- Complete NEW `words\王冠.md`, lines 1–43.
- Complete reused `words\冠.md`, lines 1–36, including its activated component link.
- Exactly the added Common words line in `kanji\王.md`, original line 39. Unchanged 王 teaching was context, not a fresh full review.

Supporting material read included all 13 complete comparison articles—冗/完/守/帽/元/帽子/蓋/栓/被る/トップ/最高/王/カバー—all **177 distinct complete JMdict families**, five complete raw character records, the pinned SVG and geometry, runtime diff, source metadata, supplied public dictionary observations and included contract extracts. These are **supplied evidence**, not independent upstream retrieval.

## Verdicts

| Assignment | Correctness | Scoped coverage | Phone-TEXT comprehensibility |
|---|---|---|---|
| NEW `kanji\冠.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| NEW `words\王冠.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| Reused `words\冠.md`, complete article and navigation change | **UNVERIFIED**¹ | **CLEAN** | **CLEAN** |
| `kanji\王.md`, added line 39 only | **CLEAN** | **CLEAN** | **CLEAN** |

**CLEAN** means no actionable defect established within this bounded review, not exhaustive correctness.

¹ The reused article’s linguistic teaching and navigation establish no actionable defect. Its N2 metadata is demonstrably preserved, but the packet does not expose an independent vocabulary-level source record establishing that assignment.

### NEW `kanji\冠.md`

**Correctness:** Full and selected readings match the frozen character record: onyomi `[カン]`, kunyomi `[かんむり]`; offered stems are therefore `かん` and `かんむり`. Each selected reading has its own row and linked example. 王冠 is the exact lexical item おうかん, allocated **王 オウ + 冠 カン**; 冠 かんむり is the native noun, not the pronunciation of the peerless construction.

Nine strokes, radical **冖/14**, and grade 8 agree with the raw record. N1 membership is supported by frozen community source row **88**, not by treating KANJIDIC’s legacy JLPT field as a modern syllabus.

**Coverage:** Headgear, kanji-top terminology and restricted formal 世界に冠たる are sufficiently distinguished. The complete families do not justify importing archaic variants, title-counting, unrelated specialized compounds or additional word readings into the frozen character-reading lists.

**Text comprehensibility:** The explanation distinguishes actual 冖 from 宀’s added upper dot. 元/寸 and 冗/完/守 comparisons are modern-shape comparisons; the mnemonic is explicitly invented. No unsupported etymology or phonetic analysis is asserted.

### NEW `words\王冠.md`

**Correctness:** The general-word family supports おうかん and both crown and bottle-cap senses. Supplied Daijisen observations additionally support awarded crowns and the metal beer-bottle closure. The body appropriately narrows “bottle cap” to a **crown-type metal closure**, rather than every lid or screw cap.

Both example readings and translations fit their sentences. 王冠をかぶっています describes wearing; 瓶の王冠を外しました naturally describes removing the closure. The putting-on/wearing distinction and modifier–head explanation are sound. No vocabulary JLPT level is inferred or declared.

**Coverage:** Royal versus awarded crowns, the separate closure sense, broader related nouns and the prohibition against transferring 冠たる to 王冠 meet the article’s practical scope.

**Text comprehensibility:** The two examples explicitly separate headgear from household objects, with complete kana readings and translations. The broad heading gloss is adequately qualified by the nearby definition and final restriction.

### Reused `words\冠.md`

**Correctness:** The supplied complete family supports ceremonial headgear and crowns, **かんむり-restricted** kanji-top and sponsorship/title uses, and **かん-restricted** peerless teaching. 世界に冠たる技術 and its reading/translation are appropriate; the article does not pronounce that meaning かんむり or present unrestricted substitution for “best.”

The original gold-crown example retains correct readings, including 金 **きん**, and natural かぶっていました. Stable identity, primary **かんむり**, wago classification, N2 field and all eight original guards remain unchanged.

**Coverage:** The complete article adequately separates its primary noun from supplementary reading-specific teaching. The navigation-only change does not require adding every dictionary branch or another example quota.

**Text comprehensibility:** Reading labels and the explicit supplementary-use warning prevent the main semantic confusion. The new link has a substantive, understandable anchor and preserves the original explanation.

### Added `kanji\王.md` line 39

**Correctness:** 王冠 おうかん and its two qualified meanings agree with the word article and supplied dictionaries.

**Coverage:** This is a useful reciprocal Common words addition; it does not alter 王’s readings, level or existing teaching.

**Text comprehensibility:** The complete reading and “crown-type bottle cap” qualification make the line understandable without suggesting that 王 alone means a bottle closure.

### Quiz and reciprocal-link audit

The three curated kanji wrong choices have the actual displayed titles **冗 “superfluous; redundant,” 完 “complete,” 守 “guard; obey.”** Their supplied ordinary and secondary senses establish no competing “crown; peerless” answer. 完’s shared カン does not itself establish safety; its meanings were considered separately. Related **帽 “hat; headgear”** overlaps and appropriately remains a comparison rather than a curated wrong answer.

No competing answer was established among the supplied legacy default-four labels: person; rest; what; enter/put in; go out/exit; mouth; woman/female; sun/day; moon/month; man/male; buy. This does **not** certify larger or random pools.

NEW 王冠 retains exactly the direct exclusions **冠/帽子/蓋/栓**. Reused 冠 retains **帽子/名前/名/題/最高/いちばん/一流/トップ**. The headgear, naming and ranking overlaps justify preserving these protections. Secondary senses were considered, including 栓’s flow-control sense, トップ’s leadership/home-page senses and 帽子’s restricted Go use; these neither erase genuine overlap nor make every related term interchangeable. No additional actionable exclusion defect was established. Exclusions are direct pairs, **not transitive cliques**.

All three mapped pairs have both textual directions:

| Pair | Kanji → word | Word → kanji |
|---|---|---|
| 冠 / 冠 | `kanji\冠.md:23,36,40` | `words\冠.md:25` |
| 冠 / 王冠 | `kanji\冠.md:23,35,41` | `words\王冠.md:25` |
| 王 / 王冠 | `kanji\王.md:39` | `words\王冠.md:25` |

Thus all **six directions** are present, including the activated existing component link and the older 王 card’s addition. No incidental-mention backlink requirement was imposed.

## Findings

**None established as proven actionable defects.** The N2 source-provenance uncertainty is recorded below rather than misreported as an incorrect level or silently marked CLEAN.

## Optional

`words\冠.md:33`: adding “formal” before the 冠たる explanation would align its register wording with `kanji\冠.md:46`. This is nonblocking polish, not an established teaching error.

## Limits

- **N2 vocabulary provenance:** `words\冠.md:5` retains `jlpt: 2`, and the diff confirms preservation. However, the included extracts provide no independent vocabulary-source row establishing N2. An exact source record is needed to close that specific correctness uncertainty; the kanji’s N1 classification cannot supply it.
- No independent Git/signature/hash, upstream dictionary, community-list or KanjiVG retrieval was performed. Public dictionary observations remain coordinator-supplied evidence.
- The SVG and geometry text support nine ordered strokes: 冖 first, 元-shaped strokes next, then 寸. Their organization agrees with the shape explanation. Converter equality or matching coordinates would **not** establish successful native drawing.
- Supplied font evidence says exact 冖/宀 are absent from the three main-font cmaps and outside RareHan ranges. That establishes neither rendering failure nor successful fallback. Native font display, stroke interaction and route acceptance remain unverified.
- Phone verdicts concern **text only**. This report provides no native-speaker, process, physical-phone, font, drawing, live-app or release certification.
- No edits were made.
