import shutil
from b130_common import CHARS, HERE, PACKET, sha, start_guard, write

guard = start_guard()
try:
    assert CHARS == list("塀拍桜皇耗")
    planning = HERE / "planning-five-001"
    assert not planning.exists()
    planning.mkdir()
    for name in ("b130_common.py", "survey_b130.py", "survey-001.log", "survey-memory-001.json"):
        write(planning / name, (HERE / name).read_bytes())
    inventory = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes())
                 for p in PACKET.rglob("*") if p.is_file()}
    shutil.move(str(PACKET), str(planning / "source-packet"))
    write(planning / "inventory.json", {"initialSurvey": list("塀拍桜皇耗"), "files": inventory,
          "selectedForTeaching": list("塀拍耗"),
          "notSelected": {
              "桜": "Complete Nikkoku native さくら entry adds timber, bark, colour/layers, pattern/crest, horsemeat, silver coin, courtesan rank, tea, playing card, fish-fin, shill/arrangement, charcoal and proper-name/work-title senses; Jitsu adds ゆすらうめ. Positive evidence is preserved, not rejected for frequency or priority.",
              "皇": "Daijisen and Jitsu add divinity, greatness/brilliance/decoration, correction, leisure/hurry/fear and connective borrowing, with several native forms and unresolved text-extracted historical glyphs. This would enlarge the single-review packet beyond the chosen three."},
          "disposition": "Planning only. No teaching or gates had been authored. Original source survey and complete captures remain historical local evidence."})
finally:
    write(HERE / "split-survey-memory-001.json", guard.finish())
