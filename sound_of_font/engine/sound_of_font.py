"""Sound of Font engine: phonetic conversion, spell/grammar, inline helptext."""

from __future__ import annotations

import bisect
import json
import os
import re
import threading
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping

from ..dictionaries.multilingual_lexicon import (
    EN_COMMON_WORDS,
    EN_CORRECTIONS,
    HEADING_KEYWORDS,
    LANGUAGES,
    LATIN_LANGUAGES,
    NUMBER_SOUNDS,
    TEMPLATES,
    UNSPACED_LANGUAGES,
    WORDS,
)

LEAD_PUNCT = "([{\"'“‘¿¡«<"
TRAIL_PUNCT = ".,;:!?)]}\"'”’…।॥»>。、，！？؟،؛۔።፣"
SENTENCE_END = ".!?。！？।؟۔።"

_URL_OR_ID = re.compile(
    r"^(?:[a-z][a-z0-9+.\-]*://\S+|www\.\S+|[^\s@]+@[^\s@]+\.[^\s@]+|[@#]\S+"
    r"|[\w\-]+(?:\.[\w\-]+)*\.(?:com|in|org|net|io|ai|co|dev|app|cloud)(?:/\S*)?)$",
    re.IGNORECASE,
)
_CURRENCY = re.compile(
    r"^(?:rs\.?|inr|usd|eur|gbp|aed|sar|sgd|myr|rm|s\$|jpy|krw|bdt|₹|\$|€|£|¥|₩|৳|௹|฿|⃁|⃃)\s*\d[\d,]*(?:\.\d+)?(?:/-)?$",
    re.IGNORECASE,
)
_CURRENCY_WORDS = {
    "rs", "rs.", "inr", "usd", "eur", "gbp", "aed", "sar", "sgd", "myr", "rm",
    "s$", "jpy", "krw", "bdt", "no", "no.", "#", "₹", "$", "€", "£", "¥", "₩", "৳", "௹", "฿", "⃁", "⃃",
}
_LATIN_WORD = re.compile(r"^[A-Za-z]+(?:'[A-Za-z]+)?$")
_ABBREVIATIONS = {"rs", "mr", "mrs", "ms", "dr", "no", "etc", "e.g", "i.e", "st"}


def detect_default_language(system_locale: str | None = None) -> str:
    """Map a system/app locale (``ta_IN.UTF-8``, ``zh-Hans-CN``) to a language code."""
    if system_locale is None:
        for key in ("LC_ALL", "LC_MESSAGES", "LANG"):
            if os.environ.get(key):
                system_locale = os.environ[key]
                break
    if not system_locale:
        return "en"
    tag = system_locale.split(".")[0].split("@")[0].replace("_", "-").lower()
    if tag in LANGUAGES:
        return tag
    base = tag.split("-")[0]
    base = {"id": "ms", "in": "ms"}.get(base, base)
    return base if base in LANGUAGES else "en"


def split_punct(token: str) -> tuple[str, str, str]:
    rest = token.lstrip(LEAD_PUNCT)
    lead = token[: len(token) - len(rest)]
    core = rest.rstrip(TRAIL_PUNCT)
    return lead, core, rest[len(core):]


def is_protected(token: str) -> bool:
    """True for numbers, currency, dates, URLs, emails, codes and acronyms."""
    if _URL_OR_ID.match(token) or _CURRENCY.match(token):
        return True
    if any(ch.isdigit() for ch in token):
        return True
    return len(token) > 1 and token.isascii() and token.isalpha() and token.isupper()


def sound_skeleton(word: str) -> str:
    """Collapse spelling variants that sound alike into one key."""
    s = word.lower()
    for old, new in (("zh", "l"), ("sh", "s"), ("th", "t"), ("dh", "d"), ("bh", "b"),
                     ("ph", "p"), ("gh", "g"), ("kh", "k"), ("ch", "c"), ("jh", "j"),
                     ("ee", "i"), ("oo", "u"), ("w", "v"), ("ck", "k"), ("q", "k")):
        s = s.replace(old, new)
    return re.sub(r"(.)\1+", r"\1", s)


_VOWELS = set("aeiou")
_SIMILAR = {frozenset(p) for p in ("td", "kg", "pb", "cs", "cj", "sz", "vb", "fp", "nm", "iy", "uv", "lr")}


def acoustic_distance(a: str, b: str) -> float:
    """Weighted edit distance: vowel and voicing slips are cheap."""
    def indel(ch: str) -> float:
        return 0.6 if ch in _VOWELS or ch == "h" else 1.0

    prev = [0.0]
    for ch in b:
        prev.append(prev[-1] + indel(ch))
    for x in a:
        cur = [prev[0] + indel(x)]
        for j, y in enumerate(b, 1):
            if x == y:
                sub = 0.0
            elif frozenset((x, y)) in _SIMILAR:
                sub = 0.35
            elif x in _VOWELS and y in _VOWELS:
                sub = 0.6
            else:
                sub = 1.0
            cur.append(min(prev[j - 1] + sub, prev[j] + indel(x), cur[j - 1] + indel(y)))
        prev = cur
    return prev[-1]


