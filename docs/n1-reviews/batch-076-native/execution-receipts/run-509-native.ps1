$ErrorActionPreference = 'Stop'
$prior = Join-Path $PSScriptRoot '..\learning-japanese\docs\n1-reviews\batch-075-native\execution-receipts\run-501-native.ps1'
$script = Get-Content -LiteralPath $prior -Raw
$replacements = [ordered]@{
    '075' = '076'
    'execution=501' = 'execution=509'
    'execution-500.json' = 'execution-508.json'
    '774b469a-1a55-4725-8f81-f6361070ef9e' = 'c95bf82c-3d6c-4930-b063-7711425685fe'
    '1ae9135616852380db2cf1d7cc5a369da5ab7d3e' = 'b8a999695d67981e270e7a4fea559b712b26cf9b'
}
foreach ($entry in $replacements.GetEnumerator()) {
    if (-not $script.Contains($entry.Key)) { throw "Prior recipe anchor missing: $($entry.Key)" }
    $script = $script.Replace($entry.Key, $entry.Value)
}
$expanded = Join-Path $PSScriptRoot 'run-509-native-expanded.ps1'
if (Test-Path -LiteralPath $expanded) { throw 'Refusing to overwrite expanded execution recipe.' }
Set-Content -LiteralPath $expanded -Value $script -Encoding utf8NoBOM
& $expanded
exit $LASTEXITCODE
