"""Deep Verification Suite for Compiled v3.0.0 Font Binaries, HarfBuzz Shaping, Weight Steps & Low-Res Clarity.

Tests the REAL compiled OTF/TTF/WOFF/WOFF2 binaries in `dist/` across all 5 canonical families (27 styles / 108 binaries):
  1. Complete 5-family, 27-style, 108-binary & 27-UFO3 inventory + legal `name` & `fsType=0` verification
  2. Hybrid COLRv1 (`PaintLinearGradient` mild gradient) + COLRv0 + CPAL + SVGZ `<linearGradient>` verification
  3. Real HarfBuzz (`uharfbuzz`) OpenType shaping of `Aaahhh Fonts Vibe`:
     - Default English untouched (`vanakkam 1 Rs1` stays ASCII)
     - Inline `:ta:vanakkam`, `:ta:1u`, `:hi:namaste`, `:ml:namaskaram`, `:kn:namaskara`, `:ru:privet`, `:ja:konnichiwa`
     - `ss06` Tamil Sound-of-Font mode: `vanakkam`/`vanakam` -> `_snd_ta_vanakkam`, `1u`/`onnu`/`ondru` -> `_snd_ta_ondru`,
       while standalone `1`, `Rs1`, `Rs1u`, and `21u` stay strictly unconverted!
  4. Visible ink-density progression (`Regular 400 < SemiBold 600 < ExtraBold 800`, Regular non-thin) across Latin & world scripts
  5. Low-resolution (`12px`, `16px`, `32px`) glyph disambiguation (`0/O/o`, `I/l/1`, `a/o`) across all 5 families
"""
from __future__ import annotations

import pathlib
import sys
import unittest

import numpy as np
import ots
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DIST = ROOT / "dist"

EXPECTED_FAMILIES = {
    "aj-shresti": ("AJShresti", 6),
    "aj-sahasvi": ("AJSahasvi", 3),
    "aj-anushya": ("AJAnushya", 6),
    "aj-talin": ("AJTalin", 6),
    "aaahhh-fonts-vibe": ("AaahhhFontsVibe", 6),
}


