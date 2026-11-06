param([Parameter(Mandatory=$true)][string]$ExpectedHead,
      [Parameter(Mandatory=$true)][ValidateSet('push','issue')][string]$Mode)
$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$progress = Get-Content (Join-Path $PSScriptRoot 'progress.json') -Raw | ConvertFrom-Json -Depth 100
if ($progress.checkpoint -ne 589 -or $progress.batch -ne '084') { throw 'Unexpected checkpoint' }
$head = & git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $head -ne $ExpectedHead) { throw 'Signed HEAD mismatch' }
$signature = & git -C $root log -1 '--format=%G?'
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Signature mismatch' }
$dirty = & git -C $root status --porcelain
if ($LASTEXITCODE -ne 0 -or $dirty) { throw 'Content worktree not wholly clean' }
$app = Join-Path (Split-Path $PSScriptRoot) 'kanji-cards-android'
$appHead = & git -C $app rev-parse HEAD
$appDirty = & git -C $app status --porcelain
if ($LASTEXITCODE -ne 0 -or $appDirty -or $appHead -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d') { throw 'Android state changed' }
$appSignature = & git -C $app log -1 '--format=%G?'
if ($LASTEXITCODE -ne 0 -or $appSignature -ne 'G') { throw 'Android signature mismatch' }
$runner = Get-Content (Join-Path $PSScriptRoot 'runner.json') -Raw | ConvertFrom-Json
if ($runner.pid -ne 19008 -or $runner.status -ne 'running' -or $runner.sessionId -ne 'f2ec9d32-d497-4f17-80e8-e775b928f778') { throw 'Launcher identity uncertain' }
$chain = @()
$current = $PID
for ($i = 0; $i -lt 8 -and $current; $i++) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$current"
    if (-not $process) { break }
    $chain += $process.ProcessId
    $current = $process.ParentProcessId
}
if (19008 -notin $chain) { throw 'Expected parent launcher ownership uncertain; yield without lock access' }
if ($env:GH_TOKEN) { throw 'Unexpected inherited token environment' }
try {
    $env:GH_TOKEN = & gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable' }
    $identity = & gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Owner identity mismatch' }
    if ($Mode -eq 'push') {
        & git -C $root fetch origin main
        if ($LASTEXITCODE -ne 0) { throw 'Fresh main fetch failed' }
        & git -C $root merge-base --is-ancestor origin/main HEAD
        if ($LASTEXITCODE -ne 0) { throw 'Main advanced; combined merge/revalidation required before push' }
        & git -C $root -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin HEAD:main
        if ($LASTEXITCODE -ne 0) { throw 'Normal owner push failed' }
        $remote = & git -C $root ls-remote origin refs/heads/main
        if ($LASTEXITCODE -ne 0 -or ($remote -split '\s+')[0] -ne $ExpectedHead) { throw 'Exact remote SHA mismatch' }
    } else {
        $bodyPath = Join-Path $PSScriptRoot 'batch-084-publication-comment.txt'
        $payloadPath = Join-Path $PSScriptRoot 'batch-084-publication-issue-payload.json'
        $postedPath = Join-Path $PSScriptRoot 'batch-084-publication-issue-posted.json'
        $verifiedPath = Join-Path $PSScriptRoot 'batch-084-publication-issue-receipt.json'
        if ((Test-Path $postedPath) -or (Test-Path $verifiedPath)) { throw 'Issue receipt already exists; inspect before repeating' }
        $body = [IO.File]::ReadAllText($bodyPath)
        @{body=$body} | ConvertTo-Json | Set-Content $payloadPath -Encoding utf8
        & gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath > $postedPath
        if ($LASTEXITCODE -ne 0) { throw 'Owner issue post failed; inspect saved response before any retry' }
        $posted = Get-Content $postedPath -Raw | ConvertFrom-Json
        & gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)" > $verifiedPath
        if ($LASTEXITCODE -ne 0) { throw 'Issue readback failed' }
        $verified = Get-Content $verifiedPath -Raw | ConvertFrom-Json
        if ($verified.user.login -ne 'stop-cran' -or $verified.body.Replace("`r`n","`n").TrimEnd() -ne $body.Replace("`r`n","`n").TrimEnd()) { throw 'Owner author/body verification failed' }
        Write-Output $verified.html_url
    }
} finally {
    Remove-Item Env:GH_TOKEN -ErrorAction SilentlyContinue
}
