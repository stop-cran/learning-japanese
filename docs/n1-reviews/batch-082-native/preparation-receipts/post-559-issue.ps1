$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$signed = git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read local commit.' }
$signature = git -C $root log -1 --format=%G?
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Normal signature not verified.' }
$body = @"
Batch **082 / 准**: the bounded native fixture and compiled instrumentation APK are saved locally at ``$signed`` (normal signature verified); **not published**.

The complete frozen ``4f5812bc`` Git archive matches all **8,372 runtime hashes**, manifest version ``0739a82c9699f031`` and original budgets: 8,394 entries, 30,361,958 compressed / 44,438,578 inflated / 44,170,240 retained bytes. The native test APK embeds those exact archive bytes and compiled successfully with one Gradle worker, without the HOST-only heap init or any production/guest heap/guard change. Temporary Android source/assets were removed; both dedicated worktrees are clean.

Planned assertions cover production ContentSync **once** (1,094 kanji / 5,050 words / 114 N1), Full+Lite source and curated readings (ジュン, empty kun; only じゅん offered), all 31 scoped Han across four production families including 冫/氵/辶/隹 fallback, both new articles and the narrow 教/助教授 changes, two mapped reciprocal pairs plus the title-comparison pair (six directions), N1 selection, meaning/reading, ten-stroke tracing then recall, system Back and offline routes.

Evidence: ``docs/n1-sources/execution-559.json``, ``docs/n1-sources/batch-082-native-fixture-verification.json`` and ``docs/n1-reviews/batch-082-native/``. Qualified TEST-ONLY Android ``1c1b7bf4`` preserves production ``f9b59a2``; recovered host results and original two-family textual closure are retained, not rerun or relabeled. Validator and regenerated manifest passed without runtime changes.

**No device/emulator, native case, PNG/visual confirmation or phone acceptance occurred here.** Next checkpoint is native execution after fresh ownership checks, then serial original-family dependent visual confirmations and every integration/publication gate. Published remains **108/1,228**, with **1,120 remaining**. Physical-phone, general-release and whole-set acceptance remain outstanding. Historical failures and limitations are preserved; no next batch, second runner or optional historical session helper access.
"@
$bodyPath = "$control\execution-559-issue-body.txt"
$responsePath = "$control\execution-559-issue-response.json"
foreach ($path in @($bodyPath, $responsePath)) {
    if (Test-Path -LiteralPath $path) { throw "Receipt already exists: $path" }
}
[System.IO.File]::WriteAllText($bodyPath, $body + "`n", [System.Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran)
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable.' }
    $identity = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Wrong scoped identity.' }
    $url = gh issue comment 60 --repo stop-cran/learning-japanese --body-file $bodyPath
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed.' }
    $url | Set-Content "$control\execution-559-issue-url.txt"
    $commentId = ($url -split 'issuecomment-')[-1].Trim()
    $response = gh api "repos/stop-cran/learning-japanese/issues/comments/$commentId"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot retrieve issue receipt.' }
    [System.IO.File]::WriteAllText($responsePath, ($response -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
