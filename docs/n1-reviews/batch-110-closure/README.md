# Batch 110 (張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖): two-family textual review closure

This directory closes the independent textual review of batch 110 and preserves
its evidence. The batch adds fifteen N1 kanji cards with their stroke data and
links the new kanji in ninety-three existing word articles; it adds no new word
article. Two reviewers from two different model families, Claude and GPT, read
the frozen draft (`453af714`) on all four facets without seeing each other's
work. Claude reported one major defect that GPT's initial round did not (the 器
mnemonic described the centre of the character as 犬, "dog", where the modern
form has 大) and four minor ones (価, 激, 応 and a missing 嫌/怪 exclusion). GPT
independently reported the 価 defect and the 嫌/怪 exclusion and added the stale
応援 statement, a missing 素/料 exclusion, two exclusions whose claimed overlap
does not hold (応/募 and 級/校) and two walls of text (基 and 素); all five of
its findings are minor. All of it was reconciled in `10d79652`, and Claude then
confirmed that commit with no findings.

The GPT confirmation of `10d79652` resolved all five of its earlier findings
but reported one new minor defect on 嫌: the contraction や of いや, attested by
JMdict and Digital Daijisen, could be drawn as a wrong option for the reading
prompt いや. The author first answered with a documented limitation; a GPT-only
follow-up rejected that answer and named the mitigation, which `30f2bd7c`
applies: いや is no longer practised in the reading quiz, while the reading, its
table row and its words stay on the card. GPT confirmed `30f2bd7c` with no
findings (see "The 嫌 や finding and its follow-up" below).

`30f2bd7c` descends from `20f0db4c`, the `origin/main` of the time, through the
freeze; no merge of `origin/main` was needed. Two commits follow the freeze and
change teaching content: `10d79652` (the 15 cards, `words/応援.md` and
`manifest.json`) and `30f2bd7c` (`kanji/嫌.md` and `manifest.json`). Fourteen of
the fifteen cards at `30f2bd7c` are byte-identical to the versions at
`10d79652` that both confirmations examined without a finding on them; the
fifteenth, 嫌, was confirmed by the GPT reviewer alone (see Limits). The commit
that adds this record changes only `docs/`, which the content archive excludes,
so the teaching content, `manifest.json` and the budgets are exactly those gated
at `30f2bd7c`. The tree was checked mechanically (see below). No native,
rendered, phone, CI or archive credit is claimed by this record; publication is
recorded separately.

## Teaching scope

| File | Change |
|---|---|
| `kanji/張.md` `器.md` `素.md` `応.md` `仮.md` `基.md` `価.md` `激.md` `嫌.md` `縮.md` `騒.md` `統.md` `級.md` `整.md` `暖.md` | 15 new N1 cards |
| `strokes/<kanji>.json` for the same 15 kanji | generated stroke data (KanjiVG revision `70a0b7ae`) |
| `words/` 93 existing articles (one frozen diff each in `packet/diffs/`, named `words__<article>.md.diff`) | each gains one link `[X](../kanji/X.md)` to a batch kanji, 93 links in all (張 8, 器 7, 素 7, 応 7, 仮 7, 基 7, 価 6, 激 6, 嫌 6, 縮 6, 騒 6, 統 5, 級 5, 整 5, 暖 5); 90 articles only wrap a kanji, while `応援.md`, `整備.md` and `物騒.md` also correct or drop a stale "has no card" statement; 96 lines are replaced in all (91 articles change one line, 整備 two and 応援 three); `応援.md` was revised once more after the freeze |
| `manifest.json` | regenerated index, not reviewed content |

At `30f2bd7c` the payload went from 8,511 to 8,541 manifest entries (kanji
1,146 to 1,161, strokes 1,146 to 1,161, words 5,082 unchanged) and
`contentVersion` from `fe02221511f427e5` to `18d0f3df4071aa30`. The freeze had
`3f0f13d8a00f4fd5` and `10d79652` had `eb332dd7994dd3ba`; the sixteen files
revised after the freeze (the 15 cards and `words/応援.md`; 嫌 twice) account
for the difference. The local archive went from 8,533 to 8,563 entries.

## Reviews

All times are UTC. The two initial runs took place on 2026-11-11 and the other
four on 2026-11-12; the six runs did not overlap. The actual model is taken
from each session's usage record, not from the requested model. The first four
runs each covered all four facets (correctness, scoped coverage, consistency
and quiz safety, comprehensibility). The two initial runs, made at reasoning
effort `high`, were told which facets to examine deepest; each confirmation was
asked to check every changed line for new defects on all four facets and to
give a disposition for every item of the author's statement. The audits do not
record the reasoning effort of the four later runs. The last two runs are
narrower GPT-only rounds: `followup-gpt` is the follow-up on the open 嫌
finding, with the author's claims C1-C13, and `followup2-gpt` is the delta
confirmation of the one-card change, with the claims N1-N10.

