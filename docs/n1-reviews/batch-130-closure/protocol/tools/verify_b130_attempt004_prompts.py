"""Verify that attempt-004 review inputs differ from attempt 003 only by fresh run identity."""
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha


ROOT = WS / "scratch-130" / "review"
PROMPTS = ROOT / "prompts"


def ident(data):
    require(b"-003" not in data, "Attempt-004 output retains attempt-003 identity")
    return data.replace(b"-004", b"-003").replace(b"review 004", b"review 003")


def same(new, old):
    require(ident(new) == old, "Attempt-004 bytes differ beyond identity")
    return {"old": sha(old), "new": sha(new)}


def main():
    old_pre = json.loads(frozen(PROMPTS / "preflight-compact-003.json"))
    new_raw = frozen(PROMPTS / "preflight-compact-004.json")
    new_pre = json.loads(new_raw)
    require(new_pre["builder"]["path"] == str(TOOLS / "build-prompts-b130-attempt004.py"), "Builder differs")
    for key in ("packetManifestSha256", "coreChainSha256", "template", "order", "reportDirectory"):
        require(new_pre[key] == old_pre[key], f"Preflight {key} differs")
    checks = {"template": same(frozen(PROMPTS / "template-compact-004.txt"), frozen(PROMPTS / "template-compact-003.txt"))}
    added = {}
    for key, spec in new_pre["runs"].items():
        old = old_pre["runs"][key]
        require(json.loads(ident(json.dumps(spec, ensure_ascii=False).encode("utf-8"))) == old, f"{key} run spec differs")
        checks[f"{key}Prompt"] = same(frozen(spec["prompt"], spec["promptSha256"]), frozen(old["prompt"], old["promptSha256"]))
        checks[f"{key}Kickoff"] = same(frozen(spec["kickoff"]), frozen(old["kickoff"]))
        require(not Path(spec["report"]).exists(), "Attempt-004 report already exists")
        new_cfg, old_cfg = json.loads(frozen(spec["auditConfig"])), json.loads(frozen(old["auditConfig"]))
        new_files, old_files = new_cfg.pop("files"), old_cfg.pop("files")
        require(json.loads(ident(json.dumps(new_cfg, ensure_ascii=False).encode("utf-8"))) == old_cfg, "Audit config differs")
        require([ident(f["path"].encode()).decode() for f in new_files[-2:]] == [f["path"] for f in old_files[-2:]],
                "Prompt/kickoff bindings differ")
        old_map = {f["path"]: f["sha256"] for f in old_files[:-2]}
        new_map = {f["path"]: f["sha256"] for f in new_files[:-2]}
        require(all(new_map.get(p) == h for p, h in old_map.items()), "A previously bound input changed or vanished")
        extra = {p: h for p, h in new_map.items() if p not in old_map}
        require(all(Path(p).parent == TOOLS and Path(p).suffix == ".py" for p in extra), "Unexpected added binding")
        for path, digest in extra.items():
            frozen(path, digest)
        require(not added or added == extra, "Families bind different inputs")
        added = extra
    print(freeze_json(ROOT / "attempt004-prompt-verification-001.json", {
        "batch": 130, "status": "PASS", "previousPreflight": str(PROMPTS / "preflight-compact-003.json"),
        "currentPreflight": str(PROMPTS / "preflight-compact-004.json"), "currentPreflightSha256": sha(new_raw),
        "checks": checks, "addedFrozenToolBindings": added,
        "result": "Template, prompts, kickoffs, run specs and audit configs equal attempt 003 after reverting only "
                  "-004/review 004 identity. Audit configs additionally bind only frozen review tools created after "
                  "attempt 003; every earlier binding is unchanged.",
        "verifier": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
    }))


if __name__ == "__main__":
    main()
