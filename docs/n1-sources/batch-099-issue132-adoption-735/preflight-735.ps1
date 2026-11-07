$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$session = 'fc7ebb05-a8bf-4501-9314-c7759000faa7'
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne $session -or $runner.pid -ne 28480) { throw 'Uncertain runner ownership' }
$ancestry = @()
$process = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while ($process -and $ancestry.Count -lt 12) {
    $ancestry += $process.ProcessId
    if ($process.ProcessId -eq $runner.pid) { break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($process.ParentProcessId)"
}
if (-not $process -or $process.ProcessId -ne $runner.pid) { throw 'Live launcher missing from ancestry' }
if ($process.CommandLine -notmatch '(?i)-EncodedCommand\s+(\S+)') { throw 'Expected encoded launcher' }
$decoded = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
if (-not $decoded.Contains("& $control\runner.ps1")) { throw 'Wrong decoded launcher' }
$hash = (Get-FileHash "$control\runner.ps1").Hash.ToLowerInvariant()
if ($hash -ne 'f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af') { throw 'Launcher changed' }
$coordinator = $ancestry | ForEach-Object {
    Get-CimInstance Win32_Process -Filter "ProcessId=$_"
} | Where-Object { $_.Name -eq 'copilot.exe' -and $_.CommandLine.Contains("--session-id $session") }
if (-not $coordinator) { throw 'Wrong coordinator session' }
$progress = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($progress.checkpoint -ne 734 -or $progress.batch -ne '099') { throw 'Checkpoint changed' }
foreach ($spec in @(
    @("$control\..\learning-japanese", '309189fcda2723ddcf652a9ae5cba7c807d24872'),
    @("$control\..\kanji-cards-android", 'bf30cdead8515739bc0e671d57a54b9a3109dd46')
)) {
    if ((git -C $spec[0] rev-parse HEAD) -ne $spec[1]) { throw 'Unexpected head' }
    if ((git -C $spec[0] log -1 '--format=%G?') -ne 'G') { throw 'Signature not verified' }
    if (git -C $spec[0] status --porcelain) { throw 'Worktree not wholly clean' }
}
[ordered]@{
    execution = 735
    sessionId = $session
    verifiedAt = [DateTimeOffset]::Now.ToString('o')
    ancestry = $ancestry
    liveParentPid = $process.ProcessId
    decodedLauncherMatches = $true
    launcherSha256 = $hash
    checkpoint = 734
    dedicatedWorktreesClean = $true
    exactSignedHeadsVerified = $true
    lockTouched = $false
    parentLockRole = 'Live parent launcher owns runner.lock; no child acquire/delete/unlock/read-probe.'
} | ConvertTo-Json -Depth 8 | Set-Content "$control\logs\$session\preflight-735.json" -Encoding utf8NoBOM
Write-Output 'Live launcher, checkpoint and clean signed heads verified without touching parent lock.'
