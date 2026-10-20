#!/usr/bin/env python3
"""Generate scene images for word cards with an Azure OpenAI image deployment.

Usage: python tools/generate_images.py [--set pilot] [--only WORD ...] [--apply]

Legacy sets read tools/image_prompts.json. --plan reads a reviewed taught-sense inventory;
--artifacts stores original PNGs and request receipts outside the content payload.
With a plan, --apply ONLY writes complete, visually reviewed catalogs (no paid requests).
--check validates the entire plan without generation. Existing images are never overwritten.
Authentication uses `az account get-access-token`; nothing secret is written to disk.
"""
import argparse
import base64
import binascii
from datetime import datetime, timezone
import hashlib
import io
import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image
from validate import MAX_IMAGE_BYTES, MAX_IMAGES_TOTAL_BYTES
from validate_scenes import validate_catalog

ROOT = Path(__file__).resolve().parent.parent
ACCOUNT = "oai-kanji-icon-61298"
URL = f"https://{ACCOUNT}.openai.azure.com/openai/deployments/img/images/generations?api-version=2025-04-01-preview"
SIZE = 512
WEBP_QUALITY = 80
SUBSCRIPTION = os.environ.get("AZURE_SUBSCRIPTION_ID")
SCENE_FIELDS = ("id", "sense", "image", "description", "quizEligible")
REQUEST = {"size": "1024x1024", "n": 1, "quality": "medium", "output_format": "png"}
_access_token = ""
_expires_at = 0


class GenerationFailure(RuntimeError):
    def __init__(self, message: str, retry_safe: bool = False):
        super().__init__(message)
        self.retry_safe = retry_safe


def token(force: bool = False) -> str:
    global _access_token, _expires_at
    if not SUBSCRIPTION:
        raise ValueError("Set --subscription or AZURE_SUBSCRIPTION_ID explicitly before generation")
    if not force and _access_token and _expires_at > time.time() + 300:
        return _access_token
    result = json.loads(subprocess.check_output(
        ["az.cmd", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com",
         "--subscription", SUBSCRIPTION, "-o", "json"], text=True))
    _access_token, _expires_at = result["accessToken"], int(result["expires_on"])
    return _access_token


