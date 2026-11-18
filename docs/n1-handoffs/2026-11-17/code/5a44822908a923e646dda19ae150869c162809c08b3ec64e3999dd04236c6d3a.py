"""Exactly invertible compact line encoding for record-oriented dictionary XML.

The encoded text is self-describing: its header declares the root element, the
record element, the newline count between records, element aliases (tag plus
exact ordered attributes) and bare first children. ``decode`` rebuilds the
original XML bytes without consulting the original; ``encode`` refuses any
input whose decoded form is not byte-identical to that input.
"""
import hashlib
import re
from xml.etree import ElementTree

MAGIC = "COMPACT-XML-V1"
RECORD_SEP = " ¦ "
ITEM_SEP = " | "
NAME = re.compile(r"[A-Za-z_#][A-Za-z0-9_:.-]*\Z")
FORBIDDEN = ("\n", "\r", "\t", "|", "¦", "{", "}", "&", "<")
ATTR_FORBIDDEN = FORBIDDEN + ("[", "]", "=", ",", '"', ">")
XML_NS = "{http://www.w3.org/XML/1998/namespace}"


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _attr_name(key):
    return "xml:" + key[len(XML_NS):] if key.startswith(XML_NS) else key


def _check_value(value, what):
    _require(not any(token in value for token in FORBIDDEN), f"Unencodable character in {what}: {value!r}")
    _require(value == value.strip(" "), f"Surrounding spaces in {what}: {value!r}")


def _signature(element):
    return element.tag, tuple((_attr_name(k), v) for k, v in element.attrib.items())


def _parse_alias(text):
    short, _, full = text.partition("=")
    tag, _, rest = full.partition("[")
    attrs = ()
    if rest:
        _require(rest.endswith("]"), f"Bad alias: {text}")
        attrs = tuple(tuple(pair.split("=", 1)) for pair in rest[:-1].split(","))
    _require(NAME.match(short) and NAME.match(tag) and all(len(a) == 2 for a in attrs), f"Bad alias: {text}")
    return short, (tag, attrs)


def _format_attrs(attrs):
    return "[" + ",".join(f"{k}={v}" for k, v in attrs) + "]" if attrs else ""


def encode(original, *, root, record, separator, aliases, bare):
    """Encode original XML bytes. aliases: list of 'short=tag[attr=value,...]'; bare: {parent: child}."""
    text = original.decode("utf-8")
    _require(b"\r" not in original and "&" not in text, "Unsupported line endings or XML references")
    alias_map = dict(_parse_alias(a) for a in aliases)
    _require(len(set(alias_map.values())) == len(alias_map), "Aliases must be one-to-one")
    by_signature = {sig: short for short, sig in alias_map.items()}
    _require(not set(alias_map) & {sig[0] for sig in alias_map.values()}, "Alias collides with a tag")
    tree = ElementTree.fromstring(original)
    _require(tree.tag == root and not tree.attrib, "Unexpected root")

    def item(element, depth):
        sig = _signature(element)
        _require(not element.tail or element.tail.strip() == "" and depth == 0, "Unexpected tail text")
        for key, value in sig[1]:
            _require(not any(token in value for token in ATTR_FORBIDDEN) and value == value.strip(),
                     f"Unencodable attribute value {value!r}")
        name = by_signature.get(sig)
        if name is None:
            _require(sig[0] not in alias_map and NAME.match(sig[0]), f"Unencodable tag {sig[0]}")
            name = sig[0] + _format_attrs(sig[1])
        children = list(element)
        if not children:
            value = element.text or ""
            _check_value(value, element.tag)
            return f"{name}={value}"
        _require(element.text is None, f"Mixed content in {element.tag}")
        parts = []
        for index, child in enumerate(children):
            _require(child.tail is None, f"Unexpected whitespace in {element.tag}")
            if index == 0 and bare.get(element.tag) == child.tag:
                _require(not child.attrib and not list(child) and child.text, f"Bad bare child {child.tag}")
                _check_value(child.text, child.tag)
                _require("=" not in child.text, "Bare value contains '='")
                parts.append(child.text)
            else:
                parts.append(item(child, depth + 1))
        if depth == 0:
            return name + " " + ITEM_SEP.join(parts)
        return name + "{" + ITEM_SEP.join(parts) + "}"

    lines = []
    for rec in tree:
        _require(rec.tag == record and not rec.attrib and rec.text is None, "Unexpected record element")
        fields = []
        for index, child in enumerate(rec):
            _require(child.tail is None, "Unexpected whitespace in record")
            if index == 0 and bare.get(record) == child.tag:
                _require(not child.attrib and not list(child) and child.text, "Bad bare record child")
                _check_value(child.text, child.tag)
                _require("=" not in child.text and " " not in child.text, "Bare record value is ambiguous")
                fields.append(child.text)
            else:
                fields.append(item(child, 0))
        lines.append(RECORD_SEP.join(fields))
    header = [MAGIC, f"%root {root}", f"%record {record}", f"%separator {separator}",
              f"%source-sha256 {_sha(original)}", f"%source-bytes {len(original)}"]
    header += [f"%alias {a}" for a in aliases]
    header += [f"%bare {parent}={child}" for parent, child in bare.items()]
    header.append("%end")
    encoded = ("\n".join(header + lines) + "\n").encode("utf-8")
    _require(decode(encoded) == original, "Encoding is not byte-exactly invertible")
    return encoded


