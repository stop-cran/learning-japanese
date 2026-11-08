$ErrorActionPreference = 'Stop'
$control = 'C:\Users\stop-\n1-kanji-workspace\control'
$repo = 'C:\Users\stop-\n1-kanji-workspace\learning-japanese'
$logs = "$control\logs\1a8efc89-5c08-4ef4-8a51-6813b11bd676"
Set-Location $repo
$head = (& git rev-parse HEAD).Trim()
if ((& git rev-parse 'HEAD^') -ne 'ddd01d5fea912de7a3d43cd25bdc631b5e0ac0ed') { throw 'Unexpected draft parent' }
if ((& git log -1 '--format=%G?') -ne 'G') { throw 'Invalid signature' }
if (& git status --porcelain --untracked-files=all) { throw 'Draft worktree dirty' }
$body = @"
Batch 105 / checkpoint 809: **bounded LOCAL UNREVIEWED runtime draft saved; no publication**.

Normally signed local freeze: ``$head``. Published main remains ``047c2cef6b6a48b1738f2c5957de01be481c63e1``.

Drafted frozen row116 勁 plus its one necessary support article 雄勁ゆうけい and generated nine-stroke geometry. Full source metadata [ケイ]/[つよ.い] is preserved; practice selects [ケイ]/[] (けい). 勁い remains explicitly search-only recognition, not ordinary spelling, a duplicate article or a reading question. Existing 強い/N5/つよい is untouched. 雄勁 teaches vigorous style in art/prose using the attested 雄勁な筆跡 phrase, explains な, and carries no inferred vocabulary level. 雄 remains a plain component with complete written-word metadata, not an out-of-batch card.

The draft has three existing N1 wrong choices 功/劾/剖, four direct kanji safeguards 強/剛/力/勢 and six direct word safeguards 強い/強力/力強い/剛健/力/勢い. These are symmetric nontransitive pair guards, not synonym cliques or universal semantic safety. One mapped pair links both ways; there are no activated baseline pairs or baseline runtime edits. Modern 巠+力 mnemonic is not etymology; canonical 力/no19 and structure-unclassified remain.

The retained pinned SVG was converted with the unchanged pinned converter:9 paths/16 points per path, exact output verified. All8,466 baseline runtime hashes are preserved; the manifest adds only kanji/勁.md, words/雄勁.md and strokes/勁.json. New contentVersion:5572c6c467e6b73b. Actual draft inventory is14 Han, all verified against frozen Unicode; 刂/勁/巠 are absent from all three bundled cmaps. **Cmap absence is not a glyph failure.** Fresh four-font/default-system native fallback and readability acceptance remains mandatory.

87 focused validator tests, validation, regenerated/fresh manifest, vocabulary consistency, budget, frozen-input/metadata/baseline/link/reading/stroke/font and whitespace checks passed. Measured local budget:8,491 entries,44,421,542 retained bytes,44,689,880 inflated bytes,30,316,766 local ZIP bytes; all unchanged publishing guards remain. Vocabulary coverage remains2122/2431 reviewed prompts at pilot stage, not full coverage.

Source-completion808's full49 older-body/28 comparison-family inspection is inherited evidence, not claimed as a fresh full reread. The exact draft audit, logs and durable authoring recipe are committed. No independent reviewer, Android/native run, rendered acceptance, runtime push or phone acceptance is claimed.

Published additions remain **131/1,228;1,097 acceptance remainder**. Next is SAME105's two serial blind different-model-family textual initial reviews of this same frozen snapshot, covering both complete new articles and all three review facets. Every original qualified Android/finite-semantic/native/rendered, combined-current-main/full-suite, normal signing, terminalCI and exact immutable ZIP/hash/budget gate remains required after reconciliation. Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 clients are required; old clients ignore curation/guards. Physical-phone, general-release and whole-set acceptance remain outstanding.

Parent runner PID13320 retains lock ownership; no child lock acquisition/read/delete/unlock or optional historical-session helper access occurred. No batch106 or second runner was started.
"@
$bodyPath = "$control\batch-105-draft-809-issue-body.txt"
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
    [IO.File]::WriteAllText("$logs\issue-receipt-809.json", ($receipt | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
