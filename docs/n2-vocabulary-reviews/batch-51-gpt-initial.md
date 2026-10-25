## Snapshot: `9de757c1fdaff0d2012091652d43247998307d29`; committed content only

Parent: `e2edfb235baf79faefae1a7df0785d6f394cf2d4`. Read `batch-51-frozen-snapshot.json` first.

**Result: five quiz-correctness findings affecting six new articles.** No actionable defect was established in their teaching prose, source mappings, or the three reciprocal kanji edits. This is a read-only review of the supplied frozen content; its committed/clean status was not independently verified through Git.

## Scope: gpt-6.1-sol / family gpt

Completely read all twenty assigned articles, `kanji\畳.md`, `kanji\線.md`, `kanji\袋.md`, and `related.patch`. Also completely read **116 distinct older word articles**, including every declared exclusion target, substantive comparisons, and additional ambiguity candidates. No agents, delegation, or edits were used.

Read the required `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, and `docs\content-format.md:18–126`; the permitted vocabulary/source snapshots, assigned TSV rows **N2:1002–N2:1021 only**, `docs\confusable-words.md`, and `docs\jlpt-levels.md`.

Private evidence was restricted to the permitted files under the exact supplied `batch-51-` prefix. Completely read the mapping, principal, component, and label JSONL files; all ten complete family renderings; and both public-body files. The renderings declare **218 complete families / 482 senses, including the twenty principals / 36 senses**—not 218 additional families or all 321 captured identities. Inspected actual restrictions, spelling/reading flags, inherited POS, and one-based selected/additional senses rather than relying on mapping notes.

The twenty original public lexical captures were read as **author captures**, not fresh retrievals. Fresh Jisho lexical bodies were additionally obtained for ちゃんと, ぐしゃぐしゃ, ぐずぐず, だらだら, 成立, 重なる, and すっと.

`review-evidence.json` was read only in its header/early-mapping portion and one tail excerpt; `principal-reading.txt` was not read. The complete compact records and relevant complete lexical/article bodies supplied the evidence used below. No prohibited author/review ledgers, rationale-bearing batch file, private scripts, or other reviewers’ reports were opened.

## Verdicts: individual articles, mappings, and kanji edits

**Correctness includes quiz metadata.** Scoped coverage concerns practical teaching coverage, not exhaustive dictionary expansion. Thus an article can have adequate teaching coverage and comprehensibility while requiring a quiz exclusion fix.

Mapping notation below is **JMdict entry: selected senses; +additional senses**, all one-based.

| Source ID | Exact article / status | Correctness | Scoped coverage | Comprehensibility | Mapping |
|---|---|---|---|---|---|
| N2:1002 | `words\助かる.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1344380:1–3 |
| N2:1003 | `words\但し.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1416190:1 |
| N2:1004 | `words\畳む.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1356780:1; +2,3 |
| N2:1005 | `words\立ち止まる.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1551350:1 |
| N2:1006 | `words\たちまち.md` — new | **NEEDS FIX — F01** | CLEAN | CLEAN | CLEAN — 1288480:1,2 |
| N2:1007 | `words\建つ.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1597045:1 |
| N2:1008 | `words\発つ.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 2857436:1 |
| N2:1009 | `words\脱線.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1416560:1,2 |
| N2:1010 | `words\妥当.md` — new | **NEEDS FIX — F02** | CLEAN | CLEAN | CLEAN — 1408540:1 |
| N2:1011 | `words\例える.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1597130:1 |
| N2:1012 | `words\頼もしい.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1548380:1,2 |
| N2:1013 | `words\足袋.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1404920:1 |
| N2:1014 | `words\ダブル.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1077110:1; +2–6 |
| N2:1015 | `words\だます.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1574550:1; +2 |
| N2:1016 | `words\溜まる.md` — new | **NEEDS FIX — F03** | CLEAN | CLEAN | CLEAN — 1552650:1 |
| N2:1017 | `words\ダム.md` — new | CLEAN | CLEAN | CLEAN | CLEAN — 1077140:1 |
| N2:1018 | `words\ため息.md` — new; source 溜息 | CLEAN | CLEAN | CLEAN | CLEAN — 1597190:1 |
| N2:1019 | `words\ためらう.md` — new | **NEEDS FIX — F04** | CLEAN | CLEAN | CLEAN — 1573390:1 |
| N2:1020 | `words\溜める.md` — new | **NEEDS FIX — F03** | CLEAN | CLEAN | CLEAN — 1552630:1; +2 |
| N2:1021 | `words\だらしない.md` — new | **NEEDS FIX — F05** | CLEAN | CLEAN | CLEAN — 1007500:1; +2 |

All twenty mappings teach the applicable source spelling, reading, and meaning. The 溜息 → ため息 normalization retains recognition of the source spelling. Teaching correctly avoids reproducing the misleading transitive 建つ gloss, erroneous ダム “dumb,” and dated derogatory English for だらしない. Search-only, rare, and outdated forms are appropriately distinguished from recommended practice. No invented pinned sense numbers were established.

| Related kanji passage | Correctness | Scoped coverage | Comprehensibility | Assessment |
|---|---|---|---|---|
| `kanji\畳.md:30,39,44` | CLEAN | CLEAN | CLEAN | Substantive 畳む links in the `たた.む` reading row and Common words; correct transitive godan examples. |
| `kanji\線.md:30,45` | CLEAN | CLEAN | CLEAN | 脱線 appears under セン and Common words, with だっせん and the ダツ + セン sound change. |
| `kanji\袋.md:33,41,48` | CLEAN | CLEAN | CLEAN | 足袋 uses explicitly qualified **whole-word たび**, without manufacturing individual 足た or 袋び readings. |

**Baseline metadata preservation: CLEAN within the supplied patch comparison.** The patch contains no front-matter changes. The existing reading qualifications and metadata remain intact. Independently checking that patch against the actual parent commit remains **UNVERIFIED**.

All written Han characters are retained in the new headword metadata. The thirteen existing component cards receive substantive word-side links; missing **但・脱・妥・溜** cards are not invented, and those characters remain in the applicable written-kanji arrays.

## Findings: eight missing direct exclusion pairs

These findings concern actual overlapping meanings, not shared topics, homophony, or transitive propagation through another exclusion. The complete displayed titles differ, so exact-title deduplication does not protect these pairs. Both cards’ declarations were inspected. One declaration per pair is sufficient because exclusions are symmetric and also operate between distractor choices.

**F01 — Medium · quiz correctness · high confidence.**

**Location:** `words\たちまち.md:9`; counterpart `words\すっと.md:2–9,15–18`. The titles are **“in an instant; suddenly”** and **“swiftly; smoothly.”** Despite its narrower title, the complete すっと body explicitly includes “all of a sudden”; the freshly retrieved [Jisho すっと entry](https://jisho.org/word/すっと) also documents that ordinary use. Consequently, the new title’s “suddenly” can be a defensible answer for すっと. **Minimal remedy:** add `すっと` to たちまち’s exclusions. This is direct evidence, not an inference through 急に.

**F02 — Medium · quiz correctness · high confidence for 成立; medium-high for 適する.**

**Location:** `words\妥当.md:9`; counterparts `words\成立.md:4,9,16–21` and `words\適する.md:4,9,16–21`. The complete titles are **“reasonable; appropriate; valid,” “formation; conclusion; validity,”** and **“suit; be suitable for.”** 成立 explicitly teaches an argument holding or being valid, confirmed by the complete fresh [Jisho 成立 entry](https://jisho.org/word/成立). This overlaps 妥当’s logical soundness—not merely legal-document validity. 適する explicitly teaches suitability for a purpose or audience, overlapping “appropriate”; the pinned 妥当 record and captured Daijisen body also recognize fitting/applying. Neither pair is declared. **Minimal remedy:** add `成立` and `適する` to 妥当’s exclusions. The unsuccessful fresh 適する retrievals are not evidence for this finding; its support is the complete older article and inspected 妥当 records.

**F03 — Medium · quiz correctness · high confidence.**

**Location:** `words\溜まる.md:9`, `words\溜める.md:9`; counterpart `words\重なる.md:4,9,16–21,33`. The titles are **“accumulate; build up,” “accumulate; store; leave unpaid,”** and **“be piled up; overlap.”** 重なる’s complete body expressly teaches accumulation and repeated problems building up. The complete fresh [Jisho 重なる entry](https://jisho.org/word/重なる) independently documents accumulation, including stress piling up. Thus either new “accumulate” label can be defensible for 重なる; the English label does not encode the Japanese transitivity distinction. **Minimal remedy:** add `重なる` independently to both new cards’ exclusions. Existing guards involving 重ねる or 積もる do not supply these two nontransitive edges.

**F04 — Medium · quiz correctness · high confidence.**

**Location:** `words\ためらう.md:9`; counterpart `words\ぐずぐず.md:4,8,17–19,28`. The titles are **“hesitate; waver”** and **“dawdling; grumbling; unsettled.”** The complete older article explicitly teaches “delaying or hesitating,” so this is not a conclusion drawn only from its title or dawdling imagery. The captured Daijisen ためらう body directly describes indecision using ぐずぐずする, and the fresh [Jisho ぐずぐず lexical result](https://jisho.org/search/ぐずぐず) includes hesitant action. **Minimal remedy:** add `ぐずぐず` to ためらう’s exclusions. Its existing 迷う guard does not block this pair.

**F05 — Medium · quiz correctness · high confidence for ぐしゃぐしゃ; medium-high for だらだら.**

**Location:** `words\だらしない.md:9`; counterparts `words\ぐしゃぐしゃ.md:4,8,17,28` and `words\だらだら.md:4,8,17–21,29`. Their complete titles are **“sloppy; undisciplined; weak-willed,” “crumpled; messy; soggy,”** and **“trickling; dragging on; idling.”** The inspected principal record for だらしない includes ordinary untidiness, slovenliness, and slackness. ぐしゃぐしゃ’s complete body teaches non-wet messy hair; its fresh [Jisho entry](https://jisho.org/word/ぐしゃぐしゃ) separately confirms untidiness/disorganization. This finding does **not** confuse wet “sloppy” with untidy appearance. だらだら teaches slack activity, and its complete fresh [Jisho entry](https://jisho.org/word/だらだら) documents a slovenly/lazy manner. Those ordinary uses make the new “sloppy” label defensible. **Minimal remedy:** add `ぐしゃぐしゃ` and `だらだら` to だらしない’s exclusions; no wider idling or texture network is implied.

No actionable excessive exclusion was established among the inspected declarations.

## Optional: none

## Limits: verification boundaries

File tools cannot execute Git. I therefore did **not** independently verify HEAD, clean-worktree status, parent/commit contents, creation-versus-rename history, hashes, or the author’s equivalence checks. “New” classifications follow the frozen manifest. The supplied inspection counts and hash/equivalence assertions are not reviewer-executed checks.

The review did not inspect all 321 captured identities or every existing word article. Omitted records were not treated as evidence of lexical absence. Successful fresh dictionary bodies are current public evidence, not independently verified copies of the pinned JMdict snapshot; no pinned sense numbers were inferred from them.

Several Weblio, Kotobank, and Jisho requests returned 404s, unrelated material, or pages without lexical bodies. Those responses were not counted as verification. In particular, no fresh exact 適する dictionary body was obtained.

**CLEAN** means no actionable defect established within this actual scope—not exhaustive correctness, a relative-frequency finding, or native-speaker certification.
