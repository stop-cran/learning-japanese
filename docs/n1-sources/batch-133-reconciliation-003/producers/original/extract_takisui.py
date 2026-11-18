"""Extract complete named publisher sections from the frozen Kotobank 滝水 capture."""
import hashlib
import html
import json
import pathlib
import re

D = pathlib.Path(__file__).resolve().parent
CAPTURE = D / "takisui-kotobank.html"
EXPECTED = "5100a307551e7d6bf0f92665c5783cdd010fe85c6a49b9cbdc618af3d440099f"


def text_lines(fragment):
    s = re.sub(r"<(script|style)\b.*?</\1>", "", fragment, flags=re.S)
    s = re.sub(r"<br\s*/?>|</(p|li|h\d|div|section|dt|dd|ol|ul)>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    lines = [re.sub(r"[ \t\u3000]+", " ", x).strip() for x in s.splitlines()]
    return [x for x in lines if x]


def main():
    raw = CAPTURE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED:
        raise SystemExit(f"capture hash mismatch: {digest}")
    articles = re.findall(r"<article\b.*?</article>", raw.decode("utf-8"), flags=re.S)
    sections = []
    for index, article in enumerate(articles, 1):
        lines = text_lines(article)
        sections.append({"index": index, "title": lines[0] if lines else "", "lines": lines})
    out = D / "takisui-sections.txt"
    body = []
    for section in sections:
        body.append(f"=== article {section['index']}")
        body.extend(section["lines"])
    out.write_text("\n".join(body) + "\n", encoding="utf-8", newline="\n")
    receipt = {
        "capture": CAPTURE.name,
        "captureSha256": digest,
        "url": "https://kotobank.jp/word/%E6%BB%9D%E6%B0%B4-1447140",
        "articles": len(sections),
        "output": out.name,
        "outputSha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }
    (D / "takisui-sections.receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
