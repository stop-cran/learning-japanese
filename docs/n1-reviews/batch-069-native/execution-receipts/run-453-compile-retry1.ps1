$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$content = Join-Path $workspace 'learning-japanese'
$android = Join-Path $workspace 'kanji-cards-android'
$folder = Join-Path $control 'artifacts\batch-069-native-retry1-compile'
if (Test-Path $folder) { throw 'Existing compilation; refusing overwrite.' }
$fixture = Join-Path $content 'docs\n1-reviews\batch-069-native\N1Batch069NativeRetry1Test.kt'
$archive = Join-Path $control 'artifacts\n1-batch-069-e2457397-envelope.zip'
$target = Join-Path $android 'app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch069NativeRetry1Test.kt'
$asset = Join-Path $android 'app\src\androidTest\assets\n1-batch-069-e2457397-envelope.zip'
$apk = Join-Path $control 'artifacts\n1-batch-069-native-retry1-test.apk'
foreach ($path in @($target,$asset,$apk)) { if (Test-Path $path) { throw "Never overwrite: $path" } }
if ((Get-FileHash $archive).Hash.ToLowerInvariant() -ne 'cae3662a9fe46008ce7f0ea66980e84cc712f45d77558fbd9e2e947bd930a198') { throw 'Archive changed.' }
if ((git -C $android rev-parse HEAD) -ne 'f9b59a2bc5a203c6b4de26be50021a4c720dc22c' -or (git -C $android status --porcelain)) { throw 'Android changed.' }
$fixtureHash = (Get-FileHash $fixture).Hash.ToLowerInvariant()
New-Item -ItemType Directory -Path $folder | Out-Null
$installedSource = $false
$installedAsset = $false
try {
    Copy-Item $fixture $target
    $installedSource = $true
    Copy-Item $archive $asset
    $installedAsset = $true
    $env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
    $env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
    Set-Location $android
    & .\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process' *> (Join-Path $folder 'compile.txt')
    $code = $LASTEXITCODE
    $code | Set-Content (Join-Path $folder 'exit-code.txt')
    Get-Content (Join-Path $folder 'compile.txt') -Tail 10
    if ($code -ne 0) { throw "Retry compilation failed: $code" }
    Copy-Item 'app\build\outputs\apk\androidTest\debug\app-debug-androidTest.apk' $apk
} finally {
    if ($installedSource) {
        if ((Get-FileHash $target).Hash.ToLowerInvariant() -ne $fixtureHash) { throw 'Temporary fixture changed; preserve it.' }
        Remove-Item -LiteralPath $target
    }
    if ($installedAsset) {
        if ((Get-FileHash $asset).Hash.ToLowerInvariant() -ne 'cae3662a9fe46008ce7f0ea66980e84cc712f45d77558fbd9e2e947bd930a198') { throw 'Temporary archive changed; preserve it.' }
        Remove-Item -LiteralPath $asset
    }
}
if (git -C $android status --porcelain) { throw 'Android cleanup not clean.' }
[ordered]@{
    fixture=$fixture;fixtureSha256=$fixtureHash;apk=$apk;apkSha256=(Get-FileHash $apk).Hash.ToLowerInvariant()
    exactArchiveSha256='cae3662a9fe46008ce7f0ea66980e84cc712f45d77558fbd9e2e947bd930a198'
    exitCode=0;temporarySourcesCleaned=$true;androidClean=$true
} | ConvertTo-Json | Set-Content (Join-Path $control 'batch-069-native-retry1-compilation.json') -Encoding utf8NoBOM
