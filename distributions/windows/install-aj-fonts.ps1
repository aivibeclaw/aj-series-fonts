#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Zero-Icon Core-OS Managed Installer for AJ Series & Aaahhh Fonts Vibe Enterprise Typefaces v3.1.0
  - Purges legacy duplicate OTF / 3DPress / 3DLift / KR binaries and stale Adobe / Office caches
  - Installs all 27 canonical Default 3D Mild-Gradient Press TTF binaries into C:\Windows\Fonts
  - Registers every font immediately via Win32 GDI AddFontResourceW + WM_FONTCHANGE broadcast API
  - Refreshes Windows FontCache service so Adobe CC, Office, Browsers & WinUI re-index immediately
  - Configures AJ Shresti as Active Default Windows UI Font, Chrome/Edge translation hints, Closed Captions & Office Theme XML
#>
param(
    [string]$FontsSourceDir = "$PSScriptRoot\fonts",
    [switch]$SkipDefaultSystemFontOverride
)
$ErrorActionPreference = "Stop"

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class Win32FontApi {
    [DllImport("gdi32.dll", CharSet = CharSet.Unicode)]
    public static extern int AddFontResourceW(string lpszFilename);
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern IntPtr SendMessageTimeout(IntPtr hWnd, uint Msg, UIntPtr wParam, IntPtr lParam, uint fuFlags, uint uTimeout, out UIntPtr lpdwResult);
}
"@

$WinFontsDir = Join-Path $env:WINDIR "Fonts"
$FontsRegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
$SubRegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"

# Clean legacy 3DPress / 3DLift / KR shard files & stale Adobe/Office caches
Get-ChildItem -Path $WinFontsDir -Filter "AJ*3D*.ttf" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $WinFontsDir -Filter "AJ*KR-*.ttf" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
if ($env:LOCALAPPDATA) {
    Get-ChildItem -Path (Join-Path $env:LOCALAPPDATA "Adobe") -Filter "AdobeFnt*.lst" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Remove-Item -Path (Join-Path $env:LOCALAPPDATA "Microsoft\FontCache") -Recurse -Force -ErrorAction SilentlyContinue
}

$files = Get-ChildItem -Path $FontsSourceDir -Include *.ttf -Recurse
if ($files.Count -eq 0) { throw "No .ttf font files found in $FontsSourceDir" }

$installed = 0
foreach ($f in $files) {
    $dest = Join-Path $WinFontsDir $f.Name
    Copy-Item -Path $f.FullName -Destination $dest -Force
    $regName = "$($f.BaseName.Replace('-', ' ')) (TrueType)"
    Set-ItemProperty -Path $FontsRegPath -Name $regName -Value $f.Name -Type String
    [void][Win32FontApi]::AddFontResourceW($dest)
    $installed++
}

if (-not $SkipDefaultSystemFontOverride) {
    $segoeMap = @{
        "Segoe UI (TrueType)"                    = "AJShresti-Regular.ttf"
        "Segoe UI Semilight (TrueType)"          = "AJShresti-Regular.ttf"
        "Segoe UI Semibold (TrueType)"           = "AJShresti-SemiBold.ttf"
        "Segoe UI Bold (TrueType)"               = "AJShresti-ExtraBold.ttf"
        "Segoe UI Italic (TrueType)"             = "AJShresti-Italic.ttf"
        "Segoe UI Semibold Italic (TrueType)"    = "AJShresti-SemiBoldItalic.ttf"
        "Segoe UI Bold Italic (TrueType)"        = "AJShresti-ExtraBoldItalic.ttf"
    }
    foreach ($kv in $segoeMap.GetEnumerator()) {
        Set-ItemProperty -Path $FontsRegPath -Name $kv.Key -Value $kv.Value -Type String
    }
    Set-ItemProperty -Path $SubRegPath -Name "Segoe UI" -Value "AJ Shresti" -Type String
    Set-ItemProperty -Path $SubRegPath -Name "MS Shell Dlg" -Value "AJ Shresti" -Type String
    Set-ItemProperty -Path $SubRegPath -Name "MS Shell Dlg 2" -Value "AJ Shresti" -Type String
}

