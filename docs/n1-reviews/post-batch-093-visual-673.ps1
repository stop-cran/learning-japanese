$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
if ($p.checkpoint -ne 672 -or $p.batch -ne '093' -or
    $p.stage -ne 'batch-093-original-session-dependent-visual-confirmations' -or
    (git -C $content rev-parse HEAD^) -ne '66aea026e511368a236c0b427c880aa80ea7f02f' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or
    (git -C $content status --porcelain --untracked-files=all) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or
    (git -C $android status --porcelain --untracked-files=all)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$e = Get-Content "$content\docs\n1-reviews\batch-093-visual-reconciliation-673.json" -Raw | ConvertFrom-Json
if ($e.status -ne 'dependent-visual-review-closed-awaiting-combined-acceptance' -or
    -not $e.serialReviewerProcessesExited -or -not $e.allToolViewsSerial -or
    $e.actionableRemainingFindings -ne 0 -or $e.consequentialUnresolvedInScopeClaims -ne 0) {
    throw 'Visual acceptance evidence incomplete.'
}
$summary = Get-Content "$control\batch-093-visual-673-issue-summary.txt" -Raw
$body = "Batch 093: **original-session dependent visual confirmations closed; current-main combined acceptance and publication remain pending**. Normally signed LOCAL evidence ``$saved``; unchanged teaching ``27663944c7217a19e7de2f363e1b31a5f13452b6``. No runtime publication or batch 094.`n`n$summary"
$prefix = "$control\batch-093-visual-673-"
$payloadPath = $prefix + 'issue-payload.json'
$postedPath = $prefix + 'issue-posted.json'
$receiptPath = $prefix + 'issue-receipt.json'
if ((Test-Path $postedPath) -or (Test-Path $receiptPath)) {
    throw 'Existing issue receipt; never repost.'
}
$body | Set-Content ($prefix + 'issue-body.txt') -Encoding utf8NoBOM -NoNewline
@{body=$body} | ConvertTo-Json | Set-Content $payloadPath -Encoding utf8NoBOM
$oldToken = $env:GH_TOKEN
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable.' }
    $identity = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Owner identity mismatch.' }
    $postedText = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed.' }
    $postedText | Set-Content $postedPath -Encoding utf8NoBOM
    $posted = $postedText | ConvertFrom-Json
    $verifiedText = gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue verification failed.' }
    $verified = $verifiedText | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) {
        throw 'Owner/body verification failed.'
    }
    $verifiedText | Set-Content $receiptPath -Encoding utf8NoBOM
    Write-Output $verified.html_url
} finally {
    $env:GH_TOKEN = $oldToken
}
