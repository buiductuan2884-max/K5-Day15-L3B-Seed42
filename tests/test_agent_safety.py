"""Safety behavior of the fixed retrieval/decision workflow without API calls."""

import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "codebase"))
import agent  # noqa: E402


CURRENT = {
    "id": "SRC-CURRENT",
    "topic": "public_policy",
    "operator": "Demo operator",
    "text": "General policy: one free date change at least 12 hours before departure.",
    "source": "Public policy",
    "version": "2026-11-01",
}
EXPIRED = {
    "id": "SRC-OLD",
    "topic": "pet_policy",
    "operator": "Demo operator",
    "text": "Old pet rule.",
    "source": "Archived policy",
    "version": "2024-01-01 (hiệu lực đến 31/12/2025)",
}


def decision(kind, message, citations=None):
    return {"text": json.dumps({
        "decision": kind, "message": message, "citation_ids": citations or [],
        "summary": "Customer request", "category": "khac",
        "provided_fields": {}, "missing_fields": [],
    }, ensure_ascii=False)}


class AgentSafetyTests(unittest.TestCase):
    def answer_with(self, passages, reply):
        with patch.object(agent.tools, "search_knowledge", return_value=passages), \
             patch.object(agent.tools, "build_ticket_draft", return_value={"status": "draft"}), \
             patch.object(agent, "call_model", return_value=reply):
            return agent.answer("Customer request")

    def test_public_policy_answer_keeps_retrieved_citation(self):
        result = self.answer_with([CURRENT], decision(
            "answer", "One free date change at least 12 hours before departure.", ["SRC-CURRENT"]))
        self.assertIn("SRC-CURRENT", result["output"])
        self.assertNotIn("ticket_draft", result)

    def test_draft_never_claims_it_was_transferred(self):
        result = self.answer_with([CURRENT], decision(
            "ticket_draft", "Yêu cầu của bạn đã được chuyển cho nhân viên."))
        self.assertEqual(result["ticket_draft"]["status"], "draft")
        self.assertIn("bản nháp", result["output"])
        self.assertNotIn("đã được chuyển", result["output"])

    def test_draft_never_promises_payment_timing(self):
        result = self.answer_with([CURRENT], decision(
            "ticket_draft", "Tiền sẽ về tài khoản trong 3–7 ngày."))
        self.assertIn("bản nháp", result["output"])
        self.assertNotIn("Tiền sẽ về", result["output"])

    def test_expired_answer_becomes_explained_draft(self):
        result = self.answer_with([EXPIRED], decision(
            "answer", "The old rule is current.", ["SRC-OLD"]))
        self.assertEqual(result["ticket_draft"]["status"], "draft")
        self.assertIn("hết hiệu lực", result["output"])
        self.assertNotIn("The old rule is current", result["output"])

    def test_expired_only_clarification_becomes_draft(self):
        result = self.answer_with([EXPIRED], decision("clarify", "Which trip?"))
        self.assertEqual(result["ticket_draft"]["status"], "draft")
        self.assertIn("hết hiệu lực", result["output"])

    def test_draft_citing_old_source_explains_handoff(self):
        result = self.answer_with([EXPIRED, CURRENT], decision(
            "ticket_draft", "The cited policy expired.", ["SRC-OLD"]))
        self.assertEqual(result["ticket_draft"]["status"], "draft")
        self.assertIn("hết hiệu lực", result["output"])
        self.assertIn("nhân viên", result["output"])


if __name__ == "__main__":
    unittest.main()
