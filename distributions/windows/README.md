# Windows 10/11, Microsoft 365 & Intune Deployment Kit (v3.1.0, 5 families, 27 styles)

## Published downloads
- Website: https://fonts.aivibe.cloud
- Release v3.1.0: https://github.com/aivibe-org/aj-series-fonts/releases/tag/v3.1.0 (`AJ-Series-Fonts-v3.1.0-Windows-Core.msi`, `-Store-Headless.msix`, `-Microsoft-Store.msix`, `.msixupload`)

## Intune
1. Copy the `.ttf` files from `dist/*/ttf/` into `distributions/windows/fonts/`.
2. Package with the Win32 Content Prep Tool (`IntuneWinAppUtil.exe -c . -s install-aj-fonts.ps1 -o out/`).
3. Upload the `.intunewin` as a Win32 app with `detect-aj-fonts.ps1` as the detection rule.
4. For direct downloads, build the `.msi` (WiX v4) and sign it with `sign-windows-msi.ps1`.
