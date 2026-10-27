## Snapshot: d30143529a24516ba47ea82f15c0c3d66a1a98ad; committed content only

Parent: `a1a8b73757e760d15d12a1af85511a49b0ac519b`.

The frozen receipt was read first and identifies this as clean, committed content. This review uses that snapshot attribution; file tools cannot execute Git, so I could not independently verify HEAD, worktree cleanliness, or commit-to-file correspondence.

## Scope: gpt-6.1-sol; family gpt

Independent, serial, read-only review: no agents, delegation, concurrent work, edits, or other reviewer reports.

Actual complete reads:
- All twenty assigned word articles, all eight related current kanji bodies, the complete `related.patch`, and all eight baseline kanji bodies in the permitted inspection renderings.
- All twenty mappings, twenty complete principal families containing 28 senses, thirty-four complete component records, and 268 complete comparison-label records. Restrictions, flags, inherited POS, raw source fields, and selected one-based senses were included.
- All eleven family-inspection chunks and the complete supplemental 大きな・別れ・別れる families: **310 distinct families / 669 senses**, including the principals. All seventeen older-body renderings contained **133 complete older articles**; direct complete repository reads of 大きな, 別れ, and 別れる brought older-body coverage to **136 articles**.
- Both complete public-capture text files and their JSON capture receipts: twenty principal and two supplemental entries. These are **one public dictionary authority—Digital Daijisen via Weblio—not twenty-two independent dictionaries**.

