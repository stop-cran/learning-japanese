import copy
import json
import re
import xml.etree.ElementTree as ET
from b131_common import BASE, HERE, PACKET, REPO, git, normalized, sha, start_guard, write
from survey_b131 import records
from survey_b131_002 import xml_output

def flatten(node):
    head = node.tag + "".join(f"@{k}={v}" for k, v in node.attrib.items())
    if not len(node):
        return head + "=" + (node.text or "").strip()
    return head + "{" + "; ".join(flatten(n) for n in node) + "}"

ADDITIONAL = {
    "衛": "revolve revolving circuit encircle encircling enclosure enclose enclosures patrol patrols patroling keep keeping sustain support assistance aid help save rescue nurse nursing oversee watchful security precaution protect precautionary",
    "羊": "blessing blessings fortune luck favorable virtuous virtue goodness beauty beautiful sign indication auspice happiness felicitous fortunate felicitous play walk walking leisure roam wandering bank notes note",
    "霜": "perishing dying die death dead destroy destruction damage abolish extinct extinction demise decay wither fade vanish disappear disappearance loss waste decrease consume consumption knife blade sword edge pointed keen strict severity rigorous rigor hardship hardships difficult difficulty suffering suffering bitter bitterness evil drug ash ashes grey gray silver whiteness",
}

guard = start_guard()
try:
    kd = {n.findtext("literal"): copy.deepcopy(n) for n in records("kanjidic2", guard)}
    manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    prior = {p.stem for p in (PACKET / "comparison-cards").glob("*.md")}
    comparisons = set(prior)
    for ch in "衛羊霜":
        old = json.loads((PACKET / "scans" / (ch + ".json")).read_text(encoding="utf8"))
        keys = set(old["expandedKeywords"]) | set(ADDITIONAL[ch].split())
        rows = copy.deepcopy(old["rows"])
        for row in rows:
            row["matchedKeywords"] = sorted(keys & set(re.findall("[a-z]+", " ".join([row["title"], *row["completeMeanings"]]).lower())))
            if row["matchedKeywords"]:
                comparisons.add(row["kanji"])
        scan = {**old, "expandedKeywords": sorted(keys), "rows": rows, "matches": [r["kanji"] for r in rows if r["matchedKeywords"]],
                "reason": "Supplement positive monolingual/native senses; broaden semantic stems missed by initial literal-token scan. Retain every original scan row."}
        write(PACKET / "scans-002" / (ch + ".json"), scan)
    added = comparisons - prior
    for ch in sorted(added):
        write(PACKET / "comparison-cards" / (ch + ".md"), git("show", f"{BASE}:kanji/{ch}.md"))
    selected, membership = [], {}
    for node in records("jmdict", guard):
        keb = {n.text for n in node.findall("k_ele/keb")}
        predicates = [f"exact-spelling:{c}" for c in sorted(keb & added)]
        if predicates:
            selected.append(copy.deepcopy(node))
            membership[node.findtext("ent_seq")] = predicates
    write(PACKET / "supplemental-query-membership.json", membership)
    outputs = {
        "jmdict-supplemental-families.xml": xml_output(PACKET / "jmdict-supplemental-families.xml", "JMdict", selected),
        "kanjidic2-supplemental-comparisons.xml": xml_output(PACKET / "kanjidic2-supplemental-comparisons.xml", "kanjidic2", [kd[c] for c in sorted(added)]),
    }
    write(PACKET / "supplemental-source-receipt.json", {"base": BASE, "sourceReceiptSha256": sha((PACKET / "source-receipt.json").read_bytes()),
        "allExactSpellings": sorted(added), "predicate": "Complete families having an exact spelling equal to a newly matched baseline comparison; no sense or priority filtering.",
        "transformation": "Complete parsed/reserialized XML, canonical original-field equality; not raw source slices.", "outputs": outputs,
        "producerSha256": sha(__import__("pathlib").Path(__file__).read_bytes())})
    rows = []
    for ch in sorted(added):
        means = [n.text for n in kd[ch].findall("reading_meaning/rmgroup/meaning") if n.get("m_lang") in (None, "en")]
        exact = [flatten(n) for n in selected if f"exact-spelling:{ch}" in membership[n.findtext("ent_seq")]]
        rows.append("CARD " + ch + "\n" + normalized(PACKET / "comparison-cards" / (ch + ".md")) +
                    "\nCOMPLETE KD ENGLISH: " + "; ".join(means) + "\nCOMPLETE EXACT-SPELLING FAMILIES:\n" + "\n".join(exact))
    for i in range(0, len(rows), 8):
        write(HERE / f"supplement-cards-{i // 8 + 1:02}.txt", ("\n\n".join(rows[i:i + 8]) + "\n").encode())
    print(json.dumps({"added": sorted(added), "comparisonCount": len(comparisons),
        "newMatches": {c: [r["kanji"] for r in json.loads((PACKET / "scans-002" / (c + ".json")).read_text(encoding="utf8"))["rows"] if r["matchedKeywords"] and r["kanji"] in added] for c in "衛羊霜"}}, ensure_ascii=False))
finally:
    write(HERE / "supplement-memory-001.json", guard.finish())
