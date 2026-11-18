"""Independent neutral byte/source/capacity verification; not teaching adjudication."""
import copy
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
PREP = ROOT / "neutral-preparation-001"
HERE = PREP / "projected-successor-001"
PACKET = HERE / "packet"
sys.path.insert(0, str(WS / "review-tools"))
sys.path.insert(0, str(HERE / "protocol-001"))
from common import CHECKS, SNAP, frozen, require, sha, start_guard, freeze_json
from verify_b134_sources import Git, FINGERPRINT, OWNER
from b129_confirmation_presentation import canonical
from b128_external_sources import extract
from source_query_union import selects
from b134_common import verify_packet, validate_report_destination
from b134_runtime import verify_chain

BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
PREFIX = "docs/n1-sources/batch-134/"
RUNNER = {"path": str(ROOT / "guarded-test-v3.py"),
          "sha256": "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"}
PROOFS = {
    "source-proof-002.json": "f3a80ee569a1bfd4f452e3f413a6377f5d01cac665e978dfc3e6db722c809393",
    "payload-proof-001.json": "ec47228ee313a82d872e7235f6f4a6b048737f24254d26405418c840dbd65d1a",
    "gate-verification-002/verification.json": "1caed56d80a213605d59eac6cc7ecc69829083cbdaa606b684edd77fb9162694",
    "packet-verification-001/verification.json": "fb95e655419fe9ecc0465ac565fb309397fb8843c22362b08cf5a1feda4d478a"}


def load(path, digest=None):
    return json.loads(frozen(path, digest))


def projection(full):
    result = copy.deepcopy(ET.fromstring(full))
    for character in result:
        for node in list(character):
            if node.tag in ("codepoint", "dic_number", "query_code"):
                character.remove(node)
        for group in character.findall("reading_meaning/rmgroup"):
            for node in list(group):
                if node.tag == "meaning" and node.get("m_lang", "en") != "en":
                    group.remove(node)
                elif node.tag == "reading" and node.get("r_type") in ("pinyin", "korean_r", "korean_h", "vietnam"):
                    group.remove(node)
    return canonical(ET.tostring(result, encoding="utf-8"))


def projection_controls(full, projected):
    expected = projection(full)
    require(expected == canonical(projected), "Projection loses/changes unauthorized fields")
    root = ET.fromstring(projected)
    controls = []
    for field in ("literal", "radical", "misc", "reading_meaning"):
        changed = copy.deepcopy(root)
        changed[0].remove(changed[0].find(field))
        require(canonical(ET.tostring(changed)) != expected, "Unauthorized removal accepted")
        controls.append("remove " + field)
    for path in ("literal", "radical/rad_value", "misc/stroke_count", "reading_meaning/rmgroup/reading",
                 "reading_meaning/rmgroup/meaning"):
        changed = copy.deepcopy(root)
        node = next(changed.iterfind("character/" + path), None)
        require(node is not None, "Projection control field unavailable: " + path)
        node.text = (node.text or "") + "-unauthorized"
        require(canonical(ET.tostring(changed)) != expected, "Unauthorized text change accepted")
        controls.append("alter " + path)
    for mutation in ("order", "count", "extra-field", "literal-attribute", "reading-attribute",
                     "misc-attribute", "add-codepoint"):
        changed = copy.deepcopy(root)
        if mutation == "order":
            changed[0], changed[1] = changed[1], changed[0]
        elif mutation == "count":
            changed.remove(changed[-1])
        elif mutation == "extra-field":
            ET.SubElement(changed[0], "unexpected").text = "x"
        elif mutation == "add-codepoint":
            ET.SubElement(changed[0], "codepoint").text = "not dropped"
        else:
            path = {"literal-attribute": "literal", "reading-attribute": "reading_meaning/rmgroup/reading",
                    "misc-attribute": "misc"}[mutation]
            changed[0].find(path).set("unexpected", "x")
        require(canonical(ET.tostring(changed)) != expected, "Unauthorized projection mutation accepted")
        controls.append(mutation)
    require(len(controls) == 16, "Projection control inventory differs")
    return controls


