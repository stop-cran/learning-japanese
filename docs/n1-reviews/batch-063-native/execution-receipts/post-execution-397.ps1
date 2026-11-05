$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$head = & git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot identify signed local checkpoint' }
if ((& git -C $root show -s '--format=%G?' HEAD) -ne 'G') { throw 'Normal valid signature required' }
$body = @"
Batch063 bounded native/visual confirmation closed at local signed evidence commit ``$head``; teaching remains unchanged at ``ddad655f71c06e7cb2c749de18596863a800a73d``. This is NOT a runtime publication.

Reused ORIGINAL ``claude-opus-5.5`` and ``gpt-6.1-sol`` sessions serially for dependent visual confirmation. Both actual models verified from execution/usage, exited0; complete Claude report/execution archive preceded GPT launch. View-only configuration, onecallperresponse, zero overlaps/failedtools/truncations. Each read all3 teaching files, four bounded native fixture ranges, terminal log/route receipt and25PNGnames with20distinctsourcebytehashes. Both found no actionable content defect across correctness/scopedcoverage/boundedcomprehensibility. Their approximate19visuallydifferentstates are not sourcebyte counts; original reports preserved unchanged. Optional wrapping/spacing/chip/appdrawingwording suggestions not adopted as content changes.

Actual four production font rows show readable targets including fallback亻/傚 and倣/放 distinction. Newly inspected kanji-meaning screenshot exposes BOTH complete reading rows; shifted kanji-on-reading clips leftlabels. Prior396 narrower coordinator inspection remains historical. Current visual supplement distinguishes inherited35family/source judgments, freshpixels and supplied396native2terminal0 results. No fresh native/Android rerun. Actual quiz meaning options were riceplant/salary;stipend/willow/imitate;emulate, not authored放/方/付. Both reading tasks/feedback visible; On/KunGood and DrawAgain persistence supplied from fixture. No new persisted meaninggrade, MLKit recognition, successfulhumanrecall or fallbackface identification claimed.

HistoricalClaude063-P1 one overlappingtwo-view response remains noncompliant; later dependent confirmations do not retroactively grant strictinitialprocess acceptance. Complete reports/prompts/model/tool/range/serialization/imagehash evidence and reconciliation are in ``docs/n1-reviews/batch-063-visual-*`` and ``batch-063-native-acceptance.json``. Validator/manifestfreshness/originalarchivebudgets pass; runtime remains8317manifestfiles/versionc19b742b7e6320a7.

Checkpoint397/statuscontinue, FULL controlhistory preserved. NEXT: latestmain normalnonrewriting integration, allcombined validation/audits, normal signing and authorizedowner fastforwardpush, terminalgreenCI and EVERYimmutablepublicZIPruntimehash/budgets BEFOREdelivery or064. Published89/1228,1139remaining; localdraft90 NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. No batch064 or secondrunner.
"@
$bodyPath = Join-Path $PSScriptRoot 'execution-397-issue-body.txt'
if (Test-Path $bodyPath) { throw 'Never overwrite original issue evidence' }
[IO.File]::WriteAllText($bodyPath, $body)
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Unexpected inherited token' }
try {
    $env:GH_TOKEN = & gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner authentication unavailable' }
    $login = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Wrong command-scoped identity' }
    $url = & gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed' }
    $id = ($url -split 'issuecomment-')[-1]
    $comment = & gh api "repos/stop-cran/learning-japanese/issues/comments/$id" | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0 -or $comment.user.login -ne 'stop-cran') { throw 'Public issue author verification failed' }
    $normalize = { param($text) $text.Replace("`r`n", "`n").TrimEnd("`r", "`n") }
    if ((& $normalize $comment.body) -ne (& $normalize $body)) { throw 'Public issue body verification failed' }
    @{
        url = $url
        commentId = [long]$id
        author = $comment.user.login
        bodyVerified = $true
        localCommit = $head
        runtimePublished = $false
        bodyComparison = 'Exact text after CRLF-to-LF and trailing-newline normalization.'
    } | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot 'execution-397-issue-receipt.json')
    Write-Output $url
}
finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
