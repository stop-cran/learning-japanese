# N1 kanji continuation preservation handoff (2026-11-25)

This is a preservation snapshot, not publication, review approval, or permission to skip any step of the
batch pipeline. No tests, builds, review admissions, merges, or releases were run for the copied files. The
only checks were a SHA-256 comparison of every copy with its source, a comparison of the ten draft stroke
files with `b171_strokes.json` and the pinned stroke-input receipt, and a baseline
`python tools/check_content_budget.py` run on `beca991c`. Source files were copied byte for byte, except
checkpoints 155, 156 and 157, which were trimmed to remove verbatim Digital Daijisen text; their
`inventory.json` rows record both the trimmed and the source hash. The Python under `code/` is historical
scratch tooling with hard-coded paths, batch numbers and bases: adapt it, never rerun it unchanged.
Everything under `b171-draft/` is unreviewed and earns no delivery credit. The copied checkpoints keep
superseded details, so this README and the
[continuation section of the authoring notes](../../n1-authoring-notes.md#continuation-state-after-b170-2026-11-25)
win where they disagree.

## State at writing

| Item | Value |
| --- | --- |
| Main when this handoff was prepared | `beca991c03d66578b2abccce7f29de1c4a2ab983`, the signed B170 receipt. Main then moved to `dd057663ae8ed6c89647704655311082a8551a02` (17 docs-only commits from another session: reader-review guidance in `.github/copilot-instructions.md`, `docs/content-format.md`, the listening-authoring instructions and two listening docs; no N1 content and no `manifest.json` change). The commit that adds this folder (`97282e43`) touches only `docs/` and `.github/`. Another session's PR #67 (`c70ee454`, `docs/content-format.md` only) landed next, and a docs-only follow-up commit then corrected this folder's figures and guidance. **Fetch main and diff it against `beca991c` before planning.** |
| Delivered | 728 = 722 N1 + 6 retained N2 (保 案 派 第 策 結) |
| Remaining | 500 = 305 Jōyō + 195 name-use rows. `docs/n1-sources/source-index.json` has 1,232 rows: 1,228 pending (728 delivered + 500 remaining) and 4 baseline-preserved. |
| Last published | B170 (慈 慕 慨 慶 憂 憤 憾 懇 懲 遺): content `bb6d668220d3bdf1e21c779b3273da666a9fb4bf`, [CI 45541483925](https://github.com/stop-cran/learning-japanese/actions/runs/45541483925); receipt `beca991c…`, [CI 45541653997](https://github.com/stop-cran/learning-japanese/actions/runs/45541653997); contentVersion `f48bb363357e2a64`. |
| In progress | B171: evidence and plan complete, membership and stroke files drafted, **content and render scripts not written**. No B171 batch commit exists and nothing is under review; the draft files are preserved here, not at their real paths. |
| Running | Nothing. The single sequential writer session was paused and idle. |
| Issue checkpoints | [#60 comment 7152185324](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7152185324) (B170); the checkpoint for this handoff follows it. |

## Preservation map

| Path here | Original location | Contents |
| --- | --- | --- |
| `inventory.json` | generated | `sourcePath`, `snapshotPath`, `sha256` and `bytes` for 81 files (the folder holds 84: also this README, `inventory.json` and `.gitattributes`); the three trimmed checkpoints also carry `sourceSha256`, `sourceBytes` and `modification` |
| `B171-RESUME.md` | writer session `files\` | The writer's pause note; this README supersedes it where they differ |
| `code/writer/` | writer session `files\` | `b169_*.py` and `b170_*.py` (content text, render, strokes, panel, close, publish, follow-up), `b171_lookup.py`, `b171_strokes.py`, `n1_gates.py`, and the `b169/b170/b171_strokes.json` inputs |
| `code/lean/` | `n1-kanji-workspace\lean\` | `n1lib.py` and the lean checks (`quiz_safety`, `reading_options`, `reading_exposure`, `n1_batch_tool` lint, `n1cmds`, `jm`, `kanjipedia`, `n1_closure`, `n1_audit`, …). None of this was in Git before. |
| `b171-draft/` | untracked files in `b171-wt` | `docs/n1-sources/batch-171-membership.json` and the ten stroke files 戒 戯 扉 扶 抄 把 抑 披 抹 露. They sit here, not at their real paths, so that unreviewed membership and strokes never appear on `main`'s audited and shipped paths. |
| `evidence/b171/` | `n1-kanji-workspace\` | Author evidence: `b171-cands.txt`, JMdict lookups `b171-jm.json`…`jm8.json` and `.txt` lists, `b171-joyo.txt`, `b171-readings.json`, `b171-words.txt`, `b171-inv.txt` |
| `stroke-inputs-receipt.json` | the stroke-input cache's `receipt.json` | Pins the KanjiVG revision, converter blob ids and per-kanji svg hashes |
| `writer-checkpoints/` | writer session `checkpoints\` | 025, 100, 155–158. **155, 156 and 157 are trimmed.** 155 and 157 held verbatim Digital Daijisen tables, and 156 held three one-line definitions (警戒, 扶養, 抑制), cut here to their first clause; re-fetch an entry when authoring (`python n1_batch_tool.py webcheck <kanji…> --out <dir>`, or `webtest.py <word>`) and quote only a short clause, as the cards do. The checkpoints also cite files in the writer's session-state `files\` folder (their "Session files dir"); only those listed here are preserved. |

Deliberately not copied: scraped Daijisen/Weblio pages (`b171-dj*.json`), the raw `JMdict_e.gz` and its cache,
`lean\cache\` (rebuildable), the KanjiVG svg cache (re-fetchable), and temporary files.

## Resuming B171

Keep a single writer: no second session may author or publish N1 batches meanwhile.

1. Fetch `origin/main`. On the writer PC, `b171-wt` already exists (branch `n1-b171`, at `beca991c`, with the eleven
   untracked draft files); check `git worktree list` and reuse it. Elsewhere, create a short-rooted worktree at
   `beca991c03d66578b2abccce7f29de1c4a2ab983` named `b171-wt`, on branch `n1-b171` created with `--no-track` (see
   "Local working trees and publishing" in `.github/copilot-instructions.md`). The scripts assert the worktree's
   directory name (`Path.cwd().name`) and read `docs/n1-sources/…` relative to it, so run them with the worktree as the
   working directory. The draft is rooted at `beca991c`: the membership file's `selectionBase` and `baseCommit` both
   name it, as do `b171_strokes.py` and the gate command. "Integration rule" below says how to move `baseCommit`.
2. Copy `b171-draft/docs/n1-sources/batch-171-membership.json` and `b171-draft/strokes/*.json` into that worktree
   (the writer PC's `b171-wt` already holds them) and compare each with its `inventory.json` hash. The stroke counts
   are 戒7 戯15 扉12 扶7 抄7 把7 抑7 披8 抹8 露21. Alternatively delete the stroke files and rerun `b171_strokes.py`,
   which needs the KanjiVG cache and refuses to overwrite an existing file.
3. Recreate the layout the scripts assume, next to `b171-wt` (all of it is already in place on the writer PC):
   `lean\` (from `code/lean/`), `jmdict\` (pinned inputs, see below), and `b171-readings.json`, `b171-joyo.txt`
   copied from `evidence/b171/`. `n1lib.py` hard-codes `C:\Users\romanko\n1-kanji-workspace\{jmdict,lean}` and
   defaults `N1_REPO` to a stale clone: set `N1_REPO` to the active worktree, or let `n1_gates.py` set it.
4. Write `b171_content.py` and `b171_render.py` from `b170_content.py` and `b170_render.py`. Checkpoint 157 is the
   fullest input (headings `b170_content.py format`, `b170_render.py → b171_render.py changes`, `Card plan`,
   `Distractor and exclusion card titles`, `Verified JMdict entries (pinned)`, `Joyo rows`, `Word frontmatter
   plan`, `Examples`, `Unselected readings`, `Shape cues`). Checkpoint 155 adds `Constituent card edits (exact
   current lines)`, and 158 adds `meta_scan findings at base`. The B170 scripts hard-code everything, so search
   each copy for `170` and `b170`: the batch number in paths, ids and commit messages, `b170-wt` → `b171-wt`,
   `BASE`/`base`, `..\b170-readings.json` and `..\b170-scan`, the member-list asserts in `b170_render.py` (lines 24–25
   expect the first nine absent rows plus the pulled-forward 遺; B171's is 露), the `kanqual=={'遺憾'}` check (line 40)
   and the accounting figures (see "Pipeline pitfalls" below).
5. Render, then `python tools/validate.py`, `python tools/build_manifest.py`, `word_quiz_audit.py` (0 problems; it is
   `docs/n1-reviews/batch-156-closure/packet/evidence/audits/word_quiz_audit.py` and takes the checkout root, then the
   words), `python tools/audit_n1_batch.py --batch 171`, and `n1_gates.py 171 beca991c03d66578b2abccce7f29de1c4a2ab983 "戒 戯 扉 扶 抄 把 抑 披 抹 露" "警 握 暴 曲 養 本 制 茶" "警戒 戯曲 扉 扶養 抄本 把握 抑制 披露 抹茶 暴露"`
   (about 8 minutes). B170's gate run at its base (`4dff7a1c`; `b170-n1gates.txt` on the writer PC, not in Git, and checkpoint
   100, "Gates", says to expect them) found only the pre-existing `kanji/産.md` lint errors (う.まれる, うぶ-, む.す lack a
   Readings row) and 13 warnings; this handoff did not re-measure them at `beca991c`. Disclose whatever remains, do not fix
   it. If a rerender is needed, restore
   the base state first (`git checkout <base> -- kanji words docs/n1-sources manifest.json strokes`, delete the new
   files except the membership file) instead of hand-editing the ledger.
6. Signed draft commit `N1 B171 draft: 戒 戯 扉 扶 抄 把 抑 披 抹 露`. Then close in the order B167–B170 used (scripts in
   `code/writer/`; "Pipeline pitfalls" below lists what each hard-codes):
   1. Serial blind reviews with `b171_panel.py` (from `b170_panel.py`): `packet`, `initial`, `followup`, `final`, with
      initial, follow-up and final stages in the original sessions (B168–B170: claude-sonnet-5.5 correctness →
      gpt-6.2-sol consistency and quiz safety → grok-4.7 comprehensibility; record the models that actually respond).
      Write `docs/n1-reviews/batch-171-closure/reconciliation.md`, which the close script requires, and create
      `..\b171-review-runs\followup-snapshot` and `final-snapshot` yourself (the full SHA each stage reviewed; "Pipeline
      pitfalls" has the format): no preserved script writes them and the close script needs at least one.
   2. If `origin/main` moved, the integration merge ("Integration rule" below).
   3. `b171_close.py` (from `b170_close.py`), then `b171_publish.py content` (signed close commit, push, GitHub's
      signature check, CI on the exact SHA, ZIP verification, `tools/n1_record_publication.py`) and
      `b171_publish.py receipt` (signed receipt commit, push, CI, ZIP comparison and counts).
   4. A #60 checkpoint and a recount. The target is **738 delivered / 490 remaining**. B172 is expected to be
      拐 拒 拓 拘 拙 拠 拳 拷 挑 据; reselect on the B171 receipt.

**Integration rule.** `origin/main` is already past `beca991c` and other sessions keep pushing, so plan a re-root. As of
`c70ee454` everything since `beca991c` touches only `docs/` and `.github/`, so the audit's immutable-input check still
passes (`source-index.json` and `baseline-word-candidates.json` must equal their copies at `baseCommit`). Closure is then an
integration merge, as in B167–B169 (`HEAD^1` = last reviewed snapshot, `HEAD^2` = `origin/main`). In the merge commit, set
`baseCommit` to the new upstream in both `batch-171-membership.json` and `batch-171-progress.json` and leave
`selectionBase` at `beca991c`: B167–B169 moved only `baseCommit` (`originalBase` → `newBase`: `de6dd519` → `b132a5b0`,
`ac5304ba` → `2f5cade1`, `894d3052` → `37404d7e`), and nothing in `tools/` reads `selectionBase`. What the scripts check:

- `tools/audit_n1_batch.py` requires the ledger's and the membership's `baseCommit` to match.
- `b170_publish.py content` asserts `remote() == baseCommit` and, for a merge, `HEAD == integratedSnapshot`,
  `HEAD^1 == reviewedSnapshot` and `HEAD^2 == baseCommit` (without a merge: `HEAD == reviewedSnapshot` and
  `integration.upstream == baseCommit`). Its `release()` helper requires the remote tip to equal the base again at push
  time, so redo the merge if `origin/main` moves in between.
- `b170_close.py` does not rewrite `baseCommit`; it compares `origin/main` with it (lines 14–22). Equal: it asserts that
  `HEAD` is the last reviewed snapshot and writes `integration` as `{upstream, merged: false, note}` (B170's record, with
  no `integratedSnapshot`). Different: it asserts `HEAD^1` is the last reviewed snapshot and `HEAD^2` is `origin/main`,
  sets `integratedSnapshot` and writes `{upstream, merged: true}`. **It cannot close a re-rooted merge unchanged.** The
  merge commit already moves `baseCommit` to `origin/main`, so the two are equal, the script takes the no-merge branch
  and its `HEAD` assertion (line 17) fails on the merge commit before anything is written. The merge branch is reachable
  only while `baseCommit` still differs from `origin/main`, and then `b170_publish.py content` fails on
  `remote() == baseCommit` (line 31). Do not move `baseCommit` after the close instead: `b170_publish.py` line 34 stages
  only the ledger and the closure folder, so an edited membership file stays uncommitted and `release()` stops at its
  clean-tree check (line 13).
- B169 closed with `b169_close.py` (the only earlier close script kept; the B167 and B168 ledgers have the same shape),
  whose line 14 asserts `HEAD^1 == last reviewed snapshot` and `HEAD^2 == baseCommit` and whose line 15 sets
  `integratedSnapshot` to `HEAD`. It has no `integration` branch, so the richer records written by hand stand
  (`originalBase`, `reviewedTeaching`, `newBase`, `preservedReviewedArticleAndStrokeBlobs`, `upstreamArticles`,
  `manifestRebuilt`, `integratedContentVersion`, plus `combinedArticles` and `combinedNote` in B168 and B169). They carry neither
  `merged` nor `upstream`, and `b170_publish.py` line 32 reads `integration.merged` and raises `KeyError` without it.
  **Recipe for a merge close:** in `b171_close.py` replace lines 14–22 with `b169_close.py` lines 14–15, keep the
  hand-written `integration` record and add `merged: true` and `upstream` to it (B170's record carries `upstream`; the
  publish script reads only `merged` on this path). For a no-merge close, as B170 did, `b170_close.py` works as it is. The
  merge-close change has not been run.

Preserve reviewed article and stroke blobs byte for byte (B167 kept 39, B168 39, B169 36). If upstream edited a card that
the batch also edited, combine both edits by hand and record it: B168 did this for `kanji/問.md`, while B169 recorded
`combinedArticles: []` because no reviewed file overlapped. Re-run `python tools/build_manifest.py` and
`git diff --exit-code manifest.json` after the merge. An untested alternative is to fast-forward the still-unreviewed
`b171-wt` to `origin/main` before the draft commit and use that commit for `BASE`, the gate base and `baseCommit`; B170's
non-merge close path would then apply if `main` has not moved again, but nobody has run it that way.

### B171 card plan

| Kanji | Word | Reading | JMdict entry | Selected | Title | Distractors | Exclusions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 戒 | 警戒 | けいかい | 1252310 | カイ | guard against; admonish | 械成戦 | 警慎禁律注守懲訓備衛護 |
| 戯 | 戯曲 | ぎきょく | 1225010 | ギ | play; jest; drama | 虚戦成 | 遊劇娯興楽演笑奏弾幕芸 |
| 扉 | 扉 | とびら | 1483380 | とびら | door; title page | 非悲俳 | 戸門窓関開閉隣 |
| 扶 | 扶養 | ふよう | 1496990 | フ | help; support | 夫技失 | 助援支養補佐救護丞賛 |
| 抄 | 抄本 | しょうほん | 1349540 | ショウ | excerpt; extract | 少妙秒 | 抜略写録要訳選粋抽択 |
| 把 | 把握 | はあく | 1470910 | ハ | grasp; bundle | 色拝抗 | 握持取束捕執抱括柄 |
| 抑 | 抑制 | よくせい | 1547290 | ヨク | restrain; hold down | 仰迎柳 | 圧押制止縛禁防節 |
| 披 | 披露 | ひろう | 1483490 | ヒ | open; reveal | 被波彼 | 示発表展開現告顕露呈宣掲爆剖 |
| 抹 | 抹茶 | まっちゃ | 1525220 | マツ | rub out; powder | 未味株 | 消削除擦塗粉殺末摩磨 |
| 露 | 暴露 | ばくろ | 1601280 | ロ | dew; expose | 路霧雪 | 顕裸呈浴披滴 |

- **Membership** (`sourceRow`): 戒 402, 戯 403, 扉 406, 扶 408, 抄 410, 把 411, 抑 412, 披 415, 抹 417, and 露 1177, pulled forward
  so that 披露 gives 露's ロウ reading a qualifying route (`EXTRA_MAP={'露':[('披露','ひろう','1483490','ロウ')]}`).
  拐 moves to B172.
- **Word senses.** 戯曲 teaches sense 1 only (`PARTIAL={'戯曲':[1]}`; ledger note "JMdict sense 2 'Chinese opera' not
  taught"). 扉 teaches senses 1–2. 抄本 and 抹茶 carry only news2/spec2, which count as qualifying tags under the owner's decision
  ([#60 comment 7112026459](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7112026459)); the
  others carry ichi1 or news1. New words carry no JLPT level. Avoid 戯言 (ambiguous, search-only under 1756640) and 朝露.
- **悪戯.** 戯 reuses `words/悪戯.md` (entry 1151580; senses 1, 2, 4, 5; `newArticle=False`; a whole-word jukujikun, so
  nothing is allocated to 戯). It is an activated baseline pair and must be in the mappings; link 戯 in that file
  and add a Common-words line on 戯, not a readings-table row. The exact row is in checkpoint 158 under
  `b170_render.py → b171_render.py changes`. Its committed blob is LF, although a checkout shows CRLF under
  `core.autocrlf=true`: checkpoints 155–157 call it CRLF, and 158 corrects them. The render write-out follows the base
  blob (`git show <base>:<path>`), so keep that rule and confirm with `git ls-files --eol`.
- **Constituent cards.** Link the existing mentions on 警 (lines 31 and 37), 握 (line 59) and 暴 (lines 29 and 38); add a
  Common-words line on 曲, 養, 本, 制, 茶. Collapse the Metadata on 警 and 握, which `meta_scan.py` (kept at
  `docs/n1-reviews/batch-137-closure/confirm-packet/gpt/evidence/meta_scan.py`; run it as
  `python -X utf8 meta_scan.py REPO KANJI...` with `N1_LEAN` set) reads only
  as the first `Metadata:` line: 警 has only a `Dictionary:` line (line 46, ids 1252330 1252360 1252310) and 握 has a
  wrapped paragraph (lines 92–97). Follow B167 閉/凡 and B168 縫, and record before and after in
  `changedReusedPassages`. Other metadata gaps (曲, 本, 制, 茶) are listed in checkpoint 158.
- **Kanji with no card, never @-linked:** 頁 摘 控 鎮 謄 巴 肥 戈 廾 卬 虍 曝 闔 鈔 碾 扌. Avoid glyphs in
  U+2E80–2FDF and U+3400–4DBF, and check any other code point in `RareHan.isRare`'s ranges (U+F900–FAFF,
  U+20000–2FFFF) before using it: `RareHanTest` fails on one that its `covered` set lacks.
- **Jōyō table pages:** 戒 23, 戯 34, 扉 130, 扶 133, 抄 79, 把 124, 抑 153, 披 130, 抹 145, 露 160, 暴 143.

### Pipeline pitfalls

These come from reading the preserved scripts in `code/writer/` and checkpoint 100, not from a B171 run. Checkpoint 100
(`writer-checkpoints/100-b170-reviews-done-fixes-planne.md`) is the only written account of the stages; its headings are
`### Render`, `### Gates (in b170-wt)`, `### Panel (b170_panel.py, run from b170-wt)`, `### Close and publish`,
`### Publishing mechanics`, `### Content facts` and `### Quirks`.

- **No gate checks `accounting`.** The render writes the whole block, `b170_close.py` then sets
  `reviewClosedPendingRecordsWithCards` and `localUnreviewedDrafts`, and once the content is on `main`
  `tools/n1_record_publication.py` changes the published figures (`advance_accounting` adds the member count to
  `publishedPendingRecordsWithCards` and `publishedN1Additions`, subtracts it from `undelivered` and sets
  `overallN1TaskComplete`). Only the receipt step asserts any of it (the published and undelivered counts), so a wrong
  figure surfaces after the content is on `main`, and nothing asserts `notStarted`, `localUnreviewedDrafts` or
  `reviewClosedPendingRecordsWithCards`. The B170 scripts hard-code the figures in three places, and each moves by 10 for B171:
  - `b171_render.py`, the `acc` literal (B170 line 141): `publishedPendingRecordsWithCards=728` (B170: 718),
    `publishedN1Additions=722` (712), `undelivered=500` (510) and `notStarted=490` (500); `frozenPendingRecords=1228`,
    `n2Placements=6` and `localUnreviewedDrafts=10` stay.
  - `b171_close.py` (B170 line 40): `reviewClosedPendingRecordsWithCards=738` (728).
  - `b171_publish.py`, `receipt` mode (B170 lines 42 and 51): 738 delivered and 490 undelivered (728 and 500).
- **Review rubric.** `b170_panel.py` line 22 builds `rubric.txt` from `.github/copilot-instructions.md` as it stands in the
  draft snapshot `s`: everything before `## Grammar exercises`, plus the text from `## Independent review and reconciliation`
  up to `## Worked example`. `### N1 kanji batches` sits under `## Large card expansions`, inside that second range. A draft
  rooted at `beca991c` reads that commit's file, which lacks the subsection; the file has grown since (278 lines at
  `beca991c`, 324 at `dd057663`, 365 at `97282e43`, 402 in the follow-up), so rooting the draft later hands the reviewers
  instruction text that B170's reviewers did not have. Either cut the slice at `### N1 kanji batches` and say what else
  changed, or disclose the difference. Do not rename those headings.
- **Review tooling.** `b170_panel.py` needs PyYAML, asserts `Path.cwd().name == "b170-wt"` and hard-codes `base`. The packet
  goes to `b170-packet-<s[:8]>` beside the worktree (`mkdir(exist_ok=False)`) and the run logs to `b170-review-runs`. A
  reviewer whose log already exists is refused (as is `initial` when its `.id` file exists), so a retry needs the old file
  moved aside or a new stage name such as `final2`, which reads `final2-task.txt`. Each stage starts
  `copilot --no-auto-update --model <m> --session-id=<uuid>` (`--resume=<uuid>` for `followup` and `final`) with only the
  `view` tool, in the packet directory, and fails unless every returned message names the requested model. `followup` reads
  `confirmation-task.txt` and `final` reads `last-task.txt` from the packet directory: write them with the earlier findings,
  the revised snapshot SHA and the diff (`git diff <initial>..HEAD -- words kanji`). Replace the B170 content that the script
  hard-codes: the 26-word comparison list `cw`, the keyword regex `rx`, the `snapshot.txt` sentence and the three `profiles`
  (model and facet). That sentence says "no existing word article is reused as a support", which is false for B171: 戯
  reuses `words/悪戯.md` (`newArticle=False`), and `pack()` packs only articles whose mapping has `newArticle` set, so add 悪戯
  to `cw` and correct the sentence. `b170_followup.py` hard-codes `b170-wt`, `..\b170-packet-0ac3eaad` and `..\b170-weblio`.
  The packet, the run logs and `b170-weblio` were not preserved; `b171_panel.py packet` rebuilds the packet from the
  committed draft.
- **Review snapshot files.** `b170_close.py` (lines 10–13) builds its stage list from `..\b170-review-runs\followup-snapshot`
  and `final-snapshot`, each read with `read_text('ascii')` and no stripping and later compared with `==` against
  `git rev-parse` output, so each file must hold exactly the 40-character SHA that stage reviewed, with no newline or space
  after it. B170's are 40 bytes each (followup `63ff44d350ec8d6be3b024d6c462119e1ac2ccb2`, final
  `3a9b777a76a910b84cfbea50e366b0194201eea4`, the snapshots in its `provenance.json`), and `b169-review-runs\` holds a pair
  of the same form. Checkpoint 100 says the runner writes `runs/{stage}-snapshot`, but the preserved `b170_panel.py` does not,
  so create `..\b171-review-runs\followup-snapshot` and `final-snapshot` by hand. The initial stage is not a file: it is `s`,
  the first-parent first commit after `base` (`b170_panel.py` line 8). The close script needs at least one of the two files
  (`len(stages) >= 2`), takes the last stage's SHA as `reviewedSnapshot` and, for a merge close, requires `HEAD^1` to equal it.
  It then reads `<reviewer>-<stage>.jsonl` and `.md` from the same folder for every stage and reviewer, which is where
  `b170_panel.py` writes its run logs and reports.
- **Render, close and publish.** Besides the figures above and the lines that step 4 lists, `b170_render.py` asserts that the
  pinned `..\jmdict\JMdict_e.gz` hashes to the `continuation` pin (line 28) and hard-codes batch 170 in its `ledger` literal
  (line 142: the selection reason, `batch-170-jmdict-selection.json` and `batch-170-jmdict.xml`), in the dictionary-check
  text (line 143) and in its output paths (line 144: `batch-170-progress.json` and `batch-170-jmdict-selection.json`;
  line 146: `batch-170-jmdict.xml`). `b170_close.py` reads the batch-170 ledger, needs
  `docs/n1-reviews/batch-170-closure/reconciliation.md`, writes the reports, `.gitattributes` (`* -text`) and
  `provenance.json`, and asserts for each report a successful `result`, the requested model and strictly serial stage times.
  `b170_publish.py` hard-codes `b170-wt`, the ledger, closure and publication paths, `b170-zip-<sha12>`, the batch number in
  its two commit messages and in `--batch 170`, the `--review-identity` text (a claim about the reviewers: make it say what
  B171's reviewers did), a check that `gh api user` returns `stop-cran` (so `GH_TOKEN` must hold that account's token),
  the signing key `D4C9A275A218AF747B787AFA9D94B9D311BD26A7` and the CI workflow id `378446878` (line 20; on 2026-11-25
  "Validate content", `.github/workflows/validate.yml`, active). `b171_strokes.py` hard-codes `WT`, `BASE` and the KanjiVG
  cache path; copy it for B172 and change them. Mechanics to expect:
  - `b170_close.py` line 3 imports `b170_panel`, whose top-level code runs and asserts the worktree name, so the scripts
    must sit together, run from the worktree and, in the copy, import `b171_panel`.
  - The close script creates `reports\` with `mkdir(exist_ok=False)` (line 24) and saves the ledger last (line 42). A
    failure in between leaves `docs/n1-reviews/batch-171-closure/reports`, and a re-run raises `FileExistsError` until that
    folder is deleted; the ledger itself is untouched.
  - `b170_publish.py` signs its commit first and only then calls `release()`, which needs a completely clean tree
    (`git status --porcelain`, so untracked files count). Both modes also assert `HEAD` before they sign, and that stops
    holding once the signed commit exists, so a failure inside or after `release()` cannot be re-run unchanged: finish the
    remaining steps by hand (push, signature and CI check, ZIP verification, `tools/n1_record_publication.py`) or edit a copy.
- **Gates.** `n1_gates.py BATCH BASE 'KANJI' 'CHANGED KANJI' 'WORDS'` runs from the worktree and sets `N1_REPO` and `N1_LEAN`
  itself. Its steps are `unittest`, `validate`, `budget`, `grammar`, `audit`, `quiz_safety`, `reading_exposure`,
  `reading_options`, `lint`, `meta_scan` and `word_quiz`; `ONLY="lint word_quiz"` restricts them, and it ends with
  `== manifest fresh: True` when rebuilding the manifest changes nothing. The `budget` step is the local
  `tools/check_content_budget.py`, which counts CRLF on a Windows checkout with `core.autocrlf=true` (see "Budget" under
  "Other open items").

## Non-Git inputs

| Input | On the writer PC | If lost |
| --- | --- | --- |
| Pinned JMdict (`docs/n1-sources/continuation-inputs.json`) | `C:\Users\romanko\n1-kanji-workspace\jmdict\JMdict_e.gz`: 10,603,352 bytes, sha256 `42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec`, EDRDG `Last-Modified` 17 Nov 2026 | **Not available from EDRDG as pinned.** On 2026-11-25 EDRDG's current `JMdict_e.gz` (`Last-Modified` 25 Nov 2026, 10,613,343 bytes) differed from the pin, and EDRDG offers no dated copies (third-party snapshots were not searched). This PC holds the only known copy and no backup was made; the pin record says raw dictionary bytes stay outside Git, so the owner should choose where a backup goes. Never substitute a newer file silently: add a new pin record, as B135 did after the 2026-11-17 PC move, and disclose it. The per-batch `docs/n1-sources/batch-NNN-jmdict*.xml` excerpts and `evidence/b171/` partly mitigate the loss. |
| Jōyō table PDF and page text | `jmdict\joyokanjihyo_20101130.pdf` (sha256 `d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42`), `joyo-pages.json` (sha256 `f5574709f1db32f4e891e981d97ee95bb3b81ba532afb4a1f3344849a69c86c0`, pdfplumber text) | Re-download from [bunka.go.jp](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf) and rebuild with pdfplumber. The rows are extracted text, not a visual inspection of PDF glyphs. |
| KanjiVG stroke inputs | `stroke-inputs-70a0b7ae0c18\` in the coordinator session's files folder (1,061 files: `svg\<code>.svg` and `generated\<code>.json` for 530 rows, the kanji left at B167's receipt `ac5304ba`, which includes the 30 delivered in B168–B170, plus `receipt.json`; the code is the five-digit lowercase hex code point) | Refetch `kanjivg/kanjivg@70a0b7ae0c18ceb5cb358274b029cce0234a43bc` svgs and check their git blob ids and sizes against `source-index.json`'s `kanjivgInventory`. That is only half of it: `b171_strokes.py` (line 46) also requires each `generated\<code>.json` to equal its converted output byte for byte and to match the receipt's `sha256`, so regenerate those with `tools/generate_strokes.py` and `tools/order_variants.json` at the blob ids the receipt pins (`generatorGitBlob`, `variantsGitBlob`; the script checks them against the base at lines 21–24) and the receipt's `revision` (line 27). `stroke-inputs-receipt.json` holds the expected values, and the ten B171 stroke files are also under `b171-draft/strokes/`. |
| Lean caches | `lean\cache\` (about 21 MB) | `n1lib.build_jmdict_cache(force=False)`, `n1lib.build_kanjidic_cache(force=False)`, `jm_extra.build(force=False)` |
| Weblio and Daijisen pages | not preserved | Re-fetch with `webcheck` or `webtest.py` |

## Other open items

- **Rare-font prerequisite (Android), not fixed.** 13 of the 25 code points that Android's `RareHan.kt` routes to bundled fonts
  are missing from the assigned font and from `RareHanTest`'s inventory: `U+2E8C U+2E95 U+2EA4 U+2ECC U+2ECF U+2ED6
  U+3404 U+342E U+4343 U+2008A U+21C2A U+2298F U+27607`. Twenty-two earlier cards are affected
  ([#60 comment 7138231670](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7138231670)); B169 and B170
  added none. This is a static cmap check, not an observation on a device. It does not block content publication (content CI
  runs no Android tests), but it blocks whole-set acceptance. `RareHanTest` failed in all nine observed Android `main` CI runs
  (2026-11-15 to 2026-11-21). Android's log does not name the content commit it cloned, so the content behind each run is a
  candidate inferred from the checkout's file count and the content push times; the first red run's candidate held two
  uncovered code points (U+2EA4 in 援, U+2ECF in 廊). It is tracked in
  [kanji-cards-android#147](https://github.com/stop-cran/kanji-cards-android/issues/147), which lists the options and the evidence.
  The remedy is the font-subset mechanism with the [Android #83](https://github.com/stop-cran/kanji-cards-android/issues/83)
  precedent, or revising the affected teaching; the choice is an open owner decision. A dry run on the writer PC (an
  unmodified `tools/make_rare_font.py` from Android `main`, content `97282e43`, HanaMin 8.030 checked against its pinned
  SHA-256 values) found a glyph for all 25 code points and made the two subsets about 3 KB larger. It was not applied, and
  no local Android build or device test was run for it, so no Android test has run with the larger subsets.
- **Eleven blocked name-use rows:** 崚 彪 晟 燿 舜 赳 have no usable pinned spelling; 侑 嵯 怜 滉 瑚 need out-of-scope
  constituents. Recheck each at its turn and never fabricate support. 瑠/璃, 芙/蓉 and 袈/裟 depend on each other.
- **Budget.** CI's `tools/check_content_budget.py` passed on `97282e43` and printed 10,180 files, 10,196 entries,
  57,070,495 retained bytes and `localZipBytes` 36,911,540. The real zipball in
  `docs/n1-reviews/batch-170-publication/zip-receipt.json` is 37,599,206 compressed bytes, and the exported tree is
  identical in paths and bytes to B170's content commit `bb6d668` (compared as `git archive` name-to-sha256 maps), so that
  receipt applies. That leaves 7,941,217 bytes under the 62 MiB
  retained guard and 6,440,986 under the 42 MiB compressed guard by the zipball (7,128,652 by `localZipBytes`); MB figures
  here are decimal and the guards are MiB (about 7.57 and 6.14 MiB of headroom). B161–B170 added 71,971 retained bytes per
  batch on average (about 44 KB compressed), with peaks of 130,105 (B169) and 92,984 (B170). If growth continues like these
  batches, the remaining ~50 batches would use about 3.6 MB retained at the mean, 5.6 MB at the last two batches' mean and
  6.5 MB at B169's rate, all inside the headroom (compressed: about 2.2 MB at the mean, 4.9 MB at B169's 98,881 per batch).
  The peak is an observation, not a bound, and the 195 name-use rows may grow differently. Take headroom from CI or the
  receipt, not from a local run: a Windows checkout with `core.autocrlf=true` counts CRLF, and the same tree printed
  57,686,579 retained and 36,998,290 `localZipBytes` there (the committed blob sizes sum to CI's retained and inflated
  figures). The retained guard was raised from 56 to 62 MiB in `f072122b` (2026-11-22), whose message says to keep headroom
  under the 64 MiB Android import cap; it now sits 2 MiB below that limit, and the root `README.md` ("App archive
  packaging") says raising it above the limit requires an updated importer to reach users first. Suggested practice (the
  author's, not a recorded owner rule): tell the owner before raising any guard again, and do it in a separate, disclosed
  commit before the guard is hit. Documents and handoff folders are export-ignored and never count.
- **Limits stay in force.** Daijisen, Kanjipedia, standard-table and KanjiVG checks are author records, quiz checks are
  static simulations, and there is no native-speaker, Android, device or whole-set acceptance claim.

## Attribution

The original articles and cards are licensed under CC BY-SA 4.0 (see `LICENSE`). `strokes/*.json` derive from
[KanjiVG](https://kanjivg.tagaini.net) (© Ulrich Apel and contributors) and remain under CC BY-SA 3.0; the converted
files name the source revision, and the draft stroke files here do too. Readings, stroke counts and radicals use
KANJIDIC2 and JMdict (© James William Breen and the Electronic Dictionary Research and Development Group), used under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) following the
[EDRDG terms](https://www.edrdg.org/edrdg/licence.html); the lookup files under `evidence/b171/` are excerpts of that
data. Explanations and examples are original teaching text, and this handoff holds only short cited Digital Daijisen
clauses, no full entries.

For GitHub writes, use the repository owner's account (`stop-cran`) without changing shared global authentication: set
`GH_TOKEN` from `gh auth token --user stop-cran` for each command and never store it. Sign commits with the configured owner
key and stop rather than retrying if signing waits on an unavailable passphrase. The "Local working trees and publishing"
section of `.github/copilot-instructions.md` lists the path-length, duplicate-commit and signing-key checks that apply to
every push.
