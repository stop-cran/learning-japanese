"""Record substantive adjudication of the original GPT confirmation after its final audit."""
import datetime
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha

OUT = WS / "scratch-131" / "review" / "confirm-003"
RUN = "N1-B131-GPT-CONFIRM-003"


def main():
    final_path = OUT / (RUN + "-final.json")
    final = json.loads(frozen(final_path))
    require(final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["confirmation"] == "CONFIRMED"
            and final["candidate"] == "88a9dfab6a783b082659b742a24242342bb2e461", "Unexpected final")
    report = frozen(final["report"]["path"], final["report"]["sha256"])
    structure = json.loads(frozen(final["structure"]["path"], final["structure"]["sha256"]))
    require(structure["status"] == "PASS" and not structure["nonAccepting"] and structure["findings"] == 0
            and structure["dispositions"] == {"O1": "RESOLVED"},
            "Structure is not an accepting confirmation")
    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    require(not audit["breaches"] and audit["chainRead"] == audit["chainRequired"] == 20
            and audit["writes"] == audit["readbacks"] == 1 and audit["fetches"] == 0
            and audit["messages"] == ["CONFIRMED"], "Audit is not a clean confirmation")
    frozen(final["context"]["path"], final["context"]["sha256"])
    adjudication = {
        "run": RUN, "method": "All 85 source citations (74 unique) were resolved against sources "
                              "reconstructed from the verified hash-bound chain segments; decisive "
                              "dictionary, card and external lines were read by the coordinator.",
        "dispositions": {
            "O1": "ACCEPTED: 霜.md:14 declares 酒; the qualified note retains the 隠語大辞典 Meiji-and-later "
                  "disclosure (external-06-jargon.txt:4-7); 酒 alcohol/sake JMdict 1329010.",
        },
        "openComparisons": "D1-D5, D8, D11, D13-D21 and the E10 霜/卒 branch were reassessed with direct "
                           "line-14 pairs on 衛 (援 循 番 士 軍 送 抵) and 霜 (氷 凍 酒 涼 久 害 枯 殺 卒). "
                           "D6/D7/D9/D10/D12, D22 益 and E1-E9 retain their original bounded scope (L3/L4).",
        "q2": "ACCEPTED bounded 冴/霜 non-collision: 冴 title 'clear; sharp-minded' versus 霜 'frost'; "
              "complete 冴える JMdict 1297050 includes the old-fashioned 'to become intensely cold' sense, "
              "and 霜's sharp/severe metaphor (external-05-03.txt:14) is not mental alertness. No direct pair "
              "exists on either endpoint; the claim is limited to the opened senses.",
        "basisChecks": "番 watch/guard/lookout (2022640), 送る to escort (1402730), 援護 support/help "
                       "restricted to 援護 and covering/protection unrestricted (1588790), 循環 (1341340), "
                       "抵抗 (1436260) are present with the stated glosses and restrictions.",
        "citationImprecision": "Note-line citations are consistently one line early: 衛.md 78-79/80-81/82/"
                               "83-84/85-88 correspond to content at 79-80/81-82/83/84-85/86-88, and 霜.md "
                               "86-88/89-91/92-98 to 87-89/90-92/93-98. Non-consequential: each cited "
                               "content exists in the adjacent supplied lines and line 14 is exact.",
        "communityMembership": "L1 modern-level membership of 衛/羊/霜 is closed by the named community "
                               "array, not an official JLPT syllabus.",
        "limitsRetained": "L1-L12 retained, including six latent smaller-pool reading collisions, unread "
                          "non-selected records, no caller/custom/multi-borrow/Kotlin/native/device/APK claim "
                          "and no delivery or whole-set credit.",
    }
    adjudication_binding = freeze_json(OUT / (RUN + "-adjudication.json"), adjudication)
    print(json.dumps(freeze_json(OUT / (RUN + "-acceptance.json"), {
        "run": RUN, "batch": 131, "candidate": final["candidate"],
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "session": final["session"], "reviewAccepted": True, "confirmation": "CONFIRMED",
        "report": final["report"], "final": {"path": str(final_path), "sha256": sha(frozen(final_path))},
        "reportBytes": len(report), "adjudication": adjudication_binding,
        "tool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "acceptanceLimit": "Second family's accepted confirmation on signed88a9dfab. Both families are "
                           "now confirmed; publication still requires closure, CI and ZIP verification.",
    })))


if __name__ == "__main__":
    main()
