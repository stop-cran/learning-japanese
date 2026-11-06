$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$log = Join-Path $control 'logs\bb3b3736-672b-44f7-b9a6-8be9048f0c84'
$lock = [IO.File]::Open((Join-Path $control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $progress = Get-Content -LiteralPath (Join-Path $control 'progress.json') -Raw | ConvertFrom-Json
    if ($progress.checkpoint -ne 570 -or $progress.batch -ne '083' -or
        $progress.stage -ne 'fresh-host-android-checks-running') { throw 'Checkpoint changed.' }
    if ((git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
        (git -C $android status --porcelain)) { throw 'Unexpected Android state.' }
    $arguments = @(':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
        ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
        '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
        '-Pkotlin.compiler.execution.strategy=in-process', '--init-script',
        (Join-Path $control 'batch-065-host-integration-heap.init.gradle'))
    $arguments | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $log 'android-arguments.json') -Encoding utf8NoBOM
    $env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
    $env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
    Set-Location -LiteralPath $android
    [DateTimeOffset]::UtcNow.ToString('o') | Set-Content -LiteralPath (Join-Path $log 'android-start.txt')
    & .\gradlew.bat @arguments *> (Join-Path $log 'android.txt')
    $code = $LASTEXITCODE
    $code | Set-Content -LiteralPath (Join-Path $log 'android-exit.txt')
    [DateTimeOffset]::UtcNow.ToString('o') | Set-Content -LiteralPath (Join-Path $log 'android-end.txt')
    Get-Content -LiteralPath (Join-Path $log 'android.txt') -Tail 15
    exit $code
} finally {
    $lock.Dispose()
}
