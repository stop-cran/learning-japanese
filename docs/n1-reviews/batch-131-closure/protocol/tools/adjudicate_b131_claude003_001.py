"""Bind the coordinator's substantive dispositions to the unchanged Claude003 report."""
import json
import re
from pathlib import Path

from b131_review_v3_common import HERE, PACKET, RECORDS, freeze_json, frozen, require, sha


def source(name):
    return frozen(PACKET.joinpath(*name.split("/"))).decode("utf-8")


def line(name, number):
    return source(name).splitlines()[number - 1]


def exclusions(name):
    match = re.search(r"^quiz_exclusions: \[(.*)\]\r?$", source(name), re.M)
    return [c.strip() for c in match[1].split(",")] if match else []


def main():
    run = "N1-B131-CLAUDE-003"
    candidate = "1359b467e0edee8822c665614d6ca57e42785c4d"
    report = HERE / "reports" / "review-claude-003" / "initial-claude-003.md"
    report_sha = "a3034b4c4c6f1b58ce97e9765b3e0f01248f7d30b82116b594ab5bc2cb666011"
    frozen(report, report_sha)
    final_path = HERE / f"{run}-final.json"
    final_raw = frozen(final_path, "11f438b764a8ae675a30c5997a61d923a37d782472e685dcb11ebd3d8da3475b")
    final = json.loads(final_raw)
    require(final["candidate"] == candidate and not final["problems"]
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION",
            "Final execution did not pass")
    execution = final["execution"]
    require(execution["coreRead"] == 66 and execution["extensionRead"] == 9
            and execution["writes"] == execution["readbacks"] == 1 and execution["fetches"] == 0
            and execution["actualResponseModels"] == ["claude-opus-5-5"]
            and execution["messages"][-1] == "NEEDS FIX", "Unexpected execution")
    bound = {key: json.loads(frozen(final[key]["path"], final[key]["sha256"]))
             for key in ("context", "structure", "evidenceCheck", "finalAudit")}
    require(bound["context"]["status"] == "PASS" and not bound["context"]["compactions"],
            "Context did not pass")
    structure = bound["structure"]
    require(structure["status"] == "PASS" and structure["overall"] == "NEEDS FIX"
            and (structure["findings"], structure["optionalPoints"], structure["limits"], structure["deRows"])
            == (2, 3, 7, 29), "Unexpected report structure")
    evidence = bound["evidenceCheck"]
    require(not evidence["issues"] and evidence["report"]["sha256"] == report_sha
            and len(evidence["formalCitations"]) == 22
            and all(c["opened"] for c in evidence["formalCitations"])
            and len(evidence["comparisons"]) == 29
            and all(c["titleMatches"] for c in evidence["comparisons"]), "Evidence bindings failed")
    require(bound["finalAudit"]["reviewerIdle"] and bound["finalAudit"]["readbackVerified"],
            "Reviewer did not finish")

    frost, guard = "snapshot/kanji/霜.md", "snapshot/kanji/衛.md"
    require(line(frost, 3) == "title: frost" and line(guard, 3) == "title: guard; defense", "Titles changed")
    require({"冷", "寒"} <= set(exclusions(frost))
            and not {"凍", "氷"} & set(exclusions(frost)), "F1 target pairs changed")
    for character, title in (("凍", "freeze; frozen"), ("氷", "ice; freeze")):
        require(line(f"repo/kanji/{character}.md", 3) == f"title: {title}"
                and "霜" not in exclusions(f"repo/kanji/{character}.md"), "F1 counterpart changed")
    require("氷の結晶" in line("evidence/external-snapshots/05-extract.txt", 17)
            and "細かい氷" in line("evidence/external-snapshots/05-extract.txt", 18)
            and "frost heaving" in line("evidence/external-snapshots/06-extract.txt", 177), "F1 sources changed")
    require("援" not in exclusions(guard) and "衛" not in exclusions("repo/kanji/援.md"), "F2 pair changed")
    require("protection" in line("evidence/kanjidic2-review-projection.xml", 2)
            and "<literal>援</literal>" in line("evidence/kanjidic2-review-projection.xml", 87)
            and "<meaning>save</meaning>" in line("evidence/kanjidic2-review-projection.xml", 87),
            "Independent F2 dictionary evidence changed")
    require("not every act of aid is defense" in line("repo/kanji/援.md", 72), "F2 qualification changed")
    require("周りをまわる" in line("evidence/external-snapshots/01-extract.txt", 13)
            and "going-around sense" in line("repo/kanji/循.md", 43)
            and "循" not in exclusions(guard) and "衛" not in exclusions("repo/kanji/循.md"),
            "C1 sources or direct pair changed")
    require("酒類一切" in line("evidence/external-snapshots/06-extract.txt", 32)
            and "明治以降の隠語" in line("evidence/external-snapshots/06-extract.txt", 33), "Slang scope changed")
    require(ord("衛") == 0x885B and ord("衞") == 0x885E, "Unicode identities")
    fonts = source("evidence/font-cmap.json")
    require(fonts.count('"U+885B": true') == 3 and fonts.count('"U+885E": false') == 3,
            "Font-cmap correction changed")

    result = {
        "run": run, "candidate": candidate, "finalSha256": sha(final_raw),
        "final": {"path": str(final_path), "sha256": sha(final_raw)},
        "report": {"path": str(report), "sha256": report_sha},
        "claimsAdjudicated": True,
        "rawVerdict": "NEEDS FIX", "verdict": "NEEDS FIX", "acceptedFindings": ["F1", "F2"],
        "verdictScope": "Bounded report acceptance with explicit qualifications and coordinator dispositions; not wholesale adoption of every sentence or publication approval.",
        "findingAdjudication": {
            "F1": {
                "decision": "Accepted, low severity, as direct ice/freezing label precautions.",
                "basis": "Daijisen explicitly defines 霜 as ice crystals and refrigerator frost as fine ice (05-extract:17-18). Actual labels are frost, ice; freeze and freeze; frozen; no endpoint declares either pair. KANJIDIC projection:28,109 independently retains frozen/refrigerate and ice/freeze. Existing 冷/寒 precautions make the narrower ice/freezing omission inconsistent.",
                "required": "Add 氷 and 凍 to 霜's direct quiz_exclusions with a short qualified Notes explanation, preserving metadata, readings and geometry; validate and rebuild the manifest.",
                "qualification": "Not synonymy: frost is deposited ice, not every freezing event. The cited English frost-heaving/permafrost discussion does not establish a new Japanese bare-霜 sense. Accept based on the ordinary ice/freezing label overlap, not that English extrapolation or a universal hypernym-exclusion rule.",
            },
            "F2": {
                "decision": "Accepted, low severity, as a direct protective-aid precaution.",
                "basis": "Actual 援 article:66-72 explicitly discusses help/save and protection/rescue, while 衛 displays guard; defense. Independent KANJIDIC projection:2,87 gives 衛 protection and 援 save; Daijisen 01-extract:12 gives 守る. Neither endpoint declares the pair.",
                "required": "Add 援 to 衛's direct quiz_exclusions and briefly distinguish protective aid/rescue from guarding; preserve prior guards and other content.",
                "qualification": "Not inferred merely from both cards excluding 守/防: those pairs are not transitive. Direct protect/save evidence supports the precaution; general assistance and all forms of aid are not defense.",
            },
        },
        "optionalPoints": {
            "O1": "Optional only. 字通 03-extract:38-39 and 05-extract:42-43 supports the offered classifications, but conservative structure-unclassified tags and explicitly modern mnemonics are valid. Do not require retagging or claim visual verification.",
            "O2": "The optional recommendation is retained but its assertion that 衛 only orbits a centre is not accepted. See coordinator C1 below.",
            "O3": "Source-supported optional qualified disclosure. 06-extract:27-33 identifies a historical jargon compilation; no ordinary alcohol sense or mandatory 酒 exclusion is established. 羊's extra historical precautions do not turn that slang into ordinary modern usage.",
        },
        "coordinatorReconciliationItems": [{
            "id": "C1", "origin": "Coordinator adjudication of O2/D16; not an additional independent reviewer finding.",
            "decision": "Resolve before signed successor acceptance; preferably add the direct 衛/循 precaution.",
            "basis": "Daijisen 01-extract:13 says 周りをまわる/取り巻く, not only astronomical orbiting. Actual 循 displays follow; cycle and describes a going-around sense (循.md:3,22,43). Neither endpoint declares the pair. The report's narrow orbit-versus-cycle distinction does not justify dismissing that broader source sense.",
            "required": "Either declare 循 on 衛 with qualified circling/circulation wording, or provide an independently sourced ordinary-sense distinction in reconciliation. Do not derive a transitive exclusion from 回/周.",
        }],
        "otherDispositions": {
            "D4": "Accept only the bounded conclusion that the supplied evidence does not establish an ordinary wrong-answer collision. 冴.md:22-24 explicitly distinguishes older intense cold from modern clarity/alertness; projection:25 retains cold and source-only readings. Do not adopt a claim that 冴 has no cold sense or justify harmlessness solely by differing titles.",
            "D5-D8": "Aging, withering, hardship and sword-related compounds or metaphors do not automatically broaden bare 霜 into all those ordinary meanings. Preserve whole-word/register restrictions.",
            "D10-D13": "Guarding/protection is not an army, organized unit, general martial activity or simply seeing someone off. Existing conservative 兵/卒 guards do not prove transitive 軍/隊/武/送 requirements.",
            "D17-D24": "Accept as bounded judgments, not universal synonym certification: species/category, animal/flock, auspicious-good/beauty or righteousness, paper-cash/wealth or treasure, and auspicious sign/tally-charm differ. The rare slang branches do not force every possible cash/asset relation.",
            "E1-E5": "All five direct pairs are declared on the new endpoints. Calendar 未, time-interval 宙, favorable 令 and soldier 兵/卒 branches remain qualified, not interchangeable with their primary displayed titles.",
            "citationErrata": "F1 霜.md:13 ->14; its white/cold Notes span61-66, not59-62. F2 衛.md:15 and 援.md:15 ->14. O2 循.md:15 ->14 and :44 ->43. E3 KANJIDIC 令 is line14, not13. These nearby source-line errors do not erase the actual cited facts; raw report remains unchanged.",
            "fontErratum": "Reject L5's parenthesis '衛 itself': U+885E is 衞, the older variant. Actual writing target 衛 is U+885B and is present in all three frozen cmaps (font-cmap.json:195-196,410-411,625-626). This coordinator-only correction does not claim that the reviewer read the cmap or establish rendered/native/device acceptance.",
            "execution": "66/66 core and9/9 extension segments; single write/readback; no fetches; exact two messages; correct model/long_context; zero compactions; 22 opened formal citations; 29 actual title matches. Peak input554904, below the585151 phase2 projection. Report hash unchanged after tooling repair.",
            "limits": "Retain L1-L7 except the corrected Unicode identification. No visual geometry, arbitrary/custom/multi-borrow pools, Kotlin/device, installed APK, whole-set or publication acceptance. No universal harmlessness guarantee for unrequested comparisons.",
        },
        "toolRecovery": {
            "derivation": str(RECORDS / "preparation003-lifecycle006-derivation-001.json"),
            "derivationSha256": "7280f1a49e75896eec78ae6d0fd9384a8f81ffe053fe93bef8f23f2fad362e7b",
            "controlsSha256": "f058b0a3ba18152ef237e65ab2015185adc8c550656257f0fe235bb10b766729",
            "explanation": "Original coordinator subprocess omitted review-tools from sys.path. Frozen successor only supplies PYTHONPATH and unique audit-bound partial-record paths. Actual unchanged structure checker passes the actual report and rejects a malformed control; failed execution and old context remain intact. No reviewer retry or prompt change.",
        },
        "publicationAccepted": False,
        "next": "Admit GPT003 serially on unchanged1359 and exact frozen kickoff. Do not share any Claude findings, selections, this adjudication or coordinator notes. Reconcile F1/F2/C1 only after both initial reviews.",
    }
    print(json.dumps(freeze_json(HERE / f"{run}-adjudication.json", result)))


if __name__ == "__main__":
    main()
