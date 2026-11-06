$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$session = '94a69f58-a6ed-411f-b1bc-90b6e47ccb68'
$logs = Join-Path "$control\logs" $session
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne $session -or $runner.pid -ne 19008) {
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
$ancestry | ConvertTo-Json | Set-Content "$logs\runner-ancestry-580.json" -Encoding utf8NoBOM
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 579 -or $p.batch -ne '083' -or $p.stage -ne 'batch-083-combined-main-acceptance-in-progress') {
    throw 'Checkpoint context changed.'
}
foreach ($tree in @(@{root=$content; head='a70c9deb565e696772342675c2a9c99b09967e8a'},
    @{root=$android; head='1c1b7bf42cc91d820a93169f1088dc647ac51c0d'})) {
    if ((git -C $tree.root rev-parse HEAD) -ne $tree.head -or
        (git -C $tree.root log -1 '--format=%G?') -ne 'G' -or
        (git -C $tree.root status --porcelain)) { throw 'Dedicated signed worktree not wholly clean/exact.' }
}
if ((git -C $content rev-parse origin/main) -ne '21a5cb1328aadd437139a6b850f07298a2e2985d') {
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
} | ConvertTo-Json | Set-Content "$logs\host-command-580.json" -Encoding utf8NoBOM
Set-Location $android
Get-Date -Format o | Set-Content "$logs\host-start-580.txt"
& .\gradlew.bat @arguments *> "$logs\host-580.txt"
$code = $LASTEXITCODE
$code | Set-Content "$logs\host-exit-580.txt"
Get-Date -Format o | Set-Content "$logs\host-end-580.txt"
Get-Content "$logs\host-580.txt" -Tail 16
exit $code
