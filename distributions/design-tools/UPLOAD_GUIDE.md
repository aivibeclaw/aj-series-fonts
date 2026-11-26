# AJ Series Enterprise Typefaces (`v2.1.0`) — Elite Global Design & Office Ecosystem Publishing Guide

**Exclusive IP Owner**: Aravind Jayamohan, India (`aravind.j.naidu@gmail.com`)  
**Authorized Publishers**: Aivibe Software Services Private Limited (Chennai) · AjAir Tech Mobility LLP · QRaise Structures  
**Canonical Global CDN**: `https://fonts.aivibe.cloud` · Cloudflare Pages: `https://aj-series-fonts.pages.dev` · Firebase: `https://aj-series-fonts.web.app`  
**Registry API**: `https://fonts.aivibe.cloud/api/v2/fonts.json` · **4-Role CSS**: `https://fonts.aivibe.cloud/css/aj-series-roles.css`

---

## Structured 4-Role System Typography Hierarchy (Apply Everywhere)

| Tier | Role | Typeface Family | Key Design Spec |
|---|---|---|---|
| **Level 1** | **Headers (`H1` / Hero / Display)** | **`AJ Sahasvi`** | Sculpted Horizon Royal Small-Caps (`720→516 UPM`, `1.61:1` calligraphic contrast) |
| **Level 2** | **Sub-Headings (`H2–H3`) & Active OS Default** | **`AJ Shresti`** | Architectural Geometric Sans (curved-foot `t`, zero-stub `r`) |
| **Level 3** | **3rd-Level Text (`H4` / Callouts / Accents)** | **`AJ Talin`** | `0°` Precision Straight Connected Running Script (`calt`) + `11°` Italic |
| **Body** | **Body Text & Dense UI (`9pt–13pt`)** | **`AJ Anushya`** | Zero-Tail Ultra-Clarity Reading Sans (WCAG AAA open counters) |

---

## 1. Microsoft Office & Microsoft 365 (`aravind@aivibe.in`)
- **macOS Local Office (INSTALLED & LIVE)**:
  - Theme Font Scheme deployed to `~/Library/Group Containers/UBF8T346G9.Office/User Content.localized/Themes.localized/Theme Fonts/AJ-Series-Enterprise.xml` (`MajorFont = AJ Sahasvi`, `MinorFont = AJ Anushya` across Latin, Arabic, Devanagari, Tamil, Telugu, Bengali, Japanese, and Korean).
  - Select **Design › Fonts › AJ Series Enterprise** inside Microsoft Word, Excel, and PowerPoint.
- **Organization-Wide Microsoft 365 Cloud Fonts (`OfficeFontLibrary`)**:
  - Run `distributions/windows/m365-cloud-fonts/Publish-M365CloudFonts.ps1` as M365 SharePoint Admin (`aravind@aivibe.in`) and upload all 21 `.otf` binaries from `dist/*/otf/` so every Word, PowerPoint, and Excel desktop/web user in the organization automatically sees `AJ Sahasvi`, `AJ Shresti`, `AJ Talin`, and `AJ Anushya` natively in the Office font dropdown.
- **Windows 10/11 Core-OS & Microsoft Partner Center (`aravind@aivibe.in`)**:
  - Headless Core MSI: `AJ-Series-Fonts-v2.1.0-Windows-Core.msi` (`0` Start Menu icons, sets `Segoe UI`/`MS Shell Dlg` → `AJ Shresti`).
  - Headless Store MSIX: `AJ-Series-Fonts-v2.1.0-Store-Headless.msix` (`uap7:SharedFonts`, `0` Start Menu tiles) + submit one-time `windows.sharedFonts` allowlist ticket using `distributions/windows/msix-store/STORE_APPROVAL_REQUEST.md`.

## 2. Adobe Creative Cloud & Adobe Fonts Foundry (`aravind@aivibe.in`)
- **Local Adobe InDesign 2026 / Acrobat DC / Creative Cloud (INSTALLED & LIVE)**:
  - All **21 canonical Default 3D Paper-Press `.ttf`** binaries installed cleanly in `/Library/Fonts/AJ-Series/` (embed both `OpenType-SVG` for Adobe CC and `COLRv0` for CoreText/Web, with zero duplicate OTF/KR menu collisions).
- **Adobe Creative Cloud Sync (Personal & Team Cloud Fonts)**:
  - Open **Creative Cloud Desktop › Manage Fonts › Add Fonts to Creative Cloud** (or `https://fonts.adobe.com/my_fonts`), select all 21 `.otf` files in `dist/*/otf/` — syncs automatically across Photoshop, Illustrator, InDesign, Premiere Pro, After Effects, Acrobat, and Adobe Express.
