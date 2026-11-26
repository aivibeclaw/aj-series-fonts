# AJ Series & Aaahhh Fonts Vibe Enterprise Typefaces (`v3.0.0`)

> **100% Handcrafted Enterprise Superfamily — 5 Canonical Families (27 Styles · 108 Binaries · 27 UFO3 Masters) · Default 3D Pressed with Mild Gradient Effect (`COLRv1` + `COLRv0` + `CPAL` + `OpenType-SVG`) · "Sound of Font" Smart Phonetic Multilingual Engine · 25+ Native Languages (14 World Scripts) · Extreme Low-Res OCR Clarity · 28 Global Currencies**

- **Exclusive Intellectual Property & Copyright Owner**: **ARAVIND JAYAMOHAN**, India (`aravind.j.naidu@gmail.com` · `aravind@aivibe.in` · `aravindjayamohan@ymail.com`) — **100% Full Rights Exclusively Owned & Retained**.
- **Authorized Enterprise Publishers & White-Label Licensees**:
  1. **Aivibe Software Services Private Limited**, Chennai, India (`github.com/aivibe-org` · `github.com/aivibeclaw`)
  2. **AjAir Tech Mobility LLP**, India (`github.com/ajaitech`)
  3. **QRaise Structures**, India
- **Ecosystem Application Grant**: Free unmodified application, web, OS, AI/OCR, database, CMS, FinTech & ERP embedding under [`LICENSE.md`](LICENSE.md) & [`AIVIBE_ECOSYSTEM_FONT_LICENSE.md`](AIVIBE_ECOSYSTEM_FONT_LICENSE.md) (no glyph/copyright modification; no standalone commercial font resale).

---

## 1. The 5 Canonical Typeface Families (27 Unified Styles)

| # | Family | Role | Styles | Handcrafted Visual & Smart DNA |
|---|---|---|---|---|
| 01 | **AJ Sahasvi** | Level 1 Headers (`H1` / Display) | `400 / 600 / 800` (3) | 1-of-1 **"Sculpted Horizon"** Royal Small-Caps (`720` CAP / `516` Small-Cap), Default 3D Mild-Gradient Press |
| 02 | **AJ Shresti** | Level 2 Sub-Headings & Active OS Default | `400 / 600 / 800` + Italics (6) | Architectural rounded geometric sans, curved-foot `t`, zero-stub `r`, dramatic ExtraBold, Default 3D Mild-Gradient Press |
| 03 | **AJ Talin** | Level 3 Editorial & Signatures | `400 / 600 / 800` (`0°`) + `11°` Italics (6) | Point-by-point handcrafted running script (`OpenType calt`, teardrop `a` vs crown-bridge `o`), Default 3D Mild-Gradient Press |
| 04 | **AJ Anushya** | Body Text & `9pt–13pt` Micro-Clarity | `400 / 600 / 800` + Italics (6) | Humanist zero-stub reading sans, WCAG AAA & low-DPI OCR confidence, Default 3D Mild-Gradient Press |
| 05 | **Aaahhh Fonts Vibe** | **"Sound of Font"** — Smart Phonetic Multilingual Typeface | `400 / 600 / 800` + Italics (6) | Built on **AJ Anushya** zero-stub clarity + **Acoustic Resonance Wave** masters, embedded OpenType `GSUB` phonetic shaping (`ss06`–`ss15` + `:ta:`/`:hi:` triggers) + Cross-Platform Smart Phonetic, Spell/Grammar, OS-Merged Lexicon & Context Inline Ghost-Text Engine ([`sound_of_font/`](sound_of_font/)), Default 3D Mild-Gradient Press |

---

## 2. "Sound of Font" (`Aaahhh Fonts Vibe`) Highlights

