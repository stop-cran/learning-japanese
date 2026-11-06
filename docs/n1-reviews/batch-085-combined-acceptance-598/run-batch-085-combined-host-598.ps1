$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$session = '4e19ca44-0f2d-4721-996a-8f32a6f5d943'
$logs = Join-Path "$control\logs" $session
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne $session -or $runner.pid -ne 19008) {
    throw 'Unexpected live launcher context; preserve and yield.'
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
    $ancestry += [pscustomobject]@{pid=$process.ProcessId; parent=$process.ParentProcessId; command=$command}
    if ($ancestor -eq $runner.pid) {
        $owned = $command -match 'n1-kanji-workspace\\control\\runner.ps1'
        break
    }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Expected launcher not verified; no lock access attempted.' }
$ancestry | ConvertTo-Json | Set-Content "$logs\runner-ancestry-598.json" -Encoding utf8NoBOM
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 597 -or $p.batch -ne '085' -or
    $p.stage -ne 'batch-085-combined-main-integration-in-progress') {
    throw 'Checkpoint context changed.'
}
foreach ($tree in @(
    @{root=$content; head='40eb5dcee006ef142721fcd9c9e923c616f6a89e'},
    @{root=$android; head='1c1b7bf42cc91d820a93169f1088dc647ac51c0d'}
)) {
    if ((git -C $tree.root rev-parse HEAD) -ne $tree.head -or
        (git -C $tree.root log -1 '--format=%G?') -ne 'G' -or
        (git -C $tree.root status --porcelain)) {
        throw 'Dedicated worktree not wholly clean with exact signed head.'
    }
}
if ((git -C $content rev-parse origin/main) -ne '97a16b0027b05c0528d78971dd3b17cce17d8056') {
    throw 'Main changed; integrate and reassess before testing.'
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
} | ConvertTo-Json | Set-Content "$logs\host-command-598.json" -Encoding utf8NoBOM
Set-Location $android
Get-Date -Format o | Set-Content "$logs\host-start-598.txt"
& .\gradlew.bat @arguments *> "$logs\host-598.txt"
$code = $LASTEXITCODE
$code | Set-Content "$logs\host-exit-598.txt"
Get-Date -Format o | Set-Content "$logs\host-end-598.txt"
Get-Content "$logs\host-598.txt" -Tail 16
exit $code
