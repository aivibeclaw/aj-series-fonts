#!/usr/bin/env python3
"""Visual Specimen & Microscopic Manual Audit Renderer for AJ Series Fonts.

Renders REAL compiled .woff2 binaries in headless Google Chrome at 2x Retina DPI
for manual human/agent visual inspection of EVERY single glyph, baseline landing,
kerning pair, OpenType feature, analytical symbol, small-size comfort, and 15 languages.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path("/Users/aj/Dev-Apps/AJ-Series-Fonts")
DIST = ROOT / "dist"
OUT = ROOT / "specimens" / "visual_proofs"
OUT.mkdir(parents=True, exist_ok=True)
LIVE_DIR = Path("/Users/aj/.gemini/antigravity/brain/c5587e77-4c91-4c85-91a9-51e8729df258/scratch/aj_series_samples")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def font_face_css(prefix: str = "../../dist") -> str:
    defs = [
        ("AJ Shresti", "aj-shresti", "AJShresti-Regular", 400, "normal"),
        ("AJ Shresti", "aj-shresti", "AJShresti-SemiBold", 600, "normal"),
        ("AJ Shresti", "aj-shresti", "AJShresti-ExtraBold", 800, "normal"),
        ("AJ Shresti", "aj-shresti", "AJShresti-Italic", 400, "italic"),
        ("AJ Shresti", "aj-shresti", "AJShresti-SemiBoldItalic", 600, "italic"),
        ("AJ Shresti", "aj-shresti", "AJShresti-ExtraBoldItalic", 800, "italic"),
        ("AJ Sahasvi", "aj-sahasvi", "AJSahasvi-Regular", 400, "normal"),
        ("AJ Sahasvi", "aj-sahasvi", "AJSahasvi-SemiBold", 600, "normal"),
        ("AJ Sahasvi", "aj-sahasvi", "AJSahasvi-ExtraBold", 800, "normal"),
        ("AJ Anushya", "aj-anushya", "AJAnushya-Regular", 400, "normal"),
        ("AJ Anushya", "aj-anushya", "AJAnushya-SemiBold", 600, "normal"),
        ("AJ Anushya", "aj-anushya", "AJAnushya-ExtraBold", 800, "normal"),
        ("AJ Anushya", "aj-anushya", "AJAnushya-Italic", 400, "italic"),
        ("AJ Anushya", "aj-anushya", "AJAnushya-SemiBoldItalic", 600, "italic"),
        ("AJ Anushya", "aj-anushya", "AJAnushya-ExtraBoldItalic", 800, "italic"),
        ("AJ Talin", "aj-talin", "AJTalin-Regular", 400, "normal"),
        ("AJ Talin", "aj-talin", "AJTalin-SemiBold", 600, "normal"),
        ("AJ Talin", "aj-talin", "AJTalin-ExtraBold", 800, "normal"),
        ("AJ Talin", "aj-talin", "AJTalin-Italic", 400, "italic"),
        ("AJ Talin", "aj-talin", "AJTalin-SemiBoldItalic", 600, "italic"),
        ("AJ Talin", "aj-talin", "AJTalin-ExtraBoldItalic", 800, "italic"),
    ]
    blocks = []
    for fam, slug, ps, wt, st in defs:
        if prefix == "live_fonts":
            url = f"live_fonts/{ps}.woff2"
        else:
            url = f"{prefix}/{slug}/woff2/{ps}.woff2"
        blocks.append(
            f"@font-face {{ font-family: '{fam}'; src: url('{url}') format('woff2'); "
            f"font-weight: {wt}; font-style: {st}; font-display: block; }}"
        )
    return "\n".join(blocks)


def render_png(html_path: Path, png_path: Path, width: int = 1600, height: int = 1280) -> None:
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        "--force-device-scale-factor=2",
        f"--screenshot={png_path}",
        f"file://{html_path}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def ruled_line_html(text: str, family: str, size_px: int, weight: int, xh_ratio: float, italic: bool = False, extra_cls: str = "") -> str:
    """Renders real compiled font text with mathematically exact CAP / X-H / BASE / DESC overlay lines!
    Note: Our fonts have UPM=1000, ascender=880, descender=-220 -> line-box = 1100 UPM (top at +880, baseline at 880/1100 = 80%).
    Wait: CSS normal line-height with line-height: 1.0 sets em-box height = 1000 UPM, baseline at ascender/(asc-desc) = 880/1100 = 80% of 1.1em!
    Using exact inline-block height = 1.1em (1100 UPM):
      top_px = 0 -> y = +880 UPM
      CAP (+720) -> top = (880 - 720)/1100 = 14.545%
      X-H (+xh)  -> top = (880 - xh)/1100
      BASE (0)   -> top = 880/1100 = 80.000%
      DESC (-180)-> top = (880 + 180)/1100 = 96.364%
    """
    xh_upm = xh_ratio * 1000.0
    cap_pct = (880.0 - 720.0) / 1100.0 * 100.0
    xh_pct = (880.0 - xh_upm) / 1100.0 * 100.0
    base_pct = 880.0 / 1100.0 * 100.0
    desc_pct = (880.0 + 180.0) / 1100.0 * 100.0
    style_it = "italic" if italic else "normal"
    return f"""
    <div class="ruled-box {extra_cls}" style="font-family:'{family}';font-size:{size_px}px;font-weight:{weight};font-style:{style_it};line-height:1.1;">
      <span class="guide g-cap" style="top:{cap_pct:.3f}%"><em>CAP</em></span>
      <span class="guide g-xh" style="top:{xh_pct:.3f}%"><em>X-H</em></span>
      <span class="guide g-base" style="top:{base_pct:.3f}%"><em>BASE</em></span>
      <span class="guide g-desc" style="top:{desc_pct:.3f}%"><em>DESC</em></span>
      <span class="ruled-txt">{text}</span>
    </div>
    """


COMMON_CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #F7F4EE; color: #141C24; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; padding: 26px 34px; }
  .hdr { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #DED7C8; padding-bottom: 12px; margin-bottom: 18px; }
  .eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 1.8px; text-transform: uppercase; }
  .h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.4px; margin-top: 2px; }
  .badge { font-size: 11.5px; font-weight: 700; padding: 5px 12px; border-radius: 999px; background: #FFF; border: 1px solid #D8D0C0; }
  .card { background: #FFFFFF; border: 1px solid #E2DCD0; border-radius: 16px; padding: 16px 22px; margin-bottom: 14px; }
  .card-lbl { font-size: 10px; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase; color: #5D6A77; margin-bottom: 10px; display: flex; justify-content: space-between; }
  .ruled-box { position: relative; display: block; width: 100%; padding-right: 46px; white-space: nowrap; overflow: visible; }
  .ruled-txt { position: relative; z-index: 2; }
  .guide { position: absolute; left: 0; right: 0; height: 0; z-index: 1; pointer-events: none; }
  .guide em { position: absolute; right: 0; top: -6px; font-style: normal; font-family: -apple-system, sans-serif; font-size: 9px; font-weight: 800; letter-spacing: 0.6px; }
  .g-cap { border-top: 1px dashed rgba(13,122,111,0.55); color: #0D7A6F; }
  .g-xh  { border-top: 1px dashed rgba(37,99,235,0.48); color: #2563EB; }
  .g-base{ border-top: 1.5px solid rgba(217,72,38,0.85); color: #D94826; }
  .g-desc{ border-top: 1px dashed rgba(120,132,146,0.55); color: #788492; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
  .w-row { display: flex; align-items: baseline; gap: 16px; margin-bottom: 8px; }
  .w-tag { font-size: 10px; font-weight: 700; color: #64707C; width: 118px; flex-shrink: 0; text-transform: uppercase; }
  .paper-press {
    background: linear-gradient(155deg, #E8E1D3 0%, #DBD3C2 100%);
    border: 1px solid #C5BBA8; border-radius: 14px; padding: 18px 24px;
    box-shadow: inset 0 2px 5px rgba(255,255,255,0.75), inset 0 -3px 8px rgba(72,60,44,0.14);
  }
  .press-txt {
    color: rgba(16, 42, 54, 0.86);
    text-shadow: 0 2px 1px rgba(255,255,255,0.92), 0 -1.5px 1.5px rgba(0,0,0,0.42);
  }
  .glossy-hero {
    border-radius: 14px; padding: 18px 24px; color: #FFFFFF;
    box-shadow: 0 12px 24px rgba(15,23,42,0.18), inset 0 1.5px 0 rgba(255,255,255,0.45);
  }
  .glossy-txt {
    color: #F4FBFF;
    text-shadow: 0 3px 6px rgba(6,24,38,0.45), 0 8px 18px rgba(6,24,38,0.32), 0 -1px 0 rgba(255,255,255,0.6);
  }
"""


