"""GPT004-only output namespace; all teaching/source/forecast bytes remain compact-002."""
import json

from b131_review_v3_common import *

PRIOR = RECORDS / "preparation-003"
HERE = RECORDS / "preparation-004"
RUNS = ("N1-B131-GPT-004",)
DEFAULT_PREFLIGHT = HERE / "prompts" / "preflight-compact-004.json"
POLICY = HERE / "capacity-policy-004.json"
TELEMETRY = RECORDS / "capacity" / "gpt003-neutral-telemetry-001.json"
TELEMETRY_SHA = "858bcef9314908bdfc40b5ca5d714837b611ee4b8fb6cedb91e2b468d2d9fb1a"
ACCEPTANCE = PRIOR / "N1-B131-CLAUDE-003-acceptance.json"
ACCEPTANCE_SHA = "1ed83db9be063f5f80e5d36df3a928e7fd9a8a3353c94b59d0c7fc99adb129e8"


def review_dir(batch):
    require(int(batch) == 131, "Preparation004 is B131-only")
    return HERE


def load_batch(batch):
    value = json.loads(frozen(review_dir(batch) / "batch.json"))
    require(value["candidate"] == CANDIDATE and value["base"] == BASE and value["members"] == MEMBERS
            and value["repo"] == str(REPO), "Candidate configuration differs")
    value["configSha256"] = sha(frozen(HERE / "batch.json"))
    return value


def accepted_prerequisite():
    raw = frozen(ACCEPTANCE, ACCEPTANCE_SHA)
    record = json.loads(raw)
    identity = {key: record[key] for key in ("run", "candidate", "reviewAccepted")}
    require(identity == {"run": "N1-B131-CLAUDE-003", "candidate": CANDIDATE, "reviewAccepted": True},
            "Prior accepted Claude003 identity changed")
    return {"path": str(ACCEPTANCE), "sha256": sha(raw), **identity,
            "scope": "Acceptance identity only; no report, adjudication or findings used."}
