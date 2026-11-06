$ErrorActionPreference = 'Stop'
$c = $PSScriptRoot
$r = Join-Path (Split-Path $c -Parent) 'learning-japanese'
$a = Join-Path (Split-Path $c -Parent) 'kanji-cards-android'
$logs = "$c\logs\ed3499c0-6a0d-4ef9-82b6-fa2f03f3c1a9"
if ((git -C $r rev-parse 'HEAD^').Trim() -ne 'f23dae44b7c044087f1fe7d31176c4c1534f6e94' -or
    (git -C $r log -1 '--format=%G?').Trim() -ne 'G' -or (git -C $r status --porcelain)) {
    throw 'Content checkpoint is not the expected normally signed, wholly clean child.'
}
if ((git -C $a rev-parse HEAD).Trim() -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $a log -1 '--format=%G?').Trim() -ne 'G' -or (git -C $a status --porcelain)) {
    throw 'Dedicated Android state changed.'
}
$p = Get-Content "$c\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 606 -or $p.batch -ne '086' -or
    $p.stage -ne 'batch-086-combined-main-integration-in-progress') { throw 'Checkpoint context changed.' }
$runner = Get-Content "$c\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 19008 -or
    $runner.sessionId -ne 'ed3499c0-6a0d-4ef9-82b6-fa2f03f3c1a9') { throw 'Launcher context changed.' }
$ancestor = $PID
$owned = $false
while ($ancestor -gt 0) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if ($null -eq $process) { break }
    if ($ancestor -eq $runner.pid) { $owned = $true; break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Expected live launcher is not an ancestor; preserve/yield without lock access.' }
$body = [IO.File]::ReadAllText("$logs\issue-body-607.txt", [Text.Encoding]::UTF8)
$head = (git -C $r rev-parse HEAD).Trim()
$body += "`nNormally signed LOCAL evidence checkpoint: $head.`n"
$payload = "$logs\issue-payload-607.json"
if (Test-Path $payload) { throw 'Preserve existing issue attempt; do not repost blindly.' }
[IO.File]::WriteAllText("$logs\issue-body-607.txt", $body, [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText($payload, (@{body=$body} | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable.' }
    $login = (gh api user --jq .login).Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Owner identity mismatch.' }
    $posted = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payload
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed; preserve attempt and yield.' }
    [IO.File]::WriteAllText("$logs\issue-posted-607.json", ($posted -join "`n"), [Text.UTF8Encoding]::new($false))
    $comment = ($posted -join "`n") | ConvertFrom-Json
    $verified = gh api "repos/stop-cran/learning-japanese/issues/comments/$($comment.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue receipt retrieval failed.' }
    $receipt = ($verified -join "`n") | ConvertFrom-Json
    if ($receipt.user.login -ne 'stop-cran' -or $receipt.body -cne $body) { throw 'Issue author/body mismatch.' }
    [IO.File]::WriteAllText("$logs\issue-verified-607.json", ($verified -join "`n"), [Text.UTF8Encoding]::new($false))
    Write-Output $receipt.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