def _ink_sum(ttf_path: pathlib.Path, text: str, px: int = 42) -> int:
    font = ImageFont.truetype(str(ttf_path), px)
    img = Image.new("L", (max(480, px * len(text) * 2), px * 3), 0)
    draw = ImageDraw.Draw(img)
    draw.text((20, px // 2), text, font=font, fill=255)
    arr = np.asarray(img, dtype=np.int64)
    return int(arr.sum())


def _glyph_bitmap_norm(ttf_path: pathlib.Path, ch: str, px: int = 16) -> np.ndarray:
    font = ImageFont.truetype(str(ttf_path), px)
    img = Image.new("L", (px * 3, px * 3), 0)
    draw = ImageDraw.Draw(img)
    draw.text((px // 2, px // 2), ch, font=font, fill=255)
    arr = (np.asarray(img) > 40).astype(np.float32)
    return arr


def _hb_shape_names(ttf_path: pathlib.Path, text: str, features: dict[str, bool] | None = None) -> list[str]:
    tt = TTFont(ttf_path)
    order = tt.getGlyphOrder()
    blob = hb.Blob.from_file_path(str(ttf_path))
    face = hb.Face(blob)
    font = hb.Font(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {})
    return [order[info.codepoint] for info in buf.glyph_infos]


class CompiledFontSuiteTests(unittest.TestCase):
    def test_01_complete_5_families_27_styles_108_binaries(self) -> None:
        total_bins = 0
        for slug, (_pfx, count) in EXPECTED_FAMILIES.items():
            for fmt in ("otf", "ttf", "woff", "woff2"):
                files = sorted((DIST / slug / fmt).glob(f"*.{fmt}"))
                self.assertEqual(len(files), count, f"{slug}/{fmt} expected {count}, got {len(files)}")
                for f in files:
                    self.assertGreater(f.stat().st_size, 50_000, f"{f} unexpectedly small")
                    total_bins += 1
        self.assertEqual(total_bins, 108)

    def test_02_ots_sanitize_and_legal_metadata(self) -> None:
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            reg_ttf = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            r = ots.sanitize(str(reg_ttf), capture_output=True)
            self.assertEqual(r.returncode, 0, f"OTS failed on {reg_ttf}: {r.stderr}")
            tt = TTFont(reg_ttf)
            self.assertEqual(tt["OS/2"].fsType, 0)
            cp_rec = tt["name"].getDebugName(0) or ""
            self.assertIn("Aravind Jayamohan", cp_rec)
            self.assertIn("Aivibe Software Services Private Limited", cp_rec)
            # Verify 14-script Unicode coverage (>= 4,250 codepoints!)
            cmap = tt.getBestCmap()
            self.assertGreaterEqual(len(cmap), 4250)
            for sample_ch in ("A", "₹", "வ", "न", "న", "ന", "ನ", "ন", "ਸ", "م", "ے", "П", "あ", "안", "你", "ก", "ሀ"):
                self.assertIn(ord(sample_ch), cmap, f"Missing {sample_ch} in {reg_ttf.name}")

    def test_03_default_3d_mild_gradient_colrv1_colrv0_svg(self) -> None:
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            ttf = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            tt = TTFont(ttf)
            self.assertIn("COLR", tt)
            self.assertIn("CPAL", tt)
            self.assertIn("SVG ", tt)
            self.assertEqual(tt["COLR"].version, 1)
            self.assertGreater(tt["COLR"].table.BaseGlyphRecordCount, 4000)
            self.assertGreater(tt["COLR"].table.BaseGlyphList.BaseGlyphCount, 4000)
            self.assertEqual(len(tt["CPAL"].palettes), 4)
            self.assertEqual(len(tt["CPAL"].palettes[0]), 7)
            self.assertTrue(tt["SVG "].docList[0].compressed)
            self.assertIn("linearGradient", tt["SVG "].docList[0].data)
            # Verify CoreText + Skia COLRv1 ColorStop.Alpha parity (prevents opaque white bleaching!)
            grad_paints = [
                p.Paint for p in tt["COLR"].table.LayerList.Paint if p.Paint.Format == 4
            ]
            self.assertGreater(len(grad_paints), 4000)
            gp0 = grad_paints[0]
            self.assertEqual(gp0.x0, gp0.x1, "Gradient vector must be strictly vertical (width-invariant)")
            stops = gp0.ColorLine.ColorStop
            self.assertAlmostEqual(stops[0].Alpha, 0.20, places=2)
            self.assertAlmostEqual(stops[1].Alpha, 0.02, places=2)
            self.assertAlmostEqual(stops[2].Alpha, 0.12, places=2)
            # Verify OTF/SVG <defs><path id="b..."/></defs> + dual <use> so SVG fill="url(#pg)" applies!
            self.assertIn('<use xlink:href="#b', tt["SVG "].docList[0].data)
            self.assertIn('fill="url(#pg)"', tt["SVG "].docList[0].data)

    def test_04_visible_weight_progression_regular_semibold_extrabold(self) -> None:
        samples = [
            ("Latin", "Hamburgefonstiv 012345"),
            ("Tamil", "வணக்கம் தமிழ்"),
            ("Hindi", "नमस्ते भारत"),
            ("Malayalam", "നമസ്കാരം"),
            ("Kannada", "ನಮಸ್ಕಾರ"),
            ("Cyrillic", "Привет Мир"),
            ("Chinese", "你好世界"),
        ]
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            reg = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            sb = DIST / slug / "ttf" / f"{pfx}-SemiBold.ttf"
            eb = DIST / slug / "ttf" / f"{pfx}-ExtraBold.ttf"
            for label, txt in samples:
                i_reg = _ink_sum(reg, txt)
                i_sb = _ink_sum(sb, txt)
                i_eb = _ink_sum(eb, txt)
                self.assertGreater(i_reg, 20_000, f"{pfx} Regular {label} is too thin!")
                self.assertGreater(i_sb, int(i_reg * 1.08), f"{pfx} SemiBold not visibly bolder than Regular on {label}: {i_reg} -> {i_sb}")
                self.assertGreater(i_eb, int(i_sb * 1.08), f"{pfx} ExtraBold not visibly bolder than SemiBold on {label}: {i_sb} -> {i_eb}")

    def test_05_aaahhh_fonts_vibe_harfbuzz_sound_of_font_shaping(self) -> None:
        vibe_ttf = DIST / "aaahhh-fonts-vibe" / "ttf" / "AaahhhFontsVibe-Regular.ttf"
        # 1. Default English mode: plain English, standalone 1, and Rs1 remain untouched
        self.assertEqual(_hb_shape_names(vibe_ttf, "1"), ["one"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "Rs1"), ["R", "s", "one"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "vanakkam"), list("vanakkam"))

        # 2. Inline `:lang:word` triggers work out-of-the-box in default calt!
        self.assertEqual(_hb_shape_names(vibe_ttf, ":ta:vanakkam"), ["_snd_ta_vanakkam"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":ta:1u"), ["_snd_ta_ondru"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":hi:namaste"), ["_snd_hi_namaste"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":ml:namaskaram"), ["_snd_ml_namaskaram"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":kn:namaskara"), ["_snd_kn_namaskara"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":ru:privet"), ["_snd_ru_privet"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":ja:konnichiwa"), ["_snd_ja_konnichiwa"])

        # 3. `ss06` Tamil Sound-of-Font Stylistic Set: phonetic conversion + strict numeric/currency guards!
        ta_feat = {"ss06": True}
        self.assertEqual(_hb_shape_names(vibe_ttf, "vanakkam", ta_feat), ["_snd_ta_vanakkam"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "vanakam", ta_feat), ["_snd_ta_vanakkam"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "1u", ta_feat), ["_snd_ta_ondru"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "onnu", ta_feat), ["_snd_ta_ondru"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "ondru", ta_feat), ["_snd_ta_ondru"])
        # Edge-case guards: standalone '1', 'Rs1', 'Rs1u', '21u', '$1u', '₹1u', 'Rs.1u', '2026-1u' MUST NOT convert!
        self.assertEqual(_hb_shape_names(vibe_ttf, "1", ta_feat), ["one"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "Rs1", ta_feat), ["R", "s", "one"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "Rs1u", ta_feat), ["R", "s", "one", "u"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "21u", ta_feat), ["two", "one", "u"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "$1u", ta_feat), ["dollar", "one", "u"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "₹1u", ta_feat), ["uni20B9", "one", "u"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "Rs.1u", ta_feat), ["R", "s", "period", "one", "u"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "2026-1u", ta_feat), ["two", "zero", "two", "six", "hyphen", "one", "u"])

    def test_08_zero_missing_lexicon_chars_across_all_24_languages(self) -> None:
        from sound_of_font.dictionaries.multilingual_lexicon import NUMBER_SOUNDS, TEMPLATES, WORDS

        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            cmap = TTFont(DIST / slug / "ttf" / f"{pfx}-Regular.ttf").getBestCmap()
            missing: list[tuple[str, str, str]] = []
            for lang in WORDS:
                for txt in (WORDS[lang], *TEMPLATES[lang].values(), *NUMBER_SOUNDS.get(lang, {}).values()):
                    for ch in txt:
                        if ord(ch) > 127 and ord(ch) not in cmap:
                            missing.append((lang, ch, f"U+{ord(ch):04X}"))
            self.assertEqual(missing, [], f"{pfx} missing lexicon chars: {missing[:10]}")

    def test_06_low_resolution_12px_16px_ocr_disambiguation(self) -> None:
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            reg = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            for px in (12, 16):
                b0 = _glyph_bitmap_norm(reg, "0", px)
                bO = _glyph_bitmap_norm(reg, "O", px)
                bI = _glyph_bitmap_norm(reg, "I", px)
                bl = _glyph_bitmap_norm(reg, "l", px)
                b1 = _glyph_bitmap_norm(reg, "1", px)
                self.assertGreater(b0.sum(), 4.0, f"{pfx} 0 vanished at {px}px!")
                self.assertGreater(b1.sum(), 4.0, f"{pfx} 1 vanished at {px}px!")
                # Ensure 0 != O and 1 != I and 1 != l at pixel level even at 12px!
                self.assertFalse(np.array_equal(b0, bO), f"{pfx} 0 identical to O at {px}px")
                self.assertFalse(np.array_equal(b1, bI), f"{pfx} 1 identical to I at {px}px")
                self.assertFalse(np.array_equal(b1, bl), f"{pfx} 1 identical to l at {px}px")

    def test_07_tesseract_lstm_ocr_accuracy_12px_to_32px(self) -> None:
        import difflib
        import shutil
        import subprocess
        import tempfile

        tess = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"
        if not pathlib.Path(tess).exists():
            self.skipTest("tesseract CLI not installed")
        sample = "Invoice Rs1250 Leave Request 2026 Clear Vision 100"
        with tempfile.TemporaryDirectory() as tmp:
            for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
                reg = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
                for px in (32, 16, 12):
                    fnt = ImageFont.truetype(str(reg), px)
                    im = Image.new("RGB", (max(780, px * 38), max(80, px * 4)), (255, 255, 255))
                    ImageDraw.Draw(im).text((24, max(16, px)), sample, fill=(15, 20, 30), font=fnt)
                    p = pathlib.Path(tmp) / f"{slug}_{px}.png"
                    im.save(p)
                    r = subprocess.run([tess, str(p), "stdout", "--oem", "1", "--psm", "7"], capture_output=True, text=True, check=True)
                    rec = r.stdout.strip()
                    a = sample.lower() if slug == "aj-sahasvi" else sample
                    b = rec.lower() if slug == "aj-sahasvi" else rec
                    ratio = difflib.SequenceMatcher(None, a, b).ratio()
                    self.assertGreaterEqual(ratio, 0.95, f"{pfx} OCR accuracy {ratio:.3f} < 0.95 at {px}px: {rec!r}")

    def test_09_os2_codepage_ranges_roman_cooltype_safe(self) -> None:
        cjk_thai_mask = (1 << 16) | (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20) | (1 << 21)
        checked = 0
        for slug, (_pfx, _cnt) in EXPECTED_FAMILIES.items():
            for fmt in ("otf", "ttf", "woff", "woff2"):
                for fp in sorted((DIST / slug / fmt).glob(f"*.{fmt}")):
                    tt = TTFont(fp)
                    os2 = tt["OS/2"]
                    self.assertEqual(os2.ulCodePageRange2, 0, f"{fp.name} ulCodePageRange2=0x{os2.ulCodePageRange2:08x} != 0")
                    self.assertEqual(os2.ulCodePageRange1 & cjk_thai_mask, 0, f"{fp.name} has CJK/Thai bits in ulCodePageRange1")
                    self.assertEqual(os2.ulCodePageRange1 & 1, 1, f"{fp.name} missing Latin-1 bit 0")
                    checked += 1
        self.assertEqual(checked, 108)

    def test_10_urdu_rtl_joining_and_seamless_baseline(self) -> None:
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            ttf = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            self.assertEqual(
                _hb_shape_names(ttf, "شکریہ"),
                ["arHehGoal.fina", "arFarsiYeh.init", "arReh.fina", "arKeheh.medi", "arSheen.init"],
            )
            self.assertEqual(
                _hb_shape_names(ttf, "علیکم"),
                ["arMeem.fina", "arKeheh.medi", "arFarsiYeh.medi", "arLam.medi", "arAin.init"],
            )
            self.assertIn("arHehDoachashmee.medi", _hb_shape_names(ttf, "بھائی"))
            self.assertIn("arGaf.init", _hb_shape_names(ttf, "گھر"))
            self.assertIn("arTcheh.medi", _hb_shape_names(ttf, "کچھ"))
            self.assertIn("arPeh.init", _hb_shape_names(ttf, "پاکستان"))
            self.assertIn("arTteh.init", _hb_shape_names(ttf, "ٹماٹر"))
            self.assertIn("arDdal", _hb_shape_names(ttf, "ڈاکٹر"))
            self.assertIn("arRreh", _hb_shape_names(ttf, "گاڑی"))
            self.assertEqual(_hb_shape_names(ttf, "ہاں"), ["arNoonGhunna", "arAlef.fina", "arHehGoal.init"])
            self.assertEqual(
                _hb_shape_names(ttf, "نہیں"),
                ["arNoonGhunna.fina", "arFarsiYeh.medi", "arHehGoal.medi", "arNoon.init"],
            )
            self.assertIn("arYehBarree.fina", _hb_shape_names(ttf, "لے"))
            tt = TTFont(ttf)
            self.assertEqual(tt["glyf"]["arHehGoal.fina"].numberOfContours, 1, f"{pfx} arHehGoal.fina has disconnected contours!")

    def test_11_devanagari_dvva_open_counter_and_maharashtra_conjunct(self) -> None:
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            for ttf in sorted((DIST / slug / "ttf").glob("*.ttf")):
                tt = TTFont(ttf)
                self.assertGreaterEqual(
                    tt["glyf"]["dvVa"].numberOfContours,
                    2,
                    f"{ttf.name} dvVa lost its open inner counter!",
                )
            reg = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            for px in (16, 32):
                b_va = _glyph_bitmap_norm(reg, "व", px)
                b_ba = _glyph_bitmap_norm(reg, "ब", px)
                self.assertFalse(np.array_equal(b_va, b_ba), f"{pfx} व identical to ब at {px}px")
            shaped_mh = _hb_shape_names(reg, "महाराष्ट्र")
            self.assertIn("dvSsttra", shaped_mh, f"{pfx} महाराष्ट्र did not form dvSsttra: {shaped_mh}")
            self.assertNotIn("dvVirama", shaped_mh)

    def test_12_thai_combining_marks_centered_in_thai_and_dflt(self) -> None:
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            ttf = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            tt = TTFont(ttf)
            order = tt.getGlyphOrder()
            blob = hb.Blob.from_file_path(str(ttf))
            face = hb.Face(blob)
            font = hb.Font(face)
            for script_tag in ("Thai", "Zyyy"):
                buf = hb.Buffer()
                buf.add_str("สวัสดี")
                buf.direction = "ltr"
                buf.script = script_tag
                hb.shape(font, buf)
                infos = buf.glyph_infos
                positions = buf.glyph_positions
                # Index 1 = thU0E27 (ว), Index 2 = thU0E31 (ั)
                b_adv = positions[1].x_advance
                g_mark = tt["glyf"][order[infos[2].codepoint]]
                mark_center = b_adv + positions[2].x_offset + 0.5 * (g_mark.xMin + g_mark.xMax)
                self.assertEqual(positions[2].x_advance, 0)
                self.assertGreater(positions[2].y_offset, 500, f"{pfx} ({script_tag}) thU0E31 missing y_offset")
                self.assertGreater(mark_center, b_adv * 0.25, f"{pfx} ({script_tag}) thU0E31 too far left: {mark_center} vs {b_adv}")
                self.assertLess(mark_center, b_adv * 0.80, f"{pfx} ({script_tag}) thU0E31 floating right: {mark_center} vs {b_adv}")

            # Verify mkmk stacks tone above upper vowel in นี้ (น + ี + ้)
            buf_mkmk = hb.Buffer()
            buf_mkmk.add_str("นี้")
            buf_mkmk.guess_segment_properties()
            hb.shape(font, buf_mkmk)
            self.assertGreater(buf_mkmk.glyph_positions[-1].y_offset, 700, f"{pfx} mkmk tone did not stack on นี้")

    def test_13_malayalam_kannada_tamil_shaping_and_glyph_integrity(self) -> None:
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            ttf = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            tt = TTFont(ttf)
            order = tt.getGlyphOrder()
            blob = hb.Blob.from_file_path(str(ttf))
            face = hb.Face(blob)
            font = hb.Font(face)

            # Malayalam: നന്ദി -> mlNa + mlNda + mlMatraI, and നമസ്കാരം virama non-colliding above mlSa
            self.assertEqual(_hb_shape_names(ttf, "നന്ദി"), ["mlNa", "mlNda", "mlMatraI"])
            buf_ml = hb.Buffer()
            buf_ml.add_str("നമസ്കാരം")
            buf_ml.guess_segment_properties()
            hb.shape(font, buf_ml)
            sa_ymax = tt["glyf"]["mlSa"].yMax
            vir_ymin_placed = buf_ml.glyph_positions[3].y_offset + tt["glyf"]["mlVirama"].yMin
            self.assertGreater(vir_ymin_placed, sa_ymax + 10, f"{pfx} mlVirama collides with mlSa: {vir_ymin_placed} <= {sa_ymax}")

            # Kannada: ನಮಸ್ಕಾರ -> knKa.blwf must have negative x_offset & negative y_offset (not unanchored 0,0!)
            buf_kn = hb.Buffer()
            buf_kn.add_str("ನಮಸ್ಕಾರ")
            buf_kn.guess_segment_properties()
            hb.shape(font, buf_kn)
            blwf_idx = [i for i, inf in enumerate(buf_kn.glyph_infos) if order[inf.codepoint] == "knKa.blwf"][0]
            self.assertLess(buf_kn.glyph_positions[blwf_idx].x_offset, -100, f"{pfx} knKa.blwf unanchored x_offset in ನಮಸ್ಕಾರ")
            self.assertLess(buf_kn.glyph_positions[blwf_idx].y_offset, -40, f"{pfx} knKa.blwf unanchored y_offset in ನಮಸ್ಕಾರ")

            # Tamil: ஒன்று / இரண்டு / மூன்று shaping + tmO distinct from tmU + connected tmTtaU
            self.assertEqual(_hb_shape_names(ttf, "ஒன்று"), ["tmO", "tmNnna", "tmPulli", "tmRraU"])
            self.assertEqual(_hb_shape_names(ttf, "இரண்டு"), ["tmI", "tmRa", "tmNna", "tmPulli", "tmTtaU"])
            self.assertEqual(_hb_shape_names(ttf, "மூன்று"), ["tmMaUu", "tmNnna", "tmPulli", "tmRraU"])
            self.assertLess(tt["glyf"]["tmO"].yMin, -40, f"{pfx} tmO missing descending lower-right leg")
            self.assertGreater(tt["glyf"]["tmU"].yMin, -15, f"{pfx} tmU unexpectedly descends below baseline")
            self.assertLessEqual(tt["glyf"]["tmTtaU"].numberOfContours, 2, f"{pfx} tmTtaU has detached strokes")

    def test_14_round3_shresti_double_storey_a_vs_o_and_low_res_I_1_rn_m(self) -> None:
        sh_reg = DIST / "aj-shresti" / "ttf" / "AJShresti-Regular.ttf"
        for px in range(9, 17):
            ba = _glyph_bitmap_norm(sh_reg, "a", px)
            bo = _glyph_bitmap_norm(sh_reg, "o", px)
            diff_px = int(np.abs(ba - bo).sum())
            self.assertGreaterEqual(
                diff_px, 8, f"AJShresti 'a' vs 'o' diff={diff_px}px < 8px at {px}px!"
            )
        # Verify accented 'a' variants inherited double-storey 'a' (not old single-storey 'o'+stem)
        tt_sh = TTFont(sh_reg)
        cmap_sh = tt_sh.getBestCmap()
        a_contours = tt_sh["glyf"]["a"].numberOfContours
        self.assertEqual(a_contours, 2, "AJShresti 'a' should have 2 contours (outer + lower loop counter)")
        for ch in "áàâäãåāă":
            gname = cmap_sh[ord(ch)]
            self.assertGreaterEqual(
                tt_sh["glyf"][gname].numberOfContours,
                3,
                f"AJShresti {ch} ({gname}) did not inherit double-storey 'a'",
            )
        # aogonek merges ogonek into the right foot of double-storey 'a' (2 contours + descender < -80)
        g_og = tt_sh["glyf"][cmap_sh[ord("ą")]]
        self.assertGreaterEqual(g_og.numberOfContours, 2)
        self.assertLess(g_og.yMin, -80)

        for slug, pfx in [
            ("aj-shresti", "AJShresti"),
            ("aj-anushya", "AJAnushya"),
            ("aaahhh-fonts-vibe", "AaahhhFontsVibe"),
        ]:
            ttf = DIST / slug / "ttf" / f"{pfx}-Regular.ttf"
            for px in (9, 10):
                bI = _glyph_bitmap_norm(ttf, "I", px)
                b1 = _glyph_bitmap_norm(ttf, "1", px)
                diff_i1 = int(np.abs(bI - b1).sum())
                self.assertGreaterEqual(
                    diff_i1, 5, f"{pfx} 'I' vs '1' diff={diff_i1}px < 5px at {px}px!"
                )
                fnt = ImageFont.truetype(str(ttf), px)
                im_rn = Image.new("L", (px * 5, px * 3), 0)
                im_m = Image.new("L", (px * 5, px * 3), 0)
                ImageDraw.Draw(im_rn).text((4, 4), "rn", font=fnt, fill=255)
                ImageDraw.Draw(im_m).text((4, 4), "m", font=fnt, fill=255)
                a_rn = (np.asarray(im_rn) > 40).astype(np.int32)
                a_m = (np.asarray(im_m) > 40).astype(np.int32)
                diff_rnm = int(np.abs(a_rn - a_m).sum())
                self.assertGreaterEqual(
                    diff_rnm, 4, f"{pfx} 'rn' vs 'm' diff={diff_rnm}px < 4px at {px}px!"
                )

    def test_15_round3_108_colrv1_otf_svg_dark_rim_linegap_and_sidecars(self) -> None:
        import json
        from sound_of_font import BackgroundFontMetadataIndexer

        checked = 0
        for slug, (_pfx, _cnt) in EXPECTED_FAMILIES.items():
            meta_p = DIST / slug / "metadata.json"
            self.assertTrue(meta_p.exists(), f"Missing metadata.json for {slug}")
            meta = json.loads(meta_p.read_text(encoding="utf-8"))
            self.assertTrue(meta.get("colrv1"))
            self.assertGreaterEqual(meta["ocr_confidence"], 0.985)
            self.assertLessEqual(meta["ocr_confidence"], 0.999)

            for fmt in ("otf", "ttf", "woff", "woff2"):
                for fp in sorted((DIST / slug / fmt).glob(f"*.{fmt}")):
                    r = ots.sanitize(str(fp), capture_output=True)
                    self.assertEqual(r.returncode, 0, f"OTS failed on {fp}: {r.stderr}")
                    tt = TTFont(fp)
                    self.assertIn("COLR", tt, f"Missing COLR in {fp.name}")
                    self.assertIn("CPAL", tt, f"Missing CPAL in {fp.name}")
                    self.assertIn("SVG ", tt, f"Missing SVG in {fp.name}")
                    self.assertEqual(tt["COLR"].version, 1, f"{fp.name} COLR version != 1")
                    self.assertEqual(tt["hhea"].lineGap, 60, f"{fp.name} hhea.lineGap != 60")
                    self.assertEqual(tt["OS/2"].sTypoLineGap, 60, f"{fp.name} sTypoLineGap != 60")
                    rim_alpha = tt["CPAL"].palettes[0][1].alpha / 255.0
                    self.assertAlmostEqual(rim_alpha, 0.26, delta=0.02, msg=f"{fp.name} rim alpha={rim_alpha}")
                    self.assertIn('fill-opacity="0.26"', tt["SVG "].docList[0].data)
                    checked += 1
        self.assertEqual(checked, 108)

        idx = BackgroundFontMetadataIndexer(DIST)
        idx.start()
        self.assertTrue(idx.wait())
        for slug in EXPECTED_FAMILIES:
            conf = idx.index["families"][slug]["ocr_confidence"]
            self.assertIsNotNone(conf, f"Indexer missing ocr_confidence for {slug}")
            self.assertGreaterEqual(conf, 0.985)

    def test_16_round3_multiscript_everyday_chars_counters_and_arabic_dots(self) -> None:
        required_chars = (
            "ሐሠኸዐዠጨጸፀሥዓለምረቃሐይነፃ"
            "ௐ௰௱௲௹"
            "৳"
            "ヴ"
            "京本東語阪准助帮常很感批气申非客再"
        )
        expected_ar_contours = {
            "arBeh": 2, "arPeh": 4, "arTeh": 3, "arTteh": 2, "arTheh": 4,
            "arFeh": 3, "arQaf": 4, "arKhah": 2, "arDdal": 2, "arYeh": 3,
            "arYeh.fina": 3, "arThal": 2, "arSheen": 4, "arGhain": 2,
            "arTehMarbuta": 4, "arDammatan": 2, "arFathatan": 2, "arKasratan": 2,
        }
        for slug, (pfx, _cnt) in EXPECTED_FAMILIES.items():
            reg = TTFont(DIST / slug / "ttf" / f"{pfx}-Regular.ttf")
            eb = TTFont(DIST / slug / "ttf" / f"{pfx}-ExtraBold.ttf")
            cmap = reg.getBestCmap()
            for ch in required_chars:
                self.assertIn(ord(ch), cmap, f"{pfx} missing {ch} (U+{ord(ch):04X})")

            for tt_font, wname in ((reg, "Regular"), (eb, "ExtraBold")):
                for gname in ("thU0E2A", "tmVa", "tmNna"):
                    self.assertGreaterEqual(
                        tt_font["glyf"][gname].numberOfContours,
                        2,
                        f"{pfx}-{wname} {gname} inner loop counter collapsed!",
                    )
            for ar_g, min_c in expected_ar_contours.items():
                self.assertGreaterEqual(
                    eb["glyf"][ar_g].numberOfContours,
                    min_c,
                    f"{pfx}-ExtraBold {ar_g} fused dot into bowl (contours={eb['glyf'][ar_g].numberOfContours} < {min_c})",
                )

    def test_17_round3_vibe_gsub_dlig_order_recipes_and_space_currency_guards(self) -> None:
        vibe_ttf = DIST / "aaahhh-fonts-vibe" / "ttf" / "AaahhhFontsVibe-Regular.ttf"
        # 1. Sound-of-Font runs BEFORE dlig (`sub s t by s_t;`)
        self.assertEqual(_hb_shape_names(vibe_ttf, ":hi:namaste", {"dlig": True}), ["_snd_hi_namaste"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "namaste", {"dlig": True, "ss07": True}), ["_snd_hi_namaste"])
        self.assertEqual(_hb_shape_names(vibe_ttf, "namasthe", {"dlig": True, "ss07": True}), ["_snd_hi_namaste"])

        # 2. Bengali & Telugu & new inline triggers + Tamil 4u..10u & Vanakam/VANAKKAM/wanakkam
        self.assertEqual(_hb_shape_names(vibe_ttf, ":bn:nomoshkar"), ["_snd_bn_nomoshkar"])
        for bn_word in ("nomoshkar", "nomoskar", "namaskar"):
            self.assertEqual(_hb_shape_names(vibe_ttf, bn_word, {"ss11": True}), ["_snd_bn_nomoshkar"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":te:namaskaram"), ["_snd_te_namaskaram"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":zh:nihao"), ["_snd_zh_nihao"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":th:sawatdee"), ["_snd_th_sawatdee"])
        self.assertEqual(_hb_shape_names(vibe_ttf, ":am:selam"), ["_snd_am_selam"])

        ta_feat = {"ss06": True}
        for v in ("Vanakam", "VANAKKAM", "wanakkam"):
            self.assertEqual(_hb_shape_names(vibe_ttf, v, ta_feat), ["_snd_ta_vanakkam"])
        for n_tok in ("4u", "5u", "6u", "7u", "8u", "9u", "10u"):
            shaped = _hb_shape_names(vibe_ttf, n_tok, ta_feat)
            self.assertEqual(len(shaped), 1, f"{n_tok} did not shape to single Tamil numeral word glyph: {shaped}")
            self.assertTrue(shaped[0].startswith("_snd_ta_"))

        # 3. Space-separated currency & No. guards in ss06
        for guarded in ("Rs 1u", "Rs. 1u", "$ 1u", "₹ 1u", "No. 1u"):
            shaped = _hb_shape_names(vibe_ttf, guarded, ta_feat)
            self.assertEqual(shaped[-2:], ["one", "u"], f"{guarded} wrongly converted 1u in ss06: {shaped}")


if __name__ == "__main__":
    unittest.main()
