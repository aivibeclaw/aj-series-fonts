"""AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (Python 3.8+, standard library only).

Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
Provided "AS IS" without warranty. https://fonts.aivibe.cloud
"""
from __future__ import annotations

from typing import Iterable, NamedTuple, Optional, Tuple

VERSION = "3.1.0"

# /* PLACEHOLDER: Configure your CDN/local font base URL here */
DEFAULT_FONT_BASE_URL = "https://fonts.aivibe.cloud/fonts"


class Family(NamedTuple):
    id: str
    name: str
    prefix: str
    level: str
    role: str
    has_italic: bool
    italic_angle: float
    x_height: int
    generic: str


FAMILIES: Tuple[Family, ...] = (
    Family("aj-sahasvi", "AJ Sahasvi", "AJSahasvi", "1", "Level 1 Headers (H1)", False, 0, 516, "serif"),
    Family("aj-shresti", "AJ Shresti", "AJShresti", "2", "Level 2 Sub-Headings & OS Default", True, 10, 534, "sans-serif"),
    Family("aj-talin", "AJ Talin", "AJTalin", "3", "Level 3 Script", True, 11, 492, "cursive"),
    Family("aj-anushya", "AJ Anushya", "AJAnushya", "body", "Body Reading", True, 9, 556, "sans-serif"),
    Family("aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", "sound", "Sound of Font", True, 9.5, 558, "sans-serif"),
)

WEIGHTS = {400: "Regular", 600: "SemiBold", 800: "ExtraBold"}
FORMATS = {"woff2": "woff2", "woff": "woff", "ttf": "truetype", "otf": "opentype"}

# ss06-ss18 take effect in Aaahhh Fonts Vibe only.
SOUND_STYLISTIC_SETS = {
    "ta": "ss06", "hi": "ss07", "te": "ss08", "ml": "ss09", "kn": "ss10", "bn": "ss11", "pa": "ss12",
    "ar": "ss13", "ur": "ss13", "ja": "ss14", "ru": "ss15", "zh": "ss16", "th": "ss17", "am": "ss18",
}
FEATURE_TAGS = frozenset(
    "kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05".split()
) | frozenset(SOUND_STYLISTIC_SETS.values())

# OCR disambiguation metadata: character groups the designs keep visually distinct.
OCR_DISAMBIGUATION_GROUPS = (("0", "O", "o"), ("I", "l", "1"), ("a", "b", "6"), ("rn", "m"), ("cl", "d"))
OCR_RECOMMENDED_FAMILY = "AJ Anushya"
OCR_RECOMMENDED_MIN_PX = 12
OCR_FEATURE_SETTINGS = '"zero" 1, "tnum" 1, "liga" 0, "dlig" 0'


def family(key: str) -> Family:
    """Look up a family by id or name."""
    for item in FAMILIES:
        if key in (item.id, item.name):
            return item
    raise ValueError(f"unknown family: {key!r}")


def style_name(key: str, weight: int = 400, italic: bool = False) -> str:
    fam = family(key)
    if weight not in WEIGHTS:
        raise ValueError(f"unsupported weight: {weight}")
    if italic and not fam.has_italic:
        raise ValueError(f"{fam.name} has no italic")
    if not italic:
        return WEIGHTS[weight]
    return "Italic" if weight == 400 else WEIGHTS[weight] + "Italic"


def font_url(key: str, weight: int = 400, italic: bool = False, fmt: str = "woff2",
             base_url: str = DEFAULT_FONT_BASE_URL) -> str:
    if fmt not in FORMATS:
        raise ValueError(f"unsupported format: {fmt}")
    if any(c in base_url for c in "\"'\\\r\n"):
        raise ValueError("base_url contains characters that are unsafe in CSS")
    return f"{base_url.rstrip('/')}/{family(key).prefix}-{style_name(key, weight, italic)}.{fmt}"


def font_stack(key: str) -> str:
    fam = family(key)
    return f'"{fam.name}", system-ui, {fam.generic}'


def font_face_css(key: str, weight: int = 400, italic: bool = False,
                  base_url: str = DEFAULT_FONT_BASE_URL) -> str:
    url = font_url(key, weight, italic, "woff2", base_url)
    style = "italic" if italic else "normal"
    return (f'@font-face {{ font-family: "{family(key).name}"; src: url("{url}") format("woff2"); '
            f"font-weight: {weight}; font-style: {style}; font-display: swap; }}")


def all_font_face_css(base_url: str = DEFAULT_FONT_BASE_URL) -> str:
    """All 27 @font-face rules."""
    return "\n".join(
        font_face_css(fam.id, weight, italic, base_url)
        for fam in FAMILIES
        for italic in ((False, True) if fam.has_italic else (False,))
        for weight in WEIGHTS
    )


def feature_settings(enable: Iterable[str] = (), disable: Iterable[str] = ()) -> str:
    """Value for CSS font-feature-settings."""
    parts = []
    for tags, value in ((enable, 1), (disable, 0)):
        for tag in tags:
            if tag not in FEATURE_TAGS:
                raise ValueError(f"unsupported OpenType feature: {tag}")
            parts.append(f'"{tag}" {value}')
    return ", ".join(parts) or "normal"


def sound_feature_settings(language: str) -> str:
    tag: Optional[str] = SOUND_STYLISTIC_SETS.get(language)
    if tag is None:
        raise ValueError(f"no Sound of Font set for language: {language}")
    return feature_settings((tag, "calt"))
