"""Validate contract-1 task drafts and exact-output approval declarations.

Validation is not listening approval or proof of platform playback. Prior source-scoped
id/exposureId bindings may be supplied to check_listening_tasks as identity_ledger;
explicit bindings in docs/listening-task-sources.json are also enforced when present.
"""
from __future__ import annotations

import datetime
import hashlib
import io
import json
import re
from pathlib import Path

from validate_listening import (
    HASH, MAX_AUDIO_BYTES, _id, _records, _require, _text, _unique_ids,
    canonical_hash, opus_duration_ms,
)

MAX_IMAGE_BYTES = 150 * 1024
MAX_MEDIA_BYTES = 6 * 1024 * 1024
STAGE_ROLES = {
    "task-based": ["instruction", "focus", "passage", "focus-repeat"],
    "key-point": ["instruction", "focus", "passage", "focus-repeat"],
    "verbal-expression": ["instruction", "situation", "choice", "choice", "choice"],
    "quick-response": ["instruction", "utterance", "choice", "choice", "choice"],
}


class UnsupportedTaskError(ValueError):
    """Authoring input requires an unsupported schema, policy or task type."""


def content_hash(document: dict) -> str:
    return canonical_hash({key: value for key, value in document.items() if key not in {"media", "approval"}})


def media_hash(media: dict) -> str:
    return canonical_hash(media)


def _fields(value, name: str, required: str, optional: str = "") -> None:
    _require(isinstance(value, dict), f"{name} must be an object")
    required_keys, optional_keys = set(required.split()), set(optional.split())
    _require(not (set(value) - required_keys - optional_keys), f"{name} has unknown fields")
    _require(required_keys <= set(value), f"{name} is missing required fields")


def _bounded_text(value, name: str, maximum: int = 2000) -> str:
    _text(value, name, maximum)
    _require(len(value) <= maximum, f"{name} exceeds {maximum} characters")
    return value


def _references(value, name: str, available: set[str]) -> list[str]:
    _require(isinstance(value, list) and 0 < len(value) <= len(available)
             and all(isinstance(item, str) and item in available for item in value)
             and len(value) == len(set(value)), f"{name} must identify distinct existing turns")
    return value


def _media_path(value, folder: str, suffix: str) -> str:
    _require(isinstance(value, str)
             and re.fullmatch(rf"{folder}/[a-z0-9]+(?:-[a-z0-9]+)*\.{suffix}", value) is not None,
             f"unsafe {folder} path; expected a flat lowercase {suffix} filename")
    _id(value[len(folder) + 1:-(len(suffix) + 1)], f"{folder} filename")
    return value


def _digest(value, name: str) -> str:
    _require(isinstance(value, str) and HASH.fullmatch(value) is not None, f"invalid {name} hash")
    return value


def _asset(root: Path, path: str, digest: str, limit: int) -> bytes:
    file = root / path
    _require(file.is_file() and not file.is_symlink() and file.resolve().is_relative_to(root.resolve()),
             f"missing or unsafe media file: {path}")
    _require(file.stat().st_size <= limit, f"{path} exceeds {limit} bytes")
    data = file.read_bytes()
    _require(hashlib.sha256(data).hexdigest() == digest, f"media hash mismatch: {path}")
    return data


def _webp(data: bytes) -> None:
    from PIL import Image

    _require(data[:4] == b"RIFF" and data[8:12] == b"WEBP"
             and int.from_bytes(data[4:8], "little") + 8 == len(data), "invalid WebP container")
    try:
        with Image.open(io.BytesIO(data)) as image:
            _require(image.format == "WEBP" and image.n_frames == 1
                     and 1 <= image.width <= 2048 and 1 <= image.height <= 2048,
                     "image must be one WebP frame with sides 1-2048 pixels")
            image.load()
    except (Image.DecompressionBombError, OSError) as exc:
        raise ValueError(f"invalid WebP image: {exc}") from exc


