# Microsoft Intune Win32 detection rule for AJ Series Fonts v3.1.0 (all 27 canonical styles)
$Required = @(
    "AJSahasvi-Regular.ttf",
    "AJSahasvi-SemiBold.ttf",
    "AJSahasvi-ExtraBold.ttf",
    "AJShresti-Regular.ttf",
    "AJShresti-Italic.ttf",
    "AJShresti-SemiBold.ttf",
    "AJShresti-SemiBoldItalic.ttf",
    "AJShresti-ExtraBold.ttf",
    "AJShresti-ExtraBoldItalic.ttf",
    "AJTalin-Regular.ttf",
    "AJTalin-Italic.ttf",
    "AJTalin-SemiBold.ttf",
    "AJTalin-SemiBoldItalic.ttf",
    "AJTalin-ExtraBold.ttf",
    "AJTalin-ExtraBoldItalic.ttf",
    "AJAnushya-Regular.ttf",
    "AJAnushya-Italic.ttf",
    "AJAnushya-SemiBold.ttf",
    "AJAnushya-SemiBoldItalic.ttf",
    "AJAnushya-ExtraBold.ttf",
    "AJAnushya-ExtraBoldItalic.ttf",
    "AaahhhFontsVibe-Regular.ttf",
    "AaahhhFontsVibe-Italic.ttf",
    "AaahhhFontsVibe-SemiBold.ttf",
    "AaahhhFontsVibe-SemiBoldItalic.ttf",
    "AaahhhFontsVibe-ExtraBold.ttf",
    "AaahhhFontsVibe-ExtraBoldItalic.ttf"
)
$Missing = $Required | Where-Object { -not (Test-Path (Join-Path "$env:WINDIR\Fonts" $_)) }
if ($Missing.Count -eq 0) { Write-Output "Detected"; exit 0 } else { exit 1 }
