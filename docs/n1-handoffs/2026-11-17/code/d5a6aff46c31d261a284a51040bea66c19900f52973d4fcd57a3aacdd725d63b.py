"""Render batch N's Claude and GPT review prompts, kickoffs and audit configs from the accepted B116 GPT-004 prompt.

The template is the frozen GPT-004 prompt with counted literal replacements. Before rendering batch N, the same
value functions are applied to the B116 s1 packet and chain; the result must equal the original prompt bytes.
Usage: python -B build-prompts-v2.py <batch>
"""
import datetime
import json
import re
import sys
from pathlib import Path

from common import (CHECKS, COORDINATOR, SNAP, TOOLS, WS, freeze_json, frozen, json_bytes, load_batch, packet_dir,
                    require, review_dir, sha, verify_packet, word, write_frozen)

SOURCE = WS / "scratch-116" / "prompts-116" / "initial-gpt-116-004.txt"
SOURCE_SHA = "0504bacc8d11cea917d7504d8631774f90913cbd569fe5f561562f70a665caaf"
B116_PACKET = WS / "review-packets" / "batch-116-9e18d940-s1"
B116_CHAIN = WS / "scratch-116" / "core-chain-s1.json"
B116_CHAIN_SHA = "103879a8b64fc23f59e9debb8675688be612d5453ae6d92fc51953436c62b23b"
REF_HEAD = ("ELIGIBILITY REFERENCE (exact bytes of the packet's eligibility-reference.json: mechanically extracted "
            "original frontmatter, in card order):\n")
REF_END = "END ELIGIBILITY REFERENCE"
RUNS = {"claude": ("CLAUDE", "claude-opus-5.5", "Claude"), "gpt": ("GPT", "gpt-6.1-sol", "GPT")}
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


def wrappers(diff, members):
    articles, current = {}, None
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
            articles[current] = []
        elif current and line.startswith("+") and not line.startswith("+++"):
            articles[current] += [c for c in members for _ in range(line.count(f"](../kanji/{c}.md)"))]
        elif current and line.startswith("-") and not line.startswith("---"):
            for c in members:
                for _ in range(line.count(f"](../kanji/{c}.md)")):
                    articles[current].remove(c)
    return articles


def plural(n, noun):
    return f"{word(n)} {noun}" + ("" if n == 1 else "s")


def values(root, chain, run, prompt_path, report, extra_reads=None):
    packet = json.loads((root / "packet.json").read_bytes())
    reference = (root / "eligibility-reference.json").read_bytes().decode("utf-8")
    cards = json.loads(reference)["cards"]
    members, modified, unchanged = packet["newKanji"], packet["modifiedExisting"], packet["supportingUnchanged"]
    titles = (root / "evidence" / "title-index.txt").read_bytes()
    lines = titles.decode("utf-8").split("\n")[:-1]
    per_article = wrappers((root / "diffs" / "existing.diff").read_bytes().decode("utf-8"), members)
    total = sum(map(len, per_article.values()))
    stems = [Path(u).stem for u in unchanged]
    words_reads = f"the {plural(len(modified), 'changed snapshot' + chr(92) + 'words article')} " \
                  f"({plural(total, 'wrapper')} in total); "
    words_reads += "".join(f"the complete unchanged repo\\words\\{s}.md as supporting evidence; " for s in stems)
    check = (f"Check the {plural(total, 'link wrapper')} across {plural(len(modified), 'word-article change')} in "
             "diffs\\existing.diff against the complete changed articles, for correct targets and no other change.")
    for article, linked in per_article.items():
        if len(linked) == 2:
            check += f" Both {linked[0]} and {linked[1]} links are added to the same {Path(article).stem} article."
        elif len(linked) > 2:
            check += f" The {' '.join(linked)} links are all added to the same {Path(article).stem} article."
    if stems:
        check += f" Use unchanged {', '.join(stems)} as supporting evidence, not a new or modified article."
    slots = [c for row in cards for c in row["distractors"]]
    sources = [s["source"] for s in chain["sources"]]
    if extra_reads is None:
        supplied = sum(s.startswith(f"{SNAP}/") and s.endswith("-extract.txt") for s in sources)
        extra_reads = ("\nLast, the supplied external snapshots: evidence\\external-snapshots\\manifest.json, then "
                       + (f"each of its {plural(supplied, 'SUPPLIED complete Weblio source-section extract')} in index order."
                          if supplied else "no extract (none was supplied).")
                       + " These are the only external sources for this pass.")
    return {
        "RUN": run, "PACKET": str(root), "SNAPSHOT": packet["candidate"], "BASE": packet["base"],
        "SUMS": sha((root / "SHA256SUMS.json").read_bytes()), "REPORT": str(report), "PROMPT_PATH": str(prompt_path),
        "FIRST_SEGMENT": chain["segments"][0]["path"], "SEGMENTS": str(len(chain["segments"])),
        "NEW_KANJI_PHRASE": f"the {word(len(members))} new kanji ({' '.join(members)})", "N_WORD": word(len(members)),
        "WORDS_READS": words_reads, "CHECKS": ", ".join(s[7:-4] for s in sources if s.startswith("checks/")),
        "TITLE_SHA": sha(titles), "TITLE_COUNT": str(len(lines)), "TITLE_FIRST": lines[0], "TITLE_LAST": lines[-1],
        "C_LINE": f"All {len(slots)} curated distractor slots ({len(set(slots))} distinct repo\\kanji copies): "
                  + " / ".join(f"{row['card']}: {' '.join(row['distractors'])}" for row in cards) + ".",
        "EXTRA_READS": extra_reads, "REFERENCE": reference, "WRAPPER_CHECK": check,
        "CARD_ROWS": "".join(f"| {c} | <{c}-correctness-verdict> | <{c}-coverage-verdict> | <{c}-consistency-verdict> "
                             f"| <{c}-comprehensibility-verdict> | <{c}-evidence> |\n" for c in members),
        "BATCH": f"B{packet['batch']}",
    }