# ---------------------------------------------------------------- transliteration

def _longest(table: Mapping[str, object], s: str, i: int, size: int = 4) -> str | None:
    for n in range(size, 0, -1):
        chunk = s[i:i + n]
        if len(chunk) == n and chunk in table:
            return chunk
    return None


_DEVA_C = dict(zip(
    "k kh g gh ch chh j jh t th d dh n p ph f b bh m y r l v w s sh h c q z".split(),
    "क ख ग घ च छ ज झ त थ द ध न प फ फ ब भ म य र ल व व स श ह क क ज".split()))
_TAMIL_C = dict(zip(
    "ngk ngg njch njc ndr nth ndh ng nj k kh g gh c ch j t th d dh n p ph f b bh m y r l v w s sh h zh q z".split(),
    "ங்க ங்க ஞ்ச ஞ்ச ன்ற ந்த ந்த ங்க ஞ்ச க க க க ச ச ஜ ட த ட த ந ப ப ப ப ப ம ய ர ல வ வ ச ஷ ஹ ழ க ஜ".split()))
_VOWEL_KEYS = ("a", "aa", "i", "ee", "ii", "u", "oo", "uu", "e", "ae", "ai", "o", "oa", "au")
_DEVA_V = dict(zip(_VOWEL_KEYS, "अ आ इ ई ई उ ऊ ऊ ए ए ऐ ओ ओ औ".split()))
_DEVA_M = dict(zip(_VOWEL_KEYS, ["", "ा", "ि", "ी", "ी", "ु", "ू", "ू", "े", "े", "ै", "ो", "ो", "ौ"]))
_TAMIL_V = dict(zip(_VOWEL_KEYS, "அ ஆ இ ஈ ஈ உ ஊ ஊ எ ஏ ஐ ஒ ஓ ஔ".split()))
_TAMIL_M = dict(zip(_VOWEL_KEYS, ["", "ா", "ி", "ீ", "ீ", "ு", "ூ", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]))
# ISCII-aligned Unicode blocks: Devanagari code point + offset = target script.
_BLOCK_OFFSET = {"bn": 0x80, "pa": 0x100, "te": 0x300, "kn": 0x380, "ml": 0x400}
_DRAVIDIAN = ("ta", "ta-sen", "te", "ml", "kn")


def _brahmic(word: str, lang: str) -> str:
    tamil = lang in ("ta", "ta-sen")
    cons = _TAMIL_C if tamil else _DEVA_C
    vow = dict(_TAMIL_V if tamil else _DEVA_V)
    mat = dict(_TAMIL_M if tamil else _DEVA_M)
    virama = "்" if tamil else "्"
    if lang in ("te", "ml", "kn"):
        vow.update(e="ऎ", o="ऒ")
        mat.update(e="ॆ", o="ॊ")
    out: list[str] = []
    i = 0
    while i < len(word):
        c = _longest(cons, word, i)
        if c:
            i += len(c)
            glyph = cons[c]
            if tamil and c == "n" and i > 1:
                glyph = "ன"
            v = _longest(vow, word, i)
            if v:
                out.append(glyph + mat[v])
                i += len(v)
            elif i < len(word) or (lang in _DRAVIDIAN and len(glyph) == 1):
                out.append(glyph + virama)
            else:
                out.append(glyph)
            continue
        v = _longest(vow, word, i)
        if v:
            out.append(vow[v])
            i += len(v)
        else:
            out.append(word[i])
            i += 1
    text = "".join(out)
    if lang == "bn":
        text = text.replace("व", "ब")
    if lang == "pa":
        text = text.replace("ष", "श")
    offset = _BLOCK_OFFSET.get(lang)
    if offset:
        text = "".join(chr(ord(ch) + offset) if "ऀ" <= ch <= "ॿ" else ch for ch in text)
    return text


def _table(keys: str, values: str) -> dict[str, str]:
    return dict(zip(keys.split(), values.split()))


_CYRILLIC = _table(
    "shch zh kh ts ch sh yu ya yo a b v g d e z i j k l m n o p r s t u f h y c w x q",
    "щ ж х ц ч ш ю я ё а б в г д е з и й к л м н о п р с т у ф х ы к в кс к")


