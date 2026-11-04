param([Parameter(Mandatory=$true)][ValidateSet('accepted','terminal')][string]$Phase)
$ErrorActionPreference = 'Stop'
$source = Get-Content (Join-Path $PSScriptRoot 'verify-batch-028-publication.ps1') -Raw
$source = $source.Replace('batch-028-', 'batch-056-')
$source = $source.Replace('$PSScriptRoot', "'$PSScriptRoot'")
. ([scriptblock]::Create($source)) -Phase $Phase
