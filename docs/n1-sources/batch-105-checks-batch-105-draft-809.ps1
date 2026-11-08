$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$repo = 'C:\Users\stop-\n1-kanji-workspace\learning-japanese'
$control = 'C:\Users\stop-\n1-kanji-workspace\control'
$logs = "$control\logs\1a8efc89-5c08-4ef4-8a51-6813b11bd676"
Set-Location $repo
if ((& git rev-parse HEAD) -ne 'ddd01d5fea912de7a3d43cd25bdc631b5e0ac0ed') { throw 'Unexpected content HEAD' }
if ((& git log -1 '--format=%G?') -ne 'G') { throw 'Invalid content signature' }
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
if ($runner.pid -ne 13320 -or $runner.status -ne 'running' -or
    $runner.sessionId -ne '1a8efc89-5c08-4ef4-8a51-6813b11bd676') {
    throw 'Uncertain parent/session ownership'
}
if (-not (Get-CimInstance Win32_Process -Filter 'ProcessId=13320')) { throw 'Parent launcher absent' }
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
if ($progress.checkpoint -ne 808 -or $progress.batch -ne '105') { throw 'Unexpected checkpoint' }
$android = 'C:\Users\stop-\n1-kanji-workspace\kanji-cards-android'
if ((& git -C $android rev-parse HEAD) -ne 'bf30cdead8515739bc0e671d57a54b9a3109dd46') {
    throw 'Unexpected qualified Android HEAD'
}
if ((& git -C $android log -1 '--format=%G?') -ne 'G') { throw 'Invalid Android signature' }
if (& git -C $android status --porcelain --untracked-files=all) { throw 'Android not wholly clean' }
$changes = @(& git -c core.quotepath=false status --porcelain --untracked-files=all)
if ($changes | Where-Object { $_ -notmatch '^(\?\?| M|M |A |AM) (kanji/勁\.md|words/雄勁\.md|strokes/勁\.json|manifest\.json|docs/n1-sources/(batch-105-|execution-809\.json))' }) {
    throw 'Unaccounted-for content changes'
}
& python -B tools\validate.py *> "$logs\809-validate.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
& python -B tools\build_manifest.py *> "$logs\809-manifest.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
& python -B -m unittest discover -s tools -p 'test_validate.py' *> "$logs\809-focused-tests.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused validator tests failed' }
& python -B tools\grammar_vocabulary.py check *> "$logs\809-vocabulary.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
& python -B tools\check_content_budget.py *> "$logs\809-budget.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
& python -B "$control\draft-batch-105-809.py" audit *> "$logs\809-audit.txt"
if ($LASTEXITCODE -ne 0) { throw 'Draft audit failed' }
& git --no-pager diff --check *> "$logs\809-whitespace.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\809-focused-tests.txt" | Select-Object -Last 4
Get-Content "$logs\809-validate.txt"
Get-Content "$logs\809-manifest.txt"
Get-Content "$logs\809-budget.txt"
Get-Content "$logs\809-vocabulary.txt"
