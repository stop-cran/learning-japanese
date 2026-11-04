from pathlib import Path

c = Path(__file__).resolve().parent
source = (c / "reconcile-execution-243.py").read_text(encoding="utf-8").split("record = {", 1)[0]
for before, after in [
    ("46e073816162fa756dbd19c87dd380ad0dc81ec3", "66211c0f70abdc92f565bebb095e6c18344bde52"),
    ("7c7d6839-e647-4495-bdc4-feb224373fee", "80a82572-cc26-4d43-b490-52fbc401e296"),
    ("243", "252"), ("047", "048"),
    ('"kanji-lookalikes", "word-sign-example", "word-components", "word-animal-comparison", "word-sign-boundary"',
     '"kanji-lookalikes", "reused-en-mnemonic", "word-sign-example", "word-components", "word-sign-boundary"'),
    ("[140, 255]", "[140, 275]"), ("[139:255]", "[139:275]"),
    ("len(calls) == 15", "len(calls) == 17"),
    ('calls.values()}) == 15', 'calls.values()}) == 17'),
    ("All15 calls in15distinctturns", "All17 calls in17distinctturns"),
]:
    assert before in source, before
    source = source.replace(before, after)
source += '''
record = {
    "schemaVersion": 1, "execution": 252, "batch": "048",
    "status": "native-and-freshAndroid-verified-pending-local-validation",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "contentSnapshot": snapshot,
    "reviewedTeachingSnapshot": "ac944d9e66a6aeb4f8272f89a6fe1b40d87b47c9",
    "native": native, "artifactIndex": index, "provenance": provenance,
    "android": android, "androidProvenance": android_provenance,
    "copiedEvidence": copied, "mechanicalVerification": mechanical,
    "independentVisual": visual,
    "coordinatorDirectImages": [
        str(control / "artifacts" / "batch-048-parent-native-attempt-1" / f"n1-048-{p}.png")
        for p in ("font-pairs", "kanji-reading-disposition")
    ],
    "coordinatorAdjudication": {
        "findings": [], "unresolvedConsequentialClaimsWithinBoundedVisualScope": [],
        "result": "Bounded visual acceptance, no teaching change. Coordinator directly viewed font-pairs and kanji-reading-disposition; other eight actual PNG reads belong to original reviewer, not current coordinator. Parent ten operational reads retained separately.",
        "originalFindings": "Two blind textual initials34/33calls plus bounded original-session supplements3/3calls, zero internaloverlaps/XMLrangeviolations preserved. Initial common task incorrectly called演unchanged and omitted exactdelta; supplements closed演line24componentlink on unchanged teaching snapshot, not retroactive blind coverage. Two nonblocking optional Claude groups retained. Eight supplied Japanese sections across seven pages, not fresh upstream retrieval. Coordinator alone freshly inspected pinned86lineSVG geometry at earlier authoring checkpoint.",
        "processDeviation": "No overlapping or unfinished tool calls in this visual pass.",
        "reportQualification": "Original report preserved verbatim. Snapshot and operational facts supplied, not reviewer Git/hash/native test verification. Ten hash-equivalent viewports not separate independent reads. Clipped columns, keyboard-covered content and full articles not certified; no phone/quiz/drawing screenshot or interaction inferred. Earlier coordinator SVG inspection is distinct from current returned-image dimension/resampling checks.",
        "optional": [
            {
                "status": "optional",
                "claim": "Right edge of Typical words is clipped in captured viewport.",
                "disposition": "Visible sideways-scroll hint and readable post-table paragraph preserve selectedとら/verifiedインcalendar recognition distinction. No demonstrated blocking defect; horizontal interaction and unseen columns not certified."
            }
        ],
        "fallbackDisposition": "寅演黄申 each have four distinct raster styles across Gothic/Mincho/Textbook/Brush. 宀氵虍黃 each share one Gothic-like system fallback across families, not four bundled designs; exact face unidentified. Bounded API35 readability and shape distinctions accepted, not physical-phone or exact-face provenance certification.",
    },
    "limits": "Bounded API35 emulator only. Original unchangedfixture accepted1terminal0/0/32glyphs/fullContentSyncONCEoffline, including changed演link/SystemBack. Parent source/artifact and fresh249Android3+1 exactXML verified, not rerun. Actual5580owned20980stopped/requested2048MiB automatic2560MiB/appheap192m576m unchanged. OriginalClaude17serialviews/10PNG/0overlaps/0unfinished/exit0; original and actual resized returned bytes separately archived. Ten hash-equivalent viewports not independently viewed. Clipped/offscreen/fullarticles/keyboard-coveredcontent not certified. No freshquizdrawing/phone/native-speaker/generalrelease/currentmain/CI/publicZIP acceptance. CompatibleAndroidf9b59a2+ required; oldclients ignore curation and8000entry clients reject collection. Public74/1154remaining unchanged; no049/publication.",
}
save(reviews / "batch-048-native-acceptance.json", record)
print("Archived batch048 parent recovery and original reviewer exact report/17serialviews/10PNG returns.")
'''
target = c / "reconcile-execution-252.py"
assert not target.exists()
target.write_text(source, encoding="utf-8")

source = (c / "audit-batch-048-draft.py").read_text(encoding="utf-8")
for before, after in [
    ('source = raw.decode("utf-8")', 'source = raw.decode("utf-8").replace("save(folder /", "save(control /")'),
    ('execution": 247', 'execution": 252'), ("execution=247", "execution=252"),
    ("execution-247-", "execution-252-"),
    ('scope["save"](scope["folder"] / "batch-048-draft-audit.json", result)',
     'scope["save"](control / "execution-252-source-audit.json", result)'),
]:
    assert before in source, before
    source = source.replace(before, after)
source += '''
result.update(execution=252, stage="mechanical-source-audit-at-native-visual-checkpoint",
    limits="Mechanical re-verification on unchanged teaching, not fresh linguistic/source-page/native acceptance. Original textual and bounded visual reviews retained separately; latest-main/publication and physical-phone/general-release pending.")
result["qualifiedSourceSectionsReverified"]["boundary"] = "Mechanical source hashes/ranges/markers and pinned geometry/converter candidate reverified using the inspected original qualification audit prefix. No fresh source-page/SVG comprehension or retrieval claimed in execution252; earlier author inspection remains historical."
scope["save"](control / "execution-252-source-audit.json", result)
'''
target = c / "audit-execution-252-source.py"
assert not target.exists()
target.write_text(source, encoding="utf-8")
print("Prepared evidence archival and unchanged-content mechanical audit adapters.")
