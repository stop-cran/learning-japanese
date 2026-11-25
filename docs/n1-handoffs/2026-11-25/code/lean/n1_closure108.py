"""One-off: assemble docs/n1-reviews/batch-108-closure from preserved reviewer artifacts."""
import gzip
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ART = pathlib.Path(r"C:\Users\stop-\n1-kanji-workspace\control\artifacts")
REPO = pathlib.Path(r"C:\Users\romanko\n1-kanji-workspace\learning-japanese")
OUT = REPO / "docs" / "n1-reviews" / "batch-108-closure"
CLOSURE = ART / "batch-108-revised-textual-closure-873" / "closure.json"
PACKET = ART / "batch-108-revised-common-packet-872"

RUNS = [
    ("initial-claude", "initial", "Claude", "batch-108-original-detached-review-68445241-9d37-47c1-b1d2-9db2aef39762", None),
    ("initial-gpt", "initial", "GPT", "batch-108-second-detached-review-edd6e0d7-022e-4948-a88b-8cbf81c24c14", None),
    ("initial-grok", "initial", "Grok", "batch-108-third-detached-review-4766beb0-a508-4cf9-a83f-2999baad25b9", None),
    ("confirm-gpt", "confirm", "GPT", "batch-108-revised-review-gpt-3f06c073-8e60-496f-a86a-ca614bd50bac", "initial-gpt"),
    ("confirm-claude", "confirm", "Claude", "batch-108-revised-review-claude-976dba79-3c27-4efb-9180-5fab053bd317", "initial-claude"),
    ("confirm-grok", "confirm", "Grok", "batch-108-revised-review-grok-b6cdc998-214d-41cd-a911-8ff675c2afc1", "initial-grok"),
]
TEACHING = ["kanji/勧.md", "kanji/告.md", "strokes/勧.json", "words/勧告.md", "words/勧める.md"]


def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=REPO, check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout.strip()


def git_bytes(*args):
    return subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=REPO, check=True,
                          capture_output=True).stdout


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def to_crlf(data):
    return data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")


def initial_packet_labels():
    """Raw-byte SHA-256 labels printed in the 19-part initial packet, keyed by repo-relative path."""
    text = "".join(gzip.decompress(p.read_bytes()).decode("utf-8")
                   for p in sorted((REPO / "docs/n1-reviews/batch-108-textual-862").glob("common-part-*.txt.gz")))
    labels = {}
    pattern = r"^SOURCE (?P<path>[^;\r\n]+?); complete original lines [\d-]+; SHA256 (?P<sha>[0-9a-f]{64})"
    for m in re.finditer(pattern, text, re.M):
        marker = "learning-japanese\\"
        if marker in m["path"]:
            labels[m["path"].split(marker, 1)[1].replace("\\", "/")] = m["sha"]
    return labels


def confirm_packet_labels():
    """Raw-byte SHA-256 labels printed in the 4-part confirmation packet, keyed by repo-relative path."""
    text = "".join((PACKET / f"common-part-0{i}.txt").read_text(encoding="utf-8") for i in range(1, 5))
    pattern = r"^SOURCE (?P<path>[^;\r\n]+); signed snapshot (?P<snap>[0-9a-f]{40}); actual raw SHA256 (?P<sha>[0-9a-f]{64})"
    return {m["path"]: m["sha"] for m in re.finditer(pattern, text, re.M)}


