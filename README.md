# Redacto

A pan-Unicode redaction font. Every glyph is a solid black rectangle—the
typographic equivalent of a censored document.

Redacto covers all assigned code points in the Unicode Basic Multilingual
Plane (~55 000 glyphs). Each glyph is a full-height (ascender-to-descender)
filled rectangle whose advance width equals a standard *n*-width (500 units
in a 1 000 UPM design). Because the outlines are vector, the font works at
any point size.

## Formats

The build produces three files - click to download:

| File | Format |
|------|--------|
| [`Redacto-Regular.otf`](fonts/Redacto-Regular.otf) | CFF-flavored OpenType |
| [`Redacto-Regular.ttf`](fonts/Redacto-Regular.ttf) | TrueType-flavored OpenType |
| [`Redacto-Regular.woff2`](fonts/Redacto-Regular.woff2) | WOFF2 (web) |

## Building

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
make
```

Or directly:

```
python3 sources/build.py
```

The compiled fonts are written to `fonts/`.

## License

Redacto is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).
