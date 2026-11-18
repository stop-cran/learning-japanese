# Independent B114 review packet

Snapshot: 8c2bdc27e5d556e639a4d0e9239ae5f2009c400f
Base: 0485c873d2ac636373c7bdf739df97ff66f9160f

Review all fifteen new kanji cards, their generated stroke references and the
fifteen link-only changes to existing declaring word articles. There is no new
word/article file. packet.json identifies the exact teaching scope. Reviewers
receive the same immutable snapshot, rubric and source access and work serially.

## Boundaries and shared contract

Work read-only and blind. Do not edit/stage/commit/push, start agents, run shell
commands or launch JVM/emulator/ADB work. Write only your assigned report outside
the packet. The run-specific instruction file gives the narrower chain-only
access rules, phase boundary, fetch cap and single-report rule. Those rules
override any wider access suggestion in this packet's copied rubric.

Inspect correctness, scoped coverage, consistency/quiz safety and comprehensibility.
Use CLEAN, NEEDS FIX or UNVERIFIED separately for those facets, with evidence,
confidence, severity, line citations and remaining limitations. No finding quota.
CLEAN means no demonstrated defect within the inspected scope, not exhaustive
correctness. Do not mark a consequential unresolved claim CLEAN.

Inspect complete applicable dictionary entries and actual comparison cards, with
restrictions, sense-local flags, ordinary secondary senses and displayed labels.
Exclusions are direct pairs, not transitive cliques. Distinct title strings or
shared topics alone do not settle ambiguity. Source readings remain separate from
selected quiz readings, each of which needs a linked, allocated dictionary example.
Mnemonics are not historical or phonetic evidence.

snapshot contains 45 changed teaching/geometry files. repo/kanji contains all 1,221
same-commit kanji cards for mechanical comparison requests; repo/words contains
only the fifteen mapped articles, not the whole 5,083-article corpus. The diff
contains the fifteen link wrappers. The full runtime manifest is supplied for
scope/hash context, not a claim that every runtime asset is exported or reviewed.
The author's progress ledger is excluded to preserve blinding.

## Source evidence

The XML preserves 65 complete matched JMdict families and all fifteen KANJIDIC2
records. The dictionary index lists queried spellings, including empty results;
an empty exact query is not evidence that an expression is impossible.
Raw metadata, neutral source provenance, public character-entry URLs, pinned
SVGs, a mechanically derived component/count index, the Joyo PDF and cached
text rows are supplied. The author inspection summaries are not supplied.
Reading an extracted Joyo row is not a fresh visual inspection of its PDF glyph.
The run-specific chain identifies which of these assets the reviewer may read.

## Mechanical-evidence limits

The checks are host/static evidence, not linguistic verdicts. The exposure
checker is a Python model using this tree's full N1/All pools and Starter plus
one borrowed target, with 100 sampled seeds per prompt/pool and exact modeled
reachability. The bounded adapter retained the reading restrictions/search-only
flags of all matching single-character families. Supplemental character readings
come from the named public character headings; the helper labels them 'card text'
without distinguishing that origin.

The log's legacy phrases 'production' and 'not a pool the app builds' are model
labels, not verified claims about all current app callers. Actual Kotlin draws,
custom/caller-built pools, arbitrary missing content, multiple borrowed cards,
native execution and installed-client compatibility are not established. Do not
infer universal safety from zero modeled hits or turn a latent example into a
demonstrated live-app failure. Judge the reported exposure within its actual scope.

No fresh visual stroke-geometry/native/device acceptance is claimed. The previously
delivered 5c000bd APK predates kanji quiz_exclusions; this packet does not establish
its compatibility. The local archive estimate is not an exact published ZIP test.
Published totals remain 210 N1 additions plus six N2 placements; these fifteen
drafts are not yet additional deliveries.
