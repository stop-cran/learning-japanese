from pathlib import Path

control = Path(__file__).resolve().parent
source = (control / "audit-batch-046-draft.py").read_text(encoding="utf-8")
for before, after in [
    ('execution": 229', 'execution": 234'), ("execution=229", "execution=234"),
    ("execution-229-", "execution-234-"),
    ('source = raw.decode("utf-8")', 'source = raw.decode("utf-8").replace("save(folder /", "save(control /")'),
    ('scope["save"](scope["folder"] / "batch-046-draft-audit.json", result)',
     'scope["save"](control / "execution-234-source-audit.json", result)'),
]:
    assert before in source, before
    source = source.replace(before, after)
target = control / "audit-execution-234-source.py"
assert not target.exists()
target.write_text(source, encoding="utf-8")

source = (control / "reconcile-execution-216.py").read_text(encoding="utf-8").split("record = {", 1)[0]
for before, after in [
    ("216", "234"), ("044", "046"),
    ("bb63b6182784ddc318574ef77490c2c9c672fe70", "1537828bb31c8835f3f114737fc1199bfce84cd4"),
    ("80caf75e-72b4-46da-a623-a2b89219e51f", "21ddf0a8-3024-4f98-b2f4-4ab1f216cdee"),
    ('"selection", "kanji-mnemonic"', '"selection", "kanji-radical", "kanji-mnemonic"'),
    ("len(calls) == 13", "len(calls) == 14"),
    ('calls.values()}) == 13', 'calls.values()}) == 14'),
    ("len(returned) == 8", "len(returned) == 9"),
    ('assert "None blocking or consequential." in report_content',
     'assert "Findings:" in report_content'),
    ("All13 calls in13distinctturns", "All14 calls in14distinctturns"),
    ("Eight PNG", "Nine PNG"),
    ("Five original reports", "Two original reports"),
]:
    assert before in source, before
    source = source.replace(before, after)
target = control / "reconcile-execution-234.py"
assert not target.exists()
target.write_text(source + '''
record = {
    "schemaVersion": 1, "execution": 234, "batch": "046",
    "status": "native-and-freshAndroid-verified-pending-local-validation",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "contentSnapshot": snapshot,
    "reviewedTeachingSnapshot": "006ef78f117fd3bcfa5d4425121e5ffaab448448",
    "native": native, "artifactIndex": index, "provenance": provenance,
    "android": android, "androidProvenance": android_provenance,
    "copiedEvidence": copied, "mechanicalVerification": mechanical,
    "independentVisual": visual,
    "coordinatorDirectImages": [
        str(control / "artifacts" / "batch-046-parent-native-attempt-1" / f"n1-046-{p}.png")
        for p in ("font-pairs", "kanji-reading-disposition")
    ],
    "coordinatorAdjudication": {
        "findings": [], "unresolvedConsequentialClaimsWithinBoundedVisualScope": [],
        "result": "Bounded visual acceptance, no teaching change. Coordinator directly viewed font-pairs and kanji-reading-disposition; other seven actual PNG reads belong to original reviewer, not current coordinator. Parent nine operational reads retained separately.",
        "originalFindings": "Two original blind textual reports42/45calls1/0overlaps/0XMLrangeviolations/all34resources and five nonblocking optional Claude items preserved. Six Daijisen plus two Kanjipedia sections across seven pages, not five Daijisen. Optional sake sense supported for 日読みの酉; extra jocular register unverified and not taught. GPT live metadata corroboration is not frozen-byte authentication. Coordinator pinned stroke6/interior and7/bottom audit remains separate from original textual review.",
        "processDeviation": "No overlapping or unfinished tool calls in this visual pass; not a claim about inherited initial overlap.",
        "reportQualification": "Original report preserved verbatim. Snapshot and operational facts supplied, not reviewer Git/hash/native test verification. Nine hash-equivalent viewports not separate independent reads. Clipped columns, keyboard-covered content and full articles not certified; no phone/quiz/drawing screenshot or interaction inferred.",
        "optional": [],
        "fallbackDisposition": "All seven 酉西鳥酒配曲画 have four distinct raster styles across Gothic/Mincho/Textbook/Brush. Bounded API35 readability and 酉/西 distinction accepted; not exact font-face provenance or physical-phone certification.",
    },
    "limits": "Bounded API35 emulator only. Original unchangedfixture accepted1terminal0/0/28glyphs/fullContentSyncONCEoffline. Parent source/artifact and fresh231Android3+1 exactXML verified, not rerun. Actual5580owned20048stopped/requested2048MiB automatic2560MiB/appheap192m576m unchanged. OriginalClaude14serialviews/9PNG/0overlaps/0unfinished/exit0; original and actual resized returned bytes separately archived. Nine hash-equivalent viewports not independently viewed. Clipped/offscreen/fullarticles/keyboard-coveredcontent not certified. No freshquizdrawing/phone/native-speaker/generalrelease/currentmain/CI/publicZIP acceptance. CompatibleAndroidf9b59a2+ required; oldclients ignore curation and8000entry clients reject collection. Public72/1156remaining unchanged; no047/publication.",
}
save(reviews / "batch-046-native-acceptance.json", record)
print("Archived batch046 parent recovery and original reviewer exact report/14serialviews/9PNG returns.")
''', encoding="utf-8")
print("Generated current-batch source audit and bounded visual evidence archiver.")
