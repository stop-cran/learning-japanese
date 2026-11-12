"""Validate unpublished reading packages against the agreed schema 1 transport.

The default manifest must not publish these files. This checker still rejects a
package that could not be rendered once a reading map is deliberately enabled.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
HASH = re.compile(r"[0-9a-f]{64}")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
IMAGE_PATH = re.compile(r"reading-images/[a-z0-9]+(?:-[a-z0-9]+)*\.webp")
QUOTE = re.compile(r"「([^」]+)」")
BASES = {"original", "traditional-plot", "public-domain-text"}
ROLES = {"plot-check", "wording-source"}
N5_MIN_CHARS = 1000
N5_MAX_CHARS = 1500
N5_SECTIONS = 8
N5_MIN_PER_TIER = 4

PACKAGE_KEYS = {
    "schemaVersion", "id", "jlpt", "title", "japaneseTitle", "levelRationale",
    "provenance", "sections", "questions",
}
PROVENANCE_KEYS = {"originalTitle", "adaptation", "consulted", "credits", "rights", "distribution"}
ADAPTATION_KEYS = {"label", "basis"}
CONSULT_KEYS = {"originalTitle", "author", "edition", "sourceUrl", "accessed", "role"}
RIGHTS_KEYS = {"status", "note"}
DISTRIBUTION_KEYS = {"reviewed", "note"}
SECTION_KEYS = {"id", "text", "translation", "vocabulary"}
SPAN_KEYS = {"start", "end", "text", "reading", "headword", "gloss", "word"}
QUESTION_KEYS = {"id", "tier", "prompt", "options", "correctOptionId", "explanation", "evidence", "image"}
OPTION_KEYS = {"id", "text"}
EVIDENCE_KEYS = {"sectionId", "start", "end"}
IMAGE_KEYS = {"path", "sha256", "description"}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _pairs(pairs):
    keys = [key for key, _ in pairs]
    _require(len(keys) == len(set(keys)), "duplicate JSON key")
    return dict(pairs)


def load_package(path: Path) -> dict:
    raw = path.read_bytes()
    _require(b"\r" not in raw, "reading JSON must use LF line endings")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"reading JSON is not UTF-8: {exc}") from exc
    try:
        document = json.loads(text, object_pairs_hook=_pairs, parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"invalid JSON constant {value}")))
    except json.JSONDecodeError as exc:
        raise ValueError(f"reading JSON is invalid: {exc}") from exc
    _require(isinstance(document, dict), "reading package must be a JSON object")
    return document


def _plain(value, name: str, maximum: int = 2000) -> str:
    _require(isinstance(value, str) and 0 < len(value.strip()) <= maximum, f"{name} must be nonempty bounded text")
    _require(not any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value), f"{name} must be plain text")
    return value


def _id(value, name: str) -> str:
    _require(isinstance(value, str) and len(value) <= 80 and ID.fullmatch(value) is not None, f"invalid {name}")
    return value


def _int(value, name: str, low: int, high: int) -> int:
    _require(type(value) is int and low <= value <= high, f"invalid {name}")
    return value


def _keys(value, name: str, allowed: set[str], required: set[str]) -> dict:
    _require(isinstance(value, dict), f"{name} must be an object")
    _require(None not in value.values(), f"{name} must omit empty optional fields instead of using null")
    unknown = set(value) - allowed
    missing = required - set(value)
    _require(not unknown, f"{name} has unknown fields: {', '.join(sorted(unknown))}")
    _require(not missing, f"{name} is missing: {', '.join(sorted(missing))}")
    return value


def _records(value, name: str, low: int, high: int) -> list[dict]:
    _require(isinstance(value, list) and low <= len(value) <= high and all(isinstance(item, dict) for item in value),
             f"invalid {name}")
    return value


def _strings(value, name: str, low: int, high: int) -> list[str]:
    _require(isinstance(value, list) and low <= len(value) <= high, f"invalid {name}")
    return [_plain(item, name, 1000) for item in value]


def _offset(value, name: str, limit: int) -> int:
    number = _int(value, name, 0, limit)
    return number


def _spans(section: dict, known_words: set[str] | None) -> None:
    text = _plain(section["text"], "section text", 2000)
    _require("<" not in text and ">" not in text and "](" not in text and "`" not in text,
             f"{section['id']}: section text must not contain markup")
    if "translation" in section:
        _plain(section["translation"], "section translation", 2000)
    vocabulary = section.get("vocabulary", [])
    spans = _records(vocabulary, f"{section['id']} vocabulary", 0, 128)
    cursor = 0
    for index, span in enumerate(spans):
        item = _keys(span, f"{section['id']} span {index}", SPAN_KEYS, SPAN_KEYS - {"word"})
        start = _offset(item["start"], "span start", len(text))
        end = _offset(item["end"], "span end", len(text))
        _require(cursor <= start < end, f"{section['id']}: overlapping or empty span at {start}")
        surface = text[start:end]
        _require(surface == item["text"], f"{section['id']}: span text does not match offsets")
        _plain(item["reading"], "span reading", 80)
        _plain(item["headword"], "span headword", 80)
        _plain(item["gloss"], "span gloss", 200)
        if "word" in item:
            word = _plain(item["word"], "span word", 80)
            _require("/" not in word and "\\" not in word, "span word must be a card id, not a path")
            if known_words is not None:
                _require(word in known_words, f"span word has no card: {word}")
        cursor = end


def _provenance(value: dict) -> None:
    item = _keys(value, "provenance", PROVENANCE_KEYS, PROVENANCE_KEYS - {"consulted"})
    _plain(item["originalTitle"], "provenance title", 200)
    adaptation = _keys(item["adaptation"], "adaptation", ADAPTATION_KEYS, ADAPTATION_KEYS)
    _plain(adaptation["label"], "adaptation label", 200)
    basis = adaptation["basis"]
    _require(basis in BASES, "invalid adaptation basis")
    consulted = item.get("consulted", [])
    records = _records(consulted, "consulted", 0, 8)
    _require(basis == "original" or records, "consulted sources are required unless the basis is original")
    roles = []
    for index, source in enumerate(records):
        fields = _keys(source, f"consulted {index}", CONSULT_KEYS, CONSULT_KEYS)
        _plain(fields["originalTitle"], "consulted title", 200)
        _plain(fields["author"], "consulted author", 200)
        _plain(fields["edition"], "consulted edition", 500)
        url = _plain(fields["sourceUrl"], "consulted URL", 500)
        _require(url.startswith("https://"), "consulted URL must be https")
        accessed = fields["accessed"]
        _require(isinstance(accessed, str) and DATE.fullmatch(accessed) is not None, "invalid consulted access date")
        _require(fields["role"] in ROLES, "invalid consulted role")
        roles.append(fields["role"])
    _require(basis != "original" or not records or "wording-source" not in roles,
             "an original package cannot use a consulted file as its wording source")
    rights = _keys(item["rights"], "rights", RIGHTS_KEYS, RIGHTS_KEYS)
    _require(rights["status"] == "original-wording", "only original-wording is accepted until another status is agreed")
    _plain(rights["note"], "rights note", 1000)
    _require("wording-source" not in roles, "original wording cannot cite a wording source")
    _require(basis != "public-domain-text", "public-domain-text needs an agreed rights status before use")
    _strings(item["credits"], "credits", 1, 8)
    distribution = _keys(item["distribution"], "distribution", DISTRIBUTION_KEYS, DISTRIBUTION_KEYS)
    reviewed = distribution["reviewed"]
    _require(isinstance(reviewed, list) and len(reviewed) <= 16, "invalid reviewed jurisdictions")
    for jurisdiction in reviewed:
        _plain(jurisdiction, "jurisdiction", 80)
    _plain(distribution["note"], "distribution note", 1000)


def _questions(document: dict, sections: dict[str, str]) -> list[int]:
    questions = _records(document["questions"], "questions", 1, 128)
    ids = [_id(question.get("id"), "question ID") for question in questions]
    _require(len(ids) == len(set(ids)), "duplicate question ID")
    tiers = []
    for question in questions:
        item = _keys(question, f"question {question.get('id')}", QUESTION_KEYS, QUESTION_KEYS - {"image"})
        tiers.append(_int(item["tier"], "question tier", 1, 4))
        prompt = _plain(item["prompt"], "prompt", 500)
        for quote in QUOTE.findall(prompt):
            _require(any(quote in text for text in sections.values()), "prompt quotes text that is not in the passage")
        options = _records(item["options"], "options", 2, 4)
        option_ids = []
        labels = []
        for option in options:
            fields = _keys(option, "option", OPTION_KEYS, OPTION_KEYS)
            option_ids.append(_id(fields["id"], "option ID"))
            labels.append(_plain(fields["text"], "option text", 300))
        _require(len(option_ids) == len(set(option_ids)), "duplicate option ID")
        _require(len(labels) == len(set(labels)), "duplicate option text")
        _require(item["correctOptionId"] in option_ids, "correctOptionId must reference an option in this question")
        _plain(item["explanation"], "explanation", 1000)
        evidence = _records(item["evidence"], "evidence", 1, 8)
        for span in evidence:
            fields = _keys(span, "evidence", EVIDENCE_KEYS, EVIDENCE_KEYS)
            section_id = _id(fields["sectionId"], "evidence section")
            _require(section_id in sections, "evidence section is missing")
            text = sections[section_id]
            start = _offset(fields["start"], "evidence start", len(text))
            end = _offset(fields["end"], "evidence end", len(text))
            _require(start < end and text[start:end].strip(), "evidence range is empty")
        if "image" in item:
            image = _keys(item["image"], "question image", IMAGE_KEYS, IMAGE_KEYS)
            _require(isinstance(image["path"], str) and IMAGE_PATH.fullmatch(image["path"]) is not None,
                     "invalid question image path")
            _require(isinstance(image["sha256"], str) and HASH.fullmatch(image["sha256"]) is not None,
                     "invalid question image hash")
            _plain(image["description"], "image description", 500)
    return tiers


def _literary(document: dict, tiers: list[int]) -> None:
    _require(document["jlpt"] == 5, "the current reading band accepts only N5")
    sections = document["sections"]
    _require(len(sections) == N5_SECTIONS, f"N5 reading passages use {N5_SECTIONS} sections")
    total = sum(len(section["text"]) for section in sections)
    _require(N5_MIN_CHARS <= total <= N5_MAX_CHARS, f"N5 passage length {total} is outside {N5_MIN_CHARS}-{N5_MAX_CHARS}")
    counts = {tier: tiers.count(tier) for tier in range(1, 5)}
    _require(all(counts[tier] >= N5_MIN_PER_TIER for tier in range(1, 5)),
             "N5 questions need at least four items in each tier")


def validate_document(document: dict, path: str, *, known_words: set[str] | None = None, literary: bool = False) -> None:
    """Validate one package. Literary mode enforces the current N5 authoring band."""
    package = _keys(document, "package", PACKAGE_KEYS, PACKAGE_KEYS)
    _require(package["schemaVersion"] == 1, "unsupported reading schema")
    package_id = _id(package["id"], "package ID")
    _require(Path(path).name == f"{package_id}.json", "package ID must match its filename")
    _require(path.startswith("reading/"), "reading packages live in reading/")
    _int(package["jlpt"], "jlpt", 1, 5)
    _plain(package["title"], "title", 200)
    _plain(package["japaneseTitle"], "japaneseTitle", 200)
    _plain(package["levelRationale"], "levelRationale", 2000)
    _provenance(package["provenance"])
    sections = _records(package["sections"], "sections", 1, 100)
    section_ids = []
    section_text = {}
    for section in sections:
        item = _keys(section, "section", SECTION_KEYS, SECTION_KEYS - {"translation", "vocabulary"})
        section_id = _id(item["id"], "section ID")
        section_ids.append(section_id)
        _spans(item, known_words)
        section_text[section_id] = item["text"]
    _require(len(section_ids) == len(set(section_ids)), "duplicate section ID")
    tiers = _questions(package, section_text)
    if literary:
        _literary(package, tiers)


def word_ids(root: Path) -> set[str]:
    return {path.stem for path in (root / "words").glob("*.md") if path.is_file()}


def check_reading(err, root: Path) -> None:
    known = word_ids(root)
    referenced = set()
    for path in sorted((root / "reading").glob("*.json")):
        relative = path.relative_to(root).as_posix()
        try:
            document = load_package(path)
            validate_document(document, relative, known_words=known, literary=True)
            for question in document["questions"]:
                if "image" in question:
                    image = root / question["image"]["path"]
                    _require(image.is_file(), "question image is missing")
                    digest = hashlib.sha256(image.read_bytes()).hexdigest()
                    _require(digest == question["image"]["sha256"], "question image hash does not match")
                    referenced.add(question["image"]["path"])
        except (ValueError, TypeError, KeyError, OSError) as exc:
            err(path, str(exc))
    image_root = root / "reading-images"
    if image_root.is_dir():
        for path in sorted(image_root.glob("*")):
            if path.is_file() and path.relative_to(root).as_posix() not in referenced:
                err(path, "reading image has no valid question reference")
