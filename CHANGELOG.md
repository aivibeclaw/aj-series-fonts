# Changelog — AJ Series & Aaahhh Fonts Vibe

Copyright (c) 2026 Aravind Jayamohan, India. Entries below `3.0.0` describe superseded releases and are kept as history.

## [3.1.0] — 2026-11-27
### Licensing
- New identifier `LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1`.
- Added the strict non-rebrandability and read-only metadata lock clause.
- Copyright stated as exclusive and non-transferable to Aravind Jayamohan, India; "as is", no-warranty terms made explicit.
- `CLA.md` now assigns contribution copyright to the Owner.

### Added
- Public zero-dependency SDK bindings in `distributions/sdks/`: Python, TypeScript, Swift, Kotlin, Rust, Go, C#, Java, PHP and SQL.
- `agentic/mcp-typography-protocol.json`: read-only MCP / JSON-RPC font capability and AI Spark index schema.
- Level-based hierarchy and 25 locales in design tokens.

### Changed
- Tokens load fonts from `https://fonts.aivibe.cloud/fonts/` instead of local build paths.
- Corrected the token hierarchy: AJ Sahasvi = H1, AJ Shresti = sub-headings and OS default, AJ Talin = level 3 script, AJ Anushya = body.
- Documentation, keymaps, manifests and organisation profiles updated to `v3.1.0`, with published install links and `ss06`–`ss18`.

### Privacy
- Removed personal email addresses, signing identifiers and local paths from documentation, tokens, keymaps and manifests.

## [3.0.0] — 2026-11-26
### Added
- Fifth family, **Aaahhh Fonts Vibe** ("Sound of Font"), with OpenType phonetic shaping, giving 5 families, 27 styles and 108 binaries.
- 14 native non-Latin world scripts alongside Latin inside the binaries, replacing companion-font stacks.
- Default 3D mild-gradient press (`COLRv1` + `COLRv0` + `CPAL` + OpenType-SVG) across all styles.
- SDK, licensing and ecosystem integration kits.

### Fixed
- Urdu right-to-left joining, Devanagari conjuncts, Thai mark centring, Malayalam, Kannada and Tamil glyphs.
- `OS/2` code page ranges; CoreText `COLRv1` alpha and OTF SVG gradient rendering.
- Double-storey AJ Shresti `a`; low-resolution `I`/`1` and `rn`/`m` disambiguation; dark-mode rim on colour glyphs.

## [2.1.0] — 2026-11-23
### Fixed & Upgraded — True 4-Family Unique Styling Across ALL Languages + Global System-Font Store Apps
- **True 4-Family Unique Styling Across Every Language & Numerals (`(private-foundry-module)` + Elliptical Calligraphic Pen Engine in `(private-foundry-module)`)**:
  - Every non-Latin script (**Arabic RTL, Devanagari Hindi/Marathi, Tamil, Telugu, Bengali, Japanese Hiragana/Katakana, 2,350-syllable Korean Hangul**) AND all **`0–9` Numerals** now express 4 genuinely distinct architectural personalities matching their Latin families:
    - **`AJ Shresti`**: Bold architectural geometric display (`1.06×` presence, `0.84×` horizontal optical relief).
    - **`AJ Sahasvi`**: 1-of-1 Sculpted Horizon royal luxury (`1.61:1` calligraphic broad-nib vertical/horizontal contrast + asymmetric left-entry crown wing & right-exit baseline horizon foot).
    - **`AJ Anushya`**: Airy zero-stub micro-clarity monoline (`0.78×` stroke weight, widened open counters, zero decorative overhangs).
    - **`AJ Talin`**: Precision straight `0°` upright calligraphic running script (`28°` broad-nib modulation + sweeping circular baseline exit curls).
- **Restored Approved Latin Details**:
  - **`AJ Sahasvi`**: Restored exact Royal Tall-Initial (`720 UPM`) → Small-Caps (`516 UPM`, `71.7%`) visual hierarchy with `1.39:1` contrast (fixing the flattened `548 UPM` drift and Title Case specimens).
  - **`AJ Shresti`**: Restored approved curved-foot lowercase `t` and smooth zero-stub `r` matching `01_AJ_Shresti_Sample.png`.
  - **Tamil & Telugu**: Refined open inner counter proportions for cleaner native legibility across all 4 families.
  - **`LICENSE.md`**: Updated header to `v2.1.0` enumerating all 57 TTF / 156 compiled binaries (`Core`, `3D Press`, `3D Lift`, `KR`).
- **Apple Universal App Store Font Provider + Xcode Cloud + Store Listing (`apps/apple/`, `ci_scripts/`, `TestFlight/`)**:
  - Built & compile-verified Universal SwiftUI App (`in.aivibe.ajseriesfonts`) with `com.apple.developer.user-fonts` (`app-usage`, `system-install`) + `CTFontManagerRegisterFontURLs` (adds all 57 styles directly into iOS/iPadOS `Settings › General › Fonts`) and sandboxed Apple Font Book integration on macOS.
  - Added Xcode Cloud CI scripts (`ci_post_clone.sh`, `ci_pre_xcodebuild.sh`, `ci_post_xcodebuild.sh`), `setup_app_store_connect.py` API script, complete App Store listing metadata, Privacy/Support HTML pages, App Icon, and 6 real HarfBuzz/COLRv0 App Store screenshots.
