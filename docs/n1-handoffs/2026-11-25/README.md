# N1 kanji continuation preservation handoff (2026-11-25)

This is a preservation snapshot, not publication, review approval, or permission to skip any step of the
batch pipeline. No tests, builds, review admissions, merges, or releases were run for the copied files. The
only checks were a SHA-256 comparison of every copy with its source, a comparison of the ten draft stroke
files with `b171_strokes.json` and the pinned stroke-input receipt, and a baseline
`python tools/check_content_budget.py` run on `beca991c`. Source files were copied byte for byte, except
checkpoints 155 and 157, which were trimmed to remove verbatim Digital Daijisen tables; their
`inventory.json` rows record both the trimmed and the source hash. The Python under `code/` is historical
scratch tooling with hard-coded paths, batch numbers and bases: adapt it, never rerun it unchanged.
Everything under `b171-draft/` is unreviewed and earns no delivery credit. The copied checkpoints keep
superseded details, so this README and the
[continuation section of the authoring notes](../../n1-authoring-notes.md#continuation-state-after-b170-2026-11-25)
win where they disagree.

## State at writing

| Item | Value |
| --- | --- |
| Main when this handoff was prepared | `beca991c03d66578b2abccce7f29de1c4a2ab983`, the signed B170 receipt. Main then moved to `dd057663ae8ed6c89647704655311082a8551a02` (17 docs-only commits from another session: reader-review guidance in `.github/copilot-instructions.md`, `docs/content-format.md` and three listening docs; no N1 content and no `manifest.json` change). The commit that adds this folder moves it again. **Fetch main and diff it against `beca991c` before planning.** |
| Delivered | 728 = 722 N1 + 6 retained N2 (保 案 派 第 策 結) |
| Remaining | 500 = 305 Jōyō + 195 name-use rows. `docs/n1-sources/source-index.json` has 1,232 rows: 1,228 pending (728 delivered + 500 remaining) and 4 baseline-preserved. |
| Last published | B170 (慈 慕 慨 慶 憂 憤 憾 懇 懲 遺): content `bb6d668220d3bdf1e21c779b3273da666a9fb4bf`, [CI 45541483925](https://github.com/stop-cran/learning-japanese/actions/runs/45541483925); receipt `beca991c…`, [CI 45541653997](https://github.com/stop-cran/learning-japanese/actions/runs/45541653997); contentVersion `f48bb363357e2a64`. |
| In progress | B171: evidence and plan complete, membership and stroke files drafted, **content and render scripts not written**. Nothing is committed, signed, pushed or under review. |
| Running | Nothing. The single sequential writer session was paused and idle. |
| Issue checkpoints | [#60 comment 7152185324](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7152185324) (B170); the checkpoint for this handoff follows it. |

## Preservation map

| Path here | Original location | Contents |
| --- | --- | --- |
| `inventory.json` | generated | `sourcePath`, `snapshotPath`, `sha256` and `bytes` for the other 81 files |
| `B171-RESUME.md` | writer session `files\` | The writer's pause note; this README supersedes it where they differ |
| `code/writer/` | writer session `files\` | `b169_*.py` and `b170_*.py` (content text, render, strokes, panel, close, publish, follow-up), `b171_lookup.py`, `b171_strokes.py`, `n1_gates.py`, and the `b169/b170/b171_strokes.json` inputs |
| `code/lean/` | `n1-kanji-workspace\lean\` | `n1lib.py` and the lean checks (`quiz_safety`, `reading_options`, `reading_exposure`, `n1_batch_tool` lint, `n1cmds`, `jm`, `kanjipedia`, `n1_closure`, `n1_audit`, …). None of this was in Git before. |
| `b171-draft/` | untracked files in `b171-wt` | `docs/n1-sources/batch-171-membership.json` and the ten stroke files 戒 戯 扉 扶 抄 把 抑 披 抹 露. They sit here, not at their real paths, so that unreviewed membership and strokes never appear on `main`'s audited and shipped paths. |
| `evidence/b171/` | `n1-kanji-workspace\` | Author evidence: `b171-cands.txt`, JMdict lookups `b171-jm.json`…`jm8.json` and `.txt` lists, `b171-joyo.txt`, `b171-readings.json`, `b171-words.txt`, `b171-inv.txt` |
| `stroke-inputs-receipt.json` | the stroke-input cache's `receipt.json` | Pins the KanjiVG revision, converter blob ids and per-kanji svg hashes |
| `writer-checkpoints/` | writer session `checkpoints\` | 025, 100, 155–158. **155 and 157 are trimmed.** Their Digital Daijisen tables were verbatim dictionary entries; re-fetch an entry when authoring (`python n1_batch_tool.py webcheck <kanji…> --out <dir>`, or `webtest.py <word>`) and quote only a short clause, as the cards do. |

Deliberately not copied: scraped Daijisen/Weblio pages (`b171-dj*.json`), the raw `JMdict_e.gz` and its cache,
`lean\cache\` (rebuildable), the KanjiVG svg cache (re-fetchable), and temporary files.

## Resuming B171

Keep a single writer: no second session may author or publish N1 batches meanwhile.

1. Fetch `origin/main`. Create a short-rooted worktree at `beca991c03d66578b2abccce7f29de1c4a2ab983` named
   `b171-wt`, on branch `n1-b171` created with `--no-track` (see "Local working trees and publishing" in
   `.github/copilot-instructions.md`). Scripts assert the directory name. Keep the draft rooted at `beca991c`:
   the membership file's `selectionBase` and `baseCommit` both name it, as do `b171_strokes.py` and the gate
   command.
2. Copy `b171-draft/docs/n1-sources/batch-171-membership.json` and `b171-draft/strokes/*.json` into that worktree
   and compare each with its `inventory.json` hash. The stroke counts are 戒7 戯15 扉12 扶7 抄7 把7 抑7 披8 抹8
   露21. Alternatively delete the stroke files and rerun `b171_strokes.py`, which needs the KanjiVG cache and
   refuses to overwrite an existing file.
3. Recreate the layout the scripts assume, next to `b171-wt`: `lean\` (from `code/lean/`), `jmdict\` (pinned inputs,
   see below), and `b171-readings.json`, `b171-joyo.txt` copied from `evidence/b171/`. `n1lib.py` hard-codes
   `C:\Users\romanko\n1-kanji-workspace\{jmdict,lean}` and defaults `N1_REPO` to a stale clone: set `N1_REPO` to the
   active worktree, or let `n1_gates.py` set it.
4. Write `b171_content.py` and `b171_render.py` from `b170_content.py` and `b170_render.py`. Checkpoint 157 is the
   fullest input (headings `b170_content.py format`, `b170_render.py → b171_render.py changes`, `Card plan`,
   `Distractor and exclusion card titles`, `Verified JMdict entries (pinned)`, `Joyo rows`, `Word frontmatter
   plan`, `Examples`, `Unselected readings`, `Shape cues`). Checkpoint 155 adds `Constituent card edits (exact
   current lines)`, and 158 adds `meta_scan findings at base`. Constants to update in every B170 copy: the batch
   number, `b170-wt` → `b171-wt`, `BASE`/`base`, and `..\b170-readings.json`, `..\b170-scan`.
5. Render, then `python tools/validate.py`, `python tools/build_manifest.py`, `word_quiz_audit.py` (0 problems),
   `python tools/audit_n1_batch.py --batch 171`, and `n1_gates.py 171 beca991c03d66578b2abccce7f29de1c4a2ab983 "戒 戯 扉 扶 抄 把 抑 披 抹 露" "警 握 暴 曲 養 本 制 茶" "警戒 戯曲 扉 扶養 抄本 把握 抑制 披露 抹茶 暴露"`
   (about 8 minutes). Expect only the pre-existing `kanji/産.md` lint errors (う.まれる, うぶ-, む.す lack a
   Readings row) and 13 pre-existing warnings; disclose them, do not fix them. If a rerender is needed, restore
   the base state first (`git checkout <base> -- kanji words docs/n1-sources manifest.json strokes`, delete the new
   files except the membership file) instead of hand-editing the ledger.
6. Signed draft commit `N1 B171 draft: 戒 戯 扉 扶 抄 把 抑 披 抹 露`. Then the serial blind reviews with initial,
   follow-up and final stages in the original sessions (B168–B170: claude-sonnet-5.5 correctness → gpt-6.2-sol
   consistency and quiz safety → grok-4.7 comprehensibility; record the models that actually respond), `b171_close.py`,
   integration, signed content and receipt commits, ZIP verification, a #60 checkpoint and a recount. The target is
   **738 delivered / 490 remaining** (`b170_publish.py` hard-codes 728/500, so edit it). B172 is expected to be
   拐 拒 拓 拘 拙 拠 拳 拷 挑 据; reselect on the B171 receipt.

**Integration rule.** Main is already past `beca991c`, so closure will be an integration merge (`HEAD^1` = last reviewed
snapshot, `HEAD^2` = `origin/main`), as in B167–B169. In the same merge commit, set `baseCommit` to the new upstream
in both `batch-171-membership.json` and `batch-171-progress.json` and add the `integration` record as B168 and B169 wrote it
(`originalBase`, `reviewedTeaching`, `newBase`, `preservedReviewedArticleAndStrokeBlobs`, `upstreamArticles`,
`combinedArticles`, `combinedNote`, `manifestRebuilt`, `integratedContentVersion`; B167 has the same keys without the two
`combined…` ones). `b170_close.py`'s merged branch records only `{upstream, merged: true}` and does not rewrite
`baseCommit`, yet `b170_publish.py` asserts `remote() == baseCommit` and `HEAD^2 == baseCommit`, and
`audit_n1_batch.py` requires the ledger and membership `baseCommit` to match. Preserve reviewed article and stroke
blobs byte for byte (B167 kept 39, B168 39, B169 36). If upstream edited a card that the batch also edited, combine both
edits by hand and record it: B168 did this for `kanji/問.md`, while B169 recorded `combinedArticles: []` because no reviewed
file overlapped. Re-run `python tools/build_manifest.py` and `git diff --exit-code manifest.json` after the merge.

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

## Non-Git inputs

| Input | On the writer PC | If lost |
| --- | --- | --- |
| Pinned JMdict (`docs/n1-sources/continuation-inputs.json`) | `C:\Users\romanko\n1-kanji-workspace\jmdict\JMdict_e.gz`: 10,603,352 bytes, sha256 `42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec`, EDRDG `Last-Modified` 17 Nov 2026 | **Not re-downloadable**: EDRDG serves only the latest file, so this PC holds the only copy. Never substitute a newer file silently; add a new pin record as B135 did and disclose it. The per-batch `docs/n1-sources/batch-NNN-jmdict*.xml` excerpts and `evidence/b171/` partly mitigate the loss. |
| Jōyō table PDF and page text | `jmdict\joyokanjihyo_20101130.pdf` (sha256 `d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42`), `joyo-pages.json` (sha256 `f5574709f1db32f4e891e981d97ee95bb3b81ba532afb4a1f3344849a69c86c0`, pdfplumber text) | Re-download from [bunka.go.jp](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf) and rebuild with pdfplumber. The rows are extracted text, not a visual inspection of PDF glyphs. |
| KanjiVG stroke inputs | `stroke-inputs-70a0b7ae0c18\` in the coordinator session's files folder (1,061 files, 530 rows: every remaining N1 kanji) | Refetch `kanjivg/kanjivg@70a0b7ae0c18ceb5cb358274b029cce0234a43bc` svgs and check their git blob ids and sizes against `source-index.json`'s `kanjivgInventory`; `stroke-inputs-receipt.json` holds the expected values. |
| Lean caches | `lean\cache\` (about 21 MB) | `n1lib.build_jmdict_cache(force=False)`, `n1lib.build_kanjidic_cache(force=False)`, `jm_extra.build(force=False)` |
| Weblio and Daijisen pages | not preserved | Re-fetch with `webcheck` or `webtest.py` |

## Other open items

- **Rare-font prerequisite (Android), not fixed.** 13 of the 25 code points that Android's `RareHan.kt` routes to bundled fonts
  are missing from the assigned font and from `RareHanTest`'s inventory: `U+2E8C U+2E95 U+2EA4 U+2ECC U+2ECF U+2ED6
  U+3404 U+342E U+4343 U+2008A U+21C2A U+2298F U+27607`. Twenty-two earlier cards are affected
  ([#60 comment 7138231670](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7138231670)); B169 and B170
  added none. This is a static cmap check, not an observation on a device, and it blocks whole-set acceptance only.
  The remedy is the font-subset mechanism with the [Android #83](https://github.com/stop-cran/kanji-cards-android/issues/83)
  precedent, or revising the affected teaching.
- **Eleven blocked name-use rows:** 崚 彪 晟 燿 舜 赳 have no usable pinned spelling; 侑 嵯 怜 滉 瑚 need out-of-scope
  constituents. Recheck each at its turn and never fabricate support. 瑠/璃, 芙/蓉 and 袈/裟 depend on each other.
- **Budget.** `tools/check_content_budget.py` passes at the `beca991c` baseline with about 7.3 MB of retained-bytes
  headroom under the 62 MiB guard (57,686,579 retained) and about 7.0 MB under the 42 MiB compressed guard
  (`localZipBytes` 36,998,290). The last ten batches added about 72 KB of retained bytes each (peak 130 KB at B169), so the
  remaining ~50 batches need about 3.6–6.5 MB: enough at the mean, tight at the peak, and the compressed figure has not
  been tracked per batch. The retained guard was raised from 56 to 62 MiB in `f072122b` and sits 2 MiB below the Android
  importer's 64 MiB limit; the root `README.md` ("App archive packaging") says raising it above that limit requires an
  updated importer to reach users first. The owner's standing instruction was "try x2 for now. Then maybe we increase
  more", so ask before raising any guard, and do it in a separate, disclosed commit before the guard is hit. Documents
  and handoff folders are export-ignored and never count.
- **Limits stay in force.** Daijisen, Kanjipedia, standard-table and KanjiVG checks are author records, quiz checks are
  static simulations, and there is no native-speaker, Android, device or whole-set acceptance claim.

## Attribution

The original articles and cards are licensed under CC BY-SA 4.0 (see `LICENSE`). `strokes/*.json` derive from
[KanjiVG](https://kanjivg.tagaini.net) (© Ulrich Apel and contributors) and remain under CC BY-SA 3.0; the converted
files name the source revision, and the draft stroke files here do too. Readings, stroke counts and radicals use
KANJIDIC2 and JMdict (© James William Breen and the Electronic Dictionary Research and Development Group), used under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) following the
[EDRDG terms](https://www.edrdg.org/edrdg/licence.html); the lookup files under `evidence/b171/` are excerpts of that
data. Explanations and examples are original teaching text, and this handoff holds no verbatim Digital Daijisen entries.

For GitHub writes, use the repository owner's account (`stop-cran`) without changing shared global authentication: set
`GH_TOKEN` from `gh auth token --user stop-cran` for each command and never store it. Sign commits with the configured owner
key and stop rather than retrying if signing waits on an unavailable passphrase. The "Local working trees and publishing"
section of `.github/copilot-instructions.md` lists the path-length, duplicate-commit and signing-key checks that apply to
every push.
