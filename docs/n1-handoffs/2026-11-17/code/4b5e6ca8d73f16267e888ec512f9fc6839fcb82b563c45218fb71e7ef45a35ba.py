"""B130's signed final-union, JSON reading-key and progress schema checks."""
import ast
import json

from common import require
from verify_b130_payload import BASE, MEMBERS, PREFIX, SUPPORTS

FINAL_VERIFIER_SHA = "6910aa8d05dc7da5b7e42c178add8853dc965601affa793533f1a5c278b8617a"
RESIDUAL = "jmdict-final-families.xml"


def verify_final_proof(proof, source_sha, candidate):
    require(proof["batch"] == 130 and proof["base"] == BASE and proof["candidate"] == candidate
            and proof["status"] == "PASS" and not proof["memory"]["breach"]
            and proof["sourceProof"]["sha256"] == source_sha
            and proof["verifierSha256"] == FINAL_VERIFIER_SHA
            and PREFIX + RESIDUAL in proof["signedInputs"], "Final source proof is not bound to this candidate")


def receipt_outputs(receipt):
    require(("outputs" in receipt) != ("finalAdditionalOutput" in receipt),
            "Source receipt needs exactly one output representation")
    return receipt["outputs"] if "outputs" in receipt else {RESIDUAL: receipt["finalAdditionalOutput"]}


def verify_reading_keys(producer_raw, reading_raw, log_raw, required):
    expected = ast.parse(
        'extras = json.loads((PACKET / "reading-keys.json").read_text(encoding="utf-8"))["testedKeys"]'
    ).body[0].value
    assignments = [node.value for node in ast.parse(producer_raw).body if isinstance(node, ast.Assign)
                   and any(isinstance(target, ast.Name) and target.id == "extras" for target in node.targets)]
    require(len(assignments) == 1 and ast.dump(assignments[0]) == ast.dump(expected),
            "Reading producer does not read exactly the signed tested-key map")
    extras = json.loads(reading_raw)["testedKeys"]
    require(set(extras) == set(MEMBERS)
            and all(isinstance(keys, list) and keys and len(keys) == len(set(keys))
                    and all(isinstance(key, str) and key for key in keys) for keys in extras.values())
            and all(set(keys) <= set(extras.get(char, [])) for char, keys in required.items()),
            "Positive supplemental reading keys are not explicitly tested")
    prefix = "Explicit supplemental reading keys: "
    lines = [line[len(prefix):] for line in log_raw.decode("utf-8").splitlines() if line.startswith(prefix)]
    require(len(lines) == 1 and json.loads(lines[0]) == extras,
            "Reading-exposure log does not record exactly the signed tested keys")
    return extras


def verify_progress(progress, facts, payload):
    require(progress["batch"] == 130 and progress["base"] == BASE
            and progress["status"] == "local-unreviewed-author-candidate"
            and progress["members"] == MEMBERS and progress["sourceRows"] == [191, 419, 879]
            and progress["publishedDelivered"] == 261 and progress["frozenTotal"] == 1228
            and progress["undelivered"] == 967 and progress["localUnpublishedDrafts"] == len(MEMBERS)
            and progress["deliveryNotIncremented"] is True
            and progress["supports"] == [[char, word] for char in MEMBERS for word in SUPPORTS[char]]
            and progress["proseException"] is None and facts["wordProseExceptions"] == []
            and progress["manifestSha256"] == payload["manifestSha256"]
            and progress["contentVersion"] == payload["contentVersion"]
            and progress["activePairTable"] == "batch-130/" + facts["pairDispositions"]
            and progress["completeJmdictFamilies"] == facts["expectedJmdictFamilies"],
            "Premature publication or changed progress scope")
