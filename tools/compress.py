"""Losslessly re-saves the PNG icons so they are as small as possible."""
from pathlib import Path
from PIL import Image
pub = Path(__file__).resolve().parent.parent / "public"
for p in [*pub.glob("*.png"), *pub.glob("icons/*.png")]:
    before = p.stat().st_size
    Image.open(p).save(p, optimize=True)
    print(f"{p.relative_to(pub)}: {before//1024} KB -> {p.stat().st_size//1024} KB")
