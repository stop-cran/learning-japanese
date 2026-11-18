"""Version the packet/prompt builders for complete Weblio section evidence."""
import difflib
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen


def replace_once(text, before, after):
    require(text.count(before) == 1, f"Expected one replacement: {before[:80]!r}")
    return text.replace(before, after)


def main():
    original = frozen(TOOLS / "build-packet.py")
    text = original.decode("utf-8")
    text = replace_once(
        text,
        "candidate manifest, and the one-time snapshot capture. Digital Daijisen extracts use extract-daijisen-v1.",
        "candidate manifest, and the one-time snapshot capture. All named Weblio source sections are extracted.",
    )
    text = replace_once(text, "Usage: python -B build-packet.py <batch>",
                        "Usage: python -B build-packet-v2.py <batch>")
    text = replace_once(
        text, '\ndef main(batch):',
        '\nfrom weblio_sections import METHOD as SECTION_METHOD, extract as extract_sections\n\n\ndef main(batch):',
    )
    text = replace_once(text, "text, problem = extract(raw)", "text, problem = extract_sections(raw)")
    text = replace_once(text, '"extractionMethod": METHOD,', '"extractionMethod": SECTION_METHOD,')
    text = replace_once(
        text, "build, with mechanical Digital Daijisen extracts ({supplied} supplied); a failed or",
        "build, with complete named-source section extracts ({supplied} supplied responses); a failed or",
    )
    text = replace_once(
        text, "ambiguous page is recorded without any substitute. Raw SVGs, raw responses and the",
        "ambiguous page is recorded without any substitute. Each section keeps its source label;\n"
              "different dictionaries are not one unified entry. Raw SVGs, raw responses and the",
    )
    before = '"builder": {"path": str(TOOLS / "build-packet.py"), "sha256": sha((TOOLS / "build-packet.py").read_bytes())},'
    after = '"builder": {"path": str(TOOLS / "build-packet-v2.py"), "sha256": sha((TOOLS / "build-packet-v2.py").read_bytes()),\n' \
            '                          "extractorSha256": sha((TOOLS / "weblio_sections.py").read_bytes())},'
    text = replace_once(text, before, after)
    packet = text.encode("utf-8")

    prompt_original = frozen(TOOLS / "build-prompts.py")
    prompt_text = prompt_original.decode("utf-8")
    prompt_text = replace_once(prompt_text, "Usage: python -B build-prompts.py <batch>",
                               "Usage: python -B build-prompts-v2.py <batch>")
    prompt_text = replace_once(prompt_text, "'SUPPLIED Digital Daijisen extract'",
                               "'SUPPLIED complete Weblio source-section extract'")
    prompt_text = replace_once(
        prompt_text,
        '"builder": {"path": str(TOOLS / "build-prompts.py"), "sha256": sha((TOOLS / "build-prompts.py").read_bytes())},',
        '"builder": {"path": str(TOOLS / "build-prompts-v2.py"), "sha256": sha((TOOLS / "build-prompts-v2.py").read_bytes())},',
    )
    prompt = prompt_text.encode("utf-8")
    outputs = {"build-packet-v2.py": (original, packet), "build-prompts-v2.py": (prompt_original, prompt)}
    proof_path = WS / "scratch-118" / "review" / "source-section-tooling.json"
    require(not proof_path.exists() and all(not (TOOLS / name).exists() for name in outputs),
            "Preserve existing source-section tooling")
    for name, (_, data) in outputs.items():
        compile(data, name, "exec")
    derivations = []
    for name, (before_bytes, data) in outputs.items():
        source_name = name.replace("-v2", "")
        binding = write_frozen(TOOLS / name, data)
        patch = "".join(difflib.unified_diff(
            before_bytes.decode("utf-8").splitlines(keepends=True),
            data.decode("utf-8").splitlines(keepends=True),
            fromfile=source_name, tofile=name,
        )).encode("utf-8")
        patch_binding = write_frozen(proof_path.parent / f"{name}.patch", patch)
        derivations.append({"source": str(TOOLS / source_name), "sourceSha256": sha(before_bytes),
                            "output": binding, "patch": patch_binding})
    result = {
        "purpose": "Supply all complete named Weblio source sections with preserved classifications.",
        "derivations": derivations,
        "extractor": {"path": str(TOOLS / "weblio_sections.py"),
                      "sha256": sha((TOOLS / "weblio_sections.py").read_bytes())},
        "unchanged": "Original builders, receipt formats, gate checks, blinding, serial admission, "
                     "RAM guards and report/audit contracts. Prompt B116 byte-equality proof is retained.",
        "limits": "Tool preparation only; actual candidate packet and linguistic acceptance remain pending.",
    }
    print(json.dumps(freeze_json(proof_path, result)))


if __name__ == "__main__":
    main()
