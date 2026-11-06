$ErrorActionPreference = 'Stop'
if (Test-Path Env:\GH_TOKEN) { throw 'Unexpected inherited GH_TOKEN' }
$before = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $before -ne 'romanko-ms') { throw 'Unexpected default identity' }
$logs = Join-Path $PSScriptRoot 'logs\ecff7653-5e6e-4424-8cb2-a4825995bdb4'
$body = Join-Path $logs 'issue-553-body.txt'
$receipt = Join-Path $logs 'issue-553-created.json'
$verified = Join-Path $logs 'issue-553-verified.json'
if ((Test-Path $receipt) -or (Test-Path $verified)) { throw 'Do not duplicate issue evidence' }
if (-not (Test-Path $body)) { throw 'Exact issue body missing' }
$ownerToken = & gh auth token --user stop-cran
if ($LASTEXITCODE -ne 0 -or -not $ownerToken) { throw 'Owner token unavailable' }
try {
    $env:GH_TOKEN = $ownerToken
    $ownerToken = $null
    $owner = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $owner -ne 'stop-cran') { throw 'Owner identity mismatch' }
    & gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST -F "body=@$body" > $receipt
    if ($LASTEXITCODE -ne 0) { throw 'Issue publication failed; preserve response' }
    $result = Get-Content $receipt -Raw | ConvertFrom-Json
    if ($result.user.login -ne 'stop-cran') { throw 'Issue author mismatch' }
    & gh api "repos/stop-cran/learning-japanese/issues/comments/$($result.id)" > $verified
    if ($LASTEXITCODE -ne 0) { throw 'Issue read-back failed' }
    Write-Output $result.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
    $ownerToken = $null
}
$after = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $after -ne 'romanko-ms') { throw 'Default identity changed' }
