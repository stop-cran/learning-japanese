$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$logs = "$control\logs\705603bf-c82b-4428-89cc-12d3b66a42db"
$head = (git -C $repo rev-parse HEAD).Trim()
& "$control\preflight-843.ps1" -ReceiptName 'preflight-843-before-issue.json' -ExpectedContentHead $head
if ($LASTEXITCODE -ne 0) { throw 'Report preflight failed' }
if ((git -C $repo rev-parse 'HEAD^') -ne '25e3bac1ae63ac017e9810b5ea2a2d43e2d573c4') {
    throw 'Unexpected source-completion parent'
}
$marker = 'Batch 107 / checkpoint 843:'
$body = [IO.File]::ReadAllText("$control\batch-107-source-843-issue-template.txt").Replace('__SOURCE_COMMIT__', $head)
$bodyPath = "$control\batch-107-source-843-issue-body.txt"
if (Test-Path $bodyPath) { throw 'Issue body already exists; preserve and inspect rather than repost' }
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable' }
    $login = (gh api user --jq '.login').Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Unexpected issue identity' }
    $pagesRaw = gh api 'repos/stop-cran/learning-japanese/issues/60/comments?per_page=100' --paginate --slurp
    if ($LASTEXITCODE -ne 0) { throw 'Marker search failed; do not post' }
    $pages = ($pagesRaw -join "`n") | ConvertFrom-Json
    $found = @(foreach ($page in $pages) {
        foreach ($comment in $page) {
            if ($comment.user.login -eq 'stop-cran' -and $comment.body.Contains($marker)) {
                $comment | Select-Object id,html_url,body
            }
        }
    })
    [IO.File]::WriteAllText("$logs\issue-marker-search-843.json", (ConvertTo-Json -InputObject $found -Depth 5), [Text.UTF8Encoding]::new($false))
    if ($found.Count -gt 1) { throw 'Ambiguous existing markers; preserve and yield' }
    if ($found.Count -eq 1) {
        $url = $found[0].html_url
    } else {
        $url = (gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath).Trim()
        if ($LASTEXITCODE -ne 0) { throw 'Issue update uncertain; preserve and yield without repost' }
    }
    [IO.File]::WriteAllText("$logs\issue-post-url-843.txt", $url, [Text.UTF8Encoding]::new($false))
    if ($url -notmatch '#issuecomment-(\d+)$') { throw 'Invalid issue URL; preserve and yield' }
    $id = $Matches[1]
    $raw = gh api "repos/stop-cran/learning-japanese/issues/comments/$id"
    if ($LASTEXITCODE -ne 0) { throw 'Receipt retrieval uncertain; do not repost' }
    [IO.File]::WriteAllText("$logs\issue-response-843.json", ($raw -join "`n"), [Text.UTF8Encoding]::new($false))
    $comment = ($raw -join "`n") | ConvertFrom-Json
    if ($comment.user.login -ne 'stop-cran' -or $comment.html_url -ne $url) { throw 'Issue identity/URL failed' }
    if ($comment.body.Replace("`r`n", "`n").TrimEnd() -ne $body.Replace("`r`n", "`n").TrimEnd()) {
        throw 'Issue body verification failed'
    }
    $receipt = @{
        id=$comment.id; url=$url; author=$comment.user.login; verified=$true; localCommit=$head
        marker=$marker; existingMarkerCheckedBeforePosting=$true
        bodySha256=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData(
            [Text.Encoding]::UTF8.GetBytes($comment.body))).ToLowerInvariant()
    }
    [IO.File]::WriteAllText("$logs\issue-receipt-843.json", ($receipt | ConvertTo-Json -Depth 4), [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