def validate_document(document: dict, path: str, root: Path | None = None) -> bool:
    """Return declared approval readiness; malformed supported drafts raise ValueError."""
    _require(isinstance(document, dict), "listening task must be an object")
    for field in ("schemaVersion", "policyVersion"):
        if type(document.get(field)) is not int or document[field] != 1:
            raise UnsupportedTaskError(f"unsupported listening task {field}: {document.get(field)!r}")
    task_type = document.get("taskType")
    if not isinstance(task_type, str) or task_type not in STAGE_ROLES:
        raise UnsupportedTaskError(f"unsupported listening task type: {task_type!r}")
    _fields(document, "task",
            "schemaVersion policyVersion jlpt id exposureId taskType kind usage title topic levelRationale "
            "speakers turns stages choiceMode options answer evidence explanation",
            "blueprint visual vocabulary media approval")
    canonical_hash(document)
    identity = _id(document["id"], "task ID")
    _id(document["exposureId"], "exposure ID")
    _require(path == f"listening-tasks/{identity}.json", "task ID must match its filename")
    _require(type(document["jlpt"]) is int and document["jlpt"] == 5, "jlpt must be integer 5")
    _require(document["kind"] in ("dialogue", "monologue"), "invalid task kind")
    _require(document["usage"] in ("scored", "example"), "invalid task usage")
    if "blueprint" in document:
        _require(document["blueprint"] == "n5-section-v1", "unsupported task blueprint")
    for field in ("title", "topic", "levelRationale", "explanation"):
        _bounded_text(document[field], field)

    speakers = _records(document["speakers"], "speakers", 2, 4)
    speaker_ids = _unique_ids(speakers, "speaker")
    for speaker in speakers:
        _fields(speaker, "speaker", "id role voice ratePercent")
        _require(speaker["role"] in ("narrator", "character"), "invalid speaker role")
        _bounded_text(speaker["voice"], "speaker voice")
        _require(isinstance(speaker["voice"], str)
                 and re.fullmatch(r"ja-JP-[A-Za-z]+Neural", speaker["voice"]) is not None,
                 "invalid Japanese stock voice")
        _require(type(speaker["ratePercent"]) is int and -15 <= speaker["ratePercent"] <= 0,
                 "ratePercent must be an integer from -15 to 0")
    _require(sum(s["role"] == "narrator" for s in speakers) == 1, "exactly one narrator is required")
    _require(sum(s["role"] == "character" for s in speakers) == (2 if document["kind"] == "dialogue" else 1),
             "character speaker count does not match kind")
    turns = _records(document["turns"], "turns", 1, 32)
    turn_ids = _unique_ids(turns, "turn")
    for turn in turns:
        _fields(turn, "turn", "id speaker text translation", "spokenText")
        _require(isinstance(turn["speaker"], str) and turn["speaker"] in speaker_ids, "unknown turn speaker")
        for field in ("text", "translation", "spokenText"):
            if field in turn:
                _bounded_text(turn[field], f"turn {field}", 500)
    character_ids = {speaker["id"] for speaker in speakers if speaker["role"] == "character"}
    _require(character_ids <= {turn["speaker"] for turn in turns}, "every character speaker must have turns")
    turns_by_id = {turn["id"]: turn for turn in turns}

    audio_choices = task_type in ("verbal-expression", "quick-response")
    mode = document["choiceMode"]
    _require(mode == "audio" if audio_choices else mode in ("text", "visual"), "invalid task choiceMode")
    count = 3 if audio_choices else 4
    options = _records(document["options"], "options", count, count)
    option_ids = _unique_ids(options, "option")
    for number, option in enumerate(options, 1):
        _fields(option, "option", "id number label translation rationale")
        _require(type(option["number"]) is int and option["number"] == number,
                 "option numbers must be consecutive 1..N in authored order")
        _bounded_text(option["label"], "option label", 500)
        for field in ("translation", "rationale"):
            _bounded_text(option[field], f"option {field}")
    _require(len({option["label"] for option in options}) == count, "option labels must be distinct")
    _require(isinstance(document["answer"], str) and document["answer"] in option_ids,
             "answer must identify one option")

    stages = _records(document["stages"], "stages", 1, 8)
    _unique_ids(stages, "stage")
    used_turns, story_turns = set(), set()
    for stage in stages:
        _fields(stage, "stage", "id role turns", "optionId")
        refs = _references(stage["turns"], "stage turns", turn_ids)
        used_turns.update(refs)
        if stage["role"] in ("passage", "situation", "utterance"):
            story_turns.update(refs)
        if stage["role"] != "choice":
            _require("optionId" not in stage, "optionId is only allowed on a choice stage")
    _require([stage["role"] for stage in stages] == STAGE_ROLES[task_type], "invalid task stage role order")
    _require(used_turns == turn_ids, "every turn must be used by a stage")
    if audio_choices:
        for stage, option in zip(stages[2:], options):
            _require(stage.get("optionId") == option["id"] and len(stage["turns"]) == 1,
                     "choice stages must link one turn to each option in number order")
            turn = turns_by_id[stage["turns"][0]]
            _require(turn["text"] == f'{option["number"]}。{option["label"]}',
                     "spoken choice source must be <number>。<label>")
    else:
        _require(stages[1]["turns"] == stages[3]["turns"], "focus-repeat must repeat the exact focus turn list")
    evidence = _references(document["evidence"], "evidence", turn_ids)
    _require(story_turns.intersection(evidence), "evidence must include a passage, situation or utterance turn")

    if "visual" in document:
        visual = document["visual"]
        _fields(visual, "visual", "role description")
        _require(visual["role"] in ("context", "required"), "invalid visual role")
        _bounded_text(visual["description"], "visual description")
    if task_type == "quick-response":
        _require("visual" not in document, "quick-response cannot have a picture")
    elif task_type == "verbal-expression" or mode == "visual":
        _require("visual" in document and document["visual"]["role"] == "required",
                 "this task requires a required visual")
    for tip in _records(document.get("vocabulary", []), "vocabulary", 0, 30):
        _fields(tip, "vocabulary", "surface reading gloss", "word")
        for field in ("surface", "reading", "gloss"):
            _bounded_text(tip[field], f"vocabulary {field}", 300)
        if "word" in tip:
            word = _bounded_text(tip["word"], "vocabulary word", 80)
            _require(not any(char in word for char in '/\\:<>|"*?') and word not in (".", ".."),
                     "unsafe vocabulary word")
            if root is not None:
                _require(f"{word}.md" in {file.name for file in (root / "words").glob("*.md") if file.is_file()},
                         f"missing word article: {word}")

    current_hash = content_hash(document)
    if "media" not in document:
        _require("approval" not in document, "approval without media")
        return False
    media = document["media"]
    _fields(media, "media", "contentSha256 audio", "image")
    _require(media["contentSha256"] == current_hash, "media was generated for a different content package")
    audio = media["audio"]
    _require(isinstance(audio, dict) and set(audio) == {stage["id"] for stage in stages},
             "media audio keys must exactly match stage IDs")
    _require(("image" in media) == ("visual" in document), "media image must be present iff visual is present")
    total_duration, bindings = 0, {}
    for stage in stages:
        clip = audio[stage["id"]]
        _fields(clip, "audio clip", "path sha256 durationMs turns")
        clip_path = _media_path(clip["path"], "task-audio", "ogg")
        digest = _digest(clip["sha256"], "audio")
        duration = clip["durationMs"]
        _require(type(duration) is int and 250 <= duration <= 90000, "audio duration must be 250-90000 ms")
        total_duration += duration
        timings = _records(clip["turns"], "audio turns", len(stage["turns"]), len(stage["turns"]))
        _require([timing.get("id") for timing in timings] == stage["turns"], "audio turn order mismatch")
        end = 0
        for timing in timings:
            _fields(timing, "audio timing", "id startMs endMs")
            start, finish = timing["startMs"], timing["endMs"]
            _require(type(start) is int and type(finish) is int and end <= start < finish <= duration,
                     "invalid turn timing")
            end = finish
        # Reuse is permitted only for the same exact turns and output, never another script.
        binding = (digest, duration, canonical_hash(timings))
        _require(clip_path not in bindings or bindings[clip_path] == binding, "conflicting shared audio binding")
        if root is not None and clip_path not in bindings:
            data = _asset(root, clip_path, digest, MAX_AUDIO_BYTES)
            _require(abs(opus_duration_ms(data, 250, 90000) - duration) <= 100,
                     "container duration disagrees with metadata")
        bindings[clip_path] = binding
    _require(total_duration <= 150000, "total stage occurrence duration exceeds 150000 ms")
    if "image" in media:
        image = media["image"]
        _fields(image, "image", "path sha256")
        image_path = _media_path(image["path"], "task-images", "webp")
        digest = _digest(image["sha256"], "image")
        if root is not None:
            _webp(_asset(root, image_path, digest, MAX_IMAGE_BYTES))
    if "approval" not in document:
        return False
    approval = document["approval"]
    _fields(approval, "approval", "status contentSha256 mediaSha256 reviewedOn note")
    _require(approval["status"] == "approved", "invalid approval status")
    _require(approval["contentSha256"] == current_hash and approval["mediaSha256"] == media_hash(media),
             "stale task approval")
    _bounded_text(approval["note"], "approval note")
    date = approval["reviewedOn"]
    _require(isinstance(date, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date) is not None,
             "invalid approval date")
    datetime.date.fromisoformat(date)
    return True


