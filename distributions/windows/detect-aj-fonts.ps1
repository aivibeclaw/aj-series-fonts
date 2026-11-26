# Microsoft Intune Win32 Detection Rule for AJ Series Fonts v2.0.0
$Required = @("AJShresti-Regular.otf", "AJSahasvi-Regular.otf", "AJAnushya-Regular.otf", "AJTalin-Regular.otf")
$Missing = $Required | Where-Object { -not (Test-Path (Join-Path "$env:WINDIR\Fonts" $_)) }
if ($Missing.Count -eq 0) { Write-Output "Detected"; exit 0 } else { exit 1 }
