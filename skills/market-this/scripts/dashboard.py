#!/usr/bin/env python3
"""Build a one-file HTML dashboard from a Market This dossier.

Usage:
    python3 dashboard.py dossier.json dashboard.html

Shows the goal, the weakest pillar, the ten pillar scores in chain order,
the chosen motion and channel tests, and the weekly metrics against the
baseline. No external files or scripts; opens in any browser.
Standard library only.
"""
import html
import json
import sys

CHAIN = ["market", "customer", "problem", "positioning", "offer",
         "pricing", "motion", "channels", "message", "proof"]


def esc(value):
    return html.escape("" if value is None else str(value))


def num(value):
    if value is None:
        return "?"
    return f"{value:g}" if float(value).is_integer() else f"{value:.1f}"


def pillars_svg(pillars, weakest):
    by_name = {p.get("name"): p for p in pillars}
    width, left, right, row_h = 760, 130, 150, 38
    plot_w = width - left - right
    height = 40 + row_h * len(CHAIN)
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Pillar scores out of 10">']
    parts.append(f'<text x="{left}" y="20" class="axis">score out of 10</text>')
    for i, name in enumerate(CHAIN):
        p = by_name.get(name, {})
        s = p.get("score")
        y = 40 + i * row_h
        is_w = name == weakest
        parts.append(f'<text x="{left - 12}" y="{y + 18}" text-anchor="end" class="{"name bn-text" if is_w else "name"}">{esc(name)}</text>')
        parts.append(f'<rect x="{left}" y="{y + 6}" width="{plot_w}" height="18" rx="4" class="track"/>')
        if isinstance(s, (int, float)):
            cls = "bar bn" if is_w else ("bar good-bar" if s >= 7 else "bar")
            parts.append(f'<rect x="{left}" y="{y + 6}" width="{max(2, plot_w * s / 10):.1f}" height="18" rx="4" class="{cls}"/>')
            parts.append(f'<text x="{left + plot_w + 10}" y="{y + 18}" class="val">{num(s)} · {esc(p.get("label", "unknown"))}</text>')
        else:
            parts.append(f'<text x="{left + plot_w + 10}" y="{y + 18}" class="val">not scored</text>')
    parts.append("</svg>")
    return "".join(parts)


def channel_table(channels):
    rows = []
    for c in channels or []:
        result = c.get("result")
        cls = "good" if result in ("keep", "works", True) else ""
        rows.append(f"<tr><td>{esc(c.get('name'))}</td><td>{esc(c.get('test'))}</td><td>{esc(c.get('threshold'))}</td><td class='{cls}'>{esc(result if result is not None else 'running')}</td></tr>")
    if not rows:
        return "<p class='muted'>No channels chosen yet.</p>"
    return "<table><tr><th>Channel</th><th>Test</th><th>Success threshold</th><th>Result</th></tr>" + "".join(rows) + "</table>"


