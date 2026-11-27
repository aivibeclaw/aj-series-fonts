# AJ Series & Aaahhh Fonts Vibe (`v3.1.0`) — Global System-Font Publishing Playbook

**Exclusive, non-transferable copyright:** Aravind Jayamohan, India (`@ajaitech`)
**Authorized Publishers:** Aivibe Software Services Private Limited · AjAir Tech Mobility LLP · QRaise Structures
**CDN:** https://fonts.aivibe.cloud · **Install hub:** https://fonts.aivibe.cloud/install
**Release base:** `https://github.com/aivibe-org/aj-series-fonts/releases/download/v3.1.0/`

## Typography Hierarchy

| Level | Role | Family |
|---|---|---|
| Level 1 | Headers (H1) | **AJ Sahasvi** |
| Level 2 | Sub-headings & OS default | **AJ Shresti** |
| Level 3 | Script accents and callouts | **AJ Talin** |
| Body | Reading and dense UI | **AJ Anushya** |
| Sound of Font | Phonetic typing | **Aaahhh Fonts Vibe** |

## Channel Matrix

This table is the publishing plan. Confirm each channel is live before announcing it. Download names are relative to `https://fonts.aivibe.cloud/downloads/`.

| # | Channel | Artifact | Publisher gate |
|---|---|---|---|
| 1 | Web CDN | `https://fonts.aivibe.cloud/fonts/*.woff2` | Hosting deploy |
| 2 | macOS | `AJ-Series-Fonts-v3.1.0-macOS.pkg` | Signed, notarized and stapled |
| 3 | Homebrew | `aivibe-org/homebrew-fonts`, cask `font-aj-series` | Checksum updated to the release |
| 4 | iOS / iPadOS | `AJ-Series-Fonts-v3.1.0.mobileconfig` | Signed profile or MDM |
| 5 | Apple App Store | Font provider app | App Store review |
| 6 | Windows | `AJ-Series-Fonts-v3.1.0-Windows-Core.zip`, WinGet | Code signing, WinGet review |
| 7 | Microsoft Store | Headless MSIX shared fonts | Store capability approval |
| 8 | Microsoft 365 | Organisation cloud fonts | Tenant administrator |
| 9 | Adobe, Figma, Canva | OTF upload | Organisation administrator |
| 10 | Linux | `fonts-aj-series_3.1.0_all.deb`, RPM, AUR | Repository acceptance |
| 11 | Android | `AJ-Series-Fonts-AOSP-SystemModule-v3.1.0.zip`, Downloadable Fonts provider | Play review; OEM agreements |
| 12 | OEM theme stores | Vendor theme packages | Vendor review |
| 13 | Google Fonts | Separate SIL OFL 1.1 edition | **Requires the Owner's explicit approval**: OFL permits modification, so it differs from the main licence |
| 14 | npm | `@aivibe/aj-series-fonts` | Registry publish |

## Release Gate

1. Version is `3.1.0` in every artifact; counts are 5 families, 27 styles, 108 binaries.
2. Font sanitiser and QA reports pass for the release being published.
3. Signatures and `SHA256SUMS.txt` match the uploaded files.
4. Every published URL returns the intended `v3.1.0` file.
5. No secrets, signing identifiers, personal contact data or local paths in public files.

Terms: [`LICENSE.md`](./LICENSE.md).
