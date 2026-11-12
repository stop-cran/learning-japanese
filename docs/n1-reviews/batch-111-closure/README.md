# Batch 111 (修 句 房 授 敷 旬 標 独 率 節 義 製 評 養 鏡): two-family textual review closure

This directory closes the independent textual review of batch 111 and preserves
its evidence. The batch adds fifteen N1 kanji cards with their stroke data and
links the new kanji in sixty existing word articles; it adds no new word
article. The fifteen are the absent frozen rows that exactly four existing word
articles declare: there are sixteen, and 従 is deferred because no existing
article uses its reading ジュウ. Two reviewers from two different model
families, Claude and GPT, read the same frozen draft (`3b30803e`) on all four
facets without seeing each other's work. Claude reported two low findings (敷
and 鏡) and four optional notes. GPT reported two minor findings (節 lacked
direct exclusions with 句 and 旬, and 義 excluded 税, "tax; fiscal duty," as if
it overlapped 役 and 務) and two optional points; the two reports share no
finding. The author
changed six cards in `bf9ee962` and answered the remaining points with reasons.
Claude then CONFIRMED that commit with no findings. GPT resolved both of its
findings and its optional point OB, accepted the author's answer to OA and found
no new defect, but returned UNVERIFIED with findings none: its limit L1 (the
quiz audits are supplied Python ports, not an executed Android client) stayed
only partially resolved, and it wrote that the contract does not permit
CONFIRMED while L1 remains so.

The author accepts L1 as a disclosed, non-blocking, bounded evidence limit, as
batch 110 accepted its L3, and ran no further round. This record therefore
claims no joint CONFIRMED: the Claude confirmation is CONFIRMED and the GPT
confirmation is UNVERIFIED with findings none and L1 partially resolved (see
Reviews and Limits).

`bf9ee962` descends from `f40a1391`, the `origin/main` of the time, through the
freeze; no merge of `origin/main` was needed. One commit follows the freeze and
changes teaching content: `bf9ee962` (six cards and `manifest.json`). Nine of
the fifteen cards (修 句 授 旬 標 独 率 製 養), all sixty word articles,
`kanji/価.md`, `kanji/暖.md` and all fifteen stroke files at `bf9ee962` are
byte-identical to the freeze; the other six cards (房 敷 節 義 評 鏡) differ.
The commit that adds this record changes only `docs/`, which the content
archive excludes, so the teaching content, `manifest.json` and the budgets are
exactly those gated at `bf9ee962`. The tree was checked mechanically (see
below). No native, rendered, phone, CI or archive credit is claimed by this
record; publication is recorded separately.

## Teaching scope

| File | Change |
|---|---|
| `kanji/修.md` `句.md` `房.md` `授.md` `敷.md` `旬.md` `標.md` `独.md` `率.md` `節.md` `義.md` `製.md` `評.md` `養.md` `鏡.md` | 15 new N1 cards |
| `strokes/<kanji>.json` for the same 15 kanji | generated stroke data (KanjiVG revision `70a0b7ae`) |
| `words/` 60 existing articles (one frozen diff each in `packet/diffs/`, named `words__<article>.md.diff`) | each gains one link `[X](../kanji/X.md)` to a batch kanji, 60 links in all (four for each of the 15 kanji); 59 articles only wrap a kanji, while `句読点.md` also drops the stale sentence "There is no 句 card currently." (`words/句読点.md:25`) |
| `kanji/価.md`, `kanji/暖.md` (`packet/diffs/kanji__価.md.diff`, `kanji__暖.md.diff`) | the closing bullet of each card (`:54`) named one kanji that had no card (評 in 価, 房 in 暖); it now links the new card |
| `manifest.json` | regenerated index, not reviewed content |

At `bf9ee962` the payload went from 8,541 to 8,571 manifest entries (kanji
1,161 to 1,176, strokes 1,161 to 1,176, words 5,082 unchanged) and
`contentVersion` from `18d0f3df4071aa30` to `0c3d8f4a2c6bcb19`. The freeze had
`3f255571cd82aa08`; the six cards revised after the freeze account for the
difference. The local archive went from 8,563 to 8,593 entries.

## Reviews

All times are UTC. The four runs all took place on 2026-11-12 and did not
overlap. The actual model is taken from each session's usage record, not from
the requested model. All four runs covered all four facets (correctness, scoped
coverage, consistency and quiz safety, comprehensibility). The two initial
runs, made at reasoning effort `high`, were told which facets to examine
deepest; each confirmation was asked to check every changed line for new
defects on all four facets and to give a disposition for every item of the
author's statement. The audits do not record the reasoning effort of the two
confirmations.

