$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$snapshot = 'f4e7d506c9f6cdacd1d1a406eebe891fe283ac87'
$session = '54bc51a8-88e8-4869-98bc-2db0fc6cb7cb'
$prefix = 'batch-043-visual-claude'
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Refusing to overwrite original visual execution' }
if ($env:GH_TOKEN) { throw 'Reviewer must not inherit owner GH_TOKEN' }
if ((& git -C $root rev-parse HEAD) -ne $snapshot) { throw 'Unexpected snapshot' }
if (& git -C $root status --porcelain -- kanji words articles strokes manifest.json) { throw 'Teaching must remain frozen' }
$started = (Get-Date).ToString('o')
$prompt = "Read the entire bounded visual task at $PSScriptRoot\batch-043-visual-prompt.txt and execute read-only. Strictly ONE tool call per response, await completion, never parallelize even text reads. Return complete report in final answer."
& copilot --model claude-opus-5.5 --resume $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view glob rg web_fetch --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
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
