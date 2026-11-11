# Batch 109 (催 促 摩 擦 括 弧 抵 抗 撮 影 攻 撃 掲 批 択): two-family textual review closure

This directory closes the independent textual review of batch 109 and preserves
its evidence. The batch adds fifteen N1 kanji cards with their stroke data and
links the new kanji in eighteen existing word articles; it adds no new word
article. Two reviewers from two different model families, Claude and GPT, read
the frozen draft (`0a20f4bf`) on all four facets without seeing each other's
work. Both independently reported the same major quiz-safety defect: the curated
wrong answer 形 on the 影 card is a defensible meaning of 影. GPT also reported
thirteen missing direct quiz exclusions, five of which Claude had found
independently, and both reported smaller wording and evidence defects. All of it
was reconciled in `a3e0610a`, the only commit after the freeze that changes
teaching content, and both original reviewers then confirmed the corrected text
with no findings.

`a3e0610a` descends from `308ab608`, the `origin/main` of the time, through the
freeze; no merge of `origin/main` was needed. The commit that adds this record
changes only `docs/`, which the content archive excludes, so the teaching
content, `manifest.json` and the budgets are exactly those that were reviewed,
confirmed and gated. The tree was checked mechanically (see below). No native,
rendered, phone, CI or archive credit is claimed by this record; publication is
recorded separately.

## Teaching scope

| File | Change |
|---|---|
| `kanji/催.md` `促.md` `摩.md` `擦.md` `括.md` `弧.md` `抵.md` `抗.md` `撮.md` `影.md` `攻.md` `撃.md` `掲.md` `批.md` `択.md` | 15 new N1 cards |
| `strokes/<kanji>.json` for the same 15 kanji | generated stroke data (KanjiVG revision `70a0b7ae`) |
| `words/` 催し 催促 反抗 専攻 影 影響 批判 批評 抵抗 括弧 掲示 摩擦 撮る 撮影 擦る 攻める 攻撃 選択 (`.md`) | 18 existing articles, one line each: the new kanji are wrapped in `[X](../kanji/X.md)` links (24 links in all); nothing else changes |
| `manifest.json` | regenerated index, not reviewed content |

At the confirmed snapshot the payload went from 8,481 to 8,511 manifest entries
(kanji 1,131 to 1,146, strokes 1,131 to 1,146, words 5,082 unchanged) and
`contentVersion` from `baf07138f3468ac9` to `fe02221511f427e5`. The freeze had
`a4c36b5e19e5e105`; the thirteen revised cards account for the difference. The
local archive went from 8,503 to 8,533 entries.

## Reviews

All times are UTC on 2026-11-11. At most one reviewer was active at any instant
and the four runs did not overlap. The actual model is taken from each session's
usage record, not from the requested model. Each run covered all four facets
(correctness, scoped coverage, consistency and quiz safety, comprehensibility);
the two initial runs, made at reasoning effort `high`, were told which facets to
examine deepest. Each confirmation was asked to check every changed line for new
defects on all four facets and to give a disposition for every item of the
author's statement.

| Run | Actual model | Snapshot | Window | API requests | Tool calls (max in flight) | Examined deepest |
|---|---|---|---|---|---|---|
| `initial-claude` | claude-opus-5.5 | `0a20f4bf` | 18:11:32-18:23:19 | 92 | 96 (3) | correctness, scoped coverage |
| `initial-gpt` | gpt-6.1-sol | `0a20f4bf` | 18:24:53-18:43:25 | 65 | 65 (1) | consistency and quiz safety, comprehensibility |
| `confirm-claude` | claude-opus-5.5 | `a3e0610a` | 19:22:45-19:26:42 | 38 | 39 (2) | revised text, all facets |
| `confirm-gpt` | gpt-6.1-sol | `a3e0610a` | 19:28:21-19:38:19 | 67 | 67 (1) | revised text, all facets |

The initial verdicts differed in detail and agreed on the defect. Claude passed
correctness, scoped coverage and comprehensibility with minor defects (摩 and
擦) and failed consistency and quiz safety (影 major, 括 minor). GPT returned
correctness, scoped coverage and comprehensibility CLEAN and consistency and
quiz safety NEEDS FIX (影 major, missing direct exclusions major), with the
cards 撃 (撃/敗) and 批 (攻/批) marked UNVERIFIED. Both confirmations returned
CONFIRMED with findings none.

