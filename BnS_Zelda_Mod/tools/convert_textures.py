#!/usr/bin/env python3
"""
N64 (OOT) texture converter -> PNG for Unity import.
Handles raw binary texture rasters pulled from SoH .o2r dumps.

Since the decompiled textures lack width/height/format metadata in filename,
we infer from file size. This is a best-effort decoder used to preview/produce
Unity-ready PNGs. For exact geometry use ZAPD (SoH asset extractor).
"""
import os, sys, struct
from pathlib import Path

def try_write_png(path, width, height, pixels_rgba):
    """Write a minimal PNG (no zlib dependency beyond stdlib)"""
    import zlib
    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        c += struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)
        return c
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    raw = b""
    for y in range(height):
        raw += b"\x00"
        row = bytearray()
        for x in range(width):
            idx = (y * width + x) * 4
            row += bytes(pixels_rgba[idx:idx+4])
        raw += bytes(row)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    Path(path).write_bytes(png)

def decode_rgba16(data, w, h):
    px = []
    for i in range(0, len(data), 2):
        v = struct.unpack(">H", data[i:i+2])[0]
        r = (v >> 11) & 0x1f; g = (v >> 6) & 0x1f; b = (v >> 1) & 0x1f; a = v & 1
        r = (r << 3) | (r >> 2); g = (g << 3) | (g >> 2); b = (b << 3) | (b >> 2)
        a = 255 if a else 0
        px += [r, g, b, a]
    return px

def decode_ia8(data, w, h):
    px = []
    for v in data:
        px += [v, v, v, v]  # IA8: intensity+alpha same byte
    return px

def decode_ia16(data, w, h):
    px = []
    for i in range(0, len(data), 2):
        v = struct.unpack(">H", data[i:i+2])[0]
        intensity = (v >> 8) & 0xff; alpha = v & 0xff
        px += [intensity, intensity, intensity, alpha]
    return px

def decode_ci4_with_palette(data, pal_data, w, h):
    px = []
    for byte in data:
        idx_hi = byte >> 4; idx_lo = byte & 0xf
        for idx in (idx_hi, idx_lo):
            if idx * 2 + 1 < len(pal_data):
                v = struct.unpack(">H", pal_data[idx*2:idx*2+2])[0]
                r = (v >> 11) & 0x1f; g = (v >> 6) & 0x1f; b = (v >> 1) & 0x1f; a = v & 1
                px += [(r<<3)|(r>>2), (g<<3)|(g>>2), (b<<3)|(b>>2), 255 if a else 0]
            else:
                px += [0,0,0,0]
    return px

def guess_and_decode(path, outdir):
    data = Path(path).read_bytes()
    size = len(data)
    name = Path(path).name
    out_png = Path(outdir) / (name + ".png")
    if out_png.exists():
        return
    # Try common square/rectangular sizes by probing divisibility
    candidates = []
    for dim in [(64,64),(128,32),(32,64),(128,128),(256,32),(160,720),(128,128),
                (32,32),(128,64),(256,256),(64,32),(48,48),(128,16),(96,32)]:
        w,h = dim
        bpp2 = w*h*2
        bpp1 = w*h
        if size == bpp2:
            candidates.append((w,h,2))
        if size == bpp1:
            candidates.append((w,h,1))
    if not candidates:
        print(f"  [skip] {name}: size {size} not recognized")
        return
    w,h,bpp = candidates[0]
    try:
        if bpp == 2:
            px = decode_rgba16(data, w, h)
        else:
            px = decode_ia8(data, w, h)
        try_write_png(out_png, w, h, px)
        print(f"  [ok] {name} -> {w}x{h} -> {out_png.name}")
    except Exception as e:
        print(f"  [err] {name}: {e}")

def main():
    src = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else "out_png"
    os.makedirs(outdir, exist_ok=True)
    path = Path(src)
    files = [path] if path.is_file() else sorted(path.rglob("*"))
    n = 0
    for f in files:
        if f.is_file():
            guess_and_decode(f, outdir)
            n += 1
    print(f"Processed {n} files into {outdir}")

if __name__ == "__main__":
    main()