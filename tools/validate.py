#!/usr/bin/env python3
"""Validate kanji/, words/, articles/ and strokes/ of this content repo.

Usage: python tools/validate.py
Requires: pip install pyyaml
Exit code 1 when any error is found.
"""
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parent.parent
# Kotlin Char.isWhitespace includes Unicode separators, but not U+0085 (NEL).
KOTLIN_WHITESPACE = ("\t\n\v\f\r\x1c\x1d\x1e\x1f \u00a0\u1680"
                     "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a"
                     "\u2028\u2029\u202f\u205f\u3000")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
KANA = re.compile(r"^[ぁ-ゟァ-ヿー.\-]+$")
RAW_HTML = re.compile(r"<\s*/?\s*(script|iframe|style|object|embed|img|a|div|span|svg)\b", re.I)

KANJI_REQUIRED = ["kanji", "title", "jlpt", "tags", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"]
WORD_REQUIRED = ["word", "reading", "title", "type", "kanji", "tags"]
WORD_TYPES = {"kango", "wago", "jukujikun", "gairaigo"}
KANJI_LISTS = ("tags", "onyomi", "kunyomi", "distractors")
WORD_LISTS = ("kanji", "tags")
KANJI_INTS = ("jlpt", "strokes", "radicalNumber")
KANJI_SECTIONS = ["Meaning and origin", "Readings", "Common words", "Notes"]
WORD_SECTIONS = ["Meaning", "How the kanji combine", "Synonyms and antonyms", "Distinctive meaning"]

errors: list[str] = []


def err(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT).as_posix()}: {message}")


def parse(path: Path):
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        err(path, f"not valid UTF-8: {exc}")
        return None, ""
    text = text.removeprefix("\ufeff").replace("\r\n", "\n")
    end = text.find("\n---", 4) if text.startswith("---\n") else -1
    if end < 0:
        return None, text
    header = text[4:end]
    after_marker = text.find("\n", end + 1)
    body = text[after_marker + 1:].lstrip("\n") if after_marker >= 0 else ""
    fields = parse_android_header(header)
    article = path.parent.name == "articles"
    try:
        if article and fields is None and not has_yaml_mapping_root(header):
            return None, text
        meta = yaml.safe_load(header)
    except RecursionError:
        err(path, "front matter YAML nesting is too deep")
        return None, text
    except (yaml.YAMLError, ValueError) as exc:
        err(path, f"invalid front matter YAML: {exc}")
        return None, text
    if article and meta is None and fields == {}:
        meta = {}
    if not isinstance(meta, dict):
        err(path, "front matter must be a mapping of field names to values")
        return None, body
    check_android_front_matter(path, fields, meta)
    return meta, text if article and fields is None else body


def has_yaml_mapping_root(header: str) -> bool:
    """Distinguish intended article metadata from ordinary Markdown after a thematic break."""
    try:
        for event in yaml.parse(header):
            if isinstance(event, (yaml.MappingStartEvent, yaml.SequenceStartEvent,
                                  yaml.ScalarEvent, yaml.AliasEvent)):
                return isinstance(event, yaml.MappingStartEvent)
    except yaml.YAMLError:
        return False
    return False


def parse_android_header(header: str) -> dict[str, str | list[str]] | None:
    """Mirror FrontMatter.kt at kanji-cards-android 8c130a25, including its whitespace."""
    def unquote(value: str) -> str:
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            return value[1:-1]
        return value

    fields: dict[str, str | list[str]] = {}
    for line in header.split("\n"):
        if not line.strip(KOTLIN_WHITESPACE) or line.lstrip(KOTLIN_WHITESPACE).startswith("#"):
            continue
        key, colon, raw = line.partition(":")
        if not colon or not key:
            return None
        raw = raw.strip(KOTLIN_WHITESPACE)
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1]
            value = ([unquote(item.strip(KOTLIN_WHITESPACE)) for item in inner.split(",")]
                     if inner.strip(KOTLIN_WHITESPACE) else [])
        else:
            value = unquote(raw)
        fields[key.strip(KOTLIN_WHITESPACE)] = value
    return fields


def check_android_front_matter(path: Path, fields: dict | None, meta: dict) -> None:
    if fields is None:
        err(path, "Android front matter requires 'key: value' on each non-comment header line")
        return
    if path.parent.name == "kanji":
        known = KANJI_REQUIRED + ["phonetic", "distractors"]
    elif path.parent.name == "words":
        known = WORD_REQUIRED
    else:
        known = ["title"]
    for key in known:
        if key not in meta and key not in fields:
            continue
        yaml_value = meta.get(key)
        expected = yaml_value if isinstance(yaml_value, list) else str(yaml_value)
        if key not in meta or key not in fields or fields[key] != expected:
            err(path, f"'{key}' is interpreted differently by YAML and Android; "
                "use flat scalars or inline lists without YAML escapes, inline comments, "
                "or commas inside list values")


