$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$session = 'fba96d45-7b95-46df-9ccf-c5222c8b627e'
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
$adb = "$env:ANDROID_HOME\platform-tools\adb.exe"
$serial = 'emulator-5580'
$folder = "$control\artifacts\batch-091-native-revision-attempt-654"
$receipt = "$control\batch-091-native-revision-attempt-654-execution.json"
if ((Test-Path $folder) -or (Test-Path $receipt)) { throw 'Existing attempt; never overwrite.' }
$compiled = Get-Content "$control\batch-091-revised-compiled-654.json" -Raw | ConvertFrom-Json
$preparation = $compiled.fixtureVerification
$result = [ordered]@{
    execution=654; batch='091'; startedAt=[DateTimeOffset]::Now.ToString('o')
    serial=$serial; contentSnapshot=$preparation.contentSnapshot; androidSnapshot=$preparation.androidSnapshot
    coordinatorHead='fe3ec10b34e5b26fd286d7a79b33b6b6a03afda6'
    appApk=$compiled.appApk.path; appApkSha256=$compiled.appApk.sha256
    testApk=$compiled.testApk.path; testApkSha256=$compiled.testApk.sha256
    fixtureSha256=$preparation.fixtureSha256; archiveSha256=$preparation.archiveSha256
    nativeExecuted=$false; passed=$false; failure=$null
    guestOrAppHeapChanged=$false; guardsChanged=$false; parentLockTouched=$false
}
New-Item -ItemType Directory -Path $folder | Out-Null
$emulator = $null
$qemuPid = $null
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
    $checkpoint = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
    if ($checkpoint.checkpoint -ne 653 -or $checkpoint.status -ne 'continue' -or
        $checkpoint.batch -ne '091' -or $checkpoint.stage -ne 'batch-091-revised-native-confirmation-in-progress') { throw 'Checkpoint changed.' }
    foreach ($entry in @(@{root=$content;head=$result.coordinatorHead}, @{root=$android;head=$preparation.androidSnapshot})) {
        if ((git -C $entry.root rev-parse HEAD) -ne $entry.head -or $LASTEXITCODE -ne 0) { throw 'Signed head changed.' }
        if ((git -C $entry.root status --porcelain) -or $LASTEXITCODE -ne 0) { throw 'Worktree not wholly clean.' }
        if ((git -C $entry.root log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature not good.' }
    }
    if ((git -C $android diff $preparation.productionBaseline HEAD -- app/src/main core/src/main gradle.properties) -or
        $LASTEXITCODE -ne 0) { throw 'Production baseline changed.' }
    foreach ($entry in @(@{path=$preparation.archive;hash=$preparation.archiveSha256},
        @{path=$preparation.fixture;hash=$preparation.fixtureSha256},
        @{path=$compiled.testApk.path;hash=$compiled.testApk.sha256},
        @{path=$compiled.appApk.path;hash=$compiled.appApk.sha256})) {
        if ((Get-FileHash -LiteralPath $entry.path).Hash.ToLowerInvariant() -ne $entry.hash) { throw 'Frozen input changed.' }
    }
    $runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
    if ($runner.pid -ne 19008 -or $runner.status -ne 'running' -or $runner.sessionId -ne $session) { throw 'Parent ownership uncertain.' }
    $ancestor = $PID
    $ancestry = @()
    while ($ancestor -gt 0) {
        $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
        if (-not $process) { break }
        $ancestry += $process | Select-Object ProcessId,ParentProcessId,Name
        if ($ancestor -eq $runner.pid) { break }
        $ancestor = $process.ParentProcessId
    }
    if ($ancestor -ne $runner.pid) { throw 'Parent not live ancestor; yield without lock access.' }
    $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($runner.pid)"
    $encoded = [regex]::Match($parent.CommandLine, '-EncodedCommand\s+(\S+)')
    if (-not $encoded.Success -or [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded.Groups[1].Value)) -notlike "*$control\runner.ps1*") {
        throw 'Launcher command ownership uncertain; no lock access attempted.'
    }
    $result.launcherCommandMatches = $true
    $result.parentAncestry = $ancestry
    $devices = (& $adb devices -l 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) { throw 'adb device inspection failed.' }
    $connections = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object {
        $_.LocalPort -in @(5580,5581) -or $_.RemotePort -in @(5580,5581)
    } | Select-Object LocalAddress,RemoteAddress,LocalPort,RemotePort,State,OwningProcess)
    $result.preexistingEmulators = @(Get-CimInstance Win32_Process | Where-Object {
        $_.Name -match 'emulator|qemu'
    } | Select-Object ProcessId,ParentProcessId,Name,CommandLine)
    $result.prelaunch = @{verifiedAt=[DateTimeOffset]::Now.ToString('o');devices=$devices;connections=$connections}
    if ($devices -match 'emulator-5580' -or $connections.Count -gt 0) { throw '5580/5581 occupied; no helper launched.' }
    $arguments = @('-avd','N3_Acceptance_20261029','-port','5580','-read-only','-no-snapshot','-no-window','-no-audio',
        '-gpu','host','-feature','-Vulkan','-memory','2048','-cores','2')
    $emulator = Start-Process -FilePath "$env:ANDROID_HOME\emulator\emulator.exe" -ArgumentList $arguments -PassThru `
        -RedirectStandardOutput "$folder\emulator-stdout.txt" -RedirectStandardError "$folder\emulator-stderr.txt"
    $result.parentEmulatorPid = $emulator.Id
    $result.emulatorArguments = $arguments
    $deadline = [DateTimeOffset]::Now.AddMinutes(4)
    do {
        Start-Sleep -Seconds 5
        $boot = (& $adb -s $serial shell getprop sys.boot_completed 2>$null | Out-String).Trim()
        if ($emulator.HasExited) { throw 'Owned emulator exited before boot.' }
    } until ($boot -eq '1' -or [DateTimeOffset]::Now -gt $deadline)
    if ($boot -ne '1') { throw 'Owned emulator boot deadline exceeded.' }
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
    Invoke-Adb @('install','-r','-t',$compiled.appApk.path) | Out-Null
    Invoke-Adb @('install','-r','-t',$compiled.testApk.path) | Out-Null
    Invoke-Adb @('shell','svc','wifi','disable') | Out-Null
    Invoke-Adb @('shell','svc','data','disable') | Out-Null
    Start-Sleep -Seconds 5
    $result.network = (Invoke-Adb @('shell','dumpsys','connectivity') | Select-String -SimpleMatch 'Active default network:' | Out-String).Trim()
    if ($result.network -ne 'Active default network: none') { throw 'Offline precondition missing.' }
    $result.nativeExecuted = $true
    $classes = 'io.github.stopcran.kanji.ui.N1Batch091ArticleTest'
    $result.instrumentationCommand = "adb -s $serial shell am instrument -w -r -e n1Disposable true -e class $classes io.github.stopcran.kanji.test/androidx.test.runner.AndroidJUnitRunner"
    $log = "$folder\instrumentation.txt"
    & $adb -s $serial shell am instrument -w -r -e n1Disposable true -e class $classes `
        'io.github.stopcran.kanji.test/androidx.test.runner.AndroidJUnitRunner' 2>&1 | Tee-Object -FilePath $log
    $result.adbExitCode = $LASTEXITCODE
    $raw = Get-Content $log -Raw
    $result.terminalSuccessCases = [regex]::Matches($raw,'(?m)^INSTRUMENTATION_STATUS_CODE: 0\s*$').Count
    $result.passed = $result.adbExitCode -eq 0 -and $result.terminalSuccessCases -eq 1 -and
        $raw -match 'OK \(1 test\)' -and $raw -notmatch 'INSTRUMENTATION_STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED'
    $remote = '/sdcard/Android/data/io.github.stopcran.kanji/files'
    $files = @(Invoke-Adb @('shell','ls',$remote) | Where-Object { $_ -match '^n1-091-[\p{L}\p{N}-]+\.(png|json|txt)$' })
    foreach ($file in $files) { Invoke-Adb @('pull',"$remote/$file",(Join-Path $folder $file)) | Out-Null }
    $result.artifacts = @($files)
    if (-not $result.passed) {
        & $adb -s $serial logcat -d -t 1500 2>&1 | Set-Content "$folder\failure-logcat.txt" -Encoding utf8NoBOM
        throw 'Native acceptance failed; raw results preserved.'
    }
} catch {
    $result.failure = $_.Exception.Message
    $result.exactError = ($_ | Format-List * -Force | Out-String)
    Write-Output "NATIVE_ATTEMPT_FAILURE=$($result.failure)"
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
    Copy-Item $receipt "$folder\execution.json"
}
[pscustomobject]$result | Select-Object execution,batch,passed,failure,terminalSuccessCases,parentEmulatorPid,qemuPid,ownedHelperStopped,ownedQemuStopped | ConvertTo-Json
if (-not $result.passed) { exit 1 }
