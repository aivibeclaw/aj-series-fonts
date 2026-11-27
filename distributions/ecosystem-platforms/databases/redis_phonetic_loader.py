"""Redis Typography & Stylistic-Set Metadata Loader for AJ Series & Aaahhh Fonts Vibe (v3.1.0).

Indexes canonical 5-family PostScript names, weights, CDN URLs, and OpenType `ss06`–`ss18`
feature tags into Redis hashes without exposing private Sound-of-Font engine internals.
"""
from __future__ import annotations

import json

SUITE_VERSION = "3.1.0"
# PLACEHOLDER: Override CDN_BASE_URL with your internal/edge font mirror if self-hosting unmodified binaries
CDN_BASE_URL = "https://fonts.aivibe.cloud/fonts"

FAMILIES = (
    ("aj-sahasvi", "AJ Sahasvi", "AJSahasvi", ("Regular", "SemiBold", "ExtraBold")),
    ("aj-shresti", "AJ Shresti", "AJShresti", ("Regular", "Italic", "SemiBold", "SemiBoldItalic", "ExtraBold", "ExtraBoldItalic")),
    ("aj-talin", "AJ Talin", "AJTalin", ("Regular", "Italic", "SemiBold", "SemiBoldItalic", "ExtraBold", "ExtraBoldItalic")),
    ("aj-anushya", "AJ Anushya", "AJAnushya", ("Regular", "Italic", "SemiBold", "SemiBoldItalic", "ExtraBold", "ExtraBoldItalic")),
    ("aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", ("Regular", "Italic", "SemiBold", "SemiBoldItalic", "ExtraBold", "ExtraBoldItalic")),
)

LOCALE_FEATURES = {
    "ta": "ss06", "ta-sen": "ss06", "hi": "ss07", "hi-prathmic": "ss07",
    "te": "ss08", "ml": "ss09", "kn": "ss10", "bn": "ss11", "pa": "ss12",
    "ar": "ss13", "ur": "ss13", "ja": "ss14", "ru": "ss15", "zh": "ss16",
    "th": "ss17", "am": "ss18",
}


def build_catalog_entries(key_prefix: str = "aj:fonts:v3_1") -> list[tuple[str, str, str]]:
    """Return `(hash_key, field, json_value)` triples ready for Redis `HSET` pipelining."""
    ops: list[tuple[str, str, str]] = []
    for slug, family, prefix, styles in FAMILIES:
        for style in styles:
            ps_name = f"{prefix}-{style}"
            payload = json.dumps({
                "family": family,
                "style": style,
                "postScriptName": ps_name,
                "woff2": f"{CDN_BASE_URL}/{ps_name}.woff2",
                "version": SUITE_VERSION,
            })
            ops.append((f"{key_prefix}:styles", ps_name, payload))
    for locale, ss in LOCALE_FEATURES.items():
        ops.append((f"{key_prefix}:features", locale, ss))
    return ops


# PLACEHOLDER: Pass an authenticated `redis.Redis.from_url(...)` client configured via environment secrets
def load_into_redis(redis_client, key_prefix: str = "aj:fonts:v3_1") -> int:
    pipe = redis_client.pipeline(transaction=False)
    entries = build_catalog_entries(key_prefix)
    for hkey, field, val in entries:
        pipe.hset(hkey, field, val)
    pipe.execute()
    return len(entries)


if __name__ == "__main__":
    sample = build_catalog_entries()
    print(json.dumps({"version": SUITE_VERSION, "redis_hset_entries": len(sample)}))
