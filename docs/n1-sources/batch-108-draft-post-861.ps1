$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$logs = "$control\logs\68a0ce7a-9dab-430c-b0ad-8a474a9c56fa"
$head = (git -C $repo rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Cannot authenticate draft commit' }
if ((git -C $repo rev-parse 'HEAD^').Trim() -ne '64b30465652a60d891291a64ca075aa107a2d01a' -or
    (git -C $repo log -1 '--format=%G?').Trim() -ne 'G') {
    throw 'Unexpected draft-checkpoint parent or signature'
}
if (git -C $repo status --porcelain --untracked-files=all) { throw 'Draft worktree not wholly clean' }
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
$coordinator = Get-CimInstance Win32_Process -Filter 'ProcessId=29460'
$parent = Get-CimInstance Win32_Process -Filter 'ProcessId=27864'
if ($runner.status -ne 'running' -or $runner.sessionId -ne '68a0ce7a-9dab-430c-b0ad-8a474a9c56fa' -or
    $runner.pid -ne 27864 -or $coordinator.ParentProcessId -ne $parent.ProcessId) {
    throw 'Live runner ownership uncertain'
}
$marker = 'Batch 108 / checkpoint 861:'
$body = [IO.File]::ReadAllText("$control\batch-108-draft-861-issue-template.txt").Replace('__DRAFT_COMMIT__', $head)
$bodyPath = "$control\batch-108-draft-861-issue-body.txt"
if (Test-Path -LiteralPath $bodyPath) {
    if ([IO.File]::ReadAllText($bodyPath) -ne $body) { throw 'Existing issue body differs' }
} else {
    [IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
}
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable' }
    $login = (gh api user --jq '.login').Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Unexpected issue identity' }
    $raw = gh api 'repos/stop-cran/learning-japanese/issues/60/comments?per_page=100' --paginate --slurp
    if ($LASTEXITCODE -ne 0) { throw 'Existing marker search failed; do not post' }
    $pages = ($raw -join "`n") | ConvertFrom-Json
    $found = @(foreach ($page in $pages) {
        foreach ($comment in $page) {
            if ($comment.user.login -eq 'stop-cran' -and $comment.body.Contains($marker)) {
                $comment | Select-Object id,html_url,body
            }
        }
    })
    [IO.File]::WriteAllText("$logs\issue-marker-search-861.json",
        (ConvertTo-Json -InputObject $found -Depth 5), [Text.UTF8Encoding]::new($false))
    if ($found.Count -gt 1) { throw 'Ambiguous marker; preserve and yield' }
    if ($found.Count -eq 1) {
        $url = $found[0].html_url
    } else {
        $url = (gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath).Trim()
        if ($LASTEXITCODE -ne 0) { throw 'Post outcome uncertain; preserve and yield without repost' }
    }
    [IO.File]::WriteAllText("$logs\issue-post-url-861.txt", $url, [Text.UTF8Encoding]::new($false))
    if ($url -notmatch '#issuecomment-(\d+)$') { throw 'Issue URL uncertain; do not repost' }
    $id = $Matches[1]
    $raw = gh api "repos/stop-cran/learning-japanese/issues/comments/$id"
    if ($LASTEXITCODE -ne 0) { throw 'Receipt retrieval uncertain; do not repost' }
    [IO.File]::WriteAllText("$logs\issue-response-861.json", ($raw -join "`n"), [Text.UTF8Encoding]::new($false))
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
    [IO.File]::WriteAllText("$logs\issue-receipt-861.json", ($receipt | ConvertTo-Json -Depth 4),
        [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
