## Snapshot: 6102eb03c5be228d73a5584972bcbd88d138c60c; committed content only

Parent: `09310e308ec2becf8ab405f8be37bc57188a1b56`.

The frozen receipt identifies **18 physically new articles and two unchanged reuses**. 混ぜる is the batch79 reuse; または is the original-baseline N4 reuse. The packet’s 19 baseline-relative `newArticles` paths are consistent with that distinction.

The commit association is supplied evidence: file tools cannot execute Git, so I could not independently verify the commit, worktree cleanliness, hashes, or rendering equivalence.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Review was read-only and serial, without agents, delegation, edits, or concurrent work.

I read completely:
- All twenty assigned word articles; all three related kanji bodies; `related.patch`; the older related-kanji rendering; both reused articles’ older bodies.
- All **20 mappings, 20 complete principal families/35 senses, 30 complete component records, and 262 comparison-label records**, using the required complete JSONL ranges.
- All fourteen family-inspection chunks and the five extra comparison families. Their supplied deduplicated union is **331 families/870 senses**, not the entire available 479/1231.
- All twenty-one older-body renderings containing 164 articles; the four direct comparison bodies 出会い, 横切る, 横断, 解決; and five additional bodies 完了, 終了, 合う, たちまち, 直に: **173 distinct comparison/reuse bodies**.
- The complete public capture text: twenty positive lexical captures from **Digital Daijisen via Weblio, one authority**. I excluded the unrelated classical 急ぐ／速ぐ heading from またぐ’s evidence.

I also read the requested instructions, `content-format.md:18–103`, the TSV header and **only lines 1582–1601**, both repository snapshot documents, and `confusable-words.md:1–150`. Targeted searches checked actual component-card existence and relevant declarations. No prohibited ledger, rationale packet, reviewer report, or unpermitted private file was read.

## Verdicts:

**Five articles need quiz-exclusion corrections.** I established no separate defect in their definitions, selected-sense coverage, examples, or comprehensibility. Missing guards are classified below as **Correctness** defects because they permit defensible answers to be treated as wrong.

CLEAN means no actionable defect established within this review’s scope, not exhaustive certification.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
| --- | --- | --- | --- | --- | --- |
| N2:1582 | 混ぜる ← 交ぜる | CLEAN | CLEAN | CLEAN | Unchanged reuse; same-entry spelling explicitly recognized; transitive construction preserved. |
| N2:1583 | またぐ | CLEAN | CLEAN | CLEAN | Both selected 跨ぐ senses taught; godan forms and crossed-object を are clear. |
| N2:1584 | または ← 又は | CLEAN | CLEAN | CLEAN | Unchanged N4 identity; written reading または retained, with pronounced わ explained. |
| N2:1585 | 待合室 | CLEAN | CLEAN | CLEAN | Waiting-room meaning, mixed native-first formation, and existing component links are sound. |
| N2:1586 | 待ち合わせる | CLEAN | CLEAN | CLEAN | Prior arrangement and practical 人と／場所で／時刻に frames are clear; both dictionary transitivity labels acknowledged. |
| N2:1587 | 街角 | CLEAN | CLEAN | CLEAN | Street corner and まちかど taught; primary metadata includes 街 despite its absent card. |
| N2:1588 | 真っ暗 | NEEDS FIX | CLEAN | CLEAN | Missing secondary-sense quiz guard against 終わる: B80-01. |
| N2:1589 | 真っ黒 | CLEAN | CLEAN | CLEAN | Black, tanning, and black-with-dirt senses distinguished without making dirt or tanning universal. |
| N2:1590 | 真っ青 | CLEAN | CLEAN | CLEAN | Deep blue and ghastly pale covered; whole reading まっさお correctly explained. |
| N2:1591 | 真っ先 | CLEAN | CLEAN | CLEAN | First/foremost uses and practical 真っ先に attachment are clear. |
| N2:1592 | 真っ白 | CLEAN | CLEAN | CLEAN | White and blank covered; obsolete ましろ correctly restricted to 真白. |
| N2:1593 | 祭る | NEEDS FIX | CLEAN | CLEAN | Ritual teaching and deity/spirit を are sound; missing 敬う guard: B80-02. |
| N2:1594 | 窓口 | CLEAN | CLEAN | CLEAN | Service-counter and contact-person senses are both practical and comprehensible. |
| N2:1595 | まとまる ← 纏まる | NEEDS FIX | CLEAN | CLEAN | All three selected senses and intransitivity taught; guard omissions: B80-03, B80-04. |
| N2:1596 | まとめる ← 纏める | NEEDS FIX | CLEAN | CLEAN | All four selected senses and transitivity taught; guard omissions: B80-03, B80-04. |
| N2:1597 | 真似る | CLEAN | CLEAN | CLEAN | Imitation, object marking, forms, and contrasts with 倣う／似る are clear. |
| N2:1598 | まぶしい | CLEAN | CLEAN | CLEAN | Literal glare and figurative radiance covered; recognized spellings/readings do not become invented frequency rules. |
| N2:1599 | まぶた | CLEAN | CLEAN | CLEAN | Eyelid meaning and spelling flags handled correctly; 上まぶた is correctly うわまぶた. |
| N2:1600 | マフラー | CLEAN | CLEAN | CLEAN | Warm scarf and exhaust muffler covered; garment contrasts remain tendencies, not absolute rules. |
| N2:1601 | まもなく ← 間も無く | NEEDS FIX | CLEAN | CLEAN | Source spelling and separate verb-attachment recognition taught; missing 直に guard: B80-05. |

