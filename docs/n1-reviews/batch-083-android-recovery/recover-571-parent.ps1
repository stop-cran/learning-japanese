$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$content = Join-Path $workspace 'learning-japanese'
$android = Join-Path $workspace 'kanji-cards-android'
$lock = [IO.File]::Open((Join-Path $control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $path = Join-Path $control 'progress.json'
    $progress = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
    if ($progress.checkpoint -ne 571 -or $progress.batch -ne '083' -or
        $progress.status -ne 'blocked' -or $progress.remainingAdditions -ne 1119 -or
        $progress.lastPublishedCommit -ne '21a5cb1328aadd437139a6b850f07298a2e2985d') {
        throw 'Checkpoint changed.'
    }
    foreach ($repository in @(
        @{ path = $content; head = 'c3ebb45896b3637ad784ba33d89e8fff3356925a' },
        @{ path = $android; head = '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' }
    )) {
        if ((git -C $repository.path rev-parse HEAD) -ne $repository.head -or
            (git -C $repository.path log -1 --format=%G?) -ne 'G' -or
            (git -C $repository.path status --porcelain)) { throw 'Unexpected worktree state.' }
    }
    $execution = Get-Content -LiteralPath (Join-Path $content 'docs\n1-sources\execution-571.json') -Raw | ConvertFrom-Json
    foreach ($artifact in $execution.provenance) {
        foreach ($copy in @((Join-Path $content $artifact.archive))) {
            if ((Get-FileHash -LiteralPath $copy).Hash.ToLowerInvariant() -ne $artifact.sha256) {
                throw 'Original571 evidence changed.'
            }
        }
        if ((Get-FileHash -LiteralPath (Join-Path $control 'run-571-android.ps1')).Hash.ToLowerInvariant() -ne
            $execution.provenance[0].sha256) { throw 'Original failed wrapper changed.' }
        $operationalHelper = Join-Path $control 'checkpoint-571.py'
        if ((Get-FileHash -LiteralPath $operationalHelper).Hash.ToLowerInvariant() -ne
            'f71d5a28b33c06a275a2c51f00401d60a67bd3ba416dcfe0423e02e58d234484') {
            throw 'Operational helper changed since inspected post-archive correction.'
        }
    }
    $init = Join-Path $control 'batch-065-host-integration-heap.init.gradle'
    if ((Get-FileHash -LiteralPath $init).Hash.ToLowerInvariant() -ne
        '438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24') {
        throw 'Qualified HOST heap changed.'
    }
    $receiptPath = Join-Path $control 'batch-083-parent-android-recovery.json'
    $receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
    if ($receipt.checkpoint -ne 571 -or $receipt.batch -ne '083' -or
        $receipt.androidHead -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
        $receipt.localContentHead -ne 'c3ebb45896b3637ad784ba33d89e8fff3356925a' -or
        $receipt.exitCode -ne 0 -or $receipt.tasks -ne '41 actionable tasks: 41 executed' -or
        @($receipt.tests).Count -ne 2) { throw 'Fresh receipt mismatch.' }
    $expectedNames = @(
        'hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent',
        'completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent',
        'parsesRealContentRepoWhenPresent',
        'contentRareCharactersAreCoveredByBundledFont'
    )
    $actualNames = @($receipt.tests | ForEach-Object { $_.caseNames })
    if (@(Compare-Object $expectedNames $actualNames).Count) { throw 'Named cases mismatch.' }
    $directory = Join-Path $control 'artifacts\batch-083-parent-lock-recovery'
    if ((Get-Content -LiteralPath (Join-Path $directory 'exit.txt') -Raw).Trim() -ne '0') {
        throw 'Actual Gradle exit mismatch.'
    }
    $started = [DateTimeOffset]::Parse((Get-Content -LiteralPath (Join-Path $directory 'start.txt') -Raw).Trim())
    foreach ($test in $receipt.tests) {
        $timestamp = [DateTimeOffset]::Parse($test.timestamp, [Globalization.CultureInfo]::InvariantCulture,
            [Globalization.DateTimeStyles]::AssumeUniversal)
        if ($test.failures -or $test.errors -or $test.skipped -or
            $timestamp -lt $started) { throw 'Invalid fresh results.' }
        foreach ($copy in @($test.sourcePath, $test.artifactPath)) {
            if ((Get-FileHash -LiteralPath $copy).Hash.ToLowerInvariant() -ne $test.sha256) {
                throw 'Fresh source/copied XML mismatch.'
            }
        }
    }
    $snapshot = Join-Path $directory 'progress-before-parent-recovery.json'
    if (Test-Path -LiteralPath $snapshot) { throw 'Do not overwrite recovery snapshot.' }
    Copy-Item -LiteralPath $path -Destination $snapshot
    $progress | Add-Member -NotePropertyName historicalExecution571LockBlocker -NotePropertyValue $progress.blocker
    $progress | Add-Member -NotePropertyName historicalExecution571LockNextAction -NotePropertyValue $progress.nextAction
    $progress | Add-Member -NotePropertyName parentBatch083AndroidRecovery -NotePropertyValue $receipt
    $disposition = [ordered]@{
        verifiedAt = [DateTimeOffset]::Now.ToString('o')
        originalFailure = 'Child attempted parent-only exclusive acquisition; zero tests ran. Original evidence retained, not retroaccepted.'
        operationalHelperDifference = 'Archived checkpoint-571.py hash86e555 remains exact. Existing control copy hashf71d5a differs: finish correctly records contentTestedCommit null on zero-test block, preservedContentCommit, plus verify-blocked mode. Direct diff inspected before recovery; do not overwrite either or rerun helper. Failed wrapper and all archived evidence match original hashes.'
        ownership = 'runner.ps1, not read-only supervise.ps1, owned the original lock. v100 exited before this parent recovery acquired exclusivity.'
        prevention = 'Every launcher prompt now requires runner-lock-role-notes.txt. Normal child wrappers must retain checks without reacquiring the live parent lock.'
        lockImplementationUnchanged = $true
        qualifiedHostHeapUnchanged = $true
        freshGate = $receiptPath
        scope = 'HOST recovery only; signed archival, native, visual, integration and publication remain pending.'
        provenance = @('runner.ps1', 'runner-lock-role-notes.txt', 'run-571-parent-android.ps1',
            'verify-parent-android.ps1', 'recover-571-parent.ps1', 'checkpoint-571.py') | ForEach-Object {
            $file = Join-Path $control $_
            @{ path = $file; sha256 = (Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant() }
        }
    }
    $dispositionPath = Join-Path $control 'batch-083-parent-lock-disposition.json'
    if (Test-Path -LiteralPath $dispositionPath) { throw 'Do not overwrite disposition.' }
    $disposition | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $dispositionPath -Encoding utf8NoBOM
    $progress | Add-Member -NotePropertyName parentExecution571LockDisposition -NotePropertyValue $disposition
    $progress.status = 'continue'
    $progress.blocker = $null
    $progress.stage = 'batch-083-parent-lock-recovery-android-passed-pending-signed-evidence'
    $progress.nextAction = 'SAME083571 parent lock-role disposition and fresh HOST gate complete. Read control\batch-083-parent-lock-disposition.json, batch-083-parent-android-recovery.json and runner-lock-role-notes.txt. Original571 child wrapper failed File.Open BEFORE Gradle, zero tests; failed wrapper and archived helper/diagnostic/provenance/full history retained unchanged, NOT retroaccepted. Operational control helper already has post-archive zero-test attribution correction and verify-blocked mode; inspected diff and exact separate hashes recorded in disposition, neither copy overwritten or rerun. Actual owner was runner.ps1 (not read-only supervise.ps1); oldv100 exited, then parent acquired available exclusive lock and ran FIRST actual083 unchanged3RealContent+1RareHan at qualified065HOST2g, one worker/reruntasks. Actual exit0,3m19s,41tasks41executed; independent XML names/counts/freshUTC/root/source-copyhashes/whollyclean signed contentc3ebb45896b3637ad784ba33d89e8fff3356925a and Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d verified. No heap/policy/lock flags or production changes. This live launcher owns runner.lock throughout child lifetime: child wrappers MUST NOT reacquire/delete/unlock it; keep all checkpoint/signed-head/clean-state/acceptance guards. FIRST archive actual recovery receipt/XML/logs/helper/disposition/qualification and normally SIGNED LOCAL recoveredAndroid evidence BEFORE083native preparation. Do not rerun HOST or initial textual reviews absent new concern. Preserve textualclosure677c9864340303be42a4bd77aa21d5229167ddb8/teaching4b8bfcc4bc4fff4c73185a8cc6c27d4cb5736efc/reconciliation/sourcefamilies/fullreadings and all29Han/fourfonts including 冫/夌/阝/隹. Android exact1c test-onlybaseline atop frozenproductionf9; do not revert to literalf9 or adopt newer app behavior. HOSTinit never used for native. Then full frozen productionContentSyncONCE, all29Han/fourfonts/Paint/directPNG/legibility/lookalikes/selection/meaning/curatedreadings/drawing/articles/reciprocallinks/SystemBack/offline/persistence, freshlocalANDremoteportownership includingTimeWait, explicitadbserial, ownedreadonlyAVD5580/5581 only, actualnamedterminal0everycase/noskips/no-2/-3. ORIGINALserialtwo-familydependentvisual before current-main integration. Latestmain/allcurrentcombinedPython(actual372 at082, recompute if changed)/validator/vocabulary/manifest/exactreviewedquizguards/originalarchivebudgets, normal signedownerfastforwardpush/exactpublicSHA/actualterminalgreenCI/everyimmutableZIPruntimehash/terminalreceipts/ownerissue60 BEFORE084. Preserve all original source/review/process/read-depth/viewport/fallback/MLKit/phone/generalrelease/whole-set limits. Scopedreviewer --add-dir control; no optional historicalsessionhelpers. Exactlyone coordinator/atmostone actualreviewer; all heavy stages sequential. Published109/1228,remaining1119/latestpublic21a5cb1328aadd437139a6b850f07298a2e2985d/greenCI42242423726;083NOTdelivered. Full progress history preserved; runtime/journal launcher-owned.'
    $temporary = "$path.parent571.tmp"
    $progress | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $temporary -Encoding utf8NoBOM
    $check = Get-Content -LiteralPath $temporary -Raw | ConvertFrom-Json
    if ($check.checkpoint -ne 571 -or $check.status -ne 'continue' -or
        $check.remainingAdditions -ne 1119 -or -not $check.historicalExecution571LockBlocker) {
        throw 'Recovery invariant failed.'
    }
    Move-Item -LiteralPath $temporary -Destination $path -Force
    @{ checkpoint = 571; status = 'continue'; freshTests = 4; remaining = 1119 } | ConvertTo-Json
} finally {
    $lock.Dispose()
}
