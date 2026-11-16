import json
import sys
from pathlib import Path
from b131_common import HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write
from candidate_b131 import BASE, CHARS

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

REASONS = {c: {} for c in CHARS}


def group(ch, others, decision, reason):
    for other in others:
        assert other not in REASONS[ch], (ch, other)
        REASONS[ch][other] = (decision, reason)


group("衛", "保守防看監警兵卒", "guard",
      "Positive defense/protection and guard-person ranges directly warrant protection/watch-over/guard/soldier precautions. Watching is not necessarily preventing harm; neither every soldier nor every graduation is a guard.")
group("衛", "囲包括周回転輪舞", "guard",
      "Daijisen's circling/surrounding and Jitsu's めぐる/かこむ inventory directly warrant enclosure/circuit/revolving/circling precautions. Not all wrapping, tying, wheels or dancing is guarding or orbiting.")
group("衛", "丞凌助勢援支柱武紹貯蔵置", "distinct",
      "Assistance, enduring/surpassing, force/momentum, structural support, martial arts, introduction/inheritance, saving/storing/possessing and placement have complete positive secondary ranges but neither displayed label denotes a guard or defense. Helping, a guard's equipment, saving resources and protecting someone are not automatically identical activities; no transitive guard inheritance.")
group("衛", "丸円", "distinct",
      "Roundness/circle/yen/pellet/castle-enclosure/currency ranges retained. A circle or round object is not the act of circling; the guard/defense title does not denote a circle or yen. The enclosure noun in the complete 丸 family is a location, not the patrol around it.")
group("衛", "区国域州帯界畔辺領境塀", "distinct",
      "The named ancient state 衛 and qualified 衛服 territorial category are preserved. They do not establish the generic country/state/region/zone/world/boundary/paddy-ridge/vicinity/territory/wall labels as meanings of ordinary 衛. A guarded boundary is an object/location relation, not lexical identity; administrative ward is not the protective English ward-off.")
group("衛", "更鏡", "distinct",
      "更's night-watch is a time division, not a guarding person; renew/grow-late does not define 衛. 鏡's mirror/lens/model/barrel-head/mochi and document-cover senses do not denote defense or circling. Reflection and a complete circular object's shape are not a patrol.")

group("羊", "紙札金貨財毛髪房未", "guard",
      "Nikkoku explicitly retains paper/paper-products/banknotes and hairdresser/shop wordplay; Weblio slang separately retains head hair. Guard paper/banknote/money/property/currency and hair/tuft labels conservatively, not every asset or material product. 未 independently has Sheep/Ram/Goat zodiac senses: sheep as a displayed answer can be correct there despite the not-yet title.")
group("羊", "良好令幸福兆運徳恩", "guard",
      "Jitsu explicitly supplies good/auspicious/auspicious sign through standing for 祥. Broad good/favorable/good-fortune/omen and goodness/blessing labels receive direct precautions. These are not claims that an ordinary sheep is virtue, kindness, command or every fortune.")
group("羊", "丑丙亥午卯子寅巳申辰酉", "distinct",
      "Complete calendar/animal/hour/direction/lunar-month and native secondary families retained. These branches/stems are not the Sheep branch; a generic sign-keyword hit cannot equate all zodiac identities. Child/offspring and child suffix/particle-related uses do not denote an adult sheep animal in general.")
group("羊", "伝凶占厄指易注票符署解象通", "distinct",
      "Conveying/legend, ill fortune, divination, misfortune, pointing/digits, ease, pouring/annotation, ballot/token/signature, solving, elephant/image and passage/commuting are distinct from sheep, paper/head-hair slang and the positive auspicious use. Bad omens are not favorable omens. A ballot or signature may use paper, and a symbol may be an omen, but those object/material or indication relations do not transfer their displayed identities.")
group("羊", "劇歩悠演行遊", "distinct",
      "The obsolete Noh title 羊 is a proper work, not the generic drama/performance/play meaning. 相羊 wandering is a qualified complete expression, not evidence that bare 羊 means every step, leisure interval, act, journey, walk or play activity. All complete secondary senses remain retained.")
group("羊", "息結美補", "distinct",
      "Breath/son/interest/rest, tying/joining/concluding and assistant/supplement are not sheep or paper/hair slang. 美 has a visible 羊-shaped radical and beauty/august senses, not a bare sheep sense; favorable auspiciousness is not a general beauty label. Tying up hair is an action upon hair, not its name.")

group("霜", "白毛髪冷寒凜鋭激切刻険", "guard",
      "Positive white/grey-hair, white/cold/sharp/intense/severe branches directly warrant these broad-label precautions. 切 retains sharp/keen/acute, 刻 additionally strictness, 険 harsh/sharp looks or tongue; neither every cut, carving nor perilous slope is frost. Cold material and freezing process differ.")
group("霜", "年時代期歳齢歴宙", "guard",
      "Nikkoku/Jitsu explicitly retain years/time/elapsed years, also visible in 星霜. Direct precautions cover broad time/period/age/passage labels and 宙's qualified classical time branch, not a claim that every clock moment or outer space is frost.")
group("霜", "粉末薬剤", "guard",
      "Nikkoku's charred and powdered medicinal material is a positive standalone native secondary sense. Powder and medicinal-preparation labels require direct precautions despite different main titles. These are not claims that frost is ordinary flour or a universally safe drug.")
group("霜", "失損亡死破討耗荒", "guard",
      "Jitsu positively retains perishing and loss. Broad loss/damage/perish/destroy/lay-waste precautions are direct while historical allocation remains qualified. This does not equate every defeat, attack, sorrow or use of resources with frost.")
