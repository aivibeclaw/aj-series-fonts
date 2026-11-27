# frozen_string_literal: true
# AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (Ruby 3.0+, standard library only)
# Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
# Provided "AS IS" without warranty. https://fonts.aivibe.cloud

module AJFontsSDK
  VERSION = "3.1.0"

  # /* PLACEHOLDER: Configure your CDN/local font base URL here */
  DEFAULT_FONT_BASE_URL = "https://fonts.aivibe.cloud/fonts"

  Family = Struct.new(:id, :name, :prefix, :level, :role, :has_italic, :italic_angle, :x_height, :generic, keyword_init: true)

  FAMILIES = [
    Family.new(id: "aj-sahasvi", name: "AJ Sahasvi", prefix: "AJSahasvi", level: "1", role: "Level 1 Headers (H1)", has_italic: false, italic_angle: 0.0, x_height: 516, generic: "serif"),
    Family.new(id: "aj-shresti", name: "AJ Shresti", prefix: "AJShresti", level: "2", role: "Level 2 Sub-Headings & OS Default", has_italic: true, italic_angle: 10.0, x_height: 534, generic: "sans-serif"),
    Family.new(id: "aj-talin", name: "AJ Talin", prefix: "AJTalin", level: "3", role: "Level 3 Script", has_italic: true, italic_angle: 11.0, x_height: 492, generic: "cursive"),
    Family.new(id: "aj-anushya", name: "AJ Anushya", prefix: "AJAnushya", level: "body", role: "Body Reading", has_italic: true, italic_angle: 9.0, x_height: 556, generic: "sans-serif"),
    Family.new(id: "aaahhh-fonts-vibe", name: "Aaahhh Fonts Vibe", prefix: "AaahhhFontsVibe", level: "sound", role: "Sound of Font", has_italic: true, italic_angle: 9.5, x_height: 558, generic: "sans-serif")
  ].freeze

  WEIGHTS = { 400 => "Regular", 600 => "SemiBold", 800 => "ExtraBold" }.freeze
  FORMATS = %w[woff2 woff ttf otf].freeze
  SOUND_STYLISTIC_SETS = {
    "ta" => "ss06", "hi" => "ss07", "te" => "ss08", "ml" => "ss09", "kn" => "ss10", "bn" => "ss11", "pa" => "ss12",
    "ar" => "ss13", "ur" => "ss13", "ja" => "ss14", "ru" => "ss15", "zh" => "ss16", "th" => "ss17", "am" => "ss18"
  }.freeze

  module_function

  def family(key)
    fam = FAMILIES.find { |f| f.id == key || f.name == key }
    raise ArgumentError, "Unknown family: #{key}" unless fam
    fam
  end

  def style_name(key, weight: 400, italic: false)
    fam = family(key)
    w = WEIGHTS.fetch(weight) { raise ArgumentError, "Unsupported weight: #{weight}" }
    raise ArgumentError, "#{fam.name} has no italic" if italic && !fam.has_italic
    return w unless italic
    weight == 400 ? "Italic" : "#{w}Italic"
  end

  def font_url(key, weight: 400, italic: false, fmt: "woff2", base_url: DEFAULT_FONT_BASE_URL)
    raise ArgumentError, "Unsupported format: #{fmt}" unless FORMATS.include?(fmt)
    raise ArgumentError, "Unsafe base_url" if base_url.match?(/["'\\\r\n]/)
    "#{base_url.chomp('/')}/#{family(key).prefix}-#{style_name(key, weight: weight, italic: italic)}.#{fmt}"
  end

  def font_face_css(key, weight: 400, italic: false, base_url: DEFAULT_FONT_BASE_URL)
    url = font_url(key, weight: weight, italic: italic, fmt: "woff2", base_url: base_url)
    st = italic ? "italic" : "normal"
    %(@font-face { font-family: "#{family(key).name}"; src: url("#{url}") format("woff2"); font-weight: #{weight}; font-style: #{st}; font-display: swap; })
  end

  def sound_feature_settings(language)
    tag = SOUND_STYLISTIC_SETS.fetch(language) { raise ArgumentError, "No Sound of Font set for language: #{language}" }
    %("#{tag}" 1, "calt" 1)
  end
end
