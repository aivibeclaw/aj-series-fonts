# Publish AJ Series Fonts into Microsoft 365 Cloud Fonts (Word, PowerPoint, Excel font dropdowns!)
# Requires SharePoint Online Management Shell & Microsoft 365 Global/SharePoint Admin
param(
  [Parameter(Mandatory=$true)][string]$TenantAdminUrl,  # e.g. https://aivibe-admin.sharepoint.com
  [Parameter(Mandatory=$true)][string]$FontLibraryUrl   # e.g. https://aivibe.sharepoint.com/sites/BrandAssets/AJSeriesFonts
)
Connect-SPOService -Url $TenantAdminUrl
Add-SPOOrgAssetsLibrary -LibraryUrl $FontLibraryUrl -OrgAssetType OfficeFontLibrary -CdnType Private
Write-Host 'AJ Series Fonts registered as Microsoft 365 Organization Cloud Fonts! Upload all 21 .otf or 57 .ttf files to the SharePoint library.'
