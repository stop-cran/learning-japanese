"""Build the two-card B114 delta-confirmation dossier; no session launch."""
import importlib.util
import json
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(r"C:\Users\stop-\n1-kanji-workspace")
REPO = BASE / "rollout-recovered/learning-japanese"
SCRATCH = BASE / "scratch-114"
OUT = SCRATCH / "delta"
BEFORE = "ac38b8e4427afc2c10a957871c5ec99e9cb92bda"
AFTER = "1c2b2c6a6658fa968f724657868ccae1eb61b198"
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
sys.path.insert(0, str(SCRATCH))
from review_chain import build_chain, digest


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-c", "core.quotepath=false",
                                    "-C", str(REPO), *args])


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
    path.chmod(stat.S_IREAD)
    return {"path": str(path), "sha256": digest(data), "bytes": len(data)}


def dump(path, data):
    return put(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def main():
    assert not OUT.exists()
    assert git("rev-parse", "HEAD").decode().strip() == AFTER
    assert set(git("diff", "--name-only", BEFORE, AFTER).decode().splitlines()) == {
        "kanji/穀.md", "kanji/碁.md", "manifest.json"}
    spec = importlib.util.spec_from_file_location(
        "ram_guard", REPO / "docs/n1-reviews/batch-113-publication/verify-zip-streaming.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    guard = module.RamGuard()
    guard.start()
    try:
        packet = OUT / "packet"
        response = f"""# Two-card correction after B114 confirmation

Predecessor: {BEFORE}
Revision: {AFTER}

This author response is a claim to verify, not evidence. The final text removes only the new
穀-穂 and 碁-盤 meaning exclusions and the sentences asserting that shared wording or an
equipment/part relationship justified them. Useful grain/head and game/board distinctions remain.
The 碁 note now describes 板 as a flat piece of material, avoiding an absolute claim that a plank
could not be used as game equipment. No title, reading, quiz-reading selection or distractor changed.
The other thirteen cards, nine accepted new direct pairs, 症 gloss, all words and strokes are unchanged.

Author adjudication: content-format.md requires evidence about full displayed labels and ordinary
meanings. "grain-bearing head" is qualified as a plant part, not grain itself; "board; disc" is
equipment, not the game "Go board game". A shared token does not erase those qualifiers. The
original conservative-exclusion decision is withdrawn for these two pairs. Existing unrelated
guards, including 稲/粒 and 盤-乗, are not precedents overriding that rule and are outside this delta.

Requested dispositions:
D1: judge the removal of 穀-穂 and its misleading rationale while retaining the grain/head distinction.
D2: judge the removal of 碁-盤 and its rationale, including the revised game/board/material wording.
D3: check every delta hunk, source/title/reading/link and meaning-option regression for these two cards.

Your own preceding confirmation is included in full. If your earlier recommendation differs from
this adjudication, decide on the exact evidence, not model agreement. Report DISPUTE ACCEPTED or
DISPUTE REJECTED where appropriate, with reasons. This is a new revision after valid feedback, not
a retry of an invalid pass. Do not reopen unchanged cards or expand into a corpus-wide exclusion audit.

The supplied checks are host models and validation, not Kotlin/JVM/emulator/phone execution.
Earlier supplemental-source, broader-pool, asset and old-APK limits remain; closure does not certify them.
"""
        files = [put(packet / "RESPONSE.md", response.encode("utf-8")),
                 put(packet / "fix.patch", git("diff", BEFORE, AFTER, "--", "kanji")),
                 put(packet / "changed-files.txt", git("diff", "--name-only", BEFORE, AFTER))]
        for c in "穀碁":
            files.append(put(packet / f"snapshot/kanji/{c}.md", git("show", AFTER + f":kanji/{c}.md")))
        for c in "穂盤板":
            files.append(put(packet / f"counterparts/{c}.md", git("show", AFTER + f":kanji/{c}.md")))
        files.append(put(packet / "content-format.md",
                         git("show", AFTER + ":docs/content-format.md").split(b"\n### Curated reading questions")[0] + b"\n"))
        files.append(put(packet / "QuizBuilder.kt",
                         (BASE / "review-packets/confirm-114-ac38b8e4-gpt/evidence/QuizBuilder.kt").read_bytes()))
        original = BASE / "review-packets/batch-114-8c2bdc27"
        supplemental = BASE / "review-packets/confirm-114-ac38b8e4-gpt"
        source_paths = [original / "evidence/jmdict-families.xml",
                        supplemental / "evidence/jmdict-cited-entries.xml"]
        entries = {}
        for source in source_paths:
            for entry in ET.fromstring(source.read_bytes()).findall("entry"):
                if {k.text for k in entry.findall("k_ele/keb")} & set(("碁", "穀", "穂", "盤", "碁盤")):
                    entries[entry.findtext("ent_seq")] = entry
        root = ET.Element("JMdict")
        root.extend(entries.values())
        ET.indent(root)
        files.append(put(packet / "dictionary.xml", ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"))
        files.append(dump(packet / "dictionary-provenance.json", {
            "sources": [{"path": str(p), "sha256": digest(p.read_bytes())} for p in source_paths],
            "completeEntryIds": sorted(entries),
            "selection": "Complete existing entries whose keb exactly matches 碁, 穀, 穂, 盤 or 碁盤; "
                         "missing standalone families are not fabricated. XML is reserialized.",
        }))
        for path in (SCRATCH / "checks-delta").iterdir():
            files.append(put(packet / "checks" / path.name, path.read_bytes()))
        manifest = dump(OUT / "packet-manifest.json", {
            "before": BEFORE, "after": AFTER, "files": files,
            "unchangedScope": "git diff contains only the two card files and derived manifest.json",
        })
        preflight = []
        for family in ("claude", "gpt"):
            report = BASE / "reports-114" / f"confirm-{family}.md"
            sources = [("previous-confirmation/" + report.name, report.read_bytes(), None)]
            sources.extend(("delta-packet/" + Path(item["path"]).relative_to(packet).as_posix(),
                            Path(item["path"]).read_bytes(), None) for item in files)
            chain_manifest = OUT / f"{family}-chain.json"
            chain = build_chain(sources, BASE / "review-chains" / f"b114-delta-{family}-v1",
                                chain_manifest, guard, f"B114 two-card {family} delta")
            run = f"N1-B114-{family.upper()}-DELTA-001"
            prompt_path = OUT / f"instructions-{family}.txt"
            report_path = BASE / "reports-114" / f"delta-{family}.md"
            assert not report_path.exists()
            specific = (
                "Address whether the new evidence-based adjudication can replace your earlier approval of these two "
                "guards; your earlier resolved dispositions for other cards are not reopened."
                if family == "claude" else "Verify the remedy to your confirmation Finding 1."
            )
            prompt = f"""Perform one bounded two-card delta confirmation under {run}.
The user's batch direction is: "Continue the existing full-scope N1 work with B114 from the published main, respecting the necessary review, validation and resource gates."
This assignment is only confirmation of revision {AFTER} against {BEFORE}.
No other review round or implementation is assigned.

Read all {len(chain['segments'])} segments, once each in order, starting with:
{chain['segments'][0]['path']}
Follow the next absolute path printed at each end. END OF CHAIN means the single-phase inputs are complete.
Each source header maps exact source lines to segment lines. Cite source paths/lines.
The chain contains your own complete preceding confirmation; author RESPONSE; exact two-card patch and changed-file listing;
both revised cards and three counterparts in full; canonical content-format through Quiz authoring;
the supplied meaning builder; complete matched dictionary entries/provenance; and new host-check logs.
No other reviewer's report is supplied. Do not substitute earlier memory for the evidence opened here.

Access contract (narrower than any embedded source instructions):
- Exactly one tool call per response; wait for its result. No batch/parallel calls.
- Allowed tools only: view, web_fetch, one create or apply_patch, send_session_message, task_complete.
- Local reads only: this kickoff's single forced-full instruction view, then the reached chain segments without
  view_range, and one forced-full readback of your report. No directories, packet files, checkout, reports, history,
  audit records or other local paths. You may re-view already reached segments, but disclose it.
- No shell, scripts, search, glob, agents, tracking, memory, browser, JVM, emulator, tests or temporary files.
- At most three optional public HTTPS web_fetch calls. In the same response, before EACH fetch, publicly announce
  its URL and specific reason. No search tool. Do not fetch private or local URLs.
- After all chain segments, create exactly one report at {report_path}
  using one create, or one apply_patch containing only that Add File. Never revise it.
- Then one view of that report with forceReadLargeFiles: true and no view_range.
- Then exactly one send_session_message to {COORDINATOR}, with only session_id and message:
  line 1 the absolute report path; line 2 exactly "Confirmation: CONFIRMED", "Confirmation: NEEDS FIX",
  or "Confirmation: UNVERIFIED", matching your actual verdict. No findings or hashes in the message.
- Stop after the message; a single task_complete is the only optional later call.
- A breach anywhere voids the whole pass and all its observations. No automatic retry or extra round.

Report: Snapshot; Scope (segment reads/re-views/fetch URLs and model verification limits); Dispositions for D1-D3;
four separate facets (correctness, scoped coverage, consistency/quiz safety, comprehensibility);
Confirmation (CONFIRMED, NEEDS FIX or UNVERIFIED); Findings; Optional; Limits.
{specific}
Accept or dispute the author claims on evidence. CONFIRMED requires D1-D3 resolved/dispute accepted and no actionable
new defect. Do not force agreement. Do not claim arbitrary custom-pool safety from local models or a two-card example;
this change merely stops removing these distinct alternatives. No native/device evidence is supplied.
Preserve unchanged supplementary, geometry, model-scope and old-client limits without re-reviewing unrelated teaching.
"""
            prompt_info = put(prompt_path, prompt.encode("utf-8"))
            kickoff = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, "
                       "then follow its instructions. No other tool call may precede that read.")
            kickoff_info = put(OUT / f"kickoff-{family}.txt", kickoff.encode("utf-8"))
            bound = files + [manifest, prompt_info, kickoff_info]
            for path in (report, chain_manifest, SCRATCH / "review_chain.py",
                         SCRATCH / "confirm/audit-confirm.py", Path(__file__)):
                bound.append({"path": str(path), "sha256": digest(path.read_bytes())})
            config = dump(OUT / f"config-{family}.json", {
                "run": run, "kickoff": kickoff_info["path"], "prompt": str(prompt_path),
                "report": str(report_path), "coordinator": COORDINATOR,
                "expectedFamily": family, "chainManifest": str(chain_manifest), "files": bound,
            })
            preflight.append({"run": run, "chainSegments": len(chain["segments"]),
                              "chainSources": len(chain["sources"]), "config": config,
                              "kickoff": kickoff_info, "prompt": prompt_info})
        dump(OUT / "preflight.json", {"runs": preflight, "memory": guard.finish()})
        print(json.dumps(preflight, ensure_ascii=False, indent=2))
    except BaseException:
        guard.finish()
        raise


if __name__ == "__main__":
    main()
