#!/usr/bin/env python3
"""Inspect, validate, and package approved art for Signal Stage.

The script is intentionally dependency-free. It never edits a source asset and
never overwrites an existing library package.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import mimetypes
import os
import re
import shutil
import struct
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


INGESTION_SCHEMA = "third-signal/signal-stage-ingestion/v1"
RUNTIME_SCHEMA = "third-signal/signal-stage/v1"
READING_MODES = {"focus", "sequence", "stage", "mosaic", "drift", "break"}
LOCK_STATES = {"fluid", "guided", "locked"}
MOTION_CLASSES = {"ambient", "narrative", "editorial", "silence"}
TEXT_POLICIES = {"dynamic", "hybrid", "baked-editorial"}
APPROVAL_STATES = {"approved", "finalized", "locked"}
PASS_STATES = {"approved", "passed", "locked", "available-local", "verified-local", "finalized"}
REJECT_STATES = {"rejected", "superseded", "failed", "inaccessible"}
EVIDENCE_ROLES = {
    "rejected-candidate",
    "phone-qa-unlettered",
    "phone-qa-lettered",
    "qa-report",
    "prompt-record",
    "lettering-source",
    "script",
    "shot-plan",
    "continuity-ledger",
    "web-reader",
}
VISUAL_ROLES = {
    "text-free-master",
    "static-lettered-master",
    "reader-webp",
    "four-panel-web-art",
    "comic-spread",
    "comic-page",
    "wind-spread",
    "hero-master",
    "reader-art",
    "character-design-sheet",
}
VISUAL_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".svg"}
CUE_KINDS = {"dialogue", "caption", "sfx", "document"}
PREFERRED_ZONES = {"upper_left", "upper_right", "lower_left", "lower_right", "center"}
MOBILE_ZONES = {"upper_third", "lower_third", "center"}
ENTER_ANIMATIONS = {"soft_reveal", "cut", "rise"}
EXIT_ANIMATIONS = {"fade", "cut"}
WEIGHTS = {"low", "medium", "high"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "signal-stage-story"


def fail(message: str, code: int = 2) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def read_json_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    blocks = re.findall(r"```(?:json|story-pack-manifest)?\s*\n(.*?)\n```", text, flags=re.DOTALL | re.IGNORECASE)
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and ("story_pack" in data or "assets" in data):
            return data
    fail(f"no usable JSON object found in {path}")
    return {}


def write_json(path: Path, data: dict[str, Any], force: bool = False) -> None:
    if path.exists() and not force:
        fail(f"output already exists: {path}; choose a new path or use --force")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
        return struct.unpack(">II", header[16:24])
    return None


def jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None
        while True:
            marker_start = handle.read(1)
            if not marker_start:
                return None
            if marker_start != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9"}:
                continue
            raw_length = handle.read(2)
            if len(raw_length) != 2:
                return None
            length = struct.unpack(">H", raw_length)[0]
            if marker and marker[0] in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                payload = handle.read(5)
                if len(payload) != 5:
                    return None
                height, width = struct.unpack(">HH", payload[1:5])
                return width, height
            handle.seek(max(length - 2, 0), 1)


def webp_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        data = handle.read(32)
    if len(data) < 16 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    kind = data[12:16]
    if kind == b"VP8X" and len(data) >= 30:
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if kind == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
        bits = int.from_bytes(data[21:25], "little")
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
        return width, height
    if kind == b"VP8 " and len(data) >= 30 and data[23:26] == b"\x9d\x01\x2a":
        width, height = struct.unpack("<HH", data[26:30])
        return width & 0x3FFF, height & 0x3FFF
    return None


def svg_dimensions(path: Path) -> tuple[int, int] | None:
    head = path.read_text(encoding="utf-8", errors="ignore")[:8192]
    width_match = re.search(r"\bwidth=[\"']([0-9.]+)", head)
    height_match = re.search(r"\bheight=[\"']([0-9.]+)", head)
    if width_match and height_match:
        return int(float(width_match.group(1))), int(float(height_match.group(1)))
    viewbox = re.search(r"\bviewBox=[\"']\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)", head)
    if viewbox:
        return int(float(viewbox.group(1))), int(float(viewbox.group(2)))
    return None


def image_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as image:
            return int(image.width), int(image.height)
    except (ImportError, OSError):
        for detector in (png_dimensions, jpeg_dimensions, webp_dimensions):
            try:
                dimensions = detector(path)
            except (OSError, ValueError, struct.error):
                dimensions = None
            if dimensions:
                return dimensions
        if path.suffix.lower() == ".svg":
            return svg_dimensions(path)
    return None


def unique_asset_id(role: str, used: set[str]) -> str:
    base = slugify(role)
    candidate = base
    number = 2
    while candidate in used:
        candidate = f"{base}-{number}"
        number += 1
    used.add(candidate)
    return candidate


def infer_contains_lettering(asset: dict[str, Any], role: str) -> bool | None:
    if "contains_lettering" in asset:
        return bool(asset["contains_lettering"])
    if role in {"text-free-master", "four-panel-web-art"}:
        return False
    if "lettered" in role or role == "reader-webp":
        return True
    return None


def is_visual(role: str, path: Path) -> bool:
    return role in VISUAL_ROLES or path.suffix.lower() in VISUAL_EXTENSIONS


def infer_package_approval(pack: dict[str, Any]) -> tuple[str, str]:
    production_status = str(pack.get("production_status", "")).lower()
    if production_status in {"approved", "finalized", "locked", "published", "production"}:
        state = "finalized" if production_status in {"finalized", "published", "production"} else production_status
        return state, f"story_pack.production_status={production_status}"

    delivery = {str(item.get("name")): str(item.get("status")) for item in pack.get("delivery_targets", []) if isinstance(item, dict)}
    quality = {str(item.get("id")): str(item.get("status")) for item in pack.get("quality_bars", []) if isinstance(item, dict)}
    if delivery.get("production-deployment") == "passed" and quality.get("canon-lock") == "passed":
        return "finalized", "production-deployment and canon-lock passed"
    return "pending", "no package-level final approval found"


def resolve_source_path(asset_path: str, asset_root: Path) -> Path:
    candidate = Path(asset_path).expanduser()
    if not candidate.is_absolute():
        candidate = asset_root / candidate
    return candidate.resolve(strict=False)


def inspect_command(args: argparse.Namespace) -> None:
    source = Path(args.source).expanduser().resolve()
    if not source.is_file():
        fail(f"source manifest not found: {source}")
    document = read_json_document(source)
    pack = document.get("story_pack", document)
    if not isinstance(pack, dict):
        fail("story_pack must be a JSON object")

    package_id = slugify(args.id or str(pack.get("id") or pack.get("title") or source.stem))
    title = str(args.title or pack.get("title") or package_id.replace("-", " ").title())
    asset_root = Path(args.asset_root).expanduser().resolve() if args.asset_root else source.parent
    used_ids: set[str] = set()
    approved_asset_ids = set(args.approved_asset_id or [])
    records: list[dict[str, Any]] = []
    integrity_blockers: list[str] = []

    for index, raw in enumerate(pack.get("assets", []), start=1):
        if not isinstance(raw, dict):
            integrity_blockers.append(f"asset {index} is not an object")
            continue
        role = str(raw.get("role") or raw.get("kind") or f"asset-{index}")
        asset_id = unique_asset_id(str(raw.get("id") or role), used_ids)
        raw_path = str(raw.get("path") or raw.get("source_path") or raw.get("current_local_path") or "")
        resolved = resolve_source_path(raw_path, asset_root) if raw_path else None
        status = str(raw.get("status") or raw.get("binary_state") or "unknown").lower()
        rejected = status in REJECT_STATES or role in EVIDENCE_ROLES or "rejected" in raw_path.lower()
        visual = bool(resolved and is_visual(role, resolved))
        exists = bool(resolved and resolved.is_file())
        binary_state = str(raw.get("binary_state") or ("verified-local" if exists else "needs-export"))
        asset_dna_id = str(raw.get("asset_dna_id") or f"{package_id.upper().replace('-', '_')}::{asset_id.upper().replace('-', '_')}")
        explicitly_approved = asset_id in approved_asset_ids or asset_dna_id in approved_asset_ids
        asset_approval_state = str(
            args.approval if explicitly_approved and args.approval else raw.get("approval_state") or "pending"
        )
        release_eligible = (
            visual
            and exists
            and status in PASS_STATES
            and asset_approval_state in APPROVAL_STATES
            and not rejected
        )
        contains_lettering = infer_contains_lettering(raw, role)

        record: dict[str, Any] = {
            "id": asset_id,
            "asset_dna_id": asset_dna_id,
            "role": role,
            "source_path": str(resolved) if resolved else "",
            "filename": resolved.name if resolved else Path(raw_path).name,
            "mime": str(raw.get("mime") or raw.get("mime_type") or mimetypes.guess_type(raw_path)[0] or "application/octet-stream"),
            "width": None,
            "height": None,
            "bytes": None,
            "sha256": None,
            "status": status,
            "binary_state": binary_state,
            "approval_state": asset_approval_state,
            "canon_state": str(raw.get("canon_state") or "not-applicable"),
            "contains_lettering": contains_lettering,
            "release_eligible": release_eligible,
            "immutable": release_eligible,
        }
        if raw.get("reason"):
            record["reason"] = str(raw["reason"])
        if raw.get("source_role"):
            record["source_role"] = str(raw["source_role"])
        if isinstance(raw.get("origin"), dict):
            record["origin"] = copy.deepcopy(raw["origin"])
        if isinstance(raw.get("lineage"), dict):
            record["lineage"] = copy.deepcopy(raw["lineage"])

        if exists and resolved:
            actual_bytes = resolved.stat().st_size
            actual_sha = sha256_file(resolved)
            dimensions = image_dimensions(resolved) if visual else None
            record["bytes"] = actual_bytes
            record["sha256"] = actual_sha
            record["binary_state"] = "verified-local"
            if dimensions:
                record["width"], record["height"] = dimensions

            declared_sha = raw.get("sha256")
            declared_bytes = raw.get("bytes")
            declared_width = raw.get("width", raw.get("pixel_width"))
            declared_height = raw.get("height", raw.get("pixel_height"))
            mismatches: list[str] = []
            if declared_sha and str(declared_sha).lower() != actual_sha:
                mismatches.append("sha256")
            if declared_bytes is not None and int(declared_bytes) != actual_bytes:
                mismatches.append("bytes")
            if dimensions and declared_width is not None and int(declared_width) != dimensions[0]:
                mismatches.append("width")
            if dimensions and declared_height is not None and int(declared_height) != dimensions[1]:
                mismatches.append("height")
            if mismatches:
                record["integrity"] = "mismatch"
                record["mismatches"] = mismatches
                record["release_eligible"] = False
                record["immutable"] = False
                if visual or explicitly_approved:
                    integrity_blockers.append(f"{asset_id} does not match declared {', '.join(mismatches)}")
                else:
                    record["integrity_note"] = "non-visual evidence changed after the immutable source snapshot"
            else:
                record["integrity"] = "verified"
        else:
            record["integrity"] = "missing"
            if visual and status in PASS_STATES:
                integrity_blockers.append(f"approved visual asset is missing locally: {raw_path}")
        records.append(record)

    inferred_approval, inferred_evidence = infer_package_approval(pack)
    approval_state = args.approval or inferred_approval
    approval_evidence = args.approval_evidence or ("operator assertion" if args.approval else inferred_evidence)

    clean_assets = [item for item in records if item["release_eligible"] and item.get("contains_lettering") is False]
    baked_assets = [item for item in records if item["release_eligible"] and item.get("contains_lettering") is True]
    unknown_text_assets = [item for item in records if item["release_eligible"] and item.get("contains_lettering") is None]

    text_policy = args.text_policy
    if text_policy == "auto":
        text_policy = "dynamic" if clean_assets else "unresolved"

    if text_policy == "dynamic":
        candidates = clean_assets
    elif text_policy in {"hybrid", "baked-editorial"}:
        candidates = baked_assets + clean_assets + unknown_text_assets
    else:
        candidates = clean_assets + baked_assets + unknown_text_assets

    role_priority = {
        "four-panel-web-art": 0,
        "reader-art": 1,
        "text-free-master": 2,
        "wind-spread": 3,
        "comic-spread": 4,
        "comic-page": 5,
        "reader-webp": 6,
        "static-lettered-master": 7,
    }
    candidates.sort(key=lambda item: role_priority.get(str(item["role"]), 50))
    primary = candidates[0] if candidates else None

    blockers = list(integrity_blockers)
    if approval_state not in APPROVAL_STATES:
        blockers.append("package approval is pending or unsupported")
    if not approval_evidence.strip():
        blockers.append("approval evidence is missing")
    if approved_asset_ids and approval_state not in APPROVAL_STATES:
        blockers.append("asset approval override requires an approved package state")
    unknown_approved_ids = approved_asset_ids - {
        item["id"] for item in records
    } - {
        item["asset_dna_id"] for item in records
    }
    if unknown_approved_ids:
        blockers.append(f"approved asset ids are missing from source inventory: {', '.join(sorted(unknown_approved_ids))}")
    if text_policy not in TEXT_POLICIES:
        blockers.append("text policy is unresolved; choose dynamic, hybrid, or baked-editorial")
    if text_policy == "dynamic" and not clean_assets:
        blockers.append("dynamic text requires an approved clean master")
    if not primary:
        blockers.append("no release-eligible visual source is available")

    default_asset_id = primary["id"] if primary else "unresolved-asset"
    runtime = {
        "state": "draft",
        "direction_evidence": "",
        "story": {
            "id": package_id,
            "title": title,
            "chapter": "Library entry",
            "subtitle": "",
            "credit": "A Third Signal production",
            "profile": {
                "id": args.property,
                "label": "Direction profile pending",
                "accent": "#c9a35f",
                "surface": "#08090a",
                "text": "#ede4d3",
                "motion_doctrine": "Use motion only to reveal information, redirect attention, or deepen atmosphere.",
            },
            "audio": {
                "id": "ambient-disabled",
                "label": "Ambient sound",
                "type": "generated-rain",
                "default_on": False,
            },
        },
        "beats": [
            {
                "id": package_id,
                "order": 1,
                "scene": "Direction pending",
                "pages": "Source package",
                "title": title,
                "mode": "focus",
                "lock": "locked",
                "scroll_screens": 2.4,
                "asset_id": default_asset_id,
                "alt": "",
                "motion": {"dominant": "editorial", "ambient": [], "intensity": 1},
                "desktop": {"object_position": "50% 50%", "start_scale": 1.0, "end_scale": 1.06},
                "mobile": {"object_position": "50% 50%", "start_scale": 1.08, "end_scale": 1.18},
                "shots": [],
                "anchors": [
                    {"id": "canvas-center", "label": "Canvas center", "x": 50, "y": 50, "mobile_x": 50, "mobile_y": 50, "safe_radius": 10}
                ],
                "cues": [],
                "direction": "",
                "reduced_motion": "",
            }
        ],
    }

    gates = [
        {"id": "approval", "status": "passed" if approval_state in APPROVAL_STATES else "blocked", "evidence": approval_evidence},
        {"id": "asset-integrity", "status": "passed" if not integrity_blockers else "blocked", "evidence": "local bytes, dimensions, and hashes inspected"},
        {"id": "release-source", "status": "passed" if primary else "blocked", "evidence": primary["id"] if primary else "none"},
        {"id": "text-policy", "status": "passed" if text_policy in TEXT_POLICIES and not (text_policy == "dynamic" and not clean_assets) else "blocked", "evidence": text_policy},
        {"id": "direction", "status": "pending", "evidence": "runtime.state=draft"},
        {"id": "publication", "status": "not-authorized", "evidence": "ingestion does not authorize live integration or deployment"},
    ]

    spec = {
        "schema": INGESTION_SCHEMA,
        "created_at": utc_now(),
        "package": {
            "id": package_id,
            "title": title,
            "property": args.property,
            "version": str(pack.get("version") or "1.0.0"),
            "source_manifest": str(source),
            "source_manifest_sha256": sha256_file(source),
            "source_status": str(pack.get("production_status") or "unspecified"),
            "canonical": pack.get("canonical"),
            "dispatch_number": pack.get("dispatch_number"),
        },
        "approval": {"state": approval_state, "evidence": approval_evidence},
        "policy": {
            "text": text_policy,
            "approved_pixels_immutable": True,
            "derivatives_only": True,
            "allow_generation": False,
            "rejected_assets": "evidence-only",
            "publication_authorized": False,
        },
        "assets": records,
        "runtime": runtime,
        "gates": gates,
        "state": "blocked" if blockers else "ready-for-direction",
        "blockers": blockers,
    }
    write_json(Path(args.output).expanduser().resolve(), spec, force=args.force)
    print(json.dumps({"state": spec["state"], "output": str(Path(args.output).expanduser().resolve()), "blockers": blockers}, indent=2))


def require_keys(value: dict[str, Any], keys: list[str], prefix: str, errors: list[str]) -> None:
    for key in keys:
        if key not in value or value[key] is None or value[key] == "":
            errors.append(f"{prefix}.{key} is required")


def percent(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, (int, float)) or not 0 <= float(value) <= 100:
        errors.append(f"{label} must be a number from 0 to 100")


def validate_spec(spec: dict[str, Any], production_ready: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if spec.get("schema") != INGESTION_SCHEMA:
        errors.append(f"schema must be {INGESTION_SCHEMA}")

    package = spec.get("package")
    approval = spec.get("approval")
    policy = spec.get("policy")
    runtime = spec.get("runtime")
    assets = spec.get("assets")
    if not isinstance(package, dict):
        errors.append("package must be an object")
        package = {}
    if not isinstance(approval, dict):
        errors.append("approval must be an object")
        approval = {}
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
        policy = {}
    if not isinstance(runtime, dict):
        errors.append("runtime must be an object")
        runtime = {}
    if not isinstance(assets, list) or not assets:
        errors.append("assets must be a non-empty array")
        assets = []

    require_keys(package, ["id", "title", "property", "version", "source_manifest", "source_manifest_sha256"], "package", errors)
    source_manifest = Path(str(package.get("source_manifest") or ""))
    if not source_manifest.is_file():
        errors.append("package.source_manifest is missing locally")
    elif sha256_file(source_manifest) != package.get("source_manifest_sha256"):
        errors.append("package.source_manifest_sha256 no longer matches the source manifest")
    if approval.get("state") not in APPROVAL_STATES:
        errors.append("approval.state must be approved, finalized, or locked")
    if not str(approval.get("evidence") or "").strip():
        errors.append("approval.evidence is required")
    if policy.get("text") not in TEXT_POLICIES:
        errors.append("policy.text must be dynamic, hybrid, or baked-editorial")
    for flag in ["approved_pixels_immutable", "derivatives_only"]:
        if policy.get(flag) is not True:
            errors.append(f"policy.{flag} must be true")
    if policy.get("allow_generation") is not False:
        errors.append("policy.allow_generation must be false")

    asset_index: dict[str, dict[str, Any]] = {}
    for index, asset in enumerate(assets):
        label = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{label} must be an object")
            continue
        require_keys(asset, ["id", "role", "source_path", "filename", "status", "integrity"], label, errors)
        asset_id = str(asset.get("id") or "")
        if asset_id in asset_index:
            errors.append(f"duplicate asset id: {asset_id}")
        asset_index[asset_id] = asset
        if asset.get("release_eligible") and (asset.get("status") in REJECT_STATES or asset.get("role") in EVIDENCE_ROLES):
            errors.append(f"{asset_id} is evidence/rejected and cannot be release eligible")
        if asset.get("release_eligible"):
            source_path = Path(str(asset.get("source_path") or ""))
            if not source_path.is_file():
                errors.append(f"release asset missing: {asset_id}")
                continue
            actual_sha = sha256_file(source_path)
            actual_bytes = source_path.stat().st_size
            if actual_sha != asset.get("sha256"):
                errors.append(f"release asset hash changed: {asset_id}")
            if actual_bytes != asset.get("bytes"):
                errors.append(f"release asset size changed: {asset_id}")

    story = runtime.get("story") if isinstance(runtime.get("story"), dict) else {}
    beats = runtime.get("beats") if isinstance(runtime.get("beats"), list) else []
    if production_ready:
        if runtime.get("state") not in {"guided", "approved"}:
            errors.append("runtime.state must be guided or approved for production")
        if not str(runtime.get("direction_evidence") or "").strip():
            errors.append("runtime.direction_evidence is required for production")
        require_keys(story, ["id", "title", "chapter", "subtitle", "credit", "profile", "audio"], "runtime.story", errors)
        profile = story.get("profile") if isinstance(story.get("profile"), dict) else {}
        require_keys(profile, ["id", "label", "accent", "surface", "text", "motion_doctrine"], "runtime.story.profile", errors)
        audio = story.get("audio") if isinstance(story.get("audio"), dict) else {}
        require_keys(audio, ["id", "label", "type", "default_on"], "runtime.story.audio", errors)
        if audio.get("type") != "generated-rain":
            errors.append("runtime.story.audio.type must be generated-rain for the current Signal Stage v1 adapter")
        if not beats:
            errors.append("runtime.beats must contain at least one beat")

    seen_beat_ids: set[str] = set()
    seen_orders: set[int] = set()
    for index, beat in enumerate(beats):
        label = f"runtime.beats[{index}]"
        if not isinstance(beat, dict):
            errors.append(f"{label} must be an object")
            continue
        if production_ready:
            require_keys(
                beat,
                ["id", "order", "scene", "pages", "title", "mode", "lock", "scroll_screens", "asset_id", "alt", "motion", "desktop", "mobile", "shots", "anchors", "cues", "direction", "reduced_motion"],
                label,
                errors,
            )
        beat_id = str(beat.get("id") or "")
        if beat_id in seen_beat_ids:
            errors.append(f"duplicate beat id: {beat_id}")
        seen_beat_ids.add(beat_id)
        order = beat.get("order")
        if isinstance(order, int):
            if order in seen_orders:
                errors.append(f"duplicate beat order: {order}")
            seen_orders.add(order)
        elif production_ready:
            errors.append(f"{label}.order must be an integer")
        if beat.get("mode") not in READING_MODES:
            errors.append(f"{label}.mode is unsupported")
        if beat.get("lock") not in LOCK_STATES:
            errors.append(f"{label}.lock is unsupported")
        asset_id = str(beat.get("asset_id") or "")
        selected = asset_index.get(asset_id)
        if not selected:
            errors.append(f"{label}.asset_id does not exist: {asset_id}")
        elif not selected.get("release_eligible"):
            errors.append(f"{label}.asset_id is not release eligible: {asset_id}")
        elif policy.get("text") == "dynamic" and selected.get("contains_lettering") is not False:
            errors.append(f"{label} uses a lettered/unknown asset under dynamic text policy")

        motion = beat.get("motion") if isinstance(beat.get("motion"), dict) else {}
        if motion.get("dominant") not in MOTION_CLASSES:
            errors.append(f"{label}.motion.dominant is unsupported")
        intensity = motion.get("intensity")
        if not isinstance(intensity, int) or intensity < 0 or intensity > 3:
            errors.append(f"{label}.motion.intensity must be an integer from 0 to 3")

        for viewport_name in ["desktop", "mobile"]:
            viewport = beat.get(viewport_name) if isinstance(beat.get(viewport_name), dict) else {}
            require_keys(viewport, ["object_position", "start_scale", "end_scale"], f"{label}.{viewport_name}", errors)
            for scale_name in ["start_scale", "end_scale"]:
                scale = viewport.get(scale_name)
                if not isinstance(scale, (int, float)) or not 0.5 <= float(scale) <= 3:
                    errors.append(f"{label}.{viewport_name}.{scale_name} must be between 0.5 and 3")

        anchors = beat.get("anchors") if isinstance(beat.get("anchors"), list) else []
        if production_ready and not anchors:
            errors.append(f"{label}.anchors must contain at least one anchor")
        anchor_ids: set[str] = set()
        for anchor_index, anchor in enumerate(anchors):
            anchor_label = f"{label}.anchors[{anchor_index}]"
            if not isinstance(anchor, dict):
                errors.append(f"{anchor_label} must be an object")
                continue
            require_keys(anchor, ["id", "label", "x", "y"], anchor_label, errors)
            anchor_id = str(anchor.get("id") or "")
            if anchor_id in anchor_ids:
                errors.append(f"duplicate anchor id in {beat_id}: {anchor_id}")
            anchor_ids.add(anchor_id)
            percent(anchor.get("x"), f"{anchor_label}.x", errors)
            percent(anchor.get("y"), f"{anchor_label}.y", errors)
            if "mobile_x" in anchor:
                percent(anchor.get("mobile_x"), f"{anchor_label}.mobile_x", errors)
            if "mobile_y" in anchor:
                percent(anchor.get("mobile_y"), f"{anchor_label}.mobile_y", errors)

        shots = beat.get("shots") if isinstance(beat.get("shots"), list) else []
        if production_ready and beat.get("mode") in {"sequence", "mosaic"} and len(shots) < 2:
            errors.append(f"{label}.shots needs at least two shots for {beat.get('mode')} mode")

        cues = beat.get("cues") if isinstance(beat.get("cues"), list) else []
        progress_values: list[float] = []
        for cue_index, cue in enumerate(cues):
            cue_label = f"{label}.cues[{cue_index}]"
            if not isinstance(cue, dict):
                errors.append(f"{cue_label} must be an object")
                continue
            require_keys(cue, ["id", "kind", "speaker", "text", "preferred_zone", "mobile_fallback", "trigger", "animation", "priority", "emotional_weight", "voice_sync"], cue_label, errors)
            if cue.get("kind") not in CUE_KINDS:
                errors.append(f"{cue_label}.kind is unsupported")
            if cue.get("preferred_zone") not in PREFERRED_ZONES:
                errors.append(f"{cue_label}.preferred_zone is unsupported")
            if cue.get("mobile_fallback") not in MOBILE_ZONES:
                errors.append(f"{cue_label}.mobile_fallback is unsupported")
            anchor_id = cue.get("anchor")
            if anchor_id and anchor_id not in anchor_ids:
                errors.append(f"{cue_label}.anchor does not exist in beat: {anchor_id}")
            trigger = cue.get("trigger") if isinstance(cue.get("trigger"), dict) else {}
            progress = trigger.get("progress")
            if trigger.get("type") != "scroll" or not isinstance(progress, (int, float)) or not 0 <= float(progress) <= 1:
                errors.append(f"{cue_label}.trigger must be scroll progress from 0 to 1")
            elif isinstance(progress, (int, float)):
                progress_values.append(float(progress))
            animation = cue.get("animation") if isinstance(cue.get("animation"), dict) else {}
            if animation.get("enter") not in ENTER_ANIMATIONS or animation.get("exit") not in EXIT_ANIMATIONS:
                errors.append(f"{cue_label}.animation is unsupported")
            if not isinstance(animation.get("hold_ms"), int) or animation.get("hold_ms", 0) <= 0:
                errors.append(f"{cue_label}.animation.hold_ms must be a positive integer")
            if cue.get("emotional_weight") not in WEIGHTS:
                errors.append(f"{cue_label}.emotional_weight is unsupported")
        if progress_values != sorted(progress_values):
            warnings.append(f"{label}.cues are not ordered by trigger progress")
        if policy.get("text") == "baked-editorial" and cues:
            warnings.append(f"{label} has cues under baked-editorial; confirm no baked wording is duplicated")

    if production_ready and spec.get("state") == "blocked":
        errors.append("spec.state is blocked")
    return errors, warnings


def validate_command(args: argparse.Namespace) -> None:
    spec_path = Path(args.spec).expanduser().resolve()
    if not spec_path.is_file():
        fail(f"spec not found: {spec_path}")
    spec = read_json_document(spec_path)
    errors, warnings = validate_spec(spec, args.production_ready)
    report = {"valid": not errors, "production_ready": args.production_ready and not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


def safe_output_name(asset_id: str, source: Path) -> str:
    return f"{slugify(asset_id)}{source.suffix.lower()}"


def copy_verified(source: Path, destination: Path, expected_sha: str) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    copied_sha = sha256_file(destination)
    if copied_sha != expected_sha:
        fail(f"copy verification failed for {destination}")
    return {"path": str(destination), "bytes": destination.stat().st_size, "sha256": copied_sha}


def package_command(args: argparse.Namespace) -> None:
    spec_path = Path(args.spec).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not spec_path.is_file():
        fail(f"spec not found: {spec_path}")
    if output.exists():
        fail(f"package output already exists: {output}; use a new versioned directory")
    spec = read_json_document(spec_path)
    errors, warnings = validate_spec(spec, production_ready=True)
    if errors:
        print(json.dumps({"valid": False, "errors": errors, "warnings": warnings}, indent=2), file=sys.stderr)
        raise SystemExit(1)

    package_id = slugify(str(spec["package"]["id"]))
    asset_index = {asset["id"]: asset for asset in spec["assets"]}
    referenced_ids = list(dict.fromkeys(str(beat["asset_id"]) for beat in spec["runtime"]["beats"]))
    temp_parent = output.parent
    temp_parent.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix=f".{output.name}.", dir=str(temp_parent)))
    try:
        source_dir = temp_root / "source"
        public_entry_dir = temp_root / "public" / "library" / package_id
        runtime_dir = public_entry_dir / "assets"
        source_dir.mkdir(parents=True)
        runtime_dir.mkdir(parents=True)
        runtime_asset_paths: dict[str, str] = {}
        provenance_assets: list[dict[str, Any]] = []

        public_prefix = "/" + args.public_prefix.strip("/") if args.public_prefix.strip("/") else ""
        for asset_id in referenced_ids:
            asset = asset_index[asset_id]
            source = Path(asset["source_path"])
            output_name = safe_output_name(asset_id, source)
            source_copy = source_dir / output_name
            runtime_copy = runtime_dir / output_name
            source_info = copy_verified(source, source_copy, asset["sha256"])
            runtime_info = copy_verified(source, runtime_copy, asset["sha256"])
            runtime_asset_paths[asset_id] = f"{public_prefix}/{package_id}/assets/{output_name}"
            provenance_assets.append(
                {
                    "asset_id": asset_id,
                    "asset_dna_id": asset.get("asset_dna_id"),
                    "role": asset["role"],
                    "origin": asset.get("origin"),
                    "lineage": asset.get("lineage"),
                    "original_path": asset["source_path"],
                    "original_sha256": asset["sha256"],
                    "source_copy": {**source_info, "path": f"source/{output_name}"},
                    "runtime_copy": {**runtime_info, "path": f"public/library/{package_id}/assets/{output_name}"},
                    "transformation": "byte-identical copy",
                }
            )

        story = copy.deepcopy(spec["runtime"]["story"])
        story_beats = []
        for beat in spec["runtime"]["beats"]:
            runtime_beat = copy.deepcopy(beat)
            asset_id = runtime_beat.pop("asset_id")
            runtime_beat["image"] = runtime_asset_paths[asset_id]
            story_beats.append(runtime_beat)
        story["beats"] = story_beats
        runtime_manifest = {"schema": RUNTIME_SCHEMA, "story": story}
        provenance = {
            "schema": "third-signal/signal-stage-provenance/v1",
            "created_at": utc_now(),
            "package_id": package_id,
            "ingestion_spec": str(spec_path),
            "ingestion_spec_sha256": sha256_file(spec_path),
            "source_manifest": spec["package"]["source_manifest"],
            "source_manifest_sha256": spec["package"]["source_manifest_sha256"],
            "approval": spec["approval"],
            "policy": spec["policy"],
            "assets": provenance_assets,
            "warnings": warnings,
            "publication_authorized": False,
        }
        write_json(temp_root / "ingestion.json", spec)
        write_json(public_entry_dir / "story.json", runtime_manifest)
        write_json(temp_root / "provenance.json", provenance)
        temp_root.replace(output)
    except Exception:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise

    result = {
        "packaged": True,
        "output": str(output),
        "story_manifest": str(output / "public" / "library" / package_id / "story.json"),
        "asset_count": len(referenced_ids),
        "beat_count": len(spec["runtime"]["beats"]),
        "warnings": warnings,
        "publication_authorized": False,
    }
    print(json.dumps(result, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare approved art for the Signal Stage library")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Create a non-mutating ingestion spec from a Story Pack manifest")
    inspect_parser.add_argument("--source", required=True, help="Raw JSON or Markdown Story Pack manifest")
    inspect_parser.add_argument("--output", required=True, help="Destination ingestion JSON")
    inspect_parser.add_argument("--asset-root", help="Verified root used to resolve relative asset paths")
    inspect_parser.add_argument("--property", default="wind", help="IP or direction profile slug")
    inspect_parser.add_argument("--id", help="Override package id")
    inspect_parser.add_argument("--title", help="Override package title")
    inspect_parser.add_argument("--text-policy", choices=["auto", *sorted(TEXT_POLICIES)], default="auto")
    inspect_parser.add_argument("--approval", choices=sorted(APPROVAL_STATES), help="Explicit approval supplied by user or approval artifact")
    inspect_parser.add_argument("--approval-evidence", help="Named artifact or instruction supporting explicit approval")
    inspect_parser.add_argument(
        "--approved-asset-id",
        action="append",
        default=[],
        help="Asset inventory id or Asset DNA id explicitly covered by the approval; repeat for multiple assets",
    )
    inspect_parser.add_argument("--force", action="store_true", help="Replace only the output spec; never touches source assets")
    inspect_parser.set_defaults(func=inspect_command)

    validate_parser = subparsers.add_parser("validate", help="Validate an ingestion spec and its source assets")
    validate_parser.add_argument("--spec", required=True)
    validate_parser.add_argument("--production-ready", action="store_true", help="Require complete approved direction metadata")
    validate_parser.set_defaults(func=validate_command)

    package_parser = subparsers.add_parser("package", help="Create a versioned Signal Stage library pack")
    package_parser.add_argument("--spec", required=True)
    package_parser.add_argument("--output", required=True, help="New output directory; existing directories are refused")
    package_parser.add_argument("--public-prefix", default="library", help="Browser URL prefix before package id")
    package_parser.set_defaults(func=package_command)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
