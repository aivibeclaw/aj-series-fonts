#!/usr/bin/env bash
set -euo pipefail
PKG="$(cd "$(dirname "$0")/.." && pwd)/distributions/macos/AJ-Series-Fonts-v3.0.0-macOS.pkg"
PROFILE="${1:-AJ-Notary-Profile}"
echo "Submitting $PKG to Apple Notary Service using profile '$PROFILE'..."
xcrun notarytool submit "$PKG" --keychain-profile "$PROFILE" --wait
echo "Stapling offline Apple Gatekeeper ticket..."
xcrun stapler staple "$PKG"
spctl -a -vvv -t install "$PKG"
echo "DONE: macOS Installer is Apple-Notarized & Gatekeeper-Verified!"
