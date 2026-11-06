$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$logs = Join-Path $control 'logs\7857506a-a446-4579-9f9f-ac206713bc8b'
foreach ($name in @('android-command.txt', 'android-start.txt', 'android-end.txt', 'android-exit.txt', 'android.txt')) {
    if (Test-Path (Join-Path $logs $name)) { throw "Existing attempt: $name" }
}
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
Set-Location (Join-Path (Split-Path $control -Parent) 'kanji-cards-android')
$arguments = @(':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
    ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
    '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
    '-Pkotlin.compiler.execution.strategy=in-process', '--init-script',
    (Join-Path $control 'batch-065-host-integration-heap.init.gradle'))
('.\gradlew.bat ' + ($arguments -join ' ')) |
    Set-Content (Join-Path $logs 'android-command.txt') -Encoding utf8NoBOM
[DateTimeOffset]::UtcNow.ToString('o') |
    Set-Content (Join-Path $logs 'android-start.txt') -Encoding utf8NoBOM
& .\gradlew.bat @arguments *> (Join-Path $logs 'android.txt')
$code = $LASTEXITCODE
[DateTimeOffset]::UtcNow.ToString('o') |
    Set-Content (Join-Path $logs 'android-end.txt') -Encoding utf8NoBOM
$code | Set-Content (Join-Path $logs 'android-exit.txt') -Encoding utf8NoBOM
Get-Content (Join-Path $logs 'android.txt') -Tail 18
exit $code
