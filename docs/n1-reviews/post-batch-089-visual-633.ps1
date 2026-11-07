$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$state = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($state.checkpoint -ne 632 -or $state.batch -ne '089' -or
    $state.stage -ne 'batch-089-dependent-visual-confirmations' -or
    $runner.pid -ne 19008 -or $runner.sessionId -ne 'cb82a0d8-5174-4b40-8f66-1fe1551fb391' -or
    -not (Get-Process -Id 19008 -ErrorAction SilentlyContinue) -or
    (git -C $content rev-parse HEAD^) -ne 'cc8e90416d207d879058c22e493fbba78a2b3603' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint or live parent ownership precondition failed.'
}
$p = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
$owned = $false
while ($p) {
    if ($p.ProcessId -eq 19008) { $owned = $true; break }
    $p = Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)"
}
if (-not $owned) { throw 'Expected parent ancestry not established; yield.' }
$evidence = Get-Content "$content\docs\n1-reviews\batch-089-visual-reconciliation-633.json" -Raw | ConvertFrom-Json
if (-not $evidence.serialReviewerProcessesExited -or
    -not $evidence.allAssignedResourcesReturned -or -not $evidence.allToolViewsSerial -or
    $evidence.eachReviewerImagesDecoded -ne 11 -or
    $evidence.runtimeAcceptedForPublication -or $evidence.runtimePublished) {
    throw 'Dependent visual checkpoint evidence inconsistent.'
}
$body = @"
Batch 089 (U+51F6): **original two-family dependent visual confirmations complete; combined current-main acceptance and publication remain pending**. Normally signed LOCAL evidence ``$saved``; teaching unchanged from ``4b84608b5ca8889d45a176667975524f6645bd8d``. No runtime edit or push.

Original Claude Opus 5.5 (``claude-opus-5.5``, session ``a56b5dcb-9fed-4785-848e-41708f65598f``), then original GPT-6.1 Sol (``gpt-6.1-sol``, session ``3286add7-2824-4df6-933a-c8bba3890927``), each completed **13 strictly serial view calls / 11 decoded PNGs**: eight mapped sheets covering all43native captures, plus three separate Compose font panels. Each process exited0 before the next started; no tool/process overlap. Both new articles and ONLY the changed U+4F5C navigation line have **CLEAN rendered comprehensibility**, with correctness/coverage inherited from their preserved initial textual reviews. No actionable defect or new blind-review credit. Original GPT redundant/truncated-tail read limitations remain explicit.

All23Han, especially crossing U+4E42 and open-topped U+51F5, remain visible/distinguishable in four production font selections. Both complete new article projections and the one changed linked example line are readable. The agricultural noun/very-poor-yield explanation preserves not-harvest-verb/not-necessarily-zero-yield/not-famine/not-bad-work boundaries and compound-specific crop/yield composition. Complementary horizontally scrolled captures expose the full linked reading row; no manufactured static-clipping defect. Original optional additions and cosmetic fallback-weight/header remarks remain nonblocking, not findings.

Actual returned PNG payloads decoded and dimension-checked; hashes agree across models. The tool resized sheets **1500x2260 to1327x2000** and original font panels **1080x2400 to900x2000**; not source-byte-identical or unscaled views. 92individual+4wholewordPaint probes remain recycled hash evidence, **not96exported/viewedPNGs or identified fallback face**.

Pictured N1 meaning options: ill fortune; evil versus commonplace; mediocre / convex; protruding / concave; sunken. Supplied actual N1 AND All production-builder receipts show the same four identities, all3curatedwrongcards available, zero fallback; All is receipt evidence, not separately pictured. Only these tested configurations are closed, not futurecustom/randompools or oldclients. One on key U+304D U+3087 U+3046 Good/1of1done, rawkun[] and explicitquizkun[], Full/Lite agreement.

Inherited native632: both terminal cases0/no skips; full archive ``72614eda`` through productionContentSync **ONCE**,1112kanji/5068words/121N1/zeroProblems/acceptedVersion ``c6562f11cb371053``/epoch1; fourstroke injectedtrace/recallgiveup, botharticles/2mappedpairs/4directions/1directguard/SystemBack/offline. **No fresh native/Android run in633**, realhandwriting, offlineMLKit, physicalphone or native-speaker claim. Qualified TESTONLY Android ``1c1b7bf4`` retains production ``f9b59a2``, not latestappmain.

Complete reports, lossless raw JSON streams, prompts, actual model/process/range/image audits and evidence-based reconciliation are committed under ``docs/n1-reviews/*633*``, indexed by ``docs/n1-sources/execution-633.json``. All **8426runtime hashes** and manifest freshness reverified; no teaching/runtime change. Dedicated worktrees clean. No historical session-helper access, parent-lock acquisition/deletion/unlock, new permission denial, second runner or090.

Checkpoint633 continues SAME089 with normal current-main integration and actual combined-tree acceptance. All original source/baseline/link/reading/twofamily/native gates, changed-teaching independent review, required fullPython/vocabulary/manifest/budget/audits/applicable nonskippedAndroid checks, normal signing/ownerfastforward, terminalgreenCI, **EVERY immutable public ZIP runtime entry hash**, original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath and ownerissue gates remain mandatory. No unreviewed push, guard/heap increase or productionapp change. Published unchanged **115/1228;1113remaining**. Physicalphone/generalrelease/whole-set acceptance remains outstanding; project incomplete.
"@
$prefix = "$control\batch-089-visual-633-issue-"
if ((Test-Path ($prefix + 'posted.json')) -or (Test-Path ($prefix + 'receipt.json'))) {
    throw 'Existing issue receipt; never repost.'
}
$body | Set-Content ($prefix + 'body.txt') -Encoding utf8NoBOM -NoNewline
@{body=$body} | ConvertTo-Json | Set-Content ($prefix + 'payload.json') -Encoding utf8NoBOM
$oldToken = $env:GH_TOKEN
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $postedText = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input ($prefix + 'payload.json')
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed.' }
    $postedText | Set-Content ($prefix + 'posted.json') -Encoding utf8NoBOM
    $posted = $postedText | ConvertFrom-Json
    $verifiedText = gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue verification failed.' }
    $verified = $verifiedText | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Owner/body verification failed.' }
    $verifiedText | Set-Content ($prefix + 'receipt.json') -Encoding utf8NoBOM
    Write-Output $verified.html_url
} finally {
    $env:GH_TOKEN = $oldToken
}
