# -*- coding: utf-8 -*-
"""Tests for sheet_to_ready (the AI-preps/human-sends pipeline). Run from tools/:
    python -m unittest leadgen.tests.test_sheet_to_ready
No network, no sending."""
import os, csv, io, tempfile, unittest
from leadgen import sheet_to_ready as s2r


def _csv(path, rows, header):
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header); w.writeheader()
        for r in rows:
            w.writerow(r)


class SheetToReadyTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.rec = os.path.join(self.d, "r.csv")
        self.sup = os.path.join(self.d, "s.csv")

    def test_clean_dedupe_suppress_then_ready(self):
        _csv(self.rec, [
            {"email": "A@x.example", "first_name": "A", "company": "Acme"},
            {"email": "a@x.example", "first_name": "A", "company": "Acme"},   # duplicate (case-insensitive)
            {"email": "bad", "first_name": "B", "company": "B"},              # bad email
            {"email": "c@y.example", "first_name": "C", "company": "Cee"},
            {"email": "client@z.example", "first_name": "D", "company": "Zed"},  # suppressed
        ], ["email", "first_name", "company"])
        _csv(self.sup, [{"email": "client@z.example"}], ["email"])
        out = s2r.build_package(self.rec, "{{company}} hi", "Hi {{first_name}}",
                                suppress_csv=self.sup, out_dir=os.path.join(self.d, "pkg"))
        self.assertTrue(out["ready"])
        st = out["recipients"]
        self.assertEqual(st["kept"], 2)
        self.assertEqual(st["dropped_duplicate"], 1)
        self.assertEqual(st["dropped_bad_email"], 1)
        self.assertEqual(st["dropped_suppressed"], 1)
        self.assertTrue(os.path.exists(out["outputs"]["recipients_ready_csv"]))

    def test_merge_leak_blocks_ready(self):
        _csv(self.rec, [{"email": "a@x.example", "first_name": "A", "company": ""}],
             ["email", "first_name", "company"])
        out = s2r.build_package(self.rec, "{{company}}", "Hi {{first_name}} at {{company}}",
                                out_dir=os.path.join(self.d, "pkg2"))
        self.assertFalse(out["ready"])
        self.assertFalse(out["merge_preview"]["clean"])

    def test_no_email_column_raises(self):
        _csv(self.rec, [{"name": "A"}], ["name"])
        with self.assertRaises(ValueError):
            s2r.build_package(self.rec, "x", "y", out_dir=os.path.join(self.d, "pkg3"))

    def test_zero_valid_recipients_not_ready(self):
        _csv(self.rec, [{"email": "bad", "first_name": "A", "company": "X"}],
             ["email", "first_name", "company"])
        out = s2r.build_package(self.rec, "{{company}}", "Hi {{first_name}}",
                                out_dir=os.path.join(self.d, "pkg4"))
        self.assertFalse(out["ready"])
        self.assertEqual(out["recipients"]["kept"], 0)

    def test_gsheet_url_parsing(self):
        from leadgen import gsheet
        sid, gid = gsheet.extract_id_gid("https://docs.google.com/spreadsheets/d/1AbC-_dEf/edit#gid=42")
        self.assertEqual(sid, "1AbC-_dEf"); self.assertEqual(gid, "42")
        sid2, gid2 = gsheet.extract_id_gid("https://docs.google.com/spreadsheets/d/1AbC-_dEf/edit")
        self.assertEqual(sid2, "1AbC-_dEf"); self.assertEqual(gid2, "0")   # default tab
        self.assertIn("export?format=csv&gid=42", gsheet.export_csv_url("1AbC-_dEf", "42"))
        with self.assertRaises(ValueError):
            gsheet.extract_id_gid("not a sheet link")

    def test_draft_shell_is_create_only_dry_run(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "warm-1"
        from leadgen import config as lc
        lc.LEDGER_PATH = os.path.join(self.d, "ledger.jsonl")
        res = s2r.build_draft("[LG-AGENT] dj sheet 2606 r1", "warm-1", "Subj", "Body",
                              run_id="r1", created_at_utc="t", dry_run=True)
        self.assertEqual(res["status"], "DRAFT")
        self.assertTrue(res["dry_run"])


    def test_merge_preview_case_insensitive(self):
        from leadgen import merge_preview
        out = merge_preview.validate("Hi {{FIRST_NAME}} at {{COMPANY}}",
                                     [{"first_name": "Sam", "company": "Acme"}])
        self.assertTrue(out["clean"])   # {{FIRST_NAME}} resolves a 'first_name' column

    def test_enroll_to_draft_dry_run_and_guards(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "779999"
        from leadgen import config as lc
        from leadgen.wp_client import WoodpeckerClient, ForbiddenAction
        lc.LEDGER_PATH = os.path.join(self.d, "ledger2.jsonl")
        res = s2r.build_draft("[LG-AGENT] sheet test", "779999", "S", "<p>B</p>",
                              run_id="r", created_at_utc="t", dry_run=True)
        cid = res["campaign_id"]
        c = WoodpeckerClient(dry_run=True)
        en = c.enroll_to_draft(cid, [{"email": "a@x.example", "first_name": "A", "company": "X"}])
        self.assertEqual(en["enrolled"], 1); self.assertTrue(en["dry_run"])
        with self.assertRaises(ForbiddenAction):          # foreign campaign
            c.enroll_to_draft("not-owned", [{"email": "a@x.example"}])
        os.environ["WOODPECKER_AGENT_BUILD"] = "off"
        with self.assertRaises(ForbiddenAction):          # kill switch off
            c.enroll_to_draft(cid, [{"email": "a@x.example"}])
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"

    def test_enroll_endpoint_does_not_open_a_send_path(self):
        # the add_prospects endpoint is allow-listed, but /run etc. are still blocked
        from leadgen.wp_client import WoodpeckerClient, ForbiddenAction
        c = WoodpeckerClient(key="t", dry_run=True)
        for method, path in (("POST", "/rest/v1/campaigns/1/run"),
                             ("PUT", "/rest/v2/campaigns/1"),
                             ("POST", "/rest/v2/campaigns/1/run")):
            with self.assertRaises(ForbiddenAction):
                c._http(method, path)

    def test_prospect_carries_snippets_only_when_present(self):
        # per-prospect snippets (snippet1..15) ride along to Woodpecker if supplied,
        # and are omitted entirely otherwise (so single-template flows are unaffected).
        from leadgen.wp_client import WoodpeckerClient
        with_snip = WoodpeckerClient._prospect(
            {"email": "A@x.example", "first_name": "A", "company": "Co",
             "snippet1": "warm 1", "snippet2": "warm 2", "snippet3": "direct"})
        self.assertEqual(with_snip["email"], "a@x.example")
        self.assertEqual(with_snip["snippet1"], "warm 1")
        self.assertEqual(with_snip["snippet3"], "direct")
        self.assertNotIn("snippet4", with_snip)
        plain = WoodpeckerClient._prospect({"email": "b@x.example", "first_name": "B"})
        self.assertFalse(any(k.startswith("snippet") for k in plain))

    def test_build_sequence_draft_is_three_step_create_only_dry_run(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "warm-1"
        from leadgen import config as lc
        lc.LEDGER_PATH = os.path.join(self.d, "ledger_seq.jsonl")
        spec = [
            {"subject": "s1 {{COMPANY}}", "message": '{{SNIPPET_1 | "fb"}}', "days_to_next": 3},
            {"subject": "s2", "message": '{{SNIPPET_2 | "fb"}}', "days_to_next": 4},
            {"subject": "s3", "message": '{{SNIPPET_3 | "fb"}}', "days_to_next": 1},
        ]
        res = s2r.build_sequence_draft("[LG-AGENT] seq test", "warm-1", spec,
                                       run_id="r", created_at_utc="t", dry_run=True)
        self.assertEqual(res["status"], "DRAFT")
        self.assertTrue(res["dry_run"])

    def test_build_sequence_draft_chains_followup_after(self):
        # verify the START -> EMAIL -> EMAIL -> EMAIL chain + per-step delays, without network
        import leadgen.wp_client as wc
        captured = {}

        def fake_create(self, name, mailbox_id, settings, steps, run_id=None, created_at_utc=None):
            captured["steps"] = steps
            return {"campaign_id": "DRYRUN", "status": "DRAFT", "dry_run": True}

        orig = wc.WoodpeckerClient.create_campaign
        wc.WoodpeckerClient.create_campaign = fake_create
        try:
            spec = [
                {"subject": "s1", "message": '{{SNIPPET_1 | "fb"}}', "days_to_next": 3},
                {"subject": "s2", "message": '{{SNIPPET_2 | "fb"}}', "days_to_next": 4},
                {"subject": "s3", "message": '{{SNIPPET_3 | "fb"}}', "days_to_next": 1},
            ]
            s2r.build_sequence_draft("[LG-AGENT] seq", "warm-1", spec, dry_run=True)
        finally:
            wc.WoodpeckerClient.create_campaign = orig
        steps = captured["steps"]
        self.assertEqual(steps["type"], "START")
        e1 = steps["followup"]; e2 = e1["followup"]; e3 = e2["followup"]
        self.assertEqual([e1["type"], e2["type"], e3["type"]], ["EMAIL", "EMAIL", "EMAIL"])
        self.assertEqual(e1["followup_after"], {"range": "DAY", "value": 3})
        self.assertEqual(e2["followup_after"], {"range": "DAY", "value": 4})
        self.assertIsNone(e3["followup"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
