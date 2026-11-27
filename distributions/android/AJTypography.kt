package `in`.aivibe.fonts.ajseries

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

/**
 * AJ Series Enterprise Typefaces v3.1.0 — Structured 5-Role Android & Jetpack Compose System Typography:
 *  - Level 1 Headers (Display / H1)     -> AJ Sahasvi (Sculpted Horizon Royal Small-Caps)
 *  - Level 2 Sub-Headings (H2–H3 / UI)  -> AJ Shresti (Architectural Geometric — Active OS Default)
 *  - Level 3 Text (H4 / Labels / Quotes)-> AJ Talin   (0° Straight Connected Running Script, calt)
 *  - Body Text (Paragraphs / Dense UI)  -> AJ Anushya (Zero-Tail Ultra-Clarity Reading Sans)
 *  - Sound of Font                      -> Aaahhh Fonts Vibe (AJFontFamilies.AaahhhVibe)
 */
object AJFontFamilies {
    val Sahasvi = FontFamily(
        Font(R.font.aj_sahasvi_regular, FontWeight.Normal),
        Font(R.font.aj_sahasvi_semibold, FontWeight.SemiBold),
        Font(R.font.aj_sahasvi_extrabold, FontWeight.ExtraBold),
    )
    val Shresti = FontFamily(
        Font(R.font.aj_shresti_regular, FontWeight.Normal),
        Font(R.font.aj_shresti_semibold, FontWeight.SemiBold),
        Font(R.font.aj_shresti_extrabold, FontWeight.ExtraBold),
        Font(R.font.aj_shresti_italic, FontWeight.Normal, FontStyle.Italic),
        Font(R.font.aj_shresti_semibolditalic, FontWeight.SemiBold, FontStyle.Italic),
        Font(R.font.aj_shresti_extrabolditalic, FontWeight.ExtraBold, FontStyle.Italic),
    )
    val Talin = FontFamily(
        Font(R.font.aj_talin_regular, FontWeight.Normal),
        Font(R.font.aj_talin_semibold, FontWeight.SemiBold),
        Font(R.font.aj_talin_extrabold, FontWeight.ExtraBold),
        Font(R.font.aj_talin_italic, FontWeight.Normal, FontStyle.Italic),
        Font(R.font.aj_talin_semibolditalic, FontWeight.SemiBold, FontStyle.Italic),
        Font(R.font.aj_talin_extrabolditalic, FontWeight.ExtraBold, FontStyle.Italic),
    )
    val Anushya = FontFamily(
        Font(R.font.aj_anushya_regular, FontWeight.Normal),
        Font(R.font.aj_anushya_semibold, FontWeight.SemiBold),
        Font(R.font.aj_anushya_extrabold, FontWeight.ExtraBold),
        Font(R.font.aj_anushya_italic, FontWeight.Normal, FontStyle.Italic),
        Font(R.font.aj_anushya_semibolditalic, FontWeight.SemiBold, FontStyle.Italic),
        Font(R.font.aj_anushya_extrabolditalic, FontWeight.ExtraBold, FontStyle.Italic),
    )
    val AaahhhVibe = FontFamily(
        Font(R.font.aaahhh_fonts_vibe_regular, FontWeight.Normal),
        Font(R.font.aaahhh_fonts_vibe_semibold, FontWeight.SemiBold),
        Font(R.font.aaahhh_fonts_vibe_extrabold, FontWeight.ExtraBold),
        Font(R.font.aaahhh_fonts_vibe_italic, FontWeight.Normal, FontStyle.Italic),
        Font(R.font.aaahhh_fonts_vibe_semibolditalic, FontWeight.SemiBold, FontStyle.Italic),
        Font(R.font.aaahhh_fonts_vibe_extrabolditalic, FontWeight.ExtraBold, FontStyle.Italic),
    )
}

val AJSystemMaterialTypography = Typography(
    // Level 1: Headers -> AJ Sahasvi
    displayLarge = TextStyle(fontFamily = AJFontFamilies.Sahasvi, fontWeight = FontWeight.ExtraBold, fontSize = 40.sp, lineHeight = 46.sp),
    displayMedium = TextStyle(fontFamily = AJFontFamilies.Sahasvi, fontWeight = FontWeight.ExtraBold, fontSize = 32.sp, lineHeight = 38.sp),
    headlineLarge = TextStyle(fontFamily = AJFontFamilies.Sahasvi, fontWeight = FontWeight.SemiBold, fontSize = 28.sp, lineHeight = 34.sp),
    // Level 2: Sub-Headings & Active System UI -> AJ Shresti
    headlineMedium = TextStyle(fontFamily = AJFontFamilies.Shresti, fontWeight = FontWeight.SemiBold, fontSize = 24.sp, lineHeight = 30.sp),
    titleLarge = TextStyle(fontFamily = AJFontFamilies.Shresti, fontWeight = FontWeight.SemiBold, fontSize = 20.sp, lineHeight = 26.sp),
    titleMedium = TextStyle(fontFamily = AJFontFamilies.Shresti, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, lineHeight = 22.sp),
    // Level 3: 3rd-Level Text & Accents -> AJ Talin
    titleSmall = TextStyle(fontFamily = AJFontFamilies.Talin, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, lineHeight = 22.sp, fontFeatureSettings = "calt"),
    labelLarge = TextStyle(fontFamily = AJFontFamilies.Talin, fontWeight = FontWeight.SemiBold, fontSize = 15.sp, lineHeight = 20.sp, fontFeatureSettings = "calt"),
    // Body Text -> AJ Anushya
    bodyLarge = TextStyle(fontFamily = AJFontFamilies.Anushya, fontWeight = FontWeight.Normal, fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium = TextStyle(fontFamily = AJFontFamilies.Anushya, fontWeight = FontWeight.Normal, fontSize = 14.sp, lineHeight = 20.sp),
    bodySmall = TextStyle(fontFamily = AJFontFamilies.Anushya, fontWeight = FontWeight.Normal, fontSize = 12.sp, lineHeight = 16.sp),
)
