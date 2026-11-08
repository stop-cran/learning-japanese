$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = "$control\..\learning-japanese"
$logs = "$control\logs\2472a3c1-ac5f-4972-aa59-315365085f22"
Set-Location $repo
$head = (git rev-parse HEAD).Trim()
if ((git rev-parse 'HEAD^') -ne '0c582f18b31f65a5e1a908d92e37dde3d34f81ee' -or $LASTEXITCODE -ne 0) {
    throw 'Unexpected checkpoint parent'
}
if ((git log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Invalid signature' }
if ((git status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Checkpoint worktree dirty' }
$body = @"
Batch 106 / checkpoint 819: **LOCAL initial source-only checkpoint**, not new published teaching.

Normally signed saved commit: ``$head``; published main remains ``0c582f18b31f65a5e1a908d92e37dde3d34f81ee``.

Frozen row117 勅: retained and author-inspected all44 complete member JMdict families plus17 complete comparison families, FOUR full raw character records, FIVE actual existing articles, the exact Digital Daijisen character/nounちょく/nounみことのり headings and both勅令 senses, and the pinned NINE-path SVG (not converted). Five frozen input hashes and both decompressed dictionary hashes passed.

Full metadata [チョク]/[いまし.める,みことのり] stays in source order. Proposed practice [チョク]/[] and one necessary 勅令ちょくれい support remain **provisional**. No vocabulary level is inferred. いまし.める is documented by KANJIDIC2; the frozen member families provide no lexical example, while complete exact-reading families distinguish 戒める/誡める/警める from rope-binding 縛める, none written with勅. Exact contemporary written use/register remains UNVERIFIED: retain qualified source-only information, not an invented ordinary 勅める example or a dropped/invalid reading. みことのり IS a documented reading of勅, NOT search-only; the dictionary's ▽ notation and final usefulness still need examination.

The proposed compound's general sovereign-order sense must stay distinct from its specific Meiji-constitution legal sense. No blanket Japanese-emperor-only, ordinary-command substitution or every-old-edict-is-void claim is established. Exact natural examples, labels, three wrong distractors, ordinary secondary senses, direct symmetric NONTRANSITIVE safeguards and fallback audit remain pending.

No existing written/primary-reading candidate or activated frozen member pair was found. If勅令 is selected, all-mapped accounting includes TWO pairs/FOUR link directions through both勅 and令. Adding a勅令 common-word line to the existing令 card would be **new example teaching**, not a pre-existing-text navigation-only edit, and must be sourced/reviewed. Final support/curation, comparison/quiz/link/baseline/Han/font and converter plan remain required BEFORE runtime drafting.

43 focused source tests, validation, unchanged regenerated manifest, budget, vocabulary consistency and exact packet/baseline/runtime audits passed. All1128 kanji/5079 word metadata and bytes, all8469 runtime hashes and contentVersion5572c6c467e6b73b are unchanged. Vocabulary consistency retains its reported pilot scope, not whole-corpus completion. Initial console encoding, redundant beyond-EOF range and corrected over-broad generated dictionary-wrapper extraction diagnostics are preserved; no permission denial or lost evidence occurred.

No reviewer, Android/native run, runtime draft/push, phone evidence or acceptance credit is claimed. Published additions remain **132/1228;1096 acceptance remainder**. Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 clients remain required; old clients ignore curation/guards. Physical-phone, general-release and whole-set acceptance remain outstanding. All historical limitations and original acceptance/publication gates remain intact.

Next: SAME106 bounded source completion, then a later local unreviewed runtime freeze only when source-ready. Parent runner PID13320 retained lock ownership; no child lock acquisition/read/delete/unlock or historical-session helper access. No107 or second runner.
"@
$bodyPath = "$control\batch-106-source-819-issue-body.txt"
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable' }
    $login = (gh api user --jq '.login').Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Unexpected issue identity' }
    $url = (gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed' }
    $id = ($url -split 'issuecomment-')[1]
    $raw = gh api "repos/stop-cran/learning-japanese/issues/comments/$id"
    if ($LASTEXITCODE -ne 0) { throw 'Issue receipt retrieval failed' }
    $comment = $raw | ConvertFrom-Json
    if ($comment.user.login -ne 'stop-cran') { throw 'Issue author verification failed' }
    if ($comment.body.Replace("`r`n", "`n") -ne $body.Replace("`r`n", "`n")) { throw 'Issue body verification failed' }
    $receipt = @{
        id=$comment.id; url=$url; author=$comment.user.login; verified=$true; localCommit=$head
        bodySha256=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData(
            [Text.Encoding]::UTF8.GetBytes($comment.body))).ToLowerInvariant()
    }
    [IO.File]::WriteAllText("$logs\issue-receipt-819.json", ($receipt | ConvertTo-Json -Depth 4),
                          [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
