#!/usr/bin/env python3
"""Validate kanji/, words/, articles/ and strokes/ of this content repo.

Usage: python tools/validate.py
Requires: pip install pyyaml
Exit code 1 when any error is found.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
KANA = re.compile(r"^[ぁ-ゟァ-ヿー.\-]+$")
RAW_HTML = re.compile(r"<\s*/?\s*(script|iframe|style|object|embed|img|a|div|span|svg)\b", re.I)

KANJI_REQUIRED = ["kanji", "title", "jlpt", "tags", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"]
WORD_REQUIRED = ["word", "reading", "title", "type", "kanji", "tags"]
WORD_TYPES = {"kango", "wago", "jukujikun", "gairaigo"}

errors: list[str] = []


def err(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT).as_posix()}: {message}")


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text.replace("\r\n", "\n"))
    if not match:
        return None, text
    try:
        return yaml.safe_load(match.group(1)) or {}, match.group(2)
    except yaml.YAMLError as exc:
        err(path, f"invalid front matter YAML: {exc}")
        return None, text


def check_links(path: Path, body: str) -> None:
    if RAW_HTML.search(body):
        err(path, "raw HTML is not allowed")
    for target in LINK.findall(body):
        if re.match(r"https://", target) or target.startswith("#"):
            continue
        if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I):
            err(path, f"unsupported link scheme: {target}")
            continue
        file_part = unquote(target.split("#", 1)[0])
        if not file_part.endswith(".md"):
            err(path, f"link must target a .md file: {target}")
            continue
        if not (path.parent / file_part).resolve().is_file():
            err(path, f"broken link: {target}")


def check_kanji(path: Path, meta: dict, titles: dict) -> None:
    for key in KANJI_REQUIRED:
        if key not in meta:
            err(path, f"missing field '{key}'")
    if err_count_for(path):
        return
    if meta["kanji"] != path.stem or len(meta["kanji"]) != 1:
        err(path, "'kanji' must be a single character equal to the file name")
    if meta["jlpt"] not in (1, 2, 3, 4, 5):
        err(path, "'jlpt' must be 1-5")
    for key in ("onyomi", "kunyomi"):
        for reading in meta[key]:
            if not KANA.match(reading):
                err(path, f"{key} entry is not kana: {reading}")
    title = meta["title"].strip().lower()
    if title in titles:
        err(path, f"duplicate title '{meta['title']}' (also {titles[title]})")
    titles[title] = path.name
    strokes_path = ROOT / "strokes" / f"{meta['kanji']}.json"
    if not strokes_path.is_file():
        err(path, "missing strokes file (run tools/generate_strokes.py)")
    else:
        data = json.loads(strokes_path.read_text(encoding="utf-8"))
        if data.get("strokeCount") != meta["strokes"] or len(data.get("strokes", [])) != meta["strokes"]:
            err(path, f"strokes count {meta['strokes']} does not match {strokes_path.name}")
    for other in meta.get("distractors", []):
        if not (ROOT / "kanji" / f"{other}.md").is_file():
            err(path, f"distractor '{other}' has no card")


def check_word(path: Path, meta: dict) -> None:
    for key in WORD_REQUIRED:
        if key not in meta:
            err(path, f"missing field '{key}'")
    if err_count_for(path):
        return
    if meta["word"] != path.stem:
        err(path, "'word' must equal the file name")
    if not KANA.match(meta["reading"]):
        err(path, f"reading is not kana: {meta['reading']}")
    if meta["type"] not in WORD_TYPES:
        err(path, f"unknown type '{meta['type']}'")
    for char in meta["kanji"]:
        if char not in meta["word"]:
            err(path, f"kanji '{char}' does not occur in the word")


def err_count_for(path: Path) -> int:
    rel = path.relative_to(ROOT).as_posix()
    return sum(1 for e in errors if e.startswith(rel + ":"))


def main() -> int:
    titles: dict[str, str] = {}
    for folder, checker in (("kanji", None), ("words", None), ("articles", None)):
        for path in sorted((ROOT / folder).glob("*.md")):
            meta, body = parse(path)
            if folder == "articles":
                check_links(path, body)
                continue
            if meta is None:
                err(path, "missing front matter")
                continue
            if folder == "kanji":
                check_kanji(path, meta, titles)
            else:
                check_word(path, meta)
            check_links(path, body)
    for message in errors:
        print(message)
    print(f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
