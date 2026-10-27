## Snapshot: `2a93457f855a5e6a92ee3b09287db81a29e53ab3`

**Scoped editorial verdict: CLEAN.** Committed content only, as identified by the supplied correction snapshot; parent/initial snapshot: `4c40b75eb68980ad3744c172f8adac8c32016342`.

The supplied patch contains exactly eight word-article diffs. Snapshot identity and committed cleanliness remain receipt-dependent: **file-only tools cannot independently execute Git or recompute the frozen hashes.**

## Scope: bounded same-family confirmation

Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family `gpt`. This is a follow-up by the original model family, not a new independent full-batch review.

Inspected all eight article diffs and their current surrounding contexts, relevant comparison/link-target cards, permitted dictionary evidence, and my own archived initial report. Separately checked the exact **unchanged** official-guide attributions in `words\映す.md:38–44`, `words\写る.md:40–46`, and `words\映る.md:42–48`.

No edits, delegation, or agents. No other reviewer’s report or prohibited author/review material was read. No full re-review of unchanged teaching, comparison articles, kanji passages, remaining batch articles, mappings, or reuse claims is claimed.

## Verdicts: changed contexts and exact attribution checks

| Article | Assessed scope | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `words\浮かぶ.md` | Direct 現れる・出る guards in context | CLEAN | CLEAN | CLEAN |
| `words\浮かべる.md` | Direct 表す guard in context | CLEAN | CLEAN | CLEAN |
| `words\承る.md` | Direct 頂戴・受付 guards in context | CLEAN | CLEAN | CLEAN |
| `words\受け取り.md` | Direct 頂戴 guard in context | CLEAN | CLEAN | CLEAN |
| `words\打ち合わせ.md` | 会合 guard and substantive 合わせる link | CLEAN | CLEAN | CLEAN |
| `words\打ち消す.md` | Substantive 肯定 link | CLEAN | CLEAN | CLEAN |
| `words\映る.md` | 似合う guard, retained lesson focus, exact official attribution | CLEAN | CLEAN | CLEAN |
| `words\有無.md` | Named homophones, removed aside, exact comparison citation | CLEAN | CLEAN | CLEAN |
| `words\映す.md` | Evidence-only check, lines 38–44 | CLEAN | CLEAN | CLEAN |
| `words\写る.md` | Evidence-only check, lines 40–46 | CLEAN | CLEAN | CLEAN |

CLEAN means acceptance within these scopes, not exhaustive correctness or native-speaker certification.

## Findings: reconciliation and regression check

**Resolved — initial F01a–e.** The declarations at line 9 now directly exclude every identified pair: 浮かぶ/現れる, 浮かぶ/出る, 浮かべる/表す, 承る/頂戴, 承る/受付, 受け取り/頂戴, 打ち合わせ/会合, and 映る/似合う. The inspected answer titles and dictionary senses support these guards. They do not assert unrestricted Japanese substitution or equivalent parts of speech. Exact-title deduplication is separate; exclusions operate symmetrically but not transitively.

For 浮かべる, the relevant 表す card is **あらわす**, JMdict **1263490**, including expression sense 3—not the separate **ひょうす** family, **2410100**. Independently fetched Digital Daijisen 浮かべる sense 2 also supports outward expression. For 映る, JMdict **1173710** and independently fetched Seisenban sense ② support the recognized harmonizing/suitability use. The added guard does not expand the lesson’s reflection/display focus or establish present-day frequency.

**Resolved — initial F02.** `words\打ち合わせ.md:29` now links 合わせる at its substantive component explanation; `words\打ち消す.md:36` links 肯定 at the qualified antonym comparison. Both destinations exist and support the stated relationships. The qualification that affirmation is not the opposite of every sound-masking use remains intact.

**Resolved — original official-guide evidence-access gap; all three exact attributions are supported.** I interpreted the actual readable entry **025**, one-based **PDF page 12 / printed page 8**, including its footnote:

- `映す.md:38–44`: the entry places 写真を写す under image recording and ビデオを映す under reproduction/projection. This supports the stated recording-versus-display distinction and “play/show a video.”
- `写る.md:40–46`: the footnote explains ビデオに写る as being filmed and retained as an image, permits 映 for an image being reproduced, and permits 映る for simultaneous camera/display operation when taking the reproduction viewpoint.
- `映る.md:42–48`: the same passage supports playback and live-camera images viewed as displays.

The passage therefore supports the claims **as qualified in the articles**, not an absolute photograph/video boundary. This closes an evidence gap in unchanged teaching; it is not another teaching-text correction.

**Independently accepted — 有無, not an original finding of mine.** `words\有無.md:18` now explicitly distinguishes 生む・産む (うむ), “give birth; produce.” The supplied pinned JMdict family **1588410**, senses 1–2, supports the reading and glosses; its exact entry number is added at line 43. The unrelated computer aside is removed. The contrast is comprehensible and does not imply a homophone-based quiz exclusion.

**No actionable regression established** in the eight changed contexts.

## Optional: none

## Limits: provenance and coverage

The official passage is **shared author-extracted cached evidence**, not my independent PDF retrieval. Its recorded method is `pypdf PdfReader`, `pages[11].extract_text()`, without reconstruction or editorial rewriting. The committed packet records extraction SHA256 `2f60b5d18f11138560764a3a8aa72d0cb788614cf2125b89774d219e114b7e9c` and the source PDF hash. I read and independently interpreted the supplied text but did not recompute either hash or publicly refetch the PDF.

Public dictionary fetches supplied relevant definition bodies for 浮かべる, 承る, and 映る; the definition-less Daijisen headings for the latter two were not evidence. Other supplied dictionary families and inspection receipts retain their author-supplied provenance. No irrelevant or failed public fetch was relied upon.

No consequential linguistic claim remains unresolved within this bounded scope. No frequency measurement, runtime quiz audit, or broader unchanged-content certification is claimed.
