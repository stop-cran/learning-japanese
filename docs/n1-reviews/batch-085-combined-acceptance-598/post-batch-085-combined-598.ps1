$ErrorActionPreference = 'Stop'
$c = $PSScriptRoot
$r = Join-Path (Split-Path $c -Parent) 'learning-japanese'
$a = Join-Path (Split-Path $c -Parent) 'kanji-cards-android'
$logs = "$c\logs\4e19ca44-0f2d-4721-996a-8f32a6f5d943"
if ((git -C $r rev-parse 'HEAD^').Trim() -ne '40eb5dcee006ef142721fcd9c9e923c616f6a89e' -or
    (git -C $r log -1 '--format=%G?').Trim() -ne 'G' -or (git -C $r status --porcelain)) {
    throw 'Content checkpoint is not the expected normally signed, wholly clean child.'
}
if ((git -C $a rev-parse HEAD).Trim() -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $a log -1 '--format=%G?').Trim() -ne 'G' -or (git -C $a status --porcelain)) {
    throw 'Dedicated Android state changed.'
}
$p = Get-Content "$c\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 597 -or $p.batch -ne '085' -or
    $p.stage -ne 'batch-085-combined-main-integration-in-progress') { throw 'Checkpoint context changed.' }
$runner = Get-Content "$c\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 19008 -or
    $runner.sessionId -ne '4e19ca44-0f2d-4721-996a-8f32a6f5d943') { throw 'Launcher context changed.' }
$ancestor = $PID
$owned = $false
while ($ancestor -gt 0) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if ($null -eq $process) { break }
    if ($ancestor -eq $runner.pid) { $owned = $true; break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Expected live launcher is not an ancestor; preserve/yield without lock access.' }
$body = [IO.File]::ReadAllText("$logs\issue-body-598.txt", [Text.Encoding]::UTF8)
$head = (git -C $r rev-parse HEAD).Trim()
$body += "`nNormally signed LOCAL evidence checkpoint: $head.`n"
$payload = "$logs\issue-payload-598.json"
if (Test-Path $payload) { throw 'Preserve existing issue attempt; do not repost blindly.' }
[IO.File]::WriteAllText("$logs\issue-body-598.txt", $body, [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText($payload, (@{body=$body} | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable.' }
    $login = (gh api user --jq .login).Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Owner identity mismatch.' }
    $posted = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payload
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed; preserve attempt and yield.' }
    [IO.File]::WriteAllText("$logs\issue-posted-598.json", ($posted -join "`n"), [Text.UTF8Encoding]::new($false))
    $comment = ($posted -join "`n") | ConvertFrom-Json
    $verified = gh api "repos/stop-cran/learning-japanese/issues/comments/$($comment.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue receipt retrieval failed.' }
    $receipt = ($verified -join "`n") | ConvertFrom-Json
    if ($receipt.user.login -ne 'stop-cran' -or $receipt.body -cne $body) {
        throw 'Issue author/body mismatch.'
    }
    [IO.File]::WriteAllText("$logs\issue-verified-598.json", ($verified -join "`n"), [Text.UTF8Encoding]::new($false))
    Write-Output $receipt.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
