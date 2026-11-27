"""Hugging Face Spaces Gradio App — AJ Series & Aaahhh Fonts Vibe (v3.1.0) Specimen & OpenType Studio.

Standalone Gradio demo showcasing the 5 canonical AJ Series & Aaahhh Fonts Vibe families,
OpenType stylistic sets (`ss06`–`ss18`), and inline `:lang:` phonetic shaping triggers.
Core Sound-of-Font phonetic/lexicon engine source is withheld from public distribution.
"""
from __future__ import annotations

# PLACEHOLDER: Override CDN_BASE_URL if self-hosting unmodified AJ Series WOFF2 binaries
CDN_BASE_URL = "https://fonts.aivibe.cloud"

LANGUAGES = {
    "en": ("English", ""),
    "ta": ("Tamil (தமிழ்)", "ss06"),
    "ta-sen": ("Sen Tamil (செந்தமிழ்)", "ss06"),
    "hi": ("Hindi (हिन्दी)", "ss07"),
    "hi-prathmic": ("Prathmic Hindi", "ss07"),
    "te": ("Telugu (తెలుగు)", "ss08"),
    "ml": ("Malayalam (മലയാളം)", "ss09"),
    "kn": ("Kannada (ಕನ್ನಡ)", "ss10"),
    "bn": ("Bengali (বাংলা)", "ss11"),
    "mr": ("Marathi (मराठी)", "ss07"),
    "pa": ("Punjabi (ਪੰਜਾਬੀ)", "ss12"),
    "ar": ("Arabic (العربية)", "ss13"),
    "ur": ("Urdu (اردو)", "ss13"),
    "sa": ("Sanskrit (संस्कृतम्)", "ss07"),
    "ja": ("Japanese (日本語)", "ss14"),
    "ru": ("Russian (Русский)", "ss15"),
    "es": ("Spanish (Español)", ""),
    "fr": ("French (Français)", ""),
    "de": ("German (Deutsch)", ""),
    "ms": ("Bahasa Melayu", ""),
    "zh": ("Chinese (中文)", "ss16"),
    "ko": ("Korean (한국어)", ""),
    "th": ("Thai (ไทย)", "ss17"),
    "am": ("Amharic (አማርኛ)", "ss18"),
    "vi": ("Vietnamese (Tiếng Việt)", ""),
}


def render_specimen_html(sample_text: str, lang: str, weight: int) -> str:
    _label, ss = LANGUAGES.get(lang, ("English", ""))
    ffs = f'"calt" 1, "kern" 1, "{ss}" 1' if ss else '"calt" 1, "kern" 1'
    rtl = 'dir="rtl"' if lang in ("ar", "ur") else 'dir="ltr"'
    safe = (
        sample_text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        f'<link rel="stylesheet" href="{CDN_BASE_URL}/css/index.css">'
        f'<div {rtl} style="padding:20px;border-radius:12px;background:#faf8f4;color:#141b2d;'
        f"font-family:'Aaahhh Fonts Vibe','AJ Anushya',sans-serif;font-weight:{int(weight)};"
        f'font-size:32px;line-height:1.6;font-feature-settings:{ffs};">{safe}</div>'
    )


def create_gradio_demo():
    import gradio as gr  # type: ignore[import-not-found]

    with gr.Blocks(title="AJ Series & Aaahhh Fonts Vibe (v3.1.0)") as demo:
        gr.Markdown("# AJ Series & Aaahhh Fonts Vibe (`v3.1.0`) — OpenType & 3D Press Specimen Studio")
        with gr.Row():
            lang = gr.Dropdown(choices=list(LANGUAGES.keys()), value="ta", label="Locale (25 Locales)")
            weight = gr.Dropdown(choices=[400, 600, 800], value=600, label="Font Weight")
        sample = gr.Textbox(value=":ta:vanakkam · 1u · Rs1,250 · தமிழ் எழுத்து", label="Specimen / Trigger Input")
        out = gr.HTML()
        btn = gr.Button("Render Specimen", variant="primary")
        btn.click(render_specimen_html, inputs=[sample, lang, weight], outputs=[out])
    return demo


if __name__ == "__main__":
    create_gradio_demo().launch()
