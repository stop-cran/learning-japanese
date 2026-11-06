$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$signed = git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read local commit.' }
$signature = git -C $root log -1 --format=%G?
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Normal signature not verified.' }
$body = @"
Batch **082 / 准**: native acceptance and coordinator screenshot inspection are saved at normally signed LOCAL commit ``$signed``. **Not published; independent two-family visual confirmation is still required.**

Both named cases returned terminal **status 0**, with **2 passed / no skips**, on freshly owned read-only API35 ``emulator-5580`` (parent PID5996/QEMU27284), stopped after checks. No preexisting device/emulator or occupied5580/5581 was found. Host GPU/Vulkan-disabled/2048MiB/two cores and original192m/576m guest heaps were retained; no HOST-only init, heap or archive-guard change.

The exact frozen full ``4f5812bc`` Git archive passed production ContentSync **once**: **1,094 kanji / 5,050 words / 114 N1**, version ``0739a82c9699f031``, zero problems, accepted reading parser epoch1. Full+Lite retain soleジュン and empty kun, with explicit curated subsets and onlyじゅん offered. N1 selection, meaning/reading feedback and1/1 completion, complete准/准教授 articles, exact教/助教授 changed passages, two mapped reciprocal pairs plus one comparison pair (six directions), System Back and offline routes passed.

All **31 scoped Han / four production families**, including **冫/氵/辶/隹**, have124 individual Paint probes plus4 whole-word rasters and three actual Compose panels. All **51 original PNGs** are preserved in28 byte groups; coordinator inspected five labeled contact sheets (43.33% thumbnails) and directly viewed all three original font panels. No actionable blank/replacement glyph or display issue was established in that scope. Horizontal reading-table states collectively show labels and example, not every column simultaneously. Exact fallback font face was not identified.

Ten reference-path injected trace strokes and give-up recall exercise the drawing flow, **not handwriting recognition, human memory or phone acceptance**; the offline handwriting model was unavailable. The original source/review/process/read-depth/citation/permission/OOM/viewport/MLKit limitations remain intact. Qualified TEST-ONLY Android ``1c1b7bf4`` preserves production ``f9b59a2``; recovered558 host checks and559 compilation are inherited honestly.

Evidence: ``docs/n1-sources/execution-560.json`` and ``docs/n1-reviews/batch-082-native/``. Validator/regenerated manifest passed; all **8,372 runtime hashes** and original archive budgets reverified with runtime bytes unchanged. Both dedicated worktrees clean. No reviewer, integration/publication,083 or second runner.

Next: serial original-family dependent visual confirmations, then all current-main integration/publication/CI/immutable-ZIP gates. Published remains **108/1,228**, **1,120 remaining**. Physical-phone, general-release and whole-set acceptance outstanding.
"@
$bodyPath = "$control\execution-560-issue-body.txt"
$responsePath = "$control\execution-560-issue-response.json"
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
    $url | Set-Content "$control\execution-560-issue-url.txt"
    $commentId = ($url -split 'issuecomment-')[-1].Trim()
    $response = gh api "repos/stop-cran/learning-japanese/issues/comments/$commentId"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot retrieve issue receipt.' }
    [System.IO.File]::WriteAllText($responsePath, ($response -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
