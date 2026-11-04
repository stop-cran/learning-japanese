from pathlib import Path

c = Path(__file__).resolve().parent
source = (c / "reconcile-execution-234.py").read_text(encoding="utf-8").split("record = {", 1)[0]
for before, after in [
    ("234", "243"), ("046", "047"),
    ("1537828bb31c8835f3f114737fc1199bfce84cd4", "46e073816162fa756dbd19c87dd380ad0dc81ec3"),
    ("21ddf0a8-3024-4f98-b2f4-4ab1f216cdee", "7c7d6839-e647-4495-bdc4-feb224373fee"),
    ('"word-components", "word-animal-comparison")', '"word-components", "word-animal-comparison", "word-sign-boundary")'),
    ("[150, 245]", "[140, 255]"), ("[149:245]", "[139:255]"),
    ("len(calls) == 14", "len(calls) == 15"),
    ('calls.values()}) == 14', 'calls.values()}) == 15'),
    ("len(returned) == 9", "len(returned) == 10"),
    ("All14 calls in14distinctturns", "All15 calls in15distinctturns"),
    ("Nine PNG returns", "Ten PNG returns"),
]:
    assert before in source, before
    source = source.replace(before, after)
source += '''
record = {
    "schemaVersion": 1, "execution": 243, "batch": "047",
    "status": "native-and-freshAndroid-verified-pending-local-validation",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "contentSnapshot": snapshot,
    "reviewedTeachingSnapshot": "0afe0379c8e4bf799728d56601ff654ba54199c7",
    "native": native, "artifactIndex": index, "provenance": provenance,
    "android": android, "androidProvenance": android_provenance,
    "copiedEvidence": copied, "mechanicalVerification": mechanical,
    "independentVisual": visual,
    "coordinatorDirectImages": [
        str(control / "artifacts" / "batch-047-parent-native-attempt-1" / f"n1-047-{p}.png")
        for p in ("font-pairs", "kanji-reading-disposition")
    ],
    "coordinatorAdjudication": {
        "findings": [], "unresolvedConsequentialClaimsWithinBoundedVisualScope": [],
        "result": "Bounded visual acceptance, no teaching change. Coordinator directly viewed font-pairs and kanji-reading-disposition; other eight actual PNG reads belong to original reviewer, not current coordinator. Parent ten operational reads retained separately.",
        "originalFindings": "Two original blind textual reports42/42calls1/0overlaps/0XMLrangeviolations/all30resources and three nonblocking optional Claude groups preserved. Eight supplied Japanese sections across seven pages, not fresh upstream retrieval. Coordinator alone freshly inspected pinned complete five-path SVG geometry; initial Claude did not inspect it. No initial review rerun or manufactured serialization.",
        "processDeviation": "No overlapping or unfinished tool calls in this visual pass; not a claim about inherited initial overlap.",
        "reportQualification": "Original report preserved verbatim. Snapshot and operational facts supplied, not reviewer Git/hash/native test verification. Nine hash-equivalent viewports not separate independent reads. Clipped columns, keyboard-covered content and full articles not certified; no phone/quiz/drawing screenshot or interaction inferred. Reviewer statement about coordinator geometry refers to earlier source SVG inspection, not measured layout geometry or pixel metrics; current coordinator separately verifies returned-image correspondence.",
        "optional": [
            {
                "status": "optional",
                "claim": "Right edge of Typical words is clipped in captured viewport.",
                "disposition": "Visible sideways-scroll hint and fully readable post-table paragraph preserve selectedう/verifiedボウ/source-onlyモウ distinction. No demonstrated blocking defect; horizontal interaction and unseen columns not certified."
            },
            {
                "status": "optional",
                "claim": "Kana wrapping and selection-chip edge clipping.",
                "disposition": "Cosmetic wrapping does not change text or introduce demonstrated ambiguity. Chip row is sideways scrolling; unseen chip content and interaction not certified."
            }
        ],
        "fallbackDisposition": "卯卵印柳東 each have four distinct raster styles across Gothic/Mincho/Textbook/Brush. 卩 and旁 each share one Gothic-like system fallback across families, not four bundled designs; exact face unidentified. Bounded API35 readability and shape distinctions accepted, not physical-phone or exact-face provenance certification.",
    },
    "limits": "Bounded API35 emulator only. Original unchangedfixture accepted1terminal0/0/28glyphs/fullContentSyncONCEoffline. Parent source/artifact and fresh240Android3+1 exactXML verified, not rerun. Actual5580owned516stopped/requested2048MiB automatic2560MiB/appheap192m576m unchanged. OriginalClaude15serialviews/10PNG/0overlaps/0unfinished/exit0; original and actual resized returned bytes separately archived. Nine hash-equivalent viewports not independently viewed. Clipped/offscreen/fullarticles/keyboard-coveredcontent not certified. No freshquizdrawing/phone/native-speaker/generalrelease/currentmain/CI/publicZIP acceptance. CompatibleAndroidf9b59a2+ required; oldclients ignore curation and8000entry clients reject collection. Public73/1155remaining unchanged; no048/publication.",
}
save(reviews / "batch-047-native-acceptance.json", record)
print("Archived batch047 parent recovery and original reviewer exact report/15serialviews/10PNG returns.")
'''
target = c / "reconcile-execution-243.py"
assert not target.exists()
target.write_text(source, encoding="utf-8")
