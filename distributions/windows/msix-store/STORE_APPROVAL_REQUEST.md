# Microsoft Store `windows.sharedFonts` Allowlist Request & Partner Center Guide

## Step 1 — Request `windows.sharedFonts` Permission (Mandatory One-Time Microsoft Gate)
Open https://aka.ms/storesupport → **Dashboard / App Submission Assistance** and submit:

```
Subject: Publisher Permission Request for windows.sharedFonts Extension (AJ Series Fonts)

Publisher: Aivibe Software Services Private Limited (Chennai, India)
App Name: AJ Series Fonts (AivibeSoftwareServices.AJSeriesFonts)
Reason: We are publishing 4 100% original enterprise typeface families (AJ Shresti, AJ Sahasvi, AJ Anushya, AJ Talin — 57 certified TTF styles passing OTS 156/156 and FontBakery 0 FAIL) so Windows 10/11 users can install them natively into Windows Settings > Personalization > Fonts for Microsoft Word, PowerPoint, Excel, and desktop apps.
IP Proof: Exclusive IP Owner Aravind Jayamohan, India (aravind.j.naidu@gmail.com) has granted Aivibe Software Services Private Limited perpetual publishing rights (attached LICENSE.md & CERTIFICATION_REPORT.md).
```

## Step 2 — Build & Upload `.msixupload`
On Windows 11 with Windows SDK installed, copy `dist/*/ttf/*.ttf` into `Assets\Fonts\`, build the companion previewer `AJSeriesFontsWin.exe`, run `makeappx pack /d . /p AJ-Series-Fonts-v2.1.0.msix`, and upload to **Microsoft Partner Center** (Microsoft automatically signs Store MSIX packages!).
