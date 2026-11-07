$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
if ($p.checkpoint -ne 663 -or $p.batch -ne '092' -or
    $p.stage -ne 'batch-092-original-session-dependent-visual-confirmations' -or
    (git -C $content rev-parse HEAD^) -ne '09c9cfde7513a0dc7a7ca5a07d28131a3476015f' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$e = Get-Content "$content\docs\n1-reviews\batch-092-visual-reconciliation-664.json" -Raw | ConvertFrom-Json
if ($e.status -ne 'dependent-visual-review-closed-awaiting-combined-acceptance' -or
    -not $e.serialReviewerProcessesExited -or -not $e.allToolViewsSerial -or
    $e.actionableRemainingFindings -ne 0) { throw 'Visual acceptance evidence incomplete.' }
$body = @"
Batch 092 (刈): **both original-session dependent visual confirmations closed; current-main combined acceptance and publication remain pending**. Normally signed LOCAL evidence ``$saved``; unchanged teaching ``6246dc622f7139c2a0e16d2e03847d6494391fae``. No runtime publication or batch 093.

Original Claude Opus 5.5 (``claude-opus-5.5``, session ``2f27854e-184a-4f54-8d7d-962197573318``, PID15216) then original GPT-6.1 Sol (``gpt-6.1-sol``, session ``4ff2dfd7-8eed-456f-8f4d-4acd64d2a820``, PID22788) each exited0 after **27 strictly serial view calls / 25 decoded original PNG views**, with no overlapping or unfinished tools and every assigned text/image returned. Claude actually exited and its full report was saved before GPT launched. Actual models confirmed from returned messages and usage. **Dependent follow-ups, not new blind initial reviews.**

Both complete kanji 刈 and reused N3 刈る retain **CLEAN inherited correctness/coverage and bounded rendered comprehensibility**, with no actionable defect or consequential unresolved in-scope claim. All16 scoped Han are readable/distinguishable in three original Compose panels across Gothic/Mincho/Textbook/Brush, including fallback U+5202 刂 and 刈/切/刀/乃/凹/凸; whole 刈除 is legible. Complementary horizontally scrolled reading-table views expose the full row. Some route captures are byte duplicates:25views correspond to22distinctsourceimages;17of42captures were not separately viewed. Tools resized1080x2400 originals to900x2000. The64individual+4wholewordPaint probes are not68viewedPNG exports or identifiedfallbackface. Claude explicitly notes that the word body's top heading was not separately pictured; full article completeness also uses supplied fulltext/native-scroll assertions.

Pictured N1 selection/meaning feedback and supplied production N1/All receipts retain allthree available curated wrong labels, zero fallback, and exactly mow/reap versus乃/凹/凸. Onlykunかる was offered through correctfeedback/1of1Done; rawガイ,カイ/か.る and full/Lite equality/persistedGood/NOonkeys remain supplied native assertions, not reviewer-executed tests. Both刈除 readings remain recognized/unselected, not source-only, obsolete or frequency-ranked. Existing N3 刈る identity/reading/title/level/original切るguard preserved; only componentlink/direct収穫guard changed. One all-mapped/baseline pair, two directions, SystemBack/offline routes remain consistent.

Inherited native663 evidence remains exact: BOTHterminalcases0/no skips; fullarchive62c6d3e2 imported through productionContentSync ONCE,1115kanji/5070words/124N1/zeroProblems/version8445a5717d080dcc/acceptedRoomreadingEpoch1. Four pinned strokes exercised injectedtrace/practice/recallgiveup; actual UI explicitlymodelunavailable/shape-onlygrading. **Not humanhandwriting, successfulMLKit or phone evidence.** No new664Android/native run; qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latest appmain; native663 ownedhelpers already stopped.

Both complete original reports, prompts, model/process/read/image audits and losslessly compressed raw execution events are archived with ``docs/n1-reviews/batch-092-visual-reconciliation-664.json`` and ``docs/n1-sources/execution-664.json``. Earlier optional hairtranslation/inflectionkana/収穫contrast suggestions remain nonblocking; fontweight and kana-wrap observations are polish, not a missingglyph or demonstrated learning defect. Independent upstream/Git verification, fallbackface identity and all original source/read limitations remain explicit. Coordinator reverified all8434runtime hashes and manifest freshness; runtime bytes unchanged.

Checkpoint664 continues SAME092 with fresh-current-main normal nonrewriting integration, changed-teaching review if needed and actual combined-tree Python/vocabulary/manifest/budget/baseline/membership/link/reading/applicable non-skippedAndroid acceptance. All normal-signing/ownerfast-forward/terminalgreenCI/everyimmutablepublicZIPruntimehash/original18000entries42MiBcompressed80MiBinflated56MiBretained/per-file-media-safe-path gates remain. Parent launcher retains runner.lock; no child reacquisition/delete/unlock, historical session-helper access, new permission denial, productionapp change or weakened gate. Published count remains **118/1228;1110remaining**. Physical-phone, general-release and whole-set acceptance remain outstanding.
"@
$prefix = "$control\batch-092-visual-664-"
$payloadPath = $prefix + 'issue-payload.json'
$postedPath = $prefix + 'issue-posted.json'
$receiptPath = $prefix + 'issue-receipt.json'
if ((Test-Path $postedPath) -or (Test-Path $receiptPath)) { throw 'Existing issue receipt; never repost.' }
$body | Set-Content ($prefix + 'issue-body.txt') -Encoding utf8NoBOM -NoNewline
@{body=$body} | ConvertTo-Json | Set-Content $payloadPath -Encoding utf8NoBOM
$oldToken = $env:GH_TOKEN
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable.' }
    $identity = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Owner identity mismatch.' }
    $postedText = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed.' }
    $postedText | Set-Content $postedPath -Encoding utf8NoBOM
    $posted = $postedText | ConvertFrom-Json
    $verifiedText = gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue verification failed.' }
    $verified = $verifiedText | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Owner/body verification failed.' }
    $verifiedText | Set-Content $receiptPath -Encoding utf8NoBOM
    Write-Output $verified.html_url
} finally {
    $env:GH_TOKEN = $oldToken
}
