/**
 * AJ Series & Aaahhh Fonts Vibe (v3.1.0) — TypeScript Agentic & Sound-of-Font Contract
 * Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
 * Authorized Publishers: Aivibe Software Services Private Limited (Chennai),
 *                        AjAir Tech Mobility LLP, QRaise Structures.
 */

export type AJFontFamily =
  | "AJ Shresti"
  | "AJ Sahasvi"
  | "AJ Anushya"
  | "AJ Talin"
  | "Aaahhh Fonts Vibe";

export type AJFontWeight = 400 | 600 | 800;

export type AJPlatformLanguage =
  | "en" | "ta" | "ta-sen" | "hi" | "hi-prathmic" | "te" | "ml" | "kn"
  | "bn" | "mr" | "pa" | "ar" | "ur" | "sa" | "ja" | "ru"
  | "es" | "fr" | "de" | "ms" | "zh" | "ko" | "th" | "am"
  | "vi";

export type AJOpenTypeFeature =
  | "kern" | "mark" | "calt" | "liga" | "dlig"
  | "tnum" | "pnum" | "zero" | "ss01" | "ss02" | "ss05"
  | "ss06" | "ss07" | "ss08" | "ss09" | "ss10" | "ss11" | "ss12" | "ss13" | "ss14" | "ss15" | "ss16" | "ss17" | "ss18"
  | "case" | "sups" | "subs" | "numr" | "dnom" | "frac";

export interface AJTypographySelection {
  family: AJFontFamily;
  weight: AJFontWeight;
  italic?: boolean;
  language?: AJPlatformLanguage;
  soundOfFontMode?: boolean;
  openTypeFeatures?: AJOpenTypeFeature[];
  accessibilityProfile?: "standard" | "wcag-aaa" | "dyslexia-wide" | "micro-9pt" | "ocr-extreme";
  presentationEffect?: "default-3d-mild-gradient-press" | "clean" | "paper-pressed-3d" | "glossy-3d";
}

export interface AJStrokeGlyphPath {
  advance: number;
  strokes: Array<
    | { type: "stroke"; d: string; w: number }
    | { type: "circle"; cx: number; cy: number; r: number }
  >;
}
