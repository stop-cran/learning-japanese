# B134 integration-impact confirmation (replacement review)

Reviewer: N1-B134-INTEG-CLAUDE-REPLACEMENT-001 (Claude model family; this is a fresh
replacement review, not a resumption of an earlier reviewer session). I did not read any
other reviewer's report.

## Snapshot

- Reviewed merge commit (M2): `bf9aa740208cceb660788f150b2a4e76930d41d1`
  ("Merge origin/main (9d7b5121) into N1 B134 continuation"). Worktree HEAD resolved to the same commit.
- Parent 1 (B134 handoff): `2eb0e9c97d44e61bf611153ce5899714c1aec35a`
- Parent 2 (origin/main): `9d7b512133f536027c0b601ae0273273b42072ce`
- Merge base (independently recomputed): `830f740bdbe33ac2207acb491cd58e6ab3ab8b8b`
- B134 review snapshot `cc374051` (full `cc374051efa7…`) and closure `ae155573` (full
  `ae1555736086…`); `cc374051` is an ancestor of `ae155573`, which is an ancestor of Parent 1.

## Scope

All checks used commit objects only (`git rev-parse`, `rev-list --parents`, `merge-base`,
`diff --name-only/--name-status --no-renames`, `ls-tree`, `show`, `grep`, `log -S`, `cat-file`) plus
read-only `python -X utf8 -B -` snippets piped through stdin that read git blobs and printed
results. I did not run `tools/build_manifest.py` or any other repository tool.

1. **Mechanical merge integrity.** Computed `diff P1..M2` (139 paths) and `diff P2..M2`
   (1801 paths). Their intersection is only `manifest.json`, so every other path in M2 equals one
   parent, including deletions and mode changes. The P1..M2 set equals base..main exactly
   (72 A, 67 M), and the P2..M2 set equals base..P1 exactly. The only path both sides changed from
   the base is `manifest.json`. `ls-tree` confirms identical blobs for the B134 runtime files at M2,
   `cc374051`, `ae155573` and P1: `kanji/紫.md` `883dbfe6…`, `strokes/紫.json` `0bc7abe0…` and
   `words/紫.md` `3b5901cf…`. Main never changed `words/紫.md`: P2 and the base both have `7230a3c8…`.
   M2 carries the B134 version.
2. **Manifest derivation.** I reimplemented `tools/build_manifest.py` at M2 together with
   `tools/content_language.py`. The reimplementation used the same folders, top-level-only file
   selection, CRLF-normalised versus raw hashing rules, optional payload keys, `contentVersion` formula
   and `indent=1, sort_keys=True` serialisation. It read every blob from the M2 tree (all modes
   `100644`, with no dotfiles or subfolders in the content folders) and derived 7930 `files` entries plus
   the image, scene, listening, audio, curriculum and task payloads. The result was **byte-identical** to the
   committed M2 `manifest.json` (`contentVersion` `ac8420d2a014cf25` in both). The 紫 entries are present
   and match the derived hashes: `kanji/紫.md` `a25c1666…`, `strokes/紫.json` `642dff22…` and
   `words/紫.md` `b7acdf54…`. A three-way per-entry check against the base found 0 problems: main changed
   99 entries, B134 changed 3 file entries, and no entry was changed differently by both sides. The
   only additional difference is the recomputed `contentVersion`. The worktree has no untracked or
   ignored files in the manifest content folders, so a filesystem run would hash the same set.
3. **Teaching/quiz impact.** Main changed only one kanji card, `kanji/気.md`, and nine `words/*気*.md`
   articles. I checked every main hunk in `kanji/` and `words/` with `-U0`. Each is a pure 2-line
   insertion at the end of the body, adding a "see 気 expressions" link. No frontmatter changed: no
   `title`, `tags`, readings, `distractors` or `quiz_exclusions` changed. Main added no `kanji/`,
   `words/` or `strokes/` files. Its additions were 19 articles, 33 docs and 20 grammar files. The
   kanji set (1262) and words set (5084) are identical in P1 and M2. Every 紫 distractor (古, 右, 川)
   and all 58 `quiz_exclusions` IDs resolve to existing cards at M2, and their blobs are unchanged
   from P1 to M2. The articles that 紫 links to (`words/紫.md`, `words/色.md`) are unchanged from P1
   to M2. The linked kanji (包, 古, 右, 川, 書, 濃, 紺, 食) are also outside main's change set. No card declares 紫
   in `distractors` or `quiz_exclusions` at P1 or M2. Per `docs/content-format.md` §Quiz authoring,
   meaning choices come from kanji-card titles, tags and quiz fields, none of which main altered.
   The reading-question inputs for 紫 (`quizOnyomi: []`, `quizKunyomi: [むらさき]` → `words/紫.md`)
   are unchanged. Main also changed `docs/content-format.md` and `docs/confusable-words.md`, but those
   edits only update grammar counts and 気 cross-references.
4. **New content using 紫.** I ran `git log -S'紫' 830f740b..9d7b5121` and found no commits. I scanned
   every main-side diff line for 紫, むらさき and ムラサキ and found no hits. I ran `git grep` at M2 over
   all 138 main-changed non-manifest paths for 紫, むらさき, ムラサキ, `%E7%B4%AB`, `\u7d2b`, `&#x7d2b;`,
   murasaki, gromwell, purple, violet, ultraviolet and 紫外. That also found no hits. Across the whole M2 tree
   outside `docs/n1-*`, 紫 appears only in pre-existing N2 vocabulary docs, `words/山水.md`, B134's own
   files, the manifest and incidental binary-byte matches. None of those files was changed by main. B134 itself
   changed no tools, README or shared docs except `docs/n1-authoring-notes.md`, which main did not touch.
   The grammar vocabulary review (`docs/grammar-vocabulary-review.json`) is keyed per grammar
   exercise, contains no 紫, and has no words-folder digest that B134's `words/紫.md` edit could make stale.

## Verdicts

- Mechanical merge integrity: CLEAN
- Manifest derivation: CLEAN
- Teaching/quiz impact on B134: CLEAN
- Overlapping substantive conflict: CLEAN

## Findings

None.

## Limits

- The manifest result is independent derivation by reimplementing the tool's logic over git blobs, not
  an execution of `tools/build_manifest.py`, as the packet requires. A divergence between my
  reimplementation and the tool is possible only if the tool depends on filesystem state outside
  the tree. I found no untracked or ignored files in its folders.
- Quiz-behaviour conclusions rely on the content contract in `docs/content-format.md` at M2.
  The Android app source (`stop-cran/kanji-cards-android` QuizBuilder) is not in this repository,
  and I did not inspect or run it. I did not run `tools/validate.py` or the unit tests on M2.
- I did not re-review the 紫 card's prose, as the mandate requires.
- I ran `git status --short` once to inspect the worktree. It may have refreshed git's index stat
  cache, but it changed no tracked content, refs or worktree files. The worktree also holds an
  untracked `docs/n1-reviews/batch-134-integration-001/` directory, which is not part of M2 and
  which I did not review.

OVERALL: CLEAN
