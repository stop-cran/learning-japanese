$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = "$control\..\learning-japanese"
$logs = "$control\logs\4656604b-eebf-4190-bcb5-d2e6ae5ddd3e"
Set-Location $repo
$head = (& git rev-parse HEAD).Trim()
if ((git rev-parse 'HEAD^') -ne '5fe224b5c611e8ca0c7c5a1fcbd5ea4a025e606a' -or
    (git log -1 '--format=%G?') -ne 'G' -or
    (git status --porcelain --untracked-files=all)) { throw 'Expected clean normally signed review checkpoint' }
$body = @"
Batch106 / checkpoint822: **two-family independent textual review complete; teaching unchanged; no publication**.

Normally signed local evidence checkpoint: ``$head``. Blind initial reviewers examined the SAME signed draft ``5fe224b5c611e8ca0c7c5a1fcbd5ea4a025e606a``: complete new 勅 and necessary support 勅令, plus the exact new teaching line in 令, all three facets per unit,28 existing comparison/fallback bodies,79 distinct complete JMdict families,10 raw character records and3 archived public texts. Actual returned models: Claude Opus5.5 (claude-opus-5.5) and GPT-6.1 Sol (gpt-6.1-sol). Each used exactly one read-only view returning the complete identical common packet, with no truncation/internal overlap/unfinished tool. First process exited before second started. Complete original reports, lossless raw executions, actual sessions/models/configuration and returned-byte limits are preserved.

Both new articles and the changed令line received CLEAN for correctness, scoped coverage and phone-TEXT comprehensibility. No established actionable textual defect or consequential unresolved positive teaching claim remains; modern writtenいまし.める remains explicitly unverified, not endorsed. The weak potential勅/訓fallback concern is retained for actual finite-option assessment, not forced withdrawn or promoted to a new guard without evidence. Equivalent observations across whole reports were compared; no unique verified defect or model ranking is claimed. Optional display-key wording, overlap wording, source-footer and vocabulary expansion remain optional. No teaching changed, so changed-passage confirmations are unnecessary here.

Exact full on[チョク]/kun[いまし.める,みことのり], selected[チョク]/[] normalized keyちょく, documented nounみことのり and outside-Joyo-reading-list qualification,9 generated strokes,2 direct kanji/6 direct word guards,2 reciprocal pairs/4 directions and the single exact令addition remain unchanged. Sovereign-general and Meiji legal meanings stay distinct without a blanket legal-validity claim. 勅令 has no inferred vocabulary level and is necessary support, NOT N1 vocabulary delivery.

Focused source tests, validation, regenerated unchanged manifest, vocabulary consistency, review/process/provenance/runtime preservation, whitespace and unchanged archive-budget checks passed; exact logs committed. Runtime/manifest bytes match the frozen draft. All original source/draft/acceptance/historical limits remain intact.

**Textual acceptance is not actual quiz/native/phone acceptance.** Next bounded checkpoint: SAME106 qualified signed stop-cran/kanji-cards-android ``bf30cdead8515739bc0e671d57a54b9a3109dd46`` HOST and finite semantic options in defaultN1/All/custom/reduced pools, kanji and word BOTH directions, actual fallback labels including retained訓hypothesis, with non-skipped RealContentTest and RareHanTest. Later fresh native ContentSyncONCE/N1/All/meaning/reading/drawing/articles/Back/offline/allfourfont/defaultsystem/wholeword/radical/lookalike/rendered checks remain mandatory. Cmap presence/absence does not prove readability. Combined-current-main/full-suite, normal signing, owner fast-forward push, terminalgreenCI and every immutable ZIP runtime hash/budget gate remain open; unchanged18000entries/42MiBcompressed/80MiBinflated/56MiBretained.

Published additions remain **132/1,228;1,096 acceptance remainder**. No runtime pushed or batch107 started. Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 required; old clients ignore curation/guards. Physical-phone, general-release and whole-set acceptance remain outstanding. Historical permission/process/read-depth/OOM/ANR/routing/rendering limits are preserved without retroacceptance. Parent PID13320 owns runner.lock; no child lock access/reacquisition/delete/unlock, optional historical-session helper access or second runner.
"@
$bodyPath = "$control\batch-106-review-822-issue-body.txt"
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
    [IO.File]::WriteAllText("$logs\issue-receipt-822.json", ($receipt | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