group("霜", "久元先再分初度悠昔暮秒際辺才", "distinct",
      "Long/former/previous/repeated/initial time, parts/minutes/seconds, occurrence counts, leisure/remoteness, ancient days, dusk/livelihood, occasion/edge/vicinity and talent remain distinct in both displayed-label directions. Years passing is not every ordering or duration word; a shared complete secondary age/time sense does not make the current talent or location labels definitions of frost.")
group("霜", "仏傾冒凶医卒参召喫困悪暗枯減痛眠苦費辛返酸難魔", "distinct",
      "Buddha/dead-person, tilt, braving danger, ill fortune, healing profession, graduation, participation, respectful summoning/eating, consumption, difficulty, badness, darkness, plant withering, decrease, pain, sleeping, suffering/bitterness, expense, spicy/painful, repayment, acid and demons are not established by either displayed-label direction. Harm is not every cause or consequence of harm; frost damage does not make these ordinary meanings of bare 霜. Positive perish/death and hardship secondary senses are retained, not transferred transitively into unrelated current labels.")
group("霜", "冴凍氷灰炭房投椋移結老葉銀雪黒", "distinct",
      "Complete clarity/skill/cold, freezing/ice, ash/charcoal/charred remains, hair-tuft, throwing, grey-starling/tree, shifting, tying, growing old, leaf/grass-blade, silver/money, snow and black/guilt ranges retained. Coldness is not the displayed clear-minded/frozen/ice identities; burning a preparation does not make it generic ash/charcoal or black. Grey hair is not a starling, all silver things, a tuft shape, tying hair or every act of aging; a grass blade is not sharpness. Snow is precipitation, not surface frost.")
group("霜", "刀刃剣", "distinct",
      "Complete sword/blade/edge and secondary weapon/tool/money/stinger/rice ranges inspected. 秋霜/霜剣 sword metaphors are complete-word senses, not evidence for ordinary bare 霜 as the name of every sword. Sharpness as a property does not itself name the blade; target frost likewise does not define those weapons.")
for ch in CHARS:
    group(ch, "古右石", "curated",
          "Full old/antiquity/used-item, right/above-mentioned/political-right/better-of-two, and stone/jewel/flint/game-piece/calculus/volume/counter ranges inspected. None of these displayed labels denotes guarding/defense, sheep or frost. Years passing and grey hair do not make frost the adjective old; a protective object being old or made of stone is not lexical identity.")

guard = start_guard()
try:
    members = []
    for ch in CHARS:
        fm, _ = n1lib.parse(normalized(REPO / "kanji" / (ch + ".md")))
        scanpath = PACKET / "scans-002" / (ch + ".json")
        scan = json.loads(scanpath.read_text(encoding="utf8"))
        required = set(scan["matches"]) | set(fm["distractors"]) | set(fm["quiz_exclusions"])
        assert required <= REASONS[ch].keys(), (ch, sorted(required - REASONS[ch].keys()))
        assert set(fm["quiz_exclusions"]) == {k for k, (d, _) in REASONS[ch].items() if d == "guard"}
        pairs = []
        for other, (decision, reason) in REASONS[ch].items():
            path = PACKET / "comparison-cards" / (other + ".md")
            raw = path.read_bytes()
            assert raw == git("show", f"{BASE}:kanji/{other}.md")
            ofm, _ = n1lib.parse(raw.replace(b"\r\n", b"\n").decode())
            pairs.append({"pair": [ch, other], "comparisonTitle": ofm["title"], "decision": decision,
                          "comparisonLabelOnTarget": f"Actual comparison label {ofm['title']!r} considered against complete qualified {ch} range. {reason}",
                          "targetLabelOnComparison": f"Actual target label {fm['title']!r} considered against complete qualified {other} range. {reason}",
                          "baselineCardSha256": sha(raw), "scanMatch": other in scan["matches"]})
        members.append({"kanji": ch, "targetTitle": fm["title"], "scanRows": len(scan["rows"]),
                        "originalScanBase": scan["base"], "candidateBase": BASE,
                        "scanFile": f"scans-002/{ch}.json", "scanSha256": sha(scanpath.read_bytes()), "pairs": pairs})
    for a, b in [("衛", "羊"), ("衛", "霜"), ("羊", "霜")]:
        members.append({"newMemberPair": [a, b], "decision": "distinct",
                        "bothDirections": "Guarding/defense/circling, sheep with qualified paper/head-hair/auspicious senses, and frost with qualified grey-hair/time/powder/perishing senses do not validate one another's displayed guard/defense, sheep and frost labels. Shared secondary hair is retained without treating all differing main labels as synonymous."})
    write(PACKET / "pair-dispositions.json", {
        "base": BASE, "members": members,
        "rule": "Finite scan hits plus curated/excluded comparisons. Direct OR symmetry only; no transitive closure. Precautions are not universal synonymy.",
        "readCoverage": "All 178 actual comparison Meaning/Notes projections, complete exact-spelling family fields/senses/restrictions and complete KD English meanings read. Full actual supports/curated cards read. Projections are not claims to have manually read every whole comparison card or raw XML bytes.",
        "readbackBindings": {p.name: sha(p.read_bytes()) for p in sorted(HERE.glob("semantic-*.jsonl"))},
        "originalEvidenceRebinding": "base-adaptation.json verifies all baseline kanji blobs unchanged from original scan base.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    print(json.dumps({"pairRows": sum(len(m.get("pairs", [])) for m in members)}, ensure_ascii=False))
finally:
    write(HERE / "editorial-memory-001.json", guard.finish())
