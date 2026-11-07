$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$session = 'f980cb7f-4783-4a86-9e11-fe07ed360018'
$folder = "$control\batch-094-corrected-native-686"
$receipt = "$folder\execution.json"
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
$adb = "$env:ANDROID_HOME\platform-tools\adb.exe"
$serial = 'emulator-5580'
$evidence = Get-Content "$folder\verification.json" -Raw | ConvertFrom-Json
$target = "$android\app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch094Correction686Test.kt"
$asset = Join-Path "$android\app\src\androidTest\assets" (Split-Path $evidence.archive -Leaf)
$testApk = "$folder\corrected-test.apk"
$appApk = "$control\artifacts\n1-batch-094-native-app.apk"
$baselineAppHash = '0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407'
foreach ($path in @($receipt, $target, $asset, $testApk, "$folder\compile.txt")) {
    if (Test-Path -LiteralPath $path) { throw "Never overwrite an existing attempt: $path" }
}
$result = [ordered]@{
    execution=686; batch='094'; startedAt=[DateTimeOffset]::Now.ToString('o')
    serial=$serial; contentSnapshot=$evidence.contentSnapshot; androidSnapshot=$evidence.androidSnapshot
    contentVersion=$evidence.contentVersion; fixtureSha256=$evidence.fixtureSha256
    archiveSha256=$evidence.archiveSha256; appApkSha256=$baselineAppHash
    compiled=$false; nativeExecuted=$false; passed=$false; failure=$null
    guestOrAppHeapChanged=$false; guardsChanged=$false; parentLockTouched=$false
}
$emulator = $null
$qemuPid = $null
function Assert-CleanHeads {
    foreach ($entry in @(@{root=$content;head=$evidence.contentSnapshot}, @{root=$android;head=$evidence.androidSnapshot})) {
        if ((git -C $entry.root rev-parse HEAD) -ne $entry.head -or $LASTEXITCODE -ne 0) { throw 'Signed head changed.' }
        if ((git -C $entry.root status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Worktree not wholly clean.' }
        if ((git -C $entry.root log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature not good.' }
    }
}
function Invoke-Adb {
    param([string[]]$Arguments)
    $output = & $adb -s $serial @Arguments 2>&1
    $code = $LASTEXITCODE
    "adb -s $serial $($Arguments -join ' ')" | Add-Content "$folder\adb-operations.txt" -Encoding utf8
    $output | Add-Content "$folder\adb-operations.txt" -Encoding utf8
    if ($code -ne 0) { throw "adb failed ($code): $($Arguments -join ' '): $output" }
    return $output
}
try {
    $state = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
    if ($state.checkpoint -ne 685 -or $state.batch -ne '094' -or $state.status -ne 'continue' -or
        $state.stage -ne 'batch-094-corrected-native-in-progress') { throw 'Checkpoint context changed.' }
    $runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
    if ($runner.pid -ne 19008 -or $runner.status -ne 'running' -or $runner.sessionId -ne $session) { throw 'Parent context uncertain.' }
    $ancestor = $PID
    $ancestry = @()
    while ($ancestor -gt 0 -and $ancestry.Count -lt 12) {
        $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
        if (-not $process) { break }
        $ancestry += $process | Select-Object ProcessId,ParentProcessId,Name
        if ($ancestor -eq $runner.pid) { break }
        $ancestor = $process.ParentProcessId
    }
    if ($ancestor -ne $runner.pid) { throw 'Parent is not live ancestor; no lock access attempted.' }
    $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($runner.pid)"
    $encoded = [regex]::Match($parent.CommandLine, '-EncodedCommand\s+(\S+)')
    if (-not $encoded.Success -or [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded.Groups[1].Value)) -notlike "*$control\runner.ps1*") {
        throw 'Launcher ownership uncertain.'
    }
    $result.launcherCommandMatches = $true
    $result.parentAncestry = $ancestry
    Assert-CleanHeads
    if ((git -C $android diff $evidence.productionBaseline HEAD -- app/src/main core/src/main gradle.properties) -or
        $LASTEXITCODE -ne 0) { throw 'Production baseline changed.' }
    foreach ($entry in @(@{path=$evidence.fixture;hash=$evidence.fixtureSha256},
        @{path=$evidence.archive;hash=$evidence.archiveSha256}, @{path=$appApk;hash=$baselineAppHash})) {
        if ((Get-FileHash -LiteralPath $entry.path).Hash.ToLowerInvariant() -ne $entry.hash) { throw 'Frozen input changed.' }
    }
    $installedSource = $false
    $installedAsset = $false
    try {
        Copy-Item -LiteralPath $evidence.fixture -Destination $target
        $installedSource = $true
        Copy-Item -LiteralPath $evidence.archive -Destination $asset
        $installedAsset = $true
        Set-Location $android
        $arguments = @(':app:assembleDebugAndroidTest', '--no-daemon', '--no-parallel', '--max-workers=1',
            '-Pkotlin.compiler.execution.strategy=in-process')
        $result.compileArguments = $arguments
        $result.JAVA_HOME = $env:JAVA_HOME
        $result.ANDROID_HOME = $env:ANDROID_HOME
        $result.compileStartedAt = [DateTimeOffset]::Now.ToString('o')
        & .\gradlew.bat @arguments *> "$folder\compile.txt"
        $result.compileExitCode = $LASTEXITCODE
        $result.compileCompletedAt = [DateTimeOffset]::Now.ToString('o')
        if ($result.compileExitCode -ne 0) { throw 'Native fixture compilation failed; log retained.' }
        $builtApp = "$android\app\build\outputs\apk\debug\app-debug.apk"
        if ((Get-FileHash -LiteralPath $builtApp).Hash.ToLowerInvariant() -ne $baselineAppHash) { throw 'Production app APK changed.' }
        Copy-Item -LiteralPath "$android\app\build\outputs\apk\androidTest\debug\app-debug-androidTest.apk" -Destination $testApk
        $result.testApkSha256 = (Get-FileHash -LiteralPath $testApk).Hash.ToLowerInvariant()
        $result.compiled = $true
    } finally {
        if ($installedSource) {
            if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $evidence.fixtureSha256) { throw 'Temporary source changed; preserve.' }
            Remove-Item -LiteralPath $target
        }
        if ($installedAsset) {
            if ((Get-FileHash -LiteralPath $asset).Hash.ToLowerInvariant() -ne $evidence.archiveSha256) { throw 'Temporary archive changed; preserve.' }
            Remove-Item -LiteralPath $asset
        }
    }
    Assert-CleanHeads
    $devices = (& $adb devices -l 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) { throw 'Device inspection failed.' }
    $connections = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object {
        $_.LocalPort -in @(5580,5581) -or $_.RemotePort -in @(5580,5581)
    } | Select-Object LocalAddress,RemoteAddress,LocalPort,RemotePort,State,OwningProcess)
    $result.preexistingEmulators = @(Get-CimInstance Win32_Process | Where-Object {
        $_.Name -match 'emulator|qemu'
    } | Select-Object ProcessId,ParentProcessId,Name,CommandLine)
    $result.prelaunch = @{verifiedAt=[DateTimeOffset]::Now.ToString('o');devices=$devices;connections=$connections}
    if ($devices -match 'emulator-5580' -or $connections.Count -gt 0) { throw '5580/5581 occupied; no helper launched.' }
    $emulatorArguments = @('-avd','N3_Acceptance_20261029','-port','5580','-read-only','-no-snapshot','-no-window','-no-audio',
        '-gpu','host','-feature','-Vulkan','-memory','2048','-cores','2')
    $emulator = Start-Process -FilePath "$env:ANDROID_HOME\emulator\emulator.exe" -ArgumentList $emulatorArguments -PassThru `
        -RedirectStandardOutput "$folder\emulator-stdout.txt" -RedirectStandardError "$folder\emulator-stderr.txt"
    $result.parentEmulatorPid = $emulator.Id
    $result.emulatorArguments = $emulatorArguments
    $deadline = [DateTimeOffset]::Now.AddMinutes(4)
    do {
        Start-Sleep -Seconds 5
        $boot = (& $adb -s $serial shell getprop sys.boot_completed 2>$null | Out-String).Trim()
        if ($emulator.HasExited) { throw 'Owned emulator exited before boot.' }
    } until ($boot -eq '1' -or [DateTimeOffset]::Now -gt $deadline)
    if ($boot -ne '1') { throw 'Emulator boot deadline exceeded.' }
    $qemu = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($emulator.Id)" | Where-Object { $_.Name -like 'qemu-system*' })
    if ($qemu.Count -ne 1) { throw 'Cannot establish owned QEMU child.' }
    $qemuPid = $qemu[0].ProcessId
    $result.qemuPid = $qemuPid
    $listeners = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object { $_.LocalPort -in @(5580,5581) -and $_.State -eq 'Listen' })
    if (-not $listeners -or @($listeners | Where-Object { $_.OwningProcess -ne $qemuPid }).Count -gt 0) { throw 'Helper port ownership mismatch.' }
    $result.listeners = @($listeners | Select-Object LocalPort,OwningProcess)
    Write-Output "OWNED_HELPER_RESPONSIVE serial=$serial parent=$($emulator.Id) qemu=$qemuPid boot=$boot"
    Start-Sleep -Seconds 90
    $result.fingerprint = (Invoke-Adb @('shell','getprop','ro.build.fingerprint') | Out-String).Trim()
    $result.heapGrowth = (Invoke-Adb @('shell','getprop','dalvik.vm.heapgrowthlimit') | Out-String).Trim()
    $result.heapSize = (Invoke-Adb @('shell','getprop','dalvik.vm.heapsize') | Out-String).Trim()
    if ($result.fingerprint -ne 'google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys' -or
        $result.heapGrowth -ne '192m' -or $result.heapSize -ne '576m') { throw 'Unexpected guest identity/heaps.' }
    Invoke-Adb @('install','-r','-t',$appApk) | Out-Null
    Invoke-Adb @('install','-r','-t',$testApk) | Out-Null
    Invoke-Adb @('shell','svc','wifi','disable') | Out-Null
    Invoke-Adb @('shell','svc','data','disable') | Out-Null
    Start-Sleep -Seconds 5
    $result.network = (Invoke-Adb @('shell','dumpsys','connectivity') | Select-String -SimpleMatch 'Active default network:' | Out-String).Trim()
    if ($result.network -ne 'Active default network: none') { throw 'Offline precondition missing.' }
    $result.nativeExecuted = $true
    $class = 'io.github.stopcran.kanji.ui.N1Batch094Correction686Test'
    $result.instrumentationCommand = "adb -s $serial shell am instrument -w -r -e n1Disposable true -e class $class io.github.stopcran.kanji.test/androidx.test.runner.AndroidJUnitRunner"
    & $adb -s $serial shell am instrument -w -r -e n1Disposable true -e class $class `
        'io.github.stopcran.kanji.test/androidx.test.runner.AndroidJUnitRunner' 2>&1 | Tee-Object -FilePath "$folder\instrumentation.txt"
    $result.adbExitCode = $LASTEXITCODE
    $raw = Get-Content "$folder\instrumentation.txt" -Raw
    $result.terminalSuccessCases = [regex]::Matches($raw,'(?m)^INSTRUMENTATION_STATUS_CODE: 0\s*$').Count
    $result.passed = $result.adbExitCode -eq 0 -and $result.terminalSuccessCases -eq 1 -and $raw -match 'OK \(1 test\)' -and
        $raw -notmatch 'INSTRUMENTATION_STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED|INSTRUMENTATION_STATUS: (?:ignored|assumptionFailure)'
    if (-not $result.passed) {
        & $adb -s $serial logcat -d -t 1500 2>&1 | Set-Content "$folder\failure-logcat.txt" -Encoding utf8NoBOM
        throw 'Native acceptance failed; raw results retained.'
    }
    Invoke-Adb @('pull','/sdcard/Android/data/io.github.stopcran.kanji/files/n1-094-correction-686.json',"$folder\n1-094-correction-686.json") | Out-Null
    Assert-CleanHeads
} catch {
    $result.failure = $_.Exception.Message
    $result.exactError = ($_ | Format-List * -Force | Out-String)
    Write-Output "CORRECTION686_FAILURE=$($result.failure)"
} finally {
    if ($emulator) {
        if (-not $qemuPid) {
            $child = @(Get-CimInstance Win32_Process -Filter "ParentProcessId=$($emulator.Id)" | Where-Object { $_.Name -like 'qemu-system*' })
            if ($child.Count -eq 1) { $qemuPid = $child[0].ProcessId; $result.qemuPid = $qemuPid }
        }
        $current = if ($qemuPid) { Get-CimInstance Win32_Process -Filter "ProcessId=$qemuPid" }
        if ($current -and $current.ParentProcessId -eq $emulator.Id) {
            & $adb -s $serial emu kill 2>&1 | Add-Content "$folder\adb-operations.txt" -Encoding utf8
            $result.stopAdbExitCode = $LASTEXITCODE
            $emulator.WaitForExit(30000) | Out-Null
        }
        $result.ownedHelperStopped = -not (Get-Process -Id $emulator.Id -ErrorAction SilentlyContinue)
        $result.ownedQemuStopped = if ($qemuPid) { -not (Get-Process -Id $qemuPid -ErrorAction SilentlyContinue) } else { $null }
    }
    $result.completedAt = [DateTimeOffset]::Now.ToString('o')
    $result | ConvertTo-Json -Depth 10 | Set-Content $receipt -Encoding utf8NoBOM
}
[pscustomobject]$result | Select-Object execution,batch,compiled,passed,failure,terminalSuccessCases,parentEmulatorPid,qemuPid,ownedHelperStopped,ownedQemuStopped | ConvertTo-Json
if (-not $result.passed -or $result.failure) { exit 1 }