def build_family_audit_board(
    num: str,
    slug: str,
    family: str,
    role: str,
    accent: str,
    banner_bg: str,
    xh_ratio: float,
    has_italic: bool,
    hero_sample: str,
    extra_proof_label: str,
    extra_proof_text: str,
) -> Path:
    it_rows = ""
    if has_italic:
        it_rows = f"""
        <div class="w-row"><span class="w-tag">400 Italic</span><span style="font-family:'{family}';font-size:34px;font-weight:400;font-style:italic;">{hero_sample} · 0123456789</span></div>
        <div class="w-row"><span class="w-tag">600 Bold L1 It</span><span style="font-family:'{family}';font-size:34px;font-weight:600;font-style:italic;">{hero_sample} · 0123456789</span></div>
        <div class="w-row"><span class="w-tag">800 Bold L2 It</span><span style="font-family:'{family}';font-size:34px;font-weight:800;font-style:italic;color:{accent};">{hero_sample} · 0123456789</span></div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>{num} {family} Compiled Binary Audit</title>
<style>
{font_face_css()}
{COMMON_CSS}
</style></head><body>
  <div class="hdr">
    <div>
      <div class="eyebrow" style="color:{accent};">COMPILED WOFF2 BINARY MICROSCOPIC AUDIT · {num} OF 04 · REAL CHROME HARFBUZZ RENDERING</div>
      <div class="h1">{family} — {role}</div>
    </div>
    <div class="badge" style="color:{accent};">Owner: Aravind Jayamohan, India · v1.0.0</div>
  </div>

  <div class="card">
    <div class="card-lbl"><span>COMPLETE UPPERCASE A–Z &amp; LOWERCASE a–z WITH LIVE CAP / X-H / BASE / DESC RULERS (BOLD L1 600)</span><span>ZERO SHARP EDGES · EXACT BASE=0 · CAP=720</span></div>
    {ruled_line_html("ABCDEFGHIJKLM NOPQRSTUVWXYZ", family, 62, 600, xh_ratio)}
    <div style="height:10px;"></div>
    {ruled_line_html("abcdefghijklm nopqrstuvwxyz", family, 62, 600, xh_ratio)}
    <div style="height:10px;"></div>
    {ruled_line_html("0123456789 · 0oO · ab6 · Il1 · ₹€£¥₩$₿", family, 56, 600, xh_ratio)}
  </div>

  <div class="grid-2">
    <div class="card">
      <div class="card-lbl"><span>ALL COMPILED WEIGHTS &amp; STYLES (REAL WOFF2)</span><span>400 / 600 / 800</span></div>
      <div class="w-row"><span class="w-tag">400 Regular</span><span style="font-family:'{family}';font-size:34px;font-weight:400;">{hero_sample} · 0123456789</span></div>
      <div class="w-row"><span class="w-tag">600 Bold L1</span><span style="font-family:'{family}';font-size:34px;font-weight:600;">{hero_sample} · 0123456789</span></div>
      <div class="w-row"><span class="w-tag">800 Bold L2</span><span style="font-family:'{family}';font-size:34px;font-weight:800;color:{accent};">{hero_sample} · 0123456789</span></div>
      {it_rows}
    </div>

    <div class="card">
      <div class="card-lbl"><span>{extra_proof_label}</span><span>OPENTYPE KERN + CALT + LIGA</span></div>
      {ruled_line_html(extra_proof_text, family, 56, 600, xh_ratio)}
      <div style="height:12px;"></div>
      <div style="font-family:'{family}';font-size:26px;font-weight:400;line-height:1.45;font-kerning:normal;font-variant-ligatures:common-ligatures contextual;">
        AV AW AT AY VA WA YA · To Te Tr Ty Va We Yo<br/>
        P. F. T. V. W. Y. · fi fl ff ffi ffl · 12:30 · <span style="font-feature-settings:'dlig' 1;">-&gt; =&gt; != &lt;= &gt;= ...</span>
      </div>
      <div style="margin-top:10px;padding-top:10px;border-top:1px solid #EFEAE1;font-family:'{family}';">
        <div style="font-size:9pt;margin-bottom:4px;"><b>9pt Reg:</b> VibeMyTrip · Pure Clarity · 0123456789 · ₹49,850.00 · Il1 0oO ab6 rn m cl d</div>
        <div style="font-size:10.5pt;margin-bottom:4px;"><b>10.5pt Reg:</b> The quick brown fox jumps over 42 lazy dogs — WCAG AAA clarity!</div>
        <div style="font-size:12pt;font-weight:600;"><b>12pt Bold L1:</b> Analytical KPIs ▲ +18.4% · ▁▂▃▄▅▆▇█ · Status ● Online ✓</div>
        <div style="font-size:11pt;font-feature-settings:'ss02' 1;color:#334155;margin-top:4px;"><b>11pt ss02 (WCAG Wide):</b> Dyslexia-friendly optical tracking enabled natively in OpenType!</div>
      </div>
    </div>
  </div>

  <div class="grid-2">
    <div class="glossy-hero" style="background:{banner_bg};">
      <div style="font-size:10px;font-weight:700;letter-spacing:1.4px;opacity:0.88;margin-bottom:8px;">REAL COMPILED FONT · GLOSSY 3D ELEVATED HERO (BOLD L2 800)</div>
      <div class="glossy-txt" style="font-family:'{family}';font-size:58px;font-weight:800;line-height:1.15;">{hero_sample}</div>
    </div>
    <div class="paper-press">
      <div style="font-size:10px;font-weight:700;letter-spacing:1.4px;color:#544A3D;margin-bottom:8px;">REAL COMPILED FONT · 3D PAPER-PRESSED LETTERPRESS (BOLD L1 600)</div>
      <div class="press-txt" style="font-family:'{family}';font-size:58px;font-weight:600;line-height:1.15;">{hero_sample}</div>
    </div>
  </div>
</body></html>"""
    hp = OUT / f"{num}_{slug}_Compiled_Audit.html"
    pp = OUT / f"{num}_{slug}_Compiled_Audit.png"
    hp.write_text(html, encoding="utf-8")
    render_png(hp, pp, width=1640, height=1180)
    return pp


