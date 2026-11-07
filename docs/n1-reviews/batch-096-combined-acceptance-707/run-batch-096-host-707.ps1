$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$log = Join-Path $control 'logs\299afd0f-ad92-4c3b-91c9-b6b56934517d'
$env:PYTHONIOENCODING = 'utf-8'
python -X utf8 -B (Join-Path $control 'accept-batch-096-combined-707.py') preflight
if ($LASTEXITCODE -ne 0) { throw 'Signed-head/clean-state/live-parent/checkpoint preflight failed.' }
$arguments = @(':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
    ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
    '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
    '-Pkotlin.compiler.execution.strategy=in-process', '--init-script',
    (Join-Path $control 'batch-065-host-integration-heap.init.gradle'))
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
@{arguments=$arguments; JAVA_HOME=$env:JAVA_HOME; ANDROID_HOME=$env:ANDROID_HOME;
    parentLockTouched=$false; hostOnlyHeapInit=$true; guestOrAppHeapChanged=$false
} | ConvertTo-Json | Set-Content (Join-Path $log 'host-command-707.json') -Encoding utf8NoBOM
Set-Location -LiteralPath (Join-Path (Split-Path $control -Parent) 'kanji-cards-android')
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content (Join-Path $log 'host-start-707.txt')
& .\gradlew.bat @arguments *> (Join-Path $log 'host-707.txt')
$code = $LASTEXITCODE
$code | Set-Content (Join-Path $log 'host-exit-707.txt')
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content (Join-Path $log 'host-end-707.txt')
Get-Content (Join-Path $log 'host-707.txt') -Tail 16
exit $code
