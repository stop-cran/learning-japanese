"""Prepare the core chain or a mechanically selected extension; never launch a reviewer."""
import argparse
import importlib.util
import json
import stat
from pathlib import Path

from review_chain import build_chain, digest, validate_selection

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent / "review-packets" / "batch-114-8c2bdc27"
PACKET_SHA = "eb6b1042060f561cd6ff49054d0e11533c15008ea0f6bbc064b07614b1701e15"


def freeze_json(path, value):
    with path.open("xb") as stream:
        stream.write((json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    path.chmod(stat.S_IREAD)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--reply", type=Path)
    parser.add_argument("--run")
    parser.add_argument("--phase1-audit", type=Path)
    parser.add_argument("--records-root", type=Path, default=HERE, help="Synthetic tests only")
    parser.add_argument("--chains-root", type=Path, default=HERE.parent / "review-chains", help="Synthetic tests only")
    args = parser.parse_args(argv)
    records, chains = args.records_root, args.chains_root
    if args.reply and (not args.run or not args.phase1_audit):
        parser.error("Extension preparation requires --reply, --run and --phase1-audit")
    if args.run and not args.run.replace("-", "").isalnum():
        parser.error("Run identifier must contain letters, digits or hyphens only")
    guard_path = HERE.parent / "rollout-recovered" / "learning-japanese" / "docs" / "n1-reviews" / "batch-113-publication" / "verify-zip-streaming.py"
    spec = importlib.util.spec_from_file_location("published_ram_guard", guard_path)
    resource = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resource)
    guard = resource.RamGuard()
    guard.start()
    try:
        manifest_bytes = (PACKET / "SHA256SUMS.json").read_bytes()
        assert digest(manifest_bytes) == PACKET_SHA
        sums = json.loads(manifest_bytes)
        for relative, expected in sums.items():
            guard.check()
            path = PACKET / Path(relative)
            assert digest(path.read_bytes()) == expected, relative
            assert not path.stat().st_mode & stat.S_IWRITE, relative
        reference = json.loads((PACKET / "eligibility-reference.json").read_bytes())
        packet = json.loads((PACKET / "packet.json").read_bytes())
        members = packet["newKanji"]
        sources, missing = [], []

        def add(relative, last=None, display=None):
            data = (PACKET / Path(relative)).read_bytes()
            assert digest(data) == sums[relative], relative
            sources.append((display or relative, data, last))

        if args.reply:
            assert not args.reply.stat().st_mode & stat.S_IWRITE
            assert not args.phase1_audit.stat().st_mode & stat.S_IWRITE
            reply_bytes = args.reply.read_bytes()
            phase1_bytes = args.phase1_audit.read_bytes()
            phase1 = json.loads(phase1_bytes)
            assert phase1["status"] == "PHASE1_READY" and phase1["breaches"] == []
            assert phase1["phase1ListSha256"] == digest(reply_bytes)
            selection = validate_selection(reply_bytes.decode("utf-8"), reference)
            if not selection["valid"]:
                freeze_json(records / f"{args.run}-extension-void.json", {
                    "status": "VOID", "run": args.run, "extensionBuilt": False,
                    "replySha256": digest(reply_bytes), "errors": selection["errors"],
                    "quarantine": "No observations may become review evidence, reconciliation input or later hints.",
                })
                raise ValueError("Invalid list; no extension created")
            for entry in selection["entries"]:
                relative = f"repo/kanji/{entry['character']}.md"
                if relative not in sums:
                    missing.append(entry["requestLine"])
                else:
                    add(relative, display=f"{relative} [{entry['label']}]")
            directory = chains / f"b114-{args.run}-extension"
            manifest_path = records / f"{args.run}-extension.json"
            message_path = records / f"{args.run}-phase2-message.txt"
            assert not message_path.exists()
            label = f"B114 {args.run} extension"
        else:
            for relative in ("REVIEW.md", "packet.json", "rubric/copilot-instructions.md",
                             "rubric/content-structure.instructions.md"):
                add(relative)
            add("repo/docs/content-format.md", 139)
            add("repo/docs/jlpt-levels.md")
            for c in members:
                add(f"snapshot/kanji/{c}.md")
            for c in members:
                add(f"snapshot/strokes/{c}.json")
            add("diffs/existing.diff")
            for relative in packet["modifiedExisting"]:
                add(f"snapshot/{relative}")
            for name in ("lint", "quiz-safety", "linkplan", "reading-exposure-final", "unittest",
                         "validate", "manifest", "manifest-rebuild", "budget", "vocabulary"):
                add(f"checks/{name}.txt")
            for name in ("source-metadata.json", "kanjidic2-records.xml", "jmdict-families.xml",
                         "dictionary-index.json", "joyo-rows.json", "shape-evidence.json",
                         "provenance.json", "title-index.txt"):
                add(f"evidence/{name}")
            curated = list(dict.fromkeys(c for row in reference["cards"] for c in row["distractors"]))
            for c in curated:
                add(f"repo/kanji/{c}.md")
            directory = chains / "b114-initial-v1"
            manifest_path = records / "core-chain.json"
            label = "B114 required core"
        chain = build_chain(sources, directory, manifest_path, guard, label)
        guard.check()
        if args.reply:
            message = chain["segments"][0]["path"] + "\n" + (
                "Missing entries:\n" + "\n".join(missing) if missing else "Missing entries: none")
            with message_path.open("xb") as stream:
                stream.write(message.encode("utf-8"))
            message_path.chmod(stat.S_IREAD)
        memory = guard.finish()
        memory["peakScope"] = "Chain-builder Python process including its monitor thread."
        memory["additionalChecks"] = "During packet verification, source segmentation and segment writing, plus phase boundaries."
        record = {
            "packetManifestSha256": PACKET_SHA, "chainManifest": str(manifest_path),
            "chainManifestSha256": digest(manifest_path.read_bytes()),
            "firstSegment": chain["segments"][0]["path"], "segments": len(chain["segments"]),
            "sources": len(chain["sources"]), "missingVerbatim": missing, "memory": memory,
        }
        if args.reply:
            record.update(replySha256=digest(reply_bytes), phase1AuditSha256=digest(phase1_bytes),
                          phase2Message=str(message_path), phase2MessageSha256=digest(message_path.read_bytes()))
        freeze_json(records / (f"{args.run}-extension-preflight.json" if args.reply else "core-chain-preflight.json"), record)
        print(json.dumps(record, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
