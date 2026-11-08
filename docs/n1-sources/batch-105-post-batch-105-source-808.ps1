$ErrorActionPreference = 'Stop'
$control = 'C:\Users\stop-\n1-kanji-workspace\control'
$repo = 'C:\Users\stop-\n1-kanji-workspace\learning-japanese'
$logs = "$control\logs\2fe17ac2-9fd1-4657-8231-22e9510a84b9"
Set-Location $repo
$head = (& git rev-parse HEAD).Trim()
if ((& git rev-parse 'HEAD^') -ne 'c2abec23b8feeb639b0773bd06b96022cd8ddda8') { throw 'Unexpected checkpoint parent' }
if ((& git log -1 '--format=%G?') -ne 'G') { throw 'Invalid signature' }
if (& git status --porcelain --untracked-files=all) { throw 'Checkpoint worktree dirty' }
$body = @"
Batch 105 / checkpoint 808: **source completion saved locally; no new runtime publication**.

Normally signed local commit: ``$head``. Published main remains ``047c2cef6b6a48b1738f2c5957de01be481c63e1``.

Frozen row116 勁 is source-ready for a later bounded unreviewed runtime draft. Exact evidence retains nine complete member families plus28 complete comparison families (36 distinct total), nine complete raw character records,49 fully inspected existing article bodies including11 actual legacy two-choice fallback cards, and four actual Digital Daijisen entries. All five frozen input hashes and both decompressed dictionary hashes passed; no source bytes or historical receipts were replaced.

Full metadata [ケイ]/[つよ.い] stays in source order; proposed practice is [ケイ]/[] with one necessary 雄勁ゆうけい support article, no inferred vocabulary level. 勁い remains documented search-only recognition, not an ordinary spelling or a quiz question. Existing 強い/N5/つよい stays unchanged. Exact character/word entries support the selected allocation and the attested 雄勁な筆跡 example; explain な and do not invent a generic strong substitution, gender restriction, automaticする or absolute art-only boundary. 雄 remains a plain component with complete word metadata, not an out-of-batch card.

The source plan fixes three existing N1 wrong choices 功/劾/剖, four demonstrated direct kanji safeguards 強/剛/力/勢 and six direct word safeguards 強い/強力/力強い/剛健/力/勢い. These are symmetric nontransitive pair guards, not synonym cliques or universal semantic safety. There is one mapped pair/two link directions, no activated baseline pair and no baseline runtime edit. Ordinary secondary senses and actual labels were inspected; unrelated legacy two-choice cards are not silently rewritten.

The unchanged pinned converter and nine-path SVG are ready, but geometry is not generated. Proposed22-Han audit finds 刂/勁/巠 absent from all three bundled cmaps: **not a glyph failure**, and final actual-Han/four-font/default-system native fallback readability remains mandatory. Modern 巠+力 mnemonic is not etymology; preserve canonical 力/no19 and structure-unclassified.

43 focused source tests, validation, regenerated unchanged manifest, budget, vocabulary consistency and exact source/baseline/runtime audits passed. All8,466 runtime hashes/contentVersion a5bc9b199c7df334 are unchanged. Vocabulary coverage remains2122/2431 reviewed prompts at pilot stage. The initial local extraction/all-three-choice assumptions were caught by assertions and corrected against actual wrapper/metadata evidence before saving; no new permission denial occurred.

No runtime draft/push, independent review, Android/native run or phone acceptance is claimed. Published additions remain **131/1,228;1,097 acceptance remainder**. Every original two-serial-family review, qualified Android/native/rendered, combined-current-main, normal signing, terminalCI and exact immutable ZIP/hash/budget gate remains required. Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 clients are required; old clients ignore curation/guards. Physical-phone, general-release and whole-set acceptance remain outstanding.

Next: SAME105 bounded LOCAL UNREVIEWED runtime draft/freeze only. Parent runner PID13320 retains lock ownership; no child lock acquisition/read/delete/unlock, optional historical-session helper access, batch106 or second runner.
"@
$bodyPath = "$control\batch-105-source-808-issue-body.txt"
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
    [IO.File]::WriteAllText("$logs\issue-receipt-808.json", ($receipt | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
