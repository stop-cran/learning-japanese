$ErrorActionPreference = 'Stop'
$c = $PSScriptRoot
$r = Join-Path (Split-Path $c -Parent) 'learning-japanese'
$a = Join-Path (Split-Path $c -Parent) 'kanji-cards-android'
$head = (git -C $r rev-parse HEAD).Trim()
if ((git -C $r rev-parse 'HEAD^').Trim() -ne '40305851ec490c698e31277d5d67386e34272bb8' -or
    (git -C $r log -1 '--format=%G?').Trim() -ne 'G' -or (git -C $r status --porcelain)) {
    throw 'Content checkpoint is not the expected normally signed, wholly clean child.'
}
if ((git -C $a rev-parse HEAD).Trim() -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $a log -1 '--format=%G?').Trim() -ne 'G' -or (git -C $a status --porcelain)) {
    throw 'Dedicated Android state changed.'
}
$p = Get-Content "$c\progress.json" -Raw | ConvertFrom-Json
if ($p.checkpoint -ne 588 -or $p.batch -ne '084' -or
    $p.stage -ne 'batch-084-combined-main-integration-in-progress') { throw 'Checkpoint context changed.' }
$runner = Get-Content "$c\runner.json" -Raw | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 19008 -or
    $runner.sessionId -ne '60ad0d56-a96f-42e1-a1f6-8cf1b979a255') { throw 'Launcher context changed.' }
$ancestor = $PID
$owned = $false
while ($ancestor -gt 0) {
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$ancestor"
    if ($null -eq $process) { break }
    if ($ancestor -eq $runner.pid) { $owned = $true; break }
    $ancestor = $process.ParentProcessId
}
if (-not $owned) { throw 'Expected live launcher is not an ancestor; preserve/yield without lock access.' }
$body = @"
Batch084 checkpoint589: **latest-main integration and combined-tree acceptance passed locally; publication is next**. Normal signed merge40305851ec490c698e31277d5d67386e34272bb8 integrates public main106a36dd9617a0d0826a512da82ee1ed9bf9e34d without rewriting. Only generated manifest.json conflicted; regenerated from the complete actual tree. Reviewed 凜 kanji, necessary word article and pinned15-stroke geometry remain byte-identical. All29 incoming runtime additions and43 existing-word link-only changes match public main exactly; no substantive teaching conflict edits or new independent review claimed. Normally signed LOCAL evidence checkpoint: $head.

Combined version8c3fa3ee6f2b1ebc: every8408 runtime hash verified,1107kanji/5060words/116N1labels/121 named-source members. The incoming11 lower-level cards include six frozenN1 members 保案派第策結 deliberately placed earlier atN2 and five nonmembers; retain levels/identities and no duplicate cards. Those six are **not six accepted issue60 batches**. Published issue60 count remains110/1228,1118 remaining acceptance; batch084 is still unpublished.

Fresh actual-combined acceptance:372Python tests, validator0errors, vocabulary consistency, regenerated fresh manifest, exact disjoint runtime union, frozen-source input/decompression/lexical re-extraction, full metadata readings/curation, original985kanji/4942words/985strokes with recorded narrow exceptions, membership/one reciprocal pair/two directions/20direct word guards and pinned stroke regeneration passed. Local budget8430entries,44,258,241retained bytes,44,526,579inflated bytes,30,229,123compressed bytes; original18,000entries/42MiBcompressed/80MiBinflated/56MiBretained/per-file/media/safe-path guards unchanged.

Fresh Android HOST on exact signed combined tree: RealContentTest3 and RareHanTest1 executed with zero skips/errors/failures; BUILD SUCCESSFUL, all41tasks executed. The tests resolve the actual dedicated sibling checkout and import the combined full publication fixture. Exact qualified TESTONLYAndroid1c1b7bf4 atop unchanged productionf9; explicitJDK17/SDK, one worker and inherited HOSTONLY heap init, no native/app/guest heap change.

Original584 two-family blind/textual confirmations and588 dependent visual/detail reports, actual models/sessions/serial exits/hashes plus587two terminalcase0 native results/all archived artifacts reverified, NOT rerun. Native ContentSyncONCE remains premerge version74b87b47347b78c1/1096kanji5053words116N1, **not a native import of this combined version**. Incoming public lower-level payload is disjoint; N1 pool, three default curated labels, 凜 readings/articles/strokes/routes unchanged and fresh combined full-archive HOST import passed; no new native concern established. Both original ClaudeOpus5.5/GPT6.1Sol visual confirmations and source-onlykun/kun[] disposition retained. All original source/process/read-depth/downscale/fine-body-stroke/fallback-face/MLKit/phone/AllUI/custom/larger/random/padded/partial/reverse-pool limits remain; injected reference tracing/give-up is not human handwriting/MLKit/phone evidence.

Evidence: docs/n1-sources/execution-589.json and docs/n1-reviews/batch-084-combined-acceptance-589 (lossless outputs, non-skipped XML, durable control recipes). **Next bounded checkpoint: fresh-main recheck, normal signed owner fast-forward publication, exact remoteSHA/terminalgreenCI/EVERY immutable public ZIP runtime hash and unchanged budgets, durable publication/verified owner receipt before085.** No push or085 here. Physical-phone/general-release/whole-set acceptance remains outstanding; project incomplete. Live parent19008 verified in ancestry; child never opens/reacquires/deletes/unlocks runner.lock. Approved workspace/control/committed evidence only; no optional historical-session artifact or actual new permission denial.
"@
$bodyPath = "$c\batch-084-combined-589-issue.txt"
$payloadPath = "$c\batch-084-combined-589-issue-payload.json"
if (Test-Path $bodyPath) { throw 'Preserve existing issue attempt; do not repost blindly.' }
[IO.File]::WriteAllText($bodyPath, $body + "`n", [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText($payloadPath, (@{body=$body} | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable.' }
    $login = (gh api user --jq .login).Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Owner identity mismatch.' }
    $posted = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed; preserve attempt and yield.' }
    [IO.File]::WriteAllText("$c\batch-084-combined-589-issue-posted.json", ($posted -join "`n"), [Text.UTF8Encoding]::new($false))
    $comment = ($posted -join "`n") | ConvertFrom-Json
    $verified = gh api "repos/stop-cran/learning-japanese/issues/comments/$($comment.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue receipt retrieval failed.' }
    $receipt = ($verified -join "`n") | ConvertFrom-Json
    if ($receipt.user.login -ne 'stop-cran' -or
        $receipt.body.Replace("`r`n", "`n").TrimEnd() -ne $body.Replace("`r`n", "`n").TrimEnd()) {
        throw 'Issue author/body mismatch.'
    }
    [IO.File]::WriteAllText("$c\batch-084-combined-589-issue-verified.json", ($verified -join "`n"), [Text.UTF8Encoding]::new($false))
    Write-Output $receipt.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
