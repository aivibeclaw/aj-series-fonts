# AJ Series — Cross-Platform Smart Keystroke & Global Currency Input Kit (`v3.1.0`)

Type all **28 global currencies** (including Unicode 17.0 **Saudi Riyal `U+20C1`** & Unicode 18.0 **UAE Dirham `U+20C3`**), KPI indicators, and agentic UI symbols effortlessly on **every OS & framework**.

## 1. Zero-Install OpenType `ss05` (Built Directly Into Every AJ Font Binary!)
Enable OpenType Stylistic Set 5 (`font-feature-settings: "ss05" 1;` on Web/CSS, Figma, InDesign, Word, macOS, Android, iOS) and simply type plain ASCII:

| Type | Renders | Symbol | Codepoint |
|---|---|---|---|
| `:inr:` | ₹ | Indian Rupee | `U+20B9` |
| `:usd:` | $ | US Dollar | `U+0024` |
| `:eur:` | € | Euro | `U+20AC` |
| `:gbp:` | £ | British Pound | `U+00A3` |
| `:jpy:` | ¥ | Yen / Yuan | `U+00A5` |
| `:krw:` | ₩ | Korean Won | `U+20A9` |
| `:sar:` | ⃁ | Saudi Riyal (2025, Unicode 17.0) | `U+20C1` |
| `:aed:` | ⃃ | UAE Dirham (2025, Unicode 18.0) | `U+20C3` |
| `:btc:` | ₿ | Bitcoin | `U+20BF` |
| `:thb:` / `:vnd:` / `:try:` / `:rub:` | ฿ ₫ ₺ ₽ | Baht / Dong / Lira / Ruble | `U+0E3F` / `20AB` / `20BA` / `20BD` |
| `:php:` / `:ngn:` / `:ils:` / `:uah:` | ₱ ₦ ₪ ₴ | Peso / Naira / Shekel / Hryvnia | `U+20B1` / `20A6` / `20AA` / `20B4` |
| `:ok:` / `:no:` / `:up:` / `:dn:` / `:ai:` / `:star:` / `:cmd:` | ✓ ✕ ▲ ▼ ✦ ★ ⌘ | Enterprise & Agentic UI | `U+2713`..`U+2318` |

## 2. Aaahhh Fonts Vibe ("Sound of Font") Phonetic Triggers
Built into `Aaahhh Fonts Vibe`: inline `calt` / `dlig` triggers (`:ta:vanakkam`, `:ta:1u`, `:hi:namaste`, `:ml:namaskaram`, `:kn:namaskara`, `:pa:satsriakal`, `:ru:privet`, `:ja:konnichiwa`) and whole-word stylistic sets `ss06`–`ss18`. Numbers and currency such as `1` and `Rs1` stay as typed. `expandAJKeystrokes` expands the same triggers into real Unicode text.

## 3. Input Files
- **macOS:** [AJ-Series-Global.keylayout](https://github.com/aivibe-org/aj-series-fonts/blob/v3.1.0/keymaps/AJ-Series-Global.keylayout). Copy into `~/Library/Keyboard Layouts/`, log out and in, then select **AJ Series Global**.
- **Windows:** [AJ-Series-Windows.ahk](https://github.com/aivibe-org/aj-series-fonts/blob/v3.1.0/keymaps/AJ-Series-Windows.ahk). Run with AutoHotkey v2.
- **Linux:** [AJ-Series-Compose.XCompose](https://github.com/aivibe-org/aj-series-fonts/blob/v3.1.0/keymaps/AJ-Series-Compose.XCompose). Append to `~/.XCompose`.
- **Web / React / Electron:** [aj-keystrokes.ts](https://github.com/aivibe-org/aj-series-fonts/blob/v3.1.0/keymaps/aj-keystrokes.ts). Import `expandAJKeystrokes`.

Install the fonts: https://fonts.aivibe.cloud/install

Copyright (c) 2026 Aravind Jayamohan, India. See the repository `LICENSE.md`.
