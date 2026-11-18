import json
import re
import sys
from pathlib import Path

from common_134 import BASE, HERE, REPO, ROOT, git, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

REASONS = {
    "丙": "Third class/rank is not the specific rank 検校; the broad rank wording nevertheless merits a direct precaution.",
    "並": "Rank with or equal is a verb of comparison; average grade and a row are not the specific rank 検校.",
    "久": "The complete character source gives old story; the specific abbreviated title of The Tale of Genji merits a qualified broad-story precaution, not an equation of duration and a novel.",
    "京": "The exact 江戸 family calls Edo the shogunate capital. The sourced abbreviated Edo use merits a direct capital-label precaution, not an assertion that all capitals are Edo.",
    "仲": "The color's literary association with ゆかり and the name reading have unresolved relation-label scope. Protect the broad relationship label without teaching that every relationship means purple.",
    "位": "The native word identifies a particular rank, 検校. The broad rank label warrants a direct precaution; not every throne or position is that rank.",
    "係": "The literary ゆかり association has unresolved connection-label scope. Protect the broad label, not every duty or person in charge.",
    "冊": "The Tale of Genji is a specific work; 冊 covers volumes and book counting. A broad book-label precaution does not equate every counter with that title.",
    "准": "An associate rank is not established as 検校; retain a conservative direct rank-label precaution, not a universal equivalence.",
    "列": "Rank in the complete family is a row, ranks of peers or taxonomic series, not the specific office 検校.",
    "包": "The historical ツツム gloss has unresolved scope and matches 包's supported verb. Directly guard the pair without asserting an ordinary modern wrap meaning.",
    "匹": "The complete noun family includes a roll of cloth, while 紫 can name purple cloth. A broad cloth precaution does not say all rolls are purple.",
    "女": "日本国語大辞典 records 紫 for woman; 女's primary woman label warrants a direct precaution, not the reverse claim that every woman is called 紫.",
    "娘": "The complete 娘 family includes a young woman, and 紫 has a source-positive woman use. Guard the broad overlapping label without equating daughter and purple.",
    "婦": "Complete 婦 family 2268500 includes woman, and 紫 has a woman use. Guard the overlap without treating every wife or bride as 紫.",
    "局": "Complete 局 family 1239570 includes court lady, while 紫 has a woman sense. Guard the broad person label; an office or palace room is not automatically 紫.",
    "層": "Story here is a building floor, not a literary narrative; social strata and layers are not the particular rank 検校.",
    "巻": "Complete family 1211140 includes a book volume and a roll of cloth. The sourced work and purple-cloth uses warrant a broad precaution, not general identity.",
    "市": "紫 abbreviates Edo, a specific city. The broad city label merits a precaution; a market and every city are not Edo.",
    "布": "The native 紫 entry includes purple cloth; 布 means cloth broadly. Directly protect the broader label without calling all fabric purple.",
    "文": "Complete family 1505080 includes a book or writings; 紫 can abbreviate a particular literary work. A broad writing precaution does not equate every sentence with that title.",
    "本": "Complete family 1522150 includes book and volume, whereas 紫 can abbreviate The Tale of Genji. Protect the broad label, not every origin or book.",
    "札": "The full native family includes a slip of paper; 紫 includes purple paper. Guard this broad paper overlap without claiming banknotes are all purple.",
    "机": "A desk is furniture used for writing, not the particular literary work, color, plant, condiment or other sourced uses.",
    "根": "Root is a plant part and a source of dye, not the whole gromwell plant or the purple color. The complete 紫根 compound means gromwell root; it does not allocate root to bare 紫.",
    "格": "The complete family includes rank and status; 紫 names a particular rank. A direct precaution protects the broad label, not all rules or grammar cases.",
    "植": "Its displayed 'plant' could be read as a noun, and its linked 植物 explicitly denotes plants. Purple gromwell is a plant; protect the unresolved broad label, not every planting action.",
    "極": "KANJIDIC2 gives highest rank, while 紫 names a particular rank. Protect the broad rank label without equating every extreme or pole with 検校.",
    "殿": "Palace and lord differ from 紫's specific woman, rank, Edo and literary-work uses. Palace-related 紫 compounds do not alone allocate palace to bare 紫.",
    "稲": "Rice plant (Oryza sativa) and purple gromwell (Lithospermum erythrorhizon) are different plants; the broad category alone is not identity.",
    "筆": "Complete 筆 family includes the written word; 紫 can abbreviate a particular literary work. Protect that broad label, not every brush or act of writing.",
    "紙": "The native 紫 entry includes purple paper; 紙 names paper broadly. A direct precaution does not say all paper is purple.",
    "級": "The full 級 family includes rank; 紫 names a specific rank. Guard the broad label without equating school grades and 検校.",
    "統": "The character's complete meanings include relationship and linked 系統 includes lineage. The literary ゆかり association warrants a qualified precaution, not universal synonymy.",
    "編": "Complete 編 family includes a completed literary work; 紫 abbreviates a specific novel. A direct broad-work precaution does not equate knitting and purple.",
    "美": "字通 describes 紫 used for beautiful or sacred things. Protect the unresolved broad beauty label without claiming every beautiful thing is purple.",
    "色": "紫 denotes a particular color; 色 denotes color generally and also has other senses. Protect the broad label, not all colors or lovers as 紫.",
    "苗": "A seedling is a young plant, and purple gromwell is a plant. Guard the broad plant label without claiming every seedling is gromwell.",
    "草": "The native 草 family includes herb; purple gromwell is an herbaceous plant. Guard the broad label without calling all grass gromwell.",
    "著": "The complete 著 family includes a written work or book; 紫 abbreviates a particular novel. Guard the broad work label, not the act of publishing in general.",
    "記": "KANJIDIC2 gives narrative and the complete family gives an account or record. Guard the unresolved broad narrative label against a specific novel, not every diary as 紫.",
    "話": "Complete family 1600900 includes tale or story; 紫 abbreviates a specific tale. Guard the broad label without claiming all talk or stories are that work.",
    "課": "The character is a lesson, section or counter for chapters, not the entire named literary work; a chapter of a book does not make the counter a title.",
    "調": "The full character source includes writing style and the native family gives form or meter. A style is not the named novel itself, nor the other sourced 紫 senses.",
    "資": "Capital means funds or resources here, not a capital city; materials/data are not the particular literary work or color.",
    "都": "The complete family includes city and capital; 紫 abbreviates Edo. A direct precaution protects the broad city label without equating all metropolises with Edo.",
    "関": "Connection and relationship are broad; the literary ゆかり association warrants a qualified precaution, not a claim that a barrier or every relation is purple.",
    "隻": "Fish is a counter example for bundled items, not the fish noun itself. It is not the source-positive sardine name.",
    "館": "Complete family 1216210 includes noblewoman. 紫 has a sourced woman use, so guard the broad person label without equating every building with purple.",
    "魚": "日本国語大辞典 gives 紫 as a sardine name and 魚 denotes fish broadly. Guard the broad label, not all fish as sardines.",
    "古": "Oldness, antiquity and used goods are distinct from the color, plant, condiment and qualified names. 古典 is a whole compound for classics; it does not make bare 古 the named Tale of Genji.",
    "右": "Direction, right hand, above-mentioned and the better of two do not denote the sourced color, plant, condiment, specific names or other qualified uses.",
    "川": "A river or stream is not the color, gromwell, condiment, particular rank, woman, literary title or city; a plant near water is only association.",
}

