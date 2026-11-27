# AJ Series & Aaahhh Fonts Vibe (`v3.1.0`)

**5 canonical families · 27 styles · 108 binaries · 25 languages · 14 native non-Latin world scripts plus Latin**

Default 3D mild-gradient press (`COLRv1` + `COLRv0` + `CPAL` + OpenType-SVG), low-resolution and OCR-oriented disambiguation, and the Sound of Font phonetic typeface.

- **Exclusive, non-transferable copyright:** Aravind Jayamohan, India (`@ajaitech`)
- **Authorized Enterprise Licensees:** Aivibe Software Services Private Limited · AjAir Tech Mobility LLP · QRaise Structures
- **Licence:** [`LICENSE.md`](LICENSE.md) (`LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1`). Free unmodified use, strictly "as is". No modification, rebranding or standalone resale.
- **Websites:** https://fonts.aivibe.cloud · https://www.aivibe.in

## Install

| Platform | Command or download |
|---|---|
| All platforms | https://fonts.aivibe.cloud/install |
| macOS | `curl -fsSL https://fonts.aivibe.cloud/install/macos.sh \| bash` |
| Linux | `curl -fsSL https://fonts.aivibe.cloud/install/linux.sh \| sudo bash` |
| Windows (Administrator PowerShell) | `irm https://fonts.aivibe.cloud/install/windows.ps1 \| iex` |
| macOS package | https://fonts.aivibe.cloud/downloads/AJ-Series-Fonts-v3.1.0-macOS.pkg |
| Windows archive | https://fonts.aivibe.cloud/downloads/AJ-Series-Fonts-v3.1.0-Windows-Core.zip |
| iOS / iPadOS profile | https://fonts.aivibe.cloud/downloads/AJ-Series-Fonts-v3.1.0.mobileconfig |
| Debian / Ubuntu | https://fonts.aivibe.cloud/downloads/fonts-aj-series_3.1.0_all.deb |
| Android system module | https://fonts.aivibe.cloud/downloads/AJ-Series-Fonts-AOSP-SystemModule-v3.1.0.zip |
| Release assets | `https://github.com/aivibe-org/aj-series-fonts/releases/download/v3.1.0/<file>` |

Homebrew:

```bash
brew tap aivibe-org/fonts https://github.com/aivibe-org/homebrew-fonts
brew install --cask font-aj-series
```

Web:

```css
@import url("https://fonts.aivibe.cloud/css/aj-series.css");
body { font-family: "AJ Anushya", system-ui, sans-serif; }
h1   { font-family: "AJ Sahasvi", serif; font-weight: 800; }
```

Design tokens: [`tokens/`](tokens/). Language bindings: [`distributions/sdks/`](distributions/sdks/README.md).

## Families

| # | Family | Level | Styles | Character |
|---|---|---|---|---|
| 01 | **AJ Sahasvi** | Level 1 Headers (H1) | `400/600/800` (3) | Sculpted Horizon small-caps |
| 02 | **AJ Shresti** | Level 2 Sub-Headings & OS Default | `400/600/800` + Italics (6) | Rounded geometric sans |
| 03 | **AJ Talin** | Level 3 Script | `400/600/800` + Italics (6) | Connected running script (`calt`) |
| 04 | **AJ Anushya** | Body Reading | `400/600/800` + Italics (6) | Zero-stub reading sans |
| 05 | **Aaahhh Fonts Vibe** | Sound of Font | `400/600/800` + Italics (6) | Phonetic shaping typeface |

## Sound of Font

`Aaahhh Fonts Vibe` turns romanized words typed on an English keyboard into regional scripts. Plain English is left unchanged until you opt in.

- Inline triggers: `:ta:vanakkam` → வணக்கம், `:hi:namaste` → नमस्ते
- Per-language stylistic sets:

| Set | Language | Set | Language |
|---|---|---|---|
| `ss06` | Tamil | `ss13` | Arabic / Urdu |
| `ss07` | Hindi | `ss14` | Japanese |
| `ss08` | Telugu | `ss15` | Russian |
| `ss09` | Malayalam | `ss16` | Chinese |
| `ss10` | Kannada | `ss17` | Thai |
| `ss11` | Bengali | `ss18` | Amharic |
| `ss12` | Punjabi | | |

Font-level shaping covers a fixed word list. Numbers and currency such as `1` and `Rs1` stay as typed.

## Languages and Scripts

**25 languages:** `en`, `ta`, `ta-sen`, `hi`, `hi-prathmic`, `te`, `ml`, `kn`, `bn`, `mr`, `pa`, `ar`, `ur`, `sa`, `ja`, `ru`, `es`, `fr`, `de`, `ms`, `zh`, `ko`, `th`, `am`, `vi`.

**14 native non-Latin scripts:** Tamil, Devanagari, Telugu, Malayalam, Kannada, Bengali, Gurmukhi, Perso-Arabic, Cyrillic, Japanese Kana, Hangul, Han (core set), Thai, Ethiopic. See [`MULTILINGUAL_ARCHITECTURE.md`](MULTILINGUAL_ARCHITECTURE.md).

## Documentation

[Accessibility & agentic](ACCESSIBILITY_AND_AGENTIC.md) · [Architecture](ARCHITECTURE_MASTER_PLAN_V3.md) · [Publishing playbook](GLOBAL_SYSTEM_FONT_PUBLISHING_PLAYBOOK.md) · [Trust](TRUST_NOTARIZATION_AND_PUBLISHING.md) · [Research](RESEARCH_BENCHMARK_AND_SOLUTIONS.md) · [Keymaps](keymaps/README.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md)