def generate(prompt: str, auth: dict | None = None) -> bytes:
    body = json.dumps({"prompt": prompt, **REQUEST}).encode()
    for attempt in range(6):
        headers = auth if auth is not None else {"Authorization": "Bearer " + token()}
        req = urllib.request.Request(URL, body, {**headers, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                data = json.load(response)
            return base64.b64decode(data["data"][0]["b64_json"], validate=True)
        except urllib.error.HTTPError as e:
            if e.code == 401 and auth is None and attempt == 0:
                token(force=True)
                continue
            if e.code != 429:
                detail = e.read(4096).decode("utf-8", errors="replace").strip()
                request_id = e.headers.get("apim-request-id", "not supplied")
                raise GenerationFailure(f"Image request rejected with HTTP {e.code} (request {request_id}): {detail}",
                                        retry_safe=400 <= e.code < 500 and e.code != 408) from e
            delay = e.headers.get("Retry-After", "")
            seconds = min(300, int(delay)) if delay.isdecimal() else 30 * (attempt + 1)
            print(f"HTTP 429; retry in {seconds}s ({attempt + 1}/6)", flush=True)
            if attempt < 5:
                time.sleep(seconds)
        except (OSError, ValueError, KeyError, IndexError, TypeError, binascii.Error) as e:
            raise GenerationFailure("No usable response; generation/billing outcome is uncertain") from e
    raise GenerationFailure("Image deployment remains rate-limited; resume later", retry_safe=True)


def to_webp(png: bytes) -> bytes:
    with Image.open(io.BytesIO(png)) as original:
        if original.format != "PNG" or original.width != original.height or not 1 <= original.width <= 2048 or original.n_frames != 1:
            raise ValueError("Expected one square PNG frame, at most 2048 pixels per side")
        image = original.convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    out = io.BytesIO()
    image.save(out, "WEBP", quality=WEBP_QUALITY, method=6)
    data = out.getvalue()
    validate_webp(data)
    return data


def validate_webp(data: bytes) -> None:
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("WebP exceeds the 100 KiB authoring limit")
    with Image.open(io.BytesIO(data)) as image:
        if image.format != "WEBP" or image.size != (SIZE, SIZE) or image.n_frames != 1:
            raise ValueError("Expected a single-frame 512x512 WebP")
        image.load()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_atomic(path: Path, data: bytes, replace: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as file:
        temporary = Path(file.name)
        file.write(data)
        file.flush()
        os.fsync(file.fileno())
    try:
        if path.exists() and not replace:
            raise FileExistsError(path)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def write_json(path: Path, data: dict) -> None:
    write_atomic(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode(), replace=True)


def read_plan(path: Path, root: Path = ROOT) -> dict:
    plan = json.loads(path.read_text(encoding="utf-8"))
    if (type(plan.get("schemaVersion")) is not int or plan["schemaVersion"] != 1
            or not isinstance(plan.get("words"), dict) or not plan["words"]):
        raise ValueError("Expected a version-1 scene plan with words")
    owners = {}
    for word, entry in plan["words"].items():
        validate_catalog({"schemaVersion": 1, "word": word, "scenes": entry["scenes"]}, f"{word}.json")
        article = root / "words" / f"{word}.md"
        if digest(article.read_bytes()) != entry["articleSha256"]:
            raise ValueError(f"{word}: card changed since the scene inventory; review its basis first")
        for scene in entry["scenes"]:
            if not isinstance(scene.get("prompt"), str) or not scene["prompt"].strip():
                raise ValueError(f"{word}/{scene['id']}: missing generation prompt")
            image = scene["image"]
            if image in owners:
                raise ValueError(f"{image}: already owned by {owners[image]}")
            owners[image] = word
            if "existingSha256" in scene:
                data = (root / image).read_bytes()
                if digest(data) != scene["existingSha256"]:
                    raise ValueError(f"{image}: approved bytes changed; refusing to replace them")
                validate_webp(data)
    return plan


def receipt_paths(artifacts: Path, scene: dict) -> tuple[Path, Path]:
    name = Path(scene["image"]).stem
    return artifacts / f"{name}.json", artifacts / f"{name}.png"


def generate_scene(word: str, entry: dict, scene: dict, style: str, artifacts: Path,
                   root: Path = ROOT, retry_uncertain: bool = False) -> None:
    target = root / scene["image"]
    if "existingSha256" in scene:
        return
    receipt_path, png_path = receipt_paths(artifacts, scene)
    if png_path.exists() and not receipt_path.exists():
        raise ValueError(f"{png_path.name}: original output has no request receipt")
    request = {"word": word, "sceneId": scene["id"], "image": scene["image"],
               "articleSha256": entry["articleSha256"], "prompt": f"{scene['prompt']} {style}",
               "endpoint": URL, "parameters": REQUEST}
    receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else {"request": request, "attempts": []}
    if receipt["request"] != request:
        raise ValueError(f"{target.name}: request changed; retain the old output and use a new image filename")
    if target.exists():
        data = target.read_bytes()
        if digest(data) != receipt.get("imageSha256"):
            raise ValueError(f"{target.name}: existing image has no matching receipt; refusing regeneration")
        validate_webp(data)
        if receipt.get("status") != "complete":
            if digest(png_path.read_bytes()) != receipt.get("pngSha256"):
                raise ValueError(f"{png_path.name}: original output changed")
            receipt["status"] = "complete"
            write_json(receipt_path, receipt)
            print("recovered completion receipt", target.name, flush=True)
        print("kept", target.name, flush=True)
        return
    if not png_path.exists():
        if receipt.get("status") in ("requesting", "uncertain") and not retry_uncertain:
            raise ValueError(f"{target.name}: previous request may have been billed; inspect before --retry-uncertain")
        # Authenticate before marking a request as sent, so a local login failure cannot imply paid generation.
        token()
        receipt["status"] = "requesting"
        receipt["attempts"].append({"startedAt": datetime.now(timezone.utc).isoformat()})
        write_json(receipt_path, receipt)
        try:
            png = generate(request["prompt"])
        except GenerationFailure as exc:
            receipt["status"] = "deferred" if exc.retry_safe else "uncertain"
            receipt["attempts"][-1]["error"] = str(exc)
            write_json(receipt_path, receipt)
            raise
        write_atomic(png_path, png)
        receipt["generatedAt"] = datetime.now(timezone.utc).isoformat()
    png = png_path.read_bytes()
    if receipt.get("pngSha256") not in (None, digest(png)):
        raise ValueError(f"{png_path.name}: original output changed")
    receipt["pngSha256"] = digest(png)
    receipt["status"] = "downloaded"
    write_json(receipt_path, receipt)
    data = to_webp(png)
    total = sum(path.stat().st_size for path in (root / "images").glob("*.webp"))
    if total + len(data) > MAX_IMAGES_TOTAL_BYTES:
        raise ValueError("Writing this image would exceed the 25 MiB authoring budget")
    receipt.update(imageSha256=digest(data), imageBytes=len(data), storedFormat={
        "format": "WEBP", "width": SIZE, "height": SIZE, "quality": WEBP_QUALITY, "method": 6,
    })
    write_json(receipt_path, receipt)
    write_atomic(target, data)
    receipt["status"] = "complete"
    write_json(receipt_path, receipt)
    print("generated", target.name, len(data), "bytes", flush=True)


def apply_catalogs(words: dict, artifacts: Path, root: Path = ROOT) -> None:
    catalogs = {}
    for word, entry in words.items():
        for scene in entry["scenes"]:
            data = (root / scene["image"]).read_bytes()
            validate_webp(data)
            expected = scene.get("existingSha256")
            if expected is None:
                receipt_path, _ = receipt_paths(artifacts, scene)
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                expected = receipt["imageSha256"]
                review = scene.get("advisoryReview", {})
                if review.get("verdict") not in ("ACCEPT", "ARTICLE_ONLY") or review.get("imageSha256") != expected:
                    raise ValueError(f"{scene['image']}: needs an actual hash-pinned visual review before publication")
                if not isinstance(review.get("note"), str) or not review["note"].strip():
                    raise ValueError(f"{scene['image']}: visual review needs its actual observations")
                if scene["quizEligible"] and review["verdict"] != "ACCEPT":
                    raise ValueError(f"{scene['image']}: article-only review cannot enable quizzes")
            if digest(data) != expected:
                raise ValueError(f"{scene['image']}: reviewed image changed")
        catalogs[word] = {"schemaVersion": 1, "word": word,
                          "scenes": [{field: scene[field] for field in SCENE_FIELDS} for scene in entry["scenes"]]}
    for word, catalog in catalogs.items():
        write_json(root / "scenes" / f"{word}.json", catalog)
    print("Applied", len(catalogs), "catalogs; lexical cards and legacy fields were not rewritten.")


def apply_front_matter(word: str, scene: str) -> None:
    card = ROOT / "words" / f"{word}.md"
    raw = card.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(eol)
    end = lines.index("---", 1)
    lines = [ln for ln in lines[:end] if not ln.startswith(("image:", "image_scene:"))] + lines[end:]
    end = lines.index("---", 1)
    lines[end:end] = [f"image: images/{word}.webp", f"image_scene: {scene}"]
    card.write_bytes(eol.join(lines).encode("utf-8"))


def main() -> None:
    global SUBSCRIPTION
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--set", default="pilot")
    source.add_argument("--plan", type=Path)
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--artifacts", type=Path)
    parser.add_argument("--retry-uncertain", action="store_true")
    parser.add_argument("--subscription", default=SUBSCRIPTION)
    args = parser.parse_args()
    SUBSCRIPTION = args.subscription
    config = json.loads((ROOT / "tools" / "image_prompts.json").read_text(encoding="utf-8"))
    if args.plan:
        plan = read_plan(args.plan)
        words = plan["words"]
        if args.only:
            unknown = set(args.only) - words.keys()
            if unknown:
                parser.error(f"Unknown words: {sorted(unknown)}")
            words = {word: entry for word, entry in words.items() if word in args.only}
        print("Plan:", len(words), "words,", sum(len(entry["scenes"]) for entry in words.values()), "scenes", flush=True)
        if args.check:
            return
        if args.artifacts is None:
            parser.error("--plan requires --artifacts for resumable original outputs and request receipts")
        if args.apply:
            apply_catalogs(words, args.artifacts)
        else:
            for word, entry in words.items():
                for scene in entry["scenes"]:
                    generate_scene(word, entry, scene, config["style"], args.artifacts, retry_uncertain=args.retry_uncertain)
        return
    scenes = config[args.set]
    out_dir = ROOT / "images"
    out_dir.mkdir(exist_ok=True)
    for word, scene in scenes.items():
        if args.only and word not in args.only:
            continue
        target = out_dir / f"{word}.webp"
        if not target.exists() and not args.check:
            write_atomic(target, to_webp(generate(f"{scene} {config['style']}")))
            print("generated", word, target.stat().st_size, "bytes", flush=True)
        if args.apply and not args.check:
            apply_front_matter(word, scene)


if __name__ == "__main__":
    main()
