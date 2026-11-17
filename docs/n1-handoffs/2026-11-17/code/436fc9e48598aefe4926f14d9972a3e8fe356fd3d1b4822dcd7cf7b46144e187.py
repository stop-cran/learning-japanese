"""Derive the B127 packet builder without modifying the frozen generic builder."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen


def main():
    here = Path(__file__).resolve().parent
    source = here / "build-packet-v4.py"
    raw = frozen(source)
    replacements = [
        ("from weblio_sections import METHOD as SECTION_METHOD, extract as extract_sections",
         "from b127_external_sources import METHOD as SECTION_METHOD, extract as extract_sections"),
        ("text, problem = extract_sections(raw)", 'text, problem = extract_sections(raw, result["finalUrl"])'),
        ("build-packet-v4.py", "build-packet-b127.py"),
        ('"weblio_sections.py"', '"b127_external_sources.py"'),
        ("raw Weblio responses fetched once at packet", "raw cited-source responses fetched once at packet"),
        ("with complete named-source section extracts", "with complete neutral source extracts"),
        ("The installed 5c000bd APK predates quiz_exclusions; compatibility is not claimed.",
         "Historical installed-APK references are not current device observations; compatibility is not claimed."),
    ]
    text, changes = raw.decode("utf-8"), []
    for before, after in replacements:
        count = text.count(before)
        require(count > 0 and after not in text, f"Ambiguous packet substitution: {before}")
        text = text.replace(before, after)
        changes.append({"before": before, "after": after, "count": count})
    restored = text
    for item in reversed(changes):
        require(restored.count(item["after"]) == item["count"], "Packet reverse count differs")
        restored = restored.replace(item["after"], item["before"])
    require(restored.encode("utf-8") == raw, "Unexpected packet changes")
    target = here / "build-packet-b127.py"
    compile(text, str(target), "exec")
    binding = write_frozen(target, text.encode("utf-8"))
    print(json.dumps(freeze_json(here.parent / "scratch-127" / "review" / "packet-builder-derivation.json", {
        "source": str(source), "sourceSha256": sha(raw), "target": binding,
        "substitutions": changes, "reverseExact": True,
        "reason": "Supply the actual Kanjipedia/Kotobank citations neutrally and avoid a stale installed-device claim.",
        "extractor": {"path": str(here / "b127_external_sources.py"),
                      "sha256": sha(frozen(here / "b127_external_sources.py"))},
    })))


if __name__ == "__main__":
    main()
