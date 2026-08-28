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

    def test_example_is_valid(self) -> None:
        self.assertEqual([], module.validate_manifest(self.data))

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

    def test_running_task_requires_lease(self) -> None:
        self.data["tasks"][0]["status"] = "running"
        errors = module.validate_manifest(self.data)
        self.assertTrue(any("requires a holder and lease expiry" in error for error in errors))

    def test_mutation_receipt_requires_approval_and_full_hash(self) -> None:
        data = copy.deepcopy(self.data)
        data["receipts"] = [
            {
                "receipt_id": "receipt_example",
                "task_id": "task_public_surface_audit_example",
                "run_id": "run_example",
                "attempt": 1,
                "swarm_trace_id": "trace_public_surface_audit_example",
                "role_id": "public-surface-steward",
                "adapter_id": "grokbot",
                "runtime_node_id": "grok-cloud-01",
                "status": "ok",
                "input_hashes": [],
                "outputs": [{"artifact_ref": "artifact", "sha256": "abc", "type": "proposal"}],
                "mutations": [{"type": "site.publish", "destination": "https://thirdsignal.ai/"}],
                "approvals_used": [],
                "validation": [],
                "started_at": "2026-08-28T12:00:00Z",
                "finished_at": "2026-08-28T12:01:00Z",
                "next_action": "operator_review"
            }
        ]
        errors = module.validate_manifest(data)
        self.assertTrue(any("full lowercase SHA-256" in error for error in errors))
        self.assertTrue(any("mutations require approvals_used" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
