#!/usr/bin/env python3
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

OUTPUT = Path("info-card.svg")


NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
PREV = "2026-07-22"
STACK = "python • svg • github actions"
HIGHLIGHTS = "profile art + automation"


def render_row(label: str, value: str, delay: float, static: bool) -> str:
    begin = "0s" if static else f"{delay}s"
    opacity = "1" if static else "0"
    return f'''<g opacity="{opacity}">\n    <animate attributeName="opacity" values="0;1" dur="0.45s" begin="{begin}" fill="freeze"/>\n    <animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.45s" begin="{begin}" fill="freeze"/>\n    <text x="28" y="{40 + 32 * delay:.0f}" font-family="monospace" font-size="14" fill="#7bdc8a">{label}</text>\n    <text x="130" y="{40 + 32 * delay:.0f}" font-family="monospace" font-size="14" fill="#f3f6f8">{value}</text>\n  </g>'''


def main() -> int:
    static = os.getenv("STATIC") == "1"
    rows = [
        ("Now", NOW, 0.18),
        ("Prev", PREV, 0.32),
        ("Stack", STACK, 0.46),
        ("Highlights", HIGHLIGHTS, 0.60),
    ]

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 250">',
        '<rect width="500" height="250" fill="#0d1117" rx="14"/>',
        '<rect x="1" y="1" width="498" height="30" fill="#161b22" rx="14"/>',
        '<text x="18" y="21" font-family="monospace" font-size="13" fill="#7bdc8a">avi@github ~ $ neofetch</text>',
    ]

    for label, value, delay in rows:
        parts.append(render_row(label, value, delay, static))

    parts.append('</svg>')
    OUTPUT.write_text('\n'.join(parts), encoding="utf-8")
    print(f"Info card SVG written to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
