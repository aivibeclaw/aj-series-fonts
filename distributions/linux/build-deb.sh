#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STAGE="/tmp/fonts-aj-series_2.0.0_all"
rm -rf "$STAGE"
mkdir -p "$STAGE/DEBIAN" "$STAGE/usr/share/fonts/opentype/aj-series" "$STAGE/usr/share/fonts/truetype/aj-series" "$STAGE/etc/fonts/conf.d"
cp "$ROOT"/dist/*/otf/*.otf "$STAGE/usr/share/fonts/opentype/aj-series/"
cp "$ROOT"/dist/*/ttf/*3D*.ttf "$ROOT"/dist/*/ttf/*KR-*.ttf "$STAGE/usr/share/fonts/truetype/aj-series/"
cp "$ROOT/distributions/linux/65-aj-series.conf" "$STAGE/etc/fonts/conf.d/"
cat > "$STAGE/DEBIAN/control" <<'EOF'
Package: fonts-aj-series
Version: 2.0.0
Section: fonts
Priority: optional
Architecture: all
Maintainer: Aravind Jayamohan <aravind.j.naidu@gmail.com>
Description: AJ Series Enterprise Original Multi-Script & Native 3D COLR Typefaces
 Exclusive IP owned by Aravind Jayamohan, India.
EOF
dpkg-deb --build "$STAGE" "$ROOT/distributions/linux/fonts-aj-series_2.0.0_all.deb"
