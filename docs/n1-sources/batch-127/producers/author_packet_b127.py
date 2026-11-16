import json
import re
from b127_common import BASE, HERE, PACKET, REPO, git, sha, start_guard, write

GUARDS = {
    "亡": ("The quoted old-dictionary ホロブ reading is perishing-related; 亡's deceased label is conservatively separated from that source branch, not asserted to be an ordinary 倉 meaning.", "The storehouse label does not fit 亡; the risk is the reverse label."),
    "入": ("Jitsu directly includes storing (おさめる); 入's broad put-in label can describe putting into storage.", "倉's building label is not an ordinary label for 入; this is a one-direction broad-label guard."),
    "収": ("収's displayed collect/store label directly overlaps the Jitsu store sense of 倉.", "Storehouse is not the action 収; the direct storage-verb overlap justifies the guard without equating every sense."),
    "室": ("Both complete KANJIDIC2 records have cellar; 室's room/chamber label is broad enough to admit a storage chamber.", "倉's storehouse label is too narrow for arbitrary 室; the shared cellar branch motivates a conservative pair guard."),
    "府": ("KANJIDIC2 explicitly gives 府 the secondary storehouse sense, so the new title can be defensible for 府.", "Urban-prefecture/administration is not taught as a sense of 倉; this is the reverse-prompt risk, not universal synonymy."),
    "庫": ("Both characters and the full 1592380 family support storehouse/warehouse and くら.", "Either displayed storehouse label is defensible for either character."),
    "急": ("Kanjipedia and Daijisen positively give 倉 sudden/hurried senses; urgent/sudden is therefore not a reliably wrong label.", "倉's storage label is not an ordinary label for 急; the sudden branch independently warrants the guard."),
    "突": ("倉's source-positive sudden sense overlaps the sudden half of 突's thrust/sudden label.", "倉 does not acquire a thrust sense, and 突 does not acquire storage; the direct sudden overlap is sufficient."),
    "置": ("Jitsu's storing branch can be described by 置's broad put/place label, so conservatively guard this direction.", "A granary is not an ordinary meaning of 置; this does not assert unrestricted synonymy."),
    "蔵": ("The displayed storehouse/keep-in-storage label overlaps both the noun くら family and Jitsu's store gloss.", "The granary/storehouse label is defensible for 蔵; shared spelling family is checked, not assumed from shape."),
    "貯": ("The displayed save-up/store label overlaps the positively supplied store branch, not just the building's association with goods.", "Granary/storehouse is not the saving action 貯; a one-direction broad-label overlap still warrants a direct guard."),
}
NO_GUARD = {
    "保": "Maintaining/protecting a state is not a granary. Conversely storing goods does not guarantee preserving/protecting them; no unrestricted protect/preserve character gloss was established for 倉.",
    "倒": "Toppling/collapsing is not the source's suddenness or fragility; a fragile thing may collapse, but outcome is not synonymy. Neither displayed label answers the other prompt.",
    "傾": "Ruin occurs in 傾's source meanings, but the displayed label is tilt/incline. No tilt sense of 倉 or storehouse sense of 傾 was established.",
    "凌": "Keep-(rain)-out belongs to enduring/staving off, not keeping goods in a building. Neither endure/surpass nor granary/storehouse describes the other character.",
    "出": "Put OUT is the opposite direction from storing IN; the actual label is go-out/exit, not storage. Neither displayed label fits the other character.",
    "募": "Gather contributions is seeking recruits/donations, not a storage building; the displayed recruit/solicit label does not mean 倉's storing sense.",
    "召": "Put ON is clothing in a respectful verb, not storing; summon/respectful actions and granary/storehouse cannot answer one another.",
    "含": "Contain/include is inclusion or holding in the mouth, not putting away in a storehouse. Shared containment association does not establish either displayed label as the other's meaning.",
    "囲": "The source's store/preserve gloss was inspected alongside 囲う's enclosing branch. Its actual surround/enclose label is not established for 倉; a prison is an enclosed place, not the action surround. 倉's building label is not a source meaning of 囲.",
    "宝": "A treasury contains treasure, but 宝 is the valuables, not the storage place. Neither displayed label is a synonym for the other; no contents-to-container inference.",
    "容": "Contain/appearance concerns capacity or form. A granary has capacity but is not a synonym of contain, and no appearance sense of 倉 is established.",
    "寄": "Gather/collect is an expanded-keyword hit. Its displayed draw-near/stop-by label is not storing or a storehouse, nor is the new label a meaning of 寄.",
    "店": "English store is polysemous: 店 is a SHOP, not a warehouse. A warehouse-style shop is a compound use, not proof either character means the other's displayed title.",
    "張": "Put UP A TENT is stretching/spreading, not storing. Its assert branch does not fit 倉 either; the new building label does not fit 張.",
    "拾": "Picking up/gathering precedes possible storage but is not storing or the building. Neither displayed label is justified for the other character.",
    "指": "Put INTO is an isolated source-gloss token; the actual finger/pointing senses do not mean a storehouse or source-positive 倉 sense.",
    "採": "Picking/collecting/adopting does not mean storing. The scan deliberately overincluded collect; the new building label and 採's title do not answer each other's prompt.",
    "掲": "Put UP means hoist/post/display, not put away in storage. Publishing is also not a source meaning of 倉; shelved-publication whole-word お蔵入り does not mean publish.",
    "整": "Put IN ORDER is arranging/adjusting, not a storehouse or the act of storing; the phrasal-verb object disambiguates the token hit.",
    "植": "Put IN THE GROUND is planting, not a cellar or storage. Neither the title nor source planting sense supplies the other's displayed label.",
    "泊": "Put UP AT means lodging; anchoring and overnight staying do not mean a warehouse. A building used for storage is not thereby overnight accommodation.",
    "破": "Destroy/tear/break is an action, not the quoted もろし quality of fragility. 倉's old ほろぶ is perishing, not an unrestricted transitive tearing action; neither displayed title fits the other.",
    "著": "Put ON means wear; the actual write/remarkable title does not mean 倉. Being withheld from publication is a whole お倉入り sense, not a write/publish character gloss.",
    "被": "Put ON means covering/wearing, not storage; the source's roof mnemonic is not evidence that 倉 means cover/incur. Neither displayed title is valid for the other.",
    "討": "Destroy is in 討's dictionary meanings, but its actual attack/discuss label does not answer 倉. Old ほろぶ does not supply attack/discuss, and 討 is not a storage building.",
    "部": "Magazine is the publication counted by 部, not a storage magazine. Section/department and granary/storehouse are not mutual labels; 部屋's room is a whole compound.",
    "集": "Gathering is not storing: gathering people/attention/objects does not itself put them away. No gather character gloss is positively established for 倉, and 集 does not mean the storage building.",
}