- **Global System-Font Publishing Packages Across All Platforms (`apps/android/`, `distributions/`, `GLOBAL_SYSTEM_FONT_PUBLISHING_PLAYBOOK.md`)**:
  - **Android**: Jetpack Compose app + official AndroidX Downloadable Fonts `ContentProvider` (`in.aivibe.fonts.ajseries.provider`) + Play Store listing & `1024×500` Feature Graphic + **4 Xiaomi HyperOS `.mtz`**, **4 Huawei HarmonyOS `.hwt`**, **AOSP `/system/fonts/` module `.zip`**, and Samsung/Monotype & OPPO/Vivo foundry partner kits.
  - **Windows**: Microsoft Store MSIX (`AppxManifest.xml` declaring `uap4:Extension Category="windows.sharedFonts"` for all 57 TTFs + `aka.ms/storesupport` allowlist request) + WinGet 1.6 manifests + Microsoft 365 SharePoint Organization Cloud Fonts script.
  - **macOS & Linux**: Re-notarized & stapled macOS `.pkg` (Apple Notary accepted!), Homebrew Cask (`font-aj-series.rb`), real built Debian `.deb` (`fonts-aj-series_2.1.0_all.deb`), RPM `.spec`, Arch AUR `PKGBUILD`, and Google Fonts Dual-Track SIL OFL 1.1 `METADATA.pb` files.

## [2.0.0] — 2026-11-22
### Added — Elite Multi-Script, Native 3D Impressions, Global Currencies & Certified Trust Stack
- **Native OpenType `COLRv0` + `CPAL` (`0xFFFF` Dynamic Color) 3D Impressions**: Compiled **48 native 3D binaries** (`3D Press` Paper-Punched Deboss + `3D Lift` Glossy 3D Elevated) across Regular (400), SemiBold (600), and ExtraBold (800) for all 4 families (`AJ Shresti`, `AJ Sahasvi`, `AJ Anushya`, `AJ Talin`) — working in any user-selected color with zero CSS `text-shadow`.
- **1-of-1 Redesigned `AJ Sahasvi` ("Sculpted Horizon")**: Replaced symmetric slab/Roman flanges with asymmetric directional lead canopies, bottom-right exit anchors, warm `1.30:1` comfort contrast, vaulted `A`/`H` crossbars, curved `R`/`K`/`Q` legs, and elevated `548 UPM` Small-Caps.
- **`AJ Shresti` Optical Comfort Upgrade**: Added `0.90×` horizontal crossbar optical breathing, wider `46°` apertures, and balanced `+12 UPM` round-bowl overshoot.
- **Uniform Equal-Width Slim Numerals (`0–9`)**: Harmonized all 10 digits (including balanced `1`, `4`, `7`) to one slim `426 UPM` tabular box and uniform optical width (`±6 UPM`).
- **28 Global Currencies + Cross-Platform Keystrokes**: Added Unicode 17.0 **Saudi Riyal (`U+20C1`)**, Unicode 18.0 **UAE Dirham (`U+20C3`)**, and 19 additional world currencies + built-in OpenType `ss05` ASCII keystrokes (`:inr:`, `:aed:`, `:sar:`, etc.) + macOS `.keylayout`, Windows `.ahk`, Linux `.XCompose`, and TypeScript SDK.
- **25+ Native Languages & Multi-Script OpenType Shaping**:
  - Added 18 European & Vietnamese Latin languages (`locl` `FRA/DEU/ESP/ITA/PTG/NLD/TRK/ROM/PLK/CAT/VIT`, language-specific `GPOS` spacing, 90+ stacked Vietnamese diacritics, German Capital `ẞ`, smart `Th/ct/st/fj` ligatures).
  - Built 6 native non-Latin CAD script modules directly inside all 4 core families: **Arabic RTL (`arab`)**, **Devanagari Hindi & Marathi (`dev2`)**, **Tamil (`tml2` + Uyirmei-U `psts`)**, **Telugu (`tel2`)**, **Bengali (`bng2` preserving structural knots)**, and **Japanese Hiragana & Katakana**.
  - Built **12 native Korean Hangul companion styles (`AJ*KR`, 2,350 KS X 1001 syllables each)**.
- **Full Digital Trust, QA Certification & 13-Platform Distribution**:
  - Added OpenType `meta` (`dlng`/`slng` BCP-47), `ttfautohint` Windows 96-DPI ClearType hinting, `ots-sanitize` (`156/156 PASS`), FontBakery OpenType certification (`0 FAIL`), GPG signatures, DigiCert RFC 3161 timestamps, SPDX 2.3 SBOM, W3C SRI hashes, Apple Developer ID signed macOS `.pkg`, iOS `.mobileconfig`, Windows/Intune kit, Android Compose module, Linux `.deb` kit, `@aj-series/fonts` npm package, and Dual-Track optional Google Fonts SIL OFL 1.1 Reserved-Name Core pack.

## [1.0.0] — 2026-11-22
- Initial 4-family Latin Extended-A release (`21` styles / `84` binaries + `21` UFO3 masters) with proprietary ownership attribution to Aravind Jayamohan, India.
