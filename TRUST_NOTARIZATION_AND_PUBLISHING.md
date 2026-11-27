# Digital Trust, Certification, Notarization & Publishing (`v3.1.0`)

**Exclusive, non-transferable copyright:** Aravind Jayamohan, India (`@ajaitech`)
**Authorized Licensees & Publishers:** Aivibe Software Services Private Limited · AjAir Tech Mobility LLP · QRaise Structures
**Official URLs:** https://fonts.aivibe.cloud · https://www.aivibe.in

Signing identities, keys and account identifiers are never stored in public files. Release tooling resolves them from the signer's keychain or environment.

This document describes required controls. It is not a certificate that a given build has passed them; check the reports published with the release.

## 1. Binary Trust

| Control | Requirement |
|---|---|
| `name` table provenance | Owner copyright, licence and vendor URL, read-only |
| `fsType` | `0` (Installable Embedding) |
| `meta` table | `dlng` / `slng` language tags |
| Vendor ID | `AJFM`; register through Microsoft Typography's vendor registration process |
| OpenType Sanitizer | All 108 binaries pass |
| FontBakery | No `FAIL` results |
| Hinting | `ttfautohint` for TrueType and web fonts |
| `DSIG` | Omitted (deprecated for modern targets) |

## 2. Signing and Notarization

- **macOS:** sign the `.pkg` with a Developer ID Installer identity, notarize with `notarytool`, staple, then verify with `spctl -a -vv -t install`.
- **iOS / iPadOS:** sign the `.mobileconfig` so devices show it as verified.
- **Windows:** Authenticode-sign installers with an RFC 3161 SHA-256 timestamp.
- **Linux:** sign packages or repository metadata.
- **Supply chain:** publish `SHA256SUMS.txt` with a detached signature and trusted timestamp, SRI hashes for web fonts, and an SPDX SBOM.

## 3. Verify a Download

```bash
shasum -a 256 AJ-Series-Fonts-v3.1.0-macOS.pkg   # compare with SHA256SUMS.txt
spctl -a -vv -t install AJ-Series-Fonts-v3.1.0-macOS.pkg
```

Official sources: `https://fonts.aivibe.cloud/downloads/` and `https://github.com/aivibe-org/aj-series-fonts/releases/download/v3.1.0/`.

## 4. Legal Registration

- Copyright registration in India in the name of Aravind Jayamohan (recognised across Berne Convention countries).
- Trademarks in Class 9 and Class 42 for `AJ Sahasvi`, `AJ Shresti`, `AJ Talin`, `AJ Anushya`, `Aaahhh Fonts Vibe` and `AJ Series`, extendable through the Madrid Protocol.

These are filing plans unless a registration number is published.

## 5. Platform Publishing and Licence Fit

| Platform | Licence accepted | Artifact |
|---|---|---|
| GitHub Releases, web CDN, npm | Ecosystem licence | All formats, SRI, checksums |
| macOS, iOS, Windows, Linux, Android | Ecosystem licence | Signed installers and packages |
| Figma, Canva, Adobe | Ecosystem licence | OTF / TTF upload |
| Commercial font marketplaces | Owner or Authorized Licensees only | OTF + WOFF2 + EULA |
| Google Fonts | SIL OFL 1.1 only | Separate edition, Owner approval required |

See [`GLOBAL_SYSTEM_FONT_PUBLISHING_PLAYBOOK.md`](./GLOBAL_SYSTEM_FONT_PUBLISHING_PLAYBOOK.md).
