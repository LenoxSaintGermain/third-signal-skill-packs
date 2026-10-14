import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "capture_at_creation.py"
SPEC = importlib.util.spec_from_file_location("capture_at_creation", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class CaptureAtCreationTests(unittest.TestCase):
    def test_copies_bytes_and_records_unknown_generation_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "generated.png"
            png_header = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + (1536).to_bytes(4, "big") + (1024).to_bytes(4, "big")
            source.write_bytes(png_header + b"source-bytes")
            destination_dir = root / "package" / "source"

            self.assertEqual(MODULE.main([
                "--source", str(source), "--destination-dir", str(destination_dir),
                "--asset-dna-id", "TEST_ASSET_0001", "--conversation-id", "conversation-1",
                "--tool", "image-generation",
            ]), 0)

            captured = destination_dir / source.name
            receipt_path = destination_dir / "receipts" / "TEST_ASSET_0001.json"
            self.assertEqual(captured.read_bytes(), source.read_bytes())
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt["binary"]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertEqual(receipt["binary"]["dimensions"], {"width": 1536, "height": 1024})
            self.assertEqual(receipt["generation"]["model"]["status"], "not recorded or exposed")
            self.assertEqual(receipt["state"]["approval"], "pending")

            self.assertEqual(MODULE.main([
                "--source", str(source), "--destination-dir", str(destination_dir),
                "--asset-dna-id", "TEST_ASSET_0001", "--conversation-id", "conversation-1",
                "--tool", "image-generation",
            ]), 2)


if __name__ == "__main__":
    unittest.main()
