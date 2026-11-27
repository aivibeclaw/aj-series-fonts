-- AJ Series & Aaahhh Fonts Vibe catalog v3.1.0 (SQLite 3 / PostgreSQL)
-- Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
-- SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
-- Provided "AS IS" without warranty. https://fonts.aivibe.cloud

CREATE TABLE aj_setting (key VARCHAR(64) PRIMARY KEY, value VARCHAR(512) NOT NULL);

CREATE TABLE aj_family (
  id VARCHAR(32) PRIMARY KEY, name VARCHAR(64) NOT NULL UNIQUE, prefix VARCHAR(32) NOT NULL,
  level VARCHAR(8) NOT NULL, role VARCHAR(64) NOT NULL, has_italic INTEGER NOT NULL,
  italic_angle NUMERIC(4,1) NOT NULL, x_height INTEGER NOT NULL, generic_fallback VARCHAR(16) NOT NULL
);

CREATE TABLE aj_style (
  ps_name VARCHAR(64) PRIMARY KEY, family_id VARCHAR(32) NOT NULL REFERENCES aj_family(id),
  style VARCHAR(32) NOT NULL, weight INTEGER NOT NULL CHECK (weight IN (400, 600, 800)), italic INTEGER NOT NULL CHECK (italic IN (0, 1))
);

CREATE TABLE aj_locale (tag VARCHAR(16) PRIMARY KEY, direction VARCHAR(3) NOT NULL);

-- ss06-ss18 take effect in Aaahhh Fonts Vibe only.
CREATE TABLE aj_sound_set (language VARCHAR(8) PRIMARY KEY, feature_tag CHAR(4) NOT NULL);

-- OCR disambiguation metadata: space-separated groups the designs keep visually distinct.
CREATE TABLE aj_ocr_group (id INTEGER PRIMARY KEY, glyphs VARCHAR(32) NOT NULL);

/* PLACEHOLDER: Configure your CDN/local font base URL here */
INSERT INTO aj_setting VALUES ('font_base_url', 'https://fonts.aivibe.cloud/fonts');
INSERT INTO aj_setting VALUES ('version', '3.1.0');
INSERT INTO aj_setting VALUES ('ocr_feature_settings', '"zero" 1, "tnum" 1, "liga" 0, "dlig" 0');
INSERT INTO aj_setting VALUES ('ocr_recommended_family', 'AJ Anushya');
INSERT INTO aj_setting VALUES ('ocr_recommended_min_px', '12');

INSERT INTO aj_family VALUES
  ('aj-sahasvi', 'AJ Sahasvi', 'AJSahasvi', '1', 'Level 1 Headers (H1)', 0, 0, 516, 'serif'),
  ('aj-shresti', 'AJ Shresti', 'AJShresti', '2', 'Level 2 Sub-Headings & OS Default', 1, 10, 534, 'sans-serif'),
  ('aj-talin', 'AJ Talin', 'AJTalin', '3', 'Level 3 Script', 1, 11, 492, 'cursive'),
  ('aj-anushya', 'AJ Anushya', 'AJAnushya', 'body', 'Body Reading', 1, 9, 556, 'sans-serif'),
  ('aaahhh-fonts-vibe', 'Aaahhh Fonts Vibe', 'AaahhhFontsVibe', 'sound', 'Sound of Font', 1, 9.5, 558, 'sans-serif');

