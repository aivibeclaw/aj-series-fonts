/**
 * AJ Series Fonts — Cross-Platform Smart Keystroke, Global Currency & Symbol Mapper
 * Works identically across Web (React/Next/Vue), Electron, React Native, iOS, and Android.
 *
 * Also mirrors OpenType `ss05` ("AJ Smart Currency & Symbol Keystrokes") built directly
 * into every compiled AJ Shresti, AJ Sahasvi, AJ Anushya, AJ Talin, and Aaahhh Fonts Vibe
 * font binary, plus `Aaahhh Fonts Vibe` ("Sound of Font") `:lang:word` phonetic triggers!
 *
 * Copyright (c) 2026 Aravind Jayamohan, India (@ajaitech) — v3.1.0 — https://fonts.aivibe.cloud
 * Authorized Licensees: Aivibe Software Services Private Limited (Chennai),
 *                       AjAir Tech Mobility LLP, QRaise Structures.
 */

export interface AJKeystrokeEntry {
  shortcut: string;
  char: string;
  codepoint: string;
  name: string;
  category: "currency" | "analytical" | "agentic" | "punctuation" | "phonetic";
  macOption?: string;
  winAlt?: string;
}

export const AJ_KEYSTROKES: readonly AJKeystrokeEntry[] = [
  // Top Global Currencies + Unicode 17.0 Saudi Riyal & Unicode 18.0 UAE Dirham
  { shortcut: ":inr:", char: "\u20B9", codepoint: "U+20B9", name: "Indian Rupee", category: "currency", macOption: "Opt+R", winAlt: "Ctrl+Alt+4" },
  { shortcut: ":usd:", char: "$", codepoint: "U+0024", name: "US Dollar", category: "currency", macOption: "Shift+4", winAlt: "Shift+4" },
  { shortcut: ":eur:", char: "\u20AC", codepoint: "U+20AC", name: "Euro", category: "currency", macOption: "Opt+Shift+2", winAlt: "Alt+0128" },
  { shortcut: ":gbp:", char: "\u00A3", codepoint: "U+00A3", name: "British Pound", category: "currency", macOption: "Opt+3", winAlt: "Alt+0163" },
  { shortcut: ":jpy:", char: "\u00A5", codepoint: "U+00A5", name: "Japanese Yen / Chinese Yuan", category: "currency", macOption: "Opt+Y", winAlt: "Alt+0165" },
  { shortcut: ":krw:", char: "\u20A9", codepoint: "U+20A9", name: "Korean Won", category: "currency", macOption: "Opt+W", winAlt: "Alt+8361" },
  { shortcut: ":sar:", char: "\u20C1", codepoint: "U+20C1", name: "Saudi Riyal (Unicode 17.0)", category: "currency", macOption: "Opt+Shift+R", winAlt: "AHK :sar:" },
  { shortcut: ":aed:", char: "\u20C3", codepoint: "U+20C3", name: "UAE Dirham (Unicode 18.0)", category: "currency", macOption: "Opt+Shift+D", winAlt: "AHK :aed:" },
  { shortcut: ":btc:", char: "\u20BF", codepoint: "U+20BF", name: "Bitcoin", category: "currency", macOption: "Opt+Shift+B", winAlt: "AHK :btc:" },
  { shortcut: ":thb:", char: "\u0E3F", codepoint: "U+0E3F", name: "Thai Baht", category: "currency", macOption: "Opt+B", winAlt: "AHK :thb:" },
  { shortcut: ":vnd:", char: "\u20AB", codepoint: "U+20AB", name: "Vietnamese Dong", category: "currency", macOption: "Opt+D", winAlt: "AHK :vnd:" },
  { shortcut: ":try:", char: "\u20BA", codepoint: "U+20BA", name: "Turkish Lira", category: "currency", macOption: "Opt+T", winAlt: "AHK :try:" },
  { shortcut: ":rub:", char: "\u20BD", codepoint: "U+20BD", name: "Russian Ruble", category: "currency", macOption: "Opt+Shift+P", winAlt: "AHK :rub:" },
  { shortcut: ":php:", char: "\u20B1", codepoint: "U+20B1", name: "Philippine Peso", category: "currency", macOption: "Opt+P", winAlt: "AHK :php:" },
  { shortcut: ":ngn:", char: "\u20A6", codepoint: "U+20A6", name: "Nigerian Naira", category: "currency", macOption: "Opt+Shift+N", winAlt: "AHK :ngn:" },
  { shortcut: ":ils:", char: "\u20AA", codepoint: "U+20AA", name: "Israeli New Shekel", category: "currency", macOption: "Opt+Shift+S", winAlt: "AHK :ils:" },
  { shortcut: ":uah:", char: "\u20B4", codepoint: "U+20B4", name: "Ukrainian Hryvnia", category: "currency", macOption: "Opt+Shift+H", winAlt: "AHK :uah:" },
  { shortcut: ":ghs:", char: "\u20B5", codepoint: "U+20B5", name: "Ghanaian Cedi", category: "currency", macOption: "Opt+Shift+C", winAlt: "AHK :ghs:" },
  { shortcut: ":kzt:", char: "\u20B8", codepoint: "U+20B8", name: "Kazakhstani Tenge", category: "currency", macOption: "Opt+Shift+T", winAlt: "AHK :kzt:" },
  { shortcut: ":azn:", char: "\u20BC", codepoint: "U+20BC", name: "Azerbaijani Manat", category: "currency", macOption: "Opt+Shift+M", winAlt: "AHK :azn:" },
  { shortcut: ":gel:", char: "\u20BE", codepoint: "U+20BE", name: "Georgian Lari", category: "currency", macOption: "Opt+Shift+L", winAlt: "AHK :gel:" },
  { shortcut: ":bdt:", char: "\u09F3", codepoint: "U+09F3", name: "Bangladeshi / Bengali Taka", category: "currency", macOption: "AHK :bdt:", winAlt: "AHK :bdt:" },
  { shortcut: ":tmr:", char: "\u0BF9", codepoint: "U+0BF9", name: "Classical Sen Tamil Rupee", category: "currency", macOption: "AHK :tmr:", winAlt: "AHK :tmr:" },
  // Analytical & Agentic UI Symbols
  { shortcut: ":ok:", char: "\u2713", codepoint: "U+2713", name: "Checkmark", category: "agentic", macOption: "Opt+V", winAlt: "AHK :ok:" },
  { shortcut: ":no:", char: "\u2715", codepoint: "U+2715", name: "Cross / Fail", category: "agentic", macOption: "Opt+X", winAlt: "AHK :no:" },
  { shortcut: ":up:", char: "\u25B2", codepoint: "U+25B2", name: "KPI Trend Up", category: "analytical", macOption: "Opt+Shift+U", winAlt: "AHK :up:" },
  { shortcut: ":dn:", char: "\u25BC", codepoint: "U+25BC", name: "KPI Trend Down", category: "analytical", macOption: "Opt+Shift+J", winAlt: "AHK :dn:" },
  { shortcut: ":star:", char: "\u2605", codepoint: "U+2605", name: "Solid Star", category: "agentic", macOption: "Opt+Shift+8", winAlt: "AHK :star:" },
  { shortcut: ":ai:", char: "\u2726", codepoint: "U+2726", name: "AI Sparkle", category: "agentic", macOption: "Opt+Shift+A", winAlt: "AHK :ai:" },
  { shortcut: ":cmd:", char: "\u2318", codepoint: "U+2318", name: "Command Key", category: "agentic", macOption: "Opt+Shift+K", winAlt: "AHK :cmd:" },
  { shortcut: ":warn:", char: "\u26A0", codepoint: "U+26A0", name: "Warning Triangle", category: "analytical", macOption: "Opt+Shift+W", winAlt: "AHK :warn:" },
  { shortcut: ":gear:", char: "\u2699", codepoint: "U+2699", name: "Settings Gear", category: "agentic", macOption: "Opt+Shift+G", winAlt: "AHK :gear:" },
  // Sound of Font (Aaahhh Fonts Vibe) Inline Phonetic Keystroke Triggers
  { shortcut: ":ta:vanakkam", char: "வணக்கம்", codepoint: "ta-phonetic", name: "Tamil Greeting (Vanakkam)", category: "phonetic" },
  { shortcut: ":ta:vanakam", char: "வணக்கம்", codepoint: "ta-phonetic", name: "Tamil Greeting (Vanakam)", category: "phonetic" },
  { shortcut: ":ta:wanakkam", char: "வணக்கம்", codepoint: "ta-phonetic", name: "Tamil Greeting (Wanakkam)", category: "phonetic" },
  { shortcut: ":ta:Vanakam", char: "வணக்கம்", codepoint: "ta-phonetic", name: "Tamil Greeting (Vanakam)", category: "phonetic" },
  { shortcut: ":ta:VANAKKAM", char: "வணக்கம்", codepoint: "ta-phonetic", name: "Tamil Greeting (VANAKKAM)", category: "phonetic" },
  { shortcut: ":ta:1u", char: "ஒன்று", codepoint: "ta-num-1u", name: "Tamil Number Sound 1u / onnu / ondru", category: "phonetic" },
  { shortcut: ":ta:onnu", char: "ஒன்று", codepoint: "ta-num-onnu", name: "Tamil Number Sound onnu", category: "phonetic" },
  { shortcut: ":ta:ondru", char: "ஒன்று", codepoint: "ta-num-ondru", name: "Tamil Number Sound ondru", category: "phonetic" },
  { shortcut: ":ta:2u", char: "இரண்டு", codepoint: "ta-num-2u", name: "Tamil Number Sound 2u", category: "phonetic" },
  { shortcut: ":ta:3u", char: "மூன்று", codepoint: "ta-num-3u", name: "Tamil Number Sound 3u", category: "phonetic" },
  { shortcut: ":ta:4u", char: "நான்கு", codepoint: "ta-num-4u", name: "Tamil Number Sound 4u", category: "phonetic" },
  { shortcut: ":ta:5u", char: "ஐந்து", codepoint: "ta-num-5u", name: "Tamil Number Sound 5u", category: "phonetic" },
  { shortcut: ":ta:6u", char: "ஆறு", codepoint: "ta-num-6u", name: "Tamil Number Sound 6u", category: "phonetic" },
  { shortcut: ":ta:7u", char: "ஏழு", codepoint: "ta-num-7u", name: "Tamil Number Sound 7u", category: "phonetic" },
  { shortcut: ":ta:8u", char: "எட்டு", codepoint: "ta-num-8u", name: "Tamil Number Sound 8u", category: "phonetic" },
  { shortcut: ":ta:9u", char: "ஒன்பது", codepoint: "ta-num-9u", name: "Tamil Number Sound 9u", category: "phonetic" },
  { shortcut: ":ta:10u", char: "பத்து", codepoint: "ta-num-10u", name: "Tamil Number Sound 10u", category: "phonetic" },
  { shortcut: ":ta:nandri", char: "நன்றி", codepoint: "ta-phonetic", name: "Tamil Thank You (Nandri)", category: "phonetic" },
  { shortcut: ":ta:vinnappam", char: "விண்ணப்பம்", codepoint: "ta-phonetic", name: "Tamil Application (Vinnappam)", category: "phonetic" },
  { shortcut: ":ta:panivudan", char: "பணிவுடன்", codepoint: "ta-phonetic", name: "Tamil Humbly (Panivudan)", category: "phonetic" },
  { shortcut: ":hi:namaste", char: "नमस्ते", codepoint: "hi-phonetic", name: "Hindi Greeting (Namaste)", category: "phonetic" },
  { shortcut: ":hi:namasthe", char: "नमस्ते", codepoint: "hi-phonetic", name: "Hindi Greeting (Namasthe)", category: "phonetic" },
  { shortcut: ":hi:dhanyavad", char: "धन्यवाद", codepoint: "hi-phonetic", name: "Hindi Thank You (Dhanyavad)", category: "phonetic" },
  { shortcut: ":hi:bharat", char: "भारत", codepoint: "hi-phonetic", name: "Hindi India (Bharat)", category: "phonetic" },
  { shortcut: ":te:namaskaram", char: "నమస్కారం", codepoint: "te-phonetic", name: "Telugu Greeting (Namaskaram)", category: "phonetic" },
  { shortcut: ":ml:namaskaram", char: "നമസ്കാരം", codepoint: "ml-phonetic", name: "Malayalam Greeting (Namaskaram)", category: "phonetic" },
  { shortcut: ":kn:namaskara", char: "ನಮಸ್ಕಾರ", codepoint: "kn-phonetic", name: "Kannada Greeting (Namaskara)", category: "phonetic" },
  { shortcut: ":bn:nomoshkar", char: "নমস্কার", codepoint: "bn-phonetic", name: "Bengali Greeting (Nomoshkar)", category: "phonetic" },
  { shortcut: ":bn:nomoskar", char: "নমস্কার", codepoint: "bn-phonetic", name: "Bengali Greeting (Nomoskar)", category: "phonetic" },
  { shortcut: ":bn:namaskar", char: "নমস্কার", codepoint: "bn-phonetic", name: "Bengali Greeting (Namaskar)", category: "phonetic" },
  { shortcut: ":pa:satsriakal", char: "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ", codepoint: "pa-phonetic", name: "Punjabi Greeting (Sat Sri Akal)", category: "phonetic" },
  { shortcut: ":ar:marhaban", char: "مرحبا", codepoint: "ar-phonetic", name: "Arabic Greeting (Marhaban)", category: "phonetic" },
  { shortcut: ":ur:adab", char: "آداب", codepoint: "ur-phonetic", name: "Urdu Greeting (Adab)", category: "phonetic" },
  { shortcut: ":ja:konnichiwa", char: "こんにちは", codepoint: "ja-phonetic", name: "Japanese Greeting (Konnichiwa)", category: "phonetic" },
  { shortcut: ":ru:privet", char: "привет", codepoint: "ru-phonetic", name: "Russian Greeting (Privet)", category: "phonetic" },
  { shortcut: ":zh:nihao", char: "你好", codepoint: "zh-phonetic", name: "Chinese Greeting (Nihao)", category: "phonetic" },
  { shortcut: ":th:sawatdee", char: "สวัสดี", codepoint: "th-phonetic", name: "Thai Greeting (Sawatdee)", category: "phonetic" },
  { shortcut: ":am:selam", char: "ሰላም", codepoint: "am-phonetic", name: "Amharic Greeting (Selam)", category: "phonetic" },
] as const;

const SHORTCUT_MAP = new Map<string, string>(AJ_KEYSTROKES.map((k) => [k.shortcut, k.char]));
const SHORTCUT_REGEX = /:[a-z]{2}:[A-Za-z0-9]+|:[a-z]{2,4}:/g;

/** Expand AJ `:code:` & `:lang:word` mnemonics into canonical Unicode characters for clipboard/DB/PDF parity. */
export function expandAJKeystrokes(input: string): string {
  return input.replace(SHORTCUT_REGEX, (m) => SHORTCUT_MAP.get(m) ?? m);
}
