$ErrorActionPreference = 'Stop'
$control = 'C:\Users\stop-\n1-kanji-workspace\control'
$repo = 'C:\Users\stop-\n1-kanji-workspace\learning-japanese'
$logs = "$control\logs\07145dbf-b4fc-49c3-86c1-f2eee5205283"
Set-Location $repo
$head = (& git rev-parse HEAD).Trim()
if ((& git rev-parse 'HEAD^') -ne '047c2cef6b6a48b1738f2c5957de01be481c63e1') { throw 'Unexpected checkpoint parent' }
if ((& git log -1 '--format=%G?') -ne 'G') { throw 'Invalid signature' }
if (& git status --porcelain --untracked-files=all) { throw 'Checkpoint worktree dirty' }
$body = @"
Batch 105 / checkpoint 807: **LOCAL source-only checkpoint**, not newly published teaching.

Normally signed saved commit: ``$head``; published main remains ``047c2cef6b6a48b1738f2c5957de01be481c63e1``.

Frozen row 116 勁: retained and author-inspected all nine complete applicable JMdict families, the complete character record, four existing comparison articles, three actual Digital Daijisen blocks, and the pinned nine-path SVG (not converted). Five frozen input hashes and both decompressed dictionary hashes passed. Full metadata [ケイ]/[つよ.い] remains in source order. Proposed practice is [ケイ]/[] with one necessary 雄勁ゆうけい support article, not an inferred vocabulary level.

The full 強い family explicitly marks 勁い search-only: retain the documented kun as qualified recognition, not an ordinary spelling or a proposed quiz question. Existing 強い/N5 stays unchanged; linking it is not evidence that its written 強 supplies a 勁 reading. 雄勁's actual word entry supports descriptive vigor in writing/art and the な pattern; no unrestricted substitution for 強い or absolute art-only rule is claimed. 勁草 remains an inspected alternative candidate; its literal grass and steadfastness metaphor are not collapsed into an unrestricted resistant-idea gloss.

No existing written/primary-reading support candidate or activated baseline pair was found. One proposed all-mapped pair/two directions. 雄 has no card: preserve complete proposed word metadata, inspect its raw character record before assigning ユウ, and do not add an out-of-batch card or broken link. Strong/power labels on 強, 剛 and 力 need complete comparison-family, fallback and direct-pair investigation; they are not accepted wrong choices or decided guards. Exact labels, three wrong distractors, necessary direct symmetric nontransitive safeguards, support teaching, complete links/baseline/Han/fonts and conversion planning remain required **before runtime drafting**.

43 focused source tests, structural validation, unchanged regenerated manifest, archive budget, vocabulary consistency and exact packet/runtime audits passed. All 8,466 runtime hashes/contentVersion a5bc9b199c7df334 are unchanged. Vocabulary consistency remains its reported pilot scope, not whole-corpus annotation completion. The initial local console-encoding failure was corrected to UTF-8 and exact archives regenerated/re-audited; no new permission denial occurred.

No reviewer, Android/native run, runtime draft/push, phone evidence or acceptance credit is claimed. Published additions remain **131/1,228; 1,097 acceptance remainder**. Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 clients remain required; old clients ignore curation/guards. Physical-phone, general-release and whole-set acceptance remain outstanding. Historical review/process/rendering/permission/OOM limitations and every original publication gate are preserved.

Next: SAME105 bounded source completion, then a later local unreviewed runtime freeze only when source-ready. Parent runner PID 13320 retained lock ownership; no child lock acquisition/read/delete/unlock or historical-session helper access. No batch106 or second runner.
"@
$bodyPath = "$control\batch-105-source-807-issue-body.txt"
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
        id = $comment.id
        url = $url
        author = $comment.user.login
        bodySha256 = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($comment.body))).ToLowerInvariant()
        verified = $true
        localCommit = $head
    }
    [IO.File]::WriteAllText("$logs\issue-receipt-807.json", ($receipt | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
