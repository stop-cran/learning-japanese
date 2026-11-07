$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$session = '49dac17d-7012-48cb-b241-ce67cb94bf4e'
$logs = "$control\logs\$session"
& "$control\preflight-693.ps1"
if ($LASTEXITCODE -ne 0) { throw 'Parent-role preflight failed; preserve and yield.' }
$role = Get-Content "$logs\preflight-693.json" -Raw | ConvertFrom-Json
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 692 -or $p.batch -ne '095' -or $p.status -ne 'continue' -or
    $p.stage -ne 'batch-095-native-preparation-in-progress') { throw 'Checkpoint context changed.' }
$evidence = Get-Content "$control\batch-095-native-fixture-verification.json" -Raw | ConvertFrom-Json
$target = "$android\app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch095NativeTest.kt"
$asset = Join-Path "$android\app\src\androidTest\assets" (Split-Path $evidence.archive -Leaf)
$log = "$logs\native-compile.txt"
$exitFile = "$logs\native-compile-exit.txt"
$frozenApk = "$control\artifacts\n1-batch-095-native-test.apk"
$frozenApp = "$control\artifacts\n1-batch-095-native-app.apk"
$app = "$android\app\build\outputs\apk\debug\app-debug.apk"
$baselineAppSha256 = '0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407'
foreach ($path in @($target, $asset, $log, $exitFile, $frozenApk, $frozenApp)) {
    if (Test-Path -LiteralPath $path) { throw "Never overwrite an existing attempt: $path" }
}
foreach ($entry in @(@{path=$evidence.fixture; hash=$evidence.fixtureSha256},
    @{path=$evidence.archive; hash=$evidence.archiveSha256}, @{path=$app; hash=$baselineAppSha256})) {
    if ((Get-FileHash -LiteralPath $entry.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.hash) {
        throw "Frozen input hash mismatch: $($entry.path)"
    }
}
foreach ($tree in @(@{root=$content; head=$evidence.contentSnapshot}, @{root=$android; head=$evidence.androidSnapshot})) {
    $status = git -C $tree.root --no-pager status --porcelain --untracked-files=all
    if ($LASTEXITCODE -ne 0 -or $status) { throw 'Dedicated worktree is not wholly clean.' }
    $head = git -C $tree.root rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $tree.head) { throw 'Frozen HEAD changed.' }
    $signature = git -C $tree.root log -1 '--format=%G?'
    if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Frozen HEAD signature is not good.' }
}
$delta = git -C $android diff $evidence.productionBaseline HEAD -- app/src/main core/src/main gradle.properties
if ($LASTEXITCODE -ne 0 -or $delta) { throw 'Production baseline changed.' }
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
        coordinatorSession=$session; parentRunnerPid=$role.liveParentPid; ancestry=$role.ancestry;
        parentAncestryVerified=$true; launcherCommandMatches=$role.decodedLauncherMatches; parentLockAccessAttempted=$false;
        hostOnlyHeapInitUsed=$false; oneWorker=$true; parallel=$false; baselineAppSha256=$baselineAppSha256
    } | ConvertTo-Json -Depth 6 | Set-Content "$logs\native-compile-command.json" -Encoding utf8NoBOM
    Get-Date -Format o | Set-Content "$logs\native-compile-start.txt"
    & .\gradlew.bat @arguments *> $log
    $code = $LASTEXITCODE
    $code | Set-Content $exitFile
    Get-Date -Format o | Set-Content "$logs\native-compile-end.txt"
    Get-Content -LiteralPath $log -Tail 16
    if ($code -ne 0) { throw "Fixture compilation failed: $code; original log retained." }
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
$status = git --no-pager status --porcelain --untracked-files=all
if ($LASTEXITCODE -ne 0 -or $status) { throw 'Dedicated Android cleanup is not wholly clean.' }
