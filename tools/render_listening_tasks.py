"""Frozen task-stage authoring runs using book-skills' shared synthesis engine.

Planning, verification and HTML author previews never authorize expenditure or
listening approval. Keep run directories outside the public content repository.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import html
import importlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import listening_task_budget as budget
import validate_listening_tasks as tasks


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def service_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_engine(directory: Path):
    directory = directory.resolve()
    sys.path.insert(0, str(directory))
    engine = importlib.import_module("synthesize")
    if Path(engine.__file__).resolve().parent != directory:
        raise ValueError("A different synthesis engine is already loaded")
    engine.LANGUAGE, engine.XML_LANG = "ja", "ja-JP"
    return engine


def renderer_hash(engine) -> str:
    return tasks.canonical_hash({
        "shared": engine.pipeline_hash(),
        "adapter": file_hash(Path(__file__)),
        "budget": file_hash(Path(budget.__file__)),
        "validator": file_hash(Path(tasks.__file__)),
        "legacyValidator": file_hash(Path(__file__).with_name("validate_listening.py")),
    })


def logical_path(document: dict) -> str:
    return f"listening-tasks/{document['id']}.json"


def prepared_turns(document: dict, references: list[str]) -> list[dict]:
    speakers = {speaker["id"]: speaker for speaker in document["speakers"]}
    turns = {turn["id"]: turn for turn in document["turns"]}
    return [{"id": reference, "text": turns[reference].get("spokenText", turns[reference]["text"]),
             "voice": speakers[turns[reference]["speaker"]]["voice"],
             "rate": f'{speakers[turns[reference]["speaker"]]["ratePercent"]}%'}
            for reference in references]


def preview_entries(plan: dict) -> list[tuple[dict, list[str]]]:
    by_id = {entry["document"]["id"]: entry for entry in plan["tasks"]}
    result = []
    for selector in plan["previewTurns"]:
        identifier, turn = selector.split(":")
        entry = by_id[identifier]
        prepared_turns(entry["document"], [turn])
        result.append((entry, [turn]))
    return result


def create_plan(root: Path, content_root: Path, sources: list[Path], images: dict[str, Path],
                previews: list[str], engine, resource: str, subscription: str) -> None:
    if root.exists() or root.resolve().is_relative_to(content_root.resolve()):
        raise ValueError("Choose a new private run directory outside the content repository")
    if not 1 <= len(sources) <= 32 or not previews or len(set(previews)) != len(previews):
        raise ValueError("Select 1-32 tasks and distinct explicit preview turns")
    endpoint = engine.resolve_endpoint(resource=resource)
    if not endpoint or not subscription.strip():
        raise ValueError("Explicit existing resource and subscription bindings are required")
    entries = []
    for source in sources:
        document = budget.read_json(source)
        tasks.validate_document(document, logical_path(document), content_root)
        if source.stem != document["id"] or "media" in document or "approval" in document:
            raise ValueError("Inputs must be filename-matched drafts without media or approval")
        entries.append({"source": str(source.resolve()), "document": document,
                        "contentSha256": tasks.content_hash(document)})
    identifiers = [entry["document"]["id"] for entry in entries]
    required_images = {entry["document"]["id"] for entry in entries if "visual" in entry["document"]}
    if len(set(identifiers)) != len(identifiers) or images.keys() != required_images:
        raise ValueError("Task IDs must be unique and pictures must exactly match declared visuals")
    plan = {"version": 1, "rendererSha256": renderer_hash(engine),
            "endpointSha256": service_hash(endpoint.lower()), "subscriptionSha256": service_hash(subscription),
            "contentRoot": str(content_root.resolve()), "tasks": entries, "previewTurns": previews}
    try:
        selected = preview_entries(plan)
    except (KeyError, ValueError) as exc:
        raise ValueError("Preview selectors must identify an existing task-id:turn-id") from exc
    profiles = {(s["voice"], f'{s["ratePercent"]}%') for entry in entries for s in entry["document"]["speakers"]}
    preview_profiles = {(turn["voice"], turn["rate"]) for entry, refs in selected
                        for turn in prepared_turns(entry["document"], refs)}
    if not profiles <= preview_profiles:
        raise ValueError("Previews must cover every selected voice/rate profile")
    for entry in entries:
        identifier = entry["document"]["id"]
        if identifier in images:
            source = images[identifier].resolve()
            if source.stat().st_size > tasks.MAX_IMAGE_BYTES:
                raise ValueError("Picture exceeds the 150 KiB budget")
            tasks._webp(source.read_bytes())
            digest = file_hash(source)
            entry["image"] = {"source": str(source), "path": f"task-images/image-{digest}.webp", "sha256": digest}
    root.mkdir(parents=True)
    with budget.run_lock(root):
        for entry in entries:
            if "image" in entry:
                target = root / entry["image"]["path"]
                target.parent.mkdir(exist_ok=True)
                shutil.copyfile(entry["image"]["source"], target)
        budget.write_json(root / "plan.json", plan)


def load_plan(root: Path, engine) -> dict:
    plan = budget.read_json(root / "plan.json")
    if plan["version"] != 1 or plan["rendererSha256"] != renderer_hash(engine):
        raise ValueError("Renderer/validator changed; prepare a new frozen run")
    for entry in plan["tasks"]:
        document = entry["document"]
        tasks.validate_document(document, logical_path(document), Path(plan["contentRoot"]))
        if (tasks.content_hash(document) != entry["contentSha256"]
                or budget.read_json(Path(entry["source"])) != document):
            raise ValueError(f"Frozen learning package changed: {document['id']}")
        if "image" in entry:
            image = entry["image"]
            if file_hash(Path(image["source"])) != image["sha256"] or file_hash(root / image["path"]) != image["sha256"]:
                raise ValueError("Frozen picture changed")
    return plan


def require_same_plan(root: Path, engine, expected_hash: str) -> None:
    if tasks.canonical_hash(load_plan(root, engine)) != expected_hash:
        raise ValueError("Frozen run plan changed during rendering")


def clip_request(entry: dict, references: list[str], engine) -> dict:
    return {"rendererSha256": renderer_hash(engine), "turns": prepared_turns(entry["document"], references)}


def clip_receipt(root: Path, request: dict) -> Path:
    identifier = "stage-" + tasks.canonical_hash(request)
    return root / "records" / f"{identifier}.json"


def clip_audio_path(clip: dict) -> str:
    # Identical bytes with different turn/timing bindings must not share a task's path.
    binding = {key: clip[key] for key in ("sha256", "durationMs", "turns")}
    return f"task-audio/stage-{tasks.canonical_hash(binding)}.ogg"


def ffmpeg(engine, arguments: list[str], data: bytes | None = None) -> bytes:
    process = subprocess.run([engine._ffmpeg_exe(), "-hide_banner", "-loglevel", "error"] + arguments,
                             input=data, capture_output=True)
    if process.returncode:
        raise ValueError("Audio conversion failed: " + process.stderr.decode(errors="replace")[:1000])
    return process.stdout


def verify_audio(path: Path, expected_ms: int, engine) -> None:
    if not 0 < path.stat().st_size <= tasks.MAX_AUDIO_BYTES:
        raise ValueError("Stage audio exceeds its byte budget")
    container_ms = tasks.opus_duration_ms(path.read_bytes(), 250, 90000)
    decoded = ffmpeg(engine, ["-xerror", "-i", str(path), "-map", "0:a:0", "-ac", "1", "-ar", "24000",
                              "-f", "s16le", "pipe:1"])
    actual_ms = round(len(decoded) * 1000 / (engine.SAMPLE_RATE * engine.SAMPLE_WIDTH))
    if not 250 <= actual_ms <= 90000 or max(abs(actual_ms - expected_ms), abs(container_ms - expected_ms)) > 100:
        raise ValueError("Declared, container and decoded stage duration disagree")


def verified_clip(root: Path, request: dict, engine) -> dict:
    record = budget.read_json(clip_receipt(root, request))
    clip = record["audio"]
    digest = clip["sha256"]
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Invalid stage audio hash")
    if record["request"] != request or clip["path"] != clip_audio_path(clip):
        raise ValueError("Stage recording belongs to another request")
    audio = root / clip["path"]
    if file_hash(audio) != clip["sha256"]:
        raise ValueError("Stage audio hash changed")
    verify_audio(audio, clip["durationMs"], engine)
    return clip


def render_clip(root: Path, request: dict, engine, token, session) -> dict:
    receipt = clip_receipt(root, request)
    if receipt.exists():
        return verified_clip(root, request, engine)
    pcm = bytearray(engine._silence(150))
    timings = []
    for index, turn in enumerate(request["turns"]):
        if index:
            pcm.extend(engine._silence(350))
        start = round(len(pcm) * 1000 / (engine.SAMPLE_RATE * engine.SAMPLE_WIDTH))
        pcm.extend(engine.cached_pcm(turn["text"], token, session, turn["voice"], turn["rate"], root / ".pcm", False))
        end = round(len(pcm) * 1000 / (engine.SAMPLE_RATE * engine.SAMPLE_WIDTH))
        if end <= start:
            raise ValueError("Empty spoken turn")
        timings.append({"id": turn["id"], "startMs": start, "endMs": end})
    pcm.extend(engine._silence(200))
    duration = round(len(pcm) * 1000 / (engine.SAMPLE_RATE * engine.SAMPLE_WIDTH))
    if not 250 <= duration <= 90000:
        raise ValueError("Stage is outside 250-90000 ms; revise speech, never pad to fit")
    (root / "task-audio").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="encode-", dir=root) as temporary:
        pending = Path(temporary) / "stage.ogg"
        ffmpeg(engine, ["-y", "-f", "wav", "-i", "pipe:0", "-map_metadata", "-1", "-codec:a", "libopus",
                       "-b:a", "32k", "-vbr", "on", "-application", "voip", "-ac", "1", "-ar", "24000",
                       str(pending)], engine._wrap_wav(bytes(pcm)))
        verify_audio(pending, duration, engine)
        digest = file_hash(pending)
        clip = {"sha256": digest, "durationMs": duration, "turns": timings}
        clip["path"] = clip_audio_path(clip)
        audio = root / clip["path"]
        if audio.exists():
            if file_hash(audio) != digest:
                raise ValueError("Existing content-addressed audio has different bytes")
        else:
            pending.replace(audio)
        budget.write_json(receipt, {"request": request, "audio": clip})
    return clip


def preview_binding(root: Path, plan: dict, engine) -> list[dict]:
    return [{"selector": selector, "audio": verified_clip(root, clip_request(entry, refs, engine), engine)}
            for selector, (entry, refs) in zip(plan["previewTurns"], preview_entries(plan))]


def require_preview_approval(root: Path, plan: dict, engine) -> None:
    record = budget.read_json(root / "preview-approval.json")
    if (record["planSha256"] != tasks.canonical_hash(plan)
            or record["clips"] != preview_binding(root, plan, engine) or not record["note"].strip()):
        raise ValueError("Exact voice/pronunciation previews have not been approved")


def validate_output(document: dict, root: Path, plan: dict) -> bool:
    return tasks.validate_document(document, logical_path(document), root,
                                   vocabulary_root=Path(plan["contentRoot"]))


def render(root: Path, engine, resource: str, subscription: str, phase: str, raw_session) -> None:
    with budget.run_lock(root):
        plan = load_plan(root, engine)
        plan_hash = tasks.canonical_hash(plan)
        endpoint = engine.resolve_endpoint(resource=resource)
        if (not endpoint or service_hash(endpoint.lower()) != plan["endpointSha256"]
                or service_hash(subscription) != plan["subscriptionSha256"]):
            raise ValueError("Resource/subscription differ from the frozen plan")
        session = budget.BudgetSession(raw_session, root, endpoint, plan_hash, phase,
                                       lambda: require_same_plan(root, engine, plan_hash))
        if phase == "complete":
            if session.authorization.get("deferPreviewApproval") is True:
                # Explicit private generation is not a declaration that the previews were heard.
                preview_binding(root, plan, engine)
            else:
                require_preview_approval(root, plan, engine)
        engine.ENDPOINT = endpoint
        token = engine.make_token_provider(subscription=subscription)
        if phase == "preview":
            for entry, refs in preview_entries(plan):
                render_clip(root, clip_request(entry, refs, engine), engine, token, session)
        else:
            for entry in plan["tasks"]:
                document = entry["document"]
                clips = {stage["id"]: render_clip(root, clip_request(entry, stage["turns"], engine), engine, token, session)
                         for stage in document["stages"]}
                media = {"contentSha256": entry["contentSha256"], "audio": clips}
                if "image" in entry:
                    media["image"] = {key: entry["image"][key] for key in ("path", "sha256")}
                output = {**document, "media": media}
                validate_output(output, root, plan)
                path = root / "packages" / f"{document['id']}.json"
                if path.exists():
                    existing = budget.read_json(path)
                    if {key: value for key, value in existing.items() if key != "approval"} != output:
                        raise ValueError("Existing output package changed")
                    validate_output(existing, root, plan)
                else:
                    budget.write_json(path, output)
        require_same_plan(root, engine, plan_hash)
        write_review_page(root, plan, engine, phase)


def review_note(note: str, reviewed_on: str) -> None:
    parsed = date.fromisoformat(reviewed_on)
    if not note.strip() or parsed.isoformat() != reviewed_on or parsed > date.today():
        raise ValueError("A real listening note and nonfuture ISO review date are required")


def approve_preview(root: Path, engine, note: str, reviewed_on: str) -> None:
    review_note(note, reviewed_on)
    with budget.run_lock(root):
        plan = load_plan(root, engine)
        budget.write_json(root / "preview-approval.json", {
            "planSha256": tasks.canonical_hash(plan), "clips": preview_binding(root, plan, engine),
            "reviewedOn": reviewed_on, "note": note,
        })


def verified_package(root: Path, plan: dict, identifier: str, engine) -> dict:
    entry = next((entry for entry in plan["tasks"] if entry["document"]["id"] == identifier), None)
    if entry is None:
        raise ValueError("Task is not in this frozen run")
    document = budget.read_json(root / "packages" / f"{identifier}.json")
    if {key: value for key, value in document.items() if key not in ("media", "approval")} != entry["document"]:
        raise ValueError("Rendered learning package changed")
    expected = {stage["id"]: verified_clip(root, clip_request(entry, stage["turns"], engine), engine)
                for stage in document["stages"]}
    if document["media"]["audio"] != expected:
        raise ValueError("Rendered stages differ from the exact ordered source")
    if "image" in entry and document["media"].get("image") != {key: entry["image"][key] for key in ("path", "sha256")}:
        raise ValueError("Rendered picture differs from the plan")
    validate_output(document, root, plan)
    return document


def approve_task(root: Path, engine, identifier: str, note: str, reviewed_on: str,
                 *, listened: bool, visual: bool, native: bool, phone: bool) -> None:
    review_note(note, reviewed_on)
    with budget.run_lock(root):
        plan = load_plan(root, engine)
        require_preview_approval(root, plan, engine)
        document = verified_package(root, plan, identifier, engine)
        if not listened or not native or not phone or ("visual" in document and not visual):
            raise ValueError("Full-order listening, required picture, native and physical-phone declarations are required")
        document["approval"] = {
            "status": "approved", "contentSha256": tasks.content_hash(document),
            "mediaSha256": tasks.media_hash(document["media"]), "reviewedOn": reviewed_on, "note": note,
        }
        validate_output(document, root, plan)
        budget.write_json(root / "packages" / f"{identifier}.json", document)
        budget.write_json(root / "reviews" / f"{identifier}.json", {
            "planSha256": tasks.canonical_hash(plan), "packageSha256": tasks.canonical_hash(document),
            "listenedAllStages": listened, "visualReviewed": visual, "nativeReviewed": native, "phoneReviewed": phone,
        })


def export(root: Path, engine, identifiers: list[str], replace: bool = False) -> None:
    with budget.run_lock(root):
        plan = load_plan(root, engine)
        require_preview_approval(root, plan, engine)
        if not identifiers or len(set(identifiers)) != len(identifiers):
            raise ValueError("Select distinct, actually approved task IDs")
        content_root = Path(plan["contentRoot"])
        pending = {}
        for identifier in identifiers:
            document = verified_package(root, plan, identifier, engine)
            receipt = budget.read_json(root / "reviews" / f"{identifier}.json")
            if (not validate_output(document, root, plan)
                    or receipt["planSha256"] != tasks.canonical_hash(plan)
                    or receipt["packageSha256"] != tasks.canonical_hash(document)
                    or not all(receipt[key] is True for key in ("listenedAllStages", "nativeReviewed", "phoneReviewed"))
                    or ("visual" in document and receipt["visualReviewed"] is not True)):
                raise ValueError("Complete exact-output approval and device receipts are required")
            destination = content_root / logical_path(document)
            if destination.exists():
                old = budget.read_json(destination)
                if old["exposureId"] != document["exposureId"] or (old != document and not replace):
                    raise ValueError("Existing task differs; never rebind exposure, and use --replace for reviewed revisions")
            pending[destination] = (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            assets = list(document["media"]["audio"].values())
            if "image" in document["media"]:
                assets.append(document["media"]["image"])
            for asset in assets:
                destination = content_root / asset["path"]
                data = (root / asset["path"]).read_bytes()
                if destination.exists() and destination.read_bytes() != data:
                    raise ValueError("Existing content-addressed asset has different bytes")
                pending[destination] = data
        for destination in pending:
            if destination.is_symlink() or not destination.resolve().is_relative_to(content_root.resolve()):
                raise ValueError("Unsafe export destination")
        # Assets first; manifest regeneration is a separate, validated publication step.
        for destination, data in sorted(pending.items(), key=lambda item: item[0].suffix == ".json"):
            destination.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(data)
            try:
                temporary.replace(destination)
            finally:
                temporary.unlink(missing_ok=True)
        print("Exported approved packages only. Validate content, rebuild the manifest and check archive budgets before publishing.")


def write_review_page(root: Path, plan: dict, engine, phase: str) -> None:
    blocks = []
    if phase == "preview":
        groups = []
        for item, (entry, refs) in zip(preview_binding(root, plan, engine), preview_entries(plan)):
            turn = next(turn for turn in entry["document"]["turns"] if turn["id"] == refs[0])
            speaker = next(speaker for speaker in entry["document"]["speakers"] if speaker["id"] == turn["speaker"])
            detail = (f'{speaker["role"]}: {speaker["voice"]}, {speaker["ratePercent"]}%\n'
                      f'{turn["text"]}\nSpoken: {turn.get("spokenText", turn["text"])}\n{turn["translation"]}')
            groups.append((item["selector"], [item["audio"]], f"<pre>{html.escape(detail)}</pre>"))
    else:
        groups = []
        for entry in plan["tasks"]:
            document = verified_package(root, plan, entry["document"]["id"], engine)
            script = "\n".join(f'{turn["id"]}: {turn["text"]}\n{turn["translation"]}' for turn in document["turns"])
            feedback = "\n".join(f'{option["number"]}. {option["label"]}\n{option["translation"]}\n{option["rationale"]}'
                                 for option in document["options"])
            details = f"<pre>{html.escape(script + chr(10) + feedback + chr(10) + document['explanation'])}</pre>"
            if "image" in document["media"]:
                details = f'<img src="{document["media"]["image"]["path"]}" alt="{html.escape(document["visual"]["description"], quote=True)}">' + details
            groups.append((document["title"], [document["media"]["audio"][stage["id"]] for stage in document["stages"]], details))
    for title, clips, details in groups:
        urls = html.escape(json.dumps([clip["path"] for clip in clips]), quote=True)
        controls = "".join(f'<audio controls preload="none" src="{clip["path"]}"></audio>' for clip in clips)
        blocks.append(f'<section><h2>{html.escape(title)}</h2><button data-clips="{urls}">Play complete sequence</button>{controls}{details}</section>')
    page = """<!doctype html><meta charset="utf-8"><title>Unscored author review</title>
