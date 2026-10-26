## Snapshot: c2e4e07abeda5bd28c12d0b3f9b0102212d2ae88; committed content only

Parent: `bc3244fc7256c83e9c44499a65e6b85d586ae0aa`.

**Result: three missing English-label quiz safeguards; no actionable Japanese-teaching, mapping, component-metadata, or baseline-preservation defect established.** The commit identification comes from `frozen-snapshot.json`, not an independently executed Git check.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Read-only review, with serial tool calls and no edits, agents, delegation, or concurrent work.

Completely read all twenty assigned articles; the required instruction documents and content-format range; the TSV header and exactly physical lines 1622–1641; all twenty mappings, twenty complete principal families, 33 complete component records, and 290 comparison labels/exclusions. Reviewed spelling/reading restrictions, flags, inherited POS, raw source fields, and one-based selected senses separately from additional recognition.

Also completely read all fifteen family-inspection chunks: **370 families/941 senses**, including the twenty principals. Four additional complete families—果実, 果物, 確かめる, 肌—bring actual inspection to **374 distinct families/949 senses**, not the 515 prepared families. Read all twenty older-body chunks containing 159 complete bodies, plus the actual articles 知る, 確かめる, 皮, 実, 果物, 果実, 皮膚, and 肌: **167 complete baseline/comparison bodies**, including both reused baselines. Labels were not counted as body reads.

Read the current and baseline 蒸 kanji bodies, complete `related.patch`, CW091 lines 260–264, the allowed snapshot/JLPT documents, and both public-bodies files completely. The public captures supply nineteen applicable positive Digital Daijisen bodies through Weblio—**one Japanese dictionary authority**—and one failed 向う lookup. Independently fetched American Heritage entries for **sticky, close, fruit, skin, and check**.

The large `review-evidence.json` was read only for its introduction and the four additional complete families. Not all prepared families or all comparison articles were inspected. No prohibited ledgers, author rationale, scripts, inputs, checks, or reviewer reports were read.

## Verdicts:

`Correctness` includes quiz-answer correctness. The three NEEDS FIX judgments below concern missing guards, not incorrect Japanese definitions.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1622 | 見慣れる | CLEAN | CLEAN | CLEAN | Visual familiarity and resultant 見慣れている are distinguished; ordinary comparator senses considered. |
| N2:1623 | 醜い | CLEAN | CLEAN | CLEAN | Appearance and disgraceful conduct are appropriately separated; rare spelling qualified. |
| N2:1624 | 実る | NEEDS FIX | CLEAN | CLEAN | Godan/intransitive teaching and successful fruition are sound; missing “fruit” label guards, GPT-01. |
| N2:1625 | 身分 | CLEAN | CLEAN | CLEAN | Status, identity/origin, and circumstances/means remain distinct rather than unrestricted synonyms. |
| N2:1626 | 見本 | CLEAN | CLEAN | CLEAN | Sample/model coverage and mixed native-plus-on reading are comprehensible. |
| N2:1627 | 見舞う | CLEAN | CLEAN | CLEAN | Welfare visits/written inquiries and striking/disaster constructions are appropriately scoped. |
| N2:1628 | 未満 | CLEAN | CLEAN | CLEAN | Exact boundary exclusion is explicit; raw “insufficient” is not overgeneralized. |
| N2:1629 | 名字 | CLEAN | CLEAN | CLEAN | 苗字 recognition and surname/given-name distinctions are adequate. |
| N2:1630 | ミリ | CLEAN | CLEAN | CLEAN | Metric prefix and millimeter abbreviation are separated; unrelated city heading excluded. |
| N2:1631 | 診る | NEEDS FIX | CLEAN | CLEAN | Medical meaning, particles, and conjugation are sound; missing 確かめる guard, GPT-02. |
| N2:1632 | 民間 | CLEAN | CLEAN | CLEAN | Nongovernmental/private-sector and folk uses are distinguished from secrecy or generic popularity. |
| N2:1633 | 民謡 | CLEAN | CLEAN | CLEAN | Traditional/community-song scope appropriately qualifies the source’s “popular song.” |
| N2:1634 | 向かう, source 向う | CLEAN | CLEAN | CLEAN | Correct むかう identity; N4 and original teaching retained. |
| N2:1635 | むく, source 剥く | NEEDS FIX | CLEAN | CLEAN | 剥く/剝く, usually-kana status, and both senses are taught; missing skin/peel guards, GPT-03. |
| N2:1636 | 無限 | CLEAN | CLEAN | CLEAN | Infinity and limitless modification are distinguished; の/な guidance is supported. |
| N2:1637 | 無地 | CLEAN | CLEAN | CLEAN | Patternless/solid-colored meaning and の attachment avoid misleading “plain” generalizations. |
| N2:1638 | 蒸し暑い | CLEAN | CLEAN | CLEAN | Heat plus humidity, adjective forms, spellings, and 蒸 relationship are clear. |
| N2:1639 | 矛盾 | CLEAN | CLEAN | CLEAN | Intransitive する construction and attributed spear/shield account are appropriately presented. |
| N2:1640 | 蒸す | CLEAN | CLEAN | CLEAN | Sourced N2 added without changing the original teaching or exclusions. |
| N2:1641 | 無数 | CLEAN | CLEAN | CLEAN | の/な attachment and countless quantity avoid a rigid finite-versus-infinite rule. |

**Mappings — CLEAN in all three facets.** All twenty source associations identify the applicable lexical families and meanings. In particular, 向う/むかう maps to entry **1604800**, not むこう entry 1277140; 剥く maps to usually-kana むく entry **1474370**, not 向く. Additional recognition is not treated as a separate N2 assignment to every sense. Blank raw kanji fields were not treated as proof that dictionary spellings are absent.