def _kana_table() -> dict[str, str]:
    table = dict(zip("aiueo", "あいうえお"))
    rows = {"k": "かきくけこ", "s": "さしすせそ", "t": "たちつてと", "n": "なにぬねの",
            "h": "はひふへほ", "m": "まみむめも", "r": "らりるれろ", "g": "がぎぐげご",
            "z": "ざじずぜぞ", "d": "だぢづでど", "b": "ばびぶべぼ", "p": "ぱぴぷぺぽ"}
    for consonant, row in rows.items():
        for vowel, kana in zip("aiueo", row):
            table[consonant + vowel] = kana
    table.update({"ya": "や", "yu": "ゆ", "yo": "よ", "wa": "わ", "wo": "を", "n": "ん",
                  "shi": "し", "chi": "ち", "tsu": "つ", "fu": "ふ", "ji": "じ"})
    return table


_KANA = _kana_table()
_ARABIC = _table(
    "sh kh th dh gh aa ee oo b t j h d r z s f q k l m n w y p g v c",
    "ش خ ث ذ غ ا ي و ب ت ج ه د ر ز س ف ق ك ل م ن و ي ب ج ف ك")
_URDU = _table(
    "sh kh ch gh aa ee oo b p t j h d r z s f q k g l m n w v y c",
    "ش کھ چ غ ا ی و ب پ ت ج ہ د ر ز س ف ق ک گ ل م ن و و ی ک")
_THAI_C = _table("kh ch th ph ng k j d t n b p f m y r l w s h g",
                 "ค ช ท พ ง ก จ ด ต น บ ป ฟ ม ย ร ล ว ส ห ก")
_THAI_V = {"a": ("", "า"), "i": ("", "ิ"), "u": ("", "ุ"), "e": ("เ", ""), "o": ("โ", "")}
_ETHIOPIC = {"hh": 0x1210, "chh": 0x1328, "kh": 0x12B8, "zh": 0x12E0, "ts": 0x1338, "tz": 0x1340,
             "h": 0x1200, "l": 0x1208, "m": 0x1218, "r": 0x1228, "s": 0x1230, "sh": 0x1238,
             "q": 0x1240, "b": 0x1260, "v": 0x1268, "t": 0x1270, "ch": 0x1278, "n": 0x1290,
             "k": 0x12A8, "w": 0x12C8, "z": 0x12D8, "y": 0x12E8, "d": 0x12F0, "j": 0x1300,
             "g": 0x1308, "f": 0x1348, "p": 0x1350}
_ETHIOPIC_ORDER = {"e": 0, "u": 1, "i": 2, "a": 3, "ie": 4, "o": 6}
_ETHIOPIC_ALONE = {"a": "አ", "u": "ኡ", "i": "ኢ", "e": "እ", "o": "ኦ"}
_HANGUL_L = {"g": 0, "kk": 1, "n": 2, "d": 3, "tt": 4, "r": 5, "l": 5, "m": 6, "b": 7, "pp": 8,
             "s": 9, "ss": 10, "j": 12, "jj": 13, "ch": 14, "k": 15, "t": 16, "p": 17, "h": 18}
_HANGUL_V = {v: i for i, v in enumerate(
    "a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i".split())}
_HANGUL_T = {"g": 1, "n": 4, "d": 7, "l": 8, "r": 8, "m": 16, "b": 17, "s": 19, "ng": 21,
             "j": 22, "ch": 23, "k": 24, "t": 25, "p": 26, "h": 27}


def _greedy(word: str, table: Mapping[str, str]) -> str:
    out, i = [], 0
    while i < len(word):
        key = _longest(table, word, i)
        out.append(table[key] if key else word[i])
        i += len(key) if key else 1
    return "".join(out)


def _arabic_script(word: str, table: Mapping[str, str]) -> str:
    out, i = [], 0
    while i < len(word):
        key = _longest(table, word, i)
        if key:
            out.append(table[key])
            i += len(key)
        else:
            # Short vowels are unwritten except at word edges.
            if i == 0 or (i == len(word) - 1 and word[i] == "a"):
                out.append("ا")
            i += 1
    return "".join(out)


def _japanese(word: str) -> str:
    out, i = [], 0
    while i < len(word):
        if i + 1 < len(word) and word[i] == word[i + 1] and word[i] not in "aiueon":
            out.append("っ")
            i += 1
            continue
        key = _longest(_KANA, word, i)
        out.append(_KANA[key] if key else word[i])
        i += len(key) if key else 1
    return "".join(out)


def _thai(word: str) -> str:
    out, i = [], 0
    while i < len(word):
        c = _longest(_THAI_C, word, i)
        glyph = _THAI_C[c] if c else "อ"
        i += len(c) if c else 0
        if i < len(word) and word[i] in _THAI_V:
            before, after = _THAI_V[word[i]]
            out.append(before + glyph + after)
            i += 1
        elif c:
            out.append(glyph)
        else:
            out.append(word[i])
            i += 1
    return "".join(out)