| Run | Actual model | Snapshot | Window (UTC) | API requests | Tool calls (max in flight) | Examined deepest |
|---|---|---|---|---|---|---|
| `initial-claude` | claude-opus-5.5 | `453af714` | 11-11 22:11:07-22:22:05 | 61 | 62 (2) | correctness, scoped coverage |
| `initial-gpt` | gpt-6.1-sol | `453af714` | 11-11 22:30:01-22:51:42 | 98 | 98 (1) | consistency and quiz safety, comprehensibility |
| `confirm-claude` | claude-opus-5.5 | `10d79652` | 11-12 00:35:04-00:39:28 | 29 | 29 (1) | revised text, all facets |
| `confirm-gpt` | gpt-6.1-sol | `10d79652` | 11-12 00:42:15-00:53:55 | 89 | 89 (1) | revised text, all facets |
| `followup-gpt` | gpt-6.1-sol | `10d79652` | 11-12 03:09:38-03:27:29 | 68 | 68 (1) | the open 嫌 finding and claims C1-C13 |
| `followup2-gpt` | gpt-6.1-sol | `30f2bd7c` | 11-12 06:31:13-06:43:20 | 38 | 38 (1) | the one-card delta and claims N1-N10 |

The initial verdicts differed in detail and agreed on two defects. Claude
judged scoped coverage and the 93 word diffs CLEAN, correctness DEFECTS (器
major; 価, 激 and 応 minor), consistency and quiz safety "CLEAN with one minor
defect" (嫌 without 怪) and comprehensibility DEFECTS (minor: 器, 価 and 応).
GPT judged scoped coverage CLEAN and correctness, consistency and quiz safety,
and comprehensibility NEEDS FIX, with five minor findings; of the 93 word diffs
only 応援 needed a fix. It also marked the fallback reading options UNVERIFIED
for 23 of the 32 reading rows of the supplied simulation, which does not name
them. Both reviewers independently reported the 価 and 嫌/怪 defects.

Later rounds: the Claude confirmation returned CONFIRMED with findings none.
The GPT confirmation resolved its five earlier findings, judged the
meaning-quiz options of all 15 cards defensible and returned NEEDS FIX for one
new minor finding on 嫌 (や). The follow-up returned NEEDS FIX: it rejected the
author's decline of that finding and reported three minor findings on the
author's own claims (FU1-FU3). The delta confirmation of `30f2bd7c` returned
CONFIRMED with findings none.

The two initial runs did not receive identical evidence. The GPT prompt also
named a supplement (`supplement/`): the complete quiz simulation for all 15
cards and text extracts of 14 pages of the official Joyo table. It was built
between the two initial runs (22:27:45-22:29:28), after Claude's run had ended.
The initial packet's `mechanical-checks.md` keeps only the last 4,000
characters of each automatic check, so the start of the simulation was cut off
for Claude, which judged the options of 張, 器 and 素 from their front matter
and titles. Its two attempts to read the official Joyo table also failed (the
PDF on bunka.go.jp returned binary it could not read as text and a Wikisource
page returned 404), so its claims that depend on that table were UNVERIFIED in
that round. Both confirmation packets carry the complete simulation and the
Joyo extracts, and the Claude confirmation resolved both limits. The author
began drafting fixes while the initial GPT review was still running; the frozen
commit and the packet were not touched.

Each reviewer worked from a frozen packet of one snapshot: the initial packet
(built at 22:09:52 on 11-11 from `453af714`, 6,491 files) for both initial
runs, a confirmation packet for each family (built at 00:32:39 and 00:33:27 on
11-12 from `10d79652`, 56 files each), a follow-up packet for the GPT follow-up
(built at 03:01:54 from `10d79652`, 53 files, with a subset of the Android
sources at app commit `10d98d0d`) and a delta packet for the final GPT run
(built at 06:30:06 from `30f2bd7c`, 46 files). In the initial round neither
reviewer saw the other's report or the author's rationale. In the confirmation
round each reviewer saw the author's statement on its own findings (claims to
verify, not evidence), a neutral change list, the exact patch, the new evidence
and the automatic checks, and no other reviewer's report. The follow-up and
delta rounds went to the GPT reviewer only: the author's statement with the
claims C1-C13 and then N1-N10, the new checks and evidence and, for the delta,
a neutral change list and the exact patch. Each later run continued the session
of its family's initial review (Claude `e50d3a0c`, GPT `f10f8ee7`); the three
later GPT audits also record a re-read of the reviewer's previous report, the
Claude audits record none.

