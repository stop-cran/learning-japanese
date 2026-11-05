param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Family)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = "batch-063-visual-$Family"
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Never overwrite original execution evidence' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne '6d616d75cb15a0d574e28545c89ef45e3bcd85cb') { throw 'Unexpected evidence HEAD' }
if (& git -C $root diff ddad655f71c06e7cb2c749de18596863a800a73d -- kanji words articles strokes manifest.json) { throw 'Teaching changed' }
$model = 'claude-opus-5.5'
$session = '80bc3198-c572-419d-b7a1-2df6ec8475c5'
if ($Family -eq 'gpt') {
    $prior = Get-Content (Join-Path $root 'docs\n1-reviews\batch-063-visual-claude-execution.json') -Raw | ConvertFrom-Json
    if ($prior.exitCode -ne 0 -or $prior.observedToolOverlaps.Count -ne 0 -or $prior.multiToolResponses.Count -ne 0) { throw 'First complete serial archive required' }
    $model = 'gpt-6.1-sol'
    $session = '65373d23-fce9-455e-a51f-5bd7c89b5d17'
}
$prompt = [IO.File]::ReadAllText((Join-Path $PSScriptRoot "$prefix-prompt.txt"))
$started = (Get-Date).ToString('o')
& copilot --model $model --session-id $session --prompt $prompt --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = $model
    sessionId = $session
    snapshot = 'ddad655f71c06e7cb2c749de18596863a800a73d'
    evidenceHead = '6d616d75cb15a0d574e28545c89ef45e3bcd85cb'
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
