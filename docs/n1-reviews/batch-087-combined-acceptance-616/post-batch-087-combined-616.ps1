$ErrorActionPreference = 'Stop'
$logs = Join-Path $PSScriptRoot 'logs\b212b472-70c6-4c56-bf3f-d60fc3a970a0'
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran') { throw 'Owner identity mismatch.' }
    $body = [IO.File]::ReadAllText((Join-Path $logs 'issue-body-616.txt'))
    @{body=$body} | ConvertTo-Json -Depth 2 |
        Set-Content (Join-Path $logs 'issue-payload-616.json') -Encoding utf8NoBOM
    gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST `
        --input (Join-Path $logs 'issue-payload-616.json') |
        Set-Content (Join-Path $logs 'issue-posted-616.json') -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed; preserve response.' }
    $posted = Get-Content (Join-Path $logs 'issue-posted-616.json') -Raw | ConvertFrom-Json
    if ($posted.user.login -ne 'stop-cran' -or $posted.body -cne $body) {
        throw 'Posted author/body mismatch.'
    }
    gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" |
        Set-Content (Join-Path $logs 'issue-verified-616.json') -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Independent issue receipt fetch failed.' }
    $verified = Get-Content (Join-Path $logs 'issue-verified-616.json') -Raw | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) {
        throw 'Verified author/body mismatch.'
    }
    $verified.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