def _ledger_bindings(value, bindings: dict[str, str]) -> None:
    if isinstance(value, dict):
        if "id" in value and "exposureId" in value:
            identity, exposure = _id(value["id"], "ledger ID"), _id(value["exposureId"], "ledger exposure ID")
            _require(identity not in bindings or bindings[identity] == exposure, "conflicting identity ledger bindings")
            bindings[identity] = exposure
        for child in value.values():
            _ledger_bindings(child, bindings)
    elif isinstance(value, list):
        for child in value:
            _ledger_bindings(child, bindings)


def check_listening_tasks(err, root: Path, identity_ledger: dict[str, str] | None = None) -> None:
    """Check the new catalog without exposing any new assets to legacy validation."""
    for folder in ("listening-tasks", "task-audio", "task-images"):
        directory = root / folder
        if directory.exists() and (not directory.is_dir() or directory.is_symlink()):
            err(directory, f"{folder} must be a regular directory")
            return
    bindings = dict(identity_ledger or {})
    ledger = root / "docs" / "listening-task-sources.json"
    if ledger.is_file():
        try:
            _ledger_bindings(json.loads(ledger.read_text(encoding="utf-8")), bindings)
        except (ValueError, TypeError, OSError) as exc:
            err(ledger, str(exc))
    legacy_ids = {path.stem for path in (root / "listening").glob("*.json")}
    referenced = set()
    for path in sorted((root / "listening-tasks").glob("*")):
        try:
            _require(path.is_file() and not path.is_symlink() and path.suffix == ".json",
                     "listening-tasks requires flat JSON files")
            document = json.loads(path.read_text(encoding="utf-8"))
            validate_document(document, path.relative_to(root).as_posix(), root)
            identity = document["id"]
            _require(identity not in legacy_ids, "task ID collides with legacy listening ID")
            _require(identity not in bindings or bindings[identity] == document["exposureId"],
                     "task ID cannot rebind its ledger exposure identity")
            bindings[identity] = document["exposureId"]
            if "media" in document:
                referenced.update(clip["path"] for clip in document["media"]["audio"].values())
                if "image" in document["media"]:
                    referenced.add(document["media"]["image"]["path"])
        except (ValueError, TypeError, KeyError, OSError) as exc:
            err(path, str(exc))
    total_bytes = 0
    for folder, suffix in (("task-audio", "ogg"), ("task-images", "webp")):
        for path in sorted((root / folder).glob("*")):
            try:
                relative = path.relative_to(root).as_posix()
                _media_path(relative, folder, suffix)
                _require(path.is_file() and not path.is_symlink(), f"{folder} requires flat regular files")
                total_bytes += path.stat().st_size
                _require(relative in referenced, "media file has no valid listening task reference")
            except (ValueError, OSError) as exc:
                err(path, str(exc))
    if total_bytes > MAX_MEDIA_BYTES:
        err(root / "task-audio", "new unique audio/images exceed the combined 6 MiB budget")
