param([Parameter(Mandatory=$true)][string]$ExpectedHead,
      [Parameter(Mandatory=$true)][ValidateSet('push','issue')][string]$Mode)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$app = Join-Path (Split-Path $PSScriptRoot) 'kanji-cards-android'
$progress = Get-Content (Join-Path $PSScriptRoot 'progress.json') -Raw | ConvertFrom-Json -Depth 100
if ($progress.checkpoint -ne 656 -or $progress.batch -ne '091' -or $progress.status -ne 'continue') { throw 'Unexpected checkpoint' }
$runner = Get-Content (Join-Path $PSScriptRoot 'runner.json') -Raw | ConvertFrom-Json
if ($runner.pid -ne 19008 -or $runner.status -ne 'running' -or $runner.sessionId -ne '12849885-f3b9-470f-b0bc-cc287a1905b5') { throw 'Launcher identity uncertain' }
$current = $PID
$owned = $false
while ($current) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$current"
    if (-not $process) { break }
    if ($process.ProcessId -eq 19008) {
        $command = $process.CommandLine
        if ($command -match '-EncodedCommand ([A-Za-z0-9+/=]+)') {
            $command = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
        }
        $owned = $command.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')
        break
    }
    $current = $process.ParentProcessId
}
if (-not $owned) { throw 'Parent ownership uncertain; yield without lock access' }
foreach ($entry in @(@($root, $ExpectedHead), @($app, '1c1b7bf42cc91d820a93169f1088dc647ac51c0d'))) {
    $head = & git -C $entry[0] rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $head -ne $entry[1]) { throw 'Exact HEAD mismatch' }
    $signature = & git -C $entry[0] log -1 '--format=%G?'
    if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Signature mismatch' }
    $dirty = & git -C $entry[0] status --porcelain=v1 --untracked-files=all
    if ($LASTEXITCODE -ne 0 -or $dirty) { throw 'Worktree not wholly clean' }
}
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
        $bodyPath = Join-Path $PSScriptRoot 'batch-091-publication-comment.txt'
        $payloadPath = Join-Path $PSScriptRoot 'batch-091-publication-issue-payload.json'
        $postedPath = Join-Path $PSScriptRoot 'batch-091-publication-issue-posted.json'
        $receiptPath = Join-Path $PSScriptRoot 'batch-091-publication-issue-receipt.json'
        if ((Test-Path $postedPath) -or (Test-Path $receiptPath)) { throw 'Issue response exists; inspect before repeating' }
        $body = [IO.File]::ReadAllText($bodyPath)
        @{body=$body} | ConvertTo-Json | Set-Content $payloadPath -Encoding utf8NoBOM
        & gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath > $postedPath
        if ($LASTEXITCODE -ne 0) { throw 'Issue post failed; inspect saved response before retry' }
        $posted = Get-Content $postedPath -Raw | ConvertFrom-Json
        & gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" > $receiptPath
        if ($LASTEXITCODE -ne 0) { throw 'Issue readback failed' }
        $receipt = Get-Content $receiptPath -Raw | ConvertFrom-Json
        if ($receipt.user.login -ne 'stop-cran' -or $receipt.body -cne $body) { throw 'Exact owner/body verification failed' }
        Write-Output $receipt.html_url
    }
} finally {
    Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
}
$identity = & gh api user --jq .login
if ($LASTEXITCODE -ne 0 -or $identity -ne $globalIdentity) { throw 'Global account not preserved' }
