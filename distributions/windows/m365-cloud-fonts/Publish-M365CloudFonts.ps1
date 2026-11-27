# Publish AJ Series Fonts into Microsoft 365 Cloud Fonts (Word, PowerPoint, Excel font dropdowns).
# Requires SharePoint Online Management Shell and a Microsoft 365 Global/SharePoint Admin.
param(
  # PLACEHOLDER: <SharePoint admin center URL of your tenant>
  [Parameter(Mandatory=$true)][string]$TenantAdminUrl,
  # PLACEHOLDER: <document library URL that will hold the font files>
  [Parameter(Mandatory=$true)][string]$FontLibraryUrl
)
Connect-SPOService -Url $TenantAdminUrl
Add-SPOOrgAssetsLibrary -LibraryUrl $FontLibraryUrl -OrgAssetType OfficeFontLibrary -CdnType Private
Write-Host 'Library registered for Microsoft 365 organization fonts. Upload all 27 canonical .ttf files to it.'
