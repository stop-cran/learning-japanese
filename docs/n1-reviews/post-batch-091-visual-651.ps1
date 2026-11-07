$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
if ($p.checkpoint -ne 650 -or $p.batch -ne '091' -or
    $p.stage -ne 'batch-091-dependent-visual-confirmations' -or
    (git -C $content rev-parse HEAD^) -ne '99d11124a5eab51850be91b15c0ebd224af7f8ce' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$e = Get-Content "$content\docs\n1-sources\execution-651.json" -Raw | ConvertFrom-Json
if (-not $e.toolOverlapViolationPreserved -or $e.compliantVisualConfirmations -ne 0 -or
    $e.gptVisualLaunched -or $e.runtimeChanged -or $e.runtimePublished) {
    throw 'Partial review receipt mismatch.'
}
$body = @"
Batch 091 (刃): **partial visual-review evidence saved; visual acceptance remains open**. Normally signed LOCAL evidence ``$saved``; unchanged textually confirmed teaching ``c2a59d5c``, native archive ``f6b2ee39``. No runtime publication or batch 092.

Original Claude session ``075924f2`` resumed with actual **claude-opus-5.5** and exited 0 (PID 25128). Its complete report and losslessly archived raw execution are retained in ``docs/n1-reviews/batch-091-visual-651-*``, indexed by ``docs/n1-sources/execution-651.json``. Three text reads were serial, but **15 image views were launched together (14 overlap starts)** despite explicit one-view-per-response instructions. The coordinator wrapper correctly rejected process-contract acceptance after saving the report. This is **not** a compliant serial visual confirmation, permission denial or two-family closure. No second reviewer was launched; original GPT visual follow-up is still pending. The reviewer process is verified exited.

The report identified a **minor rendered-comprehensibility defect** at ``kanji/刃.md:24``: the mnemonic specifies an extra mark shaped like 丶, but the default Gothic quiz glyph uses a detached, left-falling short mark, while the other font selections and pinned drawing reference show a crossing, right-falling mark. The coordinator separately inspected the original font-panel-3, meaning-question and drawing-trace captures and agrees a narrowly font-variable wording qualifier is warranted. This is not a missing glyph, requirement for uniform typefaces or authorization for app/font/geometry changes. The claim, remedy, severity, evidence and process limitation remain explicitly unresolved in ``batch-091-visual-partial-651.json``; no teaching edit has been made.

Twelve mapped whole-frame contact sheets cover 23 distinct nonfont frames; exact duplicate identities account for all 47 nonfont captures, plus three original font panels for all 50 captures. This is not 50 separate fresh inspections or 88 viewed Paint probes. Original textual findings, disagreement, optional notes, nonactionable slang hypothesis, source and device limits remain intact. Complete historical checkpoint values are preserved.

All **8,432 runtime manifest hashes**, manifest freshness and unchanged contentVersion ``cb3c857f3614485d`` reverified. Existing native650 evidence remains two terminal cases 0/no skips, full archive through production ContentSync once, 1,114 kanji/5,070 words/123 N1/zero problems/Room reading epoch 1. No fresh native rerun, human-handwriting, successful offline MLKit, physical-phone or latest-app-main claim. Qualified TESTONLY Android ``1c1b7bf4`` retains production ``f9b59a2``.

Checkpoint **651** continues SAME091: complete original GPT visual assessment on the same frozen sample without the other report; reconcile the localized mnemonic issue, then bounded original-session changed-passage/rendered confirmations with verified serial tool work. Preserve the actual violation, do not erase it or count it as accepted. All original source/baseline/link/reading/two-family/native/current-main integration/combined-check/normal-signing/owner-fast-forward/terminal-CI/every-immutable-ZIP-hash/archive guards remain. Parent launcher retains runner.lock untouched; no optional historical session helper or actual new permission denial. Published count remains **117/1,228; 1,111 remaining**. Physical-phone, general-release and whole-set acceptance remain outstanding.
"@
$prefix = "$control\batch-091-visual-651-issue-"
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
