param([string]$ReceiptName = 'preflight-822.json', [switch]$EvidenceOnly)
$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$session = '4656604b-eebf-4190-bcb5-d2e6ae5ddd3e'
$head = '5fe224b5c611e8ca0c7c5a1fcbd5ea4a025e606a'
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 13320 -or $runner.sessionId -ne $session) {
    throw 'Uncertain runner ownership; preserve and yield'
}
$ancestry = @()
$process = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while ($process -and $ancestry.Count -lt 12) {
    $ancestry += $process.ProcessId
    if ($process.ProcessId -eq $runner.pid) { break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($process.ParentProcessId)"
}
if (-not $process -or $process.ProcessId -ne $runner.pid) { throw 'Live launcher ancestry missing' }
if ($process.CommandLine -notmatch '(?i)-EncodedCommand\s+(\S+)') { throw 'Expected encoded launcher' }
$decoded = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
if (-not $decoded.Contains("& $control\runner.ps1")) { throw 'Wrong decoded launcher' }
$hash = (Get-FileHash "$control\runner.ps1").Hash.ToLowerInvariant()
if ($hash -ne 'f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af') {
    throw 'Launcher changed'
}
$coordinator = $ancestry | ForEach-Object { Get-CimInstance Win32_Process -Filter "ProcessId=$_" } |
    Where-Object { $_.Name -eq 'copilot.exe' -and $_.CommandLine.Contains("--session-id $session") }
if (@($coordinator).Count -ne 1) { throw 'Wrong coordinator session' }
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
if ($progress.checkpoint -ne 821 -or $progress.status -ne 'continue' -or $progress.batch -ne '106') {
    throw 'Checkpoint changed'
}
foreach ($spec in @(
    @("$control\..\learning-japanese", $head),
    @("$control\..\kanji-cards-android", 'bf30cdead8515739bc0e671d57a54b9a3109dd46')
)) {
    if ((git -C $spec[0] rev-parse HEAD) -ne $spec[1] -or $LASTEXITCODE -ne 0) { throw 'Unexpected head' }
    if ((git -C $spec[0] log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature not verified' }
    $changes = @(git -C $spec[0] status --porcelain --untracked-files=all)
    if ($LASTEXITCODE -ne 0) { throw 'Status failed' }
    if ($EvidenceOnly -and $spec[1] -eq $head) {
        if (@($changes | Where-Object {
            $_.Substring(3) -notmatch '^docs/n1-reviews/batch-106-' -and
            $_.Substring(3) -ne 'docs/n1-sources/batch-106-progress.json'
        }).Count) {
            throw 'Unexpected worktree changes'
        }
    } elseif ($changes.Count) { throw 'Worktree not wholly clean' }
}
git -C "$control\..\learning-japanese" fetch --quiet origin main
if ($LASTEXITCODE -ne 0) { throw 'Fresh main fetch failed' }
$main = git -C "$control\..\learning-japanese" rev-parse origin/main
if ($LASTEXITCODE -ne 0 -or $main -ne '0c582f18b31f65a5e1a908d92e37dde3d34f81ee') {
    throw 'Main advanced; preserve and reconcile'
}
$receipt = "$control\logs\$session\$ReceiptName"
if (Test-Path $receipt) { throw 'Do not overwrite evidence' }
[ordered]@{
    execution=822; sessionId=$session; verifiedAt=[DateTimeOffset]::UtcNow.ToString('o')
    ancestry=$ancestry; liveParentPid=$process.ProcessId; coordinatorPid=$coordinator.ProcessId
    decodedLauncherMatches=$true; launcherSha256=$hash; checkpoint=821
    contentHead=$head; freshOriginMain=$main; initiallyWhollyClean=(-not $EvidenceOnly)
    exactSignedHeadsVerified=$true; androidHead='bf30cdead8515739bc0e671d57a54b9a3109dd46'
    parentLockRole='Live parent launcher owns runner.lock; no child acquire/delete/unlock/read-probe.'
    lockTouched=$false
} | ConvertTo-Json -Depth 8 | Set-Content $receipt -Encoding utf8NoBOM
Write-Output 'Live launcher/session/signed heads/fresh main verified; parent lock untouched.'