**Components and navigation — CLEAN in all three facets within inspection.** Written primary Han characters are represented in metadata, including 蒸し暑い’s `[蒸, 暑]`. Kana-primary むく legitimately retains `kanji: []` while teaching its recognized spellings. The bounded component-card existence check found nineteen cards among the 33 component characters; useful existing component links are present. No nonexistent character-card links are demanded.

**Baselines, kanji, and related links — CLEAN in all three facets on textual comparison.** 向かう retains its word, reading, title, N4 level, and old teaching; its additions are source-spelling recognition and direct safeguards. 蒸す differs from its complete baseline only by `jlpt: 2`, preserving its entire body, title, reading, and exclusions. 蒸 retains its metadata and unrelated teaching; the additions are 蒸し暑い in the reading/common-word lists and its dictionary reference. Both **蒸し暑い↔蒸** and existing **蒸す↔蒸** reciprocal pairs are present. CW091 is a correct link-only change.

**Existing guards:** no actionable excessive guard established. Independently inspected American Heritage weather senses support the “sticky” and “close” safeguards without making the Japanese comparison words weather synonyms. Existing reverse declarations were honored, including 向く/向かう, 対する/向かう, 無数/無限, and 湿気/蒸す; no transitive clique completion was assumed.

## Findings:

**GPT-01 — Minor; Correctness (quiz); `words\実る.md:9`. Missing direct guards against English “fruit” labels.**

The complete counterpart titles are `fruit; substance` in `words\実.md:4`, and `fruit` in `words\果物.md:5` and `words\果実.md:4`. None directly excludes 実る. These are genuinely different Japanese noun identities, but **English “fruit” is also a verb meaning to produce fruit**, making it a defensible answer to 実る’s physical sense. This is English-label ambiguity, not a claim that the Japanese nouns replace the verb.

**Minimal remedy:** add `実`, `果物`, and `果実` to 実る’s direct exclusions. 果物 and 果実 having identical titles deduplicates those two choices; it does not deduplicate `fruit` against 実る’s distinct `bear fruit; yield results` title.

**Exact evidence:** `words\実る.md:16–24`; complete JMdict 1320850 sense 1 and complete counterpart families 1320810, 1193060, 1192940; all three actual counterpart bodies; independently fetched [American Heritage, fruit](https://www.ahdictionary.com/word/search.html?q=fruit), intransitive/transitive verb definition. **Confidence: high.**

**GPT-02 — Minor; Correctness (quiz); `words\診る.md:9`. Missing 診る/確かめる safeguard.**

確かめる’s complete title is `check; make sure`, and its direct exclusions are only 確認 and チェック (`words\確かめる.md:4–9`). 診る explicitly includes checking a patient’s condition or pulse and translates 脈を診てください as “Please check my pulse” (`words\診る.md:16–20`). Consequently, the existing `check; make sure` label can be a defensible alternative for this taught use. Its guards against 確認 and チェック do **not** transitively protect 診る.

**Minimal remedy:** add `確かめる` to 診る’s exclusions. Do not broaden 診る into a general-purpose checking verb.

**Exact evidence:** complete principal JMdict 1365450 sense 1; complete 確かめる family 1205780, sense 1, in `batch-82-review-evidence.json:9698–9756`; actual complete articles; applicable marked medical sense in the captured Daijisen みる entry; independently fetched [American Heritage, check](https://www.ahdictionary.com/word/search.html?q=check), transitive senses 1a–b. **Confidence: high.**

**GPT-03 — Minor; Correctness (quiz); `words\むく.md:9`. Missing direct guards against “skin”/“peel” labels.**

The actual counterpart titles are `skin; peel; outer covering` for 皮, `skin` for 皮膚, and `skin; surface texture` for 肌 (`words\皮.md:4`, `words\皮膚.md:4`, `words\肌.md:4`). Neither side directly guards these pairs. むく explicitly teaches peeling/skinning (`words\むく.md:16–17`); English **“skin” is also a transitive removal verb**. In particular, the bare `skin` label can correctly describe むく even though its owning article teaches the anatomical noun. 皮 additionally supplies the shared English form “peel.”

**Minimal remedy:** add `皮`, `皮膚`, and `肌` to むく’s exclusions. This safeguards English answers without presenting those Japanese nouns as verb synonyms.

**Exact evidence:** complete principal JMdict 1474370 sense 1, including its usually-kana flag; complete counterpart families 1483800, 1483920, 1476450 and all three actual bodies; independently fetched [American Heritage, skin](https://www.ahdictionary.com/word/search.html?q=skin), transitive senses 1 and 3. **Confidence: high.**

## Optional:

None. Omitted rare, historical, specialist, and unrelated-wrapper senses are not themselves scoped-coverage defects.

## Limits:

File tools cannot execute Git. I did **not** independently verify HEAD, ancestry, worktree cleanliness, committed-file hashes, or packet/repository equivalence. Preservation judgments are textual comparisons of the supplied baselines, current files, and patch—not author hash checks relabeled as reviewer checks.

The failed 向う public capture is not corroboration; its mapping judgment rests on the complete pinned dictionary families. The nineteen positive Japanese captures represent one authority, not nineteen independent authorities. Live English lookups were independently inspected but are not frozen snapshot artifacts; author observations and failed Cambridge requests were not treated as verification.

No quiz runtime was executed. Findings apply the supplied symmetric, nontransitive exclusion contract to inspected titles, bodies, and meanings. CLEAN means no actionable defect established within this actual scope, not exhaustive correctness or native-speaker certification.
