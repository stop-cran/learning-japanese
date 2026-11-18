import json
import re
from b128_common import BASE, HERE, PACKET, REPO, git, sha, start_guard, write

GUARDS = {
    "口": ("Mouth is broader than lips, but can plausibly be accepted for the visible oral part; conservative broad-label guard, not identity.", "Lips name only a part of the mouth; a learner could still take the broad oral character as including its lips. Prevent the unresolved broad oral-part ambiguity.", ["JMdict 1275640", "JMdict 1359940"]),
    "花": ("Daijisen and Nikkoku give the standalone くちびる word a petal sense. Flower is broader than petal; conservatively keep the flower label out.", "JMdict 1194500 includes petal under 花/華. Lips has a documented poetic petal use, not a license to call every flower lips.", ["Daijisen くちびる sense 2", "Nikkoku くちびる sense 2", "JMdict 1194500"]),
    "震": ("Kanjipedia describes mouth-trembling in its historical account and Jitsu gives surprise; quake/tremble can compete under that qualified branch.", "Lips is not an ordinary label for 震; the opposite direction motivates the conservative direct guard.", ["Kanjipedia historical account", "Jitsu 訓義1", "JMdict 1366310"]),
    "動": ("Move is broad enough to include the mouth-trembling account. Guard the unresolved broad movement choice, not every movement as a meaning of 唇.", "Lips does not describe the motion/operation/change senses of 動. This guard is one-directional risk, not universal synonymy.", ["Kanjipedia historical account", "JMdict 1451210"]),
    "恐": ("Jitsu's おどろく and JMdict's surprised/frightened branches intersect the fear family; 恐ろしい also has surprising/startling senses. Conservatively guard fear/awe.", "Lips is not an ordinary label for 恐; the qualified surprise branch, not mouth anatomy, motivates this pair.", ["Jitsu 訓義1", "JMdict 1238680", "JMdict 1236690", "JMdict 1236750"]),
    "怖": ("Frightening and being startled differ in valency and need not coincide. The positive surprised/frightened branch leaves a broad fear-choice ambiguity; guard conservatively without asserting synonymy.", "Lips is not an ordinary label for 怖; only the reverse broad-choice risk is being prevented.", ["Jitsu 訓義1", "JMdict 1238680", "JMdict 1593480"]),
    "側": ("Jitsu quotes 脣=ホトリ in an old dictionary. The broad side label could compete with that variant gloss; ordinary currency for 唇 is not established.", "Lips is not a general label for 側. This conservative guard discloses an unresolved historical-variant side-choice ambiguity.", ["Jitsu 古辞書の訓", "JMdict 1581310", "JMdict 1590440"]),
    "辺": ("The historical variant ホトリ gloss and 辺/畔/辺り ほとり family support a plausible side/edge comparison. Guard the broad vicinity/edge label.", "Lips is not a general label for 辺; neither spelling nor all senses are declared interchangeable.", ["Jitsu 古辞書の訓", "JMdict 2842190", "JMdict 1512070"]),
    "際": ("Edge in the actual edge/occasion label is broad enough to compete with the old variant ホトリ gloss; guard conservatively.", "Lips is not an ordinary occasion/edge label for 際. This is a one-direction unresolved broad-choice guard.", ["Jitsu 古辞書の訓", "JMdict 1296290", "JMdict 1296300"]),
    "境": ("Boundary/border is broader than a bodily lip; the unresolved scope of historical 脣=ホトリ merits a conservative direct boundary-choice guard.", "Lips is not a general label for 境's border, psychological-state or Buddhist senses. No unrestricted boundary meaning is asserted for ordinary 唇.", ["Jitsu 古辞書の訓", "JMdict 1235950"]),
    "界": ("Its displayed boundary half could compete with the historical variant edge/side gloss. Guard this unresolved broad-choice risk directly, not by inheriting 境's guard.", "Lips is not an ordinary label for 界's world, kingdom, field or boundary senses.", ["Jitsu 古辞書の訓", "JMdict 1235950", "JMdict 2081500"]),
    "岸": ("The scope of old 脣=ホトリ is not settled; ほとり can mean bank/shore in the complete bilingual family. Guard shore/riverbank rather than dismiss the source gloss.", "Lips is not ordinarily a shore label for 岸; the pair is a conservative unresolved historical-variant guard, not a claim that 唇 means coastline.", ["Jitsu 古辞書の訓", "JMdict 2842190", "JMdict 1217040"]),
    "畔": ("The displayed waterside half and its ほとり family can compete with the old variant gloss. Evaluate this pair directly, not transitively through 辺 or 岸.", "Lips is not ordinarily a paddy boundary label for 畔; the historical-variant waterside risk is conservatively separated.", ["Jitsu 古辞書の訓", "JMdict 2842190", "JMdict 1250980"]),
    "音": ("Nikkoku separately gives しん as lip or labial consonant. Sound is broad enough to compete for that noun branch; guard without turning lips into all sounds.", "Lips is not a general label for 音's sound, noise, note or fame. The opposite direction motivates this qualified direct guard.", ["Nikkoku しん noun", "JMdict 1359950", "JMdict 1576900"]),
}
NO_GUARD = {
    "刃": "Cutting edge is not a generic rim or side: neither anatomical lips nor a poetic petal or being startled denotes a blade. The historical variant ホトリ gloss does not establish a cutting function.",
    "危": "Danger can cause surprise/fear but is a hazardous situation, not the response おどろく or a lip. Cause and response are not synonyms.",
    "含": "Containing/including or holding something in the mouth is an action/relation, not the lip itself; the mouth token is not semantic equality.",
    "咲": "The actual article teaches the intransitive blooming action; full 咲く also has breaking waves, not petal as a part. 唇's petal noun does not mean to bloom or open, and its lip label does not fit 咲. The displayed blossom/bloom verb label is distinguished from 花's petal-inclusive noun family.",
    "在": "Outskirts is a secondary source sense, but the displayed exist/be-located label is not lips, surprise or an edge; the old variant gloss does not establish existence as 唇's meaning.",
    "声": "A labial consonant is an articulatory class, not voice or an opinion. Even the voiced-sound sense is not the displayed voice label for every labial (which may be voiceless); anatomy is not vocal output.",
    "差": "Margin here is a comparative difference/balance, not a physical rim. Its displayed difference/gap label does not mean lips or the qualified source branches.",
    "態": "Voice (of verbs) is grammatical diathesis, not audible voice or lips. Attitude/condition is not the lip, poetic petal, historical edge gloss or surprise action.",
    "房": "Fringe is a tassel/tuft, not a generic margin; room, bunch and hanging threads do not denote lips or petals as an individual part. A bunch of flowers is not one petal.",
    "案": "Fear/worry is a scanned source branch, but the actual proposal/draft-plan label does not describe lips or being surprised. No proposal sense of 唇 is established.",
    "横": "The displayed horizontal label specifies orientation; a lip or edge need not be horizontal. Side in its word family is not proof that the historical variant gloss means horizontal.",
    "漱": "Rinsing/gargling is an action involving the mouth, not the lips as anatomy; neither displayed label denotes the other's character.",
    "片": "One-sided/sheet is not a generic side or edge. Neither the old variant gloss nor literary petals make 唇 mean one of a pair, a sheet or a fragment; the lip label does not fit 片.",
    "町": "Town/neighborhood is a settlement or town block, not a lip or a generic edge. The historical gloss does not authorize transporting every geographical sense of ほとり into 唇.",
    "管": "Drunken talk is a phrasal secondary gloss, not labial speech sounds; pipe/supervise does not describe lips. A wind instrument may use the lips, which does not make the two synonymous.",
    "菜": "Side dish is an English phrase, not spatial side. Vegetables/greens and lips/petals are distinct categories; 菜の花 is a whole compound, not evidence that 菜 means petal.",
    "行": "The bank hit is a financial institution/business, not a shore. The displayed go label does not fit the source surprise or lip branches, nor does lips label 行.",
    "裏": "Reverse side/lining is specifically the back/interior, not a generic edge. A lip may have an inner face, but that association does not establish either displayed label as the other's meaning.",
    "詞": "Part of speech is a grammatical class and lyrics/words are linguistic units, not a particular consonant articulation or lip. No words/lyrics sense of 唇 is established by Nikkoku's labial-consonant noun.",
    "話": "Talk/speak is communication or a story, not the lip or an individual labial consonant. Using lips in speaking is an instrument/action relation, not meaning equivalence.",
    "語": "Language/word is a linguistic system/unit, not lips, a poetic petal or a labial sound. Whole-word 読唇術 lip-reading does not make 唇 mean language.",
    "談": "Converse/consult concerns an exchange of information, not an articulatory class or lips. The compound dependence/proverb senses in 唇 families do not transfer to the character.",
    "輪": "The flower hit occurs in a counter for flowers; counting flowers is not being a petal. Wheel/ring is neither lips nor surprise or the qualified historical variant edge gloss.",
    "述": "State/relate means expressing an account, not naming an articulator or speech sound. Lips is not a label for 述 and no state/relate meaning is established for 唇.",
    "郊": "Outskirts/suburbs is specifically a settlement's periphery. No such administrative/settlement scope is established by the old variant gloss; neither actual label answers the other's prompt.",
    "鋭": "Sharp/keen concerns a pointed or acute quality, not an edge as a location. A lip, petal or old edge gloss does not establish sharpness, and lips does not label 鋭.",
    "響": "Resound/echo is sound carrying/repeating, not the individual labial-consonant class. Its broad sound branch does not put the actual resound/echo title on 唇; there is no echo meaning supplied by the lip noun.",
    "鳴": "Animal call/ring is producing a call or ringing sound, not lips or the labial-consonant category. A generic sound token does not make a bell or animal call a lip.",
}