| Run | Actual model | Snapshot | Window (UTC) | API requests | Tool calls (max in flight) | Examined deepest |
|---|---|---|---|---|---|---|
| `initial-claude` | claude-opus-5.5 | `3b30803e` | 11:26:01-11:36:13 | 83 | 84 (2) | correctness, scoped coverage |
| `initial-gpt` | gpt-6.1-sol | `3b30803e` | 11:44:41-12:09:46 | 87 | 87 (1) | consistency and quiz safety, comprehensibility |
| `confirm-claude` | claude-opus-5.5 | `bf9ee962` | 16:15:18-16:18:21 | 25 | 26 (2) | revised text, all facets |
| `confirm-gpt` | gpt-6.1-sol | `bf9ee962` | 16:20:45-16:32:13 | 57 | 57 (1) | revised text, all facets |

The initial reports share no finding. Claude judged correctness MINOR (F1, 敷;
F2, 鏡), scoped coverage CLEAN, consistency and quiz safety "CLEAN, with one
note" (the 鏡 title), comprehensibility "CLEAN, with one note" (the 敷 dash),
the 15 stroke files CLEAN and the 62 diffs CLEAN; it listed four optional notes
(O1-O4). GPT judged scoped coverage and comprehensibility CLEAN, and correctness
(義) and consistency and quiz safety (節 with 句 and 旬, and 義) NEEDS FIX, with
two minor findings and two optional points (OA, dense paragraphs; OB, the
ハン-to-バン step in 評判). GPT also supported the 鏡 title "mirror; lens" from
Kanjipedia's second sense ("めがね。レンズ。") and the 独 title "Germany
(abbreviation)" from Jisho, and compared all 15 stroke files with KanjiVG.

Later rounds: the Claude confirmation returned CONFIRMED with findings none (F1
and O1 RESOLVED, O2(a) RESOLVED, the declines of F2, O2(b), O2(c), O3 and O4
accepted, all four facets CLEAN). It also checked the 評 line that answered
GPT's OB, which now says "判 supplies バン, an on reading of 判 besides ハン"
instead of "判 supplies ハン", and wrote "This fixes an error I missed in round
1" (`reports/confirm-claude.md:77`). The GPT confirmation
resolved #1, #2 and OB, accepted the decline of OA (and withdrew its estimate of
"roughly 200 English words" for the 義 bullet), found no new defect and
returned UNVERIFIED with findings none, because L1 stayed PARTIALLY RESOLVED.
Its text: "The supplied meaning-builder source settles #1's custom-pool
filtering consequence for every candidate passed to that implementation,
independently of how `all` is constructed. What remains unverified is actual
caller/pool construction, Android execution and random draws, and the
installed build's compatibility." It added that the contract does not permit
CONFIRMED while L1 remains partially resolved. Its verdicts: correctness CLEAN
(the six revised cards examined; the nine unchanged cards keep their initial
CLEAN), scoped coverage CLEAN, comprehensibility CLEAN, and consistency and quiz
safety UNVERIFIED for the runtime- and pool-dependent claims under L1.

Unlike batch 110, both initial reviewers received identical evidence: the same
initial packet and the same supplement (`supplement/`: the two reading-quiz
outputs, `reading-options.txt` and `reading-exposure.txt`, and text extracts of
14 pages of the official Joyo table). The complete meaning-quiz simulation for
all 15 cards is in the packet's `mechanical-checks.md` (3,523 characters, under
the 4,000-character limit that cut it off in batch 110), and it is identical,
blank lines aside, to `confirm-packet/common/checks/quiz-safety.txt` at the fix:
no option changed. The two prompts differ only in the ordinal on the first line
(the first or second of two reviewers), the paragraph that names the facets to
examine deepest and the path of the report. Both also list seven neutral points
for the reviewer to judge independently: (a) the 鏡 title "mirror; lens"; (b)
the three 義 distractors 議 疑 技, all read ギ; (c) the 敷 readings し.く and
-し.き; (d) 率 シュツ and 養 リョウ; (e) the 節 readings -ぶし, のっと and ノット;
(f) the latent-collision lines of the reading-exposure scan; (g) the 独 title
"Germany (abbreviation)". Claude's F1 and F2 coincide with leads (c) and (a);
GPT's findings do not. The leads came from the author's own scan, not from
either reviewer.

Each reviewer worked from a frozen packet of one snapshot: the initial packet
(built at 11:20:59 from `3b30803e`, 6,444 files) for both initial runs and a
confirmation packet for each family (built at 16:12:54 and 16:13:03 from
`bf9ee962`; 44 and 43 files, each with a manifest). In the initial round
neither reviewer saw the other's report or the author's rationale. In the
confirmation round each reviewer saw the author's statement on its own findings
(claims to verify, not evidence), a neutral change list, the exact patch, the
new evidence and the automatic checks, and no other reviewer's report. The
Claude confirmation packet also carries an extract of the Kanjipedia page for 鏡
(`confirm-packet/claude/evidence/kanjipedia-鏡.txt`) on which the author's
decline of F2 rests; GPT's initial report cites the same page. Each later run
continued the session of its family's initial review (Claude `d0c86dea`, GPT
`b16a90b3`); neither confirmation audit records a re-read of the reviewer's own
previous report.

The two confirmations ran serially, in the shared content-reviewer slot that
this work shares with another workstream, under an explicit handoff and a
reservation of two rounds; the slot was returned after the second round. Both
reviewer sessions are archived.

