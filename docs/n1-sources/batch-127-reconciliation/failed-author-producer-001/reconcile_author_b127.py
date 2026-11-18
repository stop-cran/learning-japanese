import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from b127_common import HERE, PACKET, REPO, git, sha, start_guard, write
from reconcile_sources_b127 import CLAIMS, OUT, PARENT

ORIGINAL = ["庫", "蔵", "府", "室", "収", "貯", "急", "突", "亡", "置", "入"]
ADDED = ["囲", "保", "預", "容", "留", "持", "忙", "速", "死", "延", "止", "停"]
DETAILS = {
    "Q1": {
        "kind": "conservative-direct-guard",
        "strongest": "Not merely fencing: 囲い sense 2 is storage of fruit/vegetables; 囲う sense 4 stores/preserves, and KANJIDIC2 independently includes store/preserve/keep.",
        "forward": "倉 displayed / surround; enclose offered: storing goods in an enclosure can reach broad enclosing language. Complete sources do not sharply delimit that broad option against the attested storing branch.",
        "reverse": "囲 displayed / granary; storehouse offered: storage and an enclosure are positively attested, but this is not proof that every 囲 names a granary building. The storage-place boundary remains a limited ambiguity, not an asserted universal synonym.",
        "cites": ["JMdict 1155950 senses 1-2", "JMdict 1155960 senses 1-5", "JMdict 1155980 all senses", "KANJIDIC2 囲", "Jitsu 倉 kun-gloss 2"],
    },
    "Q2": {
        "kind": "conservative-direct-guard",
        "strongest": "保つ preserves/keeps/retains and also keeps food well. 保管 means safekeeping/storage; 保存 means preservation/storage, with a separate computing sense. The independent character record includes keep/preserve.",
        "forward": "倉 displayed / protect; preserve offered: safe storage protects goods, positively described in Nihon Kokugo Daijiten くら sense 1, and Jitsu gives storing. The broad preserve option is not cleared by restricting 保 to abstract states.",
        "reverse": "保 displayed / granary; storehouse offered: preserving goods is not itself a building. The compound storage gloss is context, not a constituent storehouse proof; the forward broad-choice ambiguity alone motivates this guard.",
        "cites": ["JMdict 1513250 senses 1-2", "JMdict 1513320 sense 1", "JMdict 1513530 senses 1-2", "JMdict 1513940 senses 1-2", "KANJIDIC2 保", "Nihon Kokugo Daijiten くら sense 1", "Jitsu 倉 kun-gloss 2"],
    },
    "Q3": {
        "kind": "conservative-direct-guard",
        "strongest": "預ける explicitly means deposit/place in custody; 預かる keeps/holds in custody, and 預かり includes safekeeping plus separately deferred/undecided matters. Custody is not an exclusively abstract or banking-only restriction.",
        "forward": "倉 displayed / deposit; entrust offered: the broad deposit label can describe putting goods away in safe storage. The sources establish custody and storing without resolving every ordinary English boundary between them.",
        "reverse": "預 displayed / granary; storehouse offered: custody is the relation/action, not automatically a warehouse. A storage-service association is not a general building sense; guard the unresolved forward breadth, not an invented identity.",
        "cites": ["JMdict 1544950 senses 1-5", "JMdict 1544970 senses 1-4", "JMdict 1544980 sense 1", "JMdict 1544990 senses 1-3", "JMdict 1545020 sense 1", "KANJIDIC2 預", "Jitsu 倉 kun-gloss 2"],
    },
    "Q4": {
        "kind": "conservative-direct-guard",
        "strongest": "容 independently means contain; the complete 入れる/容れる family puts/takes things in, admits and includes, with especially-容れる acceptance noted locally. 容器 is a receptacle; 収容 also includes housing/detention. No restriction is discarded.",
        "forward": "倉 displayed / contain; appearance offered: appearance does not fit storage, but the contain half can describe keeping goods inside. Putting in/containing is broader than storage; a conservative guard prevents that unresolved broad choice.",
        "reverse": "容 displayed / granary; storehouse offered: a receptacle or capacity to contain is not necessarily a storehouse. The compound container/housing senses are not promoted to a universal constituent building meaning.",
        "cites": ["JMdict 1465610 all nine senses, especially sense 3 usage note", "JMdict 1545370 sense 1", "JMdict 1330880 senses 1-3", "KANJIDIC2 容", "Jitsu 倉 kun-glosses 1-3"],
    },
    "Q5": {
        "kind": "conservative-direct-guard",
        "strongest": "留める/とどめる sense 4 keeps in place/retains; sense 1 stops/halts. The とめる family includes detention/custody and 留め置く includes lock up/retain. Jitsu's 倉 prison gloss adds an actual custody branch beyond physical fastening.",
        "forward": "倉 displayed / retain; stay offered: retention can reach storing/keeping goods, while custody reaches the qualified prison branch. Staying or fastening alone does not exhaust 留; retain is conservatively guarded.",
        "reverse": "留 displayed / granary; storehouse offered: retaining or detaining does not by itself name a storehouse. This guard prevents the forward broad-label ambiguity, not an assertion that all detention places are warehouses.",
        "cites": ["JMdict 1598820 senses 1-5", "JMdict 1310670 senses 1-7", "JMdict 1552710 sense 1", "JMdict 2657130 all senses", "KANJIDIC2 留", "Jitsu 倉 kun-glosses 2-3"],
    },
    "Q6": {
        "kind": "distinct-with-positive-source-support",
        "strongest": "存する sense 3 explicitly retains/preserves/keeps, and 保存 sense 1 includes storage. These are retained, not dismissed as merely a compound or a nonexistent secondary sense.",
        "forward": "倉 displayed / exist; be aware offered: 存する senses 1-2 establish being/remaining and depending/residing, while 存ずる independently establishes knowing/awareness and belief. Neither operation labels putting goods away, the storage building, haste, the qualified cancellation, or the historical quotation; storing an existing thing does not mean exist or be aware.",
        "reverse": "存 displayed / granary; storehouse offered: even the explicit transitive preserve/retain branch of 存する and storage in 保存 describe keeping something in existence or storage, not a named grain/goods depository. The positive noun くら definition identifies that building. This is an operation/referent distinction, not just a noun/verb rule or a denial of physical preservation.",
        "cites": ["JMdict 2081030 senses 1-3", "JMdict 1983710 senses 1-2, humble-language restriction retained", "JMdict 1406150 sense 1", "JMdict 1406190 sense 1", "JMdict 1513940 senses 1-2", "KANJIDIC2 存", "original JMdict 1592380 all senses", "Nihon Kokugo Daijiten くら senses 1-7"],
    },
    "Q7": {
        "kind": "conservative-direct-guard",
        "strongest": "持つ has maintaining/keeping (sense 3), lasting/surviving (4), and taking charge (5), not only carrying/ownership. 保持 positively gives retention/preservation; 持ち also has durability and responsibility senses.",
        "forward": "倉 displayed / hold, have offered: broad holding/keeping can describe keeping goods in storage. Complete sources establish an actual keeping branch but do not sharply resolve that English option; guard conservatively.",
        "reverse": "持 displayed / granary; storehouse offered: carrying, possession, maintenance and responsibility do not establish a cargo compartment. English ship's hold and 船倉 are not evidence that 持 means that noun; the guard addresses forward broad-choice uncertainty.",
        "cites": ["JMdict 1315720 senses 1-7", "JMdict 1315730 senses 1-5", "JMdict 1612060 senses 1-4", "JMdict 1513700 sense 1", "KANJIDIC2 持", "Jitsu 倉 kun-gloss 2"],
    },
    "Q8": {
        "kind": "source-supported-direct-guard",
        "strongest": "Both complete 忙しい families independently have a hurried/restless sense, and 忙しない gives in a hurry. This is stronger than borrowing busy from the formal/literary 倉卒 compound.",
        "forward": "倉 displayed / busy offered: the common busy/hectic label and its independently attested hurried branch can compete with 倉's independently attested flustered/hurried branch. Guard the direct pair; being occupied and every kind of hurry are not declared identical.",
        "reverse": "忙 displayed / granary; storehouse offered: its busy/restless/hurried senses do not identify a goods depository. The forward ambiguity is sufficient; no reverse building identity is claimed.",
        "cites": ["JMdict 1519290 senses 1-2", "JMdict 2835296 senses 1-2", "JMdict 2008630 sense 1, usually-kana restriction retained", "JMdict 1408040 sense 1", "JMdict 1278830 senses 1-2", "JMdict 1399200 sense 1, formal/literary", "KANJIDIC2 忙", "Kanjipedia 倉 meaning 2", "Jitsu 倉 kun-gloss 4"],
    },
    "Q9": {
        "kind": "conservative-direct-guard",
        "strongest": "速い includes quick/rapid/brisk/prompt, not only vehicle speed; 速やか is quick/prompt; 速める quickens/accelerates with spelling-local usage notes. 倉's independent あわてる branch includes hurried action, not merely an English compound gloss.",
        "forward": "倉 displayed / fast offered: the quick/prompt option can reach hurried action. Sudden onset, fluster and speed are not identical, but these complete sources do not sharply delimit every ordinary broad fast choice; retain a direct conservative guard.",
        "reverse": "速 displayed / granary; storehouse offered: speed/quick occurrence does not name a storage place. Neither 急 nor 突 exclusions protect this distinct pair transitively.",
        "cites": ["JMdict 1404975 senses 1-5 with spelling restrictions", "JMdict 1405000 sense 1", "JMdict 1601080 senses 1-2 with usage notes", "JMdict 1228650 sense 1", "JMdict 1228890 sense 1", "JMdict 1278830 senses 1-2", "JMdict 1399160 sense 1", "KANJIDIC2 速", "Kanjipedia 倉 meaning 2"],
    },
    "Q10": {
        "kind": "conservative-direct-guard",
        "strongest": "Jitsu quotes ホロブ in an old dictionary without establishing modern semantic currency. The complete independent ほろぶ/ほろびる families positively include perish/die out; 死/死ぬ supply death/dying, with secondary cease/stop also retained.",
        "forward": "倉 displayed / death offered: the old ホロブ quotation plus independently documented perishing vocabulary leaves a historical breadth question, not proof that ordinary 倉 means death. Guard conservatively rather than declare the quotation current or fully harmless.",
        "reverse": "死 displayed / granary; storehouse offered: death, loss of vigor, cessation, baseball out and historical execution do not name a grain/goods depository. The remaining historical forward uncertainty alone motivates the guard.",
        "cites": ["JMdict 2013360 sense 1", "JMdict 1603610 sense 1", "JMdict 1310720 senses 1-3 with historical/field restrictions", "JMdict 1310730 senses 1-3", "KANJIDIC2 死", "Jitsu 倉 old-dictionary quotation"],
    },
    "Q11": {
        "kind": "conservative-direct-guard",
        "strongest": "Standalone くら has independently attested calling-off of a performance/planned matter. お蔵入り/お倉入り has postponed/on-hold as an idiomatic whole-word sense, distinct from its literal storage sense. 延 families positively postpone/delay, with all spelling restrictions retained.",
        "forward": "倉 displayed / prolong; postpone offered: prolonging is not cancellation; postponement can compete with shelving a plan. The complete standalone sources do not resolve every shelving/postponement boundary, so guard conservatively, without transferring the compound gloss wholesale to 倉.",
        "reverse": "延 displayed / granary; storehouse offered: extending/delaying or aggregate totals do not identify a storage building. Its positive postponement meanings support only the limited forward concern.",
        "cites": ["JMdict 1176390 senses 1-2 with stagk", "JMdict 1176430 sense 1", "JMdict 1358870 senses 1-10 with stagk", "JMdict 1600290 senses 1-9 with usage notes", "JMdict 2789120 senses 1-2 with idiom/literal distinction", "JMdict 2835880 senses 1-2", "KANJIDIC2 延", "Digital Daijisen くら sense 2", "Nihon Kokugo Daijiten くら sense 4"],
    },
    "Q12": {
        "kind": "source-supported-direct-guard",
        "strongest": "Standalone くら cancellation is independently attested, not inferred from お倉入り. 止める/やめる sense 2 and 中止 sense 2 explicitly cancel/call off planned activity.",
        "forward": "倉 displayed / stop, halt offered: stopping/calling off a planned performance is defensible for that qualified secondary sense; guard the direct pair.",
        "reverse": "止 displayed / granary; storehouse offered: stopping/ceasing does not name a storehouse. No claim that every stopping verb, rain cessation or dead end belongs to 倉.",
        "cites": ["JMdict 1310680 senses 1-2 with spelling/kana restrictions", "JMdict 1424410 senses 1-2", "JMdict 1654720 sense 1", "KANJIDIC2 止", "Digital Daijisen くら sense 2", "Nihon Kokugo Daijiten くら sense 4"],
    },
    "Q13": {
        "kind": "source-supported-direct-guard",
        "strongest": "停 has independent stopping/halt character senses and 停止 includes ceasing activity/suspension. 倉's standalone cancellation reaches that activity-stoppage label, without importing all compound stoppage senses.",
        "forward": "倉 displayed / halt; stopping offered: defensible for the qualified performance/planned-matter cancellation branch; guard the direct pair.",
        "reverse": "停 displayed / granary; storehouse offered: stopping or suspension does not name a storage building. Power outages and stopping places are not asserted as 倉 meanings.",
        "cites": ["JMdict 1434920 senses 1-4 including the archaic reading-specific mourning sense", "JMdict 1310620 senses 1-3", "JMdict 1310670 senses 1-7", "JMdict 1598820 senses 1-5", "JMdict 2657130 all senses", "KANJIDIC2 停", "Digital Daijisen くら sense 2", "Nihon Kokugo Daijiten くら sense 4"],
    },
}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        receipt = json.loads((OUT / "source-receipt.json").read_text(encoding="utf-8"))
        raw = (REPO / "kanji" / "倉.md").read_bytes()
        card = raw.decode("utf-8")
        exclusions = re.search(r"^quiz_exclusions: \[([^\]]*)\]$", card, re.M).group(1).split(", ")
        assert exclusions == ORIGINAL + ADDED
        assert (REPO / "words" / "倉庫.md").read_bytes() == git("show", f"{PARENT}:words/倉庫.md")
        rows = []
        for qid, (ch, _) in CLAIMS.items():
            path = OUT / "comparison-cards" / (ch + ".md")
            text = path.read_text(encoding="utf-8")
            assert path.read_bytes() == git("show", f"{PARENT}:kanji/{ch}.md")
            prior_other = re.search(r"^quiz_exclusions: \[([^\]]*)\]$", text, re.M)
            other_exclusions = prior_other.group(1).split(", ") if prior_other else []
            assert "倉" not in other_exclusions
            detail = DETAILS[qid]
            rows.append({
                "id": qid, "pair": ["倉", ch], "otherTitle": re.search(r"^title: (.+)$", text, re.M).group(1),
                "disposition": detail["kind"],
                "strongestPlausibleOverlap": detail["strongest"],
                "directions": {"倉DisplayedOtherTitleOffered": detail["forward"], "otherDisplayed倉TitleOffered": detail["reverse"]},
                "citations": detail["cites"],
                "recordBindings": {"character": {"file": "kanjidic2-comparison-records.xml", "literal": ch}, "completeWordFamilies": {"file": "jmdict-comparison-records.xml", "entryIds": receipt["selectors"][qid]["entryIds"]}, "comparisonCard": {"file": "comparison-cards/" + ch + ".md", "sha256": sha(path.read_bytes())}},
                "declaredEndpointStatus": {"parent": {"倉": False, ch: False}, "revision": {"倉": ch in exclusions, ch: False}, "effectiveSymmetricGuard": ch in exclusions},
                "remainingUncertainty": "No blanket linguistic equivalence asserted; unresolved broad-choice/historical boundary is prevented by this direct guard." if detail["kind"] == "conservative-direct-guard" else "Bounded to these displayed labels and complete cited records; not universal semantic clearance.",
            })
        write(OUT / "pair-dispositions.json", {
            "schemaVersion": 1, "batch": "127", "revision": "reconciliation-001", "parent": PARENT,
            "displayed倉Title": "granary; storehouse", "claims": rows,
            "originalGuardsRetainedInOrder": ORIGINAL, "addedGuardsInOrder": ADDED,
            "distinctNoGuard": ["存"], "unguardedOpenClaimIds": [],
            "conservativeGuardClaimIds": [r["id"] for r in rows if r["disposition"] == "conservative-direct-guard"],
            "exclusionSemantics": "A declaration on 倉 excludes that exact pair symmetrically; no transitive inference, current-pool or curated-exposure exemption.",
            "sourceCitationKey": {"JMdict": "jmdict-comparison-records.xml entry/ent_seq and 1-based sense number; complete entries, all variants and restrictions retained.", "KANJIDIC2": "kanjidic2-comparison-records.xml character/literal, complete records.", "original JMdict": "../batch-127/jmdict-selected-records.xml", "external": "external-source-summary.json binds full local extracts/HTML and exact lines; no new fetch."},
            "scope": "Finite Q1-Q13 only. Source-supported new branches within these pairs do not silently expand the review list. Other screened but unread candidates remain disclosed limits.",
        })
        ext = receipt["reusedExternalSnapshots"]
        write(OUT / "external-source-summary.json", {
            "parent": PARENT, "noNewCapture": True, "localBindings": ext,
            "manifest": "See bound local external-snapshots/manifest.json for exact URLs, response/extract bytes, SHA-256 and UTC capture timestamps.",
            "citations": {
                "Kanjipedia 倉 meaning 2": "01-extract.txt:21-24",
                "Nihon Kokugo Daijiten くら senses 1-7": "02-extract.txt:20-29",
                "Nihon Kokugo Daijiten くら sense 1": "02-extract.txt:20-23",
                "Nihon Kokugo Daijiten くら sense 4": "02-extract.txt:26",
                "Jitsu 倉 kun-glosses": "02-extract.txt:45-49",
                "Jitsu 倉 old-dictionary quotation": "02-extract.txt:50-51",
                "Digital Daijisen くら sense 2": "03-extract.txt:12-16",
            },
            "originalSummaries": [
                "Digital Daijisen's standalone くら sense 2 calls off a scheduled kabuki or similar performance.",
                "Nihon Kokugo Daijiten's standalone くら sense 4 describes a theatrical performance not going ahead and extends to calling off planned matters. This is independent word evidence, not a sense inferred only from お倉入り.",
                "The separate character entry and Jitsu support storage, flustered/precipitate haste, source-specific storing/prison glosses and an explicitly labelled old-dictionary reading quotation. These sections are not merged into one unrestricted entry.",
            ],
            "shortAttributedQuotation": {"dictionary": "Digital Daijisen, くら sense 2, via Weblio", "url": "https://www.weblio.jp/content/倉", "text": "歌舞伎などで、予定していた興行をやめにすること。"},
            "limits": "Textual local captures only, no visual HTML/ancient-glyph inspection or new frequency certification. Complete external extracts remain local, not copied into contributor material.",
        })
        old_ledger_path = REPO / "docs" / "n1-sources" / "batch-127-progress.json"
        ledger = json.loads(old_ledger_path.read_text(encoding="utf-8"))
        ledger.update({
            "revision": 2, "parentCandidate": PARENT, "baseCommit": PARENT,
            "publishedBase": "dd45f6fb7cd3ce579422e2333860aa6d245af898",
            "status": "local-unconfirmed-reconciled-authoring-candidate",
            "historicalLedger": {"path": "batch-127-progress.json", "sha256": sha(old_ledger_path.read_bytes())},
            "sourceEvidence": "batch-127-reconciliation/source-receipt.json",
            "comparisonEvidence": ["batch-127-reconciliation/pair-dispositions.json"],
            "authorAudit": "batch-127-reconciliation/author-audit.md",
            "authorEvidence": "batch-127-reconciliation/author-evidence.json",
            "packetInventory": "batch-127-reconciliation/packet-files.json",
            "completeSourceVerification": "batch-127-reconciliation/source-receipt.json",
            "runtimeCandidate": "To be bound after serial author gates in the reconciliation author-evidence.json and scratch handoff.",
            "authorGates": "To be bound after execution; no advance PASS claim.",
            "familyResponses": ["batch-127-reconciliation/claude-author-response.md", "batch-127-reconciliation/gpt-author-response.md"],
        })
        write(REPO / "docs" / "n1-sources" / "batch-127-progress-002.json", ledger)
        history = {}
        parent_manifest = json.loads(git("show", f"{PARENT}:manifest.json"))
        paths = git("-c", "core.quotepath=false", "ls-tree", "-r", "--name-only", PARENT, "--", "docs/n1-sources/batch-127", "docs/n1-sources/batch-127-progress.json").decode("utf-8").splitlines()
        for name in paths:
            guard.check()
            path = REPO / name
            before = git("show", f"{PARENT}:{name}")
            assert path.read_bytes() == before, name
            history[name] = {"sha256": sha(before), "bytes": len(before)}
        write(OUT / "preserved-history.json", {
            "parent": PARENT, "files": history, "allVerifiedByteIdentical": True,
            "externalPriorAuthorReceipts": {name: {"path": str(HERE / name / "summary.json"), "sha256": sha((HERE / name / "summary.json").read_bytes())} for name in ["author-gates-001", "author-gates-002", "author-gates-003", "committed-gates-001", "preservation-author-001", "preservation-committed-001"]},
            "priorPacketReference": "All original producers, failed/superseded attempts, scans, receipts and decisions stay historical. This reconciliation adds records, not replacement decisions in the old packet.",
            "parentManifestSha256": sha(git("show", f"{PARENT}:manifest.json")),
            "parentRuntimeEntries": sum(len(v) for v in parent_manifest.values() if isinstance(v, dict)),
        })
        for name in ["reconcile_sources_b127.py", "reconcile_author_b127.py"]:
            write(OUT / "producers" / name, (HERE / name).read_bytes())
        print(json.dumps({"claims": len(rows), "addedGuards": ADDED, "unguardedOpen": [], "preservedHistoricalFiles": len(history)}, ensure_ascii=False))
    finally:
        write(HERE / "reconciliation-author-001-memory.json", guard.finish())


if __name__ == "__main__":
    main()
