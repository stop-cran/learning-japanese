$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
if ($p.checkpoint -ne 654 -or $p.batch -ne '091' -or
    (git -C $content rev-parse HEAD^) -ne '4d6ea7640109a90a510d94083480b7c33c6e7ab2' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$e = Get-Content "$content\docs\n1-sources\execution-655.json" -Raw | ConvertFrom-Json
if ($e.twoFamilyDependentRenderedConfirmation -ne 'complete' -or -not $e.serialProcessAndToolsVerified -or
    $e.runtimeChanged -or $e.runtimeAccepted -or $e.runtimePublished) {
    throw 'Rendered confirmation receipt mismatch.'
}
$body = @"
Batch 091 (刃): **both original-session confirmations of the NEW revised-version mnemonic screenshot complete; signed LOCAL evidence checkpoint 655** at ``$saved``. No runtime publication or batch 092.

Original **Claude Opus 5.5** session ``075924f2`` (PID 27896) exited before original **GPT-6.1 Sol** session ``8da57d75`` (PID 24700) started. Both exited 0 with **three complete serial view calls, one decoded NEW PNG return each, zero overlaps and no unfinished tools**. Each inspected its own complete653 report, complete unchanged kanji article, and native654's original ``n1-091-kanji-04.png``. Actual returned models and view-only configuration verified; no author-token inheritance.

Both confirm the complete revised mnemonic, font qualification, crossing-diagram explanation and nonhistorical disclaimer are readable without clipping or overlap. **V1 stays resolved; revised native layout is now confirmed for this exact paragraph/screenshot.** Broader device/font/phone coverage remains limited. This is dependent confirmation, not new blind initial-review credit or retroactive discovery by GPT. Claude651's overlap violation remains rejected process evidence. Existing optional wording suggestions and source/read limitations remain preserved. Both complete reports, raw events, tool/image/process provenance and reconciliation are in ``docs/n1-reviews/batch-091-rendered-*655*``; summary in ``docs/n1-sources/execution-655.json``.

No runtime bytes changed. Fresh manifest equality and all **8,432 runtime hashes** verified for ``bfe65483a821fc13``. Native654's one terminal ArticleTest success/no skips, once-only full production ContentSync import of archive fe3ec10b (1,114 kanji, 5,070 words, 123 N1, zero Problems, Room epoch 1) are inherited exact receipts, **not new tests in655**. Reviewers viewed this one new screenshot, not the other46. GlyphTest was not rerun; inherit650's exact font evidence and limits. Qualified test-only Android1c1b7bf4 retains productionf9b59a2, not latest app main; API35 emulator is not phone evidence. Unknown fallback face/Paint probes/injected trace/no successful MLKit remain explicit.

Next bounded checkpoint stays SAME091: fetch/integrate current main with a normal non-rewriting merge if needed, regenerate derived output and run all combined-tree content/Python/vocabulary/baseline/link/membership/reading/font/budget/applicable Android checks. Independently review any substantive teaching change. Publication remains gated on full acceptance, normal signing and owner fast-forward push, terminal green CI, every immutable public ZIP runtime entry/hash, unchanged18,000-entry/42MiB compressed/80MiB inflated/56MiB retained and per-file/media/safe-path guards, and verified owner issue evidence. Do not blindly rerun unchanged source/native/review work.

Parent runner19008 retains its lock; no child lock reacquisition/deletion/unlock, optional historical-session helper access, new permission denial or second runner. **Published117/1,228;1,111remaining.** Physical-phone, general-release and whole-set acceptance remain outstanding.
"@
$prefix = "$control\batch-091-rendered-655-issue-"
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
