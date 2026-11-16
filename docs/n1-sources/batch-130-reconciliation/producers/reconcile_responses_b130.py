import json
from pathlib import Path
from b130_common import HERE, REPO, ROOT, sha, start_guard, write

OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
PARENT = "ce1b5c895fac90852143f322a115c2de4e768e20"
HASHES = {
    "claude": [
        "1271c4fd8bad602e7f72fda096377e3ad4b8754ad0511f13aac7cea66b4f7af8",
        "1234f94b595f3b13e692c0f66af13e7af62dcb28d8538824952b4a5b478398ea",
        "8bf0413650e2bb991d01786eab32648c7a3a4da8e6775ec5f9689c1c38ba04d1"],
    "gpt": [
        "4ee7e2a8f59c71f0d577114b7b0edcf01c84b6b9c71fb3e8c18ed4504657b9c3",
        "9e20ef494dbca80f3f52527404e17dd9e31f46db4dc66e156250b0cbcaafe7b9",
        "76d056fae9ab4204fc967caa2fe0f7b83e297df279a5451fa3532daf96bc97fa"],
}
GPT_LIMITS = {
    "L1": "Original initial-pass scope and supplied-hash limitations stay historical; this is author reconciliation, not a new independent initial or confirmation.",
    "L2": "No new visual geometry, font rendering, binary Joyo PDF or image-glyph identification; existing stroke bytes and source discrepancies are preserved.",
    "L3": "Every one of the 24 initially open comparison IDs is retained below and linked to a source-backed guard/precaution or bounded distinction. Old glyph and broad rare-spelling allocation uncertainty remains; protected choices are not lexical-certainty claims.",
    "L4": "New evidence adds 99 complete families, 31 complete character records, 28 actual comparison cards and narrow complete external captures. This improves the specified comparisons, not exhaustive independent source coverage.",
    "L5": "Unread index-only candidates remain limits, not new findings or a next batch. No whole-index safety assertion.",
    "L6": "Curated choices and original finite checks stay scoped to the three targets; no general safety certification of older cards or arbitrary option sets.",
    "L7": "All ten gates are rerun serially before and after signing; nonfatal Notes-mention warnings are retained in the actual logs. Automated passes are not linguistic proof.",
    "L8": "The original positive supplemental keys are still tested in bounded host N1/All/Starter-plus-one pools. Latent 拍ひゃく and 耗ぼう risks stay disclosed; no arbitrary/custom/multiple-borrow/Kotlin/native/device or old-APK acceptance.",
    "L9": "A signed local successor and local gates do not verify a served archive, publication, general release or whole-N1 delivery. Published accounting stays 261/1228, 967 remaining.",
    "L10": "No author claim to independently attest the reviewer's execution model; original declaration/attestation limitation stays historical.",
}
CLAUDE_LIMITS = {
    "L1": "The initial reviewer's model identity limitation stays historical; author reconciliation does not independently attest it.",
    "L2": "No new visual geometry, binary-PDF or rendered-font acceptance; stroke bytes and original source evidence remain unchanged.",
    "L3": "Image-only historical glyphs remain unidentified and source disagreements remain explicit; no inferred glyph identity.",
    "L4": "Only bounded host N1/All/Starter-plus-one checks. Latent 拍ひゃく and 耗ぼう risks remain; no custom/caller-built/multiple-borrow/Kotlin/native/device or old-APK acceptance. JVM/device work remains on hold.",
    "L5": "The original unread index candidates remain limits, not blanket harmless judgments. Any comparisons newly covered here are justified in neutral source rows only; no next-batch or whole-index safety claim.",
    "L6": "Broad rare 拍つ and old-dictionary allocations remain unresolved. Precautions protect specified choices rather than prove all retained family senses ordinary for bare characters.",
    "L7": "Ten serial host/static gates are rerun before and after signing. Warnings are preserved, not reclassified as linguistic proof. No publication or delivery credit.",
}

