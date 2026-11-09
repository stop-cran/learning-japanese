$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$artifacts = "$control\artifacts\batch-108-textual-862"
$head = (git -C $repo rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Cannot authenticate evidence commit' }
if ((git -C $repo rev-parse 'HEAD^').Trim() -ne '9955ac122d1b4f1084f702d3d6d5afeb82d35e3a' -or
    (git -C $repo log -1 '--format=%G?').Trim() -ne 'G') {
    throw 'Unexpected evidence parent or signature'
}
if (git -C $repo status --porcelain --untracked-files=all) { throw 'Evidence worktree not wholly clean' }
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
$coordinator = Get-CimInstance Win32_Process -Filter 'ProcessId=29432'
if ($runner.status -ne 'running' -or $runner.sessionId -ne 'c60bb35d-39a2-4212-b8ce-adede31eff34' -or
    $runner.pid -ne 27864 -or $coordinator.ParentProcessId -ne 27864) {
    throw 'Live runner ownership uncertain'
}
$marker = 'Batch 108 / checkpoint 862:'
$body = [IO.File]::ReadAllText("$control\batch-108-textual-862-issue-template.txt").Replace('__EVIDENCE_COMMIT__', $head)
$bodyPath = "$artifacts\issue-body.txt"
if (Test-Path -LiteralPath $bodyPath) { throw 'Issue attempt already exists; preserve without blind repost' }
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable' }
    if ((gh api user --jq '.login').Trim() -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Unexpected issue identity' }
    $raw = gh api 'repos/stop-cran/learning-japanese/issues/60/comments?per_page=100' --paginate --slurp
    if ($LASTEXITCODE -ne 0) { throw 'Marker search failed; do not post' }
    $pages = ($raw -join "`n") | ConvertFrom-Json
    $found = @(foreach ($page in $pages) {
        foreach ($comment in $page) {
            if ($comment.user.login -eq 'stop-cran' -and $comment.body.Contains($marker)) {
                $comment | Select-Object id,html_url,body
            }
        }
    })
    [IO.File]::WriteAllText("$artifacts\issue-marker-search.json",
        (ConvertTo-Json -InputObject $found -Depth 5), [Text.UTF8Encoding]::new($false))
    if ($found.Count -gt 1) { throw 'Ambiguous marker; preserve and yield' }
    if ($found.Count -eq 1) {
        $url = $found[0].html_url
    } else {
        $url = (gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath).Trim()
        if ($LASTEXITCODE -ne 0) { throw 'Post outcome uncertain; do not repost' }
    }
    [IO.File]::WriteAllText("$artifacts\issue-post-url.txt", $url, [Text.UTF8Encoding]::new($false))
    if ($url -notmatch '#issuecomment-(\d+)$') { throw 'Issue URL uncertain; do not repost' }
    $id = $Matches[1]
    $raw = gh api "repos/stop-cran/learning-japanese/issues/comments/$id"
    if ($LASTEXITCODE -ne 0) { throw 'Receipt retrieval uncertain; do not repost' }
    [IO.File]::WriteAllText("$artifacts\issue-response.json", ($raw -join "`n"), [Text.UTF8Encoding]::new($false))
    $comment = ($raw -join "`n") | ConvertFrom-Json
    if ($comment.user.login -ne 'stop-cran' -or $comment.html_url -ne $url -or
        $comment.body.Replace("`r`n", "`n").TrimEnd() -ne $body.Replace("`r`n", "`n").TrimEnd()) {
        throw 'Owner/body/URL verification failed'
    }
    $receipt = @{
        id=$comment.id; url=$url; author=$comment.user.login; verified=$true; localCommit=$head
        marker=$marker; existingMarkerCheckedBeforePosting=$true
        bodySha256=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData(
            [Text.Encoding]::UTF8.GetBytes($comment.body))).ToLowerInvariant()
    }
    [IO.File]::WriteAllText("$artifacts\issue-receipt.json", ($receipt | ConvertTo-Json -Depth 4),
        [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
