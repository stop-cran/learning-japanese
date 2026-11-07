import importlib.util
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("batch096", C / "review-batch-096.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.review
R, S, V = r.R, r.S, r.V


def prepare():
    r.frozen()
    parts, sources = [], []
    paths = [
        S / "batch-096-final-label-jmdict.xml",
        R / "words" / "活力.md", R / "words" / "ばりばり.md",
        R / "kanji" / "山.md", R / "kanji" / "刀.md",
    ]
    for path in paths:
        body = path.read_text(encoding="utf-8-sig")
        parts.append(f"COMPLETE SOURCE {path}; SHA256 {r.sha(path)}\n" +
                     "\n".join(f"{i}: {s}" for i, s in enumerate(body.splitlines(), 1)))
        sources.append({"path": str(path), "sha256": r.sha(path)})
    parts.append("COORDINATOR INVENTORY OBSERVATION, frozen snapshot b26bcf9b: "
                 "words\\頑丈.md does not exist. This is path membership, not a linguistic judgment "
                 "or an independently performed lookup by the reviewer.")
    assert not (R / "words" / "頑丈.md").exists()
    families = []
    for name in ["jmdict", "comparison-jmdict", "final-label-jmdict"]:
        families += [e.findtext("ent_seq") for e in ET.parse(S / f"batch-096-{name}.xml").getroot().findall("entry")]
    assert len(families) == 105 and len(set(families)) == 102
    packet = C / "batch-096-supplement-packet.txt"
    assert not packet.exists()
    packet.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    required = {"path": str(packet), "start": 1,
                "end": len(packet.read_text(encoding="utf-8").splitlines()), "sha256": r.sha(packet)}
    r.save(V / "batch-096-supplement-required-review-ranges.json", [required])
    r.save(V / "batch-096-supplement-provenance.json", {
        "snapshot": r.SNAPSHOT, "sources": sources, "completeAdditionalFamilies": 2,
        "combinedDistinctCompleteFamilies": 102, "combinedFamilyOccurrences": 105,
        "initialDistinctCompleteFamilies": 100, "initialFamilyOccurrences": 103,
        "initialPacketOmission": "Final-label JMdict packet and four existing article bodies omitted from initial common packet. Originals preserved; identical bounded original-session supplement supplied serially to both models.",
        "packetSha256": r.sha(packet),
        "limits": "Dependent original-session coverage completion, not a second fresh blind initial review or upstream retrieval.",
    })
    prompt = f"""ORIGINAL-SESSION bounded evidence-coverage completion for unchanged signed batch096 snapshot {r.SNAPSHOT}.
Your original report and observations remain yours. No other review report or author adjudication supplied.
The initial common packet included100 distinct complete families, but omitted the separately committed
final-label packet containing TWO additional families. Read exactly ONE additional resource:
{packet}
Use ONE view call, forceReadLargeFiles=true, no range, for the complete {packet.stat().st_size}-byte/{required['end']}-line
resource. Only view is exposed; no shell, edits, delegation or parallel calls. Disclose truncation/unread limits.
Both original model sessions receive identical evidence and task. No teaching diff since your initial review.

The supplement supplies complete frozen JMdict1208480活力 and1010340ばりばり, the complete unchanged
活力/ばりばり/山/刀 articles and a precise coordinator path-inventory observation. Initial plus supplement:
102 distinct complete families (105 occurrences) and12 raw character records. Do not claim independent
upstream retrieval or independent filesystem verification of the observation. Assess actual final labels,
ordinary secondary senses and the twelfth direct guard剛健/活力; assess whetherばりばり establishes another
necessary guard from actual label and use, not mere shared topic. Review linked山/刀 context as necessary,
not unrelated legacy full rewrites. Reconcile any of YOUR original hypotheses/limits affected by these bytes.
Do not silently withdraw an unresolved consequential teaching claim or manufacture a finding quota.

Return COMPLETE bounded follow-up report with Snapshot, Scope (actual model and reads), separate correctness/
scoped coverage/phone-text comprehensibility verdicts for BOTH new剛 and剛健 articles; Findings with severity,
facet, originalfile:lines, precise claim/impact, remedy, evidence and confidence, or none; Optional; Limits.
For original observations now supported/withdrawn/still unresolved, state exact disposition and evidence.
Native font/drawing/UI/phone/production pools remain pending; textual coverage is not those gates.
"""
    (C / "batch-096-supplement-prompt.txt").write_text(prompt, encoding="utf-8")
    shutil.copyfile(packet, V / packet.name)
    shutil.copyfile(C / "batch-096-supplement-prompt.txt", V / "batch-096-supplement-task.txt")
    shutil.copyfile(Path(__file__), V / Path(__file__).name)
    print("Prepared supplementary identical packet; combined102 distinct families.")


def run(label):
    r.PACKET = C / "batch-096-supplement-packet.txt"
    r.PROMPT = C / "batch-096-supplement-prompt.txt"
    initial = r.load(V / f"batch-096-initial-{label}-execution.json")
    assert r.absent(initial["launcherPid"])
    source = m.BASE.read_text(encoding="utf-8")
    start = source.index("def run(label):")
    end = source.index('\n\nif __name__ == "__main__":', start)
    code = source[start:end].replace("batch-089-initial-", "batch-096-supplement-")
    code = code.replace("batch-089-required-review-ranges.json", "batch-096-supplement-required-review-ranges.json")
    code = code.replace("session = str(uuid.uuid4())", "session = " + repr(initial["sessionId"]))
    code = code.replace('"--session-id", session', '"--resume", session')
    exec(compile(code, str(m.BASE), "exec"), r.__dict__)
    r.run(label)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare()
    else:
        run(sys.argv[2])
