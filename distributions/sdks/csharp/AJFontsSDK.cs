// AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (C#, .NET base library only).
// Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
// Provided "AS IS" without warranty. https://fonts.aivibe.cloud
using System;
using System.Collections.Generic;
using System.Linq;

namespace Aivibe.Fonts
{
    public sealed record AJFamily(
        string Id, string Name, string Prefix, string Level, string Role,
        bool HasItalic, double ItalicAngle, int XHeight, string Generic);

    public static class AJFontsSDK
    {
        public const string Version = "3.1.0";

        /* PLACEHOLDER: Configure your CDN/local font base URL here */
        public const string DefaultFontBaseUrl = "https://fonts.aivibe.cloud/fonts";

        public static readonly IReadOnlyList<AJFamily> Families = new[]
        {
            new AJFamily("aj-sahasvi", "AJ Sahasvi", "AJSahasvi", "1", "Level 1 Headers (H1)", false, 0, 516, "serif"),
            new AJFamily("aj-shresti", "AJ Shresti", "AJShresti", "2", "Level 2 Sub-Headings & OS Default", true, 10, 534, "sans-serif"),
            new AJFamily("aj-talin", "AJ Talin", "AJTalin", "3", "Level 3 Script", true, 11, 492, "cursive"),
            new AJFamily("aj-anushya", "AJ Anushya", "AJAnushya", "body", "Body Reading", true, 9, 556, "sans-serif"),
            new AJFamily("aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", "sound", "Sound of Font", true, 9.5, 558, "sans-serif"),
        };

        public static readonly IReadOnlyList<int> Weights = new[] { 400, 600, 800 };

        private static readonly Dictionary<int, string> WeightNames =
            new() { [400] = "Regular", [600] = "SemiBold", [800] = "ExtraBold" };

        /// <summary>ss06-ss18 take effect in Aaahhh Fonts Vibe only.</summary>
        public static readonly IReadOnlyDictionary<string, string> SoundStylisticSets = new Dictionary<string, string>
        {
            ["ta"] = "ss06", ["hi"] = "ss07", ["te"] = "ss08", ["ml"] = "ss09", ["kn"] = "ss10", ["bn"] = "ss11", ["pa"] = "ss12",
            ["ar"] = "ss13", ["ur"] = "ss13", ["ja"] = "ss14", ["ru"] = "ss15", ["zh"] = "ss16", ["th"] = "ss17", ["am"] = "ss18",
        };

        private static readonly HashSet<string> FeatureTags = new(
            "kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05"
                .Split(' ').Concat(SoundStylisticSets.Values));

        /// <summary>OCR disambiguation metadata: character groups the designs keep visually distinct.</summary>
        public static readonly string[][] OcrDisambiguationGroups =
        {
            new[] { "0", "O", "o" }, new[] { "I", "l", "1" }, new[] { "a", "b", "6" }, new[] { "rn", "m" }, new[] { "cl", "d" },
        };
        public const string OcrRecommendedFamily = "AJ Anushya";
        public const int OcrRecommendedMinPx = 12;
        public const string OcrFeatureSettings = "\"zero\" 1, \"tnum\" 1, \"liga\" 0, \"dlig\" 0";

        public static AJFamily Family(string key) =>
            Families.FirstOrDefault(f => f.Id == key || f.Name == key)
            ?? throw new ArgumentException($"unknown family: {key}");

        public static string StyleName(string key, int weight = 400, bool italic = false)
        {
            var fam = Family(key);
            if (!WeightNames.TryGetValue(weight, out var name)) throw new ArgumentException($"unsupported weight: {weight}");
            if (italic && !fam.HasItalic) throw new ArgumentException($"{fam.Name} has no italic");
            if (!italic) return name;
            return weight == 400 ? "Italic" : name + "Italic";
        }

        public static string FontUrl(string key, int weight = 400, bool italic = false, string format = "woff2",
                                     string baseUrl = DefaultFontBaseUrl)
        {
            if (baseUrl.IndexOfAny(new[] { '"', '\'', '\\', '\r', '\n' }) >= 0)
                throw new ArgumentException("baseUrl contains characters that are unsafe in CSS");
            return $"{baseUrl.TrimEnd('/')}/{Family(key).Prefix}-{StyleName(key, weight, italic)}.{format}";
        }

        public static string FontStack(string key)
        {
            var fam = Family(key);
            return $"\"{fam.Name}\", system-ui, {fam.Generic}";
        }

        public static string FontFaceCss(string key, int weight = 400, bool italic = false,
                                         string baseUrl = DefaultFontBaseUrl)
        {
            var url = FontUrl(key, weight, italic, "woff2", baseUrl);
            var style = italic ? "italic" : "normal";
            return $"@font-face {{ font-family: \"{Family(key).Name}\"; src: url(\"{url}\") format(\"woff2\"); font-weight: {weight}; font-style: {style}; font-display: swap; }}";
        }

        /// <summary>All 27 @font-face rules.</summary>
        public static string AllFontFaceCss(string baseUrl = DefaultFontBaseUrl) =>
            string.Join("\n",
                from fam in Families
                from italic in fam.HasItalic ? new[] { false, true } : new[] { false }
                from weight in Weights
                select FontFaceCss(fam.Id, weight, italic, baseUrl));

        public static string FeatureSettings(IEnumerable<string>? enable = null, IEnumerable<string>? disable = null)
        {
            var parts = (enable ?? Array.Empty<string>()).Select(t => (Tag: t, Value: 1))
                .Concat((disable ?? Array.Empty<string>()).Select(t => (Tag: t, Value: 0)))
                .Select(p => FeatureTags.Contains(p.Tag)
                    ? $"\"{p.Tag}\" {p.Value}"
                    : throw new ArgumentException($"unsupported OpenType feature: {p.Tag}"))
                .ToList();
            return parts.Count == 0 ? "normal" : string.Join(", ", parts);
        }

        public static string SoundFeatureSettings(string language) =>
            SoundStylisticSets.TryGetValue(language, out var tag)
                ? FeatureSettings(new[] { tag, "calt" })
                : throw new ArgumentException($"no Sound of Font set for language: {language}");
    }
}
