# AJ Series (`v3.1.0`) — Font Benchmark & Design Responses

**Prepared for:** Aravind Jayamohan, India (`@ajaitech`)
**Scope:** widely adopted typefaces per script, commonly reported pain points, and the AJ Series design response. The comparisons are qualitative design research, not measured test results.

## 1. Benchmark Matrix

| Script / domain | Widely used | Why adopted | Reported pain points | AJ Series design response |
|---|---|---|---|---|
| Latin UI | Inter, SF Pro, Roboto | Tall x-height, tabular figures | Generic look, `I/l` ambiguity, platform licence limits | Distinct silhouettes, disambiguated `0/o/O`, `I/l/1`, tabular numerals, `ss02` |
| Titling | Cinzel, Trajan, Copperplate, Optima | Monumental authority | Overuse; hairlines vanish when small | AJ Sahasvi: asymmetric canopy and exit foot, no hairlines, `516` small-caps |
| European and Vietnamese Latin | Inter, IBM Plex, Noto Sans | Broad coverage | Locale spacing and diacritic collisions | `locl` rules and stacked Vietnamese diacritics |
| Devanagari | Noto Sans Devanagari, Poppins, Hind, Mukta | Fallback coverage, UI clarity | Rigid geometry, reph and matra collisions | Continuous headline, conjuncts, collision-aware matras |
| Tamil | Noto Sans Tamil, Hind Madurai, Mukta Malar | Balance and reach | Boxy terminals, cramped vowel signs | Rounded bowls, generous uyirmei clearance |
| Telugu | Noto Sans Telugu, Hind Guntur | Coverage | Loops fill in at heavy weights; clipping | Open loop counters, balanced vertical metrics |
| Malayalam, Kannada, Gurmukhi | Noto Sans families | System availability | Dense forms at small sizes | Native letterforms in all 5 families |
| Bengali | Noto Sans Bengali, Hind Siliguri | Ubiquity | Missing structural knots, crowded vowels | Knots preserved, matra clearance |
| Arabic and Urdu | IBM Plex Arabic, Cairo, Noto | Dashboard and mobile use | Boxy forms, mark overlap | Right-to-left joining, mark positioning |
| Cyrillic | Inter, Roboto, PT Sans | Coverage | Latin-first proportions | Native Cyrillic matched to each family |
| Japanese | BIZ UDPGothic, Hiragino, Noto Sans JP | Universal-design clarity | Large payloads, thin rendering | Native rounded kana; Kanji outside the core set uses a fallback |
| Korean | Pretendard, Noto Sans KR | Hangul and Latin harmony | Large payloads | 2,350 syllables from original jamo masters |
| Chinese | PingFang SC, HarmonyOS Sans, Noto Sans SC | Open apertures | Large files, ecosystem tie-in | Native core Han set with fallback for the rest |
| Thai and Ethiopic | Noto, system fonts | Availability | Tone stacking; few design choices | Native glyphs and mark stacking |

## 2. Colour Font Compatibility

AJ Series ships `COLRv1` and `COLRv0` with `CPAL` and OpenType-SVG, plus monochrome outlines. Applications pick the richest format they support and otherwise fall back to outlines. Verify design tools and PDF pipelines before relying on colour output.

## 3. Currency and Keystrokes

- Native currency symbols include Saudi Riyal (`U+20C1`) and UAE Dirham (`U+20C3`) with `₹ $ € £ ¥ ₩ ₿ ฿ ₫ ₺ ₽ ₴ ₪ ₦ ₱ ₵ ₡ ₸ ₼ ₾ ₮ ₭ ₨ ﷼ ¢ ¤`.
- `ss05` turns `:inr:`, `:eur:`, `:sar:`, `:aed:`, `:ok:`, `:ai:` and similar into symbols.
- Native input maps are in [`keymaps/`](./keymaps/README.md).

Install: https://fonts.aivibe.cloud/install
