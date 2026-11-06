$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$signed = git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read local commit.' }
$signature = git -C $root log -1 --format=%G?
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Normal signature not verified.' }
$body = @"
Batch **082 / 准**, checkpoint **565**: corrected native execution and coordinator screenshot inspection are saved in normally signed LOCAL commit ``$signed``. **Not published; independent corrected-runtime visual confirmations remain outstanding.**

Both named corrected native cases completed with individual terminal **status0**, **2 tests / no skips**, on the approved disposable API35 read-only emulator. Production ContentSync imported the complete frozen corrected ``e108bbeb`` archive **once**: **1,094 kanji / 5,050 words / 114 N1**, contentVersion ``d82e7fefe3898a70``, zero problems, accepted reading-parser epoch1.

The actual meaning question now contains exactly **准 / 冴 / 冶 / 隼** with the exact four source titles, **no 倣 or fallback choice**. The question and correct-feedback PNGs show every label untruncated. Full+Lite curated-reading transport and the sole **じゅん** key passed. **34 scoped Han**, including 冴/冶/隼 and 冫/氵/辶/隹, passed **136 individual + 4 whole-word raster probes** across four production families. Three actual Compose panels were inspected, with no established blank/replacement glyph or misleading look-alike.

Complete 准/准教授 text across scroll states, exact 教 bullet / 助教授 successor paragraph, **six link directions**, N1 selection, meaning/reading feedback, ten-stroke injected tracing, System Back and offline route passed. The **51 original PNGs / 28 byte groups** are preserved; all28 representatives were inspected through five contact sheets, plus direct views of three original font panels and the meaning question/feedback. Source images are1080x2400; the viewer fits them to900x2000 and contact sheets are downscaled further, so this is not51 separate full-resolution reads.

Fresh port/device ownership was verified immediately before launch: only owned ``emulator-5580``, parent PID25860 / QEMU12960; both stopped after collection. No owner device or real owner progress was modified. Exact preserved app/test APK, fixture and archive hashes were checked; **8,372 runtime hashes**, manifest freshness and original archive budgets reverified unchanged. Previous uncorrected fixtures/archives/reports remain intact. Qualified TEST-ONLY Android ``1c1b7bf4`` preserves production ``f9b59a2``; no heap or guard increase, HOST rerun or redundant compile.

Evidence: ``docs/n1-sources/execution-565.json`` and ``docs/n1-reviews/batch-082-native-corrected/``. Next checkpoint: serial original-family dependent **changed-runtime visual confirmations**, then reconciliation and every remaining integration/publication gate. Coordinator inspection is not independent closure. Offline shape-only tracing and give-up recall are **not human memory, recognition, MLKit-download or phone acceptance**. The bounded default-four N1 question is covered, not arbitrary future/custom/partial pools. All historical source/reviewer/process/lookup/denial/OOM/viewport/fallback limits remain.

Published remains **108/1,228**, **1,120 remaining**. Batch082 is not delivered; physical-phone/general-release/whole-set acceptance remains outstanding. No reviewer launched here, no083, second runner or optional historical-session helper access.
"@
$bodyPath = "$control\execution-565-issue-body.txt"
$responsePath = "$control\execution-565-issue-receipt.json"
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
    $url | Set-Content "$control\execution-565-issue-url.txt"
    $commentId = ($url -split 'issuecomment-')[-1].Trim()
    $response = gh api "repos/stop-cran/learning-japanese/issues/comments/$commentId"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot retrieve issue receipt.' }
    [System.IO.File]::WriteAllText($responsePath, ($response -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
