#!/usr/bin/env python3
"""Durable story-level queue and approval gates for Signal Publishing."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
ITEM_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ACTIONABLE_STATES = {"inbox", "source-approved"}


class DeskError(RuntimeError):
    """Raised when a desk operation would violate the workflow contract."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _items_dir(root: Path) -> Path:
    return Path(root) / "items"


def item_path(root: Path, item_id: str) -> Path:
    if not ITEM_ID_RE.fullmatch(item_id):
        raise DeskError(f"invalid item id {item_id!r}; use lowercase hyphen-case")
    return _items_dir(root) / f"{item_id}.json"


def _atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def load_item(root: Path, item_id: str) -> dict[str, Any]:
    path = item_path(root, item_id)
    if not path.is_file():
        raise DeskError(f"desk item {item_id!r} does not exist")
    return json.loads(path.read_text(encoding="utf-8"))


def list_items(root: Path) -> list[dict[str, Any]]:
    directory = _items_dir(root)
    if not directory.is_dir():
        return []
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("*.json"))]


def _event(*, actor: str, action: str, from_state: str | None, to_state: str,
           evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    event: dict[str, Any] = {
        "at": _now(),
        "actor": actor,
        "action": action,
        "from_state": from_state,
        "to_state": to_state,
    }
    if evidence:
        event["evidence"] = copy.deepcopy(evidence)
    return event


def intake(*, root: Path, item_id: str, title: str, property_slug: str,
           source: dict[str, Any], priority: int = 50,
           requested_by: str = "operator") -> dict[str, Any]:
    path = item_path(root, item_id)
    if not title.strip():
        raise DeskError("title is required")
    if not property_slug.strip():
        raise DeskError("property slug is required")
    if not isinstance(priority, int) or not 0 <= priority <= 100:
        raise DeskError("priority must be an integer from 0 to 100")
    if not source.get("type"):
        raise DeskError("source.type is required")

    if path.exists():
        existing = load_item(root, item_id)
        if existing.get("source") != source:
            raise DeskError(f"desk item {item_id!r} already exists with a different source")
        return existing

    item = {
        "schema_version": SCHEMA_VERSION,
        "id": item_id,
        "title": title.strip(),
        "property_slug": property_slug.strip(),
        "priority": priority,
        "source": copy.deepcopy(source),
        "state": "inbox",
        "artifacts": {},
        "gates": {"source_approval": None, "release_approval": None},
        "blockers": [],
        "events": [
            _event(
                actor=requested_by,
                action="intake",
                from_state=None,
                to_state="inbox",
                evidence={"source_type": source["type"]},
            )
        ],
    }
    _atomic_write(path, item)
    return item


def next_item(root: Path) -> dict[str, Any] | None:
    items = [item for item in list_items(root) if item.get("state") in ACTIONABLE_STATES]
    if not items:
        return None
    items.sort(key=lambda item: (-int(item.get("priority", 0)), item["id"]))
    return items[0]


def _transition(*, root: Path, item_id: str, actor: str, action: str,
                allowed_states: set[str], to_state: str,
                evidence: dict[str, Any] | None = None,
                mutate=None) -> dict[str, Any]:
    current = load_item(root, item_id)
    from_state = str(current.get("state"))
    if from_state not in allowed_states:
        expected = " or ".join(sorted(allowed_states))
        raise DeskError(f"{action} requires state {expected}; found {from_state}")
    updated = copy.deepcopy(current)
    if mutate is not None:
        mutate(updated)
    updated["state"] = to_state
    updated["events"].append(
        _event(
            actor=actor,
            action=action,
            from_state=from_state,
            to_state=to_state,
            evidence=evidence,
        )
    )
    _atomic_write(item_path(root, item_id), updated)
    return updated


def _existing_path(value: Path | str, label: str) -> Path:
    path = Path(value).expanduser()
    if not path.exists():
        raise DeskError(f"{label} does not exist: {path}")
    return path


def _required_evidence(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise DeskError(f"{label} evidence is required")
    return cleaned


def begin_preflight(root: Path, item_id: str, *, actor: str) -> dict[str, Any]:
    def mutate(item: dict[str, Any]) -> None:
        item["blockers"] = []

    return _transition(
        root=root,
        item_id=item_id,
        actor=actor,
        action="begin-preflight",
        allowed_states={"inbox", "needs-recovery"},
        to_state="preflight-running",
        mutate=mutate,
    )


def complete_preflight(root: Path, item_id: str, *, actor: str,
                       package_path: Path | str,
                       blockers: list[str] | None = None) -> dict[str, Any]:
    package = _existing_path(package_path, "source package")
    clean_blockers = [blocker.strip() for blocker in (blockers or []) if blocker.strip()]
    destination = "needs-recovery" if clean_blockers else "operator-review"

    def mutate(item: dict[str, Any]) -> None:
        item["artifacts"]["source_package"] = str(package)
        item["blockers"] = clean_blockers

    return _transition(
        root=root,
        item_id=item_id,
        actor=actor,
        action="complete-preflight",
        allowed_states={"preflight-running"},
        to_state=destination,
        evidence={"source_package": str(package), "blocker_count": len(clean_blockers)},
        mutate=mutate,
    )


def approve_source(root: Path, item_id: str, *, actor: str, evidence: str) -> dict[str, Any]:
    approval_evidence = _required_evidence(evidence, "source approval")

    def mutate(item: dict[str, Any]) -> None:
        if item.get("blockers"):
            raise DeskError("source approval is blocked until all recovery blockers are resolved")
        item["gates"]["source_approval"] = {
            "approved_by": actor,
            "approved_at": _now(),
            "evidence": approval_evidence,
        }

    return _transition(
        root=root,
        item_id=item_id,
        actor=actor,
        action="approve-source",
        allowed_states={"operator-review"},
        to_state="source-approved",
        evidence={"approval": approval_evidence},
        mutate=mutate,
    )


def begin_production(root: Path, item_id: str, *, actor: str) -> dict[str, Any]:
    return _transition(
        root=root,
        item_id=item_id,
        actor=actor,
        action="begin-production",
        allowed_states={"source-approved"},
        to_state="production-running",
    )


def submit_uat(root: Path, item_id: str, *, actor: str, preview: str,
               report_path: Path | str, ingestion_spec: Path | str,
               library_pack: Path | str) -> dict[str, Any]:
    preview_value = preview.strip()
    if not preview_value:
        raise DeskError("UAT preview is required")
    report = _existing_path(report_path, "UAT report")
    ingestion = _existing_path(ingestion_spec, "ingestion spec")
    package = _existing_path(library_pack, "library pack")

    def mutate(item: dict[str, Any]) -> None:
        item["artifacts"].update(
            {
                "ingestion_spec": str(ingestion),
                "library_pack": str(package),
                "uat_preview": preview_value,
                "uat_report": str(report),
            }
        )

    return _transition(
        root=root,
        item_id=item_id,
        actor=actor,
        action="submit-uat",
        allowed_states={"production-running"},
        to_state="uat-review",
        evidence={"preview": preview_value, "report": str(report)},
        mutate=mutate,
    )


def approve_release(root: Path, item_id: str, *, actor: str, evidence: str) -> dict[str, Any]:
    approval_evidence = _required_evidence(evidence, "release approval")

    def mutate(item: dict[str, Any]) -> None:
        item["gates"]["release_approval"] = {
            "approved_by": actor,
            "approved_at": _now(),
            "evidence": approval_evidence,
        }

    return _transition(
        root=root,
        item_id=item_id,
        actor=actor,
        action="approve-release",
        allowed_states={"uat-review"},
        to_state="release-approved",
        evidence={"approval": approval_evidence},
        mutate=mutate,
    )


def record_publish(root: Path, item_id: str, *, actor: str,
                   receipt: Path | str) -> dict[str, Any]:
    receipt_value = str(receipt).strip()
    if not receipt_value:
        raise DeskError("publication receipt is required")
    if "://" not in receipt_value:
        receipt_value = str(_existing_path(receipt_value, "publication receipt"))

    def mutate(item: dict[str, Any]) -> None:
        item["artifacts"]["publication_receipt"] = receipt_value

    return _transition(
        root=root,
        item_id=item_id,
        actor=actor,
        action="record-publish",
        allowed_states={"release-approved"},
        to_state="published",
        evidence={"receipt": receipt_value},
        mutate=mutate,
    )


def _json_print(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def _source_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.conversation:
        return {
            "type": "chatgpt-conversation",
            "conversation_id": args.conversation,
            "uri": f"chatgpt-conversation://{args.conversation}",
        }
    if args.manifest:
        return {"type": "local-manifest", "path": str(Path(args.manifest).expanduser())}
    if args.folder:
        return {"type": "local-folder", "path": str(Path(args.folder).expanduser())}
    raise DeskError("provide --conversation, --manifest, or --folder")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate the Signal Publishing Desk queue")
    parser.add_argument("--root", type=Path, default=Path("publishing-desk"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    intake_parser = subparsers.add_parser("intake", help="Add an item idempotently")
    intake_parser.add_argument("--id", required=True)
    intake_parser.add_argument("--title", required=True)
    intake_parser.add_argument("--property", required=True)
    source_group = intake_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--conversation")
    source_group.add_argument("--manifest")
    source_group.add_argument("--folder")
    intake_parser.add_argument("--priority", type=int, default=50)
    intake_parser.add_argument("--by", default="operator")

    subparsers.add_parser("list", help="List desk items")
    show_parser = subparsers.add_parser("show", help="Show one desk item")
    show_parser.add_argument("--id", required=True)
    subparsers.add_parser("next", help="Return the highest-priority agent-actionable item")

    begin_preflight_parser = subparsers.add_parser("begin-preflight")
    begin_preflight_parser.add_argument("--id", required=True)
    begin_preflight_parser.add_argument("--by", default="publishing-desk-agent")

    complete_preflight_parser = subparsers.add_parser("complete-preflight")
    complete_preflight_parser.add_argument("--id", required=True)
    complete_preflight_parser.add_argument("--package", type=Path, required=True)
    complete_preflight_parser.add_argument("--blocker", action="append", default=[])
    complete_preflight_parser.add_argument("--by", default="publishing-desk-agent")

    approve_source_parser = subparsers.add_parser("approve-source")
    approve_source_parser.add_argument("--id", required=True)
    approve_source_parser.add_argument("--evidence", required=True)
    approve_source_parser.add_argument("--by", required=True)

    begin_production_parser = subparsers.add_parser("begin-production")
    begin_production_parser.add_argument("--id", required=True)
    begin_production_parser.add_argument("--by", default="signal-stage-agent")

    submit_uat_parser = subparsers.add_parser("submit-uat")
    submit_uat_parser.add_argument("--id", required=True)
    submit_uat_parser.add_argument("--preview", required=True)
    submit_uat_parser.add_argument("--report", type=Path, required=True)
    submit_uat_parser.add_argument("--ingestion-spec", type=Path, required=True)
    submit_uat_parser.add_argument("--library-pack", type=Path, required=True)
    submit_uat_parser.add_argument("--by", default="signal-stage-agent")

    approve_release_parser = subparsers.add_parser("approve-release")
    approve_release_parser.add_argument("--id", required=True)
    approve_release_parser.add_argument("--evidence", required=True)
    approve_release_parser.add_argument("--by", required=True)

    record_publish_parser = subparsers.add_parser("record-publish")
    record_publish_parser.add_argument("--id", required=True)
    record_publish_parser.add_argument("--receipt", required=True)
    record_publish_parser.add_argument("--by", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "intake":
            item = intake(
                root=args.root,
                item_id=args.id,
                title=args.title,
                property_slug=args.property,
                source=_source_from_args(args),
                priority=args.priority,
                requested_by=args.by,
            )
            _json_print(item)
        elif args.command == "list":
            _json_print(list_items(args.root))
        elif args.command == "show":
            _json_print(load_item(args.root, args.id))
        elif args.command == "next":
            _json_print(next_item(args.root))
        elif args.command == "begin-preflight":
            _json_print(begin_preflight(args.root, args.id, actor=args.by))
        elif args.command == "complete-preflight":
            _json_print(
                complete_preflight(
                    args.root,
                    args.id,
                    actor=args.by,
                    package_path=args.package,
                    blockers=args.blocker,
                )
            )
        elif args.command == "approve-source":
            _json_print(
                approve_source(args.root, args.id, actor=args.by, evidence=args.evidence)
            )
        elif args.command == "begin-production":
            _json_print(begin_production(args.root, args.id, actor=args.by))
        elif args.command == "submit-uat":
            _json_print(
                submit_uat(
                    args.root,
                    args.id,
                    actor=args.by,
                    preview=args.preview,
                    report_path=args.report,
                    ingestion_spec=args.ingestion_spec,
                    library_pack=args.library_pack,
                )
            )
        elif args.command == "approve-release":
            _json_print(
                approve_release(args.root, args.id, actor=args.by, evidence=args.evidence)
            )
        elif args.command == "record-publish":
            _json_print(record_publish(args.root, args.id, actor=args.by, receipt=args.receipt))
        else:
            parser.error(f"unknown command {args.command}")
    except DeskError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
