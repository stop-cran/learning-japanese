$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne '8327db1a-6be4-4e90-9f27-d86089e17e4e') {
    throw 'Unexpected supervisor session; do not start a competing execution.'
}
$ancestor = $PID
$owned = $false
while ($ancestor -gt 0) {
    if ($ancestor -eq $runner.pid) { $owned = $true; break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if ($null -eq $process) { break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Recorded supervisor is not this execution ancestor.' }
$evidence = Get-Content "$control\batch-060-native-fixture-verification.json" -Raw | ConvertFrom-Json
$fixture = $evidence.fixture
$archive = $evidence.archive
$target = "$android\app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch060NativeTest.kt"
$asset = "$android\app\src\androidTest\assets\n1-batch-060-99d8ace0-envelope.zip"
$log = "$control\logs\execution-366-native-compile.txt"
$exitFile = "$control\logs\execution-366-native-compile-exit.txt"
$frozenApk = "$control\artifacts\n1-batch-060-native-test.apk"
foreach ($path in @($target, $asset, $log, $exitFile, $frozenApk)) {
    if (Test-Path -LiteralPath $path) { throw "Never overwrite existing attempt: $path" }
}
if ((Get-FileHash -LiteralPath $fixture -Algorithm SHA256).Hash.ToLowerInvariant() -ne $evidence.fixtureSha256) {
    throw 'Frozen fixture hash mismatch.'
}
if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $evidence.archiveSha256) {
    throw 'Frozen archive hash mismatch.'
}
Set-Location $android
$status = git --no-pager status --porcelain
if ($LASTEXITCODE -ne 0 -or $status) { throw 'Dedicated Android worktree is not clean.' }
$head = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $head -ne 'f9b59a2bc5a203c6b4de26be50021a4c720dc22c') { throw 'Android head changed.' }
$installedSource = $false
$installedAsset = $false
try {
    Copy-Item -LiteralPath $fixture -Destination $target -ErrorAction Stop
    $installedSource = $true
    Copy-Item -LiteralPath $archive -Destination $asset -ErrorAction Stop
    $installedAsset = $true
    $env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
    $env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
    Get-Date -Format o | Set-Content "$control\logs\execution-366-native-compile-start.txt"
    & .\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process' *> $log
    $code = $LASTEXITCODE
    $code | Set-Content $exitFile
    Get-Content -LiteralPath $log -Tail 14
    if ($code -ne 0) { throw "Fixture compilation failed: $code; exact original log retained." }
    Copy-Item -LiteralPath "$android\app\build\outputs\apk\androidTest\debug\app-debug-androidTest.apk" -Destination $frozenApk
} finally {
    if ($installedSource) {
        if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -ne $evidence.fixtureSha256) {
            throw 'Temporary source changed; preserve it instead of deleting.'
        }
        Remove-Item -LiteralPath $target -ErrorAction Stop
    }
    if ($installedAsset) {
        if ((Get-FileHash -LiteralPath $asset -Algorithm SHA256).Hash.ToLowerInvariant() -ne $evidence.archiveSha256) {
            throw 'Temporary asset changed; preserve it instead of deleting.'
        }
        Remove-Item -LiteralPath $asset -ErrorAction Stop
    }
}
$status = git --no-pager status --porcelain
if ($LASTEXITCODE -ne 0 -or $status) { throw 'Dedicated Android cleanup is not clean.' }
