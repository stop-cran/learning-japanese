import copy
import hashlib
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

import yaml

import generate_strokes
from audit_n1_batch import (
    activated_baseline_pairs, audit, lexical_pair, runtime_delta, teachable_lexical_pair,
)
from build_manifest import build_manifest
from freeze_n1_sources import KVG_REVISION


class N1SourcePlanAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / "docs" / "n1-sources"
        self.folder.mkdir(parents=True)
        (self.root / "tools").mkdir()
        self.batch = "900"
        self.commit = "a" * 40
        self.kanji = "甲"
        self.reading = "こうおつ"

    def write_json(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")

    def article(self, name, meta, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
                        + "---\n" + body, encoding="utf-8", newline="\n")

    def edit_meta(self, name, changes):
        path = self.root / name
        parts = path.read_text(encoding="utf-8").split("---", 2)
        meta = yaml.safe_load(parts[1])
        meta.update(changes)
        self.article(name, meta, parts[2].lstrip("\n"))

    def file(self, suffix):
        return self.folder / f"batch-{self.batch}-{suffix}.json"

    def make_fixture(self, variant):
        self.variant = variant
        self.word = "甲未" if variant == "teaching" else "甲乙"
        self.word_article = f"words/{self.word}.md"
        self.word_components = ["甲", "未"] if variant == "teaching" else ["甲", "乙"]
        self.anchor = "- old example"
        self.added = f"- [{self.word}](../{self.word_article}) {self.reading} - example"

        for item, title in (("乙", "existing"), ("丙", "third"), ("丁", "fourth"),
                            ("戊", "fifth"), ("己", "bridge")):
            self.article(f"kanji/{item}.md", {"kanji": item, "title": title, "quiz_exclusions": []},
                         f"## Common words\n{self.anchor}\n")
        self.article("words/玄.md", {"word": "玄", "title": "other"}, "Existing word.\n")
        self.write_json(self.root / "tools" / "order_variants.json", {})

        svg = ('<svg xmlns="http://www.w3.org/2000/svg">\n<path d="M 0 0 L 10 10"/>\n'
               '</svg>\n').encode("utf-8")
        blob = hashlib.sha1(b"blob " + str(len(svg)).encode("ascii") + b"\0" + svg).hexdigest()
        converter = Path(generate_strokes.__file__).read_bytes().replace(b"\r\n", b"\n")
        converter_sha = hashlib.sha256(converter).hexdigest()
        source_row = {
            "kanji": self.kanji, "sourceRow": 1,
            "metadata": {"kanji": self.kanji, "strokes": 1, "radical": "一",
                         "radicalNumber": 1, "onyomi": ["コウ"], "kunyomi": ["きのえ"],
                         "grade": "8"},
            "kanjivgInventory": {"path": f"kanji/{ord(self.kanji):05x}.svg",
                                 "type": "blob", "sha": blob, "size": len(svg)},
        }
        source_name = "docs/n1-sources/source-index.json"
        snapshot_name = "docs/n1-source-snapshot.json"
        self.write_json(self.root / source_name, [source_row])
        self.write_json(self.root / snapshot_name,
                        {"kanjivg": {"revision": KVG_REVISION,
                                     "converter": {"normalizedSha256": converter_sha}}})
        self.write_json(self.folder / "baseline-word-candidates.json", [])
        before = build_manifest(self.root)
        self.base_files = {
            "manifest.json": json.dumps(before),
            source_name: (self.root / source_name).read_text(encoding="utf-8"),
            snapshot_name: (self.root / snapshot_name).read_text(encoding="utf-8"),
            "docs/n1-sources/baseline-word-candidates.json": (
                self.folder / "baseline-word-candidates.json").read_text(encoding="utf-8"),
            "tools/order_variants.json": (self.root / "tools" / "order_variants.json").read_text(
                encoding="utf-8"),
            "kanji/乙.md": (self.root / "kanji" / "乙.md").read_text(encoding="utf-8"),
        }

        target_meta = {
            "kanji": self.kanji, "title": "new", "jlpt": 1,
            "tags": ["jlpt-n1", "grade-8"], "strokes": 1, "radical": "一", "radicalNumber": 1,
            "onyomi": ["コウ"], "kunyomi": ["きのえ"], "quizOnyomi": ["コウ"],
            "quizKunyomi": [], "distractors": ["丙", "丁", "戊"], "quiz_exclusions": ["乙"],
        }
        target_body = (
            "## Readings\n| Reading | Type | Example |\n| --- | --- | --- |\n"
            f"| コウ | on | [{self.word}](../{self.word_article}) {self.reading} |\n"
            "| きのえ | kun | Reference only; search-only and source-only spelling. |\n"
            f"## Common words\n- [{self.word}](../{self.word_article}) {self.reading}\n"
        )
        self.article("kanji/甲.md", target_meta, target_body)
        word_meta = {
            "word": self.word, "reading": self.reading, "title": "example word", "type": "kango",
            "kanji": self.word_components, "tags": ["kango"], "quiz_exclusions": ["玄"],
        }
        word_body = "[甲](../kanji/甲.md) (コウ) supplies the first component.\n"
        if variant == "current":
            word_body += "[乙](../kanji/乙.md) (オツ) supplies the second component.\n"
            existing = self.root / "kanji" / "乙.md"
            existing.write_text(existing.read_text(encoding="utf-8").replace(
                self.anchor, self.anchor + "\n" + self.added), encoding="utf-8", newline="\n")
        self.article(self.word_article, word_meta, word_body)
        self.write_json(self.root / "strokes" / "甲.json",
                        generate_strokes.convert(self.kanji, svg.decode("utf-8")))
        (self.folder / f"batch-{self.batch}-kanjivg.svg").write_bytes(svg)
        self.write_json(self.file("stroke-evidence"), {
            "revision": KVG_REVISION, "gitBlob": blob, "sha256": hashlib.sha256(svg).hexdigest(),
            "bytes": len(svg), "dictionaryStrokeCount": 1, "sourceStrokePaths": 1,
            "converterNormalizedSha256": converter_sha,
        })

        member_entry = ET.fromstring(
            f"<entry><ent_seq>1</ent_seq><k_ele><keb>{self.word}</keb></k_ele>"
            f"<r_ele><reb>{self.reading}</reb></r_ele><sense><gloss>example</gloss></sense></entry>")
        search_entry = ET.fromstring(
            "<entry><ent_seq>2</ent_seq><k_ele><keb>甲い</keb>"
            "<ke_inf>search-only kanji form</ke_inf></k_ele><r_ele><reb>きのえ</reb></r_ele>"
            "<sense><gloss>reference</gloss></sense></entry>")
        packet_names = [("lexical", "jmdict", [member_entry, search_entry]),
                        ("comparison", "comparisons", [])]
        if variant == "current":
            packet_names.append(("completion", "completion-comparisons", []))
        for selection, packet, entries in packet_names:
            self.write_json(self.file(f"{selection}-selection"),
                            {"schemaVersion": 1, "batch": self.batch,
                             "entryIds": [entry.findtext("ent_seq") for entry in entries]})
            xml_root = ET.Element("JMdict")
            for entry in entries:
                xml_root.append(copy.deepcopy(entry))
            ET.ElementTree(xml_root).write(self.folder / f"batch-{self.batch}-{packet}.xml",
                                           encoding="utf-8", xml_declaration=True)

        members = [self.kanji]
        frozen = {"batch": self.batch, "baseCommit": self.commit, "membership": members,
                  "sourceRows": [1], "members": [{"kanji": self.kanji, "sourceRow": 1}]}
        self.write_json(self.file("membership"), frozen)
        ledger = {"batch": self.batch, "baseCommit": self.commit, "membership": members,
                  "drafted": members, "sourceCompletionPlan": self.file("source-completion-plan").name,
                  "sourceCompletionAudit": self.file("source-completion-audit").name,
                  "draftAudit": self.file("draft-audit").name}
        self.write_json(self.file("progress"), ledger)
        pairs = [[self.kanji, self.word_article]]
        if variant == "current":
            pairs.append(["乙", self.word_article])
        directions = []
        for component, article in pairs:
            for origin, target in ((f"kanji/{component}.md", article),
                                   (article, f"kanji/{component}.md")):
                directions.append({"from": origin, "to": target,
                                   "href" if variant == "teaching" else "relative": f"../{target}"})
        choices = [{"kanji": item, "displayedTitle" if variant == "teaching" else "actualTitle": title}
                   for item, title in (("丙", "third"), ("丁", "fourth"), ("戊", "fifth"))]
        plan = {"schemaVersion": 1, "batch": self.batch, "membership": members,
                "sourceRows": [1], "sourcePreparationComplete": True}
        common = {key: target_meta[key] for key in ("title", "jlpt", "tags", "strokes",
                                                     "radical", "radicalNumber", "quizOnyomi",
                                                     "quizKunyomi")}
        common.update({"curatedDistractors": choices, "quizExclusions": ["乙"]})
        support = {key: word_meta[key] for key in ("word", "reading", "title", "type", "kanji", "tags")}
        support["quizExclusions"] = ["玄"]
        additions = ["kanji/甲.md", "strokes/甲.json", self.word_article]
        changes = ["kanji/乙.md"] if variant == "current" else []
        if variant == "teaching":
            plan.update({
                "publishedBase": self.commit,
                "kanjiTeachingPlan": {
                    **common, "fullOnyomi": ["コウ"], "fullKunyomi": ["きのえ"],
                    "offeredOnKeys": ["こう"], "offeredKunKeys": [],
                    "onRow": {"reading": "コウ", "type": "on", "example": self.word,
                              "kana": self.reading, "link": f"../{self.word_article}",
                              "usefulness": "A bounded example."},
                    "kunRow": {"reading": "きのえ", "type": "kun", "disposition": "Reference only.",
                               "qualification": "search-only spelling", "word": "甲い", "kana": "きのえ"},
                },
                "supportTeachingPlan": {**support, "newNecessaryArticles": [self.word_article],
                                        "reusedSupportArticles": []},
                "navigationAndBaselinePlan": {
                    "runtimePathsToAddLater": additions, "baselineRuntimePathsToChange": [],
                    "proposedAllMappedPairs": pairs, "requiredDirections": directions,
                    "activatedBaselinePairs": [],
                },
                "strokeAndFontPlan": {"pinnedSvg": f"batch-{self.batch}-kanjivg.svg", "paths": 1},
            })
            source_audit = {"schemaVersion": 1, "batch": self.batch, "completeMemberFamilies": 2,
                            "completeComparisonFamilies": 0, "distinctFamilyUnion": 2}
        else:
            plan.update({
                "publishedBaseline": self.commit,
                "sourceEvidence": {
                    "memberFamilies": f"batch-{self.batch}-jmdict.xml",
                    "initialComparisons": f"batch-{self.batch}-comparisons.xml",
                    "completionComparisons": f"batch-{self.batch}-completion-comparisons.xml",
                    "completeFamilyCounts": [2, 0, 0], "distinctCompleteFamilies": 2,
                },
                "kanjiPlan": {
                    **common, "article": "kanji/甲.md", "onyomi": ["コウ"], "kunyomi": ["きのえ"],
                    "offeredKeys": {"on": ["こう"], "kun": []},
                    "readingRows": [
                        {"kind": "on", "raw": "コウ", "selected": True, "example": self.word,
                         "reading": self.reading, "link": f"../{self.word_article}",
                         "usefulness": "A bounded example."},
                        {"kind": "kun", "raw": "きのえ", "selected": False,
                         "disposition": "Reference only."},
                    ],
                },
                "supportPlan": {"reused": [], "newNecessary": [
                    {**support, "article": self.word_article, "entryId": "1", "selectedSense": 1}]},
                "linkPlan": {"allMappedPairs": pairs, "requiredDirections": directions,
                             "activatedBaselinePairs": [],
                             "exactReusedChange": {"article": "kanji/乙.md",
                                                   "afterExistingLine": self.anchor,
                                                   "addLine": self.added}},
                "strokePlan": {"source": f"batch-{self.batch}-kanjivg.svg",
                               "evidence": self.file("stroke-evidence").name,
                               "sourceRevision": KVG_REVISION, "dictionaryAndSvgCount": 1,
                               "converterNormalizedSha256": converter_sha},
            })
            source_audit = {"schemaVersion": 1, "batch": self.batch, "memberFamilies": 2,
                            "comparisonFamilies": 0, "completeDictionaryFamilies": 2}
        self.write_json(self.file("source-completion-plan"), plan)
        self.write_json(self.file("source-completion-audit"), source_audit)
        current = build_manifest(self.root)
        self.write_json(self.root / "manifest.json", current)
        draft = {
            "schemaVersion": 1, "batch": self.batch, "sourcePlan": ledger["sourceCompletionPlan"],
            "frozenInputHashesVerified": 1, "exactSourceMembershipAndRawMetadataVerified": True,
            "runtimeAdditions": {"files": additions, "images": []}, "baselineRuntimeEdits": changes,
            "contentVersion": current["contentVersion"], "allMappedPairs": pairs,
            "activatedBaselinePairs": [], "requiredLinkDirectionsVerified": len(directions),
            "fullOnyomi": ["コウ"], "fullKunyomi": ["きのえ"], "quizOnyomi": ["コウ"],
            "quizKunyomi": [], "directKanjiGuards": ["乙"], "directWordGuards": ["玄"],
            "curatedWrongChoices": ["丙", "丁", "戊"], "strokePaths": 1, "pointsPerPath": 16,
            "exactPinnedConverterOutput": True,
            "runtimeHashes": {name: current["files"][name] for name in additions + changes},
        }
        suffix = "MirrorNotAppExecution" if variant == "current" else ""
        draft["offeredOnKeys" + suffix] = ["こう"]
        draft["offeredKunKeys" + suffix] = []
        if variant == "current":
            draft["distinctCompleteDictionaryFamiliesReproduced"] = 2
            draft.update({"publishedBaseline": self.commit, "membership": members, "sourceRow": 1})
        self.write_json(self.file("draft-audit"), draft)

    def sync_runtime(self):
        current = build_manifest(self.root)
        self.write_json(self.root / "manifest.json", current)
        path = self.file("draft-audit")
        draft = json.loads(path.read_text(encoding="utf-8"))
        draft["contentVersion"] = current["contentVersion"]
        draft["runtimeHashes"] = {name: current["files"][name] for name in draft["runtimeHashes"]}
        self.write_json(path, draft)

    def run_audit(self):
        def frozen_base(root, commit, name):
            self.assertEqual(root, self.root)
            self.assertEqual(commit, self.commit)
            return self.base_files[name]
        with patch("audit_n1_batch.base_file", side_effect=frozen_base):
            return audit(self.root, self.batch)

    def test_teaching_plan_matches_source_only_reading(self):
        self.make_fixture("teaching")
        result = self.run_audit()
        self.assertEqual((result["requiredReciprocalPairs"], result["readingDispositions"],
                          result["sourceOnlyOfferedKeys"]), (1, 2, 0))

    def test_current_plan_covers_new_and_existing_kanji(self):
        self.make_fixture("current")
        result = self.run_audit()
        self.assertEqual((result["requiredReciprocalPairs"], result["changedReusedArticles"],
                          result["dictionaryFamilies"]), (2, 1, 2))

    def test_rejects_unrelated_runtime_addition(self):
        self.make_fixture("current")
        self.article("words/余計.md", {"word": "余計"}, "Unrecorded.\n")
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Runtime additions differ"):
            self.run_audit()

    def test_rejects_unrecorded_baseline_content_change(self):
        self.make_fixture("current")
        path = self.root / "kanji" / "丙.md"
        path.write_text(path.read_text(encoding="utf-8") + "Extra.\n", encoding="utf-8")
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Changed baseline"):
            self.run_audit()

    def test_rejects_unrecorded_runtime_language_change(self):
        self.make_fixture("current")
        self.write_json(self.root / "content-language.json",
                        {"baseLanguage": "ru", "targetLanguage": "ja"})
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Baseline runtime metadata changed"):
            self.run_audit()

    def test_runtime_delta_preserves_nonversion_manifest_fields(self):
        before = {"schemaVersion": 1, "baseLanguage": "en", "targetLanguage": "ja",
                  "contentVersion": "old", "files": {}}
        after = {**before, "contentVersion": "new"}
        runtime_delta(before, after, set(), set())
        for field, value in (("schemaVersion", 2), ("baseLanguage", "ru"),
                             ("targetLanguage", "ko"), ("newField", True)):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "Baseline runtime metadata changed"):
                    runtime_delta(before, {**after, field: value}, set(), set())
        with self.assertRaisesRegex(ValueError, "Baseline runtime metadata changed"):
            runtime_delta(before, {key: value for key, value in after.items()
                                   if key != "baseLanguage"}, set(), set())

    def test_runtime_delta_rejects_empty_section_additions_and_removals(self):
        before = {"schemaVersion": 1, "contentVersion": "old", "files": {}}
        after = {**before, "contentVersion": "new"}
        with self.assertRaisesRegex(ValueError, "Baseline runtime sections changed"):
            runtime_delta(before, {**after, "unexpectedSection": {}}, set(), set())
        with self.assertRaisesRegex(ValueError, "Baseline runtime sections changed"):
            runtime_delta({**before, "emptySection": {}}, after, set(), set())

    def test_rejects_extra_text_in_recorded_baseline_edit(self):
        self.make_fixture("current")
        path = self.root / "kanji" / "乙.md"
        path.write_text(path.read_text(encoding="utf-8") + "Extra.\n", encoding="utf-8")
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
            self.run_audit()

    def test_rejects_missing_existing_kanji_to_word_link(self):
        self.make_fixture("current")
        bad_line = self.added.replace(f"../{self.word_article}", "../words/missing.md")
        path = self.root / "kanji" / "乙.md"
        path.write_text(path.read_text(encoding="utf-8").replace(self.added, bad_line), encoding="utf-8")
        plan_path = self.file("source-completion-plan")
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["linkPlan"]["exactReusedChange"]["addLine"] = bad_line
        self.write_json(plan_path, plan)
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Missing reciprocal link: kanji/乙.md"):
            self.run_audit()

    def test_rejects_missing_word_to_existing_kanji_link(self):
        self.make_fixture("current")
        path = self.root / self.word_article
        path.write_text(path.read_text(encoding="utf-8").replace("../kanji/乙.md", "../kanji/missing.md"),
                        encoding="utf-8")
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Missing reciprocal link: words/"):
            self.run_audit()

    def test_rejects_omitted_existing_component_pair(self):
        self.make_fixture("current")
        plan_path, draft_path = self.file("source-completion-plan"), self.file("draft-audit")
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        draft = json.loads(draft_path.read_text(encoding="utf-8"))
        plan["linkPlan"]["allMappedPairs"] = plan["linkPlan"]["allMappedPairs"][:1]
        draft["allMappedPairs"] = draft["allMappedPairs"][:1]
        self.write_json(plan_path, plan)
        self.write_json(draft_path, draft)
        with self.assertRaisesRegex(ValueError, "do not cover existing components"):
            self.run_audit()

    def test_rejects_omitted_written_component_and_reciprocal_link(self):
        self.make_fixture("current")
        self.edit_meta(self.word_article, {"kanji": [self.kanji]})
        path = self.root / self.word_article
        path.write_text(path.read_text(encoding="utf-8").replace(
            "[乙](../kanji/乙.md)", "乙"), encoding="utf-8")
        plan_path, draft_path = self.file("source-completion-plan"), self.file("draft-audit")
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        draft = json.loads(draft_path.read_text(encoding="utf-8"))
        plan["supportPlan"]["newNecessary"][0]["kanji"] = [self.kanji]
        plan["linkPlan"]["allMappedPairs"] = plan["linkPlan"]["allMappedPairs"][:1]
        plan["linkPlan"]["requiredDirections"] = plan["linkPlan"]["requiredDirections"][:2]
        draft["allMappedPairs"] = draft["allMappedPairs"][:1]
        draft["requiredLinkDirectionsVerified"] = 2
        self.write_json(plan_path, plan)
        self.write_json(draft_path, draft)
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Support word metadata omits a written kanji card"):
            self.run_audit()

    def test_rejects_restricted_spelling_reading_pair(self):
        self.make_fixture("current")
        packet = self.folder / f"batch-{self.batch}-jmdict.xml"
        tree = ET.parse(packet)
        ET.SubElement(tree.getroot().find("entry/r_ele"), "re_restr").text = "別"
        tree.write(packet, encoding="utf-8", xml_declaration=True)
        with self.assertRaisesRegex(ValueError, "Support identity/restrictions mismatch"):
            self.run_audit()

    def test_rejects_inapplicable_selected_sense(self):
        self.make_fixture("current")
        packet = self.folder / f"batch-{self.batch}-jmdict.xml"
        tree = ET.parse(packet)
        ET.SubElement(tree.getroot().find("entry/sense"), "stagk").text = "別"
        tree.write(packet, encoding="utf-8", xml_declaration=True)
        with self.assertRaisesRegex(ValueError, "Support identity/restrictions mismatch"):
            self.run_audit()

    def test_rejects_inapplicable_selected_sense_reading(self):
        self.make_fixture("current")
        packet = self.folder / f"batch-{self.batch}-jmdict.xml"
        tree = ET.parse(packet)
        ET.SubElement(tree.getroot().find("entry/sense"), "stagr").text = "べつ"
        tree.write(packet, encoding="utf-8", xml_declaration=True)
        with self.assertRaisesRegex(ValueError, "Support identity/restrictions mismatch"):
            self.run_audit()

    def test_rejects_search_only_support_spelling(self):
        self.make_fixture("current")
        packet = self.folder / f"batch-{self.batch}-jmdict.xml"
        tree = ET.parse(packet)
        ET.SubElement(tree.getroot().find("entry/k_ele"), "ke_inf").text = "search-only kanji form"
        tree.write(packet, encoding="utf-8", xml_declaration=True)
        with self.assertRaisesRegex(ValueError, "Support identity/restrictions mismatch"):
            self.run_audit()

    def test_rejects_search_only_support_reading(self):
        self.make_fixture("current")
        packet = self.folder / f"batch-{self.batch}-jmdict.xml"
        tree = ET.parse(packet)
        ET.SubElement(tree.getroot().find("entry/r_ele"), "re_inf").text = "search-only kana form"
        tree.write(packet, encoding="utf-8", xml_declaration=True)
        with self.assertRaisesRegex(ValueError, "Support identity/restrictions mismatch"):
            self.run_audit()

    def test_teachable_reading_requires_an_applicable_non_search_only_row(self):
        entry = ET.fromstring("""
            <entry>
              <k_ele><keb>甲乙</keb></k_ele>
              <k_ele><keb>甲丙</keb></k_ele>
              <r_ele><reb>こうおつ</reb><re_inf>search-only kana form</re_inf>
                <re_restr>甲乙</re_restr></r_ele>
              <r_ele><reb>こうおつ</reb><re_restr>甲丙</re_restr></r_ele>
              <sense><gloss>example</gloss></sense>
            </entry>
        """)
        self.assertTrue(lexical_pair(entry, "甲乙", "こうおつ"))
        self.assertFalse(teachable_lexical_pair(entry, "甲乙", "こうおつ"))
        self.assertTrue(teachable_lexical_pair(entry, "甲丙", "こうおつ"))

    def test_rejects_conflicting_duplicate_dictionary_family(self):
        self.make_fixture("current")
        source = ET.parse(self.folder / f"batch-{self.batch}-jmdict.xml").getroot().find("entry")
        source.find("sense/gloss").text = "different"
        packet = self.folder / f"batch-{self.batch}-comparisons.xml"
        root = ET.Element("JMdict")
        root.append(source)
        ET.ElementTree(root).write(packet, encoding="utf-8", xml_declaration=True)
        self.write_json(self.file("comparison-selection"),
                        {"schemaVersion": 1, "batch": self.batch, "entryIds": ["1"]})
        with self.assertRaisesRegex(ValueError, "Conflicting duplicate dictionary family"):
            self.run_audit()

    def test_rejects_source_only_reading_as_quiz_choice(self):
        self.make_fixture("teaching")
        self.edit_meta("kanji/甲.md", {"quizKunyomi": ["きのえ"]})
        article = self.root / "kanji" / "甲.md"
        article.write_text(article.read_text(encoding="utf-8").replace(
            "Reference only; search-only and source-only spelling.",
            f"[{self.word}](../{self.word_article}) {self.reading}; search-only spelling."),
            encoding="utf-8")
        plan_path, draft_path = self.file("source-completion-plan"), self.file("draft-audit")
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        draft = json.loads(draft_path.read_text(encoding="utf-8"))
        plan["kanjiTeachingPlan"]["quizKunyomi"] = ["きのえ"]
        plan["kanjiTeachingPlan"]["kunRow"].update(
            {"example": self.word, "kana": self.reading, "link": f"../{self.word_article}",
             "usefulness": "Attempt to offer the reference reading."})
        draft["quizKunyomi"] = ["きのえ"]
        self.write_json(plan_path, plan)
        self.write_json(draft_path, draft)
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Search-only reading unqualified/offered"):
            self.run_audit()

    def test_rejects_reordered_reading_dispositions(self):
        self.make_fixture("current")
        path = self.file("source-completion-plan")
        plan = json.loads(path.read_text(encoding="utf-8"))
        plan["kanjiPlan"]["readingRows"].reverse()
        self.write_json(path, plan)
        with self.assertRaisesRegex(ValueError, "reading dispositions/order"):
            self.run_audit()

    def test_rejects_wrong_displayed_reading_for_selected_example(self):
        self.make_fixture("current")
        path = self.root / "kanji" / "甲.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace(f") {self.reading} |", ") まちがい |"),
                        encoding="utf-8")
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Selected reading lacks mapped table support"):
            self.run_audit()

    def test_rejects_changed_direct_exclusion(self):
        self.make_fixture("current")
        self.edit_meta("kanji/甲.md", {"quiz_exclusions": []})
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Quiz labels or direct exclusions differ"):
            self.run_audit()

    def test_rejects_changed_word_exclusion(self):
        self.make_fixture("current")
        self.edit_meta(self.word_article, {"quiz_exclusions": []})
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Support word identity or exclusions differ"):
            self.run_audit()

    def test_rejects_identical_displayed_quiz_titles(self):
        self.make_fixture("current")
        self.edit_meta("kanji/丙.md", {"title": "new"})
        self.sync_runtime()
        before = json.loads(self.base_files["manifest.json"])
        current = json.loads((self.root / "manifest.json").read_text(encoding="utf-8"))
        before["files"]["kanji/丙.md"] = current["files"]["kanji/丙.md"]
        self.base_files["manifest.json"] = json.dumps(before)
        path = self.file("source-completion-plan")
        plan = json.loads(path.read_text(encoding="utf-8"))
        plan["kanjiPlan"]["curatedDistractors"][0]["actualTitle"] = "new"
        self.write_json(path, plan)
        with self.assertRaisesRegex(ValueError, "Quiz labels differ"):
            self.run_audit()

    def test_rejects_reverse_direct_exclusion_between_choices(self):
        self.make_fixture("current")
        self.edit_meta("kanji/丙.md", {"quiz_exclusions": ["甲"]})
        self.sync_runtime()
        before = json.loads(self.base_files["manifest.json"])
        current = json.loads((self.root / "manifest.json").read_text(encoding="utf-8"))
        before["files"]["kanji/丙.md"] = current["files"]["kanji/丙.md"]
        self.base_files["manifest.json"] = json.dumps(before)
        with self.assertRaisesRegex(ValueError, "directly excluded pair"):
            self.run_audit()

    def test_direct_exclusions_are_not_transitive(self):
        self.make_fixture("current")
        self.edit_meta("kanji/丙.md", {"quiz_exclusions": ["己"]})
        self.edit_meta("kanji/丁.md", {"quiz_exclusions": ["己"]})
        self.sync_runtime()
        before = json.loads(self.base_files["manifest.json"])
        current = json.loads((self.root / "manifest.json").read_text(encoding="utf-8"))
        for name in ("kanji/丙.md", "kanji/丁.md"):
            before["files"][name] = current["files"][name]
        self.base_files["manifest.json"] = json.dumps(before)
        self.assertEqual(self.run_audit()["requiredReciprocalPairs"], 2)

    def test_rejects_missing_activated_baseline_pair(self):
        self.make_fixture("current")
        path = self.folder / "baseline-word-candidates.json"
        self.write_json(path,
                        [{"kanji": "甲", "article": "words/既存.md"}])
        self.base_files["docs/n1-sources/baseline-word-candidates.json"] = path.read_text(
            encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Activated baseline pair missing"):
            self.run_audit()

    def test_rejects_altered_frozen_candidate_inventory(self):
        self.make_fixture("current")
        self.base_files["docs/n1-sources/baseline-word-candidates.json"] = json.dumps(
            [{"kanji": self.kanji, "article": "words/既存.md"}], ensure_ascii=False)
        with self.assertRaisesRegex(ValueError, "Immutable baseline word candidates changed"):
            self.run_audit()

    def test_accepts_crlf_frozen_candidate_blob(self):
        self.make_fixture("current")
        name = "docs/n1-sources/baseline-word-candidates.json"
        self.base_files[name] = self.base_files[name].replace("\n", "\r\n")
        self.assertEqual(self.run_audit()["activatedBaselinePairs"], 0)

    def test_prior_support_words_and_frozen_candidates_are_both_activated(self):
        before = {"files": {"words/甲別.md": "a", "words/別.md": "b", "kanji/甲.md": "c"}}
        candidates = [{"kanji": "甲", "article": "words/既存.md"},
                      {"kanji": "乙", "article": "words/別.md"}]
        self.assertEqual(activated_baseline_pairs(before, ["甲"], candidates),
                         {("甲", "words/既存.md"), ("甲", "words/甲別.md")})

    def test_rejects_unregistered_previously_added_support_word(self):
        self.make_fixture("current")
        name = "words/甲別.md"
        self.article(name, {"word": "甲別", "kanji": ["甲", "別"]}, "Existing support.\n")
        before = json.loads(self.base_files["manifest.json"])
        before["files"][name] = build_manifest(self.root)["files"][name]
        self.base_files["manifest.json"] = json.dumps(before)
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Activated baseline pair missing"):
            self.run_audit()

    def test_rejects_altered_stroke_geometry(self):
        self.make_fixture("current")
        path = self.root / "strokes" / "甲.json"
        stroke = json.loads(path.read_text(encoding="utf-8"))
        stroke["strokes"][0]["points"][0][0] += 1
        self.write_json(path, stroke)
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Stroke geometry differs"):
            self.run_audit()

    def test_accepts_crlf_checkout_of_pinned_lf_svg(self):
        self.make_fixture("current")
        path = self.folder / f"batch-{self.batch}-kanjivg.svg"
        svg = path.read_bytes()
        self.assertIn(b"\n", svg)
        path.write_bytes(svg.replace(b"\n", b"\r\n"))
        self.assertEqual(self.run_audit()["requiredReciprocalPairs"], 2)

    def test_accepts_pinned_svg_whose_source_blob_uses_crlf(self):
        self.make_fixture("current")
        path = self.folder / f"batch-{self.batch}-kanjivg.svg"
        svg = path.read_bytes().replace(b"\n", b"\r\n")
        path.write_bytes(svg)
        blob = hashlib.sha1(b"blob " + str(len(svg)).encode("ascii") + b"\0" + svg).hexdigest()
        source_name = "docs/n1-sources/source-index.json"
        source_path = self.root / source_name
        source = json.loads(source_path.read_text(encoding="utf-8"))
        source[0]["kanjivgInventory"].update({"sha": blob, "size": len(svg)})
        self.write_json(source_path, source)
        self.base_files[source_name] = source_path.read_text(encoding="utf-8")
        evidence_path = self.file("stroke-evidence")
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence.update({"bytes": len(svg), "sha256": hashlib.sha256(svg).hexdigest(), "gitBlob": blob})
        self.write_json(evidence_path, evidence)
        self.assertEqual(self.run_audit()["requiredReciprocalPairs"], 2)

    def test_rejects_modified_svg_in_crlf_checkout(self):
        self.make_fixture("current")
        path = self.folder / f"batch-{self.batch}-kanjivg.svg"
        svg = path.read_bytes().replace(b"L 10 10", b"L 20 20").replace(b"\n", b"\r\n")
        path.write_bytes(svg)
        with self.assertRaisesRegex(ValueError, "Pinned SVG or converter differs"):
            self.run_audit()

    def test_rejects_forged_svg_and_matching_receipt(self):
        self.make_fixture("current")
        svg_path = self.folder / f"batch-{self.batch}-kanjivg.svg"
        altered = svg_path.read_bytes() + b"\n"
        svg_path.write_bytes(altered)
        evidence_path = self.file("stroke-evidence")
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence.update({"bytes": len(altered), "sha256": hashlib.sha256(altered).hexdigest(),
                         "gitBlob": hashlib.sha1(b"blob " + str(len(altered)).encode("ascii")
                                                + b"\0" + altered).hexdigest()})
        self.write_json(evidence_path, evidence)
        with self.assertRaisesRegex(ValueError, "Pinned SVG or converter differs"):
            self.run_audit()

    def test_rejects_changed_stroke_order_variants(self):
        self.make_fixture("current")
        self.write_json(self.root / "tools" / "order_variants.json", {"甲": [[1]]})
        path = self.root / "strokes" / "甲.json"
        stroke = json.loads(path.read_text(encoding="utf-8"))
        stroke["orderVariants"] = [[1]]
        self.write_json(path, stroke)
        self.sync_runtime()
        with self.assertRaisesRegex(ValueError, "Frozen stroke variants changed"):
            self.run_audit()

    def test_rejects_incomplete_source_plan(self):
        self.make_fixture("current")
        path = self.file("source-completion-plan")
        plan = json.loads(path.read_text(encoding="utf-8"))
        del plan["strokePlan"]["sourceRevision"]
        self.write_json(path, plan)
        with self.assertRaisesRegex(ValueError, "Stroke plan missing required fields: sourceRevision"):
            self.run_audit()

    def test_rejects_malformed_support_list(self):
        self.make_fixture("current")
        path = self.file("source-completion-plan")
        plan = json.loads(path.read_text(encoding="utf-8"))
        plan["supportPlan"]["newNecessary"] = None
        self.write_json(path, plan)
        with self.assertRaisesRegex(ValueError, "Unsupported source-plan support articles"):
            self.run_audit()

    def test_rejects_malformed_reading_rows(self):
        self.make_fixture("current")
        path = self.file("source-completion-plan")
        plan = json.loads(path.read_text(encoding="utf-8"))
        plan["kanjiPlan"]["readingRows"] = [None]
        self.write_json(path, plan)
        with self.assertRaisesRegex(ValueError, "Invalid source-plan reading rows"):
            self.run_audit()

    def test_rejects_malformed_runtime_additions(self):
        self.make_fixture("current")
        path = self.file("draft-audit")
        draft = json.loads(path.read_text(encoding="utf-8"))
        draft["runtimeAdditions"]["files"] = None
        self.write_json(path, draft)
        with self.assertRaisesRegex(ValueError, "Draft runtime changes differ"):
            self.run_audit()

    def test_rejects_incomplete_draft_evidence(self):
        self.make_fixture("current")
        path = self.file("draft-audit")
        draft = json.loads(path.read_text(encoding="utf-8"))
        del draft["exactSourceMembershipAndRawMetadataVerified"]
        self.write_json(path, draft)
        with self.assertRaisesRegex(ValueError, "Draft audit missing required fields"):
            self.run_audit()

    def test_rejects_changed_frozen_source_snapshot(self):
        self.make_fixture("current")
        path = self.root / "docs" / "n1-source-snapshot.json"
        path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Immutable source snapshot changed"):
            self.run_audit()

    def test_new_runtime_receipt_preserves_original_draft_evidence(self):
        self.make_fixture("current")
        original_path = self.file("draft-audit")
        original_bytes = original_path.read_bytes()
        original = json.loads(original_bytes)
        path = self.root / "kanji" / "甲.md"
        path.write_text(path.read_text(encoding="utf-8") + "Reconciled wording.\n", encoding="utf-8")
        current = build_manifest(self.root)
        self.write_json(self.root / "manifest.json", current)
        revised = copy.deepcopy(original)
        revised["contentVersion"] = current["contentVersion"]
        revised["runtimeHashes"] = {name: current["files"][name] for name in revised["runtimeHashes"]}
        revised["supersedesDraftAudit"] = original_path.name
        revised_path = self.file("reconciled-audit")
        self.write_json(revised_path, revised)
        ledger_path = self.file("progress")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger.update({"draftContentVersion": original["contentVersion"],
                       "runtimeAudit": revised_path.name,
                       "runtimeAuditContentVersion": current["contentVersion"]})
        self.write_json(ledger_path, ledger)
        self.assertEqual(self.run_audit()["contentVersion"], current["contentVersion"])
        self.assertEqual(original_path.read_bytes(), original_bytes)

    def test_rejects_runtime_receipt_without_original_draft_reference(self):
        self.make_fixture("current")
        draft = json.loads(self.file("draft-audit").read_text(encoding="utf-8"))
        revised_path = self.file("reconciled-audit")
        self.write_json(revised_path, draft)
        ledger_path = self.file("progress")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger.update({"runtimeAudit": revised_path.name,
                       "runtimeAuditContentVersion": draft["contentVersion"]})
        self.write_json(ledger_path, ledger)
        with self.assertRaisesRegex(ValueError, "does not identify its original draft"):
            self.run_audit()

    def test_rejects_runtime_receipt_if_original_draft_was_removed(self):
        self.make_fixture("current")
        original_path = self.file("draft-audit")
        draft = json.loads(original_path.read_text(encoding="utf-8"))
        draft["supersedesDraftAudit"] = original_path.name
        revised_path = self.file("reconciled-audit")
        self.write_json(revised_path, draft)
        ledger_path = self.file("progress")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger.update({"runtimeAudit": revised_path.name,
                       "runtimeAuditContentVersion": draft["contentVersion"]})
        self.write_json(ledger_path, ledger)
        original_path.unlink()
        with self.assertRaisesRegex(ValueError, "Original draft audit is missing"):
            self.run_audit()

    def test_rejects_runtime_receipt_path_traversal(self):
        self.make_fixture("current")
        ledger_path = self.file("progress")
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["runtimeAudit"] = "../reconciled-audit.json"
        self.write_json(ledger_path, ledger)
        with self.assertRaisesRegex(ValueError, "Unsupported runtime-audit evidence path"):
            self.run_audit()

    def test_rejects_unknown_ledger_instead_of_key_error(self):
        self.make_fixture("current")
        path = self.file("progress")
        ledger = json.loads(path.read_text(encoding="utf-8"))
        del ledger["sourceCompletionPlan"]
        self.write_json(path, ledger)
        with self.assertRaisesRegex(ValueError, "Unsupported or incomplete batch ledger"):
            self.run_audit()

    def test_legacy_ledger_remains_supported(self):
        self.make_fixture("teaching")
        path = self.file("progress")
        ledger = json.loads(path.read_text(encoding="utf-8"))
        ledger.update({
            "supportMappings": [{"kanji": self.kanji, "article": self.word_article,
                                 "newArticle": True, "primaryReading": self.reading, "entryIds": ["1"]}],
            "requiredReciprocalPairs": [[self.kanji, self.word_article]],
            "changedReusedPassages": [],
            "dictionaryPackets": [
                {"selection": self.file("lexical-selection").name,
                 "xml": f"batch-{self.batch}-jmdict.xml"},
                {"selection": self.file("comparison-selection").name,
                 "xml": f"batch-{self.batch}-comparisons.xml"},
            ],
            "readingDispositions": [
                {"kanji": self.kanji, "kind": "on", "reading": "コウ", "selected": True,
                 "reason": "A bounded example.", "entryIds": ["1"], "article": self.word_article},
                {"kanji": self.kanji, "kind": "kun", "reading": "きのえ", "selected": False,
                 "reason": "Reference only.", "entryIds": ["2"], "sourceOnly": True},
            ],
            "curatedProjection": [{"kanji": self.kanji, "quizOnyomi": ["コウ"], "quizKunyomi": [],
                                    "onKeys": ["こう"], "kunKeys": []}],
            "quizAudit": {self.kanji: {"title": "new", "distractors": ["丙", "丁", "戊"],
                                       "labels": ["third", "fourth", "fifth"]}},
            "wordQuizAudit": {"directExclusions": [{"word": self.word, "exclude": ["玄"]}]},
        })
        self.write_json(path, ledger)
        frozen_path = self.file("membership")
        frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
        del frozen["sourceRows"]
        self.write_json(frozen_path, frozen)
        self.assertEqual(self.run_audit()["requiredReciprocalPairs"], 1)


if __name__ == "__main__":
    unittest.main()
