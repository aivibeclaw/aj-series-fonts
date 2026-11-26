cask "font-aj-series" do
  version "3.0.0"
  sha256 "3d985f41555d16d55db1efc11fbbc2022c32bc2eb140ad48b63ba7b76ae4032d"

  url "https://github.com/aivibe-org/aj-series-fonts/releases/download/v#{version}/AJ-Series-Fonts-v#{version}-macOS.pkg"
  name "AJ Series & Aaahhh Fonts Vibe Enterprise Typefaces"
  desc "5 canonical enterprise font families (27 styles · Default 3D Mild-Gradient Press · Sound of Font · 25+ unified scripts)"
  homepage "https://fonts.aivibe.cloud"

  pkg "AJ-Series-Fonts-v#{version}-macOS.pkg"

  uninstall pkgutil: "in.aivibe.fonts.ajseries.core",
            delete:  [
              "/Library/Fonts/AJ-Series",
              "/Library/Application Support/AJ-Series-Fonts",
            ]
end
