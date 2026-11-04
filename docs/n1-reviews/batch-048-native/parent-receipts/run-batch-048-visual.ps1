$ErrorActionPreference = 'Stop'
$root = Join-Path (Split-Path $PSScriptRoot) 'learning-japanese'
$snapshot = '66211c0f70abdc92f565bebb095e6c18344bde52'
$session = '80a82572-cc26-4d43-b490-52fbc401e296'
$prefix = 'batch-048-visual-claude'
$output = Join-Path $PSScriptRoot "$prefix.jsonl"
if (Test-Path $output) { throw 'Refusing to overwrite original visual execution' }
if ($env:GH_TOKEN) { throw 'Reviewer must not inherit owner GH_TOKEN' }
if ((& git -C $root rev-parse HEAD) -ne $snapshot) { throw 'Unexpected snapshot' }
if (& git -C $root status --porcelain -- kanji words articles strokes manifest.json) { throw 'Teaching must remain frozen' }
$started = (Get-Date).ToString('o')
$env:N1_VISUAL_STARTED = $started
@'
import json, os
from pathlib import Path
c = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
p = c / "progress.json"
d = json.loads(p.read_text(encoding="utf-8-sig"))
assert d["checkpoint"] == 251
d["activeExecution"].update(status="original-reviewer-visual-running", reviewerStartedAt=os.environ["N1_VISUAL_STARTED"])
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
'@ | python -B -
if ($LASTEXITCODE -ne 0) { throw 'Starting state update failed' }
Remove-Item Env:N1_VISUAL_STARTED
$prompt = "Read the entire bounded visual task at $PSScriptRoot\batch-048-visual-prompt.txt and execute read-only. Strictly ONE tool call per response, await completion, never parallelize even text reads. Return complete report in final answer."
& copilot --model claude-opus-5.5 --resume $session --prompt $prompt --add-dir $PSScriptRoot --available-tools view glob rg web_fetch --allow-all-tools --disable-builtin-mcps --no-ask-user --no-color --output-format json --usage-output-file (Join-Path $PSScriptRoot "$prefix-usage.json") --log-dir (Join-Path $PSScriptRoot "review-logs\$prefix") 1> $output 2> (Join-Path $PSScriptRoot "$prefix-stderr.txt")
$code = $LASTEXITCODE
@{
    requestedModel = 'claude-opus-5.5'
    sessionId = $session
    snapshot = $snapshot
    startedAt = $started
    completedAt = (Get-Date).ToString('o')
    exitCode = $code
    launcherPid = $PID
} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $PSScriptRoot "$prefix-process.json")
Write-Output "$prefix process exited with code $code"
exit $code
