"""Build one family's frozen B114 confirmation read chain; never launch a reviewer."""
import argparse
import importlib.util
import json
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from review_chain import build_chain, digest  # noqa: E402

WORKSPACE = HERE.parent.parent
ORIGINAL = WORKSPACE / "review-packets" / "batch-114-8c2bdc27"
ORIGINAL_SHA = "eb6b1042060f561cd6ff49054d0e11533c15008ea0f6bbc064b07614b1701e15"
PACKETS = {
    "claude": ("confirm-114-ac38b8e4-claude", "048056af4b6ae9f751bf748be673ff7e1d2b2d869961cf882bccca8144da4767",
               "initial-claude.md", "c021b162371ff4276f2ca3ec3da754f62cbacb4e924b0e9f1abbaa100b92dbfa", "房庁部課集拾利績怪穂盤板気"),
    "gpt": ("confirm-114-ac38b8e4-gpt", "64a114e8abfa3f2a743abb8b8c6b7b6432c0bc01b91bdde1350595a9cec0b779",
            "initial-gpt.md", "aa409e26a4ef70ff11d76988b5b45fec01e567aff04d65fdff5d371f13bd35be", "房庁部課集拾利績怪穂盤板"),
}
CHECKS = ("budget.txt", "link-targets.tsv", "lint.txt", "manifest.txt", "quiz-safety.txt", "reading-exposure.txt",
          "reading-options.txt", "unittest.txt", "validate.txt", "vocabulary.txt")


def frozen(path, expected):
    assert not path.stat().st_mode & stat.S_IWRITE, path
    data = path.read_bytes()
    assert digest(data) == expected, path
    return data


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("family", choices=sorted(PACKETS))
    args = parser.parse_args(argv)
    name, packet_sha, report_name, report_sha, counterparts = PACKETS[args.family]
    packet = WORKSPACE / "review-packets" / name
    guard_path = (WORKSPACE / "rollout-recovered" / "learning-japanese" / "docs" / "n1-reviews"
                  / "batch-113-publication" / "verify-zip-streaming.py")
    spec = importlib.util.spec_from_file_location("published_ram_guard", guard_path)
    resource = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resource)
    guard = resource.RamGuard()
    guard.start()
    try:
        manifest = json.loads(frozen(packet / "packet-manifest.json", packet_sha))
        files = manifest["files"]
        on_disk = {p.relative_to(packet).as_posix() for p in packet.rglob("*") if p.is_file()}
        assert on_disk == set(files) | {"packet-manifest.json"}, on_disk ^ set(files)
        sums = json.loads(frozen(ORIGINAL / "SHA256SUMS.json", ORIGINAL_SHA))
        sources, used = [], []

        def confirm(relative, last=None):
            guard.check()
            sources.append((f"confirm-packet/{relative}", frozen(packet / relative, files[relative]["sha256"]), last))
            used.append(relative)

        def original(relative, last=None):
            guard.check()
            sources.append((f"original-packet/{relative}", frozen(ORIGINAL / relative, sums[relative]), last))

        confirm("INSTRUCTIONS.md")
        sources.append((f"initial-report/{report_name}",
                        frozen(WORKSPACE / "reports-114" / report_name, report_sha), None))
        for relative in ("RESPONSE.md", "CHANGES.md", "diffs/fix.patch", "diffs/changed-lines.txt",
                         "diffs/changed-files.txt"):
            confirm(relative)
        for card in manifest["members"]:
            confirm(f"snapshot/kanji/{card}.md")
        for card in counterparts:
            original(f"repo/kanji/{card}.md")
        for check in CHECKS:
            confirm(f"checks/{check}")
        for relative in ("evidence/README.md", "evidence/jmdict-cited-entries.xml", "evidence/QuizBuilder.kt"):
            confirm(relative)
        for relative in ("rubric/copilot-instructions.md", "rubric/content-structure.instructions.md"):
            original(relative)
        original("repo/docs/content-format.md", 139)
        for relative in ("evidence/kanjidic2-records.xml", "evidence/jmdict-families.xml",
                         "evidence/title-index.txt"):
            original(relative)
        assert sorted(used) == sorted(files), set(files) ^ set(used)
        directory = WORKSPACE / "review-chains" / f"b114-confirm-{args.family}-v1"
        manifest_path = HERE / f"{args.family}-chain.json"
        chain = build_chain(sources, directory, manifest_path, guard, f"B114 {args.family} confirmation")
        guard.check()
        memory = guard.finish()
        memory["peakScope"] = "Chain-builder Python process including its monitor thread."
        record = {
            "family": args.family, "packet": str(packet), "packetManifestSha256": packet_sha,
            "originalSumsSha256": ORIGINAL_SHA, "initialReportSha256": report_sha,
            "chainManifest": str(manifest_path), "chainManifestSha256": digest(manifest_path.read_bytes()),
            "firstSegment": chain["segments"][0]["path"], "segments": len(chain["segments"]),
            "sources": len(chain["sources"]), "memory": memory,
        }
        out = HERE / f"{args.family}-chain-preflight.json"
        with out.open("xb") as stream:
            stream.write((json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        out.chmod(stat.S_IREAD)
        print(json.dumps(record, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