- **Global Adobe Fonts Catalog (Foundry Partner Onboarding)**:
  - Submit foundry inquiry to **Adobe Fonts Foundry Partners** (`https://fonts.adobe.com/foundries` / `type-partners@adobe.com`) attaching:
    - Exclusive IP Ownership attestation (`LICENSE.md` — Aravind Jayamohan, India),
    - QA Certification (`trust/CERTIFICATION_REPORT.md` — OTS 84/84 PASS, FontBakery 628 PASS / 0 FAIL),
    - Visual specimen proofs (`specimens/visual_proofs/11_v21_4Family_Unique_Multilingual_Audit.png`),
    - Certified `.otf` binaries (`dist/*/otf/`).

## 3. Canva Brand Kit (`aravind.j.naidu@gmail.com`)
- Open **Canva › Brand Hub › Brand Kits** (`https://www.canva.com/brand`) signed in as `aravind.j.naidu@gmail.com`:
  1. Click **Brand Fonts › Upload a font** and upload all 21 `.otf` files from `dist/*/otf/` (`AJSahasvi-*.otf`, `AJShresti-*.otf`, `AJTalin-*.otf`, `AJAnushya-*.otf`).
  2. Configure the official 4-Role Brand Kit Hierarchy:
     - **Title / Heading**: `AJ Sahasvi ExtraBold`
     - **Subtitle / Subheading**: `AJ Shresti SemiBold`
     - **Section Header / Quote (Level 3)**: `AJ Talin SemiBold`
     - **Body / Caption**: `AJ Anushya Regular`

## 4. Figma Organization / Team Shared Fonts (`aravind@aivibe.in`)
- Open **Figma Admin › Resources › Fonts** (`https://www.figma.com/files`) signed in as `aravind@aivibe.in`:
  1. Upload all 21 `.otf` files from `dist/*/otf/` so every designer across browser & desktop automatically loads all 4 AJ Series families.
  2. Create shared Figma Text Styles matching the 4-role hierarchy (`H1/Header = AJ Sahasvi`, `H2–H3/Subheading = AJ Shresti`, `H4/Accent = AJ Talin`, `Body/UI = AJ Anushya`).
  3. On macOS local browser usage without Org plan, Figma Font Helper automatically discovers all 21 canonical Default 3D Press styles already live in macOS CoreText (`/Library/Fonts/AJ-Series/`).

## 5. Google Docs, Google Sheets, Google Slides & Global Android GMS (`fonts.google.com`)
- **Platform Architecture Reality**: Google Docs, Google Sheets, and Google Slides do **not** support uploading proprietary `.ttf`/`.otf` files via API or UI. Their native global font dropdown ("More fonts") loads **exclusively from Google Fonts (`github.com/google/fonts`)** — which also automatically distributes fonts to **stock Android (`com.google.android.gms.fonts`)**, **ChromeOS**, **Figma's global default list**, and **Canva's global default list**.
- **Mandatory Licensing Gate (Owner Confirmation Required)**: Google Fonts strictly requires releasing the submitted files under the **SIL Open Font License 1.1 (`OFL.txt`)** (irrevocable open-source license).
- **Ready-to-Submit Dual-Track Package (`distributions/google-fonts-ofl/`)**:
  - Stages ONLY the flat Core families (`ajshresti`, `ajsahasvi`, `ajanushya`, `ajtalin`) with `OFL.txt` Reserved Font Names protecting `"AJ Shresti"`, `"AJ Sahasvi"`, `"AJ Anushya"`, `"AJ Talin"`, and `"AJ Series"`, while keeping **Native COLRv0 3D Press / 3D Lift & Enterprise Core-OS Installers 100% proprietary**.
  - Submit PR to `github.com/google/fonts` ONLY upon explicit owner sign-off on SIL OFL 1.1 for the flat Core track.

## 6. Commercial Global Font Foundries & OEM System Stores
- **Monotype / MyFonts / Samsung Galaxy Store FlipFont**: Follow `distributions/android-oem/samsung-monotype-flipfont/SAMSUNG_MONOTYPE_FLIPFONT_SUBMISSION.md`.
- **Xiaomi HyperOS (`.mtz` × 4)** & **Huawei HarmonyOS (`.hwt` × 4)**: Prebuilt binaries ready in Release `v2.1.0` (`zhuti.designer.intl.xiaomi.com` & `developer.huawei.com`).
- **OPPO / OnePlus (HeyTap) & Vivo (Theme Studio)**: Follow `distributions/android-oem/oppo-vivo-themes/OPPO_ONEPLUS_VIVO_THEME_SUBMISSION.md`.
- **Fontspring / Fontstand / Creative Market**: Package `dist/*/otf/`, `dist/*/woff2/`, `specimens/visual_proofs/`, and `LICENSE.md`.
