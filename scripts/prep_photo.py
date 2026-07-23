#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps

try:
    from rembg import remove
except Exception:  # pragma: no cover - optional dependency for local portrait prep
    remove = None


OUTPUT_NAME = "source-prepped.png"


def load_image(path: Path) -> Image.Image:
    with Image.open(path) as src:
        rgb = src.convert("RGB")
    return rgb


def remove_background(image: Image.Image) -> Image.Image:
    if remove is None:
        return image
    try:
        result = remove(image)
        if result.mode == "RGBA":
            return result
        return result.convert("RGBA")
    except Exception:
        return image


def clahe_enhance(image: Image.Image) -> Image.Image:
    arr = np.asarray(image)
    if arr.ndim == 3:
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    else:
        gray = arr

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return Image.fromarray(enhanced).convert("L")


def white_compose(image: Image.Image) -> Image.Image:
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    white = Image.new("RGBA", image.size, "white")
    white.paste(image, (0, 0), image.getchannel("A"))
    return white.convert("RGB")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py source-photo.jpg")
        return 1

    source = Path(sys.argv[1])
    if not source.exists():
        print(f"Source image not found: {source}")
        return 1

    image = load_image(source)
    image = remove_background(image)
    image = clahe_enhance(image)
    image = white_compose(image)

    output = source.with_name(OUTPUT_NAME)
    image.save(output)
    print(f"Prepared image written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
