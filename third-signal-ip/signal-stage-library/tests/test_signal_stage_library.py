import base64
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "signal_stage_library.py"


class SignalStageLibraryTests(unittest.TestCase):
    def test_inspect_preserves_asset_dna_origin_lineage_and_missing_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            image = root / "approved.png"
            image.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="))
            manifest = root / "source.json"
            output = root / "ingestion.json"
            manifest.write_text(json.dumps({
                "story_pack": {
                    "id": "witch-time-economy",
                    "title": "Witches / Time Economy",
                    "version": "0.1.0",
                    "production_status": "finalized",
                    "assets": [
                        {
                            "id": "approved-sheet",
                            "asset_dna_id": "WITCH_ASSET_0001",
                            "role": "text-free-master",
                            "path": image.name,
                            "binary_state": "verified-local",
                            "approval_state": "approved",
                            "canon_state": "provisional",
                            "contains_lettering": False,
                            "status": "available-local",
                            "origin": {"conversation_id": "thread-1", "file_id": "file-1"},
                            "lineage": {"parents": [], "relationships": ["generated-from-prompt"]},
                        },
                        {
                            "id": "missing-original",
                            "asset_dna_id": "WITCH_ASSET_0002",
                            "role": "character-design-sheet",
                            "path": "/mnt/data/missing.png",
                            "binary_state": "known-runtime-reference",
                            "approval_state": "pending",
                            "canon_state": "proposed",
                            "status": "needs-export",
                            "origin": {"conversation_id": "thread-1", "runtime_path": "/mnt/data/missing.png"},
                            "lineage": {"parents": [], "relationships": []},
                        },
                    ],
                }
            }), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "inspect", "--source", str(manifest), "--output", str(output), "--property", "witches", "--text-policy", "dynamic"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            spec = json.loads(output.read_text(encoding="utf-8"))
            approved, missing = spec["assets"]
            self.assertEqual(approved["id"], "approved-sheet")
            self.assertEqual(approved["asset_dna_id"], "WITCH_ASSET_0001")
            self.assertEqual(approved["binary_state"], "verified-local")
            self.assertEqual(approved["origin"]["file_id"], "file-1")
            self.assertEqual(approved["lineage"]["relationships"], ["generated-from-prompt"])
            self.assertTrue(approved["release_eligible"])
            self.assertEqual(missing["binary_state"], "known-runtime-reference")
            self.assertFalse(missing["release_eligible"])

    def test_conversation_source_template_declares_independent_states(self):
        template = json.loads((SKILL_ROOT / "references" / "source-package-template.json").read_text(encoding="utf-8"))
        asset = template["story_pack"]["assets"][0]
        self.assertIn("asset_dna_id", asset)
        self.assertIn("binary_state", asset)
        self.assertIn("approval_state", asset)
        self.assertIn("canon_state", asset)
        self.assertIn("origin", asset)
        self.assertIn("lineage", asset)

    def test_post_package_approval_is_scoped_to_selected_asset_dna(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            image = root / "asset-blob"
            image.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="))
            evidence = root / "EXPORT_MANIFEST.md"
            evidence.write_text("approval addendum\n", encoding="utf-8")
            manifest = root / "inventory.json"
            output = root / "ingestion.json"
            manifest.write_text(json.dumps({
                "package_id": "witches-time-economy-source-v2",
                "assets": [
                    {
                        "id": "witch-character-sheet-0001",
                        "asset_dna_id": "WTE_ASSET_0001",
                        "role": "character-design-sheet",
                        "current_local_path": str(image),
                        "binary_state": "available-local",
                        "approval_state": "pending",
                        "canon_state": "proposed",
                        "release_eligible": False,
                        "mime_type": "image/png",
                        "pixel_width": 1,
                        "pixel_height": 1,
                        "bytes": image.stat().st_size,
                    },
                    {
                        "id": "conversation-cleanshot-0001",
                        "asset_dna_id": "WTE_ASSET_0002",
                        "role": "conversation-screenshot",
                        "current_local_path": None,
                        "binary_state": "needs-export",
                        "approval_state": "pending",
                        "canon_state": "not-applicable",
                        "release_eligible": False,
                    },
                    {
                        "id": "drive-export-manifest-0001",
                        "asset_dna_id": "WTE_DOC_0001",
                        "role": "recovery-manifest",
                        "current_local_path": str(evidence),
                        "binary_state": "verified-local",
                        "approval_state": "approved",
                        "canon_state": "not-applicable",
                        "release_eligible": False,
                        "bytes": 1,
                        "sha256": "0" * 64,
                    },
                ],
            }), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "inspect",
                    "--source",
                    str(manifest),
                    "--output",
                    str(output),
                    "--property",
                    "witches-time-economy",
                    "--text-policy",
                    "hybrid",
                    "--approval",
                    "approved",
                    "--approval-evidence",
                    "Publishing Desk source approval",
                    "--approved-asset-id",
                    "WTE_ASSET_0001",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            spec = json.loads(output.read_text(encoding="utf-8"))
            approved, missing, changed_evidence = spec["assets"]
            self.assertEqual(spec["state"], "ready-for-direction")
            self.assertEqual(approved["source_path"], str(image.resolve()))
            self.assertEqual(approved["approval_state"], "approved")
            self.assertTrue(approved["release_eligible"])
            self.assertEqual(missing["approval_state"], "pending")
            self.assertFalse(missing["release_eligible"])
            self.assertEqual(changed_evidence["integrity"], "mismatch")
            self.assertIn("immutable source snapshot", changed_evidence["integrity_note"])


if __name__ == "__main__":
    unittest.main()
