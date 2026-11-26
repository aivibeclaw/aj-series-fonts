#!/usr/bin/env python3
"""Render Native macOS CoreText Proof Board (`specimens/v3_5families_multilingual_proof.png`)
directly from compiled `dist/` TTF binaries with strict ZERO-SYSTEM-FALLBACK verification!
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/aj/Dev-Apps/AJ-Series-Fonts")
OUT_PNG = ROOT / "specimens" / "v3_5families_multilingual_proof.png"

SWIFT_SRC = r'''
import Foundation
import CoreText
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let root = URL(fileURLWithPath: CommandLine.arguments[1])
let outPath = URL(fileURLWithPath: CommandLine.arguments[2])

func loadFont(_ relPath: String, _ size: CGFloat) -> (CTFont, String) {
    let url = root.appendingPathComponent(relPath) as CFURL
    guard let arr = CTFontManagerCreateFontDescriptorsFromURL(url) as? [CTFontDescriptor],
          let desc = arr.first else {
        fatalError("Failed to load font at \(relPath)")
    }
    let noFallbackAttrs: [CFString: Any] = [
        kCTFontCascadeListAttribute: [] as [CTFontDescriptor]
    ]
    let cleanDesc = CTFontDescriptorCreateCopyWithAttributes(desc, noFallbackAttrs as CFDictionary)
    let f = CTFontCreateWithFontDescriptor(cleanDesc, size, nil)
    let ps = CTFontCopyPostScriptName(f) as String
    return (f, ps)
}

let W = 1640
let H = 1360
let cs = CGColorSpaceCreateDeviceRGB()
let ctx = CGContext(
    data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
    space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
)!

func rgb(_ r: CGFloat, _ g: CGFloat, _ b: CGFloat) -> CGColor {
    return CGColor(red: r/255.0, green: g/255.0, blue: b/255.0, alpha: 1.0)
}

ctx.setFillColor(rgb(246, 244, 238))
ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))

var fallbackViolations: [String] = []

func drawStrict(_ text: String, _ fontPair: (CTFont, String), _ x: CGFloat, _ y: CGFloat, _ color: CGColor) -> CGFloat {
    let attrs: [CFString: Any] = [
        kCTFontAttributeName: fontPair.0,
        kCTForegroundColorAttributeName: color
    ]
    let astr = CFAttributedStringCreate(nil, text as CFString, attrs as CFDictionary)!
    let line = CTLineCreateWithAttributedString(astr)
    let runs = CTLineGetGlyphRuns(line) as! [CTRun]
    for run in runs {
        let rAttrs = CTRunGetAttributes(run) as NSDictionary
        let rf = rAttrs[kCTFontAttributeName] as! CTFont
        let rps = CTFontCopyPostScriptName(rf) as String
        if rps != fontPair.1 {
            fallbackViolations.append("Expected \(fontPair.1), got \(rps) in: \(text)")
        }
        let cnt = CTRunGetGlyphCount(run)
        var glyphs = [CGGlyph](repeating: 0, count: cnt)
        CTRunGetGlyphs(run, CFRangeMake(0, cnt), &glyphs)
        if glyphs.contains(0) {
            fallbackViolations.append("Missing glyph (.notdef) in \(fontPair.1) for: \(text)")
        }
    }
    ctx.textPosition = CGPoint(x: x, y: y)
    CTLineDraw(line, ctx)
    return CGFloat(CTLineGetTypographicBounds(line, nil, nil, nil))
}

let cNavy = rgb(18, 36, 76)
let cInk  = rgb(16, 22, 34)
let cMute = rgb(72, 82, 96)
let cTeal = rgb(12, 84, 68)

var y: CGFloat = CGFloat(H - 56)

// Header
_ = drawStrict(
    "AJ SERIES ENTERPRISE TYPEFACES & AAAHHH FONTS VIBE — v3.0.0 NATIVE CORETEXT PROOF",
    loadFont("dist/aj-sahasvi/ttf/AJSahasvi-ExtraBold.ttf", 25),
    40, y, cNavy
)
y -= 28
_ = drawStrict(
    "5 Handcrafted Families · 27 Styles · 4,513 Codepoints · Dark-Safe 3D Mild-Gradient (COLRv1 + COLRv0 + SVG, 108/108) · 24+ Languages",
    loadFont("dist/aj-shresti/ttf/AJShresti-SemiBold.ttf", 14.5),
    40, y, cMute
)

// 5 Families Weight Progression
y -= 42
let fams: [(String, String, String)] = [
    ("1. AJ Sahasvi (Display)", "aj-sahasvi", "AJSahasvi"),
    ("2. AJ Shresti (System UI)", "aj-shresti", "AJShresti"),
    ("3. AJ Anushya (Clarity)", "aj-anushya", "AJAnushya"),
    ("4. AJ Talin (Script)", "aj-talin", "AJTalin"),
    ("5. Aaahhh Fonts Vibe", "aaahhh-fonts-vibe", "AaahhhFontsVibe")
]
for (lbl, slug, pfx) in fams {
    _ = drawStrict("\(lbl) 400: Sovereign Clarity Rs1,250", loadFont("dist/\(slug)/ttf/\(pfx)-Regular.ttf", 19), 40, y, cInk)
    _ = drawStrict("600 SemiBold: வணக்கம் नमस्ते", loadFont("dist/\(slug)/ttf/\(pfx)-SemiBold.ttf", 19), 700, y, cInk)
    _ = drawStrict("800 ExtraBold: ULTRA CLEAR", loadFont("dist/\(slug)/ttf/\(pfx)-ExtraBold.ttf", 19), 1140, y, cInk)
    y -= 38
}

// Sound of Font Section
y -= 18
_ = drawStrict(
    "SOUND OF FONT (AAAHHH FONTS VIBE) — OPENTYPE GSUB INLINE TRIGGERS & STRICT NUMERIC GUARDS",
    loadFont("dist/aj-sahasvi/ttf/AJSahasvi-ExtraBold.ttf", 18.5),
    40, y, cTeal
)
y -= 28
_ = drawStrict(
    "Typed ASCII:   :ta:vanakkam  :ta:1u  :ta:nandri   |   Guards:  1   Rs1   $1u   No. 1   |   :hi:namaste  :hi:dhanyavad   |   :pa:satsriakal",
    loadFont("dist/aj-anushya/ttf/AJAnushya-Regular.ttf", 14.5),
    40, y, cMute
)
y -= 32
_ = drawStrict(
    "Shaped Vibe:  :ta:vanakkam  :ta:1u  :ta:nandri  |  Guards: 1  Rs1  $1u  No. 1  |  :hi:namaste  :hi:dhanyavad  |  :pa:satsriakal",
    loadFont("dist/aaahhh-fonts-vibe/ttf/AaahhhFontsVibe-SemiBold.ttf", 22),
    40, y, cInk
)
y -= 34
_ = drawStrict(
    "More Scripts:  :te:namaskaram  :ml:namaskaram  :kn:namaskara  :bn:nomoshkar  :zh:nihao  :th:sawatdee  :am:selam  :ja:konnichiwa  :ru:privet",
    loadFont("dist/aaahhh-fonts-vibe/ttf/AaahhhFontsVibe-Regular.ttf", 20),
    40, y, cInk
)

// 24+ Global Languages Section
y -= 44
_ = drawStrict(
    "24+ GLOBAL LANGUAGES ACROSS 14 WORLD SCRIPT SYSTEMS (ZERO SYSTEM FALLBACK)",
    loadFont("dist/aj-sahasvi/ttf/AJSahasvi-ExtraBold.ttf", 18.5),
    40, y, cNavy
)
y -= 32

let bodyFont = loadFont("dist/aj-anushya/ttf/AJAnushya-Regular.ttf", 20.5)
let langRows: [String] = [
    "EN / ES / FR / DE / MS: Clear Comfort Typography · Español Diseño · Français Élégance · Deutsch Präzision · Selamat Pagi Singapura",
    "Tamil & Sen Tamil (ta): வணக்கம் தமிழ் எழுத்து · ௐ வாழ்க செந்தமிழ் ௰ ௱ ௲ ௹ · ஒன்று இரண்டு மூன்று நன்றி",
    "Hindi / Marathi / Sanskrit (Devanagari): नमस्ते भारत · धन्यवाद · नमस्कार महाराष्ट्र · सत्यमेव जयते संस्कृतम्",
    "Telugu (te — joined talakattu): నమస్కారం తెలుగు అక్షరమాల · ధన్యవాదాలు · సెలవు దరఖాస్తు",
    "Malayalam & Kannada (ml / kn): നമസ്കാരം മലയാളം നന്ദി · ನಮಸ್ಕಾರ ಕನ್ನಡ ಧನ್ಯವಾದ",
    "Bengali & Gurmukhi Punjabi (bn / pa): নমস্কার বাংলা ধন্যবাদ ৳ · ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਪੰਜਾਬੀ ਧੰਨਵਾਦ ੴ",
]
for r in langRows {
    _ = drawStrict(r, bodyFont, 40, y, cInk)
    y -= 38
}

// Arabic & Urdu RTL row (explicit label + clean RTL run so word order & joining are 100% natural!)
let wLbl = drawStrict("Arabic & Urdu RTL (ar / ur): ", bodyFont, 40, y, cInk)
_ = drawStrict("السلام علیکم اردو شکریہ · بھائی گھر کچھ · السلام عليكم ورحمة الله شكرا", bodyFont, 40 + wLbl + 8, y, cInk)
y -= 38

let langRows2: [String] = [
    "Russian Cyrillic (ru): Здравствуйте Мир · Чистая Типографика Спасибо Пожалуйста",
    "Japanese & Chinese (ja / zh): こんにちは カタカナ ヴ 東京 日本語 大阪 · 你好世界 不客气 再见 批准 帮助 非常 感谢",
    "Korean Hangul (ko): 안녕하세요 한국어 감사합니다 휴가 신청서 승인",
    "Thai & Amharic Ethiopic (th / am): สวัสดี ภาษาไทย ขอบคุณ ใบลา · ሰላም ኢትዮጵያ ሥራ ዓለም ጨረቃ ጸሐይ ነፃ ፩፪፫፬፭",
]
for r in langRows2 {
    _ = drawStrict(r, bodyFont, 40, y, cInk)
    y -= 38
}

// Low-Res & OCR Clarity Ladder
y -= 16
_ = drawStrict(
    "LOW-RESOLUTION & NEURAL OCR CLARITY LADDER (16PX · 12PX · 10PX — 0I1L / O0 / B8 / S5 / Rs1,080.50)",
    loadFont("dist/aj-sahasvi/ttf/AJSahasvi-ExtraBold.ttf", 17.5),
    40, y, cNavy
)
y -= 28
_ = drawStrict(
    "16px AJ Anushya: 0O1Il B8 S5 Z2 Rs1,080.50 INV-2026-0049 | வணக்கம் ஒன்று नमस्ते धन्यवाद महाराष्ट्र ನಮಸ್ಕಾರ നന്ദി شکریہ สวัสดี 你好 ሰላም",
    loadFont("dist/aj-anushya/ttf/AJAnushya-Regular.ttf", 16),
    40, y, cInk
)
y -= 24
_ = drawStrict(
    "12px Aaahhh Vibe: 0O1Il B8 S5 Z2 Rs1,080.50 INV-2026-0049 | வணக்கம் ஒன்று नमस्ते धन्यवाद महाराष्ट्र ನಮಸ್ಕಾರ നന്ദി شکریہ สวัสดี 你好 ሰላም",
    loadFont("dist/aaahhh-fonts-vibe/ttf/AaahhhFontsVibe-Regular.ttf", 12),
    40, y, cInk
)
y -= 20
_ = drawStrict(
    "10px AJ Shresti SemiBold: 0O1Il B8 S5 Z2 Rs1,080.50 INV-2026-0049 | வணக்கம் ஒன்று नमस्ते धन्यवाद महाराष्ट्र ನಮಸ್ಕಾರ നന്ദി شکریہ สวัสดี 你好 ሰላም",
    loadFont("dist/aj-shresti/ttf/AJShresti-SemiBold.ttf", 10),
    40, y, cInk
)

if !fallbackViolations.isEmpty {
    for v in fallbackViolations {
        fputs("FALLBACK VIOLATION: \(v)\n", stderr)
    }
    exit(2)
}

let img = ctx.makeImage()!
let dest = CGImageDestinationCreateWithURL(outPath as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, img, nil)
CGImageDestinationFinalize(dest)
print("Rendered zero-fallback CoreText proof -> \(outPath.path)")
'''


def main() -> None:
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".swift", delete=False, encoding="utf-8") as f:
        f.write(SWIFT_SRC)
        swift_path = Path(f.name)
    try:
        subprocess.run(["swift", str(swift_path), str(ROOT), str(OUT_PNG)], check=True)
    finally:
        swift_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