def template(source, b116):
    text = source
    require("{{" not in text, "Source already contains a placeholder")
    head, rest = text.split(REF_HEAD, 1)
    reference, tail = rest.split(REF_END, 1)
    require(reference == b116["REFERENCE"], "Reference bytes differ")
    text = head + REF_HEAD + "{{REFERENCE}}" + REF_END + tail
    rules = [(b116["CARD_ROWS"], "{{CARD_ROWS}}", 1), (b116["C_LINE"] + "\n", "{{C_LINE}}{{EXTRA_READS}}\n", 1),
             (b116["WRAPPER_CHECK"], "{{WRAPPER_CHECK}}", 1), (b116["WORDS_READS"], "{{WORDS_READS}}", 1),
             (b116["NEW_KANJI_PHRASE"], "{{NEW_KANJI_PHRASE}}", 1), (b116["PACKET"], "{{PACKET}}", 1),
             (b116["PROMPT_PATH"], "{{PROMPT_PATH}}", 1), (b116["REPORT"], "{{REPORT}}", 1),
             (b116["FIRST_SEGMENT"], "{{FIRST_SEGMENT}}", 1), (b116["SNAPSHOT"], "{{SNAPSHOT}}", 1),
             (b116["BASE"], "{{BASE}}", 1), (b116["SUMS"], "{{SUMS}}", 1), (b116["TITLE_SHA"], "{{TITLE_SHA}}", 1),
             (b116["CHECKS"], "{{CHECKS}}", 1), (b116["RUN"], "{{RUN}}", 3),
             ("all 18 segments", "all {{SEGMENTS}} segments", 1), ("segment 18 ends", "segment {{SEGMENTS}} ends", 1),
             ("all 18 core segments", "all {{SEGMENTS}} core segments", 2),
             ("their three snapshot\\strokes", "their {{N_WORD}} snapshot\\strokes", 1),
             ("three new cards", "{{N_WORD}} new cards", 5),
             ("the 1232 same-commit", "the {{TITLE_COUNT}} same-commit", 1),
             ("lines 1-1232", "lines 1-{{TITLE_COUNT}}", 1), ("line 1232 is", "line {{TITLE_COUNT}} is", 1),
             (f"\"{b116['TITLE_FIRST']}\"", "\"{{TITLE_FIRST}}\"", 1),
             (f"\"{b116['TITLE_LAST']}\"", "\"{{TITLE_LAST}}\"", 1), ("B116", "{{BATCH}}", None)]
    counts = []
    for literal, replacement, expected in rules:
        count = text.count(literal)
        require(count and (expected is None or count == expected), f"Count {count} for {literal[:60]!r}")
        text = text.replace(literal, replacement)
        counts.append({"literal": literal, "placeholder": replacement, "count": count})
    stripped = PLACEHOLDER.sub("", text)
    for token in ("116", "1232", "three", "憲", "監", "督", "責", "9e18d940", "18 "):
        require(token not in stripped, f"Residual batch-specific token {token!r}")
    return text, counts


def render(text, value_map):
    used = set(PLACEHOLDER.findall(text))
    require(used == set(value_map), f"Placeholder set mismatch: {sorted(used ^ set(value_map))}")
    return PLACEHOLDER.sub(lambda m: value_map[m[1]], text)


