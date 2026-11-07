$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$content = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$android = Join-Path (Split-Path $control -Parent) 'kanji-cards-android'
$state = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
$saved = git -C $content rev-parse HEAD
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($state.checkpoint -ne 641 -or $state.batch -ne '090' -or
    $state.stage -ne 'batch-090-dependent-visual-confirmations' -or
    $runner.pid -ne 19008 -or $runner.sessionId -ne '9abde9c2-6ba1-4aa8-970c-92bb2a057a53' -or
    (git -C $content rev-parse HEAD^) -ne '8308d49fce923789c9b2126ff71b0b581a44c849' -or
    (git -C $content log -1 '--format=%G?') -ne 'G' -or (git -C $content status --porcelain) -or
    (git -C $android rev-parse HEAD) -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d' -or
    (git -C $android log -1 '--format=%G?') -ne 'G' -or (git -C $android status --porcelain)) {
    throw 'Signed clean checkpoint precondition failed.'
}
$p = Get-CimInstance Win32_Process -Filter "ProcessId=$PID"
while ($p -and $p.ProcessId -ne 19008) {
    $p = Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)"
}
if (-not $p) { throw 'Expected live parent ancestry not established; yield.' }
$launcher = $p.CommandLine
if ($launcher -match '(?i)-EncodedCommand\s+([A-Za-z0-9+/=]+)') {
    $launcher = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
}
if (-not $launcher.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')) {
    throw 'Expected parent launcher command not established; yield.'
}
$evidence = Get-Content "$content\docs\n1-reviews\batch-090-visual-reconciliation-642.json" -Raw | ConvertFrom-Json
if (-not $evidence.serialReviewerProcessesExited -or
    -not $evidence.allAssignedResourcesReturned -or -not $evidence.allToolViewsSerial -or
    $evidence.eachReviewerImagesDecoded -ne 14 -or
    $evidence.runtimeAcceptedForPublication -or $evidence.runtimePublished) {
    throw 'Dependent visual checkpoint evidence inconsistent.'
}
$body = @"
Batch 090 (U+5200): **original two-family dependent visual confirmations complete; combined current-main acceptance and publication remain pending**. Normally signed LOCAL evidence ``$saved``; teaching unchanged from ``e044e953133548dd37fdf1dba449de2f4ee7575f``. No runtime edit or push.

Original Claude Opus 5.5 (``claude-opus-5.5``, session ``63fa1d59-4733-497f-bc2d-b6202471619d``), then original GPT-6.1 Sol (``gpt-6.1-sol``, session ``f0995652-508c-4921-a3dd-08e89e67eb46``), each completed **16 strictly serial view calls / 14 decoded PNGs**: eleven mapped sheets covering all64native captures, plus three separate Compose font panels. Each process exited0 before the next started; no tool/process overlap. Both new articles and ONLY the four changed reused passages have **CLEAN rendered comprehensibility**, with correctness/coverage inherited from preserved initial textual reviews. No actionable defect or new blind-review credit. Claude explicitly used same-session compacted notes for the first four sheets; original reports and read/provenance limits remain, not equal fresh-read depth.

All18Han remain distinguishable in four production font selections, especially U+5200 inward-starting sweep versus crossing U+529B and U+4E43/U+51F9/U+51F8. Both complete new article projections and the four changed linked passages are readable. The traditional Japanese sword noun, neutral museum/photo sentences, lexical Japan modifier plus sword, both documented whole-word pronunciations, qualified shape/subtype/tool distinctions and explicitly modern-shape mnemonic survive rendering. Complementary horizontally scrolled captures expose the reading table. Original optional additions and ordinary kana-wrapping polish remain nonblocking. Possible shared fallback-face speculation is unverified and not needed for bounded distinguishable-glyph acceptance.

Actual returned PNG payloads decoded and dimension-checked; hashes agree across models. The tool resized sheets **1500x2260 to1327x2000** and original font panels **1080x2400 to900x2000**; not source-byte-identical or unscaled views. 72individual+4wholewordPaint probes remain recycled hash evidence, **not76exported/viewedPNGs or identified fallback face**.

