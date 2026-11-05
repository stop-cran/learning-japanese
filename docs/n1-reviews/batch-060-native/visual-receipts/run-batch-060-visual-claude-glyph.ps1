$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = 'batch-060-visual-claude-glyph'
$snapshot = '8f9bad077f40cac9a31523a27d192accc59dcd0d'
$session = '34dbb43d-2a7f-4fa9-9e45-00c50c1281a1'
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Refusing to overwrite original clarification' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne $snapshot) { throw 'Unexpected snapshot' }
$previous = Get-Content -Raw (Join-Path $PSScriptRoot 'batch-060-visual-gpt-process.json') | ConvertFrom-Json
if ($previous.exitCode -ne 0) { throw 'Previous reviewer must exit successfully' }
if (Get-Process -Id $previous.launcherPid -ErrorAction SilentlyContinue) { throw 'Previous reviewer still active' }
if (-not (Test-Path (Join-Path $root 'docs\n1-reviews\batch-060-visual-gpt-execution.json'))) { throw 'Archive previous reviewer first' }
$prompt = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'batch-060-visual-claude-glyph-task.txt'))
$started = (Get-Date).ToString('o')
& copilot --model claude-opus-5.5 --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = 'claude-opus-5.5'
    sessionId = $session
    snapshot = $snapshot
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
