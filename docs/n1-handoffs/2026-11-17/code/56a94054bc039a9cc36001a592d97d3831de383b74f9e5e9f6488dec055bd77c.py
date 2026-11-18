"""Extract every complete named Weblio source section without selecting claims."""
import re

from common import TOOLS, load_module

original = load_module("n1_original_packet_extract", TOOLS / "build-packet.py")
MARKER = re.compile(r"<!--(\u958b\u59cb|\u7d42\u4e86)\s*([^<>]*?)\s*-->")
START = "\u958b\u59cb"
METHOD = (
    "extract-weblio-sections-v1: strict UTF-8; identify every named Weblio start/end "
    "comment; require nonempty unique names, matching adjacent start/end pairs and "
    "no unrecognized start/end comments. Process every pair in response order; do "
    "not select sections by claim. For each complete body, apply the unchanged "
    "extract-daijisen-v1 text transformation, substituting only its boundary markers "
    "to invoke the original extractor. Prepend an explicit 'Weblio source section: "
    "<name>' provenance label to each body. Preserve every extracted section; any "
    "ambiguous or empty section makes the entire response AMBIGUOUS. This preserves "
    "source classifications; it does not treat different dictionaries as one entry. "
    "Underlying text transformation: " + original.METHOD
)


def extract(raw):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return None, f"Response is not strict UTF-8: {error}"
    markers = list(MARKER.finditer(text))
    apparent = re.findall(r"<!--(?:\u958b\u59cb|\u7d42\u4e86)", text)
    if len(markers) != len(apparent) or not markers or len(markers) % 2:
        return None, "Unrecognized, absent or unpaired source-section markers"
    sections, names = [], set()
    for offset in range(0, len(markers), 2):
        start, end = markers[offset:offset + 2]
        name = start[2].strip()
        if (start[1] != START or end[1] == START or not name
                or name != end[2].strip() or name in names):
            return None, f"Ambiguous source-section pair at marker {offset + 1}"
        names.add(name)
        body = text[start.end():end.start()]
        bounded = (original.START + body + original.END).encode("utf-8")
        rendered, problem = original.extract(bounded)
        if problem:
            return None, f"Source section {name!r}: {problem}"
        sections.append(f"Weblio source section: {name}\n{rendered}")
    return "\n".join(sections), None