Serial tool work was required of every reviewer, and the audits record how it
went. Five of the six runs were strictly serial, with at most one call in
flight: the Claude confirmation and all four GPT runs. The initial Claude run
issued one overlapping start, two `view` calls at 22:11:44.827, about 37
seconds into the run (up to two calls in flight). The audit flag "recursive
shell commands over packet directories: 2" on the initial GPT run is a false
positive: the two matches are the power operator in a Bézier script (`s**3`,
`t**3`) and a `'**'` string in a `startswith` tuple, and neither lists a
directory. The audits classify none of the shell commands as writing a file,
and each run wrote only its own report. The runs issued 25, 55, 15, 7, 5 and 4
shell commands, in table order. This record therefore claims strictly serial
work for five runs and one overlapping start for the sixth.

In three audits (both initial runs and the Claude confirmation) `outsidePaths`
is empty. In the other three it holds one entry, the bare `review-packets`
directory, which those runs' inline Python scripts used as the base path of the
allowed packet paths. No other path outside the allowed ones is recorded.

The prompts allowed public web sources, and the two GPT follow-up prompts also
allowed the raw Android files at the pinned commit. The audits record 5, 4, 0,
11, 5 and 1 web-tool calls, in table order (public dictionary and Joyo pages;
in the follow-up also three Android sources from raw.githubusercontent.com).
The audits count only the web tools, so the author also scanned the session
event logs for network calls made inside shell scripts: 15 shell commands of
the initial GPT run (11 to Weblio, one to kanjiapi.dev and three to
raw.githubusercontent.com for KanjiVG), one of the GPT confirmation and two of
the follow-up; the delta run and both Claude runs made none.

`reports/` holds the six verbatim reports, stored with LF line ends; their
SHA-256 values equal the `reportSha256` of the audits. `prompts/` holds the
exact prompts as the reviewers received them; each audit records exactly one
user message, so no steering message was sent in any run. `scope-audits/` holds
the read-scope and model-identity audits. An audit's `reviewAccepted: false` is
by design: it records read scope and model identity only, not acceptance.

`packet/` holds the initial packet's instructions and mechanical checks, a
gzipped manifest (the SHA-256 of each of its 248 named files and one aggregate
hash of the 6,243-file repository context export), the 93 word diffs and the
evidence (JMdict digest and families, KANJIDIC2 records, pinned source metadata
and the 15 Digital Daijisen extracts from Weblio). The snapshot cards, strokes
and words are the Git blobs at `453af714` and are not copied. `confirm-packet/`
holds the 38 files common to both confirmations (change list, exact patch,
cited JMdict entries, Joyo table extracts and two page crops for 器, KanjiVG
records for 器 and 激, `QuizBuilder.kt`, `KanjiReadings.kt`, `Words.kt` and the
automatic checks), each family's instructions, author's statement and file
manifest, and the packet provenance. `followup-packet/` (39 files) holds the
follow-up's instructions, the author's statement (claims C1-C13), the runs of
the app's real reading-quiz code on this snapshot's cards, the reading-exposure
scan, the author's tools and the Android source subset. `delta-packet/` (32
files) holds the delta round's change list, the author's statement (claims
N1-N10), the exact patch, the gate logs and checks re-run at `30f2bd7c` in
`checks/`, and the evidence. `supplement/` (16 files) holds what the initial GPT
run received in addition.

Three SHA-256 values in `provenance.json` refer to packet files that are not
stored here and cannot be checked from this folder: `packet.manifestSha256`
(the hash of the full manifest as JSON with sorted keys; the stored manifest
folds the 6,243 context files into one aggregate and so hashes differently) and
the `packet.titlesSha256` entries for `kanji-titles.tsv` and `word-titles.tsv`.

## Reconciliation

Item labels: Claude's F1-F5 and O1-O6 are the labels in its own report.
Claude's `L1`-`L3` are questions the author added in
`confirm-packet/claude/RESPONSE.md` (the Joyo table claims, the options for 張 器
素, and the reading prompts). GPT's initial report numbers its findings 1-5;
`#1`-`#5` (with `#3a`, `#3b`, `#4a` and `#4b`), `OA`, `OB` and `L1`-`L4` are the
labels the author gave those findings, GPT's optional points and its stated
limits in `confirm-packet/gpt/RESPONSE.md`. The GPT confirmation numbers its one
new finding 1; `FU1`-`FU3` are the author's labels for the three findings of
the follow-up, `C1`-`C13` its claims in `followup-packet/RESPONSE.md`, and
`D1`-`D6` and `N1`-`N10` the sections and claims of `delta-packet/RESPONSE.md`.
Line references are to the cards at `30f2bd7c`.

