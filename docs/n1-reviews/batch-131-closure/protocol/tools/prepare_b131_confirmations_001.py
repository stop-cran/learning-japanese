"""Build bounded source-complete record selections for original B131 reviewers."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from b129_confirmation_presentation import canonical, compact_xml, lexical_articles, named_section
from b131_confirmation_routing_001 import INITIALS, capacity_check, check_context
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from confirm_b131_003 import build
from verify_b131_revision_sources_001 import PACKET, PREFIX, REPO, ROOT
from verify_b131_sources import Git
from verify_b131_payload import RUNNER

PROOF_SHA = "368ead3a7bf597bab4c70ae8f7d968883b9e0d666f1b447b7e7e9d0f99d069ff"
OUTPUT = ROOT / "confirmation-001-neutral"
FAMILIES = re.compile(r"\b(?:claude|anthropic|opus|sonnet|haiku|gpt|openai|codex)\b", re.I)


def compact_records(raw, tag, key, identities):
    root = ET.fromstring(raw)
    original = {node.findtext(key): canonical(ET.tostring(node, encoding="utf-8"))
                for node in root}
    require(len(original) == len(root) and identities <= original.keys(), "Ambiguous record selection")
    for node in list(root):
        require(node.tag == tag, "Unexpected XML child")
        if node.findtext(key) not in identities:
            root.remove(node)
    result = compact_xml(ET.tostring(root, encoding="utf-8"))
    restored = {node.findtext(key): canonical(ET.tostring(node, encoding="utf-8"))
                for node in ET.fromstring(result)}
    require(restored == {identity: original[identity] for identity in identities},
            "Selected complete records changed")
    return result, sorted(original.keys() - identities)


def main():
    require(not OUTPUT.exists(), "Preserve existing confirmation preparation")
    proof_path = ROOT / "revision-evidence-001" / "verification.json"
    proof = json.loads(frozen(proof_path, PROOF_SHA))
    require(proof["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY"
            and proof["pairCount"] == 17 and not proof["reviewAccepted"]
            and not proof["publicationAccepted"], "Unverified signed revision")
    guard, _ = start_guard("B131 isolated bounded confirmation preparation")
    git = Git(REPO, RUNNER, guard)
    candidate = proof["candidate"]
    shared = []

    def blob(path):
        raw = git("show", candidate + ":" + path)
        require(raw == (REPO / path).read_bytes(), "Signed checkout changed")
        return raw

    def supplied(name, source, raw):
        require(not FAMILIES.search(raw.decode("utf-8")), "Shared source contains review attribution")
        path = OUTPUT / name
        item = write_frozen(path, raw)
        binding = {"path": str(path), "sha256": item["sha256"], "source": source}
        shared.append(binding)
        return binding

    try:
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate is not clean")
        table_raw = blob(PREFIX + "pair-dispositions-001.json")
        table = json.loads(table_raw)
        membership = json.loads(blob(PREFIX + "query-membership.json"))
        exact_ids = {identity for identity, queries in membership.items()
                     if any(query.startswith("exact-spelling:") for query in queries)}
        q2 = next(row for row in table["rows"] if row["id"] == "Q2")
        selected_ids = exact_ids | {str(identity) for identity in q2["sources"]["completeJmdictEntryIds"]}
        jm_raw = blob(PREFIX + "jmdict-families.xml")
        jm, omitted_jm = compact_records(jm_raw, "entry", "ent_seq", selected_ids)
        supplied("jmdict-complete-records.xml", "evidence/reconciliation/jmdict-complete-records.xml", jm)
        kd_raw = blob(PREFIX + "kanjidic2-records.xml")
        kd_ids = set("\u885b\u971c\u51b4\u63f4")
        kd, omitted_kd = compact_records(kd_raw, "character", "literal", kd_ids)
        supplied("kanjidic2-complete-records.xml", "evidence/reconciliation/kanjidic2-complete-records.xml", kd)
        manifest_raw = frozen(PACKET / "evidence" / "external-snapshots" / "manifest.json")
        manifest = json.loads(manifest_raw)
        external_bindings = []
        for index, character in ((1, "\u885b"), (5, "\u971c")):
            capture = next(item for item in manifest["snapshots"] if item["index"] == index)
            raw = frozen(PACKET / capture["response"]["path"], capture["response"]["sha256"])
            sections, omitted = lexical_articles(raw, capture["citedUrl"], character)
            require(len(sections) == 3, "Expected three whole lexical dictionary articles")
            for number, section in enumerate(sections, 1):
                name = f"external-{index:02d}-{number:02d}.txt"
                item = supplied(name, "external-reconciliation/" + name, section["text"].encode("utf-8"))
                external_bindings.append({
                    "output": item["source"], "sha256": item["sha256"],
                    "originalCaptureSha256": capture["response"]["sha256"],
                    "url": capture["citedUrl"], "capturedAt": capture["capturedAt"],
                    **{key: value for key, value in section.items() if key != "text"},
                    "otherArticleLocatorsNotReread": omitted,
                })
        capture = next(item for item in manifest["snapshots"] if item["index"] == 6)
        raw = frozen(PACKET / capture["extract"]["path"], capture["extract"]["sha256"])
        text, lines = named_section(raw, "\u96a0\u8a9e\u5927\u8f9e\u5178")
        item = supplied("external-06-jargon.txt", "external-reconciliation/external-06-jargon.txt", text)
        external_bindings.append({"output": item["source"], "sha256": item["sha256"],
                                  "originalExtractSha256": capture["extract"]["sha256"],
                                  "originalLines": lines, "url": capture["citedUrl"],
                                  "capturedAt": capture["capturedAt"]})
        presentation = {
            "candidate": candidate, "parent": proof["parent"],
            "selection": "Bounded changed-passage confirmation, not a fresh full-card review.",
            "jmdict": {
                "signedSource": PREFIX + "jmdict-families.xml", "signedSha256": sha(jm_raw),
                "selectedCompleteEntryIds": sorted(selected_ids), "notRereadEntryIds": omitted_jm,
                "rule": "Every exact-spelling match in the independently reproduced reconciliation "
                        "queries, plus every complete family cited for the one unguarded comparison. "
                        "No sense, variant, language, reading or restriction is removed within a selected family. "
                        "Remaining records are incidental references in unchanged counterpart articles; "
                        "they are not reread or claimed reviewed here.",
            },
            "kanjidic2": {
                "signedSource": PREFIX + "kanjidic2-records.xml", "signedSha256": sha(kd_raw),
                "selectedCompleteRecords": sorted(kd_ids), "notRereadRecords": omitted_kd,
                "rule": "Complete records for the two changed targets, the unguarded cold/freezing "
                        "comparison and the explicit save/protect aid claim. All fields/languages/nanori "
                        "retained. Other counterpart metadata and all readings are unchanged and verified "
                        "mechanically, not independently re-audited here.",
            },
            "externalArticles": external_bindings,
            "externalScope": "Whole Daijisen, Seisen Nihon Kokugo Daijiten and Jitsu articles for each "
                             "changed target, plus the whole named jargon section. Encyclopedias, site "
                             "navigation, other Weblio sections, source images/layout and other unchanged "
                             "source captures are not reread. No selected passage replaces a source article.",
            "authorClaims": "The original report, own author response, exact revised cards and diff "
                            "are supplied. The paired author table/mapping is supplied only where explicitly "
                            "listed. Any author claim unsupported by supplied sources remains unverified. "
                            "A guarded precaution is not an assertion of synonymy or a proof about all pools.",
        }
        supplied("presentation.json", "verification/presentation.json",
                 (json.dumps(presentation, ensure_ascii=False, separators=(",", ":")) + "\n").encode())
        runtime = json.loads(frozen(proof["proofs"]["runtime"]["path"], proof["proofs"]["runtime"]["sha256"]))
        summary = {
            "candidate": candidate, "parent": proof["parent"], "base": proof["base"],
            "status": "SIGNED_MECHANICAL_CHECKS_ONLY", "proofSha256": PROOF_SHA,
            "runtimeEntries": runtime["runtimeEntries"], "changedRuntimeCards": runtime["runtimeChanged"],
            "manifestSha256": runtime["manifestSha256"], "contentVersion": runtime["contentVersion"],
            "unchanged": "All other 8735 runtime entries including the third batch member, supports, "
                         "strokes, ordered readings, practice keys and curated distractors.",
            "sourceVerification": "All 78 complete query-output families and 19 character records were "
                                  "independently reproduced from the pinned full dictionary streams; "
                                  "the presentation record lists the narrower actual reread selection.",
            "hostChecks": "All ten author and ten committed gates independently bound to exact commands, "
                          "serial execution, successful receipts, signed producers and manifest bytes.",
            "warningCount": proof["warningCount"], "semanticAcceptance": False,
            "limits": "Six latent smaller-pool reading collisions retained. No arbitrary/custom/"
                      "multiple-borrow, Kotlin/native/device, font rendering, old APK or publication acceptance.",
        }
        supplied("verification.json", "verification/verification.json",
                 (json.dumps(summary, ensure_ascii=False, separators=(",", ":")) + "\n").encode())
        for name in ORDERED_LOGS:
            item = proof["capturedExecutionFiles"]["committed-gates-001/" + name + ".log"]
            raw = frozen(item["path"], item["sha256"])
            supplied("checks-" + name + ".log", "committed-checks/" + name + ".log", raw)
        revised = [f"kanji/{char}.md" for char in sorted(
            set(runtime["cardMetadata"]) | {row["pair"][1] for row in table["rows"]})]
        for path in revised:
            require(not FAMILIES.search(blob(path).decode("utf-8")), "Shared card contains attribution")
        prepared = []
        for family, initial in INITIALS.items():
            run = "N1-B131-" + family.upper() + "-CONFIRM-001"
            acceptance = ROOT / initial["directory"] / (initial["run"] + "-acceptance.json")
            own_response = PREFIX + f"responses/{family}-response-001.md"
            extra = list(shared)
            own = [own_response]
            if family == "gpt":
                own.extend([PREFIX + "pair-dispositions-001.json",
                            PREFIX + "responses/gpt-mapping-001.json",
                            "docs/n1-source-snapshot.json"])
                snapshot = json.loads(blob("docs/n1-source-snapshot.json"))
                membership_name = "n1-kanji-source-20261102.json"
                raw = (WS / "control" / "inputs" / membership_name).read_bytes()
                require(sha(raw) == snapshot["inputs"][membership_name]["sha256"]
                        and len(raw) == snapshot["inputs"][membership_name]["bytes"]
                        and set("\u885b\u7f8a\u971c") <= set(json.loads(raw)),
                        "Frozen community membership binding differs")
                path = OUTPUT / membership_name
                saved = write_frozen(path, raw)
                extra.append({"path": str(path), "sha256": saved["sha256"],
                              "source": "evidence/community/" + membership_name})
            spec = {
                "batch": 131, "run": run, "family": family, "candidate": candidate,
                "session": initial["session"],
                "acceptance": {"path": str(acceptance), "sha256": initial["acceptanceSha256"]},
                "revisedSources": [*revised, *own], "originalSources": [], "additionalSources": extra,
            }
            if family == "gpt":
                spec.update(basis="adjudicated-initial", priorVerdict="UNVERIFIED")
            path = ROOT / "confirm-003" / (run + "-spec.json")
            freeze_json(path, spec)
            build(path)
            chain = json.loads(frozen(ROOT / "confirm-003" / (run + "-chain.json")))
            context = check_context(Path.home() / ".copilot" / "session-state" /
                                    initial["session"] / "events.jsonl", family)
            forecast = capacity_check(context, chain)
            prepared.append({"run": run, "session": initial["session"], "capacity": forecast,
                             "segments": len(chain["segments"]), "sourceCount": len(chain["sources"])})
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Candidate changed")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Confirmation preparation breached RAM guard")
    print(json.dumps(freeze_json(ROOT / "confirmation-001-preparation.json", {
        "status": "PREPARED_NOT_ADMITTED", "candidate": candidate, "runs": prepared,
        "proofSha256": PROOF_SHA, "sharedSources": shared, "memory": memory,
        "reviewersLaunched": False, "publicationAccepted": False,
        "producerSha256": sha(frozen(Path(__file__))),
        "limits": "Actual record/source reread scope is explicitly bounded in presentation.json. "
                  "No author/reviewer conclusion is accepted. Fresh full-roster admission is required.",
    })))


ORDERED_LOGS = ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate",
                "manifest", "unittest", "budget", "vocabulary", "manifest-rebuild")


if __name__ == "__main__":
    main()
