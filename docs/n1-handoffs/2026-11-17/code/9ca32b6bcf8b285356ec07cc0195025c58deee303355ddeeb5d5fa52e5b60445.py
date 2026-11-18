"""Adapt the verified source checks to B123's actual selection and gate schema."""
import json

from common import freeze_json, frozen, require, review_dir, sha, write_frozen

BASE = "6e433d4046144f6eb2593ab2661cc7206c9139be"
OLD_BASE = "86a19f750c6eec7e2f18b87899091380774bdf84"
CHARS = "型例規則法典式幅準律憲域般類師象儀制程令車書達竹側形体状格常王君指治監数方測計"
QUERIES = set(CHARS + "範") | {
    "範囲", "模範", "規範", "範疇", "地球儀", "象る", "上達", "書く", "車", "師範",
}
SOURCES = {
    "verify-source-records.py": "eaa065457bbf2fb04a66a50e57e8d2ed65f385570be3b676eb6596c685af222c",
    "prepare-source-contract.py": "cb8ea56e9bafd61f4af5141a4d196c83ec7d1bafe6c2f00f6a2e2a3653d9b9bc",
    "test-source-records.py": "1e4cbd77c0caca79bdf8f617cf5fc399223dd89669ee8295c8285ffdbf479010",
}

SUMMARY_CHECK = '''
def verify_committed_summary(summary, config, manifest_sha, runner_sha):
    require(summary["batch"] == "123" and summary["status"] == "PASS"
            and summary["mode"] == "committed" and summary["base"] == config["base"]
            and summary["startingHead"] == config["candidate"]
            and len(summary["checks"]) == len(CHECKS)
            and set(summary["checks"]) == set(CHECKS)
            and summary["manifestSha256"] == manifest_sha
            and ("manifestReproducible" not in summary
                 or summary["manifestReproducible"] is True)
            and summary["runnerSha256"] == runner_sha, "Committed gate summary mismatch")

'''


def main():
    outputs, records = {}, []
    for filename, expected in SOURCES.items():
        source = review_dir(122) / filename
        raw = frozen(source, expected)
        text, changes = raw.decode("utf-8").replace("\r\n", "\n"), []

        def replace(before, after, optional=False):
            nonlocal text
            count = text.count(before)
            require(count > 0 or optional, f"Missing substitution in {filename}: {before!r}")
            if count:
                text = text.replace(before, after)
                changes.append({"before": before, "after": after, "count": count})

        for before, after in (
            ("B122", "B123"), ("b122", "b123"), ("batch-122", "batch-123"),
            ("scratch-122", "scratch-123"), (OLD_BASE, BASE),
            ('"batch": 122', '"batch": 123'), ('["batch"] == 122', '["batch"] == 123'),
        ):
            replace(before, after, optional=True)

        if filename == "verify-source-records.py":
            replace('MEMBER = "悠"', 'MEMBER = "範"')
            start = text.index("COMPARISONS = ")
            end = text.index("INPUTS = ", start)
            replace(text[start:end],
                    f"COMPARISONS = set({CHARS!r})\nQUERIES = {set_literal(QUERIES)}\n")
            replace('("selected", "comparison", "choice") if kind == "kanjidic2" else ("selected", "comparison")',
                    '("selected", "comparison")')
            replace('{"selected": {MEMBER}, "comparison": COMPARISONS, "choice": CHOICES}',
                    '{"selected": {MEMBER}, "comparison": COMPARISONS}')
        elif filename == "prepare-source-contract.py":
            for before, after in (
                ('MEMBER, WORD, ROW = "悠", "悠々", 367', 'MEMBER, WORD, ROW = "範", "範囲", 810'),
                ('"expectedKanji": 1242', '"expectedKanji": 1243'),
                ('            "kanjidic2-choice-records.xml",\n', ''),
                ('"kanjidic2-selected-records.xml", "kanjidic2-comparison-records.xml",\n'
                 '            "kanjidic2-choice-records.xml")',
                 '"kanjidic2-selected-records.xml", "kanjidic2-comparison-records.xml")'),
                ('{"delivered": 251, "total": 1228, "undelivered": 977}',
                 '{"delivered": 252, "total": 1228, "undelivered": 976}'),
                ('len(pending & represented(previous)) == 251', 'len(pending & represented(previous)) == 252'),
                ('len(pending & represented(current)) == 252', 'len(pending & represented(current)) == 253'),
                ('len(represented(current)) == 1242', 'len(represented(current)) == 1243'),
                ('"sourceMembersPublishedBeforeBatch": 251', '"sourceMembersPublishedBeforeBatch": 252'),
                ('"sourceMembersInCandidate": 252', '"sourceMembersInCandidate": 253'),
                ('extract = "悠\\nユウ 悠然，悠長，悠々"', 'extract = "範\\nハン 範囲，師範，模範"'),
                ('json.loads(joyo_raw)["149"]', 'json.loads(joyo_raw)["128"]'),
                ('"printedPage": 149', '"printedPage": 128'),
            ):
                replace(before, after)
            replace("\ndef main(candidate, gate_name):", SUMMARY_CHECK + "\ndef main(candidate, gate_name):")
            start = text.index('        require(summary["status"]')
            end = text.index("        gate_records = []", start)
            replace(text[start:end],
                    '        runner_sha = receipt["producerSha256"]["run-checks.py"]\n'
                    '        require(runner_sha == author["runnerSha256"]\n'
                    '                == sha((WS / "scratch-123" / "run-checks.py").read_bytes()),\n'
                    '                "Author gate runner changed")\n'
                    '        verify_committed_summary(summary, config, sha(manifest_raw), runner_sha)\n')
            replace('                    and result["exitCode"] == 0 and result["logSha256"] == sha(log)\n',
                    '                    and result["exitCode"] == result["childExitCodeAfterCleanup"] == 0\n'
                    '                    and result["logSha256"] == sha(log)\n'
                    '                    and result["runnerSha256"] == runner_sha\n'
                    '                    and result["guardSha256"] == "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"\n'
                    '                    and result["waitTimeoutSeconds"] == 0.1\n')
        else:
            for before, after in (("悠々", "範囲"), ("ゆうゆう", "はんい"),
                                  ("悠久", "模範"), ("悠", "範")):
                replace(before, after)

        require("悠" not in text and "b122" not in text and "B122" not in text,
                f"Old selection leaked into {filename}")
        output = review_dir(123) / filename
        compile(text, str(output), "exec")
        outputs[output] = text.encode("utf-8")
        records.append({"source": str(source), "sourceSha256": expected,
                        "target": str(output), "targetSha256": sha(outputs[output]),
                        "scriptLineEndings": "LF; original source bytes remain unchanged",
                        "substitutions": changes})
    require(all(not path.exists() for path in outputs), "Preserve existing B123 source tools")
    for path, data in outputs.items():
        write_frozen(path, data)
    print(json.dumps(freeze_json(review_dir(123) / "source-tool-derivation.json", {
        "batch": 123, "derivations": records,
        "schemaAdaptation": "Four complete XML selections; curated-choice KD records are in the "
                            "comparison selection. Summary runner identity replaces the absent redundant "
                            "summary reproducibility flag; both actual manifest receipts and the rebuild "
                            "reproducibility flag remain mandatory. Added runner/guard/child-exit bindings.",
        "scope": "Prepared only; no candidate, source or review acceptance.",
    })))


def set_literal(values):
    return "{" + ", ".join(repr(value) for value in sorted(values)) + "}"


if __name__ == "__main__":
    main()
