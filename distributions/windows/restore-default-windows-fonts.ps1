#Requires -RunAsAdministrator
$FontsRegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
$SubRegPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes"
$orig = @{
    "Segoe UI (TrueType)"                 = "segoeui.ttf"
    "Segoe UI Semilight (TrueType)"       = "segoeuisl.ttf"
    "Segoe UI Semibold (TrueType)"        = "seguisb.ttf"
    "Segoe UI Bold (TrueType)"            = "segoeuib.ttf"
    "Segoe UI Italic (TrueType)"          = "segoeuii.ttf"
    "Segoe UI Semibold Italic (TrueType)" = "seguisbi.ttf"
    "Segoe UI Bold Italic (TrueType)"     = "segoeuiz.ttf"
}
foreach ($kv in $orig.GetEnumerator()) {
    Set-ItemProperty -Path $FontsRegPath -Name $kv.Key -Value $kv.Value -Type String
}
Remove-ItemProperty -Path $SubRegPath -Name "Segoe UI" -ErrorAction SilentlyContinue
Set-ItemProperty -Path $SubRegPath -Name "MS Shell Dlg" -Value "Microsoft Sans Serif" -Type String
Set-ItemProperty -Path $SubRegPath -Name "MS Shell Dlg 2" -Value "Tahoma" -Type String
Write-Host "Restored default Windows Segoe UI system font (AJ Series Fonts remain installed)."
