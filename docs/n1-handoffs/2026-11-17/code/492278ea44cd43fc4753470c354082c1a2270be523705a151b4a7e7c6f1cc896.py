import json
import b134_integrated_v2 as c
from common import start_guard
from verify_b134_packet import RUNNER
from verify_b134_sources import Git
from verify_b134_payload import runtime_entries
C = "ae1555736086fa6a7ee29c9707ba4b07e82bf979"
guard, _ = start_guard("B134 v2 original() real check")
try:
    git = Git(c.REPO, RUNNER, guard)
    ledger, counts = c.original(git, C)
    c.identity(git, c.INCOMING, [c.BASE])
    n = len(runtime_entries(json.loads(c.blob(git, C, "manifest.json"))))
    base = git("merge-base", C, c.INCOMING).decode().strip()
finally:
    memory = guard.finish()
print(json.dumps({"status": "PASS", "reviewed": c.REVIEWED, "closure": C, "counts": counts,
                  "runtimeEntriesAtC": n, "mergeBase": base, "breach": memory["breach"]}, indent=1))
