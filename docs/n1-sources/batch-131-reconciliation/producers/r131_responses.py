import json
import re
from r131_common import *

HASHES = {
    "claude": ["a3034b4c4c6f1b58ce97e9765b3e0f01248f7d30b82116b594ab5bc2cb666011",
               "0a78c8bed5773f11d9006692153d2857579202413e18145c0330f79a6acd4fde",
               "1ed83db9be063f5f80e5d36df3a928e7fd9a8a3353c94b59d0c7fc99adb129e8"],
    "gpt": ["5beb3b59e197ff115f154b82f579a5a9da2155d39270887269d06234b6e5c8b1",
            "8cd4e7bc2ea984ea52e310a32df724537e13a965eb33c4a9aa7ca1468f39f752",
            "40e0a72e7feedd8918fea6ca90b56d3d4652688d7dfc5cfe4888e6d613244537"],
}

guard = start_guard()
try:
    table_path = PACKET / "pair-dispositions-001.json"
    table = json.loads(table_path.read_text(encoding="utf8"))
    indexed = {r["id"]: r for r in table["rows"]}
    table_sha = sha(table_path.read_bytes())
    for family, prep, run in (("claude", "003", "003"), ("gpt", "004", "004")):
        root = SCRIPTS / "review" / ("preparation-" + prep)
        name = f"N1-B131-{family.upper()}-{run}"
        paths = [root / "reports" / f"review-{family}-{run}" / f"initial-{family}-{run}.md",
                 root / (name + "-adjudication.json"), root / (name + "-acceptance.json")]
        for path, digest in zip(paths, HASHES[family]):
            assert sha(path.read_bytes()) == digest, path
        report = paths[0].read_text(encoding="utf8")
        # Preserve only this family's own literal limit statements, with corrections separate.
        original_limits = dict(re.findall(r"^- (L\d+): (.+)$", report, re.M))
        assert len(original_limits) == (7 if family == "claude" else 14)
        if family == "claude":
            findings = {"F1": ["R1", "R2"], "F2": ["R3"], "C1": ["R4"]}
            mapping = []
            optional = {
                "O1": "Not adopted: structure-unclassified tags and explicitly modern non-etymological mnemonics remain. Retagging is outside this guard-only revision.",
                "O2": "Direct 循 precaution adopted from unrestricted circling/going around. The narrow claim that 衛 only orbits a centre is not adopted.",
                "O3": "Adopted as a qualified 酒 precaution using the independently attested bare historical-jargon sense, not ordinary modern usage."}
            settled = {
                "D4": "Bounded distinction retained with full newer family evidence: pair 霜/冴 in the neutral table explicitly retains old intense cold and KD freezing keys and assesses both actual displayed-label directions.",
                "D5-D8": "No blanket broadening from aging, withering, hardship or sword compounds. The actual additional 枯 precaution is independently qualified by bare-character perishing and complete 枯れる death evidence, not 霜枯れ alone.",
                "D10-D13": "No automatic army/unit/martial/seeing-off meanings. Actual 軍/士/送 precautions protect their separately qualified military-guard/protective-escort regions; compound allocation remains limited.",
                "D17-D24": "Original bounded judgments retained, not general synonym certification or a requirement to broaden 羊.",
                "E1-E5": "Existing direct guards preserved; no transitive inference and no changed ordinary meaning."}
            errata = [
                "Historical offsets: 霜.md:13 ->14; white/cold Notes span61-66, not59-62; 衛.md:15 and 援.md:15 ->14; 循.md:15 ->14 and :44 ->43; KANJIDIC 令 line14, not13.",
                "L5 Unicode correction: U+885E is 衞, the older variant, not the target 衛 U+885B. The latter is present in all three frozen cmaps. No rendered/native/device claim follows."]
            text = """# B131 Claude003 author response 001

Parent: 1359b467e0edee8822c665614d6ca57e42785c4d.
F1 adds direct 霜/氷 and 霜/凍 guards for deposited/refrigerator ice,
not every freezing event. F2 adds 衛/援 for directly protective aid/rescue,
not all assistance. C1 and optional O2 are addressed by 衛/循 using
unrestricted circling and historical メグル, not an orbit-only distinction.
Optional O1 retagging is not adopted; O3 receives a register-qualified 酒 note.

The neutral table also justifies each actual additional safeguard individually.
Military-guard, protective-escort, warding-off, elapsed-time and historical
loss/perishing regions remain qualified, not universally interchangeable
ordinary senses. Full 番2022640 independently retains watch/guard.
霜/冴 remains a bounded distinction without denying old cold/freezing evidence.
羊, full metadata except appended guards, selected practice, existing prose,
supports and strokes are unchanged. Notes are additive, not a content rewrite.

This is an author response awaiting independent confirmation, not a new
review, a changed original verdict, publication approval or delivered credit.
"""
        else:
            findings = {}
            mapping = []
            native = {"Q1": "D1/O1", "Q2": "D4", "Q3": "D5", "Q4": "D8",
                      "Q5": "D11", "Q6": "D13", "Q7": "D14", "Q8": "E10 (霜)",
                      "Q9": "D15", "Q10": "D16", "Q11": "D17", "Q12": "D18", "Q13": "D20"}
            for key, native_id in native.items():
                row = indexed[key]
                mapping.append({"id": key, "originalComparisonId": native_id, "pair": row["pair"],
                                "decision": row["decision"], "neutralTableSha256": table_sha,
                                "openAuthorHold": row["openQuizHold"],
                                "authorStatus": "resolved-awaiting-independent-confirmation"})
            optional = {"O1": "Adopted as a register-qualified direct 酒 precaution; Meiji-and-later jargon is not presented as ordinary modern usage."}
            settled = {
                "D2": "Direct 霜/氷 guard with deposited-ice qualification.",
                "D3": "Direct 霜/凍 guard; not every freezing event.",
                "D19": "Direct 衛/循 guard; unrestricted circling/going around retained.",
                "D21": "Direct 衛/援 guard for protective aid/rescue, not general help.",
                "D6/D7/D9/D10/D12": "Accepted bounded 老/経/世/月/敗 distinctions retained; no extra guard or general harmlessness claim.",
                "D22": "益 has no current card: non-actionable now. Future 益 must consider 羊's qualified 祥 good/auspicious branch; no card added and 羊 unchanged.",
                "E1-E9": "All original direct declarations retained; symmetric, not transitive.",
                "E10 (衛)": "Existing 衛/卒 guard preserved."}
            errata = [
                "L1 remains a reviewer limit. Mechanical community membership is covered separately by coordinator-frozen n1-published-membership-6da1184b.json and b131-membership-tool-capture, not historical KD level1 or new author linguistic acceptance.",
                "L2 exact-spelling absences in the old union remain historical. The new independently pinned 78-family extraction retains full variants/restrictions, including bare 番/士/酒/涼 and zero matches; no lexical-absence inference.",
                "L4 original unresolved statements stay historical. This author's finite dispositions now protect twelve Q pairs and retain a bounded two-direction Q2 distinction; confirmation has not occurred."]
            text = """# B131 GPT004 author response 001

Parent: 1359b467e0edee8822c665614d6ca57e42785c4d.
All Q1-Q13 IDs are retained in gpt-mapping-001.json, with their original
D/E associations and the exact neutral-table hash. Twelve receive individually
qualified direct precautions; Q2 (霜/冴) retains a cited two-direction
bounded non-collision. Its old frigid sense, cold/freezing keys and rare
冴寒 are positive evidence, not discarded. Clarity/mental alertness does
not translate 霜's cold/sharp/severe comparisons; deposited frost does not
define becoming cold/freezing or being clear/skilful.

Additional direct guards protect 霜/氷, 霜/凍, 衛/援 and 衛/循.
霜/酒 acknowledges bare historical jargon, not ordinary modern usage.
The time/loss/death, military-guard and protective-escort safeguards retain
lexical-allocation uncertainty rather than assert every pair synonymous.
For Q9 complete bare 番2022640 independently has watch/guard, not just
当番. For Q7 perish is not automatically cause death; the precaution
protects uncertainty in the positive destructive/loss branch.

All actual comparison articles, 78 complete narrowly queried JMdict families
and 19 complete character records are retained with exact receipts.
Original packets/reports remain unchanged. No author hold remains within
this finite inventory; this does not rewrite the initial UNVERIFIED verdict.
Two independent original-family confirmations are still required.
Published accounting remains 264/1228, 964 remaining; no delivery credit.
"""
        value = {"run": name, "parent": PARENT,
                 "originalBindings": [{"path": str(p), "sha256": h} for p, h in zip(paths, HASHES[family])],
                 "findings": findings, "comparisonDispositions": mapping,
                 "neutralTable": "pair-dispositions-001.json", "neutralTableSha256": table_sha,
                 "optionalPoints": optional, "otherDispositions": settled,
                 "originalLimitsRetainedVerbatim": original_limits,
                 "separateErrataAndAuthorUpdates": errata,
                 "independentConfirmation": False, "publicationAccepted": False,
                 "limits": "Bounded source and host checks only; image gaps, glyph scope, arbitrary/custom/multiple-borrow pools, Kotlin/native/device, installed APK and whole-set/publication remain outside acceptance."}
        text += "\n## Dispositions\n\n" + "\n".join(f"- {k}: {v}" for k, v in {**optional, **settled}.items())
        text += "\n\n## Separate errata and author updates\n\n" + "\n".join("- " + v for v in errata)
        text += "\n\n## Retained original limits\n\n" + "\n".join(f"- {k}: {v}" for k, v in original_limits.items()) + "\n"
        other = "gpt" if family == "claude" else "claude"
        assert other not in text.lower()
        assert other not in json.dumps(value, ensure_ascii=False).lower()
        write(PACKET / "responses" / (family + "-mapping-001.json"), value)
        write(PACKET / "responses" / (family + "-response-001.md"), text.encode())
    print("Two family-isolated responses bound; immutable originals and literal limits retained.")
finally:
    write(HERE / "responses-memory-001.json", guard.finish())
