$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$bodyPath = "$control\batch-084-visual-588-issue.txt"
$payloadPath = "$control\batch-084-visual-588-issue-payload.json"
$postedPath = "$control\batch-084-visual-588-issue-posted.json"
$verifiedPath = "$control\batch-084-visual-588-issue-verified.json"
foreach ($path in @($payloadPath, $postedPath, $verifiedPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing issue attempt; inspect rather than duplicate.' }
}
$head = git -C $content rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read checkpoint HEAD.' }
if ((git -C $content rev-parse 'HEAD^') -ne 'a445a3f154afd5833fa99ba0c6abe13379402e1f') { throw 'Unexpected checkpoint parent.' }
if ((git -C $content log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature not good.' }
if ((git -C $content status --porcelain) -or $LASTEXITCODE -ne 0) { throw 'Content worktree not clean.' }
$body = (Get-Content -LiteralPath $bodyPath -Raw).TrimEnd()
if (-not $body.Contains($head)) { throw 'Checkpoint commit missing from issue body.' }
@{body=$body} | ConvertTo-Json | Set-Content -LiteralPath $payloadPath -Encoding utf8NoBOM
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Scoped owner token unavailable.' }
    $identity = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Scoped owner identity mismatch.' }
    gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath |
        Set-Content -LiteralPath $postedPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed; preserve response.' }
    $posted = Get-Content -LiteralPath $postedPath -Raw | ConvertFrom-Json
    gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" |
        Set-Content -LiteralPath $verifiedPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Cannot verify owner issue receipt.' }
    $verified = Get-Content -LiteralPath $verifiedPath -Raw | ConvertFrom-Json
    $normalize = { param($text) $text.Replace("`r`n", "`n").TrimEnd() }
    if ($verified.user.login -ne 'stop-cran' -or (& $normalize $verified.body) -cne (& $normalize $body)) {
        throw 'Owner author/body verification failed.'
    }
    Write-Output $verified.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
