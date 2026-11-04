from pathlib import Path

c = Path(__file__).resolve().parent
source = (c / "stage-execution-243.py").read_text(encoding="utf-8")
for before, after in [
    ("46e073816162fa756dbd19c87dd380ad0dc81ec3", "66211c0f70abdc92f565bebb095e6c18344bde52"),
    ("243", "252"), ("047", "048"),
    ("2122/2521", "2122/2431"),
    ("46e0738-envelope", "66211c0-envelope"), ("8269", "8272"), ("8290", "8293"),
    ('"successfulViews": 15', '"successfulViews": 17'),
    ('"internalOverlappingStarts": 0', '"internalOverlappingStarts": 3'),
    ('"Freshparent240exactsource/copiedXML3+1errorsfailuresskips0;no252rerun."',
     '"Freshparent249exactsource/copiedXML3+1errorsfailuresskips0;no252rerun."'),
    ('"projectPublishedAdditions": 73, "remainingAdditions": 1155',
     '"projectPublishedAdditions": 74, "remainingAdditions": 1154'),
    ('"published": 73, "remaining": 1155', '"published": 74, "remaining": 1154'),
    ('"Originalunchangedfixture accepted1terminal0/0/fullContentSyncONCEoffline/28glyphprobes."',
     '"Originalunchangedfixture accepted1terminal0/0/fullContentSyncONCEoffline/32glyphprobes/changed演linkSystemBack."'),
]:
    assert before in source, before
    source = source.replace(before, after)
start = source.index('    "sourceAndBaselineAudit":')
end = source.index('    "limits":', start)
source = source[:start] + '''    "sourceAndBaselineAudit": "Five frozen input hashes/two decompressions/two exact extractions/26complete families/seven raw character records; exact75localadditions/985kanji4942words985strokesbaseline with exact original tiger/monkey guards. Exact pinned11stroke conversion/fonts/one required reciprocalpair/zeroactivatedbaselinepairs/twoorderedreadingdispositions/solekun-emptyon/direct虎guard/threewrong演黄申. Eight supplied sections=fiveDaijisen+oneNikkoku+twoKanjipedia/sevenHTMLpages, not eight dictionaries or fresh retrieval. Fullイン/とら retained;インverifiedcalendarrecognition/notobsolete/name-only. Exact演line24componentlink delta preserved. Source hashes prove bytes, not comprehension.",
    "audit": "parent-receipts/execution-252-source-audit.json",
    "auditExecutionNote": "Execution252 validation and mechanical audit exited0 under Python -X utf8. Helper generation initially asserted on replacement ordering before writing outputs; fixed without touching teaching or relaunching reviewer. An early live JSONL probe hit an incomplete in-flight line; completed raw execution parsed and audited only after process exit. Unsupported CLI help topic models returned1; current supported help options and actual execution/provider model identity retained.",
''' + source[end:]
start = source.index("names = [")
end = source.index("sources = ", start)
source = source[:start] + '''names = [
    "execution-252-source-audit.json", "execution-252-validation-receipts.json",
    "batch-048-stroke-audit.json", "verify-execution-252-recovery.py",
    "reconcile-execution-252.py", "audit-execution-252-source.py",
    "audit-batch-048-draft.py", "audit-batch-040-draft.py", "execution-246-audit.py",
    "run-batch-048-visual.ps1", "prepare-execution-252.py",
    "prepare-execution-252-evidence.py", "validate-execution-252.py",
    "prepare-execution-252-stage.py",
]
''' + source[end:]
start = source.index("next_action = (")
end = source.index("for path, field in (", start)
source = source[:start] + '''next_action = (
    "Resume SAME048 from signed native/visual evidence checkpoint; teaching unchangedac944d9/66211c0. "
    "Read docs/n1-reviews/batch-048-native-acceptance.json, preserved original visual report/execution receipt, "
    "docs/n1-sources/execution-252.json and COMPLETE live progress history. "
    "Do not rerun recovered Android/native/reviewer evidence without demonstrated new concern. "
    "Normal latest origin/main fetch/nonrewriting merge and actual combined-tree source/baseline/bothguards/"
    "readings/reciprocal/manifest/grammarvocabulary/361tests/originalbudgets/compatibility acceptance "
    "before publication; normal signing only, owner-scoped fast-forward push, exact remoteSHA, "
    "actual terminalgreenCI and every immutable publicZIP runtime entry/hash before counting "
    "published75/1153remaining. Current public74/1228,1154remaining/lastpublished3b2f689 unchanged. "
    "Originalunchangedfixture accepted1terminal0/0/32glyphs/fullContentSyncONCEoffline/changed演linkBack; "
    "fresh249Android3+1 exactXMLnames/timestamps/sourcecopy/root verified, not rerun. "
    "寅演黄申eachfourstyles;宀氵虍黃eachsharedGothic-likefallback/exactfaceunknown/notfourbundleddesigns; "
    "boundedAPI35readability accepted. OriginalClaudeactualclaude-opus-5.5/17views14distincttoolturns/"
    "onefour-textbatch3overlappingstarts/max4active violating explicitserialprompt;10PNGindividuallyserial/"
    "zeroimageoverlaps/zero unfinished/actualexit0. Do not claim strict all-tool serialization. "
    "Exact source/resizedreturnedpayloads separately retained. Report15response count corrected to "
    "actual14toolturns; clipped甲寅secondreading not fullyvisible/recoverable, reportoverclaim qualified. "
    "Ten additional hash-equivalent viewports not separate independent reads. "
    "Two blind actualdifferentfamilyinitials34/33calls plus originalsupplements3/3calls/nooverlaps/"
    "noXMLrangeviolations/twooptionalClaude groups preserved. Initial common task incorrectlycalled演unchanged/"
    "omitteddelta; originalsupplements closed演line24componentlink, not retroactiveblindcoverage. "
    "Eight supplied sections/sevenpages; no freshsource-page/SVG linguistic read in252. "
    "Fullイン/とら/order retained,emptyon/solekunとら;インverifiedcalendarrecognition/notobsolete/name-only; "
    "one reciprocalpair/zeroactivatedbaselinepairs/direct虎guard/wrong演黄申/bothoriginal虎猿guards/11strokes. "
    "Clipped/offscreen/fullarticles/keyboard-coveredcontent/fallbackquiz/freshquizdrawing/phone/"
    "native-speaker/generalrelease unverified. CompatibleAndroidf9b59a2+ required; oldclientsignorecuration/"
    "8000entryclientsreject. Actual5580owned20980stopped/requested2048MiBautomatic2560MiB/"
    "appheap192m576munchanged. No049/secondrunner/heapguardchange/amendment. "
    "Actualpermissiondenial/signingwait: preserve/report/yield, no retry/workaround."
)
''' + source[end:]
target = c / "stage-execution-252.py"
assert not target.exists()
target.write_text(source, encoding="utf-8")
print("Prepared evidence-only staging with preserved process deviation and publication boundary.")