| Item | Disposition |
|---|---|
| Claude F1 (major), 器: the mnemonic described the centre of the character as 犬 "dog". The modern Joyo 器 has 大 there (15 strokes: four 口 and 大); the 犬 centre belongs to the older 16-stroke form that the Joyo table prints in round brackets as the compatibility ideograph U+FA38. GPT's initial report did not mention it. | Rebuilt in `10d79652`: the mnemonic now names 大 and says the centre has no dot (`器.md:29`), and a new paragraph explains the older form (`器.md:27`). Stroke data unchanged. Evidence in `confirm-packet/common/evidence/`: the Joyo page 33 extract, two page crops and KanjiVG `05668.svg`. Claude RESOLVED (and its L1); the GPT confirmation judged correctness CLEAN, checking the claim against the crops and KanjiVG, not the original PDF. |
| Claude F2 and GPT #1 (both minor, independent), 価: the sentence on 価格 contradicted itself ("In 価格, 格 supplies カク, so 価 is か in both syllables of かかく."). | `価.md:37` now reads 価 as か and 格 as supplying カク, the same split as `words/価格.md:25`. Both RESOLVED. |
| GPT #2 (minor), 応援: `words/応援.md` said that neither 応 nor 援 had a kanji card, although 応 is in this batch. | `words/応援.md:32-33` now says "Both written characters belong in the word, though 援 does not have a kanji card here." (there is no `kanji/援.md`); the link to 応 at `:30` was already in the freeze. This is the only word article changed after the freeze. RESOLVED. |
| Claude F3 (minor) and GPT OB (optional; the same passage), 激: the mnemonic placed 白 "at the top right" and 放 as a unit "below it"; in the character 白 sits above 方 in the middle and 攵 stands at the far right. | `激.md:27` now says 氵 at the left, 白 over 方 in the middle and 攵 at the far right, with 方 and 攵 together making 放 (KanjiVG `06fc0.svg` in `confirm-packet/common/evidence/`). Both RESOLVED. |
| Claude F4 (minor), 応: the card said 用 supplies ヨウ, "which is why ヨウ appears in the word without being a reading of 応", while the same card has a ヨウ row. | `応.md:40` now says "In 応用, 応 is read オウ and 用 supplies ヨウ."; the ヨウ row (`:34`) and the Daijisen paragraph (`:44`) agree. Claude RESOLVED. |
| Claude F5 (minor) and GPT #3a (independent), 嫌/怪: 嫌 is titled "dislike; suspicion" and excludes 疑, but not 怪 "suspicious; uncanny". | 怪 added to the exclusions of 嫌 (`嫌.md:14`, `[憎, 疑, 怪]`) and to the overlap note (`嫌.md:60`). It is declared on 嫌 only, because the app's `QuizBuilder` treats an exclusion as symmetric; `怪.md` is unchanged. Both RESOLVED. |
| GPT #3b (minor), 素/料: 料 "materials, fee," overlaps the material sense of 素 but was not excluded. | 料 added to the exclusions of 素 (`素.md:14`) and to the overlap bullet (`素.md:61`; JMdict 1260670 supplies the material and ingredient sense of 素). `料.md` is unchanged. RESOLVED. |
| GPT #4a and #4b (minor), 応/募 and 級/校: exclusions whose claimed overlap does not hold. | Both exclusions removed (`応.md:14`, `級.md:14`) and dropped from the overlap bullets (`応.md:60`, `級.md:55`); new contrast bullets say why: 募 is the recruiting side of 応募 (`応.md:61`), and 学校 is the school itself while a 学級 is one class within it (`級.md:56`). Neither `募.md` nor `校.md` declares an exclusion. RESOLVED. |
| GPT #5 (minor), 基 and 素: at the freeze a 264-word paragraph in `基.md:35`, a 244-word one in `素.md:35` and openings of 161 and 138 words. | The long paragraphs were split (基 into six, `基.md:37, 39, 41, 43, 45, 47`; 素 into five, `素.md:37, 39, 41, 43, 45`) and the openings cut to 37 and 36 words (`:23` in both). The word lists dropped from the openings stay in the readings tables and the common words, and no reading, qualification or citation was deleted. The longest paragraph of 基 is now 88 words (`基.md:25`), of 素 82 (`素.md:25`); the longest of any card is 99 words (`暖.md:23`). RESOLVED. |
| Optional points adopted: Claude O1 (素: the ス row omitted 素敵 and 素晴らしい), O2 (嫌: "older compounds"), O3 (縮 and 騒: "read as a whole word", then split) and O5 (応: まさに). | O1: `素.md:39` and `:63` (JMdict 1397350 and 1397300; 素敵 and 素晴らしい stay unlinked). O2: `嫌.md:23` now says "in a few compounds"; "formal" was not used because JMdict 嫌疑 (1257320) carries no register tag. O3: `縮.md:56` and `騒.md:56` ("In this word 縮 is read ちり, which is not one of the readings above."; likewise さい for 騒). O5: `応.md:38` (JMdict 1376640 正に, 2856503 将に, 2856504 当に; まさに is usually written in kana). Claude RESOLVED. |
| Declined by the author and accepted by the reviewers: Claude O4 (a link on half of the unit 仮名 in `words/仮名遣い.md`), O6 for 整 and for 嫌い (glosses), and GPT OA (long openings and word inventories on the other cards). | O4: `words/仮名遣い.md:24` has no stand-alone 仮 anywhere, so the contracted unit 仮名 is where the link goes. O6 (整): `整.md:23` keeps "maintenance or putting in place" (JMdict 1376240: "maintenance; servicing"; "putting in place; development"). O6 (嫌い): `嫌.md:36` keeps "disliked; dislike" (JMdict 1257240 sense 1 is "disliking; hating; detesting"; the article title is "disliked, dislike"). OA: partly adopted (only 基 and 素 were shortened); the 13 other openings are 38 to 99 words, the longest `暖.md:23`. DECLINE ACCEPTED by Claude and GPT. |
| Claude confirmation, optional notes on `暖.md:42` ("it" refers to ノン) and `暖.md:40` (the Joyo "⇔ 温" note applies only to あたたか). | Not adopted: only paragraph breaks of 暖 differ from the freeze, so the confirmed text stays as confirmed. |
| Limits raised in the confirmations: Claude L1 (Joyo claims), L2 (options for 張 器 素), L3 (reading prompts); GPT L1 (fallback reading options), L2 (no quiz implementation in the initial packet), L3 (Joyo claims compared only with text extracts), L4 (its other stated limits). | Claude L1 and L2 RESOLVED by the Joyo extracts and the complete simulation in the confirmation packet. Claude L3 RESOLVED: it found no wrong option that is a valid reading of its card in the audit's pool; the only unlisted reading it could draw was お for 応 オウ (3 of 200 seeds; KANJIDIC2 lists it only as a nanori). The author later corrected the pool statement and the audit's inventory (see the 嫌 section below). GPT L2 RESOLVED (the confirmation packet carries `QuizBuilder.kt`, `KanjiReadings.kt` and `Words.kt`). GPT L1 and L3 were PARTIALLY RESOLVED in its confirmation; after the follow-up L1 stands as RESOLVED, a bounded evidence limit, and L3 is accepted as a disclosed, non-blocking limit; L4 needed no disposition. GPT also corrected the author's count (the reading queue has 26 prompts, not 32 rows) and noted that an artificial two-card pool of 騒 and 西 gives ソウ the wrong labels セイ, サイ and ス. |
| GPT confirmation finding 1 (minor, new), 嫌: the contraction や as a wrong option for the prompt いや. | See "The 嫌 や finding and its follow-up" below. Resolved in `30f2bd7c`. |

