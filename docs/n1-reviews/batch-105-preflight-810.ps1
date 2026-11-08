param(
    [string]$ReceiptName = 'preflight-810.json',
    [string]$ExpectedHead = '27e252daa091e21c907ff6799818f6b2da74c7aa'
)
$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$session = '595bb5b4-8cc4-4f57-bcb1-4b31d3c6e957'
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 13320 -or $runner.sessionId -ne $session) { throw 'Uncertain runner ownership; preserve and yield' }
$chain = @()
$process = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while ($process -and $chain.Count -lt 12) {
    $chain += [ordered]@{pid=$process.ProcessId; parent=$process.ParentProcessId; name=$process.Name}
    if ($process.ProcessId -eq $runner.pid) { break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($process.ParentProcessId)"
}
if (-not $process -or $process.ProcessId -ne $runner.pid) { throw 'Live launcher ancestry missing' }
if ($process.CommandLine -notmatch '(?i)-EncodedCommand\s+(\S+)') { throw 'Expected encoded launcher' }
$decoded = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
if (-not $decoded.Contains("& $control\runner.ps1")) { throw 'Wrong decoded launcher' }
$hash = (Get-FileHash "$control\runner.ps1").Hash.ToLowerInvariant()
if ($hash -ne 'f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af') { throw 'Launcher changed' }
$coordinator = $chain | ForEach-Object { Get-CimInstance Win32_Process -Filter "ProcessId=$($_.pid)" } |
    Where-Object { $_.Name -eq 'copilot.exe' -and $_.CommandLine.Contains("--session-id $session") }
if (@($coordinator).Count -ne 1) { throw 'Wrong coordinator session' }
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
if ($progress.checkpoint -ne 809 -or $progress.status -ne 'continue' -or $progress.batch -ne '105') { throw 'Checkpoint changed' }
foreach ($spec in @(
    @("$control\..\learning-japanese", $ExpectedHead),
    @("$control\..\kanji-cards-android", 'bf30cdead8515739bc0e671d57a54b9a3109dd46')
)) {
    if ((git -C $spec[0] rev-parse HEAD) -ne $spec[1] -or $LASTEXITCODE -ne 0) { throw 'Unexpected head' }
    if ((git -C $spec[0] log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature not verified' }
    $changes = @(git -C $spec[0] status --porcelain --untracked-files=all)
    if ($LASTEXITCODE -ne 0) { throw 'Status failed' }
    if ($spec[1] -eq 'bf30cdead8515739bc0e671d57a54b9a3109dd46' -and $changes.Count) { throw 'Android not clean' }
    foreach ($line in $changes) {
        if (-not $line.Substring(3).StartsWith('docs/n1-reviews/batch-105-') -and
            $line.Substring(3) -ne 'docs/n1-sources/batch-105-progress.json') { throw 'Unaccounted worktree change' }
    }
}
if ((git -C "$control\..\learning-japanese" rev-parse origin/main) -ne '047c2cef6b6a48b1738f2c5957de01be481c63e1') { throw 'Main changed' }
$receipt = "$control\logs\$session\$ReceiptName"
if (Test-Path $receipt) { throw 'Do not overwrite preflight evidence' }
[ordered]@{
    execution=810; sessionId=$session; verifiedAt=[DateTimeOffset]::UtcNow.ToString('o')
    chain=$chain; liveParentPid=$process.ProcessId; coordinatorPid=$coordinator.ProcessId
    decodedLauncher=$decoded; launcherSha256=$hash; checkpoint=809
    contentHead=$ExpectedHead
    exactSignedHeadsVerified=$true
    worktreeCheck='Initially wholly clean; only accounted batch105 review evidence permitted thereafter; runtime and Android clean.'
    parentLockRole='Live parent launcher owns runner.lock; no child acquire/delete/unlock/read-probe.'
    lockTouched=$false
} | ConvertTo-Json -Depth 8 | Set-Content $receipt -Encoding utf8NoBOM
Write-Output 'Live launcher/session/signed heads and scoped clean state verified; parent lock untouched.'
