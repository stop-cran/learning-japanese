"""Preserve the failed CRLF anchor attempt and resume only byte-equal/newline-equal outputs."""
from b131_review_v2_common import TOOLS, freeze_json, frozen, require, sha, start_guard, write_frozen


def main():
    guard, _ = start_guard("B131 protocol CRLF-safe successor preparation")
    try:
        source = TOOLS / "build_b131_protocol_002.py"
        raw = frozen(source)
        text = raw.decode("utf-8")
        before = '            text = transform(raw.decode("utf-8"))'
        require(text.count(before) == 1, "Transform anchor differs")
        text = text.replace(before, '            text = transform(raw.decode("utf-8").replace("\\r\\n", "\\n"))')
        before = '            output = write_frozen(destination, text.encode("utf-8"))'
        after = (
            '            if destination.exists():\n'
            '                existing = frozen(destination)\n'
            '                require(existing.replace(b"\\r\\n", b"\\n") == text.encode("utf-8"),\n'
            '                        "Preserved prior derived code differs beyond line endings")\n'
            '                output = {"path": str(destination), "sha256": sha(existing), "bytes": len(existing)}\n'
            '            else:\n'
            '                output = write_frozen(destination, text.encode("utf-8"))')
        require(text.count(before) == 1, "Output anchor differs")
        text = text.replace(before, after).replace("build_b131_protocol_002.py", "build_b131_protocol_003.py")
        compile(text, "build_b131_protocol_003.py", "exec")
        output = write_frozen(TOOLS / "build_b131_protocol_003.py", text.encode("utf-8"))
        print(freeze_json(TOOLS / "b131-protocol-successor-003.json", {
            "source": str(source), "sourceSha256": sha(raw), "output": output,
            "reason": "Frozen Windows CRLF source did not match an LF adaptation anchor. "
                      "Normalize implementation text before adapting. Existing derived outputs are reused "
                      "only if equal after CRLF-to-LF normalization; they remain untouched."}))
    finally:
        require(not guard.finish()["breach"], "Successor preparation RAM breach")


if __name__ == "__main__":
    main()
