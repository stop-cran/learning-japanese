param([Parameter(Mandatory=$true)][ValidateSet('glyph','selection')][string]$Turn)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = "batch-061-visual-claude-$Turn"
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if (Test-Path (Join-Path $PSScriptRoot "$prefix.jsonl")) { throw 'Refusing to overwrite original' }
if ((& git -C $root rev-parse HEAD) -ne 'f2267727d982589890b2f4ae0b17e82666337956') { throw 'Snapshot changed' }
$priorPrefix = if ($Turn -eq 'glyph') { 'batch-061-visual-claude' } else { 'batch-061-visual-claude-glyph' }
$prior = Get-Content -Raw (Join-Path $root "docs\n1-reviews\$priorPrefix-execution.json") | ConvertFrom-Json
if ($prior.exitCode -ne 0 -or (Get-Process -Id $prior.launcherPid -ErrorAction SilentlyContinue)) { throw 'Prior review process not exited0' }
$prompt = Get-Content -Raw (Join-Path $PSScriptRoot "$prefix-task.txt")
$started = (Get-Date).ToString('o')
& copilot --model claude-opus-5.5 --session-id 537a357b-564b-433a-897c-1285b08defb2 --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> (Join-Path $PSScriptRoot "$prefix.jsonl") 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = 'claude-opus-5.5'
    sessionId = '537a357b-564b-433a-897c-1285b08defb2'
    snapshot = 'f2267727d982589890b2f4ae0b17e82666337956'
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
