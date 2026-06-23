# -*- coding: utf-8 -*-
"""Safety tests for the Growth Hacker toolkit. Run from D:\\Y\\DJ:
    python -m unittest growthhacker.tests.test_safety
No posting, no email, no live account.
"""
import os, json, tempfile, unittest
from growthhacker import config, publish_gate, seam_emitter, brain_metrics, ulid, audit

ORGANIC_OK = {
    "type": "organic_post", "channel": "LinkedIn-post", "asset_ref": "PC2-post-01",
    "utm": "utm_source=li", "tracked_cta": "https://iksula.co/x?c=1", "calendar_status": "Scheduled",
}
EVENT_OK = {
    "source_asset_ref": "PC2-post-01", "source_channel": "LinkedIn-post",
    "intent_signal": {"signal_type": "comment", "verbatim_text": "interested", "observed_at": "t"},
    "region": "US", "captured_at": "2026-06-22T00:00:00Z",
    "contact_identity": {"platform_handle": "@priya"},
}


class PublishGateTests(unittest.TestCase):
    def setUp(self):
        os.environ["GROWTH_PUBLISH"] = "on"

    def test_switch_off_holds(self):
        os.environ["GROWTH_PUBLISH"] = "off"
        self.assertEqual(publish_gate.evaluate(ORGANIC_OK)["verdict"], "HOLD")

    def test_organic_full_pass(self):
        self.assertEqual(publish_gate.evaluate(ORGANIC_OK)["verdict"], "ALLOW")

    def test_uninstrumented_held(self):
        a = {**ORGANIC_OK}; a.pop("utm")
        v = publish_gate.evaluate(a)
        self.assertEqual(v["verdict"], "HOLD")
        self.assertTrue(any("not_instrumented" in h for h in v["holds"]))

    def test_unscheduled_held(self):
        v = publish_gate.evaluate({**ORGANIC_OK, "calendar_status": "Planned"})
        self.assertTrue(any("calendar_row_not_scheduled" in h for h in v["holds"]))

    def test_paid_without_budget_held(self):
        a = {**ORGANIC_OK, "type": "paid_post"}
        v = publish_gate.evaluate(a)
        self.assertTrue(any("paid_without_budget_approval" in h for h in v["holds"]))
        a2 = {**a, "budget_approved": True}
        self.assertEqual(publish_gate.evaluate(a2)["verdict"], "ALLOW")

    def test_named_byline_requires_voice_approval(self):
        a = {"type": "community_reply_as_byline", "channel": "LinkedIn-post",
             "asset_ref": "x", "is_named_byline": True}
        v = publish_gate.evaluate(a)
        self.assertTrue(any("byline_voice_not_approved" in h for h in v["holds"]))
        self.assertEqual(publish_gate.evaluate({**a, "approval_token": "dj-ok"})["verdict"], "ALLOW")

    def test_byline_without_flag_still_gated(self):
        # the voice gate must NOT be opt-in via a caller-supplied flag
        a = {"type": "community_reply_as_byline", "channel": "LinkedIn-post", "asset_ref": "x"}
        v = publish_gate.evaluate(a)
        self.assertEqual(v["verdict"], "HOLD")
        self.assertTrue(any("byline_voice_not_approved" in h for h in v["holds"]))

    def test_broadcast_email_requires_human(self):
        a = {"type": "broadcast_email", "channel": "Telegram", "asset_ref": "x"}
        v = publish_gate.evaluate(a)
        self.assertTrue(any("broadcast_first_send_not_human_approved" in h for h in v["holds"]))

    def test_broadcast_email_requires_instrumentation(self):
        a = {"type": "broadcast_email", "channel": "Telegram", "asset_ref": "x", "approval_token": "ok"}
        v = publish_gate.evaluate(a)
        self.assertTrue(any("not_instrumented" in h for h in v["holds"]))

    def test_bad_channel_held(self):
        v = publish_gate.evaluate({**ORGANIC_OK, "channel": "cold-email"})
        self.assertTrue(any("channel_not_allowed" in h for h in v["holds"]))


