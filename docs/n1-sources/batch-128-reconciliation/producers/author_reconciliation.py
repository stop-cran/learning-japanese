import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from recon_common import BASE, HERE, ORIGINAL, PACKET, PARENT, REPO, ROOT, SCRATCH, git, sha, start_guard, write

ROWS = [
    ("Q1", "刃", [1369820, 1369830, 1369890, 2842190], "conservative-direct-guard",
     "The qualified blade/cutting-edge label is narrower than a generic edge. JMdict 1369820 positively specifies the edge of a knife/sword and separately an electrical-plug prong; 1369830 additionally has forged-blade pattern, sharpness and a marked unhulled-rice sense. Those do not establish lip synonymy. Nevertheless KANJIDIC2 also gives unqualified edge and the historical 脣=ホトリ quotation lacks context fixing which edges it can denote. The modern waterside preference in 2842190 is not an exclusive historical restriction. Retain the cutting distinction, but guard the residual qualified-edge choice rather than assert it is reliably wrong under that unknown historical range.",
     "Lips is not the ordinary gloss of a sword, plug prong, sharpness or rice. The ordinary blade/knife-edge definitions are positive evidence of difference, not a denial of KANJIDIC2 edge. The guard prevents the unresolved broad edge-label ambiguity in the forward direction, not a claim that every sense of either endpoint is interchangeable.",
     "Historical quotation's precise reach remains unsettled; deliberately guarded, not lexically resolved."),
    ("Q2", "声", [1380440, 2843115, 1359950], "no-guard",
     "Voice is not the definition of a lip or of the labial-consonant category in 1359950/Nikkoku しん. Complete 1380440 includes generic sound and the linguistic voice/voiced-sound sense, not just animal/human voice. A voiced sound can also be labial: these classes may intersect, but voicing is not the lip-articulation criterion that defines a labial. The offered label voice does not offer unqualified sound. The separate 2843115 also retains Buddhist voice/sound, Chinese tone/mark and accent; none makes voice the name of a lip or of every labial.",
     "Lips does not name voice, an expressed opinion/wish, a bird/insect call, a sense of arrival, a voiced sound, Buddhist sound, tone or accent. A body part producing a sound is not that sound's ordinary answer. This explicitly considers the broad sound senses without reducing 声 to its first example or claiming voiced and labial sounds are disjoint.",
     "No claim that all sounds or phonetic classes are disjoint; this is the actual voice/lips label pair."),
    ("Q3", "差", [1291070, 1291330, 2423450, 2711180, 2842190], "no-guard",
     "Difference; gap offers discrepancy or separation, not the side/edge/bank named by modern ほとり or the lip/petal/startle/labial senses. A gap can lie between lips but is not either lip or its edge. KANJIDIC2 margin is retained without claiming it must be numeric; that undisplayed English word does not change the offered label into edge.",
     "Lips is not an ordinary answer for a difference, mathematical difference or margin, nor for the complete さし/さす families: face-to-face/between, impediment, Noh recitative, two-player games, emphasis/counter, ruler; shining, visibility, tinge, water rising, emotion arising, raising/inserting, wearing, sumo insertion, poling/pouring/applying colour, lighting, closing or stopping mid-action. Applying lipstick involves lips but does not mean lips. No numeric-only restriction is imposed on the unrestricted character gloss.",
     "The two offered directions do not require resolving every English sense of margin."),
    ("Q4", "房", [1519300, 2222290, 2842190], "no-guard",
     "Room; tassel; bunch names a compartment or a tuft/cluster, not a lip or generic border. The independent 1519300 positively groups fringe with a tuft of hair/threads and tassel, and separately gives fruit/flower clusters and citrus segments. This is not a peripheral-land fringe silently inferred from selected examples. A cluster of flowers is not a petal definition.",
     "Lips is not an ordinary name for a tuft/fringe/tassel, bunch, citrus section, chamber/prison cell/atrium, a monk's home/monk or the astronomical room constellation in 2222290. The character's broader fringe gloss remains recorded; a decorative edging or thin bag-like segment does not itself denote lips or the historical side word.",
     "The complete familial meanings support this pair, not a global ban on all fringe metaphors."),
    ("Q5", "案", [1154770, 1220210, 1586940, 1238680], "no-guard",
     "Proposal; draft plan does not express being startled, frightened or alarmed. The fear/worry KANJIDIC2 gloss is positively retained and independently supported by 案ずる 1586940 sense1, which restricts the anxious sense to 案ずる. The offered planning label does not display that fear sense; the old おどろく evidence does not make a proposal a definition of 唇.",
     "Lips is not an answer for fear/worry, devising/considering/investigating, proposal/draft/expectation or desk. 1586940 restricts stroking/rubbing/patting/grasping to 按ずる, not 案ずる; that spelling restriction is preserved rather than generalized. Fear and surprise can overlap; that does not make lips a label for either all anxiety or a plan.",
     "Fear is not dismissed as rare or absent; its two-direction relevance is explicitly evaluated."),
    ("Q6", "横", [1180570, 2842190], "no-guard",
     "Horizontal describes orientation, not a lip, petal, labial consonant, surprise or the unspecified side in the old ホトリ quotation. Complete 1180570 also records side-to-side/width, a box's side, beside/next to, and unconnected. They are retained, but the offered horizontal is not an unqualified side label. A mouth may be horizontal without horizontal naming lips.",
     "Lips is not an ordinary gloss of orientation, width, the side of a box, adjacency or unconnectedness, nor of KANJIDIC2 woof/unreasonable/perverse. No claim is made that every historical side meaning is water-only. This differs from the direct broad 側 label; no exclusion is propagated through 側.",
     "The historical quotation is not exhaustively reconstructed; the offered labels remain distinct."),
    ("Q7", "鋭", [1174890, 1174960, 1861190, 2842190], "no-guard",
     "Sharp; keen denotes sharpness, pointed/piercing qualities or perception, not an edge as a place. 1174890 retains the knife/claw, pain/tone, criticism/attack/question/gaze/sound and discerning-perception senses; surprise does not mean sharp or perceptive. Unlike the explicitly nominal cutting-edge choice in Q1, the offered adjectives do not display KANJIDIC2 edge or weapon.",
     "Lips is not the ordinary name for any of those qualities, a violent action, a sharp weapon/blade or a fine soldier in complete 1861190. KANJIDIC2 edge is not discarded or silently restricted to knives; even its broad boundary interpretation does not make the actual answer lips an ordinary synonym for 鋭. A sharp lip shape is an attributed property, not the word's meaning.",
     "Q1's cautious nominal-edge guard is not a transitive policy for adjective labels."),
    ("Q8", "響", [1009280, 1238610, 1602130, 1612890, 1359950], "no-guard",
     "Resound; echo specifies propagation/reverberation (and English echo can be the resulting reflected sound), not any labial consonant as such. A labial may echo, but being labial neither requires nor names an echo. The mouth-trembling account likewise does not assert resounding. The complete sources also retain physical shaking/vibration, effect/impression, generic distinctive sound/noise, and commotion; these are not silently reduced to echoes.",
     "Lips is not an ordinary answer for sound, resonance, vibration, influence, impression or commotion. Complete 1602130's bare 響 is flagged irregular okurigana; 1009280/1612890 contain どよめき/どよめく with their kana/spelling qualifications. Those full-word senses do not make a body part their meaning. The broad sound/vibrate senses are considered without denying that the events can involve lips.",
     "No inference from 響/音 or 響/震 exclusions; only the direct offered labels are decided."),
    ("Q9", "鳴", [1532870, 1532880, 1532910, 1359950], "no-guard",
     "Animal call; ring names calling or sounding/ringing, not a lip or the labial phonetic class. A labial sound is not defined by an animal call, bell-like ring or reflected echo. The English noun ring is an audible ring in the taught source; its unrelated circular-jewelry homograph does not name a lip or petal either. Generic sound/cry/echo character glosses remain recorded, not limited to animal calls.",
     "Lips does not name sounding, echoing, an animal call, the 鳴く-restricted mahjong meld call, causing a sound/snort/snap/crack, being popular/reputed, stating/complaining or the marked farting sense. The entire 1532880 family is retained, not only its first ringing sense. An articulator and any output from it are not interchangeable labels.",
     "No general claim about every possible sound label or transitive use of 鳴/音."),
    ("Q10", "危", [1218360, 1218380, 1218410, 1218560, 2177790, 1238680], "no-guard",
     "Danger names hazard/risk, not the emotional response of being startled/alarmed. A hazard can cause fright without being that response. This is not a claim that 危 lacks emotional senses: 1218410 positively gives fear/doubt/misgivings/anxiety/apprehension, and 1218360/1218380 include precariousness/uncertainty and a warning interjection.",
     "Lips is not an answer for hazard, fear/uneasiness, worry, uncertainty, a narrow escape, sketchiness, a warning or the rooftop constellation in 2177790. The complete frightened/alarmed 驚く sense is considered; neither it nor the whole warning 危ない makes lips a normal name for 危's meanings.",
     "Fear and alarm need not be disjoint; the offered danger/lips labels are the criterion."),
    ("Q11", "在", [1296400, 2260090, 2842190], "no-guard",
     "Exist; be located does not name a lip, petal, labial, surprise or a side/outer area. The fact that lips and shores exist is a proposition about them, not a translation. Complete 2260090 positively includes countryside/outskirts/suburbs as well as presence and a place-name prefix; those are not erased by the existence title.",
     "Lips is not an ordinary answer for existence, possession, location, a resulting state/event, countryside, suburbs, presence or residence. The hypothetical forward outskirts ambiguity is addressed directly for Q12, whose displayed label actually supplies it. That does not make lips an ordinary translation of 在's rural/place senses or propagate 郊's guard.",
     "A secondary place gloss can intersect old ホトリ without making this different offered-label pair ambiguous."),
    ("Q12", "郊", [1242290, 1282490, 2842190], "conservative-direct-guard",
     "Outskirts; suburbs is qualified urban outer-area wording, not every side or shoreline. Complete 1282490 defines a residential city outskirt/commuter belt; 1242290 additionally gives city environs/surrounding area. Modern 2842190 says side especially of a waterbody, plus edge/bank/shore; especially is not only. It also cannot fix the old 脣=ホトリ quotation's unexpressed range. The peripheral/surrounding-area answer therefore remains within the unresolved broad outer-area class: directly guard it rather than claim modern-water-only evidence settles it.",
     "Lips is not the ordinary answer for residential suburbs, rural area or city environs. This guard prevents the forward historical-variant broad-choice ambiguity and does not assert that a suburb is a lip or that historical ホトリ definitely meant every suburb. All actual 郊 senses remain distinct from the ordinary anatomy.",
     "Historical context remains unsettled and explicitly guarded; not a modern synonymy finding."),
    ("Q13", "騒", [1403000, 1403020, 1403040, 1403060, 1502640, 1596440, 1238680, 1359950], "no-guard",
     "Make noise; uproar is audible or agitated commotion, not a generic labial consonant. Complete 騒ぐ also has rustling, merrymaking, clamor/fuss, losing one's cool/panicking and tense/uneasy/excited feelings. Surprise may lead to those responses but is not the definition of uproar or making noise; neither every surprise nor every labial is noisy commotion. This uses the positive senses, not a bare noun/verb distinction.",
     "Lips does not name din, restlessness, panic, a turbulent era, dangerous/unsettled conditions, excitement/disturbance, literary verse or sorrow. Source-only うれい and the card's sorrow/indignation-related literary account are retained as such, not ordinary example readings or a lip meaning. Full 騒 words are not reduced to their first noise gloss, nor are whole 物騒 senses allocated arbitrarily to a constituent.",
     "No new ordinary 唇 reading or universal separation of alarm/agitation is asserted."),
    ("Q14", "叫", [1235910, 1386780, 1238680, 1359950], "no-guard",
     "Shout; exclaim means an audible outcry or explicit appeal. Complete 1235910 also gives advocacy/insistence/protest, and 1386780 scream/shriek/exclamation. Being startled may cause an exclamation but does not itself assert vocalization; the positive おどろく source has the surprised/frightened state, not an imperative to shout. A labial consonant is defined by lip articulation, not loudness or exclamatory function.",
     "Lips is not an ordinary answer for a scream, vocal exclamation or insistent advocacy. The sources include these communicative functions, not only a mechanical action-versus-consonant distinction. Surprise and shouting can co-occur without establishing either offered label as the other's meaning.",
     "Bounded source-backed distinction, not a claim that lip-produced sounds can never be shouted."),
    ("Q15", "咲", [1194500, 1297210, 2397140, 1359940], "conservative-direct-guard",
     "The actual blossom; bloom choice lacks a part-of-speech marker and can be read as a noun near the positively sourced petal sense. JMdict 1194500 places flower/blossom/bloom/petal in one noun sense. Guard that label ambiguity directly, not by propagation from 花. Complete 1297210 positively gives the intransitive flowering action and an archaic rising-waves sense; 2397140 gives courteous/forced laughter. None establishes that 咲く itself means a petal or lips.",
     "Lips is not the ordinary answer for a flower opening, a rising wave or courteous/forced laughter. The guard is for the noun-like forward choice, not universal synonymy or a rule excluding every flower-related card.",
     "F1 label-consistency repair. O1 optional historical classification remains unchanged."),
]


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        kd = {n.findtext("literal"): n for n in ET.parse(PACKET / "kanjidic2-complete-records.xml").findall("character")}
        available = {n.findtext("ent_seq") for n in ET.parse(PACKET / "jmdict-complete-records.xml").findall("entry")}
        card = (REPO / "kanji" / "唇.md").read_text(encoding="utf-8")
        guards = re.search(r"^quiz_exclusions: \[([^\]]*)\]", card, re.M).group(1).split(", ")
        table = []
        for claim, char, entries, decision, forward, reverse, limit in ROWS:
            assert {str(i) for i in entries} <= available
            text = (PACKET / "comparison-cards" / (char + ".md")).read_text(encoding="utf-8")
            endpoint = re.search(r"^quiz_exclusions: \[([^\]]*)\]", text, re.M)
            endpoint_exclusions = endpoint.group(1).split(", ") if endpoint else []
            assert "唇" not in endpoint_exclusions
            assert (char in guards) == (decision == "conservative-direct-guard")
            table.append({
                "id": claim, "pair": ["唇", char], "displayedLabels": ["lips", re.search(r"^title: (.+)$", text, re.M).group(1)],
                "decision": decision, "withNewPromptAndOtherLabel": forward, "withOtherPromptAndNewLabel": reverse,
                "completeCharacterEnglishMeanings": [m.text for m in kd[char].findall("reading_meaning/rmgroup/meaning") if "m_lang" not in m.attrib],
                "sources": [{"file": "jmdict-complete-records.xml", "ent_seq": str(i)} for i in entries] + [
                    {"file": "kanjidic2-complete-records.xml", "literal": char}, {"file": "source-notes.json", "sections": ["petal", "surprise", "historicalVariant", "labialNoun"]},
                    {"file": "comparison-cards/" + char + ".md", "coverage": "complete same-parent card, including all frontmatter and body"}],
                "declaredEndpointStatus": {"newEndpoint": char in guards, "comparisonEndpoint": False, "symmetric": True, "nonTransitive": True},
                "residualLimit": limit,
            })
        write(PACKET / "pair-dispositions.json", {
            "parentCommit": PARENT, "publishedBase": BASE, "newKanji": "唇",
            "criterion": "Both actually offered label directions, including ordinary/taught secondary meanings. An undisplayed broad gloss is not erased, but is not automatically substituted for the offered title.",
            "priorScanAndDecisions": "../batch-128/pair-dispositions.json", "priorDecisionsPreservedNotRewritten": True,
            "claims": table, "addedDirectGuards": ["咲", "刃", "郊"], "retainedDirectGuards": guards[:14],
            "totalDeclaredDirectGuards": len(guards), "openUnguardedClaims": [],
            "boundedCarryForward": {"片": "Sheet/leaf/one-of-two is not petal/lips. 花片 is a whole petal word, not unrestricted identity of its constituents; no new guard."},
            "limits": "Conservative guards retain unresolved historical scope, not asserted synonymy. No unrequested whole-corpus or custom/native acceptance.",
        })
        capture = ROOT / "review-packets" / "batch-128-fb3c98d8" / "evidence" / "external-snapshots" / "02-extract.txt"
        write(PACKET / "source-notes.json", {
            "source": "Kotobank's separate Digital Daijisen, Seisenban Nihon Kokugo Daijiten and Jitsu sections",
            "url": "https://kotobank.jp/word/唇-55487",
            "existingFullCaptures": "../batch-128/external-source-bindings.json",
            "existingBindingSha256": sha((ORIGINAL / "external-source-bindings.json").read_bytes()),
            "localExtract": {"path": str(capture), "sha256": sha(capture.read_bytes()), "publishedWholeExtract": False},
            "petal": {"citations": "Daijisen native word sense2; Nikkoku native word sense2; local extract lines16-17,27", "excerpts": ["２ 花びら。", "② 花びら。花弁。"], "qualification": "Classical poetic examples support the editorial literary description; no explicit register flag is supplied."},
            "surprise": {"citations": "Jitsu 字訓 and 訓義1, local extract lines55,60-62", "excerpt": "おどろく", "qualification": "Not every emotional response or a new ordinary word pronunciation."},
            "historicalVariant": {"citations": "Jitsu 古辞書の訓, local extract line64", "excerpt": "脣　ホトリ・クチビル", "qualification": "The quotation supplies no usage context fixing its reach. Modern JMdict 2842190 is relevant, not a complete reconstruction or a water-only restriction."},
            "labialNoun": {"citations": "Nikkoku separate noun しん, local extract lines28-29", "excerpt": "くちびる。また、唇音", "qualification": "Articulation class, not universal identity with every voiced/echoing/noisy sound."},
            "optionalO1": "No optional formation enrichment. Structure-unclassified, omitted phonetic metadata and explicitly non-etymological shape mnemonic remain unchanged.",
            "newExternalCaptures": 0,
        })
        print(json.dumps({"claims": len(table), "addedGuards": ["咲", "刃", "郊"], "totalGuards": len(guards)}, ensure_ascii=False))
    finally:
        write(SCRATCH / "reconciliation-author-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
