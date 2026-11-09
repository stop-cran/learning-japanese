$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$control = $PSScriptRoot
$repo = "$control\..\rollout-recovered\learning-japanese"
$logs = "$control\logs\68ceabfa-9c21-4d59-86f5-8b82acb120cb"
Set-Location $repo
python -B -m unittest discover -s tools -p 'test_*n1*.py' *> "$logs\source-tests-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
python -B tools\extract_n1_jmdict.py --input "$control\inputs\n1-implementation-JMdict_e.gz" --selection docs\n1-sources\batch-108-lexical-selection.json --output docs\n1-sources\batch-108-jmdict.xml --check *> "$logs\extract-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Exact-current complete-family check failed' }
python -B tools\validate.py *> "$logs\validate-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validator failed' }
python -B tools\build_manifest.py *> "$logs\manifest-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest generation failed' }
git --no-pager diff --exit-code -- manifest.json *> "$logs\manifest-diff-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Source-only work changed manifest' }
python -B tools\check_content_budget.py *> "$logs\budget-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Archive budget check failed' }
python -B tools\grammar_vocabulary.py check *> "$logs\vocabulary-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
python -B "$control\prepare-batch-108-859.py" check *> "$logs\audit-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Exact frozen-source and unchanged-baseline check failed' }
git --no-pager diff --check *> "$logs\whitespace-859.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$logs\source-tests-859.txt" | Select-Object -Last 4
Get-Content "$logs\extract-859.txt"
Get-Content "$logs\validate-859.txt" | Select-Object -Last 1
Get-Content "$logs\budget-859.txt" | Select-Object -Last 10
Get-Content "$logs\vocabulary-859.txt"
Get-Content "$logs\audit-859.txt"
