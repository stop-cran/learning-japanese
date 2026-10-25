#!/usr/bin/env python3
"""Validate counters/*.json (counter-usage cards). Run by tools/validate.py; structure only, not Japanese accuracy.

Usage: python tools/validate_counters.py
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KANA = re.compile(r"^[ぁ-ゟァ-ヿー]+$")
CARD_KEYS = {"id", "kind", "text", "en", "noun", "phrase", "reading", "good", "kana", "hard", "distractors", "note", "readingAnswers"}
REQUIRED = ("id", "kind", "text", "en", "noun", "phrase", "reading", "good", "kana", "distractors")


def check_counters(err, root: Path = ROOT) -> int:
    """Reports problems through err(path, message); returns the number of counter files read."""
    files = sorted((root / "counters").glob("*.json"))
    cards: dict[str, dict] = {}
    accepted: dict[str, set[str]] = {}
    reverse: list[tuple[Path, dict, str]] = []
    reverse_ids: set[str] = set()
    expression_ids: set[str] = set()
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
            err(path, f"not valid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            err(path, "must be a JSON object")
            continue
        if type(data.get("schemaVersion")) is not int or data["schemaVersion"] not in (1, 2):
            err(path, "'schemaVersion' must be 1 or 2")
            continue
        if data.get("group", "everyday") not in ("everyday", "time"):
            err(path, "'group' must be everyday or time")
        article = data.get("article")
        if article is not None and (
                not isinstance(article, str) or not re.fullmatch(r"articles/[a-z0-9-]+\.md", article)
                or not (root / article).is_file()):
            err(path, "'article' must reference an existing article")
        if data.get("id") != path.stem:
            err(path, "'id' must equal the file name")
        counter = data.get("counter")
        if not isinstance(counter, str) or not counter.strip():
            err(path, "missing 'counter'")
            continue
        if not isinstance(data.get("reading"), str) or not KANA.match(data["reading"]):
            err(path, "'reading' must be kana")
        if not isinstance(data.get("title"), str) or not data["title"].strip():
            err(path, "missing 'title'")
        if type(data.get("level")) is not int or data["level"] not in (1, 2, 3, 4, 5):
            err(path, "'level' must be 1-5")
        sources = data.get("sources", [])
        if not isinstance(sources, list) or not all(isinstance(s, str) and s.startswith("https://") for s in sources):
            err(path, "'sources' must list https URLs")
        if data["schemaVersion"] == 2:
            check_expressions(path, data, expression_ids, err)
            continue
        if data.get("expressions"):
            err(path, "whole expressions require schema 2")
        for word, support in (data.get("vocabulary") or {}).items():
            if not isinstance(support, dict) or not KANA.match(str(support.get("reading", ""))) or not support.get("gloss"):
                err(path, f"vocabulary '{word}' needs a kana reading and a gloss")
        group = data.get("cards")
        if not isinstance(group, list) or not group:
            err(path, "'cards' must be a non-empty list")
            continue
        for card in group:
            check_card(path, counter, card, cards, accepted, err)
        for item in data.get("reverse", []):
            reverse.append((path, item, counter))
    for path, item, counter in reverse:
        check_reverse(path, item, counter, cards, accepted, reverse_ids, err)
    for key in expression_ids & (set(cards) | reverse_ids):
        err(root / "counters", f"expression ID '{key}' collides with a legacy card")
    return len(files)

def answer_key(value, reading=False):
    value = "".join(c for c in unicodedata.normalize("NFKC", value) if not c.isspace() or c == "\x85")
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in value) if reading else value


def check_readings(path, key, canonical, answers, err):
    if (not isinstance(answers, list) or not 1 <= len(answers) <= 8 or canonical not in answers
            or any(not isinstance(a, str) or len(a) > 80 or not KANA.fullmatch(a) for a in answers)):
        err(path, f"{key}: invalid canonical-expression readings")
    elif len({answer_key(a, True) for a in answers}) != len(answers):
        err(path, f"{key}: duplicate reading answers")


def check_expressions(path, data, seen, err):
    if not {"schemaVersion", "id", "counter", "reading", "title", "level", "group", "article", "expressions"} <= data.keys():
        err(path, "incomplete expression file")
    allowed = {"schemaVersion", "id", "counter", "reading", "title", "level", "sources",
               "cards", "reverse", "vocabulary", "group", "article", "expressions"}
    if set(data) - allowed:
        err(path, f"unknown v2 fields: {sorted(set(data) - allowed)}")
    for key in ("cards", "reverse"):
        if key in data and (not isinstance(data[key], list) or data[key]):
            err(path, f"v2 '{key}' must be an empty array when supplied")
    vocabulary = data.get("vocabulary", {})
    if not isinstance(vocabulary, dict) or any(
            not isinstance(word, dict) or set(word) - {"reading", "gloss"}
            or any(not isinstance(value, str) for value in word.values())
            for word in vocabulary.values()):
        err(path, "v2 vocabulary must map names to reading/gloss string objects")
    items = data.get("expressions")
    if data.get("cards") or data.get("reverse") or not isinstance(items, list) or not 1 <= len(items) <= 256:
        err(path, "v2 needs 1-256 expressions, not suffix or reverse cards")
        return
    if not data.get("article"):
        err(path, "v2 expressions need an article")
    required = {"id", "cue", "written", "writtenAnswers", "reading", "readingAnswers", "explanation"}
    for item in items:
        if not isinstance(item, dict) or set(item) != required:
            err(path, "expression needs exactly the documented fields")
            continue
        key = item["id"]
        if not isinstance(key, str) or not re.fullmatch(r"[a-z]+-[a-z]+-\d+", key):
            err(path, "invalid expression ID")
            continue
        if key in seen:
            err(path, f"{key}: duplicate expression ID")
        seen.add(key)
        if any(not isinstance(item[k], str) or not item[k].strip() or len(item[k]) > 1000
               for k in ("cue", "written", "explanation")):
            err(path, f"{key}: incomplete or oversized expression")
        forms = item["writtenAnswers"]
        if (not isinstance(forms, list) or not 1 <= len(forms) <= 16 or item["written"] not in forms
                or any(not isinstance(a, str) or not a.strip() or len(a) > 80 for a in forms)):
            err(path, f"{key}: invalid written answers")
        elif len({answer_key(a) for a in forms}) != len(forms):
            err(path, f"{key}: duplicate written answers")
        check_readings(path, key, item["reading"], item["readingAnswers"], err)


def check_card(path, counter, card, cards, accepted, err) -> None:
    if not isinstance(card, dict) or any(k not in card for k in REQUIRED):
        err(path, f"card needs {', '.join(REQUIRED)}")
        return
    key = card["id"]
    if set(card) - CARD_KEYS:
        err(path, f"{key}: unknown fields {sorted(set(card) - CARD_KEYS)}")
    if not isinstance(key, str) or not re.fullmatch(r"[a-z]+-[a-z]+-\d+", key):
        err(path, f"{key}: id must look like hon-pen-1")
        return
    if key in cards:
        err(path, f"{key}: duplicate card ID")
        return
    for field in ("kind", "text", "en", "noun", "phrase", "reading"):
        if not isinstance(card[field], str) or not card[field].strip():
            err(path, f"{key}: empty '{field}'")
    if card["text"].count("{}") != 1:
        err(path, f"{key}: text needs exactly one {{}} blank")
    elif card["phrase"] not in card["text"].replace("{}", counter):
        err(path, f"{key}: phrase is not in the sentence completed with the counter")
    good, kana = list(card["good"]), list(card["kana"])
    if len(set(good)) != len(good) or len(set(kana)) != len(kana):
        err(path, f"{key}: repeated accepted form")
    if set(good) & set(kana):
        err(path, f"{key}: form listed as both good and kana")
    if counter not in good or card["phrase"] not in good:
        err(path, f"{key}: 'good' must include the counter and the complete phrase")
    if card["reading"] not in good + kana:
        err(path, f"{key}: the phrase reading must be an accepted form")
    for form in kana:
        if not KANA.match(form):
            err(path, f"{key}: kana form '{form}' is not kana")
    if not KANA.match(card["reading"]):
        err(path, f"{key}: reading is not kana")
    if "readingAnswers" in card and not isinstance(card["readingAnswers"], list):
        err(path, f"{key}: readingAnswers must be an array")
    elif card.get("readingAnswers"):
        check_readings(path, key, card["reading"], card["readingAnswers"], err)
    forms = set(good) | set(kana)
    for variant in card.get("hard", []):
        v_forms = variant.get("forms", [])
        if not variant.get("reason") or variant.get("phrase") not in v_forms or variant.get("reading") not in v_forms:
            err(path, f"{key}: yellow variant needs forms including its phrase and reading, and a reason")
        if forms & set(v_forms):
            err(path, f"{key}: yellow variant repeats another tier's form")
        forms |= set(v_forms)
    wrong = card["distractors"]
    if len(wrong) != 3 or len(set(wrong)) != 3:
        err(path, f"{key}: needs three distinct distractors")
    if forms & set(wrong):
        err(path, f"{key}: a distractor is an accepted answer")
    cards[key] = card
    accepted[key] = forms


def check_reverse(path, item, counter, cards, accepted, reverse_ids, err) -> None:
    key = item.get("id")
    if not isinstance(key, str) or key in reverse_ids or key in cards:
        err(path, f"reverse '{key}': missing or duplicate ID")
        return
    reverse_ids.add(key)
    options = item.get("options", [])
    if len(options) != 4 or len(set(options)) != 4 or item.get("answer") not in options:
        err(path, f"{key}: needs four distinct options including the answer")
        return
    unknown = [o for o in options if o not in cards]
    if unknown:
        err(path, f"{key}: unknown option cards {unknown}")
        return
    matches = [o for o in options if counter in accepted[o]]
    if matches != [item["answer"]]:
        err(path, f"{key}: expected exactly the answer to accept {counter}, got {matches}")


def main() -> int:
    problems: list[str] = []
    count = check_counters(lambda p, m: problems.append(f"{p.relative_to(ROOT).as_posix()}: {m}"))
    for message in problems:
        print(message)
    print(f"{count} counter file(s), {len(problems)} error(s); Japanese accuracy is not validated")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
