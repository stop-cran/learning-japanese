"""Preserve unused Claude003 and prepare a smaller complete decisive-record follow-up."""
import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from b129_confirmation_presentation import canonical, compact_xml
from b130_context_confirmation import ROOT, binding
from common import TOOLS, freeze_json, frozen, require, sha, start_guard, write_frozen
from prepare_b130_confirmations import additional, neutral
from prepare_b130_followup_engine import replace_once

UNUSED = "N1-B130-CLAUDE-CONFIRM-003"
RUN = "N1-B130-CLAUDE-CONFIRM-004"
OUTPUT = ROOT / "confirmation-004-claude-neutral"
PREPARATION_SHA = "f0338fad27f5a3c28171cccaa207808992e5e7d61eb32d6af8ac1185a9735b8e"
CAPACITY_SHA = "63208fcb8e8bb98983f82464f5122a22736a6259dfbdf6621263a27c2d9a3393"
SELECTED = {
    "jmdict-families.xml": ("entry", "ent_seq", ("1238610", "1408810")),
    "kanjidic2-records.xml": ("character", "literal", ("\u62cd", "\u97ff")),
}


def select_complete(raw, tag, key, requested):
    root = ET.fromstring(raw)
    identities = [node.findtext(key) for node in root.findall(tag)]
    require(len(identities) == len(set(identities)) and None not in identities,
            "Ambiguous complete-record input")
    require(len(requested) == len(set(requested)) and set(requested) <= set(identities),
            "Missing or duplicate requested record")
    result = ET.Element(root.tag, root.attrib)
    before = {}
    for node in root.findall(tag):
        identity = node.findtext(key)
        if identity in requested:
            before[identity] = sha(canonical(ET.tostring(node, encoding="utf-8")).encode())
            result.append(copy.deepcopy(node))
    data = compact_xml(ET.tostring(result, encoding="utf-8"))
    after = {node.findtext(key): sha(canonical(ET.tostring(node, encoding="utf-8")).encode())
             for node in ET.fromstring(data).findall(tag)}
    require(before == after and set(after) == set(requested), "Selected full-record infoset changed")
    return data, {"inputRecords": len(identities), "selectedRecords": len(after),
                  "omittedRecordIds": [value for value in identities if value not in requested],
                  "completeSelectedRecordCanonicalSha256": before,
                  "wholeInputDocumentPresented": False}


def require_unused_claude003():
    preparation = json.loads(frozen(ROOT / "confirmation-003-preparation.json", PREPARATION_SHA))
    require(preparation["status"] == "PREPARED_NOT_ADMITTED"
            and any(row["run"] == UNUSED for row in preparation["runs"]),
            "Missing unused preparation")
    for suffix in ("admission", "final", "acceptance", "adjudication", "launch"):
        require(not (ROOT / "confirm" / f"{UNUSED}-{suffix}.json").exists(),
                "Claude003 was admitted or has an execution outcome")
    require(not (ROOT.parent.parent / "reports-130" / f"{UNUSED}.md").exists(),
            "Claude003 report exists")
    paths = [ROOT / "confirmation-003-preparation.json",
             ROOT / "followup003-capacity-observation-001.json"]
    frozen(paths[1], CAPACITY_SHA)
    paths += [ROOT / "confirm" / f"{UNUSED}-{suffix}.json"
              for suffix in ("spec", "preflight", "config", "chain")]
    paths += [ROOT / "confirm" / f"{UNUSED}-{suffix}.txt" for suffix in ("prompt", "kickoff")]
    return {"run": UNUSED, "status": "PREPARED_NOT_EXECUTED", "files": [binding(path) for path in paths],
            "reason": "Pre-admission context-capacity risk, not actual compaction or failed review. "
                      "Same reviewer and signed snapshot; narrower complete decisive-record presentation."}


def derive_tools():
    replacements = (
        ("b130_followup_lineage.py", "b130_followup_lineage_v2.py", (
            ('spec["run"] == f"N1-B130-{family.upper()}-CONFIRM-003"',
             'spec["run"] == ("N1-B130-CLAUDE-CONFIRM-004" if family == "claude"\n'
             '                            else "N1-B130-GPT-CONFIRM-003")'),
            ('    prior_run = f"N1-B130-{family.upper()}-CONFIRM-002"',
             '    if family == "claude":\n'
             '        from prepare_b130_claude004 import require_unused_claude003\n'
             '        require(spec["preparedOnlyPriorRun"] == require_unused_claude003(),\n'
             '                "Unused Claude003 preparation was skipped or relabelled")\n'
             '    prior_run = f"N1-B130-{family.upper()}-CONFIRM-002"'),
        )),
        ("b130_followup_admission.py", "b130_followup_admission_v2.py", (
            ("from b130_followup_lineage import", "from b130_followup_lineage_v2 import"),
        )),
        ("confirm_b130_followup_v2.py", "confirm_b130_followup_v3.py", (
            ("from b130_followup_admission import", "from b130_followup_admission_v2 import"),
            ("from b130_followup_lineage import", "from b130_followup_lineage_v2 import"),
            ('bindings.append(binding(Path(__file__).with_name("b130_followup_lineage.py")))',
             'bindings.append(binding(Path(__file__).with_name("b130_followup_lineage_v2.py")))\n'
             '    if spec["family"] == "claude":\n'
             '        bindings.extend(spec["preparedOnlyPriorRun"]["files"])\n'
             '        bindings.append(binding(Path(__file__).with_name("prepare_b130_claude004.py")))'),
        )),
    )
    outputs = []
    for source_name, name, changes in replacements:
        source = TOOLS / source_name
        text = frozen(source).decode("utf-8").replace("\r\n", "\n")
        for before, after in changes:
            text = replace_once(text, before, after)
        compile(text, name, "exec")
        outputs.append({"source": binding(source),
                        "output": write_frozen(TOOLS / name, text.encode())})
    return outputs


