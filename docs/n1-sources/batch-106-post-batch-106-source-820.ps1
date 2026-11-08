$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$repo = "$control\..\learning-japanese"
$sha = git -C $repo rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $sha -eq '95227f2ab8846a80061d6de27b1701fe19053161') { throw 'New signed source commit required' }
if ((git -C $repo log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Signature verification failed' }
if ((git -C $repo status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) { throw 'Worktree not wholly clean' }
$body = [IO.File]::ReadAllText("$control\batch-106-source-820-issue-template.txt").Replace('LOCAL_COMMIT_PLACEHOLDER', $sha)
$bodyPath = "$control\batch-106-source-820-issue-body.txt"
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($env:GH_TOKEN)) { throw 'Owner token unavailable' }
    $owner = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $owner -ne 'stop-cran') { throw 'Wrong process-scoped owner identity' }
    $url = gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath
    if ($LASTEXITCODE -ne 0 -or $url -notmatch '#issuecomment-(\d+)$') { throw 'Issue comment failed' }
    $id = $Matches[1]
    $raw = gh api "repos/stop-cran/learning-japanese/issues/comments/$id"
    if ($LASTEXITCODE -ne 0) { throw 'Posted comment could not be verified' }
    $posted = $raw | ConvertFrom-Json
    if ($posted.user.login -ne 'stop-cran' -or
        $posted.body.Replace("`r`n", "`n").TrimEnd("`n") -cne $body.Replace("`r`n", "`n").TrimEnd("`n")) {
        throw 'Posted issue author/body mismatch'
    }
    [ordered]@{
        url=$url; localCommit=$sha; bodySha256=(Get-FileHash $bodyPath).Hash.ToLowerInvariant()
        verified=$true; id=[long]$id; author=$posted.user.login
    } | ConvertTo-Json | Set-Content "$control\batch-106-source-820-issue-receipt.json" -Encoding utf8NoBOM
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
