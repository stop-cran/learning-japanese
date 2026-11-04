**Snapshot:** `47edd129ece0c36d7d5eaf50d1d097dfd544994f`, as identified by the supplied frozen task; no uncommitted teaching included. Commit/worktree status was not independently verified because shell/Git inspection was excluded. No changes made.

**Scope:** Independent initial review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual phone comprehensibility of all three new teaching files.

Read completely: the prescribed instruction files and documentation ranges; all five raw KANJIDIC2 character elements in `batch-036-input-metadata.json`; and all three frozen JMdict packets—1,931/481/915 lines, respectively, comprising 124/15/28 complete families (167 distinct families). XML reads were serial, explicitly bounded to at most 200 lines, with no returned-range truncations.

Comparison articles read completely:
- Kanji: 単, 戦, 営, 医.
- Animal/category words: 動物, 家畜, 熊, 牛, 犬, 猪, 猿, 猫, 虎, 豚, 象, 馬, 鹿, 鼠, 兎.
- Medical/context words: 医者, 医師, 病気, 相談, 山, 見る.

Inspected the three supplied Digital Daijisen HTML excerpts, including their actual headings and definition bodies. Searched `docs\confusable-words.md` for the scoped words; did not inspect its entire inventory. No other reviewers’ reports or author rationale were consulted.

**Verdicts:**

| New teaching file | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\獣.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\獣.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\獣医.md` | **CLEAN** | **CLEAN** | **CLEAN** |

**Findings:** None established within the assigned scope.

The complete ordered readings `ジュウ / けもの / けだもの`, 16 strokes, radical 94 and grade-8 metadata agree with the supplied 獣 KANJIDIC2 element. Explicit quiz selections preserve the full lists and have separate reading rows with correctly allocated linked examples. Both required reciprocal pairs—獣↔獣 and 獣↔獣医—are present. The three curated meaning distractors have distinct ordinary meanings; their comparison cards retain legacy full-reading exposure, which does not create an animal-meaning ambiguity here.

JMdict 1335590 supports 獣/けもの and 獣/けだもの in the animal sense. Its separate subculture sense is restricted to the `ケモノ` reading, which has `re_nokanji`; the article does not incorrectly assign that sense to written 獣. Digital Daijisen’s supplied けだもの definition supports both the mammalian animal sense and contemptuous person use; its けもの entry cross-references けだもの. The teaching therefore avoids an unsupported strict pronunciation-based animal/person division.

JMdict 1335610 and 2095820 support the veterinary practitioner terms; 1699880 supports the separate field-of-study term. The 医 comparison family also supports doctor as a noun/suffix contribution. The articles correctly distinguish professional person from field and clinic, without restricting veterinary practice to wild beasts.

All Japanese examples, kana renderings, particles and English translations are coherent. The mountain examples demonstrate location-of-action `で` versus location-of-existence `に`; the veterinary consultation example correctly separates topic `について` from consulted person `に`. Neither example requires an unsupported rare collocation.

The fifteen exclusions declared on 獣 directly guard its category-versus-animal overlaps against the actual comparison labels. No transitive protection or species-synonym clique is assumed. The modern-shape mnemonic and comparisons are intelligible and explicitly non-etymological; 犬 is correctly identified on the right. Reading support, sectioning and explanations are suitable for textual small-screen reading.

**Optional:** None necessary for this bounded objective.

**Limits:** Evidence was supplied frozen XML and supplied dictionary HTML, not independently retrieved upstream material. Artifact hashes, source authenticity and current upstream versions were not independently verified. Sentence naturalness was assessed editorially, not established through corpus attestation or native-speaker testing.

No assigned read was incomplete or truncated. The task’s nine core families overlap the 124-family lexical packet and were not counted or reread as additional families. No external reviewer-process evidence was available.

Comprehensibility verdicts concern text, not actual Android rendering or physical-phone acceptance. The stated 36-Han cmap coverage and unchanged pilot acceptance are not fresh native certification. Batch-036 Android, combined-main, CI and public-ZIP checks remain unverified here; physical-phone/general-release acceptance remains outstanding. These limits do not establish a textual defect or a blanket veto on bounded owner testing.
