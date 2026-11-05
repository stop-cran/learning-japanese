$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = 'batch-057-visual-claude-clarification'
$session = '9afffb68-5649-4bf8-9dd7-c4a39170c20c'
$snapshot = '4d460d10add0b9c88d6514837e2806b1d9946c3a'
if (Test-Path (Join-Path $PSScriptRoot "$prefix.jsonl")) { throw 'Refusing to overwrite original clarification' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
if ((& git -C $root rev-parse HEAD) -ne $snapshot) { throw 'Unexpected snapshot' }
if (& git -C $root status --porcelain -- kanji words articles strokes manifest.json) { throw 'Frozen teaching must be clean' }
$previous = Get-Content -Raw (Join-Path $PSScriptRoot 'batch-057-visual-gpt-process.json') | ConvertFrom-Json
if ($previous.exitCode -ne 0) { throw 'GPT must exit first' }
if (Get-Process -Id $previous.launcherPid -ErrorAction SilentlyContinue) { throw 'Previous launcher still active' }
if (-not (Test-Path (Join-Path $root 'docs\n1-reviews\batch-057-visual-gpt.md'))) { throw 'Archive GPT report first' }
$started = (Get-Date).ToString('o')
$prompt = "ORIGINAL claude-opus-5.5 session $session. Read the COMPLETE task $PSScriptRoot\batch-057-visual-claude-clarification-task.txt in ONE view call, then follow its exact TWO additional image reads, ONE call per response, no parallel calls. Return bounded final report; no other tools."
& copilot --model claude-opus-5.5 --session-id $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> (Join-Path $PSScriptRoot "$prefix.jsonl") 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
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
