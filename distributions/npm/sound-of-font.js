/**
 * AJ Series: lightweight OpenType stylistic-set helper (ss06-ss18) for Aaahhh Fonts Vibe.
 * CSS plumbing only. No lexicon or transliteration engine is included.
 */
export const FONT_FAMILY = "Aaahhh Fonts Vibe";

export const STYLISTIC_SETS = Object.freeze([
  "ss06", "ss07", "ss08", "ss09", "ss10", "ss11", "ss12", "ss13", "ss14", "ss15", "ss16", "ss17", "ss18",
]);

export function featureSettings(...sets) {
  for (const set of sets) {
    if (!STYLISTIC_SETS.includes(set)) {
      throw new RangeError(`Unsupported stylistic set: ${set}`);
    }
  }
  return ["calt", "kern", ...sets].map((tag) => `"${tag}" 1`).join(", ");
}

export function soundOfFontStyle(...sets) {
  return { fontFamily: `'${FONT_FAMILY}'`, fontFeatureSettings: featureSettings(...sets) };
}

export function applySoundOfFont(element, ...sets) {
  Object.assign(element.style, soundOfFontStyle(...sets));
  return element;
}
