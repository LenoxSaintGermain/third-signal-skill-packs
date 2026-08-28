#!/usr/bin/env python3
"""Fail-closed validator for Third Signal agent-workforce manifests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "third-signal-agent-workforce@2"
ADAPTER_STATES = {"offline", "shadow", "active", "degraded", "retired"}
TASK_STATES = {"queued", "claimed", "running", "approval-required", "blocked", "completed", "failed", "cancelled"}
RECEIPT_STATES = {"ok", "partial", "noop", "blocked", "failed"}
VERIFICATION_STATES = {"pending", "verified", "rejected"}
CLASSIFICATIONS = {"public", "internal", "confidential", "restricted"}
TASK_APPROVAL_POLICIES = {"none", "operator_required", "preauthorized_exact_packet"}
ROLE_APPROVAL_POLICIES = {"none", "operator_required", "operator_required_for_public_mutation"}
EFFECTS = {"read", "draft", "mutate"}
OPERATING_MODES = {"shadow", "active"}
RESUME_POLICIES = {"restart_current_inputs", "resume_exact_snapshot", "block_for_operator"}
REPLAY_SAFETY = {"read_only", "idempotent", "non_repeatable"}
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
    """Require field presence without incorrectly rejecting valid empty arrays."""
    for field in fields:
        if field not in record or record.get(field) in (None, ""):
            errors.append(f"{label}.{field} is required")


def _nonempty_strings(value: Any, label: str, errors: list[str]) -> list[str]:
    values = _list(value, label, errors)
    if not values:
        errors.append(f"{label} must contain at least one value")
    elif any(not isinstance(item, str) or not item.strip() for item in values):
        errors.append(f"{label} must contain non-empty strings")
    return [item for item in values if isinstance(item, str) and item.strip()]


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


def _parse_timestamp(value: Any, label: str, errors: list[str], nullable: bool = True) -> datetime | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be an ISO-8601 timestamp{' or null' if nullable else ''}")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} is not a valid ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{label} must include a timezone")
        return None
    return parsed


def _adapter_is_eligible(adapter: dict[str, Any], capability: str, operating_mode: str) -> bool:
    state = adapter.get("state")
    if state not in {"shadow", "active"}:
        return False
    if operating_mode == "active" and state != "active":
        return False
    return capability in adapter.get("capabilities", [])


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
    skills = _list(root.get("skills"), "skills", errors)
    roles = _list(root.get("roles"), "roles", errors)
    tasks = _list(root.get("tasks"), "tasks", errors)
    schedules = _list(root.get("schedules"), "schedules", errors)
    approvals = _list(root.get("approvals"), "approvals", errors)
    artifacts = _list(root.get("artifacts"), "artifacts", errors)
    receipts = _list(root.get("receipts"), "receipts", errors)
    events = _list(root.get("events"), "events", errors)

    adapter_ids = _unique_ids(adapters, "adapter_id", "adapters", errors)
    skill_ids = _unique_ids(skills, "skill_id", "skills", errors)
    role_ids = _unique_ids(roles, "role_id", "roles", errors)
    task_ids = _unique_ids(tasks, "task_id", "tasks", errors)
    _unique_ids(schedules, "schedule_id", "schedules", errors)
    _unique_ids(approvals, "approval_id", "approvals", errors)
    _unique_ids(artifacts, "artifact_id", "artifacts", errors)
    _unique_ids(receipts, "receipt_id", "receipts", errors)
    _unique_ids(events, "event_id", "events", errors)

    adapters_by_id: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(adapters):
        adapter = _object(raw, f"adapters[{index}]", errors)
        _required(adapter, ("adapter_id", "kind", "state", "trust_boundary", "capabilities", "credentials_ref"), f"adapters[{index}]", errors)
        if adapter.get("state") not in ADAPTER_STATES:
            errors.append(f"adapters[{index}].state is invalid")
        adapter["capabilities"] = _nonempty_strings(adapter.get("capabilities"), f"adapters[{index}].capabilities", errors)
        _parse_timestamp(adapter.get("last_heartbeat_at"), f"adapters[{index}].last_heartbeat_at", errors)
        adapters_by_id[str(adapter.get("adapter_id", ""))] = adapter

    for index, raw in enumerate(skills):
        skill = _object(raw, f"skills[{index}]", errors)
        _required(skill, ("skill_id", "version", "sha256", "source_ref"), f"skills[{index}]", errors)
        if not SHA256_RE.fullmatch(str(skill.get("sha256", ""))):
            errors.append(f"skills[{index}].sha256 must be a full lowercase SHA-256")

    roles_by_id: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(roles):
        role = _object(raw, f"roles[{index}]", errors)
        _required(role, ("role_id", "department", "mission", "capabilities", "prohibited", "approval_policy", "default_adapter", "fallback_adapters", "required_skills"), f"roles[{index}]", errors)
        if role.get("approval_policy") not in ROLE_APPROVAL_POLICIES:
            errors.append(f"roles[{index}].approval_policy is invalid")
        default_adapter = role.get("default_adapter")
        if default_adapter not in adapter_ids:
            errors.append(f"roles[{index}].default_adapter does not exist")
        elif adapters_by_id.get(str(default_adapter), {}).get("state") == "retired":
            errors.append(f"roles[{index}].default_adapter is retired and must be atomically promoted")
        fallbacks = _list(role.get("fallback_adapters"), f"roles[{index}].fallback_adapters", errors)
        for fallback in fallbacks:
            if fallback not in adapter_ids:
                errors.append(f"roles[{index}] fallback adapter does not exist: {fallback}")
            if fallback == default_adapter:
                errors.append(f"roles[{index}] fallback repeats the default adapter")
        capabilities = _nonempty_strings(role.get("capabilities"), f"roles[{index}].capabilities", errors)
        prohibited = _list(role.get("prohibited"), f"roles[{index}].prohibited", errors)
        if set(capabilities) & set(prohibited):
            errors.append(f"roles[{index}] capability is also prohibited")
        required_skills = _nonempty_strings(role.get("required_skills"), f"roles[{index}].required_skills", errors)
        for skill_id in required_skills:
            if skill_id not in skill_ids:
                errors.append(f"roles[{index}] required skill does not exist: {skill_id}")
        role["capabilities"] = capabilities
        role["prohibited"] = prohibited
        roles_by_id[str(role.get("role_id", ""))] = role

    tasks_by_id: dict[str, dict[str, Any]] = {}
    idempotency_keys: set[str] = set()
    for index, raw in enumerate(tasks):
        task = _object(raw, f"tasks[{index}]", errors)
        _required(task, ("task_id", "swarm_trace_id", "role_id", "capability", "effect", "operating_mode", "classification", "public_impact", "approval_policy", "input_refs", "output_contract", "allowed_tools", "denied_tools", "preferred_adapters", "fallback_adapters", "idempotency_key", "resume_policy", "replay_safety", "lease", "status"), f"tasks[{index}]", errors)
        role_id, capability = task.get("role_id"), str(task.get("capability", ""))
        role = roles_by_id.get(str(role_id), {})
        if role_id not in role_ids:
            errors.append(f"tasks[{index}].role_id does not exist")
        elif capability not in role.get("capabilities", []):
            errors.append(f"tasks[{index}].capability is not granted to its role")
        if task.get("effect") not in EFFECTS:
            errors.append(f"tasks[{index}].effect is invalid")
        if task.get("operating_mode") not in OPERATING_MODES:
            errors.append(f"tasks[{index}].operating_mode is invalid")
        if task.get("classification") not in CLASSIFICATIONS:
            errors.append(f"tasks[{index}].classification is invalid")
        if task.get("status") not in TASK_STATES:
            errors.append(f"tasks[{index}].status is invalid")
        if task.get("approval_policy") not in TASK_APPROVAL_POLICIES:
            errors.append(f"tasks[{index}].approval_policy is invalid")
        if task.get("resume_policy") not in RESUME_POLICIES:
            errors.append(f"tasks[{index}].resume_policy is invalid")
        if task.get("replay_safety") not in REPLAY_SAFETY:
            errors.append(f"tasks[{index}].replay_safety is invalid")
        if task.get("effect") == "read" and task.get("replay_safety") != "read_only":
            errors.append(f"tasks[{index}] read work must use replay_safety=read_only")
        if task.get("effect") == "mutate" and task.get("operating_mode") == "shadow":
            errors.append(f"tasks[{index}] shadow work cannot mutate")
        if (task.get("public_impact") is True or task.get("effect") == "mutate") and task.get("approval_policy") == "none":
            errors.append(f"tasks[{index}] external/public work cannot use approval_policy=none")

        preferred = _nonempty_strings(task.get("preferred_adapters"), f"tasks[{index}].preferred_adapters", errors)
        fallbacks = _list(task.get("fallback_adapters"), f"tasks[{index}].fallback_adapters", errors)
        operating_mode = str(task.get("operating_mode", ""))
        for lane, adapter_list in (("preferred", preferred), ("fallback", fallbacks)):
            for adapter_id in adapter_list:
                adapter = adapters_by_id.get(str(adapter_id))
                if adapter is None:
                    errors.append(f"tasks[{index}] {lane} adapter does not exist: {adapter_id}")
                elif not _adapter_is_eligible(adapter, capability, operating_mode):
                    errors.append(f"tasks[{index}] {lane} adapter is not eligible for {capability}: {adapter_id}")

        allowed_tools = _list(task.get("allowed_tools"), f"tasks[{index}].allowed_tools", errors)
        denied_tools = _list(task.get("denied_tools"), f"tasks[{index}].denied_tools", errors)
        conflict = set(allowed_tools) & (set(denied_tools) | set(role.get("prohibited", [])))
        if conflict:
            errors.append(f"tasks[{index}] allowed tools conflict with denied/prohibited tools: {sorted(conflict)}")

        key = task.get("idempotency_key")
        if isinstance(key, str):
            if key in idempotency_keys:
                errors.append(f"duplicate task idempotency_key: {key}")
            idempotency_keys.add(key)

        lease = _object(task.get("lease"), f"tasks[{index}].lease", errors)
        _required(lease, ("generation",), f"tasks[{index}].lease", errors)
        generation = lease.get("generation")
        if not isinstance(generation, int) or isinstance(generation, bool) or generation < 0:
            errors.append(f"tasks[{index}].lease.generation must be a non-negative integer")
        claimed_at = _parse_timestamp(lease.get("claimed_at"), f"tasks[{index}].lease.claimed_at", errors)
        expires_at = _parse_timestamp(lease.get("expires_at"), f"tasks[{index}].lease.expires_at", errors)
        active_lease = task.get("status") in {"claimed", "running"}
        holder = lease.get("holder_adapter")
        if active_lease:
            required_lease_fields = ("holder_adapter", "runtime_node_id", "fencing_token", "claimed_at", "expires_at")
            _required(lease, required_lease_fields, f"tasks[{index}].lease", errors)
            if not isinstance(generation, int) or generation < 1:
                errors.append(f"tasks[{index}] claimed/running work requires lease.generation >= 1")
            if holder not in [*preferred, *fallbacks]:
                errors.append(f"tasks[{index}].lease.holder_adapter is not assigned to the task")
            holder_adapter = adapters_by_id.get(str(holder))
            if holder_adapter is None or not _adapter_is_eligible(holder_adapter, capability, operating_mode):
                errors.append(f"tasks[{index}].lease holder is not an eligible adapter")
            if claimed_at and expires_at and claimed_at >= expires_at:
                errors.append(f"tasks[{index}].lease expires_at must be after claimed_at")
            if expires_at and expires_at <= datetime.now(timezone.utc):
                errors.append(f"tasks[{index}].lease is expired")
        elif any(lease.get(field) is not None for field in ("holder_adapter", "runtime_node_id", "claimed_at", "expires_at")):
            errors.append(f"tasks[{index}] inactive work must not retain an active lease")
        tasks_by_id[str(task.get("task_id", ""))] = task

    for index, raw in enumerate(schedules):
        schedule = _object(raw, f"schedules[{index}]", errors)
        _required(schedule, ("schedule_id", "role_id", "capability", "enabled", "cadence", "timezone"), f"schedules[{index}]", errors)
        if schedule.get("role_id") not in role_ids:
            errors.append(f"schedules[{index}].role_id does not exist")
        elif schedule.get("capability") not in roles_by_id.get(str(schedule.get("role_id")), {}).get("capabilities", []):
            errors.append(f"schedules[{index}].capability is not granted to its role")

    approvals_by_id: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(approvals):
        approval = _object(raw, f"approvals[{index}]", errors)
        _required(approval, ("approval_id", "status", "authorized_by", "authorized_at", "expires_at", "content_hash", "scope"), f"approvals[{index}]", errors)
        _parse_timestamp(approval.get("authorized_at"), f"approvals[{index}].authorized_at", errors, nullable=False)
        _parse_timestamp(approval.get("expires_at"), f"approvals[{index}].expires_at", errors, nullable=False)
        if not SHA256_RE.fullmatch(str(approval.get("content_hash", ""))):
            errors.append(f"approvals[{index}].content_hash must be a full lowercase SHA-256")
        approvals_by_id[str(approval.get("approval_id", ""))] = approval

    artifacts_by_id: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(artifacts):
        artifact = _object(raw, f"artifacts[{index}]", errors)
        _required(artifact, ("artifact_id", "type", "uri", "sha256", "created_at"), f"artifacts[{index}]", errors)
        if not SHA256_RE.fullmatch(str(artifact.get("sha256", ""))):
            errors.append(f"artifacts[{index}].sha256 must be a full lowercase SHA-256")
        _parse_timestamp(artifact.get("created_at"), f"artifacts[{index}].created_at", errors, nullable=False)
        artifacts_by_id[str(artifact.get("artifact_id", ""))] = artifact

    receipt_keys: set[tuple[Any, Any, Any]] = set()
    successful_verified_by_task: set[str] = set()
    for index, raw in enumerate(receipts):
        receipt = _object(raw, f"receipts[{index}]", errors)
        _required(receipt, ("receipt_id", "task_id", "run_id", "attempt", "lease_generation", "fencing_token", "swarm_trace_id", "role_id", "adapter_id", "runtime_node_id", "status", "input_hashes", "outputs", "mutations", "approvals_used", "validation", "verification", "started_at", "finished_at", "next_action"), f"receipts[{index}]", errors)
        task = tasks_by_id.get(str(receipt.get("task_id")))
        if task is None:
            errors.append(f"receipts[{index}].task_id does not exist")
        else:
            if receipt.get("swarm_trace_id") != task.get("swarm_trace_id"):
                errors.append(f"receipts[{index}].swarm_trace_id does not match its task")
            if receipt.get("role_id") != task.get("role_id"):
                errors.append(f"receipts[{index}].role_id does not match its task")
            if receipt.get("adapter_id") not in [*task.get("preferred_adapters", []), *task.get("fallback_adapters", [])]:
                errors.append(f"receipts[{index}].adapter_id is not assigned to its task")
        if receipt.get("role_id") not in role_ids:
            errors.append(f"receipts[{index}].role_id does not exist")
        if receipt.get("adapter_id") not in adapter_ids:
            errors.append(f"receipts[{index}].adapter_id does not exist")
        if receipt.get("status") not in RECEIPT_STATES:
            errors.append(f"receipts[{index}].status is invalid")
        attempt = receipt.get("attempt")
        if not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 1:
            errors.append(f"receipts[{index}].attempt must be a positive integer")
        receipt_key = (receipt.get("task_id"), receipt.get("run_id"), attempt)
        if receipt_key in receipt_keys:
            errors.append(f"duplicate receipt task/run/attempt identity: {receipt_key}")
        receipt_keys.add(receipt_key)
        lease_generation = receipt.get("lease_generation")
        if not isinstance(lease_generation, int) or isinstance(lease_generation, bool) or lease_generation < 1:
            errors.append(f"receipts[{index}].lease_generation must be a positive integer")
        if task and receipt.get("status") in {"ok", "noop"}:
            task_generation = task.get("lease", {}).get("generation")
            if lease_generation != task_generation:
                errors.append(f"receipts[{index}] successful receipt uses a stale lease generation")
            if receipt.get("fencing_token") != task.get("lease", {}).get("fencing_token"):
                errors.append(f"receipts[{index}] successful receipt uses a stale fencing token")
            if task.get("status") != "completed":
                errors.append(f"receipts[{index}] successful receipt requires task status=completed")
        _parse_timestamp(receipt.get("started_at"), f"receipts[{index}].started_at", errors, nullable=False)
        _parse_timestamp(receipt.get("finished_at"), f"receipts[{index}].finished_at", errors, nullable=False)

        outputs = _list(receipt.get("outputs"), f"receipts[{index}].outputs", errors)
        for output_index, raw_output in enumerate(outputs):
            output = _object(raw_output, f"receipts[{index}].outputs[{output_index}]", errors)
            _required(output, ("artifact_ref", "sha256", "type"), f"receipts[{index}].outputs[{output_index}]", errors)
            if not SHA256_RE.fullmatch(str(output.get("sha256", ""))):
                errors.append(f"receipts[{index}].outputs[{output_index}].sha256 must be a full lowercase SHA-256")
            artifact = artifacts_by_id.get(str(output.get("artifact_ref")))
            if artifact is None:
                errors.append(f"receipts[{index}].outputs[{output_index}].artifact_ref does not exist")
            elif output.get("sha256") != artifact.get("sha256"):
                errors.append(f"receipts[{index}].outputs[{output_index}].sha256 does not match its artifact")

        mutations = _list(receipt.get("mutations"), f"receipts[{index}].mutations", errors)
        approval_refs = _list(receipt.get("approvals_used"), f"receipts[{index}].approvals_used", errors)
        if mutations and task and task.get("effect") != "mutate":
            errors.append(f"receipts[{index}] mutations require task effect=mutate")
        if mutations and not approval_refs:
            errors.append(f"receipts[{index}] mutations require approvals_used")
        for approval_ref in approval_refs:
            approval = approvals_by_id.get(str(approval_ref))
            if approval is None:
                errors.append(f"receipts[{index}] approval does not exist: {approval_ref}")
            elif approval.get("status") != "approved":
                errors.append(f"receipts[{index}] approval is not approved: {approval_ref}")
        for mutation_index, raw_mutation in enumerate(mutations):
            mutation = _object(raw_mutation, f"receipts[{index}].mutations[{mutation_index}]", errors)
            _required(mutation, ("type", "destination", "observed_result", "lease_generation", "fencing_token"), f"receipts[{index}].mutations[{mutation_index}]", errors)
            if task and (mutation.get("lease_generation") != task.get("lease", {}).get("generation") or mutation.get("fencing_token") != task.get("lease", {}).get("fencing_token")):
                errors.append(f"receipts[{index}].mutations[{mutation_index}] failed lease fencing")

        verification = _object(receipt.get("verification"), f"receipts[{index}].verification", errors)
        _required(verification, ("status",), f"receipts[{index}].verification", errors)
        if verification.get("status") not in VERIFICATION_STATES:
            errors.append(f"receipts[{index}].verification.status is invalid")
        if verification.get("status") == "verified":
            _required(verification, ("verifier", "verified_at"), f"receipts[{index}].verification", errors)
            _parse_timestamp(verification.get("verified_at"), f"receipts[{index}].verification.verified_at", errors, nullable=False)
            if receipt.get("status") in {"ok", "noop"}:
                successful_verified_by_task.add(str(receipt.get("task_id")))

    for index, raw in enumerate(events):
        event = _object(raw, f"events[{index}]", errors)
        _required(event, ("event_id", "event_type", "task_id", "lease_generation", "recorded_at", "source", "status"), f"events[{index}]", errors)
        if event.get("task_id") not in task_ids:
            errors.append(f"events[{index}].task_id does not exist")
        if not isinstance(event.get("lease_generation"), int) or event.get("lease_generation") < 0:
            errors.append(f"events[{index}].lease_generation must be a non-negative integer")
        _parse_timestamp(event.get("recorded_at"), f"events[{index}].recorded_at", errors, nullable=False)

    for index, task in enumerate(tasks):
        if isinstance(task, dict) and task.get("status") == "completed" and task.get("task_id") not in successful_verified_by_task:
            errors.append(f"tasks[{index}] completed work requires a verified ok/noop receipt")
        generation = task.get("lease", {}).get("generation") if isinstance(task, dict) else None
        if isinstance(generation, int) and generation > 1:
            expired_generations = {
                event.get("lease_generation")
                for event in events
                if isinstance(event, dict) and event.get("task_id") == task.get("task_id") and event.get("event_type") == "lease.expired"
            }
            if generation - 1 not in expired_generations:
                errors.append(f"tasks[{index}] failover generation requires a control-plane lease.expired event")

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
