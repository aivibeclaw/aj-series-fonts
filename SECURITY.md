# Security & Intellectual Property Policy

## Supported Versions

| Release | Status | Notes |
| :--- | :--- | :--- |
| `v3.0.x` | Supported | All 5 canonical families (`27` styles · `108` OTS-sanitized binaries) + `Sound of Font` SDK |
| `< v3.0.0` | Superseded | Upgrade to `v3.0.0` |

## Cryptographic & Binary Integrity Guarantees
- Every compiled `.ttf`, `.otf`, `.woff`, and `.woff2` binary is validated through **OpenType Sanitizer (`ots-sanitize`)** with zero parser warnings and hashed in `SHA256SUMS.txt`.
- The `Sound of Font` runtime (`sound_of_font/`) uses pure deterministic data structures with **zero `eval`**, **zero network telemetry**, and **zero prototype-pollution vectors**.

## Reporting a Vulnerability
Please report font-parser, installer, or SDK security findings via a private GitHub Security Advisory on this repository or through official enterprise channels listed at [https://www.aivibe.in](https://www.aivibe.in). Do not post exploit payloads in public issues.
