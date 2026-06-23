# -*- coding: utf-8 -*-
"""Brain writer guard — performance-analytics-growth (AGGREGATE only, NO PII).

The Brain is append-only aggregates, one writer per namespace, no per-prospect PII.
This makes that structural: every row must match the fixed schema exactly, and any
row that looks like per-prospect PII (or carries an off-schema key) is REJECTED.
Raw-first: dumps to _brain/_raw/ before writing the synthesised feed.
"""
import os, re, csv, io
from . import config

_EMAIL_RE = re.compile(r"[^\s@]+@[^\s@]+\.[^\s@]+")
_HANDLE_RE = re.compile(r"@[A-Za-z][A-Za-z0-9_]{1,}")    # @handle (not '@9am')
_PRIMITIVE = (str, int, float, bool, type(None))


def _value_has_pii(v):
    s = "%s" % (v,)
    return bool(_EMAIL_RE.search(s) or _HANDLE_RE.search(s))


def validate_rows(rows):
    """Raise if any row breaks the schema lock, carries a non-primitive cell (an
    aggregate cell is never a dict/list), or looks like per-prospect PII. Returns rows."""
    allowed = set(config.BRAIN_METRIC_SCHEMA)
    for i, row in enumerate(rows):
        extra = set(row) - allowed
        if extra:
            raise ValueError("row %d has non-schema keys %s (Brain feed is fixed-schema)" % (i, sorted(extra)))
        for k, v in row.items():
            if any(p in str(k).lower() for p in config.PII_LIKE_KEYS):
                raise ValueError("row %d key %r is PII-like — the Brain is aggregates-only" % (i, k))
            if not isinstance(v, _PRIMITIVE):
                raise ValueError("row %d cell %r is non-primitive (%s) — aggregates only, no nested objects"
                                 % (i, k, type(v).__name__))
            if _value_has_pii(v):
                raise ValueError("row %d value under %r looks like PII (email/@handle)" % (i, k))
    return rows


def write_growth_metrics(rows, yymmdd, raw_note="raw capture", base_dir=None):
    """Append validated aggregate rows to performance-analytics-growth-YYMMDD.csv.
    yymmdd is supplied by the caller (no clock here). Raw-first to _brain_raw."""
    validate_rows(rows)
    base = base_dir or config.ROOT
    raw_dir = os.path.join(base, "_state", "_brain_raw")
    feed_dir = os.path.join(base, "_state", "_brain_feeds")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(feed_dir, exist_ok=True)

    # raw-first: dump the raw rows before the synthesised feed
    raw_path = os.path.join(raw_dir, "performance-analytics-growth-%s-raw.csv" % yymmdd)
    _append_csv(raw_path, rows)

    feed_path = os.path.join(feed_dir, "performance-analytics-growth-%s.csv" % yymmdd)
    _append_csv(feed_path, rows)
    return {"written": len(rows), "feed": feed_path, "raw": raw_path}


def _append_csv(path, rows):
    new = not os.path.exists(path)
    with io.open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(config.BRAIN_METRIC_SCHEMA))
        if new:
            w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in config.BRAIN_METRIC_SCHEMA})
