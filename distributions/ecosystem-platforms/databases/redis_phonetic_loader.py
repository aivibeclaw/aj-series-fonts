"""Redis Phonetic Prefix & Skeleton Loader for Aaahhh Fonts Vibe (Sound of Font v3.0.0).

Exports deterministic Redis RESP / pipeline commands indexing all 24 languages'
exact phonetic triggers, sound skeletons, and Tamil number-words (`1u`/`onnu`/`ondru` -> `ஒன்று`).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sound_of_font.dictionaries.multilingual_lexicon import LANGUAGES, NUMBER_SOUNDS, WORDS  # noqa: E402
from sound_of_font.engine.sound_of_font import sound_skeleton  # noqa: E402


def build_redis_entries(key_prefix: str = "aj:sof:v3") -> list[tuple[str, str, str]]:
    """Return `(hash_key, field, native_value)` triples ready for `HSET` pipelining."""
    ops: list[tuple[str, str, str]] = []
    for lang in LANGUAGES:
        h_exact = f"{key_prefix}:{lang}:exact"
        h_skel = f"{key_prefix}:{lang}:skeleton"
        for entry in WORDS[lang].split():
            native, _, aliases = entry.partition("|")
            native = native.replace("_", " ")
            for roman in (aliases.split(",") if aliases else [native.lower()]):
                r_low = roman.lower()
                ops.append((h_exact, r_low, native))
                sk = sound_skeleton(r_low)
                if sk:
                    ops.append((h_skel, sk, native))
        for r_num, n_num in NUMBER_SOUNDS.get(lang, {}).items():
            ops.append((h_exact, r_num.lower(), n_num))
    return ops


def load_into_redis(redis_client, key_prefix: str = "aj:sof:v3") -> int:
    pipe = redis_client.pipeline(transaction=False)
    entries = build_redis_entries(key_prefix)
    for hkey, field, val in entries:
        pipe.hset(hkey, field, val)
    pipe.execute()
    return len(entries)


if __name__ == "__main__":
    sample = build_redis_entries()
    print(json.dumps({"version": "3.0.0", "languages": len(LANGUAGES), "redis_hset_entries": len(sample)}))
