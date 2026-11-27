/**
 * Supabase Edge Function (Deno / Web Fetch API) — AJ Series & Aaahhh Fonts Vibe (v3.1.0)
 * Read-only OpenType stylistic-set (`ss06`–`ss18`) & font-catalog configuration helper.
 * Core phonetic/lexicon engine internals are proprietary and withheld from public distribution.
 *
 * /* PLACEHOLDER: Configure SUPABASE_URL and SUPABASE_ANON_KEY via `supabase secrets set` if pairing with custom storage */
 * /* PLACEHOLDER: Configure AJ_FONT_CDN_BASE_URL (defaults to https://fonts.aivibe.cloud/fonts) */
 */

export const SUITE_VERSION = "3.1.0";
export const CDN_BASE_URL = /* PLACEHOLDER: Override with your self-hosted font asset origin */ "https://fonts.aivibe.cloud/fonts";

export const SOUND_OF_FONT_FEATURES: Record<string, string> = {
  ta: "ss06",
  "ta-sen": "ss06",
  hi: "ss07",
  "hi-prathmic": "ss07",
  mr: "ss07",
  sa: "ss07",
  te: "ss08",
  ml: "ss09",
  kn: "ss10",
  bn: "ss11",
  pa: "ss12",
  ar: "ss13",
  ur: "ss13",
  ja: "ss14",
  ru: "ss15",
  zh: "ss16",
  th: "ss17",
  am: "ss18",
};

export function buildCssFontDeclaration(locale = "en"): { fontFamily: string; fontFeatureSettings: string } {
  const ss = SOUND_OF_FONT_FEATURES[locale];
  const tags = ss ? [`"calt" 1`, `"kern" 1`, `"${ss}" 1`] : [`"calt" 1`, `"kern" 1`];
  return {
    fontFamily: "'Aaahhh Fonts Vibe', 'AJ Anushya', sans-serif",
    fontFeatureSettings: tags.join(", "),
  };
}

export default {
  async fetch(req: Request): Promise<Response> {
    const url = new URL(req.url);
    const locale = url.searchParams.get("lang") || "en";
    const body = JSON.stringify({
      suite: "AJ Series & Aaahhh Fonts Vibe",
      version: SUITE_VERSION,
      copyright: "Copyright (c) 2026 Aravind Jayamohan, India",
      warranty: "PROVIDED STRICTLY AS IS WITHOUT WARRANTY OF ANY KIND",
      cdnBaseUrl: CDN_BASE_URL,
      locale,
      css: buildCssFontDeclaration(locale),
    });
    return new Response(body, {
      headers: {
        "content-type": "application/json; charset=utf-8",
        "cache-control": "public, max-age=300",
      },
    });
  },
};