<style>body{font:18px sans-serif;max-width:900px;margin:2em auto;padding:1em}section{border-top:1px solid #777;padding:1em 0}audio{display:block;margin:1em 0}img{max-width:100%;width:512px}pre{white-space:pre-wrap}button{font:inherit;padding:.6em}</style>
<h1>AUTHOR REVIEW - UNSCORED</h1><p>Private unapproved outputs. This browser page is not C/D native playback, physical-device acceptance, or a declaration that anyone listened.</p>
<button id="stop">Stop sequence</button><audio id="sequence" controls></audio>""" + "".join(blocks) + """
<script>
const player=document.querySelector('#sequence');let queue=[],cursor=0,generation=0;
function stop(){generation++;queue=[];document.querySelectorAll('audio').forEach(a=>a.pause());}
document.querySelector('#stop').onclick=stop;
document.querySelectorAll('[data-clips]').forEach(button=>button.onclick=()=>{
  stop();
  queue=JSON.parse(button.dataset.clips);cursor=0;next();
});
document.querySelectorAll('audio').forEach(audio=>audio.addEventListener('play',()=>{
  document.querySelectorAll('audio').forEach(other=>{if(other!==audio)other.pause();});
  if(audio!==player){generation++;queue=[];}
}));
function next(){if(cursor<queue.length){const current=generation;player.src=queue[cursor++];player.play().catch(error=>{
  if(current===generation){stop();alert(error.message);}
});}}
player.onended=()=>{if(player.ended)next();};
player.onerror=()=>{if(player.error){stop();alert('Audio failed; this is not listening approval.');}};
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
</script>"""
    (root / f"{phase}-review.html").write_text(page, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, required=True, help="book-skills reference directory")
    parser.add_argument("--run", type=Path, required=True, help="Private run directory outside the content repository")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--content-root", type=Path, required=True)
    plan.add_argument("--inputs", nargs="+", type=Path, required=True)
    plan.add_argument("--image", action="append", default=[], help="task-id=path-to-WebP")
    plan.add_argument("--preview-turn", action="append", required=True, help="task-id:turn-id")
    auth = commands.add_parser("authorize")
    auth.add_argument("--owner-authorized", action="store_true", required=True)
    auth.add_argument("--scope", choices=("preview", "complete"), required=True)
    auth.add_argument("--max-request-units", type=int, required=True)
    auth.add_argument("--max-usd", required=True)
    auth.add_argument("--usd-per-million", required=True, help="Verified applicable USD stock-neural price")
    auth.add_argument("--note", required=True)
    auth.add_argument("--defer-preview-approval", action="store_true",
                      help="Explicitly authorize complete private generation before audition; approval/export gates remain")
    rendering = commands.add_parser("render")
    rendering.add_argument("--allow-paid", action="store_true", required=True)
    rendering.add_argument("--phase", choices=("preview", "complete"), required=True)
    for command in (plan, rendering):
        command.add_argument("--resource", required=True)
        command.add_argument("--subscription", required=True)
    preview = commands.add_parser("approve-preview")
    preview.add_argument("--listened", action="store_true", required=True)
    approval = commands.add_parser("approve-task")
    approval.add_argument("--task-id", required=True)
    for flag in ("listened-all-stages", "native-reviewed", "phone-reviewed"):
        approval.add_argument("--" + flag, action="store_true", required=True)
    approval.add_argument("--visual-reviewed", action="store_true")
    for command in (preview, approval):
        command.add_argument("--note", required=True)
        command.add_argument("--reviewed-on", required=True)
    exporting = commands.add_parser("export")
    exporting.add_argument("--task-id", action="append", required=True)
    exporting.add_argument("--replace", action="store_true")
    verification = commands.add_parser("verify")
    verification.add_argument("--phase", choices=("preview", "complete"), required=True)
    args = parser.parse_args()
    root, engine = args.run.resolve(), load_engine(args.engine)
    if args.command == "plan":
        images = {}
        for value in args.image:
            identifier, path = value.split("=", 1)
            if identifier in images:
                raise ValueError("Duplicate task picture")
            images[identifier] = Path(path)
        create_plan(root, args.content_root.resolve(), args.inputs, images, args.preview_turn, engine, args.resource, args.subscription)
    elif args.command == "authorize":
        budget.authorize(root, tasks.canonical_hash(load_plan(root, engine)), args.scope, args.max_request_units,
                         args.max_usd, args.usd_per_million, args.note, defer_preview_approval=args.defer_preview_approval)
    elif args.command == "render":
        import requests
        with requests.Session() as session:
            render(root, engine, args.resource, args.subscription, args.phase, session)
    elif args.command == "approve-preview":
        approve_preview(root, engine, args.note, args.reviewed_on)
    elif args.command == "approve-task":
        approve_task(root, engine, args.task_id, args.note, args.reviewed_on, listened=args.listened_all_stages,
                     visual=args.visual_reviewed, native=args.native_reviewed, phone=args.phone_reviewed)
    elif args.command == "export":
        export(root, engine, args.task_id, args.replace)
    else:
        with budget.run_lock(root):
            write_review_page(root, load_plan(root, engine), engine, args.phase)
        print("Bytes, stage order and output bindings verified; no listening or device approval inferred.")


if __name__ == "__main__":
    main()
