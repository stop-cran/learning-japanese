$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$prefix = Join-Path $control 'batch-094-correction-685-issue-'
foreach ($suffix in @('body.txt', 'posted.json', 'receipt.json')) {
    if (Test-Path -LiteralPath ($prefix + $suffix)) { throw 'Existing issue evidence; inspect instead of reposting.' }
}
$head = git -C $content rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Normal signed head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Worktree not wholly clean.' }
$evidence = Get-Content "$content\docs\n1-sources\execution-685.json" -Raw | ConvertFrom-Json
if ($evidence.runtimeAccepted -or $evidence.runtimePublished -or $evidence.runtime.runtimeChangedThisExecution) {
    throw 'Unexpected runtime change or acceptance.'
}
$body = @"
### Batch 094: correction confirmations checkpoint 685 (not publication)

Saved normally signed LOCAL evidence at ``$head``. Both original model-family sessions, actual **claude-opus-5.5** and **gpt-6.1-sol**, confirmed the same frozen correction ``b85d7a4d`` / contentVersion ``74b7e886a1afbd46``: append only the directly source-backed **削る / 縮める** exclusion, preserving all prior exclusions/order, titles, identities, easier levels, readings, prose, links and geometry.

The original-session processes ran serially and exited 0; their three/two full text reads were strictly serial with no overlaps. Complete reports, raw events, actual models, common exact-diff/dictionary evidence and process audits are archived in ``docs/n1-reviews/batch-094-correction-reconciliation-685.json`` and ``docs/n1-sources/execution-685.json``. This is dependent confirmation, **not new blind-review credit**. Original 683 overlap/rejection/serial repair is preserved unchanged.

The observed finding is **resolved textually, partially resolved overall**: both reviewers found no actionable correction regression, but the **corrected exact native ContentSync import and production builder enforcement remain pending**. Next bounded checkpoint: import the full corrected archive once through production ContentSync and inspect the new direct guard in both quiz directions, both target orientations, All and bounded custom pools, with non-skipped terminal native evidence. The earlier 682 archive and 85 unchanged visual captures remain inherited evidence, not corrected-import evidence.

All 8,438 current runtime hashes and manifest freshness were verified; no runtime content changed in this execution. No new Android/native, physical-phone, human-handwriting/MLKit or publication acceptance is claimed. Current-main integration, combined checks, normal signing, owner fast-forward, terminal CI, exact public ZIP/hash/budget and all acceptance gates remain. Parent lock untouched; no optional historical-session helper access, new permission denial or second runner. **Published 120/1,228; 1,108 remaining.** Physical-phone/general-release and whole-set acceptance remain outstanding; batch 095 has not started.
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