**Kanji and baseline preservation:** All three kanji receive **CLEAN / CLEAN / CLEAN** for correctness, scoped coverage, and comprehensibility within the supplied evidence.

- **角:** The patch adds 街角 to the かど row and common words, and adds entry `1204580` to the citation list. YAML metadata and unrelated teaching remain unchanged.
- **祭:** The patch links the existing 祭る reading example and verb note, and adds its common-word link. Metadata and unrelated teaching remain unchanged.
- **混:** The current body matches the supplied older rendering and retains 混ぜる navigation. No change is represented in the patch.

Both reused word bodies preserve their prior teaching and metadata in the supplied comparisons. In particular, または retains `jlpt: 4`, its identity, title, and `reading: または`. Independent Git-level unchanged status remains unverified.

**Components and reciprocal links — CLEAN across all three facets:** All sixteen distinct primary written Han are represented in word metadata. Every primary component with an existing card is linked; 街 correctly remains unlinked because no `kanji\街.md` exists. Existing lower-level links are substantive, including 待／合／室, 真 and the colour/darkness components, 窓／口, 似, alternative-spelling 交, and 間. Kana-primary cards correctly retain `kanji: []`.

The new primary N2 pairs **街角 ↔ 角** and **祭る ↔ 祭** are reciprocal. The existing **混ぜる ↔ 混** pair is also reciprocal and preserved.

**Mappings — CLEAN across all three facets:** All twenty source rows agree with their mappings and applicable principal families. This includes 交ぜる → 混ぜる (`1290310`), 又は → または (`1524990`), 纏まる／纏める → kana-primary cards, and 間も無く → まもなく. Blank raw kanji fields were not treated as proof that dictionary spellings do not exist. Additional recognition—especially まもなく’s second sense—was assessed separately, without assigning it an independent N2 level.

## Findings:

**B80-01 — Medium; Correctness; `words\真っ暗.md:9`.**

The exclusion list omits **終わる**, whose ordinary colloquial secondary meaning can answer the unqualified title “utterly hopeless.” Neither card declares the pair. This can create a defensible alternative in meaning quizzes; the fact that the older body concentrates on ending/finishing does not remove the secondary meaning.

**Minimal remedy:** Add `終わる` to 真っ暗’s exclusions.

**Exact evidence:** 真っ暗’s title at line 4 and principal `1363190:2`, “utterly hopeless”; complete family `1589600:5` in `family-inspection-10.txt`, “to be hopeless,” marked colloquial and used as 終わって(い)る. The complete older 終わる body has no reverse guard. This is a quiz safeguard, not a request to expand the N2 lesson. **Confidence: high.**

**B80-02 — Medium; Correctness; `words\祭る.md:9`.**

