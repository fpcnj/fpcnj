#!/usr/bin/env python3
"""Copy and compress public FPC photos; draw favicon set. Skip tax/EIN/IDs."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

SRC = Path("/Users/kingofthehill/Documents/FPC")
IMG = SRC / "fpc_images"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "image"

# Public church photos only. No EIN, tax, exemption, vendor-ID, or name-card files.
PHOTOS = {
    "hero-front.jpg": IMG / "01_fpcfront.jpg",
    "campus-front.jpg": IMG / "frontview.jpg",
    "historic.jpg": IMG / "02_historic_church.jpg",
    "sanctuary.jpg": IMG / "chaple.jpg",
    "worship.jpg": IMG / "service.jpg",
    "congregation.jpg": IMG / "crowd.jpg",
    "kids.jpg": IMG / "kids.jpg",
    "fair.jpg": IMG / "fair.jpg",
    "facepainting.jpg": IMG / "facepainting.jpg",
    "tent.jpg": IMG / "tent.jpg",
    "prayer-sign.jpg": IMG / "sign.jpg",
    "campus-back.jpg": IMG / "backview.jpg",
    "campus-side.jpg": IMG / "sideview.jpg",
    "bulletin.jpg": IMG / "bullitin.jpg",
    "fellowship.jpg": SRC / "IMG_0707.jpg",
    "skyline.jpg": IMG / "01_skyline.jpg",
}


def compress(src: Path, dest: Path, max_side: int = 1400, quality: int = 78) -> None:
    im = Image.open(src)
    im = im.convert("RGB")
    w, h = im.size
    scale = min(1.0, max_side / float(max(w, h)))
    if scale < 1.0:
        im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)


def draw_mark(size: int) -> Image.Image:
    navy = (26, 39, 68, 255)
    gold = (184, 145, 58, 255)
    cream = (251, 247, 239, 255)
    im = Image.new("RGBA", (size, size), navy)
    d = ImageDraw.Draw(im)
    pad = size * 0.08
    d.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=size * 0.12,
        outline=gold,
        width=max(2, size // 28),
    )
    cx, cy = size / 2.0, size * 0.52
    bar = max(size // 11, 3)
    # Latin cross
    d.rectangle([cx - bar / 2, size * 0.22, cx + bar / 2, size * 0.82], fill=cream)
    d.rectangle([size * 0.26, cy - bar / 2, size * 0.74, cy + bar / 2], fill=cream)
    d.rectangle([cx - bar / 4, size * 0.24, cx + bar / 4, size * 0.80], fill=gold)
    d.rectangle([size * 0.28, cy - bar / 4, size * 0.72, cy + bar / 4], fill=gold)
    return im


def write_favicons() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="First Presbyterian Church Palisades Park">
  <rect width="64" height="64" rx="12" fill="#1a2744"/>
  <rect x="5" y="5" width="54" height="54" rx="9" fill="none" stroke="#b8913a" stroke-width="2.4"/>
  <rect x="29" y="12" width="6" height="40" fill="#fbf7ef"/>
  <rect x="16" y="30" width="32" height="6" fill="#fbf7ef"/>
  <rect x="30" y="14" width="4" height="36" fill="#b8913a"/>
  <rect x="18" y="31.5" width="28" height="3" fill="#b8913a"/>
</svg>
"""
    (OUT / "favicon.svg").write_text(svg, encoding="utf-8")
    mark32 = draw_mark(32)
    mark180 = draw_mark(180)
    mark512 = draw_mark(512)
    mark32.save(OUT / "favicon-32.png", "PNG", optimize=True)
    mark180.save(OUT / "apple-touch-icon.png", "PNG", optimize=True)
    mark512.save(OUT / "icon-512.png", "PNG", optimize=True)
    ico = draw_mark(256)
    ico.save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in PHOTOS.items():
        if not src.exists():
            raise SystemExit(f"missing source photo: {src}")
        compress(src, OUT / name)
        out = OUT / name
        print(f"{name}: {out.stat().st_size} bytes from {src.name}")
    write_favicons()
    print("favicons written")


if __name__ == "__main__":
    main()
