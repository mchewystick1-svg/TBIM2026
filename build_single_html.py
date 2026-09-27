#!/usr/bin/env python3
"""Bundle index.html + data.js + routes.js + every used image in assets/ into ONE file:
TBIM_Interactive_Map.html (works offline, can be emailed / uploaded anywhere).

Usage:  python3 excel_to_data.py      (only if Excel changed)
        python3 build_single_html.py
Optional: if Pillow is installed (pip3 install pillow), large PNG/JPG images are
re-encoded as WebP to keep the file small. Without Pillow they are embedded as-is.
"""
import base64, io, mimetypes, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "TBIM_Interactive_Map.html"
BIG = 100_000  # bytes: images larger than this are re-encoded (if Pillow is available)

try:
    from PIL import Image
except ImportError:
    Image = None


def data_uri(rel):
    f = HERE / rel
    raw = f.read_bytes()
    mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
    if f.suffix.lower() == ".webp":
        mime = "image/webp"
    if Image and len(raw) > BIG and f.suffix.lower() in (".png", ".jpg", ".jpeg"):
        im = Image.open(io.BytesIO(raw))
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=88, method=6)
        if buf.tell() < len(raw):
            raw, mime = buf.getvalue(), "image/webp"
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def main():
    html = (HERE / "index.html").read_text(encoding="utf-8")
    for js in ("data.js", "routes.js"):
        code = (HERE / js).read_text(encoding="utf-8").replace("</script", "<\\/script")
        tag = f'<script src="{js}"></script>'
        assert tag in html, f"{tag} not found in index.html"
        html = html.replace(tag, f"<script>\n{code}\n</script>")

    used = sorted(set(re.findall(r"assets/[A-Za-z0-9_./-]+\.(?:png|jpe?g|webp|svg|gif)", html)))
    missing = [p for p in used if not (HERE / p).exists()]
    if missing:
        raise SystemExit("Missing files: " + ", ".join(missing))
    uris = {p: data_uri(p) for p in used}
    html = re.sub(r"assets/[A-Za-z0-9_./-]+\.(?:png|jpe?g|webp|svg|gif)", lambda m: uris[m.group(0)], html)

    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.name}: {len(used)} images embedded, {OUT.stat().st_size / 1e6:.1f} MB"
          + ("" if Image else " (install Pillow to make it smaller)"))


if __name__ == "__main__":
    main()
