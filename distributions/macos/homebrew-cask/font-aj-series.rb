cask "font-aj-series" do
  version "3.1.0"
  sha256 "3dddf4649125fde21ce6f42246de3606c523a041c3138b1ebeb1757983e6f8ec"

  url "https://github.com/aivibe-org/aj-series-fonts/releases/download/v#{version}/AJ-Series-Fonts-v#{version}-macOS.pkg"
  name "AJ Series & Aaahhh Fonts Vibe Enterprise Typefaces"
  desc "5 canonical font families (27 styles)"
  homepage "https://fonts.aivibe.cloud"

  pkg "AJ-Series-Fonts-v#{version}-macOS.pkg"

  uninstall pkgutil: "in.aivibe.fonts.ajseries.core",
            delete:  [
              "/Library/Fonts/AJ-Series",
              "/Library/Application Support/AJ-Series-Fonts",
            ]
end