Two model families reviewed the batch, each on all four facets. That meets the
issue-60 requirement of at least two families per batch on one fixed snapshot
with independent blind initial findings, with fixes confirmed by the original
reviewers; the one exception to a joint confirmation is the one-card change in
`30f2bd7c`, which the GPT reviewer that raised the finding confirmed alone (the
Claude reviewer confirmed `10d79652`). The repository rule of three facet-split
reviewers from three model families (`.github/copilot-instructions.md`,
"Independent review and reconciliation") applies to a new word card or learner
article, a new app-facing file under `words/` or `articles/`. Batch 110 adds no
such file, and its 93 word edits only wrap kanji in links (three also correct
or drop a stale "has no card" statement), so review stays proportional. That
reading is the author's and is repeated under Limits.

### The 嫌 や finding and its follow-up

The GPT confirmation of `10d79652` reported that the attested contraction や of
嫌 could be offered as a wrong option for the reading prompt いや. JMdict (entry
1587610) lists や for 嫌 without restriction, and Digital Daijisen has
や【▽嫌／×厭】 as a sound change of いや; KANJIDIC2 lists ケン, ゲン, きら.う,
きら.い and いや, not や. The option builder excludes only readings listed on
the target card, so nothing stopped や from being drawn. GPT's minimal case is a
pool of 嫌 and 屋. The author's Kotlin cross-check, which runs the app's real
option code on this snapshot's cards, offered や in 400 of 400 seeds for both
きらう and いや in that pool, while the ゲン prompt offered おく
(`followup-packet/checks/kotlin-reading-run.txt:85-87`).

In the N1 and All stacks (1,161 cards each) the いや prompt never drew や
(`followup-packet/checks/kotlin-reading-run.txt:50-51`). A short Starter
"Practice more" session is different: the app pads its pool with borrowed cards
(at app commit `10d98d0d` only the Starter stack is padded), and with 嫌 as the
borrowed card the pool is the 118 Starter cards plus 嫌. There the いや prompt
drew や in 1,310 of 4,000 seeds, while the ゲン and きらう prompts did not
(`followup-packet/checks/kotlin-starter-run.txt:35`,
`followup-packet/checks/kotlin-vs-exact.txt:104`,
`followup-packet/RESPONSE.md:74`).

The author first declined to change the card: the finding stood as a
documented limitation, backed by a corrected audit, the real Kotlin code run on
the pools the app builds, a disclosed remaining production path (the
borrowed-card Starter session) and two client proposals. The GPT follow-up
rejected that answer (DECLINE REJECTED) and named the mitigation it would
accept: remove only いや from `quizKunyomi`; keep `kunyomi`, the いや row and its
vocabulary; and update the practice-selection paragraph.

