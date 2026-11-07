$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
if ($p.checkpoint -ne 652 -or $p.batch -ne '091' -or
    (git -C $content rev-parse HEAD^) -ne '1cfd5bd36e707ee78ba4401e48ffba9815854d58' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$e = Get-Content "$content\docs\n1-sources\execution-653.json" -Raw | ConvertFrom-Json
if ($e.twoFamilyCorrectionConfirmation -ne 'complete' -or -not $e.serialProcessAndToolsVerified -or
    $e.runtimeChanged -or $e.runtimeAccepted -or $e.runtimePublished) {
    throw 'Correction confirmation receipt mismatch.'
}
$body = @"
Batch 091 (刃): **both original-session mnemonic confirmations complete; local evidence checkpoint 653 saved** at normally signed ``$saved``. No runtime publication or batch 092.

Original **Claude Opus 5.5** session ``075924f2`` (PID 18224) finished before original **GPT-6.1 Sol** session ``8da57d75`` (PID 30260) started. Both exited 0 with **six complete serial view calls, three decoded original PNG returns, zero overlaps and no unfinished tools** each. Each read its own earlier report, exact correction diff, complete revised kanji article, and the original font-panel-3/meaning-question/drawing-trace images. Only read-only view was exposed; no author-token inheritance. Complete reports, raw events, actual models, tool/read receipts and helper provenance are archived in ``docs/n1-reviews/batch-091-mnemonic-653-*``.

Both confirm that the revised description accurately accommodates the detached Gothic shortmark and crossing pinned-diagram mark, preserves the mnemonic/nonhistorical qualification and introduces no established regression. **Localized V1 is resolved in text.** GPT's earlier CLEAN verdict is not rewritten as discovery/agreement with the original concern. Claude651's 14 overlapping starts remain rejected process evidence; this new serial confirmation does not retroactively repair them. Claude's detached/separate, stroke-direction and “here” wording suggestions remain optional. Original findings, hypotheses and limitations stay preserved.

No runtime payload changed this execution. Fresh manifest equality and all **8,432 runtime hashes** pass for ``bfe65483a821fc13``. The original screenshots show **old version cb3c857f3614485d**, so they support shape comparison, **not import/rendering of the revised mnemonic**. No fresh native/device acceptance is claimed. Native650's two terminal-case successes/no skips and once-only full production import of archive f6b2ee39 (1,114 kanji, 5,070 words, 123 N1, zero Problems, Room epoch 1) retain their exact old-version scope.

``docs/n1-sources/execution-653.json`` and ``docs/n1-reviews/batch-091-mnemonic-reconciliation-653.json`` preserve reconciliation. Checkpoint continues SAME091: determine and perform the smallest justified revised-version native import/rendering confirmation using approved workspace fixtures; then retain all combined-current-main, normal merge/signing, two-family changed-teaching, owner fast-forward, terminal CI, every immutable ZIP runtime hash and unchanged archive/per-file/media/path acceptance gates. No broad dictionary/reviewer loops without newly established need.

Parent runner19008 retains its lock; no child lock acquisition/deletion/unlock, optional historical-session helper access, actual new permission denial or second runner. API35/test-only Android1c1b7bf4 retaining productionf9b59a2, unidentified fallback face, injected trace/no successful MLKit and original evidence limits remain. **Published 117/1,228; 1,111 remaining.** Physical-phone, general-release and whole-set acceptance remain outstanding.
"@
$prefix = "$control\batch-091-mnemonic-653-issue-"
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
