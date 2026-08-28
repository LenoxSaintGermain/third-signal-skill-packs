#!/usr/bin/env python3
"""Fail-closed validator for Third Signal agent-workforce manifests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA = "third-signal-agent-workforce@1"
ADAPTER_STATES = {"offline", "shadow", "active", "degraded", "retired"}
TASK_STATES = {"queued", "claimed", "running", "approval-required", "blocked", "completed", "failed", "cancelled"}
RECEIPT_STATES = {"ok", "partial", "noop", "blocked", "failed"}
CLASSIFICATIONS = {"public", "internal", "confidential", "restricted"}
TASK_APPROVAL_POLICIES = {"none", "operator_required", "preauthorized_exact_packet"}
ROLE_APPROVAL_POLICIES = {"none", "operator_required", "operator_required_for_public_mutation"}
MUTATING_CAPABILITY_MARKERS = (".publish", ".deploy", ".send", ".delete", ".purchase", ".permission", ".authorize")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _object(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def _list(value: Any, label: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    return value


def _required(record: dict[str, Any], fields: tuple[str, ...], label: str, errors: list[str]) -> None:
    for field in fields:
        if record.get(field) in (None, "", []):
            errors.append(f"{label}.{field} is required")


def _unique_ids(records: list[Any], field: str, label: str, errors: list[str]) -> set[str]:
    result: set[str] = set()
    for index, raw in enumerate(records):
        record = _object(raw, f"{label}[{index}]", errors)
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}[{index}].{field} is required")
        elif value in result:
            errors.append(f"duplicate {label} {field}: {value}")
        else:
            result.add(value)
    return result


def _timestamp(value: Any, label: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be an ISO-8601 timestamp or null")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} is not a valid ISO-8601 timestamp")


def validate_manifest(data: Any) -> list[str]:
    errors: list[str] = []
    root = _object(data, "manifest", errors)
    if root.get("schema") != SCHEMA:
        errors.append(f"manifest.schema must equal {SCHEMA}")

    control = _object(root.get("control_plane"), "control_plane", errors)
    _required(control, ("control_plane_id", "authority", "external_mutation_default"), "control_plane", errors)
    if control.get("authority") in {"grokbot", "hermes", "codex", "claude", "gemini"}:
        errors.append("control_plane.authority must be provider-neutral")

    adapters = _list(root.get("adapters"), "adapters", errors)
    roles = _list(root.get("roles"), "roles", errors)
    tasks = _list(root.get("tasks"), "tasks", errors)
    receipts = _list(root.get("receipts"), "receipts", errors)
    adapter_ids = _unique_ids(adapters, "adapter_id", "adapters", errors)
    role_ids = _unique_ids(roles, "role_id", "roles", errors)
    task_ids = _unique_ids(tasks, "task_id", "tasks", errors)
    _unique_ids(receipts, "receipt_id", "receipts", errors)

    adapter_capabilities: dict[str, set[str]] = {}
    for index, raw in enumerate(adapters):
        adapter = _object(raw, f"adapters[{index}]", errors)
        _required(adapter, ("adapter_id", "kind", "state", "trust_boundary", "capabilities", "credentials_ref"), f"adapters[{index}]", errors)
        if adapter.get("state") not in ADAPTER_STATES:
            errors.append(f"adapters[{index}].state is invalid")
        capabilities = _list(adapter.get("capabilities"), f"adapters[{index}].capabilities", errors)
        if any(not isinstance(item, str) or not item for item in capabilities):
            errors.append(f"adapters[{index}].capabilities must contain non-empty strings")
        adapter_capabilities[str(adapter.get("adapter_id", ""))] = {item for item in capabilities if isinstance(item, str) and item}

    role_capabilities: dict[str, set[str]] = {}
    for index, raw in enumerate(roles):
        role = _object(raw, f"roles[{index}]", errors)
        _required(role, ("role_id", "department", "mission", "capabilities", "prohibited", "approval_policy", "default_adapter", "fallback_adapters", "required_skills"), f"roles[{index}]", errors)
        if role.get("approval_policy") not in ROLE_APPROVAL_POLICIES:
            errors.append(f"roles[{index}].approval_policy is invalid")
        default_adapter = role.get("default_adapter")
        if default_adapter not in adapter_ids:
            errors.append(f"roles[{index}].default_adapter does not exist")
        fallbacks = _list(role.get("fallback_adapters"), f"roles[{index}].fallback_adapters", errors)
        for fallback in fallbacks:
            if fallback not in adapter_ids:
                errors.append(f"roles[{index}] fallback adapter does not exist: {fallback}")
            if fallback == default_adapter:
                errors.append(f"roles[{index}] fallback repeats the default adapter")
        capabilities = _list(role.get("capabilities"), f"roles[{index}].capabilities", errors)
        prohibited = _list(role.get("prohibited"), f"roles[{index}].prohibited", errors)
        if set(capabilities) & set(prohibited):
            errors.append(f"roles[{index}] capability is also prohibited")
        role_capabilities[str(role.get("role_id", ""))] = {item for item in capabilities if isinstance(item, str) and item}

    for index, raw in enumerate(tasks):
        task = _object(raw, f"tasks[{index}]", errors)
        _required(task, ("task_id", "swarm_trace_id", "role_id", "capability", "classification", "public_impact", "approval_policy", "input_refs", "output_contract", "allowed_tools", "denied_tools", "preferred_adapters", "fallback_adapters", "idempotency_key", "lease", "status"), f"tasks[{index}]", errors)
        role_id, capability = task.get("role_id"), task.get("capability")
        if role_id not in role_ids:
            errors.append(f"tasks[{index}].role_id does not exist")
        elif capability not in role_capabilities.get(str(role_id), set()):
            errors.append(f"tasks[{index}].capability is not granted to its role")
        if task.get("classification") not in CLASSIFICATIONS:
            errors.append(f"tasks[{index}].classification is invalid")
        if task.get("status") not in TASK_STATES:
            errors.append(f"tasks[{index}].status is invalid")
        if task.get("approval_policy") not in TASK_APPROVAL_POLICIES:
            errors.append(f"tasks[{index}].approval_policy is invalid")
        preferred = _list(task.get("preferred_adapters"), f"tasks[{index}].preferred_adapters", errors)
        fallbacks = _list(task.get("fallback_adapters"), f"tasks[{index}].fallback_adapters", errors)
        for adapter_id in [*preferred, *fallbacks]:
            if adapter_id not in adapter_ids:
                errors.append(f"tasks[{index}] adapter does not exist: {adapter_id}")
        if preferred and isinstance(capability, str) and not any(capability in adapter_capabilities.get(str(adapter_id), set()) for adapter_id in preferred):
            errors.append(f"tasks[{index}] no preferred adapter declares capability {capability}")
        mutating = isinstance(capability, str) and any(marker in capability for marker in MUTATING_CAPABILITY_MARKERS)
        if (task.get("public_impact") is True or mutating) and task.get("approval_policy") == "none":
            errors.append(f"tasks[{index}] external/public work cannot use approval_policy=none")
        lease = _object(task.get("lease"), f"tasks[{index}].lease", errors)
        _timestamp(lease.get("expires_at"), f"tasks[{index}].lease.expires_at", errors)
        if task.get("status") in {"claimed", "running"} and (not lease.get("holder") or not lease.get("expires_at")):
            errors.append(f"tasks[{index}] claimed/running work requires a holder and lease expiry")

    for index, raw in enumerate(receipts):
        receipt = _object(raw, f"receipts[{index}]", errors)
        _required(receipt, ("receipt_id", "task_id", "run_id", "attempt", "swarm_trace_id", "role_id", "adapter_id", "runtime_node_id", "status", "input_hashes", "outputs", "mutations", "approvals_used", "validation", "started_at", "finished_at", "next_action"), f"receipts[{index}]", errors)
        if receipt.get("task_id") not in task_ids:
            errors.append(f"receipts[{index}].task_id does not exist")
        if receipt.get("role_id") not in role_ids:
            errors.append(f"receipts[{index}].role_id does not exist")
        if receipt.get("adapter_id") not in adapter_ids:
            errors.append(f"receipts[{index}].adapter_id does not exist")
        if receipt.get("status") not in RECEIPT_STATES:
            errors.append(f"receipts[{index}].status is invalid")
        _timestamp(receipt.get("started_at"), f"receipts[{index}].started_at", errors)
        _timestamp(receipt.get("finished_at"), f"receipts[{index}].finished_at", errors)
        for output_index, raw_output in enumerate(_list(receipt.get("outputs"), f"receipts[{index}].outputs", errors)):
            output = _object(raw_output, f"receipts[{index}].outputs[{output_index}]", errors)
            if not SHA256_RE.fullmatch(str(output.get("sha256", ""))):
                errors.append(f"receipts[{index}].outputs[{output_index}].sha256 must be a full lowercase SHA-256")
        mutations = _list(receipt.get("mutations"), f"receipts[{index}].mutations", errors)
        approvals = _list(receipt.get("approvals_used"), f"receipts[{index}].approvals_used", errors)
        if mutations and not approvals:
            errors.append(f"receipts[{index}] mutations require approvals_used")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2
    errors = validate_manifest(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"VALID: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