def _amharic(word: str) -> str:
    out, i = [], 0
    while i < len(word):
        c = _longest(_ETHIOPIC, word, i)
        if c:
            i += len(c)
            v = _longest(_ETHIOPIC_ORDER, word, i)
            out.append(chr(_ETHIOPIC[c] + (_ETHIOPIC_ORDER[v] if v else 5)))
            i += len(v) if v else 0
        else:
            out.append(_ETHIOPIC_ALONE.get(word[i], word[i]))
            i += 1
    return "".join(out)


def _hangul(word: str) -> str:
    out, i = [], 0
    while i < len(word):
        onset = _longest(_HANGUL_L, word, i)
        j = i + (len(onset) if onset else 0)
        vowel = _longest(_HANGUL_V, word, j)
        if not onset and not vowel:
            out.append(word[i])
            i += 1
            continue
        j += len(vowel) if vowel else 0
        coda = _longest(_HANGUL_T, word, j) if vowel else None
        # A consonant followed by a vowel starts the next syllable.
        if coda and _longest(_HANGUL_V, word, j + len(coda)):
            coda = None
        j += len(coda) if coda else 0
        lead = _HANGUL_L[onset] if onset else 11
        mid = _HANGUL_V[vowel] if vowel else 18
        out.append(chr(0xAC00 + lead * 588 + mid * 28 + (_HANGUL_T[coda] if coda else 0)))
        i = j
    return "".join(out)


def transliterate(word: str, lang: str) -> str:
    """Algorithmic fallback. Latin-script languages and zh are returned unchanged."""
    w = word.lower()
    if lang in ("ta", "ta-sen", "hi", "hi-prathmic", "mr", "sa", "te", "ml", "kn", "bn", "pa"):
        return _brahmic(w, lang)
    if lang == "ru":
        return _greedy(w, _CYRILLIC)
    if lang == "ja":
        return _japanese(w)
    if lang in ("ar", "ur"):
        return _arabic_script(w, _URDU if lang == "ur" else _ARABIC)
    if lang == "th":
        return _thai(w)
    if lang == "am":
        return _amharic(w)
    if lang == "ko":
        return _hangul(w)
    return word


# ---------------------------------------------------------------- engine

@dataclass
class InlineSuggestion:
    replacement_word: str = ""
    inline_ghost_completion: str = ""
    next_words: list[str] = field(default_factory=list)
    full_clause_suggestion: str = ""
    category: str | None = None


@dataclass
class CommitResult:
    committed_word: str
    text: str
    replaced: bool
    inline_ghost_completion: str = ""
    next_words: list[str] = field(default_factory=list)
    full_clause_suggestion: str = ""


