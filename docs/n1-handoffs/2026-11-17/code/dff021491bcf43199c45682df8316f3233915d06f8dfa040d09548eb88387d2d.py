"""Fresh003 lifecycle paths; compact-002 evidence, core, caps and forecast remain immutable."""
import json
from pathlib import Path

from b131_review_v2_common import *
import b131_review_v2_common as predecessor

OLD_PREP = predecessor.HERE
HERE = RECORDS / "preparation-003"
RUNS = ("N1-B131-CLAUDE-003", "N1-B131-GPT-003")
CORE = OLD_PREP / "core-chain-compact-002.json"
DEFAULT_PREFLIGHT = HERE / "prompts" / "preflight-compact-003.json"
IMMUTABLE_BINDINGS = (
    (PACKET / "SHA256SUMS.json", "7a8308db2ca5f912afbb61151afff31f98ee5b35c5b357957e9c80835010305c"),
    (OLD_HERE / "source-contract.json", "94c879183f0e012cf5c6ff64189dc5fb92a2b8e310cc9c58dde263b83e3f532d"),
    (CORE, "c6ce97ff03a25a08029689fe0e0cb26af83c97853892cd1bee135094956c8bdb"),
    (OLD_PREP / "review_chain.py", "2e4184500af5f4361d996a3568ed4f6abf2f3999f80556fa07ac3e22782d12ae"),
    (FORECAST, "1d524f25ed065fb5a2c9f4ecfbad1e28a25b4b54d0b058c6bbcd1619283ca3bb"),
)


def review_dir(batch):
    require(int(batch) == 131, "Preparation003 is B131-only")
    return HERE


def load_batch(batch):
    value = json.loads(frozen(review_dir(batch) / "batch.json"))
    require(value["candidate"] == CANDIDATE and value["base"] == BASE and value["members"] == MEMBERS
            and value["repo"] == str(REPO), "Candidate configuration differs")
    value["configSha256"] = sha(frozen(HERE / "batch.json"))
    return value