Pictured N1 meaning options: sword; blade versus thereupon; possessive no / concave; sunken / convex; protruding. Supplied actual N1 AND All production-builder receipts show the same four identities, all3curatedwrongcards available, zero fallback; All is receipt evidence, not separately pictured. Only those tested configurations are closed, not futurecustom/randompools or oldclients. Exactly on U+3068 U+3046 and kun U+304B U+305F U+306A receive correct feedback/2of2done. Raw on/kun lists retain source-only U+305D U+308A in order; it is not offered as a prompt or inferred from the jukujikun razor word. Full/Lite agreement and persisted Good keys are receipt evidence.

Inherited native641: both terminal cases0/no skips; full archive ``40bc5a55`` through productionContentSync **ONCE**,1113kanji/5069words/122N1/zeroProblems/acceptedVersion ``ceee0f79a6d394df``/epoch1; twostroke injectedtrace/recallgiveup, botharticles/5mappedpairs/10directions/1directJapaneseSword-katanaWordguard/SystemBack/offline. Existing katanaN3/razorN2/sharp exclusion preserved. **No fresh native/Android run in642**, realhandwriting, offlineMLKit, physicalphone or native-speaker claim. Qualified TESTONLY Android ``1c1b7bf4`` retains production ``f9b59a2``, not latestappmain. First641wrapper escaping failure before device launch remains preserved, not a permission denial or lock recovery.

Complete reports, lossless raw JSON streams, prompts, actual model/process/range/image audits and evidence-based reconciliation are committed under ``docs/n1-reviews/*642*``, indexed by ``docs/n1-sources/execution-642.json``. All **8429runtime hashes** and manifest freshness reverified; no teaching/runtime change. Dedicated worktrees clean. No historical session-helper access, parent-lock acquisition/deletion/unlock, new permission denial, second runner or091.

Checkpoint642 continues SAME090 with normal current-main integration and actual combined-tree acceptance. All original source/baseline/link/reading/twofamily/native gates, changed-teaching independent review, required fullPython/vocabulary/manifest/budget/audits/applicable nonskippedAndroid checks, normal signing/ownerfastforward, terminalgreenCI, **EVERY immutable public ZIP runtime entry hash**, original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath and ownerissue gates remain mandatory. No unreviewed push, guard/heap increase or productionapp change. Published unchanged **116/1228;1112remaining**. Physicalphone/generalrelease/whole-set acceptance remains outstanding; project incomplete.
"@
$prefix = "$control\batch-090-visual-642-issue-"
if ((Test-Path ($prefix + 'posted.json')) -or (Test-Path ($prefix + 'receipt.json'))) {
    throw 'Existing issue receipt; never repost.'
}
$body | Set-Content ($prefix + 'body.txt') -Encoding utf8NoBOM -NoNewline
@{body=$body} | ConvertTo-Json | Set-Content ($prefix + 'payload.json') -Encoding utf8NoBOM
$oldToken = $env:GH_TOKEN
try {
    $env:GH_TOKEN = gh auth token --user stop-cran
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner credential unavailable.' }
    if ((gh api user --jq .login) -ne 'stop-cran' -or $LASTEXITCODE -ne 0) { throw 'Owner identity mismatch.' }
    $postedText = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input ($prefix + 'payload.json')
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed.' }
    $postedText | Set-Content ($prefix + 'posted.json') -Encoding utf8NoBOM
    $posted = $postedText | ConvertFrom-Json
    $verifiedText = gh api "repos/stop-cran/learning-japanese/issues/comments/$($posted.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue verification failed.' }
    $verified = $verifiedText | ConvertFrom-Json
    if ($verified.user.login -ne 'stop-cran' -or $verified.body -cne $body) { throw 'Owner/body verification failed.' }
    $verifiedText | Set-Content ($prefix + 'receipt.json') -Encoding utf8NoBOM
    Write-Output $verified.html_url
} finally {
    $env:GH_TOKEN = $oldToken
}
