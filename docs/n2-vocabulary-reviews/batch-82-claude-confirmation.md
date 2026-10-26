## Snapshot

- **Revised commit:** 6244a236f9ba26870928c7721f16903b367cbdae
- **Parent/authored:** c2e4e07abeda5bd28c12d0b3f9b0102212d2ae88
- **Committed content only.** File tools read the working tree and cannot run Git. That the files match the commit, and every hash or preservation check, are the author's assertions, not checks I ran.

## Scope

**Model:** claude-opus-5.5 (claude family). I made no edits and used no shell, agents or delegation.

**Fresh complete reads:**
- **Correction materials:** correction-snapshot.json, correction.patch, related.patch and correction-reconciliation.json.
- **Instructions:** .github\copilot-instructions.md, content-structure.instructions.md, content-format.md:18-103 and confusable-words.md:260-264.
- **Articles:** all 20 assigned articles and the complete kanji\蒸.md.
- **Historical records:** mappings (20), principals (20 families/32 senses), components (33) and labels (290, read as [1,100], [101,200], [201,290]).
- **TSV:** header [1,1] and rows [1622,1641] only.
- **Correction evidence:** correction-principals-and-comparisons.jsonl (44 families) and public-bodies.txt.
- **Older bodies:** all 19 mandatory ones.
- **Extra full bodies:** 原, 野 and 顔, plus a reread of 無地.

**Title and exclusion lines only (grep within words\):**
- 平野, 対する, 向く, 蒸気 and 水蒸気.
- Every "close", "plain" and "face" title.

**Live public fetches (all succeeded):** American Heritage entries for fruit, skin, check, close and sticky, plus two extra entries, plain and face. None of these responses is hashed.

**Not read:**
- Both optional private files.
- The prepared families beyond the 44 + 20 records.
- Bodies of the grep-only cards.

**Scheduling deviations:** two turns each issued three parallel views (見慣れる/醜い/実る and 実/果物/果実). Every other call was serial.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1622 | 見慣れる | CLEAN | CLEAN | CLEAN | A predicate example is optional |
| N2:1623 | 醜い | CLEAN | CLEAN | CLEAN | B82-04 resolved |
| N2:1624 | 実る | CLEAN | CLEAN | CLEAN | GPT-01 guards added; fruit verb confirmed |
| N2:1625 | 身分 | CLEAN | CLEAN | CLEAN | No excessive guard established |
| N2:1626 | 見本 | CLEAN | CLEAN | CLEAN | sample/model titles guarded |
| N2:1627 | 見舞う | CLEAN | CLEAN | CLEAN | |
| N2:1628 | 未満 | CLEAN | CLEAN | CLEAN | Source-gloss prose rewritten for learners |
| N2:1629 | 名字 | CLEAN | CLEAN | CLEAN | |
| N2:1630 | ミリ | CLEAN | CLEAN | CLEAN | City sentence removed |
| N2:1631 | 診る | CLEAN | CLEAN | CLEAN | GPT-02 guard added; check confirmed |
| N2:1632 | 民間 | CLEAN | CLEAN | CLEAN | |
| N2:1633 | 民謡 | CLEAN | CLEAN | CLEAN | |
| N2:1634 | 向かう | NEEDS FIX | CLEAN | CLEAN | B82-06: 顔 guard missing (predates batch) |
| N2:1635 | むく | CLEAN | CLEAN | CLEAN | B82-01/GPT-03 resolved; を role clarified |
| N2:1636 | 無限 | CLEAN | CLEAN | CLEAN | |
| N2:1637 | 無地 | NEEDS FIX | CLEAN | CLEAN | B82-05: 原/野 guards missing |
| N2:1638 | 蒸し暑い | CLEAN | CLEAN | CLEAN | B82-02 withdrawn |
| N2:1639 | 矛盾 | CLEAN | CLEAN | CLEAN | |
| N2:1640 | 蒸す | CLEAN | CLEAN | CLEAN | Only jlpt:2 added |
| N2:1641 | 無数 | CLEAN | CLEAN | CLEAN | Example change deferred |

**Mappings: CLEAN.**
- 向う maps to 1604800 むかう, not 1277140 むこう. Entry 1277140 lists 向う only as irregular okurigana.
- 剥く maps to 1474370, the usually-kana むく. It is not 向く, and the すく heading is separate.
- Both 剥く and 剝く are recognized, without a duplicate card.
- The TSV rows and selected senses are unchanged.

**Components: CLEAN.** All 33 records were checked. Existing cards are linked, and no missing card (for example 身, 醜, 診, 無, 矛, 剥) was invented.