def main(batch):
    config = load_batch(batch)
    n, records = config["batch"], review_dir(batch)
    prompts = records / "prompts"
    require(not prompts.exists(), "Prompts already built; preserve them")
    source = frozen(SOURCE, SOURCE_SHA).decode("utf-8")
    b116_chain = json.loads(frozen(B116_CHAIN, B116_CHAIN_SHA))
    b116 = values(B116_PACKET, b116_chain, "N1-B116-GPT-004", SOURCE,
                  WS / "reports-116" / "initial-gpt-004.md", extra_reads="")
    text, counts = template(source, b116)
    require(render(text, b116) == source, "B116 render-equality proof failed")
    root, _, packet_sha = verify_packet(config)
    chain = json.loads(frozen(records / "core-chain.json"))
    preflight_core = json.loads(frozen(records / "core-chain-preflight.json"))
    require(preflight_core["packetManifestSha256"] == packet_sha
            and preflight_core["chainManifestSha256"] == sha((records / "core-chain.json").read_bytes()),
            "Core chain is not bound to this packet")
    require([s["source"][7:-4] for s in chain["sources"] if s["source"].startswith("checks/")] == list(CHECKS),
            "Check order differs")
    reports = WS / f"reports-{n}"
    tools = sorted(TOOLS.glob("*.py"))
    bound = [*tools, *(records / name for name in (
        "review_chain.py", "audit-review.py", "check-report-structure.py", "check-run-context.py",
        "test-review-chain.py", "test-report-structure.py", "test-review-audit.py", "tooling-derivation.json",
        "batch.json", "packet-build.json", "core-chain.json", "core-chain-preflight.json")),
        records / "snapshots" / "fetch-record.json", root / "SHA256SUMS.json", root / "eligibility-reference.json",
        root / SNAP / "manifest.json"]
    files = [{"path": str(p), "sha256": sha(frozen(p))} for p in bound]
    outputs, runs = {}, {}
    for key, (label, model, name) in RUNS.items():
        run = f"N1-B{n}-{label}-001"
        prompt_path = prompts / f"initial-{key}-001.txt"
        kickoff_path = prompts / f"kickoff-{key}-001.txt"
        report = reports / f"initial-{key}-001.md"
        rendered = render(text, values(root, chain, run, prompt_path, report)).encode("utf-8")
        kickoff = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, then "
                   "follow its instructions. No other tool call may precede that read.").encode("ascii")
        audit = {
            "run": run, "kickoff": str(kickoff_path), "prompt": str(prompt_path), "report": str(report),
            "coordinator": COORDINATOR, "expectedFamily": key, "coreManifest": str(records / "core-chain.json"),
            "reference": str(root / "eligibility-reference.json"), "completionContract": "entire-message-enum-v1",
            "completionContractScope": "coordinator-tool-message-only", "reportStructureContract": "report-structure-v1",
            "reportStructureChecker": str(records / "check-report-structure.py"),
            "files": files + [{"path": str(prompt_path), "sha256": sha(rendered)},
                              {"path": str(kickoff_path), "sha256": sha(kickoff)}],
            "maxWebFetches": 0,
        }
        outputs[prompt_path], outputs[kickoff_path] = rendered, kickoff
        outputs[prompts / f"audit-config-{run}.json"] = json_bytes(audit)
        runs[key] = {"run": run, "prompt": str(prompt_path), "promptSha256": sha(rendered),
                     "kickoff": str(kickoff_path), "kickoffText": kickoff.decode("ascii"),
                     "auditConfig": str(prompts / f"audit-config-{run}.json"), "report": str(report),
                     "launch": {"mode": "interactive", "model": model, "contextTier": "long_context",
                                "freshSession": True, "sessionName": f"B{n} {name} review 001"}}
    require(outputs[prompts / "initial-claude-001.txt"].replace(b"CLAUDE", b"GPT").replace(b"-claude-", b"-gpt-")
            == outputs[prompts / "initial-gpt-001.txt"], "Claude and GPT prompts differ beyond identity")
    reports.mkdir(exist_ok=True)
    require(not any(reports.iterdir()), "Report directory is not empty")
    template_bytes = text.encode("utf-8")
    for path, data in outputs.items():
        write_frozen(path, data)
    write_frozen(prompts / "template.txt", template_bytes)
    record = {
        "batch": n, "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "packetManifestSha256": packet_sha, "coreChainSha256": sha((records / "core-chain.json").read_bytes()),
        "template": {"source": str(SOURCE), "sourceSha256": SOURCE_SHA, "templateSha256": sha(template_bytes),
                     "replacements": counts, "b116RenderEqualsSource": True},
        "blindness": "Same accepted GPT-004 prompt form; only batch identity, counts, paths, the eligibility reference, "
                     "the curated-slot list and a neutral external-snapshot read line differ. No verdict, finding, "
                     "comparison, source answer or earlier observation is supplied.",
        "runs": runs, "reportDirectory": str(reports), "order": ["claude", "gpt"],
        "builder": {"path": str(TOOLS / "build-prompts-v2.py"), "sha256": sha((TOOLS / "build-prompts-v2.py").read_bytes())},
    }
    freeze_json(prompts / "preflight.json", record)
    print(json.dumps(record, ensure_ascii=False, indent=1)[:4000])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
