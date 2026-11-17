import json, sys
from pathlib import Path
from common import load_module
R=Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review")
rt=load_module("diag_runtime003", R/"authorization-runtime-003"/"b134_authorized_confirmation_v2.py")
legacy=rt.legacy
orig_modules=legacy.modules
def modules():
    res=orig_modules()
    auditor=res[0]
    if not getattr(auditor,"_diag",False):
        oa=auditor.audit
        def audit(*a,**k):
            out=oa(*a,**k)
            keep={k2:out.get(k2) for k2 in ("status","breaches","notes","unexpectedUserMessages","fetches","chainRead","chainRequired","writes","readbacks","readbackVerified","reportBinding","reviewerIdle")}
            keep["messagesLen"]=len(out.get("messages",[]))
            keep["messages"]=[str(m)[:300] for m in out.get("messages",[])]
            print("AUDIT", json.dumps(keep,ensure_ascii=False,indent=1))
            return out
        auditor.audit=audit; auditor._diag=True
    return res
legacy.modules=modules
try:
    legacy.main(["final", str(R/"authorized-gpt-confirmation-002"/"preflight.json"), str(R/"authorized-gpt-admit-001"/"admission.json"), str(R/"authorized-gpt-final-diag-out-001")])
except Exception as e:
    print("ERR", type(e).__name__, e)

