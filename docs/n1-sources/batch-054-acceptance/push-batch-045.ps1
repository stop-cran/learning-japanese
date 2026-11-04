$ErrorActionPreference = 'Stop'
if ($env:GH_TOKEN) { throw 'Unexpected inherited token' }
try {
    $env:GH_TOKEN = & gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable' }
    $identity = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Wrong scoped identity' }
    & git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin HEAD:main
    if ($LASTEXITCODE -ne 0) { throw 'Owner fast-forward push failed; preserve exact failure' }
    $head = & git rev-parse HEAD
    $remote = & git ls-remote origin refs/heads/main
    if ($LASTEXITCODE -ne 0 -or ($remote -split '\s+')[0] -ne $head) { throw 'Remote main mismatch' }
} finally {
    Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
}
$global = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $global -ne 'romanko-ms') { throw 'Global identity changed' }
