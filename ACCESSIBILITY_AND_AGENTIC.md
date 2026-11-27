# Accessibility, Agentic Integration & Motion Typography (`v3.1.0`)

WCAG 2.2 AAA is a design target. Conformance applies to a finished page or app, not to a font, so verify your own product.

## 1. Accessibility in Glyphs and OpenType

- **Disambiguation:** slashed `0` vs `O` vs `o`; `I` vs `l` vs `1`; `a` vs `b` vs `6`; `rn` vs `m`; `cl` vs `d`.
- **Small sizes (9–13 pt):** use **AJ Anushya** (`556` UPM x-height, open apertures, zero protruding stubs).
- **Wide-reading mode (`ss02`):** `font-feature-settings: "ss02" 1` adds optical tracking. In AJ Talin it also separates connected forms. The `.aj-a11y-dyslexia` class in [`tokens/accessibility.css`](./tokens/accessibility.css) applies it.
- **Unicode:** symbols and currencies use their Unicode code points, so copy, paste and screen readers keep working. Sound of Font substitutions change only what is drawn; the stored text remains what was typed.
- **System preferences:** the tokens respect `prefers-contrast`, `forced-colors` and `prefers-reduced-motion`.

## 2. Agentic and Machine-Readable Typography

| File | Purpose |
|---|---|
| [`agentic/aj-series.manifest.json`](./agentic/aj-series.manifest.json) | Capability registry: 5 families, metrics, features, 25 languages |
| [`agentic/mcp-typography-protocol.json`](./agentic/mcp-typography-protocol.json) | Read-only MCP / JSON-RPC tool, resource and index schema |
| [`agentic/font-selector-schema.json`](./agentic/font-selector-schema.json) | JSON Schema (2020-12) for typography selections |
| [`agentic/index.d.ts`](./agentic/index.d.ts) | TypeScript types |
| [`tokens/aj-series.tokens.json`](./tokens/aj-series.tokens.json) | Design tokens |
| [`distributions/sdks/`](./distributions/sdks/README.md) | Language bindings with OCR disambiguation constants |

The MCP file is a protocol definition, not a running server. Its `<1 ms` figure is a latency budget for an in-memory index lookup that implementers should measure.

## 3. Motion

- Use tabular numerals (`tnum`) for counters so digits do not shift (`.aj-anim-kpi-counter`).
- Stroke paths for all 5 families are in `animation/stroke-paths/` for write-on animation.
- Motion tokens are in [`tokens/animations.css`](./tokens/animations.css) and stop under `prefers-reduced-motion`.

## 4. Install

https://fonts.aivibe.cloud/install
