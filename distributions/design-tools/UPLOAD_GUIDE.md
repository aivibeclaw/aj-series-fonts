# AJ Series & Aaahhh Fonts Vibe (v3.1.0): Design & Office Ecosystem Publishing Guide

**Exclusive IP Owner**: Aravind Jayamohan, India
**Authorized Publishers**: Aivibe Software Services Private Limited (Chennai) · AjAir Tech Mobility LLP · QRaise Structures
**Website & CDN**: https://fonts.aivibe.cloud
**Downloads**: https://github.com/aivibe-org/aj-series-fonts/releases/tag/v3.1.0

> Sign in to each service with `<PLACEHOLDER: organization admin account>`. Never record account addresses here.

## Role hierarchy (apply everywhere)
| Role | Family |
|---|---|
| Headers (H1 / Display) | **AJ Sahasvi** |
| Sub-headings & OS default | **AJ Shresti** |
| Level-3 text, callouts | **AJ Talin** |
| Body & dense UI | **AJ Anushya** |
| Sound of Font input | **Aaahhh Fonts Vibe** |

## 1. Microsoft Office & Microsoft 365
- Local Office: install the Theme Font Scheme `AJ-Series-Enterprise.xml` (the macOS and Windows installers do this).
- Organization cloud fonts: run `distributions/windows/m365-cloud-fonts/Publish-M365CloudFonts.ps1` with your own
  `<PLACEHOLDER: tenant admin URL>` and `<PLACEHOLDER: font library URL>`, then upload the 27 `.ttf` files.
- Windows packages: `AJ-Series-Fonts-v3.1.0-Windows-Core.msi` and `AJ-Series-Fonts-v3.1.0-Store-Headless.msix`.
  Request the `windows.sharedFonts` allowlist with `distributions/windows/msix-store/STORE_APPROVAL_REQUEST.md`.

## 2. Adobe Creative Cloud & Adobe Fonts
- Creative Cloud Desktop > Manage Fonts > Add Fonts: upload the 27 `.otf` files.
- Foundry onboarding: https://fonts.adobe.com/foundries (attach `LICENSE.md`, the certification report, specimens, `.otf` files).

## 3. Canva Brand Kit
- Brand Hub > Brand Kits (https://www.canva.com/brand) > Brand Fonts > Upload: the 27 `.otf` files, then map the roles above.

## 4. Figma
- Figma Admin > Resources > Fonts: upload the 27 `.otf` files and create text styles for the roles above.

## 5. Google Fonts (Docs, Sheets, Slides, Android GMS, ChromeOS)
- Google's font list only loads from `github.com/google/fonts`, which requires SIL OFL 1.1 (irrevocable).
- Staging kit: `distributions/google-fonts-ofl/`. Submit only after explicit owner sign-off. The OFL grant is
  conditional and does not relicense the main suite.

## 6. Foundries & OEM stores
- Samsung / Monotype, Xiaomi, Huawei, OPPO / OnePlus / Vivo: see the guides under `distributions/android-oem/`.
