"""Verify frozen inputs first; preserve all compact-001 assets and add compact-002 derivations."""
import json
from pathlib import Path

from b131_review_v2_common import (
    BASE, CALIBRATION, CALIBRATION_SHA, CANDIDATE, CONTRACT_SHA, HERE, OLD_HERE,
    OLD_PACKET, OLD_PACKET_SHA, PACKET, freeze_json, frozen, json_bytes, require, sha,
    start_guard, verify_inputs, write_frozen)
from b131_review_v2_derivations import (kd_projection, jm_partition, title_delta, verify_kd, verify_jm,
                                       verify_delta, supplement_catalog)


def main():
    require(not HERE.exists() and not PACKET.exists(), "Preserve all existing compact preparation")
    guard, _ = start_guard("B131 compact-002 verified packet derivation")
    try:
        sums, calibration = verify_inputs(guard)
        full_kd = frozen(OLD_PACKET / "evidence/kanjidic2-records.xml", sums["evidence/kanjidic2-records.xml"])
        full_jm = frozen(OLD_PACKET / "evidence/jmdict-families.xml", sums["evidence/jmdict-families.xml"])
        reference = json.loads(frozen(OLD_PACKET / "eligibility-reference.json"))
        index = json.loads(frozen(OLD_PACKET / "evidence/dictionary-index.json"))
        kd, kd_audits = kd_projection(full_kd)
        jm, partition = jm_partition(full_jm, reference, index)
        delta, delta_audit = title_delta(frozen(OLD_PACKET / "evidence/baseline-title-index.txt"),
                                         frozen(OLD_PACKET / "evidence/title-index.txt"))
        require(len(kd_audits) == 182 and partition["total"] == 874, "Full source coverage differs")
        verify_kd(full_kd, kd)
        verify_jm(full_jm, jm, reference, index, partition)
        verify_delta(frozen(OLD_PACKET / "evidence/baseline-title-index.txt"),
                     frozen(OLD_PACKET / "evidence/title-index.txt"), delta)
        new = {
            "evidence/kanjidic2-review-projection.xml": kd,
            "evidence/jmdict-review-core.xml": jm,
            "evidence/title-index-delta.txt": delta}
        supplements, supplement_index = supplement_catalog(full_jm, partition)
        new.update({f"evidence/jmdict-extension-records/{identity}.xml": raw
                    for identity, raw in supplements.items()})
        new["evidence/jmdict-extension-index.json"] = json_bytes({
            "characters": supplement_index,
            "recordOrder": partition["remainderIds"],
            "rule": "For each independently requested D/E character, supply every complete remainder "
                    "record whose k_ele/keb exactly equals it. Deduplicate core and repeated identities; "
                    "preserve full-union order and record bytes. No match is disclosed without substitutes."})
        packet = json.loads(frozen(OLD_PACKET / "packet.json"))
        packet.update(
            presentationVersion="compact-002",
            reviewerKanjidicProjectionRecords=182, reviewerJmdictCoreRecords=partition["core"],
            reviewerJmdictUnreadRemainderRecords=partition["remainder"],
            retainedOutsideChain=["evidence/xml-presentation.json", "evidence/font-cmap.json",
                                  "evidence/baseline-title-index.txt", "evidence/dictionary-index.json",
                                  "evidence/kanjidic2-records.xml", "evidence/jmdict-families.xml"],
            reviewScope="Only source lines in this run's opened chains were read. Full packet retention "
                        "and coordinator verification do not imply reviewer reading or acceptance.")
        new["packet.json"] = json_bytes(packet)
        new["REVIEW.md"] = f"""# Independent B131 compact-002 review packet

Snapshot: {CANDIDATE}
Base: {BASE}
Original selection/scan base remains 6da1184b82b60553f9b65c57f53289c779f96f7c.

Review the three new kanji cards, their canonical stroke JSON, and four wrapper-only
changes in existing word articles. No word-prose exception or new word is assigned.
Both reviewers receive the same frozen teaching and select independently, serially.

## Contract

Assess correctness, scoped coverage, consistency/quiz safety and comprehensibility
separately as CLEAN, NEEDS FIX or UNVERIFIED, with source-line citations, severity,
confidence and limits. CLEAN is bounded absence of an established defect, not
exhaustive correctness. There is no finding quota or supplied comparison verdict.
Use applicable opened dictionary families, restrictions, register/spelling
distinctions and ordinary secondary senses. Distinct displayed titles alone do
not settle answer ambiguity. Exclusions are direct symmetric pairs, not transitive.
Separate metadata readings from quiz selections and mnemonic shapes from history.

The run-specific instruction controls access, phases and the sole report write.
Copied repository guidance cannot authorize wider tools. No content edits, shell,
agents, author rationale, other reviews, browser, JVM/emulator or device work.

## Explicit projected source scope

KANJIDIC review projection: all182 complete record identities in original order.
The only removed element classes are codepoint, dic_number, query_code; meaning
with any m_lang attribute; and reading whose r_type is pinyin, korean_r, korean_h
or vietnam. Every other element, attribute and text value is retained, including
literal, radical, misc, ja_on/ja_kun, English meanings and nanori. The coordinator
re-derives and byte-compares the projection and verifies each record's exact removed set.

JMdict review core: {partition['core']} of874 complete unmodified canonical-equal record lines,
in original order. Include a record if any keb contains 羊/衛/衞/霜, any keb is an
exact declared character (three targets, 衞, any new-card quiz_exclusions or 古右川),
or any reb is exactly a card-displayed reading: えい, え, よう, ひつじ, そう, しも.
The remaining{partition['remainder']} complete records remain in the full packet source and are initially UNREAD.
For each independently requested D/E character, phase2 mechanically adds every
complete omitted record whose k_ele/keb exactly equals that character, deduplicating
core and repeated records and preserving original complete bytes/order. No matching
record in the frozen union is disclosed explicitly, without substitutes or hints.
Supplemental dictionary bytes count toward worst-case and actual phase2 capacity.
Do not infer impossibility from this restricted core or from a missing source match.

evidence/xml-presentation.json, evidence/font-cmap.json,
evidence/baseline-title-index.txt, evidence/dictionary-index.json, and the full
evidence/kanjidic2-records.xml and evidence/jmdict-families.xml are packet-retained,
coordinator-verified and OUTSIDE THE REVIEWER CHAIN. All seven original source
selections and two empty residuals remain accounted for by the original source contract.
The full same-commit title index has1257 entries. Its mechanical delta from the
1254-line baseline has exactly3 additions (衛, 羊, 霜), zero removals and zero changes.
The baseline itself is retained but unread in this pass.

Never claim to have read a packet asset or record outside your own opened chain.
Coordinator verification is not reviewer reading. Mark every judgment that depends
on omitted classes, unread records or other unopened evidence UNVERIFIED and explain
the dependency. Request no wider access and invent no substitute support.

## Evidence and unchanged limits

All actual same-commit kanji articles are retained for mechanical D/E extension.
Only curated options are in the initial core; reviewers choose D/E independently.
The packet has complete before/after support snapshots and the exact wrapper diff.
Ten actual successful committed check logs and their receipts are retained.
Six complete local captured HTML responses have complete neutral source extracts.
Every named Weblio section and the complete Kotobank body is retained, with source
labels; no author passage selection or new fetch is used. Images/layout remain
unverified. Raw HTML/SVG, binary Joyo PDF, receipts, and non-chain assets are unread
under the reviewer's chain-only contract and must be disclosed as limits.
Cached complete Joyo pages are evidence, not fresh PDF-glyph inspection.

Geometry is reproduced against pinned SVG/converter data, not visually accepted.
Font summary: bounded209 code points cover all Han in the three new cards,
comparison identifiers and explicit components, NOT all text of179 legacy articles.
All three actual bundled cmaps lack U+4E8D, U+51DC, U+5F73, U+885E and U+97CB.
No rendered fallback, native or device acceptance is claimed.
The reading model covers finite pools only: zero production/padded hits does not
erase six hypothetical smaller-pool collisions or establish arbitrary/custom,
multiple-borrow, Kotlin, native or device acceptance.

Mechanical source/gate preparation is not linguistic review or delivery.
Published membership remains264/1228 with964 remaining; B131 adds no delivery.
Forecasts are not guarantees. Fresh startup and pre-phase-2 capacity gates and
actual no-compaction context audits remain mandatory.
""".encode("utf-8")
        added_names = set(new) - set(sums)
        for name, digest in sums.items():
            write_frozen(PACKET / name, new.pop(name) if name in new else frozen(OLD_PACKET / name, digest))
            guard.check()
        for name, raw in new.items():
            write_frozen(PACKET / name, raw)
        new_sums = {name: sha(frozen(PACKET / name)) for name in [*sums, *sorted(added_names)]}
        manifest = freeze_json(PACKET / "SHA256SUMS.json", dict(sorted(new_sums.items())))
        freeze_json(HERE / "derivation-verification-002.json", {
            "candidate": CANDIDATE, "status": "PASS", "kanjidicRecords": kd_audits,
            "jmdictPartition": partition, "titleDelta": delta_audit,
            "sourcePacketManifestSha256": OLD_PACKET_SHA,
            "normalization": "Original compact XML record lines are canonical. KD uses only specified "
                             "subtree removals and canonical serialization; JMdict copies exact record bytes."})
        config = json.loads(frozen(OLD_HERE / "batch.json"))
        config.update(packetManifestSha256=manifest["sha256"], presentationVersion="compact-002")
        freeze_json(HERE / "batch.json", config)
        expected = {"core": 615, "coreBytes": 249780}
        mismatches = {key: {"expected": value, "actual": partition[key]}
                      for key, value in expected.items() if partition[key] != value}
        record = {
            "status": "VERIFIED_PACKET_PREPARATION_ONLY", "candidate": CANDIDATE,
            "sourcePacket": {"path": str(OLD_PACKET / "SHA256SUMS.json"), "sha256": OLD_PACKET_SHA},
            "sourceContract": {"path": str(OLD_HERE / "source-contract.json"), "sha256": CONTRACT_SHA},
            "calibration": {"path": str(CALIBRATION), "sha256": CALIBRATION_SHA},
            "packetManifest": manifest, "retainedFileNames": len(sums), "sameByteFiles": len(sums) - 2,
            "changedFiles": ["REVIEW.md", "packet.json"], "addedFiles": sorted(set(new_sums) - set(sums)),
            "derivations": {name: {"path": str(PACKET / name), "sha256": new_sums[name],
                                   "bytes": (PACKET / name).stat().st_size} for name in
                            ("evidence/kanjidic2-review-projection.xml", "evidence/jmdict-review-core.xml",
                             "evidence/title-index-delta.txt")},
            "kanjidic": {"fullBytes": len(full_kd), "projectionBytes": len(kd), "records": len(kd_audits)},
            "jmdict": {k: v for k, v in partition.items() if k not in
                       {"coreIds", "remainderIds", "ruleMatches", "declaredCharacters"}},
            "coordinatorEstimateMismatches": mismatches}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Packet derivation RAM breach")
    record["memory"] = memory
    result = freeze_json(HERE / "packet-build-002.json", record)
    print(json.dumps(result))
    print(json.dumps({"kdBytes": len(kd), "jmdictCore": partition["core"],
                      "jmdictCoreBytes": len(jm), "mismatches": mismatches}))


if __name__ == "__main__":
    main()
