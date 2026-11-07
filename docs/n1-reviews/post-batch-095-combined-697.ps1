$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$bodyPath = "$control\batch-095-combined-697-issue-body.txt"
$postedPath = "$control\batch-095-combined-697-issue-posted.json"
$receiptPath = "$control\batch-095-combined-697-issue-receipt.json"
foreach ($path in @($bodyPath, $postedPath, $receiptPath)) {
    if (Test-Path -LiteralPath $path) { throw 'Existing receipt; inspect rather than repost.' }
}
$head = git -C $content rev-parse HEAD
$parent = git -C $content rev-parse HEAD^
if ($LASTEXITCODE -ne 0 -or $parent -ne '6c9450427e476fd60437520cdedae693d77bbdcc' -or
    (git -C $content log -1 '--format=%G?') -ne 'G') { throw 'Normally signed exact child evidence head required.' }
if ((git -C $content status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Content worktree not wholly clean.' }
$evidence = Get-Content "$content\docs\n1-sources\execution-697.json" -Raw | ConvertFrom-Json
if ($evidence.actionableRemainingFindings -ne 0 -or $evidence.consequentialUnresolvedInScopeClaims -ne 0 -or
    $evidence.runtimePublished -or $evidence.runtimeAccepted -or
    $evidence.exactCombinedNativeImport -ne 'pending') { throw 'Unexpected evidence state.' }
$body = @"
### Batch 095: combined-main teaching checkpoint 697 (not publication)

Saved normally signed LOCAL evidence at ``$head``; both dedicated worktrees remain clean. Original **Claude Opus 5.5** and **GPT-6.1 Sol** sessions completed the required bounded dependent confirmations of the incoming eleven-file current-main teaching delta on the same frozen signed ``6c945042`` snapshot (combined merge ``d5a6823c``). Actual model/session/process/tool evidence, original complete reports, common packets, ten complete frozen JMdict families and reconciliation are preserved in ``docs/n1-reviews/batch-095-combined-teaching-reconciliation-697.json`` and ``docs/n1-sources/execution-697.json``. This is not new blind batch-review credit.

Both reviewers received all six common text chunks: exact incoming diff, eleven complete current articles, three unchanged comparison articles, ten full dictionary families and source navigation without the upstream review/adjudication. Each independently fetched the eight actual public sources. Claude exited before GPT started; both processes exited 0, with no overlapping or unfinished tool calls. All eleven changed passages are **CLEAN separately for correctness, scoped coverage and textual comprehensibility**; no actionable defect or consequential unresolved claim remains in this bounded scope. Two Claude suggestions (pin the live Wiktionary link; explain source-local smallness wording) remain optional, with evidence-based dispositions; no runtime edit was needed.

Source limits remain explicit: both inspected the relevant Daijisen 子 senses, but neither freshly inspected Daijisen's 菓子 heading; Nipponica directly supports the historical fruit claim (Claude preview only; GPT additional bounded ranges). Other large-page truncations are preserved. The attributed competing accounts of ゆず do not establish ultimate etymological consensus. Original 691/694/695 records remain inherited with all their limits, including the rejected original Claude695 overlap and its separate minimal serial repair.

All **8,441 runtime manifest hashes**, manifest freshness, validation and unchanged archive budgets were reverified; ``3eebfff0fdad5e28`` is unchanged. Checkpoint696's 372 Python tests, four non-skipped Android cases and combined source/baseline/reading/stroke/link/font checks remain inherited, not newly executed here.

**Next gate:** a clearly named new full combined archive through production ContentSync **once**, asserting actual imported counts/problems and accepted Room version ``3eebfff0fdad5e28``/reading epoch1 plus curation, direct guards and links. The older native694 import is not this changed manifest. No new native/phone/human-handwriting/MLKit/latest-app-main/full-pool/CI/public-ZIP/publication acceptance is claimed. Afterwards retain fresh-main integration/revalidation, normal signing, owner fast-forward, terminal CI, exact immutable public ZIP and original budget gates.

No runtime publication or batch096 here. **Published 121/1,228; 1,107 remaining.** Physical-phone/general-release/whole-set acceptance remains outstanding. Parent runner lock untouched; no optional historical-session helper access or new permission denial.
"@
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $payload = "$control\batch-095-combined-697-issue-payload.json"
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
