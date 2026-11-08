$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$repo = 'C:\Users\stop-\n1-kanji-workspace\learning-japanese'
$control = 'C:\Users\stop-\n1-kanji-workspace\control'
$logs = "$control\logs\2fe17ac2-9fd1-4657-8231-22e9510a84b9"
Set-Location $repo
if ((& git rev-parse HEAD) -ne 'c2abec23b8feeb639b0773bd06b96022cd8ddda8') { throw 'Unexpected content HEAD' }
if ((& git log -1 '--format=%G?') -ne 'G') { throw 'Content signature not valid' }
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
if ($runner.pid -ne 13320 -or $runner.status -ne 'running' -or
    $runner.sessionId -ne '2fe17ac2-9fd1-4657-8231-22e9510a84b9') {
    throw 'Uncertain parent/session ownership'
}
if (-not (Get-CimInstance Win32_Process -Filter 'ProcessId=13320')) { throw 'Parent launcher absent' }
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
if ($progress.checkpoint -ne 807 -or $progress.batch -ne '105') { throw 'Unexpected checkpoint' }
$android = 'C:\Users\stop-\n1-kanji-workspace\kanji-cards-android'
if ((& git -C $android rev-parse HEAD) -ne 'bf30cdead8515739bc0e671d57a54b9a3109dd46') {
    throw 'Unexpected qualified Android HEAD'
}
if ((& git -C $android log -1 '--format=%G?') -ne 'G') { throw 'Android signature not valid' }
if (& git -C $android status --porcelain --untracked-files=all) { throw 'Android worktree not wholly clean' }
$changes = @(& git -c core.quotepath=false status --porcelain --untracked-files=all)
if ($changes | Where-Object { $_ -notmatch '^(\?\?| M|M |A |AM) docs/n1-sources/(batch-105-|execution-808\.json)' }) {
    throw 'Unaccounted-for content changes'
}
& python -B "$control\complete-batch-105-808.py" preparation *> "$logs\preparation-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source preparation audit failed' }
& python -B -m unittest discover -s tools -p 'test_*n1*.py' *> "$logs\source-tests-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
& python -B tools\validate.py *> "$logs\validate-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
& python -B tools\build_manifest.py *> "$logs\manifest-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
& git --no-pager diff --exit-code -- manifest.json *> "$logs\manifest-diff-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-only operation changed manifest' }
& python -B tools\check_content_budget.py *> "$logs\budget-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
& python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency check failed' }
& python -B "$control\complete-batch-105-808.py" audit *> "$logs\audit-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-completion audit failed' }
& git --no-pager diff --check *> "$logs\whitespace-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
& git --no-pager diff --cached --check *>> "$logs\whitespace-808.txt"
if ($LASTEXITCODE -ne 0) { throw 'Staged whitespace check failed' }
Get-Content "$logs\source-tests-808.txt" | Select-Object -Last 4
Get-Content "$logs\validate-808.txt" | Select-Object -Last 1
Get-Content "$logs\budget-808.txt"
Get-Content "$logs\vocabulary-808.txt"
