"""Write the frozen B133 coordinator adjudication of the verified source-only reconciliation."""
import json
from datetime import datetime, timezone
from pathlib import Path

from common import freeze_json, frozen, require, sha
from verify_b133_payload import BASE, HERE

CANDIDATE = "ad047ace020579f81bde250ac948b9a4cb597887"
SRC = HERE.parent / "source-reconciliation-001"
OUT = HERE / "coordinator-adjudication-001.json"
INVENTORY_SHA = "771407a30005890503babae922f454e672f1d92ee504111bd83a7974960d4eb7"
DISPOSITIONS_SHA = "186a32810d754df0a53b1555f20a66a3a0fc33514b2a8654c394e3a4c72feb92"
VERIFICATION_SHA = "d6c01b0501e4c3d23c8ab250a5cd674a32270058e5f7a3252b39bf5d185443fb"

ADD, KEEP = "ADD_QUALIFIED_DIRECT_PRECAUTION", "RETAIN_DISTINCTION"
PENDING_ADD = "OPEN_PENDING_SIGNED_CHANGE_AND_ORIGINAL_REVIEWER_CONFIRMATION"
PENDING_KEEP = "RETAINED_PENDING_ORIGINAL_REVIEWER_CONFIRMATION"
DECISIONS = {
    ("鉛", "鉱"): (ADD, "あらがね/鉱 names ore and unrefined metal; 'ore; mineral' is a broad category label like the "
                  "existing 金/素 metal/element guards. JMdict 1736440 鉛鉱 means lead mine/deposits, not lead ore; "
                  "no refined-metal distinction is relied on."),
    ("鉛", "鉄"): (KEEP, "Both displayed labels name different specific metals. 鉄's own published curated distractors "
                  "are the specific metals 銅 and 銀, so specific-versus-specific metal labels are an intended "
                  "distinction. Nikkoku かね【金・鉄・銀・銅】 leaves per-spelling mapping unresolved, but even a generic "
                  "metal sense of 鉄 would not make 'lead (metal)' correct for 鉄 or 'iron' correct for 鉛; the broad "
                  "metal label is already guarded by 金."),
    ("滝", "速"): (ADD, "滝 records 急流/奔流 (rapids marked archaic in JMdict but unmarked in Daijisen) and 速い "
                  "independently describes fast river flow; consistent with the existing 急 precaution. Shared "
                  "evidence resolves both Claude C3 and GPT Q3/D8, each retained as a separate claim ID."),
    ("鉛", "似"): (KEEP, "似 is an imitate/resemble/counterfeit action (似せる 贋造する); 鉛's sense is the counterfeit-money "
                  "artifact. Noun versus action; KD untyped English 'counterfeit' does not establish a bare money noun."),
    ("琴", "具"): (ADD, "Standalone 具 is tool/means/equipment; 'tools; ingredients' is a broad implement label "
                  "consistent with the existing 器/械 guards. Not transitive from 琴-器 and 器-具."),
    ("滝", "岩"): (ADD, "World Encyclopedia folklore (Miyata Noboru) records タキ as sheer cliff from the Chugoku region "
                  "westward. Not an unrestricted modern sense or standard dictionary gloss of 滝; nevertheless a "
                  "qualified precaution, matching this candidate's existing 琴-墓/丘 treatment of a qualified 字通 "
                  "Chu-language sense. The Note must state the restriction and that no rock is a waterfall."),
    ("琴", "機"): (KEEP, "機 covers machinery, loom, trigger, occasion and function; no bare musical-instrument or "
                  "string sense was established."),
    ("琴", "糸"): (ADD, "Daijisen and Nikkoku record standalone 糸 for stringed instruments such as koto/shamisen and "
                  "their music, beyond compound association."),
    ("琴", "緒"): (ADD, "字通 古辞書の訓 cites 〔和名抄〕琴 古度乃乎（ことのを） with unresolved historical scope, while 緒 "
                  "independently includes instrument strings (琴の緒). Conservative qualified precaution for an "
                  "unresolved label, consistent with the article's existing policy; the Note must not teach that 琴 "
                  "means cord or string."),
    ("琴", "線"): (KEEP, "Displayed 'line; track' does not name a string or instrument; 線's thread-like senses and the "
                  "whole word 琴線 do not transfer to bare 琴, and ことのを does not map to 'line'."),
    ("琴", "索"): (KEEP, "索 rope is 太い縄/つな, plus search/scatter senses; no instrument-string sense."),
    ("鉛", "遅"): (ADD, "Nikkoku 鉛 heavy/dull figurative sense; 遅 おそ independently dull/slow; consistent with the "
                  "existing 鈍 precaution."),
    ("鉛", "円"): (ADD, "Nikkoku まろ【円・丸】[2] means 銭 and the complete JMdict 丸/円 family has slang money; "
                  "consistent with the existing 両/札/貨/銀 money guards. Do not transfer every 丸 sense to 円."),
    ("鉛", "倣"): (KEEP, "倣 imitate/emulate/follow is an action; no bare counterfeit-money noun."),
    ("滝", "声"): (ADD, "字通 滝 lists rain sound (あめのおと); 声 includes inanimate sound in Daijisen, Nikkoku and "
                  "JMdict; consistent with the existing 音/響/騒/鳴 guards."),
    ("滝", "険"): (ADD, "Steep terrain/place of 険 overlaps the same qualified regional タキ cliff branch as 岩; "
                  "qualified precaution with the same restriction."),
    ("滝", "激"): (ADD, "字通 激 describes surging obstructed water (はげしく流れる) and 滝 includes 激湍/奔流; "
                  "consistent with 急/流."),
    ("滝", "液"): (KEEP, "液 'liquid' is a superordinate category of the secondary 滝水 abbreviation; the broad water "
                  "label is already guarded by 水."),
}
CROSS = {
    "pair": ["鉛", "具"], "decision": KEEP,
    "reason": "Nikkoku 具 sense 6 includes pigments with added 鉛白, while 鉛's displayed label is 'lead (metal)' and "
              "具's displayed label 'tools; ingredients' names neither face powder nor lead. No new comparison "
              "character or precaution; disclosed to both confirmations.",
    "resolutionStatus": PENDING_KEEP,
}
OPTIONAL = [
    {"id": "Claude O1", "decision": "NO_CHANGE", "reason": "The '(metal)' qualifier already separates lead from "
     "the guide verb/率 homograph."},
    {"id": "Claude O2", "decision": "NO_CHANGE", "reason": "Phonetic-component analysis is optional, not required."},
    {"id": "Claude O3", "decision": "NO_CHANGE", "reason": "Keep 'waterfall; rapids': Daijisen records 急流/奔流 "
     "without an archaic mark, and the existing guards are built on the current title."},
    {"id": "Claude O4", "decision": "NO_CHANGE", "reason": "No pinned per-reading Joyo source in batch evidence; "
     "ロウ/ソウ are already marked not practised."},
]
CHANGES = {
    "kanji/鉛.md": ["鉱", "遅", "円"],
    "kanji/滝.md": ["速", "声", "激", "岩", "険"],
    "kanji/琴.md": ["具", "糸", "緒"],
}


