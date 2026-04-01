#!/usr/bin/env python3
"""Build script for the Redacto font family.

Generates OpenType fonts (.otf, .ttf, .woff2) covering all assigned
Unicode Basic Multilingual Plane code points.  Every glyph is a
full-height black rectangle whose advance width equals a standard n-width.
"""

import unicodedata
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.misc.psCharStrings import T2CharString
from fontTools.ttLib import TTFont

# ── Design constants ─────────────────────────────────────────────────
UPM = 1000
ASCENDER = 800
DESCENDER = -200
X_HEIGHT = 500
CAP_HEIGHT = 700
GLYPH_WIDTH = 500  # n-width: advance width of every glyph

FAMILY = "Redacto"
STYLE = "Regular"
PS_NAME = "Redacto-Regular"
VERSION = "Version 1.000"

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "fonts"


# ── Helpers ──────────────────────────────────────────────────────────

def collect_codepoints():
    """Return sorted list of all assigned BMP code points."""
    cps = []
    for cp in range(1, 0x10000):
        if 0xD800 <= cp <= 0xDFFF:
            continue  # surrogates
        if unicodedata.category(chr(cp)) != "Cn":
            cps.append(cp)
    return cps


def glyph_name(cp):
    return f"uni{cp:04X}"


def name_strings():
    return dict(
        familyName=FAMILY,
        styleName=STYLE,
        uniqueFontIdentifier=f"1.000;NONE;{PS_NAME}",
        fullName=f"{FAMILY} {STYLE}",
        version=VERSION,
        psName=PS_NAME,
        licenseDescription=(
            "This Font Software is licensed under the SIL Open Font "
            "License, Version 1.1."
        ),
        licenseInfoURL="https://openfontlicense.org",
    )


def os2_values():
    return dict(
        sTypoAscender=ASCENDER,
        sTypoDescender=DESCENDER,
        sTypoLineGap=0,
        usWinAscent=ASCENDER,
        usWinDescent=-DESCENDER,
        sxHeight=X_HEIGHT,
        sCapHeight=CAP_HEIGHT,
        fsType=0x0000,  # installable embedding
    )


# ── TTF builder ──────────────────────────────────────────────────────

def build_ttf(glyph_order, cmap):
    """Build a TrueType-flavored OpenType font (.ttf)."""
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap, allowFallback=True)

    # One rectangle outline, shared by every glyph
    pen = TTGlyphPen(None)
    pen.moveTo((0, DESCENDER))
    pen.lineTo((GLYPH_WIDTH, DESCENDER))
    pen.lineTo((GLYPH_WIDTH, ASCENDER))
    pen.lineTo((0, ASCENDER))
    pen.closePath()
    rect = pen.glyph()

    fb.setupGlyf({name: rect for name in glyph_order})
    fb.setupHorizontalMetrics({n: (GLYPH_WIDTH, 0) for n in glyph_order})
    fb.setupHorizontalHeader(ascent=ASCENDER, descent=DESCENDER)
    fb.setupNameTable(name_strings())
    fb.setupOS2(**os2_values())
    fb.setupPost(isFixedPitch=1)

    path = OUT / "Redacto-Regular.ttf"
    fb.save(str(path))
    return path


# ── OTF (CFF) builder ───────────────────────────────────────────────

def build_otf(glyph_order, cmap):
    """Build a CFF-flavored OpenType font (.otf)."""
    fb = FontBuilder(UPM, isTTF=False)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap, allowFallback=True)

    # Build one reference charstring, then stamp copies for each glyph.
    pen = T2CharStringPen(GLYPH_WIDTH, None)
    pen.moveTo((0, DESCENDER))
    pen.lineTo((GLYPH_WIDTH, DESCENDER))
    pen.lineTo((GLYPH_WIDTH, ASCENDER))
    pen.lineTo((0, ASCENDER))
    pen.closePath()
    ref = pen.getCharString()
    program = list(ref.program)

    charstrings = {}
    for name in glyph_order:
        cs = T2CharString()
        cs.program = list(program)
        charstrings[name] = cs

    fb.setupCFF(PS_NAME, {"FullName": PS_NAME}, charstrings, {})
    fb.setupHorizontalMetrics({n: (GLYPH_WIDTH, 0) for n in glyph_order})
    fb.setupHorizontalHeader(ascent=ASCENDER, descent=DESCENDER)
    fb.setupNameTable(name_strings())
    fb.setupOS2(**os2_values())
    fb.setupPost(isFixedPitch=1)

    path = OUT / "Redacto-Regular.otf"
    fb.save(str(path))
    return path


# ── WOFF2 converter ─────────────────────────────────────────────────

def build_woff2(source_ttf):
    """Convert an existing TTF to WOFF2."""
    font = TTFont(str(source_ttf))
    font.flavor = "woff2"
    path = OUT / "Redacto-Regular.woff2"
    font.save(str(path))
    return path


# ── Main ─────────────────────────────────────────────────────────────

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    codepoints = collect_codepoints()
    glyph_order = [".notdef"] + [glyph_name(cp) for cp in codepoints]
    cmap = {cp: glyph_name(cp) for cp in codepoints}

    n = len(codepoints)
    print(f"Building Redacto  ({n} BMP code points + .notdef)")

    print("  TTF  …", end=" ", flush=True)
    ttf = build_ttf(glyph_order, cmap)
    print(ttf.name)

    print("  OTF  …", end=" ", flush=True)
    otf = build_otf(glyph_order, cmap)
    print(otf.name)

    print("  WOFF2…", end=" ", flush=True)
    w2 = build_woff2(ttf)
    print(w2.name)

    print("Done.")


if __name__ == "__main__":
    main()