INSERT INTO aj_style VALUES
  ('AJSahasvi-Regular', 'aj-sahasvi', 'Regular', 400, 0),
  ('AJSahasvi-SemiBold', 'aj-sahasvi', 'SemiBold', 600, 0),
  ('AJSahasvi-ExtraBold', 'aj-sahasvi', 'ExtraBold', 800, 0),
  ('AJShresti-Regular', 'aj-shresti', 'Regular', 400, 0),
  ('AJShresti-SemiBold', 'aj-shresti', 'SemiBold', 600, 0),
  ('AJShresti-ExtraBold', 'aj-shresti', 'ExtraBold', 800, 0),
  ('AJShresti-Italic', 'aj-shresti', 'Italic', 400, 1),
  ('AJShresti-SemiBoldItalic', 'aj-shresti', 'SemiBoldItalic', 600, 1),
  ('AJShresti-ExtraBoldItalic', 'aj-shresti', 'ExtraBoldItalic', 800, 1),
  ('AJTalin-Regular', 'aj-talin', 'Regular', 400, 0),
  ('AJTalin-SemiBold', 'aj-talin', 'SemiBold', 600, 0),
  ('AJTalin-ExtraBold', 'aj-talin', 'ExtraBold', 800, 0),
  ('AJTalin-Italic', 'aj-talin', 'Italic', 400, 1),
  ('AJTalin-SemiBoldItalic', 'aj-talin', 'SemiBoldItalic', 600, 1),
  ('AJTalin-ExtraBoldItalic', 'aj-talin', 'ExtraBoldItalic', 800, 1),
  ('AJAnushya-Regular', 'aj-anushya', 'Regular', 400, 0),
  ('AJAnushya-SemiBold', 'aj-anushya', 'SemiBold', 600, 0),
  ('AJAnushya-ExtraBold', 'aj-anushya', 'ExtraBold', 800, 0),
  ('AJAnushya-Italic', 'aj-anushya', 'Italic', 400, 1),
  ('AJAnushya-SemiBoldItalic', 'aj-anushya', 'SemiBoldItalic', 600, 1),
  ('AJAnushya-ExtraBoldItalic', 'aj-anushya', 'ExtraBoldItalic', 800, 1),
  ('AaahhhFontsVibe-Regular', 'aaahhh-fonts-vibe', 'Regular', 400, 0),
  ('AaahhhFontsVibe-SemiBold', 'aaahhh-fonts-vibe', 'SemiBold', 600, 0),
  ('AaahhhFontsVibe-ExtraBold', 'aaahhh-fonts-vibe', 'ExtraBold', 800, 0),
  ('AaahhhFontsVibe-Italic', 'aaahhh-fonts-vibe', 'Italic', 400, 1),
  ('AaahhhFontsVibe-SemiBoldItalic', 'aaahhh-fonts-vibe', 'SemiBoldItalic', 600, 1),
  ('AaahhhFontsVibe-ExtraBoldItalic', 'aaahhh-fonts-vibe', 'ExtraBoldItalic', 800, 1);

INSERT INTO aj_locale VALUES
  ('en', 'ltr'),
  ('ta', 'ltr'),
  ('ta-sen', 'ltr'),
  ('hi', 'ltr'),
  ('hi-prathmic', 'ltr'),
  ('te', 'ltr'),
  ('ml', 'ltr'),
  ('kn', 'ltr'),
  ('bn', 'ltr'),
  ('mr', 'ltr'),
  ('pa', 'ltr'),
  ('ar', 'rtl'),
  ('ur', 'rtl'),
  ('sa', 'ltr'),
  ('ja', 'ltr'),
  ('ru', 'ltr'),
  ('es', 'ltr'),
  ('fr', 'ltr'),
  ('de', 'ltr'),
  ('ms', 'ltr'),
  ('zh', 'ltr'),
  ('ko', 'ltr'),
  ('th', 'ltr'),
  ('am', 'ltr'),
  ('vi', 'ltr');

INSERT INTO aj_sound_set VALUES
  ('ta', 'ss06'),
  ('hi', 'ss07'),
  ('te', 'ss08'),
  ('ml', 'ss09'),
  ('kn', 'ss10'),
  ('bn', 'ss11'),
  ('pa', 'ss12'),
  ('ar', 'ss13'),
  ('ur', 'ss13'),
  ('ja', 'ss14'),
  ('ru', 'ss15'),
  ('zh', 'ss16'),
  ('th', 'ss17'),
  ('am', 'ss18');

INSERT INTO aj_ocr_group VALUES
  (1, '0 O o'),
  (2, 'I l 1'),
  (3, 'a b 6'),
  (4, 'rn m'),
  (5, 'cl d');

CREATE VIEW aj_style_css AS
SELECT s.ps_name, f.name AS family, s.weight, s.italic,
       (SELECT value FROM aj_setting WHERE key = 'font_base_url') || '/' || s.ps_name || '.woff2' AS woff2_url,
       '@font-face { font-family: "' || f.name || '"; src: url("'
         || (SELECT value FROM aj_setting WHERE key = 'font_base_url') || '/' || s.ps_name
         || '.woff2") format("woff2"); font-weight: ' || s.weight || '; font-style: '
         || CASE WHEN s.italic = 1 THEN 'italic' ELSE 'normal' END || '; font-display: swap; }' AS font_face_css
FROM aj_style s JOIN aj_family f ON f.id = s.family_id;
