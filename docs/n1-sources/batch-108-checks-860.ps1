$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$app = "$control\..\rollout-recovered\kanji-cards-android"
$logs = "$control\logs\d29e3fec-c862-40dc-ad3a-454bdb39426f"
$runner = [IO.File]::ReadAllText("$control\runner.json") | ConvertFrom-Json
$progress = [IO.File]::ReadAllText("$control\progress.json") | ConvertFrom-Json
$coordinator = Get-CimInstance Win32_Process -Filter 'ProcessId=26376'
$parent = Get-CimInstance Win32_Process -Filter 'ProcessId=27864'
$scriptHash = (Get-FileHash "$control\runner.ps1").Hash.ToLowerInvariant()
if ($runner.status -ne 'running' -or $runner.sessionId -ne 'd29e3fec-c862-40dc-ad3a-454bdb39426f' -or
    $runner.pid -ne 27864 -or $coordinator.ParentProcessId -ne $parent.ProcessId -or
    $scriptHash -ne '81b1f0021403fe7e5e3d6da9d7a03e5565621975e3a4f99db4e84873d5c3a45c' -or
    $progress.checkpoint -ne 859 -or $progress.batch -ne '108' -or $progress.status -ne 'continue') {
    throw 'Live launcher/coordinator/checkpoint ownership uncertain'
}
Set-Location $repo
if ((git rev-parse HEAD).Trim() -ne '4e33eafe4bbf8b29a06b76a66ddc47a2e7cc1f81' -or
    (git log -1 '--format=%G?').Trim() -ne 'G') { throw 'Unexpected content signed HEAD' }
if ((git -C $app rev-parse HEAD).Trim() -ne 'bf30cdead8515739bc0e671d57a54b9a3109dd46' -or
    (git -C $app log -1 '--format=%G?').Trim() -ne 'G' -or
    (git -C $app status --porcelain --untracked-files=all)) { throw 'Android signed/clean preflight failed' }
$paths = @(git -c core.quotepath=false status --porcelain --untracked-files=all)
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect source changes' }
foreach ($line in $paths) {
    if (-not $line.Substring(3).StartsWith('docs/n1-sources/batch-108-')) {
        throw "Unaccounted change: $line"
    }
}
$receipt = @{
    execution=860; batch='108'; runnerPid=27864; coordinatorPid=26376
    liveRunnerIsCoordinatorParent=$true; runnerScriptSha256=$scriptHash
    parentLockTouched=$false; androidWhollyClean=$true; contentChangesSourceOnly=$true
    signedContentHead='4e33eafe4bbf8b29a06b76a66ddc47a2e7cc1f81'
    signedAndroidHead='bf30cdead8515739bc0e671d57a54b9a3109dd46'
    checkedAt=[DateTimeOffset]::UtcNow.ToString('o')
}
[IO.File]::WriteAllText("$logs\preflight-860.json", ($receipt | ConvertTo-Json -Depth 4),
    [Text.UTF8Encoding]::new($false))
python -B -m unittest discover -s tools -p 'test_*n1*.py' *> "$logs\source-tests-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
python -B tools\extract_n1_jmdict.py --input "$control\inputs\n1-implementation-JMdict_e.gz" --selection docs\n1-sources\batch-108-lexical-selection.json --output docs\n1-sources\batch-108-jmdict.xml --check *> "$logs\extract-member-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Member complete-family check failed' }
python -B tools\extract_n1_jmdict.py --input "$control\inputs\n1-implementation-JMdict_e.gz" --selection docs\n1-sources\batch-108-comparison-selection.json --output docs\n1-sources\batch-108-comparison-jmdict.xml --check *> "$logs\extract-comparison-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Comparison complete-family check failed' }
python -B tools\validate.py *> "$logs\validate-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
python -B tools\build_manifest.py *> "$logs\manifest-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
git --no-pager diff --exit-code -- manifest.json *> "$logs\manifest-diff-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-only work changed manifest' }
python -B tools\check_content_budget.py *> "$logs\budget-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
python -B "$control\prepare-batch-108-860.py" check *> "$logs\audit-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Exact-current source completion audit failed' }
git --no-pager diff --check *> "$logs\whitespace-860.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\source-tests-860.txt" | Select-Object -Last 4
Get-Content "$logs\extract-member-860.txt","$logs\extract-comparison-860.txt"
Get-Content "$logs\validate-860.txt" | Select-Object -Last 1
Get-Content "$logs\budget-860.txt" | Select-Object -Last 10
Get-Content "$logs\vocabulary-860.txt","$logs\audit-860.txt"