def _strip_marks(word: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", word) if not unicodedata.combining(c))


def _norm(word: str) -> str:
    return split_punct(word)[1].lower()


class SoundOfFontEngine:
    def __init__(self, language: str | None = None, system_locale: str | None = None):
        self.language = language if language in LANGUAGES else detect_default_language(system_locale)
        self._user: dict[str, dict[str, str]] = {}
        self._index_cache: dict[str, tuple] = {}
        self._words_exact_cache: dict[str, set[str]] = {}
        self._template_cache: dict[tuple[str, str], list[tuple[str, str]]] = {}
        self._convert_cache: dict[tuple[str, str], str] = {}
        self._os_words: set[str] = set()
        self._os_sorted: list[str] = []
        self._os_lock = threading.Lock()
        self._os_thread: threading.Thread | None = None
        self.merge_os_dictionary()

    def _lang(self, lang: str | None) -> str:
        return lang if lang in LANGUAGES else self.language

    # ---- dictionaries

    def merge_os_dictionary(self, path: str = "/usr/share/dict/words", wait: bool = False) -> bool:
        """Schedule a background load of the OS word list; returns without blocking."""
        if not os.path.isfile(path):
            return False
        prev_thread = self._os_thread

        def load() -> None:
            if prev_thread is not None and prev_thread.is_alive():
                prev_thread.join(timeout=2.0)
            with open(path, encoding="utf-8", errors="ignore") as handle:
                words = {line.strip().lower() for line in handle if line.strip()}
            with self._os_lock:
                merged = self._os_words | words
                self._os_sorted = sorted(merged)
                self._os_words = merged

        self._os_thread = threading.Thread(target=load, daemon=True)
        self._os_thread.start()
        if wait:
            self._os_thread.join()
        return True

    def add_user_words(self, words: Iterable[str] | Mapping[str, str], lang: str = "en") -> None:
        """Add words (list) or phonetic spellings (``{roman: native}``)."""
        pairs = words.items() if isinstance(words, Mapping) else ((w, w) for w in words)
        bucket = self._user.setdefault(lang, {})
        for roman, native in pairs:
            if roman and native:
                bucket[roman.lower()] = native
        self._convert_cache.clear()

    def is_known_word(self, word: str, lang: str = "en") -> bool:
        low = word.lower()
        if low in self._user.get(lang, {}):
            return True
        if lang == "en" and low in self._os_words:
            return True
        return low in self._index(lang)[0]

    def _template(self, category: str, lang: str) -> list[tuple[str, str]]:
        key = (category, lang)
        if key not in self._template_cache:
            pairs = []
            for part in TEMPLATES[lang][category].split():
                native, _, roman = part.partition("|")
                native = native.replace("_", " ")
                pairs.append((native, roman or _strip_marks(_norm(native))))
            self._template_cache[key] = pairs
        return self._template_cache[key]

    def _index(self, lang: str) -> tuple:
        """(exact roman->native, skeleton->native, first letter->[(skeleton, native)])."""
        if lang not in self._index_cache:
            exact: dict[str, str] = {}
            skeletons: dict[str, str] = {}
            buckets: dict[str, list[tuple[str, str]]] = {}

            def add(roman: str, native: str) -> None:
                exact.setdefault(roman, native)
                key = sound_skeleton(roman)
                if key and key not in skeletons:
                    skeletons[key] = native
                    buckets.setdefault(key[0], []).append((key, native))

            for entry in WORDS[lang].split():
                native, _, aliases = entry.partition("|")
                native = native.replace("_", " ")
                for roman in (aliases.split(",") if aliases else [native.lower()]):
                    add(roman, native)
            for category in TEMPLATES[lang]:
                for native, roman in self._template(category, lang):
                    bare = split_punct(native)[1]
                    if lang not in LATIN_LANGUAGES or len(roman) >= 4:
                        if _LATIN_WORD.match(roman):
                            add(roman.lower(), bare)
            self._index_cache[lang] = (exact, skeletons, buckets)
        return self._index_cache[lang]

    # ---- conversion

    def _match_sound(self, core: str, lang: str) -> str:
        low = core.lower()
        user = self._user.get(lang, {})
        if low in user:
            return user[low]
        if lang == "en":
            fixed = EN_CORRECTIONS.get(low)
            if not fixed:
                return core
            return fixed[0].upper() + fixed[1:] if core[0].isupper() else fixed
        exact, skeletons, buckets = self._index(lang)
        if lang in LATIN_LANGUAGES:
            native = exact.get(low)
            if not native:
                return core
            return native[0].upper() + native[1:] if core[0].isupper() else native
        if low in exact:
            return exact[low]
        key = sound_skeleton(low)
        if len(key) >= 3 and key in skeletons:
            return skeletons[key]
        if len(key) >= 5:
            limit = 0.7 if len(key) <= 6 else 1.2
            best, best_score = None, limit + 1e-9
            for candidate, native in buckets.get(key[0], ()):
                if abs(len(candidate) - len(key)) <= 2:
                    score = acoustic_distance(key, candidate)
                    if score < best_score:
                        best, best_score = native, score
            if best:
                return best
        return transliterate(low, lang)

    def convert_token(self, token: str, lang: str | None = None) -> str:
        lang = self._lang(lang)
        if not token:
            return token
        if any(ch.isspace() for ch in token):
            return self.convert_text(token, lang)
        cached = self._convert_cache.get((lang, token))
        if cached is not None:
            return cached
        result = self._convert_uncached(token, lang)
        if len(self._convert_cache) >= 4096:
            self._convert_cache.clear()
        self._convert_cache[(lang, token)] = result
        return result

    def _words_exact(self, lang: str) -> set[str]:
        if lang not in self._words_exact_cache:
            keys: set[str] = set()
            for entry in WORDS[lang].split():
                native, _, aliases = entry.partition("|")
                for roman in (aliases.split(",") if aliases else [native.lower()]):
                    keys.add(roman.lower())
            self._words_exact_cache[lang] = keys
        return self._words_exact_cache[lang]

    def _convert_uncached(self, token: str, lang: str) -> str:
        if _URL_OR_ID.match(token) or _CURRENCY.match(token):
            return token
        lead, core, trail = split_punct(token)
        if not core:
            return token
        if _URL_OR_ID.match(core) or _CURRENCY.match(core) or core.lower() in ("rs", "s$"):
            return token
        if trail.startswith(".") and core.lower() in _ABBREVIATIONS:
            return token
        sound = NUMBER_SOUNDS.get(lang, {}).get(core.lower())
        if sound:
            return lead + sound + trail
        low = core.lower()
        allow_upper_phonetic = (
            lang != "en"
            and len(core) > 1
            and core.isascii()
            and core.isalpha()
            and core.isupper()
            and (low in self._words_exact(lang) or low in self._user.get(lang, {}))
        )
        if (is_protected(core) and not allow_upper_phonetic) or not _LATIN_WORD.match(core):
            return token
        return lead + self._match_sound(core, lang) + trail

    def convert_text(self, text: str, lang: str | None = None) -> str:
        lang = self._lang(lang)
        parts = re.split(r"(\s+|[—–])", text)
        out: list[str] = []
        prev_tok = ""
        n_parts = len(parts)
        for idx, part in enumerate(parts):
            if not part or part.isspace() or part in ("—", "–"):
                out.append(part)
                continue
            _, core, _ = split_punct(part)
            next_core = ""
            for k in range(idx + 1, n_parts):
                cand = parts[k]
                if cand and not cand.isspace() and cand not in ("—", "–"):
                    next_core = split_punct(cand)[1]
                    break
            if (part.lower() in _CURRENCY_WORDS or core.lower() in _CURRENCY_WORDS) and next_core[:1].isdigit():
                out.append(part)
            elif prev_tok.lower() in _CURRENCY_WORDS and core.lower() in NUMBER_SOUNDS.get(lang, {}):
                out.append(part)
            else:
                out.append(self.convert_token(part, lang))
            prev_tok = part
        return "".join(out)

    # ---- spelling and grammar

    def auto_correct_sentence(self, text: str, lang: str | None = None) -> str:
        lang = self._lang(lang)
        text = re.sub(r"(?<=\S)[ \t]{2,}", " ", text)
        text = re.sub(r"(?<=\S)[ \t]+(?=[,;:!?.](?:\s|$))", "", text)
        if lang == "en":
            return self._correct_english(text)
        if lang in ("ta", "ta-sen"):
            return self._per_sentence(text, lambda words: self._agree_tamil(words, lang))
        if lang in ("hi", "hi-prathmic"):
            return self._per_sentence(text, self._agree_hindi)
        return text

    def _correct_english(self, text: str) -> str:
        parts = re.split(r"(\s+)", text)
        start = True
        for i, token in enumerate(parts):
            if not token or token.isspace():
                continue
            lead, core, trail = split_punct(token)
            if core and not is_protected(token) and _LATIN_WORD.match(core):
                core = self._match_sound(core, "en")
                if start:
                    core = core[0].upper() + core[1:]
                parts[i] = lead + core + trail
            start = trail[:1] in (".", "!", "?") and core.lower() not in _ABBREVIATIONS
        result = "".join(parts)
        for pattern, repl in ((r"\bI (?:is|are)\b", "I am"), (r"\b([Yy]ou|[Tt]hey|[Ww]e) is\b", r"\1 are"),
                              (r"\b([Hh]e|[Ss]he|[Ii]t) don't\b", r"\1 doesn't")):
            result = re.sub(pattern, repl, result)
        return result

    @staticmethod
    def _per_sentence(text: str, fix) -> str:
        chunks = re.split(r"([.!?।\n]+)", text)
        for i in range(0, len(chunks), 2):
            parts = re.split(r"(\s+)", chunks[i])
            positions = [j for j, p in enumerate(parts) if p and not p.isspace()]
            if positions:
                words = fix([parts[j] for j in positions])
                for j, word in zip(positions, words):
                    parts[j] = word
                chunks[i] = "".join(parts)
        return "".join(chunks)

    @staticmethod
    def _agree_tamil(words: list[str], lang: str) -> list[str]:
        if lang == "ta-sen":
            formal = {"ரொம்ப": "மிகவும்", "தேங்க்ஸ்": "நன்றி", "லீவு": "விடுப்பு",
                      "ஆபீஸ்": "அலுவலகம்", "ஸ்கூல்": "பள்ளி", "நீ": "நீங்கள்"}
            words = [formal.get(w, w) for w in words]
        subjects = [w for w in words if w in ("நான்", "நீங்கள்")]
        if len(subjects) != 1 or len(words) < 2:
            return words
        wanted = "கிறேன்" if subjects[0] == "நான்" else "கிறீர்கள்"
        lead, core, trail = split_punct(words[-1])
        for ending in ("கிறீர்கள்", "கிறார்கள்", "கிறோம்", "கிறேன்", "கிறாய்", "கிறான்", "கிறாள்", "கிறார்"):
            if core.endswith(ending):
                words[-1] = lead + core[: -len(ending)] + wanted + trail
                break
        return words

    @staticmethod
    def _agree_hindi(words: list[str]) -> list[str]:
        subjects = [w for w in words if w in ("मैं", "आप")]
        if len(subjects) != 1 or len(words) < 2:
            return words
        lead, core, trail = split_punct(words[-1])
        if core in ("है", "हैं", "हो", "हूँ", "हूं"):
            words[-1] = lead + ("हूँ" if subjects[0] == "मैं" else "हैं") + trail
        return words

    # ---- context helptext

    def detect_category(self, heading: str, prior_text: str = "") -> str | None:
        for source in (heading, prior_text):
            low = (source or "").lower()
            if not low:
                continue
            for category, keywords in HEADING_KEYWORDS:
                for keyword in keywords:
                    if keyword.isascii():
                        if re.search(r"\b" + re.escape(keyword) + r"\b", low):
                            return category
                    elif keyword in low:
                        return category
        return None

    @staticmethod
    def _locate(prior: str, words: list[tuple[str, str]], lang: str) -> int | None:
        """Index of the next expected template word, or None if the user deviated."""
        if not prior.strip():
            return 0
        if lang in UNSPACED_LANGUAGES:
            compact = "".join(prior.split())
            for k in range(len(words), 0, -1):
                if compact.endswith("".join(n for n, _ in words[:k])):
                    return k
            return None
        typed = [_norm(t) for t in prior.split() if _norm(t)]
        if not typed:
            return 0
        flat: list[tuple[str, int | None]] = []
        for idx, (n_str, _) in enumerate(words):
            subs = [_norm(part) for part in n_str.split() if _norm(part)] or [_norm(n_str)]
            for k, sub in enumerate(subs):
                flat.append((sub, (idx + 1) if k == len(subs) - 1 else None))
        best, position = 0, None
        for j, (_sub, next_pos) in enumerate(flat):
            if next_pos is None:
                continue
            n = 0
            while n < len(typed) and n <= j and flat[j - n][0] == typed[-1 - n]:
                n += 1
            if n > best:
                best, position = n, next_pos
        return position

    @staticmethod
    def _word_matches(typed: str, native: str, roman: str) -> bool:
        low = typed.lower()
        if roman.lower().startswith(low) or native.lower().startswith(low):
            return True
        return len(low) >= 3 and sound_skeleton(roman).startswith(sound_skeleton(low))

    @staticmethod
    def _body(heading: str, prior: str) -> str:
        head = (heading or "").strip()
        if head and prior.lstrip().startswith(head):
            return prior.lstrip()[len(head):]
        return prior

    def suggest_inline(self, heading: str, prior_text: str, current_input: str,
                       lang: str | None = None) -> InlineSuggestion:
        lang = self._lang(lang)
        category = self.detect_category(heading, prior_text)
        typed = current_input.strip()
        core = split_punct(typed)[1]
        sound = NUMBER_SOUNDS.get(lang, {}).get(core.lower())
        allow_upper_phonetic = (
            lang != "en"
            and len(core) > 1
            and core.isascii()
            and core.isalpha()
            and core.isupper()
            and (core.lower() in self._words_exact(lang) or core.lower() in self._user.get(lang, {}))
        )
        if typed and (sound or (is_protected(typed) and not allow_upper_phonetic)):
            return InlineSuggestion(replacement_word=self.convert_token(typed, lang), category=category)
        joiner = "" if lang in UNSPACED_LANGUAGES else " "
        if category:
            words = self._template(category, lang)
            position = self._locate(self._body(heading, prior_text or ""), words, lang)
            match = None
            if position is not None and position < len(words):
                if not core or self._word_matches(core, *words[position]):
                    match = position
            if match is None and len(core) >= 3:
                match = next((i for i, w in enumerate(words) if self._word_matches(core, *w)), None)
            if match is not None:
                end = match
                while end < len(words) - 1 and words[end][0][-1] not in SENTENCE_END:
                    end += 1
                clause = joiner.join(n for n, _ in words[match:end + 1])
                native = words[match][0]
                ghost = clause[len(core):] if core and clause.lower().startswith(core.lower()) else clause
                start = match + 1 if core else match
                return InlineSuggestion(
                    replacement_word=native if core else "",
                    inline_ghost_completion=ghost,
                    next_words=[n for n, _ in words[start:start + 4]],
                    full_clause_suggestion=clause,
                    category=category,
                )
        replacement = self.convert_token(typed, lang) if typed else ""
        ghost = self._complete(core, lang) if len(core) >= 3 else ""
        return InlineSuggestion(replacement_word=replacement, inline_ghost_completion=ghost, category=category)

    def _complete(self, prefix: str, lang: str) -> str:
        low = prefix.lower()
        pool = list(self._user.get(lang, {}))
        if lang == "en":
            pool += list(self._index("en")[0])
            pool += sorted(EN_COMMON_WORDS)
        for word in pool:
            if word.startswith(low) and len(word) > len(low):
                return word[len(low):]
        if lang == "en" and self._os_sorted:
            with self._os_lock:
                i = bisect.bisect_right(self._os_sorted, low)
                if i < len(self._os_sorted) and self._os_sorted[i].startswith(low):
                    return self._os_sorted[i][len(low):]
        return ""

    def on_space_commit(self, heading: str, prior_text: str, current_token: str,
                        lang: str | None = None) -> CommitResult:
        lang = self._lang(lang)
        prior = prior_text or ""
        token = current_token.strip()
        if not token:
            return CommitResult(committed_word="", text=prior, replaced=False)
        joiner = "" if lang in UNSPACED_LANGUAGES else " "
        prev_words = prior.split()
        prev_last = prev_words[-1].lower() if prev_words else ""
        _, core_tok, _ = split_punct(token)
        if prev_last in _CURRENCY_WORDS and core_tok.lower() in NUMBER_SOUNDS.get(lang, {}):
            committed = token
        else:
            committed = self._context_word(heading, prior, token, lang) or self.convert_token(token, lang)
        gap = joiner if prior and not prior[-1].isspace() else ""
        text = prior + gap + committed + joiner
        upcoming = self.suggest_inline(heading, text, "", lang)
        return CommitResult(
            committed_word=committed,
            text=text,
            replaced=committed != token,
            inline_ghost_completion=upcoming.inline_ghost_completion,
            next_words=upcoming.next_words,
            full_clause_suggestion=upcoming.full_clause_suggestion,
        )

    def _context_word(self, heading: str, prior: str, token: str, lang: str) -> str | None:
        """The expected template word, only if the token is a start or sound of it."""
        category = self.detect_category(heading, prior)
        lead, core, trail = split_punct(token)
        low = core.lower()
        allow_upper_phonetic = (
            lang != "en"
            and len(core) > 1
            and core.isascii()
            and core.isalpha()
            and core.isupper()
            and (low in self._words_exact(lang) or low in self._user.get(lang, {}))
        )
        if not category or not core or (is_protected(core) and not allow_upper_phonetic) or low in NUMBER_SOUNDS.get(lang, {}):
            return None
        if _URL_OR_ID.match(token) or low in self._user.get(lang, {}):
            return None
        if lang == "en" and low in EN_CORRECTIONS and low != "i":
            return None
        words = self._template(category, lang)
        position = self._locate(self._body(heading, prior), words, lang)
        match: int | None = None
        if position is not None and position < len(words):
            native_p, roman_p = words[position]
            if lang == "en":
                if not (position == 0 and len(core) == 1 and low in ("a", "i") and roman_p.lower() != low):
                    if roman_p.lower().startswith(low) or native_p.lower().startswith(low):
                        match = position
            elif self._word_matches(core, native_p, roman_p):
                match = position
        if match is None and len(core) >= 3:
            if not (lang == "en" and low in EN_COMMON_WORDS):
                match = next((i for i, w in enumerate(words) if self._word_matches(core, *w)), None)
        if match is None:
            return None
        native, roman = words[match]
        if low != roman.lower() and low in self._index(lang)[0] and lang != "en":
            return None
        if trail:
            native = split_punct(native)[1] + trail
        return lead + native


# ---------------------------------------------------------------- font metadata

class BackgroundFontMetadataIndexer:
    """Indexes ``dist/<family>/**/<Name>-<Style>.<ext>`` on a daemon thread."""

    EXTENSIONS = (".woff2", ".woff", ".ttf", ".otf")

    def __init__(self, dist_dir: str | os.PathLike | None = None):
        self.dist_dir = Path(dist_dir) if dist_dir else Path(__file__).resolve().parents[2] / "dist"
        self.index: dict = {}
        self.error: str | None = None
        self._done = threading.Event()

    def start(self) -> float:
        """Start indexing; returns the dispatch time in milliseconds."""
        began = time.perf_counter()
        self._done.clear()
        threading.Thread(target=self._run, daemon=True).start()
        return (time.perf_counter() - began) * 1000

    def wait(self, timeout: float | None = 5.0) -> bool:
        return self._done.wait(timeout)

    def _run(self) -> None:
        try:
            began = time.perf_counter()
            families: dict[str, dict] = {}
            folders = sorted(p for p in self.dist_dir.iterdir() if p.is_dir()) if self.dist_dir.is_dir() else []
            for folder in folders:
                styles, files = set(), []
                for path in folder.rglob("*"):
                    if path.suffix.lower() in self.EXTENSIONS:
                        files.append(str(path.relative_to(self.dist_dir)))
                        styles.add(path.stem.rsplit("-", 1)[1] if "-" in path.stem else "Regular")
                if files:
                    families[folder.name] = {
                        "styles": sorted(styles),
                        "files": sorted(files),
                        "ocr_confidence": self._ocr_confidence(folder),
                    }
            self.index = {
                "families": families,
                "family_count": len(families),
                "style_count": sum(len(f["styles"]) for f in families.values()),
                "languages": list(LANGUAGES),
                "scan_ms": (time.perf_counter() - began) * 1000,
            }
        except OSError as exc:
            self.error = str(exc)
        finally:
            self._done.set()

    @staticmethod
    def _ocr_confidence(folder: Path) -> float | None:
        """Read a measured value from a JSON sidecar; None when none exists."""
        for path in sorted(folder.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(data, dict) and isinstance(data.get("ocr_confidence"), (int, float)):
                return float(data["ocr_confidence"])
        return None
