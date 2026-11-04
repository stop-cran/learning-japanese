$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$prefix = 'batch-056-visual-claude-clarification'
if (Test-Path (Join-Path $PSScriptRoot "$prefix.jsonl")) { throw 'Refusing to overwrite original clarification' }
if ($env:GH_TOKEN -or $env:GITHUB_TOKEN) { throw 'Reviewer must not inherit owner tokens' }
foreach ($label in 'claude','gpt') {
    $previous = Get-Content -Raw (Join-Path $PSScriptRoot "batch-056-visual-$label-process.json") | ConvertFrom-Json
    if ($previous.exitCode -ne 0) { throw 'Original followups must have exited' }
    if (Get-Process -Id $previous.launcherPid -ErrorAction SilentlyContinue) { throw 'Previous launcher active' }
}
if ((& git -C $root rev-parse HEAD) -ne '6283ee5e6b90598cf92516ee6abf7cfa91d08e68') { throw 'Frozen snapshot changed' }
$prompt = @"
SAME056 ORIGINAL claude-opus-5.5 session 1d0d537e-254a-4bb9-908c-0737834391cb: bounded correction of YOUR visual report only, not a new initial, other-review comparison or native rerun.
Exactly ONE view call PER RESPONSE; await completion. Only three reads:
1. Read your complete report $root\docs\n1-reviews\batch-056-visual-claude.md.
2. View $root\docs\n1-reviews\batch-056-native\attempt-3-retry2\n1-056-kanji-radical.png.
3. In a separate response view $root\docs\n1-reviews\batch-056-native\attempt-3-retry2\n1-056-kanji-kun-reading.png.
Execution audit contradicts your no-deviations assertion: two image calls started 2026-11-04T22:44:22.956Z and .957Z, completed 22:44:23.347Z and .395Z. This is ONE observed internal overlap, not reviewer-process concurrency. Preserve this history; do not claim new serial rereads erase it. Original process33calls/24actualPNGs allreturned; both reviewer processes exited serially.
Other report qualifications to reconcile: exact24sourcehashes are distinct, so your visual-similarity comment is NOT byte identity. Bounded captures cannot establish everyrow/fullarticle/everycolumn visibility; left readinglabels are clipped. Withdraw that universal claim rather than invent a new screenshot or font-scale test.
Meaning option "thereupon; possessive no" corresponds to authored乃, not established之; withdraw speculative identity unless verified, no extra read needed. Actual persisted fixture evidence is BOTH curated reading Good logs and drawing Again after Next; meaning exited Back before persistence. Your "meaning; readings3; Draw1" description is unsupported and must be corrected. Drawing reference-touch/ungradedtrace/modelunavailablegeometry-only/recallmiss NOThuman correctrecall or MLKit. Fontface unidentified; ともしいfrequency/register UNVERIFIEDandnotclaimed.
Return a concise complete correction supplement with Snapshot/Scope/Verdicts(all3article facets)/Findings/Optional/Limits. Explicitly reconcile each inaccurate statement, retaining original report unchanged. No teaching edits/newsource/nativeclaims, no otherreport/shell/search/delegation. No manufactured finding; if readingsclip prevents universalcertification mark only that claim UNVERIFIED. This can close boundedvisualscope without certifying hiddencontent.
"@
$started = (Get-Date).ToString('o')
& copilot --model claude-opus-5.5 --resume 1d0d537e-254a-4bb9-908c-0737834391cb --prompt $prompt --add-dir $PSScriptRoot --available-tools view --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> (Join-Path $PSScriptRoot "$prefix.jsonl") 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = 'claude-opus-5.5'
    sessionId = '1d0d537e-254a-4bb9-908c-0737834391cb'
    snapshot = '6283ee5e6b90598cf92516ee6abf7cfa91d08e68'
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
