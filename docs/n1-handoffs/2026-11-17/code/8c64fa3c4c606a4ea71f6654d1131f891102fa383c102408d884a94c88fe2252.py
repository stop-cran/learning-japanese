"""Inspect structural B131 inputs without reading author adjudication."""
import json
import re
from pathlib import Path

from common import WS, start_guard
from prepare_b131_source_facts import CANDIDATE, REPO, RUNNER, PREFIX
from verify_b131_sources import Git


def main():
    guard, _ = start_guard("B131 neutral schema inspection")
    git = Git(REPO, RUNNER, guard)
    try:
        for name in ("external-capture-bindings.json", "stroke-font-evidence.json",
                     "stroke-font-evidence-002.json", "source-rows.json"):
            value = json.loads(git("show", CANDIDATE + ":" + PREFIX + name))
            print("FILE", name)
            if name == "external-capture-bindings.json":
                print(json.dumps(value, ensure_ascii=False))
            else:
                print(json.dumps({k: (v if not isinstance(v, (list, dict)) else
                                      {"count": len(v), "sample": (v[:1] if isinstance(v, list)
                                                                  else list(v.items())[:1])})
                                  for k, v in value.items()}, ensure_ascii=False)
                      if isinstance(value, dict) else json.dumps(value[:1], ensure_ascii=False))
        for p in sorted((WS / "scratch-131" / "review" / "packet-verification-002" / "external").glob("*.html")):
            text = p.read_text("utf-8")
            print("EXTERNAL", p.name, len(text.encode("utf-8")),
                  re.findall(r"<article\b([^>]*)>", text))
        for name in ("review_chain.py", "audit-review.py", "check-report-structure.py",
                     "check-run-context.py", "test-review-chain.py",
                     "test-report-structure.py", "test-review-audit.py"):
            p = WS / "scratch-130" / "review" / name
            print("REFERENCE", name, p.stat().st_size)
    finally:
        guard.finish()


if __name__ == "__main__":
    main()