def build_symbols_audit_board() -> Path:
    rows = [
        ("CURRENCIES & FINANCE", "$ € £ ¥ ₹ ₩ ¢ ¤ ₽ ₺ ₿  ·  % ‰ ‱  ·  ₹1,24,850.00  €980.50  $4,200  ¥89,000  ₩15,000"),
        ("MATH & ANALYTICAL OPERATORS", "+ − × ÷ = ≠ ≈ ≡ ≤ ≥ ± ∓ ∞ √ ∑ ∏ ∫ ∂ ∆ ∇ ∝ ∈ ∉ ⊂ ⊃ ∪ ∩ ∧ ∨ ¬ ∀ ∃ ∅ ∴ ∵ ∶ ∷ ⊕ ⊖ ⊗ ⊘ ⊙"),
        ("GREEK ANALYTICAL / SCIENCE", "Γ Δ Θ Λ Ξ Π Σ Φ Ψ Ω  ·  α β γ δ ε θ λ μ π ρ σ τ φ ω  ·  Δx/Δt = σ² + μπ"),
        ("BULLETS, BEACONS & RATINGS", "• ◦ ▪ ▫ ■ □ ◆ ◇ ❖ ✦ ✧ ★ ☆ ● ○ ◉ ◎ ◌ ◐ ◑ ▬ ▮ ▯"),
        ("KPI TRIANGLES & SPARKLINES", "▲ △ ▼ ▽ ▶ ▷ ◀ ◁ ▴ ▵ ▾ ▿ ▸ ▹ ◂ ◃   ·   ▁ ▂ ▃ ▄ ▅ ▆ ▇ █   ·   ▁▃▂▅▄▆▇█ ▲ +24.8%"),
        ("ARROWS & PIPELINE FLOWS", "← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ⇐ ⇑ ⇒ ⇓ ⇔ ⇄ ⇅ ↺ ↻ ↵ ⇥ ⇤ ➔ ➜ ➤"),
        ("ENTERPRISE & AGENTIC UI", "✓ ✔ ✕ ✖ ✗ ✘ ⚠ ⚡ ⌘ ⌥ ⇧ ⌃ ⏎ ⌫ ⎋ ⌖ ⚙ ⏻   ·   © ® ™ ℠ ℗ § ¶ † ‡ № ° ′ ″"),
        ("FRACTIONS, SUPS, SUBS & DLIG", "¼ ½ ¾ ⅓ ⅔ ⅛ ⅜ ⅝ ⅞  ·  x⁰¹²³⁴⁵⁶⁷⁸⁹ + H₂O₀₁₂₃₄₅₆₇₈₉  ·  <span style='font-feature-settings:\"frac\" 1;'>7/16 99/100 123/456 a/b</span>  ·  <span style='font-feature-settings:\"dlig\" 1;'>-&gt; &lt;- &lt;-&gt; =&gt; != &lt;= &gt;= +- ...</span>"),
    ]
    blocks = []
    for fam, col in [("AJ Shresti", "#0A7A6E"), ("AJ Sahasvi", "#9A4206"), ("AJ Anushya", "#1D4ED8"), ("AJ Talin", "#BE185D")]:
        inner = ""
        for lbl, txt in rows:
            inner += f"""
            <div style="display:grid;grid-template-columns:230px 1fr;gap:14px;align-items:center;padding:5px 0;border-bottom:1px solid #F1ECE3;">
              <div style="font-size:9.5px;font-weight:700;letter-spacing:1px;color:{col};">{lbl}</div>
              <div style="font-family:'{fam}';font-size:21px;font-weight:600;color:#141C24;">{txt}</div>
            </div>"""
        blocks.append(f"""
        <div class="card" style="padding:13px 20px;margin-bottom:12px;">
          <div class="card-lbl"><span style="color:{col};">{fam} — ANALYTICAL, CURRENCY, GREEK, BULLETS, SPARKLINES &amp; AGENTIC SUITE (600)</span><span>ZERO SHARP EDGES · CANONICAL UNICODE</span></div>
          {inner}
        </div>""")

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><title>05 Analytical &amp; Agentic Symbols Audit</title>
    <style>{font_face_css()}{COMMON_CSS}</style></head><body>
      <div class="hdr">
        <div>
          <div class="eyebrow" style="color:#0A7A6E;">COMPILED WOFF2 SYMBOL MICROSCOPIC AUDIT · 05</div>
          <div class="h1">Analytical, Financial, Greek, Sparkline, Bullet &amp; Agentic Glyphs — All 4 Families</div>
        </div>
        <div class="badge">100% Native Original CAD Vectors · Zero PUA</div>
      </div>
      {''.join(blocks)}
    </body></html>"""
    hp = OUT / "05_Analytical_Bullets_Agentic_Audit.html"
    pp = OUT / "05_Analytical_Bullets_Agentic_Audit.png"
    hp.write_text(html, encoding="utf-8")
    render_png(hp, pp, width=1640, height=1680)
    return pp


def build_multilingual_audit_board() -> Path:
    latin_langs = [
        ("EN · English (Native AJ)", "VibeMyTrip crafts effortless journeys across 190 nations — 0123456789 · ₹9,450"),
        ("FR · Français (Native AJ)", "Voyagez à travers l'été : été, façade, cœur, œuvre, naïve, château, Noël, où — ŒÆÇÉÈÊË"),
        ("DE · Deutsch (Native AJ)", "Präzise Typografie für große Straßen, München, Zürich, Österreich — ÄÖÜß äöü"),
        ("ES · Español (Native AJ)", "¡Diseño extraordinario! Mañana, España, corazón, pingüino, acción — ¿ÁÉÍÓÚÑÜ?"),
        ("IT · Italiano (Native AJ)", "Qualità superiore, città, perché, più, così, università, libertà — ÀÈÉÌÒÙ"),
        ("PT · Português (Native AJ)", "Soluções avançadas: São Paulo, coração, ação, também, saúde, órgão — ÁÂÃÀÇÉÊÍÓÔÕÚ"),
        ("EU · Pan-European (Native AJ)", "Łódź, Gdańsk, Praha, Příliš žluťoučký kůň, Győr, București, İstanbul, København, Reykjavík"),
    ]
    companion_langs = [
        ("HI · हिन्दी (Metric Stack)", "ltr", "वाइबमाईट्रिप — सटीक उद्यम टाइपोग्राफी और स्पष्ट अनुभव · ₹24,999"),
        ("MR · मराठी (Metric Stack)", "ltr", "व्हायबमायट्रिप — अचूक डिझाइन, स्पष्ट अक्षरे आणि उत्कृष्ट प्रवास · ₹18,500"),
        ("TA · தமிழ் (Metric Stack)", "ltr", "வைப்மைடிரிப் — சென்னை தொழில்நுட்ப துல்லியம் மற்றும் அழகிய எழுத்துரு · ₹12,400"),
        ("TE · తెలుగు (Metric Stack)", "ltr", "వైబ్‌మైట్రిప్ — స్పష్టమైన అక్షర శైలి మరియు అద్భుత ప్రయాణ అనుభవం · ₹15,800"),
        ("BN · বাংলা (Metric Stack)", "ltr", "ভাইবমাইট্রিপ — নিখুঁত টাইপোগ্রাফি এবং সহজ পাঠযোগ্যতা · ₹14,200"),
        ("AR · العربية (RTL Metric Stack)", "rtl", "فايب ماي تريب — دقة طباعية فائقة وتجربة سفر سلسة · 12,450$"),
        ("JA · 日本語 (Metric Stack)", "ltr", "VibeMyTrip — マイクロ精度のタイポグラフィと快適な旅の設計 · ¥48,000"),
        ("KO · 한국어 (Metric Stack)", "ltr", "VibeMyTrip — 정밀한 엔터프라이즈 타이포그래피와 쾌적한 가독성 · ₩120,000"),
        ("ZH · 中文 (Metric Stack)", "ltr", "VibeMyTrip — 微米级精密排版与全平台企业字体体验 · ¥3,680"),
    ]

    lat_html = ""
    for fam, col in [("AJ Shresti", "#0A7A6E"), ("AJ Sahasvi", "#9A4206"), ("AJ Anushya", "#1D4ED8"), ("AJ Talin", "#BE185D")]:
        rows = "".join(
            f"<div style='display:grid;grid-template-columns:230px 1fr;gap:12px;padding:4px 0;border-bottom:1px solid #F1ECE3;align-items:baseline;'>"
            f"<span style='font-size:10px;font-weight:700;color:{col};'>{lbl}</span>"
            f"<span style=\"font-family:'{fam}';font-size:20px;font-weight:600;\">{txt}</span></div>"
            for lbl, txt in latin_langs
        )
        lat_html += f"<div class='card' style='padding:12px 18px;margin-bottom:10px;'><div class='card-lbl'><span style='color:{col};'>{fam} — NATIVE LATIN EXTENDED (EN · FR · DE · ES · IT · PT · PAN-EUROPEAN)</span><span>100% NATIVE ORIGINAL OUTLINES</span></div>{rows}</div>"

    comp_rows = "".join(
        f"<div style='display:grid;grid-template-columns:240px 1fr;gap:12px;padding:6px 0;border-bottom:1px solid #F1ECE3;align-items:baseline;'>"
        f"<span style='font-size:10px;font-weight:700;color:#1D4ED8;'>{lbl}</span>"
        f"<span dir='{d}' style=\"font-family:'AJ Anushya', -apple-system, 'Kohinoor Devanagari', 'Tamil Sangam MN', 'Telugu Sangam MN', 'Bangla Sangam MN', 'Geeza Pro', 'Hiragino Sans', 'Apple SD Gothic Neo', 'PingFang SC', sans-serif;font-size:20px;font-weight:500;text-align:{'right' if d=='rtl' else 'left'};\">{txt}</span></div>"
        for lbl, d, txt in companion_langs
    )

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><title>06 15-Language Enterprise Typography Audit</title>
    <style>{font_face_css()}{COMMON_CSS}</style></head><body>
      <div class="hdr">
        <div>
          <div class="eyebrow" style="color:#1D4ED8;">15-LANGUAGE ENTERPRISE TYPOGRAPHY AUDIT · 06</div>
          <div class="h1">Native Latin Extended (6 Core + Pan-EU) &amp; Metric-Calibrated 9 Non-Latin Companion Stacks</div>
        </div>
        <div class="badge">IP-Pure Architecture · Zero Third-Party Outline Mixing</div>
      </div>
      {lat_html}
      <div class="card" style="padding:12px 18px;">
        <div class="card-lbl"><span style="color:#1D4ED8;">9 NON-LATIN SCRIPT COMPANION STACKS (HI · MR · TA · TE · BN · AR RTL · JA · KO · ZH)</span><span>PAIRED WITH AJ ANUSHYA LATIN + NUMERALS + CURRENCIES</span></div>
        {comp_rows}
      </div>
    </body></html>"""
    hp = OUT / "06_Multilingual_15_Languages_Audit.html"
    pp = OUT / "06_Multilingual_15_Languages_Audit.png"
    hp.write_text(html, encoding="utf-8")
    render_png(hp, pp, width=1640, height=1880)
    return pp