The follow-up also found three minor errors in the author's statement, all
accepted. FU1: the production conditions were described too restrictively, as
嫌 with 兼, or with 兼 and 験, in a short Starter session can still offer や.
FU2: the length filter of `mutations` applies to the generated output, so
`mutations("お")` yields `おう`. FU3: JMdict's イヤ is the entry's kana-only
reading (`re_nokanji`); the や attestation itself was verified.

`30f2bd7c` applies the mitigation. `嫌.md:12` reads `quizKunyomi: [きら.う,
きら.い]`, while `kunyomi` (`:10`) still lists いや; the いや row ends "not
selected for questions here" (`:37`) and the selection paragraph names ゲン,
きら.う and きら.い (`:43`). The card now asks two reading prompts (ゲン and
きらう) instead of three, and the batch's reading-prompt list has 25 entries
instead of 26.

A new paragraph (`嫌.md:45`) says that JMdict lists や as a further reading of
嫌, that Digital Daijisen explains it as a sound change of いや, that KANJIDIC2
does not list it and that a question about いや could show や as a wrong
option. It adds: "This is a teaching selection, not a claim that いや is
invalid, obsolete or rare."

The delta confirmation of `30f2bd7c` (GPT only) returned CONFIRMED with
findings none. It resolved F1 by content selection (not by claiming that the
client mechanism was repaired) and FU1-FU3, and verified N1-N9 with
qualifications: N5 (the pools the client builds never drew や for 嫌) at source
and record level, claiming no new Kotlin run; N6 (no pool the client builds can
offer や) as an argument over the fixed snapshot, not an enumeration; N8 without
an independent whole-tree count of the phrase "wrong option". N10 (that the
gates of `30f2bd7c` passed) was not independently verified.

Artificial small pools would still permit や as a wrong option: `[嫌, 屋]`,
`[嫌, 家]` and `[嫌, 八]` for きらう, and `[嫌, 夜]`, `[嫌, 冶]` and `[嫌, 野]`
for ゲン; the real code drew や in all 400 seeds of each
(`delta-packet/checks/kotlin-vs-exact.txt:54, 56, 58, 59, 61, 63`). For きらう
the pool `[嫌, 冶]` has no valid wrong option at all (`:62`). These pools are
not shipped, and the client builds no such pool at `10d98d0d` (N6 and N7,
`delta-packet/RESPONSE.md:97-98`). The author claims no universal property.

The follow-up also corrected three earlier statements of the author
(`followup-packet/RESPONSE.md:36-47`). The confirmation packets said that the
audit pool was every card in `kanji/` while the app draws from the cards the
learner has studied (`confirm-packet/claude/RESPONSE.md:116-117`,
`confirm-packet/gpt/RESPONSE.md:115-116`,
`confirm-packet/common/CHANGES.md:98-99`). For N1 and All the readings screen
in fact builds its pool from the whole stack (all 1,161 cards of the snapshot);
only a short Starter session has another pool.

The audit's "0 problem(s)" for 嫌 was wrong because its inventory lacked the
single-kanji entries of JMdict, which attest や; the older
`confirm-packet/common/checks/reading-options.txt` still has that gap. The
intermediate conclusion that や cannot be drawn in any pool had missed the
padding path and was withdrawn. The corrected inventory (KANJIDIC2 on, kun and
nanori readings, the single-kanji entries of JMdict and readings printed in the
card text; `followup-packet/RESPONSE.md:142-144`) belongs to the
reading-exposure audit, whose 嫌 section lists や
(`followup-packet/checks/reading-exposure.txt:167-168`). The delta packet's
`reading-options.txt` still comes from the older tool and names や for 嫌 only
because it was run with `--extra 嫌=や`
(`delta-packet/evidence/README.md:125-128`).

The author proposed two client changes to the owner and counts neither as
protection. (A) A data-driven list of attested extra readings that only the
option builder's excluded-key set reads, so that `onyomi` and `kunyomi` stay
equal to KANJIDIC2; it needs a new content field, a parser change and a schema
change, coordinated with issue #61. (B) A generic rule that rejects a wrong
option that is a prefix or suffix of a reading of the target, a shortened or
contracted form; it needs no content field and would catch this case and, for
example, 寝 い.ぬ→い and 神 かみ→み from the scan, but not 前 まえ→さき
(`followup-packet/RESPONSE.md:119-128`). The author opened no work item;
whether to track one is the owner's decision.

The exploratory scan of every card
(`delta-packet/checks/reading-exposure.txt:309-340`) found 305 cards with JMdict
single-kanji readings beyond their own and checked 887 prompts in the N1, All
and Starter pools. It lists 19 hits in whole-stack pools and 12 further hits
that occur only in a Starter session that borrows the card. These are
untriaged, heuristic leads on cards outside this batch, not findings, and the
author changed none of those cards. GPT's mechanical recount of the 19
whole-stack lines at `10d79652` found nine distinct prompts on eight cards
(`reports/followup-gpt.md:58`); the author names them as 冠 前 寝 日 片 真 神 酒
(`followup-packet/RESPONSE.md:215-217`).

