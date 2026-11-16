"""Prepare publication copies without redistributing complete external source extracts."""
import gzip
import json
from pathlib import Path

from common import json_bytes, require, sha


def is_local_only_source(source):
    source = source.removeprefix("original-packet/")
    return (source.startswith("evidence/external-snapshots/")
            and source != "evidence/external-snapshots/manifest.json")


def prepare(manifest_raw, segment_bytes):
    manifest = json.loads(manifest_raw)
    segments = manifest["segments"]
    require(set(segment_bytes) == {s["path"] for s in segments}, "Chain segment set differs")
    files = {"manifest.json": manifest_raw}
    archived, local_only = [], []
    for segment in segments:
        raw = segment_bytes[segment["path"]]
        require(sha(raw) == segment["sha256"], "Original chain segment hash differs")
        protected = [
            part for part in segment["parts"]
            if is_local_only_source(part["source"])
        ]
        if protected:
            local_only.append({
                "index": segment["index"],
                "sha256": segment["sha256"],
                "bytes": len(raw),
                "sources": [
                    {"source": p["source"], "sha256": p["sha256"],
                     "firstLine": p["a"], "lastLine": p["b"]}
                    for p in protected
                ],
            })
            continue
        name = Path(segment["path"]).name + ".gz"
        require(name not in files, "Duplicate archive segment name")
        packed = gzip.compress(raw, mtime=0)
        require(gzip.decompress(packed) == raw, "Chain compression differs")
        files[name] = packed
        archived.append(segment["index"])
    retention = {
        "schemaVersion": 1,
        "originalManifestSha256": sha(manifest_raw),
        "originalSegments": len(segments),
        "archivedSegmentIndices": archived,
        "localOnlySegments": local_only,
        "policy": "Segments containing complete external source extracts remain local in full, "
                  "including any other material sharing those segments. The original manifest, "
                  "source ranges and hashes are retained without altering review inputs. "
                  "This publication archive is not a complete copy of the local read chains.",
    }
    files["retention.json"] = json_bytes(retention)
    return files, retention