def main():
    require(not OUTPUT.exists(), "Preserve earlier preparation")
    unused = require_unused_claude003()
    outputs = derive_tools()
    from confirm_b130_followup_v3 import build_followup

    guard, _ = start_guard("B130 bounded Claude004 preparation")
    try:
        original = ROOT / "confirmation-003-neutral"
        disclosure = json.loads(frozen(original / "presentation.json"))
        selected = {}
        for name, (tag, key, ids) in SELECTED.items():
            path = original / name
            raw = frozen(path, disclosure["files"][name]["presentedSha256"])
            data, facts = select_complete(raw, tag, key, ids)
            require(neutral(data), "Source contains reviewer attribution")
            output = OUTPUT / name
            write_frozen(output, data)
            selected[name] = {**facts, "inputPresentation": binding(path),
                              "outputPresentation": binding(output)}
            disclosure["files"][name] = {
                **disclosure["files"][name], "presentedSha256": sha(data),
                "completeInfosetOrObjectPreserved": False,
                "canonicalSha256": sha(canonical(data).encode()), "recordSelection": selected[name],
            }
        disclosure["method"] = (
            "Complete selected XML records, without sense, language, spelling, register, attribute or "
            "child-field projection. Canonical equality is verified per selected full record. "
            "This is NOT preservation of the entire99-family or31-character presentation. "
            "Both complete28-row pair tables remain unchanged; their unchanged rows are history/context.")
        disclosure["scope"] = (
            "The exact d4406172-to-1ac4053c delta changes only the direct拍/響 precaution and qualified "
            "effect/impression Notes. Both decisive complete JMdict families1238610/1408810 and the "
            "complete拍/響 character records are supplied, alongside all three scoped cards, their three "
            "support articles, complete響 counterpart, both full pair tables and actual check evidence. "
            "The other97 reconciliation families and29 character records are NOT reread in this pass. "
            "Their earlier reading is historical, not a new complete-source review claim. The other "
            "unchanged comparisons, original519 families/192 characters and external captures are also "
            "not reread. Prior limits remain. Assess only this narrow delta, not new full-card safety.")
        require(neutral(json.dumps(disclosure, ensure_ascii=False).encode()), "Disclosure is not neutral")
        freeze_json(OUTPUT / "presentation.json", disclosure)
        old_spec = ROOT / "confirm" / f"{UNUSED}-spec.json"
        spec = json.loads(frozen(old_spec))
        spec.update(run=RUN, preparedOnlyPriorRun=unused)
        replaced = set()
        for index, item in enumerate(spec["additionalSources"]):
            name = Path(item["path"]).name
            if name in (*SELECTED, "presentation.json"):
                spec["additionalSources"][index] = additional(OUTPUT / name, item["source"])
                replaced.add(name)
        require(replaced == {*SELECTED, "presentation.json"}, "Expected source selection differs")
        spec_path = ROOT / "confirm" / f"{RUN}-spec.json"
        freeze_json(spec_path, spec)
        build_followup(spec_path)
        chain = json.loads(frozen(ROOT / "confirm" / f"{RUN}-chain.json"))
        old_chain = json.loads(frozen(ROOT / "confirm" / f"{UNUSED}-chain.json"))
        old_bytes = sum(row["bytes"] for row in old_chain["segments"])
        chain_bytes = sum(row["bytes"] for row in chain["segments"])
        require(chain_bytes < old_bytes - 100000, "Narrowing did not materially reduce capacity risk")
        comparison_path = ROOT / "followup003-capacity-comparison-001" / "output.log"
        comparison = json.loads(frozen(comparison_path))
        projected = comparison["lastUsage"]["inputTokens"] + comparison["ratioOnlyNotPrediction"] * chain_bytes
        require(projected < 720000, "Observed growth comparison still too close to historical compaction")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation RAM guard breached")
    print(json.dumps(freeze_json(ROOT / "claude004-preparation.json", {
        "batch": 130, "run": RUN, "candidate": spec["candidate"], "session": spec["session"],
        "status": "PREPARED_NOT_ADMITTED", "spec": binding(spec_path),
        "preflight": binding(ROOT / "confirm" / f"{RUN}-preflight.json"),
        "unusedPreparation": unused, "oldChainBytes": old_bytes, "chainBytes": chain_bytes,
        "segments": len(chain["segments"]), "selection": selected, "tooling": outputs,
        "capacityComparison": binding(comparison_path), "linearObservationNotAcceptance": projected,
        "limits": "Byte/usage comparison is not a token forecast or universal threshold. Actual context "
                  "and complete bounded-access audits remain mandatory. No confirmation launched or accepted.",
        "memory": memory, "producer": binding(__file__),
    })))


if __name__ == "__main__":
    main()
