# Authenticode SHA-256 Signing + DigiCert RFC 3161 Timestamping for Windows MSI
param([Parameter(Mandatory=$true)][string]$MsiPath)
signtool.exe sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a "$MsiPath"
signtool.exe verify /pa "$MsiPath"
