# Contributing to AJ Series Fonts & Aaahhh Fonts Vibe ("Sound of Font")

Thank you for contributing to the **Aivibe Open-Ecosystem Typography & Phonetic Intelligence Suite**.

## What You Can Contribute
1. **Phonetic Lexicon & Regional Sound Aliases (`sound_of_font/dictionaries/`)**:
   - Additional romanized sound aliases, dialect variants, and sentence/heading templates across all 24+ supported languages.
2. **Ecosystem & Platform Adapters (`distributions/ecosystem-platforms/`)**:
   - Integration connectors, Docker/Helm manifests, Linux distro specs, WordPress/Wix helpers, Supabase/PostgreSQL/Redis indexing helpers, and FinTech/ERP templates.
3. **Shaper, OCR & Accessibility Diagnostics (`tests/`)**:
   - Reproducible test cases for HarfBuzz, CoreText, DirectWrite, FreeType, low-resolution (`9px–16px`) rasterization, and OCR engines.

## Protected Assets (Read-Only)
- Compiled font binaries (`*.ttf`, `*.otf`, `*.woff`, `*.woff2`), reserved family names (`AJ Sahasvi`, `AJ Shresti`, `AJ Talin`, `AJ Anushya`, `Aaahhh Fonts Vibe`), and glyph outlines remain under the exclusive copyright of **Aravind Jayamohan** (`AIVIBE_ECOSYSTEM_FONT_LICENSE.md`). Pull requests must not alter font names, copyright metadata, or license files.

## Pull Request Checklist
1. Review and agree to [`CLA.md`](./CLA.md).
2. Run the automated verification suite before opening a PR:
   ```bash
   python3 -m unittest discover -s tests -v
   ```
3. Ensure numeric/currency guards (`1`, `Rs1`, `$10`, ISO dates) remain untouched in all `Sound of Font` phonetic tests.
