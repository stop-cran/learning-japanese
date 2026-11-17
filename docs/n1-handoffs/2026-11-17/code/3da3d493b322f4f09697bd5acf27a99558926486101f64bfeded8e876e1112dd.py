"""Read explicit source-name adaptations without relabeling signed evidence."""
import json

from common import frozen, require, sha


def load(config, signed_blob):
    binding = config["sourceContract"]
    contract = json.loads(frozen(binding["path"], binding["sha256"]))
    require(contract["candidate"] == config["candidate"] and contract["base"] == config["base"]
            and contract["batch"] == config["batch"], "Source contract belongs to another snapshot")
    for path, digest in contract["signedSources"].items():
        require(sha(signed_blob(path)) == digest, f"Signed source changed: {path}")
    for name in contract["files"]:
        read(contract, name)
    return contract


def read(contract, name):
    binding = contract["files"][name]
    return frozen(binding["path"], binding["sha256"])