Each reviewer worked from a frozen packet of one snapshot: the initial packet
(built at 18:09:21 from `0a20f4bf`, 6,326 files) for both initial runs and a
confirmation packet (built from `a3e0610a`) for each confirmation. The audits
record no read outside the allowed paths (`outsidePaths` is empty in all four).
In the initial round neither reviewer saw the other's report or the author's
rationale. In the confirmation round each reviewer saw the author's statement on
its own findings (claims to verify, not evidence), a neutral change list, the
exact patch, the new evidence and the automatic checks, and no other reviewer's
report. The GPT confirmation also re-read its own initial report; the Claude
confirmation did not reopen its own.

Serial tool work was required of every reviewer, and the audits record how it
went. The two GPT runs were strictly serial. The initial Claude run issued four
overlapping `view` starts between 18:12:47 and 18:13:36 (up to three calls in
flight), all before the coordinator's steering message at 18:13:48
(`prompts/initial-claude-steering-1.txt`); there was no overlap after it. The
Claude confirmation had one overlapping start, two `view` calls in flight, at
19:23:19. The initial Claude run also made two recursive PowerShell listings of
the packet directory (6,327 files each) and 17 PowerShell calls in all, among
them a scripted lookup of 58 example words on jisho.org (listed in its report),
plus three jisho.org web fetches. Apart from its report no reviewer wrote a
file. This record therefore claims strictly serial work only for the two GPT
runs.

`reports/` holds the four verbatim reports, stored with LF line ends; their
SHA-256 values equal the `reportSha256` of the audits. `prompts/` holds the
exact prompts, including the one steering message. `scope-audits/` holds the
read-scope and model-identity audits. An audit's `reviewAccepted: false` is by
design: it records read scope and model identity only, not acceptance.

`packet/` holds the initial packet's instructions and mechanical checks, a
gzipped manifest (the SHA-256 of each of its 98 named files and one aggregate
hash of the 6,228-file repository context export), the 18 word diffs and the
evidence (JMdict digest and families, KANJIDIC2 records, pinned source metadata
and the 15 Digital Daijisen extracts from Weblio). The snapshot cards, strokes
and words are the Git blobs at `0a20f4bf` and are not copied. `confirm-packet/`
holds the 23 files common to both confirmations (change list, exact patch,
cited JMdict entries, Joyo table extracts, KanjiVG records, `QuizBuilder.kt` and
the automatic checks), each family's instructions, author's statement and file
manifest, and the packet provenance.

## Reconciliation

Item labels: Claude's F1-F5 and O1-O10 are the labels in its own report. GPT's
report numbers its findings 1 and 2; `#1`, `#2a`-`#2h`, `OA`-`OC` and
`L1`-`L3` are the labels the author gave those findings, GPT's optional points
and its stated limits in `confirm-packet/gpt/RESPONSE.md`. Claude's `L1` is the
author's own question in `confirm-packet/claude/RESPONSE.md`. Line references
are to the cards at `a3e0610a`.

