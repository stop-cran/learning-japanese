$ErrorActionPreference = 'Stop'
$control = 'C:\Users\stop-\n1-kanji-workspace\control'
$bodyPath = Join-Path $control 'batch-046-review-checkpoint-comment.txt'
$receiptPath = Join-Path $control 'batch-046-review-issue-receipt.json'
if (Test-Path $receiptPath) { throw 'Existing receipt; refusing a duplicate issue comment' }
if (Test-Path Env:\GH_TOKEN) { throw 'Unexpected inherited GH_TOKEN; no auth operation attempted' }
$before = (& gh api user --jq .login)
if ($LASTEXITCODE -ne 0 -or $before -ne 'romanko-ms') { throw 'Unexpected default identity; no comment attempted' }
$ownerToken = (& gh auth token --user stop-cran)
if ($LASTEXITCODE -ne 0 -or -not $ownerToken) { throw 'Owner token unavailable' }
function Invoke-OwnerGh {
    param([string[]]$GhArguments)
    $start = [System.Diagnostics.ProcessStartInfo]::new('gh')
    $start.UseShellExecute = $false
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.Environment['GH_TOKEN'] = $ownerToken
    foreach ($argument in $GhArguments) { $start.ArgumentList.Add($argument) }
    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $start
    try {
        if (-not $process.Start()) { throw 'Owner gh child did not start' }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        $process.WaitForExit()
        $stdout = $stdoutTask.GetAwaiter().GetResult()
        $stderr = $stderrTask.GetAwaiter().GetResult()
        if ($process.ExitCode -ne 0) { throw "Owner gh child failed: $stderr" }
        return $stdout.TrimEnd()
    } finally {
        $process.Dispose()
    }
}
try {
    $owner = Invoke-OwnerGh -GhArguments @('api', 'user', '--jq', '.login')
    if ($owner -ne 'stop-cran') { throw 'Owner identity lookup mismatch; no comment attempted' }
    $url = Invoke-OwnerGh -GhArguments @('issue', 'comment', '60', '--repo', 'stop-cran/learning-japanese', '--body-file', $bodyPath)
    if ($url -notmatch '#issuecomment-(\d+)$') { throw 'Issue comment did not return receipt' }
    $id = $Matches[1]
    $raw = Invoke-OwnerGh -GhArguments @('api', "repos/stop-cran/learning-japanese/issues/comments/$id")
    $comment = $raw | ConvertFrom-Json -DateKind String
    $expected = (Get-Content -Raw -Encoding utf8 $bodyPath).TrimEnd()
    if ($comment.user.login -ne 'stop-cran' -or $comment.body.TrimEnd() -ne $expected) {
        throw 'Issue author/body readback mismatch'
    }
    $raw | Set-Content -Encoding utf8 $receiptPath
} finally {
    $ownerToken = $null
}
$after = (& gh api user --jq .login)
if ($LASTEXITCODE -ne 0 -or $after -ne 'romanko-ms') { throw 'Default GitHub identity changed' }
Write-Output $comment.html_url
