$ErrorActionPreference = 'Stop'
$repo = "$PSScriptRoot\..\rollout-recovered\learning-japanese"
$logs = "$PSScriptRoot\logs\70ed1fca-b2a0-4267-bff3-7b7e4362d9ea"
$head = (git -C $repo rev-parse HEAD).Trim()
& "$PSScriptRoot\preflight-844.ps1" -ReceiptName 'preflight-844-before-issue.json' -ExpectedContentHead $head
if ($LASTEXITCODE -ne 0) { throw 'Report preflight failed' }
if ((git -C $repo rev-parse 'HEAD^') -ne 'dfed2c150d7fe921aacdb1d616ff527df1935f3b') {
    throw 'Unexpected draft parent'
}
$marker = 'Batch 107 / checkpoint 844:'
$body = [IO.File]::ReadAllText("$PSScriptRoot\batch-107-draft-844-issue-template.txt").Replace('__DRAFT_COMMIT__', $head)
# Qualify references outside the content repository.
$body = $body.Replace('Android #125/#132', 'stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132')
$bodyPath = "$logs\issue-body-844.txt"
if (Test-Path $bodyPath) { throw 'Existing body; preserve and inspect rather than repost' }
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable' }
    $login = (gh api user --jq '.login').Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Unexpected owner identity' }
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
    [IO.File]::WriteAllText("$logs\issue-marker-search-844.json",
        (ConvertTo-Json -InputObject $found -Depth 5), [Text.UTF8Encoding]::new($false))
    if ($found.Count -gt 1) { throw 'Ambiguous marker; preserve and yield' }
    if ($found.Count -eq 1) { $url = $found[0].html_url } else {
        $url = (gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath).Trim()
        if ($LASTEXITCODE -ne 0) { throw 'Issue update uncertain; no blind repost' }
    }
    [IO.File]::WriteAllText("$logs\issue-post-url-844.txt", $url, [Text.UTF8Encoding]::new($false))
    if ($url -notmatch '#issuecomment-(\d+)$') { throw 'Invalid report URL' }
    $id = $Matches[1]
    $raw = gh api "repos/stop-cran/learning-japanese/issues/comments/$id"
    if ($LASTEXITCODE -ne 0) { throw 'Report retrieval uncertain; no repost' }
    $comment = ($raw -join "`n") | ConvertFrom-Json
    [IO.File]::WriteAllText("$logs\issue-receipt-844.json", ($raw -join "`n"), [Text.UTF8Encoding]::new($false))
    if ($comment.user.login -ne 'stop-cran' -or $comment.html_url -ne $url -or
        $comment.body.Replace("`r`n","`n").TrimEnd() -ne $body.Replace("`r`n","`n").TrimEnd()) {
        throw 'Exact owner/URL/body verification failed'
    }
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
