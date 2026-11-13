# Independent B112 review packet

Snapshot: d6ad96ebf7d0352d54184ed44a382f70e4497f7b
Base: 0320ba4a199432374096360e984b7dc5754dd6bc

Review the fifteen new kanji cards, their generated stroke references, the
45 backlink additions across 44 existing word articles, and three narrow
existing-kanji remark changes. There are no new word/article files.
The exact file list is in packet.json. The two independent reviewers receive
the same snapshot, rubric and source access and work serially.

## Boundaries

Work read-only and blind. Do not edit/stage/commit/push, start other agents,
start background processes, or run JVM/Gradle/emulator work. Write only the
report path specified in your assignment, outside this packet.
Use one tool call/command at a time; large reads need bounded ranges.
Do not open other packets, reports, live checkouts, session histories,
batch progress records, author design notes or author-review rationale.
Public dictionary/source lookups are allowed; inspect actual relevant entries.

snapshot\ contains the 77 changed teaching/geometry files from the exact Git
commit. diffs\existing.diff contains only the 47 existing-file changes.
repo\kanji and repo\words are complete same-commit context exports, not
additional editing/review scope. They permit actual comparison-article,
backlink, title, source-word and reading-list inspection. Other runtime
assets are not exported. The manifest is supplied for scope/hash checks.
The repo README's publication counts still describe the previously published
checkpoint; packet.json gives this draft tree's counts. Publication closure
documentation has not been written yet.

## Review contract

Read rubric\copilot-instructions.md and
rubric\content-structure.instructions.md, plus repo\docs\content-format.md's
kanji/quiz contracts. Cover correctness, scoped coverage, consistency/quiz
safety and comprehensibility for the complete shared scope. Do not split
the fifteen cards into disjoint reviewer assignments.

Inspect complete applicable dictionary entries and actual reused/comparison
articles, including spelling/reading restrictions and sense-local flags.
evidence\jmdict-families.xml preserves all elements of 75 applicable families;
dictionary-index.json maps queries to entries. Source readings, counts and
radicals are in source-metadata.json and the full KANJIDIC2 records.
evidence\kanjivg has the pinned SVGs. The official Joyo PDF and extracted
rows are provided. Provenance lists hashes, attribution and public
character-entry URLs, without author conclusions. Consult independent
public sources as needed; a filename, digest or successful fetch alone
does not verify a linguistic claim.

Retain raw source readings separately from quiz selections; selected
readings need their own linked and dictionary-supported examples.
Judge the actual displayed meaning labels and ordinary secondary senses,
not title-string inequality. Exclusions are direct pairs, not transitive
cliques. No invented phonetic/etymological claims or constituent readings
for irregular whole words. Keep register and spelling qualifications
attached to the relevant reading/sense. Do not demand exhaustive history
or unrelated vocabulary.

## Mechanical-evidence limits

checks\ contains host outputs, not linguistic verdicts. The reading audit
is a Python port with full N1/All pools and Starter plus one borrowed target.
Its legacy prose claiming these are all actual app pools, or that custom
pools are not built by an app, is NOT established by the run. Custom and
caller-built pools, multiple borrowed Starter cards, actual Kotlin draws,
native execution and installed-client compatibility are unverified.
The reported 11 latent entries include eight nanori-only entries outside
the lexical teaching scope and three other dictionary/character readings.
Do not infer a universal safety guarantee from zero modeled hits.
JVM/emulator work is held. The last delivered 5c000bd APK predates kanji
quiz_exclusions; neither this packet nor host checks establish phone acceptance.
The manifest contains 8,601 runtime files; 1,191 kanji and 5,082 word articles.

## Report

Snapshot: <full candidate SHA; actual model if verifiable>
Scope: <files inspected; clearly disclose any unread or partial scope>
Verdicts: <correctness, scoped coverage, consistency/quiz safety,
comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, per card where different>
Findings: <severity; facet; file:lines; claim/impact; remedy; precise source;
confidence>
Optional: <nonblocking expansion or polish, or none>
Limits: <unverified claims and evidence/execution limitations, or none>

CLEAN means no actionable defect established within the inspected scope,
not exhaustive correctness. Do not label consequential unresolved claims
CLEAN. No finding quota. Separate established defects from hypotheses and
optional polish. If file output truncates, finish the necessary range
before claiming a complete read. Preserve a clear record of the actual scope.
