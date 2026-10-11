#!/usr/bin/env python3
"""Check the N5 counter draft's structure; not Japanese accuracy or live app schema."""
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent


def validate(data):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    groups = data["counters"]
    rows = [card for group in groups for card in group["cards"]]
    cards = {card["id"]: card for card in rows}
    check(len(groups) == 10, "expected ten counter groups")
    check(len(rows) == 120, "expected 120 forward cards")
    check(len(cards) == len(rows), "duplicate forward ID")
    check(len({g["id"] for g in groups}) == len(groups), "duplicate counter ID")
    check(len({c["text"] for c in rows}) == len(rows), "duplicate prompt")
    hard = data.get("hard_variants", {})
    check(set(hard) <= set(cards), "yellow variants reference unknown cards")
    accepted = {}
    for group in groups:
        check(len(group["cards"]) == 12, f"{group['id']}: expected twelve cards")
        check(set(group["sources"]) <= set(data["sources"]), f"{group['id']}: unknown source")
        for card in group["cards"]:
            key = card["id"]
            check(card["text"].count("{}") == 1, f"{key}: expected one blank")
            completed = card["text"].replace("{}", group["counter"])
            check(card["phrase"] in completed, f"{key}: phrase does not match completed prompt")
            check(not re.search(r"[0-9０-９]", card["text"]), f"{key}: expected kanji numerals")
            for field in ("en", "noun", "kind", "phrase", "reading"):
                check(bool(card[field]), f"{key}: empty {field}")
            good = set(card["good"])
            kana = set(card["kana"])
            check(len(good) == len(card["good"]), f"{key}: duplicate green variant")
            check(len(kana) == len(card["kana"]), f"{key}: duplicate kana variant")
            check(not good & kana, f"{key}: variant in conflicting tiers")
            check(group["counter"] in good and card["phrase"] in good, f"{key}: missing canonical answer")
            check(card["reading"] in good | kana, f"{key}: missing canonical reading")
            forms = good | kana
            for variant in hard.get(key, []):
                check(bool(variant["reason"]), f"{key}: yellow answer needs explanation")
                check(variant["phrase"] in variant["forms"], f"{key}: yellow phrase not accepted")
                check(variant["reading"] in variant["forms"], f"{key}: yellow reading not accepted")
                check(not forms & set(variant["forms"]), f"{key}: conflicting yellow variants")
                forms.update(variant["forms"])
            wrong = card["distractors"]
            check(len(wrong) == len(set(wrong)) == 3, f"{key}: expected three distinct distractors")
            check(not forms & set(wrong), f"{key}: accepted answer used as distractor")
            accepted[key] = forms
    reverse = data["reverse_cards"]
    check(len(reverse) == 20, "expected twenty reverse cards")
    reverse_ids = {card["id"] for card in reverse}
    check(len(reverse_ids) == len(reverse), "duplicate reverse ID")
    check(not reverse_ids & set(cards), "forward/reverse ID collision")
    for card in reverse:
        key = card["id"]
        options = card["options"]
        check(len(options) == len(set(options)) == 4, f"{key}: expected four distinct options")
        check(set(options) <= set(cards), f"{key}: unknown option card")
        matches = [option for option in options if card["counter"] in accepted.get(option, set())]
        check(matches == [card["answer"]], f"{key}: reverse answer is ambiguous or incompatible")
    for word, support in data.get("vocabulary", {}).items():
        check(bool(support["reading"]) and bool(support["gloss"]), f"{word}: incomplete vocabulary support")
    return errors


def main():
    data = yaml.safe_load((ROOT / "docs" / "counter-n5.yaml").read_text(encoding="utf-8"))
    errors = validate(data)
    for error in errors:
        print(error)
    print(f"Counter draft: {len(errors)} structural error(s); language accuracy is not validated.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
