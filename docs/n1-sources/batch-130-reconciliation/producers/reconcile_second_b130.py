import collections
import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from b130_common import BASE, HERE, REPO, ROOT, git, sha, start_guard, write

PARENT = "d440617274eef6ea7611e60f147d6483f29ca710"
OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    files = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files")
    bindings = {
        files / "b130-reconciliation-002-brief.txt": "28451f0e4e91a07061b2ad1401dec215324d8dec1f17c4c3c60c0ee1384fab46",
        HERE / "review" / "reconciliation-002-author-admission.json": "2ef0fb645c95c32deef88a7df1b68e6820c702052cce771dee251a5233fd6e30",
        ROOT / "reports-130" / "N1-B130-GPT-CONFIRM-002.md": "aaad9e747c80c93868a5b3bf448e9e36f2f9cf35f123df6e71f5aca249ed58dd",
        HERE / "review" / "confirm" / "N1-B130-GPT-CONFIRM-002-adjudication.json": "a7115a06a8202f9bfafde09b4a899fc3512d70d10d676595cd8c38b9d827bfea",
        HERE / "review" / "confirm" / "N1-B130-GPT-CONFIRM-002-acceptance.json": "07ca737011314f7b7f55bcf6e5fea6be26821738c0d09d06c87326cbcc742c08",
        ROOT / "reports-130" / "N1-B130-CLAUDE-CONFIRM-002.md": "1affaf9fa5b58aea000b76cf56260624dbb8dba7c103429e32a0339c22d9ce0e",
    }
    for path, digest in bindings.items():
        assert sha(path.read_bytes()) == digest, str(path)
    write(HERE / "reconciliation-002-source-read-001" / "assignment-bindings.json",
          {str(path): digest for path, digest in bindings.items()})
    source = OUT / "jmdict-families.xml"
    records = {node.findtext("ent_seq"): node for node in ET.parse(source).getroot()}
    receipt = json.loads((OUT / "source-receipt.json").read_text(encoding="utf-8"))
    canonical = {}
    for identifier in ("1238610", "1408810"):
        canonical[identifier] = sha(ET.canonicalize(ET.tostring(records[identifier], encoding="unicode"), strip_text=True).encode())
        assert canonical[identifier] == receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"][identifier]
    reused = ("jmdict-families.xml", "kanjidic2-records.xml", "comparison-cards/響.md",
              "source-receipt.json", "query-membership.json", "external-capture-bindings.json",
              "authored-source-analysis-001.json", "pair-dispositions-001.json")
    for name in reused:
        rel = (OUT / name).relative_to(REPO).as_posix()
        assert (OUT / name).read_bytes() == git("show", PARENT + ":" + rel)
    write(OUT / "source-reuse-002.json", {
        "parent": PARENT, "method": "Reuse existing complete pinned selections; no new query, survey or fetch.",
        "files": {name: sha((OUT / name).read_bytes()) for name in reused},
        "completeFamiliesRead": canonical,
        "positiveDefinitions": {
            "1238610": "Complete 響く: resound/be heard far away, reverberate/shake/vibrate, come home/remain, have an effect/make an impression.",
            "1408810": "Complete 打つ family: retains rare 拍つ and every sense including move/impress/touch, with no per-spelling sense allocation. Its other senses are retained, not collapsed to this excerpt.",
        },
        "allocation": "The audible clapping/resonance distinction remains, but does not settle the effect/impression region. Protect that consequential uncertainty with one direct symmetric precaution, not an ordinary-synonym finding.",
        "completeRecordsRemainAt": "jmdict-families.xml",
        "sourceReadReceipt": {"path": str(HERE / "reconciliation-002-source-read-001" / "receipt.json"),
                              "sha256": sha((HERE / "reconciliation-002-source-read-001" / "receipt.json").read_bytes())},
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    previous_raw = (OUT / "pair-dispositions-001.json").read_bytes()
    previous = json.loads(previous_raw)
    current = copy.deepcopy(previous)
    row = next(item for item in current["rows"] if item["pair"] == ["拍", "響"])
    row.update({
        "decision": "precaution",
        "positiveSourceBasis": row["positiveSourceBasis"] + " Complete 1408810 also retains moving/impressing/touching with rare 拍つ, without per-spelling allocation; this is a consequential unresolved comparison rather than an ordinary collision.",
        "comparisonLabelOnTarget": "Resound/echo differs from ordinary clapping or musical pulse. Its effect/impression region meets the unallocated moving/impressing/touching senses of the complete 打つ/rare 拍つ family, so the audible distinction alone cannot establish whole-pair harmlessness.",
        "targetLabelOnComparison": "Ordinary clap/musical beat is not itself a definition of resonance or effect. Whether the broad family's effect/impression senses apply to ordinary bare 拍 remains unresolved; protect this question directly rather than assert either universal synonymy or harmlessness.",
        "qualification": "Direct precaution for unresolved effect/impression allocation, not a proven ordinary collision or a new missing-exclusion finding. Complete rare-spelling restrictions remain. Lexical uncertainty is not removed by the guard.",
        "directExclusionOnNewEndpoint": True, "openQuizHold": False,
    })
    row["completeFamilyCanonicalHashes"]["1408810"] = canonical["1408810"]
    current.update({
        "parent": PARENT, "counts": dict(collections.Counter(item["decision"] for item in current["rows"])),
        "supersedes": {"path": "pair-dispositions-001.json", "sha256": sha(previous_raw),
                       "historyPreserved": True, "changedPairOnly": ["拍", "響"]},
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    assert current["counts"] == {"guard": 8, "precaution": 17, "bounded-noncollision": 3}
    assert [a["pair"] for a, b in zip(previous["rows"], current["rows"]) if a != b] == [["拍", "響"]]
    write(OUT / "pair-dispositions-002.json", current)
    pair_sha = sha((OUT / "pair-dispositions-002.json").read_bytes())
    old_mapping = json.loads((OUT / "responses" / "gpt-mapping-001.json").read_text(encoding="utf-8"))
    old_d18 = next(item for item in old_mapping["comparisonDispositions"] if item["id"] == "D18")
    for family in ("claude", "gpt"):
        own = {str(path): digest for path, digest in bindings.items()
               if family.upper() in path.name}
        mapping = {
            "parent": PARENT, "authorStatus": "unpublished-proposal-awaiting-two-independent-confirmations",
            "ownConfirmationBindings": own,
            "historicalMapping": {"path": family + "-mapping-001.json",
                                  "sha256": sha((OUT / "responses" / (family + "-mapping-001.json")).read_bytes())},
            "neutralPair": ["拍", "響"], "neutralTable": "../pair-dispositions-002.json",
            "neutralTableSha256": pair_sha, "authorDisposition": "precaution",
            "lexicalAllocationResolved": False, "ordinaryCollisionEstablished": False,
            "oldSnapshotAcceptanceNotTransferred": True, "reviewContactOrLaunch": False,
        }
        if family == "gpt":
            mapping.update({
                "originalOpenClaimIds": old_mapping["originalOpenClaimIds"],
                "originalComparisonQuestions": [item["initialQuestion"] for item in old_mapping["comparisonDispositions"]],
                "historicalD18Disposition": old_d18,
                "currentD18": {"id": "D18", "confirmationLimit": "L1", "authorDisposition": "precaution",
                               "directPairProtected": True, "lexicalAllocationResolved": False,
                               "status": "author-addressed-awaiting-independent-confirmation"},
                "confirmationStatus": "Valid executed UNVERIFIED evidence on the old snapshot, not failed/void or confirmation acceptance.",
                "citationErratum": "The compact confirmation XML's 響く1238610 is line10, not L1's line8 (記1223130); 打つ1408810 is line26. This is the adjudicated presentation erratum, not the retained pretty XML's line numbers. Raw report stays unchanged.",
                "retainedConfirmationLimits": ["L" + str(i) for i in range(1, 9)],
            })
        else:
            mapping["neutralReason"] = "The complete 響く effect/impression senses and unallocated complete 打つ/rare 拍つ move/impress/touch senses motivate a direct precaution. The ordinary audible meanings remain distinct; no ordinary synonymy or independent source allocation is claimed."
            mapping["retainedConfirmationLimits"] = ["L" + str(i) for i in range(1, 6)]
        other = "gpt" if family == "claude" else "claude"
        assert other not in json.dumps(mapping, ensure_ascii=False).lower()
        write(OUT / "responses" / (family + "-mapping-002.json"), mapping)
    responses = {
        "claude": """# B130 Claude author response 002

Parent: d440617274eef6ea7611e60f147d6483f29ca710.
This is an unpublished author proposal awaiting two independent confirmations.
The historical accepted confirmation applies to the parent only.

The sole runtime delta appends 響 to 拍's direct precautions and minimally
qualifies its Notes. Complete 響く1238610 positively includes having an effect
and making an impression. Complete 打つ1408810 retains rare 拍つ and
moving/impressing/touching without per-spelling allocation. Distinguishing
clapping or a beat from audible resonance does not resolve that broader region.
The precaution protects the unresolved question, not ordinary synonymy or a
newly proven collision. No new source or query was needed.

The neutral pair-dispositions-002.json changes only this pair; all earlier
dispositions and responses remain historical. Ordered metadata, selected
readings, curated choices, support articles, geometry and other runtime bytes
are preserved. Historical confirmation limits L1-L5 remain: identity,
image/source scope, bounded host mechanics, rare-family allocation and
mechanical rather than linguistic check evidence. Ten serial gates before and
after signing do not supply independent confirmation or native/device safety.
No push, reviewer contact, publication or delivery credit is claimed.
""",
        "gpt": """# B130 GPT author response 002

Parent: d440617274eef6ea7611e60f147d6483f29ca710.
This is an unpublished author proposal awaiting two independent confirmations.
The valid executed UNVERIFIED confirmation remains historical evidence,
not a failed/void execution or accepted confirmation of the successor.

D18 / confirmation L1: 響 is now appended as a direct precaution on 拍.
The Notes preserve ordinary clapping/beat versus audible resonance while
protecting the unresolved effect/impression region. Complete 響く1238610
positively has effect/impression senses; complete 打つ1408810 retains rare
拍つ and move/impress/touch without per-spelling allocation. The added guard
does not establish an ordinary collision, allocate every sense to bare 拍 or
turn the original question into a newly proven missing-exclusion finding.

Citation erratum: L1's compact XML line8 is 記1223130. 響く1238610 is line10;
打つ1408810 is line26. These are compact presentation lines, not line numbers
in the retained pretty XML. The raw report is unchanged and the erratum does
not remove the substantive uncertainty.

The new neutral table changes only 拍/響 to a precaution. gpt-mapping-002.json
preserves all 24 original IDs/questions and the old D18 disposition; no initial
question or historical limit is erased. F1-F4 and O1 remain as historically
disposed, not newly reviewed here. Confirmation limits L1-L8 remain, including
unresolved lexical/image allocation, bounded host-only readings, latent
拍ひゃく/耗ぼう, unread index candidates, nonfatal warnings and no native/device,
old-APK, publication or delivery acceptance. All other runtime bytes remain
unchanged except manifest regeneration. Ten serial gates are run before and
after signing; the signed identity and receipts are bound at handoff.
""",
    }
    for family, text in responses.items():
        other = "gpt" if family == "claude" else "claude"
        assert other not in text.lower()
        write(OUT / "responses" / (family + "-response-002.md"), text.encode())
    print(json.dumps({"pairCounts": current["counts"], "changedPair": ["拍", "響"],
                      "sourceQueries": 0, "sourceFetches": 0, "pairTableSha256": pair_sha}, ensure_ascii=False))
finally:
    write(HERE / "reconciliation-002-source-read-001" / "author-memory.json", guard.finish())
