# -*- coding: utf-8 -*-
"""Merge-preview validation — the curly-brace token-leak guardrail.

The worst-case Vishal named: a personalization field like {{company}} renders
literally to all 1,000 recipients. This renders a template against each prospect
row and reports EXACTLY which rows/fields would leak, so a campaign can be halted
before any send. Pure local logic — no network, no PII leaves the process.
"""
import re

# Woodpecker uses {{FIELD}} (and {{FIELD|fallback}}) snippet syntax.
TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*(?:\|([^}]*))?\}\}")


def required_fields(template):
    """Every merge field referenced in the template."""
    return [m.group(1) for m in TOKEN_RE.finditer(template or "")]


def render_row(template, row):
    """Render one row. Returns (rendered_text, leaked_fields).

    A field 'leaks' when it has no fallback and the row has no non-empty value
    for it — i.e. the literal {{field}} would survive into the sent email.
    """
    leaks = []
    lower = {str(k).lower(): v for k, v in (row or {}).items()}  # case-insensitive lookup

    def repl(m):
        field, fallback = m.group(1), m.group(2)
        val = row.get(field)
        if val is None or str(val).strip() == "":
            val = lower.get(field.lower())     # {{FIRST_NAME}} resolves a 'first_name' column
        if val is not None and str(val).strip() != "":
            return str(val)
        if fallback is not None:           # {{first_name|there}} -> 'there'
            return fallback
        leaks.append(field)                # no value, no fallback -> LEAK
        return m.group(0)                  # leave the literal token in place

    rendered = TOKEN_RE.sub(repl, template or "")
    return rendered, leaks


def validate(template, rows, subject=None):
    """Validate a template (+ optional subject) against all rows.

    Returns a dict: {clean: bool, total: int, leaking_rows: [...], fields: [...]}
    `clean` is True only if NO row leaks any field in subject or body.
    """
    fields = sorted(set(required_fields(subject or "") + required_fields(template)))
    leaking = []
    for i, row in enumerate(rows):
        _, body_leaks = render_row(template, row)
        subj_leaks = []
        if subject:
            _, subj_leaks = render_row(subject, row)
        all_leaks = sorted(set(body_leaks + subj_leaks))
        if all_leaks:
            leaking.append({
                "row_index": i,
                "email": row.get("email") or row.get("Email") or "<no-email>",
                "leaked_fields": all_leaks,
            })
    return {
        "clean": len(leaking) == 0,
        "total": len(rows),
        "leaking_count": len(leaking),
        "leaking_rows": leaking,
        "fields": fields,
    }
