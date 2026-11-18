"""Preserve the byte-budget controller and derive a calibrated capacity-only successor."""
from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen


def main():
    source = TOOLS / "confirm_b133.py"
    raw = frozen(source, "c3bf64d441ed207a5d6ad5e392dfc8d7a13a6de83f62f8c37c1f5efcef5ff404")
    before = raw.decode("utf-8")
    changes = [
        ("from b133_closure_records import collect_initial_record",
         "from b133_closure_records import collect_initial_record\n"
         "from b133_confirmation_capacity import confirmation_cost"),
        ("    total = sum(row[\"bytes\"] for row in chain[\"segments\"])\n"
         "    peak = observed[\"lastInputTokens\"] + total + prompt_bytes + DRIFT_ALLOWANCE + REPORT_ALLOWANCE",
         "    measured = confirmation_cost(chain)\n"
         "    total = measured[\"chainBytes\"]\n"
         "    peak = observed[\"lastInputTokens\"] + measured[\"tokens\"] + prompt_bytes + DRIFT_ALLOWANCE + REPORT_ALLOWANCE"),
        ("\"method\": \"Conservative one estimated token per rendered byte; live telemetry still required.\",",
         "\"estimatedChainTokens\": measured[\"tokens\"], \"calibration\": measured,\n"
         "        \"method\": measured[\"method\"],"),
        ("                    binding(chain_path), binding(Path(__file__)),",
         "                    binding(chain_path), binding(Path(__file__)),\n"
         "                    binding(Path(__file__).with_name(\"b133_confirmation_capacity.py\")),\n"
         "                    binding(P / \"tools\" / \"capacity004.py\"),\n"
         "                    binding(P / \"tools\" / \"capacity004_units.py\"),"),
    ]
    newline = "\r\n" if "\r\n" in before else "\n"
    changes = [(old.replace("\n", newline), new.replace("\n", newline)) for old, new in changes]
    after = before
    for old, new in changes:
        require(after.count(old) == 1, "Controller source differed")
        after = after.replace(old, new)
    restored = after
    for old, new in reversed(changes):
        restored = restored.replace(new, old)
    require(restored == before, "Non-capacity controller change")
    capacity = TOOLS / "b133_confirmation_capacity.py"
    capacity.chmod(0o444)
    ref = write_frozen(TOOLS / "confirm_b133_v2.py", after.encode("utf-8"))
    record = {
        "original": {"path": str(source), "sha256": sha(raw)}, "successor": ref,
        "capacity": {"path": str(capacity), "sha256": sha(frozen(capacity))},
        "scope": "Capacity estimate only: existing B133 calibration; same 700000 gate and all reserves. "
                 "Full source reconstruction and additional binding of capacity helpers. "
                 "No reviewer admitted and no previously failed review relabeled.",
    }
    print(freeze_json(WS / "scratch-133" / "review" / "confirmation-002" / "capacity-successor.json", record))


if __name__ == "__main__":
    main()
