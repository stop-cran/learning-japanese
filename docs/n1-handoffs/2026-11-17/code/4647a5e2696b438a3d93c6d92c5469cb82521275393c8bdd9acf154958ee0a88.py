"""Prepare the same fresh Claude reviewer's bounded reconciliation-003 continuation."""
import json

from b133_fresh_confirmation_v2 import (
    ADJUDICATION_SHA256, ADJUDICATION_SOURCE, CONTINUATION_RUN, PRIOR_REPORT_SOURCE,
    adjudication_path, prior,
)
from common import freeze_json, frozen, require
from confirm_b133_fresh_v2 import OUT, validate_spec

REVISION = "b1acf155fb8c7e1066a5c3baf88ae98ab92c29ac"
BASIS = (
    "Your CONFIRM-002 on d7d6cff92afe8220c16a5daa76f1c3f00a2bef30 returned UNVERIFIED. "
    "Its report and evidence-only coordinator adjudication are supplied separately. The source check "
    "confirmed that 日本国語大辞典 たきすい【滝水】 names an Edo sake, not water from a waterfall; "
    "the latter meanings belong to the separate たきみず and ろうすい entries. Owner-signed revision "
    + REVISION + ", the sole child of d7d6cff9, corrects the 滝 Meaning sentence and 液 Note rationale, "
    "appends 酒 after 液 in quiz_exclusions with one qualified Note, and adds a 滝水 citation. No other "
    "runtime article changed. The evidence/revision-proof-003.json and diffs/reconciliation-003.patch "
    "bind that exact delta; diffs/fix.patch is cumulative from ad047ace. "
    "evidence/coordinator-dispositions-003.json supersedes the earlier dispositions only for the 滝-液 "
    "rationale and the new 滝-酒 decision. It contains 19 pair decisions: 13 added precautions and six "
    "retained distinctions. Review all 19 on the actual b1acf155 snapshot, including every Note and "
    "qualification, the corrected abbreviation and its citation, and the disclosed 鉛-具 cross-pair. "
    "Explicitly judge the retained 鉛-鉄, 鉛-似, 鉛-倣, 琴-機, 琴-線 and 琴-索 distinctions. "
    "Check the five JMdict identities newly cited by the reconciliation (1396980,1404975,1380440,"
    "1244950,1343610) against the complete signed reconciliation families. State whether each prior "
    "CONFIRM-002 observation still applies, and give the original C1-C3 and O1-O4 dispositions. "
    "The earlier L8 locator observation was checked: the existing :12/:17 references were correct; "
    "no change to those pointers was made. Verify rather than inherit that conclusion. "
    "The original Claude initial review and CONFIRM-001 are historical evidence from another session, "
    "not your own firsthand review. Complete selected publisher sections and full selected JMdict "
    "families are supplied, not whole pages, HTML/layout/images or a fresh whole-dictionary/KANJIDIC2 "
    "reread. Earlier unchanged citations remain outside the reconciliation citation audit. "
    "Precautions are quiz-safety guards, not universal synonymy claims. Independently check all supplied "
    "claims and disclose unresolved uncertainty; no verdict is required or presumed."
)


def main():
    spec = json.loads(frozen(OUT / "N1-B133-CLAUDE-CONFIRM-002-spec.json"))
    gpt = json.loads(frozen(OUT / "N1-B133-GPT-CONFIRM-003-spec.json"))
    final, _ = prior()
    require(gpt["candidate"] == REVISION and spec["session"] == final["session"],
            "Revision or continuation session differs")
    additions = [
        row for row in gpt["additionalSources"]
        if row["source"] in (
            "evidence/coordinator-dispositions-003.json", "evidence/revision-proof-003.json",
            "diffs/reconciliation-003.patch", "evidence/external/takisui-sections.txt",
        )
    ]
    require(len(additions) == 4, "Missing current revision source")
    additions.extend([
        {"source": PRIOR_REPORT_SOURCE, **final["report"]},
        {"source": ADJUDICATION_SOURCE, "path": str(adjudication_path()),
         "sha256": ADJUDICATION_SHA256},
    ])
    spec.update(run=CONTINUATION_RUN, candidate=REVISION, basisText=BASIS)
    spec["revisedSources"].append("kanji/酒.md")
    spec["additionalSources"].extend(additions)
    require(len(spec["revisedSources"]) == len(set(spec["revisedSources"])),
            "Duplicate revised source")
    names = [row["source"] for row in spec["additionalSources"]]
    require(len(names) == len(set(names)) and all("gpt" not in name.lower() for name in names),
            "Duplicate source or other-family evidence")
    for row in spec["additionalSources"]:
        frozen(row["path"], row["sha256"])
    validate_spec(spec)
    print(json.dumps(freeze_json(OUT / (CONTINUATION_RUN + "-spec.json"), spec)))


if __name__ == "__main__":
    main()
