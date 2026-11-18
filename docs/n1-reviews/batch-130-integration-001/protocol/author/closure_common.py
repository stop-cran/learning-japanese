import json
import stat
import sys
from pathlib import Path

SCRATCH = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-130")
sys.path.insert(0, str(SCRATCH / "integration-001-author"))
from integration_common import FINGERPRINT, REPO, command, git, sha, start_guard, tree_entries, write

HERE = Path(__file__).resolve().parent
ROOT = SCRATCH.parent
REVIEW = SCRATCH / "review"
TOOLS = ROOT / "review-tools"
PARENT = "37a53e75446bacad8ade4e212404b121d4a01af1"
PREVIOUS = "1ac4053c5da955c3afaafc1e879e63a98ee42526"
PARENTS = ["9151a6f6ad5bdba9b58178167fba4cabab876504", "153c6b833f68d99f59cbbce34b0bdc6d09a59bc7"]
ARCHIVE = "docs/n1-reviews/batch-130-integration-001"
OLD = "docs/n1-reviews/batch-130-closure"
LEDGER = "docs/n1-sources/batch-130-progress.json"
MANIFEST_SHA = "23583ae2a885bd67212f8a541415a08bd6411c05763e1813bbd13145a7399495"
VERSION = "3df59f6cf1dee0f2"
RUNTIME = {"manifestSha256": MANIFEST_SHA, "contentVersion": VERSION, "runtimeEntries": 8730}
RUNS = {"claude": "N1-B130-CLAUDE-CONFIRM-005", "gpt": "N1-B130-GPT-CONFIRM-004"}
ACCEPTANCE = {
    "claude": "2fda565acde87bea3b5d06c6ac9f8ffdeb93f81241342a8bdcb92a5fd974f6aa",
    "gpt": "6f5026409b120973533ff183038bd2b2983d446fdf55f4f4c763d9be1e0bb3ae",
}
LIMITS = [
    "Integration-impact confirmation only, on exact37a53e75; no independent linguistic certification of the unrelated age-counter change or whole-N1 review.",
    "Earlier closure, reports, accepted and unaccepted snapshots, D18 and excluded/prepared-only histories retain their original identities and qualifications.",
    "Rare-spelling/effect-impression allocation, historical image glyphs, dictionary disagreements and unread-index comparisons remain unresolved as previously disclosed.",
    "Bounded N1/All/Starter-plus-one host evidence only; latent 拍ひゃく and 耗ぼう and arbitrary/custom/multiple-borrow risks remain.",
    "No Kotlin/native/device/old-APK/font-rendering/served-ZIP acceptance, publication approval or delivery credit.",
    "Both current reports' complete six/eight limits and every earlier ledger limit remain applicable.",
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def raw(path, expected=None):
    path = Path(path)
    data = path.read_bytes()
    require(expected is None or sha(data) == expected, "Input hash differs: " + str(path))
    return data


def load(path):
    return json.loads(raw(path))


def frozen(path, expected=None):
    data = raw(path, expected)
    require(not Path(path).stat().st_mode & stat.S_IWRITE, "Frozen input writable: " + str(path))
    return data


def freeze(path, data):
    write(path, data)
    path.chmod(stat.S_IREAD)
    require(path.read_bytes() == data if isinstance(data, bytes) else load(path) == data, "Readback differs")


def binding(path):
    return {"path": str(path), "sha256": sha(raw(path)), "bytes": path.stat().st_size}


def signature(ref):
    git("verify-commit", ref)
    fields = git("show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%GF%n%G?", ref).decode().splitlines()
    require(fields == ["Roman Konstantinovskiy", "stop-cran@list.ru",
                       "Roman Konstantinovskiy", "stop-cran@list.ru", FINGERPRINT, "G"],
            "Owner signature/identity differs")
    require("Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
            in git("show", "-s", "--format=%B", ref).decode(), "Missing required trailer")
    return {"author": fields[:2], "committer": fields[2:4], "fingerprint": fields[4], "status": fields[5]}


def admitted_inputs():
    brief = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b130-integration-closure-author-brief.txt")
    admission = REVIEW / "integration-closure-author-admission-001" / "admission.json"
    frozen(brief, "6697263e95e3cacf3481d7a6e9fa21fa0a8035248e170a9f68e7c7f093794746")
    frozen(admission, "39d5d951cbef2262b591ad2572dd6ed789e74ca00b8c549e09961425c031acff")
    record = load(admission)
    require(record["admitted"] and record["candidate"] == PARENT, "Wrong author admission")
    frozen(Path(record["snapshot"]["path"]), record["snapshot"]["sha256"])
    return {"brief": binding(brief), "coordinatorAdmission": binding(admission),
            "localOnlySnapshot": record["snapshot"], "rawInputsRemainLocal": True}


def integration_review(provenance_sha, validation_sha, previous):
    return {
        "status": "closed-with-disclosed-limits", "reviewedSnapshot": PARENT,
        "previousReviewedSnapshot": PREVIOUS, "parents": PARENTS, "runtimeCandidate": RUNTIME,
        "finalRuns": list(RUNS.values()), "closurePath": ARCHIVE,
        "closureProvenanceSha256": provenance_sha, "validationProvenanceSha256": validation_sha,
        "scope": "Two accepted same-family independent integration-impact confirmations on the exact signed integration; not automatic transfer of the earlier snapshot's acceptance.",
        "limits": LIMITS, "previousLimitsPreserved": previous["limits"],
        "currentRawAuditsClean": True, "currentControlMessageAdjudicationUsed": False,
        "publicationAccepted": False, "deliveryCredit": 0,
    }


def make_ledger(previous, provenance_sha, validation_sha):
    require("activeReviewedSnapshot" not in previous and "integrationReview" not in previous,
            "Integration extension already exists")
    require(previous["reviewedSnapshot"] == PREVIOUS
            and previous["status"] == "textual-review-closed-publication-pending"
            and previous["published"] == [] and previous["runtimePublished"] is False
            and previous["accounting"]["publishedPendingRecordsWithCards"] == 261
            and previous["accounting"]["undelivered"] == 967, "Prior ledger boundary differs")
    return {**previous, "activeReviewedSnapshot": PARENT,
            "integrationReview": integration_review(provenance_sha, validation_sha, previous)}


def check_ledger(previous, current, provenance_sha, validation_sha):
    require(current == make_ledger(previous, provenance_sha, validation_sha),
            "Ledger must preserve every old key/value and add exactly the explicit extension")


def check_delta(before, after):
    require(set(before) <= set(after), "Tracked parent path removed")
    require({path for path in before if before[path] != after[path]} == {LEDGER},
            "Changed old blob/mode outside primary ledger")
    require(before[LEDGER]["mode"] == after[LEDGER]["mode"], "Ledger Git mode changed")
    added = set(after) - set(before)
    require(added and all(path.startswith(ARCHIVE + "/") for path in added), "Unscoped new path")
    return added


def mode_tree(mode):
    head = git("rev-parse", "HEAD").decode().strip()
    if mode == "author":
        require(head == PARENT, "Wrong author parent")
    else:
        require(git("rev-parse", "HEAD^@").decode().split() == [PARENT], "Not a direct contributor-only child")
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Committed tree dirty")
    require(not git("diff", "--name-only") and not git("ls-files", "--others", "--exclude-standard"),
            "Unstaged or untracked content")
    return head, git("write-tree").decode().strip()


def check_lineage(provenance, validation, provenance_sha):
    require(provenance["reviewedSnapshot"] == validation["candidate"] == PARENT
            and provenance["previousReviewedSnapshot"] == PREVIOUS
            and provenance["parents"] == PARENTS
            and provenance["runtimeCandidate"] == validation["runtimeCandidate"] == RUNTIME
            and provenance["finalRuns"] == list(RUNS.values())
            and validation["reviewClosureSha256"] == provenance_sha, "Archive lineage/binding differs")
    lineage = provenance["reviewLineage"]
    require(len(lineage) == 2 and {row["family"] for row in lineage} == set(RUNS)
            and len({row["session"] for row in lineage}) == 2, "Independent lineage differs")
    for row in lineage:
        family = row["family"]
        require(row["run"] == RUNS[family] and row["snapshot"] == PARENT
                and row["priorSnapshot"] == PREVIOUS and row["rawVerdict"] == "CONFIRMED"
                and row["rawAuditWasClean"] and not row["controlMessageAdjudicationApplied"],
                "Current integration evidence was relabelled")


def check_archive(guard):
    out = REPO / ARCHIVE
    provenance_raw = frozen(out / "provenance.json")
    validation_raw = frozen(out / "validation-provenance.json")
    provenance, validation = map(json.loads, (provenance_raw, validation_raw))
    check_lineage(provenance, validation, sha(provenance_raw))
    first, second = provenance["recordedFileSha256"], validation["recordedFileSha256"]
    require(not first.keys() & second.keys(), "Archive inventories overlap")
    inventory = {**first, **second}
    expected = set(inventory) | {"provenance.json", "validation-provenance.json"}
    actual = {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}
    require(actual == expected, "Archive contains missing/uninventoried files")
    for name, digest in inventory.items():
        guard.check()
        frozen(out / name, digest)
    return provenance, validation, inventory, sha(provenance_raw), sha(validation_raw)
