# Follow-up packet: N1 kanji batch 110, snapshot 10d79652 (unchanged)

You are the same reviewer who wrote the initial report (snapshot 453af714) and the confirmation report (revised snapshot
10d79652) on this batch. The batch has NOT changed since your confirmation report: the snapshot is still commit
`10d7965266b69ed81703ab69f20cff873a0526e9`, and the 15 cards in `snapshot\kanji\` of this packet are byte-identical to the
cards in your confirmation packet. One item of your confirmation report is still open: your finding 1 (嫌 and the
contracted reading や), together with the limit L1 that belongs to it. This is a short, focused round about that point
only. You will not see any other reviewer's report; do not look for one.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your
  report to the one path named in your assignment. Read-only inline scripts that write no files are allowed (for example
  to rebuild a pool from `evidence\cards-reading-metadata.tsv` or to compare bytes). Do not start other agents, sessions
  or background jobs.
- **Serial.** Make exactly ONE tool call per response, wait for its result, then decide the next call. Read large files
  in ranges. Never list a directory recursively.
- **Allowed local reads.** (1) this packet; (2) your confirmation packet
  `C:\Users\stop-\n1-kanji-workspace\review-packets\confirm-110-10d79652-gpt`; (3) the original packet
  `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-110-453af714` (read-only); (4) your own reports
  `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\initial-gpt.md` and
  `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\confirm-gpt.md`. Open no other local path: no
  repository checkouts or clones, no `docs\n1-reviews`, no other packets and no other reports. Public web sources are
  allowed and encouraged, including the public raw URLs of the Android repository at the pinned commit (see
  `evidence\README.md`).
- **Report path.** Write your report to this one path only:
  `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\followup-gpt.md`

## What the round is about

Your finding 1 showed that the contracted native reading や of 嫌 (a sound-change form of いや) is attested but not
listed in the card, so a reading-quiz pool that contains a card offering や can show や as a wrong option next to the
correct いや. You asked for protection in the reading-option mechanism, smaller-pool cases in the audit, a corrected
inventory of attested readings, and for the pinned KANJIDIC2 metadata to be preserved. The author has since examined
which pools the app really builds and which production code paths can offer や, using the real Kotlin code of the
Android client at one pinned commit. The author's results and position are in `RESPONSE.md`; the sources are in
`evidence\`.

## What to read (in this order)

1. `RESPONSE.md`: the author's statement. It corrects two earlier author statements, gives the author's position on
   F1, L1 and L3 (IDs defined there) and lists the claims C1 to C13 with exact anchors. These are claims to verify,
   **not evidence**.
2. `evidence\README.md`: what each evidence file is and how it was obtained.
3. `evidence\android\`: the Android client sources, exact git blobs of ONE pinned commit of the public repository
   `stop-cran/kanji-cards-android`. `SOURCES.tsv` gives size, SHA-256, blob id and the public raw URL of each file;
   the author compared the bytes at each URL with the blobs when the packet was built. `call-sites.txt` and `routes.txt`
   are `git grep` outputs over every `*.kt` file of that commit. `compare-5c000bd-to-10d98d0d.txt` and `.patch` compare
   the reading-pool sources with an older commit (context for one disclosed limit only). Line numbers in `RESPONSE.md`
   refer to these copies.
4. `evidence\cards-reading-metadata.tsv` (every card of the snapshot: tags, readings, asked readings, distractors,
   exclusions), `evidence\jmdict-cited-entries.xml` (complete JMdict entries 1587610 and 2711110) and, in the original
   packet, `evidence\public-source\weblio-嫌.txt` (the Digital Daijisen text you cited).
5. `checks\` and `evidence\tools\`: the author's own analysis (claims to verify, not evidence). The Kotlin run outputs
   come from a scratch test (`evidence\tools\ScratchReadingExposureTest.kt.txt`) that is not part of the app and cannot be
   run without the Android checkout. The source-level cases can be reproduced by hand from
   `evidence\android\core\src\main\kotlin\io\github\stopcran\kanji\core\reading\KanjiReadings.kt` and
   `evidence\cards-reading-metadata.tsv`. The Python tools need the whole content tree and the pinned dictionary
   inputs, which are not in this packet; read them as method descriptions.
6. `snapshot\kanji\嫌.md` only as needed (the card text did not change since your confirmation).

## Tasks

1. **Dispositions.** Give a disposition for **F1** and **L1**, using the same vocabulary as before: `RESOLVED`,
   `PARTIALLY RESOLVED`, `NOT RESOLVED`, `DECLINE ACCEPTED`, `DECLINE REJECTED`. The author does NOT change any card text
   for F1: he corrects the audit and its inventory, discloses the path that remains, and proposes a change in the client.
   Judge whether that is acceptable. For **L3** (Joyo claims compared only with text extracts) give a statement: does the
   remaining limit block your confirmation, and if so what evidence would resolve it; or is it an accepted, disclosed
   limit.
2. **Claims.** For each of C1 to C13 in `RESPONSE.md` say `VERIFIED`, `NOT VERIFIED` or `WRONG`, and what you opened. At
   least reproduce by hand (a) your own source-level case, the pool `[嫌, 屋]` for the kun'yomi prompt いや, from
   `KanjiReadings.kt` and the metadata file; (b) which pool the readings screen uses and when padding happens (C1 to
   C3); (c) whether any production path can offer や for 嫌 (C6 to C8). If you find a production path or pool the
   author missed, or a wrong number, report it as `WRONG` or as a new finding.
3. **Judgement.** The one production path that remains is narrow (the kun'yomi prompt いや of 嫌 in a short Starter
   "Practice more" session in which 嫌 is borrowed). Is a documented limitation plus a proposed change in the client
   acceptable for it? If not, name the content mitigation you would accept and say why it does not conflict with your own
   remedy ("preserve pinned KANJIDIC2 metadata rather than silently presenting an extra value as part of that source
   record"); say so if you see a better alternative.
4. **New findings.** Report only what is new and established. Do not re-raise a point you have dispositioned unless the
   author's answer is wrong. No finding quota.

Verify consequential claims yourself against the sources. A search snippet is not verification. Say what you could not
verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit 10d79652; reviewer model as you identify it>
Scope: <files opened and how deeply>
Dispositions: <F1, L1 and L3, one line each: ID - DISPOSITION or statement - short reason and evidence>
Verdicts: <consistency and quiz safety: CLEAN | NEEDS FIX | UNVERIFIED, one line; the other three facets of your confirmation report stand unless this round changes them (then say so)>
Claims: <C1 to C13, one line each: ID - VERIFIED | NOT VERIFIED | WRONG - what you opened>
Confirmation: <CONFIRMED | NEEDS FIX | UNVERIFIED - CONFIRMED only if F1 and L1 are RESOLVED or DECLINE ACCEPTED and you established no new actionable defect. This line replaces the Confirmation line of your confirmation report; every other disposition of that report stands>
Findings: <new findings only: numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence; or none>
Optional: <nonblocking polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. Separate defects from optional polish and editorial preference.
