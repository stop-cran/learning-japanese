"""Exact pre-build sizing of B133 confirmation chain variants; writes only a new sizing directory."""
import json
import subprocess
import sys
from pathlib import Path

import confirm_b133_v2 as controller
from common import WS, freeze_json, frozen, require, sha, start_guard

REVIEW = WS / "scratch-133" / "review"
REVISION = "110b4ffb6af078eb2adb00645db4c9e0bd6db188"
ALL_CARDS = "琴 鉛 滝 鉱 遅 円 速 声 激 岩 険 具 糸 緒 鉄 似 倣 機 線 索 液".split()
GPT_RETAINED_CARDS = "似 倣 機 線 索 液".split()
GPT_RETAINED_EXTRACTS = "似 似せる 倣 機 線 索 液".split()


def git(*args):
    return subprocess.run(["git", "-C", str(controller.REPO), *args], capture_output=True, check=True).stdout


def additional(index_path, index_sha, exclude=()):
    rows = json.loads(frozen(index_path, index_sha))["sources"]
    skip = {f"evidence/external/{name}-extract.txt" for name in exclude}
    return [{key: row[key] for key in ("source", "path", "sha256")} for row in rows if row["source"] not in skip]


def variants(bounded, derived):
    scoped = [card for card in ALL_CARDS if card not in GPT_RETAINED_CARDS]
    return {
        "complete": (ALL_CARDS, bounded() + derived()),
        "claude-claims-and-changes": (scoped, bounded(GPT_RETAINED_EXTRACTS) + derived()),
        "claude-claims-changes-plus-retained-cards": (ALL_CARDS, bounded(GPT_RETAINED_EXTRACTS) + derived()),
    }


def main(output, family, basis_path, bounded_sha, derived_sha):
    output = Path(output)
    require(output.parent == REVIEW and not output.exists(), "Use a new direct child of scratch-133/review")
    require(git("rev-parse", "HEAD").decode().strip() == REVISION and not git("status", "--porcelain=v1"),
            "Sizing requires the clean signed revision checkout")
    basis_text = frozen(basis_path).decode("utf-8")
    session = controller.INITIALS[family]["session"]
    refs, original, ids = controller.initial(family, session)
    events = Path.home() / ".copilot" / "session-state" / session / "events.jsonl"
    observed = controller.context(events.read_bytes(), family)
    delta = git("diff", "--no-color", controller.CANDIDATE, REVISION, "--", ".",
                ":(exclude)manifest.json", ":(exclude)docs")
    bounded = lambda exclude=(): additional(  # noqa: E731
        REVIEW / "confirmation-sources-002" / "index.json", bounded_sha, exclude)
    derived = lambda: additional(REVIEW / "confirmation-sources-003" / "index.json", derived_sha)  # noqa: E731
    run = f"N1-B133-{family.upper()}-CONFIRM-001"
    results = {}
    guard, _ = start_guard("B133 confirmation sizing")
    try:
        for name, (cards, extra) in variants(bounded, derived).items():
            revised = [f"kanji/{card}.md" for card in cards]
            spec = {"family": family, "run": run, "session": session, "candidate": REVISION,
                    "teachingChange": True, "scope": ["琴", "鉛", "滝"], "revisedSources": revised,
                    "additionalSources": extra, "basis": "adjudicated-initial",
                    "priorVerdict": controller.INITIALS[family]["verdict"], "basisText": basis_text}
            controller.validate_spec(spec)
            sources = [("initial-report/" + Path(refs["report"]["path"]).name, original, None),
                       ("diffs/fix.patch", delta, None)]
            sources += [("snapshot/" + path, git("show", f"{REVISION}:{path}"), None) for path in revised]
            sources += [(item["source"], frozen(item["path"], item["sha256"]), None) for item in extra]
            directory = output / name
            chain = controller.build_chain(sources, directory / "segments", directory / "chain.json", guard, name)
            controller.verify_chain(chain, sources)
            prompt = controller.render(spec, refs["report"], chain, directory / "prompt.txt",
                                       controller.REPORTS / (run + ".md"), ids)
            try:
                forecast = controller.capacity(observed, chain, len(prompt))
                status = forecast["status"]
            except Exception as error:  # record exact failure; the gate itself is unchanged
                forecast, status = {"error": str(error)}, "FAIL_CAPACITY"
            measured = controller.confirmation_cost(chain)
            results[name] = {
                "status": status, "cards": cards, "additionalSources": [item["source"] for item in extra],
                "sources": len(sources), "segments": len(chain["segments"]), "promptBytes": len(prompt),
                "estimatedChainTokens": measured["tokens"], "envelopeTokens": measured["envelopeTokens"],
                "lastInputTokens": observed["lastInputTokens"],
                "projectedPeak": (observed["lastInputTokens"] + measured["tokens"] + len(prompt)
                                  + controller.DRIFT_ALLOWANCE + controller.REPORT_ALLOWANCE),
                "gate": min(controller.STARTUP_GATE, controller.PROFILES[family]["maxPromptTokens"]),
                "forecast": forecast,
            }
    finally:
        require(not guard.finish()["breach"], "Sizing RAM breach")
    record = {"batch": 133, "family": family, "revision": REVISION, "eventsSha256": observed["eventsSha256"],
              "basis": {"path": str(basis_path), "sha256": sha(basis_text.encode("utf-8"))},
              "tool": {"path": __file__, "sha256": sha(Path(__file__).read_bytes())},
              "purpose": "Sizing only; no preflight, config, report, admission or reviewer contact.",
              "variants": results}
    print(json.dumps(freeze_json(output / "sizing.json", record)))
    for name, row in results.items():
        print(name, row["status"], row["segments"], row["promptBytes"], row["estimatedChainTokens"],
              row["projectedPeak"], row["gate"])


if __name__ == "__main__":
    main(*sys.argv[1:])
