from recon_common import *
from run_gates import run_gate

out = HERE / "manifest-preparation-001"
assert not out.exists()
out.mkdir()
digest = run_gate("manifest", out, None)
write(out / "summary.json", {"status": "PASS", "purpose": "Prepare final manifest before the packet inventory; not a substitute for either serial ten-gate run.",
                             "manifestSha256": digest})
