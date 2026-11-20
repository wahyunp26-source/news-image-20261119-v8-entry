#!/usr/bin/env python3
# news-image-20261119 v8 — "The World in One Day" front page, 19 November 2026.
# New method: the artwork and the type are REAL raster assets, made at build
# time (generated illustrations + text rendered with a real font). This program
# only decodes those PNG assets and composites them into the page.
# Python stdlib only (json, os, struct, sys, zlib). No network. Deterministic.
import json
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 241, 221)
INK = (17, 17, 17)


def decode_png(data):
    # Minimal PNG decoder: 8-bit, colour types 2 (RGB) and 6 (RGBA),
    # non-interlaced, all five row filters. Returns (w, h, rgba bytearray).
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    pos = 8
    idat = bytearray()
    w = h = None
    bitdepth = ctype = None
    interlace = None
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        tag = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        if tag == b"IHDR":
            w, h, bitdepth, ctype, _c, _f, interlace = struct.unpack(
                ">IIBBBBB", chunk)
        elif tag == b"IDAT":
            idat += chunk
        elif tag == b"IEND":
            break
        pos += 12 + ln
    if bitdepth != 8 or interlace != 0 or ctype not in (2, 6):
        raise ValueError("unsupported PNG: depth=%s type=%s interlace=%s"
                         % (bitdepth, ctype, interlace))
    ch = 3 if ctype == 2 else 4
    raw = zlib.decompress(bytes(idat))
    stride = w * ch
    out = bytearray(w * h * 4)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        if f == 1:
            for i in range(ch, stride):
                line[i] = (line[i] + line[i - ch]) & 0xFF
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif f == 3:
            for i in range(stride):
                a = line[i - ch] if i >= ch else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif f == 4:
            for i in range(stride):
                a = line[i - ch] if i >= ch else 0
                b = prev[i]
                c = prev[i - ch] if i >= ch else 0
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        elif f != 0:
            raise ValueError("bad PNG filter %d" % f)
        for x in range(w):
            o = (y * w + x) * 4
            s = x * ch
            if ch == 4:
                out[o:o + 4] = line[s:s + 4]
            else:
                out[o:o + 3] = line[s:s + 3]
                out[o + 3] = 255
        prev = line
    return w, h, out


class Page:
    def __init__(self):
        self.buf = bytearray(W * H * 3)
        for i in range(W * H):
            o = i * 3
            self.buf[o], self.buf[o + 1], self.buf[o + 2] = PAPER

    def rect(self, x0, y0, x1, y1, c):
        x0 = max(0, x0); y0 = max(0, y0)
        x1 = min(W, x1); y1 = min(H, y1)
        for y in range(y0, y1):
            base = y * W * 3
            for x in range(x0, x1):
                o = base + x * 3
                self.buf[o], self.buf[o + 1], self.buf[o + 2] = c

    def paste(self, w, h, rgba, dx, dy):
        for y in range(h):
            py = dy + y
            if py < 0 or py >= H:
                continue
            for x in range(w):
                px = dx + x
                if px < 0 or px >= W:
                    continue
                s = (y * w + x) * 4
                a = rgba[s + 3]
                if a == 0:
                    continue
                o = (py * W + px) * 3
                if a == 255:
                    self.buf[o] = rgba[s]
                    self.buf[o + 1] = rgba[s + 1]
                    self.buf[o + 2] = rgba[s + 2]
                else:
                    self.buf[o] = (rgba[s] * a + self.buf[o] * (255 - a)) // 255
                    self.buf[o + 1] = (rgba[s + 1] * a + self.buf[o + 1] * (255 - a)) // 255
                    self.buf[o + 2] = (rgba[s + 2] * a + self.buf[o + 2] * (255 - a)) // 255


def write_png(path, rgb):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(rgb[y * W * 3:(y + 1) * W * 3])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    with open(os.path.join(base, "manifest.json")) as f:
        manifest = json.load(f)
    pg = Page()
    # frame
    pg.rect(14, 14, 1010, 16, INK)
    pg.rect(14, 1008, 1010, 1010, INK)
    pg.rect(14, 14, 16, 1010, INK)
    pg.rect(1008, 14, 1010, 1010, INK)
    # section dividers
    pg.rect(20, 498, 1004, 500, INK)
    pg.rect(20, 786, 1004, 787, INK)
    for entry in manifest:
        with open(os.path.join(base, entry["file"]), "rb") as f:
            data = f.read()
        w, h, rgba = decode_png(data)
        pg.paste(w, h, rgba, entry["x"], entry["y"])
    write_png("entry.png", pg.buf)
    print("page written")


if __name__ == "__main__":
    main()
