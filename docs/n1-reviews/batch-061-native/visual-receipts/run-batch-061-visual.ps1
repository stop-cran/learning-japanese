param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Label)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$snapshot = 'f2267727d982589890b2f4ae0b17e82666337956'
$session = if ($Label -eq 'claude') { '537a357b-564b-433a-897c-1285b08defb2' } else { '89aec53d-9f60-44ad-9cd7-f859fe24d8fd' }
$model = if ($Label -eq 'claude') { 'claude-opus-5.5' } else { 'gpt-6.1-sol' }
$prefix = "batch-061-visual-$Label"
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Refusing to overwrite original visual execution' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne $snapshot) { throw 'Unexpected snapshot' }
if (& git -C $root status --porcelain -- kanji words articles strokes manifest.json) { throw 'Frozen teaching must be clean' }
if ($Label -eq 'gpt') {
    $previous = Get-Content -Raw (Join-Path $PSScriptRoot 'batch-061-visual-claude-process.json') | ConvertFrom-Json
    if ($previous.exitCode -ne 0) { throw 'Claude must exit successfully first' }
    if (Get-Process -Id $previous.launcherPid -ErrorAction SilentlyContinue) { throw 'Previous launcher still active' }
    $audit = Get-Content -Raw (Join-Path $root 'docs\n1-reviews\batch-061-visual-claude-execution.json') | ConvertFrom-Json
    if ($audit.unfinishedTools.Count) { throw 'Unfinished Claude calls' }
    if (-not $audit.expectedPngMembershipReturned -or $audit.imagePayloadsVerified -ne 20) { throw 'Claude visual coverage incomplete' }
    foreach ($turn in @('glyph','selection')) {
        $receipt = Get-Content -Raw (Join-Path $root "docs\n1-reviews\batch-061-visual-claude-$turn-execution.json") | ConvertFrom-Json
        if ($receipt.exitCode -ne 0 -or $receipt.observedToolOverlaps.Count -or $receipt.multiToolResponses.Count -or $receipt.toolCalls.Count -ne 1 -or $receipt.imagePayloadsVerified -ne 1) { throw 'Single-image Claude remediation incomplete' }
        if (Get-Process -Id $receipt.launcherPid -ErrorAction SilentlyContinue) { throw 'Claude remediation still active' }
    }
}
$followup = if ($Label -eq 'claude') { "YOUR latest confirmation is $root\docs\n1-reviews\batch-061-dependent-claude-turn-4.md." } else { 'Your original report is the latest textual review; no separate confirmation is required.' }
$started = (Get-Date).ToString('o')
$prompt = "You are ORIGINAL $model in session $session. Read the ENTIRE bounded shared visual task at $PSScriptRoot\batch-061-visual-task.txt and execute read-only. YOUR original report is $root\docs\n1-reviews\batch-061-initial-$Label.md. $followup Exactly ONE view call per response, await completion, NEVER parallelize even text reads. Return complete FINAL report."
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
