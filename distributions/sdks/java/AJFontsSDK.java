// AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (Java 17+, JDK only).
// Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
// Provided "AS IS" without warranty. https://fonts.aivibe.cloud

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public final class AJFontsSDK {
    private AJFontsSDK() {}

    public static final String VERSION = "3.1.0";

    /* PLACEHOLDER: Configure your CDN/local font base URL here */
    public static final String DEFAULT_FONT_BASE_URL = "https://fonts.aivibe.cloud/fonts";

    public record Family(String id, String name, String prefix, String level, String role,
                         boolean hasItalic, double italicAngle, int xHeight, String generic) {}

    public static final List<Family> FAMILIES = List.of(
        new Family("aj-sahasvi", "AJ Sahasvi", "AJSahasvi", "1", "Level 1 Headers (H1)", false, 0, 516, "serif"),
        new Family("aj-shresti", "AJ Shresti", "AJShresti", "2", "Level 2 Sub-Headings & OS Default", true, 10, 534, "sans-serif"),
        new Family("aj-talin", "AJ Talin", "AJTalin", "3", "Level 3 Script", true, 11, 492, "cursive"),
        new Family("aj-anushya", "AJ Anushya", "AJAnushya", "body", "Body Reading", true, 9, 556, "sans-serif"),
        new Family("aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", "sound", "Sound of Font", true, 9.5, 558, "sans-serif"));

    public static final List<Integer> WEIGHTS = List.of(400, 600, 800);
    private static final Map<Integer, String> WEIGHT_NAMES = Map.of(400, "Regular", 600, "SemiBold", 800, "ExtraBold");

    /** ss06-ss18 take effect in Aaahhh Fonts Vibe only. */
    public static final Map<String, String> SOUND_STYLISTIC_SETS = Map.ofEntries(
        Map.entry("ta", "ss06"), Map.entry("hi", "ss07"), Map.entry("te", "ss08"), Map.entry("ml", "ss09"),
        Map.entry("kn", "ss10"), Map.entry("bn", "ss11"), Map.entry("pa", "ss12"), Map.entry("ar", "ss13"),
        Map.entry("ur", "ss13"), Map.entry("ja", "ss14"), Map.entry("ru", "ss15"), Map.entry("zh", "ss16"),
        Map.entry("th", "ss17"), Map.entry("am", "ss18"));

    private static final List<String> BASE_FEATURES = List.of(
        "kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05".split(" "));

    /** OCR disambiguation metadata: character groups the designs keep visually distinct. */
    public static final List<List<String>> OCR_DISAMBIGUATION_GROUPS = List.of(
        List.of("0", "O", "o"), List.of("I", "l", "1"), List.of("a", "b", "6"), List.of("rn", "m"), List.of("cl", "d"));
    public static final String OCR_RECOMMENDED_FAMILY = "AJ Anushya";
    public static final int OCR_RECOMMENDED_MIN_PX = 12;
    public static final String OCR_FEATURE_SETTINGS = "\"zero\" 1, \"tnum\" 1, \"liga\" 0, \"dlig\" 0";

    public static Family family(String key) {
        return FAMILIES.stream()
            .filter(f -> f.id().equals(key) || f.name().equals(key))
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("unknown family: " + key));
    }

    public static String styleName(String key, int weight, boolean italic) {
        Family fam = family(key);
        if (!WEIGHTS.contains(weight)) throw new IllegalArgumentException("unsupported weight: " + weight);
        if (italic && !fam.hasItalic()) throw new IllegalArgumentException(fam.name() + " has no italic");
        String name = WEIGHT_NAMES.get(weight);
        if (!italic) return name;
        return weight == 400 ? "Italic" : name + "Italic";
    }

    public static String fontUrl(String key, int weight, boolean italic, String format, String baseUrl) {
        if (baseUrl.chars().anyMatch(c -> "\"'\\\r\n".indexOf(c) >= 0)) {
            throw new IllegalArgumentException("baseUrl contains characters that are unsafe in CSS");
        }
        return baseUrl.replaceAll("/+$", "") + "/" + family(key).prefix() + "-" + styleName(key, weight, italic) + "." + format;
    }

    public static String fontStack(String key) {
        Family fam = family(key);
        return "\"" + fam.name() + "\", system-ui, " + fam.generic();
    }

    public static String fontFaceCss(String key, int weight, boolean italic, String baseUrl) {
        String url = fontUrl(key, weight, italic, "woff2", baseUrl);
        return "@font-face { font-family: \"" + family(key).name() + "\"; src: url(\"" + url + "\") format(\"woff2\"); "
            + "font-weight: " + weight + "; font-style: " + (italic ? "italic" : "normal") + "; font-display: swap; }";
    }

    /** All 27 {@code @font-face} rules. */
    public static String allFontFaceCss(String baseUrl) {
        List<String> rules = new ArrayList<>();
        for (Family fam : FAMILIES) {
            for (boolean italic : fam.hasItalic() ? new boolean[] {false, true} : new boolean[] {false}) {
                for (int weight : WEIGHTS) {
                    rules.add(fontFaceCss(fam.id(), weight, italic, baseUrl));
                }
            }
        }
        return String.join("\n", rules);
    }

    public static String featureSettings(List<String> enable, List<String> disable) {
        List<String> parts = new ArrayList<>();
        for (String tag : enable) parts.add(feature(tag, 1));
        for (String tag : disable) parts.add(feature(tag, 0));
        return parts.isEmpty() ? "normal" : String.join(", ", parts);
    }

    private static String feature(String tag, int value) {
        if (!BASE_FEATURES.contains(tag) && !SOUND_STYLISTIC_SETS.containsValue(tag)) {
            throw new IllegalArgumentException("unsupported OpenType feature: " + tag);
        }
        return "\"" + tag + "\" " + value;
    }

    public static String soundFeatureSettings(String language) {
        String tag = SOUND_STYLISTIC_SETS.get(language);
        if (tag == null) throw new IllegalArgumentException("no Sound of Font set for language: " + language);
        return featureSettings(List.of(tag, "calt"), List.of());
    }
}
