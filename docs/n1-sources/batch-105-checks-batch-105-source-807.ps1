$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$repo = 'C:\Users\stop-\n1-kanji-workspace\learning-japanese'
$control = 'C:\Users\stop-\n1-kanji-workspace\control'
$logs = "$control\logs\07145dbf-b4fc-49c3-86c1-f2eee5205283"
Set-Location $repo
$head = & git rev-parse HEAD
if ($head -ne '047c2cef6b6a48b1738f2c5957de01be481c63e1') { throw 'Unexpected content HEAD' }
if ((& git log -1 '--format=%G?') -ne 'G') { throw 'Content signature not valid' }
$runner = Get-Content "$control\runner.json" -Raw | ConvertFrom-Json
if ($runner.pid -ne 13320 -or $runner.sessionId -ne '07145dbf-b4fc-49c3-86c1-f2eee5205283') {
    throw 'Uncertain parent/session ownership'
}
if (-not (Get-CimInstance Win32_Process -Filter 'ProcessId=13320')) { throw 'Parent launcher absent' }
$progress = Get-Content "$control\progress.json" -Raw | ConvertFrom-Json
if ($progress.checkpoint -ne 806 -or $progress.batch -ne '105') { throw 'Unexpected checkpoint' }
$android = 'C:\Users\stop-\n1-kanji-workspace\kanji-cards-android'
if ((& git -C $android rev-parse HEAD) -ne 'bf30cdead8515739bc0e671d57a54b9a3109dd46') {
    throw 'Unexpected qualified Android HEAD'
}
if ((& git -C $android log -1 '--format=%G?') -ne 'G') { throw 'Android signature not valid' }
if (& git -C $android status --porcelain --untracked-files=all) { throw 'Android worktree not wholly clean' }
$changes = @(& git status --porcelain --untracked-files=all)
if ($changes | Where-Object { $_ -notmatch '^\?\? docs/n1-sources/(batch-105-|execution-807\.json)' }) {
    throw 'Unaccounted-for content changes'
}
& python -B -m unittest discover -s tools -p 'test_*n1*.py' *> "$logs\source-tests-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
& python -B tools\validate.py *> "$logs\validate-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
& python -B tools\build_manifest.py *> "$logs\manifest-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
& git --no-pager diff --exit-code -- manifest.json *> "$logs\manifest-diff-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-only operation changed manifest' }
& python -B tools\check_content_budget.py *> "$logs\budget-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
& python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency check failed' }
& python -B "$control\prepare-batch-105-807.py" audit *> "$logs\audit-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source packet audit failed' }
& git --no-pager diff --check *> "$logs\whitespace-807.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\source-tests-807.txt" | Select-Object -Last 4
Get-Content "$logs\validate-807.txt" | Select-Object -Last 1
Get-Content "$logs\budget-807.txt" | Select-Object -Last 10
Get-Content "$logs\vocabulary-807.txt"
