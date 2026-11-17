"""Repackage a stopped CA export downloaded as a Drive folder ZIP."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import zipfile

from ca_bundle import verify_bundle
from unpack_ca_export import MAX_BYTES, unpack

MEMBER = re.compile(
    r"(?:quiz_deadlines\.json|CML311[123]_(?:W0[1-5]_(?:manifest\.json|files_\d+\.zip)|Q[1-5]_quiz\.json))"
)
COHORTS = ("CML3111", "CML3112", "CML3113")


def recover(source, output):
    source, output = Path(source).expanduser().resolve(), Path(output).expanduser().resolve()
    if output.exists():
        raise FileExistsError("Output already exists; choose a different output path.")
    if source == output:
        raise ValueError("Source and output must be different files.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".ca-recovery-", dir=output.parent) as tmp:
        os.chmod(tmp, 0o700)
        candidate = Path(tmp) / "bundle.zip"
        entries, cutoffs, seen, exported_metadata = [], set(), set(), None
        with zipfile.ZipFile(source) as incoming, zipfile.ZipFile(candidate, "w", allowZip64=True) as bundle:
            total = 0
            for item in incoming.infolist():
                path = PurePosixPath(item.filename)
                if path.is_absolute() or ".." in path.parts or "\\" in item.filename or stat.S_ISLNK(item.external_attr >> 16):
                    raise ValueError("Unsafe ZIP entry: " + item.filename)
                if item.is_dir():
                    continue
                name = path.name
                if name != "ca_bundle.json" and not MEMBER.fullmatch(name):
                    raise ValueError("Unexpected export file: " + item.filename)
                if name in seen:
                    raise ValueError("Duplicate export file: " + name)
                seen.add(name)
                total += item.file_size
                if total > MAX_BYTES:
                    raise ValueError("Export exceeds the grader's extraction limit.")
                content = incoming.read(item)
                if name == "ca_bundle.json":
                    exported_metadata = json.loads(content)
                    continue
                if name.endswith("_manifest.json") or name.endswith("_quiz.json"):
                    meta = json.loads(content)
                    if not isinstance(meta.get("cutoff"), str):
                        raise ValueError("Missing export cutoff: " + name)
                    cutoffs.add(meta["cutoff"])
                    if name.endswith("_manifest.json"):
                        if meta.get("key", "").replace("|", "_") + "_manifest.json" != name:
                            raise ValueError("Assignment manifest identity mismatch: " + name)
                        if meta.get("errors"):
                            raise ValueError("Export reports attachment errors: " + name)
                    else:
                        expected = name.replace("_Q", "|").replace("_quiz.json", "")
                        quizzes = meta.get("quizzes", [])
                        if len(quizzes) != 1 or quizzes[0].get("key") != expected:
                            raise ValueError("Quiz identity mismatch: " + name)
                        if meta.get("source_kind") != "recorded_sheet_scores_with_form_receipts":
                            raise ValueError("Recorded quiz scores missing: " + name)
                bundle.writestr(name, content)
                entries.append({"name": name, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)})
            required = {"quiz_deadlines.json"}
            required.update(f"{c}_W{i:02}_manifest.json" for c in COHORTS for i in range(1, 6))
            required.update(f"{c}_Q{i}_quiz.json" for c in COHORTS for i in range(1, 6))
            missing = required - seen
            if missing:
                raise ValueError("Incomplete download; missing: " + ", ".join(sorted(missing)))
            if len(cutoffs) != 1:
                raise ValueError("Export pieces have inconsistent cutoffs.")
            cutoff = cutoffs.pop()
            metadata = exported_metadata if exported_metadata is not None else {
                "format": "IUEA_CA_BUNDLE", "version": 1,
                "complete": True, "cutoff": cutoff, "files": entries,
            }
            if metadata.get("cutoff") != cutoff:
                raise ValueError("Bundle cutoff differs from the export pieces.")
            bundle.writestr("ca_bundle.json", json.dumps(metadata))
        verify_bundle(candidate)
        _, issues = unpack(candidate, Path(tmp) / "check")
        if issues:
            raise ValueError("Missing or unreadable attachments; retain all downloaded parts.")
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as target, candidate.open("rb") as source_file:
                while block := source_file.read(1024 * 1024):
                    target.write(block)
        except BaseException:
            output.unlink(missing_ok=True)
            raise
    return output, exported_metadata is not None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("download", help="Drive folder ZIP from the stopped export")
    parser.add_argument("output", help="New private grading ZIP path")
    args = parser.parse_args()
    output, source_inventory = recover(args.download, args.output)
    print("Recovered:", output)
    print("Bundle inventory:", "exporter-generated and verified." if source_inventory else
          "generated locally; attachment hashes were checked against the saved manifests.")


if __name__ == "__main__":
    main()