guard = start_guard()
try:
    pairs_path = OUT / "pair-dispositions-001.json"
    pairs = json.loads(pairs_path.read_text(encoding="utf-8"))
    indexed = {"/".join(r["pair"]): r for r in pairs["rows"]}
    table_sha = sha(pairs_path.read_bytes())
    for family, hashes in HASHES.items():
        run = "N1-B130-" + family.upper() + "-004"
        paths = [
            ROOT / "reports-130" / ("initial-" + family + "-004.md"),
            HERE / "review" / (run + "-adjudication.json"),
            HERE / "review" / (run + "-acceptance.json"),
        ]
        for path, digest in zip(paths, hashes):
            assert sha(path.read_bytes()) == digest, path
        adjudication = json.loads(paths[1].read_text(encoding="utf-8"))
        if family == "gpt":
            expected_ids = "D2 D3 D4 D5 D6 D8 D9 D10 D11 D12 D13 D14 D17 D18 D19 D20 D21 D22 D23 D24 D26 E5 E7 E8".split()
            assert adjudication["openClaimIds"] == expected_ids
            mapping = []
            for question in adjudication["unresolvedComparisons"]:
                target = next(iter(question["relatedNewCards"]))
                key = target + "/" + question["card"]
                row = indexed[key]
                mapping.append({
                    "id": question["id"], "pair": row["pair"],
                    "initialQuestion": question,
                    "authorDisposition": row["decision"],
                    "neutralRow": key, "neutralTableSha256": table_sha,
                    "authorStatus": "protected-with-qualified-lexical-uncertainty" if row["directExclusionOnNewEndpoint"]
                                   and row["decision"] == "precaution" else "source-backed-bounded-disposition",
                    "independentConfirmation": "not performed",
                    "openQuizHold": row["openQuizHold"],
                })
            assert [r["id"] for r in mapping] == expected_ids
            findings = {"F1": ["耗/便"], "F2": ["耗/擦"], "F3": ["耗/削"], "F4": ["拍/突"]}
            limits = GPT_LIMITS
            optional = {"O1": "Optional simplification not adopted: existing fully qualified historical lookup strings remain unchanged; full positive supplemental forms and allocation uncertainty stay in source evidence."}
            introduction = """# B130 GPT004 author response 001

Parent: ce1b5c895fac90852143f322a115c2de4e768e20.
This response describes the actual authored successor; the signed revision and
committed checks are bound separately at handoff. It is not confirmation or publication.

F1-F4: direct guards now protect 耗/便, 耗/擦, 耗/削 and 拍/突.
Qualified Notes distinguish news from convenience, friction from every rubbing
action, reduction from all consumption, and hand-striking from every thrust.

All 24 initially unresolved IDs remain historical in gpt-mapping-001.json.
Each maps to an explicit neutral bidirectional row, complete comparison card,
complete-family hashes and positive source rationale. This does not rewrite
the initial report's open IDs or call every candidate a proven collision.
The neutral table distinguishes established overlaps, qualified precautions
and four bounded distinctions. There is no unprotected consequential quiz hold
in this authored finite table; unresolved lexical allocation is still explicit.

In particular, independent new 信/音 entries establish news without a counter
or compound inference; 疲れる explicitly has object wear; 磨れる retains a rare
wear-out spelling; 下/落/退 have positive diminution senses. 乗り's kana-preferred
rhythm and 勉/勇 encouragement are not erased by their first titles.
Writing precautions for 記/識/筆 do not make broad 打つ-family senses ordinary
bare-拍 senses. 文/書 distinguish the written medium/action from news content;
研's complete physical refinement senses and 響's complete sound/effect senses
receive bounded distinctions, not title-only or physical/abstract dismissals.
城's qualified guard uses its independently captured historical カキ lookup,
not a wall sense inferred from the compound alone.

Citation erratum acknowledged: 摩耗/磨耗 is entry1604200 at initial
jmdict-families.xml:243, not :242. The original report/adjudication are unchanged.
Optional O1 remains optional and was not adopted.
"""
        else:
            mapping = []
            findings = {"F1": ["耗/擦", "耗/摩"], "F2": ["耗/削"]}
            assert adjudication["openClaimIds"] == []
            limits = CLAUDE_LIMITS
            optional = {
                "O1": "Adopted: ベイ is explained as voiced within compounds, without denying its separate pinned KANJIDIC2 entry.",
                "O2": "A direct 用 precaution now explicitly protects the broad use label against taught using-up; not every use depletes.",
                "O3": "Optional threshold expansion not adopted; prior 辺 guard and bounded 際 distinction remain. No new 際 defect is claimed.",
                "O4": "Optional blanket Notes expansion not adopted. Prior guards and qualified historical strings remain; exact nonfatal warning text is preserved.",
                "O5": "Adopted: 耗 clearly names curated 右/川/本 and labels 石/未 comparisons only.",
            }
            introduction = """# B130 Claude004 author response 001

Parent: ce1b5c895fac90852143f322a115c2de4e768e20.
This response describes the actual authored successor; the signed revision and
committed checks are bound separately at handoff. It is not confirmation or publication.

F1 is addressed with direct 耗/擦 and 耗/摩 guards and qualified friction/wear
Notes. F2 takes the permitted direct-guard remedy for 耗/削, with an explicit
reduction rationale. Rubbing, decrease and consumption remain distinct; no
transitive exclusion or universal synonymy is asserted.

The original bounded harmless 磨 judgment remains historical, not rewritten.
The newly opened complete 1595930 family independently retains rare 磨れる
with wear-out/becoming-worn senses. The successor therefore adds a qualified
direct 磨 precaution, rather than deriving constituent equality from 磨耗.
The neutral table explains every actual additional guard from positive sources.
New independent news/tidings entries for 信 and 音, object-wear 疲れる,
numerical/quality diminution under 下/落, rare diminishing 退く and positive
rhythm/encouragement evidence support their individual qualified dispositions.
The 拍/突 striking and writing-region precautions do not allocate every
rare 拍つ family action to ordinary bare 拍. The historical 城 guard does not
equate all castles with fences. Four source-backed bounded distinctions remain
unguarded; this is not a blanket collision claim.

All adjudicated citation errata are acknowledged as historical offsets:
the 削/用 and other actual card lines, the 拍手 families 1474820/1841790,
and 絶える at 絶.md:32 are not silently changed in the immutable report.
The original report/adjudication bytes remain unchanged.
"""
        response = {
            "run": run, "parent": PARENT,
            "originalBindings": [{"path": str(path), "sha256": digest} for path, digest in zip(paths, hashes)],
            "originalOpenClaimIds": adjudication["openClaimIds"],
            "findings": {fid: {"authorStatus": "addressed-awaiting-independent-confirmation",
                               "neutralPairs": keys, "neutralTableSha256": table_sha}
                         for fid, keys in findings.items()},
            "comparisonDispositions": mapping, "optionalPoints": optional, "limits": limits,
            "independentConfirmation": False, "publicationAccepted": False,
            "boundary": "Family-isolated author response only. No reviewer contact or confirmation launch. Neutral table has no reviewer identities or claim IDs.",
        }
        write(OUT / "responses" / (family + "-mapping-001.json"), response)
        text = introduction + "\n## Optional dispositions\n\n" + "\n".join(
            "- " + key + ": " + value for key, value in optional.items())
        text += "\n\n## Retained limits\n\n" + "\n".join("- " + key + ": " + value for key, value in limits.items()) + "\n"
        assert ("claude" if family == "gpt" else "gpt") not in text.lower()
        write(OUT / "responses" / (family + "-response-001.md"), text.encode("utf-8"))
    print(json.dumps({"isolatedResponses": 2, "historicalGptOpenIdsRetained": 24, "neutralPairs": len(indexed)}))
finally:
    write(HERE / "reconciliation-001" / "responses-memory-001.json", guard.finish())
