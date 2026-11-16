import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from b130_common import BASE, HERE, REPO, git, normalized, sha, start_guard, write

PARENT = "ce1b5c895fac90852143f322a115c2de4e768e20"
OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
INITIAL = REPO / "docs" / "n1-sources" / "batch-130"

# Pair, disposition, exact queries, positive evidence, both displayed directions, qualification.
DECISIONS = [
    ("耗擦", "guard", ["擦る", "擦れる"],
     "Independent Daijisen 耗 gives frictional wear; complete すれる 1595930 explicitly includes becoming worn and wearing out.",
     "Scrape/scrub can describe the rubbing operation involved in 耗's attested frictional wear; this is broader than an exact synonym.",
     "Wear down through use is defensible for 擦れる's positive wear-out sense.",
     "Not all rubbing causes depletion; a direct guard protects the overlapping wear reading."),
    ("耗摩", "precaution", ["摩る", "摩する", "擦れる"],
     "Independent 耗 has すりへる; 摩 has rub/chafe/grind in its complete character record and rub/scrub/scrape in 摩する. The complete すれる family additionally retains rare 摩れる.",
     "Rub/chafe is a consequential broad choice for the frictional-wear sense, although it need not name the resulting loss.",
     "Wear down through use can fit the retained 摩れる wear-out sense; 摩する's drawing-near and pressing senses remain distinct.",
     "A conservative direct guard, not constituent equality inferred solely from 摩耗 and not universal rubbing/depletion identity."),
    ("耗削", "guard", ["削る", "削ぐ", "削減"],
     "Complete 削る and the actual card include reducing an amount or cutting down; independent 耗 includes へる/へらす.",
     "Shave/pare can fit the physical removal side of wearing down, not every numerical decrease.",
     "Decrease is defensible for 削る's independent reducing-amount sense, beyond physical shaving.",
     "The overlap is reduction, not a claim that every cut or reduction consumes resources."),
    ("耗便", "guard", ["便", "便り"],
     "Kanjipedia explicitly defines 耗's supplemental sense as たより/知らせ. Complete 便り 1512410 positively gives news, tidings and information as well as correspondence/letter.",
     "Convenience is not a definition of 耗; the positive news nouns, rather than the first title, establish the overlapping semantic pair.",
     "Decrease/wear is not a definition of 便; the direct guard conservatively respects the independent shared secondary news sense in the two cards' complete ranges.",
     "Does not promote たより into metadata or practice, equate convenience with depletion, or make every written object news."),
    ("拍突", "guard", ["突", "突く"],
     "Daijisen and 字通 independently define 拍 hand-striking; complete 突く 1456890 includes hit/strike independently of thrust/prick.",
     "Thrust/sudden is not the whole range; its striking region can be a defensible broad choice for hand-striking.",
     "Clapping fits a hand-striking region, though a musical beat is not suddenness and not every 突く is clapping.",
     "Direct precaution for an ordinary striking overlap; no unrestricted allocation from the 打つ/拍つ family is needed."),
    ("耗文", "bounded-noncollision", ["文"],
     "Complete 文/書 1505080 gives a formal/literary letter, note or mail, books and literary arts. Other complete 文 families retain sentence, design, scriptural and unit senses. Kanjipedia allocates 耗 to news/information, not unrestricted written objects.",
     "Sentence/writing names composition or written expression; it does not define diminution, wear, or news as communicated content.",
     "Decrease/wear through use does not define 文's letter, composition, pattern or literary arts. A letter can convey news without being the noun for that news.",
     "The literary flag is retained, not used to discard the positive letter sense. This bounded content-versus-writing distinction is not an exhaustive denial of every historical use."),
    ("耗信", "precaution", ["信", "音信"],
     "New complete Daijisen 信 character entry explicitly gives a distant signal or tidings; the complete 日本国語大辞典 信 noun independently includes おとずれ/たより/音信. This goes beyond JMdict's received-message counter.",
     "Trust/belief does not define 耗, but 信's independently established secondary news/tidings sense matches the positive 耗 news sense.",
     "Decrease/wear does not define trust or faith; the semantic guard protects the source-positive secondary news range rather than claiming the first titles are interchangeable.",
     "A message counter alone was insufficient. The new independently defined noun/character sense supports this direct precaution."),
    ("耗疲", "guard", ["疲れる", "疲れ", "疲らす"],
     "Complete 疲れる 1483740 explicitly includes becoming worn out of a well-used object. Its fatigue and archaic starvation senses are retained. Independent 耗 has frictional wear and using up.",
     "Grow tired may suggest exhausted reserves, but that whole-word association alone is not the decisive proof.",
     "Wear down through use is directly defensible for 疲れる's well-used-object sense.",
     "This is new complete-family evidence for object wear, not a claim that all tiredness is bare-character depletion."),
    ("耗磨", "precaution", ["磨く", "磨る", "擦れる", "摩耗", "磨耗"],
     "Complete 磨く includes grinding a lens, scouring and scrubbing; complete 1595930 explicitly retains rare 磨れる with the wear-out sense. Independent 耗 is すりへる.",
     "Polish/grind is a potentially defensible broad label for abrasion; skill refinement is not depletion.",
     "Wear down through use is defensible for the rare but positively retained 磨れる wear-out sense, not merely the 磨耗 compound variant.",
     "Guard as a qualified rare-spelling/wear precaution. This does not make ordinary polishing identical to decrease or remove the spelling restriction."),
    ("耗研", "bounded-noncollision", ["研", "研ぐ", "研磨", "磨く"],
     "Complete 研ぐ 1598700 positively specifies sharpening/honing/whetting/grinding, rice washing, scouring/polishing/burnishing. 研磨 1592730 adds refining skills and disciplined study; rare 研く belongs to 磨く's surface/skill-refinement family, not the separate 磨れる wear-out family.",
     "Polish/study closely specifies edge or surface treatment and refinement/research; it is not a name for the loss/depletion itself.",
     "Decrease/wear down through use does not define research, sharpening a useful edge or making a surface polished. Abrasive material loss can accompany that work without being the operation's definition.",
     "This disposition uses the actual full physical families, not just abstract study or a transitive 摩/研 guard. No exhaustive denial of every historical 研 sense is claimed."),
    ("耗欠", "precaution", ["欠", "欠ける", "欠く"],
     "Complete 欠ける retains damage, becoming lost, shortage and explicitly waning of the moon; 欠く retains chipping/breaking/cracking and lack. Independent 耗 means decrease and has qualified damage/なくする senses.",
     "Lack/gap is broader than depletion but may be a defensible reduced/deficient condition against the qualified 耗 damage/loss range.",
     "Decrease is defensible for the positive lunar-waning sense; it is not a definition of absence from a meeting or a missing team member.",
     "Direct precaution rests on positive diminution/damage evidence, not state-versus-action reasoning or the idea that every lack was caused by consumption."),
    ("耗乏", "precaution", ["乏しい", "貧乏"],
     "Complete 乏しい retains scarce/limited/destitute/lacking; 貧乏 retains poverty-stricken/destitute. Independent 字通 耗 positively retains impoverished/thin land and depletion, with historical qualifications.",
     "Scarce/lacking can fit that qualified impoverished-resource range; numerical decrease does not always create scarcity.",
     "Decrease/wear is not the generic definition of poverty. A precaution covers the qualified depletion/insufficiency boundary, not a universal definition of 乏.",
     "Neither the financial/soil distinction nor an existing 貧 guard resolves the direct pair. Historical ordinary-use allocation remains qualified."),
    ("耗枯", "precaution", ["枯れる", "枯らす"],
     "Complete 枯れる gives plant withering/dying; 枯らす gives killing/drying vegetation and seasoning lumber. 字通 耗 positively discusses vegetation's 衰敗, while image-dependent historical glyph allocation is unresolved.",
     "Wither/dry up can be a broad answer in that explicitly recorded plant-decline region of 耗.",
     "Decrease/wear can describe decline, but is not a full definition of plant death, lumber seasoning or personal maturation.",
     "Direct precaution for the positive qualified plant-deterioration range, without promoting all historical usages to ordinary modern synonyms."),
    ("耗下", "guard", ["下", "下げる", "下がる", "下る"],
     "Complete 下げる 1184170 includes lower/reduce; 下がる 1184160 includes becoming lower, dropping and deterioration. Independent 耗 is decrease, not solely physical abrasion.",
     "Down/below can denote the direction of an amount's decrease, beyond spatial examples.",
     "Decrease is directly defensible for lower/reduce/go-down senses; below/under, a lower volume and giving remain distinct.",
     "A numerical/quality reduction overlap, not a claim that every descent is resource depletion."),
    ("耗落", "guard", ["落", "落ちる", "落とす"],
     "Complete 落ちる 1548550 explicitly includes decreasing popularity, quality, speed or sales and declining/deteriorating; 落とす 1589260 includes lessen/reduce.",
     "Fall down can be a broad answer for decreasing quantities, not just an object dropping spatially.",
     "Decrease is directly defensible for those positive amount/quality senses.",
     "Does not equate every fall, disappearance, failed exam or punch line with depletion."),
    ("耗退", "precaution", ["退く", "退ける", "退"],
     "Complete rare 退く ひく 1595086 independently includes lessen/subside/ebb/go down, usually written 引く. Other complete 退く families retain stepping aside, retreat and retirement.",
     "Withdraw/retreat can be a consequential broad label for receding/ebbing, but the unallocated old 耗 strings alone are not proof.",
     "Decrease is defensible for the positively retained lessening/ebbing sense; resignation and stepping aside remain distinct.",
     "Qualified rare-spelling precaution; retains the usual-spelling restriction and does not infer a modern sense from untranslated old strings."),
    ("耗用", "precaution", ["用", "用いる"],
     "Complete 用いる 1546210 gives use/utilize. Independent Daijisen 耗 explicitly specifies using so as to diminish, and the card teaches using up reserves.",
     "Use is broad enough to be a consequential answer choice for using up, although purpose/business is not depletion.",
     "Decrease/wear through use is not a definition of every use or employment; the direct precaution prevents the broad use label competing with the taught consumptive use.",
     "No claim that all use consumes; this direct decision is independent of the existing 使 exclusion."),
    ("拍鳴", "guard", ["鳴らす", "鳴る", "鳴く"],
     "Complete 鳴らす 1532880 includes beat, sound and snap fingers; independent 拍 means hand-striking/clapping. 鳴る's echo/roar and animal-call senses remain intact.",
     "Ring is broader than clapping, but the independent sounding/beating action gives a consequential overlap beyond merely the audible result of applause.",
     "Clap/beat is defensible for 鳴らす's positive beat/snap-fingers region, not for every animal call.",
     "No allocation of cymbal-sounding from the broad 拍つ family is required for this direct guard."),
    ("拍響", "bounded-noncollision", ["響", "響き", "響く"],
     "Complete 響く 1238610 gives resounding, being heard at a distance, reverberating/vibrating, coming home/remain and effects/impressions. Complete 響き 1602130 names echo, distinctive sound and its quality/feeling; 1612890 separately retains rare 響く どよめく and kana preference.",
     "Resound/echo names sound carrying or resonating, not the hand-striking/clapping operation or timed musical pulse. A clap can resound without resounding meaning clap.",
     "Clap/musical beat is not a definition of sound resonance or an effect/impression reaching someone. The broad 打つ family's moving/impressing sense has no independent ordinary bare-拍 allocation here.",
     "Bounded distinction based on positive sound/effect definitions, not an exclusively audible treatment, a different-title shortcut or transitive 音 guards. Historical family allocation stays unresolved, not declared absent."),
    ("拍勉", "precaution", ["勉める", "努める", "勉"],
     "The complete 勉 character record independently includes encourage; 努める/rare 勉める 1240820 gives exertion/endeavour. Independent 字通 拍 positively gives はやしたてる.",
     "Strive/exert effort is not clapping, but the independently positive encouragement meaning prevents dismissing the pair by that first label.",
     "Clap can name encouragement through applause, not 勉's every diligent-effort use.",
     "Conservative direct encouragement-label precaution; does not allocate all 勉める senses to ordinary 拍 or erase the rare spelling."),
    ("拍勇", "precaution", ["勇", "勇む", "勇ましい"],
     "Complete 勇 character record retains cheer up/high spirits; 勇む 1539700 gives high spirits, encouragement/liveliness; 勇ましい 1539660 includes stirring/vigorous/rousing. 拍 independently retains cheering.",
     "Courage/bravery is not a definition of 拍, but the positive cheering/high-spirits boundary is consequential despite the first label.",
     "Clap/beat is not a general definition of courage or eagerness; a direct precaution respects the positively sourced cheering region without asserting full synonymy.",
     "Do not replace encouragement of another with all states of bravery; guard is calibrated to that shared broad region."),
    ("拍乗", "precaution", ["乗り", "乗る", "乗せる", "乗"],
     "Complete 乗り 1354720 positively includes rhythm/enthusiasm with a kana-preferred qualification in that sense; 乗る 1355120 includes getting into the swing to sing/dance. Daijisen 拍 independently lists 乗り in its rhythm discussion.",
     "Ride/board is not 拍's meaning; the positive secondary rhythm range, not boarding, motivates the guard.",
     "Musical beat is a defensible broad choice in the secondary rhythm/keeping-time region, not in vehicle boarding, powers or multiplication.",
     "Preserve the kana-preferred sense qualification; do not make every instance of 乗り a literal pulse."),
    ("拍記", "precaution", ["記", "記す"],
     "Complete 記す/誌す/rare 識す 1223140 includes write, note, describe, inscribe, mark and remember. Complete 打つ/rare 拍つ 1408810 retains writing-in/marking without spelling-local allocation.",
     "Record in writing is consequential against the retained but unallocated writing/marking region of the rare 拍つ family.",
     "Clap/beat does not define ordinary 記す; the guard protects a broad allocation uncertainty rather than inventing a bare-拍 writing sense.",
     "Direct precaution, not established ordinary synonymy or transitive protection through 書; lexical allocation remains unresolved."),
    ("拍識", "precaution", ["識", "識す"],
     "Independent complete 識 character record includes write; 2228450 includes written by after a signature, and rare 識す belongs to complete 1223140. Complete rare 拍つ family retains unallocated write-in/mark.",
     "Knowledge/awareness does not define 拍, but the positive secondary writing sense meets the consequential family-allocation question.",
     "Clap/beat is not a definition of knowledge, consciousness or writing. A precaution protects the retained unallocated writing region without promoting it to ordinary bare 拍.",
     "Retain the after-signature and rare-spelling qualifications; not a different-title or missing-source-only rationale."),
    ("拍筆", "precaution", ["筆"],
     "Complete 筆 1487770 distinguishes brush/pen, brush writing/penmanship and ふで-restricted composing text; ひつ also counts land plots. Complete rare 拍つ family retains unallocated writing-in/marking.",
     "Brush/writing is consequential in that retained writing/marking region, not because every writing implement resembles a clapper.",
     "Clap/beat does not define a brush, text composition or a land lot. Direct precaution covers the unresolved writing allocation, not every sense of 筆.",
     "Preserve reading restrictions and implement/action distinctions; no claim that bare 拍 ordinarily composes text."),
    ("塀城", "precaution", ["城", "城壁"],
     "Complete 城 families distinguish castle/fortress/place-name suffix and archaic wall-surrounded fortification; 城壁 separately means defensive wall. New complete Daijisen 城 entries define a fortified place, not any fence. The separately attributed 字通 城 explicitly retains historical カキ among lookup forms.",
     "Castle does not normally name a garden fence. The positive historical enclosing-wall lookup nevertheless motivates a qualified direct precaution.",
     "Boundary wall/fence names the enclosing structure, not the whole castle or fortified town; it can meet that qualified historical カキ question.",
     "Not an inference of bare 城 wall solely from 城壁, nor resolution of the old form's modern range or image-only glyphs."),
    ("耗書", "bounded-noncollision", ["書", "文"],
     "Complete 書 2037940 gives book/document, calligraphy/penmanship/handwriting and letter/note; complete 文/書 1505080 retains literary letter/mail and books. Kanjipedia independently specifies 耗 news/information.",
     "Write names composing/inscribing text, not the information or news conveyed; it is not a definition of decrease/wear or the positive news noun.",
     "Decrease/wear is not a definition of 書's writing, document, calligraphy or letter. A letter can convey news without being interchangeable with its content.",
     "Does not discard the secondary letter noun, rely just on different first titles, or infer protection through 拍/書. Bounded writing/content distinction, not an exhaustive historical negative."),
    ("耗音", "precaution", ["音", "音信"],
     "New complete Daijisen 音 character entry independently gives たより under both オン and イン; its おと entry also retains visiting/tidings as a quoted historical sense. Kanjipedia 耗 independently has たより/知らせ.",
     "Sound is not depletion or news; nevertheless the independently attested news/tidings character sense overlaps 耗 without inference from 音耗.",
     "Decrease/wear does not define sound or its phonetic/music uses. Guard covers the shared positive secondary news range.",
     "Does not claim a counter or a compound alone proves the noun. Keeps historical examples distinct from ordinary sound and does not promote supplemental readings."),
]


