#!/usr/bin/env python3
"""Print '*<skill>* — <description>' for each skill SKILL.md added/changed between two shas."""
import subprocess, sys, re, os

base, head = sys.argv[1], sys.argv[2]
try:
    out = subprocess.check_output(["git", "diff", "--name-only", base, head], text=True)
except Exception:
    sys.exit(0)

skills, lines = set(), []
for f in out.splitlines():
    m = re.search(r"(skills/[^/]+)/SKILL\.md$", f)
    if m:
        skills.add(m.group(1) + "/SKILL.md")

def desc(path):
    if not os.path.exists(path):
        return ""
    t = open(path, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---", t, re.DOTALL)
    if not fm:
        return ""
    body = fm.group(1).splitlines()
    for i, ln in enumerate(body):
        if ln.startswith("description:"):
            val = ln.split(":", 1)[1].strip()
            if val in (">-", ">", "|", "|-", ""):  # folded/blocked scalar -> gather indented lines
                buf = []
                for nx in body[i+1:]:
                    if nx.strip() == "" or nx[:1] in (" ", "\t"):
                        buf.append(nx.strip())
                    else:
                        break
                return " ".join(x for x in buf if x).strip()
            return val.strip().strip('"').strip("'")
    return ""

for s in sorted(skills):
    name = s.split("/")[1] if s.startswith("skills/") else s
    # path may be plugins/iksula-agents/skills/<name>/SKILL.md
    full = subprocess.check_output(["git", "diff", "--name-only", base, head], text=True)
    cand = [p for p in full.splitlines() if p.endswith(s) or p.endswith("/"+s)]
    path = cand[0] if cand else s
    d = desc(path)
    d = (d[:280] + "…") if len(d) > 281 else d
    lines.append(f"*{name}* — {d}" if d else f"*{name}*")

print("\n".join(lines))