def _split(text):
    parts, depth, start, index = [], 0, 0, 0
    while index < len(text):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            _require(depth >= 0, "Unbalanced braces")
        elif depth == 0 and text.startswith(ITEM_SEP, index):
            parts.append(text[start:index])
            index += len(ITEM_SEP)
            start = index
            continue
        index += 1
    _require(depth == 0, "Unbalanced braces")
    parts.append(text[start:])
    return parts


def decode(encoded):
    lines = encoded.decode("utf-8").split("\n")
    _require(lines[0] == MAGIC and lines[-1] == "", "Not compact-xml-v1")
    meta, aliases, bare, index = {}, {}, {}, 1
    while lines[index] != "%end":
        key, _, value = lines[index].partition(" ")
        if key == "%alias":
            short, sig = _parse_alias(value)
            _require(short not in aliases, "Duplicate alias")
            aliases[short] = sig
        elif key == "%bare":
            parent, _, child = value.partition("=")
            bare[parent] = child
        else:
            _require(key[1:] not in meta, "Duplicate header")
            meta[key[1:]] = value
        index += 1
    records = lines[index + 1:-1]

    def open_tag(name):
        if name in aliases:
            tag, attrs = aliases[name]
        else:
            tag, _, rest = name.partition("[")
            attrs = ()
            if rest:
                _require(rest.endswith("]"), f"Bad element head {name}")
                attrs = tuple(tuple(p.split("=", 1)) for p in rest[:-1].split(","))
        _require(NAME.match(tag), f"Bad tag {tag}")
        return tag, "<" + tag + "".join(f' {k}="{v}"' for k, v in attrs) + ">"

    def element(text, depth):
        match = re.match(r"[^\[{= ]+(\[[^\]]*\])?", text)
        _require(match and match.end() < len(text), f"Bad item {text!r}")
        at = match.end()
        tag, opening = open_tag(text[:at])
        marker = text[at]
        _require(marker in ("=", "{") or marker == " " and depth == 0, f"Bad item {text!r}")
        if marker == "=":
            body = text[at + 1:]
        else:
            if marker == "{":
                _require(text.endswith("}"), f"Bad nested item {text!r}")
                inner = text[at + 1:-1]
            else:
                inner = text[at + 1:]
            body = children(_split(inner), tag, depth + 1)
        return f"{opening}{body}</{tag}>"

    def children(parts, parent, depth):
        out = []
        for i, part in enumerate(parts):
            if i == 0 and parent in bare:
                out.append(f"<{bare[parent]}>{part}</{bare[parent]}>")
            else:
                out.append(element(part, depth))
        return "".join(out)

    record = meta["record"]
    body = []
    for line in records:
        fields = line.split(RECORD_SEP)
        out = []
        for i, field in enumerate(fields):
            if i == 0 and record in bare:
                out.append(f"<{bare[record]}>{field}</{bare[record]}>")
            else:
                out.append(element(field, 0))
        body.append(f"<{record}>" + "".join(out) + f"</{record}>")
    newline = "\n" * int(meta["separator"])
    root = meta["root"]
    result = (f"<{root}>\n" + newline.join(body) + f"{newline}</{root}>\n").encode("utf-8")
    _require(len(result) == int(meta["source-bytes"]) and _sha(result) == meta["source-sha256"],
             "Decoded bytes do not match the declared source")
    return result
