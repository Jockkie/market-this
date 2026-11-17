#!/usr/bin/env python3
"""Van Westendorp price sensitivity analysis.

Usage: python3 price_test.py answers.csv [chart.html]

CSV columns: too_cheap, cheap, expensive, too_expensive (one row per
respondent, numbers only). Prints the acceptable price range and the key
price points; optionally writes a one-file HTML chart. Standard library only.

Points:
- PMC (point of marginal cheapness): "too cheap" crosses "not cheap" (1 - cheap)
- PME (point of marginal expensiveness): "too expensive" crosses "not expensive" (1 - expensive)
- OPP (optimal price point): "too cheap" crosses "too expensive"
- IPP (indifference price point): "cheap" crosses "expensive"
"""
import csv
import html
import sys

COLS = ["too_cheap", "cheap", "expensive", "too_expensive"]


def load(path):
    rows, dropped = [], 0
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                v = [float(r[c]) for c in COLS]
            except (KeyError, ValueError):
                dropped += 1
                continue
            if v[0] <= v[1] <= v[2] <= v[3]:
                rows.append(v)
            else:
                dropped += 1
    if dropped:
        print(f"Dropped {dropped} answers that were empty, not numeric, or not in rising order (too cheap <= cheap <= expensive <= too expensive).")
    return rows


def curves(rows):
    prices = sorted({p for r in rows for p in r})
    n = len(rows)
    out = []
    for p in prices:
        too_cheap = sum(r[0] >= p for r in rows) / n       # falls as price rises
        cheap = sum(r[1] >= p for r in rows) / n
        expensive = sum(r[2] <= p for r in rows) / n       # rises as price rises
        too_exp = sum(r[3] <= p for r in rows) / n
        out.append((p, too_cheap, cheap, expensive, too_exp))
    return out


def cross(data, f, g):
    prev = None
    for row in data:
        d = f(row) - g(row)
        if prev is not None and (prev[1] > 0) != (d > 0):
            p0, d0 = prev[0], prev[1]
            p1 = row[0]
            return p0 + (p1 - p0) * (d0 / (d0 - d)) if d0 != d else p1
        prev = (row[0], d)
    return None


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    rows = load(argv[1])
    if len(rows) < 10:
        print(f"Only {len(rows)} valid answers. Aim for 30 or more; read the result as a rough direction.")
    if not rows:
        return
    data = curves(rows)
    pmc = cross(data, lambda r: r[1], lambda r: 1 - r[2])
    pme = cross(data, lambda r: r[4], lambda r: 1 - r[3])
    opp = cross(data, lambda r: r[1], lambda r: r[4])
    ipp = cross(data, lambda r: r[2], lambda r: r[3])
    fmt = lambda v: "n/a" if v is None else f"{v:,.2f}"
    print(f"Respondents: {len(rows)}")
    print(f"Acceptable range: {fmt(pmc)} to {fmt(pme)}")
    print(f"Optimal price point (OPP): {fmt(opp)} · Indifference price point (IPP): {fmt(ipp)}")
    print("Treat this as a direction to test with real offers, not a final price.")
    if len(argv) > 2:
        lo, hi = data[0][0], data[-1][0]
        W, H, L, B = 760, 360, 50, 40
        x = lambda p: L + (p - lo) / ((hi - lo) or 1) * (W - L - 20)
        y = lambda v: H - B - v * (H - B - 20)
        names = [("Too cheap", 1, "#5D4037"), ("Not cheap", 2, "#9E9E9E"),
                 ("Not expensive", 3, "#388E3C"), ("Too expensive", 4, "#F57C00")]
        lines = []
        for name, i, col in names:
            pts = " ".join(f"{x(r[0]):.1f},{y((1 - r[i]) if i in (2, 3) else r[i]):.1f}" for r in data)
            lines.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2"/>')
        band = ""
        if pmc and pme:
            band = f'<rect x="{x(pmc):.1f}" y="20" width="{x(pme) - x(pmc):.1f}" height="{H - B - 20}" fill="#388E3C" opacity=".08"/>'
        mark = f'<line x1="{x(opp):.1f}" x2="{x(opp):.1f}" y1="20" y2="{H - B}" stroke="#212121" stroke-dasharray="3 3"/>' if opp else ""
        legend = "".join(f'<span style="margin-right:14px"><i style="display:inline-block;width:12px;height:3px;background:{c};vertical-align:middle"></i> {n}</span>' for n, _, c in names)
        page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Price test</title>
<style>body{{font:14px/1.5 Inter,system-ui,sans-serif;background:#F5F5DC;color:#212121;max-width:820px;margin:40px auto;padding:0 20px}}
.card{{background:#FBFBEE;border:1px solid rgba(33,33,33,.12);border-radius:10px;padding:18px}} svg{{width:100%;height:auto}} text{{font-size:11px;fill:#5D4037}}</style></head><body>
<h1 style="letter-spacing:-.03em">Van Westendorp price test</h1>
<p>Acceptable range <strong>{fmt(pmc)} to {fmt(pme)}</strong> · Optimal price point <strong>{fmt(opp)}</strong> · {len(rows)} respondents</p>
<div class="card"><svg viewBox="0 0 {W} {H}">{band}{''.join(lines)}{mark}
<text x="{L}" y="{H - 12}">{fmt(lo)}</text><text x="{W - 60}" y="{H - 12}">{fmt(hi)}</text></svg><div>{legend}</div></div>
<p style="color:#5D4037;font-size:12px">A direction to test with real offers. Market This by Jockkie Studio.</p></body></html>"""
        with open(argv[2], "w", encoding="utf-8") as f:
            f.write(page)
        print(f"Chart written to {argv[2]}")


if __name__ == "__main__":
    main(sys.argv)
