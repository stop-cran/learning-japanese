$ErrorActionPreference = 'Stop'
$c = 'C:\Users\stop-\n1-kanji-workspace\control'
$r = 'C:\Users\stop-\n1-kanji-workspace\learning-japanese'
$head = (git -C $r rev-parse HEAD).Trim()
if ((git -C $r rev-parse 'HEAD^').Trim() -ne '2f24c5c456ea7a026762f6c6c95b2bcdcebb337b') { throw 'Unexpected checkpoint parent' }
if ((git -C $r log -1 --format='%G?').Trim() -ne 'G') { throw 'Signature not good' }
if (git -C $r status --porcelain) { throw 'Content worktree not clean' }
$a = 'C:\Users\stop-\n1-kanji-workspace\kanji-cards-android'
if ((git -C $a rev-parse HEAD).Trim() -ne '1c1b7bf42cc91d820a93169f1088dc647ac51c0d') { throw 'Android head changed' }
if (git -C $a status --porcelain) { throw 'Android worktree not clean' }
$p = Get-Content -Raw (Join-Path $c 'progress.json') | ConvertFrom-Json
if ($p.checkpoint -ne 578 -or $p.batch -ne '083' -or $p.status -ne 'continue') { throw 'Unexpected checkpoint' }
$body = @"
Batch 083 checkpoint579: original Claude Opus 5.5 and GPT-6.1 Sol reviewers completed **serial dependent visual confirmations** against signed unchanged teaching7cc896f4/evidence2f24c5c4. Each received the same complete 114,997-byte packet and 31 original-path PNGs representing all56 captures by exact-byte deduplication. All66 child processes exited0; actual model identities, complete packet returns, single-view resource turns, returned-image payloads and no overlap verified. Complete reports and per-image observations are preserved, not rewritten.

All three new articles (凌, 凌ぐ, 凌駕) are CLEAN for correctness, scoped coverage and bounded visual comprehensibility. All30 Han/four production families and two wholewords remain distinguishable; actual meaning choices/feedback, both curated reading questions/feedback/2of2Done, article bodies across scrolling and drawing states were inspected. **083-NATIVE-574-CHOICE is resolved** for the exact tested default-four N1/All builder and actual N1 UI configuration; original574 failure remains immutable. No universal synonym-disjointness, All UI/custom/random/padded/partial/larger/reverse-pool safety claim.

Limits preserved: source1080x2400 images returned900x2000; not original-resolution/fallback-face certification. Word-body headings aboveMeaning were not directly captured (full source/native heading-existence assertions, appbar and linked kana supplied); no established rendering defect, but not every heading visually confirmed. Final loading/All0 semantics dump is not settled-screen proof; its timing/cause remains unverified. Ten injected reference strokes and give-up recall are not human handwriting/MLKit/phone acceptance; unavailable offline handwriting model shown honestly. Fresh577 HOST4/no-skips/compile and578 both corrected native cases terminal0 are inherited, not rerun. No heap/guard/algorithm/level change.

Normally signed LOCAL evidence: $head. Durable records: docs/n1-sources/execution-579.json and docs/n1-reviews/batch-083-visual-reconciliation.json, with complete reports/coverage/recipes and qualifications. Validator0errors, regenerated manifest byte-unchanged/version6dfe6a1e287ce5df, all8376runtimehashes and batch baseline/link/membership audit verified. Next: latest-main normal merge and actual combined-tree acceptance, then normal owner publication/remote CI/exact immutable ZIP gates. **No publication or batch084 here.** Published remains109/1228,1119remaining; batch083 not delivered. Physical-phone/general-release/whole-set acceptance outstanding. Parent runner.lock untouched; no optional historical-session helpers or new permission denials.
"@
$bodyPath = Join-Path $c 'batch-083-visual-579-issue.txt'
if (Test-Path $bodyPath) { throw 'Never overwrite an existing issue attempt' }
[IO.File]::WriteAllText($bodyPath, $body + "`n", [Text.UTF8Encoding]::new($false))
$payloadPath = Join-Path $c 'batch-083-visual-579-issue-payload.json'
[IO.File]::WriteAllText($payloadPath, (@{ body = $body } | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
try {
    $env:GH_TOKEN = (gh auth token --user stop-cran).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $env:GH_TOKEN) { throw 'Owner token unavailable' }
    $login = (gh api user --jq .login).Trim()
    if ($LASTEXITCODE -ne 0 -or $login -ne 'stop-cran') { throw 'Owner identity mismatch' }
    $posted = gh api repos/stop-cran/learning-japanese/issues/60/comments --method POST --input $payloadPath
    if ($LASTEXITCODE -ne 0) { throw 'Issue comment failed; preserve attempt and yield' }
    [IO.File]::WriteAllText((Join-Path $c 'batch-083-visual-579-issue-posted.json'), ($posted -join "`n"), [Text.UTF8Encoding]::new($false))
    $comment = ($posted -join "`n") | ConvertFrom-Json
    $verified = gh api "repos/stop-cran/learning-japanese/issues/comments/$($comment.id)"
    if ($LASTEXITCODE -ne 0) { throw 'Issue receipt retrieval failed' }
    $receipt = ($verified -join "`n") | ConvertFrom-Json
    if ($receipt.user.login -ne 'stop-cran') { throw 'Issue author mismatch' }
    if ($receipt.body.Replace("`r`n", "`n").TrimEnd() -ne $body.Replace("`r`n", "`n").TrimEnd()) { throw 'Issue body mismatch' }
    [IO.File]::WriteAllText((Join-Path $c 'batch-083-visual-579-issue-verified.json'), ($verified -join "`n"), [Text.UTF8Encoding]::new($false))
    Write-Output $receipt.html_url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
