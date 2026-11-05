param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Family, [switch]$SerialRepair)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = "batch-067-visual-$Family"
if ($SerialRepair) {
    if ($Family -ne 'claude') { throw 'Only the actual Claude two-text-read deviation is repair scope' }
    $prefix += '-serial-repair'
}
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Never overwrite original execution evidence' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne 'a6c57b57f7c90f5a9c78e5bdf953bd2df768d5ed') { throw 'Unexpected evidence HEAD' }
if (& git -C $root diff 5cb2ea4bc804ac218b17d5c583d4fba95e60971c -- kanji words articles strokes manifest.json) { throw 'Teaching changed' }
$processes = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'copilot.exe' })
$processes | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Depth 3 | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-preflight.json")
if ($processes | Where-Object { $_.CommandLine -match '0d237a1b-fdf8-4ea8-8c5d-03aa6a6d86a0|ab7f642d-37b9-4069-8a9c-4fc5e6bc071a' }) { throw 'Original reviewer session already active' }
$model = 'claude-opus-5.5'
$session = '0d237a1b-fdf8-4ea8-8c5d-03aa6a6d86a0'
if ($Family -eq 'gpt') {
    $prior = Get-Content (Join-Path $root 'docs\n1-reviews\batch-067-visual-claude-execution.json') -Raw | ConvertFrom-Json
    $repair = Get-Content (Join-Path $root 'docs\n1-reviews\batch-067-visual-claude-serial-repair-execution.json') -Raw | ConvertFrom-Json
    if ($prior.exitCode -ne 0 -or $prior.missingRequiredText.Count -ne 0 -or $prior.imagePayloadsVerified -ne 23 -or -not $repair.serialRepairAccepted) { throw 'First complete archive and exact bounded serial repair required' }
    $model = 'gpt-6.1-sol'
    $session = 'ab7f642d-37b9-4069-8a9c-4fc5e6bc071a'
}
$prompt = [IO.File]::ReadAllText((Join-Path $PSScriptRoot "$prefix-prompt.txt"))
$started = (Get-Date).ToString('o')
& copilot --model $model --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = $model
    sessionId = $session
    snapshot = '5cb2ea4bc804ac218b17d5c583d4fba95e60971c'
    evidenceHead = 'a6c57b57f7c90f5a9c78e5bdf953bd2df768d5ed'
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
