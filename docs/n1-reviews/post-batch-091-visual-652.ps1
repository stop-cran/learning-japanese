$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
if ($p.checkpoint -ne 651 -or $p.batch -ne '091' -or
    (git -C $content rev-parse HEAD^) -ne 'e19a64832234160ae46ec48ea417687ca7bfe881' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$e = Get-Content "$content\docs\n1-sources\execution-652.json" -Raw | ConvertFrom-Json
if (-not $e.gptVisualAssessmentCompleted -or -not $e.serialProcessAndToolsVerified -or
    -not $e.runtimeChanged -or $e.runtimeAccepted -or $e.runtimePublished) {
    throw 'Unconfirmed correction receipt mismatch.'
}
$body = @"
Batch 091 (刃): **original GPT visual assessment completed; narrowly corrected mnemonic saved locally, awaiting both original-session confirmations**. Normally signed LOCAL UNCONFIRMED freeze ``$saved``; no runtime push or batch 092.

Original GPT session ``8da57d75`` resumed with actual **gpt-6.1-sol**, PID 28408, exited 0. Execution evidence verifies **18 serial view calls, 15 decoded image returns, no overlaps, no unfinished tools, all assigned text returned without truncation**. The report covers both articles and all supplied font panels/contact sheets, with inherited textual conclusions, and establishes no defect. It was not shown Claude's report or coordinator adjudication. This is dependent visual evidence, not new blind initial review. Complete report/raw events/model/tool receipts are preserved under ``docs/n1-reviews/batch-091-visual-652-*``.

Claude's prior **14 tool-overlap starts remain preserved and rejected as process-contract acceptance**. The models' observations are not rewritten as agreement: GPT reported CLEAN; the coordinator freshly inspected the original font-panel-3, meaning-question and drawing-trace images and verified the detached left-falling default-Gothic mark versus the crossing mark in other font selections and the pinned diagram. This supports a minor, localized comprehension clarification rather than a font/glyph/geometry change. ``kanji/刃.md:24`` now describes an extra short mark, noting that some fonts show a separate stroke while the diagram shows it crossing the longer sloping stroke. It remains explicitly a modern-shape mnemonic, not etymology.

``python -B tools\validate.py`` passed with zero errors; the manifest was regenerated. All **8,432 runtime hashes** and freshness pass for version **``bfe65483a821fc13``**. Exactly one runtime payload changed: that mnemonic paragraph. Metadata/readings/order, selected は/empty on list, words, quiz choices, five direct guards, links and stroke geometry remain unchanged. No word title was changed. The new wording is **not independently confirmed or natively rendered/imported yet**.

``docs/n1-sources/execution-652.json`` and ``docs/n1-reviews/batch-091-visual-reconciliation-652.json`` retain the exact diff, evidence, disagreement, original optional findings and limitations. Existing native650 results remain evidence for **old archive f6b2ee39/version cb3c857f3614485d**, not this correction: two terminal cases 0/no skips, full production ContentSync once, 1,114 kanji/5,070 words/123 N1/zero Problems/Room epoch 1. No fresh native, physical-phone, human-handwriting, successful offline MLKit, identified fallback-face or latest-app-main claim. Qualified test-only Android ``1c1b7bf4`` retains production ``f9b59a2``.

Checkpoint **652** continues SAME091: serial bounded changed-passage/relevant-rendered confirmation in original Claude then original GPT sessions, retaining actual process/read audits and the prior process violation. All original source, baseline, link, reading, two-family, native, combined-current-main, normal signing, owner fast-forward, terminal CI, every immutable ZIP runtime hash and unchanged archive/per-file/media/path limits remain gates. No parent-lock access, optional historical-session helper access or actual new permission denial. Published count remains **117/1,228; 1,111 remaining**; physical-phone/general-release/whole-set acceptance remains outstanding.
"@
$prefix = "$control\batch-091-visual-652-issue-"
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
