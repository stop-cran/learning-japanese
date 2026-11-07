$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$session = 'e13bc447-6efd-4a7d-b640-0e5dadd40fd1'
$logs = Join-Path "$control\logs" $session
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne $session -or $runner.pid -ne 19008) {
    throw 'Unexpected launcher context; preserve and yield.'
}
$ancestor = $PID
$owned = $false
$ancestry = @()
while ($ancestor -gt 0) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if ($null -eq $process) { break }
    $command = $process.CommandLine
    if ($command -match '-EncodedCommand ([A-Za-z0-9+/=]+)') {
        $command = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
    }
    $matchesLauncher = $command.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')
    $ancestry += [pscustomobject]@{
        pid=$process.ProcessId; parent=$process.ParentProcessId; launcherCommandMatches=$matchesLauncher
    }
    if ($ancestor -eq $runner.pid) { $owned = $matchesLauncher; break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Parent launcher uncertain; no lock access attempted.' }
$ancestry | ConvertTo-Json | Set-Content "$logs\runner-ancestry-643.json" -Encoding utf8NoBOM
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 642 -or $p.batch -ne '090' -or
    $p.stage -ne 'batch-090-combined-main-integration-in-progress') { throw 'Checkpoint changed.' }
foreach ($tree in @(
    @{root=$content; head='3f1530421f967983dc1a588b23c6b8ca88436d8f'},
    @{root=$android; head='1c1b7bf42cc91d820a93169f1088dc647ac51c0d'}
)) {
    if ((git -C $tree.root rev-parse HEAD) -ne $tree.head -or
        (git -C $tree.root log -1 '--format=%G?') -ne 'G' -or
        (git -C $tree.root status --porcelain=v1 --untracked-files=all)) {
        throw 'Worktree not wholly clean at exact signed head.'
    }
}
if ((git -C $content rev-parse origin/main) -ne 'ebfd48dc911f32be0eeb9426db2f2d35a9084044') {
    throw 'Main changed; integrate and reassess.'
}
$arguments = @(':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
    ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
    '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
    '-Pkotlin.compiler.execution.strategy=in-process', '--init-script',
    "$control\batch-065-host-integration-heap.init.gradle")
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
@{arguments=$arguments; JAVA_HOME=$env:JAVA_HOME; ANDROID_HOME=$env:ANDROID_HOME;
    workingDirectory=$android; exactSiblingContent=$content; parentRunnerPid=$runner.pid;
    parentLockTouched=$false; hostOnlyHeapInit=$true; nativeHeapInit=$false
} | ConvertTo-Json | Set-Content "$logs\host-command-643.json" -Encoding utf8NoBOM
Set-Location $android
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content "$logs\host-start-643.txt"
& .\gradlew.bat @arguments *> "$logs\host-643.txt"
$code = $LASTEXITCODE
$code | Set-Content "$logs\host-exit-643.txt"
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content "$logs\host-end-643.txt"
Get-Content "$logs\host-643.txt" -Tail 16
exit $code
