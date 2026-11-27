# Multilingual Architecture (`v3.1.0`)

All **5 families** (AJ Sahasvi, AJ Shresti, AJ Talin, AJ Anushya, Aaahhh Fonts Vibe; 27 styles) carry **Latin plus 14 native non-Latin scripts inside the font binaries**. No companion font is needed for the coverage listed here.

## 1. Native Scripts

| # | Script | Languages | Notes |
|---|---|---|---|
| — | Latin | `en`, `es`, `fr`, `de`, `ms`, `vi` | Also other European Latin languages; stacked Vietnamese diacritics |
| 1 | Tamil | `ta`, `ta-sen` | Uyirmei shaping |
| 2 | Devanagari | `hi`, `hi-prathmic`, `mr`, `sa` | Conjuncts, reph, i-matra |
| 3 | Telugu | `te` | Open loop counters |
| 4 | Malayalam | `ml` | |
| 5 | Kannada | `kn` | Subjoined forms |
| 6 | Bengali | `bn` | Structural knots preserved |
| 7 | Gurmukhi | `pa` | |
| 8 | Perso-Arabic | `ar`, `ur` | Right-to-left joining |
| 9 | Cyrillic | `ru` | |
| 10 | Japanese Kana | `ja` | Hiragana and Katakana; Kanji outside the Han core set needs a fallback |
| 11 | Hangul | `ko` | 2,350 KS X 1001 syllables |
| 12 | Han | `zh` | Core set, not full Hanzi; use a fallback for other characters |
| 13 | Thai | `th` | Mark and tone stacking |
| 14 | Ethiopic | `am` | Ge'ez syllabary |

**25 languages:** `en`, `ta`, `ta-sen`, `hi`, `hi-prathmic`, `te`, `ml`, `kn`, `bn`, `mr`, `pa`, `ar`, `ur`, `sa`, `ja`, `ru`, `es`, `fr`, `de`, `ms`, `zh`, `ko`, `th`, `am`, `vi`. `ta-sen` and `hi-prathmic` are project labels for registers of `ta` and `hi`, not registered BCP-47 tags.

## 2. Sound of Font (`Aaahhh Fonts Vibe`)

Phonetic shaping is built into `Aaahhh Fonts Vibe` only:

- **Inline triggers** (`calt` / `dlig`): `:ta:vanakkam`, `:hi:namaste`, `:ml:namaskaram`.
- **Stylistic sets:** `ss06` ta, `ss07` hi, `ss08` te, `ss09` ml, `ss10` kn, `ss11` bn, `ss12` pa, `ss13` ar/ur, `ss14` ja, `ss15` ru, `ss16` zh, `ss17` th, `ss18` am.
- Shaping covers a fixed word list and changes display only; stored text stays as typed.
- Enable one language set at a time, because spellings can overlap.

## 3. Web Use

Use [`tokens/multilingual-15lang.css`](./tokens/multilingual-15lang.css) (the filename is kept for compatibility; it covers all 25 languages) and mark content with `lang` and `dir`:

```html
<link rel="stylesheet" href="aj-series.css">
<link rel="stylesheet" href="multilingual-15lang.css">
<p lang="ta">வணக்கம்</p>
<p lang="ur" dir="rtl">آداب</p>
<p data-aj-sound="ta">vanakkam</p>
```

Fonts are served from `https://fonts.aivibe.cloud/fonts/`. Full multi-script files are several megabytes each, so load only the styles you use.

## 4. Install

https://fonts.aivibe.cloud/install
