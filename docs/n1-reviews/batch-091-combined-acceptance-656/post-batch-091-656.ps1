$ErrorActionPreference = 'Stop'
$log = Join-Path $PSScriptRoot 'logs\bf2bf78f-2a42-401f-8d4b-e4c00a084073'
if ($env:GH_TOKEN) { throw 'Unexpected inherited owner token.' }
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran') { throw 'Owner identity mismatch.' }
    $body = [IO.File]::ReadAllText((Join-Path $log 'issue-body-656.txt'))
    @{body=$body} | ConvertTo-Json -Depth 2 |
        Set-Content (Join-Path $log 'issue-payload-656.json') -Encoding utf8NoBOM
    gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST `
        --input (Join-Path $log 'issue-payload-656.json') |
        Set-Content (Join-Path $log 'issue-posted-656.json') -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed; preserve response.' }
    $posted = Get-Content (Join-Path $log 'issue-posted-656.json') -Raw | ConvertFrom-Json
    if ($posted.user.login -ne 'stop-cran' -or $posted.body -cne $body) { throw 'Posted author/body mismatch.' }
    gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" |
        Set-Content (Join-Path $log 'issue-verified-656.json') -Encoding utf8NoBOM
    if ($LASTEXITCODE -ne 0) { throw 'Independent issue receipt fetch failed.' }
    $verified = Get-Content (Join-Path $log 'issue-verified-656.json') -Raw | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Verified author/body mismatch.' }
    $verified.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
