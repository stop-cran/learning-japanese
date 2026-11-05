param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Family, [switch]$Recovery)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = "batch-065-visual-$Family"
if ($Recovery) { $prefix += '-serial-recovery' }
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Never overwrite original execution evidence' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne '18c87f8ac27f3bd0eb59f4320130bfdfd34a755f') { throw 'Unexpected evidence HEAD' }
if (& git -C $root diff 45c275e7c041d8486705ab860a31f34e51ac7a70 -- kanji words articles strokes manifest.json) { throw 'Teaching changed' }
$processes = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'copilot.exe' })
$processes | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Depth 3 | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-preflight.json")
if ($processes | Where-Object { $_.CommandLine -match '9555ba9e-42a2-497b-b221-dff6587e98e0|491afc55-0d7d-42d1-aef9-3d2f6681b28b' }) { throw 'Original reviewer session already active' }
$model = 'claude-opus-5.5'
$session = '9555ba9e-42a2-497b-b221-dff6587e98e0'
if ($Family -eq 'gpt') {
    $prior = Get-Content (Join-Path $root 'docs\n1-reviews\batch-065-visual-claude-serial-recovery-execution.json') -Raw | ConvertFrom-Json
    if (-not $prior.processAndCoverageAccepted -or $prior.exitCode -ne 0) { throw 'First complete serial archive required' }
    $model = 'gpt-6.1-sol'
    $session = '491afc55-0d7d-42d1-aef9-3d2f6681b28b'
}
$prompt = [IO.File]::ReadAllText((Join-Path $PSScriptRoot "$prefix-prompt.txt"))
$started = (Get-Date).ToString('o')
& copilot --model $model --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = $model
    sessionId = $session
    snapshot = '45c275e7c041d8486705ab860a31f34e51ac7a70'
    evidenceHead = '18c87f8ac27f3bd0eb59f4320130bfdfd34a755f'
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