**Reciprocal pairs: CLEAN.**
- New pair 蒸し暑い/蒸: kanji\蒸.md lists 蒸し暑い in the む.す row and in Common words, with entry 1356870.
- Existing 蒸す/蒸 is intact.

**Baseline preservation: CLEAN.**
- 向かう keeps N4, its identity, reading, title, primary kanji and old body. 向こう is linked only in the new alias paragraph.
- 蒸す changes only by jlpt:2.
- The correction does not touch the kanji card or CW091.

## Findings

**Original findings and author dispositions:**
- **B82-01 / GPT-03 — resolved.** むく now guards 皮, 皮膚 and 肌. American Heritage confirms skin as a verb: transitive 1 "To remove skin from" and 3 "remove (an outer covering); peel off".
- **GPT-01 — independently confirmed.** American Heritage lists fruit as a verb: "To produce or cause to produce fruit". The three families stay separate (1320810 実/み, 1193060 果物, 1192940 果実), and じつ/まこと/さね are not the み card.
- **GPT-02 — confirmed.** Transitive check 1a–b is inspect/verify. 診る teaches 脈を診て "check my pulse", and 確かめる is titled "check; make sure".
- **B82-02 — withdrawn** (medium-high confidence). Live American Heritage confirms close adjective 14 ("Warm and humid or stuffy: close weather") and sticky adjective 3 ("Warm and humid; muggy").
  - The six guarded titles contain these words as bare alternatives.
  - The 蒸し暑い article itself teaches this weather English.
  - Qualified titles are correctly left unguarded: 閉める, 締め切る, くっつく, 接近, 側, 近々, 暮れる, 仲良し, 親友, 惜しい, 塞がる, 畳む and 近付ける.
  - This rests on ambiguity in the English labels, not on Japanese synonymy or harmlessness.
- **B82-03 — resolved.** The meta prose is gone. The weather-English explanation, the French-source fact, 剥く/剝く and the usually-kana status are all kept.
- **B82-04 — resolved.** 美しい is linked, and 見憎い is described as a rare spelling of the same adjective.
- **むく object role — resolved.**
- **Adopted polish (実る, 無限, 無数, 未満, 向こう link) — resolved,** with no regressions and the old teaching kept.
- **Deferred items (無数 example, 未満/以内, 見慣れる predicate) — remain optional.**
- **身分/無地 "harmless" remarks — no defect.**

**New findings:**
- **B82-05 — Minor; Correctness (quiz guard); medium-high confidence.**
  - Location: 無地.md:9, with its title at :4 and its English-"plain" note at :39-41; 原.md:4; 野.md:4.
  - Claim: 無地 "plain; patternless" and 原/野 "open field; plain" share the bare word "plain", but no guard links them in either direction.
  - Evidence: American Heritage gives plain adjective 6 "Not dyed, twilled, or patterned" and noun 1a, a level area of land. This is the same English part-of-speech ambiguity accepted for fruit and skin.
  - The article guards the other English meanings it names, "ordinary" (普通, 平凡) and "unshowy" (地味), but not "geographic plain". 平野.md:9 already guards 原 and 野.
  - The original batch introduced this; my original review missed it.
  - Remedy: add 原 and 野 to 無地's quiz_exclusions.
- **B82-06 — Minor; Correctness (quiz guard); medium confidence.**
  - Location: 向かう.md:4 and :9; 顔.md:4 (顔 has no exclusions).
  - Claim: the bare word "face" appears in both titles. American Heritage gives face noun 1a and verbs (transitive 1, intransitive 1).
  - 対する and 向く already guard 向かう; 顔 does not.
  - This predates the batch, and it is not a correction regression.
  - Remedy: add 顔 to 向かう's quiz_exclusions. That is a front-matter change only; the title and body stay untouched.

## Optional

- 名字: the "not read なじ" note adds little.
- 無限: could mention 有限; I did not check whether a 有限 card exists.
- 民謡: the "dictionary translation 'popular song'" wording could be smoother.
- 未満/以内 and a predicate 見慣れる example remain open.
- むく/裸: "bare teeth" is a qualified phrase, so no guard is needed.

## Limits

- **Steam follow-up, unverified:** 蒸す "steam food" against 蒸気 "steam; vapor" and 水蒸気 "water vapor; steam" is unguarded in both directions.
  - I read only the titles and did not fetch the American Heritage "steam" entry.
  - 蒸す is frozen, so any fix belongs on those other cards in a separate pass.
- **Single dictionary authority:** Japanese evidence comes from Digital Daijisen only, and the 向う capture failed.
- **Live captures:** the American Heritage fetches are live and unhashed.
- **Guard history:** I did not verify whether the batch added 向かう's existing guards.
- **No guarantees:** this is not exhaustive correctness, native-speaker certification, a frequency claim or a runtime quiz guarantee.
