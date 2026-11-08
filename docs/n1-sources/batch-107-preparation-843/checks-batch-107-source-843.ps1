$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$logs = "$control\logs\705603bf-c82b-4428-89cc-12d3b66a42db"
Set-Location $repo
& "$control\preflight-843.ps1" -ReceiptName 'preflight-843-checks.json' -SourceOnly
if ($LASTEXITCODE -ne 0) { throw 'Preflight failed' }
python -B -m unittest discover -s tools -p 'test_*n1*.py' *> "$logs\source-tests-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
python -B tools\extract_n1_jmdict.py --input "$control\inputs\n1-implementation-JMdict_e.gz" --selection docs\n1-sources\batch-107-lexical-selection.json --output docs\n1-sources\batch-107-jmdict.xml --check *> "$logs\extract-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Existing extractor check failed' }
python -B tools\validate.py *> "$logs\validate-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
python -B tools\build_manifest.py *> "$logs\manifest-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
git --no-pager diff --exit-code -- manifest.json *> "$logs\manifest-diff-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-only operation changed manifest' }
python -B tools\check_content_budget.py *> "$logs\budget-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget failed' }
python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
python -B "$control\complete-batch-107-843.py" check *> "$logs\audit-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Exact source and baseline check failed' }
git --no-pager diff --check *> "$logs\whitespace-843.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\source-tests-843.txt" | Select-Object -Last 4
Get-Content "$logs\extract-843.txt"
Get-Content "$logs\validate-843.txt" | Select-Object -Last 1
Get-Content "$logs\budget-843.txt" | Select-Object -Last 10
Get-Content "$logs\vocabulary-843.txt"
Get-Content "$logs\audit-843.txt"