Serial tool work was required of every reviewer, and the audits record how it
went. Two of the four runs were strictly serial, with at most one call in
flight: both GPT runs. Each Claude run issued one overlapping start, two `view`
calls at 11:26:21.495 in the initial run (about 20 seconds in) and at
16:15:39.626 in the confirmation (about 21 seconds in), each with up to two
calls in flight. A 340-character reminder from the coordinator followed each
(at 11:27:03.663 and 16:16:18.710); it asks for strictly one call per response
and for the overlap to be recorded under Limits, and says nothing about the
batch. Both Claude reports record the overlap. The audit flag "recursive shell
commands over packet directories: 1" on the initial GPT run is a false
positive: the one match is the power operator in a Bézier script (`(1-t)**3`),
which lists no directory; the `corpusScans` entry of that audit (the packet
directory, 6,445 files, `recursive: true`) comes from the same command. The
audits classify none of the shell commands as writing a file, and each run
wrote only its own report. The runs issued 31, 48, 14 and 5 shell commands, in
table order. This record therefore claims strictly serial work for two runs and
one overlapping start for each of the other two.

The Claude confirmation also used one tool that the other runs did not,
`send_session_message`. After writing its report it sent one line to the
coordinator's session: "Confirmation report written to
reports-111\confirm-claude.md — verdict CONFIRMED, no new findings." The message
carries nothing beyond the verdict of the report, and the audit lists the tool
under "other tools used".

In three audits (`initial-gpt` and both confirmations) `outsidePaths` is empty.
In the initial Claude audit it holds one entry, the bare `review-packets`
directory, which four of that run's PowerShell snippets used as the base path of
allowed packet paths (`$p='…\review-packets'`, then
`$p\batch-111-3b30803e\evidence\public-source\…`). No other path outside the
allowed ones is recorded.

The prompts allowed public web sources. The audits record 0, 5, 1 and 9
web-tool calls, in table order (Weblio, Jisho and Kanjipedia pages, one web
search for the 鏡 title and the KANJIDIC2 DTD). The audits count only the web
tools, so the author also scanned the session event logs for network calls made
inside shell scripts: 14 shell commands of the initial GPT run (eight to Weblio,
one to kanjiapi.dev, which answered HTTP 403, three to jisho.org and two to
raw.githubusercontent.com for KanjiVG); the other three runs made none. Those
commands carried much of that reviewer's independent checking: the Daijisen
entries of all 15 kanji, 48 Jisho word queries and the 15 KanjiVG files compared
with the stroke data.

`reports/` holds the four verbatim reports, stored with LF line ends; their
SHA-256 values equal the `reportSha256` of the audits. `prompts/` holds the
exact prompts as the reviewers received them and the two steering reminders
(`steering-initial-claude.txt`, `steering-confirm-claude.txt`). Each audit
records the user messages of its run: the prompt and, for the two Claude runs,
the reminder; the two GPT runs received only the prompt. The stored initial
prompt files end with one line feed: the `userMessages` hash of an initial audit
is the SHA-256 of the prompt without it, and `promptSha256` in `provenance.json`
is that of the stored file. The confirmation prompts have no trailing newline,
so both hashes agree. `scope-audits/` holds the read-scope and model-identity
audits. An audit's `reviewAccepted: false` is by design: it records read scope
and model identity only, not acceptance.

`packet/` holds the initial packet's instructions and mechanical checks, a
gzipped manifest (the SHA-256 of each of its 186 named files and one aggregate
hash of the 6,258-file repository context export), the 62 diffs (the 60 word
diffs and those of 価 and 暖) and the evidence (JMdict digest and families,
KANJIDIC2 records, pinned source metadata and the 15 Digital Daijisen extracts
from Weblio). The snapshot cards, strokes and words are the Git blobs at
`3b30803e` and are not copied. `confirm-packet/` holds the 25 files common to
both confirmations (change list, exact patch, cited JMdict entries, a KANJIDIC2
extract for 判, six Joyo table extracts, `QuizBuilder.kt`, `KanjiReadings.kt`,
`Words.kt` and the ten automatic check outputs), each family's instructions,
author's statement, evidence note and file manifest (the Claude packet adds the
Kanjipedia extract for 鏡) and the packet provenance. The 15 snapshot cards of a
confirmation packet are the Git blobs at `bf9ee962`, listed in its manifest and
not copied. `supplement/` (18 files) holds what both initial runs received in
addition to the packet.

Three SHA-256 values in `provenance.json` refer to packet files that are not
stored here and cannot be checked from this folder: `packet.manifestSha256`
(the hash of the full manifest as JSON with sorted keys; the stored manifest
folds the 6,258 context files into one aggregate and so hashes differently) and
the `packet.titlesSha256` entries for `kanji-titles.tsv` and `word-titles.tsv`.

## Reconciliation