| Item | Disposition |
|---|---|
| Claude F1 (major) and GPT #1 (major), independently: the curated wrong answer 形 "shape; form" on 影 is a defensible meaning (JMdict 1590145 sense 1 "shadow; silhouette; figure; shape"; Daijisen 物の姿や形). | Changed in `a3e0610a`: distractors `[景, 英, 京]` (`影.md:13`), exclusions `[映, 形, 像, 象, 光, 跡]` (`影.md:14`), notes at `影.md:45-46, 48`. Both confirmations RESOLVED. |
| GPT #2 (major; rows #2a-#2h, 13 pairs), Claude F2 (minor, 括) and optional O6 and O10 (催/促, 抵): wrong answers that share a meaning with the target but were not excluded. | Added as direct exclusions, each declared on one card because the app's `QuizBuilder` treats an exclusion as symmetric: 催/促, 促/責, 括/包, 括/囲, 抵/反, 抵/対, 影/像, 影/象, 影/光, 影/跡, 摩/研, 攻/研 and 掲/刷 (the 13 of #2; Claude had found five of them: 催/促, 括/包, 括/囲, 抵/反, 抵/対), plus 影/形 (#1), 攻/批 and 撃/敗 (see below): 16 pairs in all. None completes a clique and none is also a distractor of its declaring card (checked by script and by `validate.py`). Each is explained in a note on its card. |
| Claude F3 (minor): the 摩 readings paragraph contradicted its rows. | Rewritten around the official Joyo table (マ is its only reading of 摩; the kun readings are kept for recognition; 摩する is マ plus する, JMdict 1982610) and a Joyo p. 144 evidence line added (`摩.md:36, 51`). |
| Claude F4 (minor) and GPT OB: 擦 こす.る was unqualified; 擦過傷 is formal. | こする is "usually written in kana" (JMdict 1298910); 擦過傷 is "the formal term" (JMdict 1298950); the Joyo table lists サツ, す.る and す.れる but not こす.る; Joyo p. 62 evidence line added (`擦.md:23, 35, 38, 53`). |
| Claude F5 (minor) and GPT OC: 撮 and 掲 call the top element 日 where the convention is 曰. | Wording changed to "a wide 日-like box (曰)" (`撮.md:25`, `掲.md:25`); 掲 now names its right-hand part as a variant of 曷 (KanjiVG `kvg:variant`) and no longer links to the 日 card. |
| Optional wording adopted: Claude O2 (link 大抵 to its word article), O3 (弧 says Daijisen lists "bow" as its first sense rather than an "older" one), O4 (抗がん剤 named with 抗癌剤 as the variant spelling), O7 (the 攻 and 撃 notes say both characters concern attacking); GPT OA (shorter 抵当 gloss, "doubled consonant sound", Go-on explained). | Adopted (`抵.md:23`, `弧.md:23`, `抗.md:23`, `攻.md:44`, `撃.md:42`, `促.md:23`, `影.md:34`). Both confirmations RESOLVED. |
| GPT L1 (撃/敗, UNVERIFIED): attributed 敗 to the curated list of 撃. | Disputed: 敗 is a distractor of 攻 (`攻.md:13`, `[功, 放, 敗]`); the curated list of 撃 is `[投, 殺, 設]`. A defensive 撃/敗 exclusion was added anyway because KANJIDIC2 lists "defeat" among the meanings of 撃 (`撃.md:14, 44`). GPT answered DISPUTE ACCEPTED and withdrew the attribution. |
| GPT L2 (攻/批, UNVERIFIED). | Exclusion and note added (`攻.md:14, 49`): KANJIDIC2 lists "criticize" for 攻 and JMdict 1279170 (攻撃) sense 2 is "criticism; censure; denunciation; condemnation". RESOLVED. |
| Claude L1, a question from the author: does the app fall back to other cards while three curated wrong answers remain? | Claude read `QuizBuilder.kt`: options come from the curated distractors in order, a candidate is skipped if either card excludes the target or an already chosen option, and other cards are added only when fewer than three curated ones survive. F2, O6 and O10 were therefore latent fallback risks, not live risks in the default options (all 15 cards fill three of three); the exclusions stay as direct-title-overlap protection. RESOLVED. |
| Declined by the author and accepted by Claude: O1; O2 title ("resist; collide" kept); O3 弱 framing; O5 (速 kept for 促); O6 (集 kept for 催); O8 (もよう.す already marked source-only); O9 (existing and out of scope: 括弧 is `uk`, and `words/撮る.md` has no Dictionary line). | Unchanged. |
| GPT L3: limits on strokes, sentences, native speakers and phones. | No stroke file, sentence or word article changed, so nothing is claimed. DECLINE ACCEPTED; the limits are kept below. |
| Optional points not adopted: Claude's four (`掲.md:25` "toward the sun"; the duplicated 研磨/研摩 fact at `摩.md:45-46`; no 催 parity bullet at `促.md:42`; no kana note in the `擦.md:43` common-words bullet) and GPT's one (`摩.md:36`: write the whole-word reading as `摩る する` and keep the dotted す.る for the table). | Both reviewers called them optional polish. Left unchanged so the confirmed snapshot stays exactly as confirmed. |

Two model families reviewed the batch, each on all four facets. That meets the
issue-60 requirement of at least two families per batch on one fixed snapshot
with independent blind initial findings, confirmed by the original reviewers.
The repository rule of three facet-split reviewers from three model families
(`.github/copilot-instructions.md`, "Independent review and reconciliation")
applies to a new word card or learner article, a new app-facing file under
`words/` or `articles/`. Batch 109 adds no such file, and its eighteen word
edits only wrap kanji in links, so review stays proportional. That reading is
the author's and is repeated under Limits.