## Byte identity

`provenance.json` records the snapshots, the packet and the six runs (session,
actual models, window, API requests, tool calls and the SHA-256 of each report,
prompt and audit). Of the 123 teaching files at the freeze (15 cards, 15 stroke
files and 93 word articles), 107 are the same Git blobs at `30f2bd7c`: all 15
stroke files and 92 of the 93 word articles. The other 16 (the 15 cards and
`words/応援.md`) changed. `git diff --shortstat 453af714 30f2bd7c` shows 17
files (those 16 and `manifest.json`), 163 insertions and 63 deletions; against
the base `20f0db4c` the whole batch is 124 files, 1,160 insertions and 190
deletions, with no new `words/` or `articles/` file. Between `10d79652` and
`30f2bd7c` only `kanji/嫌.md` and `manifest.json` differ.

Five cards (張 仮 統 整 暖) differ from the freeze in whitespace only (paragraph
breaks); the other ten (器 素 応 基 価 激 嫌 縮 騒 級) changed wording,
exclusions or notes. The front matter changed in five lines of four cards:
`quiz_exclusions` of 素 (+料), 応 (-募), 嫌 (+怪) and 級 (-校), and
`quizKunyomi` of 嫌 (-いや); the titles, tags, KANJIDIC2 readings and curated
distractors of all 15 cards are unchanged. Counting the prose paragraphs of the
Meaning and origin and Readings sections (tables and bullets excluded), the
cards had 45 at the freeze, three per card, the longest 264 words (`基.md:35`);
at `30f2bd7c` they have 94, the longest 99 words (`暖.md:23`, an opening that
was already that long at the freeze).

The snapshot copies in the initial packet have Windows (CRLF) line ends while
Git stores LF; for all 123 snapshot files, converting the blob at `453af714` to
CRLF reproduces the SHA-256 recorded in the packet manifest. Both confirmation
packets list the same 16 blob IDs (the 15 cards and `words/応援.md`); all 16
equal the Git blobs at `10d79652` and none equals the blob at the freeze. The
follow-up packet lists 15 card blob IDs, all equal to the blobs at `10d79652`.
The delta packet lists the 15 cards at `30f2bd7c` and, as their base, the 15 at
`10d79652`; all 30 equal the Git blobs, and exactly one card differs between
them: `kanji/嫌.md` (blob `13acf1ee9a693d6d5da019d72d97336f02b1c052` at
`10d79652`, `52a73a70028b01a97295820ff08eb78ee7487287` at `30f2bd7c`). Converted
to LF, the 嫌 card has these sizes and SHA-256 values:

- `10d79652`: 5,379 bytes,
  `622980074175867923a1f1a6a569721295ce74f247327637ce36073700f3f302`
- `30f2bd7c`: 5,736 bytes,
  `033867582ec3df45d00a0311caf74d0594c22bfb8ff7f18428ed82ac94842312`

`10d79652` was made by amending an earlier local fix commit, `abd5dbe6`, that no
reviewer was shown and that was never published; no run of this record falls
between 22:51:42 on 11-11 and 00:35:04 on 11-12. Both confirmation packets were
built from `10d79652` (00:32 UTC on 11-12).

## Integrated-tree checks (mechanical, not reviewer credit)

At `30f2bd7c`: lint 0 errors and 17 warnings (16 existing word articles whose
Dictionary line cites no JMdict entry id, and `words/嫌い.md`, which has no
Dictionary line; none concerns a new card and no changed line in `words/` is a
Dictionary line); 431 unit tests pass; validation 0 errors; budget 8,563
entries, 45,176,219 retained bytes, 45,447,529 inflated, 30,575,129 local ZIP
bytes; vocabulary 2122/2431; manifest rebuild shows no diff. The option
simulation (`delta-packet/checks/quiz-safety.txt`) reports 0 errors and 0
warnings and shows three wrong titles in the meaning quiz for each of the 15
cards; none of them is among the 11 existing cards that fall back to
tag-similar options. The link checks find no unresolved link: 109 links on the
lines changed up to `10d79652` (`confirm-packet/common/checks/link-targets.tsv`)
and the 2 links of the changed line `嫌.md:37`
(`delta-packet/checks/link-targets.tsv`). The reading-option audit
(`delta-packet/checks/reading-options.txt`) ends with "0 problem(s)", and the
reading-exposure scan reports for the 15 cards 0 production hits, 0
padded-session hits and 5 latent collisions (an attested reading offered by
another card that no pool the app builds can draw;
`delta-packet/checks/reading-exposure.txt:307`). The Android JVM tests
`RealContentTest`, `RareHanTest` and `KanjiReadingsTest` (commands at
`delta-packet/evidence/README.md:121-124`) ended BUILD SUCCESSFUL; the logs
record no test counts, so none is claimed. The author's Kotlin cross-check
checked 50 whole-stack-pool prompts, 25 Starter-session prompts and 26
small-pool prompts with 0 problems (last line of
`delta-packet/checks/kotlin-vs-exact.txt`). There is no merge in the tree:
`origin/main` was still `20f0db4c` when this record was written.

