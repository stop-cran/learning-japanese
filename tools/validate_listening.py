"""Validate the bounded N5 listening schema and hash-bound audio approvals."""
from __future__ import annotations

import datetime
import hashlib
import json
import re
from pathlib import Path

ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
HASH = re.compile(r"[0-9a-f]{64}")
AUDIO_PATH = re.compile(r"audio/[a-z0-9]+(?:-[a-z0-9]+)*\.ogg")
MAX_AUDIO_BYTES = 512 * 1024


def canonical_hash(payload) -> str:
    """Hash integer-only listening JSON, preserving arrays and Unicode."""
    def integers_only(value):
        _require(not isinstance(value, float), "listening JSON numbers must be integers")
        for child in value.values() if isinstance(value, dict) else value if isinstance(value, list) else ():
            integers_only(child)
    integers_only(payload)
    return hashlib.sha256(json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")).hexdigest()


def content_hash(document: dict) -> str:
    return canonical_hash({key: value for key, value in document.items() if key not in {"audio", "audioReview"}})


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _text(value, name: str, maximum: int = 2000) -> str:
    _require(isinstance(value, str) and 0 < len(value.strip()) <= maximum
             and not any(ord(char) < 32 or 127 <= ord(char) <= 159 for char in value), f"{name} must be nonempty bounded plain text")
    return value


def _id(value, name: str) -> str:
    _require(isinstance(value, str) and len(value) <= 80 and ID.fullmatch(value) is not None, f"invalid {name}")
    return value


def _records(value, name: str, minimum: int, maximum: int) -> list[dict]:
    _require(isinstance(value, list) and minimum <= len(value) <= maximum
             and all(isinstance(item, dict) for item in value), f"invalid {name} collection")
    return value


def _unique_ids(items: list[dict], name: str) -> set[str]:
    ids = [_id(item.get("id"), f"{name} ID") for item in items]
    _require(len(ids) == len(set(ids)), f"duplicate {name} ID")
    return set(ids)


def opus_duration_ms(data: bytes, minimum_ms: int = 15000, maximum_ms: int = 60000) -> int:
    """Check a complete mono Ogg Opus stream; granule positions use the Opus 48 kHz clock."""
    _require(0 < len(data) <= MAX_AUDIO_BYTES, "audio exceeds the 512 KiB envelope")
    offset, sequence, serial, last_granule = 0, 0, None, 0
    packets, pending = [], bytearray()
    ended, audio_packets = False, 0
    crc_table = []
    for byte in range(256):
        crc = byte << 24
        for _ in range(8):
            crc = ((crc << 1) ^ (0x04C11DB7 if crc & 0x80000000 else 0)) & 0xFFFFFFFF
        crc_table.append(crc)
    while offset < len(data):
        _require(not ended and offset + 27 <= len(data), "truncated or trailing Ogg data")
        header = data[offset:offset + 27]
        _require(header[:5] == b"OggS\x00", "audio is not Ogg")
        flags, count = header[5], header[26]
        _require(flags & ~7 == 0 and bool(flags & 2) == (sequence == 0), "invalid Ogg page flags")
        _require(bool(flags & 1) == bool(pending), "invalid Ogg packet continuation")
        current_serial = int.from_bytes(header[14:18], "little")
        _require(serial in (None, current_serial), "chained Ogg streams are not supported")
        serial = current_serial
        _require(int.from_bytes(header[18:22], "little") == sequence, "discontinuous Ogg pages")
        sequence += 1
        table_end = offset + 27 + count
        _require(table_end <= len(data), "truncated Ogg segment table")
        lengths = data[offset + 27:table_end]
        end = table_end + sum(lengths)
        _require(end <= len(data), "truncated Ogg packet")
        crc = 0
        for index in range(offset, end):
            byte = 0 if offset + 22 <= index < offset + 26 else data[index]
            crc = ((crc << 8) ^ crc_table[((crc >> 24) ^ byte) & 255]) & 0xFFFFFFFF
        _require(crc == int.from_bytes(header[22:26], "little"), "Ogg page checksum mismatch")
        cursor = table_end
        for length in lengths:
            pending.extend(data[cursor:cursor + length])
            cursor += length
            if length < 255:
                if len(packets) < 2:
                    packets.append(bytes(pending))
                else:
                    _require(len(pending) > 0, "empty Opus audio packet")
                    audio_packets += 1
                pending.clear()
        granule = int.from_bytes(header[6:14], "little")
        if granule != (1 << 64) - 1:
            _require(granule >= last_granule, "decreasing Opus granule position")
            last_granule = granule
        ended = bool(flags & 4)
        offset = end
    _require(ended and not pending and len(packets) == 2 and audio_packets > 0, "incomplete Ogg stream")
    head, tags = packets
    _require(len(head) == 19 and head[:8] == b"OpusHead" and head[8] == 1
             and head[9] == 1 and head[18] == 0, "only standard mono Opus is supported")
    _require(tags.startswith(b"OpusTags"), "missing Opus tags")
    preskip = int.from_bytes(head[10:12], "little")
    _require(last_granule <= maximum_ms * 48 + preskip, "Opus granule position exceeds the media envelope")
    duration = (last_granule - preskip) * 1000 // 48000
    _require(minimum_ms <= duration <= maximum_ms,
             f"audio must be {minimum_ms}-{maximum_ms} milliseconds")
    return duration


def validate_document(document: dict, path: str, root: Path | None = None) -> bool:
    """Return explicit approval readiness; malformed drafts or approval declarations fail."""
    _require(isinstance(document, dict), "listening document must be an object")
    _require(type(document.get("schemaVersion")) is int and document["schemaVersion"] == 1, "unsupported listening schema")
    identity = _id(document.get("id"), "passage ID")
    _require(path == f"listening/{identity}.json", "passage ID must match its filename")
    _require(type(document.get("jlpt")) is int and document["jlpt"] == 5, "this pilot accepts only integer jlpt: 5")
    for name in ("title", "topic", "levelRationale"):
        _text(document.get(name), name)
    kind = document.get("kind")
    _require(kind in {"dialogue", "monologue"}, "kind must be dialogue or monologue")
    speakers = _records(document.get("speakers"), "speakers", 1, 2)
    speaker_ids = _unique_ids(speakers, "speaker")
    _require(len(speakers) == (2 if kind == "dialogue" else 1), "speaker count does not match kind")
    for speaker in speakers:
        _require(isinstance(speaker.get("voice"), str)
                 and re.fullmatch(r"ja-JP-[A-Za-z]+Neural", speaker["voice"]) is not None, "invalid Japanese stock voice")
        rate = speaker.get("ratePercent")
        _require(type(rate) is int and -15 <= rate <= 0, "ratePercent must be an integer from -15 to 0")
    turns = _records(document.get("turns"), "turns", 1, 16)
    turn_ids = _unique_ids(turns, "turn")
    _require({turn.get("speaker") for turn in turns} == speaker_ids, "every declared speaker must have turns")
    for turn in turns:
        for name in ("text", "translation"):
            _text(turn.get(name), f"turn {name}", 500)
        if "spokenText" in turn:
            _text(turn["spokenText"], "spokenText", 500)
    questions = _records(document.get("questions"), "questions", 3, 3)
    _unique_ids(questions, "question")
    _require(all(type(item.get("mainPoint")) is bool for item in questions)
             and sum(item["mainPoint"] for item in questions) == 1, "exactly one main-point question is required")
    for question in questions:
        for name in ("prompt", "explanation"):
            _text(question.get(name), f"question {name}")
        options = _records(question.get("options"), "options", 4, 4)
        option_ids = _unique_ids(options, "option")
        labels = [_text(option.get("label"), "option label", 300) for option in options]
        _require(len(set(labels)) == 4, "option labels must be distinct")
        for option in options:
            _text(option.get("rationale"), "option rationale")
        _require(question.get("answer") in option_ids, "answer must identify one option")
        evidence = question.get("evidence")
        _require(isinstance(evidence, list) and 0 < len(evidence) <= len(turns)
                 and all(isinstance(item, str) and item in turn_ids for item in evidence)
                 and len(evidence) == len(set(evidence)), "evidence must identify distinct existing turns")
    for tip in _records(document.get("vocabulary", []), "vocabulary", 0, 30):
        for name in ("surface", "reading", "gloss"):
            _text(tip.get(name), f"vocabulary {name}", 300)
        if "word" in tip:
            word = _text(tip["word"], "vocabulary word", 80)
            _require(not any(char in word for char in "/\\") and word not in {".", ".."}, "unsafe vocabulary word")
            if root is not None:
                _require((root / "words" / f"{word}.md").is_file(), f"missing word article: {word}")
    image = document.get("image")
    if image is not None:
        _require(isinstance(image, dict) and isinstance(image.get("path"), str)
                 and re.fullmatch(r"images/[^/\\\s]+\.webp", image["path"]) is not None, "unsafe image path")
        _require(isinstance(image.get("sha256"), str) and HASH.fullmatch(image["sha256"]) is not None, "invalid image hash")
        if root is not None:
            _require((root / image["path"]).is_file(), "missing listening image")
            _require(hashlib.sha256((root / image["path"]).read_bytes()).hexdigest() == image["sha256"], "listening image hash mismatch")
    current_hash = content_hash(document)
    audio, review = document.get("audio"), document.get("audioReview")
    if audio is None:
        _require(review is None, "audio review without audio")
        return False
    _require(isinstance(audio, dict), "audio must be an object")
    _require(audio.get("path") == f"audio/{identity}.ogg", "audio path must match passage ID")
    digest = audio.get("sha256")
    _require(isinstance(digest, str) and HASH.fullmatch(digest) is not None, "invalid audio hash")
    _require(audio.get("contentSha256") == current_hash, "audio was generated for a different content package")
    duration = audio.get("durationMs")
    _require(type(duration) is int and 15000 <= duration <= 60000, "invalid audio duration")
    timings = _records(audio.get("turns"), "audio turns", len(turns), len(turns))
    _require([turn.get("id") for turn in timings] == [turn["id"] for turn in turns], "audio turn order mismatch")
    end = 0
    for timing in timings:
        start, finish = timing.get("startMs"), timing.get("endMs")
        _require(type(start) is int and type(finish) is int and end <= start < finish <= duration, "invalid turn timing")
        end = finish
    if root is not None:
        audio_file = root / audio["path"]
        _require(audio_file.is_file(), "missing audio file")
        _require(audio_file.stat().st_size <= MAX_AUDIO_BYTES, "audio exceeds 512 KiB")
        data = audio_file.read_bytes()
        _require(hashlib.sha256(data).hexdigest() == digest, "audio hash mismatch")
        _require(abs(opus_duration_ms(data) - duration) <= 100, "decoded container duration disagrees with metadata")
    if review is None:
        return False
    _require(isinstance(review, dict) and review.get("status") == "approved", "invalid audioReview declaration")
    _require(review.get("audioSha256") == digest and review.get("contentSha256") == current_hash, "stale audio approval")
    _text(review.get("note"), "audio review note")
    date = review.get("reviewedOn")
    _require(isinstance(date, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) is not None, "invalid audio review date")
    datetime.date.fromisoformat(date)
    return True


def check_listening(err, root: Path, check_image=None) -> set[str]:
    referenced, images = set(), set()
    for path in sorted((root / "listening").glob("*.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            validate_document(document, path.relative_to(root).as_posix(), root)
            if document.get("image"):
                images.add(document["image"]["path"])
                if check_image is not None:
                    check_image(path, root / document["image"]["path"])
            if document.get("audio"):
                referenced.add(document["audio"]["path"])
        except (ValueError, TypeError, KeyError, OSError) as exc:
            err(path, str(exc))
    for path in sorted((root / "audio").glob("*")):
        if path.is_file() and path.relative_to(root).as_posix() not in referenced:
            err(path, "audio file has no valid listening document reference")
    return images
