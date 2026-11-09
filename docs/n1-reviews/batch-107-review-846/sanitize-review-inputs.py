#!/usr/bin/env python3
"""Publish path-redacted copies without changing the original review-input bytes."""
import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path

EXPECTED = {
    "review-prompt.original.txt": "05939b565afedac6a15e1b29f6739ced40017bb561b38010648170621370648c",
    "common-packet.original.txt": "8511ec0650e0cac7c9993997a3c40d5182611511d34bfaf042d0a583d8afacca",
}
SENSITIVE = (
    r"\b(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
    r"Bearer\s+[A-Za-z0-9._~+/-]{20,}",
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sanitize(raw, roots):
    text = raw.decode("utf-8")
    mappings = []
    for label, root in roots:
        for suffix, value in (("_ESCAPED", root.replace("\\", "\\\\")), ("", root)):
            token = f"__{label}{suffix}__"
            if token in text:
                raise ValueError(f"Redaction token already occurs: {token}")
            mappings.append((token, value))
    sanitized = text
    counts = {}
    for token, value in mappings:
        counts[token] = sanitized.count(value)
        sanitized = sanitized.replace(value, token)
    if re.search(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]", sanitized):
        raise ValueError("A Windows absolute path remains")
    if any(re.search(pattern, sanitized, re.IGNORECASE) for pattern in SENSITIVE):
        raise ValueError("Credential-shaped material requires manual review")
    restored = sanitized
    for token, value in mappings:
        restored = restored.replace(token, value)
    if restored != text:
        raise ValueError("Path redaction changed other input text")
    return sanitized.encode("utf-8"), counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--originals", type=Path, required=True)
    parser.add_argument("--content-root", required=True)
    parser.add_argument("--git-metadata-root", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    outputs = {
        "review-prompt.original.txt": args.output_dir / "review-prompt.sanitized.txt",
        "common-packet.original.txt": args.output_dir / "common-packet.sanitized.txt.gz",
    }
    receipt_path = args.output_dir / "sanitized-inputs-provenance.json"
    if receipt_path.exists() or any(path.exists() for path in outputs.values()):
        raise FileExistsError("Refusing to overwrite review evidence")
    roots = [("CONTENT_ROOT", args.content_root), ("GIT_METADATA_ROOT", args.git_metadata_root)]
    receipt = {"batch": "107", "inputs": {}, "limits": (
        "The reviewers read the original bytes, not these path-redacted copies. "
        "Only reversible root-path substitutions were made; exact originals and raw events remain local. "
        "The credential-shaped pattern scan is not a general privacy certification.")}
    for name, output_path in outputs.items():
        original = (args.originals / name).read_bytes()
        if digest(original) != EXPECTED[name]:
            raise ValueError(f"Original input hash differs: {name}")
        sanitized, counts = sanitize(original, roots)
        output = gzip.compress(sanitized, compresslevel=9, mtime=0) if output_path.suffix == ".gz" else sanitized
        if output_path.suffix == ".gz" and gzip.decompress(output) != sanitized:
            raise ValueError("Compressed copy does not reproduce sanitized bytes")
        with output_path.open("xb") as stream:
            stream.write(output)
        receipt["inputs"][name] = {
            "originalSha256": EXPECTED[name], "originalBytes": len(original),
            "sanitizedSha256": digest(sanitized), "sanitizedBytes": len(sanitized),
            "publishedCopy": output_path.name, "publishedCopySha256": digest(output),
            "pathSubstitutionCounts": counts,
        }
    with receipt_path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=True))
