/** AJ Series: lightweight OpenType stylistic-set helper (ss06-ss18) for Aaahhh Fonts Vibe. */
export type StylisticSet =
  | "ss06" | "ss07" | "ss08" | "ss09" | "ss10" | "ss11" | "ss12"
  | "ss13" | "ss14" | "ss15" | "ss16" | "ss17" | "ss18";

export interface SoundOfFontStyle {
  fontFamily: string;
  fontFeatureSettings: string;
}

export declare const FONT_FAMILY: "Aaahhh Fonts Vibe";
export declare const STYLISTIC_SETS: readonly StylisticSet[];
export declare function featureSettings(...sets: StylisticSet[]): string;
export declare function soundOfFontStyle(...sets: StylisticSet[]): SoundOfFontStyle;
export declare function applySoundOfFont<T extends { style: SoundOfFontStyle }>(
  element: T,
  ...sets: StylisticSet[]
): T;
