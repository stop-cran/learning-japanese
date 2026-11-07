$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$bodyPath = "$control\batch-095-integration-696-issue-body.txt"
$postedPath = "$control\batch-095-integration-696-issue-posted.json"
$receiptPath = "$control\batch-095-integration-696-issue-receipt.json"
foreach ($path in @($bodyPath, $postedPath, $receiptPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing receipt; inspect rather than repost.' }
}
$head = git -C $content rev-parse HEAD
$parent = git -C $content rev-parse HEAD^
if ($LASTEXITCODE -ne 0 -or $parent -ne 'd5a6823c70583ab5c64a63a863993b9577466937' -or
    (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Normally signed exact child evidence head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Content worktree not wholly clean.' }
$evidence = Get-Content "$content\docs\n1-sources\execution-696.json" -Raw | ConvertFrom-Json
if ($evidence.pythonTestsPassed -ne 372 -or $evidence.hostTestsExecuted -ne 4 -or
    $evidence.hostTestsSkipped -ne 0 -or $evidence.runtimeAccepted -or $evidence.runtimePublished) {
    throw 'Unexpected evidence state.'
}
$body = @"
### Batch 095: combined-main checkpoint 696 (not publication)

Saved normally signed LOCAL integration ``d5a6823c70583ab5c64a63a863993b9577466937`` (parents ``515666e9`` and current main ``da374717``), followed by signed evidence ``$head``. Both dedicated worktrees are clean. The only conflict was ``manifest.json``, regenerated with the existing generator; all eleven incoming teaching files and their source record are byte-preserved from main, while all four batch-095 runtime files remain unchanged.

On the actual combined tree, **372 Python tests**, validation, vocabulary consistency, manifest freshness, frozen dictionary/baseline/membership/reading/link/stroke/font-provenance audits and **4 fresh Android cases, zero skips** passed. RealContentTest resolves this dedicated content checkout; actual XML reports and timestamps are retained. The combined manifest has **8,441 runtime hashes**, version **3eebfff0fdad5e28**. Local archive: 8,463 entries; 30,276,035 compressed / 44,612,586 inflated / 44,344,248 retained bytes, within unchanged guards. Vocabulary coverage remains the existing 2,122/2,431 reviewed-prompt pilot; this is consistency, not full coverage.

**Acceptance remains open:** incoming substantive 子/nominal-ending amendments have an upstream independent review with unavailable model, not batch-095 two-family credit. Bounded changed-passage confirmation by both original reviewer families is next. Earlier native 694 imported version ``463619d79972e9f2``, not this changed manifest: preserve its full evidence and obtain a new bounded exact-combined full-archive production ContentSync import once, with actual accepted Room version/counts/epoch. Batch-095 visible teaching, 32 Han, fonts, strokes, reading/quiz metadata and prior route evidence are unchanged; no fresh native/visual result is claimed here.

Evidence: ``docs/n1-sources/execution-696.json`` and ``docs/n1-reviews/batch-095-combined-integration-696.json``. Original two-family textual/rendered reports and rejected Claude overlap/accepted serial repair remain intact. No reviewer or emulator was launched in this execution. Qualified TESTONLY Android remains ``1c1b7bf4`` with production ``f9b59a2``; not latest app main, phone, human-handwriting, MLKit or full-pool semantic certification.

No runtime publication or batch 096. Full combined acceptance, normal signed owner fast-forward, terminal CI, every immutable public ZIP entry/hash and original packaging gates remain required. **Published 121/1,228; 1,107 remaining**, unchanged. Physical-phone/general-release/whole-set acceptance remains outstanding. Parent runner lock untouched; approved control/committed artifacts only, no optional historical-session helper access or new permission denial.
"@
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $payload = "$control\batch-095-integration-696-issue-payload.json"
    @{body=$body} | ConvertTo-Json -Depth 2 | Set-Content $payload -Encoding utf8NoBOM
    gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payload |
        Set-Content $postedPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed; preserve response.' }
    $posted = Get-Content $postedPath -Raw | ConvertFrom-Json
    if ($posted.user.login -ne 'stop-cran' -or $posted.body -cne $body) { throw 'Posted author/body mismatch.' }
    gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" |
        Set-Content $receiptPath -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Independent issue receipt fetch failed.' }
    $verified = Get-Content $receiptPath -Raw | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Verified author/body mismatch.' }
    $verified.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
