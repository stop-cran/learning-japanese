#!/usr/bin/env python3
"""Generate scene images for word cards with an Azure OpenAI image deployment.

Usage: python tools/generate_images.py [--set pilot] [--only WORD ...] [--apply]

Reads tools/image_prompts.json (shared style + a scene per word), generates one image per
word, resizes it to 512 px and saves images/<word>.webp. With --apply it also adds the
`image` and `image_scene` front-matter keys to the card. Existing images are kept.
Authentication uses `az account get-access-token`; nothing secret is written to disk.
"""
import argparse
import base64
import io
import json
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ACCOUNT = "oai-kanji-icon-61298"
URL = f"https://{ACCOUNT}.openai.azure.com/openai/deployments/img/images/generations?api-version=2025-04-01-preview"
SIZE = 512
WEBP_QUALITY = 80


def token() -> str:
    return subprocess.check_output(
        ["az.cmd", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com",
         "--query", "accessToken", "-o", "tsv"], text=True).strip()


def generate(prompt: str, auth: dict) -> bytes:
    body = json.dumps({"prompt": prompt, "size": "1024x1024", "n": 1, "quality": "medium",
                       "output_format": "png"}).encode()
    for attempt in range(6):
        req = urllib.request.Request(URL, body, {**auth, "Content-Type": "application/json"})
        try:
            data = json.load(urllib.request.urlopen(req, timeout=300))
            return base64.b64decode(data["data"][0]["b64_json"])
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, e.read().decode()[:200], flush=True)
            if e.code == 400:
                raise
            time.sleep(30 * (attempt + 1) if e.code == 429 else 10)
        except OSError as e:
            print("error", e, flush=True)
            time.sleep(10)
    raise RuntimeError("generation failed")


def to_webp(png: bytes) -> bytes:
    image = Image.open(io.BytesIO(png)).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    out = io.BytesIO()
    image.save(out, "WEBP", quality=WEBP_QUALITY, method=6)
    return out.getvalue()


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", default="pilot")
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    config = json.loads((ROOT / "tools" / "image_prompts.json").read_text(encoding="utf-8"))
    scenes = config[args.set]
    out_dir = ROOT / "images"
    out_dir.mkdir(exist_ok=True)
    auth = {"Authorization": "Bearer " + token()}
    for word, scene in scenes.items():
        if args.only and word not in args.only:
            continue
        target = out_dir / f"{word}.webp"
        if not target.exists():
            target.write_bytes(to_webp(generate(f"{scene} {config['style']}", auth)))
            print("generated", word, target.stat().st_size, "bytes", flush=True)
        if args.apply:
            apply_front_matter(word, scene)


if __name__ == "__main__":
    main()
