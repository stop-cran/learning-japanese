Snapshot: cd5d75d186efa11b89e64e215dbb239a09d93639, compared with a5c6a0ff970ab61e81d82e0d9a1c5ce06d7c96a0. Reviewer: GitHub Copilot, an OpenAI GPT-based assistant; the exact model/version is not exposed.

Scope:
- Read all 26 changed or added files completely: the ten batch kanji cards, 助 and 理, all ten word articles, the ledger, the audit tool, and both JMdict supplement files.
- Read the complete revision patch and changed-line index. Checked changed hunks against correctness, coverage, quiz consistency and comprehensibility.
- Read the supplied JMdict cited entries, relevant dictionary extracts, distractor evidence, reading checks, QuizBuilder.kt and Words.kt. Checked relevant unchanged comparison articles in the original packet.
- Screened all listed forward meaning candidates, including the large noun and verb ties, and all 813 reverse meaning pairs. Independently compared candidate identities with the frozen evidence.
- Inspected actual public dictionary entries, not search snippets. Did not consult other reviewers’ reports.

Dispositions:
- G1 — RESOLVED — The named ordinary kanji overlaps now have direct exclusions. Revised metadata, explanatory notes and ledger rows agree.
- G2 — RESOLVED — The requested secondary-sense guards are present: 併/並, 侍/仕, 侮/卑, 俗/凡・卑 and 倫/伴・輩. The corresponding senses are explained and sourced.
- G3 — RESOLVED — 侍 excludes 武士; the historical samurai sense and comparison match the cited JMdict entries.
- G4 — RESOLVED — 侮る excludes 見下ろす, whose contempt sense is now acknowledged alongside its spatial sense.
- G5 — RESOLVED — 補佐 excludes the requested assistance/helper alternatives. The revised explanation recognizes both the act and the assisting person.
- G6 — RESOLVED — 佳作 excludes 名作, together with the other stated work-related overlaps. Its honorable-mention sense remains represented.
- G7 — RESOLVED — The kanji and word forms of 俵 now guard the named bag/sack overlaps.
- G8 — RESOLVED — 佐’s officer-rank branch and 大佐 たいさ are added and supported by Digital Daijisen and JMdict 1413740.
- G9 — RESOLVED — The vulgar/lowbrow branch and 風俗’s separate industry sense are now explained. Accept the absence of a further example: the inspected candidates do not satisfy the stated common-word rule.
- L1 — RESOLVED — The ledger now supplies a sufficient row-specific justification for 諸侯, including the frequency, missing-爵 and 王侯 distinctions. This is not evidence of coordinator approval.
- L2 — RESOLVED — Manifest, budget and signature evidence is now supplied. This resolves the evidence-availability gap, not independent regeneration or cryptographic verification by this reviewer.

Verdicts:
- correctness — NEEDS FIX — 倫: Finding 1. No other new correctness defect established.
- scoped coverage — CLEAN — All ten batch cards; the source-rule omissions and 諸侯 exception are adequately explained.
- consistency and quiz safety — NEEDS FIX — words\倫理.md: Finding 2. No new collision established among the thirty curated kanji distractors.
- comprehensibility — CLEAN — No actionable new beginner-readability defect established; optional simplifications below.

Confirmation: NEEDS FIX — The earlier points are resolved, but two new minor findings remain.

Findings:

