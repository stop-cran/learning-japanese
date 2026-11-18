"""Verify published B127 chain bytes and explicit local-only source retention."""
import gzip
import io
import json
import sys
from pathlib import Path

from archive_b124_chains_v2 import is_local_only_source
from common import freeze_json, frozen, load_batch, require, sha, start_guard


def verify_chain(files, binding):
    manifest_raw = files["manifest.json"]
    require(sha(manifest_raw) == binding["manifestSha256"], "Chain manifest binding differs")
    manifest = json.loads(manifest_raw)
    retention_raw = files["retention.json"]
    require(sha(retention_raw) == binding["retentionSha256"], "Retention binding differs")
    retention = json.loads(retention_raw)
    segments = manifest["segments"]
    require(len({row["index"] for row in segments}) == len(segments), "Duplicate segment index")
    archived, local = [], []
    expected_files = {"manifest.json", "retention.json"}
    for segment in segments:
        protected = [
            part for part in segment["parts"]
            if is_local_only_source(part["source"])
        ]
        if protected:
            local.append({
                "index": segment["index"], "sha256": segment["sha256"],
                "bytes": segment["bytes"],
                "sources": [
                    {"source": part["source"], "sha256": part["sha256"],
                     "firstLine": part["a"], "lastLine": part["b"]}
                    for part in protected
                ],
            })
            continue
        name = Path(segment["path"]).name + ".gz"
        require(name not in expected_files, "Duplicate archive name")
        expected_files.add(name)
        require(name in files, "Published segment is missing")
        with gzip.GzipFile(fileobj=io.BytesIO(files[name])) as stream:
            raw = stream.read(segment["bytes"] + 1)
        require(len(raw) == segment["bytes"] and sha(raw) == segment["sha256"],
                "Published segment differs from reviewed bytes")
        archived.append(segment["index"])
    require(set(files) == expected_files, "Unexpected archive file or local-only segment published")
    require(retention["schemaVersion"] == 1
            and retention["originalManifestSha256"] == sha(manifest_raw)
            and retention["originalSegments"] == binding["segments"] == len(segments)
            and retention["archivedSegmentIndices"] == binding["archivedSegmentIndices"] == archived
            and retention["localOnlySegments"] == local
            and binding["localOnlySegmentIndices"] == [row["index"] for row in local],
            "Retention inventory does not match reviewed sources")
    return {"originalSegments": len(segments), "archivedSegments": len(archived),
            "localOnlySegments": len(local), "manifestSha256": sha(manifest_raw)}


def main(output):
    config = load_batch(127)
    root = Path(config["repo"]) / "docs" / "n1-reviews" / "batch-127-closure"
    provenance_raw = frozen(root / "provenance.json")
    provenance = json.loads(provenance_raw)
    require(provenance["batch"] == 127 and provenance["initialSnapshot"] == config["candidate"]
            and provenance["base"] == config["base"] and provenance["members"] == config["members"],
            "Closure belongs to another batch or initial snapshot")
    guard, _ = start_guard("B127 archived-chain verification")
    try:
        for path, digest in provenance["recordedFileSha256"].items():
            frozen(root / path, digest)
            guard.check()
        results = []
        for review in provenance["reviewLineage"]:
            for chain in review["chains"]:
                directory = root / chain["path"]
                files = {
                    path.relative_to(directory).as_posix(): frozen(path)
                    for path in directory.rglob("*") if path.is_file()
                }
                results.append({"run": review["run"], "path": chain["path"],
                                **verify_chain(files, chain)})
                guard.check()
        require(results, "Closure has no review chains")
        freeze_json(output, {
            "batch": 127, "status": "PASS", "candidate": provenance["reviewedSnapshot"],
            "provenanceSha256": sha(provenance_raw), "chains": results,
            "limits": "Verifies the actual closure files and known external-snapshot labels. "
                      "Other complete-capture labels require separate inspection. "
                      "This is not review acceptance, signature verification or publication.",
        })
    finally:
        require(not guard.finish()["breach"], "Archive verification RAM guard breached")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
