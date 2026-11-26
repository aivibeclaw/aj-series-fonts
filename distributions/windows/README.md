# Windows 10/11, Microsoft 365 & Intune Deployment Kit
1. Copy compiled `.otf` and `.ttf` files from `dist/*/otf/` and `dist/*/ttf/` into `distributions/windows/fonts/`.
2. Package with Microsoft Win32 Content Prep Tool (`IntuneWinAppUtil.exe -c . -s install-aj-fonts.ps1 -o out/`).
3. Upload `.intunewin` to **Microsoft Intune → Apps → Windows → Win32 App** with `detect-aj-fonts.ps1` as the detection rule.
4. For direct customer downloads, wrap into an `.msi` (WiX v4) and sign via `sign-windows-msi.ps1` using your OV/EV Code Signing Certificate.
