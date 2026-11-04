param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Label)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$snapshot = '73593c32886b12443c6da65b9b6c2e393ba01ace'
$session = if ($Label -eq 'claude') { '1bed2f69-6d63-4a81-91f7-05f664ff3030' } else { '572484bf-b4d8-4206-94b6-d046f9157dc7' }
$model = if ($Label -eq 'claude') { 'claude-opus-5.5' } else { 'gpt-6.1-sol' }
$prefix = "batch-054-visual-$Label"
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Refusing to overwrite original visual execution' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne $snapshot) { throw 'Unexpected snapshot' }
if (& git -C $root status --porcelain -- kanji words articles strokes manifest.json) { throw 'Frozen teaching must be clean' }
if ($Label -eq 'gpt') {
    $previous = Get-Content -Raw (Join-Path $PSScriptRoot 'batch-054-visual-claude-process.json') | ConvertFrom-Json
    if ($previous.exitCode -ne 0) { throw 'Claude must exit successfully first' }
    if (Get-Process -Id $previous.launcherPid -ErrorAction SilentlyContinue) { throw 'Previous launcher still active' }
    if (-not (Test-Path (Join-Path $root 'docs\n1-reviews\batch-054-visual-claude.md'))) { throw 'Archive Claude report first' }
}
$started = (Get-Date).ToString('o')
$prompt = "Read the entire bounded visual task at $PSScriptRoot\$prefix-prompt.txt and execute read-only. Strictly ONE tool call per response, await completion, never parallelize even text reads. Return complete report in final answer."
& copilot --model $model --resume $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
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
