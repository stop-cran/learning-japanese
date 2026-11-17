import copy
import gzip
import json
import unittest

from close_b134 import require_fresh_inventory, retained_chain, verify_audited_chain
from common import json_bytes, sha


def chain_fixture():
    paths = [r"C:\review\one.txt", r"C:\review\two.txt"]
    data = {paths[0]: b"native extract and colocated public data\n", paths[1]: b"public data\n"}
    rows = [{
        "index": i, "path": path, "sha256": sha(data[path]), "bytes": len(data[path]),
        "parts": [{"source": source, "sha256": sha(data[path]), "a": 1, "b": 1}],
    } for i, (path, source) in enumerate(zip(paths, (
        "reconciliation/evidence/native-example-extract.txt", "snapshot/kanji/example.md")), 1)]
    return {"segments": rows}, data


class FinalClosureControls(unittest.TestCase):
    def test_native_reconciliation_segment_remains_local_with_original_manifest(self):
        manifest, data = chain_fixture()
        before = copy.deepcopy((manifest, data))
        raw = json_bytes(manifest)
        files, retention = retained_chain(raw, data)
        self.assertEqual((manifest, data), before)
        self.assertEqual(files["manifest.json"], raw)
        self.assertNotIn("one.txt.gz", files)
        self.assertEqual(gzip.decompress(files["two.txt.gz"]), data[r"C:\review\two.txt"])
        self.assertEqual(retention["archivedSegmentIndices"], [2])
        self.assertEqual([row["index"] for row in retention["localOnlySegments"]], [1])
        self.assertEqual(json.loads(files["retention.json"]), retention)
        data[r"C:\review\two.txt"] = b"changed\n"
        with self.assertRaises(ValueError):
            retained_chain(raw, data)

    def test_report_only_optional_claim_cannot_disappear_from_resolution(self):
        report = b"### F1: Finding\n### O1: Optional point\n"
        claims = {"acceptedFindings": ["F1"], "openClaimIds": [], "coordinatorClaimIds": []}
        with self.assertRaises(ValueError):
            require_fresh_inventory(report, claims)
        claims["coordinatorClaimIds"] = ["O1"]
        require_fresh_inventory(report, claims)

    def test_equal_counts_cannot_substitute_other_chain_reads(self):
        manifest, data = chain_fixture()
        audit = {"calls": [
            {"id": str(i), "role": f"extension-{i}", "path": row["path"], "success": True}
            for i, row in enumerate(manifest["segments"], 1)]}
        events = [{
            "type": "tool.execution_complete",
            "data": {"toolCallId": str(i), "success": True,
                     "result": {"content": data[row["path"]].decode("utf-8")}},
        } for i, row in enumerate(manifest["segments"], 1)]
        verify_audited_chain(manifest, audit, events, "extension")
        mutations = (
            lambda m, a, e: m["segments"][0].update(path=r"C:\review\unread.txt"),
            lambda m, a, e: a["calls"].reverse(),
            lambda m, a, e: e[0]["data"]["result"].update(content="changed"),
            lambda m, a, e: e.append(copy.deepcopy(e[0])),
            lambda m, a, e: e[0]["data"].update(success=False),
            lambda m, a, e: m["segments"].pop(),
        )
        for index, mutate in enumerate(mutations):
            changed = copy.deepcopy((manifest, audit, events))
            mutate(*changed)
            with self.subTest(index=index), self.assertRaises(ValueError):
                verify_audited_chain(*changed, "extension")


if __name__ == "__main__":
    unittest.main()
