# Independent B113 review packet

Snapshot: fdec1c02f9b02f29659b56551cd0a1fd927cced1
Base: c42d80306926e99ec6436c80c0574e3a858a4286

Review the fifteen new kanji cards, their generated stroke references, the
30 backlink additions across 30 existing word articles (one of which also has
a narrow non-link text edit), and narrow edits to two existing kanji cards
(応 and 統). There are no new word/article files. The exact file list is in
packet.json. The two independent reviewers receive the same snapshot, rubric
and source access and work serially.

## Boundaries

Work read-only and blind. Do not edit/stage/commit/push, start other agents,
start background processes, or run JVM/Gradle/emulator work. Write only the
report path specified in your assignment, outside this packet.
Use one tool call/command at a time; large reads need bounded ranges.
Do not open other packets, reports, live checkouts, session histories,
batch progress records, author design notes or author-review rationale.
Public dictionary/source lookups are allowed; inspect actual relevant entries.

snapshot\ contains the 62 changed teaching/geometry files from the exact Git
commit. diffs\existing.diff contains only the 32 existing-file changes.
repo\kanji (1,206 cards) and repo\words (5,082 articles) are complete
same-commit context exports, not additional editing/review scope. They permit
actual comparison-article, backlink, title, source-word and reading-list
inspection. Other runtime assets are not exported. The manifest is supplied
for scope/hash checks. The repo README's publication counts still describe
the previously published checkpoint; packet.json gives this draft tree's
counts. Publication closure documentation has not been written yet.

## Review contract

Read rubric\copilot-instructions.md and
rubric\content-structure.instructions.md, plus repo\docs\content-format.md's
kanji/quiz contracts. Cover correctness, scoped coverage, consistency/quiz
safety and comprehensibility for the complete shared scope. Do not split
the fifteen cards into disjoint reviewer assignments.

Inspect complete applicable dictionary entries and actual reused/comparison
articles, including spelling/reading restrictions and sense-local flags.
evidence\jmdict-families.xml preserves all elements of 91 applicable families;
dictionary-index.json maps the 102 queried spellings to entries (an empty
list means no entry with exactly that spelling was found). Source readings,
counts and radicals are in source-metadata.json and the full KANJIDIC2
records. evidence\kanjivg has the pinned SVGs. The official Joyo PDF and
extracted rows are provided. Provenance lists hashes, attribution and public
character-entry URLs, without author conclusions. Consult independent public
sources as needed; a filename, digest or successful fetch alone does not
verify a linguistic claim.

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
(reading-exposure.txt; reading-exposure-noextra.txt repeats it without the
extra readings) is a Python port with full N1/All pools of 1,206 cards and
Starter sessions plus one borrowed target. Its legacy prose claiming these
are all actual app pools, or that custom pools are not built by an app, is
NOT established by the run. Custom and caller-built pools, multiple borrowed
Starter cards, actual Kotlin draws, native execution and installed-client
compatibility are unverified. Do not infer a universal safety guarantee from
zero modeled hits.

The audit reports 0 modeled hits and 7 latent entries: three nanori-only
entries (謝 さ/ざ/さ, outside the lexical teaching scope) and four
dictionary/character readings (縫 ぶ, 討 たずねる, 寧 にょう, 援 おん).
The helper labels every extra reading it was given "(card text)" regardless
of origin. Those extras come from the cards' own text (飢 かつ.える, 需
もと.める, 徹 とお.る/とお.す, 討 たず.ねる, 寧 ニョウ, 援 たす.ける/ひ.く)
and from saved public Wiktionary snippets that the cards do not state (縫 ブ,
徹 テチ, 誕 ダン/いつわ.る, 援 たす.け/オン). In a hypothetical Starter session
that also borrows one further holder card, the 援 on-prompt エン could draw
おん with the holders 恩, 温 or 音; the other six latent entries are not
drawable with any single extra holder. The 徹 on-prompt (テツ) has one info
line for the name-only reading つ (holders 子 通 都), drawable only in the
padded Starter session.

Quiz-safety fallback: in the full N1 and All pools exactly three prompts use
the fallback for one of the three wrong readings, each with two curated
options: 飢 kun う.える and 握 kun にぎ.る (the curated 凡 and 掲 have empty
quizKunyomi), and 誕 on タン (the curated 談 reads ダン, a voiced variant of
タン). Every other N1/All prompt is filled by the three curated options.
Starter practice sessions fill from the fallback.

The author's automated title/meaning-overlap scans and design-time review
are not a complete card-by-card read inventory of the comparison cards; read
the relevant comparison cards yourself.
JVM/emulator work is held. The last delivered 5c000bd APK predates kanji
quiz_exclusions; neither this packet nor host checks establish phone acceptance.
The manifest lists 7,777 entries in its files dictionary (8,631 runtime
entries across all nine sections); the tree has 1,206 kanji and 5,082 word
articles.

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
