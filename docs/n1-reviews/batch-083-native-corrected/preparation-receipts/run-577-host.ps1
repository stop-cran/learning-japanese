$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$logs = "$control\logs\0a43f5a9-526e-48b3-a031-45f5abcd9a2f"
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne '0a43f5a9-526e-48b3-a031-45f5abcd9a2f' -or $runner.pid -ne 19008) {
    throw 'Unexpected live parent context; preserve and yield.'
}
$ancestor = $PID
$owned = $false
$ancestry = @()
while ($ancestor -gt 0) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if ($null -eq $process) { break }
    $ancestry += $process | Select-Object ProcessId, ParentProcessId, Name
    if ($ancestor -eq $runner.pid) { $owned = $true; break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Expected live runner is not this child ancestor; no lock access attempted.' }
$ancestry | ConvertTo-Json | Set-Content "$logs\runner-ancestry-577.json" -Encoding utf8NoBOM
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 576 -or $p.batch -ne '083' -or $p.stage -ne 'batch-083-corrected-host-native-preparation-in-progress') {
    throw 'Checkpoint context changed.'
}
foreach ($tree in @(@{root=$content; head='867fe8bef228145ef0a6e48690941b0a0aa50336'},
    @{root=$android; head='1c1b7bf42cc91d820a93169f1088dc647ac51c0d'})) {
    if ((git -C $tree.root rev-parse HEAD) -ne $tree.head -or
        (git -C $tree.root log -1 '--format=%G?') -ne 'G' -or
        (git -C $tree.root status --porcelain)) { throw 'Dedicated signed worktree not wholly clean/exact.' }
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
} | ConvertTo-Json | Set-Content "$logs\host-command-577.json" -Encoding utf8NoBOM
Set-Location $android
Get-Date -Format o | Set-Content "$logs\host-start-577.txt"
& .\gradlew.bat @arguments *> "$logs\host-577.txt"
$code = $LASTEXITCODE
$code | Set-Content "$logs\host-exit-577.txt"
Get-Date -Format o | Set-Content "$logs\host-end-577.txt"
Get-Content "$logs\host-577.txt" -Tail 16
exit $code
