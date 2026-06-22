# -*- coding: utf-8 -*-
"""Minimal ULID — the seam's idempotency key (Crockford base32, 26 chars).

48-bit millisecond timestamp (10 chars) + 80-bit randomness (16 chars). Stdlib only.
"""
import os, time

_C = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"   # Crockford base32 (no I, L, O, U)
_SET = frozenset(_C)


def _enc(n, length):
    s = []
    for _ in range(length):
        s.append(_C[n & 31])
        n >>= 5
    return "".join(reversed(s))


def new_ulid(ms=None):
    if ms is None:
        ms = int(time.time() * 1000)
    rand = int.from_bytes(os.urandom(10), "big")     # 80 bits
    return _enc(ms, 10) + _enc(rand, 16)


def is_ulid(s):
    return isinstance(s, str) and len(s) == 26 and all(c in _SET for c in s.upper())
