import json
import subprocess
from datetime import datetime
from pathlib import Path

control = Path(__file__).resolve().parent
root = control.parent / "learning-japanese"
snapshot = "1537828bb31c8835f3f114737fc1199bfce84cd4"
old = "01b3d3b2f0fc0fceca382d0ce54d91c13ab464a1"
progress_path = control / "progress.json"
data = json.loads(progress_path.read_text(encoding="utf-8-sig"))
assert data["checkpoint"] == 233 and data["batch"] == "046"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip() == snapshot
backup = control / "execution-234-start-progress.json"
assert not backup.exists()
backup.write_bytes(progress_path.read_bytes())
state = {
    "execution": 234, "startingHead": snapshot,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME046 recovered native/freshAndroid verification and bounded ORIGINAL-reviewer visual confirmation; signed evidence checkpoint before publication. No047 or second runner.",
    "status": "verifying-recovered-native-evidence",
    "startingCheckpointTiming": "Saved after entire authorized request including final persisted checkpoint and approved issue, read-only guidance/heads/parent-index/helper/original-report inspection; before evidence mutation or reviewer launch.",
}
data["execution234StartingState"] = state
data["activeExecution"] = state.copy()
progress_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate(source, target, replacements):
    text = (control / source).read_text(encoding="utf-8")
    for before, after in replacements:
        assert before in text, (source, before)
        text = text.replace(before, after)
    path = control / target
    assert not path.exists(), path
    path.write_text(text, encoding="utf-8")


generate("verify-execution-225-recovery.py", "verify-execution-234-recovery.py", [
    ("225", "234"), ("045", "046"), (old, snapshot),
    ("c0c51142ac779ed8", "4a05b1fff8b65ff6"),
    ("fullSingleImportOfflineSnakeSignArticleAndSystemBack", "fullSingleImportOfflineRoosterSignArticleAndSystemBack"),
    ("snakeSignRadicalAndLookalikesAcrossFourProductionFamilies", "roosterSignRadicalAndLookalikesAcrossFourProductionFamilies"),
    ("[1, 1057, 5015, 77, 0, 1]", "[1, 1058, 5016, 78, 0, 1]"),
    ('["シ"]', '["ユウ"]'), ('["み"]', '["とり"]'),
    ("8fea7eaa7dbc8e4db7814e168c2462ad748565cca6041b7e593fa711ab9cbc70", "4d7d6f710d574edbcde9eb0ca97b94d569ef8b5394ff0f4a7fe3b60875a6a7ef"),
    ('"包己已巳巻蛇記"', '"曲画西酉配酒鳥"'),
    ('(1 if character == "已" else 4)', "4"),
    ("== 14844", "== 20048"), ("01b3d3b-envelope.zip", "1537828-envelope.zip"),
    ("已 shares one fallback style", "All seven characters have four raster styles"),
    ("fresh222Android", "fresh231Android"),
])
generate("run-batch-045-visual.ps1", "run-batch-046-visual.ps1", [
    ("045", "046"), (old, snapshot),
    ("945744ea-501d-43bd-b966-a1a8ca98177b", "21ddf0a8-3024-4f98-b2f4-4ab1f216cdee"),
])
generate("validate-execution-216.py", "validate-execution-234.py", [("216", "234")])
generate("post-execution-216.ps1", "post-execution-234.ps1", [("216", "234")])
prompt = r"""SAME046 bounded ORIGINAL-session dependent visual confirmation, not a new blind initial review.
Frozen tracked content 1537828bb31c8835f3f114737fc1199bfce84cd4; unchanged teaching 006ef78f117fd3bcfa5d4425121e5ffaab448448. Sole untracked accepted non-runtime native fixture below.
You are original Claude reviewer session 21ddf0a8-3024-4f98-b2f4-4ab1f216cdee. Read your complete initial report:
C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-046-initial-claude.md
Preserve two blind actual different-family initials42/45calls,1/0internaloverlaps,0XMLrangeviolations/all34resources returned. Your paired bird/chicken initial reads overlapped; retained, not strict tool serialization. Five optional items nonblocking. Six Daijisen and two Kanjipedia entry sections across seven pages, not five Daijisen; supplied 日読みの酉 supports sake sense but does not establish your extra jocular register. No teaching change. Do not repeat initial full source review or read the other report.
Use ONLY SERIAL view calls, ONE tool call per response, and await each result. No edits, shell, delegation, parallel wrapper, source retries or files. Return full report in final answer, not task_complete.
Read both complete current teaching files, each in its OWN RESPONSE:
C:\Users\stop-\n1-kanji-workspace\learning-japanese\kanji\酉.md
C:\Users\stop-\n1-kanji-workspace\learning-japanese\words\酉.md
Read native fixture lines150-245 only:
C:\Users\stop-\n1-kanji-workspace\learning-japanese\docs\n1-reviews\batch-046-native\N1Batch046NativeTest.kt
Then actually view EACH of these NINE accepted PNGs singly, ONE PER RESPONSE:
"""
for name in ("font-pairs", "selection", "kanji-radical", "kanji-mnemonic",
             "kanji-reading-disposition", "kanji-lookalikes", "word-sign-example",
             "word-components", "word-animal-comparison"):
    prompt += str(control / "artifacts" / "batch-046-parent-native-attempt-1" / f"n1-046-{name}.png") + "\n"