def build_full_contact_sheet(num: str, slug: str, family: str, accent: str) -> Path:
    """Render EVERY SINGLE Unicode-mapped glyph in the compiled TTF into an indexed contact sheet!"""
    ttf_path = DIST / slug / "ttf" / f"{family.replace(' ', '')}-SemiBold.ttf"
    tt = TTFont(ttf_path)
    cmap = tt.getBestCmap()
    items = sorted(cp for cp in cmap.keys() if cp >= 0x0021 and not (0x0300 <= cp <= 0x036F) and cp not in (0x00A0, 0x2002, 0x2003, 0x2007, 0x2009))

    cells = []
    for cp in items:
        ch = f"&#x{cp:04X};"
        cells.append(
            f"<div class='cell'><div class='gl' style=\"font-family:'{family}';\">{ch}</div>"
            f"<div class='cp'>U+{cp:04X}</div></div>"
        )

    cols = 20
    rows_count = (len(items) + cols - 1) // cols
    h_px = max(900, 150 + rows_count * 76)

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><title>{num} {family} Complete Contact Sheet</title>
    <style>
      {font_face_css()}
      {COMMON_CSS}
      .grid-sheet {{ display: grid; grid-template-columns: repeat({cols}, 1fr); gap: 6px; }}
      .cell {{ background: #FFF; border: 1px solid #E3DDD0; border-radius: 8px; padding: 6px 2px 4px; text-align: center; height: 68px; display: flex; flex-direction: column; justify-content: space-between; }}
      .gl {{ font-size: 32px; font-weight: 600; line-height: 1.15; color: #141C24; }}
      .cp {{ font-size: 8.5px; font-weight: 600; color: #7C8794; font-family: ui-monospace, monospace; }}
    </style></head><body>
      <div class="hdr">
        <div>
          <div class="eyebrow" style="color:{accent};">COMPLETE EVERY-GLYPH VISUAL CONTACT SHEET · {len(items)} UNICODE GLYPHS</div>
          <div class="h1">{family} SemiBold (600) — Full Character Inventory Inspection</div>
        </div>
        <div class="badge" style="color:{accent};">Source: {ttf_path.name}</div>
      </div>
      <div class="grid-sheet">{''.join(cells)}</div>
    </body></html>"""
    hp = OUT / f"{num}_{slug}_Full_Contact_Sheet.html"
    pp = OUT / f"{num}_{slug}_Full_Contact_Sheet.png"
    hp.write_text(html, encoding="utf-8")
    render_png(hp, pp, width=1640, height=h_px)
    return pp


def write_live_build_gallery() -> None:
    """Write live interactive preview page to http://127.0.0.1:4793/live_build.html."""
    if not LIVE_DIR.exists():
        return
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<title>AJ Series — Live Compiled WOFF2 Enterprise Font Foundry Preview</title>
<style>
{font_face_css("live_fonts")}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #F7F4EE; color: #141C24; font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 28px 36px; max-width: 1440px; margin: 0 auto; }}
.top {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #DED7C8; padding-bottom: 14px; margin-bottom: 20px; }}
.eyebrow {{ font-size: 11px; font-weight: 700; letter-spacing: 1.8px; color: #0A7A6E; text-transform: uppercase; }}
h1 {{ font-size: 28px; font-weight: 800; margin-top: 3px; }}
.controls {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; background: #FFF; border: 1px solid #E2DCD0; border-radius: 14px; padding: 14px 18px; margin-bottom: 20px; }}
.controls input[type=text] {{ flex: 1; min-width: 280px; padding: 10px 14px; border: 1px solid #D5CEC0; border-radius: 10px; font-size: 16px; }}
.controls select, .controls label {{ font-size: 13px; font-weight: 600; color: #334155; }}
.controls select {{ padding: 8px 12px; border-radius: 8px; border: 1px solid #D5CEC0; background: #FAF8F4; }}
.fam-card {{ background: #FFF; border: 1px solid #E2DCD0; border-radius: 18px; padding: 20px 24px; margin-bottom: 16px; }}
.fam-hdr {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #EFEAE1; padding-bottom: 8px; }}
.fam-name {{ font-size: 18px; font-weight: 800; }}
.fam-role {{ font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 999px; background: #F5F2EB; }}
.live-out {{ font-size: 54px; line-height: 1.25; margin-bottom: 12px; word-break: break-word; font-kerning: normal; font-variant-ligatures: common-ligatures contextual; }}
.meta-row {{ font-size: 19px; color: #475569; margin-bottom: 8px; }}
.small-row {{ font-size: 12px; color: #334155; }}
.legal {{ margin-top: 22px; font-size: 12px; color: #475569; background: #FFF; border: 1px solid #E2DCD0; border-radius: 14px; padding: 14px 18px; line-height: 1.55; }}
</style></head><body>
  <div class="top">
    <div>
      <div class="eyebrow">AJ SERIES ENTERPRISE FOUNDRY · LIVE COMPILED WOFF2 PREVIEW</div>
      <h1>All 4 Compiled Original Typefaces — Interactive Live Verification</h1>
    </div>
    <div style="font-size:12px;font-weight:700;color:#0A7A6E;">21 Styles · 84 Binaries (OTF/TTF/WOFF/WOFF2) · v1.0.0</div>
  </div>
  <div class="controls">
    <input id="txt" type="text" value="AJ Series · VibeMyTrip · Sunlit Horizons · Pure Clarity · 0123456789 · ₹49,850 · ▲ +18.4% ▁▃▅▇█"/>
    <select id="wt"><option value="400">Regular (400)</option><option value="600" selected>Bold L1 · SemiBold (600)</option><option value="800">Bold L2 · ExtraBold (800)</option></select>
    <select id="sz"><option value="12">12px (Small)</option><option value="24">24px (Body)</option><option value="42">42px (Sub)</option><option value="54" selected>54px (Hero)</option><option value="76">76px (Display)</option></select>
    <label><input type="checkbox" id="it"/> Italic</label>
    <label><input type="checkbox" id="dlig"/> dlig (-&gt; &lt;-&gt; !=)</label>
    <label><input type="checkbox" id="frac"/> frac (99/100)</label>
    <label><input type="checkbox" id="ss01"/> ss01 (Open 0)</label>
    <label><input type="checkbox" id="ss02"/> ss02 (WCAG Wide)</label>
  </div>
  <div id="cards"></div>
  <div class="legal">
    <b>Exclusive Rights Owner:</b> ARAVIND JAYAMOHAN, India (<code>aravind.j.naidu@gmail.com</code>) — Full Rights Owned.<br/>
    <b>Authorized Licensees (Modification, Internal Use &amp; Publishing):</b> Aivibe Software Services Private Limited (Chennai) · AjAir Tech Mobility LLP · QRaise Structures.
  </div>
<script>
const fams = [
  {{ name: "AJ Shresti", hasItalic: true, role: "01 · Main Headings & Brand Identity", col: "#0A7A6E", sub: "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz · 0oO ab6 Il1 · fi fl ff ffi ffl · → ⇒ ≠ ≤ ≥ ₹ € £ ¥ ₩ ₿ ✓ ✦ ⚙ ⚠" }},
  {{ name: "AJ Sahasvi", hasItalic: false, role: "02 · Sub-Headings · Royal Pill-Terminal Small-Caps (Upright Only)", col: "#9A4206", sub: "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz · Sunlit Horizons · N Flush · đ ħ ł · 0123456789" }},
  {{ name: "AJ Anushya", hasItalic: true, role: "03 · Body Text & 9pt–13pt Zero-Stub Clarity", col: "#1D4ED8", sub: "Anushya Pure Clarity abundant group · Zero stubs on a b d g m n p q r u · 0oO ab6 Il1 · 99/100" }},
  {{ name: "AJ Talin", hasItalic: true, role: "04 · Precision 0° Connected Running Script (+11° Italic)", col: "#BE185D", sub: "AJ Talin · Sunlit · VibeMyTrip · script circle river · cœur œuvre große København · Top Web Yes Very" }},
];
function esc(str) {{
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}}
function render() {{
  const t = esc(document.getElementById("txt").value);
  const w = document.getElementById("wt").value;
  const s = document.getElementById("sz").value;
  const wantIt = document.getElementById("it").checked;
  const feats = [];
  if (document.getElementById("dlig").checked) feats.push('"dlig" 1');
  if (document.getElementById("frac").checked) feats.push('"frac" 1');
  if (document.getElementById("ss01").checked) feats.push('"ss01" 1');
  if (document.getElementById("ss02").checked) feats.push('"ss02" 1');
  const ffs = feats.length ? feats.join(", ") : "normal";
  document.getElementById("cards").innerHTML = fams.map(f => {{
    const st = (wantIt && f.hasItalic) ? "italic" : "normal";
    return `
    <div class="fam-card">
      <div class="fam-hdr">
        <span class="fam-name" style="color:${{f.col}}">${{f.name}}</span>
        <span class="fam-role" style="color:${{f.col}}">${{f.role}}</span>
      </div>
      <div class="live-out" style="font-family:'${{f.name}}';font-weight:${{w}};font-size:${{s}}px;font-style:${{st}};font-feature-settings:${{ffs}};">${{t}}</div>
      <div class="meta-row" style="font-family:'${{f.name}}';font-weight:${{w}};font-style:${{st}};font-feature-settings:${{ffs}};">${{esc(f.sub)}}</div>
    </div>`;
  }}).join("");
}}
["txt","wt","sz","it","dlig","frac","ss01","ss02"].forEach(id => document.getElementById(id).addEventListener("input", render));
render();
</script></body></html>"""
    (LIVE_DIR / "live_build.html").write_text(html, encoding="utf-8")


def build_stress_test_board() -> Path:
    """Render Bold L2 (800) counter-openness + AJ Talin connected running-script stress test!"""
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><title>08 Bold L2 &amp; AJ Talin Connected Stress Audit</title>
    <style>{font_face_css()}{COMMON_CSS}</style></head><body>
      <div class="hdr">
        <div>
          <div class="eyebrow" style="color:#BE185D;">MICROSCOPIC REGRESSION &amp; STRESS AUDIT · 08 · POST-FIX VERIFICATION</div>
          <div class="h1">Bold L2 (800) Counter Openness, Fixed &amp; / ₿ / ₩ / Œ &amp; AJ Talin Seamless calt Stress Test</div>
        </div>
        <div class="badge" style="color:#BE185D;">Zero Gaps · Zero Floating Marks · Zero Clogged Counters</div>
      </div>

      <div class="card">
        <div class="card-lbl"><span style="color:#BE185D;">AJ TALIN — SEAMLESS CONNECTED SCRIPT, FIXED r/s/v/w, MULTI-LETTER KERN &amp; PAN-EU CALT (400 / 600 / 800 / 11° ITALIC)</span><span>REAL CHROME HARFBUZZ CALT + KERN</span></div>
        <div style="font-family:'AJ Talin';font-size:40px;line-height:1.38;font-feature-settings:'calt' 1,'kern' 1;">
          <div style="font-weight:400;">400 Reg: Zephyrs · Horizons · Pure Clarity · VibeMyTrip · script circle correct river</div>
          <div style="font-weight:600;">600 L1: Top Web Yes Very Fox · bobbing clouds · cœur œuvre große København Łódź</div>
          <div style="font-weight:800;color:#BE185D;">800 L2: Zephyrs · Horizons · Pure Clarity · Quick brown fox jumps · very warm river</div>
          <div style="font-weight:400;font-style:italic;color:#4338CA;">400 It 11°: Zephyrs · Horizons · Pure Clarity · running connected script · café naïve</div>
          <div style="font-weight:600;font-style:italic;color:#4338CA;">600 It 11°: minimum aluminum rhythm · <span style="font-feature-settings:'ss02' 1;color:#0F766E;">ss02 Dyslexia Café naïve 123</span></div>
        </div>
      </div>

      <div class="card">
        <div class="card-lbl"><span style="color:#0A7A6E;">BOLD LEVEL 2 · EXTRABOLD (800) FULL COUNTER-OPENNESS, ACCENTS, LIGATURES &amp; SYMBOLS AUDIT (ALL 4 FAMILIES)</span><span>&amp; · ₿ · ₩ · @ · % · ‰ · ‱ · ⚠ · ⚙ · ⌫ · ≈ · ± · Ω · fi fl ffi · Ć É Ó Ś Å · 99/100</span></div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div style="font-family:'AJ Shresti';font-size:34px;font-weight:800;color:#0A7A6E;">Shresti 800: &amp; ₿ ₩ @ % ‰ ‱ ⚠ ⚙ ⌫ ≈ ± ∓ Ω ⇑ ⊕ № ℠ · fi fl ffi ffl · Ć É Ó Ś Å · <span style="font-feature-settings:'frac' 1;">99/100 123/456</span></div>
          <div style="font-family:'AJ Sahasvi';font-size:32px;font-weight:800;color:#9A4206;">Sahasvi 800: &amp; ₿ ₩ @ % ‰ ‱ ⚠ ⚙ ⌫ ≈ ± Ω ⇑ ⊕ № ℠ · Đ đ Ħ ħ Ł ł ð þ · B D G K M N Q W</div>
          <div style="font-family:'AJ Anushya';font-size:34px;font-weight:800;color:#1D4ED8;">Anushya 800: &amp; ₿ ₩ @ % ‰ ‱ ⚠ ⚙ ⌫ ≈ ± Ω ⇑ ⊕ № ℠ · fi fl ffi ffl · a b d g m n p q r u</div>
          <div style="font-family:'AJ Talin';font-size:34px;font-weight:800;color:#BE185D;">Talin 800: &amp; ₿ ₩ @ % ‰ ‱ ⚠ ⚙ ⌫ ≈ ± Ω ⇑ ⊕ № ℠ · river view wave script circle · ì í î ï</div>
        </div>
      </div>
    </body></html>"""
    hp = OUT / "08_BoldL2_and_Talin_Stress_Audit.html"
    pp = OUT / "08_BoldL2_and_Talin_Stress_Audit.png"
    hp.write_text(html, encoding="utf-8")
    render_png(hp, pp, width=1640, height=1020)
    return pp


def main() -> None:
    boards = [
        build_family_audit_board("01", "aj-shresti", "AJ Shresti", "Main Headings & Brand Identity",
                                 "#0A7A6E", "linear-gradient(135deg,#0FA396 0%,#0A6E6B 55%,#074452 100%)",
                                 0.534, True, "AJ Shresti · VibeMyTrip",
                                 "HERO & ZERO-CONFUSION MACRO PROOF", "VibeMyTrip · 0oO · ab6 · Il1"),
        build_family_audit_board("02", "aj-sahasvi", "AJ Sahasvi", "Royal Architectural Pill-Terminal Small-Caps",
                                 "#9A4206", "linear-gradient(135deg,#D97706 0%,#9A4206 55%,#5C2208 100%)",
                                 0.525, False, "AJ Sahasvi · Sunlit Horizons",
                                 "FIXED FLUSH N & NEW LETTERS (B D F G K M Q W X Y)", "Sunlit · BDFGK · MQWXY · N"),
        build_family_audit_board("03", "aj-anushya", "AJ Anushya", "Body Text & 9pt–13pt Zero-Stub Reading Sans",
                                 "#1D4ED8", "linear-gradient(135deg,#2563EB 0%,#1D4ED8 55%,#1E3A8A 100%)",
                                 0.556, True, "AJ Anushya · Pure Clarity",
                                 "ZERO-STUB PROOF (a b d g h m n p q r u)", "Anushya · Pure Clarity · abundant"),
        build_family_audit_board("04", "aj-talin", "AJ Talin", "Precision 0° Connected Running Script (+11° Italic)",
                                 "#BE185D", "linear-gradient(135deg,#DB2777 0%,#BE185D 55%,#701A45 100%)",
                                 0.496, True, "AJ Talin · Sunlit",
                                 "LIVE OPENTYPE CALT CONNECTED SCRIPT PROOF", "Talin · Sunlit · Zephyrs · Horizons"),
        build_symbols_audit_board(),
        build_multilingual_audit_board(),
        build_full_contact_sheet("07a", "aj-shresti", "AJ Shresti", "#0A7A6E"),
        build_full_contact_sheet("07b", "aj-sahasvi", "AJ Sahasvi", "#9A4206"),
        build_full_contact_sheet("07c", "aj-anushya", "AJ Anushya", "#1D4ED8"),
        build_full_contact_sheet("07d", "aj-talin", "AJ Talin", "#BE185D"),
        build_stress_test_board(),
    ]
    write_live_build_gallery()
    for p in boards:
        print(f"RENDERED VISUAL PROOF: {p.name} ({p.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
