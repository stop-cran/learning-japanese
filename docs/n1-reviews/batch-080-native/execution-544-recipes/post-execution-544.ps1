$ErrorActionPreference = 'Stop'
$logs = "$PSScriptRoot\logs\7c021a91-7f02-420f-a4bb-b5817a498af3"
if (Test-Path -LiteralPath "$logs\issue-post-response-544.json") { throw 'Existing issue receipt; do not repost.' }
$body = [System.IO.File]::ReadAllText("$logs\issue-body-544.txt")
@{ body = $body } | ConvertTo-Json | Set-Content -LiteralPath "$logs\issue-request-544.json" -Encoding utf8
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0) { throw 'Owner token unavailable.' }
    $login = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Unexpected GitHub identity.' }
    $result = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input "$logs\issue-request-544.json"
    if ($LASTEXITCODE -ne 0) { throw 'Issue update failed.' }
    $result | Set-Content -LiteralPath "$logs\issue-post-response-544.json" -Encoding utf8
    $receipt = $result | ConvertFrom-Json
    $fresh = gh api "repos/stop-cran/learning-japanese/issues/comments/$($receipt.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue readback failed.' }
    $fresh | Set-Content -LiteralPath "$logs\issue-response-544.json" -Encoding utf8
    $verified = $fresh | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body.Replace("`r`n", "`n").Trim() -cne $body.Replace("`r`n", "`n").Trim()) {
        throw 'Fresh owner/body mismatch.'
    }
    Write-Output $verified.html_url
} finally {
    Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
}
