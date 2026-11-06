param(
    [Parameter(Mandatory)][ValidatePattern('^\d{3}$')][string]$Batch,
    [Parameter(Mandatory)][int]$Checkpoint,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$ContentHead,
    [Parameter(Mandatory)][DateTimeOffset]$NotBefore,
    [Parameter(Mandatory)][string]$ExecutionShellId,
    [Parameter(Mandatory)][string]$LogPath,
    [Parameter(Mandatory)][string]$Recovery,
    [ValidatePattern('^[0-9a-f]{40}$')][string]$AndroidHead = 'f9b59a2bc5a203c6b4de26be50021a4c720dc22c'
)

$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$progress = Get-Content -LiteralPath (Join-Path $control 'progress.json') -Raw | ConvertFrom-Json
if ($progress.checkpoint -ne $Checkpoint -or $progress.status -ne 'blocked' -or $progress.batch -ne $Batch) {
    throw 'Checkpoint changed; do not overwrite recovery evidence.'
}
$lock = [IO.File]::Open((Join-Path $control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
$lock.Dispose()
$appHead = $AndroidHead
foreach ($repository in @(
    @{ name = 'learning-japanese'; head = $ContentHead },
    @{ name = 'kanji-cards-android'; head = $appHead }
)) {
    $path = Join-Path $workspace $repository.name
    $actual = git -C $path rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $actual -ne $repository.head) { throw "Unexpected HEAD: $path" }
    $dirty = git -C $path status --porcelain
    if ($LASTEXITCODE -ne 0 -or $dirty) { throw "Worktree is not clean: $path" }
}
$buildLog = Get-Content -LiteralPath $LogPath -Raw
if ($buildLog -notmatch 'BUILD SUCCESSFUL in ([^\r\n]+)' -or
    $buildLog -notmatch '41 actionable tasks: 41 executed') {
    throw 'Fresh successful complete Gradle run is not recorded.'
}
$results = foreach ($case in @(
    @{ name = 'RealContentTest'; module = 'core'; task = 'test'; expected = 3 },
    @{ name = 'RareHanTest'; module = 'app'; task = 'testDebugUnitTest'; expected = 1 }
)) {
    $module = Join-Path (Join-Path $workspace 'kanji-cards-android') $case.module
    $source = Join-Path $module "build\test-results\$($case.task)\TEST-io.github.stopcran.kanji.core.$($case.name).xml"
    [xml]$xml = Get-Content -LiteralPath $source -Raw
    $suite = $xml.testsuite
    if ([int]$suite.tests -ne $case.expected -or [int]$suite.failures -ne 0 -or
        [int]$suite.errors -ne 0 -or [int]$suite.skipped -ne 0 -or
        @($suite.testcase).Count -ne $case.expected) {
        throw "Failed, skipped or missing cases: $($case.name)"
    }
    $timestamp = [DateTimeOffset]::Parse($suite.timestamp, [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::AssumeUniversal)
    if ($timestamp -lt $NotBefore) { throw "Stale XML: $($case.name)" }
    $root = [IO.Path]::GetFullPath((Join-Path $module '..\..\learning-japanese'))
    if ($root -cne (Join-Path $workspace 'learning-japanese')) { throw 'Unexpected fixture root.' }
    $copy = Join-Path $control "artifacts\batch-$Batch-parent-$($case.name).xml"
    Copy-Item -LiteralPath $source -Destination $copy
    [ordered]@{
        name = $suite.name
        tests = [int]$suite.tests
        failures = [int]$suite.failures
        errors = [int]$suite.errors
        skipped = [int]$suite.skipped
        timestamp = $suite.timestamp
        caseNames = @($suite.testcase | ForEach-Object { $_.name })
        sourcePath = $source
        artifactPath = $copy
        sha256 = (Get-FileHash -LiteralPath $copy -Algorithm SHA256).Hash.ToLowerInvariant()
        fixtureRoot = $root
    }
}
$receipt = [ordered]@{
    verifiedAt = [DateTimeOffset]::Now.ToString('o')
    checkpoint = $Checkpoint
    batch = $Batch
    localContentHead = $ContentHead
    androidHead = $appHead
    permissionRecovery = $Recovery
    shellId = $ExecutionShellId
    exitCode = 0
    buildResult = [regex]::Match($buildLog, 'BUILD SUCCESSFUL in [^\r\n]+').Value
    tasks = '41 actionable tasks: 41 executed'
    oneWorker = $true
    parallel = $false
    rerunTasks = $true
    log = $LogPath
    tests = @($results)
    worktreesClean = $true
    exclusiveLockAvailable = $true
    scope = 'Fresh Android gate only; not publication or complete rollout acceptance.'
}
$receipt | ConvertTo-Json -Depth 8 |
    Set-Content -LiteralPath (Join-Path $control "batch-$Batch-parent-android-recovery.json") -Encoding utf8NoBOM
$receipt | ConvertTo-Json -Depth 8
