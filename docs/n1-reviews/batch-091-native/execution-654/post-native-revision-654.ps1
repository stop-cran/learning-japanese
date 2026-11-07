$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
if ($p.checkpoint -ne 653 -or $p.batch -ne '091' -or
    (git -C $content rev-parse HEAD^) -ne 'fe3ec10b34e5b26fd286d7a79b33b6b6a03afda6' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$e = Get-Content "$content\docs\n1-sources\execution-654.json" -Raw | ConvertFrom-Json
if (-not $e.revisedVersionNativeConfirmed -or -not $e.executionReceipt.passed -or
    $e.executionReceipt.terminalSuccessCases -ne 1 -or $e.runtimeChanged -or
    $e.runtimeAccepted -or $e.runtimePublished -or -not $e.executionReceipt.ownedHelperStopped -or
    -not $e.executionReceipt.ownedQemuStopped) {
    throw 'Revised native receipt mismatch.'
}
$body = @"
Batch 091 (刃): **revised-version native import/rendering confirmation passed; local evidence checkpoint 654 saved** at normally signed ``$saved``. No runtime publication or batch 092.

The full immutable local Git archive of signed ``fe3ec10b`` with current contentVersion ``bfe65483a821fc13`` was imported through production **ContentSync once**: **1,114 kanji, 5,070 words, 123 N1, zero Problems**, accepted Room reading-parser epoch 1. All **8,432 runtime manifest hashes**, manifest equality/freshness and unchanged original archive/per-file limits passed: 8,454 entries; 30,443,868 compressed / 44,586,226 inflated / 44,317,888 retained bytes. This is a local native acceptance archive, **not verification of a published GitHub ZIP**.

The existing complete ArticleTest was reused with only the exact revised paragraph selector and archive/SHA/version identity substitutions. The unrelated GlyphTest was not rerun; old font evidence is inherited with its limits. Compilation passed and **one selected native case returned terminal status 0, no skips** on owned read-only API35 ``emulator-5580`` (helper13396/QEMU15708). Both owned processes were verified stopped. Host GPU/Vulkan-disabled, 2 cores/2048MiB, app/guest heaps and production guards were unchanged; no other emulator was touched.

The revised paragraph is genuinely imported and rendered now. Coordinator viewed the new original ``n1-091-kanji-04.png``: the complete mnemonic paragraph, font/separate-stroke qualification, crossing-diagram wording and nonhistorical disclaimer are readable without clipping. **47 new PNGs preserved; only that one separately visually inspected** this execution. The original two-family textual correction confirmations remain valid; **small dependent original-reviewer confirmation of this new rendered paragraph remains pending**, not manufactured closure or new blind-review credit.

Unchanged actual-route assertions also passed: both articles, one mapped pair/two directions, 先端 navigation/System Back/offline, N1/All exact meaning choices with three curated wrong cards/no fallback, only kun は offered/persisted Good/Done with no on keys, full/Lite raw readings preserved, three pinned injected drawing strokes/recall persistence and five direct word guards. Injected tracing/give-up is not human handwriting or successful MLKit recognition. Test-only Android ``1c1b7bf4`` retains production ``f9b59a2``; **not latest app main or phone evidence**.

``docs/n1-sources/execution-654.json`` and ``docs/n1-reviews/batch-091-native/execution-654/`` preserve exact fixture diff, logs, receipts, hashes, PNGs, helper provenance and limitations. Previous archives/receipts are preserved, not relabeled. No runtime teaching changed. Parent19008 retains its lock; no child lock acquisition/deletion/unlock, historical-session recipe access, new permission denial or second runner.

Continue SAME091 with the smallest serial original-session confirmation of the new mnemonic PNG, then all current-main normal merge/combined-tree/source-baseline-link-reading/two-family/signing/owner fast-forward/terminal CI/every immutable public ZIP hash and unchanged budget gates. **Published 117/1,228; 1,111 remaining.** Physical-phone, general-release and whole-set acceptance remain outstanding.
"@
$prefix = "$control\batch-091-native-revision-654-issue-"
$payloadPath = $prefix + 'payload.json'
$postedPath = $prefix + 'posted.json'
$receiptPath = $prefix + 'receipt.json'
if ((Test-Path $postedPath) -or (Test-Path $receiptPath)) { throw 'Existing issue receipt; never repost.' }
$body | Set-Content ($prefix + 'body.txt') -Encoding utf8NoBOM -NoNewline
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
