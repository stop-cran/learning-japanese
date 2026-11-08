$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$logs = "$control\logs\69167545-b703-4e71-81c9-45610a3fe234"
Set-Location $repo
& "$control\preflight-842.ps1" -ReceiptName 'preflight-842-checks.json' -SourceOnly
if ($LASTEXITCODE -ne 0) { throw 'Preflight failed' }
python -B -m unittest discover -s tools -p 'test_*n1*.py' *> "$logs\source-tests-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
python -B tools\extract_n1_jmdict.py --input "$control\inputs\n1-implementation-JMdict_e.gz" --selection docs\n1-sources\batch-107-lexical-selection.json --output docs\n1-sources\batch-107-jmdict.xml --check *> "$logs\extract-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Existing extractor exact-current-packet check failed' }
python -B tools\validate.py *> "$logs\validate-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
python -B tools\build_manifest.py *> "$logs\manifest-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
git --no-pager diff --exit-code -- manifest.json *> "$logs\manifest-diff-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-only operation changed manifest' }
python -B tools\check_content_budget.py *> "$logs\budget-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
python -B "$control\prepare-batch-107-842.py" check *> "$logs\audit-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Exact source and baseline check failed' }
git --no-pager diff --check *> "$logs\whitespace-842.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\source-tests-842.txt" | Select-Object -Last 4
Get-Content "$logs\extract-842.txt"
Get-Content "$logs\validate-842.txt" | Select-Object -Last 1
Get-Content "$logs\budget-842.txt" | Select-Object -Last 10
Get-Content "$logs\vocabulary-842.txt"
Get-Content "$logs\audit-842.txt"
