# -*- coding: utf-8 -*-
"""Fetch a Google Sheet as CSV from its link (no auth) — for sheets shared as
"Anyone with the link can view" or published to the web. Private sheets need the
Drive connector instead (the agent downloads them); this helper is the portable,
standalone path. Stdlib only.
"""
import re, urllib.request, urllib.error

_ID_RE = re.compile(r"/spreadsheets/d/([a-zA-Z0-9\-_]+)")
_GID_RE = re.compile(r"[#&?]gid=(\d+)")
_BARE_ID_RE = re.compile(r"^[a-zA-Z0-9\-_]{20,}$")

_PRIVATE_HINT = ("the sheet isn't readable from its link. Either share it as "
                 "'Anyone with the link can view', or File > Download > CSV and pass that "
                 "with --recipients, or (in Claude Code) let the agent fetch it via the Drive connector.")


def extract_id_gid(url_or_id):
    s = (url_or_id or "").strip()
    m = _ID_RE.search(s)
    if m:
        sid = m.group(1)
    elif _BARE_ID_RE.match(s):
        sid = s
    else:
        raise ValueError("could not find a Google Sheets id in: %r" % url_or_id)
    g = _GID_RE.search(s)
    return sid, (g.group(1) if g else "0")


def export_csv_url(sid, gid="0"):
    return "https://docs.google.com/spreadsheets/d/%s/export?format=csv&gid=%s" % (sid, gid)


def fetch_csv(url_or_id, dest_path):
    """Download the sheet as CSV to dest_path. Raises ValueError with a helpful
    message if the sheet is private / not link-viewable."""
    sid, gid = extract_id_gid(url_or_id)
    req = urllib.request.Request(export_csv_url(sid, gid), headers={"User-Agent": "iksula-leadgen"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            ctype = (r.headers.get("Content-Type") or "").lower()
    except urllib.error.HTTPError as e:
        raise ValueError("Google rejected the export (HTTP %s) — %s" % (e.code, _PRIVATE_HINT))
    except urllib.error.URLError as e:
        raise ValueError("network error fetching the sheet: %s" % e.reason)
    head = data[:200].lstrip().lower()
    if "text/html" in ctype or head.startswith(b"<!doctype html") or head.startswith(b"<html") \
            or b"accounts.google.com" in data[:2000].lower():
        raise ValueError(_PRIVATE_HINT)
    with open(dest_path, "wb") as f:
        f.write(data)
    return dest_path