def metric_table(metrics):
    keys = ["reach", "activation", "sales", "revenue", "referral"]
    if not metrics:
        return "<p class='muted'>No baseline recorded yet.</p>"
    head = "<tr><th>Week</th>" + "".join(f"<th>{k}</th>" for k in keys) + "</tr>"
    base = metrics[0]
    body = []
    for m in metrics:
        cells = []
        for k in keys:
            v, b = m.get(k), base.get(k)
            better = m is not base and isinstance(v, (int, float)) and isinstance(b, (int, float)) and v > b
            cells.append(f"<td class='{'good' if better else ''}'>{esc(num(v)) if v is not None else '?'}</td>")
        label = "baseline" if m is base else ""
        body.append(f"<tr><td>{esc(m.get('week'))} <span class='lbl'>{label}</span></td>{''.join(cells)}</tr>")
    return f"<table>{head}{''.join(body)}</table>"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        d = json.load(fh)

    biz = d.get("business", {}) or {}
    goal = d.get("goal", {}) or {}
    pillars = d.get("pillars", []) or []
    weakest = (d.get("weakest_pillar") or {}).get("name")
    scored = [p["score"] for p in pillars if isinstance(p.get("score"), (int, float))]
    total = sum(scored)
    pos = (d.get("positioning") or {}).get("one_line") or "positioning not written yet"
    plan = d.get("plan") or {}

    page = f"""<!doctype html>
<html lang="{esc(d.get('language', 'en'))}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Market This · {esc(biz.get('name', 'Dashboard'))}</title>
<style>
:root {{ --bg:#F5F5DC; --fg:#212121; --muted:#5D4037; --line:rgba(33,33,33,.12); --bar:rgba(33,33,33,.22); --track:rgba(33,33,33,.06); --accent:#F57C00; --good:#388E3C; --card:#FBFBEE; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#212121; --fg:#F5F5DC; --muted:rgba(245,245,220,.62); --line:rgba(245,245,220,.12); --bar:rgba(245,245,220,.28); --track:rgba(245,245,220,.06); --accent:#F57C00; --good:#C8E6C9; --card:#292929; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.55 Inter, system-ui, -apple-system, Segoe UI, sans-serif; font-variant-numeric:tabular-nums; }}
main {{ max-width:880px; margin:0 auto; padding:40px 24px 72px; }}
.eyebrow {{ font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:var(--muted); margin-bottom:14px; }}
.eyebrow::before {{ content:""; display:inline-block; width:22px; height:2px; background:var(--accent); vertical-align:middle; margin-right:10px; }}
h1 {{ font-size:30px; font-weight:700; letter-spacing:-0.04em; line-height:1.15; margin:0 0 6px; }}
h2 {{ font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.14em; color:var(--muted); margin:36px 0 12px; }}
.lead {{ font-family:Spectral, Georgia, serif; font-size:20px; line-height:1.45; margin:18px 0 0; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:18px 20px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; }}
.k {{ color:var(--muted); font-size:12.5px; }}
.v {{ font-size:22px; font-weight:700; letter-spacing:-0.03em; }}
.accent {{ color:var(--accent); }} .good {{ color:var(--good); font-weight:600; }}
svg {{ width:100%; height:auto; font-family:Inter, system-ui, sans-serif; }}
svg .name {{ fill:var(--fg); font-size:13px; }} svg .bn-text {{ fill:var(--accent); font-weight:700; }}
svg .track {{ fill:var(--track); }} svg .bar {{ fill:var(--bar); }} svg .bar.bn {{ fill:var(--accent); }} svg .good-bar {{ fill:var(--good); opacity:.75; }}
svg .val, svg .axis {{ fill:var(--muted); font-size:12px; }}
table {{ border-collapse:collapse; width:100%; }} th, td {{ text-align:left; padding:9px 10px; border-bottom:1px solid var(--line); }}
th {{ color:var(--muted); font-weight:500; font-size:12.5px; }}
.lbl {{ color:var(--muted); font-size:12px; }} .muted {{ color:var(--muted); }}
.pos {{ font-family:Spectral, Georgia, serif; font-size:18px; }}
footer {{ margin-top:44px; color:var(--muted); font-size:12px; border-top:1px solid var(--line); padding-top:14px; }}
</style>
</head>
<body><main>
<div class="eyebrow">Market This · by Jockkie Studio</div>
<h1>{esc(biz.get('name', 'Your business'))}</h1>
<div class="muted">Updated {esc(d.get('updated', ''))} · stage: {esc(d.get('stage', '?'))}</div>
<p class="lead">Weakest pillar: <strong class="accent">{esc(weakest or 'not yet confirmed')}</strong>. Fix this first; more channels will not compensate for it.</p>

<h2>At a glance</h2>
<div class="grid">
  <div class="card"><div class="k">Goal</div><div class="v">{esc(goal.get('description', '?'))}</div><div class="k">by {esc(goal.get('date', '?'))} · baseline {esc(goal.get('baseline', '?'))}</div></div>
  <div class="card"><div class="k">GTM score</div><div class="v">{total} / {len(scored) * 10 if scored else 100}</div><div class="k">{len(scored)} of 10 pillars scored</div></div>
  <div class="card"><div class="k">Motion</div><div class="v">{esc(d.get('motion', '?'))}</div><div class="k">north star: {esc(plan.get('north_star', '?'))}</div></div>
  <div class="card"><div class="k">Review</div><div class="v">{esc(plan.get('review') or '?')}</div><div class="k">re-score, next weakest pillar</div></div>
</div>

<h2>Ten pillars</h2>
<div class="card">{pillars_svg(pillars, weakest)}</div>

<h2>Positioning</h2>
<div class="card pos">{esc(pos)}</div>

<h2>Channel tests</h2>
<div class="card">{channel_table(d.get('channels'))}</div>

<h2>Weekly numbers</h2>
<div class="card">{metric_table(d.get('metrics'))}</div>

<footer>Market This by Jockkie Studio · jockkie.com · Labels: seen = stated or shown, inferred = estimated, unknown = not measured yet. This dashboard is generated from your dossier and stays with you.</footer>
</main></body></html>
"""
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"Dashboard written to {sys.argv[2]}")


if __name__ == "__main__":
    main()
