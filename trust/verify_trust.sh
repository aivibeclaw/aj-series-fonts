#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "=== 1. Verifying SHA-256 checksums for ALL 108 canonical binaries ==="
(cd "$ROOT" && shasum -a 256 -c SHA256SUMS.txt | tail -n 5)
echo "Total verified OK: $(cd "$ROOT" && shasum -a 256 -c SHA256SUMS.txt | grep -c ': OK')"
echo "=== 2. Verifying GPG Signature (Owner: Aravind Jayamohan <aravind.j.naidu@gmail.com>) ==="
gpg --verify "$ROOT/trust/SHA256SUMS.txt.asc" "$ROOT/SHA256SUMS.txt"
gpg --verify "$ROOT/trust/RELEASE_MANIFEST.json.asc" "$ROOT/RELEASE_MANIFEST.json"
echo "=== 3. Inspecting RFC 3161 Trusted Timestamp Token ==="
if [ -f "$ROOT/trust/SHA256SUMS.tsr" ]; then
  openssl ts -reply -in "$ROOT/trust/SHA256SUMS.tsr" -text | grep -E "Time stamp:|TSA:" || true
fi
echo "=== 4. Verifying macOS Signed Installer Certificate ==="
if [ -f "$ROOT/distributions/macos/AJ-Series-Fonts-v3.0.0-macOS.pkg" ]; then
  pkgutil --check-signature "$ROOT/distributions/macos/AJ-Series-Fonts-v3.0.0-macOS.pkg"
fi
echo "=== ALL TRUST CHECKS COMPLETED ==="
