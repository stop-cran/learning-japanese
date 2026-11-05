param([Parameter(Mandatory=$true)][ValidateSet('claude','gpt')][string]$Family)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = "batch-064-visual-411-$Family"
$head = '976b825f0d32d1074c63c6f7b71388daa9da81a9'
if (Test-Path (Join-Path $PSScriptRoot "$prefix.jsonl")) { throw 'Never overwrite evidence' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne $head) { throw 'Evidence HEAD changed' }
if (& git -C $root diff ff6eb7893344b806bf517ebd41bf19089bed5021 -- kanji words articles strokes manifest.json) { throw 'Teaching changed' }
$model = 'claude-opus-5.5'
$session = '28a561c9-9201-40a9-a3a1-c9e37c6d168a'
if ($Family -eq 'gpt') {
    $prior = Get-Content (Join-Path $root 'docs\n1-reviews\batch-064-visual-411-claude-execution.json') -Raw | ConvertFrom-Json
    if (-not $prior.processAndCoverageAccepted -or $prior.exitCode -ne 0) { throw 'First complete serial archive required' }
    $model = 'gpt-6.1-sol'
    $session = '1d30e91b-c5ed-4bd0-8d74-2177b9fbb0d7'
}
$active = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -like '*copilot*--model*--session-id*' }
if ($active) { throw 'Existing headless reviewer' }
$prompt = [IO.File]::ReadAllText((Join-Path $PSScriptRoot "$prefix-prompt.txt"))
$started = (Get-Date).ToString('o')
Set-Location $root
& copilot --model $model --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> (Join-Path $PSScriptRoot "$prefix.jsonl") 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel=$model; sessionId=$session; exitCode=$code; launcherPid=$PID
    snapshot='ff6eb7893344b806bf517ebd41bf19089bed5021'; evidenceHead=$head
    approvedDirectory=$PSScriptRoot; availableTools=@('view'); cwd=$root
    startedAt=$started; completedAt=(Get-Date).ToString('o')
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix exited $code"
exit $code
