$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$session = '7bdaadbe-a18f-4f7d-b635-8b2dc0c28c39'
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 19008 -or $runner.sessionId -ne $session) {
    throw 'Uncertain runner ownership; preserve and yield.'
}
$ancestry = @()
$process = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while ($process -and $ancestry.Count -lt 12) {
    $ancestry += $process.ProcessId
    if ($process.ProcessId -eq $runner.pid) { break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($process.ParentProcessId)"
}
if (-not $process -or $process.ProcessId -ne $runner.pid) { throw 'Live parent missing from ancestry.' }
if ($process.CommandLine -notmatch '(?i)-EncodedCommand\s+(\S+)') { throw 'Unexpected launcher command.' }
$decoded = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
if (-not $decoded.Contains("& $control\runner.ps1")) { throw 'Wrong decoded launcher.' }
$hash = (Get-FileHash "$control\runner.ps1" -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne 'f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af') { throw 'Launcher changed.' }
$lockContract = Get-Content "$control\runner.ps1" -Raw
if (-not $lockContract.Contains("[IO.File]::Open((Join-Path `$control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')") -or
    -not $lockContract.Contains('$lock.Dispose()')) {
    throw 'Expected parent lock contract not found.'
}
[ordered]@{
    execution=698; sessionId=$session; verifiedAt=[DateTimeOffset]::Now.ToString('o')
    ancestry=$ancestry; liveParentPid=$process.ProcessId; decodedLauncherMatches=$true
    launcherSha256=$hash; lockTouched=$false
    parentLockRole='Live launcher retains exclusive lock throughout child lifetime; no child lock operation.'
} | ConvertTo-Json -Depth 8 | Set-Content "$control\logs\$session\preflight-698.json" -Encoding utf8NoBOM
Write-Output 'Live launcher ancestry verified; parent lock untouched.'
