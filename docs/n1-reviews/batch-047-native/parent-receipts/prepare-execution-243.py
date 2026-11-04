from pathlib import Path

c = Path(__file__).resolve().parent
old = "1537828bb31c8835f3f114737fc1199bfce84cd4"
head = "46e073816162fa756dbd19c87dd380ad0dc81ec3"


def generate(source, target, changes):
    s = (c / source).read_text(encoding="utf-8")
    for before, after in changes:
        assert before in s, (source, before)
        s = s.replace(before, after)
    path = c / target
    assert not path.exists(), path
    path.write_text(s, encoding="utf-8")


common = [("234", "243"), ("046", "047"), (old, head)]
generate("verify-execution-234-recovery.py", "verify-execution-243-recovery.py", common + [
    ("4a05b1fff8b65ff6", "4ca64c255449dba4"),
    ("RoosterSign", "RabbitSign"), ("roosterSignRadicalAndLookalikes", "rabbitSignRadicalAndFallbacks"),
    ("[1, 1058, 5016, 78, 0, 1]", "[1, 1059, 5017, 79, 0, 1]"),
    ('["ユウ"]', '["ボウ", "モウ"]'), ('["とり"]', '["う"]'),
    ("4d7d6f710d574edbcde9eb0ca97b94d569ef8b5394ff0f4a7fe3b60875a6a7ef",
     "9c82a13afc9192f55b7d30248d28267125ade91b7a816a3090800cb028d4c2a7"),
    ('"曲画西酉配酒鳥"', '"卯卵印柳東卩旁"'),
    ("assert styles[character] == 4", 'assert styles[character] == (1 if character in "卩旁" else 4)'),
    ("== 20048", "== 516"), ("1537828-envelope", "46e0738-envelope"),
    ("fresh231Android", "fresh240Android"),
    ("All seven characters have four raster styles", "Five characters have four styles; 卩/旁 share fallback styles per character"),
])
generate("run-batch-046-visual.ps1", "run-batch-047-visual.ps1", [
    ("046", "047"), (old, head),
    ("21ddf0a8-3024-4f98-b2f4-4ab1f216cdee", "7c7d6839-e647-4495-bdc4-feb224373fee"),
])
generate("validate-execution-234.py", "validate-execution-243.py", [("234", "243")])
generate("post-execution-234.ps1", "post-execution-243.ps1", [("234", "243")])
source = (c / "audit-batch-047-draft.py").read_text(encoding="utf-8")
for before, after in [
    ('execution": 238', 'execution": 243'), ("execution=238", "execution=243"),
    ("execution-238-", "execution-243-"),
    ('source = raw.decode("utf-8")', 'source = raw.decode("utf-8").replace("save(folder /", "save(control /")'),
    ('scope["save"](scope["folder"] / "batch-047-draft-audit.json", result)',
     'scope["save"](control / "execution-243-source-audit.json", result)'),
]:
    assert before in source
    source = source.replace(before, after)
(c / "audit-execution-243-source.py").write_text(source, encoding="utf-8")
prompt = r"""SAME047 bounded ORIGINAL-session dependent visual confirmation, not a new blind initial review.
Frozen tracked content 46e073816162fa756dbd19c87dd380ad0dc81ec3; unchanged teaching 0afe0379c8e4bf799728d56601ff654ba54199c7. Sole untracked accepted non-runtime native fixture below.
You are original Claude reviewer session 7c7d6839-e647-4495-bdc4-feb224373fee. Read your complete initial report:
C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-047-initial-claude.md
Preserve two blind actual different-family initials42/42calls,1/0internaloverlaps,0XMLrangeviolations/all30resources returned. Your paired lexicalXML reads overlapped; retained, not strict tool serialization. Three optional groups nonblocking. Eight supplied Japanese sections across seven pages, not fresh upstream retrieval. Coordinator alone directly inspected geometry; do not claim you did.
Use ONLY SERIAL view calls, ONE tool call per response, and await each result. No edits, shell, delegation, parallel wrapper, source retries or files. Return full report in final answer, not task_complete.
Read both complete current teaching files, each in its OWN RESPONSE:
C:\Users\stop-\n1-kanji-workspace\learning-japanese\kanji\卯.md
C:\Users\stop-\n1-kanji-workspace\learning-japanese\words\卯.md
Read native fixture lines140-255 only:
C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-047-native\N1Batch047NativeTest.kt
Then actually view EACH of these TEN accepted PNGs singly, ONE PER RESPONSE:
"""
for name in ("font-pairs", "selection", "kanji-radical", "kanji-mnemonic",
             "kanji-reading-disposition", "kanji-lookalikes", "word-sign-example",
             "word-components", "word-animal-comparison", "word-sign-boundary"):
    prompt += str(c / "artifacts" / "batch-047-parent-native-attempt-1" / f"n1-047-{name}.png") + "\n"
prompt += """Assess visible readability/distinct glyphs 卯卵印柳東卩旁 in four actual production family rows; shared fallback acceptable if readable/distinguishable, not necessarily four designs. Especially check 卯/卵dots, 印leftside, 柳tree, right卩 radical26/ふしづくり, leftthree/righttwo strokes, mnemonic versus etymology, fullボウモウ/う versus sole selectedkunう, verifiedボウcalendar recognition versusモウsource-only, sign versus rabbit, whole-word卯年readings/干支えとversusかんしsense, historicalhour5-7am/6-8am, standalone卯lunar2versus卯月lunar4notGregorianApril. Flag demonstrated blocking defects; distinguish optional horizontal-table clipping and unseen passages. Initial radical PNG has a keyboard overlay at bottom; assess actual visible metadata rather than certifying hidden content.
Supplied operational evidence, not independently verified by you: unchanged original fixture attempt1 two terminalcase0/no skips,28hasGlyphprobes; 卯卵印柳東 each four raster styles, 卩 and旁 each shared Gothic-like systemfallback across families, exactface unknown/not four bundleddesigns. Full exact Git envelope productionContentSync ONCE imported1059kanji/5017words/N179/4ca64c255449dba4/problems0/epoch1/fullrawonボウモウ/fullkunう/emptyquizOn/solequizKunう. Offline reciprocal/SystemBack passed. NINE additional hash-equivalent viewports only: kanji-historical-boundary=kanji-lookalikes; kanji-month-boundary=kanji-lookalikes; word-cycle-example=word-sign-example; word-calendar-boundary=word-sign-example; backlink-kanji=kanji-mnemonic; system-back-word=word-components; word-compound-reading=word-components; word-historical-boundary=word-sign-boundary; word-month-boundary=word-sign-boundary. These are not additional independently seen images or a quiz screenshot. Fresh240Android3+1 verified separately, no rerun. Own516stopped/exacttemporaryAndroidcleanup; no other devices modified. ActualAPI35fingerprint google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys;requested2048MiB automatic2560MiB/appheap192m576m. Parent10acceptedPNGreads operational, NOT your independentvisual.
Return complete Snapshot/Scope/Verdicts/Findings/Optional/Limits report; list actual PNG reads and text ranges. Separate inherited textual CLEAN from bounded visual verdicts. No invented fresh source/Git/hash/dimensions verification, native meaning/reading/drawing sessions, phone/native-speaker/generalrelease/currentmain/CI/publicZIP claim. No optional quota; stop when no consequential in-scope defect remains. STRICTLY ONE TOOL CALL PER RESPONSE INCLUDING TEXT FILES.
"""
(c / "batch-047-visual-prompt.txt").write_text(prompt, encoding="utf-8")
print("Prepared bounded original visual followup and recovered-evidence verifier.")
