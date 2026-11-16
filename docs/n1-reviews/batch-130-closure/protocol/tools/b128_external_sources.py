"""Neutral text extraction for the actual sources cited by B128."""
import html
import re
from urllib.parse import urlsplit

from weblio_sections import extract as extract_weblio

METHOD = (
    "B128 neutral source extraction v1: Weblio uses the unchanged complete named-section extractor. "
    "Kanjipedia and Kotobank retain the complete HTML body, not selected dictionary passages; require "
    "one body and a matching character title, remove scripts/styles/comments, retain image alt text "
    "as labelled text, map block boundaries to LF, strip other tags, unescape entities and omit blank "
    "lines. Inline text stays concatenated. No author rationale is added. HTML layout and images "
    "are not visually verified; original responses remain available locally."
)
BLOCK = re.compile(r"<(?:br\b[^>]*|/(?:p|div|li|h[1-6]|tr|table|dt|dd|section|article|ul|ol|dl)\s*)>", re.I)


def extract(raw, url, expected_characters):
    host = urlsplit(url).hostname
    if host in {"weblio.jp", "www.weblio.jp"}:
        return extract_weblio(raw)
    if host not in {"www.kanjipedia.jp", "kanjipedia.jp", "kotobank.jp"}:
        return None, f"Unsupported cited-source host: {host}"
    if not expected_characters or any(not isinstance(char, str) or len(char) != 1
                                      for char in expected_characters):
        return None, "Expected at least one single-character source identity"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        return None, f"Source is not strict UTF-8: {error}"
    titles = re.findall(r"<title\b[^>]*>(.*?)</title\s*>", text, re.I | re.S)
    bodies = re.findall(r"<body\b[^>]*>(.*?)</body\s*>", text, re.I | re.S)
    label = "\u6f22\u5b57\u30da\u30c7\u30a3\u30a2" if "kanjipedia" in host else "\u30b3\u30c8\u30d0\u30f3\u30af"
    if len(titles) != 1 or len(bodies) != 1 or not any(char in html.unescape(titles[0]) for char in expected_characters) or label not in titles[0]:
        return None, "Expected one complete body and one matching character/source title"
    body = re.sub(r"<(script|style)\b[^>]*>.*?</\1\s*>", "", bodies[0], flags=re.I | re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

    def image(match):
        alt = re.search(r"\balt\s*=\s*([\"'])(.*?)\1", match[0], re.I | re.S)
        return "[image alt: " + alt[2] + "]" if alt and alt[2] else "[image without alt text]"

    body = re.sub(r"<img\b[^>]*>", image, body, flags=re.I)
    body = re.sub(r"[ \t\r\n\f]+", " ", body)
    body = BLOCK.sub("\n", body)
    body = re.sub(r"<[^>]*>", "", body)
    body = html.unescape(body)
    lines = [line.strip(" ") for line in body.split("\n") if line.strip(" ")]
    if not lines:
        return None, "Source body contains no text"
    return f"Source: {label}\nURL: {url}\n" + "\n".join(lines) + "\n", None
