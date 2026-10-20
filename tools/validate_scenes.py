"""Validation of optional, authoritative scenes/<word>.json catalogs."""
import json
import re
from pathlib import Path

IMAGE_PATH = re.compile(r"images/[^/\\\s]+\.webp")
SCENE_PATH = re.compile(r"scenes/[^/\\\s]+\.json")
SCENE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def read_catalog(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return validate_catalog(data, path.name)


def validate_catalog(data: dict, filename: str) -> dict:
    if not SCENE_PATH.fullmatch(f"scenes/{filename}"):
        raise ValueError("not a flat scenes/<word>.json path")
    if not isinstance(data, dict) or type(data.get("schemaVersion")) is not int or data["schemaVersion"] != 1:
        raise ValueError("schemaVersion must be the integer 1")
    if data.get("word") != Path(filename).stem:
        raise ValueError("word must match the file name")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("scenes must be a nonempty list")
    ids, images = set(), set()
    for scene in scenes:
        if not isinstance(scene, dict):
            raise ValueError("each scene must be an object")
        for field in ("id", "sense", "image", "description"):
            if not isinstance(scene.get(field), str) or not scene[field].strip():
                raise ValueError(f"{field} must be a nonblank string")
        if not SCENE_ID.fullmatch(scene["id"]) or scene["id"] in ids:
            raise ValueError(f"invalid or repeated scene ID '{scene['id']}'")
        if not IMAGE_PATH.fullmatch(scene["image"]):
            raise ValueError(f"{scene['id']}: not a flat images/<name>.webp path")
        if scene["image"] in images:
            raise ValueError(f"{scene['id']}: repeated image '{scene['image']}'")
        if type(scene.get("quizEligible")) is not bool:
            raise ValueError(f"{scene['id']}: quizEligible must be an explicit boolean")
        ids.add(scene["id"])
        images.add(scene["image"])
    return data


def check_scenes(err, root: Path, words: dict[str, dict], check_image_file) -> dict[str, list[str]]:
    references = {}
    folder = root / "scenes"
    if not folder.exists():
        return references
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix != ".json":
            err(path, "only flat .json scene catalogs are allowed")
            continue
        try:
            catalog = read_catalog(path)
            word = catalog["word"]
            if word not in words:
                raise ValueError(f"word '{word}' is missing")
            legacy_image = words[word].get("image")
            if legacy_image is not None:
                legacy = next((scene for scene in catalog["scenes"] if scene["image"] == legacy_image), None)
                if legacy is None or not legacy["quizEligible"] or legacy["description"] != words[word].get("image_scene"):
                    raise ValueError("legacy image must match a quiz-eligible catalog scene and its description")
        except (ValueError, UnicodeError) as exc:
            err(path, str(exc))
            continue
        references[word] = [scene["image"] for scene in catalog["scenes"]]
        for image in references[word]:
            file = root / image
            if not file.is_file():
                err(path, f"image file '{image}' does not exist")
            else:
                check_image_file(path, file)
    return references
