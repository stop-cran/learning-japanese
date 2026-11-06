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
while ($ancestor -gt 0) {
    if ($ancestor -eq $runner.pid) { $owned = $true; break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if ($null -eq $process) { break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Recorded live runner is not this child ancestor; no lock access attempted.' }
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 576 -or $p.batch -ne '083' -or $p.stage -ne 'batch-083-corrected-host-native-preparation-in-progress') {
    throw 'Checkpoint context changed.'
}
if ((Get-Content "$logs\host-exit-577.txt" -Raw).Trim() -ne '0') { throw 'Fresh HOST did not pass.' }
$evidence = Get-Content "$control\batch-083-corrected-native-fixture-verification.json" -Raw | ConvertFrom-Json
$target = "$android\app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch083CorrectedNativeTest.kt"
$asset = Join-Path "$android\app\src\androidTest\assets" (Split-Path $evidence.archive -Leaf)
$log = "$logs\corrected-native-compile-577.txt"
$exitFile = "$logs\corrected-native-compile-exit-577.txt"
$frozenApk = "$control\artifacts\n1-batch-083-corrected-577-native-test.apk"
$frozenApp = "$control\artifacts\n1-batch-083-corrected-577-native-app.apk"
$app = "$android\app\build\outputs\apk\debug\app-debug.apk"
$baselineAppSha256 = '0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407'
foreach ($path in @($target, $asset, $log, $exitFile, $frozenApk, $frozenApp)) {
    if (Test-Path -LiteralPath $path) { throw "Never overwrite an existing attempt: $path" }
}
foreach ($entry in @(@{path=$evidence.fixture; hash=$evidence.fixtureSha256},
    @{path=$evidence.archive; hash=$evidence.archiveSha256},
    @{path=$app; hash=$baselineAppSha256})) {
    if ((Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.hash) {
        throw "Frozen input hash mismatch: $($entry.path)"
    }
}
foreach ($tree in @(@{root=$content; head=$evidence.contentSnapshot}, @{root=$android; head=$evidence.androidSnapshot})) {
    $status = git -C $tree.root --no-pager status --porcelain
    if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect dedicated worktree.' }
    if ($tree.root -eq $android -and $status) { throw 'Dedicated Android worktree is not wholly clean.' }
    if ($tree.root -eq $content) {
        $tracked = git -C $content diff --name-only HEAD
        if ($LASTEXITCODE -ne 0 -or $tracked) { throw 'Content has tracked changes after freeze.' }
        $newFiles = @(git -C $content ls-files --others --exclude-standard)
        if ($LASTEXITCODE -ne 0 -or $newFiles.Count -ne 2 -or
            @($newFiles | Where-Object { $_ -notin @(
                'docs/n1-reviews/batch-083-native-corrected/N1Batch083CorrectedNativeTest.kt',
                'docs/n1-reviews/batch-083-native-corrected/fixture-from-original-083.diff'
            ) }).Count -ne 0) { throw 'Unexpected content files beyond the two accounted preparation artifacts.' }
    }
    $head = git -C $tree.root rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $tree.head) { throw 'Frozen HEAD changed.' }
    $signature = git -C $tree.root log -1 '--format=%G?'
    if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Frozen HEAD signature is not good.' }
}
$productionDelta = git -C $android diff $evidence.productionBaseline HEAD -- app/src/main core/src/main gradle.properties
if ($LASTEXITCODE -ne 0 -or $productionDelta) { throw 'Production baseline changed.' }
Set-Location $android
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
    @{arguments=$arguments; JAVA_HOME=$env:JAVA_HOME; ANDROID_HOME=$env:ANDROID_HOME;
        workingDirectory=$android; androidHead=$evidence.androidSnapshot; contentHead=$evidence.contentSnapshot;
        coordinatorSession=$runner.sessionId; parentRunnerPid=$runner.pid;
        parentAncestryVerified=$true; parentLockAccessAttempted=$false;
        hostOnlyHeapInitUsed=$false; oneWorker=$true; parallel=$false; baselineAppSha256=$baselineAppSha256
    } | ConvertTo-Json | Set-Content "$logs\corrected-native-compile-command-577.json" -Encoding utf8NoBOM
    Get-Date -Format o | Set-Content "$logs\corrected-native-compile-start-577.txt"
    & .\gradlew.bat @arguments *> $log
    $code = $LASTEXITCODE
    $code | Set-Content $exitFile
    Get-Date -Format o | Set-Content "$logs\corrected-native-compile-end-577.txt"
    Get-Content -LiteralPath $log -Tail 16
    if ($code -ne 0) { throw "Corrected fixture compilation failed: $code; exact original log retained." }
    if ((Get-FileHash -LiteralPath $app -Algorithm SHA256).Hash.ToLowerInvariant() -ne $baselineAppSha256) {
        throw 'Production app APK changed during test-only compile.'
    }
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
if ($LASTEXITCODE -ne 0 -or $status) { throw 'Dedicated Android cleanup is not wholly clean.' }
