"""Factor mechanically redundant presentation fields without removing source information."""
import json
from pathlib import Path

from common import freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from confirm_b127 import build
from prepare_b129_confirmations import neutral
from verify_b129_revision_runtime import PREFIX, REPO, REVIEW

OUTPUT = REVIEW / "confirmation-003-neutral"
PREPARATION_SHA = "79e7f0339492f5160ac755ab99c4ea43bede6d4775837d7db73281ce7cc4325c"


def compact_membership(raw):
    value = json.loads(raw)
    require(set(value) == {"queries", "recordPredicates", "zeroMatches"}, "Unknown membership fields")
    queries = value["queries"]
    identities = sorted({identity for values in queries.values() for identity in values})
    inverse = {identity: [query for query, values in queries.items() if identity in values]
               for identity in identities}
    require(inverse == value["recordPredicates"]
            and [query for query, values in queries.items() if not values] == value["zeroMatches"],
            "Membership cannot be reconstructed losslessly")
    header = {"format": "Header followed by [exact query, complete ordered identity list] per line.",
              "inputSha256": sha(raw), "queryCount": len(queries),
              "equivalence": "The original inverse is exactly reconstructed by collecting query keys "
              "in this order for each identity; original zeroMatches is exactly the ordered empty "
              "rows. Both reconstructions were compared with the signed originals. No query or "
              "identity was omitted."}
    lines = [header, *[[query, values] for query, values in queries.items()]]
    return ("\n".join(json.dumps(line, ensure_ascii=False, separators=(",", ":")) for line in lines)
            + "\n").encode()


def factor_rows(raw):
    values = [json.loads(line) for line in raw.decode().splitlines()]
    header, rows = values[0], values[1:]
    shared = {key: rows[0][key] for key in ("guardSemantics", "coverage")}
    require(all(all(row[key] == expected for key, expected in shared.items()) for row in rows),
            "Pair declarations are not identical")
    result = [{key: value for key, value in row.items() if key not in shared} for row in rows]
    require([{**row, **shared} for row in result] == rows, "Pair information lost")
    header["sharedRowFields"] = shared
    header["sharedFieldRule"] = "These two fields apply unchanged to every following row."
    return ("\n".join(json.dumps(line, ensure_ascii=False, separators=(",", ":"))
                      for line in [header, *result]) + "\n").encode()


def main():
    require(not OUTPUT.exists(), "Preserve earlier presentation")
    previous = json.loads(frozen(REVIEW / "confirmation-002-preparation.json", PREPARATION_SHA))
    guard, _ = start_guard("B129 lossless confirmation metadata factoring")
    try:
        old_pairs = REVIEW / "confirmation-002-neutral" / "pair-dispositions.jsonl"
        pair_raw = frozen(old_pairs)
        member_path = REPO / PREFIX / "jmdict-query-membership.json"
        membership_raw = member_path.read_bytes()
        require(sha(membership_raw) == "363baf203a3155142f849068f1298c3e7ab56226c6c77684d9afcfc99f10a268",
                "Signed membership changed")
        generated = {}
        for name, data, source in (
            ("pair-dispositions.jsonl", factor_rows(pair_raw), "evidence/reconciliation/pair-dispositions.jsonl"),
            ("query-membership.jsonl", compact_membership(membership_raw), "evidence/reconciliation/query-membership.jsonl"),
        ):
            require(neutral(data), "Shared metadata leaks provenance")
            generated[name] = {**write_frozen(OUTPUT / name, data), "source": source}
        runs = []
        for family in ("CLAUDE", "GPT"):
            old_run = f"N1-B129-{family}-CONFIRM-002"
            require(not (REVIEW / "confirm" / f"{old_run}-admission.json").exists(), "Already admitted")
            spec = json.loads(frozen(REVIEW / "confirm" / f"{old_run}-spec.json"))
            spec["run"] = f"N1-B129-{family}-CONFIRM-003"
            spec["revisedSources"].remove(PREFIX + "jmdict-query-membership.json")
            spec["additionalSources"] = [
                generated["pair-dispositions.jsonl"]
                if item["source"] == "evidence/reconciliation/pair-dispositions.jsonl" else item
                for item in spec["additionalSources"]
            ] + [generated["query-membership.jsonl"]]
            spec_path = REVIEW / "confirm" / f"{spec['run']}-spec.json"
            freeze_json(spec_path, spec)
            build(spec_path)
            chain = json.loads(frozen(REVIEW / "confirm" / f"{spec['run']}-chain.json"))
            runs.append({"run": spec["run"], "session": spec["session"],
                         "segments": len(chain["segments"]),
                         "chainBytes": sum(row["bytes"] for row in chain["segments"])})
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Metadata factoring RAM guard breached")
    print(json.dumps(freeze_json(REVIEW / "confirmation-003-preparation.json", {
        "candidate": previous["candidate"], "status": "PREPARED_NOT_ADMITTED",
        "priorPreparationSha256": PREPARATION_SHA, "runs": runs, "outputs": generated,
        "sourceMembershipSha256": sha(membership_raw), "sourcePairSha256": sha(pair_raw),
        "roundTripVerified": True, "memory": memory, "producerSha256": sha(frozen(Path(__file__))),
        "limits": "Same bounded sources as preparation002; only reconstructible redundancy factored. "
                  "Preparations001/002 were never admitted or delivered. Actual context audit remains required.",
    })))


if __name__ == "__main__":
    main()
