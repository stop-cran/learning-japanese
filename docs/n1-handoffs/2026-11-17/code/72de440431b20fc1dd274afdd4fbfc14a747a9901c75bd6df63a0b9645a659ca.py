"""Independently recheck projected-successor-011 against the verified 008 packet and core."""
import json
import sys
from pathlib import Path

from b134_token_meter import verify_core
from common import WS, freeze_json, frozen, json_bytes, load_module, require, sha, start_guard

ROOT = WS / "scratch-134" / "review"
PRED = ROOT / "fresh-independent-002" / "projected-successor-008"
SUCC = ROOT / "fresh-independent-002" / "projected-successor-011"
PRED_PACKET_SHA = "6f774ec7906cbe8279e972959507d8ccbbea8541273f8cfa51a405dc34fcc5f6"
PRED_CORE_SHA = "b6e49cbbcb6ebab5886dc87b9cf9557a4b213fda5d3c3b0c7c6ff3f7c18c76b8"
PRED_VERIFICATION = (ROOT / "fresh-core-verification-001" / "verification.json",
                     "da0eb528677c1c8529c11ada2b69c310f715d829f2e8fd59cfd2e4fa6113cb30")
CODEC_INDEX = (ROOT / "continuation-tools-004" / "index.json",
               "274bedd21e6d2fa754b90f9cd350dbacb651f52ebe6e283434420d7e15f977b8")
GUIDE = "evidence/lossless-core-representation-guide.md"
XML = {"evidence/jmdict-families.xml": "evidence/jmdict-families.compact-xml-v1.txt",
       "evidence/kanjidic2-review-projection.xml": "evidence/kanjidic2-review-projection.compact-xml-v1.txt"}


def main(output, packet_sha, core_sha):
    require(output.parent == ROOT and not output.exists(), "Use a new direct review output")
    guard, _ = start_guard("B134 successor-011 independent verification")
    try:
        prior = json.loads(frozen(*PRED_VERIFICATION))
        require(prior["status"].startswith("PASS") and prior["packetSha256"] == PRED_PACKET_SHA
                and prior["coreManifestSha256"] == PRED_CORE_SHA, "Predecessor verification does not bind 008")
        old_sums = json.loads(frozen(PRED / "packet" / "SHA256SUMS.json", PRED_PACKET_SHA))
        sums = json.loads(frozen(SUCC / "packet" / "SHA256SUMS.json", packet_sha))
        on_disk = {p.relative_to(SUCC / "packet").as_posix() for p in (SUCC / "packet").rglob("*") if p.is_file()}
        require(on_disk == set(sums) | {"SHA256SUMS.json"}, "Successor packet has unlisted or missing files")
        files = {}
        for name, digest in sums.items():
            files[name] = frozen(SUCC / "packet" / name, digest)
            guard.check()
        for name, digest in old_sums.items():
            require(sums.get(name) == digest and files[name] == frozen(PRED / "packet" / name, digest),
                    "Predecessor packet file not retained byte-exactly: " + name)
            guard.check()
        old_core = json.loads(frozen(PRED / "fresh-independent-core-001.json", PRED_CORE_SHA))
        old_names = [row["source"] for row in old_core["sources"]]
        codec_index = json.loads(frozen(*CODEC_INDEX))
        codec_raw = files["codec/compact_xml_v1.py"]
        require(sha(codec_raw) == codec_index["files"]["compact_xml_v1.py"]["sha256"],
                "Packet decoder is not the frozen tested codec")
        codec = load_module("packet_compact_xml_v1", SUCC / "packet" / "codec" / "compact_xml_v1.py")
        mapping, checks = {}, {}
        for old in old_names:
            if old in XML:
                new = XML[old]
                require(codec.decode(files[new]) == files[old], "Encoded XML does not decode exactly: " + old)
                kind = "compact-xml-v1"
            elif old.endswith(".json") and json_bytes(json.loads(files[old])) == files[old]:
                new = old[:-5] + ".min.json"
                value = json.loads(files[new])
                require(json_bytes(value) == files[old] and files[new] ==
                        (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8"),
                        "Minified JSON is not the exact canonical inverse: " + old)
                kind = "minified-canonical-json"
            else:
                continue
            mapping[old] = new
            checks[old] = {"converted": new, "representation": kind,
                           "originalSha256": sha(files[old]), "convertedSha256": sha(files[new])}
        expected_new = set(mapping.values()) | {GUIDE, "codec/compact_xml_v1.py"}
        require(set(sums) - set(old_sums) == expected_new and len(mapping) == 44,
                "Successor added files other than the declared lossless representations")
        expected_names = []
        for old in old_names:
            expected_names.append(mapping.get(old, old))
            if old == "REVIEW.md":
                expected_names.append(GUIDE)
        core = json.loads(frozen(SUCC / "fresh-independent-core-001.json", core_sha))
        require([row["source"] for row in core["sources"]] == expected_names,
                "Successor core is not the predecessor core with exactly the declared substitutions")
        sources = {name: files[name] for name in expected_names}
        chain_bytes = verify_core(core, sources, frozen)
        require(all(row["bytes"] < 16000 for row in core["segments"]), "Segment exceeds the meter bound")
        guide = files[GUIDE].decode("utf-8")
        example_line, example_xml = [line.strip("`") for line in guide.rstrip("\n").split("\n")
                                     if line.startswith("`")][-2:]
        encoded_lines = files[XML["evidence/jmdict-families.xml"]].decode("utf-8").split("\n")
        xml_lines = files["evidence/jmdict-families.xml"].decode("utf-8").split("\n")
        position = encoded_lines.index("%end") + 1
        record = encoded_lines.index(example_line) - position
        require(record >= 0 and xml_lines[record + 1] == example_xml,
                "Guide example is not a verbatim real record pair")
        result = {
            "status": "PASS_LOSSLESS_SUCCESSOR_RETAINS_VERIFIED_PACKET_AND_EXACTLY_INVERTS",
            "predecessorVerification": {"path": str(PRED_VERIFICATION[0]), "sha256": PRED_VERIFICATION[1]},
            "packetSha256": packet_sha, "coreManifestSha256": core_sha, "packetFiles": len(sums),
            "retainedPredecessorFiles": len(old_sums), "conversions": checks,
            "coreSources": len(sources), "segments": len(core["segments"]), "chainBytes": chain_bytes,
            "payloadBytes": sum(map(len, sources.values())),
            "guideExampleRecord": record + 1,
            "producerSha256": sha(Path(__file__).read_bytes()),
            "limits": "Mechanical lossless-representation and source-retention check only; inherits 008's signed "
                      "article/baseline/source-union verification by byte identity. No token measurement, "
                      "semantic review, reviewer admission, publication or delivery credit.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Successor verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output / "verification.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "verify_b134_successor_011.py NEW_OUTPUT_DIRECTORY PACKET_SHA CORE_SHA")
    main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3])
