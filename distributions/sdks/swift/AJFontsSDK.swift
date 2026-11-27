// AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (Swift, no dependencies).
// Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
// Provided "AS IS" without warranty. https://fonts.aivibe.cloud

public enum AJFontsError: Error, Equatable {
    case unknownFamily(String)
    case unsupportedWeight(Int)
    case noItalic(String)
    case unsupportedFeature(String)
    case unsupportedLanguage(String)
    case unsafeBaseURL
}

public struct AJFamily: Equatable {
    public let id, name, prefix, level, role: String
    public let hasItalic: Bool
    public let italicAngle: Double
    public let xHeight: Int
    public let generic: String
}

public enum AJFontsSDK {
    public static let version = "3.1.0"

    /* PLACEHOLDER: Configure your CDN/local font base URL here */
    public static let defaultFontBaseURL = "https://fonts.aivibe.cloud/fonts"

    public static let families: [AJFamily] = [
        AJFamily(id: "aj-sahasvi", name: "AJ Sahasvi", prefix: "AJSahasvi", level: "1", role: "Level 1 Headers (H1)", hasItalic: false, italicAngle: 0, xHeight: 516, generic: "serif"),
        AJFamily(id: "aj-shresti", name: "AJ Shresti", prefix: "AJShresti", level: "2", role: "Level 2 Sub-Headings & OS Default", hasItalic: true, italicAngle: 10, xHeight: 534, generic: "sans-serif"),
        AJFamily(id: "aj-talin", name: "AJ Talin", prefix: "AJTalin", level: "3", role: "Level 3 Script", hasItalic: true, italicAngle: 11, xHeight: 492, generic: "cursive"),
        AJFamily(id: "aj-anushya", name: "AJ Anushya", prefix: "AJAnushya", level: "body", role: "Body Reading", hasItalic: true, italicAngle: 9, xHeight: 556, generic: "sans-serif"),
        AJFamily(id: "aaahhh-fonts-vibe", name: "Aaahhh Fonts Vibe", prefix: "AaahhhFontsVibe", level: "sound", role: "Sound of Font", hasItalic: true, italicAngle: 9.5, xHeight: 558, generic: "sans-serif"),
    ]

    public static let weights = [400, 600, 800]
    private static let weightNames = [400: "Regular", 600: "SemiBold", 800: "ExtraBold"]

    /// ss06-ss18 take effect in Aaahhh Fonts Vibe only.
    public static let soundStylisticSets = [
        "ta": "ss06", "hi": "ss07", "te": "ss08", "ml": "ss09", "kn": "ss10", "bn": "ss11", "pa": "ss12",
        "ar": "ss13", "ur": "ss13", "ja": "ss14", "ru": "ss15", "zh": "ss16", "th": "ss17", "am": "ss18",
    ]

    public static let featureTags: Set<String> = Set(
        "kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05"
            .split(separator: " ").map(String.init)
    ).union(soundStylisticSets.values)

    /// OCR disambiguation metadata: character groups the designs keep visually distinct.
    public static let ocrDisambiguationGroups = [["0", "O", "o"], ["I", "l", "1"], ["a", "b", "6"], ["rn", "m"], ["cl", "d"]]
    public static let ocrRecommendedFamily = "AJ Anushya"
    public static let ocrRecommendedMinPx = 12
    public static let ocrFeatureSettings = "\"zero\" 1, \"tnum\" 1, \"liga\" 0, \"dlig\" 0"

    public static func family(_ key: String) throws -> AJFamily {
        guard let found = families.first(where: { $0.id == key || $0.name == key }) else {
            throw AJFontsError.unknownFamily(key)
        }
        return found
    }

    public static func styleName(_ key: String, weight: Int = 400, italic: Bool = false) throws -> String {
        let fam = try family(key)
        guard let name = weightNames[weight] else { throw AJFontsError.unsupportedWeight(weight) }
        if italic && !fam.hasItalic { throw AJFontsError.noItalic(fam.name) }
        if !italic { return name }
        return weight == 400 ? "Italic" : name + "Italic"
    }

    public static func fontURL(_ key: String, weight: Int = 400, italic: Bool = false,
                               format: String = "woff2", baseURL: String = defaultFontBaseURL) throws -> String {
        if baseURL.contains(where: { "\"'\\\r\n".contains($0) }) { throw AJFontsError.unsafeBaseURL }
        var base = baseURL
        while base.hasSuffix("/") { base.removeLast() }
        return "\(base)/\(try family(key).prefix)-\(try styleName(key, weight: weight, italic: italic)).\(format)"
    }

    public static func fontStack(_ key: String) throws -> String {
        let fam = try family(key)
        return "\"\(fam.name)\", system-ui, \(fam.generic)"
    }

    public static func fontFaceCSS(_ key: String, weight: Int = 400, italic: Bool = false,
                                   baseURL: String = defaultFontBaseURL) throws -> String {
        let url = try fontURL(key, weight: weight, italic: italic, baseURL: baseURL)
        let name = try family(key).name
        let style = italic ? "italic" : "normal"
        return "@font-face { font-family: \"\(name)\"; src: url(\"\(url)\") format(\"woff2\"); font-weight: \(weight); font-style: \(style); font-display: swap; }"
    }

    /// All 27 @font-face rules.
    public static func allFontFaceCSS(baseURL: String = defaultFontBaseURL) throws -> String {
        var rules: [String] = []
        for fam in families {
            for italic in fam.hasItalic ? [false, true] : [false] {
                for weight in weights {
                    rules.append(try fontFaceCSS(fam.id, weight: weight, italic: italic, baseURL: baseURL))
                }
            }
        }
        return rules.joined(separator: "\n")
    }

    public static func featureSettings(enable: [String] = [], disable: [String] = []) throws -> String {
        var parts: [String] = []
        for (tags, value) in [(enable, 1), (disable, 0)] {
            for tag in tags {
                guard featureTags.contains(tag) else { throw AJFontsError.unsupportedFeature(tag) }
                parts.append("\"\(tag)\" \(value)")
            }
        }
        return parts.isEmpty ? "normal" : parts.joined(separator: ", ")
    }

    public static func soundFeatureSettings(_ language: String) throws -> String {
        guard let tag = soundStylisticSets[language] else { throw AJFontsError.unsupportedLanguage(language) }
        return try featureSettings(enable: [tag, "calt"])
    }
}
