"""Derive B124 closure with explicit local-only retention for complete external extracts."""
from pathlib import Path

from common import freeze_json, frozen, sha
from derive_selected_followups import derive_file

HERE = Path(__file__).resolve().parent


def main():
    frozen(HERE / "close_selected_v2.py",
           "7f24099af81d105533ed4fb7797d53a9827ee7710fea94380ad1c59113f5a896")
    frozen(HERE / "archive_b124_chains.py",
           "5a5eed9018e2227e110a8c45b711fe4abc965f9a37f57c7daef1422c4b698909")
    old_chain = '''    def chain(path, name):
        manifest = read(path)
        copy(path, f"{name}/manifest.json")
        for segment in manifest["segments"]:
            raw = frozen(Path(segment["path"]), segment["sha256"])
            packed = gzip.compress(raw, mtime=0)
            require(gzip.decompress(packed) == raw, "Chain compression mismatch")
            put(f"{name}/{Path(segment['path']).name}.gz", packed)
        return {"path": name, "segments": len(manifest["segments"]),
                "manifestSha256": sha(frozen(path))}
'''
    new_chain = '''    def chain(path, name):
        manifest_raw = frozen(path)
        manifest = json.loads(manifest_raw)
        files, retention = prepare_public_chain(manifest_raw, {
            segment["path"]: frozen(Path(segment["path"]), segment["sha256"])
            for segment in manifest["segments"]
        })
        for relative, raw in files.items():
            put(f"{name}/{relative}", raw)
        return {"path": name, "segments": retention["originalSegments"],
                "manifestSha256": sha(manifest_raw),
                "archivedSegmentIndices": retention["archivedSegmentIndices"],
                "localOnlySegmentIndices": [item["index"] for item in retention["localOnlySegments"]],
                "retentionSha256": sha(files["retention.json"])}
'''
    closure = derive_file("close_selected_v2.py", "close_b124.py", [
        ('"""Archive verified initial reviews, adjudicated intermediate confirmations and accepted final confirmations."""',
         '"""Archive B124 review evidence with complete external-snapshot segments retained locally."""'),
        ("from close_v4 import require_historical_confirmation\n",
         "from close_v4 import require_historical_confirmation\n"
         "from archive_b124_chains import prepare as prepare_public_chain\n"),
        ("    config = load_batch(batch)\n",
         '    require(batch == 124, "This closure adapter is limited to B124")\n'
         "    config = load_batch(batch)\n"),
        (old_chain, new_chain),
        ('                     "test_selected_followups.py"):',
         '                     "test_selected_followups.py", "close_b124.py",\n'
         '                     "archive_b124_chains.py", "test_archive_b124_chains.py",\n'
         '                     "test_close_b124.py", "prepare_b124_closure.py",\n'
         '                     "b124-closure-derivation.json"):'),
        ('            "representation": "Reports, prompts and receipts are byte-exact. Complete delivered sources "\n'
         '                              "are in losslessly gzipped chains. Raw execution payloads remain local; "\n'
         '                              "audit summaries are explicit bounded derivatives.",',
         '            "representation": "Reports, prompts and receipts are byte-exact. Published chain "\n'
         '                              "segments are losslessly gzipped. Complete external-snapshot "\n'
         '                              "sections and co-located source material remain local; original "\n'
         '                              "hashes and ranges are preserved. Per-chain retention.json states "\n'
         '                              "the archived and local-only segments. Raw execution payloads remain "\n'
         '                              "local; audit summaries are explicit bounded derivatives.",'),
    ])
    tests = derive_file("test_close.py", "test_close_b124.py", [
        ("from close import require_confirmation, require_intermediate",
         "from close_b124 import require_confirmation, require_intermediate"),
        ('if __name__ == "__main__":',
         'class BatchScopeTests(unittest.TestCase):\n'
         '    def test_other_batch_is_refused_before_any_archive_write(self):\n'
         '        from close_b124 import archive\n'
         '        with self.assertRaisesRegex(ValueError, "limited to B124"):\n'
         '            archive(123, "a" * 40, [], preflight_path=None)\n'
         '\n\nif __name__ == "__main__":'),
    ])
    print(freeze_json(HERE / "b124-closure-derivation.json", {
        "derivations": [closure, tests],
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "retentionHelper": {
            "path": str(HERE / "archive_b124_chains.py"),
            "sha256": sha(frozen(HERE / "archive_b124_chains.py")),
        },
        "scope": "Reversible derivation. All review acceptance, identity, lineage, context, "
                 "structure, source-hash and memory gates remain unchanged. Only B124 may "
                 "use this adapter. Complete external-snapshot segments are kept local "
                 "with explicit per-chain retention metadata. No closure is executed here.",
    }))


if __name__ == "__main__":
    main()
