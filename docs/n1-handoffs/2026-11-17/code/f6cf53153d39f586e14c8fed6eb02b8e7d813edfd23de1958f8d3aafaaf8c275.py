"""Record substantive adjudication of the original Claude confirmation after its final audit."""
import datetime
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha

OUT = WS / "scratch-131" / "review" / "confirm-003"
RUN = "N1-B131-CLAUDE-CONFIRM-003"


def main():
    final_path = OUT / (RUN + "-final.json")
    final = json.loads(frozen(final_path))
    require(final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["confirmation"] == "CONFIRMED"
            and final["candidate"] == "88a9dfab6a783b082659b742a24242342bb2e461", "Unexpected final")
    report = frozen(final["report"]["path"], final["report"]["sha256"])
    structure = json.loads(frozen(final["structure"]["path"], final["structure"]["sha256"]))
    require(structure["status"] == "PASS" and not structure["nonAccepting"] and structure["findings"] == 0,
            "Structure is not an accepting confirmation")
    frozen(final["audit"]["path"], final["audit"]["sha256"])
    frozen(final["context"]["path"], final["context"]["sha256"])
    adjudication = {
        "run": RUN, "method": "Every cited source line was reconstructed from the verified hash-bound chain "
                              "segments and read by the coordinator; six cited JMdict entry IDs in Basis were "
                              "located in the supplied complete record file.",
        "dispositions": {
            "F1": "ACCEPTED: 霜.md:14 adds 氷/凍; 84-86 qualified note; Daijisen sense 1 (line 12) ice crystals.",
            "F2": "ACCEPTED: 衛.md:14 adds 援; 79-80 qualified; JMdict 援護 sense 2 covering/protection, 救援 relief/rescue.",
            "O1": "ACCEPTED: decline retains conservative structure-unclassified tags; 羊 unchanged per verification.",
            "O2": "ACCEPTED: 循 guard; Daijisen 衛 sense 2 周りをまわる・取り巻く (line 8); 循環 circulation/rotation/loop.",
            "O3": "ACCEPTED: 酒 guard with register qualification matching 隠語大辞典 Meiji-and-later disclosure.",
        },
        "basisChecks": "番 watch/guard/lookout (2022640), 送る to see off/escort (1402730), 卒する to die "
                       "formal (1405880), 枯れる to die (1267220), 久しい long elapsed time (1227340), "
                       "涼 cool air (2729660) are all present with the stated glosses.",
        "citationImprecision": "F1 cites external-05-01.txt:11-12 for refrigerator frost; that is Daijisen "
                               "sense 2 at line 13 of the same supplied article. Non-consequential: the claim "
                               "is true in the cited source and sense 1 alone supports the ice relation.",
        "limitsRetained": "L1-L6 retained, including the unreread non-selected records, six latent reading "
                          "collisions, no caller/custom/multi-borrow/native/device/APK claim and the "
                          "corrected 衛 U+885B erratum.",
        "q2Scope": "The bounded 霜/冴 non-collision is assessed only by the second family's own Q2 question.",
    }
    adjudication_binding = freeze_json(OUT / (RUN + "-adjudication.json"), adjudication)
    print(json.dumps(freeze_json(OUT / (RUN + "-acceptance.json"), {
        "run": RUN, "batch": 131, "candidate": final["candidate"],
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "session": final["session"], "reviewAccepted": True, "confirmation": "CONFIRMED",
        "report": final["report"], "final": {"path": str(final_path), "sha256": sha(frozen(final_path))},
        "reportBytes": len(report), "adjudication": adjudication_binding,
        "tool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "acceptanceLimit": "One family's accepted confirmation on signed88a9dfab. Publication still "
                           "requires the second family's accepted confirmation and closure checks.",
    })))


if __name__ == "__main__":
    main()
