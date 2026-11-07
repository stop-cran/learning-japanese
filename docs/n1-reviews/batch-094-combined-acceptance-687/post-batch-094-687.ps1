$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$bodyPath = "$control\batch-094-687-issue-body.txt"
$postedPath = "$control\batch-094-687-issue-posted.json"
$receiptPath = "$control\batch-094-687-issue-receipt.json"
foreach ($path in @($bodyPath,$postedPath,$receiptPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing issue receipt; inspect rather than repost.' }
}
$head = git -C $content rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Signed evidence head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Content not wholly clean.' }
$e = Get-Content "$content\docs\n1-sources\execution-687.json" -Raw | ConvertFrom-Json
if (-not $e.runtimeAccepted -or $e.runtimePublished -or $e.hostTestsExecuted -ne 4) { throw 'Unexpected evidence state.' }
$body = @"
### Batch 094: combined-tree acceptance checkpoint 687 (not publication)

Saved normally signed LOCAL evidence at ``$head``; both dedicated worktrees clean. Fresh origin/main ``48765e20`` was already integrated; normal non-rewriting merge returned Already up to date, with no runtime or teaching change. **$($e.pythonTestsPassed) Python tests**, validator, vocabulary consistency, regenerated manifest, unchanged publishing budgets and the combined source/baseline/membership/link/reading/stroke/font/hash audit passed. Fresh sibling **three RealContentTest cases + one RareHanTest**, **zero skips**, actually read this content checkout.

All **8,438 runtime hashes** match contentVersion ``74b7e886a1afbd46``. Frozen dictionary extraction verified 125 complete family occurrences / 121 distinct families and ten raw character records; all 985 baseline kanji, 4,942 baseline words and 985 stroke files retain their metadata/bytes except documented reviewed safeguards. Three all-mapped reciprocal pairs/six directions, both activated baseline pairs and all four source reading dispositions remain intact.

The original two-family textual reviews, bounded original-session corrections/rendered confirmations and exact corrected native686 import/128 direct-pair production-builder checks are inherited, not rerun or rebranded. All consequential in-scope findings are resolved. Original Claude683 tool overlap remains rejected with its separate accepted serial repair; complete reports and limits remain intact. The 41 visible Han and 85 captures are unchanged. The new 42nd raw Han, 縮, occurs only in non-rendered exclusion metadata and is covered by all bundled fonts. The first audit correctly stopped against the stale draft raw-Han set; this distinction is now recorded explicitly, not treated as fresh native visual evidence.

Qualified TESTONLY Android ``1c1b7bf4`` retains production ``f9b59a2``, **not latest app main**. Vocabulary consistency at 2,122/2,431 reviewed prompts is not full coverage. No new native/reviewer run, physical-phone, human-handwriting, successful MLKit or exhaustive live-pool semantic certification. Child never acquired/deleted/unlocked parent runner.lock; no optional historical-session helpers or new permission denials.

Evidence: ``docs/n1-sources/execution-687.json``, ``docs/n1-reviews/batch-094-combined-reconciliation-687.json`` and ``docs/n1-reviews/batch-094-combined-acceptance-687/``.

**Next:** fresh-main recheck and normal signed owner fast-forward publication, then exact remote SHA, terminal-green relevant CI, EVERY immutable public GitHub ZIP runtime hash/manifest equality and original 18,000-entry / 42-MiB compressed / 80-MiB inflated / 56-MiB retained / per-file-media-safe-path guards. Local acceptance is not public delivery. No095 or second runner. **Published 120/1,228; 1,108 remaining.** Physical-phone/general-release and whole-set acceptance remain outstanding.
"@
[IO.File]::WriteAllText($bodyPath,$body,[Text.UTF8Encoding]::new($false))
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $payload = "$control\batch-094-687-issue-payload.json"
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
