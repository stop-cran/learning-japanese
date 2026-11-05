param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Family)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$head = 'da3a602a8eaf12190c7baf4048d02d86fe20a048'
$snapshot = '38ab6072d2041325142c54cf54be5d126928eb31'
$prefix = "batch-062-visual-$Family"
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if (Test-Path (Join-Path $PSScriptRoot "$prefix.jsonl")) { throw 'Never overwrite original execution' }
if ((& git -C $root rev-parse HEAD) -ne $head) { throw 'Unexpected evidence HEAD' }
if (& git -C $root diff $snapshot -- kanji words articles strokes manifest.json) { throw 'Teaching changed' }
$sessions = @('1d12b838-18c9-407a-b065-fc6e8fe44480','38b783dc-e2cf-4226-8786-e207effbde13')
$active = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -like '*copilot*' -and $_.CommandLine -and
    ($_.CommandLine.Contains($sessions[0]) -or $_.CommandLine.Contains($sessions[1]))
})
if ($active.Count) { throw "Original reviewer process already active: $($active.ProcessId -join ',')" }
if ($Family -eq 'gpt') {
    $prior = Get-Content -Raw (Join-Path $root 'docs\n1-reviews\batch-062-visual-claude-execution.json') | ConvertFrom-Json
    if ($prior.exitCode -ne 0 -or -not $prior.processAndCoverageAccepted) { throw 'First exit/archive/audit required before second launch' }
}
$model = if ($Family -eq 'claude') { 'claude-opus-5.5' } else { 'gpt-6.1-sol' }
$session = if ($Family -eq 'claude') { $sessions[0] } else { $sessions[1] }
$prompt = @"
Reuse original $Family reviewer session $session for SAME062 dependent visual confirmation only.
Read the complete shared task with view at:
$PSScriptRoot\batch-062-visual-task.txt
Read YOUR complete original report with view at:
$root\docs\n1-reviews\batch-062-initial-$Family.md
Follow shared task exactly: only serial view, ONE tool call per response and await result.
No other reviewer's report, shell, search, editing, delegation, parallel tool wrapper or task_complete.
Read every assigned text range and each of17distinct PNGs. Return complete report and exit.
"@
if ($Family -eq 'claude') {
    $prompt += "`nAlso read YOUR complete own dependent turn2 report: $root\docs\n1-reviews\batch-062-dependent-claude-turn-2.md"
}
$promptPath = Join-Path $PSScriptRoot "$prefix-prompt.txt"
[IO.File]::WriteAllText($promptPath, $prompt)
$started = (Get-Date).ToString('o')
& copilot --model $model --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> (Join-Path $PSScriptRoot "$prefix.jsonl") 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = $model
    sessionId = $session
    snapshot = $snapshot
    evidenceHead = $head
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
python -B (Join-Path $PSScriptRoot 'archive-execution-387-visual.py') $Family
if ($LASTEXITCODE -ne 0 -or $code -ne 0) { throw 'Reviewer failed or archival/process audit failed; preserve exact evidence' }
