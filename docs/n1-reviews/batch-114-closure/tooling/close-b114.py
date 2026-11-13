"""Preserve accepted B114 review evidence without raw conversation payloads."""
import argparse
import gzip
import hashlib
import json
import stat
import subprocess
from pathlib import Path

BASE = Path(r"C:\Users\stop-\n1-kanji-workspace")
REPO = BASE / "rollout-recovered" / "learning-japanese"
SCRATCH = BASE / "scratch-114"
OUT = REPO / "docs" / "n1-reviews" / "batch-114-closure"
FREEZE = "8c2bdc27e5d556e639a4d0e9239ae5f2009c400f"
FIRST_FIX = "ac38b8e4427afc2c10a957871c5ec99e9cb92bda"
FIX = "1c2b2c6a6658fa968f724657868ccae1eb61b198"
SESSIONS = {
    "claude": "98c7bbce-f756-4954-8263-66f20c421c8c",
    "gpt": "c4b8c183-4098-4614-ad40-537b1d9dccad",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(REPO), *args])


def frozen(path, expected=None):
    assert not path.stat().st_mode & stat.S_IWRITE, f"Writable input: {path}"
    data = path.read_bytes()
    assert expected is None or sha(data) == expected, f"Hash mismatch: {path}"
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claude-adjudication", type=Path, required=True)
    parser.add_argument("--gpt-adjudication", type=Path, required=True)
    args = parser.parse_args()
    assert git("rev-parse", "HEAD").decode().strip() == FIX
    assert not OUT.exists(), "Refusing to overwrite closure evidence"
    inputs = {}
    runs = []
    for family in SESSIONS:
        for phase in ("initial", "confirm", "delta"):
            run = f"{phase}-{family}"
            if phase == "initial":
                adj_path = SCRATCH / f"N1-B114-{family.upper()}-001-final-adjudication.json"
                audit_base = SCRATCH
                prompt_dir = SCRATCH / "prompts-114"
                prompt_name = f"initial-{family}-114-001.txt"
            elif phase == "confirm":
                adj_path = SCRATCH / "confirm" / f"N1-B114-{family.upper()}-CONFIRM-001-final-adjudication.json"
                audit_base = SCRATCH / "confirm"
                prompt_dir = audit_base / "prompts"
                prompt_name = f"confirm-{family}-114-001.txt"
            else:
                adj_path = getattr(args, f"{family}_adjudication")
                audit_base = SCRATCH / "confirm"
                prompt_dir = SCRATCH / "delta"
                prompt_name = f"instructions-{family}.txt"
            adj_bytes = frozen(adj_path)
            adj = json.loads(adj_bytes)
            assert adj["status"] == "ACCEPTED_AS_REVIEW_EVIDENCE"
            audit_path = audit_base / adj["finalAudit"]
            audit_bytes = frozen(audit_path, adj["finalAuditSha256"])
            audit = json.loads(audit_bytes)
            assert audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
            assert not audit["breaches"] and audit["readbackVerified"]
            assert audit["reviewerIdle"] and not audit["recordIncomplete"]
            report = frozen(BASE / "reports-114" / f"{run}.md", adj["reportSha256"])
            inputs[f"reports/{run}.md"] = report
            inputs[f"adjudications/{run}.json"] = adj_bytes
            if adj.get("continuationAdjudication"):
                inputs["adjudications/initial-gpt-continuations.json"] = frozen(
                    SCRATCH / adj["continuationAdjudication"])
            inputs[f"prompts/{run}.txt"] = frozen(prompt_dir / prompt_name)
            kickoff_name = f"kickoff-{family}.txt" if phase == "delta" else f"kickoff-{family}-114-001.txt"
            inputs[f"prompts/{run}-kickoff.txt"] = frozen(prompt_dir / kickoff_name)
            # Audit reports contain bounded tool metadata, never raw tool results or hidden reasoning.
            public_audit = {k: v for k, v in audit.items() if k not in ("calls", "modelRecords", "eventsSource")}
            public_audit["calls"] = [
                {k: v for k, v in call.items() if k != "arguments"} for call in audit["calls"]
            ]
            inputs[f"audits/{run}.json"] = (
                json.dumps(public_audit, ensure_ascii=False, indent=2) + "\n"
            ).encode("utf-8")
            calls = audit["calls"]
            runs.append({
                "id": run, "session": SESSIONS[family],
                "snapshot": FREEZE if phase == "initial" else FIRST_FIX if phase == "confirm" else FIX,
                "actualModels": audit["actualResponseModels"],
                "reportSha256": sha(report), "nativeAuditSha256": sha(audit_bytes),
                "eventsSha256": audit["eventsSha256"],
                "firstToolUtc": calls[0]["timestamp"], "lastToolUtc": calls[-1]["timestamp"],
                "toolCalls": len(calls), "fetches": audit["fetches"],
                "coverage": ({k: audit[k] for k in ("coreRead", "coreRequired", "extensionRead", "extensionRequired")}
                             if phase == "initial" else
                             {k: audit[k] for k in ("chainRead", "chainRequired")}),
                "confirmationVerdict": adj.get("confirmationVerdict"),
            })

    packet = BASE / "review-packets" / "batch-114-8c2bdc27"
    sums_raw = frozen(packet / "SHA256SUMS.json",
                      "eb6b1042060f561cd6ff49054d0e11533c15008ea0f6bbc064b07614b1701e15")
    inputs["packet/SHA256SUMS.json"] = sums_raw
    for rel, expected in json.loads(sums_raw).items():
        data = frozen(packet / rel, expected)
        if not rel.startswith("repo/") and not rel.lower().endswith(".pdf"):
            inputs["packet/" + rel] = data

    snapshot_checks = {}
    for family in SESSIONS:
        packet = BASE / "review-packets" / f"confirm-114-ac38b8e4-{family}"
        raw = frozen(packet / "packet-manifest.json")
        manifest = json.loads(raw)
        assert manifest["candidate"] == FIRST_FIX and manifest["freeze"] == FREEZE
        inputs[f"confirm-packet/{family}/packet-manifest.json"] = raw
        for rel, info in manifest["files"].items():
            data = frozen(packet / rel, info["sha256"])
            if rel.startswith("snapshot/"):
                target = rel.removeprefix("snapshot/")
                blob = git("show", FIRST_FIX + ":" + target)
                assert data.replace(b"\r\n", b"\n") == blob
                snapshot_checks[FIRST_FIX + ":" + target] = {
                    "packetSha256": sha(data), "gitSha256": sha(blob),
                    "rawByteEqual": data == blob, "CRLFToLFEqualsGit": True,
                }
            else:
                inputs[f"confirm-packet/{family}/{rel}"] = data

    chains = {
        "initial": SCRATCH / "core-chain.json",
        "initial-claude-extension": SCRATCH / "N1-B114-CLAUDE-001-extension.json",
        "initial-gpt-extension": SCRATCH / "N1-B114-GPT-001-extension.json",
        "confirm-claude": SCRATCH / "confirm" / "claude-chain.json",
        "confirm-gpt": SCRATCH / "confirm" / "gpt-chain.json",
        "delta-claude": SCRATCH / "delta" / "claude-chain.json",
        "delta-gpt": SCRATCH / "delta" / "gpt-chain.json",
    }
    for label, path in chains.items():
        raw = frozen(path)
        inputs[f"chains/{label}/manifest.json"] = raw
        for segment in json.loads(raw)["segments"]:
            source = Path(segment["path"])
            inputs[f"chains/{label}/{source.name}"] = frozen(source, segment["sha256"])
    for name in ("review_chain.py", "audit-review.py", "test-review-chain.py",
                 "test-review-audit.py", "prepare-chain.py", "test-prepare-extension.py",
                 "filter-continuations-v2.py", "test-filter-continuations-v2.py"):
        inputs[f"tooling/{name}"] = frozen(SCRATCH / name)
    for name in ("audit-confirm.py", "test-audit-confirm.py", "prepare-confirm-chain.py",
                 "verify-confirm-chain.py", "build-confirm-prompts.py",
                 "predelivery-claude-001.json", "predelivery-gpt-001.json"):
        inputs[f"tooling/confirm/{name}"] = frozen(SCRATCH / "confirm" / name)
    for name in ("build-prompts-114.py",):
        inputs[f"tooling/{name}"] = frozen(SCRATCH / name)
    for directory in ("checks-final", "checks-delta", "checks-delta-final"):
        for path in (SCRATCH / directory).iterdir():
            assert path.is_file(), path
            inputs[f"gates/{directory}/{path.name}"] = frozen(path)
    for path in (SCRATCH / "delta").rglob("*"):
        if path.is_file():
            inputs["delta-packet/" + path.relative_to(SCRATCH / "delta").as_posix()] = frozen(path)
    for name in ("verify-b114-scope.py", "close-b114.py", "prepare-b114-delta.py", "bind-b114-delta.py",
                 "record-b114-closure.py"):
        inputs[f"tooling/{name}"] = Path(__file__).with_name(name).read_bytes()
    for path in ("source-inspection.json", "design.json", "authoring-inventory.json"):
        inputs[f"author-evidence/{path}"] = (SCRATCH / path).read_bytes()

    OUT.mkdir(parents=True)
    (OUT / ".gitattributes").write_text("* -text\nREADME.md text eol=lf\n", encoding="ascii")
    stored = {}
    for rel, data in inputs.items():
        compressed = rel.endswith(".xml") or rel.startswith("chains/") and rel.endswith(".txt")
        target = OUT / (rel + ".gz" if compressed else rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        output = gzip.compress(data, mtime=0) if compressed else data
        with target.open("xb") as stream:
            stream.write(output)
        stored[target.relative_to(OUT).as_posix()] = {
            "sha256": sha(output), "bytes": len(output),
            "uncompressedSha256": sha(data), "uncompressedBytes": len(data),
        }
    provenance = {
        "batch": 114, "initialSnapshot": FREEZE, "firstFix": FIRST_FIX, "reviewedSnapshot": FIX,
        "runs": runs, "files": stored, "snapshotByteChecks": snapshot_checks,
        "rawExecutionRecords": "Retained locally; only hashes and bounded audit metadata are published.",
        "byteNote": "Reports/prompts retain original bytes. Snapshot CRLF bytes are not called equal to LF Git blobs.",
        "quarantine": "No B113 void record, finding, observation or hint is used or copied.",
    }
    (OUT / "provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"storedFiles": len(stored), "snapshotChecks": len(snapshot_checks), "runs": runs}, indent=2))


if __name__ == "__main__":
    main()
