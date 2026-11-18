"""Bounded review presentations; original source bytes remain immutable."""
import json
import html
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from common import require, sha

DICTIONARIES = {"daijisen", "nikkokuseisen", "jitsu"}


def canonical(raw):
    return ET.canonicalize(raw.decode("utf-8"), strip_text=True)


def compact_xml(raw):
    root = ET.fromstring(raw)
    require(not root.attrib and not (root.text or "").strip(), "Unexpected root metadata")
    text = "<" + root.tag + ">\n" + "\n".join(
        ET.canonicalize(ET.tostring(child, encoding="unicode"), strip_text=True)
        for child in root) + "\n</" + root.tag + ">\n"
    result = text.encode("utf-8")
    require(canonical(result) == canonical(raw), "XML content changed")
    return result


def kd_projection(raw):
    root = ET.fromstring(raw)
    omitted = {}
    for node in root.findall("character"):
        character = node.findtext("literal")
        omitted[character] = []
        for child in list(node):
            if child.tag not in {"literal", "misc", "reading_meaning"}:
                omitted[character].append(child.tag)
                node.remove(child)
        for group in node.findall("reading_meaning/rmgroup"):
            for child in list(group):
                if child.tag == "meaning" and child.get("m_lang") not in (None, "en"):
                    omitted[character].append("meaning:" + child.get("m_lang"))
                    group.remove(child)
    return compact_xml(ET.tostring(root, encoding="utf-8")), omitted


class ArticleSpans(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text, self.rows, self.active = text, [], None
        self.starts = [0]
        self.starts.extend(match.end() for match in re.finditer("\n", text))

    def absolute_position(self):
        line, column = self.getpos()
        return self.starts[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            require(self.active is None, "Nested source articles are ambiguous")
            self.active = (dict(attrs), self.absolute_position())

    def handle_endtag(self, tag):
        if tag == "article":
            require(self.active is not None, "Unmatched article end")
            attrs, start = self.active
            end = self.text.index(">", self.absolute_position()) + 1
            self.rows.append((attrs, start, end))
            self.active = None


class ArticleText(HTMLParser):
    BLOCKS = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6",
              "tr", "table", "dt", "dd", "section", "article", "ul", "ol", "dl"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.ignored = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.ignored += 1
        if not self.ignored:
            if tag == "img":
                alt = dict(attrs).get("alt")
                self.parts.append("[image alt: " + alt + "]" if alt else "[image without alt text]")
            elif tag == "br":
                self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            require(self.ignored > 0, "Unmatched ignored element")
            self.ignored -= 1
        if not self.ignored and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.ignored:
            self.parts.append(re.sub(r"[ \t\r\n\f]+", " ", data))

    def result(self):
        require(not self.ignored, "Incomplete ignored element")
        lines = [line.strip() for line in "".join(self.parts).split("\n") if line.strip()]
        require(lines, "Empty article text")
        return "\n".join(lines) + "\n"


def lexical_articles(raw, url, character):
    text = raw.decode("utf-8")
    titles = re.findall(r"<title\b[^>]*>.*?</title\s*>", text, re.I | re.S)
    require(len(titles) == 1 and character in html.unescape(titles[0])
            and "\u30b3\u30c8\u30d0\u30f3\u30af" in titles[0], "Ambiguous source title")
    parser = ArticleSpans(text)
    parser.feed(text)
    parser.close()
    require(parser.active is None, "Incomplete final article")
    records, omitted = [], []
    seen = set()
    for attrs, start, end in parser.rows:
        identity = (attrs.get("id"), attrs.get("class"))
        require(identity not in seen, "Duplicate article locator")
        seen.add(identity)
        if not (set((attrs.get("class") or "").split()) & DICTIONARIES):
            omitted.append({"id": identity[0], "class": identity[1]})
            continue
        article = text[start:end]
        renderer = ArticleText()
        renderer.feed(article)
        renderer.close()
        body = "Source: \u30b3\u30c8\u30d0\u30f3\u30af\nURL: " + url + "\n" + renderer.result()
        records.append({
            "id": identity[0], "class": identity[1],
            "rawCharacterStart": start, "rawCharacterEnd": end,
            "rawArticleSha256": sha(article.encode("utf-8")), "text": body,
        })
    require(records, "No complete lexical dictionary articles")
    return records, omitted


def pair_projection(raw):
    table = json.loads(raw)
    for row in table["rows"]:
        row["completeJmdictFamilyIds"] = list(row.pop("completeJmdictFamilies"))
        row["comparison"].pop("rawSha256")
        row["sourceEvidence"].pop("rawCaptureSha256")
        row["sourceEvidence"].pop("completeSelectedTextSha256")
    table["presentation"] = (
        "All semantic fields, exact source locators, full excerpts and family IDs retained. "
        "Repeated hashes/file lists are in the immutable verified signed table, not repeated here.")
    return table


def named_section(raw, label):
    text = raw.decode("utf-8")
    marker = "Weblio source section: " + label
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == marker]
    require(len(starts) == 1, "Named complete source section absent or ambiguous")
    start = starts[0]
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("Weblio source section: ")), len(lines))
    require(end > start + 1, "Empty source section")
    return "".join(lines[start:end]).encode("utf-8"), [start + 1, end]
