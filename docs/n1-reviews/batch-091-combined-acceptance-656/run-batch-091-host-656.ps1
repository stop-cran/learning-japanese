$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$log = Join-Path $control 'logs\bf2bf78f-2a42-401f-8d4b-e4c00a084073'
$env:PYTHONIOENCODING = 'utf-8'
python -B (Join-Path $control 'accept-batch-091-656.py') audit
if ($LASTEXITCODE -ne 0) { throw 'Exact signed heads, clean state, launcher, checkpoint or source audit failed.' }
$progress = Get-Content (Join-Path $control 'progress.json') -Raw | ConvertFrom-Json
if ($progress.checkpoint -ne 655 -or $progress.batch -ne '091' -or
    $progress.stage -ne 'batch-091-combined-main-acceptance-in-progress') { throw 'Checkpoint changed.' }
$arguments = @(':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
    ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
    '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
    '-Pkotlin.compiler.execution.strategy=in-process', '--init-script',
    (Join-Path $control 'batch-065-host-integration-heap.init.gradle'))
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
@{arguments=$arguments; JAVA_HOME=$env:JAVA_HOME; ANDROID_HOME=$env:ANDROID_HOME;
    parentLockTouched=$false; hostOnlyHeapInit=$true; guestOrAppHeapChanged=$false
} | ConvertTo-Json | Set-Content (Join-Path $log 'host-command-656.json') -Encoding utf8NoBOM
Set-Location -LiteralPath (Join-Path (Split-Path $control -Parent) 'kanji-cards-android')
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content (Join-Path $log 'host-start-656.txt')
& .\gradlew.bat @arguments *> (Join-Path $log 'host-656.txt')
$code = $LASTEXITCODE
$code | Set-Content (Join-Path $log 'host-exit-656.txt')
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content (Join-Path $log 'host-end-656.txt')
Get-Content (Join-Path $log 'host-656.txt') -Tail 16
exit $code
