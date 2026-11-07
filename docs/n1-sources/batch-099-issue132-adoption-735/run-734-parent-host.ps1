$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$output = Join-Path $control 'artifacts\batch-099-issue132-signed-host'
$lock = [IO.File]::Open((Join-Path $control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $progress = Get-Content -LiteralPath (Join-Path $control 'progress.json') -Raw | ConvertFrom-Json
    if ($progress.checkpoint -ne 734 -or $progress.batch -ne '099' -or $progress.status -ne 'blocked') {
        throw 'Checkpoint changed.'
    }
    if (Test-Path -LiteralPath $output) { throw 'Do not overwrite evidence.' }
    foreach ($repository in @(
        @{ name = 'learning-japanese'; head = '309189fcda2723ddcf652a9ae5cba7c807d24872' },
        @{ name = 'kanji-cards-android'; head = 'bf30cdead8515739bc0e671d57a54b9a3109dd46' }
    )) {
        $path = Join-Path $workspace $repository.name
        if ((git -C $path rev-parse HEAD) -ne $repository.head -or
            (git -C $path log -1 --format=%G?) -ne 'G' -or
            (git -C $path status --porcelain)) { throw 'Unexpected worktree state.' }
    }
    $init = Join-Path $control 'batch-065-host-integration-heap.init.gradle'
    if ((Get-FileHash -LiteralPath $init).Hash.ToLowerInvariant() -ne
        '438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24') {
        throw 'Qualified HOST init changed.'
    }
    New-Item -ItemType Directory -Path $output | Out-Null
    $arguments = @(':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
        ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
        '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
        '-Pkotlin.compiler.execution.strategy=in-process', '--init-script', $init)
    $arguments | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $output 'arguments.json') -Encoding utf8NoBOM
    $env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
    $env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
    Set-Location -LiteralPath (Join-Path $workspace 'kanji-cards-android')
    [DateTimeOffset]::UtcNow.ToString('o') | Set-Content -LiteralPath (Join-Path $output 'start.txt')
    & .\gradlew.bat @arguments 2>&1 | Tee-Object -FilePath (Join-Path $output 'gradle.txt')
    $code = $LASTEXITCODE
    $code | Set-Content -LiteralPath (Join-Path $output 'exit.txt')
    [DateTimeOffset]::UtcNow.ToString('o') | Set-Content -LiteralPath (Join-Path $output 'end.txt')
    exit $code
} finally {
    $lock.Dispose()
}
