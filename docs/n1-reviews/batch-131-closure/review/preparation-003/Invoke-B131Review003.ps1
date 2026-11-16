[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('verify', 'admit', 'launch', 'phase1', 'final', 'accept')]
    [string] $Action,
    [ValidateSet('claude', 'gpt')]
    [string] $Family = 'claude',
    [string] $Argument
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$tools = 'C:\Users\stop-\n1-kanji-workspace\review-tools'
$records = 'C:\Users\stop-\n1-kanji-workspace\scratch-131\review'
$preflight = 'C:\Users\stop-\n1-kanji-workspace\scratch-131\review\preparation-003\prompts\preflight-compact-003.json'
$receipt = Join-Path $records ('preparation-v3-command-' + [guid]::NewGuid().ToString('N'))
if ($Action -eq 'verify') {
    $command = @((Join-Path $tools 'run_b127_tool.py'), (Join-Path $tools 'verify_b131_preparation_003.py'))
} else {
    if ([string]::IsNullOrWhiteSpace($Argument)) {
        throw 'A fresh admission request, live session ID, or frozen adjudication path is required.'
    }
    $command = @((Join-Path $tools 'run_b127_tool.py'), (Join-Path $tools 'step_b131_neutral_005.py'),
        '131', $Family, $Action, $Argument, $preflight)
}
& python -B (Join-Path $records 'guarded-test-v3.py') $receipt python -B @command
if ($LASTEXITCODE -ne 0) {
    throw "Guarded B131003 command refused or failed; inspect $receipt"
}
