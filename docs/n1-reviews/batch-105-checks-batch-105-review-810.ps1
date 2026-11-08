$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = "$control\..\learning-japanese"
$log = "$control\logs\595bb5b4-8cc4-4f57-bcb1-4b31d3c6e957"
& "$control\preflight-810.ps1" -ReceiptName 'preflight-810-checks.json'
if (-not $?) { throw 'Review check preflight failed' }
Set-Location $root
$env:PYTHONUTF8 = '1'
$env:PYTHONPATH = "$root\tools"
python -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch *> "$log\source-tests-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
python -B tools\validate.py *> "$log\validate-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validation failed' }
python -B tools\build_manifest.py *> "$log\manifest-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest failed' }
git diff --exit-code HEAD -- manifest.json *> "$log\manifest-diff-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest changed despite unchanged runtime' }
python -B tools\check_content_budget.py *> "$log\budget-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Budget failed' }
python -B tools\grammar_vocabulary.py check *> "$log\vocabulary-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
python -B "$control\finish-batch-105-review-810.py" audit *> "$log\review-audit-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Review evidence/runtime preservation audit failed' }
git diff --check *> "$log\whitespace-810.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$log\source-tests-810.txt" -Tail 4
Get-Content "$log\validate-810.txt"
Get-Content "$log\budget-810.txt"
Get-Content "$log\vocabulary-810.txt"
