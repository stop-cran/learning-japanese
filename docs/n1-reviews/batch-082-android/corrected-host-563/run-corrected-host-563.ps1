$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$content = Join-Path $workspace 'learning-japanese'
$android = Join-Path $workspace 'kanji-cards-android'
$out = Join-Path $control 'artifacts\batch-082-corrected-host-563'
$contentHead = 'e2b1ea6325bc705c5174c41f40a944baee5f6f64'
$androidHead = '1c1b7bf42cc91d820a93169f1088dc647ac51c0d'
$init = Join-Path $control 'batch-065-host-integration-heap.init.gradle'
if (Test-Path -LiteralPath $out) { throw 'Output already exists; preserve the original run.' }
foreach ($repo in @(@{path=$content; head=$contentHead}, @{path=$android; head=$androidHead})) {
    if ((git -C $repo.path rev-parse HEAD) -ne $repo.head -or
        (git -C $repo.path log -1 --format=%G?) -ne 'G' -or
        (git -C $repo.path status --porcelain)) { throw 'Unexpected worktree state.' }
}
if ((Get-FileHash -LiteralPath $init).Hash.ToLowerInvariant() -ne
    '438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24') {
    throw 'Qualified HOST-only init changed.'
}
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
$arguments = @(
    ':core:test', '--tests', 'io.github.stopcran.kanji.core.RealContentTest',
    '--tests', 'io.github.stopcran.kanji.core.PublishableContentFixtureTest',
    ':app:testDebugUnitTest', '--tests', 'io.github.stopcran.kanji.core.RareHanTest',
    '--no-daemon', '--no-parallel', '--max-workers=1', '--rerun-tasks',
    '-Pkotlin.compiler.execution.strategy=in-process', '--init-script', $init
)
New-Item -ItemType Directory -Path $out | Out-Null
$start = [DateTimeOffset]::UtcNow
Set-Location -LiteralPath $android
& '.\gradlew.bat' @arguments *> (Join-Path $out 'gradle.txt')
$code = $LASTEXITCODE
$end = [DateTimeOffset]::UtcNow
$receipt = [ordered]@{
    execution=563; batch='082'; contentHead=$contentHead; androidHead=$androidHead
    startedAt=$start.ToString('o'); completedAt=$end.ToString('o'); exitCode=$code
    runnerPid=$PID; workingDirectory=$android; fixtureRoot=$content
    javaHome=$env:JAVA_HOME; androidHome=$env:ANDROID_HOME
    executable=(Join-Path $android 'gradlew.bat'); arguments=$arguments
    hostOnly=$true; nativeLaunched=$false; maxWorkers=1; parallel=$false; rerunTasks=$true
}
$receipt | ConvertTo-Json -Depth 8 |
    Set-Content -LiteralPath (Join-Path $out 'command.json') -Encoding utf8NoBOM
if ($code -ne 0) { throw "Gradle failed with exit $code; original log retained." }
foreach ($test in @(
    @{module='core'; task='test'; name='RealContentTest'},
    @{module='core'; task='test'; name='PublishableContentFixtureTest'},
    @{module='app'; task='testDebugUnitTest'; name='RareHanTest'}
)) {
    $source = Join-Path $android "$($test.module)\build\test-results\$($test.task)\TEST-io.github.stopcran.kanji.core.$($test.name).xml"
    Copy-Item -LiteralPath $source -Destination (Join-Path $out "$($test.name).xml")
}
Get-Content -LiteralPath (Join-Path $out 'gradle.txt') -Tail 6
$receipt | ConvertTo-Json -Depth 8