# Register Chrome/Edge per-script & translation font hints + Windows Closed Captions / ActiveMovie subtitles
foreach ($BrowserKey in @("HKCU:\Software\Google\Chrome\FontSettings", "HKCU:\Software\Microsoft\Edge\FontSettings")) {
    New-Item -Path $BrowserKey -Force | Out-Null
    Set-ItemProperty -Path $BrowserKey -Name "StandardFontFamily" -Value "AJ Shresti" -Type String
    Set-ItemProperty -Path $BrowserKey -Name "SansSerifFontFamily" -Value "AJ Shresti" -Type String
    Set-ItemProperty -Path $BrowserKey -Name "SerifFontFamily" -Value "AJ Sahasvi" -Type String
    Set-ItemProperty -Path $BrowserKey -Name "CursiveFontFamily" -Value "AJ Talin" -Type String
    Set-ItemProperty -Path $BrowserKey -Name "TranslationBodyFont" -Value "AJ Shresti" -Type String
    Set-ItemProperty -Path $BrowserKey -Name "TranslationHeadingFont" -Value "AJ Sahasvi ExtraBold" -Type String
}
foreach ($CapKey in @("HKCU:\Software\Microsoft\ActiveMovie", "HKCU:\Software\Microsoft\ClosedCaptioning")) {
    New-Item -Path $CapKey -Force | Out-Null
    Set-ItemProperty -Path $CapKey -Name "SubtitleFont" -Value "AJ Shresti SemiBold" -Type String
    Set-ItemProperty -Path $CapKey -Name "CaptionFontFamily" -Value "AJ Shresti SemiBold" -Type String
}

# Install AJ-Series-Enterprise.xml Office Theme (majorFont = AJ Sahasvi ExtraBold, minorFont = AJ Shresti)
$ThemeXmlContent = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:fontScheme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="AJ Series Enterprise">
  <a:majorFont>
    <a:latin typeface="AJ Sahasvi ExtraBold" />
    <a:ea typeface="AJ Sahasvi ExtraBold" />
    <a:cs typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Arab" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Deva" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Taml" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Telu" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Mlym" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Knda" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Guru" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Beng" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Cyrl" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Hans" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Thai" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Ethi" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Jpan" typeface="AJ Sahasvi ExtraBold" />
    <a:font script="Hang" typeface="AJ Sahasvi ExtraBold" />
  </a:majorFont>
  <a:minorFont>
    <a:latin typeface="AJ Shresti" />
    <a:ea typeface="AJ Shresti" />
    <a:cs typeface="AJ Shresti" />
    <a:font script="Arab" typeface="AJ Shresti" />
    <a:font script="Deva" typeface="AJ Shresti" />
    <a:font script="Taml" typeface="AJ Shresti" />
    <a:font script="Telu" typeface="AJ Shresti" />
    <a:font script="Mlym" typeface="AJ Shresti" />
    <a:font script="Knda" typeface="AJ Shresti" />
    <a:font script="Guru" typeface="AJ Shresti" />
    <a:font script="Beng" typeface="AJ Shresti" />
    <a:font script="Cyrl" typeface="AJ Shresti" />
    <a:font script="Hans" typeface="AJ Shresti" />
    <a:font script="Thai" typeface="AJ Shresti" />
    <a:font script="Ethi" typeface="AJ Shresti" />
    <a:font script="Jpan" typeface="AJ Shresti" />
    <a:font script="Hang" typeface="AJ Shresti" />
  </a:minorFont>
</a:fontScheme>
'@
if ($env:APPDATA) {
    $OfficeThemeDir = Join-Path $env:APPDATA "Microsoft\Templates\Document Themes\Theme Fonts"
    New-Item -ItemType Directory -Force -Path $OfficeThemeDir | Out-Null
    Set-Content -Path (Join-Path $OfficeThemeDir "AJ-Series-Enterprise.xml") -Value $ThemeXmlContent -Encoding UTF8
}
$SysOfficeThemeDir = Join-Path ${env:ProgramFiles} "Microsoft Office\root\Document Themes 16\Theme Fonts"
if (Test-Path (Split-Path $SysOfficeThemeDir -Parent)) {
    New-Item -ItemType Directory -Force -Path $SysOfficeThemeDir | Out-Null
    Set-Content -Path (Join-Path $SysOfficeThemeDir "AJ-Series-Enterprise.xml") -Value $ThemeXmlContent -Encoding UTF8
}

# Restart Windows FontCache service & broadcast WM_FONTCHANGE so all apps re-index immediately
Stop-Service -Name "FontCache" -Force -ErrorAction SilentlyContinue
Start-Service -Name "FontCache" -ErrorAction SilentlyContinue
$res = [UIntPtr]::Zero
[void][Win32FontApi]::SendMessageTimeout([IntPtr]0xFFFF, 0x001D, [UIntPtr]::Zero, [IntPtr]::Zero, 2, 2000, [ref]$res)

Write-Host "SUCCESS: Installed & re-indexed $installed canonical AJ Series fonts, Office Theme XML, Browser & Caption bindings."