1. **Minor — correctness — `kanji\倫.md:38`: 五倫 is misleadingly reduced to filial piety.**

   The new gloss says “the five Confucian filial-piety relationships.” It faithfully reproduces the pinned JMdict gloss, but teaches an overly narrow meaning. Digital Daijisen enumerates parent–child, ruler–subject, husband–wife, older–younger and friendship relationships. These are not all filial-piety relationships.

   **Impact:** A beginner can incorrectly understand 五倫 as five kinds of parent–child obligation.

   **Remedy:** Use a sourced paraphrase such as “the five Confucian relationships.” Do not silently alter the quoted JMdict entry; distinguish the learner explanation from that quotation.

   **Evidence:** Supplied JMdict entry 1593605; the inspected [Digital Daijisen 五倫 entry](https://www.weblio.jp/content/%E4%BA%94%E5%80%AB), which lists the five relationships.

   **Confidence:** High.

2. **Minor — consistency and quiz safety — `words\倫理.md:8,28`: the new 仁 exclusion is not a direct displayed-meaning overlap.**

   倫理 displays “ethics; morals” and explains general principles governing right and wrong. 仁 displays “benevolence; compassion” and explains one particular virtue. The revised paragraph itself calls 仁 a *related* moral concept; that does not establish two defensible answers.

   **Impact:** The exclusion suppresses a distinguishable comparison because of shared subject matter, contrary to the direct-pair review requirement. This is over-exclusion, not a demonstrated false-answer collision.

   **Remedy:** Remove 仁 from this exclusion row and its corresponding ledger entry, retaining the useful comparison in the body.

   **Evidence:** Both articles’ displayed titles and Meaning sections; supplied JMdict entries 1555390 and 1369620; original rubric lines 111–112. [Digital Daijisen 仁](https://www.weblio.jp/content/%E4%BB%81) describes its Confucian ethical practice, but does not make the displayed “benevolence; compassion” interchangeable with general “ethics; morals.”

   **Confidence:** High for the displayed-title distinction.

Optional:

**Judgments on the ten groups of other-review changes**

1. **Additional word exclusions:** Accept the use-related guards on 併用, the word/vocabulary guards on 俗語, 俊足/速い, and 倫理/道徳. 善 expresses general moral goodness/virtue and is a defensible conservative guard against “morals.” Do not accept 仁 as a direct overlap; see Finding 2.
2. **侮る’s title and translations:** Accept. “Look down on; make light of” is supported, and the revised example translations are readable.
3. **倫’s expansion:** Accept the title, companion branch, 絶倫 and 不倫 explanation. The newly added 五倫 gloss needs Finding 1’s correction.
4. **合併:** Accept. The reading, merger/consolidation gloss and added supplement match cited JMdict entry 1578970.
5. **Word-article revisions:** Accept the placement of 侍’s figurative sense, 俊足’s compound explanation and spelling-restricted gifted-person sense, the restrained 併用 explanation, revised sourced comparisons, and explicit sense-1 citations. The 俊足 dictionary reconciliation is accurate but dense.
6. **王侯 and 俊英 removal:** Accept under the stated qualifying-frequency rule.
7. **Labels, 内侍, あなずる and mnemonics:** Accept. The older-form qualification and historical court-title explanation have support. Removing unsourced mnemonics introduces no coverage defect.
8. **助 and 理:** Accept the attested added readings and repaired metadata. The label needs the clarification discussed below, not a linguistic correction.
9. **Distractor replacement:** Accept semantic and inspected reading safety. Difficulty varies; see the table below.
10. **Source-tied wording:** Accept the rare-spelling qualifications, 併せる/併せて sense restrictions, 俊足 wording, historical 諸侯 label and JMdict noun/counter reading distinction for 俵. “Only reading” must remain understood as the canonical reading restriction in that entry, not denial of contextual びょう/ぴょう variants.

**Curated distractor judgments**

No member of these actual sets was established as another correct meaning answer or an attested target-reading collision.

| Card | Set | Category/difficulty judgment |
|---|---|---|
| 佐 | 母・友・子 | Very easy family/social-role grouping; all nevertheless name people. |
| 佳 | 新・古・短 | Simple descriptive alternatives; clearly different from beauty/excellence. |
| 併 | 分・動・休 | Action/state alternatives; 分’s portion sense does not mean combining. |
| 侍 | 父・母・子 | Strong family-category giveaway; safe but weak discrimination. |
| 侮 | 聞・話・会 | Everyday verbs versus contempt; easy, but not a noun/verb giveaway. |
| 侯 | 国・京・社 | Places/institutions versus a person’s rank; strong category cue. |
| 俊 | 安・少・多 | Simple quality/quantity alternatives; easy, though 安 makes the set less uniform. |
| 俗 | 天・新・名 | Mixed concepts; less category-uniform. |
| 俵 | 田・土・木 | Strong nature-category giveaway; safe but easy. |
| 倫 | 力・事・名 | Mixed abstract nouns; reasonable distinction from moral principles. |

Mixing semantic categories could improve difficulty, especially for 侍 and 俵, but should not sacrifice verified uniqueness.

Accept the stated judgments about 子, 友, 父, 分, 国・京・社, 天, 名, 田 and 事: their inspected senses do not directly supply the target meanings. 多’s source reading まさ.る does not make “many, much” a correct displayed meaning for 俊, and it is not offered for 俊’s inspected on-reading prompt.

The rejected 長/佐 and 社/俗 choices were conservative precautions, not established synonym collisions. Agree that 国/俗 is not a strict clash.

**Remaining word options**

- 諸侯 versus 武士 or 丞相 distinguishes lords from warriors/retainers or chancellors.
- 補佐 versus 代理 or 兼任 distinguishes assistance from representation or concurrent appointments.
- 併用 versus 実用, 応用 or 活用 distinguishes combined use from practical use/application.
- 倫理 versus 原理 distinguishes moral standards from an underlying explanatory principle.
- 佳作 versus 作家/作者 distinguishes a work from its creator; the newly reachable art candidates do not inherently mean a fine work.
- 俗語’s remaining language-related options retain distinguishing meanings, such as subject, honorific expression, compound, terminology and abbreviation. 言語 is the broadest label and deserves particular caution; shared linguistic subject matter alone is not proof of synonymy.
- Screening the remaining listed labels established no additional newly introduced collision. That is not an exhaustive dictionary-sense guarantee.

The independently compared reverse identities confirm six removals and no additions. Only 佳作 gains new forward candidate identities.

**Labels question**

Do **not** mechanically label every unselected batch reading “source-only.” Quiz selection, linguistic rarity and reference coverage are different matters. Retain meaningful qualifications such as rare spelling, older form, kana preference and historical use.

For 助 and 理, “reference reading” would be clearer to a beginner than “source-only here.” Crucially, their unchanged front matter lacks selected-reading overrides: this prose label does **not** disable those readings in the legacy quiz path.

**Phone readability**

Core explanations and example sentences are readable. Shorten the source-reconciliation paragraphs in `kanji\併.md:39` and `words\俊足.md:32` where possible, keeping precise dictionary details in a separate source note.

Limits:
- **No report file was written to the requested destination. No substitute file was created. This message is the complete report.**
- Work remained independent and serial: no parallel tool calls, agents, background jobs, other sessions, recursive listings or corpus scans.
- Candidate screening used bounded read-only regex projections of the large word-quiz file, including in-memory whole-file reads. This departed from the requested line-range method. Automatically generated tool-output artifacts were not opened.
- Supplied logs report 439 passing tests, fresh manifest and satisfactory budgets. I did not rerun tests, regenerate the manifest or independently verify signatures against Git objects.
- The supplied native QuizBuilder.kt implements kanji **meaning** selection; it does not establish native kanji-reading parity. Reading-exposure results come from a Python port. The inspected full pools avoid fallback collisions, but four latent readings remain: 佳 けい・えい, 侍 かみ and 俗 しょく.
- Smaller/custom pools, changed option counts and older clients are not proved safe by these outputs. Word semantic exclusions do not govern reading-option selection.
- The link audit resolved targets, but its quoted-gloss comparison fields were not usable proof of exact equality; consequential glosses were checked manually.
- All listed meaning labels were screened, but not every dictionary sense of every candidate was independently sourced.
- Newly quoted JMdict, KANJIDIC2 and Digital Daijisen material was checked against supplied evidence or actual public entries. The official Joyo PDF was not independently inspected this round.
- Coordinator acceptance of 諸侯, physical-phone usability and native-speaker acceptance remain unverified.