Item labels: Claude's F1, F2 and O1-O4 (O2 has parts (a)-(c)) are the labels in
its own report. Claude's `L1` is a question the author added in
`confirm-packet/claude/RESPONSE.md` (which side of a kun reading the leading
hyphen marks, from Claude's Assumption (a)). GPT's initial report numbers its
findings 1 and 2; `#1`, `#2`, `OA`, `OB`, `L1` and `L2` are the labels the
author gave those findings, GPT's two optional points and its stated limits in
`confirm-packet/gpt/RESPONSE.md` (`L1`: the supplied Python ports and no
executed Android client; `L2`: its other limits). Line references are to the
cards at `bf9ee962`.

| Item | Disposition |
|---|---|
| Claude F1 (low), 敷: 敷地 was filed under the suffix reading -し.き (`敷.md:35` at the freeze), and the card defined the leading dash as "a bound form, one that appears inside compounds" (`:37`). Claude offered two remedies: move 敷地 to the し.く row, or keep the row and rewrite the dash sentence as a suffix definition. GPT's initial report did not raise it. | Both remedies applied, except that the card does not say しき is the stem form of 敷く (no source supplied states that). 敷地 now sits in the し.く row (`敷.md:34`); the -し.き row is typed `kun suffix` (it was `kun, bound form`; precedents `氏.md:32`, `始.md:30`) and lists only 座敷 and 風呂敷 (`:35`); the dash sentence reads "The leading dash in -し.き marks a suffix use, one that follows another element; it is not pronounced." and adds that 敷 reads しき at the start of 敷地, 敷居 and 敷金 (`:37`). `:39` says the Daijisen lists its しき words in two groups separated by a slash, those that begin with 敷 and those that end with it (the extract prints the slash; the two descriptions are the author's, not dictionary labels), and reports that the Joyo table has no separate しき row and files 屋敷 under しく (`confirm-packet/common/evidence/joyo/p134.txt:39-41`). The same dash wording was corrected in 節 (`節.md:36`, `:39`). `docs/content-format.md:89` says only that kunyomi uses "-" for affixes, and the repository is not uniform (`稲.md:33` "kun, bound form", `編.md:45` "a bound use", `御.md:31` "kun prefix"; none is in this batch), but none of the phrases "bound form", "inside compounds", "bound use" or "kun prefix" remains in the 15 batch cards (author's script check). Claude RESOLVED. The GPT confirmation found `敷.md:34-39` supported (the Daijisen groups, the Joyo しく row including 屋敷, and a suffix explanation that does not attribute the hyphen's side to the KANJIDIC2 DTD). |
| Claude F2 (low), 鏡: "lens" in the title `mirror; lens` (`鏡.md:3`) is not a meaning of 鏡 in KANJIDIC2, and the Daijisen's second sense is an instrument that uses lenses, not a lens. Claude suggested "mirror; optical instrument" and said the owner could downgrade the point to Optional (confidence medium). GPT did not raise it. | DECLINED; the title is unchanged. Kanjipedia's second sense is ②「めがね。レンズ。」 (`confirm-packet/claude/evidence/kanjipedia-鏡.txt:20`); JMdict 鏡面 1238590 is "mirror surface; lens surface" (`鏡.md:56`); the Daijisen's second キョウ sense is an instrument that uses lenses (`鏡.md:23`, `:25`). The author's script over the 1,176 cards found 器 (`vessel; instrument`) to be the only other title containing "instrument", "lens" only in 鏡's title, and no title containing "scope", "optical" or "glass", so "mirror; optical instrument" would overlap 器 and need a new exclusion. The statement concedes that KANJIDIC2 lists no "lens" for 鏡 and that JMdict glosses 顕微鏡 1260660 and 望遠鏡 1519650 with "-scope" words. Claude DECLINE ACCEPTED after fetching the live Kanjipedia entry, noting that its own alternative "instrument" would have collided with 器. |
| Claude O1 (optional), 房 `:25`: the Daijisen gives 安房国 and illustrates the sense with 房州 and 房総, not with 安房 あわ; suggested "the old province of Awa (安房), as in 房総 ぼうそう". | CHANGED differently: `房.md:25` now says "and the old province of Awa, as in 房州 and 房総. JMdict has the province name as 安房 あわ", and the next sentence begins "For ふさ the Daijisen gives". Claude's ぼうそう was not added, because neither 房州 nor 房総 is in `jmdict-families.xml` (the GPT confirmation streamed the file and found neither either). Claude RESOLVED; the GPT confirmation found that the card no longer presents あわ as a ボウ example. |
| Claude O2(a) (optional), 鏡 `:25`, `:39`: the Daijisen's second キョウ sense lists 眼鏡 as がんきょう (a separate JMdict entry, 2862467), while `:39` says 眼鏡 めがね gives 鏡 no reading; suggested "(here read がんきょう)". | CHANGED: `鏡.md:25` gives `眼鏡 がんきょう`, "glasses; eyeglasses; spectacles," (the glosses of JMdict 2862467, added to the Metadata list at `:56`), and `:39` says the Daijisen lists 眼鏡 twice, once among its キョウ words, where it matches the separate JMdict entry 眼鏡 がんきょう, and once among its hard-to-read words, as めがね. Claude RESOLVED; the GPT confirmation found both supported by JMdict 2862467 and the public entry. |
| Claude O2(b) and O2(c) (optional), 鏡: 眼鏡 めがね is often written in kana; めいきょう is the usual reading of 明鏡, but only めいけい appears in the ケイ row. | DECLINED. (b): no statement on the card depends on how 眼鏡 is spelled (`鏡.md:39`). (c): the card does not say which reading of 明鏡 is the usual one; `:25` gives 明鏡 めいきょう as a Daijisen キョウ word, and the ケイ row (`:34`, marked "no word article yet") rests on JMdict, which lists めいけい third, after めいきょう and みょうきょう; `:37` explains it. Claude DECLINE ACCEPTED for both. |
| Claude O3 (optional), 義 reading quiz: all three curated distractors 議 疑 技 share ギ, so the ギ prompt falls back to tiered options; if wanted, swap one for a confusable kanji that is not ギ. Claude O4: the title of `words/節約.md` is a paraphrase (context, not scope). | DECLINED. O3: all three curated options are skipped as excluded, and the 義 section of the reading audit (`confirm-packet/common/checks/reading-options.txt:162-175`) shows 143 wrong options over 400 seeds (`:174`), no seed with fewer than three wrong options and no problem; the readings and distractors of 義 are unchanged. O4: `words/節約.md` is not among the files changed between the freeze and the fix (`confirm-packet/common/diffs/changed-files.txt`); in this batch it gained only a link on 節 (`:24`), and its title is outside the batch. Claude DECLINE ACCEPTED for both. |
| Claude L1 (a question the author added), 敷 and 節: which side of a kun reading the leading hyphen marks (Claude's Assumption (a)). | RESOLVED, as a convention. `docs/content-format.md:89` and the `ja_kun` entry of the KANJIDIC2 DTD say only that prefix and suffix readings are marked with a hyphen, without naming a side. The repository uses a leading hyphen for a suffix (`混.md:49`, `氏.md:32`, `始.md:30`, and now `敷.md:35` and `節.md:36`) and a trailing hyphen for a prefix (`御.md:31`, お-). Claude RESOLVED: the cards now say a leading dash marks suffix use, matching the KANJIDIC2 and EDICT convention and repository practice; it noted that the DTD text does not name the side, so the answer rests on convention, which it accepted. |
| GPT #1 (minor), 節 with 句 and 旬: neither side excluded the pair, although 句's title "phrase; verse" overlaps a sense of 節 (KANJIDIC2 "verse", "clause", "stanza"; JMdict 1386140) and 節's "season" overlaps 旬 (KANJIDIC2 "season (for specific products)"). All three cards had complete safe curated choices, so no default-pool collision was claimed; the exposure was the documented custom or larger-quiz fallback. Remedy: declare 節/句 and 節/旬 once each and infer no 句/旬 pair. | CHANGED, on 節 only: `節.md:14` is now `[季, 春, 期, 接, 制, 倹, 限, 際, 祭, 部, 句, 旬]`, while `句.md` and `旬.md` are unchanged, because `excluded(a, b)` (`confirm-packet/common/evidence/QuizBuilder.kt:26`) is true when either card lists the other, so one declaration guards both directions. `節.md:25` now ends with the second JMdict sense of the noun 節 せつ ("section (of a literary work or piece of music); passage; paragraph; verse; stanza", no word article here), and `:56` names 句 ("phrase; verse") and 旬 ("ten days; peak season") in the overlap bullet and adds "verse". The author's script over the 1,176 cards finds 節 the only card that lists 句 or 旬 in `quiz_exclusions`, no card lists either in `distractors`, and 句 and 旬 list neither each other nor 節. The curated distractors of 節 stay `[雪, 殺, 笑]`, and the wrong options shown for 節, 句 and 旬 are unchanged (`confirm-packet/common/checks/quiz-safety.txt:22`, `:3`, `:12`). GPT RESOLVED; Claude's confirmation also judged both pairs real direct overlaps. |
| GPT #2 (minor), 義: 税 was grouped with 役 and 務 as overlapping the "duty" of 義 and excluded (`義.md:14`, `:52`), but 税's title is "tax; fiscal duty", a levy and not an obligation (`税.md:3`, `:20`): a false learner-facing comparison and an unnecessary exclusion. Remedy: remove 税, or keep it as an explicit comparison. | CHANGED by removal: `義.md:14` is now `[役, 務, 意, 理, 正, 替, 敬]` (税 was the eighth), and the `:52` bullet now begins `[役](役.md), "role; duty," and [務](務.md), "duties," overlap the sense "duty" that 義 and 義務 carry`; no line of `義.md` mentions 税. `税.md` is unchanged, and neither card lists the other in `quiz_exclusions` or `distractors` (義 `[議, 疑, 技]`, 税 `[祝, 況, 説]`). GPT RESOLVED. Claude's confirmation judged the change correct in both directions: 税 keeps three curated distractors with no fallback, so the title of 義 cannot appear among 税's options. |
| GPT OA (optional): compress the dictionary and exclusion explanations of 義 (`義.md:52`, "roughly 200 English words"). | DECLINED. The bullet is 101 whitespace-separated tokens (105 at the freeze) and the longest prose paragraph of the card is 81 words (`義.md:25`), before and after. GPT reproduced the counts, DECLINE ACCEPTED, and withdrew its estimate. |
| GPT OB (optional), 評: explain the voicing ハン to バン in 評判 ひょうばん (`評.md:35` said "in 評判, 判 supplies ハン"). | CHANGED differently: `評.md:35` now says "in 評判, 判 supplies バン, an on reading of 判 besides ハン" (JMdict 評判 ひょうばん 1490070; `判.md:9` and the バン row at `:34`). The card does not call it a sound change, because バン is itself a listed on reading of 判; the 論評 sentence ("In 論評 ろんぴょう, the sound changes to ぴょう after the ン of 論.") is unchanged. This also fixes an error Claude had missed in round 1. Both reviewers RESOLVED. |
| GPT L1 (limits): the quiz audits are supplied Python ports, not an executed Android client; the custom-pool consequence of #1 follows the documented fallback contract (`docs/content-format.md:102-107`). GPT L2: its other limits. | L1 PARTIALLY RESOLVED in the GPT confirmation, which is why that confirmation is UNVERIFIED. The author accepts it as a disclosed, non-blocking, bounded evidence limit (no defect, no extra round). `QuizBuilder.kt` is from the Android checkout at app commit `10d98d0`: `excluded` is line 26 and `tryAdd` lines 28-32 (line 30 refuses a candidate that is excluded against the target or against any option already chosen), with the curated distractors at line 34 and the fallback at line 36. The file does not show how a custom pool is built and passed in as `all`, so no claim is made about which cards a pool holds. GPT lists what stays open: actual caller and pool construction, Android execution and random draws, and the installed build's compatibility. `quiz_exclusions` are honoured only by app builds from `2edbf36` onward ("Honor explicit kanji meaning pair exclusions"; the `10d98d0` checkout contains it), so nothing is claimed about any installed build. L2 needed no disposition. |
| Claude confirmation, optional notes: 敷 `:34` and `:37` could add a clause such as "しき is the noun form of 敷く"; 房 `:25` could give kana for 房州 and 房総; the 鏡 prompt キョウ has only three distinct wrong options over 400 seeds (ぎん, どん, きゅう; `confirm-packet/common/checks/reading-options.txt:221-227`). | Not adopted, and none is a defect: Claude says the current 敷 wording is correct without the clause, the 鏡 prompt is safe and unchanged from round 1, and the other two are polish. The clause would assert a derivation that no supplied source states. Any further card change would need another confirmation round and a fresh reviewer-slot reservation, so the confirmed text stays as confirmed. |

Every changed line between the freeze and the fix belongs to a row above: 房
`:25` (O1); 敷 `:34`, `:35`, `:37`, `:39` and 節 `:36`, `:39` (F1); 節 `:14`,
`:25`, `:56` (GPT #1); 義 `:14`, `:52` (GPT #2); 評 `:35` (GPT OB); 鏡 `:25`,
`:39`, `:56` (O2(a)), plus the manifest lines that follow from those edits.

Two model families reviewed the batch, each on all four facets. That meets the
issue-60 requirement of at least two families per batch on one fixed snapshot
with independent blind initial findings, with fixes confirmed by the original
reviewers, except that the GPT confirmation is UNVERIFIED (its limit L1, see
above), so there is no joint CONFIRMED. The repository rule of three facet-split
reviewers from three model families (`.github/copilot-instructions.md`,
"Independent review and reconciliation") applies to a new word card or learner
article, a new app-facing file under `words/` or `articles/`. Batch 111 adds no
such file, and its 60 word edits only wrap kanji in links (`words/句読点.md`
also drops a stale "There is no 句 card currently." sentence), so review stays
proportional. That reading is the author's and is repeated under Limits.

## Byte identity

`provenance.json` records the snapshots, the packets and the four runs (session,
actual models, window, API requests, tool calls and the SHA-256 of each report,
prompt and audit). Of the 92 teaching files at the freeze (17 cards, the 15 new
ones and the existing 価 and 暖; 15 stroke files; 60 word articles), 86 are the
same Git blobs at `bf9ee962`: all 15 stroke files, all 60 word articles, 価, 暖
and nine of the 15 new cards (修 句 授 旬 標 独 率 製 養). The other six, the
cards 房 敷 節 義 評 鏡, changed. `git diff --shortstat 3b30803e bf9ee962` shows
7 files (those six and `manifest.json`), 23 insertions and 23 deletions: 16 card
lines (房 1, 敷 4, 節 5, 義 2, 評 1, 鏡 3) and 7 manifest lines. Against the base
`f40a1391` the whole batch is 93 files, 1,020 insertions and 125 deletions (30
added, the 15 cards and their 15 stroke files; 63 modified, the 60 word
articles, 価, 暖 and `manifest.json`), with no new `words/` or `articles/` file.
The manifest has 8,541 entries at the base, 8,571 at the freeze and 8,571 at the
fix, with content versions `18d0f3df4071aa30`, `3f255571cd82aa08` and
`0c3d8f4a2c6bcb19`.

The front matter changed in two lines of two cards: `quiz_exclusions` of 節
(`節.md:14`, with 句 and 旬 added) and of 義 (`義.md:14`, with 税 removed). The
titles, tags, KANJIDIC2 readings and curated distractors of all 15 cards are
unchanged.

The snapshot copies in the initial packet have Windows (CRLF) line ends while
Git stores LF; for all 92 snapshot files, converting the blob at `3b30803e` to
CRLF reproduces the SHA-256 recorded in the packet manifest. Both confirmation
packets list the same 15 card blob IDs; all 15 equal the Git blobs at `bf9ee962`
(the same conversion reproduces their packet SHA-256 values) and exactly six
differ from the freeze. The six, as the blob ID at `3b30803e` and at `bf9ee962`:

- 房: `320f4ab4e2e1fc4e11a3de10d45b54731d11f5f8` to
  `eec3901b19219c1366a0d82f6b45fcfdc41ddc59`
- 敷: `7460e4c99538b06e728c67a57ab4519c511af582` to
  `c72b37c190c29d8bae29468dfebe8a9f33ef070b`
- 節: `46655a8a5d23b4f9706a7e378ca7e93e7368a9f2` to
  `459078871b9d229a9a381b6674ee168ac2a46ccd`
- 義: `399077e5860e2c35832f88b38301192380273d65` to
  `a07c4caf3001b620ce81c51584144d1bc18870ea`
- 評: `ae07753e659129a5ace266f3dc4b58ca3dbd0285` to
  `be57bc517fa08f4412f21435624888004ef09d17`
- 鏡: `b7b8ca373cb86b436c42526fe47db09159595f97` to
  `cb9c1c933d3909594367ac807553c6e9ec9d380d`

`bf9ee962` was made by amending earlier local fix commits that no reviewer was
shown and that were never published, so only the final commit is named here; no
run of this record falls between 12:09:46 and 16:15:18 UTC on 11-12. Both
confirmation packets were built from `bf9ee962` (at 16:12:54 and 16:13:03 UTC).
The confirmation-packet builder, which is not part of this repository, was
changed after batch 110 so that its evidence note mentions KanjiVG records only
when a packet carries them; neither confirmation packet does.

## Integrated-tree checks (mechanical, not reviewer credit)

At `bf9ee962`: lint 0 errors and 13 warnings (17 kanji files and 69 word
articles checked; ten word articles whose Dictionary line cites no JMdict entry
id, 女房 標本 標準 標識 独り言 能率 製作 評論 調節 and 風呂敷, and
`words/授業.md`, `words/眼鏡.md` and `words/鏡.md`, which have no Dictionary
line; none concerns a new card and no changed line in `words/` is a Dictionary
line); 431 unit tests pass; validation 0 errors; budget 8,593 entries,
45,306,157 retained bytes, 45,577,467 inflated, 30,635,747 local ZIP bytes;
vocabulary 2122/2431; manifest rebuild shows no diff. The option simulation
(`confirm-packet/common/checks/quiz-safety.txt`) reports 0 errors and 0 warnings
(`:48`) and shows three wrong titles in the meaning quiz for each of the 15
cards; none of them is among the 11 existing cards that fall back to
tag-similar options (`:36`, the cards at `:37-47`). It matches the simulation
printed in the initial packet's `mechanical-checks.md` at the freeze, blank
lines aside, so no option changed. The link check
(`confirm-packet/common/checks/link-targets.tsv`) finds no unresolved link: 23
links on the lines changed from the freeze to the fix (`:25`; the four links of
the 敷 table rows carry no quoted gloss, so the last column reads n/a for them).

The reading-option audit (`confirm-packet/common/checks/reading-options.txt`)
ends with "0 problem(s)" (`:238`), and the reading-exposure scan
(`confirm-packet/common/checks/reading-exposure.txt:257`) reports for the 15
cards 0 production hits, 0 padded-session hits and 6 latent collisions (an
attested reading that another card offers but that none of the N1, All and
Starter-session pools can draw): 房 お (和 悪 汚; `:42`) and わ (和 話; `:45`),
節 セツ よ (与 予 余 預; `:159`) and ふし よ (世 代 四 夜; `:169`), 養 や
(冶 夜 野; `:227`) and 鏡 あき (秋 空; `:251`). Both outputs are identical,
blank lines aside, to those the initial reviewers received in `supplement/`,
made at the freeze. The `supplement/` copies keep their blank lines, so their
line numbers are larger (`reading-options.txt:254`, `reading-exposure.txt:273`);
every line number in this record is that of the confirmation packet unless the
`supplement/` path is named.

The Android JVM tests `RealContentTest`, `RareHanTest` and `KanjiReadingsTest`
were NOT run for this batch: no JVM slot was available to this workstream, so no
test result or count is claimed. No Kotlin cross-check was run either; the
option and reading audits are Python ports of the app code. There is no merge in
the tree: `origin/main` was still `f40a1391` when this record was written.

## Limits

- The review judged text, printed simulations of the answer-option builder, two
  reading-quiz audits and source-level reads of the app's quiz code
  (`QuizBuilder.kt`, `KanjiReadings.kt` and `Words.kt`, from the Android
  checkout at app commit `10d98d0`), not a running app. No APK, emulator or UI
  run is involved. The audits are the author's Python ports of that code; they
  draw from the full 1,176-card pool and use a different random generator from
  the app's, so their seed counts describe the audit, not what a phone shows,
  and the packets do not show how a caller builds a custom pool.
- Reviewers used pinned dictionary snapshots (JMdict, KANJIDIC2, Digital
  Daijisen extracts, KanjiVG at `70a0b7ae`) and public pages (Weblio, Jisho and
  Kanjipedia, plus one web search for the 鏡 title and the KANJIDIC2 DTD). The
  live dictionaries may differ slightly, and kanjiapi.dev answered the initial
  GPT run with HTTP 403.
- Joyo table: no reviewer rendered the official PDF. The initial runs received
  text extracts of 14 pages (`supplement/`) and the confirmations six
  (`confirm-packet/common/evidence/joyo/`); the GPT confirmation compared the
  claims with those extracts, not with PDF pages, and the Claude confirmation
  did not re-open them.
- GPT L1 (see Reconciliation): the GPT confirmation is UNVERIFIED, not
  CONFIRMED, because it left L1 partially resolved. The supplied builders show
  the exclusion guard (`QuizBuilder.kt:26`, `:28-32`) but not how a caller
  builds custom or Starter-session pools, Android execution and random draws, or
  the compatibility of an installed build, so GPT's consistency and quiz-safety
  verdict is UNVERIFIED for the runtime- and pool-dependent claims. Its
  correctness, scoped coverage and comprehensibility verdicts are CLEAN and it
  reports no finding. The author accepts L1 as a disclosed, non-blocking,
  bounded evidence limit and ran no extra round, as batch 110 accepted a
  partially resolved GPT limit (L3). A follow-up with a wider set of Android
  sources, like the one batch 110 had, could narrow it; it would need a fresh
  reviewer-slot reservation.
- The confirmations covered the changed passages, not an exhaustive re-review.
  Neither re-read the nine unchanged cards (修 句 授 旬 標 独 率 製 養); both
  kept their initial verdicts for them. The GPT confirmation did not reconstruct
  the pools, enumerate abbreviated candidate tails or reproduce the author's
  all-card absence scan. The statements in the Reconciliation that rest on the
  author's own scripts over the 1,176 cards (the title search for F2, the
  exclusion and distractor search for GPT #1, the phrase check for F1) were
  reproduced by a reviewer only where the table says so.
- Strokes: the GPT initial run compared all 15 stroke files with the KanjiVG
  files at `70a0b7ae` (largest sampled discrepancy about 0.071 viewBox units in
  the 109-unit viewBox); the Claude initial run checked stroke counts. The
  reviews did not render the stroke animations, no native-speaker panel assessed
  sentence naturalness and no one tried the cards on a phone. No end-to-end
  reading-runtime or older-client certification is claimed.
- Latent collisions: the scan reports six (房 お and わ, 節 よ twice, 養 や, 鏡
  あき), and its "zero production hits" is conditional on the pools it assumes
  (GPT: "conditional on the supplied pool assumptions"). Neither reviewer's
  report lists them as a finding.
- Phone APK: as in batch 110, the last phone APK delivered to the owner was
  built from app commit `5c000bd`; its installation was not verified. That build
  predates app commit `2edbf36` ("Honor explicit kanji meaning pair
  exclusions"; in the Android history `5c000bd` is an ancestor of `2edbf36`,
  which is an ancestor of `10d98d0`), so it ignores kanji `quiz_exclusions`. The
  exclusions of this batch, including the 節 and 義 edits made in the fix,
  therefore protect only builds from `2edbf36` onward. This workstream built no
  APK for this batch.
- Two families, not three: the three-family rule covers new `words/` and
  `articles/` files, and this batch adds none (its 60 word edits only wrap
  kanji in links, apart from the stale sentence dropped from
  `words/句読点.md`). That reading is the author's. With the GPT confirmation
  UNVERIFIED there is no joint CONFIRMED; a third-family read can be added if
  the owner wants one.
- Seriality: two of the four runs (both GPT runs) were strictly serial; each
  Claude run had one overlapping start (see Reviews).
- This record was written before the push and claims no CI, archive, native,
  rendered, physical-phone, older-client, handwriting or Android JVM credit. The
  issue-60 batch cycle does not require a native run per batch; the plan is one
  native smoke at a milestone or the final acceptance.
- The multi-megabyte session event archives of the reviewers remain local and
  are not committed.
