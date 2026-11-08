$ErrorActionPreference = 'Stop'
$control = $PSScriptRoot
$root = "$control\..\learning-japanese"
$log = "$control\logs\4656604b-eebf-4190-bcb5-d2e6ae5ddd3e"
& "$control\preflight-822.ps1" -ReceiptName 'preflight-822-checks.json' -EvidenceOnly
if (-not $?) { throw 'Review check preflight failed' }
Set-Location $root
$env:PYTHONUTF8 = '1'
$env:PYTHONPATH = "$root\tools"
python -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch *> "$log\source-tests-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Focused source tests failed' }
python -B tools\validate.py *> "$log\validate-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Validation failed' }
python -B tools\build_manifest.py *> "$log\manifest-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest failed' }
git diff --exit-code HEAD -- manifest.json *> "$log\manifest-diff-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Manifest changed despite unchanged runtime' }
python -B tools\check_content_budget.py *> "$log\budget-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Budget failed' }
python -B tools\grammar_vocabulary.py check *> "$log\vocabulary-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Vocabulary consistency failed' }
python -B "$control\finish-batch-106-review-822.py" audit *> "$log\review-audit-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Review/provenance/runtime audit failed' }
git diff --check *> "$log\whitespace-822.txt"
if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed' }
Get-Content "$log\source-tests-822.txt" -Tail 4
Get-Content "$log\validate-822.txt"
Get-Content "$log\budget-822.txt"
Get-Content "$log\vocabulary-822.txt"