## Limits

- The review judged text, printed simulations of the answer-option builder, a
  reading-option audit and source-level reads of the app's quiz code
  (`QuizBuilder.kt`, `KanjiReadings.kt`, `Words.kt` and, in the follow-up
  rounds, a subset of the Android sources at app commit `10d98d0d`), not a
  running app. No APK, emulator or UI run is involved. The analysis of the
  reading prompts applies to that app commit and to the pools its code builds;
  the Kotlin cross-checks are the author's scratch test, which was never
  committed to the Android repository.
- Reviewers used pinned dictionary snapshots (JMdict, KANJIDIC2, Digital
  Daijisen extracts, KanjiVG at `70a0b7ae`) and public pages (Weblio,
  jisho.org, the official Joyo table). The live dictionaries may differ
  slightly.
- Joyo table: the Claude initial run could not read the PDF, so its Joyo-based
  claims were UNVERIFIED in that round. The Claude confirmation used text
  extracts made with pdfplumber, with page crops for 器; the GPT confirmation
  compared the claims with the same extracts and checked the 器 claim against
  the crops and KanjiVG, not against the original PDF pages. GPT accepted that
  as a disclosed, non-blocking limit. The initial Claude run also lacked the
  supplement, and its view of the simulation was cut off for 張, 器 and 素.
- The confirmations covered the changed passages, not an exhaustive re-review.
  The GPT confirmation did not reopen the other 92 word articles or the 15
  stroke files. The Claude confirmation did not re-run the simulation or the
  link and lint checks, compared the fix by tokens instead of reading the
  patch, made no new web lookup and did not reopen `words/仮名遣い.md`.
- The final delta round was GPT only: Claude did not see the one-card change to
  嫌. N10 (that the gates of `30f2bd7c` passed) was not independently verified;
  N5 rests on the author's recorded runs; N6 is an argument over the fixed
  snapshot, not an enumeration of pools. Starter sessions that borrow several
  cards were argued, not enumerated, and artificial small pools such as
  `[嫌, 屋]` still permit や for きらう (not shipped).
- Phone APK: the last phone APK delivered to the owner was built from app
  commit `5c000bd`; its installation was not verified. That build predates app
  commit `2edbf36` ("Honor explicit kanji meaning pair exclusions"; in the
  Android history `5c000bd` is an ancestor of `2edbf36`, which is an ancestor of
  `10d98d0d`), so it ignores kanji `quiz_exclusions`
  (`followup-packet/RESPONSE.md:220-227`; the author's later search of the
  Android repository, which is not part of any reviewed packet, finds no
  exclusion code in `QuizBuilder.kt` at `5c000bd`). The pair exclusions of this
  batch therefore protect only builds from `2edbf36` onward. The same search
  finds that `ReadingData.kt` at `5c000bd` already derives the asked readings
  from `quizKunyomi` (`askKun`, line 15), but that build's pool construction
  differs (`followup-packet/evidence/android/compare-5c000bd-to-10d98d0d.txt`)
  and the author did not analyse which wrong options it can offer for 嫌. The
  GPT follow-up did not establish which APK was built, copied or installed, nor
  authenticate the `2edbf36` boundary (`reports/followup-gpt.md:59`).
- Scan leads: the reading-exposure scan of every card is heuristic, and its 31
  leads on cards outside this batch are untriaged.
- Strokes: the GPT initial run compared all 15 stroke files with KanjiVG
  `70a0b7ae` (largest endpoint discrepancy about 0.071 viewBox units, largest
  stored-point distance about 0.174 units in the 109-unit viewBox); the Claude
  initial run checked stroke counts and 器 only. The reviews did not render the
  stroke animations, no native-speaker panel assessed sentence naturalness and
  no one tried the cards on a phone. No end-to-end reading-runtime or
  older-client certification is claimed.
- Strictly serial tool work is claimed for five of the six runs; the initial
  Claude run had one overlapping start (see Reviews).
- Two families, not three: the three-family rule covers new `words/` and
  `articles/` files, of which this batch has none, and the final delta round
  was confirmed by one family. A third-family read can be added if the owner
  wants one.
- No native emulator, rendered, physical-phone, older-client or handwriting
  credit. The issue-60 batch cycle does not require a native run per batch; the
  plan is one native smoke at a milestone or the final acceptance.
- The multi-megabyte session event archives of the reviewers remain local and
  are not committed.
