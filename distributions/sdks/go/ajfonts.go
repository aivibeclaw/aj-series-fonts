// Package ajfonts is the AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (standard library only).
//
// Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
// SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
// Provided "AS IS" without warranty. https://fonts.aivibe.cloud
package ajfonts

import (
	"fmt"
	"strings"
)

// Version of the SDK and font release.
const Version = "3.1.0"

/* PLACEHOLDER: Configure your CDN/local font base URL here */
const DefaultFontBaseURL = "https://fonts.aivibe.cloud/fonts"

// Family describes one canonical family.
type Family struct {
	ID, Name, Prefix, Level, Role string
	HasItalic                     bool
	ItalicAngle                   float64
	XHeight                       int
	Generic                       string
}

// Families returns the 5 canonical families.
func Families() []Family {
	return []Family{
		{"aj-sahasvi", "AJ Sahasvi", "AJSahasvi", "1", "Level 1 Headers (H1)", false, 0, 516, "serif"},
		{"aj-shresti", "AJ Shresti", "AJShresti", "2", "Level 2 Sub-Headings & OS Default", true, 10, 534, "sans-serif"},
		{"aj-talin", "AJ Talin", "AJTalin", "3", "Level 3 Script", true, 11, 492, "cursive"},
		{"aj-anushya", "AJ Anushya", "AJAnushya", "body", "Body Reading", true, 9, 556, "sans-serif"},
		{"aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", "sound", "Sound of Font", true, 9.5, 558, "sans-serif"},
	}
}

var weights = []int{400, 600, 800}

var weightNames = map[int]string{400: "Regular", 600: "SemiBold", 800: "ExtraBold"}

// SoundStylisticSets maps language to stylistic set. ss06-ss18 take effect in Aaahhh Fonts Vibe only.
var SoundStylisticSets = map[string]string{
	"ta": "ss06", "hi": "ss07", "te": "ss08", "ml": "ss09", "kn": "ss10", "bn": "ss11", "pa": "ss12",
	"ar": "ss13", "ur": "ss13", "ja": "ss14", "ru": "ss15", "zh": "ss16", "th": "ss17", "am": "ss18",
}

const baseFeatures = "kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05"

// OCRDisambiguationGroups lists character groups the designs keep visually distinct.
var OCRDisambiguationGroups = [][]string{{"0", "O", "o"}, {"I", "l", "1"}, {"a", "b", "6"}, {"rn", "m"}, {"cl", "d"}}

// OCR rendering recommendations.
const (
	OCRRecommendedFamily = "AJ Anushya"
	OCRRecommendedMinPx  = 12
	OCRFeatureSettings   = `"zero" 1, "tnum" 1, "liga" 0, "dlig" 0`
)

// Lookup finds a family by id or name.
func Lookup(key string) (Family, error) {
	for _, f := range Families() {
		if f.ID == key || f.Name == key {
			return f, nil
		}
	}
	return Family{}, fmt.Errorf("ajfonts: unknown family %q", key)
}

// StyleName returns the file style suffix, for example "SemiBoldItalic".
func StyleName(key string, weight int, italic bool) (string, error) {
	f, err := Lookup(key)
	if err != nil {
		return "", err
	}
	name, ok := weightNames[weight]
	if !ok {
		return "", fmt.Errorf("ajfonts: unsupported weight %d", weight)
	}
	switch {
	case !italic:
		return name, nil
	case !f.HasItalic:
		return "", fmt.Errorf("ajfonts: %s has no italic", f.Name)
	case weight == 400:
		return "Italic", nil
	}
	return name + "Italic", nil
}

// FontURL returns the URL of one font file.
func FontURL(baseURL, key string, weight int, italic bool, format string) (string, error) {
	if strings.ContainsAny(baseURL, "\"'\\\r\n") {
		return "", fmt.Errorf("ajfonts: base URL contains characters that are unsafe in CSS")
	}
	style, err := StyleName(key, weight, italic)
	if err != nil {
		return "", err
	}
	f, err := Lookup(key)
	if err != nil {
		return "", err
	}
	return fmt.Sprintf("%s/%s-%s.%s", strings.TrimRight(baseURL, "/"), f.Prefix, style, format), nil
}

// FontStack returns a CSS font-family stack.
func FontStack(key string) (string, error) {
	f, err := Lookup(key)
	if err != nil {
		return "", err
	}
	return fmt.Sprintf("%q, system-ui, %s", f.Name, f.Generic), nil
}

// FontFaceCSS returns one @font-face rule.
func FontFaceCSS(baseURL, key string, weight int, italic bool) (string, error) {
	url, err := FontURL(baseURL, key, weight, italic, "woff2")
	if err != nil {
		return "", err
	}
	f, err := Lookup(key)
	if err != nil {
		return "", err
	}
	style := "normal"
	if italic {
		style = "italic"
	}
	return fmt.Sprintf(`@font-face { font-family: "%s"; src: url("%s") format("woff2"); font-weight: %d; font-style: %s; font-display: swap; }`,
		f.Name, url, weight, style), nil
}

// AllFontFaceCSS returns all 27 @font-face rules.
func AllFontFaceCSS(baseURL string) (string, error) {
	var rules []string
	for _, f := range Families() {
		italics := []bool{false}
		if f.HasItalic {
			italics = append(italics, true)
		}
		for _, italic := range italics {
			for _, w := range weights {
				rule, err := FontFaceCSS(baseURL, f.ID, w, italic)
				if err != nil {
					return "", err
				}
				rules = append(rules, rule)
			}
		}
	}
	return strings.Join(rules, "\n"), nil
}

func isFeature(tag string) bool {
	for _, t := range strings.Fields(baseFeatures) {
		if t == tag {
			return true
		}
	}
	for _, t := range SoundStylisticSets {
		if t == tag {
			return true
		}
	}
	return false
}

// FeatureSettings builds a CSS font-feature-settings value.
func FeatureSettings(enable, disable []string) (string, error) {
	var parts []string
	for value, tags := range [][]string{disable, enable} {
		var group []string
		for _, tag := range tags {
			if !isFeature(tag) {
				return "", fmt.Errorf("ajfonts: unsupported OpenType feature %q", tag)
			}
			group = append(group, fmt.Sprintf("%q %d", tag, value))
		}
		parts = append(group, parts...) // enabled tags come first
	}
	if len(parts) == 0 {
		return "normal", nil
	}
	return strings.Join(parts, ", "), nil
}

// SoundFeatureSettings enables phonetic shaping for one language.
func SoundFeatureSettings(language string) (string, error) {
	tag, ok := SoundStylisticSets[language]
	if !ok {
		return "", fmt.Errorf("ajfonts: no Sound of Font set for language %q", language)
	}
	return FeatureSettings([]string{tag, "calt"}, nil)
}