def check_metadata(path: Path, meta: dict, required: list[str],
                   lists: tuple[str, ...], integers: tuple[str, ...] = (),
                   optional: tuple[str, ...] = ()) -> bool:
    if not isinstance(meta, dict):
        err(path, "front matter must be a mapping of field names to values")
        return False
    before = len(errors)
    for key in required:
        if key not in meta:
            err(path, f"missing field '{key}'")
    for key in dict.fromkeys([*required, *lists, *optional]):
        if key not in meta:
            continue
        value = meta[key]
        if key in lists:
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                err(path, f"'{key}' must be a list of strings")
        elif key in integers:
            if type(value) is not int:
                err(path, f"'{key}' must be a YAML integer (not a boolean or quoted string)")
        elif not isinstance(value, str) or not value.strip():
            err(path, f"'{key}' must be a nonempty string")
    return len(errors) == before


def check_body(path: Path, meta: dict, body: str) -> None:
    visible = []
    fence = ""
    for number, line in enumerate(body.splitlines()):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + r"{" + str(len(fence)) + r",}\s*", line):
                fence = ""
            continue
        if marker:
            fence = marker.group(1)
            continue
        visible.append((number, line))
    headings = []
    for number, line in visible:
        match = re.match(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$", line)
        if match:
            headings.append((number, len(match.group(1)), match.group(2)))
    sections = KANJI_SECTIONS if path.parent.name == "kanji" else WORD_SECTIONS
    actual = [title for _, level, title in headings if level == 2 and title in sections]
    if actual != sections:
        err(path, "body must contain these ## sections once each, in order: " + "; ".join(sections))
    if path.parent.name != "kanji":
        return
    if isinstance(meta.get("kanji"), str) and isinstance(meta.get("title"), str):
        title = f"{meta['kanji']} \u2014 {meta['title']}"
        if (not headings or headings[0][1:] != (1, title)
                or sum(level == 1 for _, level, _ in headings) != 1):
            err(path, f"body must start with a single H1 matching metadata: # {title}")
    start = headings[0][0] if headings else -1
    end = next((number for number, level, _ in headings if level == 2), len(body.splitlines()))
    labels = (r"\bStrokes:", r"\bKey\s*\(radical\):", r"\bPhonetic:", r"\bJLPT:")
    if not any(all(re.search(label, line.replace("**", ""), re.I) for label in labels)
               for number, line in visible if start < number < end):
        err(path, "kanji body needs a facts line (Strokes, Key (radical), Phonetic, JLPT) "
            "between the H1 and the first ## section")


def check_links(path: Path, body: str) -> None:
    imported_dirs = {(ROOT / folder).resolve() for folder in ("kanji", "words", "articles")}
    imported_source = path.parent.resolve() in imported_dirs
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
        target_path = (path.parent / file_part).resolve()
        if imported_source and target_path.parent not in imported_dirs:
            err(path, f"relative link targets non-imported content: {target}; "
                "use a kanji/, words/, or articles/ page, or an HTTPS source")
            continue
        if not target_path.is_file():
            err(path, f"broken link: {target}")


def is_int32(value) -> bool:
    return type(value) is int and -(2**31) <= value < 2**31


def is_finite_number(value) -> bool:
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def check_strokes(path: Path) -> int | None:
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        err(path, f"not valid UTF-8: {exc}")
        return None
    try:
        data = json.loads(text)
    except RecursionError:
        err(path, "strokes JSON nesting is too deep")
        return None
    except ValueError as exc:
        err(path, f"invalid strokes JSON: {exc}")
        return None
    if not isinstance(data, dict):
        err(path, "strokes JSON must be an object")
        return None
    if type(data.get("schemaVersion")) is not int or data["schemaVersion"] != 1:
        err(path, "'schemaVersion' must be the integer 1")
    if data.get("kanji") != path.stem:
        err(path, f"'kanji' must match the strokes file name '{path.stem}'")
    view_box = data.get("viewBox")
    if not isinstance(view_box, list) or not all(is_finite_number(value) for value in view_box):
        err(path, "'viewBox' must be a list of finite numbers")
    count = data.get("strokeCount")
    if not is_int32(count):
        err(path, "'strokeCount' must be a 32-bit integer (not a boolean)")
        count = None
    strokes = data.get("strokes")
    if not isinstance(strokes, list):
        err(path, "'strokes' must be a list")
        return count
    if count is not None and len(strokes) != count:
        err(path, "'strokeCount' does not match the number of strokes")
    for index, stroke in enumerate(strokes):
        if not isinstance(stroke, dict):
            err(path, f"strokes[{index}] must be an object")
            continue
        if not is_int32(stroke.get("id")):
            err(path, f"strokes[{index}].id must be a 32-bit integer (not a boolean)")
        if "type" in stroke and not isinstance(stroke["type"], str):
            err(path, f"strokes[{index}].type must be a string when supplied")
        points = stroke.get("points")
        if (not isinstance(points, list) or len(points) < 2
                or any(not isinstance(point, list) or len(point) != 2
                       or not all(is_finite_number(value) for value in point) for point in points)):
            err(path, f"strokes[{index}].points must contain at least 2 finite 2D points")
    return count


def check_kanji(path: Path, meta: dict, titles: dict,
                stroke_counts: dict[str, int | None] | None = None) -> None:
    if not check_metadata(path, meta, KANJI_REQUIRED, KANJI_LISTS, KANJI_INTS, ("phonetic",)):
        return
    if meta["kanji"] != path.stem or len(meta["kanji"]) != 1:
        err(path, "'kanji' must be a single character equal to the file name")
    if meta["jlpt"] not in (1, 2, 3, 4, 5):
        err(path, "'jlpt' must be 1-5")
    expected_tag = f"jlpt-n{meta['jlpt']}"
    if {tag for tag in meta["tags"] if tag.startswith("jlpt-n")} != {expected_tag}:
        err(path, f"'tags' must include '{expected_tag}' and no conflicting JLPT tag")
    if not 1 <= meta["radicalNumber"] <= 214:
        err(path, "'radicalNumber' must be 1-214")
    if meta["strokes"] < 1:
        err(path, "'strokes' must be a positive integer")
    for key in ("onyomi", "kunyomi"):
        for reading in meta[key]:
            if not KANA.match(reading):
                err(path, f"{key} entry is not kana: {reading}")
    title = meta["title"].strip().lower()
    if title in titles:
        err(path, f"duplicate title '{meta['title']}' (also {titles[title]})")
    titles[title] = path.name
    strokes_path = ROOT / "strokes" / f"{path.stem}.json"
    if not strokes_path.is_file():
        err(path, "missing strokes file (run tools/generate_strokes.py)")
    else:
        count = check_strokes(strokes_path) if stroke_counts is None else stroke_counts.get(path.stem)
        if count is not None and count != meta["strokes"]:
            err(path, f"strokes count {meta['strokes']} does not match {strokes_path.name}")
    choices = meta.get("distractors", [])
    if len(choices) != len(set(choices)):
        err(path, "'distractors' must not contain repeated entries")
    distractors = set()
    for other in choices:
        if len(other) != 1:
            err(path, f"distractor '{other}' must be a single kanji character")
        elif other == meta["kanji"]:
            err(path, "'distractors' must not include the card itself")
        elif not (ROOT / "kanji" / f"{other}.md").is_file():
            err(path, f"distractor '{other}' has no card")
        else:
            distractors.add(other)
    if len(distractors) < 2:
        err(path, "'distractors' must include at least 2 distinct existing nonself kanji")


def check_word(path: Path, meta: dict) -> None:
    if not check_metadata(path, meta, WORD_REQUIRED, WORD_LISTS):
        return
    if meta["word"] != path.stem:
        err(path, "'word' must equal the file name")
    if not KANA.match(meta["reading"]):
        err(path, f"reading is not kana: {meta['reading']}")
    if meta["type"] not in WORD_TYPES:
        err(path, f"unknown type '{meta['type']}'")
    for char in meta["kanji"]:
        if len(char) != 1:
            err(path, f"kanji entry '{char}' must be a single character")
        elif char not in meta["word"]:
            err(path, f"kanji '{char}' does not occur in the word")
    written = {char for char in meta["word"]
               if char == "\u3007" or unicodedata.name(char, "").startswith(
                   ("CJK UNIFIED IDEOGRAPH-", "CJK COMPATIBILITY IDEOGRAPH-"))}
    missing = written - set(meta["kanji"])
    if missing:
        err(path, "'kanji' is missing written Han characters: " + ", ".join(sorted(missing)))


def err_count_for(path: Path) -> int:
    rel = path.relative_to(ROOT).as_posix()
    return sum(1 for e in errors if e.startswith(rel + ":"))


def main() -> int:
    errors.clear()
    stroke_counts = {path.stem: check_strokes(path) for path in sorted((ROOT / "strokes").glob("*.json"))}
    titles: dict[str, str] = {}
    for folder in ("kanji", "words", "articles"):
        for path in sorted((ROOT / folder).glob("*.md")):
            meta, body = parse(path)
            if folder == "articles":
                check_links(path, body)
                continue
            if meta is None:
                if not err_count_for(path):
                    err(path, "missing front matter")
                continue
            if folder == "kanji":
                check_kanji(path, meta, titles, stroke_counts)
            else:
                check_word(path, meta)
            check_body(path, meta, body)
            check_links(path, body)
    for message in errors:
        print(message)
    print(f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
