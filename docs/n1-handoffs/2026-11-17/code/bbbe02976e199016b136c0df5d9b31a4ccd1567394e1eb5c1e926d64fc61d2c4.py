"""Retain URL-headword checking and support the actually cited Kanjipedia page."""
from pathlib import PurePosixPath
from urllib.parse import urlsplit

from b128_external_sources import extract
from b129_external_sources import METHOD as PRIOR_METHOD, extract_capture as prior_extract

METHOD = ("B130: retain URL-derived Weblio/Kotobank headwords. For numeric Kanjipedia URLs, "
          "require one cited card identity and verify it against the captured title, then use "
          "the unchanged complete-body extractor. " + PRIOR_METHOD)


def extract_capture(raw, capture):
    host = urlsplit(capture["requestUrl"]).hostname
    if host not in {"kanjipedia.jp", "www.kanjipedia.jp"}:
        return prior_extract(raw, capture)
    cards = capture["citedBy"]
    characters = {PurePosixPath(item["card"]).stem for item in cards}
    if (len(characters) != 1 or any(len(char) != 1 for char in characters)
            or any(PurePosixPath(item["card"]).parent.as_posix() != "snapshot/kanji"
                   or PurePosixPath(item["card"]).suffix != ".md" for item in cards)):
        return None, "Kanjipedia capture needs one actual cited card identity"
    return extract(raw, capture["finalUrl"], sorted(characters))
