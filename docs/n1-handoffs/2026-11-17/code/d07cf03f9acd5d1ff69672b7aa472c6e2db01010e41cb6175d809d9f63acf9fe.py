import copy
import unittest

import build_b134_resolution as builder
from b134_initial_records import INITIALS, actual_initial, disposition_ids
from b134_review_history import REVIEW_REFS, validate_resolution
from close_b134 import REVIEWED, history
from common import frozen, sha


def originals():
    index, evidence, inventory, protected, raws = builder.fixed_inputs()
    original, lineage = builder.original_dispositions(index, inventory, raws)
    return index, evidence, inventory, protected, original, lineage


def scenario():
    index, _, inventory, _, original, lineage = originals()
    inventory, entries, adjudications, fresh = dict(inventory), [], {}, []
    for number, (family, known) in enumerate(INITIALS.items(), 1):
        run = "N1-B134-" + family.upper() + "-FRESH-002"
        entry = {
            "run": run, "role": "replacement-independent", "family": family,
            "session": f"{number:08d}-aaaa-bbbb-cccc-dddddddddddd", "snapshot": REVIEWED,
            "verdict": "UNVERIFIED", "reviewAccepted": True, "originalSession": known["session"],
            "replacesInitialRun": "N1-B134-" + family.upper() + "-001",
            "originalReviewerConfirmation": False,
            "acceptedFindings": [], "openClaimIds": ["D1"], "coordinatorClaimIds": ["C1"],
        }
        for field in REVIEW_REFS:
            path = "reviews/" + run + "/" + field + (".md" if field == "report" else ".json")
            inventory[path] = sha(path.encode())
            entry[field] = {"path": path, "sha256": inventory[path]}
        adjudications[run] = entry["adjudication"]
        entries.append(entry)
        fresh.extend({"run": run, "id": claim, "status": "resolved",
                      "reason": "Synthetic control decision, not an actual review.",
                      "evidence": [entry["adjudication"]["path"]]} for claim in ("D1", "C1"))
    closure = history(index, entries, {}, {"path": "resolution.json", "sha256": "0" * 64}, ["x"])
    closure["recordedFileSha256"] = inventory
    claims = {}
    for family in INITIALS:
        _, refs, _, collected = actual_initial(family)
        report = frozen(refs["report"]["path"], refs["report"]["sha256"])
        claims[family] = {"report": report, "reportSha256": sha(report), "claims": collected}
    return closure, original, lineage, adjudications, fresh, inventory, claims


class ResolutionBuilderControls(unittest.TestCase):
    def test_actual_original_obligations_are_complete_and_archive_bound(self):
        _, evidence, inventory, protected, original, lineage = originals()
        required = set()
        for family in INITIALS:
            spec, refs, _, claims = actual_initial(family)
            report = frozen(refs["report"]["path"], refs["report"]["sha256"])
            required.update((spec["run"], claim) for claim in disposition_ids(report, claims))
        self.assertEqual({(row["run"], row["id"]) for row in original}, required)
        self.assertEqual(len(original), 29)
        for row in original:
            self.assertTrue(row["evidence"])
            for ref in row["evidence"]:
                self.assertEqual(inventory[ref["path"]], ref["sha256"])
        self.assertEqual(lineage, {
            "N1-B134-CLAUDE-001": "b74cdf6946c1bb885050254a57c3d269c2a52d73f48e861c598ea99d206a9b96",
            "N1-B134-GPT-001": "bd1e1d3edf5599c1546e5ce726c34e5355e921b0193f132cf972e6ec7e2df2d7",
        })
        self.assertEqual(len(evidence), len(builder.FIXED_EVIDENCE))
        self.assertEqual(len(protected), 14)

    def test_built_resolution_passes_history_validation(self):
        closure, original, lineage, adjudications, fresh, inventory, claims = scenario()
        resolution = builder.build_resolution(original, lineage, adjudications, fresh, inventory)
        validate_resolution(resolution, closure, REVIEWED, claims)
        self.assertEqual(len(resolution["dispositions"]), 33)

    def test_missing_original_or_fresh_decision_fails_history_validation(self):
        closure, original, lineage, adjudications, fresh, inventory, claims = scenario()
        for dropped_original in (True, False):
            kept_original = original[1:] if dropped_original else original
            kept_fresh = fresh if dropped_original else fresh[1:]
            resolution = builder.build_resolution(kept_original, lineage, adjudications,
                                                  kept_fresh, inventory)
            with self.subTest(dropped_original=dropped_original), self.assertRaises(ValueError):
                validate_resolution(resolution, closure, REVIEWED, claims)

    def test_unsupported_fresh_decisions_are_rejected(self):
        _, original, lineage, adjudications, fresh, inventory, _ = scenario()
        changes = (
            lambda rows: rows[0].update(status="partially resolved"),
            lambda rows: rows[0].update(reason=" "),
            lambda rows: rows[0].update(evidence=[]),
            lambda rows: rows[0].update(evidence=["verification/unarchived.json"]),
            lambda rows: rows[0].update(evidence=["../outside.json"]),
            lambda rows: rows[0].update(run="N1-B134-CLAUDE-001"),
            lambda rows: rows[0].update(extra="field"),
            lambda rows: rows.append(copy.deepcopy(rows[0])),
        )
        for index, change in enumerate(changes):
            rows = copy.deepcopy(fresh)
            change(rows)
            with self.subTest(index=index), self.assertRaises(ValueError):
                builder.build_resolution(original, lineage, adjudications, rows, inventory)


if __name__ == "__main__":
    unittest.main()
