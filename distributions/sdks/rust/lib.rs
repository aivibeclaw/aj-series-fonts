//! AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (Rust, std only).
//! Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
//! SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
//! Provided "AS IS" without warranty. <https://fonts.aivibe.cloud>

pub const VERSION: &str = "3.1.0";

/* PLACEHOLDER: Configure your CDN/local font base URL here */
pub const DEFAULT_FONT_BASE_URL: &str = "https://fonts.aivibe.cloud/fonts";

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Family {
    pub id: &'static str,
    pub name: &'static str,
    pub prefix: &'static str,
    pub level: &'static str,
    pub role: &'static str,
    pub has_italic: bool,
    pub italic_angle: f32,
    pub x_height: u16,
    pub generic: &'static str,
}

pub const FAMILIES: [Family; 5] = [
    Family { id: "aj-sahasvi", name: "AJ Sahasvi", prefix: "AJSahasvi", level: "1", role: "Level 1 Headers (H1)", has_italic: false, italic_angle: 0.0, x_height: 516, generic: "serif" },
    Family { id: "aj-shresti", name: "AJ Shresti", prefix: "AJShresti", level: "2", role: "Level 2 Sub-Headings & OS Default", has_italic: true, italic_angle: 10.0, x_height: 534, generic: "sans-serif" },
    Family { id: "aj-talin", name: "AJ Talin", prefix: "AJTalin", level: "3", role: "Level 3 Script", has_italic: true, italic_angle: 11.0, x_height: 492, generic: "cursive" },
    Family { id: "aj-anushya", name: "AJ Anushya", prefix: "AJAnushya", level: "body", role: "Body Reading", has_italic: true, italic_angle: 9.0, x_height: 556, generic: "sans-serif" },
    Family { id: "aaahhh-fonts-vibe", name: "Aaahhh Fonts Vibe", prefix: "AaahhhFontsVibe", level: "sound", role: "Sound of Font", has_italic: true, italic_angle: 9.5, x_height: 558, generic: "sans-serif" },
];

pub const WEIGHTS: [u16; 3] = [400, 600, 800];

/// ss06-ss18 take effect in Aaahhh Fonts Vibe only.
pub const SOUND_STYLISTIC_SETS: [(&str, &str); 14] = [
    ("ta", "ss06"), ("hi", "ss07"), ("te", "ss08"), ("ml", "ss09"), ("kn", "ss10"), ("bn", "ss11"), ("pa", "ss12"),
    ("ar", "ss13"), ("ur", "ss13"), ("ja", "ss14"), ("ru", "ss15"), ("zh", "ss16"), ("th", "ss17"), ("am", "ss18"),
];

const BASE_FEATURES: &str = "kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05";

/// OCR disambiguation metadata: character groups the designs keep visually distinct.
pub const OCR_DISAMBIGUATION_GROUPS: [&[&str]; 5] =
    [&["0", "O", "o"], &["I", "l", "1"], &["a", "b", "6"], &["rn", "m"], &["cl", "d"]];
pub const OCR_RECOMMENDED_FAMILY: &str = "AJ Anushya";
pub const OCR_RECOMMENDED_MIN_PX: u16 = 12;
pub const OCR_FEATURE_SETTINGS: &str = "\"zero\" 1, \"tnum\" 1, \"liga\" 0, \"dlig\" 0";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Error {
    UnknownFamily,
    UnsupportedWeight,
    NoItalic,
    UnsupportedFeature,
    UnsupportedLanguage,
    UnsafeBaseUrl,
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}

impl std::error::Error for Error {}

pub fn family(key: &str) -> Result<&'static Family, Error> {
    FAMILIES.iter().find(|f| f.id == key || f.name == key).ok_or(Error::UnknownFamily)
}

pub fn style_name(key: &str, weight: u16, italic: bool) -> Result<String, Error> {
    let fam = family(key)?;
    let name = match weight {
        400 => "Regular",
        600 => "SemiBold",
        800 => "ExtraBold",
        _ => return Err(Error::UnsupportedWeight),
    };
    if italic && !fam.has_italic {
        return Err(Error::NoItalic);
    }
    Ok(match (italic, weight) {
        (false, _) => name.to_string(),
        (true, 400) => "Italic".to_string(),
        (true, _) => format!("{name}Italic"),
    })
}

pub fn font_url(key: &str, weight: u16, italic: bool, format: &str, base_url: &str) -> Result<String, Error> {
    if base_url.contains(['"', '\'', '\\', '\r', '\n']) {
        return Err(Error::UnsafeBaseUrl);
    }
    Ok(format!(
        "{}/{}-{}.{}",
        base_url.trim_end_matches('/'),
        family(key)?.prefix,
        style_name(key, weight, italic)?,
        format
    ))
}

pub fn font_stack(key: &str) -> Result<String, Error> {
    let fam = family(key)?;
    Ok(format!("\"{}\", system-ui, {}", fam.name, fam.generic))
}

pub fn font_face_css(key: &str, weight: u16, italic: bool, base_url: &str) -> Result<String, Error> {
    let url = font_url(key, weight, italic, "woff2", base_url)?;
    let name = family(key)?.name;
    let style = if italic { "italic" } else { "normal" };
    Ok(format!(
        "@font-face {{ font-family: \"{name}\"; src: url(\"{url}\") format(\"woff2\"); font-weight: {weight}; font-style: {style}; font-display: swap; }}"
    ))
}

/// All 27 `@font-face` rules.
pub fn all_font_face_css(base_url: &str) -> Result<String, Error> {
    let mut rules = Vec::with_capacity(27);
    for fam in FAMILIES.iter() {
        let italics: &[bool] = if fam.has_italic { &[false, true] } else { &[false] };
        for &italic in italics {
            for weight in WEIGHTS {
                rules.push(font_face_css(fam.id, weight, italic, base_url)?);
            }
        }
    }
    Ok(rules.join("\n"))
}

fn is_feature(tag: &str) -> bool {
    BASE_FEATURES.split(' ').any(|t| t == tag) || SOUND_STYLISTIC_SETS.iter().any(|(_, t)| *t == tag)
}

pub fn feature_settings(enable: &[&str], disable: &[&str]) -> Result<String, Error> {
    let mut parts = Vec::new();
    for (tags, value) in [(enable, 1), (disable, 0)] {
        for tag in tags {
            if !is_feature(tag) {
                return Err(Error::UnsupportedFeature);
            }
            parts.push(format!("\"{tag}\" {value}"));
        }
    }
    Ok(if parts.is_empty() { "normal".to_string() } else { parts.join(", ") })
}

pub fn sound_feature_settings(language: &str) -> Result<String, Error> {
    let (_, tag) = SOUND_STYLISTIC_SETS
        .iter()
        .find(|(lang, _)| *lang == language)
        .ok_or(Error::UnsupportedLanguage)?;
    feature_settings(&[tag, "calt"], &[])
}
