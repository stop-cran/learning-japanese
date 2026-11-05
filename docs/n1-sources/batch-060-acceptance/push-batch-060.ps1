$ErrorActionPreference = 'Stop'
if (Test-Path Env:\GH_TOKEN) { throw 'Unexpected inherited GH_TOKEN' }
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$head = & git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read HEAD' }
$signature = & git -C $root log -1 '--format=%G?'
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Normal signature not verified' }
$dirty = & git -C $root status --porcelain
if ($LASTEXITCODE -ne 0 -or $dirty) { throw 'Content tree not clean' }
$before = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $before -ne 'romanko-ms') { throw 'Unexpected default identity' }
$ownerToken = & gh auth token --user stop-cran
if ($LASTEXITCODE -ne 0 -or -not $ownerToken) { throw 'Owner token unavailable' }
try {
    $env:GH_TOKEN = $ownerToken
    $ownerToken = $null
    $owner = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $owner -ne 'stop-cran') { throw 'Owner identity mismatch' }
    & git -C $root -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin HEAD:main
    if ($LASTEXITCODE -ne 0) { throw 'Normal owner push failed; preserve exact failure' }
    $remote = & git -C $root ls-remote origin refs/heads/main
    if ($LASTEXITCODE -ne 0 -or ($remote -split '\s+')[0] -ne $head) { throw 'Exact remote SHA mismatch' }
    Write-Output "OWNER_FASTFORWARD_REMOTE=$head"
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
    $ownerToken = $null
}
$after = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $after -ne 'romanko-ms') { throw 'Default identity changed' }
