"""Independently re-verify a frozen confirmation chain against its on-disk sources."""
import hashlib
import json
import re
import stat
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
ROOTS = {"confirm-packet": None, "initial-report": WORKSPACE / "reports-114",
         "original-packet": WORKSPACE / "review-packets" / "batch-114-8c2bdc27"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(family):
    manifest_path = Path(__file__).resolve().parent / f"{family}-chain.json"
    preflight = json.loads((manifest_path.parent / f"{family}-chain-preflight.json").read_bytes())
    assert sha(manifest_path.read_bytes()) == preflight["chainManifestSha256"]
    roots = dict(ROOTS, **{"confirm-packet": Path(preflight["packet"])})
    manifest = json.loads(manifest_path.read_bytes())
    segments = manifest["segments"]
    directory = Path(segments[0]["path"]).parent
    assert sorted(p.name for p in directory.iterdir()) == sorted(Path(s["path"]).name for s in segments)
    rebuilt = {}
    for index, segment in enumerate(segments):
        path = Path(segment["path"])
        assert not path.stat().st_mode & stat.S_IWRITE, path
        body = path.read_bytes()
        assert sha(body) == segment["sha256"] and len(body) == segment["bytes"] < 16000, path
        lines = [line + b"\n" for line in body.split(b"\n")[:-1]]
        tail = lines[-1].decode("utf-8")
        if index + 1 < len(segments):
            assert tail == f"NEXT SEGMENT: {segments[index + 1]['path']}\n", path
        else:
            assert tail.startswith("END OF CHAIN."), path
        headers = [i for i, line in enumerate(lines) if line.startswith(b"SOURCE: ")]
        assert len(headers) == len(segment["parts"]), path
        for header, part in zip(headers, segment["parts"]):
            match = re.fullmatch(r"SOURCE LINES (\d+)-(\d+) = SEGMENT LINES (\d+)-(\d+)\n",
                                 lines[header + 2].decode("utf-8"))
            a, b, first, last = map(int, match.groups())
            assert (a, b, first, last) == (part["a"], part["b"], part["segmentStart"], part["segmentEnd"])
            assert lines[header] == f"SOURCE: {part['source']}\n".encode("utf-8")
            assert lines[last] == b"END SOURCE\n"
            chunk = rebuilt.setdefault(part["source"], [])
            assert (chunk[-1][1] + 1 if chunk else 1) == a, part["source"]
            chunk.append((a, b, b"".join(lines[first - 1:last])))
    sources = manifest["sources"]
    assert [s["source"] for s in sources] == list(rebuilt)
    for record in sources:
        prefix, relative = record["source"].split("/", 1)
        data = (roots[prefix] / relative).read_bytes()
        assert sha(data) == record["sha256"], relative
        expected = b"".join(data.splitlines(keepends=True)[:record["selectedLines"]])
        joined = b"".join(c[2] for c in rebuilt[record["source"]])
        assert joined == expected and rebuilt[record["source"]][-1][1] == record["selectedLines"], relative
        if record["selectedLines"] != record["sourceLines"]:
            print(f"partial: {record['source']} {record['selectedLines']}/{record['sourceLines']}")
    print(f"{family}: {len(segments)} segments, {len(sources)} sources reassemble exactly; "
          f"max segment {max(s['bytes'] for s in segments)} B")


if __name__ == "__main__":
    main(sys.argv[1])
