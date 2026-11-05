param([Parameter(Mandatory=$true)][ValidateSet('accepted','terminal')][string]$Phase)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$head = & git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read HEAD' }
$remote = & git -C $root ls-remote origin refs/heads/main
if ($LASTEXITCODE -ne 0 -or ($remote -split '\s+')[0] -ne $head) { throw 'Remote HEAD mismatch' }
$run = $null
for ($attempt = 0; $attempt -lt 12; $attempt++) {
    $runs = & gh run list --repo stop-cran/learning-japanese --commit $head --workflow 'Validate content' --limit 5 --json databaseId,status,conclusion,headSha
    if ($LASTEXITCODE -ne 0) { throw 'CI discovery failed' }
    $run = @($runs | ConvertFrom-Json)[0]
    if ($run -and $run.headSha -eq $head) { break }
    Start-Sleep -Seconds 5
}
if (-not $run -or $run.headSha -ne $head) { throw 'Exact CI run not yet available; checkpoint pending' }
& gh run watch $run.databaseId --repo stop-cran/learning-japanese --exit-status --interval 10
if ($LASTEXITCODE -ne 0) { throw 'Exact CI did not pass' }
$ciPath = Join-Path $PSScriptRoot "artifacts\batch-071-$Phase-ci.json"
if (Test-Path $ciPath) { throw 'Never overwrite exact CI evidence' }
& gh run view $run.databaseId --repo stop-cran/learning-japanese --json databaseId,status,conclusion,headSha,workflowName,jobs > $ciPath
if ($LASTEXITCODE -ne 0) { throw 'CI receipt failed' }
$ci = Get-Content $ciPath -Raw | ConvertFrom-Json
if ($ci.headSha -ne $head -or $ci.status -ne 'completed' -or $ci.conclusion -ne 'success') { throw 'CI receipt mismatch' }
$zip = Join-Path $PSScriptRoot "artifacts\content-$($head.Substring(0,7)).zip"
if (Test-Path $zip) { throw 'Immutable ZIP already exists; verify saved artifact instead' }
& curl.exe --fail --location --silent --show-error "https://api.github.com/repos/stop-cran/learning-japanese/zipball/$head" --output $zip
if ($LASTEXITCODE -ne 0) { throw 'Public ZIP download failed' }
$receipt = Join-Path $PSScriptRoot "artifacts\content-$($head.Substring(0,7))-acceptance.json"
if (Test-Path $receipt) { throw 'Never overwrite exact public ZIP receipt' }
& python -X utf8 -B (Join-Path $PSScriptRoot 'verify-batch-002-publication.py') $head $zip $receipt
if ($LASTEXITCODE -ne 0) { throw 'Exact public runtime/archive budget verification failed' }
