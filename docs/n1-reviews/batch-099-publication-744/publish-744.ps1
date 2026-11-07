param([Parameter(Mandatory=$true)][string]$ExpectedHead,
      [Parameter(Mandatory=$true)][ValidateSet('push','issue')][string]$Mode)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$log = Join-Path $PSScriptRoot 'logs\cf779820-280a-4e99-a787-a7395b8150af'
& python -X utf8 -B (Join-Path $PSScriptRoot 'execution-744.py') context $ExpectedHead
if ($LASTEXITCODE -ne 0) { throw 'Checkpoint, live parent ownership or exact clean signed heads uncertain' }
if ($env:GH_TOKEN) { throw 'Unexpected inherited token' }
$globalIdentity = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $globalIdentity -ne 'romanko-ms') { throw 'Global identity changed' }
try {
    $env:GH_TOKEN = & gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable' }
    $identity = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Owner identity mismatch' }
    if ($Mode -eq 'push') {
        & git -C $root fetch --quiet origin main
        if ($LASTEXITCODE -ne 0) { throw 'Fresh main fetch failed' }
        & git -C $root merge-base --is-ancestor origin/main HEAD
        if ($LASTEXITCODE -ne 0) { throw 'Main advanced; merge/reconcile/revalidate before push' }
        & git -C $root -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin HEAD:main
        if ($LASTEXITCODE -ne 0) { throw 'Normal owner push failed' }
        $remote = & git -C $root ls-remote origin refs/heads/main
        if ($LASTEXITCODE -ne 0 -or ($remote -split '\s+')[0] -ne $ExpectedHead) { throw 'Exact remote SHA mismatch' }
    } else {
        $bodyPath = Join-Path $PSScriptRoot 'batch-099-publication-comment.txt'
        $payloadPath = Join-Path $log 'issue-744-payload.json'
        $postedPath = Join-Path $log 'issue-744-posted.json'
        $receiptPath = Join-Path $log 'issue-744-reread.json'
        if ((Test-Path $postedPath) -or (Test-Path $receiptPath)) { throw 'Response exists; inspect before repeating' }
        $body = [IO.File]::ReadAllText($bodyPath)
        @{body=$body} | ConvertTo-Json | Set-Content $payloadPath -Encoding utf8NoBOM
        & gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath > $postedPath
        if ($LASTEXITCODE -ne 0) { throw 'Issue post failed; inspect saved response before retry' }
        $posted = [IO.File]::ReadAllText($postedPath) | ConvertFrom-Json
        & gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" > $receiptPath
        if ($LASTEXITCODE -ne 0) { throw 'Issue readback failed' }
        $receipt = [IO.File]::ReadAllText($receiptPath) | ConvertFrom-Json
        if ($receipt.user.login -ne 'stop-cran' -or $receipt.body -cne $body) { throw 'Exact owner/body verification failed' }
        Write-Output $receipt.html_url
    }
} finally {
    Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
}
$identity = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $identity -ne $globalIdentity) { throw 'Global account not preserved' }