## Byte identity

`provenance.json` records the snapshots, the packet and the four runs (session,
actual models, window, API requests, tool calls and the SHA-256 of each report,
prompt and audit). Of the 48 teaching files at the freeze (15 cards, 15 stroke
files and 18 word articles), 35 are the same Git blobs at `a3e0610a`: the cards
批 and 択, all 15 stroke files and all 18 word articles. The other 13 cards
(促 催 弧 影 抗 抵 括 掲 摩 撃 撮 擦 攻) changed; `git diff --shortstat 0a20f4bf
a3e0610a` shows 14 files (those 13 and `manifest.json`), 56 insertions and 42
deletions. Only 影 changed its distractors; every other card kept its curated
list, and its changes are exclusions, notes, evidence lines and wording.

The snapshot copies in the initial packet have Windows (CRLF) line ends while
Git stores LF; for all 48 snapshot files, converting the blob at `0a20f4bf` to
CRLF reproduces the SHA-256 recorded in the packet manifest. Both confirmation
packets list the same 15 card blob IDs; all 15 equal the Git blobs at
`a3e0610a`, and two of them (批 and 択) equal the blobs at the freeze.
`a3e0610a` was made by amending an earlier local fix commit, `b478b727`, that
no reviewer was shown and that was never published. Both confirmation packets
were built from `a3e0610a` (19:21 UTC).

## Integrated-tree checks (mechanical, not reviewer credit)

At `a3e0610a`: lint 0 errors and 1 warning (the existing missing Dictionary line
in `words/撮る.md`); 431 unit tests pass; validation 0 errors; budget 8,533
entries, 45,039,244 retained bytes, 45,310,554 inflated, 30,513,079 local ZIP
bytes; vocabulary 2122/2431; manifest rebuild shows no diff. The option
simulation (`confirm-packet/common/checks/quiz-safety.txt`) reports 0 errors and
0 warnings, with every one of the 15 cards filling its three wrong options from
its curated list. The Android JVM `RealContentTest` (3 tests) and `RareHanTest`
(1 test) ran with no skips or failures. There is no merge in the tree:
`origin/main` was still `308ab608` when this record was written.

## Limits

- The review judged text and a printed simulation of the answer-option builder
  plus a reading of `QuizBuilder.kt`, not a running app. Claude assumed the card
  list passed to the builder is the whole corpus; GPT inspected the supplied
  automatic checks without rerunning them.
- Reviewers used pinned dictionary snapshots (JMdict, KANJIDIC2, Digital
  Daijisen extracts, KanjiVG at `70a0b7ae`) and public pages. The live
  dictionaries may differ slightly; for example the live jisho.org entry for
  摩る omits the `rK` label of the pinned JMdict entry.
- The Claude confirmation made no live web lookup and used text extracts of the
  official Joyo table made with pdfplumber without opening the PDF. The GPT
  confirmation fetched the PDF, matched its SHA-256 (`d9f28aeb...d8d42`) and
  extracted pages 62 and 144 itself. Claude did not reopen the unchanged 批 and
  択 cards; their options were checked from the printed simulation.
- The GPT confirmation covered the changed passages and the 15 printed
  simulations, not an exhaustive re-review of the unchanged dictionary families,
  the 18 word articles or the stroke files. It did not establish the source-only
  催 reading もよう.す as productive modern usage; the card marks it source-only
  and does not practise it.
- Strokes: the GPT initial run parsed all 15 stroke files and compared their
  structure, ordered types, initial coordinates and component geometry with the
  pinned KanjiVG revision; the Claude initial run checked stroke counts only.
  Neither regenerated every arc length or rendered the stroke animations. No
  native-speaker panel assessed sentence naturalness and no one tried the cards
  on a phone. No end-to-end reading-runtime or older-client certification is
  claimed.
- Strictly serial tool work is claimed only for the two GPT runs (see Reviews).
- Two families, not three: the three-family rule covers new `words/` and
  `articles/` files, of which this batch has none. A third-family read can be
  added if the owner wants one.
- No native emulator, rendered, physical-phone, older-client or handwriting
  credit. The issue-60 batch cycle does not require a native run per batch; the
  plan is one native smoke at a milestone or the final acceptance.
- The multi-megabyte session event archives of the reviewers remain local and
  are not committed.
