$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = "$control\..\learning-japanese"
$logs = "$control\logs\595bb5b4-8cc4-4f57-bcb1-4b31d3c6e957"
Set-Location $repo
$head = (& git rev-parse HEAD).Trim()
if ((git rev-parse 'HEAD^') -ne '27e252daa091e21c907ff6799818f6b2da74c7aa' -or
    (git log -1 '--format=%G?') -ne 'G' -or
    (git status --porcelain --untracked-files=all)) { throw 'Expected clean normally signed review checkpoint' }
$body = @"
Batch105 / checkpoint810: **two-family independent textual review complete; teaching unchanged; no publication**.

Normally signed local evidence checkpoint: ``$head``. Both blind initial reviewers examined the SAME signed draft ``27e252daa091e21c907ff6799818f6b2da74c7aa``: complete new 勁 and necessary support 雄勁, all three facets per article,49 existing comparison/fallback bodies,36 distinct complete JMdict families,9 raw character records and4 archived public dictionary texts. Actual returned models were Claude Opus5.5 (claude-opus-5.5) and GPT-6.1 Sol (gpt-6.1-sol). Each used exactly one read-only view returning the complete common packet; no truncation, internal tool overlap or unfinished tool. Claude exited before GPT started. Both complete original reports, raw lossless execution archives, sessions, tool/configuration and returned-byte limits are preserved.

Both articles received CLEAN for correctness, scoped coverage and phone-TEXT comprehensibility; no actionable textual defect or consequential unresolved textual claim was established. Two tentative 雄勁 quiz-pair concerns (活気/もりもり) were adjudicated against exact displayed labels and full senses, not model votes; neither establishes a mandatory extra guard. Equivalent observations across both full reports were compared, so no unique verified finding is claimed. Optional polish/expansion remains optional. No teaching changed, so changed-passage confirmations are unnecessary here.

Full on[ケイ]/kun[つよ.い], selected[ケイ]/[] keyけい, search-only勁い disposition, nine generated strokes,4 direct kanji/6 direct word guards,1 reciprocal pair/2 directions and zero baseline edits remain unchanged. 雄勁 has no inferred vocabulary level. Runtime and manifest bytes match the frozen draft; the complete8,466-entry published baseline remains preserved. Focused source tests, validation, regenerated/fresh unchanged manifest, vocabulary consistency, review/process/provenance/baseline audit, whitespace and unchanged archive-budget checks passed. Exact logs and reconciliation are committed.

**Textual acceptance is not live quiz/native/phone acceptance.** Next is SAME105's qualified stop-cran/kanji-cards-androidbf30cdead HOST+finite semantic defaultN1/All/custom actual-option acceptance with non-skipped RealContent/RareHan cases. Fresh ContentSyncONCE/N1/All/meaning/reading/drawing/article/Back/offline/four-font/default rendering (including 勁/巠/刂) remains mandatory afterward. Cmap absence is not glyph failure. Combined-current-main/full-suite, normal signing, owner fast-forward push, terminalgreenCI and every immutable ZIP runtime hash/budget gate remain open.

Published additions remain **131/1,228;1,097 acceptance remainder**. No runtime was pushed; support words are not N1 vocabulary delivery. Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 clients are required; old clients ignore curation/guards. Physical-phone, general-release and whole-set acceptance remain outstanding. Historical evidence/permission/process/read-depth/OOM/ANR/routing limits are preserved without retroacceptance. Parent PID13320 owns the runner lock; no child lock access/reacquisition/delete/unlock, optional historical-session helper access, batch106 or second runner.
"@
$bodyPath = "$control\batch-105-review-810-issue-body.txt"
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (& gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable' }
    $login = (& gh api user --jq '.login').Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Unexpected issue identity' }
    $url = (& gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed' }
    $id = ($url -split 'issuecomment-')[1]
    $comment = (& gh api "repos/stop-cran/learning-japanese/issues/comments/$id" | ConvertFrom-Json)
    if ($LASTEXITCODE -ne 0 -or $comment.user.login -ne 'stop-cran') { throw 'Issue author verification failed' }
    if ($comment.body.Replace("`r`n", "`n") -ne $body.Replace("`r`n", "`n")) { throw 'Issue body verification failed' }
    $receipt = @{
        id=$comment.id; url=$url; author=$comment.user.login; verified=$true; localCommit=$head
        bodySha256=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($comment.body))).ToLowerInvariant()
    }
    [IO.File]::WriteAllText("$logs\issue-receipt-810.json", ($receipt | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
