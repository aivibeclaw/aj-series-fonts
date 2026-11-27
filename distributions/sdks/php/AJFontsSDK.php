<?php
/**
 * AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (PHP 8.0+, no dependencies).
 * Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
 * SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
 * Provided "AS IS" without warranty. https://fonts.aivibe.cloud
 */
declare(strict_types=1);

namespace Aivibe\Fonts;

use InvalidArgumentException;

final class AJFontsSDK
{
    public const VERSION = '3.1.0';

    /* PLACEHOLDER: Configure your CDN/local font base URL here */
    public const DEFAULT_FONT_BASE_URL = 'https://fonts.aivibe.cloud/fonts';

    /** id => [name, prefix, level, role, hasItalic, italicAngle, xHeight, generic] */
    public const FAMILIES = [
        'aj-sahasvi' => ['name' => 'AJ Sahasvi', 'prefix' => 'AJSahasvi', 'level' => '1', 'role' => 'Level 1 Headers (H1)', 'hasItalic' => false, 'italicAngle' => 0, 'xHeight' => 516, 'generic' => 'serif'],
        'aj-shresti' => ['name' => 'AJ Shresti', 'prefix' => 'AJShresti', 'level' => '2', 'role' => 'Level 2 Sub-Headings & OS Default', 'hasItalic' => true, 'italicAngle' => 10, 'xHeight' => 534, 'generic' => 'sans-serif'],
        'aj-talin' => ['name' => 'AJ Talin', 'prefix' => 'AJTalin', 'level' => '3', 'role' => 'Level 3 Script', 'hasItalic' => true, 'italicAngle' => 11, 'xHeight' => 492, 'generic' => 'cursive'],
        'aj-anushya' => ['name' => 'AJ Anushya', 'prefix' => 'AJAnushya', 'level' => 'body', 'role' => 'Body Reading', 'hasItalic' => true, 'italicAngle' => 9, 'xHeight' => 556, 'generic' => 'sans-serif'],
        'aaahhh-fonts-vibe' => ['name' => 'Aaahhh Fonts Vibe', 'prefix' => 'AaahhhFontsVibe', 'level' => 'sound', 'role' => 'Sound of Font', 'hasItalic' => true, 'italicAngle' => 9.5, 'xHeight' => 558, 'generic' => 'sans-serif'],
    ];

    public const WEIGHTS = [400 => 'Regular', 600 => 'SemiBold', 800 => 'ExtraBold'];

    /** ss06-ss18 take effect in Aaahhh Fonts Vibe only. */
    public const SOUND_STYLISTIC_SETS = [
        'ta' => 'ss06', 'hi' => 'ss07', 'te' => 'ss08', 'ml' => 'ss09', 'kn' => 'ss10', 'bn' => 'ss11', 'pa' => 'ss12',
        'ar' => 'ss13', 'ur' => 'ss13', 'ja' => 'ss14', 'ru' => 'ss15', 'zh' => 'ss16', 'th' => 'ss17', 'am' => 'ss18',
    ];

    private const BASE_FEATURES = 'kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05';

    /** OCR disambiguation metadata: character groups the designs keep visually distinct. */
    public const OCR_DISAMBIGUATION_GROUPS = [['0', 'O', 'o'], ['I', 'l', '1'], ['a', 'b', '6'], ['rn', 'm'], ['cl', 'd']];
    public const OCR_RECOMMENDED_FAMILY = 'AJ Anushya';
    public const OCR_RECOMMENDED_MIN_PX = 12;
    public const OCR_FEATURE_SETTINGS = '"zero" 1, "tnum" 1, "liga" 0, "dlig" 0';

    /** Look up a family by id or name. */
    public static function family(string $key): array
    {
        foreach (self::FAMILIES as $id => $family) {
            if ($key === $id || $key === $family['name']) {
                return ['id' => $id] + $family;
            }
        }
        throw new InvalidArgumentException("unknown family: {$key}");
    }

    public static function styleName(string $key, int $weight = 400, bool $italic = false): string
    {
        $family = self::family($key);
        if (!isset(self::WEIGHTS[$weight])) {
            throw new InvalidArgumentException("unsupported weight: {$weight}");
        }
        if ($italic && !$family['hasItalic']) {
            throw new InvalidArgumentException("{$family['name']} has no italic");
        }
        if (!$italic) {
            return self::WEIGHTS[$weight];
        }
        return $weight === 400 ? 'Italic' : self::WEIGHTS[$weight] . 'Italic';
    }

    public static function fontUrl(string $key, int $weight = 400, bool $italic = false, string $format = 'woff2', string $baseUrl = self::DEFAULT_FONT_BASE_URL): string
    {
        if (strpbrk($baseUrl, "\"'\\\r\n") !== false) {
            throw new InvalidArgumentException('baseUrl contains characters that are unsafe in CSS');
        }
        return rtrim($baseUrl, '/') . '/' . self::family($key)['prefix'] . '-' . self::styleName($key, $weight, $italic) . '.' . $format;
    }

    public static function fontStack(string $key): string
    {
        $family = self::family($key);
        return "\"{$family['name']}\", system-ui, {$family['generic']}";
    }

    public static function fontFaceCss(string $key, int $weight = 400, bool $italic = false, string $baseUrl = self::DEFAULT_FONT_BASE_URL): string
    {
        $url = self::fontUrl($key, $weight, $italic, 'woff2', $baseUrl);
        $name = self::family($key)['name'];
        $style = $italic ? 'italic' : 'normal';
        return "@font-face { font-family: \"{$name}\"; src: url(\"{$url}\") format(\"woff2\"); font-weight: {$weight}; font-style: {$style}; font-display: swap; }";
    }

    /** All 27 @font-face rules. */
    public static function allFontFaceCss(string $baseUrl = self::DEFAULT_FONT_BASE_URL): string
    {
        $rules = [];
        foreach (self::FAMILIES as $id => $family) {
            foreach ($family['hasItalic'] ? [false, true] : [false] as $italic) {
                foreach (array_keys(self::WEIGHTS) as $weight) {
                    $rules[] = self::fontFaceCss($id, $weight, $italic, $baseUrl);
                }
            }
        }
        return implode("\n", $rules);
    }

    public static function featureSettings(array $enable = [], array $disable = []): string
    {
        $allowed = array_merge(explode(' ', self::BASE_FEATURES), array_values(self::SOUND_STYLISTIC_SETS));
        $parts = [];
        foreach ([[$enable, 1], [$disable, 0]] as [$tags, $value]) {
            foreach ($tags as $tag) {
                if (!in_array($tag, $allowed, true)) {
                    throw new InvalidArgumentException("unsupported OpenType feature: {$tag}");
                }
                $parts[] = "\"{$tag}\" {$value}";
            }
        }
        return $parts ? implode(', ', $parts) : 'normal';
    }

    public static function soundFeatureSettings(string $language): string
    {
        if (!isset(self::SOUND_STYLISTIC_SETS[$language])) {
            throw new InvalidArgumentException("no Sound of Font set for language: {$language}");
        }
        return self::featureSettings([self::SOUND_STYLISTIC_SETS[$language], 'calt']);
    }
}
