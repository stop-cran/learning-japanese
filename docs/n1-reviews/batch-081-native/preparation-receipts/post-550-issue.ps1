$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$logs = "$control\logs\171d8e7d-1534-400c-809f-f2e9cf730334"
$signed = git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read local signed commit.' }
$signature = git -C $root log -1 --format=%G?
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Normal signature not verified.' }
$body = @"
Batch **081 / 冶**: bounded native fixture preparation is saved locally at ``$signed`` (normal signature verified); **not published**.

The test APK compiled successfully with one Gradle worker and no HOST-only heap override. Its embedded complete signed ``95a87783`` Git archive matches all **8,369 runtime hashes**, manifest version ``f1dd5d8b9d2ff535`` and original archive budgets. Planned assertions cover production ContentSync once, full/curated Full+Lite readings (ヤ / い.る; only や offered), 29 Han across four production font families, 冫/氵 fallback, both new articles and the narrow 金 addition, two reciprocal pairs/four directions, N1 selection, meaning/reading, seven-stroke tracing/recall, system Back and offline routes.

Evidence: ``docs/n1-sources/execution-550.json`` and ``docs/n1-reviews/batch-081-native/``. Validator and regenerated manifest passed without runtime changes; temporary Android inputs were removed. Fresh host 3+1 results and original two-family textual closure are retained, not rerun or relabeled.

**No device/emulator, native case, PNG/visual confirmation or phone acceptance occurred in this checkpoint.** Next is bounded native execution after fresh device/port/PID ownership checks; later serial original-family visual confirmations and every integration/publication gate remain mandatory. Published count remains **107/1,228**, with **1,121 remaining**. Physical-phone, general-release and whole-set acceptance remain outstanding. No next batch or second runner; optional historical session helpers were not accessed.
"@
[System.IO.File]::WriteAllText("$logs\issue-body.txt", $body + "`n", [System.Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran)
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable.' }
    $identity = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Wrong scoped identity.' }
    $url = gh issue comment 60 --repo stop-cran/learning-japanese --body-file "$logs\issue-body.txt"
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed.' }
    $url | Set-Content "$logs\issue-url.txt"
    $commentId = ($url -split 'issuecomment-')[-1].Trim()
    $response = gh api "repos/stop-cran/learning-japanese/issues/comments/$commentId"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot independently retrieve issue receipt.' }
    [System.IO.File]::WriteAllText("$logs\issue-response.json", ($response -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
