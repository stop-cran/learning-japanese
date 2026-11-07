$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$bodyPath = "$control\batch-095-rendered-695-issue-body.txt"
$postedPath = "$control\batch-095-rendered-695-issue-posted.json"
$receiptPath = "$control\batch-095-rendered-695-issue-receipt.json"
foreach ($path in @($bodyPath, $postedPath, $receiptPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing receipt; inspect rather than repost.' }
}
$head = git -C $content rev-parse HEAD
$parent = git -C $content rev-parse HEAD^
if ($LASTEXITCODE -ne 0 -or $parent -ne '86966dc49fb3a22014aea0dac2b568bc7045e56d' -or
    (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Normally signed exact child evidence head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Content worktree not wholly clean.' }
$evidence = Get-Content "$content\docs\n1-sources\execution-695.json" -Raw | ConvertFrom-Json
if ($evidence.actionableRemainingFindings -ne 0 -or $evidence.consequentialUnresolvedInScopeClaims -ne 0 -or
    $evidence.runtimePublished -or $evidence.runtimeAccepted) { throw 'Unexpected evidence state.' }
$body = @"
### Batch 095: rendered-review checkpoint 695 (not publication)

Saved normally signed LOCAL evidence at ``$head``; both dedicated worktrees remain clean. Original **Claude Opus 5.5** and **GPT-6.1 Sol** sessions completed bounded dependent confirmations of the frozen teaching/native evidence. Full reports, actual model/session/process/read/PNG-payload records, complete packets and reconciliation are preserved in ``docs/n1-reviews/batch-095-rendered-reconciliation-695.json`` and ``docs/n1-sources/execution-695.json``. This is not new blind-review credit.

Both families inspected the four font panels/all 32 Han, fourteen contact sheets binding the other 56 original captures, all three articles, two reciprocal pairs/four directions, actual N1 meaning/reading/drawing/Back routes, **64 kanji choices and 384 three-direct-word-guard records**. No actionable defect or consequential unresolved claim was established in this bounded scope. Actual N1 has zero curated wrong cards; its three production fallback labels were inspected, not replaced with the All pool. Untested seeds/pools remain unverified. Missing repeated JMdict ID in an existing navigation-only article's citation list is optional provenance polish; the linked support article and committed sources supply the exact evidence. No teaching or runtime bytes changed; all 8,441 manifest payload hashes/freshness reverified.

**Process qualification:** the first Claude follow-up overlapped exactly two panel reads. That original execution remains rejected for strict serial acceptance, with complete original report/raw records intact. After its process exited, the same session performed an accepted minimal three-read serial repair (own report and the two panels). Only then did GPT run; its reads were serial, including one additional original table capture. At most one reviewer process was active at any time. No original run was retroactively called compliant.

Native checkpoint 694 remains inherited evidence: two terminal cases 0/no skips, full archive through production ContentSync once, 1,118 kanji/5,071 words/127 N1/zero problems/parser epoch 1. No fresh native test, physical-phone, human-handwriting, successful MLKit, latest-app-main or general-release acceptance is claimed. Qualified TESTONLY Android remains ``1c1b7bf4`` with production ``f9b59a2``; owned emulator is stopped.

**Next:** same batch 095, non-rewriting integration of current main (``da374717`` at this checkpoint), substantive-change review if needed, all combined-tree acceptance checks, then normal signing/owner fast-forward/terminal CI/exact public ZIP and unchanged budget gates. No publication or batch 096 here. **Published 121/1,228; 1,107 remaining.** Physical-phone/general-release/whole-set acceptance remains outstanding. Parent runner lock untouched; no optional historical-session helper access or new permission denial.
"@
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $payload = "$control\batch-095-rendered-695-issue-payload.json"
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