The list omits **敬う**. Its full title is “respect; revere,” but its complete principal sense explicitly includes worship. Consequently, “enshrine; worship” is not a reliably wrong English choice for 敬う. This is a direct worship overlap, not merely shared religious subject matter.

**Minimal remedy:** Add `敬う` to 祭る’s exclusions.

**Exact evidence:** Selected `1295250:2`, “to pray; to worship”; complete `1250700:1` in `family-inspection-03.txt`, including “to revere,” “to honour,” and “to worship.” `words\敬う.md:9` excludes 尊敬／敬意／尊重, not 祭る. **Confidence: high.**

**B80-03 — Medium; Correctness; `words\まとまる.md:9`; `words\まとめる.md:9`.**

Both lists omit **完了**, despite their selected completion/finalization meanings. 完了 is an existing card titled “completion”; its body explicitly teaches both a process finishing and someone completing it. These are direct overlaps, not a blanket noun/verb association.

**Minimal remedy:** Add `完了` to each list.

**Exact evidence:** `1611640:1` includes “to be completed,” also explicitly taught at `words\まとまる.md:16–18`; `1440930:3` includes bringing something to a conclusion/finalizing. `words\完了.md:4,15–20` teaches completion and both が／を constructions. The complete 日本国語大辞典 **かんりょう** entry additionally defines finishing completely or completing something. Existing guards against 完成 do not establish either missing direct edge to 完了; identical-title deduplication is not transitive exclusion protection. **Confidence: high.**

**B80-04 — Medium; Correctness; `words\まとまる.md:9`; `words\まとめる.md:9`.**

Three direct combining/joining overlaps remain unguarded: **まとまる／合同**, **まとめる／合同**, and **まとまる／合流**. The actual older bodies teach merger into one body and people/groups joining, not just joint-event terminology or rivers. “Come together” is a defensible answer for those uses; “put together” also overlaps 合同’s transitive combining sense.

**Minimal remedy:** Add `合同` to both lists and `合流` to まとまる’s list. These judgments do **not** imply a blanket exclusion clique.

**Exact evidence:** `1611640:2–3` covers being brought together/unified; `1440930:1` covers integration, consolidation, and unification. Complete `1285140:1` includes combination, union, joining, merger and fusion, with transitive/intransitive する labels; `1285390:2` covers joining people/groups and linking up. See also `words\合同.md:16–26` and `words\合流.md:16–25`; neither older declaration supplies the missing reverse edges. **Confidence: high.**

**B80-05 — Medium; Correctness; `words\まもなく.md:9`.**

The list guards **直**, but not the distinct ID **直に**. The written choice 直に also represents ordinary **じきに**, “soon/shortly,” explicitly recognized in that older card. Thus an unqualified “soon; shortly” prompt can have another defensible Japanese answer. This is semantic overlap through a recognized reading, not homophony alone.

**Minimal remedy:** Add `直に` to まもなく’s exclusions; preserve 直に’s primary じかに identity.

**Exact evidence:** `1215290:1`; complete `1430700:1` in `family-inspection-08.txt`, including “soon” and “shortly”; `words\直に.md:35` explicitly contrasts じかに with じきに and gives じきに着く, “arrive soon.” Its complete body has no reverse exclusion. **Confidence: high.**

## Optional:

None required. I established no actionable exclusion excess. In particular, complete evidence prevents dismissing 渡す merely as “hand over,” 頭 merely as a body part, or 空 merely as the primary そら reading: their additional meanings matter. Different transitivity or lexical category alone was not used to approve or reject a guard.

## Limits:

Git identity, hashes, cleanliness, and compact-rendering equivalence were **not independently executed checks**. Preservation judgments are based on the supplied receipt, complete older renderings, current bodies, and precise patch.

I did not inspect the remaining advertised dictionary families or the entire vocabulary corpus. The review does not certify frequency claims, native-speaker naturalness in every context, or corpus-wide quiz uniqueness.

Supplementary retrieval of 完了 from Weblio returned licensing wrappers only; a numeric Kotobank URL resolved to an unrelated entry. Neither counted as verification. The successful term-resolved Kotobank page supplied the complete **日本国語大辞典 かんりょう** entry; its separate Daijisen **ワンラ** heading was not imported. The twenty supplied positive captures remain evidence from one authority, not twenty independent dictionaries.
