$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$bodyPath = Join-Path $control 'batch-098-visual-725-issue-body.txt'
$postedPath = Join-Path $control 'batch-098-visual-725-issue-posted.json'
$receiptPath = Join-Path $control 'batch-098-visual-725-issue-receipt.json'
foreach ($path in @($postedPath, $receiptPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing issue receipt; inspect rather than repost.' }
}
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $saved = git -C "$control\..\learning-japanese" rev-parse HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Cannot identify signed evidence HEAD.' }
    $signature = git -C "$control\..\learning-japanese" log -1 '--format=%G?'
    if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Signed evidence HEAD required.' }
    $body = [IO.File]::ReadAllText($bodyPath) + "`nSigned LOCAL evidence checkpoint: $saved (signature G). Not published.`n"
    $payload = Join-Path $control 'batch-098-visual-725-issue-payload.json'
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
