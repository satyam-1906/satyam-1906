#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"
SOURCE = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")
WIDTH = 100
HEIGHT = 53


def convert_to_ascii(image: Image.Image) -> list[str]:
    image = image.convert("L")
    image = image.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
    arr = np.asarray(image)
    rows: list[str] = []
    for row in arr:
        line = ''.join(RAMP[min(len(RAMP) - 1, int((255 - value) / 256 * len(RAMP)))] for value in row)
        rows.append(line)
    return rows


def build_svg(rows: list[str]) -> str:
    cell_w = 7.3
    cell_h = 10.6
    svg_rows = []
    for index, row in enumerate(rows, start=1):
        y = 16 + (index - 1) * cell_h
        clip_id = f"clip-{index}"
        svg_rows.append(
            f'''<g>\n    <defs>\n      <clipPath id="{clip_id}">\n        <rect x="0" y="{y - cell_h + 1}" width="0" height="{cell_h + 1}">\n          <animate attributeName="width" values="0;{WIDTH * cell_w};{WIDTH * cell_w}" dur="0.38s" begin="{(index - 1) * 0.045:.3f}s" fill="freeze"/>\n        </rect>\n      </clipPath>\n    </defs>\n    <g clip-path="url(#{clip_id})">\n      <text x="0" y="{y}" font-family="monospace" font-size="10" fill="#d8e6da" letter-spacing="0.2">{row}</text>\n    </g>\n  </g>'''
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH * cell_w + 30} {HEIGHT * cell_h + 32}">\n  <rect width="100%" height="100%" fill="#07110c"/>\n  {chr(10).join(svg_rows)}\n</svg>'''
    return svg


def main() -> int:
    if not SOURCE.exists():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH * 7.3 + 30} {HEIGHT * 10.6 + 32}">
  <rect width="100%" height="100%" fill="#07110c"/>
  <text x="16" y="48" font-family="monospace" font-size="12" fill="#d8e6da">Missing source-prepped.png — add your portrait and rerun.</text>
</svg>'''
        OUTPUT.write_text(svg, encoding="utf-8")
        print(f"ASCII portrait SVG written to {OUTPUT}")
        return 0

    image = Image.open(SOURCE)
    rows = convert_to_ascii(image)
    svg = build_svg(rows)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"ASCII portrait SVG written to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
