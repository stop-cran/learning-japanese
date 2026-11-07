$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$bodyPath = "$control\batch-095-combined-native-698-issue-body.txt"
$postedPath = "$control\batch-095-combined-native-698-issue-posted.json"
$receiptPath = "$control\batch-095-combined-native-698-issue-receipt.json"
foreach ($path in @($bodyPath, $postedPath, $receiptPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing receipt; inspect rather than repost.' }
}
$head = git -C $content rev-parse HEAD
$parent = git -C $content rev-parse HEAD^
if ($LASTEXITCODE -ne 0 -or $parent -ne '6a7514c1ce11c25d58d43a8195540937a13378be' -or
    (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Normally signed exact child evidence head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Content worktree not wholly clean.' }
$evidence = Get-Content "$content\docs\n1-sources\execution-698.json" -Raw | ConvertFrom-Json
if ($evidence.exactCombinedNativeImport -ne 'passed' -or $evidence.runtimePublished -or
    $evidence.runtimeAccepted -or $evidence.acceptance.publicGithubZipAcceptance) { throw 'Unexpected evidence state.' }
$body = @"
### Batch 095: exact combined native-import checkpoint 698 (not publication)

Saved normally signed LOCAL evidence at ``$head``. The new full combined git archive from signed ``6a7514c1`` (integrated merge ``d5a6823c``) passed production ContentSync **once** on an owned read-only API35 emulator: **1,118 kanji, 5,071 words, 127 N1 cards, zero problems**, accepted Room contentVersion ``3eebfff0fdad5e28`` and reading-parser epoch1.

Full and Lite Room projections preserve raw ボウ / no kun and explicit ボウ / empty-kun curation, yielding only on-key ぼう. All three direct word-exclusion pairs passed 384 builder checks across both target orientations, directions and full/custom pools; 64 bounded meaning-pool checks and both required reciprocal link pairs (four directions) passed. This is bounded technical evidence, not certification of every possible quiz option.

The raw instrumented case terminated **status-code0, one case, no skips**. Fresh device/5580/5581/PID ownership, exact API35 fingerprint, unchanged 192m/576m guest heaps, host GPU/-Vulkan/2048MiB/two cores and offline state are preserved. Only owned emulator PID23116/QEMU5148 were stopped; both exits were verified. The parent runner lock was untouched. Test-only Android ``1c1b7bf4`` retains production ``f9b59a2``; this is **not latest app main**.

The new archive SHA-256 ``dbe15eb1ab24885305a93b4641fbeee8e7720e5ee7dac4326ac99730369736ea`` preserves all 8,441 runtime manifest hashes. Its distinct fixture, test APK hash, complete native result, command/resource/cleanup receipts and helpers are archived under ``docs/n1-reviews/batch-095-combined-native-698`` and ``docs/n1-sources/execution-698.json``. The original694 fixture/archive/results remain immutable and are not relabelled. Local git ZIP evidence is **not public GitHub ZIP acceptance**.

Teaching/runtime/geometry/font/quiz metadata are unchanged. Original691 blind reviews, native694 routes/glyphs, accepted695 rendered confirmations and697 incoming eleven-passage confirmations remain inherited with all original limits, including the rejected original Claude695 overlap and separate minimal serial repair. No new reviewer, visual, route, phone, human-handwriting, MLKit or full-pool claim is made. Combined696's372 Python/four non-skipped Android cases and source/baseline/link/readings/stroke/font checks remain inherited, not rerun here. Validation, manifest freshness and original archive budgets were freshly checked698.

**Next:** normal signed review-closed/combined acceptance; fresh-main recheck and non-rewriting merge/revalidation/changed-teaching confirmation if needed; then owner fast-forward only after all gates, terminal green CI and every exact immutable public ZIP runtime entry/hash plus original budgets. No runtime publication or batch096 here. **Published121/1,228;1,107 remaining.** Physical-phone/general-release/whole-set acceptance remains outstanding. No optional historical-session helpers or new permission denials.
"@
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $payload = "$control\batch-095-combined-native-698-issue-payload.json"
    @{body=$body} | ConvertTo-Json -Depth 2 | Set-Content $payload -Encoding utf8NoBOM
    gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payload |
        Set-Content $postedPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed; preserve response.' }
    $posted = Get-Content $postedPath -Raw | ConvertFrom-Json
    if ($posted.user.login -ne 'stop-cran' -or $posted.body -cne $body) { throw 'Posted author/body mismatch.' }
    gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" |
        Set-Content $receiptPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Independent issue receipt fetch failed.' }
    $verified = Get-Content $receiptPath -Raw | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Verified author/body mismatch.' }
    $verified.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
