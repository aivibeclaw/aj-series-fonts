# AJ Series & Aaahhh Fonts Vibe — SDK Bindings (`v3.1.0`)

Zero-dependency, secret-free source files. Copy the one you need into your project. They make no network calls and write nothing; they build strings and expose catalog data.

| Language | File | Minimum |
|---|---|---|
| Python | [`python/aj_fonts_sdk.py`](python/aj_fonts_sdk.py) | 3.8 |
| TypeScript | [`typescript/aj-fonts-sdk.ts`](typescript/aj-fonts-sdk.ts) | ES2019 |
| Swift | [`swift/AJFontsSDK.swift`](swift/AJFontsSDK.swift) | 5.5 |
| Kotlin | [`kotlin/AJFontsSDK.kt`](kotlin/AJFontsSDK.kt) | 1.6 |
| Rust | [`rust/lib.rs`](rust/lib.rs) | 2021 edition |
| Go | [`go/ajfonts.go`](go/ajfonts.go) | 1.18 |
| C# | [`csharp/AJFontsSDK.cs`](csharp/AJFontsSDK.cs) | C# 9 |
| Java | [`java/AJFontsSDK.java`](java/AJFontsSDK.java) | 17 |
| PHP | [`php/AJFontsSDK.php`](php/AJFontsSDK.php) | 8.0 |
| Ruby | [`ruby/aj_fonts_sdk.rb`](ruby/aj_fonts_sdk.rb) | 3.0 |
| SQL | [`sql/aj_fonts_catalog.sql`](sql/aj_fonts_catalog.sql) | SQLite 3 / PostgreSQL |

## What They Provide

- Registry of the 5 families (27 styles): AJ Sahasvi (H1), AJ Shresti (sub-headings and OS default), AJ Talin (script), AJ Anushya (body), Aaahhh Fonts Vibe (Sound of Font).
- File name, URL, font stack and `@font-face` builders.
- `font-feature-settings` builders, including `ss06`–`ss18` (effective in Aaahhh Fonts Vibe only).
- OCR disambiguation constants.

The SQL file provides the same data as tables and a `@font-face` view. The private Sound of Font runtime, lexicons and heuristics are not included.

## Font Base URL

Each file has one slot marked `/* PLACEHOLDER: Configure your CDN/local font base URL here */`. It defaults to `https://fonts.aivibe.cloud/fonts`; change it to self-host unmodified files.

## Example

```python
from aj_fonts_sdk import font_face_css, sound_feature_settings

print(font_face_css("AJ Sahasvi", 800))
print(sound_feature_settings("ta"))   # "ss06" 1, "calt" 1
```

Install the fonts: https://fonts.aivibe.cloud/install

## Licence

`LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1`, provided "as is" without warranty. Copyright (c) 2026 Aravind Jayamohan, India. See the repository `LICENSE.md`.
