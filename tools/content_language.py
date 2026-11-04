"""Repository-wide teaching language and localized authoring headings."""
import json
from pathlib import Path

HEADINGS = {
    "en": {
        "kanji": ["Meaning and origin", "Readings", "Common words", "Notes"],
        "words": ["Meaning", "How the kanji combine", "Synonyms and antonyms", "Distinctive meaning"],
        "facts": (r"\bStrokes:", r"\bKey\s*\(radical\):", r"\bJLPT:"),
    },
    "ru": {
        "kanji": ["Значение и происхождение", "Чтения", "Частые слова", "Примечания"],
        "words": ["Значение", "Как сочетаются кандзи", "Синонимы и антонимы", "Оттенки значения"],
        "facts": (r"\bЧерты:", r"\bКлюч\s*\(радикал\):", r"\bJLPT:"),
    },
}


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"content-language.json: duplicate field {key}")
        result[key] = value
    return result


def read_language(root: Path) -> dict[str, str]:
    path = root / "content-language.json"
    if not path.exists():
        return {"baseLanguage": "en", "targetLanguage": "ja"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError(f"content-language.json: invalid JSON: {exc}") from exc
    if (not isinstance(data, dict) or set(data) != {"baseLanguage", "targetLanguage"}
            or not isinstance(data.get("baseLanguage"), str)
            or data["baseLanguage"] not in HEADINGS or data.get("targetLanguage") != "ja"):
        raise ValueError("content-language.json: expected baseLanguage en/ru and targetLanguage ja only")
    return data
