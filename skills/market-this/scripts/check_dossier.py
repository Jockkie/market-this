#!/usr/bin/env python3
"""Check a dossier or profile before a gate or a delivery, and print the
"what you told me / what I assumed" block.

Usage:
    python3 check_dossier.py dossier.json [--gate 1|2|deliver] [--assumptions]

Works for the dossiers and profiles of all Jockkie Studio skills (it reads the
`schema` field). Checks:
  - every value labelled `seen` carries a `quote`: the user's own words
  - every label is one of seen, inferred, unknown
  - `unknown` values hold no number
  - numbers (value, low, high, score) are labelled
  - gate-specific requirements (for example: the user confirmed the bottleneck)
  - an optional top-level `assumptions` list (strings or {text, basis}) is shown
    under "I estimated"; plain "unknown" values are shown under "Still unknown"

Exit code 0 when the check passes, 1 when something must be fixed first.
With --assumptions it prints a Markdown block for the user, listing what the
user said, what was estimated and what is still unknown.
Standard library only.
"""
import argparse
import json
import sys

LABELS = {"seen", "inferred", "unknown"}
NUMERIC = ("value", "low", "high", "score")
SKIP = {"tests", "simulations", "quotes_external_tools", "external_tools", "follow_ups", "readings"}  # the skill's own records, not facts about the user


