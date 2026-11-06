$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$workspace = Split-Path $control -Parent
$content = Join-Path $workspace 'learning-japanese'
$android = Join-Path $workspace 'kanji-cards-android'
$lock = [IO.File]::Open((Join-Path $control 'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $path = Join-Path $control 'progress.json'
    $progress = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
    if ($progress.checkpoint -ne 557 -or $progress.batch -ne '082' -or
        $progress.status -ne 'blocked' -or $progress.remainingAdditions -ne 1120) {
        throw 'Checkpoint changed.'
    }
    $head = '1c1b7bf42cc91d820a93169f1088dc647ac51c0d'
    foreach ($repository in @(
        @{ path = $content; head = 'b9eb2fb52b6619c1810cc68e5da3ebbcddd6175b' },
        @{ path = $android; head = $head }
    )) {
        if ((git -C $repository.path rev-parse HEAD) -ne $repository.head -or
            (git -C $repository.path log -1 --format=%G?) -ne 'G' -or
            (git -C $repository.path status --porcelain)) { throw 'Unexpected worktree state.' }
    }
    $allowed = @('.github/copilot-instructions.md', 'docs/DESIGN.md',
        'core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt',
        'core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt',
        'core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixtureTest.kt')
    $changed = @(git -C $android diff --name-only f9b59a2bc5a203c6b4de26be50021a4c720dc22c HEAD)
    if (@(Compare-Object $allowed $changed).Count) { throw 'Unexpected pinned baseline delta.' }
    $execution = Get-Content -LiteralPath (Join-Path $content 'docs\n1-sources\execution-557.json') -Raw | ConvertFrom-Json
    foreach ($artifact in @($execution.rawAndArchivedProvenance) + @($execution.tests)) {
        $archived = Join-Path $content $artifact.archivedPath
        if ((Get-FileHash -LiteralPath $archived).Hash.ToLowerInvariant() -ne $artifact.sha256) {
            throw 'Historical failure evidence changed.'
        }
    }
    $init = Join-Path $control 'batch-065-host-integration-heap.init.gradle'
    if ((Get-FileHash -LiteralPath $init).Hash.ToLowerInvariant() -ne
        '438159ae22b313e8196a0bc011f72a3b17300146b219c5ffcc779c540a64be24') {
        throw 'Qualified HOST heap changed.'
    }
    $receipt = Get-Content -LiteralPath (Join-Path $control 'batch-082-parent-android-recovery.json') -Raw | ConvertFrom-Json
    if ($receipt.androidHead -ne $head -or $receipt.checkpoint -ne 557 -or
        $receipt.localContentHead -ne 'b9eb2fb52b6619c1810cc68e5da3ebbcddd6175b' -or
        $receipt.exitCode -ne 0 -or $receipt.tasks -ne '41 actionable tasks: 41 executed') {
        throw 'Fresh receipt mismatch.'
    }
    foreach ($test in $receipt.tests) {
        foreach ($copy in @($test.sourcePath, $test.artifactPath)) {
            if ((Get-FileHash -LiteralPath $copy).Hash.ToLowerInvariant() -ne $test.sha256) {
                throw 'Fresh source/copied XML mismatch.'
            }
        }
    }
    $directory = Join-Path $control 'artifacts\batch-082-parent-test-loader-recovery'
    if ((Get-Content -LiteralPath (Join-Path $directory 'exit.txt') -Raw).Trim() -ne '0') {
        throw 'Actual Gradle exit mismatch.'
    }
    [xml]$loader = Get-Content -LiteralPath (Join-Path $directory 'PublishableContentFixtureTest.xml') -Raw
    if ([int]$loader.testsuite.tests -ne 5 -or [int]$loader.testsuite.failures -or
        [int]$loader.testsuite.errors -or [int]$loader.testsuite.skipped) {
        throw 'Loader regression results mismatch.'
    }
    $ciRaw = gh api repos/stop-cran/kanji-cards-android/actions/runs/42222517447
    if ($LASTEXITCODE -ne 0) { throw 'CI retrieval failed.' }
    $ci = $ciRaw | ConvertFrom-Json
    if ($ci.head_sha -ne 'e46106de88892b6886f38199b5ca20f2134b27f6' -or
        $ci.status -ne 'completed' -or $ci.conclusion -ne 'success') { throw 'Exact green CI mismatch.' }
    $public = gh api repos/stop-cran/kanji-cards-android/commits/main | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0 -or $public.sha -ne $ci.head_sha -or
        -not $public.commit.verification.verified) { throw 'Signed public main mismatch.' }
    $qualification = [ordered]@{
        issue = 'https://github.com/stop-cran/kanji-cards-android/issues/130'
        mergedPr = 'https://github.com/stop-cran/kanji-cards-android/pull/131'
        verifiedAt = [DateTimeOffset]::Now.ToString('o')
        originalProductionBaseline = 'f9b59a2bc5a203c6b4de26be50021a4c720dc22c'
        qualifiedAndroidHead = $head
        signedSourcePatch = '751c471a03cd0c82e38a61a155739c3692a24f68'
        signedPublicMain = $ci.head_sha
        actualTerminalGreenCi = $ci.id
        ciEvent = $ci.event
        separateMainPushCiRun = 42224592996
        separateMainPushCiNotYetClaimedGreen = $true
        permittedDelta = $allowed
        productionSourcesUnchanged = $true
        fullReadingsAssertionsAndArchiveGuardsPreserved = $true
        contributorEvidencePreserved = $true
        loaderRegressions = 5
        freshNamedCorpusAndFontCases = 4
        failuresErrorsSkips = 0
        hostCoreTestMaxHeap = '2g'
        hostInit = $init
        scope = 'TEST-ONLY signed cherry-pick on frozen N1 app branch; no newer production/localization behavior adopted. Preserve original branch and historical OOMs. Not native/phone/whole-set acceptance.'
        invariant = 'Future N1 work uses qualifiedAndroidHead1c1b7bf, not literal oldf9b59a2. Oldf9 remains production ancestor, not current checkout HEAD. Same complete publishable corpus and all original assertions; no docs deletion or further heap increase. Pass exact AndroidHead to parent verifier. Native builds never use HOST init.'
        proof = $receipt
        artifacts = @(Get-ChildItem -LiteralPath $directory -File | ForEach-Object {
            @{ path = $_.FullName; sha256 = (Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant() }
        })
        implementation = @($allowed | ForEach-Object {
            $file = Join-Path $android $_
            @{ path = $file; sha256 = (Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant() }
        })
        parentVerifier = @{
            path = (Join-Path $control 'verify-parent-android.ps1')
            sha256 = (Get-FileHash -LiteralPath (Join-Path $control 'verify-parent-android.ps1')).Hash.ToLowerInvariant()
            delta = 'Optional explicit expected AndroidHead parameter only; default historicalf9 retained. Counts, timestamps, clean roots, source/copy hashes and task checks unchanged.'
        }
    }
    $qualificationPath = Join-Path $control 'batch-082-parent-test-loader-qualification.json'
    $qualification | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $qualificationPath -Encoding utf8NoBOM
    $progress | Add-Member -NotePropertyName historicalExecution557HostHeapBlocker -NotePropertyValue $progress.blocker
    $progress | Add-Member -NotePropertyName historicalExecution557HostHeapNextAction -NotePropertyValue $progress.nextAction
    $progress | Add-Member -NotePropertyName androidIntegrationFixtureQualification -NotePropertyValue $qualification
    $progress | Add-Member -NotePropertyName parentBatch082AndroidRecovery -NotePropertyValue $receipt
    $progress.status = 'continue'
    $progress.blocker = $null
    $progress.stage = 'batch-082-parent-publishable-fixture-android-passed-pending-signed-evidence'
    $progress.nextAction = 'SAME082557 owner-approved issue130 loader prerequisite RESOLVED with actual fresh gate. Read control\batch-082-parent-test-loader-qualification.json and batch-082-parent-android-recovery.json. PR131 merged to signedmain e46106de88892b6886f38199b5ca20f2134b27f6 after actual terminalgreenCI42222517447 BOTHcore/build; separate pushCI42224592996 not yet claimed. Dedicated Android NOW1c1b7bf42cc91d820a93169f1088dc647ac51c0d/G/whollyclean on n1/issue-130-test-loader, a signed published TESTONLY cherry-pick751c471 onto frozenf9b59a2. Production exactf9 unchanged; do NOT upgrade to latestmain app behavior or revert HEAD to literaloldf9. Original branch retained, only5test/docsfiles changed; all original parser assertions/runtimefiles/doc evidence/memory/archiveguards preserved. Fresh SAME082RealContent3+RareHan1+loader5 ALLpassed/noskips at unchanged065HOST2g init,4m50s/41tasks41executed; independent verifier actualstart/UTC/root/sourcecopyhashes/bothwholecleanheads contentb9eb2fbG. Original557attempt1+isolated2GiBOOM/restart/userretry/OOMs/failedlogs/XML and completeprogresshistory retained, NOT retroaccepted. Future same corpus HOST gates use new signedtest-onlybaseline and originalqualified2ginit; parentverifier has optional explicitAndroidHead parameter only (exact1c1b7bf), all checks retained. No native build uses HOST init. FIRST archive full actual prerequisite/source-patch/review/CI/freshXML/provenance and normally SIGNED LOCAL recoveredAndroid checkpoint BEFORE082nativefixture/device. Retain textualclosureb6bcc8f1/sourcefamilydispositions/fullreadingorder and all31Han/fourfonts including 冫/氵/辶/隹. No redundant freshHOST gate or blind initial review absent new concern. Then full frozen productionContentSyncONCE, glyph/lookalikes/selection/meaning/curatedreadings/drawing/articles/reciprocalroutes/SystemBack/offline/freshlocal+remoteportownership/actualterminal0eachnativecase/noskips, ORIGINALserialtwo-familydependentvisual, latestmain/allcombinedPython368/validator/vocabulary/manifest/exact虎猿guards/originalbudgets, normal signedownerpush/publicSHA/terminalgreenCI/everyZIPruntimehash/terminalreceipts/ownerissue60 BEFORE083. Preserve read-depth/process/citation/viewport/fallback/MLKit/phone/generalrelease/whole-set limits. Scopedreviewer --add-dir control and artifactpathpreflight remain. Published108/1228,remaining1120/latest0811f317f0762513720709ab0ca215f19ff021ca596/greenCI42200191053;082draftNOTdelivered. Exactlyone coordinator/atmostone reviewer. Historical blocker/nextAction saved separately; runtimejournal left launcher-owned.'
    $temporary = "$path.parent557.tmp"
    $progress | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $temporary -Encoding utf8NoBOM
    $check = Get-Content -LiteralPath $temporary -Raw | ConvertFrom-Json
    if ($check.checkpoint -ne 557 -or $check.status -ne 'continue' -or
        $check.remainingAdditions -ne 1120 -or
        $check.androidIntegrationFixtureQualification.qualifiedAndroidHead -ne $head) {
        throw 'Recovery invariant failed.'
    }
    Move-Item -LiteralPath $temporary -Destination $path -Force
    @{ checkpoint = 557; status = 'continue'; freshTests = 9; androidHead = $head; remaining = 1120 } | ConvertTo-Json
} finally {
    $lock.Dispose()
}
