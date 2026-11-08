$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$control = $PSScriptRoot
$repo = "$control\..\learning-japanese"
$logs = "$control\logs\2aeccbc9-c6fe-4ac9-80dc-3c90417aacdc"
Set-Location $repo
if ((git rev-parse HEAD) -ne 'aee3db6af366ff51a422448b73db9c54aa8ac326' -or $LASTEXITCODE -ne 0) {
    throw 'Unexpected content HEAD'
}
if ((git log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Invalid content signature' }
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 13320 -or
    $runner.sessionId -ne '2aeccbc9-c6fe-4ac9-80dc-3c90417aacdc') {
    throw 'Uncertain parent/session ownership'
}
if (-not (Get-CimInstance Win32_Process -Filter 'ProcessId=13320')) { throw 'Parent launcher absent' }
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
if ($progress.checkpoint -ne 820 -or $progress.batch -ne '106') { throw 'Checkpoint changed' }
$android = "$control\..\kanji-cards-android"
if ((git -C $android rev-parse HEAD) -ne 'bf30cdead8515739bc0e671d57a54b9a3109dd46' -or $LASTEXITCODE -ne 0) {
    throw 'Unexpected qualified Android HEAD'
}
if ((git -C $android log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Invalid Android signature' }
if ((git -C $android status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) {
    throw 'Android worktree not wholly clean'
}
python -B tools\validate.py *> "$logs\821-validate.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
python -B tools\build_manifest.py *> "$logs\821-manifest.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
python -B -m unittest discover -s tools -p 'test_*.py' *> "$logs\821-tests.txt"
if ($LASTEXITCODE -ne 0) { throw 'Python tests failed' }
python -B tools\grammar_vocabulary.py check *> "$logs\821-vocabulary.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency check failed' }
python -B tools\check_content_budget.py *> "$logs\821-budget.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
python -B "$control\draft-batch-106-821.py" audit *> "$logs\821-audit.txt"
if ($LASTEXITCODE -ne 0) { throw 'Exact draft/source/baseline/link/font audit failed' }
git --no-pager diff --check *> "$logs\821-whitespace.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\821-tests.txt" | Select-Object -Last 4
Get-Content "$logs\821-validate.txt" | Select-Object -Last 1
Get-Content "$logs\821-budget.txt"
Get-Content "$logs\821-vocabulary.txt"
