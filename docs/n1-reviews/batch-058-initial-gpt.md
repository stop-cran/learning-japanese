**Snapshot:** Supplied frozen commit `58b53fd31b6d55baba32c049fba62ac739feb004`; no uncommitted teaching included in the requested scope. Git identity, signature and worktree cleanliness could not be independently verified with the permitted tools.

**Scope:** Independent initial review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and phone-text comprehensibility.

Read every assigned local range completely: all five teaching files; comparison kanji `兵・近・共・木・坂・川・出`; comparison words `山・坂・砂・砂漠`; the three guidance files and assigned JLPT guidance; and the complete pinned SVG. Inspected all **68 supplied JMdict families**—42 lexical, 23 comparison and three draft-comparison—and all **11 complete KANJIDIC2 records**, including restrictions, alternative forms and sense-local qualifications. Also inspected scoped confusable-word guidance and actual title/distractor metadata for all 11 assigned legacy fallback cards. No author records or other reviewers’ reports were consulted.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| `kanji\丘.md` — complete new card | CLEAN | CLEAN | CLEAN |
| `words\砂丘.md` — complete new article | CLEAN | CLEAN | CLEAN |
| `words\丘.md` — added component link and 山 exclusion | CLEAN | CLEAN | CLEAN |
| `kanji\砂.md` — added 砂丘 common-word link | CLEAN | CLEAN | CLEAN |
| `kanji\山.md` — added 木 distractor | CLEAN | CLEAN | CLEAN |

For reused files, these verdicts cover the declared changes and tightly coupled behavior; unchanged text was read for context, not certified through unrelated reauthoring. CLEAN means no actionable defect established within this bounded scope.

**Findings:** None.

Supporting conclusions:

- **丘 metadata and reading practice:** Ordered full readings `[キュウ]` / `[おか]`, their explicit practice selections, five strokes, classical radical 一/no. 1 and grade 8 agree with the raw 丘 record. Each selected reading has its own row and correctly linked word model. The SVG contains five stroke paths and identifies the bottom 一 as the traditional radical. The mnemonic is explicitly modern-shape imagery, not etymology. Neither 比丘’s borrowed pronunciation nor archaic つかさ is improperly promoted into metadata.
- **砂丘 language and geography:** JMdict 1291520 supports `砂丘／沙丘`, `さきゅう／しゃきゅう`, and “sand dune; sand hill”; 沙丘’s irregular-kanji label is accurately qualified. サ＋キュウ allocation, modifier-plus-head explanation, Japanese/kana/English examples and particle explanations are sound. Material, landform, desert region and sandy beach remain distinct without claiming exclusive geographical compartments or an absolute mountain/hill height boundary. No vocabulary JLPT level is inferred for 砂丘.
- **Reciprocal navigation:** All three required pairs have both directions: `kanji\丘` ↔ `words\丘`, `kanji\丘` ↔ `words\砂丘`, and `kanji\砂` ↔ `words\砂丘`. Their displayed readings match the linked words.
- **Preservation:** The inspected reused 丘 article retains primary おか, independent N3, its existing title and the 坂 guard, while adding 山. The inspected 砂 and 山 retain their metadata apart from the declared 山 distractor addition. Historical preservation is assessed against the supplied change description, not an independently obtained Git diff.

Each required word exclusion was assessed directly, not through transitivity:

| Direct pair | Declaration | Assessment in both quiz directions |
|---|---|---|
| 丘–坂 | 丘 excludes 坂 | Protected; ordinary “hill” overlap warrants the guard. |
| 丘–山 | 丘 excludes 山 | Protected; 山 has an ordinary hill sense. |
| 砂丘–丘 | 砂丘 excludes 丘 | Protected; a dune is sandy rising ground. |
| 砂丘–坂 | 砂丘 excludes 坂 | Protected; dune terrain can support the displayed slope/hill interpretation. |
| 砂丘–山 | 砂丘 excludes 山 | Protected; sand-hill and broader hill interpretations can overlap. |

Under the documented symmetric contract, each declaration protects both directions; reciprocal declarations are unnecessary. Actual 砂 “sand” and 砂漠 “desert” comparisons distinguish material and region from a dune without requiring exclusions merely for shared subject matter.

**Quiz choices:** 丘’s explicit `兵／近／共` choices mean soldier/troops, near and together/shared—not hill/knoll. 山’s explicit `川／出／木` choices mean river, go out/exit and tree/wood; none is a defensible ordinary mountain answer. Its three explicit choices avoid default four-choice fallback.

The actual metadata for `人・休・何・入・出・口・女・日・月・男・買` confirms two distractors each. Adding “hill; knoll” as a possible fallback answer does not create an ordinary-meaning collision with any of those 11 targets. This does not certify larger, random or live candidate pools.

**Optional:** None.

**Limits:** Fresh retrieval of the [丘 page](https://kotobank.jp/word/%E4%B8%98-451173) exposed Shogakukan’s Digital Daijisen heading, おか／丘・岡 reading and relevant landform sense. The [砂丘 page](https://kotobank.jp/word/%E7%A0%82%E4%B8%98-68650) initially extracted an encyclopedia article credited to 遠藤邦彦, supporting wind formation and desert/coastal/river/lake settings; that extraction did not expose its publisher heading and was not relabeled Daijisen. Additional partial raw-HTML windows independently exposed Shogakukan’s actual Daijisen さきゅう definition and しゃきゅう cross-reference, plus a separate Nipponica section. The entire multi-dictionary webpage was not read; raw windows were truncated outside the inspected passages. No assigned local range remained truncated or unread. Frozen XML was supplied evidence, not freshly retrieved upstream data.

This is textual review, not native-speaker, device, physical-phone, rendered-glyph or drawing acceptance. Compatible Android `f9b59a2+` remains required for reading curation; phone/general-release acceptance is outstanding, without constituting a blanket veto on bounded owner testing. No files were changed.
