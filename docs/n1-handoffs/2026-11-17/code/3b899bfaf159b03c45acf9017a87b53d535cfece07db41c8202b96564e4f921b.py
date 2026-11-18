import gzip
import hashlib
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import b128_source_restream as module


class Guard:
    def check(self):
        pass


def entry(seq, kebs=(), rebs=(), gloss="sense"):
    k = "".join(f"<k_ele><keb>{item}</keb></k_ele>" for item in kebs)
    r = "".join(f"<r_ele><reb>{item}</reb></r_ele>" for item in rebs)
    return (f"<entry><ent_seq>{seq}</ent_seq>{k}{r}<sense>"
            f"<gloss xml:lang=\"eng\">{gloss}</gloss></sense></entry>")


def character(literal):
    return f"<character><literal>{literal}</literal><misc><grade>8</grade></misc></character>"


class RestreamTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.full = {
            "jmdict": [entry(1, ["\u5507"], ["\u304f\u3061\u3073\u308b"]),
                       entry(2, rebs=[module.READING], gloss="edge"),
                       entry(3, ["\u5507\u97f3"]), entry(4, ["\u5507\u7d05"])],
            "kanjidic2": [character(c) for c in module.LITERALS + ["\u53e3"]],
        }
        self.selected = {"jmdict": [0, 1, 2], "kanjidic2": list(range(len(module.LITERALS)))}
        self.queries = {"\u5507": ["1"], "\u5507\u97f3": ["3"], "\u53eb": [],
                        module.READING_KEY: ["2"]}

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, queries=None, alter=None):
        files, pinned, snapshot, declared = {}, {}, {"inputs": {}}, {}
        for kind, (filename, _, tag, key, output) in module.INPUTS.items():
            root = {"jmdict": "JMdict", "kanjidic2": "kanjidic2"}[kind]
            source = f"<{root}>{''.join(self.full[kind])}</{root}>".encode()
            compressed = gzip.compress(source)
            (self.dir / filename).write_bytes(compressed)
            parts = [self.full[kind][i] for i in self.selected[kind]]
            if alter and alter[0] == kind:
                parts[alter[1]] = parts[alter[1]].replace(">sense<", ">changed<")
            extracted = f"<{root}>{''.join(parts)}</{root}>".encode()
            files[module.PREFIX + output] = extracted
            ids = sorted(node.findtext(key) for node in ET.fromstring(extracted).findall(tag))
            compressed_sha = hashlib.sha256(compressed).hexdigest()
            xml_sha = hashlib.sha256(source).hexdigest()
            pinned[kind] = (filename, compressed_sha, tag, key, output)
            snapshot["inputs"][filename] = {"sha256": compressed_sha}
            snapshot[kind] = {"xmlSha256": xml_sha}
            declared[kind] = {"completeRecords": len(ids), "canonicalIdentities": ids,
                              "allSelectorsAndCanonicalRecordsMatchOriginal": True,
                              "compressedSha256": compressed_sha, "decompressedXmlSha256": xml_sha,
                              "extractedSha256": hashlib.sha256(extracted).hexdigest()}
        files[module.PREFIX + "selector-membership.json"] = json.dumps({
            "selectorRule": module.RULE, "allMatchingFamiliesIncluded": True,
            "kanjidic2LiteralSelectors": module.LITERALS,
            "exactKebOrRebQueries": self.queries if queries is None else queries}).encode()
        files[module.PREFIX + "source-verification-002.json"] = json.dumps(declared).encode()
        files["docs/n1-source-snapshot.json"] = json.dumps(snapshot).encode()
        return files.__getitem__, pinned

    def run_verify(self, **kwargs):
        blob, pinned = self.build(**kwargs)
        return module.verify(blob, Guard(), self.dir, pinned)

    def test_keb_and_reb_families_are_complete(self):
        result = self.run_verify()
        self.assertEqual(result["jmdict"]["identities"], ["1", "2", "3"])
        self.assertEqual(result["jmdict"]["membership"], self.queries)

    def test_reb_only_family_cannot_be_omitted(self):
        self.selected["jmdict"] = [0, 2]
        queries = dict(self.queries, **{module.READING_KEY: []})
        with self.assertRaisesRegex(Exception, "Missing applicable family: jmdict/2"):
            self.run_verify(queries=queries)

    def test_declared_family_without_exact_match_is_rejected(self):
        queries = dict(self.queries, **{"\u5507": ["1", "3"]})
        with self.assertRaisesRegex(Exception, "selector membership differs"):
            self.run_verify(queries=queries)

    def test_altered_record_is_rejected(self):
        with self.assertRaisesRegex(Exception, "Incomplete or altered record: jmdict/1"):
            self.run_verify(alter=("jmdict", 0))

    def test_changed_compressed_input_is_rejected(self):
        blob, pinned = self.build()
        filename = pinned["kanjidic2"][0]
        (self.dir / filename).write_bytes(gzip.compress(b"<kanjidic2></kanjidic2>"))
        with self.assertRaisesRegex(Exception, "Compressed source differs: kanjidic2"):
            module.verify(blob, Guard(), self.dir, pinned)


if __name__ == "__main__":
    unittest.main()
