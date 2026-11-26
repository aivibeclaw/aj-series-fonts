"""Hugging Face Spaces Gradio App — Aaahhh Fonts Vibe (Sound of Font v3.0.0) & OCR Clarity Studio.

Works both inside the AJ-Series-Fonts repository (using full `sound_of_font` package) and 100%
standalone when deployed directly to a Hugging Face Space directory.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if (ROOT / "sound_of_font").is_dir() and str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from sound_of_font import LANGUAGES, SoundOfFontEngine  # type: ignore[import-not-found]
except Exception:
    LANGUAGES = {
        "en": "English", "ta": "Tamil (தமிழ்)", "ta-sen": "Sen Tamil (செந்தமிழ்)",
        "hi": "Hindi (हिन्दी)", "hi-prathmic": "Prathmic Hindi", "te": "Telugu (తెలుగు)",
        "ml": "Malayalam (മലയാളം)", "kn": "Kannada (ಕನ್ನಡ)", "bn": "Bengali (বাংলা)",
        "mr": "Marathi (मराठी)", "pa": "Punjabi (ਪੰਜਾਬੀ)", "ar": "Arabic (العربية)",
        "ur": "Urdu (اردو)", "sa": "Sanskrit (संस्कृतम्)", "ja": "Japanese (日本語)",
        "ru": "Russian (Русский)", "es": "Spanish (Español)", "fr": "French (Français)",
        "de": "German (Deutsch)", "ms": "Bahasa Melayu", "zh": "Chinese (中文)",
        "th": "Thai (ไทย)", "am": "Amharic (አማርኛ)", "ko": "Korean (한국어)",
    }

    _FALLBACK_WORDS: dict[str, dict[str, str]] = {
        "ta": {"vanakkam": "வணக்கம்", "vanakam": "வணக்கம்", "1u": "ஒன்று", "onnu": "ஒன்று", "ondru": "ஒன்று", "nandri": "நன்றி", "vinnappam": "விண்ணப்பம்", "panivudan": "பணிவுடன்", "india": "இந்தியா"},
        "ta-sen": {"vanakkam": "வணக்கம்", "1u": "ஒன்று", "nandri": "நன்றி", "vinnappam": "விண்ணப்பம்"},
        "hi": {"namaste": "नमस्ते", "namaskar": "नमस्कार", "dhanyavad": "धन्यवाद", "bharat": "भारत", "1u": "एक"},
        "hi-prathmic": {"namaste": "नमस्ते", "namaskar": "नमस्कार", "1u": "एक"},
        "te": {"namaskaram": "నమస్కారం", "dhanyavadalu": "ధన్యవాదాలు", "1u": "ఒకటి"},
        "ml": {"namaskaram": "നമസ്കാരം", "nanni": "നന്ദി", "sar": "സർ,", "1u": "ഒന്ന്"},
        "kn": {"namaskara": "ನಮಸ್ಕಾರ", "dhanyavadagalu": "ಧన్యವಾದಗಳು", "1u": "ಒಂದು"},
        "bn": {"nomoshkar": "নমস্কার", "nomoskar": "নমস্কার", "namaskar": "নমস্কার", "1u": "এক"},
        "mr": {"namaskar": "नमस्कार", "dhanyavad": "धन्यवाद", "1u": "एक"},
        "pa": {"satsriakal": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "dhannvad": "ਧੰਨਵਾਦ", "1u": "ਇੱਕ"},
        "ar": {"salam": "سلام", "marhaba": "مرحبا", "shukran": "شكرا", "1u": "واحد"},
        "ur": {"salam": "سلام", "adab": "آداب", "shukriya": "شکریہ", "1u": "ایک"},
        "sa": {"namaste": "नमस्ते", "namah": "नमः", "1u": "एकम्"},
        "ja": {"konnichiwa": "こんにちは", "arigatou": "ありがとう", "1u": "ひとつ"},
        "ru": {"privet": "привет", "spasibo": "спасибо", "1u": "один"},
        "es": {"hola": "hola", "gracias": "gracias", "manana": "mañana", "1u": "uno"},
        "fr": {"bonjour": "bonjour", "merci": "merci", "coeur": "cœur", "1u": "un"},
        "de": {"hallo": "hallo", "danke": "danke", "fur": "für", "1u": "eins"},
        "ms": {"selamat": "selamat", "terimakasih": "terima kasih", "1u": "satu"},
        "zh": {"nihao": "你好", "ni": "你", "hao": "好", "wo": "我", "xiexie": "谢谢", "bukeqi": "不客气", "zaijian": "再见", "1u": "一"},
        "th": {"sawatdee": "สวัสดี", "khobkhun": "ขอบคุณ", "1u": "หนึ่ง"},
        "am": {"selam": "ሰላም", "sira": "ሥራ", "alem": "ዓለም", "1u": "አንድ"},
        "ko": {"annyeonghaseyo": "안녕하세요", "gamsahabnida": "감사합니다", "1u": "하나"},
    }

    @dataclass
    class _InlineRes:
        category: str | None
        inline_ghost_completion: str
        next_words: list[str]

    @dataclass
    class _CommitRes:
        committed_word: str
        text: str

    class SoundOfFontEngine:  # type: ignore[no-redef]
        def __init__(self, default_language: str = "ta") -> None:
            self.default_language = default_language

        def convert_token(self, token: str, lang: str = "ta") -> str:
            if not token or lang == "en" or token.isdigit():
                return token
            if re.match(r"^(?:Rs\.?|INR|USD|RM|No\.?|[₹$€£¥])\d", token, re.I):
                return token
            return _FALLBACK_WORDS.get(lang, {}).get(token.lower(), token)

        def suggest_inline(self, heading: str, prior_text: str, token: str, lang: str = "ta") -> _InlineRes:
            ctx = f"{heading} {prior_text}".lower()
            cat = "leave_letter" if any(k in ctx for k in ("leave", "permission", "application", "request")) else ("invoice" if "invoice" in ctx else None)
            conv = self.convert_token(token, lang)
            return _InlineRes(category=cat, inline_ghost_completion=conv if conv != token else "", next_words=[])

        def on_space_commit(self, heading: str, prior_text: str, token: str, lang: str = "ta") -> _CommitRes:
            word = self.convert_token(token, lang)
            joined = f"{prior_text.rstrip()} {word} ".lstrip()
            return _CommitRes(committed_word=word, text=joined)

        def auto_correct_sentence(self, text: str, lang: str = "ta") -> str:
            return text.strip()


ENGINE = SoundOfFontEngine("ta")


def run_sound_of_font(heading: str, prior_text: str, current_token: str, lang: str) -> dict:
    inline = ENGINE.suggest_inline(heading, prior_text, current_token, lang)
    committed = ENGINE.on_space_commit(heading, prior_text, current_token, lang)
    corrected = ENGINE.auto_correct_sentence(committed.text.strip(), lang)
    return {
        "language": LANGUAGES.get(lang, lang),
        "category": inline.category,
        "converted_token": ENGINE.convert_token(current_token, lang),
        "committed_word_on_space": committed.committed_word,
        "inline_ghost_completion": inline.inline_ghost_completion,
        "next_words": inline.next_words,
        "auto_corrected_sentence": corrected,
    }


def create_gradio_demo():
    import gradio as gr  # type: ignore[import-not-found]

    with gr.Blocks(title="Aaahhh Fonts Vibe — Sound of Font (v3.0.0)") as demo:
        gr.Markdown("# Aaahhh Fonts Vibe (`v3.0.0`) — Sound of Font Smart Phonetic & Context Studio")
        with gr.Row():
            lang = gr.Dropdown(choices=list(LANGUAGES.keys()), value="ta", label="Target Language (24 Languages)")
            heading = gr.Textbox(value="Leave Letter", label="Document Heading")
        prior = gr.Textbox(value="", label="Prior Sentence Context")
        token = gr.Textbox(value="vanakkam", label="Current Keystroke Token (e.g. vanakkam, 1u, Rs 1u)")
        out = gr.JSON(label="Sound of Font Output")
        btn = gr.Button("Convert & Suggest")
        btn.click(run_sound_of_font, inputs=[heading, prior, token, lang], outputs=out)
    return demo


if __name__ == "__main__":
    create_gradio_demo().launch()
