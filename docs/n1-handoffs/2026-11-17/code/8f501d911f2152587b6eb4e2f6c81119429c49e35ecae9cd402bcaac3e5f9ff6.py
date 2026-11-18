"""Derive B134 confirmation tools from frozen, tested B133 implementations."""
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen

OUT = WS / "scratch-134" / "review" / "confirmation-001"
OLD = WS / "scratch-133" / "review" / "confirmation-002"
SOURCES = {
    "confirm_b133_v2.py": "72c7862006736c8921ad4126e90e1943fccfa15cf1c806d1c9386ea9ba4c2444",
    "b133_confirmation_capacity.py": "b1a1c7b0ac9dc4ba3a0f445abdda4f6cd29b012c1dbeddd04e1134177d146e67",
    "b133_confirmation_records.py": "408838d3ce1bcecc98b58195eba56907c52ecbcea897e3990a114b224c642598",
    "accept_b133_confirmation.py": "f6ec9ce8d9415b878743864661807de04842c6f9e38594f6b29c88ebd1836f0d",
    "renderer.py": "2f8687d932e1ea7383e6e8e27da269721a69c5ba9c5ebcd772eabbde3137115c",
    "audit-confirm.py": "2b34ff28d0f6ab2204d2d7d84a9092dcc048a994899bcfd9f5503fd8b8fa0632",
    "check-confirm-structure.py": "92447027192ebdecaba3b1f49884d87d1781fd5460221ae623b7109ba82077bd",
}


def derive(name):
    source = (OLD if name in ("renderer.py", "audit-confirm.py", "check-confirm-structure.py")
              else TOOLS) / name
    before = frozen(source, SOURCES[name]).decode("utf-8")
    text, changes = before, []
    newline = "\r\n" if "\r\n" in before else "\n"

    def replace(old, new, expected=None):
        nonlocal text
        old, new = old.replace("\n", newline), new.replace("\n", newline)
        count = text.count(old)
        require(count > 0 and (expected is None or count == expected), "Unexpected source: " + name + ": " + old)
        text = text.replace(old, new)
        changes.append({"old": old, "new": new, "occurrences": count})

    replace("B133", "B134")
    if "b133" in text:
        replace("b133", "b134")
    if "133" in text:
        replace("133", "134")
    if name == "confirm_b133_v2.py":
        replace("from admit_b134_source_reconciliation import INITIALS, P, PREFLIGHT",
                "from b134_initial_records import INITIALS, P, PREFLIGHT", 1)
        replace("from b134_closure_records import collect_initial_record",
                "from b134_initial_records import collect_initial_record", 1)
        replace('OUT = ROOT / "confirmation-002"', 'OUT = ROOT / "confirmation-001"', 1)
        replace('PROTOCOL = P / "protocol-003"', 'PROTOCOL = P / "protocol-001"', 1)
        replace("from review_chain import build_chain", "from review_chain_with_optional import build_chain", 1)
        replace('PROTOCOL_MODULES = ("review_chain.py", "review_chain_with_optional.py",',
                'PROTOCOL_MODULES = ("review_chain_with_optional.py",', 1)
        replace('    require(claims == known["claims"], "Initial consequential claims differ")',
                '    normalized = json.loads(frozen(ROOT / "confirmation-initial-bindings-001" / "index.json",\n'
                '        "52b412392c5ccebf1bdf363583ceb24b3c889bce9f7a5f29a6b33e0175103eb1"))\n'
                '    require(claims == normalized["initials"][family]["claims"], "Initial claims differ")', 1)
        replace('                    binding(chain_path), binding(Path(__file__)),',
                '                    binding(chain_path), binding(Path(__file__)),\n'
                '                    binding(Path(__file__).with_name("b134_initial_records.py")),\n'
                '                    binding(Path(__file__).with_name("b134_confirmation_records.py")),\n'
                '                    binding(ROOT / "confirmation-initial-bindings-001" / "index.json",\n'
                '                        "52b412392c5ccebf1bdf363583ceb24b3c889bce9f7a5f29a6b33e0175103eb1"),', 1)
        target = TOOLS / "confirm_b134.py"
    elif name == "b133_confirmation_records.py":
        replace("from b134_closure_records import MECHANICAL_STATUS, collect_initial_record",
                "from b134_initial_records import MECHANICAL_STATUS, collect_initial_record, disposition_ids", 1)
        first = text.index("def disposition_ids(")
        last = text.index("def validate_confirmation(", first)
        replace(text[first:last].replace(newline, "\n"), "", 1)
        target = TOOLS / "b134_confirmation_records.py"
    elif name == "accept_b133_confirmation.py":
        replace("from admit_b134_source_reconciliation import INITIALS, P, PREFLIGHT",
                "from b134_initial_records import INITIALS, P, PREFLIGHT", 1)
        target = TOOLS / "accept_b134_confirmation.py"
    elif name == "audit-confirm.py":
        replace("HERE.parent / 'neutral-preparation-004' / 'successor-002' / 'protocol-003'",
                "HERE.parent / 'neutral-preparation-001' / 'projected-successor-001' / 'protocol-001'", 1)
        replace("from review_chain import digest", "from review_chain_with_optional import digest", 1)
        target = OUT / name
    elif name == "check-confirm-structure.py":
        replace(r"([CFOQ][1-9]\d?)", r"((?:(?:CLAUDE|GPT)-)?[CDEFOQL][1-9]\d*)", 1)
        target = OUT / name
    elif name == "renderer.py":
        replace("No other reviewer's report or held-run observations are supplied or authorized.",
                "No other reviewer's report is supplied or authorized. Coordinator-labeled claims may\n"
                "identify shared reconciliation work; they are not another reviewer's verdict.", 1)
        target = OUT / name
    else:
        target = TOOLS / "b134_confirmation_capacity.py"
    # Reverse patches use exact occurrence counts; a removed block is checked by forward replay below.
    replay = before
    for change in changes:
        require(replay.count(change["old"]) == change["occurrences"], "Derivation replay differs")
        replay = replay.replace(change["old"], change["new"])
    require(replay == text and "B133" not in text and "b133" not in text, "Unexpected derivation delta")
    return target, text.encode("utf-8"), {
        "source": {"path": str(source), "sha256": SOURCES[name]},
        "target": str(target), "changes": changes,
    }


def main():
    require(not OUT.exists(), "Preserve existing B134 confirmation tooling")
    prepared = [derive(name) for name in SOURCES]
    require(all(not target.exists() for target, _, _ in prepared), "Preserve existing derived tools")
    records = []
    for target, raw, record in prepared:
        record["output"] = write_frozen(target, raw)
        records.append(record)
    record = {
        "batch": 134, "status": "PREPARED_NOT_ADMITTED", "derivations": records,
        "producerSha256": sha(frozen(Path(__file__))),
        "limits": "No signed reconciliation source dossier, actual build, reviewer admission or review acceptance. "
                  "Same serial/context/700000 startup gates and complete-source chain auditing; identity-only "
                  "initial-claim normalization and explicit D/E/L/CLAUDE-C disposition IDs.",
    }
    print(json.dumps(freeze_json(OUT / "derivation.json", record)))


if __name__ == "__main__":
    main()
