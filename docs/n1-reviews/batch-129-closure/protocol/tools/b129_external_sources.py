"""Use the cited URL's character identity, including cross-card comparisons."""
from urllib.parse import unquote, urlsplit

from b128_external_sources import METHOD as ORIGINAL_METHOD, extract

METHOD = ("B129 source identity: use the single-character headword from the exact captured "
          "request URL, not the character of the citing card. " + ORIGINAL_METHOD)


def extract_capture(raw, capture):
    parts = urlsplit(capture["requestUrl"])
    prefix = "/word/" if parts.hostname == "kotobank.jp" else "/content/"
    if parts.hostname not in {"kotobank.jp", "www.weblio.jp", "weblio.jp"}:
        return None, "Unsupported B129 captured-source host"
    path = unquote(parts.path)
    if not path.startswith(prefix) or len(path.removeprefix(prefix)) != 1:
        return None, "Captured URL does not identify one character headword"
    character = path.removeprefix(prefix)
    return extract(raw, capture["finalUrl"], [character])
