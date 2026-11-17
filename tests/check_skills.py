#!/usr/bin/env python3
"""Check the SKILL.md: frontmatter, description length, files it names, and no em dashes anywhere in the skill."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
skills = glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))
if not skills:
    errors.append("no skills/<name>/SKILL.md found")
for skill_md in skills:
    folder = os.path.dirname(skill_md)
    text = open(skill_md, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{skill_md}: no frontmatter")
        continue
    front = m.group(1)
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    if not name or name.group(1).strip() != os.path.basename(folder):
        errors.append(f"{skill_md}: name must match the folder name")
    if not desc or len(desc.group(1)) > 1024:
        errors.append(f"{skill_md}: description missing or longer than 1024 characters")
    for md in glob.glob(os.path.join(folder, "**", "*.md"), recursive=True):
        body = open(md, encoding="utf-8").read()
        for ref in set(re.findall(r"`((?:references|templates|scripts)/[\w\-.]+)`", body)):
            if not os.path.exists(os.path.join(folder, ref)):
                errors.append(f"{md}: names {ref}, which does not exist")
        if "\u2014" in body:
            errors.append(f"{md}: contains an em dash")

for e in errors:
    print(e)
print(f"{len(errors)} problem(s)")
sys.exit(1 if errors else 0)
