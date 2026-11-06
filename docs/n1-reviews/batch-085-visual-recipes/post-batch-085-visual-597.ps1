$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$p = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 596 -or $p.batch -ne '085' -or
    $p.stage -ne 'batch-085-original-family-visual-confirmations') { throw 'Checkpoint context changed' }
$saved = git -C $repo rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or
    (git -C $repo log -1 '--format=%G?') -ne 'G' -or
    (git -C $repo rev-parse 'HEAD^') -ne '6921ddbd75e93e43974d2e9340f41c7f8848e626' -or
    (git -C $repo status --porcelain)) { throw 'Normally signed clean local evidence precondition failed' }
$body = @"
Batch 085: **both original reviewer families completed dependent visual confirmation; saved locally, not published**. Normally signed checkpoint: ``$saved``. Claude Opus 5.5 and GPT-6.1 Sol resumed their original sessions serially on unchanged reviewed teaching and native evidence. Complete reports, actual models, tool-returned image payloads/dimensions and 50 terminal child-process exits are preserved in docs/n1-reviews/batch-085-visual-*; reconciliation is indexed by execution-597.json.

Each reviewer received the same complete source/provenance packet, 15 labelled full-frame sheets representing all 87 native captures, and eight focused original image paths. This is **not 87 full-resolution reads**: both contact-sheet scaling and tool resizing are recorded. The bounded review covers the four new article projections, changed reused 固 bullet, 39 Han across four production font families, three whole words, default meaning choices, both scheduled reading kinds, drawing and navigation. No actionable scoped defect remains; original optional suggestions and read/lookup/rendering limits remain explicit. Exact fallback-face identity and human handwriting/MLKit recognition are not established. Selected こ.らす shares normalized key こる with こ.る, not independent queued mastery.

Prior native596 evidence remains two named terminal-status-0 cases, no skips: full production ContentSync once, 1,108 kanji / 5,063 words / 117 N1, zero problems, version 0c514711ae8d3212 and accepted Room parser epoch 1. Fresh Android checks from594 and compiled595 are inherited, not rerun or relabelled. All 8,413 runtime hashes and manifest freshness reverified without runtime changes. No app/guest heap or archive-guard changes, new native session, parent-lock acquisition or optional historical-session helper access.

Next is latest-main normal integration and combined-tree acceptance, then normal signed owner fast-forward publication, terminal CI and every immutable public ZIP runtime hash/budget check. **No runtime push or batch 086.** Published additions remain **111/1,228; 1,117 remaining**. Physical-phone, general-release and whole-set acceptance remain outstanding; the project is incomplete.
"@
$bodyPath = "$control\batch-085-visual-597-issue-body.txt"
$payloadPath = "$control\batch-085-visual-597-issue-payload.json"
$receiptPath = "$control\batch-085-visual-597-issue-receipt.json"
if (Test-Path -LiteralPath $receiptPath) { throw 'Existing receipt; never repost blindly' }
$body | Set-Content -LiteralPath $bodyPath -Encoding utf8NoBOM -NoNewline
@{body=$body} | ConvertTo-Json | Set-Content -LiteralPath $payloadPath -Encoding utf8NoBOM
$oldToken = $env:GH_TOKEN
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable' }
    $identity = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Owner identity mismatch' }
    $postedText = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed' }
    $postedText | Set-Content "$control\batch-085-visual-597-issue-posted.json" -Encoding utf8NoBOM
    $posted = $postedText | ConvertFrom-Json
    $verifiedText = gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue verification failed' }
    $verified = $verifiedText | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Owner/body verification failed' }
    $verifiedText | Set-Content -LiteralPath $receiptPath -Encoding utf8NoBOM
    Write-Output $verified.html_url
} finally {
    $env:GH_TOKEN = $oldToken
}
