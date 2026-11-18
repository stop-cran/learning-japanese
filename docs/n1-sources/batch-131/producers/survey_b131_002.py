import copy
import xml.etree.ElementTree as ET
import survey_b131 as survey
from b131_common import HERE, sha, write


def xml_output(path, tag, nodes):
    nodes = list(nodes)
    original = {n.findtext("ent_seq") or n.findtext("literal"): sha(survey.canonical(n).encode()) for n in nodes}
    root = ET.Element(tag)
    root.extend(copy.deepcopy(nodes))
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    write(path, raw)
    actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(survey.canonical(n).encode()) for n in ET.fromstring(raw)}
    assert original == actual
    return {"sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": actual}


survey.OUT = HERE / "survey-002"
survey.xml_output = xml_output
if __name__ == "__main__":
    survey.main()
