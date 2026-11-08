$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$control = $PSScriptRoot
$repo = "$control\..\learning-japanese"
$logs = "$control\logs\1f17514d-4832-4b04-bbfe-7aac0c6241c0"
Set-Location $repo
if ((git rev-parse HEAD) -ne '95227f2ab8846a80061d6de27b1701fe19053161' -or $LASTEXITCODE -ne 0) {
    throw 'Unexpected content HEAD'
}
if ((git log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Invalid content signature' }
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
if ($runner.status -ne 'running' -or $runner.pid -ne 13320 -or
    $runner.sessionId -ne '1f17514d-4832-4b04-bbfe-7aac0c6241c0') {
    throw 'Uncertain parent/session ownership'
}
if (-not (Get-CimInstance Win32_Process -Filter 'ProcessId=13320')) { throw 'Parent launcher absent' }
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
if ($progress.checkpoint -ne 819 -or $progress.batch -ne '106') { throw 'Checkpoint changed' }
$android = "$control\..\kanji-cards-android"
if ((git -C $android rev-parse HEAD) -ne 'bf30cdead8515739bc0e671d57a54b9a3109dd46' -or $LASTEXITCODE -ne 0) {
    throw 'Unexpected qualified Android HEAD'
}
if ((git -C $android log -1 '--format=%G?') -ne 'G' -or $LASTEXITCODE -ne 0) { throw 'Invalid Android signature' }
if ((git -C $android status --porcelain --untracked-files=all) -or $LASTEXITCODE -ne 0) {
    throw 'Android worktree not wholly clean'
}
$changes = @(git status --porcelain --untracked-files=all)
if ($LASTEXITCODE -ne 0 -or ($changes | Where-Object { $_ -notmatch '^( M|\?\?) docs/n1-sources/(batch-106-|execution-820\.json)' })) {
    throw 'Unaccounted-for content changes'
}
python -B -m unittest discover -s tools -p 'test_*n1*.py' *> "$logs\source-tests-820.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
python -B tools\validate.py *> "$logs\validate-820.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
python -B tools\build_manifest.py *> "$logs\manifest-820.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
git --no-pager diff --exit-code -- manifest.json *> "$logs\manifest-diff-820.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-only operation changed manifest' }
python -B tools\check_content_budget.py *> "$logs\budget-820.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-820.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency check failed' }
git --no-pager diff --check *> "$logs\whitespace-820.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\source-tests-820.txt" | Select-Object -Last 4
Get-Content "$logs\validate-820.txt" | Select-Object -Last 1
Get-Content "$logs\budget-820.txt" | Select-Object -Last 10
Get-Content "$logs\vocabulary-820.txt"