source = HERE / "source-002"
guard = start_guard()
try:
    scan = json.loads((source / "scans" / "紫.json").read_bytes())
    target_text = normalized(REPO / "kanji" / "紫.md")
    meta, _ = n1lib.parse(target_text)
    exclusions = set(meta["quiz_exclusions"])
    curated = set(meta["distractors"])
    assert len(scan["rows"]) == 1261
    assert set(REASONS) == set(scan["matches"]) | curated
    assert exclusions <= set(REASONS) and not exclusions & curated
    target_title = meta["title"]
    pairs = []
    for other, reason in REASONS.items():
        card = source / "comparison-cards" / (other + ".md")
        raw = git("show", f"{BASE}:kanji/{other}.md")
        assert card.read_bytes() == raw
        comparison_meta, _ = n1lib.parse(raw.replace(b"\r\n", b"\n").decode("utf-8"))
        title = comparison_meta["title"]
        readback = source / "comparison-readback" / (other + ".json")
        pairs.append({
            "pair": ["紫", other], "comparisonTitle": title,
            "decision": "curated" if other in curated else "guard" if other in exclusions else "distinct",
            "comparisonLabelOnTarget": f"Compared {title!r} against 紫's qualified source senses. {reason}",
            "targetLabelOnComparison": f"Compared {target_title!r} against {other}'s full card and captured character and word senses. {reason}",
            "baselineCardSha256": sha(raw), "readbackSha256": sha(readback.read_bytes()),
            "scanMatch": other in scan["matches"],
        })
    write(HERE / "analysis-001" / "pair-dispositions.json", {
        "base": BASE, "members": [{"kanji": "紫", "targetTitle": target_title,
                                    "scanRows": len(scan["rows"]), "pairs": pairs}],
        "newMemberPairs": [],
        "rule": "Direct symmetric pairs only, no transitive closure. Precautions protect unresolved broad labels, not universal synonymy.",
        "coverage": "Full baseline scan, actual comparison cards, complete English character meanings and captured applicable word-family senses; author assessment only.",
        "limits": "Finite manually expanded keywords and selected comparisons, not exhaustive synonym discovery or independent review.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
finally:
    write(HERE / "analysis-001" / "memory.json", guard.finish())
