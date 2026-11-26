# AJ Series — Cross-Platform Smart Keystroke & Global Currency Input Kit

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

## 2. Aaahhh Fonts Vibe ("Sound of Font") Phonetic Keystroke Triggers (`v3.0.0`)
Works natively via OpenType `calt`/`dlig` (`:ta:vanakkam`, `:ta:1u`, `:hi:namaste`, `:ml:namaskaram`, `:kn:namaskara`, `:pa:satsriakal`, `:ru:privet`, `:ja:konnichiwa`), Stylistic Sets `ss06`–`ss15` (with strict `1` / `Rs1` / `Rs.1u` currency & numeric guards), or via `expandAJKeystrokes` + `SoundOfFontEngine` across all 24 languages!

## 3. OS & SDK Companion Files
- **macOS Native Input**: Install [AJ-Series-Global.keylayout](file:///Users/aj/Dev-Apps/AJ-Series-Fonts/keymaps/AJ-Series-Global.keylayout) into `~/Library/Keyboard Layouts/` → Log out/in → Select **AJ Series Global**.
- **Windows Global Hotstrings**: Run [AJ-Series-Windows.ahk](file:///Users/aj/Dev-Apps/AJ-Series-Fonts/keymaps/AJ-Series-Windows.ahk) with AutoHotkey v2.
- **Linux Compose**: Append [AJ-Series-Compose.XCompose](file:///Users/aj/Dev-Apps/AJ-Series-Fonts/keymaps/AJ-Series-Compose.XCompose) to `~/.XCompose`.
- **Web / React / iOS / Android SDK**: Import `expandAJKeystrokes` from [aj-keystrokes.ts](file:///Users/aj/Dev-Apps/AJ-Series-Fonts/keymaps/aj-keystrokes.ts) and `SoundOfFontEngine` from [sound_of_font.ts](file:///Users/aj/Dev-Apps/AJ-Series-Fonts/sound_of_font/engine/sound_of_font.ts).