class SeamEmitterTests(unittest.TestCase):
    def setUp(self):
        self.q = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl").name
        os.remove(self.q)  # start empty

    def tearDown(self):
        if os.path.exists(self.q):
            os.remove(self.q)

    def test_rejects_score_field(self):
        with self.assertRaises(ValueError):
            seam_emitter.emit({**EVENT_OK, "score": 9}, queue_path=self.q)

    def test_rejects_ack_status(self):
        with self.assertRaises(ValueError):
            seam_emitter.emit({**EVENT_OK, "ack_status": "received"}, queue_path=self.q)

    def test_rejects_bad_signal_type(self):
        bad = {**EVENT_OK, "intent_signal": {"signal_type": "purchase"}}
        with self.assertRaises(ValueError):
            seam_emitter.emit(bad, queue_path=self.q)

    def test_rejects_nested_score_in_signal(self):
        bad = {**EVENT_OK, "intent_signal": {"signal_type": "comment", "score": 99, "mql": True}}
        with self.assertRaises(ValueError):
            seam_emitter.emit(bad, queue_path=self.q)

    def test_rejects_nested_account_status_in_identity(self):
        bad = {**EVENT_OK, "contact_identity": {"platform_handle": "@p", "account_status": "ECS"}}
        with self.assertRaises(ValueError):
            seam_emitter.emit(bad, queue_path=self.q)

    def test_rejects_qualification_synonyms(self):
        for k in ("tier", "lead_grade", "disposition", "MQL ", "propensity"):
            with self.assertRaises(ValueError):
                seam_emitter.emit({**EVENT_OK, k: "x"}, queue_path=self.q)

    def test_requires_asset_ref(self):
        bad = {**EVENT_OK}; bad.pop("source_asset_ref")
        with self.assertRaises(ValueError):
            seam_emitter.emit(bad, queue_path=self.q)

    def test_us_region_person_level_tag(self):
        r = seam_emitter.emit(EVENT_OK, queue_path=self.q)
        self.assertEqual(r["status"], "emitted")
        self.assertIn("person-level", r["lawful_basis_tag"])

    def test_non_us_region_company_level_failsafe(self):
        for region in ("DE", "India", "", None, "Brazil"):
            r = seam_emitter.emit({**EVENT_OK, "region": region,
                                   "correlation_id": ulid.new_ulid()}, queue_path=self.q)
            self.assertIn("company-level", r["lawful_basis_tag"])

    def test_idempotent_duplicate_is_noop(self):
        cid = ulid.new_ulid()
        e = {**EVENT_OK, "correlation_id": cid}
        first = seam_emitter.emit(e, queue_path=self.q)
        second = seam_emitter.emit(e, queue_path=self.q)
        self.assertEqual(first["status"], "emitted")
        self.assertEqual(second["status"], "duplicate")
        with open(self.q, encoding="utf-8") as f:
            self.assertEqual(sum(1 for _ in f), 1)

    def test_emitted_record_shape(self):
        seam_emitter.emit(EVENT_OK, queue_path=self.q)
        with open(self.q, encoding="utf-8") as f:
            rec = json.loads(f.readline())
        self.assertEqual(rec["emitted_by"], "growth-hacker")
        self.assertIsNone(rec["ack_status"])          # GH never sets ack
        self.assertTrue(ulid.is_ulid(rec["correlation_id"]))


class BrainMetricsTests(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()

    def test_valid_aggregate_writes(self):
        rows = [{"period": "2026-06", "source": "li", "asset_or_campaign": "PC2",
                 "channel": "LinkedIn", "metric": "impressions", "value": 1200,
                 "audience_type": "US-core", "notes": ""}]
        res = brain_metrics.write_growth_metrics(rows, "260622", base_dir=self.base)
        self.assertEqual(res["written"], 1)

    def test_rejects_pii_row(self):
        rows = [{"period": "2026-06", "source": "li", "asset_or_campaign": "PC2",
                 "channel": "LinkedIn", "metric": "x", "value": 1,
                 "audience_type": "US", "notes": "", "email": "a@b.com"}]
        with self.assertRaises(ValueError):
            brain_metrics.write_growth_metrics(rows, "260622", base_dir=self.base)

    def test_rejects_email_in_value(self):
        rows = [{"period": "2026-06", "source": "li", "asset_or_campaign": "PC2",
                 "channel": "LinkedIn", "metric": "x", "value": 1,
                 "audience_type": "US", "notes": "ping a@b.com"}]
        with self.assertRaises(ValueError):
            brain_metrics.write_growth_metrics(rows, "260622", base_dir=self.base)

    def test_rejects_nonprimitive_cell(self):
        rows = [{"period": "2026-06", "source": "li", "asset_or_campaign": "PC2",
                 "channel": "LinkedIn", "metric": "x", "value": 1,
                 "audience_type": "US", "notes": {"email": "a@b.com"}}]
        with self.assertRaises(ValueError):
            brain_metrics.write_growth_metrics(rows, "260622", base_dir=self.base)

    def test_rejects_handle_in_notes(self):
        rows = [{"period": "2026-06", "source": "li", "asset_or_campaign": "PC2",
                 "channel": "LinkedIn", "metric": "x", "value": 1,
                 "audience_type": "US", "notes": "from @priya"}]
        with self.assertRaises(ValueError):
            brain_metrics.write_growth_metrics(rows, "260622", base_dir=self.base)


class AuditScrubTests(unittest.TestCase):
    def test_recursive_redaction(self):
        scrubbed = audit._scrub({
            "details": {"who": "priya@acme.com", "h": "@priya"},
            "winners": ["x@y.com", "ok"],
            "count": 5,
        })
        blob = json.dumps(scrubbed)
        self.assertNotIn("priya@acme.com", blob)
        self.assertNotIn("@priya", blob)
        self.assertNotIn("x@y.com", blob)
        self.assertIn("5", blob)               # non-PII metadata preserved


class UlidTests(unittest.TestCase):
    def test_format(self):
        u = ulid.new_ulid()
        self.assertEqual(len(u), 26)
        self.assertTrue(ulid.is_ulid(u))
        self.assertFalse(ulid.is_ulid("not-a-ulid"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