- **English Physical Keyboard → 24+ Regional Languages by Natural Sound**:
  - Defaults cleanly to **English** (or closest OS/app locale) with zero unwanted conversions.
  - **Smart Numeric & Currency Sound Disambiguation**:
    - Standalone `"1"` stays `"1"`; `"Rs1"` / `"Rs.1"` / `"₹1"` stays `"Rs1"` / `"Rs.1"` / `"₹1"`.
    - Phonetic sound tokens `"1u"`, `"onnu"`, and `"ondru"` all convert seamlessly to Tamil **`ஒன்று`** (`2u`/`rendu`/`irandu` → **`இரண்டு`**, `vanakkam`/`vanakam` → **`வணக்கம்`**).
- **Automated Phonetic Spellcheck, Grammar Refinement & Context Next-Word Inline Helptext**:
  - Understands document headings and prior sentences (e.g., **Leave Letter / விண்ணப்பம் / छुट्टी का आवेदन**, FinTech Invoice, Official Email) — from the very first body letter typed, generous inline ghost helptext suggests both the closest sound word and next-word sentence completions, committing smoothly on **Space** in `<0.5ms`.
  - Preloaded 24-language lexicon merges non-blockingly with OS/platform dictionaries (`/usr/share/dict/words` / browser custom words).
- **Zero-Overhead Background AI Metadata Spark Indexer**:
  - Exposes structured metrics, script tags, and OCR disambiguation guarantees via [`agentic/aj-series.manifest.json`](agentic/aj-series.manifest.json) and OpenType `meta` with `0.0ms` font-switching overhead.

---

## 3. 25+ Native Languages & 14 World Script Suites Built Into Every Binary

Every style across all 5 families (`4,300` Unicode codepoints / `4,625+` base glyphs per style) includes handcrafted outlines + Default 3D Mild-Gradient Press for:
- **Latin (Pan-European, Vietnamese & Singapore/Malaysia)**: English (`en`, `en-IN`, `en-SG`), Spanish (`es`), French (`fr`), German (`de`), Bahasa Melayu (`ms-MY`, `ms-SG`), Italian, Portuguese, Polish, Turkish, Dutch, Nordic, Vietnamese (`vi`).
- **Indic & Classical Registers**: Tamil & **Sen Tamil** (`ta`), Hindi & **Prathmic Hindi** (`hi`), Marathi (`mr`), **Sanskrit** (`sa`), Telugu (`te`), **Malayalam** (`ml`), **Kannada** (`kn`), Bengali (`bn`), **Punjabi Gurmukhi** (`pa`).
- **Middle East & Perso-Arabic RTL**: Arabic (`ar`) & **Urdu** (`ur` — `ٹ پ چ ڈ ڑ ژ ک گ ں ھ ہ ی ے ۔ ۰–۹`).
- **Eurasian & East Asian**: **Russian & Slavic Cyrillic** (`ru`), Japanese Hiragana/Katakana (`ja`), Korean Hangul (`ko` — 2,350 KS X 1001 syllables), **Chinese & SG/MY Mandarin Core** (`zh`).
- **2 Underserved World Languages**: **Thai** (`th` with `mark`+`mkmk` tone stacking) and **Ethiopic Ge'ez / Amharic** (`am`).

---

## 4. Verification, Trust & Global Platform Ecosystem

```bash
./trust/verify_trust.sh
./.venv/bin/python -m unittest discover -s tests -v
```

- **Certification Report**: [`trust/CERTIFICATION_REPORT.md`](trust/CERTIFICATION_REPORT.md) (`ots-sanitize` `108/108 PASS`, FontBakery `0 FAIL`)
- **Cloud Marketplaces & Leading Ecosystem Integrations**: [`distributions/cloud-marketplaces/`](distributions/cloud-marketplaces/README.md) (AWS Marketplace, Google Workspace Marketplace) · [`distributions/ecosystem-platforms/`](distributions/ecosystem-platforms/README.md) (NVIDIA Omniverse/NIM, Hugging Face, Intel OpenVINO, Microsoft, Red Hat, Debian, Ubuntu, Supabase, Redis, PostgreSQL, Android, Chrome, WordPress, Wix, FinTech & Enterprise ERP).
