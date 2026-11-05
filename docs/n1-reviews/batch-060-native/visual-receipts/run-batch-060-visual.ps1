param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Label)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$snapshot = '8f9bad077f40cac9a31523a27d192accc59dcd0d'
$session = if ($Label -eq 'claude') { '34dbb43d-2a7f-4fa9-9e45-00c50c1281a1' } else { '8130aa10-a2af-44b9-80ca-28fb1662eb6c' }
$model = if ($Label -eq 'claude') { 'claude-opus-5.5' } else { 'gpt-6.1-sol' }
$prefix = "batch-060-visual-$Label"
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Refusing to overwrite original visual execution' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne $snapshot) { throw 'Unexpected snapshot' }
if (& git -C $root status --porcelain -- kanji words articles strokes manifest.json) { throw 'Frozen teaching must be clean' }
if ($Label -eq 'gpt') {
    $previous = Get-Content -Raw (Join-Path $PSScriptRoot 'batch-060-visual-claude-process.json') | ConvertFrom-Json
    if ($previous.exitCode -ne 0) { throw 'Claude must exit successfully first' }
    if (Get-Process -Id $previous.launcherPid -ErrorAction SilentlyContinue) { throw 'Previous launcher still active' }
    if (-not (Test-Path (Join-Path $root 'docs\n1-reviews\batch-060-visual-claude-execution.json'))) { throw 'Archive Claude report and execution first' }
}
$followup = if ($Label -eq 'claude') { "YOUR latest confirmation is $root\docs\n1-reviews\batch-060-supervised-lexical-2.md." } else { 'Your original report is the latest textual review; no separate confirmation is required.' }
$started = (Get-Date).ToString('o')
$prompt = "You are ORIGINAL $model in session $session. Read the ENTIRE bounded shared visual task at $PSScriptRoot\batch-060-visual-task.txt and execute read-only. YOUR original report is $root\docs\n1-reviews\batch-060-initial-$Label.md. $followup Exactly ONE view call per response, await completion, NEVER parallelize even text reads. Return complete FINAL report."
& copilot --model $model --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = $model
    sessionId = $session
    snapshot = $snapshot
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
