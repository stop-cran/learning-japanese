# Delta confirmation packet: N1 kanji batch 110, snapshot 30f2bd7c (one card changed since 10d79652)

You are the same reviewer who wrote the initial report (snapshot 453af714), the confirmation report (snapshot 10d79652)
and the follow-up report (snapshot 10d79652, `followup-gpt.md`) on this batch. Your follow-up report ended with
Confirmation NEEDS FIX: you rejected the author's decline of your finding 1 (嫌 and the contracted reading や), named the
mitigation you would accept (remove only いや from 嫌's `quizKunyomi`) and made three minor findings about wording in the
author's statement. The author has applied the mitigation in commit `30f2bd7c7b57e0d244a1cb86ba51e5b86121d4f8`, a child of
`10d7965266b69ed81703ab69f20cff873a0526e9`. Since that snapshot only `kanji\嫌.md` and two lines of `manifest.json` changed
(`diffs\changed-files.txt`); the other 14 cards in `snapshot\kanji\` are byte-identical to the cards in your confirmation and
follow-up packets. This is a short, focused round about that delta only. You will not see any other reviewer's report; do
not look for one.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your
  report to the one path named in your assignment. Read-only inline scripts that write no files are allowed (for example
  to rebuild a pool from `evidence\cards-reading-metadata.tsv` or to compare bytes). Do not start other agents, sessions
  or background jobs.
- **Serial.** Make exactly ONE tool call per response, wait for its result, then decide the next call. Read large files
  in ranges. Never list a directory recursively.
- **Allowed local reads.** (1) this packet; (2) your follow-up packet
  `C:\Users\stop-\n1-kanji-workspace\review-packets\followup-110-10d79652-gpt` (it holds the pinned Android sources and the
  analysis tools, which this packet does not repeat); (3) your confirmation packet
  `C:\Users\stop-\n1-kanji-workspace\review-packets\confirm-110-10d79652-gpt`; (4) the original packet
  `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-110-453af714` (read-only); (5) your own reports
  `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\initial-gpt.md`, `confirm-gpt.md` and `followup-gpt.md`
  in the same folder. Open no other local path: no repository checkouts or clones, no `docs\n1-reviews`, no other packets
  and no other reports. Public web sources are allowed and encouraged, including the public raw URLs of the Android
  repository at the pinned commit (see `evidence\README.md`).
- **Report path.** Write your report to this one path only:
  `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\followup2-gpt.md`

## What the round is about

Your follow-up report accepted one specific change as the resolution of F1: remove only `いや` from 嫌's `quizKunyomi`,
update the practice-selection paragraph, and keep the full `kunyomi` list, the いや teaching row and its vocabulary
coverage. You noted that the remaining scheduled kun'yomi prompt is きらう because the two retained entries share a stem.
The author made exactly that change, corrected the three statements you found wrong (FU1 to FU3, defined in
`RESPONSE.md`) and re-ran his analysis on the new snapshot: the Python audits and the real Kotlin code of the Android
client at the same pinned commit as before. This round asks you to confirm four things: (1) the change is what you asked
for and nothing else; (2) the changed card text is correct, consistent and understandable; (3) the pools the shipped app
builds cannot offer や for the two prompts 嫌 still has; (4) the author's corrections of his own statements are right.

## What to read (in this order)

1. `CHANGES.md`: the exact change, line by line, with the gate results before and after.
2. `RESPONSE.md`: the author's statement: his dispositions D1 to D6 on your follow-up report and the new claims N1 to N10
   with exact anchors. These are claims to verify, **not evidence**.
3. `diffs\`: `delta.patch` (the exact patch of the card), `manifest-delta.patch`, `changed-files.txt`,
   `changed-lines.txt`, and the two diffs of the author's check outputs (`checks-vs-followup.diff`,
   `reading-options-vs-confirm.diff`). Then `snapshot\kanji\嫌.md` in full, and `snapshot-identity.txt` and
   `packet-manifest.json` (commit, tree, blob ids and hashes).
4. `evidence\README.md`: what each file of this packet is, how it was produced, and what this packet deliberately does not
   repeat.
5. `evidence\cards-reading-metadata.tsv` (every card of the snapshot; it differs from the one in your follow-up packet only
   in the row of 嫌), `evidence\jmdict-cited-entries.xml` and, in the original packet, `evidence\public-source\weblio-嫌.txt`
   (the Digital Daijisen text) and `evidence\kanjidic2-records.xml` (the KANJIDIC2 record of 嫌).
6. The pinned Android sources in your follow-up packet, `evidence\android\` there (`SOURCES.tsv` has each file's blob id,
   SHA-256 and public raw URL). The sources are unchanged; this packet does not repeat them. For the claims, at least
   `core\src\main\kotlin\io\github\stopcran\kanji\core\reading\KanjiReadings.kt` lines 47 to 59 and 79 to 115.
7. `checks\`: the author's own analysis and gate logs (claims to verify, not evidence). The Kotlin run outputs come from the
   same scratch test as in your follow-up packet (`evidence\tools\ScratchReadingExposureTest.kt.txt` there), which is not
   part of the app and cannot be run without the Android checkout. The Python tools need the whole content tree and the
   pinned dictionary inputs, which are not in the packets; read them as method descriptions.

## Tasks

1. **Dispositions.** Give a disposition for **F1** (the mitigation you named), and for **FU1**, **FU2** and **FU3** (the three
   findings of your follow-up report: did the author understand them correctly and are his corrections right?), using the
   vocabulary `RESOLVED`, `PARTIALLY RESOLVED`, `NOT RESOLVED`, `DECLINE ACCEPTED`, `DECLINE REJECTED`. The follow-up
   dispositions of L1 and L3 stand; say so only if you disagree.
2. **Delta check.** For the four facets Correctness, Scoped coverage, Consistency and quiz safety, and Comprehensibility,
   judge the changed card text (`delta.patch`, `snapshot\kanji\嫌.md`) and the other changes of this delta. Your earlier
   verdicts for everything that did not change stand unless this round changes them. Look in particular at whether any
   other line of the card, or any claim in `RESPONSE.md`, still contradicts the withdrawal of いや from practice.
3. **Claims.** For each of N1 to N10 in `RESPONSE.md` say `VERIFIED`, `NOT VERIFIED` or `WRONG`, and what you opened. At
   least reproduce by hand: (a) the list of prompts the readings screen can ask for 嫌 from `snapshot\kanji\嫌.md` lines 9
   to 14 and `KanjiReadings.kt` (N4); (b) from `evidence\cards-reading-metadata.tsv` and `KanjiReadings.kt` lines 80 to 115,
   whether any Starter practice session pool can offer や for 嫌's two prompts, or the pool or path that the author's
   argument misses (N5, N6); (c) the manifest delta: that the SHA-256 on the `+` line for `kanji/嫌.md` in
   `manifest-delta.patch` is the SHA-256 of `snapshot\kanji\嫌.md` after normalising CRLF line ends to LF (N9). If you find a
   wrong number, a path the author missed, or a statement that contradicts the sources, report it as `WRONG` or as a new
   finding.
4. **New findings.** Report only what is new and established. Do not re-raise a point you have dispositioned unless the
   author's answer is wrong. No finding quota. The delta is small: about 30 to 40 tool calls should be enough.

Verify consequential claims yourself against the sources. A search snippet is not verification. Say what you could not
verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit 30f2bd7c; reviewer model as you identify it>
Scope: <files opened and how deeply>
Dispositions: <F1, FU1, FU2, FU3, one line each: ID - DISPOSITION - short reason and evidence; L1 and L3 only if you disagree with the follow-up dispositions>
Verdicts: <Correctness; Scoped coverage; Consistency and quiz safety; Comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, one line each, judged for this delta; your earlier verdicts for everything unchanged stand unless you say otherwise>
Claims: <N1 to N10, one line each: ID - VERIFIED | NOT VERIFIED | WRONG - what you opened>
Confirmation: <CONFIRMED | NEEDS FIX | UNVERIFIED - CONFIRMED only if F1 is RESOLVED and you established no new actionable defect in this delta. This line replaces the Confirmation line of your follow-up report; every other disposition of that report stands>
Findings: <new findings only: numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence; or none>
Optional: <nonblocking polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. Separate defects from optional polish and editorial preference.