guard = start_guard()
try:
    scan = json.loads((PACKET / "baseline-gloss-scan-002.json").read_text(encoding="utf-8"))
    assert set(scan["matches"]) == GUARDS.keys() | NO_GUARD.keys()
    rows = {r["kanji"]: r for r in scan["rows"]}
    decisions = []
    for char in scan["matches"]:
        record = {"kanji": char, "baselineTitle": rows[char]["title"], "completeSourceMeanings": rows[char]["meanings"], "comparisonCard": "comparison-cards/" + char + ".md"}
        if char in GUARDS:
            forward, reverse, sources = GUARDS[char]
            record.update(decision="conservative-direct-guard", otherLabelForNewPrompt=forward, newLabelForOtherPrompt=reverse, sourceBindings=sources)
        else:
            record.update(decision="no-guard", otherLabelForNewPrompt=NO_GUARD[char], newLabelForOtherPrompt="The displayed lips label is not established for this comparison character; its complete retained KANJIDIC2 record and actual card were inspected. " + NO_GUARD[char])
        decisions.append(record)
    write(PACKET / "pair-dispositions.json", {
        "baseCommit": BASE, "newKanji": "唇", "actualScan": "baseline-gloss-scan-002.json",
        "scanMatches": decisions,
        "curatedChoices": [
            {"kanji": "古", "label": "old", "otherLabelForNewPrompt": "Age/antiquity is not lips, petals, surprise, a boundary or a speech sound.", "newLabelForOtherPrompt": "No lips sense is in 古's full record or actual card. The 口-shaped base is a shape, not transferred semantics."},
            {"kanji": "右", "label": "right", "otherLabelForNewPrompt": "Right is directional, not a generic side; historical ホトリ does not establish the right-hand direction.", "newLabelForOtherPrompt": "右's direction, above-mentioned and supporting branches do not mean lips. The historical mouth-component debate does not transfer lip meaning to the whole character."},
            {"kanji": "石", "label": "stone", "otherLabelForNewPrompt": "Stone/rock, gemstone and volume measure are not lips or any supplied secondary sense.", "newLabelForOtherPrompt": "Lips does not label a stone or its complete dictionary senses. A lower box is not semantic evidence."},
        ],
        "curatedPairwiseCheck": "古/右/石 have age, rightward-direction and stone labels respectively; all three actual cards and complete character records inspected. No direct exclusion among them is declared or established here.",
        "guardPolicy": "Direct pairs only. Several deliberately prevent unresolved broad-choice ambiguities under positive secondary or variant-source glosses rather than asserting universal synonymy. No transitive guard propagation.",
        "readingAndSenseBoundary": "The ほとり quote is under 脣, not asserted ordinary 唇 pronunciation. Kanjipedia describes mouth-trembling in an origin account, not a new modern reading. Nikkoku's しん is a separate noun. Literary petals are a direct native-word sense; whole compounds' labrum, labia, dependence, lip-reading and proverb meanings are not indiscriminately assigned to 唇.",
        "limits": "Finite author disposition of actual scanned cards, not independent linguistic certification or exhaustive semantic discovery.",
    })
    frozen = json.loads(git("show", f"{BASE}:docs/n1-sources/baseline-word-candidates.json"))
    candidates = [r for r in frozen if r["kanji"] == "唇"]
    declaring, incidental = [], []
    for folder in ("kanji", "words"):
        for path in sorted((REPO / folder).glob("*.md")):
            guard.check()
            text = path.read_text(encoding="utf-8")
            if "唇" not in text and "脣" not in text:
                continue
            rel = folder + "/" + path.name
            if folder == "words":
                match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
                if match and "唇" in [s.strip() for s in match.group(1).split(",")]:
                    declaring.append({"path": rel, "reading": re.search(r"^reading: (.+)$", text, re.M).group(1), "sha256": sha(path.read_bytes()), "linkPresent": "[唇](../kanji/唇.md)" in text})
                    continue
            if rel != "kanji/唇.md":
                incidental.append({"path": rel, "sha256": sha(path.read_bytes()), "disposition": "Incidental example/comparison or compound occurrence; not a declared support-word identity. No reciprocal wrapper required."})
    assert len(declaring) == 1 and declaring[0]["path"] == "words/唇.md" and declaring[0]["linkPresent"]
    assert len(candidates) == 1 and candidates[0]["word"] == "唇"
    write(PACKET / "support-audit.json", {
        "baseCommit": BASE, "frozenCandidateRecords": candidates, "allActiveDeclaringArticles": declaring,
        "requiredReciprocalPairs": [["唇", "唇"]], "incidentalOccurrences": incidental,
        "sourceEntry": "1359940", "spelling": "唇", "reading": "くちびる",
        "allocation": "The exact single-kanji word; no segmentation assumption. 口唇/こうしん supplies コウ+シン; 口唇/くちびる is independently flagged whole-word gikun/jukujikun, not a constituent pronunciation.",
        "wordChange": "One wrapper at the substantive component introduction, and removal only of the now-false no-card sentence. All other prose/metadata/easier N2 placement preserved.",
        "newWords": 0, "requiredPairCount": 1,
    })
    pages = json.loads((HERE / "external-pages" / "receipt.json").read_text(encoding="utf-8"))
    assert all("error" not in page for page in pages)
    write(PACKET / "external-source-bindings.json", {
        "captures": pages,
        "boundedExcerpts": [
            {"source": "kanjipedia-character", "heading": "意味", "excerpt": "くちびる。「唇歯」"},
            {"source": "kotobank", "dictionary": "Digital Daijisen", "heading": "くちびる sense 2", "excerpt": "花びら。"},
            {"source": "kotobank", "dictionary": "Seisenban Nihon Kokugo Daijiten", "heading": "しん noun", "excerpt": "くちびる。また、唇音"},
            {"source": "kotobank", "dictionary": "Jitsu", "heading": "訓義", "excerpt": "1. おどろく。"},
            {"source": "kotobank", "dictionary": "Jitsu", "heading": "古辞書の訓 / 名義抄", "excerpt": "脣　ホトリ・クチビル"},
        ],
        "readingDispositions": [
            {"raw": "シン", "source": "frozen KANJIDIC2", "practice": False, "example": "口唇/こうしん", "JMdict": "1276410", "reason": "Verified compound reading, no linked word article in this bounded slice. Not a rarity assertion."},
            {"raw": "くちびる", "source": "frozen KANJIDIC2", "practice": True, "example": "唇/くちびる", "JMdict": "1359940"},
            {"raw": "おどろく", "source": "Jitsu 字訓/訓義1 and old dictionary quote", "practice": False, "reason": "Positive source-specific reading; explicitly included in host wrong-option check. Not dismissed by age/priority/standard-list status."},
            {"raw": "ほとり", "source": "Jitsu old dictionary quote under variant 脣", "practice": False, "reason": "Variant-specific historical gloss, not established ordinary 唇 reading; conservatively included in host check and edge-choice guards."},
            {"raw": "くちひる", "source": "Nikkoku tentative 上代は…か", "practice": False, "reason": "Tentative historical form, not asserted certain. Included conservatively as an external host key."},
            {"raw": "ふるえる", "source": "Conservative paraphrase of Kanjipedia's mouth-trembling historical account", "practice": False, "reason": "Not claimed as an attested surface reading; extra host key prevents the model overlooking a positive semantic paraphrase."},
            {"raw": "しん", "source": "Nikkoku separate noun", "practice": False, "reason": "Covered by frozen シン after script normalization; the lip/labial-consonant noun branch remains distinct."},
            {"raw": "くちびる in 口唇; いぐち/みつくち in 兎唇", "source": "JMdict complete families", "practice": False, "reason": "Whole-word special readings, not independent readings allocated to 唇. Sensitive/dated medical word flags retained; no new model examples from those terms."},
        ],
        "discrepancies": [
            "Frozen KANJIDIC2 gives only lips; monolingual sources positively supply petal, surprise and historical variant information. Retained separately, not silently inserted or dropped.",
            "Initial web search overgeneralized agreement of all dictionaries and a general rim meaning; actual Kanjipedia 意味 gives lips, its historical account gives mouth-trembling, and Jitsu quotes ホトリ only under 脣. Teaching and guards preserve those boundaries.",
            "Simplified web_fetch of Kotobank omitted the Daijisen, Nikkoku and Jitsu sections. Complete captured HTML/text contains them and was inspected at headings; simplified output alone was not relied on.",
            "Two guessed Kotobank lookups, /word/唇%28漢字%29 and /word/くちびる, returned 404 in web_fetch. They supply no evidence; the actual /word/唇-55487 page is captured.",
            "All three bundled cmaps cover 唇/辰/口 and curated choices, but not variant 脣 U+8123; fallback rendering remains unverified.",
        ],
        "capturePolicy": "Complete external HTML/text remains local. Only exact source bindings and bounded attributable excerpts are committed. Search summaries are discovery aids, not source verification.",
    })
    print(json.dumps({"scanPairs": len(decisions), "guards": list(GUARDS), "declaringWords": len(declaring), "incidentalOccurrences": len(incidental)}, ensure_ascii=False))
finally:
    write(HERE / "author-packet-memory-001.json", guard.finish())
