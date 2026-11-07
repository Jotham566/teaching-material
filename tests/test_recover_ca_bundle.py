import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ca_bundle import verify_bundle
from recover_ca_bundle import recover


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.members = {}
        self.cutoff = "2026-11-07T11:02:01.960Z"
        for course in ("CML3111", "CML3112", "CML3113"):
            for number in range(1, 6):
                manifest = {"key": f"{course}|W{number:02}", "cutoff": self.cutoff,
                            "records": [], "files": [], "errors": []}
                if course == "CML3111" and number == 1:
                    data = b"synthetic notebook"
                    manifest["files"] = [{"id": "test", "export_name": "test.ipynb",
                                          "sha256": hashlib.sha256(data).hexdigest()}]
                    part = io.BytesIO()
                    with zipfile.ZipFile(part, "w") as archive:
                        archive.writestr("test.ipynb", data)
                    self.members["CML3111_W01_files_1.zip"] = part.getvalue()
                quiz = {"cutoff": self.cutoff, "source_kind": "recorded_sheet_scores_with_form_receipts",
                        "quizzes": [{"key": f"{course}|{number}", "records": []}]}
                self.members[f"{course}_W{number:02}_manifest.json"] = json.dumps(manifest).encode()
                self.members[f"{course}_Q{number}_quiz.json"] = json.dumps(quiz).encode()
        self.members["quiz_deadlines.json"] = b"{}"

    def source(self):
        path = self.root / "download.zip"
        with zipfile.ZipFile(path, "w") as archive:
            for name, content in self.members.items():
                archive.writestr("Drive folder/" + name, content)
        return path

    def test_complete_recovery(self):
        output = self.root / "recovered.zip"
        recover(self.source(), output)
        self.assertEqual(verify_bundle(output)["cutoff"], self.cutoff)
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        with self.assertRaises(FileExistsError):
            recover(self.source(), output)

    def test_missing_manifest_or_attachment_part_stops(self):
        for name in ("CML3111_Q1_quiz.json", "CML3111_W01_files_1.zip"):
            original = self.members.pop(name)
            with self.assertRaises(ValueError):
                recover(self.source(), self.root / "recovered.zip")
            self.assertFalse((self.root / "recovered.zip").exists())
            self.members[name] = original

    def test_mixed_cutoffs_and_tampered_attachment_stop(self):
        quiz = json.loads(self.members["CML3111_Q1_quiz.json"])
        quiz["cutoff"] = "2026-11-06T00:00:00Z"
        self.members["CML3111_Q1_quiz.json"] = json.dumps(quiz).encode()
        with self.assertRaisesRegex(ValueError, "cutoffs"):
            recover(self.source(), self.root / "recovered.zip")
        quiz["cutoff"] = self.cutoff
        self.members["CML3111_Q1_quiz.json"] = json.dumps(quiz).encode()
        part = io.BytesIO()
        with zipfile.ZipFile(part, "w") as archive:
            archive.writestr("test.ipynb", b"modified")
        self.members["CML3111_W01_files_1.zip"] = part.getvalue()
        with self.assertRaisesRegex(ValueError, "checksum"):
            recover(self.source(), self.root / "recovered.zip")
        self.assertFalse((self.root / "recovered.zip").exists())

    def test_unexpected_and_unsafe_paths_rejected(self):
        self.members["../unexpected.txt"] = b"extra"
        with self.assertRaises(ValueError):
            recover(self.source(), self.root / "recovered.zip")


if __name__ == "__main__":
    unittest.main()
