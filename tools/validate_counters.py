#!/usr/bin/env python3
"""Validate counters/*.json (counter-usage cards). Run by tools/validate.py; structure only, not Japanese accuracy.

Usage: python tools/validate_counters.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KANA = re.compile(r"^[ぁ-ゟァ-ヿー]+$")
CARD_KEYS = {"id", "kind", "text", "en", "noun", "phrase", "reading", "good", "kana", "hard", "distractors", "note"}
REQUIRED = ("id", "kind", "text", "en", "noun", "phrase", "reading", "good", "kana", "distractors")


def check_counters(err) -> int:
    """Reports problems through err(path, message); returns the number of counter files read."""
    files = sorted((ROOT / "counters").glob("*.json"))
    cards: dict[str, dict] = {}
    accepted: dict[str, set[str]] = {}
    reverse: list[tuple[Path, dict, str]] = []
    reverse_ids: set[str] = set()
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            err(path, f"not valid JSON: {exc}")
            continue
        if not isinstance(data, dict):
            err(path, "must be a JSON object")
            continue
        if data.get("schemaVersion") != 1:
            err(path, "'schemaVersion' must be 1")
        if data.get("id") != path.stem:
            err(path, "'id' must equal the file name")
        counter = data.get("counter")
        if not isinstance(counter, str) or not counter:
            err(path, "missing 'counter'")
            continue
        if not isinstance(data.get("reading"), str) or not KANA.match(data["reading"]):
            err(path, "'reading' must be kana")
        if not isinstance(data.get("title"), str) or not data["title"]:
            err(path, "missing 'title'")
        if data.get("level") not in (1, 2, 3, 4, 5):
            err(path, "'level' must be 1-5")
        if not all(isinstance(s, str) and s.startswith("https://") for s in data.get("sources", [])):
            err(path, "'sources' must list https URLs")
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
    return len(files)


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
