$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$logs = "$control\logs\342070a3-d57f-4923-a4eb-030ef93ca108"
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne '342070a3-d57f-4923-a4eb-030ef93ca108') {
    throw 'Unexpected supervisor session; no competing execution.'
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
$evidence = Get-Content "$control\batch-082-native-fixture-verification.json" -Raw | ConvertFrom-Json
$target = "$android\app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch082NativeTest.kt"
$asset = "$android\app\src\androidTest\assets\n1-batch-082-4f5812bc-envelope.zip"
$log = "$logs\native-compile.txt"
$exitFile = "$logs\native-compile-exit.txt"
$frozenApk = "$control\artifacts\n1-batch-082-native-test.apk"
$frozenApp = "$control\artifacts\n1-batch-082-native-app.apk"
$app = "$android\app\build\outputs\apk\debug\app-debug.apk"
foreach ($path in @($target, $asset, $log, $exitFile, $frozenApk, $frozenApp)) {
    if (Test-Path -LiteralPath $path) { throw "Never overwrite an existing attempt: $path" }
}
foreach ($entry in @(@{path=$evidence.fixture; hash=$evidence.fixtureSha256},
    @{path=$evidence.archive; hash=$evidence.archiveSha256},
    @{path=$app; hash='0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407'})) {
    if ((Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.hash) {
        throw "Frozen input hash mismatch: $($entry.path)"
    }
}
Set-Location $android
$status = git --no-pager status --porcelain
if ($LASTEXITCODE -ne 0 -or $status) { throw 'Dedicated Android worktree is not clean.' }
$head = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $head -ne $evidence.androidSnapshot) { throw 'Qualified Android head changed.' }
$productionDelta = git diff f9b59a2bc5a203c6b4de26be50021a4c720dc22c HEAD -- app/src/main core/src/main gradle.properties
if ($LASTEXITCODE -ne 0 -or $productionDelta) { throw 'Production baseline changed.' }
$installedSource = $false
$installedAsset = $false
try {
    Copy-Item -LiteralPath $evidence.fixture -Destination $target -ErrorAction Stop
    $installedSource = $true
    Copy-Item -LiteralPath $evidence.archive -Destination $asset -ErrorAction Stop
    $installedAsset = $true
    $env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
    $env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
    $arguments = @(':app:assembleDebugAndroidTest', '--no-daemon', '--no-parallel', '--max-workers=1',
        '-Pkotlin.compiler.execution.strategy=in-process')
    $arguments | ConvertTo-Json | Set-Content "$logs\native-compile-arguments.json" -Encoding utf8NoBOM
    Get-Date -Format o | Set-Content "$logs\native-compile-start.txt"
    & .\gradlew.bat @arguments *> $log
    $code = $LASTEXITCODE
    $code | Set-Content $exitFile
    Get-Date -Format o | Set-Content "$logs\native-compile-end.txt"
    Get-Content -LiteralPath $log -Tail 14
    if ($code -ne 0) { throw "Fixture compilation failed: $code; exact original log retained." }
    Copy-Item -LiteralPath "$android\app\build\outputs\apk\androidTest\debug\app-debug-androidTest.apk" -Destination $frozenApk
    Copy-Item -LiteralPath $app -Destination $frozenApp
} finally {
    if ($installedSource) {
        if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -ne $evidence.fixtureSha256) {
            throw 'Temporary source changed; preserve instead of deleting.'
        }
        Remove-Item -LiteralPath $target -ErrorAction Stop
    }
    if ($installedAsset) {
        if ((Get-FileHash -LiteralPath $asset -Algorithm SHA256).Hash.ToLowerInvariant() -ne $evidence.archiveSha256) {
            throw 'Temporary asset changed; preserve instead of deleting.'
        }
        Remove-Item -LiteralPath $asset -ErrorAction Stop
    }
}
$status = git --no-pager status --porcelain
if ($LASTEXITCODE -ne 0 -or $status) { throw 'Dedicated Android cleanup is not clean.' }