def main():
    guard, _ = start_guard("B134 independent complete neutral verification")
    git = Git(WS / "b134-worktree", RUNNER, guard)

    def blob(name, rev=CANDIDATE):
        guard.check()
        return git("show", rev + ":" + name)

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Clean signed snapshot changed")
    try:
        clean()
        proofs = {n: load(ROOT / n, d) for n, d in PROOFS.items()}
        require(all(p["candidate"] == CANDIDATE and p["base"] == BASE and p["status"] == "PASS"
                    and not p["memory"]["breach"] for p in proofs.values()), "Actual proof differs")
        source, payload, gates, finite = (proofs[n] for n in PROOFS)
        require(finite["proofs"] == {n: d for n, d in PROOFS.items()
                                    if not n.startswith("packet-verification")}, "Actual proof graph differs")
        sums = verify_packet(guard)
        full_root = PREP / "complete-record-trial-003"
        full_sums = load(full_root / "packet" / "SHA256SUMS.json")
        for n, d in full_sums.items():
            frozen(full_root / "packet" / n, d)

        def packet(name):
            return frozen(PACKET / name, sums[name])
        facts = load(source["facts"]["path"], source["facts"]["sha256"])
        contract = load(full_root / "source-contract" / "contract.json")
        require(len(contract["selections"]) == 4, "Four original selections required")
        records = {r["path"]: r for r in source["sourceRecords"]}
        counts = {}
        for kind, tag, identity, name, count in (
            ("jmdict", "entry", "ent_seq", "jmdict-families.xml", 399),
            ("kanjidic2", "character", "literal", "kanjidic2-records.xml", 59)):
            merged = {}
            for selection in facts[kind + "Selections"]:
                path = PREFIX + selection["file"]
                proof = records[path]
                raw = blob(path)
                binding = contract["files"][selection["file"]]
                require(raw == frozen(binding["path"], binding["sha256"]) and sha(raw) == proof["sha256"],
                        "Complete original selection bytes differ")
                ids = []
                for node in ET.fromstring(raw):
                    key = node.findtext(identity)
                    require(node.tag == tag and key and key not in ids, "Unexpected/duplicate record")
                    require(selects(node, tag, key, selection["mode"], selection["queries"]), "Query mismatch")
                    ids.append(key)
                    value = canonical(ET.tostring(node, encoding="utf-8"))
                    if key in merged:
                        require(merged[key] == value, "Conflicting full-record duplicate")
                    merged[key] = value
                require(sorted(ids) == sorted(proof["identities"])
                        and len(ids) == proof["completeMatchingRecords"]
                        and selection["queries"] == proof["queries"] and selection["mode"] == proof["mode"],
                        "Original query membership/provenance mismatch")
            compact = ET.fromstring(packet("evidence/" + name))
            actual = {n.findtext(identity): canonical(ET.tostring(n, encoding="utf-8")) for n in compact}
            require(len(compact) == len(actual) == count and actual == merged, "Complete union loses records/fields")
            counts[kind] = len(actual)
        queries = {q for s in facts["jmdictSelections"] for q in s["queries"]}
        jm = ET.fromstring(packet("evidence/jmdict-families.xml"))
        index = json.loads(packet("evidence/dictionary-index.json"))
        require(len(queries) == 182 and set(index) == queries
                and index == {q: sorted((n.findtext("ent_seq") for n in jm
                    if selects(n, "entry", n.findtext("ent_seq"), "union", [q])), key=int) for q in queries},
                "Full predicates/zero matches differ")
        provenance = json.loads(packet("evidence/source-selection-provenance.json"))
        require(provenance["selections"] == contract["selections"] and provenance["queryCount"] == 182
                and provenance["zeroMatchQueries"] == [q for q, ids in index.items() if not ids],
                "In-core full source/query provenance differs")
        full_kd = packet("evidence/kanjidic2-records.xml")
        projected = packet("evidence/kanjidic2-review-projection.xml")
        controls = projection_controls(full_kd, projected)
        original_nodes, projected_nodes = ET.fromstring(full_kd), ET.fromstring(projected)
        require([n.findtext("literal") for n in original_nodes] == [n.findtext("literal") for n in projected_nodes],
                "Projection changes identity/order")
        for node, raw in zip(original_nodes, full_kd.splitlines(keepends=True)[1:-1]):
            name = "evidence/kanjidic2-full-records/" + node.findtext("literal") + ".xml"
            require(packet(name) == raw and canonical(raw) == canonical(ET.tostring(node)),
                    "Optional original record not byte-exact")
        manifest_raw = blob("manifest.json")
        manifest = json.loads(manifest_raw)
        require(sha(manifest_raw) == payload["manifestSha256"], "Manifest differs")
        names = sorted((n for n in manifest["files"] if n.startswith("kanji/")), key=lambda n: ord(Path(n).stem))
        require(len(names) == 1262, "Candidate article count mismatch")
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        titles = []
        for start in range(0, len(names), 100):
            batch = names[start:start + 100]
            for name, (_, raw) in zip(batch, git.objects([CANDIDATE + ":" + n for n in batch])):
                require(raw == packet("repo/" + name), "Actual candidate extension article differs")
                metadata, _ = parse(raw.decode().replace("\r\n", "\n"))
                titles.append(Path(name).stem + " " + metadata["title"])
            guard.check()
        require(packet("evidence/title-index.txt") == ("\n".join(titles) + "\n").encode(), "Title index differs")
        baseline = git("ls-tree", "-r", "--name-only", BASE, "--", "kanji").decode().splitlines()
        require(len(baseline) == 1261 and set(names) - set(baseline) == {"kanji/紫.md"}, "Baseline inventory differs")
        for start in range(0, len(baseline), 100):
            batch = baseline[start:start + 100]
            for name, (_, raw) in zip(batch, git.objects([BASE + ":" + n for n in batch])):
                require(raw == packet("repo/" + name), "Unchanged complete baseline article differs")
        baseline_bytes = ("\n".join(t for t in titles if t.split(" ", 1)[0] != "紫") + "\n").encode()
        require(baseline_bytes == packet("evidence/baseline-title-index.txt"), "Full baseline title bytes differ")
        delta = json.loads(packet("evidence/baseline-title-delta.json"))
        deleted = [x.encode() for x in delta["removedCompleteLinesUtf8"]]
        rebuilt = b"".join(x for x in packet("evidence/title-index.txt").splitlines(keepends=True) if x not in deleted)
        require(rebuilt == baseline_bytes and len(deleted) == 1 and sha(rebuilt) == delta["reconstructedBaselineSha256"],
                "Baseline delta is not exact")
        reference = json.loads(packet("eligibility-reference.json"))
        m = payload["members"][0]
        require(reference["newCards"] == ["紫"] and len(reference["cards"]) == 1
                and reference["cards"][0]["distractors"] == m["metadata"]["distractors"]
                and reference["cards"][0]["quiz_exclusions"] == m["metadata"]["quiz_exclusions"],
                "Candidate frontmatter changed")
        for name in ("kanji/紫.md", "strokes/紫.json"):
            require(packet("snapshot/" + name) == blob(name), "Target bytes differ")
        for row in payload["supportLinks"]:
            require(packet("baseline/" + row["path"]) == blob(row["path"], BASE)
                    and packet("snapshot/" + row["path"]) == blob(row["path"]), "Full support snapshot differs")
        scope = ["kanji/紫.md", "strokes/紫.json", "words/紫.md"]
        require(packet("diffs/existing.diff") == git("diff", "--no-color", BASE, CANDIDATE, "--", "words/紫.md")
                and packet("diffs/runtime-content.diff") == git("diff", "--no-color", BASE, CANDIDATE, "--", *scope),
                "Exact scoped diff differs")
        for name in ("docs/content-format.md", "docs/jlpt-levels.md", "manifest.json"):
            require(packet("repo/" + name) == blob(name), "Complete guidance/manifest differs")
        for name in (".github/copilot-instructions.md", ".github/instructions/content-structure.instructions.md"):
            require(packet("rubric/" + Path(name).name) == blob(name), "Current rubric differs")
        for name in CHECKS:
            for ext in ("json", "log"):
                binding = gates["capturedInputs"][f"committed/{name}.{ext}"]
                require(packet(f"checks/{name}.{ext}") == frozen(binding["path"], binding["sha256"]),
                        "Committed gate bytes differ")
        for name, dest in (("source-rows.json", "source-metadata.json"), ("stroke-font-evidence.json", "font-cmap.json"),
                           ("reading-keys.json", "reading-keys.json")):
            require(packet("evidence/" + dest) == blob(PREFIX + name), "Signed source/font/reading metadata differs")
        runtime = json.loads(packet("checks/full-runtime-summary.json"))
        baseline_manifest = json.loads(blob("manifest.json", BASE))
        expected_groups = {k: {"baseline": len(baseline_manifest[k]), "candidate": len(v),
                              "unchanged": sum(key in v and v[key] == value for key, value in baseline_manifest[k].items())}
                           for k, v in manifest.items() if isinstance(v, dict)}
        require(runtime["groups"] == expected_groups and len(expected_groups) == 9
                and sum(r["baseline"] for r in expected_groups.values()) == 8745
                and sum(r["candidate"] for r in expected_groups.values()) == 8747, "Nine-group runtime summary differs")
        captures = json.loads(blob(PREFIX + "external-capture-bindings.json"))["captures"]
        snapshots = json.loads(packet(SNAP + "/manifest.json"))["snapshots"]
        require(len(captures) == len(snapshots) == 2, "Capture count differs")
        for i, item in enumerate(captures, 1):
            raw = packet(f"{SNAP}/{i:02d}-response.html")
            text, problem = extract(raw, item["finalUrl"], [item["character"]])
            require(problem is None and packet(f"{SNAP}/{i:02d}-extract.txt") == text.encode()
                    and sha(raw) == item["rawSha256"], "Complete named-section/body extract differs")
            require(all(snapshots[i - 1][k] == item[k] for k in ("character", "provider", "url", "finalUrl", "capturedAt")),
                    "Reused capture provenance differs")
        build = load(HERE / "packet-build.json")
        core = load(HERE / "core-chain-001.json")
        names = build["coreSources"]
        coverage = verify_chain(core, [(n, packet(n), None) for n in names])
        require(all(row["selectedLines"] == row["sourceLines"] for row in core["sources"]),
                "Partial source in core")
        forbidden = ("authored-source-analysis", "pair-dispositions", "comparison-cards", "/scans/", "review-claude", "review-gpt")
        require(not any(any(x in n for x in forbidden) for n in sums), "Non-neutral reviewer packet input")
        preflight = load(HERE / "audit-configs-001" / "preflight.json")
        a = frozen(preflight["runs"]["claude"]["prompt"]["path"]).decode()
        b = frozen(preflight["runs"]["gpt"]["prompt"]["path"]).decode()
        require(a.replace("CLAUDE", "GPT").replace("-claude-", "-gpt-") == b, "Paired prompt differs beyond identity")
        disclosure = frozen(HERE / "DISCLOSURE-001.txt").decode()
        require(disclosure in a and disclosure in packet("REVIEW.md").decode(), "Unequal representation disclosure")
        require(core["segments"][0]["path"] in a and "At most 25" in a and "E. At most 10" in a,
                "Prompt chain/cap mismatch")
        for family, spec in preflight["runs"].items():
            validate_report_destination(spec)
            cfg = load(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"])
            for row in cfg["files"]:
                frozen(row["path"], row["sha256"])
            require(not (HERE / (spec["run"] + "-launch.json")).exists(), "Actual reviewer artifact present")
        clean()
        result = {"status": "PASS_NEUTRAL_BYTES_AND_SOURCE_COMPLETENESS_NOT_TEACHING_REVIEW", "batch": 134,
            "candidate": CANDIDATE, "base": BASE, "packetFiles": len(sums), "fullTrialFiles": len(full_sums),
            "counts": counts, "originalSelections": 4, "jmdictQueries": 182,
            "zeroMatchQueries": [q for q, ids in index.items() if not ids], "candidateArticles": 1262,
            "unchangedBaselineArticles": 1261, "runtimeGroups": expected_groups, "captureCount": 2,
            "coreCoverage": coverage, "proofs": PROOFS, "projectionNegativeControls": controls,
            "fullOriginalKDRecordsOptional": 59, "pairedPromptsIdentityOnly": True,
            "limits": "Byte/source/protocol preparation only. No semantic adjudication, rendered fallback, device, publication or actual reviewer admission."}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Independent verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(HERE / "complete-verification-001.json", result)))


if __name__ == "__main__":
    main()
