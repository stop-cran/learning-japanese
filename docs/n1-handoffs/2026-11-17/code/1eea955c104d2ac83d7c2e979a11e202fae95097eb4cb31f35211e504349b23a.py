"""Specialize the established signed-delivery tools without changing their safety gates."""
from common import TOOLS, WS, freeze_json, frozen, sha, write_frozen
from derive_b133_closure_recorders_v2 import replace


def main():
    outputs = {}
    for name in ("sign_b132_delivery.py", "publish_b132.py"):
        original = frozen(TOOLS / name)
        raw = original.replace(b"b132", b"b133").replace(b"B132", b"B133").replace(b"batch-132", b"batch-133")
        raw = replace(raw, "from record_b133_publication import validate_progress",
                      "from record_b133_publication_v2 import validate_progress")
        raw = replace(raw, "from verify_b133_teaching_revision import REVISION",
                      "from b133_closure_origins import REVISION")
        if name.startswith("sign"):
            raw = replace(raw, '"closure-gates-closure-001"', '"closure-gates-001"')
            raw = raw.replace(b"N1 grave card", b"three N1 kanji cards")
            raw = replace(raw, '        git("diff", "--cached", "--check")',
                          '        for path in staged:\n'
                          '            require(git("show", ":" + path) == (REPO / path).read_bytes(),\n'
                          '                    "Staging changed reviewed bytes: " + path)\n'
                          '        git("-c", "core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol",\n'
                          '            "diff", "--cached", "--check")')
        else:
            raw = replace(raw, '("closure-gates-" + kind + "-001")',
                          '("closure-gates-001" if kind == "closure" else "closure-gates-committed-001")')
        target = name.replace("b132", "b133")
        compile(raw, target, "exec")
        outputs[target] = {"originalSha256": sha(original), **write_frozen(TOOLS / target, raw)}
    print(freeze_json(WS / "scratch-133" / "review" / "delivery-tools-001.json", {
        "tools": outputs,
        "scope": "Actual B133 revision, paths and fresh-review-aware ledger validation. Single normal "
                 "owner signing attempt with bounded waits and no bypass, exact staged-byte checks, "
                 "default whitespace rules plus CRLF evidence handling; unchanged fast-forward, CI "
                 "and exact immutable ZIP validation.",
    }))


if __name__ == "__main__":
    main()
