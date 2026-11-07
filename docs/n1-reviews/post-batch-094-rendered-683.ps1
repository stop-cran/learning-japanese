$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$prefix = Join-Path $control 'batch-094-rendered-683-issue-'
foreach ($suffix in @('body.txt', 'posted.json', 'receipt.json')) {
    if (Test-Path -LiteralPath ($prefix + $suffix)) { throw 'Existing issue evidence; inspect instead of reposting.' }
}
$head = git -C $content rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Normal signed head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Worktree not wholly clean.' }
$evidence = Get-Content "$content\docs\n1-sources\execution-683.json" -Raw | ConvertFrom-Json
if ($evidence.runtimeAccepted -or $evidence.runtimePublished -or $evidence.runtimeChanged) { throw 'Unexpected runtime acceptance.' }
$body = @"
### Batch 094: rendered-review checkpoint 683 (not publication)

Saved normally signed LOCAL evidence at ``$head``; teaching and all 8,438 runtime hashes remain unchanged. The two original model-family sessions inspected the frozen native evidence, complete sampled choice records, and exact frozen dictionary families. This is dependent confirmation, **not new blind-review credit**. Complete reports, raw events, actual models, image returns and process audits are preserved in ``docs/n1-reviews/batch-094-rendered-reconciliation-683.json`` and ``docs/n1-sources/execution-683.json``.

No actionable visual defect was established within the five font panels/all 41 Han and twenty reduced contact sheets/all 80 route captures. Original Claude execution requested panels 1+2 together: that execution remains **rejected for strict serial acceptance**. Its complete report is preserved; a separate three-read serial follow-up freshly confirmed those two panels without relabeling the original compliant. GPT ran only after both Claude processes exited. Image scale, inherited API35/native receipts, test-only app baseline and other original limits remain explicit.

The observed **削る / 縮める** word-quiz overlap is an actionable minor finding: actual All-stack seeds 7/15 show the pair in both directions; complete JMdict 1298090 sense 2 and 1337570 sense 1 support shared ordinary reduction/shortening meanings. Next bounded checkpoint: add only that direct exclusion, preserve all original metadata/prose, validate and regenerate the manifest, freeze normally signed local correction, obtain both original-session bounded confirmations and verify the changed exact import/builder evidence. No transitive-clique expansion or cosmetic rewriting is authorized by this finding.

No runtime correction or publication occurred here. All current-main integration, combined checks, normal signing, owner fast-forward, terminal CI, exact public ZIP/hash/budget and acceptance gates remain. Parent lock untouched; no optional historical-session helper access, new permission denial or second runner. **Published 120/1,228; 1,108 remaining.** Physical-phone/general-release and whole-set acceptance remain outstanding; batch 095 has not started.
"@
[IO.File]::WriteAllText(($prefix + 'body.txt'), $body, [Text.UTF8Encoding]::new($false))
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    @{body=$body} | ConvertTo-Json -Depth 2 | Set-Content ($prefix + 'payload.json') -Encoding utf8NoBOM
    gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input ($prefix + 'payload.json') |
        Set-Content ($prefix + 'posted.json') -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue post failed; preserve response.' }
    $posted = Get-Content ($prefix + 'posted.json') -Raw | ConvertFrom-Json
    if ($posted.user.login -ne 'stop-cran' -or $posted.body -cne $body) { throw 'Posted body/author mismatch.' }
    gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" |
        Set-Content ($prefix + 'receipt.json') -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Independent receipt fetch failed.' }
    $verified = Get-Content ($prefix + 'receipt.json') -Raw | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Verified body/author mismatch.' }
    $verified.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