Also read the three required instruction/format references, both allowed N2 vocabulary/source snapshots, `docs\confusable-words.md`, and `docs\jlpt-levels.md`. TSV access was limited to the header and physical lines **1522–1541**. Restricted searches checked relevant titles and exact candidate filenames within `words\`, and component-card existence within `kanji\`; thirteen existing lower-level kanji headers were additionally inspected.

The remaining **187 prepared families / 414 senses** were not inspected. Comparison labels were not counted as full-body reads. The author-rationale file, prohibited ledgers, authoring inputs/checks, and other reviewers’ reports were not read.

## Verdicts:

**No actionable defect was established within the inspected scope.** CLEAN means that scoped result, not exhaustive correctness or native-speaker certification.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1522 | 別荘 | CLEAN | CLEAN | CLEAN | Holiday-home meaning is explicit; luxury and ownership are not falsely required. Joking prison usage is separate recognition. |
| N2:1523 | 別々 | CLEAN | CLEAN | CLEAN | Separateness and individual action are distinguished; に, の/な, and predicate constructions are supported. |
| N2:1524 | ベテラン | CLEAN | CLEAN | CLEAN | Experienced practitioner is taught without importing military status, retirement, or guaranteed superiority. |
| N2:1525 | ヘリコプター | CLEAN | CLEAN | CLEAN | Helicopter, powered-rotor description, ヘリ abbreviation, and long final vowel are clear. |
| N2:1526 | 編集 | CLEAN | CLEAN | CLEAN | Transitive editing/compilation is correctly constructed; 编む overlap and the distinction from 社説 are useful. |
| N2:1527 | 便所 | CLEAN | CLEAN | CLEAN | Assigned べんじょ is correctly selected; register guidance avoids an absolute “always insulting” claim. |
| N2:1528 | ペンチ | CLEAN | CLEAN | CLEAN | Combination-pliers identity, uses, instrumental construction, and loanword explanation are coherent. |
| N2:1529 | 望遠鏡 | CLEAN | CLEAN | CLEAN | Distant-object instrument is distinguished from microscope, mirror, and eyeglasses; whole-word reading is correct. |
| N2:1530 | 方角 | CLEAN | CLEAN | CLEAN | Physical bearing leads; thought-direction and method recognition avoid a false physical-only boundary. |
| N2:1531 | 箒 | CLEAN | CLEAN | CLEAN | Source spelling and ほうき are explicitly connected; kana examples and alternative 帚 recognition are appropriate. |
| N2:1532 | 方言 | CLEAN | CLEAN | CLEAN | Regional linguistic variation is adequately explained; social-group usage is separate recognition. |
| N2:1533 | 坊さん | CLEAN | CLEAN | CLEAN | Familiar/respectful Buddhist usage, さん formation, and the recorded boy sense are distinguished. |
| N2:1534 | 防止 | CLEAN | CLEAN | CLEAN | Prevention, transitive を construction, and compound uses are practical; comparisons do not impose an artificial disease/accident split. |
| N2:1535 | 方針 | CLEAN | CLEAN | CLEAN | Guiding policy/course is explained without making policy and detailed planning mutually exclusive. |
| N2:1536 | 包装 | CLEAN | CLEAN | CLEAN | Transitive wrapping and the noun for outer wrapping are supported; material marking is clear. |
| N2:1537 | 法則 | CLEAN | CLEAN | CLEAN | Natural regularity and rules to follow are both accommodated; no categorical nature-versus-human-rules claim. |
| N2:1538 | 包帯 | CLEAN | CLEAN | CLEAN | Body-part を包帯する and body-part に包帯を巻く are correctly distinguished. |
| N2:1539 | 膨大 | CLEAN | CLEAN | CLEAN | Adjectival magnitude and intransitive expansion are separated; 厖大/尨大 are not extended into the restricted expansion sense. |
| N2:1540 | 包丁 | CLEAN | CLEAN | CLEAN | Raw 庖丁 is explicitly recognized as the same-family spelling; common 包丁 is a justified headword, not missing coverage. |
| N2:1541 | 方程式 | CLEAN | CLEAN | CLEAN | Equation, solving construction, and figurative set-method usage are intelligible; formula is not treated as universally interchangeable. |

**Mappings — correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN, for all twenty.** The source associations, readings, dictionary identities, and selected sense arrays agree with the inspected TSV rows and complete principal records. Raw source values remain preserved. In particular, N2:1540 retains raw 庖丁 while teaching its same-family common spelling 包丁. No duplicate 庖丁 article is warranted. Additional recognition was assessed separately, without reconstructing compiler intent or assigning N2 independently to every additional sense.

**Eight kanji changes and baseline preservation:**

| Kanji | Correctness | Scoped coverage | Comprehensibility | Preservation and change |
|---|---|---|---|---|
| 編 | CLEAN | CLEAN | CLEAN | Existing 編集 mentions become links in the ヘン row/common words; applicable ID already present. |
| 角 | CLEAN | CLEAN | CLEAN | 方角 added to reading/common-word navigation, with ガク voicing; ID 1516950 appended. |
| 防 | CLEAN | CLEAN | CLEAN | 防止 added under ボウ and common words; applicable ID already present. |
| 針 | CLEAN | CLEAN | CLEAN | 方針 added under シン and existing common-word mention linked; applicable ID already present. |
| 包 | CLEAN | CLEAN | CLEAN | 包装・包帯・包丁 added under ホウ and common words; their three IDs appended. |
| 装 | CLEAN | CLEAN | CLEAN | 包装 added under ソウ and common words; ID 1515510 appended. |
| 則 | CLEAN | CLEAN | CLEAN | 法則 added under ソク and existing common-word mention linked; applicable ID already present. |
| 帯 | CLEAN | CLEAN | CLEAN | 包帯 added under タイ and common words; ID 1603360 appended. |

Against the supplied complete baselines and patch, **all eight front-matter blocks are preserved**, including readings, levels/tags, strokes, radicals, radical numbers, and distractors. No unrelated teaching passage is removed or substantively rewritten. The changes are useful navigation additions, link conversions, and applicable dictionary-ID additions.

**Component links — CLEAN.** All **27 distinct primary written Han** are represented in the assigned articles’ metadata. Exact-name inspection found **21 existing component cards**: the eight above plus 別・集・便・所・望・遠・方・言・止・法・大・程・式. Their substantive links are present. The six without cards—荘・鏡・箒・坊・膨・丁—remain represented in metadata without fabricated links. Alternative spellings do not incorrectly replace primary metadata.

**Required reciprocal links — CLEAN, 10/10:** 編集/編, 方角/角, 防止/防, 方針/針, 包装/包, 包装/装, 法則/則, 包帯/包, 包帯/帯, and 包丁/包 are present in both directions with appropriate whole-word readings.

**Quiz exclusions — no actionable excess or omission established.** Direct declarations were judged against complete titles, the relevant complete older bodies, and ordinary secondary senses, in both quiz directions and among choices. Symmetry was applied without transitive closure; identical titles were treated as deduplicated.

Consequential checks included:
- 別々’s separation guards were not rejected merely because another card is a noun or verb. 別れる’s ordinary parting sense and separate bereavement sense were inspected without transferring restrictions to 別れ.
- 方角’s method sense, 方針’s intended-course meaning, and 方程式’s figurative method sense support broader comparisons than their leading examples alone suggest.
- 防止/チェック was assessed using the actual supplemental Daijisen **チェック sense 4**, which includes inspecting and preventing unsuitable entry—not merely inspection’s possible preventive purpose.
- 膨大’s expansion comparisons were assessed against its recorded intransitive sense, not manufactured from the English adjective gloss. 広々’s actual title and spacious/open-space teaching were inspected rather than replacing its label with “extensive.”
- Shared subjects, component characters, homophony, and neighboring exclusions were not independently treated as reasons for additional guards.

## Findings:

**None established.** There are no actionable findings requiring severity, facet, location, or remedy entries.

## Optional:

None necessary for this scoped batch.

## Limits:

The Git state, hashes, and compact-rendering equivalence receipts are **author-executed checks**, not independently executed reviewer checks. Preservation conclusions concern the supplied patch and complete rendered baselines; I did not execute a parent-to-commit Git diff.

No live public retrievals or corpus/frequency searches were performed. The frozen public entries support applicable lexical meanings, but do not individually certify every example, register tendency, or historical claim. The uninspected comparison families and remaining label-only articles prevent an exhaustive whole-corpus quiz-ambiguity claim; the thirteen lower-level component cards received header/link checks, not complete body audits.

No consequential lexical uncertainty requiring an UNVERIFIED verdict remained within the inspected scope.
