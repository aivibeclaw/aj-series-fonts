/**
 * AJ Series & Aaahhh Fonts Vibe SDK v3.1.0 (TypeScript, zero dependencies).
 * Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
 * SPDX-License-Identifier: LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
 * Provided "AS IS" without warranty. https://fonts.aivibe.cloud
 */
export const VERSION = "3.1.0";

/* PLACEHOLDER: Configure your CDN/local font base URL here */
export const DEFAULT_FONT_BASE_URL = "https://fonts.aivibe.cloud/fonts";

export type Weight = 400 | 600 | 800;
export type Format = "woff2" | "woff" | "ttf" | "otf";

export interface Family {
  readonly id: string;
  readonly name: string;
  readonly prefix: string;
  readonly level: "1" | "2" | "3" | "body" | "sound";
  readonly role: string;
  readonly hasItalic: boolean;
  readonly italicAngle: number;
  readonly xHeight: number;
  readonly generic: string;
}

const f = (id: string, name: string, prefix: string, level: Family["level"], role: string,
  hasItalic: boolean, italicAngle: number, xHeight: number, generic: string): Family =>
  ({ id, name, prefix, level, role, hasItalic, italicAngle, xHeight, generic });

export const FAMILIES: readonly Family[] = [
  f("aj-sahasvi", "AJ Sahasvi", "AJSahasvi", "1", "Level 1 Headers (H1)", false, 0, 516, "serif"),
  f("aj-shresti", "AJ Shresti", "AJShresti", "2", "Level 2 Sub-Headings & OS Default", true, 10, 534, "sans-serif"),
  f("aj-talin", "AJ Talin", "AJTalin", "3", "Level 3 Script", true, 11, 492, "cursive"),
  f("aj-anushya", "AJ Anushya", "AJAnushya", "body", "Body Reading", true, 9, 556, "sans-serif"),
  f("aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", "sound", "Sound of Font", true, 9.5, 558, "sans-serif"),
];

export const WEIGHTS: readonly Weight[] = [400, 600, 800];
const WEIGHT_NAMES: Record<Weight, string> = { 400: "Regular", 600: "SemiBold", 800: "ExtraBold" };

/** ss06-ss18 take effect in Aaahhh Fonts Vibe only. */
export const SOUND_STYLISTIC_SETS: Readonly<Record<string, string>> = {
  ta: "ss06", hi: "ss07", te: "ss08", ml: "ss09", kn: "ss10", bn: "ss11", pa: "ss12",
  ar: "ss13", ur: "ss13", ja: "ss14", ru: "ss15", zh: "ss16", th: "ss17", am: "ss18",
};

export const FEATURE_TAGS: ReadonlySet<string> = new Set([
  ..."kern mark mkmk calt liga dlig locl tnum pnum zero case sups subs numr dnom frac ss01 ss02 ss05".split(" "),
  ...Object.values(SOUND_STYLISTIC_SETS),
]);

/** OCR disambiguation metadata: character groups the designs keep visually distinct. */
export const OCR_DISAMBIGUATION_GROUPS = [["0", "O", "o"], ["I", "l", "1"], ["a", "b", "6"], ["rn", "m"], ["cl", "d"]] as const;
export const OCR_RECOMMENDED_FAMILY = "AJ Anushya";
export const OCR_RECOMMENDED_MIN_PX = 12;
export const OCR_FEATURE_SETTINGS = '"zero" 1, "tnum" 1, "liga" 0, "dlig" 0';

export function family(key: string): Family {
  const found = FAMILIES.find((x) => x.id === key || x.name === key);
  if (!found) throw new Error(`unknown family: ${key}`);
  return found;
}

export function styleName(key: string, weight: Weight = 400, italic = false): string {
  const fam = family(key);
  if (!WEIGHTS.includes(weight)) throw new Error(`unsupported weight: ${weight}`);
  if (italic && !fam.hasItalic) throw new Error(`${fam.name} has no italic`);
  if (!italic) return WEIGHT_NAMES[weight];
  return weight === 400 ? "Italic" : `${WEIGHT_NAMES[weight]}Italic`;
}

export function fontUrl(key: string, weight: Weight = 400, italic = false,
  format: Format = "woff2", baseUrl: string = DEFAULT_FONT_BASE_URL): string {
  if (/["'\\\r\n]/.test(baseUrl)) throw new Error("baseUrl contains characters that are unsafe in CSS");
  return `${baseUrl.replace(/\/+$/, "")}/${family(key).prefix}-${styleName(key, weight, italic)}.${format}`;
}

export function fontStack(key: string): string {
  const fam = family(key);
  return `"${fam.name}", system-ui, ${fam.generic}`;
}

export function fontFaceCss(key: string, weight: Weight = 400, italic = false,
  baseUrl: string = DEFAULT_FONT_BASE_URL): string {
  const url = fontUrl(key, weight, italic, "woff2", baseUrl);
  return `@font-face { font-family: "${family(key).name}"; src: url("${url}") format("woff2"); ` +
    `font-weight: ${weight}; font-style: ${italic ? "italic" : "normal"}; font-display: swap; }`;
}

/** All 27 @font-face rules. */
export function allFontFaceCss(baseUrl: string = DEFAULT_FONT_BASE_URL): string {
  return FAMILIES.flatMap((fam) =>
    (fam.hasItalic ? [false, true] : [false]).flatMap((italic) =>
      WEIGHTS.map((w) => fontFaceCss(fam.id, w, italic, baseUrl)))).join("\n");
}

/** Value for CSS font-feature-settings. */
export function featureSettings(enable: readonly string[] = [], disable: readonly string[] = []): string {
  const render = (tags: readonly string[], value: 0 | 1) => tags.map((tag) => {
    if (!FEATURE_TAGS.has(tag)) throw new Error(`unsupported OpenType feature: ${tag}`);
    return `"${tag}" ${value}`;
  });
  return [...render(enable, 1), ...render(disable, 0)].join(", ") || "normal";
}

export function soundFeatureSettings(language: string): string {
  if (!Object.prototype.hasOwnProperty.call(SOUND_STYLISTIC_SETS, language)) {
    throw new Error(`no Sound of Font set for language: ${language}`);
  }
  return featureSettings([SOUND_STYLISTIC_SETS[language], "calt"]);
}
