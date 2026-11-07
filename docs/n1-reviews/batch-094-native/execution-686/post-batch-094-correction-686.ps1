$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$bodyPath = "$control\batch-094-correction-686-issue-body.txt"
$postedPath = "$control\batch-094-correction-686-issue-posted.json"
$receiptPath = "$control\batch-094-correction-686-issue-receipt.json"
foreach ($path in @($bodyPath,$postedPath,$receiptPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing issue receipt; inspect rather than repost.' }
}
$head = git -C $content rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Signed evidence head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Content not wholly clean.' }
$evidence = Get-Content "$content\docs\n1-sources\execution-686.json" -Raw | ConvertFrom-Json
if ($evidence.nativeTestsPassed -ne 1 -or $evidence.directGuardBuilderChecks -ne 128 -or
    $evidence.runtimeAccepted -or $evidence.runtimePublished) { throw 'Unexpected evidence state.' }
$body = @"
### Batch 094: corrected native checkpoint 686 (not publication)

Saved normally signed LOCAL evidence at ``$head``; both dedicated worktrees are clean. The exact corrected full Git archive ``5f0be667`` / contentVersion ``74b7e886a1afbd46`` passed production ContentSync **once**: **1,117 kanji, 5,070 words, 126 N1, zero problems**, accepted Room reading parser epoch 1. Every **8,438** runtime manifest entry/hash and exact ZIP/local runtime bytes were verified under the unchanged packaging guards. This is a local Git ZIP, not the later immutable public-GitHub-ZIP acceptance.

The focused API35 native case returned terminal per-case status **0**, no skips. All **128** production WordQuizBuilder checks passed for the direct 削る/縮める exclusion: both target orientations, both translation directions, All and bounded-custom pools, 16 seeds per configuration. Combined with both original-session textual confirmations685, this narrow observed direct-pair finding is **resolved**; this does not certify every other possible option or every random seed. Full reports, fixture, wrapper, hash receipts and raw instrumentation are preserved in ``docs/n1-reviews/batch-094-native/execution-686/``; reconciliation and evidence are ``docs/n1-reviews/batch-094-correction-reconciliation-686.json`` and ``docs/n1-sources/execution-686.json``.

Earlier 85 unchanged visual captures/font/routes682 and original-session rendered evidence683 remain inherited, not repeated or rebranded. Production Android remains unchanged at ``f9b59a2`` through the qualified TESTONLY checkout ``1c1b7bf4``, not latest app main. Owned read-only emulator5580 parent PID29596/QEMU23836 stopped; temporary Android source/asset removed. No shared device, heap or archive guard was changed. A diagnostic read of runner.lock returned the expected sharing violation; the live parent was independently verified, and child wrappers did not acquire, write, delete or unlock it. No optional historical-session helpers or new permission denials.

**Next:** fresh current-main integration/reconciliation and all combined content/Python/vocabulary/baseline/link/membership/reading/font/budget/applicable Android checks; changed substantive teaching gets independent re-review. Normal signing, owner fast-forward publication, terminal-green CI, every immutable public ZIP runtime hash/budget and verified owner issue gates remain. No runtime publication, batch095 or second runner at this checkpoint. **Published 120/1,228; 1,108 remaining.** Physical-phone/general-release and whole-set acceptance remain outstanding; no human-handwriting or successful MLKit claim.
"@
[IO.File]::WriteAllText($bodyPath,$body,[Text.UTF8Encoding]::new($false))
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $payload = "$control\batch-094-correction-686-issue-payload.json"
    @{body=$body} | ConvertTo-Json -Depth 2 | Set-Content $payload -Encoding utf8NoBOM
    gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payload |
        Set-Content $postedPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed; preserve response.' }
    $posted = Get-Content $postedPath -Raw | ConvertFrom-Json
    if ($posted.user.login -ne 'stop-cran' -or $posted.body -cne $body) { throw 'Posted author/body mismatch.' }
    gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" |
        Set-Content $receiptPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue receipt fetch failed.' }
    $verified = Get-Content $receiptPath -Raw | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Verified author/body mismatch.' }
    $verified.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
