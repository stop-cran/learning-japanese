param(
    [string]$ReceiptName = 'preflight-844.json',
    [string]$ExpectedContentHead = 'dfed2c150d7fe921aacdb1d616ff527df1935f3b',
    [switch]$Draft
)
$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$session = '70ed1fca-b2a0-4267-bff3-7b7e4362d9ea'
$content = "$control\..\rollout-recovered\learning-japanese"
$android = "$control\..\rollout-recovered\kanji-cards-android"
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 31724 -or $runner.sessionId -ne $session) {
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
if ($process.Name -ne 'pwsh.exe' -or
    $process.CommandLine -notmatch (' -NoLogo -NoProfile -File ' + [regex]::Escape("$control\runner.ps1") + '$')) {
    throw 'Wrong recovered launcher command'
}
$hash = (Get-FileHash "$control\runner.ps1").Hash.ToLowerInvariant()
if ($hash -ne '81b1f0021403fe7e5e3d6da9d7a03e5565621975e3a4f99db4e84873d5c3a45c') {
    throw 'Launcher changed'
}
$coordinator = $ancestry | ForEach-Object { Get-CimInstance Win32_Process -Filter "ProcessId=$_" } |
    Where-Object { $_.Name -eq 'copilot.exe' -and $_.CommandLine.Contains("--session-id $session") }
if (@($coordinator).Count -ne 1) { throw 'Wrong coordinator session' }
if ($env:COPILOT_ALLOW_ALL) { throw 'Coordinator approval leaked into child shell' }
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
if ($progress.checkpoint -ne 843 -or $progress.status -ne 'continue' -or
    $progress.batch -ne '107' -or $progress.remainingAdditions -ne 1095 -or
    $progress.lastPublishedCommit -ne '476f429108415d00f9d41863af9d2f9470b5bbc0') {
    throw 'Checkpoint changed'
}
if (-not $progress.execution792HistoryCorrection.ownerReportCorrection.StartsWith('https://github.com/')) {
    throw '792 correction owner report missing'
}
foreach ($spec in @(
    @($content, $ExpectedContentHead),
    @($android, 'bf30cdead8515739bc0e671d57a54b9a3109dd46')
)) {
    if ((git -C $spec[0] rev-parse HEAD) -ne $spec[1] -or $LASTEXITCODE -ne 0) { throw 'Unexpected head' }
    if ((git -C $spec[0] log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature not verified' }
    $changes = @(git -c core.quotepath=false -C $spec[0] status --porcelain --untracked-files=all)
    if ($LASTEXITCODE -ne 0) { throw 'Status failed' }
    if ($Draft -and $spec[0] -eq $content) {
        $allowed = @('kanji/勘.md','strokes/勘.json','words/勘.md','words/勘定.md',
            'words/勘違い.md','kanji/定.md','kanji/違.md','manifest.json')
        if (@($changes | Where-Object {
            $_.Substring(3) -notin $allowed -and
            $_.Substring(3) -notmatch '^docs/n1-sources/batch-107-' -and
            $_.Substring(3) -ne 'docs/n1-sources/execution-844.json'
        }).Count) { throw 'Unexpected draft changes' }
    } elseif ($changes.Count) { throw 'Worktree not wholly clean' }
}
if ((git -C $content branch --show-current) -ne 'n1/resume-after-106-476f429') {
    throw 'Unexpected recovered branch'
}
git -C $content fetch --quiet origin main
if ($LASTEXITCODE -ne 0) { throw 'Fresh main fetch failed' }
$main = git -C $content rev-parse origin/main
if ($LASTEXITCODE -ne 0 -or $main -ne '476f429108415d00f9d41863af9d2f9470b5bbc0') {
    throw 'Main advanced; preserve and reconcile'
}
$receipt = "$control\logs\$session\$ReceiptName"
if (Test-Path $receipt) { throw 'Do not overwrite evidence' }
[ordered]@{
    execution=844; sessionId=$session; verifiedAt=[DateTimeOffset]::UtcNow.ToString('o')
    ancestry=$ancestry; liveParentPid=$process.ProcessId; coordinatorPid=$coordinator.ProcessId
    exactFileLauncherMatches=$true; launcherSha256=$hash; checkpoint=843
    contentHead=$ExpectedContentHead; freshOriginMain=$main; initiallyWhollyClean=(-not $Draft)
    exactSignedHeadsVerified=$true; androidHead='bf30cdead8515739bc0e671d57a54b9a3109dd46'
    contentWorktree=$content; androidWorktree=$android; childApprovalEnvironmentAbsent=$true
    parentLockRole='Live parent launcher owns runner.lock; no child acquire/delete/unlock/read-probe.'
    lockTouched=$false
} | ConvertTo-Json -Depth 8 | Set-Content $receipt -Encoding utf8NoBOM
Write-Output 'Live launcher/session/signed recovered heads/fresh main verified; parent lock untouched.'
