#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
OUTPUT = Path("contrib-heatmap.svg")
DATA = Path("data/contributions.json")


def load_payload() -> dict:
    with DATA.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_svg(payload: dict) -> str:
    days = payload["days"]
    total = sum(item["count"] for item in days)
    cells = []

    for index, item in enumerate(days[-371:]):
        week = index // 7
        day = index % 7
        level = min(5, item["level"])
        x = 28 + week * 15
        y = 34 + day * 15
        start = 0.04 * (index % 14)
        color = PALETTE[level]
        cells.append(
            f'''<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{color}" opacity="0">\n  <animate attributeName="opacity" values="0;0;1" dur="0.35s" begin="{start:.2f}s" fill="freeze"/>\n  <animateTransform attributeName="transform" type="translate" values="0 -8;0 0" dur="0.35s" begin="{start:.2f}s" fill="freeze"/>\n</rect>'''
        )

    legend = []
    for idx, color in enumerate(PALETTE):
        legend.append(f'<rect x="{32 + idx * 18}" y="390" width="12" height="12" rx="2" fill="{color}"/>')

    footer = f"{total:,} contributions in the last year"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 430">\n  <defs>\n    <style>\n      .title {{ font: 700 16px monospace; fill: #c9d1d9; }}\n      .meta {{ font: 12px monospace; fill: #8b949e; }}\n      .footer {{ font: 13px monospace; fill: #7bdc8a; }}\n    </style>\n  </defs>\n  <rect width="860" height="430" fill="#0d1117" rx="16"/>\n  <text x="28" y="28" class="title">avi@github ~ $ ./contributions.sh</text>\n  <text x="28" y="48" class="meta">{payload['username']} · refreshed {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</text>\n  {'\n'.join(cells)}\n  <text x="28" y="382" class="meta">Less</text>\n  <text x="316" y="382" class="meta">More</text>\n  {'\n'.join(legend)}\n  <text x="28" y="412" class="footer">{footer}</text>\n</svg>'''


def main() -> int:
    payload = load_payload()
    svg = render_svg(payload)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"Heatmap SVG written to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
