$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = Join-Path (Split-Path $control -Parent) 'learning-japanese'
$work = Join-Path $control 'batch-082-corrected-visual-execution-566'
$signed = git -C $root rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot read local commit.' }
$signature = git -C $root log -1 --format=%G?
if ($LASTEXITCODE -ne 0 -or $signature -ne 'G') { throw 'Normal signature not verified.' }
$body = @"
Batch **082 / 准**, checkpoint **566**: corrected-runtime independent visual confirmations are saved in normally signed LOCAL commit ``$signed``. **082-V1 is resolved within the bounded default-four-choice configuration. Batch082 is NOT published.**

The original **Claude Opus 5.5** and **GPT-6.1 Sol** sessions ran serially on unchanged evidence HEAD ``86c77107`` / corrected teaching ``9ce870d1``. Each received the complete same source packet and **28 original-path image payloads covering 51 captures by exact-byte groups**; all60 host-dispatched child processes exited0, with only view available, no tool overlap or frozen teaching edit. Complete original reports, per-turn observations, actual model/session/process evidence and returned PNGs are preserved under ``docs/n1-reviews/batch-082-corrected-visual/``.

Both reviewers return **CLEAN** separately for correctness, scoped coverage and bounded visual comprehensibility of new 准 / 准教授 and the exact changed 教 bullet / 助教授 successor paragraph. Fresh corrected question and feedback pixels show all four labels untruncated, matching asserted **准 / 冴 / 冶 / 隼**, with no imitation option or fallback. Both close their own082-V1 runtime claim. All **34 scoped Han / four families**, including new 冴/冶/隼 and 冫/氵/辶/隹, plus whole 准教授, are readable across three Compose panels.

This is **dependent changed-runtime confirmation**, not replacement blind initials, fresh upstream dictionary review or reviewer-executed native testing. Source1080x2400 images were returned900x2000; both disclosed compressed history (Claude resources1-6, GPT1-14). Original observations remain intact; no equal retained-context or full-resolution claim. Claude's53PNG arithmetic concern is unsupported: the original receipt has **54 artifacts = 51 PNG + 3 non-PNG**, matching the actual51files/28groups. Both noted that filenames alone do not prove navigation; fixture/route/terminal evidence remains necessary.

Inherited without rerun: corrected563HOST3+1+5/no skips,564compile and565both corrected native cases terminal0/no skips; full production ContentSync ONCE1094kanji5050words114N1/version ``d82e7fefe3898a70``/zeroProblems/epoch1; Full+Lite soleジュン/kun[] andじゅん key, six linkdirections/SystemBack/offline and injected drawing. No heap/guard change. Validator0errors, regenerated manifest unchanged, all8372runtime hashes and batch baseline/reading/link audit passed.

Rare 准える imitation remains recognized, not disproved by rarity. Defaultfour N1 is visually checked; All-stack source/candidate reasoning is inherited, not separately captured; custom/partial/larger/future pools remain uncertified. Fine inline glyph detail, fallback-face identity and all original source/reviewer/process/lookup/denial/OOM/viewport/MLKit limits remain. Reference-injected tracing and give-up recall are NOT human memory/recognition/model-download/phone evidence. Historical uncorrected reports remain untouched.

Next bounded checkpoint: latest-main non-rewriting integration if needed, full combined-tree acceptance and every normal signed owner fast-forward/remoteSHA/terminalgreenCI/exactimmutableZIP publication gate, then checkpoint before083. **Published remains108/1,228;1,120remaining.** Physical-phone/general-release/whole-set acceptance remains outstanding. No new native/HOST run, runtime edit,083, second runner or optional historical-session helper access.
"@
$bodyPath = Join-Path $work 'issue-body.txt'
$receiptPath = Join-Path $work 'issue-receipt.json'
foreach ($path in @($bodyPath, $receiptPath)) {
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
    $url | Set-Content (Join-Path $work 'issue-url.txt')
    $commentId = ($url -split 'issuecomment-')[-1].Trim()
    $response = gh api "repos/stop-cran/learning-japanese/issues/comments/$commentId"
    if ($LASTEXITCODE -ne 0) { throw 'Cannot retrieve issue receipt.' }
    [System.IO.File]::WriteAllText($receiptPath, ($response -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
    Write-Output $url
} finally {
    Remove-Item Env:\GH_TOKEN -ErrorAction SilentlyContinue
}
