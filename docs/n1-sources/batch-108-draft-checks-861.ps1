$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$app = "$control\..\rollout-recovered\kanji-cards-android"
$logs = "$control\logs\68a0ce7a-9dab-430c-b0ad-8a474a9c56fa"
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
$coordinator = Get-CimInstance Win32_Process -Filter 'ProcessId=29460'
$parent = Get-CimInstance Win32_Process -Filter 'ProcessId=27864'
$hash = (Get-FileHash "$control\runner.ps1").Hash.ToLowerInvariant()
if ($runner.status -ne 'running' -or $runner.sessionId -ne '68a0ce7a-9dab-430c-b0ad-8a474a9c56fa' -or
    $runner.pid -ne 27864 -or $coordinator.ParentProcessId -ne $parent.ProcessId -or
    $hash -ne '81b1f0021403fe7e5e3d6da9d7a03e5565621975e3a4f99db4e84873d5c3a45c' -or
    $progress.checkpoint -ne 860 -or $progress.batch -ne '108' -or $progress.status -ne 'continue') {
    throw 'Live launcher/coordinator/checkpoint ownership uncertain'
}
Set-Location $repo
if ((git rev-parse HEAD).Trim() -ne '64b30465652a60d891291a64ca075aa107a2d01a' -or
    (git log -1 '--format=%G?').Trim() -ne 'G') { throw 'Unexpected content signed HEAD' }
if ((git -C $app rev-parse HEAD).Trim() -ne 'bf30cdead8515739bc0e671d57a54b9a3109dd46' -or
    (git -C $app log -1 '--format=%G?').Trim() -ne 'G' -or
    (git -C $app status --porcelain --untracked-files=all)) { throw 'Android signed/clean preflight failed' }
$allowedRuntime = @('kanji/勧.md', 'strokes/勧.json', 'words/勧告.md', 'kanji/告.md', 'words/勧める.md', 'manifest.json')
$paths = @(git -c core.quotepath=false status --porcelain --untracked-files=all)
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect draft changes' }
foreach ($line in $paths) {
    $name = $line.Substring(3)
    if ($name -notin $allowedRuntime -and -not $name.StartsWith('docs/n1-sources/batch-108-')) {
        throw "Unaccounted change: $line"
    }
}
$receipt = @{
    execution=861; batch='108'; runnerPid=27864; coordinatorPid=29460
    liveRunnerIsCoordinatorParent=$true; runnerScriptSha256=$hash
    parentLockTouched=$false; androidWhollyClean=$true; contentChangesExactlyAccounted=$true
    signedContentHead='64b30465652a60d891291a64ca075aa107a2d01a'
    signedAndroidHead='bf30cdead8515739bc0e671d57a54b9a3109dd46'
    checkedAt=[DateTimeOffset]::UtcNow.ToString('o')
}
[IO.File]::WriteAllText("$logs\preflight-861.json", ($receipt | ConvertTo-Json -Depth 4),
    [Text.UTF8Encoding]::new($false))
python -B "$control\batch-108-draft-861.py" selftest *> "$logs\audit-selftests-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Reused-support audit regressions failed' }
python -B -m unittest discover -s tools -p 'test_*.py' *> "$logs\python-tests-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Python suite failed' }
python -B tools\validate.py *> "$logs\validate-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
python -B tools\build_manifest.py *> "$logs\manifest-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
python -B tools\check_content_budget.py *> "$logs\budget-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
python -B "$control\batch-108-draft-861.py" fonts *> "$logs\fonts-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Final runtime font inventory failed' }
python -B "$control\batch-108-draft-861.py" audit *> "$logs\audit-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Exact-current draft audit failed' }
git --no-pager diff --check *> "$logs\whitespace-861.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\audit-selftests-861.txt","$logs\python-tests-861.txt" | Select-Object -Last 12
Get-Content "$logs\validate-861.txt","$logs\budget-861.txt","$logs\vocabulary-861.txt","$logs\fonts-861.txt","$logs\audit-861.txt"
