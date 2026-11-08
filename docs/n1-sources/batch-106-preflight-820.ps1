$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$session = '1f17514d-4832-4b04-bbfe-7aac0c6241c0'
$head = '95227f2ab8846a80061d6de27b1701fe19053161'
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
if ($progress.checkpoint -ne 819 -or $progress.status -ne 'continue' -or $progress.batch -ne '106') {
    throw 'Checkpoint changed'
}
foreach ($spec in @(
    @("$control\..\learning-japanese", $head),
    @("$control\..\kanji-cards-android", 'bf30cdead8515739bc0e671d57a54b9a3109dd46')
)) {
    if ((git -C $spec[0] rev-parse HEAD) -ne $spec[1] -or $LASTEXITCODE -ne 0) { throw 'Unexpected head' }
    if ((git -C $spec[0] log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature not verified' }
    if ((git -C $spec[0] status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) {
        throw 'Worktree not wholly clean'
    }
}
git -C "$control\..\learning-japanese" fetch --quiet origin main
if ($LASTEXITCODE -ne 0) { throw 'Fresh main fetch failed' }
$main = git -C "$control\..\learning-japanese" rev-parse origin/main
if ($LASTEXITCODE -ne 0 -or $main -ne '0c582f18b31f65a5e1a908d92e37dde3d34f81ee') {
    throw 'Main advanced; reconcile before source completion'
}
$receipt = "$control\logs\$session\preflight-820.json"
if (Test-Path $receipt) { throw 'Do not overwrite evidence' }
[ordered]@{
    execution=820; sessionId=$session; verifiedAt=[DateTimeOffset]::UtcNow.ToString('o')
    ancestry=$ancestry; liveParentPid=$process.ProcessId; coordinatorPid=$coordinator.ProcessId
    decodedLauncherMatches=$true; launcherSha256=$hash; checkpoint=819
    contentHead=$head; freshOriginMain=$main; dedicatedWorktreesClean=$true
    exactSignedHeadsVerified=$true; androidHead='bf30cdead8515739bc0e671d57a54b9a3109dd46'
    parentLockRole='Live parent launcher owns runner.lock; no child acquire/delete/unlock/read-probe.'
    lockTouched=$false
} | ConvertTo-Json -Depth 8 | Set-Content $receipt -Encoding utf8NoBOM
Write-Output 'Live launcher/session/clean signed heads/fresh main verified; parent lock untouched.'
