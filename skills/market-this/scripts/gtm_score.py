#!/usr/bin/env python3
"""Score the ten go-to-market pillars from a Market This dossier.

Usage: python3 gtm_score.py dossier.json
Prints the pillars in chain order, flags the weakest one (ties go to the
earlier pillar in the chain) and the overall score out of 100.
Standard library only.
"""
import json
import sys

CHAIN = ["market", "customer", "problem", "positioning", "offer",
         "pricing", "motion", "channels", "message", "proof"]


def band(score):
    if score is None:
        return "unknown"
    if score <= 3:
        return "weak"
    if score <= 6:
        return "moderate"
    return "strong"


def main(path):
    with open(path, encoding="utf-8") as f:
        dossier = json.load(f)
    pillars = {p["name"]: p for p in dossier.get("pillars", [])}
    rows, scored = [], []
    for i, name in enumerate(CHAIN):
        p = pillars.get(name, {})
        s = p.get("score")
        rows.append((name, s, band(s), p.get("label", "unknown"), p.get("evidence", "")))
        if isinstance(s, (int, float)):
            scored.append((s, i, name))
    print(f"{'pillar':<12} {'score':>5}  {'band':<9} {'label':<9} evidence")
    for name, s, b, label, ev in rows:
        print(f"{name:<12} {('-' if s is None else s):>5}  {b:<9} {label:<9} {ev}")
    if not scored:
        print("\nNo scores yet.")
        return
    weakest = min(scored)
    total = sum(s for s, _, _ in scored)
    missing = [n for n in CHAIN if not isinstance(pillars.get(n, {}).get("score"), (int, float))]
    print(f"\nOverall: {total}/{len(scored) * 10}")
    print(f"Weakest pillar: {weakest[2]} ({weakest[0]}/10)")
    if missing:
        print("Not scored yet: " + ", ".join(missing))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
