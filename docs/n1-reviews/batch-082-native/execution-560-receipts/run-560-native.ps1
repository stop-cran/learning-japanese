$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$content = Join-Path $workspace 'learning-japanese'
$android = Join-Path $workspace 'kanji-cards-android'
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
$adb = "$env:ANDROID_HOME\platform-tools\adb.exe"
$serial = 'emulator-5580'
$folder = "$control\artifacts\batch-082-native-attempt-1"
$receipt = "$control\batch-082-native-attempt-1-execution.json"
if ((Test-Path $folder) -or (Test-Path $receipt)) { throw 'Existing attempt; refusing overwrite.' }
$preparation = Get-Content "$content\docs\n1-sources\batch-082-native-fixture-verification.json" -Raw | ConvertFrom-Json
$compiled = Get-Content "$content\docs\n1-sources\execution-559.json" -Raw | ConvertFrom-Json
$testApk = $compiled.compile.apk
$appApk = $compiled.compile.appApk
foreach ($entry in @(@{path=$preparation.archive;hash=$preparation.archiveSha256},
    @{path=$preparation.fixture;hash=$preparation.fixtureSha256},
    @{path=$testApk;hash=$compiled.compile.apkSha256},
    @{path=$appApk;hash=$compiled.compile.appApkSha256})) {
    if ((Get-FileHash -LiteralPath $entry.path).Hash.ToLowerInvariant() -ne $entry.hash) { throw "Frozen input changed: $($entry.path)" }
}
if ((git -C $android rev-parse HEAD) -ne $preparation.androidSnapshot -or (git -C $android status --porcelain)) { throw 'Android changed.' }
if ((git -C $content rev-parse HEAD) -ne '35f7e9944c74a9d7a00e3beb1f96625fbf85a622' -or (git -C $content status --porcelain)) { throw 'Content changed.' }
$result = [ordered]@{
    execution=560;batch='082';attempt=1;startedAt=[DateTimeOffset]::Now.ToString('o')
    serial=$serial;contentSnapshot=$preparation.contentSnapshot;androidSnapshot=$preparation.androidSnapshot
    coordinatorHead='35f7e9944c74a9d7a00e3beb1f96625fbf85a622'
    appApk=$appApk;appApkSha256=$compiled.compile.appApkSha256
    testApk=$testApk;testApkSha256=$compiled.compile.apkSha256;fixtureSha256=$preparation.fixtureSha256
    archiveSha256=$preparation.archiveSha256;nativeExecuted=$false;passed=$false;failure=$null
    hostHeapInitUsed=$false;guestOrAppHeapChanged=$false;guardsChanged=$false
}
New-Item -ItemType Directory -Path $folder | Out-Null
Copy-Item -LiteralPath $preparation.fixture -Destination $folder
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
    $devices = (& $adb devices -l 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) { throw "adb devices failed: $devices" }
    $connections = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object { $_.LocalPort -in @(5580,5581) -or $_.RemotePort -in @(5580,5581) } | Select-Object LocalAddress,RemoteAddress,LocalPort,RemotePort,State,OwningProcess)
    $result.preexistingEmulators = @(Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'emulator|qemu' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine)
    $result.prelaunch = @{verifiedAt=[DateTimeOffset]::Now.ToString('o');devices=$devices;connections=$connections}
    if ($devices -match 'emulator-5580' -or $connections.Count -gt 0) { throw '5580/5581 occupied; no helper launched.' }
    $arguments = @('-avd','N3_Acceptance_20261029','-port','5580','-read-only','-no-snapshot','-no-window','-no-audio','-gpu','host','-feature','-Vulkan','-memory','2048','-cores','2')
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
    if ($qemu.Count -ne 1) { throw 'Cannot establish exact owned QEMU child.' }
    $qemuPid = $qemu[0].ProcessId
    $result.qemuPid = $qemuPid
    $listeners = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object { $_.LocalPort -in @(5580,5581) -and $_.State -eq 'Listen' })
    if (-not $listeners -or @($listeners | Where-Object { $_.OwningProcess -ne $qemuPid }).Count -gt 0) { throw 'Port ownership differs from helper.' }
    $result.listeners = @($listeners | Select-Object LocalPort,OwningProcess)
    Write-Output "OWNED_HELPER_RESPONSIVE serial=$serial parent=$($emulator.Id) qemu=$qemuPid boot=$boot"
    Start-Sleep -Seconds 90
    $result.fingerprint = (Invoke-Adb @('shell','getprop','ro.build.fingerprint') | Out-String).Trim()
    $result.heapGrowth = (Invoke-Adb @('shell','getprop','dalvik.vm.heapgrowthlimit') | Out-String).Trim()
    $result.heapSize = (Invoke-Adb @('shell','getprop','dalvik.vm.heapsize') | Out-String).Trim()
    if ($result.fingerprint -ne 'google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys' -or $result.heapGrowth -ne '192m' -or $result.heapSize -ne '576m') { throw 'Unexpected guest identity/heaps.' }
    Invoke-Adb @('install','-r','-t',$appApk) | Out-Null
    Invoke-Adb @('install','-r','-t',$testApk) | Out-Null
    Invoke-Adb @('shell','svc','wifi','disable') | Out-Null
    Invoke-Adb @('shell','svc','data','disable') | Out-Null
    Start-Sleep -Seconds 5
    $result.network = (Invoke-Adb @('shell','dumpsys','connectivity') | Select-String -SimpleMatch 'Active default network:' | Out-String).Trim()
    if ($result.network -ne 'Active default network: none') { throw 'Offline precondition missing.' }
    $result.nativeExecuted = $true
    $classes = 'io.github.stopcran.kanji.ui.N1Batch082GlyphTest,io.github.stopcran.kanji.ui.N1Batch082ArticleTest'
    $result.instrumentationCommand = "adb -s $serial shell am instrument -w -r -e n1Disposable true -e class $classes io.github.stopcran.kanji.test/androidx.test.runner.AndroidJUnitRunner"
    $log = "$folder\instrumentation.txt"
    & $adb -s $serial shell am instrument -w -r -e n1Disposable true -e class $classes 'io.github.stopcran.kanji.test/androidx.test.runner.AndroidJUnitRunner' 2>&1 | Tee-Object -FilePath $log
    $result.adbExitCode = $LASTEXITCODE
    $raw = Get-Content $log -Raw
    $result.terminalSuccessCases = [regex]::Matches($raw,'(?m)^INSTRUMENTATION_STATUS_CODE: 0\s*$').Count
    $result.terminalCases = @([regex]::Matches($raw, '(?ms)INSTRUMENTATION_STATUS: class=([^\r\n]+)\r?\n(?:(?!INSTRUMENTATION_STATUS_CODE:).)*?INSTRUMENTATION_STATUS: test=([^\r\n]+)\r?\n(?:(?!INSTRUMENTATION_STATUS_CODE:).)*?INSTRUMENTATION_STATUS_CODE: 0\s*$') | ForEach-Object {
        @{class=$_.Groups[1].Value;test=$_.Groups[2].Value;status=0}
    })
    $result.passed = $result.adbExitCode -eq 0 -and $result.terminalSuccessCases -eq 2 -and $result.terminalCases.Count -eq 2 -and $raw -match 'OK \(2 tests\)' -and $raw -notmatch 'INSTRUMENTATION_STATUS_CODE: -[234]'
    $remote = '/sdcard/Android/data/io.github.stopcran.kanji/files'
    $files = @(Invoke-Adb @('shell','ls',$remote) | Where-Object { $_ -match '^n1-082-[\p{L}\p{N}-]+\.(png|json|txt)$' })
    foreach ($file in $files) { Invoke-Adb @('pull',"$remote/$file",(Join-Path $folder $file)) | Out-Null }
    $result.artifacts = @($files)
    if (-not $result.passed) {
        & $adb -s $serial logcat -d -t 1500 2>&1 | Set-Content "$folder\failure-logcat.txt" -Encoding utf8NoBOM
        throw 'Native acceptance failed; raw results preserved.'
    }
} catch {
    $result.failure = $_.Exception.Message
    $result.exactError = ($_ | Format-List * -Force | Out-String)
    $result.errorPosition = $_.InvocationInfo.PositionMessage
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
