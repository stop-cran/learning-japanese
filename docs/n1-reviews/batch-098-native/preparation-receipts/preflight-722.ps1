$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$session = '9b6504c7-7546-4384-b402-c83f56ee5497'
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 19008 -or $runner.sessionId -ne $session) { throw 'Uncertain runner ownership' }
$ancestry = @()
$process = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while ($process -and $ancestry.Count -lt 12) {
    $ancestry += $process.ProcessId
    if ($process.ProcessId -eq $runner.pid) { break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($process.ParentProcessId)"
}
if (-not $process -or $process.ProcessId -ne $runner.pid) { throw 'Expected live parent missing from ancestry' }
if ($process.CommandLine -notmatch '(?i)-EncodedCommand\s+(\S+)') { throw 'Expected encoded launcher' }
$decoded = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
if (-not $decoded.Contains("& $control\runner.ps1")) { throw 'Wrong decoded launcher' }
$hash = (Get-FileHash "$control\runner.ps1" -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hash -ne 'f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af') { throw 'Launcher changed' }
if (-not (@($ancestry | ForEach-Object {
    (Get-CimInstance Win32_Process -Filter "ProcessId=$_").CommandLine
}) | Where-Object { $_ -like "*--session-id $session*" })) { throw 'Wrong coordinator session' }
[ordered]@{
    execution=722; sessionId=$session; verifiedAt=[DateTimeOffset]::Now.ToString('o')
    ancestry=$ancestry; liveParentPid=$process.ProcessId; decodedLauncherMatches=$true
    launcherSha256=$hash; lockTouched=$false
    parentLockRole='Live parent launcher owns runner.lock throughout child lifetime; no child acquire/delete/unlock/read-probe.'
} | ConvertTo-Json -Depth 8 | Set-Content "$control\logs\$session\preflight-722.json" -Encoding utf8NoBOM
Write-Output 'Live launcher ancestry verified without touching parent lock.'
