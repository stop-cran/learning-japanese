"""Copy only the neutral chain implementation, adding forecast-bound caps."""
import json
from b131_review_v2_common import HERE, OLD_HERE, freeze_json, frozen, require, sha, start_guard, write_frozen


def main():
    guard, _ = start_guard("B131 compact-002 chain engine preparation")
    try:
        source = OLD_HERE / "review_chain.py"
        raw = frozen(source)
        text = raw.decode("utf-8")
        before = '        if number > (40 if group == "D" else 10):'
        require(text.count(before) == 1, "Cap anchor differs")
        text = text.replace(before, '        from b131_capacity_002 import load_forecast\n'
                            '        if number > load_forecast()["chosenCaps"][group]:')
        compile(text, "review_chain.py", "exec")
        output = write_frozen(HERE / "review_chain.py", text.encode("utf-8"))
        print(json.dumps(freeze_json(HERE / "chain-engine-derivation-002.json", {
            "source": {"path": str(source), "sha256": sha(raw)}, "output": output,
            "rule": "Same neutral lossless chain and list validation; D/E caps read the frozen passing forecast.",
            "scope": "Implementation only; no held reviewer events, report or selection read."})))
    finally:
        require(not guard.finish()["breach"], "Chain engine RAM breach")


if __name__ == "__main__":
    main()
