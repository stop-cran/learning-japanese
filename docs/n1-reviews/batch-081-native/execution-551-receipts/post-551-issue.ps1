$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$logs = "$control\logs\239df77c-7bf3-488c-bb17-2b6fbfbb1248"
$signed = git -C $root rev-parse HEAD
$signature = git -C $root log -1 --format=%G?
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Normal signature not verified.' }
$body = @"
Batch **081 / 冶**: both bounded native cases passed locally, saved at normally signed ``$signed``; **not published**.

Both named API35 cases returned terminal status 0, with no skips. Production ContentSync imported the complete frozen signed ``95a87783`` archive once: **1,093 kanji / 5,049 words / 113 N1**, zero problems, version ``f1dd5d8b9d2ff535`` and accepted reading epoch 1. Full+Lite preserve ヤ / い.る; only ヤ is selected and や offered, with explicit empty kun selection, a saved good log and one-question Done. Complete 冶/冶金 articles plus the exact 金 bullet, two reciprocal pairs/four directions, system Back, N1 selection, meaning, seven-stroke tracing then give-up recall and offline routes passed.

All **45 original PNGs** are preserved (25 distinct byte groups inspected through five half-resolution coordinator contact sheets); three original full-resolution Compose font panels were also viewed directly. All 29 scoped Han across four production families, including 冫/氵 and 冶/治/台/始, were readable. The 116 individual + four whole-word Paint records are not 120 PNG reads or fallback-face identification. Horizontal table scroll states collectively show the labels and qualification; no single-frame all-columns claim. Offline handwriting model was unavailable: injected reference traces/shape-only comparison/give-up recall are not handwriting recognition or human-memory evidence.

Owned read-only emulator-5580 (parent18020/QEMU28948) was stopped; existing owner emulator5556 remained untouched. No rebuild, HOST-only heap override, guest/app heap change, guard change, reviewer or next batch. Prior textual closure and fresh host3+1 results are inherited, not rerun or relabeled. Evidence: ``docs/n1-sources/execution-551.json`` and ``docs/n1-reviews/batch-081-native/``.

Next: **two serial original-family independent visual confirmations**, then all combined-main integration/publication gates. Published count remains **107/1,228; 1,121 remaining**; the local 108th addition is not delivered. Physical-phone, general-release and whole-set acceptance remain outstanding; compatible curated-reading client required. Durable control helpers and approved workspace/committed inputs only; no optional historical session access or new permission denial. Overall project incomplete.
"@
[IO.File]::WriteAllText("$logs\issue-body-551.txt", $body + "`n", [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran)
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable.' }
    $identity = gh api user --jq .login
    if ($LASTEXITCODE -ne 0 -or $identity -ne 'stop-cran') { throw 'Wrong scoped identity.' }
    $url = gh issue comment 60 --repo stop-cran/learning-japanese --body-file "$logs\issue-body-551.txt"
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed.' }
    $url | Set-Content "$logs\issue-url-551.txt"
    $commentId = ($url -split 'issuecomment-')[-1].Trim()
    $response = gh api "repos/stop-cran/learning-japanese/issues/comments/$commentId"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot retrieve issue receipt.' }
    [IO.File]::WriteAllText("$logs\issue-response-551.json", ($response -join "`n") + "`n", [Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
