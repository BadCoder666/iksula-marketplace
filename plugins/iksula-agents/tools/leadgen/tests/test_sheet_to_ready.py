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


class StageCampaignTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.csv = os.path.join(self.d, "rec.csv")

    def _write(self, rows):
        _csv(self.csv, rows, ["email", "first_name", "company", "snippet1", "snippet2", "snippet3"])

    def test_read_requires_snippet_columns(self):
        from leadgen import stage_campaign as sc
        _csv(self.csv, [{"email": "a@x.example"}], ["email"])
        with self.assertRaises(ValueError):
            sc._read_recipients(self.csv)

    def test_validate_drops_empty_and_unsafe_copy(self):
        from leadgen import stage_campaign as sc
        self._write([
            {"email": "a@x.example", "first_name": "A", "company": "C", "snippet1": "one", "snippet2": "two", "snippet3": "three"},
            {"email": "b@x.example", "first_name": "B", "company": "C", "snippet1": "", "snippet2": "two", "snippet3": "three"},
            {"email": "c@x.example", "first_name": "C", "company": "C", "snippet1": "has {{TOKEN}}", "snippet2": "two", "snippet3": "three"},
        ])
        ok, problems = sc.validate(sc._read_recipients(self.csv))
        self.assertEqual([r["email"] for r in ok], ["a@x.example"])
        self.assertEqual(len(problems), 2)

    def test_steps_spec_uses_verified_snippet_syntax(self):
        from leadgen import stage_campaign as sc
        spec = sc._steps_spec(sc.DEFAULT_SUBJECTS, sc.DEFAULT_DELAYS)
        self.assertEqual(len(spec), 3)
        self.assertIn('{{SNIPPET_1 | "', spec[0]["message"])
        self.assertIn('{{SNIPPET_3 | "', spec[2]["message"])
        self.assertNotIn("{{SNIPPET1", spec[0]["message"])   # bare/no-underscore form 400s
        self.assertNotIn("UNSUBSCRIBE", spec[0]["message"])  # gdpr auto-unsub, no manual token

    def test_stage_dry_run_builds_and_enrolls(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "779999"
        from leadgen import config as lc, stage_campaign as sc
        lc.LEDGER_PATH = os.path.join(self.d, "ledger_sc.jsonl")
        self._write([
            {"email": "a@x.example", "first_name": "A", "company": "C", "snippet1": "1", "snippet2": "2", "snippet3": "3"},
            {"email": "b@x.example", "first_name": "B", "company": "C", "snippet1": "1", "snippet2": "2", "snippet3": "3"},
        ])
        res = sc.stage(self.csv, "779999", commit=False)
        self.assertTrue(res["ok"]); self.assertEqual(res["status"], "DRAFT")
        self.assertTrue(res["dry_run"]); self.assertEqual(res["enrolled"], 2)

    def test_stage_refuses_primary_mailbox(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "779999"
        from leadgen import config as lc, stage_campaign as sc
        from leadgen.wp_client import ForbiddenAction
        lc.LEDGER_PATH = os.path.join(self.d, "ledger_sc2.jsonl")
        self._write([{"email": "a@x.example", "first_name": "A", "company": "C",
                      "snippet1": "1", "snippet2": "2", "snippet3": "3"}])
        with self.assertRaises(ForbiddenAction):
            sc.stage(self.csv, "someone@iksula.com", commit=False)

    def test_paragraphize_breaks_wall_of_text(self):
        from leadgen import stage_campaign as sc
        msg = ("Hi Zainab, I came across your profile and was impressed by your work as Senior "
               "Conference Producer at eTail. We help retail and DTC brands accelerate commerce "
               "transformation. Clients typically see 15-25% improvements in digital conversion. "
               "Could we find 20 minutes next week?")
        out = sc.paragraphize(msg)
        self.assertIn("<br><br>", out)                       # got paragraph breaks
        self.assertTrue(out.startswith("Hi Zainab,"))        # greeting leads the first paragraph
        self.assertTrue(out.rstrip().endswith("?"))          # CTA question is its own last paragraph
        self.assertEqual(out.count("<br><br>"), 2)           # greeting | body | CTA -> 3 paras
        self.assertIn("15-25%", out)                         # did NOT split on the numeric range

    def test_paragraphize_preserves_author_newlines(self):
        # The real-world case: copy already has \n\n paragraph breaks (which Woodpecker collapses
        # in HTML) plus a two-line sign-off. We must convert them to explicit <br> tags.
        from leadgen import stage_campaign as sc
        copy = ("Hi Paul,\n\nI came across your profile at Wayfair.\n\n"
                "We help brands accelerate commerce. Clients see 15-25% gains.\n\n"
                "Best,\nRohit - Iksula")
        out = sc.paragraphize(copy)
        self.assertNotIn("\n", out)                              # no raw newlines survive
        self.assertEqual(out.count("<br><br>"), 3)               # 4 paragraphs -> 3 gaps
        self.assertTrue(out.endswith("Best,<br>Rohit - Iksula"))  # single newline -> single <br>
        self.assertIn("15-25%", out)

    def test_strip_signoff_removes_trailing_signature(self):
        from leadgen import stage_campaign as sc
        # one-paragraph sign-off ("Best,\nRohit - Iksula") -> gone, body preserved
        c1 = "Hi Paul,\n\nWe help brands grow.\n\nWould you be open to 20 minutes?\n\nBest,\nRohit - Iksula"
        out = sc.strip_signoff(c1)
        self.assertTrue(out.rstrip().endswith("20 minutes?"))
        self.assertNotIn("Rohit", out)
        self.assertNotIn("Best,", out)
        # valediction and name in SEPARATE paragraphs -> both removed
        c2 = "Hi A,\n\nBody here.\n\nRegards,\n\nJane Doe"
        out2 = sc.strip_signoff(c2)
        self.assertTrue(out2.rstrip().endswith("Body here."))
        self.assertNotIn("Jane", out2); self.assertNotIn("Regards", out2)

    def test_strip_signoff_leaves_normal_copy_alone(self):
        from leadgen import stage_campaign as sc
        # no sign-off -> unchanged
        c = "Hi A,\n\nThanks to your team's great work this quarter, we should talk. Free Tuesday?"
        self.assertEqual(sc.strip_signoff(c), c)   # mid-sentence 'Thanks' is NOT a valediction line
        # stage() strips the sign-off so it can't double the template signature
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "779999"
        from leadgen import config as lc, wp_client
        lc.LEDGER_PATH = os.path.join(self.d, "ledger_sig.jsonl")
        cap = {}
        orig = wp_client.WoodpeckerClient.enroll_to_draft
        wp_client.WoodpeckerClient.enroll_to_draft = lambda self, cid, rows: (cap.setdefault("r", []).extend(rows), {"enrolled": len(rows), "dry_run": True})[1]
        self._write([{"email": "a@x.example", "first_name": "A", "company": "C",
                      "snippet1": "Hi A,\n\nBody.\n\nOpen to a call?\n\nBest,\nRohit - Iksula",
                      "snippet2": "s2", "snippet3": "s3"}])
        try:
            sc.stage(self.csv, "779999", commit=False, sender_name="Vishal Sobti", sender_title="Partnerships")
        finally:
            wp_client.WoodpeckerClient.enroll_to_draft = orig
        self.assertNotIn("Rohit", cap["r"][0]["snippet1"])   # copy sign-off stripped before enroll

    def test_strip_subject_line_removes_embedded_subject(self):
        from leadgen import stage_campaign as sc
        c = "Subject: Helping Acme Accelerate Commerce\n\nHi Dana,\n\nWe help brands. Free Tuesday?"
        out = sc.strip_subject_line(c)
        self.assertFalse(out.lower().startswith("subject"))
        self.assertTrue(out.startswith("Hi Dana,"))
        # copy without a subject line is untouched
        self.assertEqual(sc.strip_subject_line("Hi Dana,\n\nBody."), "Hi Dana,\n\nBody.")
        # full pipeline in stage(): embedded subject stripped before enroll
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"; os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "779999"
        from leadgen import config as lc, wp_client
        lc.LEDGER_PATH = os.path.join(self.d, "ledger_subj.jsonl")
        cap = {}
        orig = wp_client.WoodpeckerClient.enroll_to_draft
        wp_client.WoodpeckerClient.enroll_to_draft = lambda self, cid, rows: (cap.setdefault("r", []).extend(rows), {"enrolled": len(rows), "dry_run": True})[1]
        self._write([{"email": "a@x.example", "first_name": "A", "company": "C",
                      "snippet1": "Subject: Hi there\n\nHi A,\n\nBody. Worth a call?", "snippet2": "s2", "snippet3": "s3"}])
        try:
            sc.stage(self.csv, "779999", commit=False, sender_name="Vishal Sobti")
        finally:
            wp_client.WoodpeckerClient.enroll_to_draft = orig
        self.assertNotIn("Subject", cap["r"][0]["snippet1"])

    def test_footer_fills_sender_identity(self):
        from leadgen import stage_campaign as sc
        f = sc._footer("Vishal Sobti", "Partnerships")
        self.assertIn("Vishal Sobti, Partnerships", f)
        self.assertNotIn("[Sender Name]", f)
        self.assertIn("[REGISTERED POSTAL ADDRESS REQUIRED BEFORE SEND]", f)

    def test_paragraphize_is_idempotent_and_safe(self):
        from leadgen import stage_campaign as sc
        self.assertEqual(sc.paragraphize(""), "")
        self.assertEqual(sc.paragraphize("One short line."), "One short line.")   # single sentence untouched
        pre = "Line one.<br><br>Line two."
        self.assertEqual(sc.paragraphize(pre), pre)                               # already formatted -> unchanged
        # never introduces a token-breaking char
        out = sc.paragraphize("Hi A. We do X. Worth a call?")
        for bad in ("{{", "}}", "|"):
            self.assertNotIn(bad, out)

    def test_stage_splits_paragraphs_into_separate_snippets(self):
        # The multi-paragraph message must become ONE snippet per paragraph (NOT <br> inside one
        # snippet — Woodpecker flattens snippet-internal HTML). The template carries the <p> tags.
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "779999"
        from leadgen import config as lc, stage_campaign as sc, wp_client
        lc.LEDGER_PATH = os.path.join(self.d, "ledger_fmt.jsonl")
        captured = {}
        m1 = "Hi A,\n\nI saw your work at C.\n\nWe help brands grow commerce.\n\nCould we talk 20 min?"
        self._write([{"email": "a@x.example", "first_name": "A", "company": "C",
                      "snippet1": m1, "snippet2": "Follow up para one.\n\nPara two.", "snippet3": "Direct ask?"}])
        orig = wp_client.WoodpeckerClient.enroll_to_draft
        wp_client.WoodpeckerClient.enroll_to_draft = lambda self, cid, rows: (captured.setdefault("rows", []).extend(rows), {"enrolled": len(rows), "dry_run": True})[1]
        try:
            res = sc.stage(self.csv, "779999", commit=False)
        finally:
            wp_client.WoodpeckerClient.enroll_to_draft = orig
        self.assertTrue(res["ok"])
        row = captured["rows"][0]
        self.assertEqual(row["snippet1"], "Hi A,")                 # 1st paragraph = its own snippet
        self.assertEqual(row["snippet2"], "I saw your work at C.")  # 2nd paragraph = next snippet
        for k, v in row.items():                                   # NO <br> anywhere in a snippet value
            if k.startswith("snippet"):
                self.assertNotIn("<br", v.lower())
        self.assertEqual(res["slots"], [4, 2, 1])                  # step1=4 paras, step2=2, step3=1

    def test_steps_spec_paragraphed_builds_p_per_slot(self):
        from leadgen import stage_campaign as sc
        spec = sc._steps_spec_paragraphed(sc.DEFAULT_SUBJECTS, sc.DEFAULT_DELAYS, [3, 2, 1], sc._footer("V"))
        self.assertEqual(spec[0]["message"].count("<p>{{SNIPPET_"), 3)   # step1: 3 paragraph <p>s
        self.assertIn('{{SNIPPET_1 | " "}}', spec[0]["message"])         # global numbering, verified syntax
        self.assertIn('{{SNIPPET_4 | " "}}', spec[1]["message"])         # step2 starts at snippet4
        self.assertIn('{{SNIPPET_6 | " "}}', spec[2]["message"])         # step3 starts at snippet6

    def test_allocate_slots_respects_15_budget(self):
        from leadgen import stage_campaign as sc
        self.assertEqual(sc._allocate_slots([5, 6, 5]), [5, 5, 5])   # 16 -> trim largest to fit 15
        self.assertEqual(sum(sc._allocate_slots([9, 9, 9])), 15)     # never exceeds the 15 budget
        self.assertEqual(sc._allocate_slots([2, 1, 3]), [2, 1, 3])   # under budget -> unchanged

    def test_body_template_is_readable_and_footer_closed(self):
        from leadgen import stage_campaign as sc
        spec = sc._steps_spec(sc.DEFAULT_SUBJECTS, sc.DEFAULT_DELAYS)
        msg = spec[0]["message"]
        self.assertIn("line-height", msg)                            # breathing room, not a wall
        self.assertIn("[REGISTERED POSTAL ADDRESS REQUIRED BEFORE SEND]", msg)  # closing ] present
        self.assertEqual(msg.count("<div"), msg.count("</div"))      # balanced wrappers


if __name__ == "__main__":
    unittest.main(verbosity=2)
