"""Enforcement layer ("host") for the classroom read-only agent.

A model, a script or a person can PROPOSE an operation. This host decides.
It knows nothing about prompts: it checks the operation name, the arguments,
the matter and a call budget, then either executes a local read-only lookup
or refuses. The same host is used by read_only_agent.py (requests come from a
model) and host_control_tests.py (requests come from a fixed script).
No network, no files outside the evidence folder, no side effects.
"""
import json
from pathlib import Path

ALLOWED_OPERATIONS = {"lookup"}
ALLOWED_ARGUMENTS = {"action", "contract_id", "clause"}


class ReadOnlyHost:
    def __init__(self, evidence_folder, matter="M-01", max_calls=2):
        raw = json.loads((Path(evidence_folder) / "Clause Record.json").read_text(encoding="utf-8"))
        self.records = raw if isinstance(raw, list) else [raw]
        self.matter = matter
        self.max_calls = max_calls
        self.calls = 0

    def handle(self, request, untrusted_note=None):
        """Return (decision, detail). decision is EXECUTED, DENIED or HELD."""
        if not isinstance(request, dict):
            return "HELD", "malformed request"
        action = request.get("action")
        if action not in ALLOWED_OPERATIONS:
            return "DENIED", f"operation '{action}' is not offered by this host"
        extra = set(request) - ALLOWED_ARGUMENTS
        if extra:
            return "DENIED", "unexpected arguments: " + ", ".join(sorted(extra))
        match = [r for r in self.records
                 if r["document_id"] == request.get("contract_id")
                 and str(r["clause"]) == str(request.get("clause"))
                 and r.get("matter") == self.matter]
        if not match:
            return "DENIED", "no permitted record for this document and clause in this matter"
        if self.calls >= self.max_calls:
            return "HELD", f"call budget of {self.max_calls} is used up"
        self.calls += 1
        r = match[0]
        result = {k: r[k] for k in ("document_id", "version", "clause", "text", "source_location")}
        if untrusted_note:
            result["untrusted_document_note"] = untrusted_note
        return "EXECUTED", result
