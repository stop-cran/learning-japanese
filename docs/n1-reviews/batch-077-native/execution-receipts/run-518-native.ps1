$ErrorActionPreference = 'Stop'
$prior = Join-Path $PSScriptRoot 'run-509-native-expanded.ps1'
$script = Get-Content -LiteralPath $prior -Raw
$replacements = [ordered]@{
    '076' = '077'
    'execution=509' = 'execution=518'
    'execution-508.json' = 'execution-517.json'
    'c95bf82c-3d6c-4930-b063-7711425685fe' = '851a0519-ca36-4275-8bf0-8653cd423e5e'
    'b8a999695d67981e270e7a4fea559b712b26cf9b' = '594710e8e902b9450001bb0de79e44c1384419d4'
}
foreach ($entry in $replacements.GetEnumerator()) {
    if (-not $script.Contains($entry.Key)) { throw "Prior recipe anchor missing: $($entry.Key)" }
    $script = $script.Replace($entry.Key, $entry.Value)
}
$expanded = Join-Path $PSScriptRoot 'run-518-native-expanded.ps1'
if (Test-Path -LiteralPath $expanded) { throw 'Refusing to overwrite expanded execution recipe.' }
Set-Content -LiteralPath $expanded -Value $script -Encoding utf8NoBOM
& $expanded
exit $LASTEXITCODE
