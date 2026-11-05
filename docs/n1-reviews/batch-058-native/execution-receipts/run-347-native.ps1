$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$content = Join-Path $workspace 'learning-japanese'
$android = Join-Path $workspace 'kanji-cards-android'
$sdk = 'C:\Users\stop-\AppData\Local\Android\Sdk'
$adb = Join-Path $sdk 'platform-tools\adb.exe'
$serial = 'emulator-5580'
$folder = Join-Path $control 'artifacts\batch-058-native-attempt-1'
$log = Join-Path $folder 'instrumentation.txt'
$receipt = Join-Path $control 'batch-058-native-attempt-1-execution.json'
if ((Test-Path $folder) -or (Test-Path $receipt)) { throw 'Existing native attempt; refusing overwrite.' }
$runner = Get-Content (Join-Path $control 'runner.json') -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.sessionId -ne '0721c431-c314-4900-86b9-000f3b395fa7') { throw 'Unexpected supervisor session.' }
$ancestor = $PID
$owned = $false
while ($ancestor -gt 0) {
    if ($ancestor -eq $runner.pid) { $owned = $true; break }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if (-not $process) { break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Recorded supervisor is not this coordinator ancestor.' }
$preparation = Get-Content (Join-Path $content 'docs\n1-sources\batch-058-native-preparation.json') -Raw | ConvertFrom-Json
$compiled = Get-Content (Join-Path $content 'docs\n1-sources\execution-346.json') -Raw | ConvertFrom-Json
$testApk = $compiled.compilation.apk
$appApk = Join-Path $android 'app\build\outputs\apk\debug\app-debug.apk'
foreach ($entry in @(@{path=$preparation.archive;hash=$preparation.archiveSha256},
                    @{path=$preparation.fixture;hash=$preparation.fixtureSha256},
                    @{path=$testApk;hash=$compiled.compilation.apkSha256},
                    @{path=$appApk;hash='0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407'})) {
    if ((Get-FileHash -LiteralPath $entry.path).Hash.ToLowerInvariant() -ne $entry.hash) { throw "Frozen input changed: $($entry.path)" }
}
if ((git -C $android rev-parse HEAD) -ne $preparation.androidSnapshot -or (git -C $android status --porcelain)) { throw 'Android baseline changed.' }
if ((git -C $content rev-parse HEAD) -ne '07fe24323c2775058a659502817d08928ea2401a' -or (git -C $content status --porcelain)) { throw 'Content snapshot changed.' }
$result = [ordered]@{
    execution=347;batch='058';attempt=1;startedAt=[DateTimeOffset]::Now.ToString('o')
    serial=$serial;contentSnapshot=$preparation.contentSnapshot;androidSnapshot=$preparation.androidSnapshot
    appApk=$appApk;appApkSha256=(Get-FileHash $appApk).Hash.ToLowerInvariant()
    testApk=$testApk;testApkSha256=$compiled.compilation.apkSha256;fixtureSha256=$preparation.fixtureSha256
    archiveSha256=$preparation.archiveSha256;nativeExecuted=$false;passed=$false;failure=$null
}
New-Item -ItemType Directory -Path $folder | Out-Null
Copy-Item -LiteralPath $preparation.fixture -Destination $folder
$emulator = $null
$qemuPid = $null
function Invoke-Adb {
    param([string[]]$Arguments)
    $output = & $adb -s $serial @Arguments 2>&1
    $code = $LASTEXITCODE
    $output | Add-Content (Join-Path $folder 'adb-operations.txt') -Encoding utf8
    if ($code -ne 0) { throw "adb failed ($code): $($Arguments -join ' '): $output" }
    return $output
}
try {
    $devices = (& $adb devices -l 2>&1 | Out-String)
    if ($LASTEXITCODE -ne 0) { throw "adb devices failed: $devices" }
    $connections = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object { $_.LocalPort -in @(5580,5581) -or $_.RemotePort -in @(5580,5581) } | Select-Object LocalAddress,RemoteAddress,LocalPort,RemotePort,State,OwningProcess)
    $result.prelaunch = @{verifiedAt=[DateTimeOffset]::Now.ToString('o');devices=$devices;connections=$connections}
    if ($devices -match 'emulator-5580' -or $connections.Count -gt 0) { throw '5580/5581 occupied; no helper launched.' }
    $arguments = @('-avd','N3_Acceptance_20261029','-port','5580','-read-only','-no-snapshot','-no-window','-no-audio','-gpu','host','-feature','-Vulkan','-memory','2048','-cores','2')
    $emulator = Start-Process -FilePath (Join-Path $sdk 'emulator\emulator.exe') -ArgumentList $arguments -PassThru `
        -RedirectStandardOutput (Join-Path $folder 'emulator-stdout.txt') -RedirectStandardError (Join-Path $folder 'emulator-stderr.txt')
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
    if ($qemu.Count -ne 1) { throw 'Cannot establish exact owned qemu child.' }
    $qemuPid = $qemu[0].ProcessId
    $result.qemuPid = $qemuPid
    $listeners = @(Get-NetTCPConnection -ErrorAction Stop | Where-Object { $_.LocalPort -in @(5580,5581) -and $_.State -eq 'Listen' })
    if (-not $listeners -or @($listeners | Where-Object { $_.OwningProcess -ne $qemuPid }).Count -gt 0) { throw 'Port ownership differs from owned helper.' }
    $result.listeners = @($listeners | Select-Object LocalPort,OwningProcess)
    Write-Output "OWNED_HELPER_RESPONSIVE serial=$serial parent=$($emulator.Id) qemu=$qemuPid boot=$boot"
    Start-Sleep -Seconds 90
    $result.fingerprint = (Invoke-Adb @('shell','getprop','ro.build.fingerprint') | Out-String).Trim()
    $result.heapGrowth = (Invoke-Adb @('shell','getprop','dalvik.vm.heapgrowthlimit') | Out-String).Trim()
    $result.heapSize = (Invoke-Adb @('shell','getprop','dalvik.vm.heapsize') | Out-String).Trim()
    $result.meminfo = (Invoke-Adb @('shell','cat','/proc/meminfo') | Select-Object -First 1 | Out-String).Trim()
    if ($result.fingerprint -ne 'google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys' -or $result.heapGrowth -ne '192m' -or $result.heapSize -ne '576m') { throw 'Unexpected supported guest identity/heaps.' }
    Invoke-Adb @('install','-r','-t',$appApk) | Out-Null
    Invoke-Adb @('install','-r','-t',$testApk) | Out-Null
    Invoke-Adb @('shell','svc','wifi','disable') | Out-Null
    Invoke-Adb @('shell','svc','data','disable') | Out-Null
    Start-Sleep -Seconds 5
    $result.network = (Invoke-Adb @('shell','dumpsys','connectivity') | Select-String 'Active default network:' | Out-String).Trim()
    if ($result.network -ne 'Active default network: none') { throw 'Offline precondition not established.' }
    $result.nativeExecuted = $true
    $classes = 'io.github.stopcran.kanji.ui.N1Batch058GlyphTest,io.github.stopcran.kanji.ui.N1Batch058ArticleTest'
    & $adb -s $serial shell am instrument -w -r -e n1Disposable true -e class $classes 'io.github.stopcran.kanji.test/androidx.test.runner.AndroidJUnitRunner' 2>&1 | Tee-Object -FilePath $log
    $result.adbExitCode = $LASTEXITCODE
    $raw = Get-Content $log -Raw
    $result.terminalSuccessCases = [regex]::Matches($raw,'(?m)^INSTRUMENTATION_STATUS_CODE: 0\s*$').Count
    $result.passed = $result.adbExitCode -eq 0 -and $result.terminalSuccessCases -eq 2 -and $raw -match 'OK \(2 tests\)' -and $raw -notmatch 'INSTRUMENTATION_STATUS_CODE: -[234]'
    $remote = '/sdcard/Android/data/io.github.stopcran.kanji/files'
    $files = @(Invoke-Adb @('shell','ls',$remote) | Where-Object { $_ -match '^n1-058-[a-zA-Z-]+\.(png|json|txt)$' })
    foreach ($file in $files) { Invoke-Adb @('pull',"$remote/$file",(Join-Path $folder $file)) | Out-Null }
    $result.artifacts = @($files)
    if (-not $result.passed) { throw 'Native acceptance did not pass; raw result/artifacts preserved.' }
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
            & $adb -s $serial emu kill 2>&1 | Add-Content (Join-Path $folder 'adb-operations.txt') -Encoding utf8
            $result.stopAdbExitCode = $LASTEXITCODE
            $emulator.WaitForExit(30000) | Out-Null
        }
        $result.ownedHelperStopped = -not (Get-Process -Id $emulator.Id -ErrorAction SilentlyContinue)
        $result.ownedQemuStopped = if ($qemuPid) { -not (Get-Process -Id $qemuPid -ErrorAction SilentlyContinue) } else { $null }
    }
    $result.completedAt = [DateTimeOffset]::Now.ToString('o')
    $result | ConvertTo-Json -Depth 10 | Set-Content $receipt -Encoding utf8NoBOM
    Copy-Item $receipt (Join-Path $folder 'execution.json')
}
$result | ConvertTo-Json -Depth 6
if (-not $result.passed) { exit 1 }