guard = start_guard()
try:
    scan = json.loads((PACKET / "baseline-gloss-scan-002.json").read_text(encoding="utf-8"))
    assert set(scan["matches"]) == GUARDS.keys() | NO_GUARD.keys()
    rows = {r["kanji"]: r for r in scan["rows"]}
    decisions = []
    for ch in scan["matches"]:
        record = {"kanji": ch, "baselineTitle": rows[ch]["title"], "completeSourceMeanings": rows[ch]["meanings"], "comparisonCard": "comparison-cards/" + ch + ".md"}
        if ch in GUARDS:
            forward, reverse = GUARDS[ch]
            record.update(decision="guard", otherLabelForNewPrompt=forward, newLabelForOtherPrompt=reverse)
        else:
            record.update(decision="no-guard", bothPromptLabelDirections=NO_GUARD[ch])
        decisions.append(record)
    write(PACKET / "pair-dispositions.json", {
        "baseCommit": BASE, "newKanji": "倉", "actualScan": "baseline-gloss-scan-002.json",
        "scanMatches": decisions,
        "curatedChoices": [
            {"kanji": "金", "label": "gold, money", "bothDirections": "Gold/money is what a treasury may contain, not the place. Historical くら money-source/broker word senses do not make 倉 a generic word for gold/money; 金 has no storehouse sense. Similar spreading top only."},
            {"kanji": "全", "label": "whole; complete", "bothDirections": "Completeness is not storage or a storage building; 倉 does not mean whole/complete. Similar spreading top over a different lower block."},
            {"kanji": "合", "label": "fit together", "bothDirections": "Joining/fitting is not a granary or putting away; 倉 has no established fit-together sense. Broad top and lower box form the visual comparison."},
        ],
        "curatedPairwiseCheck": "金/全/合 have distinct money, completeness and joining labels; no direct meaning exclusion among them is declared or established here.",
        "guardPolicy": "Direct pairs only. Several are conservative broad-label guards for positive secondary character glosses, not universal synonym claims. Prior exclusions are never propagated transitively.",
        "additionalSourceSenses": {
            "Kanjipedia": "Sudden/hurried is a direct character sense, independently supported by 倉皇 and 倉卒; not dismissed by the outside-Joyo にわか mark.",
            "Jitsu": "Storing and prison are direct kun-gloss senses. ほろぶ/もろし occur under explicitly labelled old-dictionary quotations; retain without promoting to ordinary KANJIDIC2 readings. No baseline prison/jail or fragile/brittle-labelled card hit this scan.",
            "Nikkokuseisen": "Shared 倉・蔵・庫 lexical head includes historical money-broker, source-of-income, shelving/cancellation, abbreviated clothing/title and a regional trade numeral nine. These are whole-word contextual senses, not unrestricted character glosses; 金 is contents not container and 全/合 are not money/shelving labels.",
            "JMdict": "Full families include magazine/elevator in くら; these mean storage uses, not periodical or passenger lift. Whole compounds such as 胸倉 collar, 小倉 bean paste, proper names and お倉入り shelving do not transfer their full gloss to 倉 alone. All records/restrictions retained.",
        },
        "limits": "Finite author disposition of actual scanned baseline cards and positive source senses, not independent linguistic or exhaustive semantic certification.",
    })
    frozen = json.loads(git("show", f"{BASE}:docs/n1-sources/baseline-word-candidates.json"))
    candidates = [r for r in frozen if r["kanji"] == "倉"]
    declaring, incidental = [], []
    for folder in ("kanji", "words"):
        for path in sorted((REPO / folder).glob("*.md")):
            guard.check()
            text = path.read_text(encoding="utf-8")
            if "倉" not in text:
                continue
            rel = folder + "/" + path.name
            if folder == "words":
                match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
                if match and "倉" in [s.strip() for s in match.group(1).split(",")]:
                    declaring.append({"path": rel, "reading": re.search(r"^reading: (.+)$", text, re.M).group(1), "sha256": sha(path.read_bytes()), "linkPresent": "[倉](../kanji/倉.md)" in text})
                    continue
            if rel != "kanji/倉.md":
                incidental.append({"path": rel, "sha256": sha(path.read_bytes()), "disposition": "Incidental example/comparison or compound occurrence, not a declared support-word identity; no wrapper required."})
    assert len(declaring) == 1 and declaring[0]["path"] == "words/倉庫.md" and declaring[0]["linkPresent"]
    assert len(candidates) == 1 and candidates[0]["word"] == "倉庫"
    write(PACKET / "support-audit.json", {
        "baseCommit": BASE, "frozenCandidateRecords": candidates, "allActiveDeclaringArticles": declaring,
        "requiredReciprocalPairs": [["倉", "倉庫"]], "incidentalOccurrences": incidental,
        "sourceEntry": "1399120", "spelling": "倉庫", "reading": "そうこ",
        "allocation": "ソウ + コ, corroborated by the source character readings and existing complete word article; not inferred from arbitrary kana substrings.",
        "sense": 1, "senseGlosses": ["storehouse", "warehouse", "godown"],
        "wordChange": "One link wrapper at the substantive component introduction only; all original metadata, easier N2 level, exclusions and non-link prose preserved.",
    })
    pages = json.loads((HERE / "external-pages" / "receipt.json").read_text(encoding="utf-8"))
    write(PACKET / "external-source-bindings.json", {
        "captures": pages,
        "boundedExcerpts": [
            {"source": "kanjipedia", "excerpt": "②にわか。あわてる。「倉皇」「倉卒」", "claim": "Positive sudden/hurried character sense; にわか is also explicitly in the kun listing."},
            {"source": "kotobank", "dictionary": "Jitsu", "excerpt": "2. 蔵と通じ、おさめる。 3. ひとや。", "claim": "Positive secondary storing/prison kun-gloss senses."},
            {"source": "kotobank", "dictionary": "Jitsu, old-dictionary quotation", "excerpt": "倉　クラ・ホロブ・モロシ", "claim": "Source labels these as old-dictionary readings, not modern examples."},
        ],
        "readingDispositions": [
            {"raw": "ソウ", "source": "frozen KANJIDIC2", "practice": True, "example": "倉庫/そうこ", "JMdict": "1399120"},
            {"raw": "くら", "source": "frozen KANJIDIC2", "practice": False, "example": "倉/くら", "JMdict": "1592380", "reason": "Valid native noun; no standalone linked word article in this slice. Not a rarity judgment."},
            {"raw": "にわか", "source": "Kanjipedia", "practice": False, "reason": "Positive supplemental character reading; retain source boundary, explicitly included in host wrong-option check."},
            {"raw": "ほろぶ,もろし", "source": "Jitsu quoted old dictionaries", "practice": False, "reason": "Explicitly labelled historical source quotations; not dropped because of missing priority or outside-Joyo status. Both explicitly included in host exposure."},
            {"raw": "おさめる,ひとや", "source": "Jitsu kun-gloss labels", "practice": False, "reason": "Semantic glosses, not asserted to be ordinary surface readings. Included conservatively as extra keys in the host check."},
        ],
        "sourceLimit": "Search summary had inconsistent Kanjipedia URLs; only the inspected/captured correct 0004231200 page supports claims. Complete external HTML remains local; only hashes and bounded attributable excerpts are published.",
    })
    print(json.dumps({"scanPairs": len(decisions), "guards": list(GUARDS), "declaringWords": len(declaring), "incidentalOccurrences": len(incidental)}, ensure_ascii=False))
finally:
    write(HERE / "author-packet-memory-001.json", guard.finish())