def main():
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    closure = load(CLOSURE)
    closure_by_family = {r["family"]: r for r in closure["reviewers"]}
    for sub in ("reports", "prompts", "scope-audits", "confirm-packet", "records"):
        (OUT / sub).mkdir(parents=True)

    prior_records = []
    for name, src in (
        ("third-family-completion-870.json", ART / "batch-108-third-family-completion-870" / "third-family-completion-and-disposition.json"),
        ("revised-textual-closure-873.json", CLOSURE),
    ):
        shutil.copyfile(src, OUT / "records" / name)
        prior_records.append({"path": f"records/{name}", "sha256": sha256(src), "bytes": src.stat().st_size})

    runs = []
    for key, phase, family, dirname, prior in RUNS:
        src = ART / dirname
        report = src / "report.md"
        shutil.copyfile(report, OUT / "reports" / f"{key}.md")
        shutil.copyfile(src / "prompt.txt", OUT / "prompts" / f"{key}.txt")
        shutil.copyfile(src / "read-scope-audit.json", OUT / "scope-audits" / f"{key}.json")
        report_sha = sha256(report)
        if phase == "confirm":
            expected = closure_by_family[family]["reportSha256"]
            assert report_sha == expected, (key, report_sha, expected)
            assert sha256(src / "own-prior-report.md") == sha256(ART / dict((k, d) for k, _, _, d, _ in RUNS)[prior] / "report.md"), key
        start = load(src / "start.json")
        exit_ = load(src / "exit.json")
        usage = load(src / "usage.json")
        models = sorted(usage["modelMetrics"])
        started = start.get("startedAt") or closure_by_family[family].get("startedAt")
        if phase == "confirm":
            started = closure_by_family[family]["startedAt"]
        completed = exit_["completedAt"] if phase == "initial" else closure_by_family[family]["exitedAt"]
        audit = load(src / "read-scope-audit.json")
        runs.append({
            "key": key,
            "phase": phase,
            "family": family,
            "session": exit_["reviewerSession"],
            "requestedModel": start.get("requestedModel"),
            "actualModels": models,
            "apiRequests": sum(m["requests"]["count"] for m in usage["modelMetrics"].values()),
            "totalApiDurationMs": usage.get("totalApiDurationMs"),
            "processStartedAt": started,
            "processExitedAt": completed,
            "exitCode": exit_["exitCode"],
            "snapshot": audit.get("snapshot") or start.get("snapshot") or start.get("frozenSnapshot"),
            "reportSha256": report_sha,
            "promptSha256": sha256(OUT / "prompts" / f"{key}.txt"),
            "scopeAuditSha256": sha256(OUT / "scope-audits" / f"{key}.json"),
        })

    runs_sorted = sorted(runs, key=lambda r: r["processStartedAt"])
    for a, b in zip(runs_sorted, runs_sorted[1:]):
        assert a["processExitedAt"] < b["processStartedAt"], (a["key"], b["key"])
    assert [r["key"] for r in runs_sorted] == [k for k, *_ in RUNS], "unexpected chronological order"
    assert all(r["exitCode"] == 0 for r in runs)

    packet_prov = load(PACKET / "provenance.json")
    packet_prov_sha = sha256(PACKET / "provenance.json")
    assert packet_prov_sha == closure["commonPacketSha256"], (packet_prov_sha, closure["commonPacketSha256"])
    parts = sorted(PACKET.glob("common-part-0*.txt"))
    assert len(parts) == 4 == len(packet_prov["parts"])
    packet = []
    for p, recorded in zip(parts, packet_prov["parts"]):
        data = p.read_bytes()
        assert pathlib.Path(recorded["path"]).name == p.name
        assert hashlib.sha256(data).hexdigest() == recorded["sha256"] and len(data) == recorded["bytes"], p.name
        with gzip.GzipFile(OUT / "confirm-packet" / f"{p.name}.gz", "wb", mtime=0) as fh:
            fh.write(data)
        packet.append({"part": p.name, "bytes": len(data), "sha256": recorded["sha256"]})
    shutil.copyfile(PACKET / "provenance.json", OUT / "confirm-packet" / "provenance.json")

    reviewed = git("rev-parse", "6547715c")
    head = git("rev-parse", "HEAD")
    blobs = []
    for path in TEACHING:
        at_reviewed = git("rev-parse", f"{reviewed}:{path}")
        at_head = git("rev-parse", f"HEAD:{path}")
        blobs.append({"path": path, "blobAtReviewedSnapshot": at_reviewed, "blobAtVerifiedHead": at_head,
                      "identical": at_reviewed == at_head})
    assert all(b["identical"] for b in blobs), blobs

    initial_labels = initial_packet_labels()
    confirm_labels = confirm_packet_labels()
    byte_forms = []
    for path in TEACHING:
        raw = git_bytes("show", f"HEAD:{path}")
        assert b"\r" not in raw, path
        crlf_sha = hashlib.sha256(to_crlf(raw)).hexdigest()
        initial_label = initial_labels.get(path)
        confirm_label = confirm_labels.get(path)
        if confirm_label is not None:
            assert confirm_label == crlf_sha, ("confirmation packet label", path)
        if initial_label is not None and path != "words/勧告.md":
            assert initial_label == crlf_sha, ("initial packet label", path)
        byte_forms.append({
            "path": path,
            "gitBlobLfSha256": hashlib.sha256(raw).hexdigest(),
            "crlfReconstructionSha256": crlf_sha,
            "initialPacketRawSha256": initial_label,
            "confirmationPacketRawSha256": confirm_label,
        })
    by_path = {b["path"]: b for b in byte_forms}
    assert by_path["words/勧告.md"]["initialPacketRawSha256"] != by_path["words/勧告.md"]["crlfReconstructionSha256"]
    assert by_path["words/勧告.md"]["confirmationPacketRawSha256"] == by_path["words/勧告.md"]["crlfReconstructionSha256"]

    provenance = {
        "schemaVersion": 1,
        "batch": "108",
        "members": ["勧"],
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "initialSnapshot": "9955ac122d1b4f1084f702d3d6d5afeb82d35e3a",
        "reviewedSnapshot": reviewed,
        "teachingVerifiedAtHead": head,
        "confirmationPacketProvenanceSha256": packet_prov_sha,
        "confirmationPacketProvenanceSha256MatchesClosureRecord": True,
        "confirmationPacketParts": packet,
        "runsInChronologicalOrder": runs_sorted,
        "serialNonOverlapping": True,
        "distinctModelFamilies": sorted({r["family"] for r in runs}),
        "teachingBlobs": blobs,
        "teachingByteForms": byte_forms,
        "priorRunnerRecords": prior_records,
    }
    (OUT / "provenance.json").write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("ok", OUT)
    for r in runs_sorted:
        print(f'{r["key"]:15} {r["actualModels"]} {r["processStartedAt"][11:19]}-{r["processExitedAt"][11:19]} api={r["apiRequests"]} snapshot={str(r["snapshot"])[:8]}')
    print("packet provenance sha == closure record:", packet_prov_sha == closure["commonPacketSha256"])
    print("reviewed", reviewed[:8], "head", head[:8])


main()
