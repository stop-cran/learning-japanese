import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b129_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

# These are authored decisions, not automatically inferred from token matches.
REASONS = {
    "茉": {
        "莉": ("Same jasmine-name element; the complete 茉莉 family supports overlap in either displayed direction.", "guard"),
        "花": ("Jasmine bears flowers; broad flower can be plausible for 茉, but jasmine is not the whole range of 花.", "guard"),
        "咲": ("The displayed noun-like blossom/bloom can plausibly describe jasmine; blooming is not specifically jasmine.", "guard"),
        "植": ("Plant/put in the ground is broader than jasmine; guard the unresolved noun-like English label without asserting equivalence.", "guard"),
        "木": ("JMdict 1534520 includes shrub/bush as well as tree; Daijisen calls 茉莉 a fragrant woody plant. The broad label is not safely wrong.", "guard"),
        "樹": ("The complete 木/樹 family permits shrub under either spelling; 樹's establish sense does not erase the positive plant overlap.", "guard"),
        "幹": ("Trunk/main part and separate stem/stalk/shaft senses concern a part, not the jasmine plant; jasmine is not a displayed meaning of 幹.", "distinct"),
        "松": ("Pine and its highest-tier secondary noun are not jasmine; shared まつ sound is checked separately, not a meaning guard.", "distinct"),
        "桂": ("Katsura/cinnamon/shogi-knight/literary moon references are not jasmine. A fragrant tree is not thereby the same species.", "distinct"),
        "梓": ("Birch/catalpa/mallotus, printing block, ritual bow and medium senses are distinct from jasmine in both directions.", "distinct"),
        "梨": ("Pear tree/fruit is a different botanical identity; theatrical compounds do not name jasmine.", "distinct"),
        "椋": ("Muku tree, its fruit and the abbreviated starling are different from jasmine; plant-category membership alone is not identity.", "distinct"),
        "楠": ("Camphor tree/wood is different from jasmine; no transfer from shared woody-plant category.", "distinct"),
        "榛": ("Hazel and alder secondary identities are not jasmine; edible nut association does not establish jasmine.", "distinct"),
        "稲": ("Rice plant is a distinct species/crop, not a jasmine meaning; plant alone is not this displayed label.", "distinct"),
        "苗": ("Seedling/rice seedling is a growth stage, not a name of jasmine; Miao/Hmong noun is unrelated.", "distinct"),
        "輪": ("Counter for flowers does not make wheel/ring jasmine; complete ring/circle/loop and counter entries remain distinct.", "distinct"),
        "未": ("Not-yet and Sheep-branch/time/direction/month senses do not mean jasmine. Rejected as curated choice because ミ collides with supplied み.", "rejected"),
        "本": ("Book/script, origin/main/real/present and counting senses do not denote jasmine. Shape similarity is independent of meanings.", "curated"),
        "古": ("Old/antiquity is not jasmine; neither the plant name nor source-positive supplemental 茉 records make it old.", "curated"),
        "石": ("Stone/jewel/flint/game-piece/calculus and volume/counter uses are not jasmine; an independent nonbotanical meaning comparison.", "curated"),
        "末": ("End/tip, new growth, descendants/future/trifles and suffix powder are not jasmine; rejected as wrong on reading because マツ/バツ overlap.", "rejected"),
    },
    "絹": {
        "布": ("Nikkoku explicitly includes 布帛 under native きぬ; cloth can be plausible for 絹 although silk is narrower than all cloth.", "guard"),
        "糸": ("Silk fibre/thread is part of the complete sense range; thread/yarn/string is broader, not safely wrong.", "guard"),
        "維": ("The full character record includes fibre; broader fibre can describe silk. Preserve 維's support/maintain/rope and これ uses separately.", "guard"),
        "紅": ("Complete JMdict 2414440 allows single 紅 もみ, red silk lining. Silk is plausible for that secondary noun even though the displayed title is crimson.", "guard"),
        "綿": ("Daijisen and Nikkoku native わた include silk wadding, and Jitsu gives きぬわた. Cotton title alone cannot erase this reverse overlap.", "guard"),
        "捕": ("Jitsu's historical snare/set-a-snare use can intersect capture; guard the unresolved broad action, not universal synonymy.", "guard"),
        "掛": ("Setting a snare intersects the broad hang/set range of 掛ける. Conservative direct guard does not identify all hanging with silk.", "guard"),
        "享": ("Receive/enjoy English glosses and enjoyment offerings are not silk or setting a trap; an accidental relation via receive is insufficient.", "distinct"),
        "匹": ("Small-animal/cloth-roll counters and standalone roll-of-cloth describe a count or roll, not silk as material. Silk does not mean a matching pair.", "distinct"),
        "受": ("Receive/accept, examinations and Buddhist sensation do not denote silk; accepting cloth is merely a possible object relation.", "distinct"),
        "召": ("Summon, put on, eat/drink and catch-a-cold honorific uses do not mean silk. Donning a silk garment does not equate them.", "distinct"),
        "幅": ("Width/range and scroll/counter-for-scrolls do not mean silk, even when a scroll support can be silk.", "distinct"),
        "掲": ("Put up/display/publish is not the Jitsu set-a-snare action solely because both can use hang in English.", "distinct"),
        "服": ("Clothing, obey/submit and doses do not mean silk as material; wearing a silk garment does not make all clothing silk.", "distinct"),
        "略": ("Abbreviation/strategy/approximately and capture/plunder character glosses do not establish trapping in a snare. No inheritance from 捕 guard.", "distinct"),
        "着": ("Wear/arrive, clothing and clothing counters are not silk; sense separation, not title-only rejection.", "distinct"),
        "移": ("Move/transfer/change is not silk. To move cloth is an object relation, not lexical overlap.", "distinct"),
        "純": ("Pure/innocent/genuine describes composition or character; 正絹 pure silk does not make 絹 alone mean pure.", "distinct"),
        "著": ("Author/work/conspicuous and older wearing uses do not mean silk; the material of clothing is not the act of wearing it.", "distinct"),
        "衣": ("The separate 衣 きぬ/い family names clothing/garment/dress, not silk material. Homophony is not synonymy; reading collision tested separately.", "distinct"),
        "被": ("Suffer/receive/cover and passive -ee uses are not silk; a textile covering is only one possible object.", "distinct"),
        "紙": ("Complete 紙 families name paper/newspaper and newspaper counters, not silk; thread-shaped radical does not determine material.", "curated"),
        "約": ("Promise/engagement, approximately and shortening/contraction are not silk, cloth or snare; shared radical is merely visual.", "curated"),
        "級": ("School grade/class/rank/kyu are not silk. The thread component does not transfer silk meaning.", "curated"),
    },
    "虹": {
        "弧": ("Rainbow can be described as an arc; arc is broader than rainbow. Guard the broad label, not every curved thing as a rainbow.", "guard"),
        "橋": ("Jitsu explicitly records borrowed bridge gloss; bridge label can be plausible for that qualified 虹 use.", "guard"),
        "皿": ("Jitsu oil-dish gloss includes a dish; the broad dish choice is not safely wrong. A plate is not generally a rainbow.", "guard"),
        "灯": ("Oil dish can function as a lamp; missing image-glyph context leaves the lamp label conservatively guarded, without claiming exact lexical equivalence.", "guard"),
        "乱": ("Jitsu explicitly gives みだれる; disordered/confused/rebellion ranges intersect the displayed disorder choice.", "guard"),
        "争": ("Jitsu explicitly gives あらそう, with quarrel/dispute supported in full JMdict 1400620.", "guard"),
        "攻": ("Jitsu's unresolved せめる can mean attack; preserve this plausible broad reading/sense rather than selecting a convenient interpretation.", "guard"),
        "討": ("Attack and argument/discussion secondary ranges intersect せめる/あらそう; not all deliberation is quarrelling.", "guard"),
        "責": ("The unspecified せめる can also be blaming/pressing. Guard unresolved broad label; not a claim that rainbow ordinarily means blame.", "guard"),
        "詰": ("Press/close-question secondary meanings plausibly intersect an unresolved せめる gloss; conservative guard only.", "guard"),
        "論": ("Complete single 論 family includes dispute/controversy, overlapping あらそう; reasoning is not universally quarrel.", "guard"),
        "蛇": ("Jitsu and encyclopedias preserve an old serpent/dragon conception. Guard the broad creature choice without asserting modern rainbow and snake nouns are synonyms.", "guard"),
        "動": ("Move/motion and disturbance as movement do not by themselves mean the Jitsu disorder/dispute use. No automatic transfer from 乱.", "distinct"),
        "婦": ("Wife/woman and bride glosses do not name a rainbow. Cultural personification does not establish the generic woman noun as a character meaning.", "distinct"),
        "巳": ("Zodiac Snake branch/time/direction/month is not an ordinary creature noun; cultural serpent association does not make 虹 a zodiac sign.", "distinct"),
        "張": ("Stretch/spread, bow counters and constellation uses do not denote rainbow; English bow shape is not the action or counter.", "distinct"),
        "拝": ("Bowing/worship/respectfully yours is unrelated to a curved arc; English bow is a homograph.", "distinct"),
        "撃": ("Shoot/strike has forceful contact not established by the unspecific せめる gloss; no transitive inheritance from attack guard.", "distinct"),
        "油": ("Oil is the contents/fuel, not the oil dish named by Jitsu; reverse rainbow label does not fit oil.", "distinct"),
        "礼": ("Etiquette/thanks/bow/gift/ceremony/key-money do not denote rainbow. Bowing versus an arc is English polysemy.", "distinct"),
        "罪": ("Crime/penalty/fault/culpability is not accusing/blaming as an action; do not extend 責's guard transitively.", "distinct"),
        "美": ("Beauty/beautiful and honorific み are qualities, not rainbow lexical senses; a beautiful rainbow need not make the words synonyms.", "distinct"),
        "背": ("Back/height/ridge/disobey is not rainbow; a bowed back is not a rainbow meaning.", "distinct"),
        "菜": ("Greens/rapeseed and side dish is food, not the oil-dish vessel; English dish polysemy matters.", "distinct"),
        "辰": ("The Dragon zodiac branch is not a generic dragon creature or rainbow; time/direction/month secondary senses are also distinct.", "distinct"),
        "紅": ("Red/crimson, rouge/lipstick and red-silk-lining secondary noun do not mean rainbow. One possible rainbow colour is not the complete phenomenon.", "curated"),
        "功": ("Merit/achievement/service and qualified いたわり entry senses do not mean rainbow, disorder or a dish.", "curated"),
        "石": ("Stone/jewel, flint, game stone/calculus and measures/counters do not mean rainbow, even if a jewel can show colours.", "curated"),
    },
}

