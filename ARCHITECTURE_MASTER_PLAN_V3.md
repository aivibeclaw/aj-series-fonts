# AJ Series & Aaahhh Fonts Vibe (`v3.1.0`) — Master Architecture

**Exclusive, non-transferable copyright:** Aravind Jayamohan, India (`@ajaitech`)
**Authorized Enterprise Licensees:** Aivibe Software Services Private Limited · AjAir Tech Mobility LLP · QRaise Structures

## 1. Canonical Families (27 Styles · 108 Binaries)

| # | Family | Slug | Styles | Level / Design |
|---|---|---|---|---|
| 01 | **AJ Sahasvi** | `aj-sahasvi` | `400/600/800` (3) | Level 1 Headers (H1). Sculpted Horizon small-caps (`720` cap / `516` small-cap) |
| 02 | **AJ Shresti** | `aj-shresti` | `400/600/800` + Italics (6) | Level 2 Sub-Headings & OS Default. Rounded geometric sans |
| 03 | **AJ Talin** | `aj-talin` | `400/600/800` + Italics (6) | Level 3 Script. Connected running script |
| 04 | **AJ Anushya** | `aj-anushya` | `400/600/800` + Italics (6) | Body Reading. Zero-stub sans, `556` x-height |
| 05 | **Aaahhh Fonts Vibe** | `aaahhh-fonts-vibe` | `400/600/800` + Italics (6) | Sound of Font. Acoustic Resonance letterforms |

Each style ships as OTF, TTF, WOFF and WOFF2.

## 2. Font Design System

- **Weights:** `400`, `600`, `800`, visibly distinct in every script with open counters.
- **Colour:** default 3D mild-gradient press using `COLRv1`, `COLRv0`, `CPAL` (foreground-colour aware) and OpenType-SVG, with outline fallback.
- **Clarity:** `gasp` grid-fitting, open apertures, `0/o/O`, `I/l/1`, `a/b/6`, `rn/m`, `cl/d` disambiguation.
- **Languages:** 25 languages; Latin plus 14 native non-Latin scripts. See [`MULTILINGUAL_ARCHITECTURE.md`](./MULTILINGUAL_ARCHITECTURE.md).
- **Embedding:** `fsType = 0`.

## 3. Sound of Font

- **Font layer:** OpenType `GSUB` in `Aaahhh Fonts Vibe`: `:lang:word` triggers and `ss06`–`ss18`, with numeric and currency guards.
- **Runtime layer:** a separate smart-typing runtime. Its lexicons and heuristics are not part of the public bindings.

## 4. Integration Surfaces

| Surface | Location |
|---|---|
| Web CDN | `https://fonts.aivibe.cloud/fonts/`, `https://fonts.aivibe.cloud/css/aj-series.css` |
| Design tokens | `tokens/` |
| Keymaps | `keymaps/` |
| Agentic contracts | `agentic/` |
| Language SDKs | `distributions/sdks/` |
| Installers | `https://fonts.aivibe.cloud/install` |
| Releases | `https://github.com/aivibe-org/aj-series-fonts/releases/download/v3.1.0/<file>` |

## 5. Licensing and Public Repositories

- `LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1`: free unmodified use "as is"; no modification, rebranding or third-party standalone resale.
- Public repositories: `aj-series-fonts`, `aaahhh-fonts-vibe`, `homebrew-fonts`, `aj-fonts-ai-vision`, `aj-fonts-data-erp`, `aj-fonts-web-os`.
- Public repositories carry no secrets, signing identifiers, personal contact data or local paths. Build sources are held privately.
