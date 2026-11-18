import copy
import unittest

import record_b134_publication as recorder
from b134_closure_progress import validate_archived_resolution
from common import json_bytes, sha
from test_b134_closure_progress import progress_fixture
from test_b134_review_history import REVIEWED


class PublicationControls(unittest.TestCase):
    def test_gate_receipts_bind_current_snapshot_and_closure(self):
        commit, manifest_sha, closure_sha = "a" * 40, "b" * 64, "c" * 64
        value = {
            "batch": 134, "status": "PASS", "base": recorder.BASE,
            "initialSnapshot": recorder.CANDIDATE, "reviewedSnapshot": REVIEWED,
            "manifestReproducible": True, "manifestSha256": manifest_sha,
            "closureProvenanceSha256": closure_sha, "closureFiles": 13,
            "checks": recorder.ORDER, "logs": {name: {} for name in recorder.ORDER},
        }
        for mode, head in (("closure", REVIEWED), ("committed", commit)):
            good = {**value, "mode": mode, "head": head}
            recorder.validate_gate(good, mode, REVIEWED, commit, manifest_sha, closure_sha, 13)
            for key, bad in (
                ("head", "d" * 40), ("mode", "author"), ("checks", recorder.ORDER[::-1]),
                ("manifestReproducible", False), ("closureFiles", 12),
                ("manifestSha256", "d" * 64), ("closureProvenanceSha256", "d" * 64),
                ("logs", {}), ("reviewedSnapshot", recorder.CANDIDATE),
            ):
                with self.subTest(mode=mode, key=key), self.assertRaises(ValueError):
                    recorder.validate_gate({**good, key: bad}, mode, REVIEWED, commit,
                                           manifest_sha, closure_sha, 13)

    def test_publication_requires_bound_complete_resolution_not_just_clean_reviews(self):
        _, closure, _, resolution, claims = progress_fixture()
        raw = json_bytes(resolution)
        ref = {"path": "resolution.json", "sha256": sha(raw)}
        closure["resolution"] = ref
        closure["recordedFileSha256"][ref["path"]] = ref["sha256"]
        validate_archived_resolution(closure, lambda path, digest: raw, claims)
        with self.assertRaises(ValueError):
            validate_archived_resolution(closure, lambda path, digest: raw + b" ", claims)
        missing = copy.deepcopy(resolution)
        missing["dispositions"].pop()
        missing_raw = json_bytes(missing)
        altered = copy.deepcopy(closure)
        altered["resolution"]["sha256"] = sha(missing_raw)
        altered["recordedFileSha256"][ref["path"]] = sha(missing_raw)
        with self.assertRaises(ValueError):
            validate_archived_resolution(altered, lambda path, digest: missing_raw, claims)
        altered = copy.deepcopy(closure)
        altered["resolution"]["path"] = "../resolution.json"
        altered["recordedFileSha256"]["../resolution.json"] = ref["sha256"]
        with self.assertRaises(ValueError):
            validate_archived_resolution(altered, lambda path, digest: raw, claims)


if __name__ == "__main__":
    unittest.main()
