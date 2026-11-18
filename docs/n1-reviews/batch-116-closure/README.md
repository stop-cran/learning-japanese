# B116 textual review closure

**Reviewed candidate:** `34687354b531a32fea9c10b745e80ac963ac1d4b`.
**Refreshed published base:** `8f35f34ccb10f166fbf6700c6c95d67f953026e3`.
**Publication:** pending at the time of this closure; a later publication receipt
must establish the remote commit, CI and exact served ZIP.

The three cards are 憲, 監 and 督, frozen source rows 394, 738 and 748.
The runtime delta adds three kanji cards and three generated stroke files.
Three reciprocal word-link wrappers are added across the existing 憲法 and 監督
articles; their metadata and all other text are preserved. There are no new
word articles and no other baseline runtime changes.

## Final confirmations

| Scope | Actual execution model | Final report | Outcome |
| --- | --- | --- | --- |
| 憲 | `claude-opus-5-5` | [CONSTITUTION-CONFIRM-004](runs/N1-B116-CONSTITUTION-CONFIRM-004/report.md) | CONFIRMED |
| 監 | `claude-opus-5-5` | [MONITORING-CONFIRM-004](runs/N1-B116-MONITORING-CONFIRM-004/report.md) | CONFIRMED |
| 督 | `claude-opus-5-5` | [SUPERVISION-CONFIRM-004](runs/N1-B116-SUPERVISION-CONFIRM-004/report.md) | CONFIRMED |
| 憲, 監, 督 | `gpt-6.1-sol` | [GPT004-CONFIRM-005](runs/N1-B116-GPT004-CONFIRM-005/report.md) | CONFIRMED |

These four serial, same-reviewer delta confirmations were accepted only after
the unchanged execution, full-session context, structure and substantive-claim
checks. The three Claude confirmations preceded the GPT confirmation. Their
audits record respectively 11, 9, 9 and 13 complete chain segments, zero fetches,
one report write and a verified readback, with no context compactions.
Model names come from the external execution records, not self-attestation.

## Reconciliation

The complete [review lineage and file hashes](provenance.json) preserve fourteen
admissible initial/follow-up records, their original reports, source chains,
prompts, dispositions and bounded execution audits. Historical `NEEDS FIX`,
`UNVERIFIED` and `HELD_OPEN_CLAIMS` states are unchanged; they are evidence of
earlier work, not clean acceptance of those snapshots. The final confirmations
resolve their own prior findings and assess the actual changed text.

Revisions 007-009 close the latest 憲/僚 finding and add conservative direct
guards for 憲 with 権, 任, 係, 士 and 数; 監 with 士 and 員; and 督 with 員.
They retain the distinction between official status, historical ranks,
authority, membership and supervision rather than teaching interchangeable
Japanese meanings. All eight previously uncertain comparisons are mitigated,
not retrospectively relabeled proven defects. The JMdict lists now identify
the newly cited comparison words and 督's previously cited 連行 and 養成.

The monitoring report's wording that Daijisen 員 gives "only" organizational
members/workers is accepted only for its person-related sense 2. The complete
entry also contains number and circumference senses; the
[separate claim adjudication](runs/N1-B116-MONITORING-CONFIRM-004/claimAdjudication.json)
explicitly preserves those facts. No raw report was rewritten.

Initial reviewers had source-only packets, not another reviewer's report.
Each follow-up received only its own earlier report and the actual revision.
Initial snapshots and scopes differ, so this record is not a controlled model
comparison or a ranking. Void or structurally rejected reports and raw session
payloads are not published here or used as acceptance evidence.

## Integration and limits

[Final scope verification](gates/final-scope.json) checks source membership,
the six older N2 placements, metadata/readings/selections/distractors, all old
exclusions, exact word wrappers and every baseline runtime hash. The official
manifest generator reproduces all 8,686 runtime entries at content version
`95e36aeb75b69306`. [Prepublication gates](gates/prepublication-34687354/summary.json)
include 431 passing tests, zero validation errors, zero scoped lint/quiz-safety
warnings, the required link pairs and archive-budget checks.

All report limits remain verbatim in their reports. In particular, this is
bounded textual review and host-model validation, not exhaustive secondary-sense
coverage, fresh visual SVG/PDF acceptance, Kotlin/JVM/native/phone execution, or
proof for arbitrary/custom and multi-borrow pools. The installed older APK
predates `quiz_exclusions`; compatibility with it is not claimed. The reading
model retains two latent smaller-pool 監 risks, distinct from the zero hits in
the specified shipped-stack and restricted Starter scenarios.

At closure, 242 of the 1,228 frozen pending source records have local textual
closure, but only 239 are delivered. The 989 undelivered include these three;
986 are not started. Publication accounting advances only after delivery
verification. The complete N1 expansion is not finished.
