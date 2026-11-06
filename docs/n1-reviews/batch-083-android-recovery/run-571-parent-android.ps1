$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$content = Join-Path $workspace 'learning-japanese'
$android = Join-Path $workspace 'kanji-cards-android'
$output = Join-Path $control 'artifacts\batch-083-parent-lock-recovery'
$lock = [IO.File]::Open((Join-Path $control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    if (Get-Process -Id 9004 -ErrorAction SilentlyContinue) { throw 'Prior runner PID still exists; investigate ownership.' }
    if (Test-Path -LiteralPath $output) { throw 'Do not overwrite recovery artifacts.' }
    $progress = Get-Content -LiteralPath (Join-Path $control 'progress.json') -Raw | ConvertFrom-Json
    if ($progress.checkpoint -ne 571 -or $progress.batch -ne '083' -or $progress.status -ne 'blocked') {
        throw 'Checkpoint changed.'
    }
    foreach ($repository in @(
        @{ path = $content; head = 'c3ebb45896b3637ad784ba33d89e8fff3356925a' },
        @{ path = $android; head = '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' }
    )) {
        if ((git -C $repository.path rev-parse HEAD) -ne $repository.head -or
            (git -C $repository.path log -1 --format=%G?) -ne 'G' -or
            (git -C $repository.path status --porcelain)) { throw 'Unexpected worktree state.' }
    }
    New-Item -ItemType Directory -Path $output | Out-Null
    $arguments = @(':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
        ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
        '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
        '-Pkotlin.compiler.execution.strategy=in-process', '--init-script',
        (Join-Path $control 'batch-065-host-integration-heap.init.gradle'))
    $arguments | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $output 'arguments.json') -Encoding utf8NoBOM
    $env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
    $env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
    Set-Location -LiteralPath $android
    [DateTimeOffset]::UtcNow.ToString('o') | Set-Content -LiteralPath (Join-Path $output 'start.txt')
    & .\gradlew.bat @arguments 2>&1 | Tee-Object -FilePath (Join-Path $output 'gradle.txt')
    $code = $LASTEXITCODE
    $code | Set-Content -LiteralPath (Join-Path $output 'exit.txt')
    [DateTimeOffset]::UtcNow.ToString('o') | Set-Content -LiteralPath (Join-Path $output 'end.txt')
    exit $code
} finally {
    $lock.Dispose()
}