def load(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def metadata(text):
    block = text.split("---", 2)[1]
    return dict(line.split(": ", 1) for line in block.strip().splitlines())


guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    receipt = load("source-receipt.json")
    membership = load("query-membership.json")
    rows = []
    for pair, decision, queries, positive, other_on_new, new_on_other, qualification in DECISIONS:
        target, other = pair
        target_fm = metadata(normalized(REPO / "kanji" / (target + ".md")))
        other_path = OUT / "comparison-cards" / (other + ".md")
        other_fm = metadata(normalized(other_path))
        assert sha(other_path.read_bytes()) == receipt["comparisonCards"][other]["sha256"]
        refs = {key: receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"][key]
                for key, selectors in membership.items()
                if set(selectors) & {"exact-spelling:" + q for q in queries}}
        assert refs, pair
        guarded = other in re.findall(r"[\u3400-\u9fff]", target_fm["quiz_exclusions"])
        assert guarded == (decision != "bounded-noncollision"), pair
        if not guarded:
            assert target not in re.findall(r"[\u3400-\u9fff]", other_fm.get("quiz_exclusions", ""))
        rows.append({
            "pair": [target, other], "decision": decision,
            "targetDisplayedTitle": target_fm["title"], "comparisonDisplayedTitle": other_fm["title"],
            "completeComparisonCard": receipt["comparisonCards"][other],
            "exactQueries": queries, "completeFamilyCanonicalHashes": refs,
            "completeCharacterRecords": {ch: receipt["outputs"]["kanjidic2-records.xml"]["canonicalRecordHashes"][ch]
                                         for ch in pair},
            "positiveSourceBasis": positive, "comparisonLabelOnTarget": other_on_new,
            "targetLabelOnComparison": new_on_other, "qualification": qualification,
            "directExclusionOnNewEndpoint": guarded, "openQuizHold": False,
        })
    assert len(rows) == 28 and len({tuple(r["pair"]) for r in rows}) == 28
    write(OUT / "pair-dispositions-001.json", {
        "parent": PARENT, "publishedBase": BASE, "rows": rows,
        "policy": "Actual complete cards and independently positive complete families; both displayed directions and secondary ranges. Direct symmetric exclusions, never transitive. A precaution is not a proven ordinary synonym.",
        "counts": {kind: sum(r["decision"] == kind for r in rows)
                   for kind in ("guard", "precaution", "bounded-noncollision")},
        "openQuizHolds": [],
        "remainingLexicalUncertainty": "Historical image glyphs, old lookup allocation and per-spelling allocation of the broad rare 拍つ family are NOT resolved. Precautions protect the specified broad choices without making those uncertain senses ordinary modern teaching.",
        "limits": "Finite 28-pair author reconciliation; not fresh independent review, whole-index safety, arbitrary/custom/multiple-borrow/native/device/visual or publication acceptance.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    captures = load("external-capture-bindings.json")
    source_analysis = {
        "音": {"sectionsRead": "Complete Digital Daijisen entries, local text lines 28-412.",
              "heading": "おん【音】［漢字項目］", "source": "小学館 デジタル大辞泉",
              "shortExcerpt": "５ たより。", "allocation": "Explicit character sense under オン and イン, not inferred from 音耗. おと also retains a literary tidings use. No added metadata reading."},
        "信": {"sectionsRead": "Complete Digital Daijisen and 精選版 日本国語大辞典 entries, local text lines 26-283.",
              "heading": "しん【信】［漢字項目］ / しん【信】", "source": "小学館 デジタル大辞泉 / 精選版 日本国語大辞典",
              "shortExcerpt": "遠くまで届く合図や便り。", "allocation": "Independent character sense and separate positive news noun; the received-message counter is not treated as sufficient by itself."},
        "城": {"sectionsRead": "Complete Digital Daijisen and 精選版 日本国語大辞典 entries lines 26-300; complete separately attributed 字通 entry lines 713-863. Only incidental encyclopedia portions were read, not the entire mixed page.",
              "heading": "じょう【城】［漢字項目］ / 城 [古辞書の訓]", "source": "小学館 デジタル大辞泉 / 平凡社 普及版 字通",
              "shortExcerpt": "カキ", "allocation": "Daijisen defines fortified place/town; 字通 positively retains historical lookup. Precaution, not a claim that ordinary castle equals fence or that image-only forms are identified."},
    }
    for item in captures["captures"]:
        ch = item["character"]
        raw = Path(item["localRawCapture"])
        assert sha(raw.read_bytes()) == item["rawSha256"]
        assert sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
        source_analysis[ch].update({
            "url": item["url"], "finalUrl": item["finalUrl"], "capturedAt": item["capturedAt"],
            "rawSha256": item["rawSha256"], "textSha256": item["textSha256"],
            "identityVerified": True,
        })
    originals = {}
    for name in ("external-capture-bindings.json", "supplemental-external-bindings.json"):
        binding = json.loads((INITIAL / name).read_text(encoding="utf-8"))
        originals[name] = sha((INITIAL / name).read_bytes())
        for item in binding["captures"]:
            raw = Path(item["localRawCapture"])
            assert sha(raw.read_bytes()) == item["rawSha256"]
            assert sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
    write(OUT / "authored-source-analysis-001.json", {
        "externalEntries": source_analysis,
        "priorCaptureBindingsUnchanged": originals,
        "priorPositiveEvidence": {
            "耗": "Original complete Daijisen has すりへる/へる/使ってへらす; Kanjipedia 0006729100 explicitly gives news/tidings; 字通 retains qualified plant decline/impoverished land and old strings. Image glyphs and full allocation remain unresolved.",
            "拍": "Original complete Daijisen independently has hand-striking and musical rhythm; 字通 independently has はやしたてる/keeping time. The rare 拍つ family is retained whole, not assigned wholesale to bare 拍.",
            "塀": "Original complete boundary-wall/fence evidence and kokuji/phonosemantic discrepancy remain. ベイ voiced-compound clarification preserves pinned metadata.",
        },
        "completeFamiliesRead": {
            "jmdict": 99, "kanjidic2": 31, "actualComparisonCards": 28,
            "localFullRecordReadbacks": "reconciliation-001/complete-families-01.jsonl through -10.jsonl and character-inventories.jsonl; complete parsed/reserialized XML, not projections.",
            "attribution": "Author inspection statement, not an independently audited reviewer read receipt.",
        },
        "zeroQueries": [q for q, count in receipt["selectors"]["queryCountsIncludingZero"].items() if not count],
        "zeroMeaning": "Zero exact-spelling matches in the pinned JMdict, not absence of character meanings or related lexical families.",
        "scope": "Full new selected records preserve all spellings, restrictions, sense and reading flags, including rare 磨れる/摩れる, rare 退く ひく, kana-preferred rhythm under 乗り, and restricted 筆 composition/counter senses.",
    })
    print(json.dumps({"pairs": len(rows), "decisions": {r["decision"]: sum(
        p["decision"] == r["decision"] for p in rows) for r in rows},
        "openQuizHolds": [], "lexicalAllocationUncertaintyRetained": True}, ensure_ascii=False))
finally:
    write(HERE / "reconciliation-001" / "decisions-memory-001.json", guard.finish())