prompt += """Assess visible readability/distinct glyphs 酉西鳥酒配曲画 in four actual production family rows; shared fallback would be acceptable if readable/distinguishable, not necessarily four designs. Especially check 酉/西 interior-line distinction, canonical 酉 radical no164, ひよみのとり/とりへん names, mnemonic versus etymology, fullユウ/とり versus sole selectedkunとり, sign versus bird/chicken, whole-word reading alternatives and historical-hour variations. Flag demonstrated blocking defects; distinguish optional horizontal-table clipping and unseen passages. Initial radical PNG has a keyboard overlay at bottom; assess actual visible metadata rather than certifying hidden content.
Supplied operational evidence, not independently verified by you: unchanged original fixture attempt1 two terminalcase0/no skips,28hasGlyphprobes; all seven characters four distinct raster styles. Full exact Git envelope productionContentSync ONCE imported1058kanji/5016words/N178/4a05b1fff8b65ff6/problems0/epoch1/fullrawonユウ/fullkunとり/emptyquizOn/solequizKunとり. Offline reciprocal/SystemBack passed. NINE additional hash-equivalent viewports only: kanji-radical-name=kanji-lookalikes; kanji-historical-boundary=kanji-lookalikes; word-cycle-example=word-sign-example; word-calendar-boundary=word-sign-example; backlink-kanji=kanji-mnemonic; system-back-word=word-components; word-compound-reading=word-components; word-sign-boundary=word-animal-comparison; word-historical-boundary=word-animal-comparison. These are not additional independently seen images or a quiz screenshot. Fresh231Android3+1 verified separately, no rerun. Own20048stopped/exacttemporaryAndroidcleanup; no other devices modified. ActualAPI35fingerprint google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys;requested2048MiB automatic2560MiB/appheap192m576m. Parent9acceptedPNGreads operational, NOT your independentvisual.
Return complete Snapshot/Scope/Verdicts/Findings/Optional/Limits report; list actual PNG reads and text ranges. Separate inherited textual CLEAN from bounded visual verdicts. No invented fresh source/Git/hash/dimensions verification, native meaning/reading/drawing sessions, phone/native-speaker/generalrelease/currentmain/CI/publicZIP claim. No optional quota; stop when no consequential in-scope defect remains. STRICTLY ONE TOOL CALL PER RESPONSE INCLUDING TEXT FILES.
"""
(control / "batch-046-visual-prompt.txt").write_text(prompt, encoding="utf-8")
print("Saved SAME046 starting scope and generated bounded helpers, full history preserved.")