guard = start_guard()
try:
    all_pairs = []
    for ch in CHARS:
        fm, _ = n1lib.parse(normalized(REPO / "kanji" / (ch + ".md")))
        scan = json.loads((PACKET / "scans-004" / (ch + ".json")).read_text(encoding="utf8"))
        required = set(scan["matches"]) | set(fm["distractors"]) | set(fm["quiz_exclusions"])
        assert required <= REASONS[ch].keys(), (ch, required - REASONS[ch].keys())
        assert set(fm["quiz_exclusions"]) == {k for k, (_, d) in REASONS[ch].items() if d == "guard"}
        assert set(fm["distractors"]) == {k for k, (_, d) in REASONS[ch].items() if d == "curated"}
        rows = []
        for other, (reason, disposition) in REASONS[ch].items():
            path = PACKET / "comparison-cards" / (other + ".md")
            raw = path.read_bytes()
            assert raw == git("show", f"{BASE}:kanji/{other}.md")
            ofm, _ = n1lib.parse(raw.replace(b"\r\n", b"\n").decode())
            if disposition == "guard":
                forward = f"{ofm['title']!r} is plausible or unresolved for {ch} in the qualified source range. {reason}"
                reverse = f"{fm['title']!r} on {other} is not asserted universally correct; the complete secondary ranges must remain visible. {reason}"
            else:
                forward = f"{ofm['title']!r} is not established as a meaning of {ch}. {reason}"
                reverse = f"{fm['title']!r} is not established as a meaning of {other}, including the full inspected secondary senses. {reason}"
            rows.append({"pair": [ch, other], "comparisonTitle": ofm["title"], "decision": disposition,
                         "targetLabelOnComparison": reverse, "comparisonLabelOnTarget": forward,
                         "sourceBasis": "Full baseline card plus complete character record and complete applicable exact-spelling JMdict families; target source notes retain external historical qualifications.",
                         "baselineCardSha256": sha(raw), "scanMatch": other in scan["matches"]})
        all_pairs.append({"kanji": ch, "targetTitle": fm["title"], "scanFile": f"scans-004/{ch}.json",
                          "scanSha256": sha((PACKET / "scans-004" / (ch + ".json")).read_bytes()),
                          "scanRows": len(scan["rows"]), "pairs": rows})
    for a, b in [("茉", "絹"), ("茉", "虹"), ("絹", "虹")]:
        all_pairs.append({"newMemberPair": [a, b], "decision": "distinct",
                          "bothDirections": "Jasmine, silk and rainbow are distinct lexical identities. Historical snare/cloth and bridge/dish/dispute senses do not establish overlap with the other new members."})
    write(PACKET / "pair-dispositions.json", {
        "base": BASE, "members": all_pairs,
        "rule": "One direct declaration makes exclusion symmetric in the host model; no transitive inference. Each finite pair records both displayed-label directions. A conservative guard protects unresolved broad labels, not universal synonymy.",
        "rejectedAbsentChoices": [{"kanji": "朱", "target": "茉", "reason": "No baseline card; preflight failure preserved."},
                                  {"kanji": "江", "target": "虹", "reason": "No baseline card; preflight failure preserved."}],
        "limits": "Finite source-based audit, not a proof of all possible synonymy, arbitrary/custom pools, multiple-borrow, native/device, visual or publication acceptance.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    captures = []
    for receipt_name in ("receipt-001.json", "receipt-002.json"):
        for item in json.loads((HERE / "external-pages" / receipt_name).read_text(encoding="utf8")):
            if item["character"] not in [*CHARS, "綿"]:
                continue
            raw_path = Path(item["localRawCapture"])
            assert sha(raw_path.read_bytes()) == item["rawSha256"]
            assert sha(raw_path.with_suffix(".txt").read_bytes()) == item["textSha256"]
            captures.append({**item, "localTextCapture": str(raw_path.with_suffix(".txt")),
                             "completeCaptureCommitted": False})
    write(PACKET / "external-source-bindings.json", {"captures": captures,
        "excerpts": [
            {"character": "茉", "provider": "Kotobank / Digital Daijisen", "quote": "マツ（呉）　マ（慣）", "disposition": "Conventional マ distinct from linked まつりか; not automatically practice."},
            {"character": "茉", "provider": "Kotobank / Jitsu", "quote": "[字訓] まつり", "disposition": "Separate source classification. KANJIDIC2 み is nanori, not kun; Weblio/Wiktionary's kun み and マチ remain discrepant."},
            {"character": "絹", "provider": "Kotobank / Nikkoku", "quote": "また、布帛", "disposition": "Positive standalone cloth sense, not merely compound evidence."},
            {"character": "絹", "provider": "Kotobank / Jitsu", "quote": "羂と通じ、わな、わなをかける。", "disposition": "Qualified borrowed character use; きぎぬ and historical かとり/かく are separately tested lookup keys."},
            {"character": "虹", "provider": "Kotobank / Jitsu", "quote": "訌に通じ、みだれる、あらそう、せめる。", "disposition": "Conservative broad action guards; also source-positive bridge/oil-dish/flag uses. Missing image glyph is not guessed."},
            {"character": "虹", "provider": "Kotobank / Nikkoku", "quote": "「にじ（虹）」をいう上代東国方言。", "disposition": "のじ specifically classified; ぬじ separately attested. Jitsu ヲニジ supplied as おにじ conservatively."},
            {"character": "綿", "provider": "Kotobank / Jitsu", "quote": "綿はきぬわた、棉はきわたをいう。", "disposition": "Native complete monolingual senses independently establish silk-wadding overlap; direct 絹/綿 guard, not dismissal as cotton."}
        ],
        "copyrightBoundary": "Full copyrighted external HTML/text captures stay local. Only hash/query bindings, short attributable excerpts and authored analysis are committed.",
        "limitations": ["Text extraction omits image glyphs and formatting; missing historical glyphs are unresolved, not reconstructed.",
                        "Complete JMdict families preserve search-only, no-kanji, spelling/reading/sense restrictions, priorities and secondary senses.",
                        "The convenience readback is lossy for repeated spelling flags; complete XML is authoritative.",
                        "Source-positive uses are not rejected for standard-list status, absent priorities or unsupported rarity claims."]})
    print(json.dumps({"pairRows": sum(len(x.get("pairs", [])) for x in all_pairs), "capturesBound": len(captures)}, ensure_ascii=False))
finally:
    write(HERE / "editorial-memory-001.json", guard.finish())
