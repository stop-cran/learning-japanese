$ErrorActionPreference = 'Stop'
if (Test-Path Env:\GH_TOKEN) { throw 'Unexpected inherited GH_TOKEN' }
$before = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $before -ne 'romanko-ms') { throw 'Unexpected default identity' }
$logs = Join-Path $PSScriptRoot 'logs\bd0d00fd-cb92-446f-b0ef-63f5522ec4a7'
$body = Join-Path $logs 'issue-520-body.txt'
$receipt = Join-Path $logs 'issue-520-created.json'
$verified = Join-Path $logs 'issue-520-verified.json'
if ((Test-Path $receipt) -or (Test-Path $verified)) { throw 'Do not duplicate existing issue evidence' }
if (-not (Test-Path $body)) { throw 'Exact issue body missing' }
$ownerToken = & gh auth token --user stop-cran
if ($LASTEXITCODE -ne 0 -or -not $ownerToken) { throw 'Owner token unavailable' }
try {
    $env:GH_TOKEN = $ownerToken
    $ownerToken = $null
    $owner = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $owner -ne 'stop-cran') { throw 'Owner identity mismatch' }
    & gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST -F "body=@$body" > $receipt
    if ($LASTEXITCODE -ne 0) { throw 'Issue publication failed; preserve exact response' }
    $result = Get-Content $receipt -Raw | ConvertFrom-Json
    if ($result.user.login -ne 'stop-cran') { throw 'Issue author mismatch' }
    & gh api "repos/stop-cran/learning-japanese/issues/comments/$($result.id)" > $verified
    if ($LASTEXITCODE -ne 0) { throw 'Fresh issue read-back failed' }
    Write-Output $result.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
    $ownerToken = $null
}
$after = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $after -ne 'romanko-ms') { throw 'Default identity changed' }
