from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "validate_hq_manifest.py"
EXAMPLE = SKILL_ROOT / "assets" / "hq-manifest.example.json"

spec = importlib.util.spec_from_file_location("validate_hq_manifest", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class ManifestValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def completed_noop(self, data: dict | None = None) -> dict:
        result = copy.deepcopy(data or self.data)
        task = result["tasks"][0]
        task["status"] = "completed"
        task["lease"] = {
            "generation": 1,
            "holder_adapter": None,
            "runtime_node_id": None,
            "fencing_token": "fence-generation-1",
            "claimed_at": None,
            "expires_at": None,
        }
        result["receipts"] = [
            {
                "receipt_id": "receipt_example",
                "task_id": task["task_id"],
                "run_id": "run_example",
                "attempt": 1,
                "lease_generation": 1,
                "fencing_token": "fence-generation-1",
                "swarm_trace_id": task["swarm_trace_id"],
                "role_id": task["role_id"],
                "adapter_id": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "status": "noop",
                "input_hashes": [],
                "outputs": [],
                "mutations": [],
                "approvals_used": [],
                "validation": ["read-only scan observed no change"],
                "verification": {
                    "status": "verified",
                    "verifier_authority": "third-signal-hq",
                    "verifier_runtime_node_id": "hq-reconciler-01",
                    "verified_at": "2026-08-28T12:02:00Z",
                },
                "started_at": "2026-08-28T12:00:00Z",
                "finished_at": "2026-08-28T12:01:00Z",
                "received_at": "2026-08-28T12:01:30Z",
                "next_action": "none",
            }
        ]
        return result

    def exact_mutation_fixture(self) -> dict:
        data = self.completed_noop()
        task = data["tasks"][0]
        data["roles"][0]["capabilities"].append("site.publish")
        data["adapters"][1]["capabilities"].append("site.publish")
        task.update(
            {
                "capability": "site.publish",
                "effect": "mutate",
                "operating_mode": "active",
                "public_impact": True,
                "approval_policy": "preauthorized_exact_packet",
                "allowed_tools": ["browser.submit"],
                "denied_tools": ["production.deploy"],
                "preferred_adapters": ["hermes"],
                "fallback_adapters": [],
                "replay_safety": "idempotent",
                "resume_policy": "block_for_operator",
            }
        )
        content_hash = "a" * 64
        asset_hash = "b" * 64
        data["approvals"] = [
            {
                "approval_id": "approval_exact_publish",
                "task_id": task["task_id"],
                "status": "approved",
                "action_type": "site.publish",
                "destination": "https://thirdsignal.ai/",
                "account": "third-signal-production",
                "authorized_by": "lenox",
                "authorized_at": "2026-08-28T11:00:00Z",
                "expires_at": "2099-08-28T11:00:00Z",
                "content_hash": content_hash,
                "asset_hashes": [asset_hash],
                "scope": {"path": "/"},
                "rollback_or_correction": "revert deployment receipt",
                "consumed": True,
                "consumed_by_receipt_id": "receipt_example",
                "consumed_at": "2026-08-28T12:00:30Z",
            }
        ]
        receipt = data["receipts"][0]
        receipt["adapter_id"] = "hermes"
        receipt["runtime_node_id"] = "hermes-local-01"
        receipt["status"] = "ok"
        receipt["approvals_used"] = ["approval_exact_publish"]
        receipt["mutations"] = [
            {
                "approval_id": "approval_exact_publish",
                "type": "site.publish",
                "destination": "https://thirdsignal.ai/",
                "account": "third-signal-production",
                "content_hash": content_hash,
                "asset_hashes": [asset_hash],
                "scope": {"path": "/"},
                "observed_result": "permalink verified",
                "lease_generation": 1,
                "fencing_token": "fence-generation-1",
            }
        ]
        return data

    def test_example_is_valid(self) -> None:
        self.assertEqual([], module.validate_manifest(self.data))

    def test_skill_hash_must_match_local_bytes(self) -> None:
        self.data["skills"][0]["sha256"] = "0" * 64
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("does not match local_path bytes" in error for error in errors))

    def test_provider_cannot_be_control_plane_authority(self) -> None:
        self.data["control_plane"]["authority"] = "grokbot"
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("provider-neutral" in error for error in errors))

    def test_public_task_requires_approval(self) -> None:
        self.data["tasks"][0]["public_impact"] = True
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("approval_policy=none" in error for error in errors))

    def test_unknown_fallback_adapter_is_rejected(self) -> None:
        self.data["roles"][0]["fallback_adapters"] = ["unknown"]
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("fallback adapter does not exist" in error for error in errors))

    def test_running_task_requires_complete_eligible_lease(self) -> None:
        self.data["tasks"][0]["status"] = "running"
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("holder_adapter is required" in error for error in errors))
        self.assertTrue(any("lease holder is not an eligible adapter" in error for error in errors))

    def test_read_only_noop_receipt_allows_empty_mutation_arrays(self) -> None:
        self.assertEqual([], module.validate_manifest(self.completed_noop()))

    def test_offline_or_unassigned_lease_holder_is_rejected(self) -> None:
        task = self.data["tasks"][0]
        task["status"] = "running"
        task["lease"] = {
            "generation": 1,
            "holder_adapter": "unknown-runtime",
            "runtime_node_id": "unknown-runtime",
            "fencing_token": "fence-generation-1",
            "claimed_at": "2099-08-28T12:00:00Z",
            "expires_at": "2099-08-28T12:10:00Z",
        }
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("not assigned" in error for error in errors))
        self.assertTrue(any("not an eligible adapter" in error for error in errors))

    def test_fallback_must_declare_task_capability(self) -> None:
        self.data["adapters"][1]["capabilities"].remove("site.audit")
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("fallback adapter does not declare" in error for error in errors))

    def test_offline_preferred_adapter_allows_eligible_fallback(self) -> None:
        self.data["adapters"][0]["state"] = "offline"
        self.assertEqual([], module.validate_manifest(self.data))

    def test_receipt_is_bound_to_trace_role_and_completed_state(self) -> None:
        data = self.completed_noop()
        data["receipts"][0]["swarm_trace_id"] = "wrong-trace"
        data["receipts"][0]["role_id"] = "wrong-role"
        data["tasks"][0]["status"] = "queued"
        errors = module.validate_manifest(data)
        self.assertTrue(any("swarm_trace_id does not match" in error for error in errors))
        self.assertTrue(any("role_id does not match" in error for error in errors))
        self.assertTrue(any("requires task status=completed" in error for error in errors))

    def test_successful_receipt_rejects_stale_generation_and_fence(self) -> None:
        data = self.completed_noop()
        data["receipts"][0]["lease_generation"] = 2
        data["receipts"][0]["fencing_token"] = "stale-fence"
        errors = module.validate_manifest(data)
        self.assertTrue(any("stale lease generation" in error for error in errors))
        self.assertTrue(any("stale fencing token" in error for error in errors))

    def test_failover_generation_requires_expiration_event(self) -> None:
        self.data["tasks"][0]["lease"]["generation"] = 2
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("lease.expired event" in error for error in errors))

    def test_verified_fallback_completion_with_fence_and_event_is_valid(self) -> None:
        data = self.completed_noop()
        task = data["tasks"][0]
        task["lease"]["generation"] = 2
        task["lease"]["fencing_token"] = "fence-generation-2"
        receipt = data["receipts"][0]
        receipt["adapter_id"] = "hermes"
        receipt["runtime_node_id"] = "hermes-local-01"
        receipt["lease_generation"] = 2
        receipt["fencing_token"] = "fence-generation-2"
        data["events"] = [
            {
                "event_id": "event_grok_lease_expired",
                "event_type": "lease.expired",
                "task_id": task["task_id"],
                "lease_generation": 1,
                "recorded_at": "2026-08-28T11:59:00Z",
                "source": "third-signal-hq",
                "status": "verified",
                "holder_adapter": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "fencing_token": "fence-generation-1",
            }
        ]
        self.assertEqual([], module.validate_manifest(data))

    def test_late_partial_receipt_after_fence_is_rejected(self) -> None:
        data = self.completed_noop()
        task = data["tasks"][0]
        task["lease"]["generation"] = 2
        task["lease"]["fencing_token"] = "fence-generation-2"
        receipt = data["receipts"][0]
        receipt["adapter_id"] = "hermes"
        receipt["lease_generation"] = 2
        receipt["fencing_token"] = "fence-generation-2"
        data["events"] = [
            {
                "event_id": "event_grok_lease_expired",
                "event_type": "lease.expired",
                "task_id": task["task_id"],
                "lease_generation": 1,
                "recorded_at": "2026-08-28T11:59:00Z",
                "source": "third-signal-hq",
                "status": "verified",
                "holder_adapter": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "fencing_token": "fence-generation-1",
            }
        ]
        late = copy.deepcopy(receipt)
        late["receipt_id"] = "receipt_late_grok"
        late["run_id"] = "run_late_grok"
        late["attempt"] = 2
        late["adapter_id"] = "grokbot"
        late["runtime_node_id"] = "grok-cloud-01"
        late["status"] = "partial"
        late["lease_generation"] = 1
        late["fencing_token"] = "fence-generation-1"
        late["started_at"] = "2026-08-28T11:55:00Z"
        late["finished_at"] = "2026-08-28T11:58:00Z"
        late["received_at"] = "2026-08-28T12:06:00Z"
        late["verification"] = {"status": "rejected"}
        data["receipts"].append(late)
        errors = module.validate_manifest(data)
        self.assertTrue(any("arrived after its lease was fenced" in error for error in errors))

    def test_lease_expiry_event_must_come_from_control_plane_and_be_verified(self) -> None:
        self.data["tasks"][0]["lease"]["generation"] = 2
        self.data["events"] = [
            {
                "event_id": "event_fabricated",
                "event_type": "lease.expired",
                "task_id": self.data["tasks"][0]["task_id"],
                "lease_generation": 1,
                "recorded_at": "2026-08-28T12:05:00Z",
                "source": "grokbot",
                "status": "fabricated",
                "holder_adapter": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "fencing_token": "fence-generation-1",
            }
        ]
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("source must be the control plane" in error for error in errors))
        self.assertTrue(any("status is invalid" in error for error in errors))
        self.assertTrue(any("must be independently verified" in error for error in errors))

    def test_retired_default_adapter_requires_atomic_promotion(self) -> None:
        self.data["adapters"][0]["state"] = "retired"
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("default_adapter is retired" in error for error in errors))

    def test_mutation_receipt_requires_approval_and_full_hash(self) -> None:
        data = self.completed_noop()
        data["receipts"][0]["status"] = "ok"
        data["receipts"][0]["outputs"] = [
            {"artifact_ref": "missing-artifact", "sha256": "abc", "type": "proposal"}
        ]
        data["receipts"][0]["mutations"] = [
            {
                "type": "site.publish",
                "destination": "https://thirdsignal.ai/",
                "observed_result": "published",
                "lease_generation": 1,
                "fencing_token": "fence-generation-1",
            }
        ]
        errors = module.validate_manifest(data)
        self.assertTrue(any("full lowercase SHA-256" in error for error in errors))
        self.assertTrue(any("artifact_ref does not exist" in error for error in errors))
        self.assertTrue(any("mutations require approvals_used" in error for error in errors))

    def test_exact_approved_mutation_with_current_fence_is_valid(self) -> None:
        self.assertEqual([], module.validate_manifest(self.exact_mutation_fixture()))

    def test_expired_approval_cannot_authorize_mutation(self) -> None:
        data = self.exact_mutation_fixture()
        data["approvals"][0]["expires_at"] = "2026-08-28T11:30:00Z"
        errors = module.validate_manifest(data)
        self.assertTrue(any("expired before the mutation finished" in error for error in errors))

    def test_approval_cannot_be_reused_by_two_receipts(self) -> None:
        data = self.exact_mutation_fixture()
        duplicate = copy.deepcopy(data["receipts"][0])
        duplicate["receipt_id"] = "receipt_second"
        duplicate["run_id"] = "run_second"
        duplicate["attempt"] = 2
        data["receipts"].append(duplicate)
        errors = module.validate_manifest(data)
        self.assertTrue(any("approval was reused" in error for error in errors))
        self.assertTrue(any("bound to a different receipt" in error for error in errors))

    def test_approval_scope_must_match_mutation(self) -> None:
        data = self.exact_mutation_fixture()
        data["approvals"][0]["scope"] = {"path": "/admin-only"}
        errors = module.validate_manifest(data)
        self.assertTrue(any("not bound to an exact approval" in error for error in errors))

    def test_verifier_must_be_control_plane_and_independent_runtime(self) -> None:
        data = self.completed_noop()
        verification = data["receipts"][0]["verification"]
        verification["verifier_authority"] = "grokbot"
        verification["verifier_runtime_node_id"] = data["receipts"][0]["runtime_node_id"]
        errors = module.validate_manifest(data)
        self.assertTrue(any("performed by the control plane" in error for error in errors))
        self.assertTrue(any("independent of the executing runtime" in error for error in errors))

    def test_expiry_event_must_precede_fallback_execution(self) -> None:
        data = self.completed_noop()
        task = data["tasks"][0]
        task["lease"]["generation"] = 2
        task["lease"]["fencing_token"] = "fence-generation-2"
        receipt = data["receipts"][0]
        receipt["adapter_id"] = "hermes"
        receipt["lease_generation"] = 2
        receipt["fencing_token"] = "fence-generation-2"
        data["events"] = [
            {
                "event_id": "event_late_expiry",
                "event_type": "lease.expired",
                "task_id": task["task_id"],
                "lease_generation": 1,
                "recorded_at": "2026-08-28T12:01:00Z",
                "source": "third-signal-hq",
                "status": "verified",
                "holder_adapter": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "fencing_token": "fence-generation-1",
            }
        ]
        errors = module.validate_manifest(data)
        self.assertTrue(any("fallback started before the prior lease was fenced" in error for error in errors))

    def test_fallback_lease_claim_must_follow_expiry_event(self) -> None:
        data = copy.deepcopy(self.data)
        data["adapters"][0]["state"] = "offline"
        task = data["tasks"][0]
        task["status"] = "running"
        task["lease"] = {
            "generation": 2,
            "holder_adapter": "hermes",
            "runtime_node_id": "hermes-local-01",
            "fencing_token": "fence-generation-2",
            "claimed_at": "2099-08-28T11:58:00Z",
            "expires_at": "2099-08-28T12:30:00Z",
        }
        data["events"] = [
            {
                "event_id": "event_late_expiry",
                "event_type": "lease.expired",
                "task_id": task["task_id"],
                "lease_generation": 1,
                "recorded_at": "2099-08-28T11:59:00Z",
                "source": "third-signal-hq",
                "status": "verified",
                "holder_adapter": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "fencing_token": "fence-generation-1",
            }
        ]
        errors = module.validate_manifest(data)
        self.assertTrue(any("fallback lease was claimed before" in error for error in errors))

    def test_prior_generation_receipt_must_match_expired_fence(self) -> None:
        data = self.completed_noop()
        task = data["tasks"][0]
        task["lease"]["generation"] = 2
        task["lease"]["fencing_token"] = "fence-generation-2"
        receipt = data["receipts"][0]
        receipt["adapter_id"] = "hermes"
        receipt["runtime_node_id"] = "hermes-local-01"
        receipt["lease_generation"] = 2
        receipt["fencing_token"] = "fence-generation-2"
        data["events"] = [
            {
                "event_id": "event_grok_expired",
                "event_type": "lease.expired",
                "task_id": task["task_id"],
                "lease_generation": 1,
                "recorded_at": "2026-08-28T11:59:00Z",
                "source": "third-signal-hq",
                "status": "verified",
                "holder_adapter": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "fencing_token": "fence-generation-1",
            }
        ]
        prior = copy.deepcopy(receipt)
        prior["receipt_id"] = "receipt_prior_partial"
        prior["run_id"] = "run_prior_partial"
        prior["attempt"] = 2
        prior["adapter_id"] = "grokbot"
        prior["runtime_node_id"] = "grok-cloud-01"
        prior["status"] = "partial"
        prior["lease_generation"] = 1
        prior["fencing_token"] = "wrong-generation-1-fence"
        prior["started_at"] = "2026-08-28T11:50:00Z"
        prior["finished_at"] = "2026-08-28T11:55:00Z"
        prior["received_at"] = "2026-08-28T11:58:00Z"
        prior["verification"] = {"status": "pending"}
        data["receipts"].append(prior)
        errors = module.validate_manifest(data)
        self.assertTrue(any("does not match the expired lease holder/runtime/fence" in error for error in errors))

    def test_one_use_approval_cannot_cover_two_mutations(self) -> None:
        data = self.exact_mutation_fixture()
        data["receipts"][0]["mutations"].append(copy.deepcopy(data["receipts"][0]["mutations"][0]))
        errors = module.validate_manifest(data)
        self.assertTrue(any("one-use approval covers multiple mutations" in error for error in errors))

    def test_verification_must_follow_receipt_and_use_registered_runtime(self) -> None:
        data = self.completed_noop()
        verification = data["receipts"][0]["verification"]
        verification["verified_at"] = "2026-08-28T11:59:00Z"
        verification["verifier_runtime_node_id"] = "unregistered-verifier"
        errors = module.validate_manifest(data)
        self.assertTrue(any("verification runtime does not exist" in error for error in errors))
        self.assertTrue(any("verification predates control-plane receipt" in error for error in errors))

    def test_duplicate_idempotency_and_receipt_attempt_are_rejected(self) -> None:
        data = self.completed_noop()
        duplicate_task = copy.deepcopy(data["tasks"][0])
        duplicate_task["task_id"] = "task_duplicate"
        duplicate_task["swarm_trace_id"] = "trace_duplicate"
        duplicate_task["status"] = "queued"
        duplicate_task["lease"] = {
            "generation": 0,
            "holder_adapter": None,
            "runtime_node_id": None,
            "fencing_token": None,
            "claimed_at": None,
            "expires_at": None,
        }
        data["tasks"].append(duplicate_task)
        duplicate_receipt = copy.deepcopy(data["receipts"][0])
        duplicate_receipt["receipt_id"] = "receipt_duplicate"
        data["receipts"].append(duplicate_receipt)
        errors = module.validate_manifest(data)
        self.assertTrue(any("duplicate task idempotency_key" in error for error in errors))
        self.assertTrue(any("duplicate receipt task/run/attempt" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