def main():
    require(not OUT.exists(), "Preserve existing adjudication")
    frozen(SRC / "inventory.json", INVENTORY_SHA)
    raw = frozen(SRC / "pair-dispositions-final.json", DISPOSITIONS_SHA)
    frozen(HERE / "source-reconciliation-verification-001.json", VERIFICATION_SHA)
    data = json.loads(raw)
    rows = data["pairRows"]
    require(len(rows) == 18 == len(DECISIONS)
            and {tuple(r["pair"]) for r in rows} == set(DECISIONS), "Pair rows differ")
    decisions = []
    for row in rows:
        decision, reason = DECISIONS[tuple(row["pair"])]
        require(row["existingDirectExclusions"] == {"aExcludesB": False, "bExcludesA": False},
                "Pair already excluded")
        decisions.append({
            "pair": row["pair"], "claimIds": row["claimIds"], "authorProposal": row["proposal"],
            "decision": decision, "reason": reason,
            "evidence": [f"source-reconciliation-001/{b['path']}:{','.join(map(str, b['lines']))} "
                         f"[{b['locator']}] sha256={b['sha256']}" for b in row["exactSourceBindings"]],
            "resolutionStatus": PENDING_ADD if decision == ADD else PENDING_KEEP,
        })
    cross = data["consequentialOutOfAssignedPairObservation"]
    require(cross["pair"] == CROSS["pair"], "Cross-pair differs")
    CROSS["evidence"] = [f"source-reconciliation-001/{b['path']}:{','.join(map(str, b['lines']))} "
                         f"[{b['locator']}] sha256={b['sha256']}" for b in cross["sourceBindings"]]
    added = {path: sorted(v) for path, v in CHANGES.items()}
    require(sorted(sum(CHANGES.values(), [])) == sorted(p[1] for p, d in DECISIONS.items() if d[0] == ADD),
            "Change boundary differs from decisions")
    record = {
        "batch": 133, "candidate": CANDIDATE, "base": BASE,
        "status": "PRECAUTIONS_JUSTIFIED_IMPLEMENTATION_AND_CONFIRMATIONS_PENDING",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "sourceInventory": {"path": str(SRC / "inventory.json"), "sha256": INVENTORY_SHA},
        "pairDispositions": {"path": str(SRC / "pair-dispositions-final.json"), "sha256": DISPOSITIONS_SHA},
        "coordinatorVerification": {"path": str(HERE / "source-reconciliation-verification-001.json"),
                                    "sha256": VERIFICATION_SHA},
        "policy": "Follow the candidate's established precaution policy: guard broad labels and positively attested "
                  "character or word senses, including qualified 字通 and regional senses already treated as "
                  "precautions (琴-墓/丘), when the counterpart's displayed label names that sense. Retain distinctions "
                  "for noun-versus-action, specific-versus-specific labels, compound-only association and "
                  "superordinate categories already guarded. Precautions are not synonymy claims.",
        "decisions": decisions, "crossPair": CROSS, "optionalPoints": OPTIONAL,
        "added": len(sum(CHANGES.values(), [])), "retained": sum(d[0] == KEEP for d in DECISIONS.values()),
        "changeBoundary": {
            "teachingArticles": list(CHANGES), "quizExclusionsAdded": added,
            "prose": "Concise qualified Notes explaining each new precaution group with directly related successful "
                     "source citations; one 滝 Note states the regional タキ cliff restriction. No other teaching edits.",
            "preserve": "Titles, readings, practice readings, distractors, common words, mnemonics, strokes, all other "
                        "articles, original batch-133 author packet and initial review records.",
            "dependentChanges": "Regenerated manifest and separate additive batch-133-reconciliation provenance and "
                                "gate evidence, following the B132 reconciliation layout.",
            "mechanism": "Symmetric direct-pair rule declared on the three new cards only; no reciprocal or transitive "
                         "edits.",
        },
        "reviewDisposition": "Claude's original CLEAN and GPT's original UNVERIFIED remain unchanged. Both original "
                             "reviewers must confirm the actual changed signed snapshot, including retained "
                             "distinctions and the 鉛-具 disclosure.",
        "publication": "BLOCKED",
        "openClaimIds": ["Q1", "Q2", "Q3", "Q4"],
        "coordinatorClaimIds": ["C1", "C2", "C3", "C4", "C5", "C6"],
        "delivered": 268, "remaining": 960,
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "limits": "Coordinator adjudication only. No teaching change, signed reconciliation, confirmation, "
                  "publication, rendering, Kotlin/native/device or whole-set acceptance.",
    }
    print(json.dumps(freeze_json(OUT, record), ensure_ascii=False))


if __name__ == "__main__":
    main()
