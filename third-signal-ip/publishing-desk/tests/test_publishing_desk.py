from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import publishing_desk as desk  # noqa: E402


WITCH_SOURCE = {
    "type": "chatgpt-conversation",
    "conversation_id": "6a6eb04a-9ae8-83ea-b24f-3ca202f71c80",
    "uri": "chatgpt-conversation://6a6eb04a-9ae8-83ea-b24f-3ca202f71c80",
}


class PublishingDeskIntakeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def intake(self, **overrides):
        values = {
            "root": self.root,
            "item_id": "witches-time-economy",
            "title": "Subverting the Witch Trope",
            "property_slug": "witches-time-economy",
            "source": WITCH_SOURCE,
            "priority": 90,
            "requested_by": "operator",
        }
        values.update(overrides)
        return desk.intake(**values)

    def test_conversation_intake_is_idempotent(self) -> None:
        first = self.intake()
        second = self.intake()

        self.assertEqual(first["id"], second["id"])
        self.assertEqual("inbox", second["state"])
        self.assertEqual(1, len(second["events"]))
        self.assertEqual(WITCH_SOURCE, second["source"])

    def test_duplicate_id_with_different_source_is_rejected(self) -> None:
        self.intake()

        with self.assertRaisesRegex(desk.DeskError, "different source"):
            self.intake(
                source={
                    "type": "chatgpt-conversation",
                    "conversation_id": "different-thread",
                    "uri": "chatgpt-conversation://different-thread",
                }
            )

    def test_next_returns_highest_priority_actionable_item(self) -> None:
        self.intake()
        desk.intake(
            root=self.root,
            item_id="lower-priority",
            title="Lower Priority",
            property_slug="lower-priority",
            source={"type": "local-manifest", "path": "/tmp/lower.json"},
            priority=10,
            requested_by="operator",
        )

        selected = desk.next_item(self.root)

        self.assertIsNotNone(selected)
        self.assertEqual("witches-time-economy", selected["id"])

    def test_intake_event_records_actor_and_state(self) -> None:
        item = self.intake(requested_by="lenox")

        self.assertEqual(
            {
                "actor": "lenox",
                "action": "intake",
                "from_state": None,
                "to_state": "inbox",
            },
            {key: item["events"][0][key] for key in (
                "actor", "action", "from_state", "to_state"
            )},
        )
        self.assertIn("at", item["events"][0])

    def test_next_excludes_operator_only_and_terminal_states(self) -> None:
        operator_item = self.intake(priority=100)
        operator_item["state"] = "operator-review"
        (self.root / "items" / "witches-time-economy.json").write_text(
            json.dumps(operator_item), encoding="utf-8"
        )
        published = desk.intake(
            root=self.root,
            item_id="already-published",
            title="Already Published",
            property_slug="already-published",
            source={"type": "local-manifest", "path": "/tmp/published.json"},
            priority=95,
            requested_by="operator",
        )
        published["state"] = "published"
        (self.root / "items" / "already-published.json").write_text(
            json.dumps(published), encoding="utf-8"
        )
        desk.intake(
            root=self.root,
            item_id="agent-actionable",
            title="Agent Actionable",
            property_slug="agent-actionable",
            source={"type": "local-manifest", "path": "/tmp/actionable.json"},
            priority=20,
            requested_by="operator",
        )

        selected = desk.next_item(self.root)

        self.assertIsNotNone(selected)
        self.assertEqual("agent-actionable", selected["id"])


class PublishingDeskWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "desk"
        self.artifacts = Path(self.temp.name) / "artifacts"
        self.artifacts.mkdir()
        self.source_package = self.artifacts / "source-package"
        self.source_package.mkdir()
        (self.source_package / "00_PACKAGE_INDEX.md").write_text("# Package\n", encoding="utf-8")
        self.uat_report = self.artifacts / "uat.md"
        self.uat_report.write_text("# UAT\n", encoding="utf-8")
        self.ingestion_spec = self.artifacts / "ingestion.json"
        self.ingestion_spec.write_text("{}\n", encoding="utf-8")
        self.library_pack = self.artifacts / "library-pack"
        self.library_pack.mkdir()
        self.receipt = self.artifacts / "publish-receipt.json"
        self.receipt.write_text('{"url":"https://example.test/story"}\n', encoding="utf-8")
        desk.intake(
            root=self.root,
            item_id="witches-time-economy",
            title="Subverting the Witch Trope",
            property_slug="witches-time-economy",
            source=WITCH_SOURCE,
            priority=90,
            requested_by="operator",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_preflight_routes_missing_originals_to_recovery(self) -> None:
        desk.begin_preflight(self.root, "witches-time-economy", actor="desk-agent")

        item = desk.complete_preflight(
            self.root,
            "witches-time-economy",
            actor="desk-agent",
            package_path=self.source_package,
            blockers=["original character sheet must be exported"],
        )

        self.assertEqual("needs-recovery", item["state"])
        self.assertEqual(["original character sheet must be exported"], item["blockers"])
        self.assertEqual(str(self.source_package), item["artifacts"]["source_package"])

    def test_source_approval_requires_operator_evidence(self) -> None:
        desk.begin_preflight(self.root, "witches-time-economy", actor="desk-agent")
        desk.complete_preflight(
            self.root,
            "witches-time-economy",
            actor="desk-agent",
            package_path=self.source_package,
            blockers=[],
        )

        with self.assertRaisesRegex(desk.DeskError, "approval evidence"):
            desk.approve_source(
                self.root,
                "witches-time-economy",
                actor="lenox",
                evidence="",
            )

        self.assertEqual("operator-review", desk.load_item(self.root, "witches-time-economy")["state"])

    def test_full_path_keeps_source_and_release_approval_separate(self) -> None:
        desk.begin_preflight(self.root, "witches-time-economy", actor="desk-agent")
        desk.complete_preflight(
            self.root,
            "witches-time-economy",
            actor="desk-agent",
            package_path=self.source_package,
            blockers=[],
        )
        desk.approve_source(
            self.root,
            "witches-time-economy",
            actor="lenox",
            evidence="Approved source package review 2026-08-21",
        )
        desk.begin_production(self.root, "witches-time-economy", actor="stage-agent")
        desk.submit_uat(
            self.root,
            "witches-time-economy",
            actor="stage-agent",
            preview="https://preview.example.test/witches",
            report_path=self.uat_report,
            ingestion_spec=self.ingestion_spec,
            library_pack=self.library_pack,
        )

        item = desk.load_item(self.root, "witches-time-economy")
        self.assertEqual("uat-review", item["state"])
        self.assertIsNotNone(item["gates"]["source_approval"])
        self.assertIsNone(item["gates"]["release_approval"])
        with self.assertRaisesRegex(desk.DeskError, "release-approved"):
            desk.record_publish(
                self.root,
                "witches-time-economy",
                actor="publisher",
                receipt=self.receipt,
            )
        self.assertEqual("uat-review", desk.load_item(self.root, "witches-time-economy")["state"])

        desk.approve_release(
            self.root,
            "witches-time-economy",
            actor="lenox",
            evidence="UAT accepted on desktop and mobile",
        )
        published = desk.record_publish(
            self.root,
            "witches-time-economy",
            actor="publisher",
            receipt=self.receipt,
        )

        self.assertEqual("published", published["state"])
        self.assertEqual(str(self.receipt), published["artifacts"]["publication_receipt"])

    def test_invalid_transition_does_not_mutate_history(self) -> None:
        before = desk.load_item(self.root, "witches-time-economy")

        with self.assertRaisesRegex(desk.DeskError, "operator-review"):
            desk.approve_source(
                self.root,
                "witches-time-economy",
                actor="lenox",
                evidence="Premature approval",
            )

        after = desk.load_item(self.root, "witches-time-economy")
        self.assertEqual(before, after)

    def test_missing_preflight_package_is_rejected_without_mutation(self) -> None:
        desk.begin_preflight(self.root, "witches-time-economy", actor="desk-agent")
        before = desk.load_item(self.root, "witches-time-economy")

        with self.assertRaisesRegex(desk.DeskError, "does not exist"):
            desk.complete_preflight(
                self.root,
                "witches-time-economy",
                actor="desk-agent",
                package_path=self.artifacts / "missing-package",
                blockers=[],
            )

        self.assertEqual(before, desk.load_item(self.root, "witches-time-economy"))


if __name__ == "__main__":
    unittest.main()
