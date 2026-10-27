## Snapshot: 88300af9b018b8735962595c837167bcad9e03bf — committed content only

Parent: `e85977a13ce629196d3e2b922e376a26056a3473`. Commit identity and committed-only status are taken from the frozen receipt. **File tools were available; Git execution was not**, so I could not independently verify the tree, worktree cleanliness or receipt hashes.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Sequential, independent, read-only review; no delegation or edits. Read all twenty new articles completely, all twenty assigned mappings and complete principal JMdict families, the fifteen-file related patch, and its changed passages in context. Checked written-kanji metadata, reciprocal examples, substantive navigation, comparison titles and direct exclusions, using targeted comparison-card reads and public dictionary retrievals.

Read the three required guidance documents and permitted provenance records. Related-file verdicts cover **the changes only**, not comprehensive review of unchanged teaching. No reused principal articles, forbidden reports or private authoring inputs were reviewed.

## Verdicts:

Quiz-safety defects are classified under **correctness**; missing required navigation under **scoped coverage**. Mapping verdicts concern the assigned spelling, reading and applicable selected senses—not navigation or exhaustive dictionary coverage.

| Source → article in `words\` | Reading | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:282 → `貸し出し.md` | かしだし | CLEAN | NEEDS FIX | CLEAN |
| N2:283 → `過失.md` | かしつ | CLEAN | CLEAN | CLEAN |
| N2:284 → `果実.md` | かじつ | CLEAN | CLEAN | CLEAN |
| N2:285 → `貸間.md` | かしま | CLEAN | CLEAN | CLEAN |
| N2:286 → `貸家.md` | かしや | CLEAN | CLEAN | CLEAN |
| N2:287 → `個所.md` | かしょ | CLEAN | CLEAN | CLEAN |
| N2:288 → `過剰.md` | かじょう | CLEAN | NEEDS FIX | CLEAN |
| N2:289 → `かじる.md` | かじる | CLEAN | CLEAN | CLEAN |
| N2:290 → `課税.md` | かぜい | CLEAN | CLEAN | CLEAN |
| N2:291 → `下線.md` | かせん | CLEAN | CLEAN | CLEAN |
| N2:292 → `カセット.md` | カセット | CLEAN | CLEAN | CLEAN |
| N2:293 → `加速.md` | かそく | CLEAN | CLEAN | CLEAN |
| N2:294 → `加速度.md` | かそくど | CLEAN | CLEAN | CLEAN |
| N2:295 → `片仮名.md` | かたかな | CLEAN | CLEAN | CLEAN |
| N2:296 → `片付く.md` | かたづく | NEEDS FIX | CLEAN | CLEAN |
| N2:297 → `塊.md` | かたまり | NEEDS FIX | CLEAN | CLEAN |
| N2:298 → `固まる.md` | かたまる | NEEDS FIX | CLEAN | CLEAN |
| N2:299 → `片道.md` | かたみち | CLEAN | CLEAN | CLEAN |
| N2:300 → `傾く.md` | かたむく | CLEAN | CLEAN | CLEAN |
| N2:301 → `片寄る.md` | かたよる | CLEAN | CLEAN | CLEAN |

**All twenty mappings: CLEAN / CLEAN / CLEAN.** Each article explicitly teaches its assigned source form, reading and applicable meaning. The qualifications appropriately distinguish negligence from accidents generally, modern intransitive 片付く from the source’s transitive-sounding gloss, plant 果実 from specialist legal uses, physical acceleration from merely increasing speed, and spelling variants from restricted readings or separate identities. Selected senses are non-exhaustive; their inclusion does not independently establish N2 membership for every secondary use.

**Each of the fifteen related changes: CLEAN / CLEAN / CLEAN:**

- `kanji\個.md`, `kanji\課.md`, `kanji\税.md`, `kanji\線.md`, `kanji\片.md`, `kanji\固.md`, `kanji\傾.md`.
- `words\貸す.md`, `words\片付ける.md`, `words\噛む.md`, `words\食べる.md`, `words\往復.md`, `words\テープ.md`, `words\ラジオカセット.md`, `words\ラジカセ.md`.

The ten required primary-form N2 reciprocal pairs are present at the actual readings. The additional `固まり → 塊` link targets an explicitly taught alias. Written-kanji arrays are complete, including characters without cards. The supplied related diff preserves existing word identities, titles and levels.

## Findings:

**B15-01 — Moderate; correctness, quiz-label ambiguity.**  
**Location:** `words\固まる.md:4,9,16-21`; comparison metadata in `words\済む.md:4` and `words\落ち着く.md:4,9,23`.

The direct exclusions omit **固まる／済む** and **固まる／落ち着く**. 固まる explicitly teaches a plan becoming firm; “be settled” in 済む’s title and “settle” in 落ち着く’s title are defensible English answers for that ordinary secondary use. Distinct primary meanings do not remove this ambiguity.

**Impact:** A learner can receive competing acceptable meaning choices. Existing paths through 片付く or 決まる do not supply these direct exclusions.

**Minimal remedy:** Add `済む` and `落ち着く` to 固まる’s `quiz_exclusions`, or declare each pair on its counterpart.

**Evidence:** Complete pinned JMdict entry **1266550, sense 2** records becoming firm/certain; the article supplies `来年の計画が固まりました`. 済む’s actual title is **“be finished; be settled”**; 落ち着く’s is **“calm down; settle”**, with an explicitly taught settled-arrangement use. Independently retrieved [Seisenban 落着く](https://kotobank.jp/word/%E8%90%BD%E7%9D%80%E3%81%8F-452941), modern intransitive senses ③–④, supports stabilization and discussion reaching a conclusion. `docs\content-format.md:79-97` requires title-sensitive, direct pairwise protection.

**Confidence:** High for the displayed-label ambiguity and missing declarations; this does not assert unrestricted Japanese interchangeability.

---

**B15-02 — Moderate; correctness, incomplete settlement/completion quiz guards.**  
**Location:** `words\片付く.md:4,9,16-20`; `words\落ち着く.md:4,9,23`; `words\済ませる.md:4,9,16-20`.

The direct exclusions omit **片付く／落ち着く** and **片付く／済ませる**. The article expressly teaches both settlement and finishing. Consequently, **“calm down; settle”** and the bare **“finish”** alternative in **“finish; get something done”** can be accepted for 片付く. The latter label does not restrict *finish* to its transitive English construction.

**Impact:** These pairs remain eligible for ambiguous choices despite protection against nearby completion and settlement cards.

**Minimal remedy:** Add direct exclusions for `落ち着く` and `済ませる`. Protection through 決まる, 終わる, 終える or しまう is not transitive.

**Evidence:** Complete pinned JMdict **1511770, senses 2–3** records being solved/disposed of and being finished. The article demonstrates both. Independently retrieved [Seisenban 片付く](https://kotobank.jp/word/%E7%89%87%E4%BB%98%E3%81%8F-463521), modern intransitive [1]⑥, supports resolution and completed work. The comparison cards’ actual titles and exclusions establish that neither direct pair is declared; the quiz contract at `docs\content-format.md:85-97` explains why intermediate exclusions are insufficient.

**Confidence:** High for the settlement pair; medium-high for the completion pair’s English-label ambiguity.

---

**B15-03 — Moderate; correctness, unprotected figurative sense in the quiz.**  
**Location:** `words\塊.md:4,9,16-20,34`; `words\具体.md:4,15`.

塊 teaches **“embodiment”**, including `彼は好奇心の塊です`, but does not exclude 具体, whose actual title is **“concreteness; embodiment”**. 具体 declares no reverse exclusion.

**Impact:** With 塊 as the Japanese prompt, “embodiment” is an explicitly taught answer, making the comparison label defensible alongside “lump; mass.”

**Minimal remedy:** Add the direct pair `塊／具体`; retain the useful figurative teaching and accurate titles.

**Evidence:** Complete pinned JMdict **1590410, sense 3** explicitly records embodiment/personification of an idea, quality or feeling. Both the new article and existing comparison card teach that English term. Independently retrieved [Seisenban 具体](https://kotobank.jp/word/%E5%85%B7%E4%BD%93-186438), sense ②, identifies the concretization/具象 use; the finding concerns the actual ambiguous English label, not universal equivalence of the Japanese nouns.

**Confidence:** High.

---

**B15-04 — Minor; scoped coverage, required substantive navigation.**  
**Location:** `words\貸し出し.md:25`; `words\過剰.md:29`.

Two substantive introductions remain unlinked despite existing matching cards: **出す**, introduced as the compound’s constituent verb, and **不足**, presented as the contrasting shortage term.

**Impact:** Learners cannot follow those base-word/contrast references directly. This is a navigation omission, not incorrect linguistic teaching.

**Minimal remedy:** Link those occurrences to `出す.md` and `不足.md`.

**Evidence:** `words\出す.md:2-7,15` teaches 出す／だす, “take out; put out”; `words\不足.md:2-7,15` teaches 不足／ふそく, shortage/insufficiency. `.github\instructions\content-structure.instructions.md:20-21` requires an existing card to be linked at substantive introduction or comparison.

**Confidence:** High.

## Optional:

None. Specialist, historical and marriage-related expansions explicitly outside the practical lessons are not required fixes.

## Limits:

Snapshot identity and file hashes were not independently verified; the frozen receipt supplies that provenance. Public pages were live corroboration, not reconstruction of the committed tree.

Quiz findings are based on actual front matter and the documented pairwise rules; the app was not executed. Selected comparison families and targeted title searches do not constitute an exhaustive whole-repository synonym audit. Failed or irrelevant retrievals—including Jisho’s nonlexical extraction and a 塊 page exposing other readings—were not treated as lexical verification.

No additional consequential unresolved lexical claim was identified within the reviewed scope. **CLEAN** means no actionable defect established here, not exhaustive correctness or native-speaker certification.