def walk(node, path, out):
    if isinstance(node, dict):
        if "label" in node or any(k in node for k in NUMERIC):
            out.append((path, node))
        for k, v in node.items():
            if k.startswith("_") or k in SKIP:
                continue
            walk(v, f"{path}.{k}" if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            name = v.get("name") or v.get("metric") or v.get("step") or v.get("task") or str(i) if isinstance(v, dict) else str(i)
            walk(v, f"{path}[{name}]", out)


def plain_unknowns(node, path):
    """Values written as the plain string 'unknown' (or null fields named in `unknowns`)."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("_") or k in SKIP:
                continue
            sub = f"{path}.{k}" if path else k
            if k == "label":
                continue
            if isinstance(v, str) and v.strip().lower() in ("unknown", "onbekend"):
                yield sub, v
            else:
                yield from plain_unknowns(v, sub)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from plain_unknowns(v, f"{path}[{i}]")


def has_number(d):
    return any(isinstance(d.get(k), (int, float)) and not isinstance(d.get(k), bool) for k in NUMERIC)


def pretty(path):
    return path.replace("_per_", " per ").replace("_", " ")


def describe(path, d):
    if d.get("value") is not None:
        val = d["value"]
    elif d.get("low") is not None:
        val = f"{d.get('low')} to {d.get('high')}"
    elif d.get("score") is not None:
        val = f"{d['score']}/10"
    else:
        val = d.get("description") or d.get("evidence") or d.get("target") or ""
    return f"{pretty(path)}: {val}".rstrip(": ")


def generic_checks(data):
    problems, items = [], []
    walk(data, "", items)
    for path, val in plain_unknowns(data, ""):
        items.append((path, {"label": "unknown"}))
    for a in data.get("assumptions", []) or []:
        text = a if isinstance(a, str) else (a.get("text") or a.get("assumption") or "")
        basis = "" if isinstance(a, str) else a.get("basis", "")
        items.append(("assumption", {"label": "inferred", "description": text, "basis": basis}))
    birth = data.get("birth") or {}
    cert = str(birth.get("time_certainty", "")).lower()
    if birth.get("time") and cert and not any(w in cert for w in ("certificate", "akte", "exact", "hospital", "ziekenhuis")):
        items.append(("assumption", {"label": "inferred", "description": f"Birth time {birth['time']} is approximate ({birth.get('time_certainty')})",
                                     "basis": "ascendant, houses and possibly the Moon depend on it"}))
    if str(data.get("schema", "")).startswith(("find-my-ikigai", "align-my-astro")):
        problems = []  # these profiles hold the user's own answers and calculations; only listed assumptions count
        return problems, [(p_, d_) for p_, d_ in items if p_ == "assumption" or d_.get("label") == "unknown" and p_ != ""]
    for path, d in items:
        label = d.get("label")
        if label is None:
            if has_number(d):
                problems.append(f"{path}: number without a label (seen, inferred or unknown)")
            continue
        if label not in LABELS:
            problems.append(f"{path}: label '{label}' is not seen, inferred or unknown")
        if label == "seen" and not str(d.get("quote", "")).strip():
            problems.append(f"{path}: labelled seen but has no quote of the user's own words; add the quote or relabel as inferred")
        if label == "unknown" and has_number(d):
            problems.append(f"{path}: labelled unknown but holds a number; remove the number or relabel")
    return problems, items


def gate_checks(data, gate):
    schema = str(data.get("schema", ""))
    p = []
    def need(cond, msg):
        if not cond:
            p.append(msg)
    if schema.startswith("consult-anything"):
        if gate in ("1", "2", "deliver"):
            need(data.get("goal", {}).get("metric") or data.get("goal", {}).get("target"), "Gate 1: the goal is missing (write it in the user's own words)")
            need(data.get("steps"), "Gate 1: the process steps are missing")
        if gate in ("2", "deliver"):
            bn = data.get("bottleneck") or {}
            need(bn.get("step"), "Gate 2: no bottleneck named")
            need(bn.get("confirmed_by_user") is True, "Gate 2: the user has not confirmed the bottleneck")
        if gate == "deliver":
            need(data.get("solution", {}).get("chosen"), "Delivery: no chosen solution")
            need(data.get("baseline", {}).get("metrics"), "Delivery: no baseline to measure against")
            need((data.get("meta") or {}).get("follow_up_date"), "Delivery: no follow-up date")
    elif schema.startswith("market-this"):
        if gate in ("1", "2", "deliver"):
            g1 = data.get("gate1") or {}
            need(g1.get("confirmed_by_user") is True, "Gate 1: the user has not confirmed the interview summary")
            need(data.get("goal", {}).get("description"), "Gate 1: the goal is missing")
        if gate in ("2", "deliver"):
            wp = data.get("weakest_pillar") or {}
            need(wp.get("name"), "Gate 2: no weakest pillar named")
            need(wp.get("confirmed_by_user") is True, "Gate 2: the user has not confirmed the weakest pillar")
        if gate == "deliver":
            need(data.get("channels"), "Delivery: no channel tests")
            need((data.get("plan") or {}).get("review"), "Delivery: no review date")
            need(data.get("metrics"), "Delivery: no baseline metrics")
    elif schema.startswith("find-my-ikigai"):
        for c in data.get("candidates", []):
            need(c.get("verdict") in ("owned", "borrowed", "mixed", "unsure", None, ""),
                 f"Candidate {c.get('name')}: verdict must be owned, borrowed, mixed or unsure")
            need(c.get("verdict_by", "user") == "user", f"Candidate {c.get('name')}: the verdict must be the user's, not yours")
        for n in data.get("needs", []):
            s = n.get("score")
            need(s is None or (isinstance(s, (int, float)) and 0 <= s <= 10), f"Need {n.get('name')}: score must be 0 to 10")
        if gate == "deliver":
            need(data.get("first_step"), "Delivery: no first step written")
            need(data.get("next_reflection"), "Delivery: no reflection date")
    elif schema.startswith("align-my-astro"):
        b = data.get("birth") or {}
        need(b.get("date"), "Profile: birth date missing")
        need(b.get("time") is None or b.get("time_certainty"), "Profile: birth time given without how certain it is")
        need(data.get("conventions"), "Profile: conventions (Tzolk'in correlation, Chinese year boundary) not recorded")
    return p


def assumptions_block(items, language):
    told, assumed, unknown = [], [], []
    my_score = "mijn score" if language.startswith("nl") else "my score"
    based_on = "op basis van" if language.startswith("nl") else "based on"
    for path, d in items:
        label = d.get("label")
        line = describe(path, d)
        if d.get("score") is not None:
            # a score is the assistant's judgment, even when the evidence is the user's
            if label == "seen" and d.get("quote"):
                told.append(f"- {pretty(path)}: \"{d.get('quote', '').strip()}\"")
            assumed.append(f"- {pretty(path)}: {my_score} {d['score']}/10")
            continue
        if label == "seen":
            told.append(f"- {line} (\"{d.get('quote', '').strip()}\")")
        elif label == "inferred":
            basis = d.get("basis") or d.get("evidence") or ""
            assumed.append(f"- {line}" + (f" ({based_on}: {basis})" if basis else ""))
        elif label == "unknown":
            unknown.append(f"- {pretty(path)}")
    nl = language.startswith("nl")
    head = ("### Wat je me vertelde en wat ik aannam", "**Jij vertelde:**", "**Ik schatte (controleer dit):**", "**Nog onbekend:**", "geen")
    if not nl:
        head = ("### What you told me and what I assumed", "**You told me:**", "**I estimated (please check):**", "**Still unknown:**", "none")
    out = [head[0], "", head[1]] + (told or [f"- {head[4]}"]) + ["", head[2]] + (assumed or [f"- {head[4]}"]) + ["", head[3]] + (unknown or [f"- {head[4]}"])
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier")
    ap.add_argument("--gate", choices=["1", "2", "deliver"])
    ap.add_argument("--assumptions", action="store_true")
    a = ap.parse_args()
    with open(a.dossier, encoding="utf-8") as f:
        data = json.load(f)
    problems, items = generic_checks(data)
    if a.gate:
        problems += gate_checks(data, a.gate)
    if a.assumptions:
        lang = (data.get("meta") or {}).get("language") or data.get("language") or "en"
        print(assumptions_block(items, lang))
        print()
    if problems:
        print(f"CHECK FAILED ({len(problems)}): fix these before continuing.")
        for p in problems:
            print(f"- {p}")
        sys.exit(1)
    counts = {l: sum(1 for _, d in items if d.get("label") == l) for l in LABELS}
    print(f"CHECK PASSED · seen {counts['seen']} · inferred {counts['inferred']} · unknown {counts['unknown']}")


if __name__ == "__main__":
    main()
