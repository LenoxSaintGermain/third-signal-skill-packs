#!/usr/bin/env python3
"""Capture a generated creative binary and its creation-time receipt.

The command is local and byte-preserving. It refuses to overwrite an existing
source file or receipt, records unavailable generation fields as unknown, and
does not change approval, canon, desk, or release state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import shutil
import struct
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_dimensions(path: Path) -> tuple[int, int] | None:
    """Read common image dimensions without decoding or rewriting the asset."""
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as image:
            return int(image.width), int(image.height)
    except (ImportError, OSError):
        pass

    with path.open("rb") as handle:
        header = handle.read(24)
    if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
        return struct.unpack(">II", header[16:24])

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
            if marker and marker[0] in {
                0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
            }:
                payload = handle.read(5)
                if len(payload) != 5:
                    return None
                height, width = struct.unpack(">HH", payload[1:5])
                return width, height
            handle.seek(max(length - 2, 0), 1)


def write_json_once(path: Path, document: dict[str, Any]) -> None:
    if path.exists():
        raise FileExistsError(f"output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def with_status(value: str | None, missing_status: str = "not recorded or exposed") -> dict[str, Any]:
    return {"value": value, "status": "recorded" if value is not None else missing_status}


def capture(args: argparse.Namespace) -> Path:
    source = Path(args.source).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"source file does not exist: {source}")

    original_filename = args.original_filename or source.name
    if Path(original_filename).name != original_filename:
        raise ValueError("--original-filename must be a basename")

    destination_dir = Path(args.destination_dir).expanduser().resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / original_filename
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    receipt_path = destination_dir / "receipts" / f"{args.asset_dna_id}.json"
    if receipt_path.exists():
        raise FileExistsError(f"receipt already exists: {receipt_path}")

    source_sha = sha256_file(source)
    shutil.copyfile(source, destination)
    captured_sha = sha256_file(destination)
    if captured_sha != source_sha:
        destination.unlink(missing_ok=True)
        raise IOError("byte-preserving capture failed: destination checksum differs from source")

    prompt = args.prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).expanduser().resolve().read_text(encoding="utf-8")
    dimensions = image_dimensions(source)
    receipt = {
        "schema_version": 1,
        "receipt_type": "source_capture",
        "capture_context": args.capture_context,
        "asset_dna_id": args.asset_dna_id,
        "captured_at": utc_now(),
        "binary": {
            "original_filename": original_filename,
            "source_path_observed": str(source),
            "captured_path": str(destination),
            "byte_size": destination.stat().st_size,
            "mime_type": mimetypes.guess_type(original_filename)[0] or "application/octet-stream",
            "dimensions": {"width": dimensions[0], "height": dimensions[1]} if dimensions else None,
            "sha256": captured_sha,
            "copy_method": "byte-preserving copy; no decode, resize, recompression, or rename",
        },
        "origin": {
            "conversation_id": args.conversation_id,
            "turn_id": args.turn_id,
            "tool": args.tool,
            "file_id": args.file_id,
        },
        "generation": {
            "prompt": with_status(prompt),
            "model": with_status(args.model),
            "seed": with_status(args.seed),
            "gen_id": with_status(args.gen_id),
            "parent_gen_id": with_status(args.parent_gen_id),
        },
        "lineage": {
            "parent_asset_dna_ids": args.parent_asset_dna_id,
            "relationships": args.relationship,
        },
        "state": {
            "binary_availability": "verified-local",
            "approval": args.approval_state,
            "canon": args.canon_state,
            "release_eligible": False,
        },
    }
    write_json_once(receipt_path, receipt)
    return receipt_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination-dir", required=True)
    parser.add_argument("--asset-dna-id", required=True)
    parser.add_argument("--conversation-id", required=True)
    parser.add_argument("--turn-id")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--capture-context", default="creation-time", choices=["creation-time", "manual-export-recovery"])
    parser.add_argument("--original-filename")
    parser.add_argument("--file-id")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--model")
    parser.add_argument("--seed")
    parser.add_argument("--gen-id")
    parser.add_argument("--parent-gen-id")
    parser.add_argument("--parent-asset-dna-id", action="append", default=[])
    parser.add_argument("--relationship", action="append", default=[])
    parser.add_argument("--approval-state", default="pending")
    parser.add_argument("--canon-state", default="proposed")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        receipt_path = capture(args)
    except (FileNotFoundError, FileExistsError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"captured: {receipt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
