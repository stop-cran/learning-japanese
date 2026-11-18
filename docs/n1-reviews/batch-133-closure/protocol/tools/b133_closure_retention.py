"""Keep overlapping chain payloads local without altering reviews or relaxing leak checks."""
import gzip
import json
from pathlib import Path

from close_b132 import publication_findings
from common import json_bytes, require, sha


def retain_overlapping_chains(files, windows, allowed, guard, retentions):
    uuids, leaks = publication_findings(files, windows, allowed, guard)
    require(not uuids, "Unknown identity must be investigated, not filtered")
    adjustments = []
    for finding in leaks:
        name = finding["file"]
        parts = name.split("/")
        require(len(parts) == 3 and parts[0] == "chains" and name.endswith(".txt.gz"),
                "Protected text outside a chain payload requires separate investigation")
        label = parts[1]
        prefix = "chains/" + label + "/"
        manifest = json.loads(files[prefix + "manifest.json"])
        rows = [row for row in manifest["segments"]
                if Path(row["path"]).name + ".gz" == parts[2]]
        require(len(rows) == 1, "Overlapping payload lacks a unique original chain binding")
        row = rows[0]
        raw = gzip.decompress(files[name])
        require(sha(raw) == row["sha256"], "Overlapping payload changed from reviewed bytes")
        retention = retentions[label]
        require(row["index"] in retention["archivedSegmentIndices"]
                and all(item["index"] != row["index"] for item in retention["localOnlySegments"]),
                "Duplicate or inconsistent retention decision")
        original_name = prefix + "retention-before-overlap-check.json"
        if original_name not in files:
            files[original_name] = files[prefix + "retention.json"]
        retention["archivedSegmentIndices"].remove(row["index"])
        retention["localOnlySegments"].append({
            "index": row["index"], "sha256": row["sha256"], "bytes": len(raw),
            "sources": [{"source": part["source"], "sha256": part["sha256"],
                         "firstLine": part["a"], "lastLine": part["b"]} for part in row["parts"]],
            "reason": "Protected external-source text overlap; entire unchanged payload retained locally.",
        })
        retention["localOnlySegments"].sort(key=lambda item: item["index"])
        retention["policy"] = (
            "Complete external extracts and any additional segment with protected external-text overlap "
            "remain local in full, including co-located material. Original manifest, sources, ranges and "
            "hashes remain unchanged. No reviewer input or report is rewritten. This archive is partial."
        )
        files[prefix + "retention.json"] = json_bytes(retention)
        del files[name]
        adjustments.append({"file": name, "index": row["index"], "sha256": row["sha256"],
                            "protectedWindows": finding["windows"]})
    return adjustments
