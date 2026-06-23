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

    def test_draft_shell_is_create_only_dry_run(self):
        os.environ["WOODPECKER_AGENT_BUILD"] = "on"
        os.environ["WOODPECKER_ALLOWED_MAILBOX_IDS"] = "warm-1"
        from leadgen import config as lc
        lc.LEDGER_PATH = os.path.join(self.d, "ledger.jsonl")
        res = s2r.build_draft("[LG-AGENT] dj sheet 2606 r1", "warm-1", "Subj", "Body",
                              run_id="r1", created_at_utc="t", dry_run=True)
        self.assertEqual(res["status"], "DRAFT")
        self.assertTrue(res["dry_run"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
