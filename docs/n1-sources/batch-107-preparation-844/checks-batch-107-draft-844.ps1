$ErrorActionPreference = 'Stop'
$logs = "$PSScriptRoot\logs\70ed1fca-b2a0-4267-bff3-7b7e4362d9ea"
& "$PSScriptRoot\preflight-844.ps1" -Draft -ReceiptName 'preflight-844-checks.json'
if ($LASTEXITCODE -ne 0) { throw 'Draft checks preflight failed' }
function Invoke-Check([string]$Name, [string[]]$Arguments) {
    $path = "$logs\$Name-844.txt"
    if (Test-Path $path) { throw 'Do not overwrite a check result' }
    & python -B @Arguments *> $path
    $code = $LASTEXITCODE
    if ($code -ne 0) { Get-Content $path; throw "$Name failed ($code)" }
    Write-Output "$Name passed"
}
Invoke-Check 'python-suite' @('-m','unittest','discover','-s','tools','-p','test_*.py')
Invoke-Check 'validator' @('tools\validate.py')
Invoke-Check 'manifest' @('tools\build_manifest.py')
Invoke-Check 'vocabulary' @('tools\grammar_vocabulary.py','check')
Invoke-Check 'budget' @('tools\check_content_budget.py')
git --no-pager diff --check *> "$logs\whitespace-844.txt"
if ($LASTEXITCODE -ne 0) { Get-Content "$logs\whitespace-844.txt"; throw 'Whitespace check failed' }
Write-Output 'All draft checks completed serially; no HOST/native/reviewer/publication claimed.'
