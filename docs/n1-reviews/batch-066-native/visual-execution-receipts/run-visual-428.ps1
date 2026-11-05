param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Family)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = "batch-066-visual-$Family"
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Never overwrite original execution evidence' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne 'b37c5ad6ffb5ab62cf4525b50afe4e2a6cdd011b') { throw 'Unexpected evidence HEAD' }
if (& git -C $root diff 6c23db00d2d14ec6d0a3537a1ef72b273e3d55e7 -- kanji words articles strokes manifest.json) { throw 'Teaching changed' }
$processes = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'copilot.exe' })
$processes | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Depth 3 | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-preflight.json")
if ($processes | Where-Object { $_.CommandLine -match '9db759dd-1a9d-4c7f-b3ab-049af5686bc4|81338bd1-836a-4b79-9fc6-69d90c5d00ab' }) { throw 'Original reviewer session already active' }
$model = 'claude-opus-5.5'
$session = '9db759dd-1a9d-4c7f-b3ab-049af5686bc4'
if ($Family -eq 'gpt') {
    $prior = Get-Content (Join-Path $root 'docs\n1-reviews\batch-066-visual-claude-execution.json') -Raw | ConvertFrom-Json
    if (-not $prior.processAndCoverageAccepted -or $prior.exitCode -ne 0) { throw 'First complete serial archive required' }
    $model = 'gpt-6.1-sol'
    $session = '81338bd1-836a-4b79-9fc6-69d90c5d00ab'
}
$prompt = [IO.File]::ReadAllText((Join-Path $PSScriptRoot "$prefix-prompt.txt"))
$started = (Get-Date).ToString('o')
& copilot --model $model --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = $model
    sessionId = $session
    snapshot = '6c23db00d2d14ec6d0a3537a1ef72b273e3d55e7'
    evidenceHead = 'b37c5ad6ffb5ab62cf4525b50afe4e2a6cdd011b'
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
