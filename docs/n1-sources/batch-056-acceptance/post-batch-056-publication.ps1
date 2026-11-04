$source = Get-Content -Raw -Encoding utf8 (Join-Path $PSScriptRoot 'post-batch-046-review.ps1')
$source = $source.Replace('batch-046-review-checkpoint-comment.txt', 'batch-056-publication-comment.txt')
$source = $source.Replace('batch-046-review-issue-receipt.json', 'batch-056-publication-issue-receipt.json')
Invoke-Expression $source
