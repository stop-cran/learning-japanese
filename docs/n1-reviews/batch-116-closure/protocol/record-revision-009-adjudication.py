"""Record the coordinator adjudication of one revision-009 (2b81b65b -> 34687354) same-reviewer confirmation."""
import hashlib
import importlib.util
import json
import re
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
CANDIDATE = "34687354b531a32fea9c10b745e80ac963ac1d4b"
RUNS = {
    "constitution": ("N1-B116-CONSTITUTION-CONFIRM-004", ["憲"], {}, "CONFIRMED", "constitution-confirm-003"),
    "monitoring": ("N1-B116-MONITORING-CONFIRM-004", ["監"], {}, "CONFIRMED", "monitoring-confirm-003"),
    "supervision": ("N1-B116-SUPERVISION-CONFIRM-004", ["督"], {"O1": "RESOLVED"}, "CONFIRMED",
                    "supervision-confirm-003"),
    "gpt004": ("N1-B116-GPT004-CONFIRM-005", ["憲", "監", "督"], {"F1": "RESOLVED"}, "CONFIRMED",
               "gpt004-confirm-004"),
}
ADDED = {"憲": "僚権任係士数", "監": "士員", "督": "員"}
CURATED = {"憲": "寄害寒"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def binding(path):
    assert not path.stat().st_mode & stat.S_IWRITE, path
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def save(path, data):
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(raw)
    path.chmod(stat.S_IREAD)
    assert path.read_bytes() == raw
    return binding(path)


def field(text, name):
    return re.search(rf"(?m)^{name}: \[([^\]]*)\]", text)[1].split(", ")


def main(key, audit_name, claims_path):
    run, scope, dispositions, verdict, old_packet = RUNS[key]
    number = run[-3:]
    audit_path = HERE / run / audit_name / "audit.json"
    audit = json.loads(audit_path.read_bytes())
    assert audit["final"] and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
    assert audit["reviewerIdle"] and not audit["recordIncomplete"]
    assert not audit["breaches"] and audit["fetches"] == 0 and audit["messages"] == [verdict]
    assert audit["chainRead"] == audit["chainRequired"]
    assert audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
    context = load("context_checker", WORK / "check-run-context.py").check(audit_path.parent / "events.jsonl")
    assert context["status"] == "PASS" and not context["compactions"]
    assert context["eventsSha256"] == audit["eventsSha256"]
    chain = json.loads((HERE / f"{run}-chain.json").read_bytes())
    report_path = WORK.parent / "reports-116" / f"confirm-{key}-{number}.md"
    report_path.chmod(stat.S_IREAD)
    structure = load("structure_checker", HERE / "check-confirm-structure.py").check(
        report_path.read_text(encoding="utf-8"), run, CANDIDATE, list(dispositions), chain, verdict)
    assert structure["status"] == "PASS" and structure["confirmation"] == verdict
    assert structure["dispositions"] == dispositions and structure["findings"] == 0
    packet = WORK.parent / "review-packets" / f"batch-116-34687354-{key}-confirm-{number}"
    previous = WORK.parent / "review-packets" / f"batch-116-2b81b65b-{old_packet}"
    for card in "憲監督":
        old_text = (previous / "snapshot" / "kanji" / f"{card}.md").read_text(encoding="utf-8")
        new_text = (packet / "snapshot" / "kanji" / f"{card}.md").read_text(encoding="utf-8")
        old, new = field(old_text, "quiz_exclusions"), field(new_text, "quiz_exclusions")
        assert len(new) == len(set(new)) and new[:len(old)] == old and new[len(old):] == list(ADDED[card])
        assert not set(new) & set(field(new_text, "distractors"))
        assert field(old_text, "distractors") == field(new_text, "distractors")
        if card in CURATED:
            assert field(new_text, "distractors") == list(CURATED[card])
    claims_raw = Path(claims_path).read_bytes()
    claims_file = Path(claims_path)
    claims_file.chmod(stat.S_IREAD)
    claims = json.loads(claims_raw)
    assert claims["run"] == run and claims["openClaimIds"] == [] and claims["claims"]
    evidence = {p.name: binding(p) for p in sorted((packet / "evidence").iterdir())
                if p.name.startswith("character-definition-") or p.name in
                ("kanjidic2-meanings.json", "jmdict-cited-entries.xml")}
    record = {
        "run": run, "session": audit["session"], "candidate": CANDIDATE, "scope": scope,
        "status": "ACCEPTED", "reportKind": "confirmation", "verdict": verdict,
        "coordinatorCoverageVerdict": "CLEAN", "reviewEvidenceAccepted": True,
        "confirmationAccepted": True, "publicationAccepted": False,
        "report": binding(report_path), "finalAudit": binding(audit_path),
        "context": save(HERE / f"{run}-context.json", context),
        "structure": save(HERE / f"{run}-structure.json", structure),
        "eventsSha256": audit["eventsSha256"], "sliceSha256": audit["sliceSha256"],
        "acceptedDispositions": dispositions, "openClaimIds": [], "openClaims": [],
        "claimAdjudication": binding(claims_file), "claims": claims["claims"],
        "sourceEvidence": {**evidence,
                           "candidateCards": {c: binding(packet / "snapshot" / "kanji" / f"{c}.md") for c in "憲監督"},
                           "checks": binding(WORK / "post-fix-013" / "summary.json"),
                           "candidateProof": binding(WORK / "revision-009-signed.json")},
        "acceptanceLimit": claims["acceptanceLimit"],
    }
    print(json.dumps(save(HERE / f"{run}-adjudication.json", record)))


if __name__ == "__main__":
    main(*sys.argv[1:4])
