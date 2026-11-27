// AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (Kotlin, standard library only).
// Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
// Provided "AS IS" without warranty. https://fonts.aivibe.cloud
package cloud.aivibe.fonts

data class AJFamily(
    val id: String, val name: String, val prefix: String, val level: String, val role: String,
    val hasItalic: Boolean, val italicAngle: Double, val xHeight: Int, val generic: String,
)

object AJFontsSDK {
    const val VERSION = "3.1.0"

    /* PLACEHOLDER: Configure your CDN/local font base URL here */
    const val DEFAULT_FONT_BASE_URL = "https://fonts.aivibe.cloud/fonts"

    val families = listOf(
        AJFamily("aj-sahasvi", "AJ Sahasvi", "AJSahasvi", "1", "Level 1 Headers (H1)", false, 0.0, 516, "serif"),
        AJFamily("aj-shresti", "AJ Shresti", "AJShresti", "2", "Level 2 Sub-Headings & OS Default", true, 10.0, 534, "sans-serif"),
        AJFamily("aj-talin", "AJ Talin", "AJTalin", "3", "Level 3 Script", true, 11.0, 492, "cursive"),
        AJFamily("aj-anushya", "AJ Anushya", "AJAnushya", "body", "Body Reading", true, 9.0, 556, "sans-serif"),
        AJFamily("aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", "sound", "Sound of Font", true, 9.5, 558, "sans-serif"),
    )

    val weights = listOf(400, 600, 800)
    private val weightNames = mapOf(400 to "Regular", 600 to "SemiBold", 800 to "ExtraBold")

    /** ss06-ss18 take effect in Aaahhh Fonts Vibe only. */
    val soundStylisticSets = mapOf(
        "ta" to "ss06", "hi" to "ss07", "te" to "ss08", "ml" to "ss09", "kn" to "ss10", "bn" to "ss11", "pa" to "ss12",
        "ar" to "ss13", "ur" to "ss13", "ja" to "ss14", "ru" to "ss15", "zh" to "ss16", "th" to "ss17", "am" to "ss18",
    )

    val featureTags: Set<String> =
        "kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05"
            .split(" ").toSet() + soundStylisticSets.values

    /** OCR disambiguation metadata: character groups the designs keep visually distinct. */
    val ocrDisambiguationGroups = listOf(listOf("0", "O", "o"), listOf("I", "l", "1"), listOf("a", "b", "6"), listOf("rn", "m"), listOf("cl", "d"))
    const val OCR_RECOMMENDED_FAMILY = "AJ Anushya"
    const val OCR_RECOMMENDED_MIN_PX = 12
    const val OCR_FEATURE_SETTINGS = "\"zero\" 1, \"tnum\" 1, \"liga\" 0, \"dlig\" 0"

    fun family(key: String): AJFamily =
        families.firstOrNull { it.id == key || it.name == key } ?: throw IllegalArgumentException("unknown family: $key")

    fun styleName(key: String, weight: Int = 400, italic: Boolean = false): String {
        val fam = family(key)
        val name = requireNotNull(weightNames[weight]) { "unsupported weight: $weight" }
        require(!italic || fam.hasItalic) { "${fam.name} has no italic" }
        return when {
            !italic -> name
            weight == 400 -> "Italic"
            else -> "${name}Italic"
        }
    }

    fun fontUrl(key: String, weight: Int = 400, italic: Boolean = false, format: String = "woff2",
                baseUrl: String = DEFAULT_FONT_BASE_URL): String {
        require(baseUrl.none { it in "\"'\\\r\n" }) { "baseUrl contains characters that are unsafe in CSS" }
        return "${baseUrl.trimEnd('/')}/${family(key).prefix}-${styleName(key, weight, italic)}.$format"
    }

    fun fontStack(key: String): String = family(key).let { "\"${it.name}\", system-ui, ${it.generic}" }

    fun fontFaceCss(key: String, weight: Int = 400, italic: Boolean = false,
                    baseUrl: String = DEFAULT_FONT_BASE_URL): String {
        val url = fontUrl(key, weight, italic, "woff2", baseUrl)
        val style = if (italic) "italic" else "normal"
        return "@font-face { font-family: \"${family(key).name}\"; src: url(\"$url\") format(\"woff2\"); font-weight: $weight; font-style: $style; font-display: swap; }"
    }

    /** All 27 @font-face rules. */
    fun allFontFaceCss(baseUrl: String = DEFAULT_FONT_BASE_URL): String =
        families.flatMap { fam ->
            val italics = if (fam.hasItalic) listOf(false, true) else listOf(false)
            italics.flatMap { italic -> weights.map { fontFaceCss(fam.id, it, italic, baseUrl) } }
        }.joinToString("\n")

    fun featureSettings(enable: List<String> = emptyList(), disable: List<String> = emptyList()): String {
        val parts = (enable.map { it to 1 } + disable.map { it to 0 }).map { (tag, value) ->
            require(tag in featureTags) { "unsupported OpenType feature: $tag" }
            "\"$tag\" $value"
        }
        return if (parts.isEmpty()) "normal" else parts.joinToString(", ")
    }

    fun soundFeatureSettings(language: String): String {
        val tag = requireNotNull(soundStylisticSets[language]) { "no Sound of Font set for language: $language" }
        return featureSettings(listOf(tag, "calt"))
    }
}
