// AJ Series Enterprise Typefaces v3.0.0 — Chromium fontSettings Auto-Binder
const SCRIPTS = ["Zyyy", "Latn", "Deva", "Taml", "Telu", "Mlym", "Knda", "Guru", "Beng", "Arab", "Cyrl", "Hans", "Thai", "Ethi", "Jpan", "Hang"];
const BINDINGS = [
  { genericFamily: "standard", fontId: "AJ Shresti" },
  { genericFamily: "sansserif", fontId: "AJ Shresti" },
  { genericFamily: "serif", fontId: "AJ Sahasvi" },
  { genericFamily: "cursive", fontId: "AJ Talin" }
];

function applyAJSeriesFontSettings() {
  if (!chrome.fontSettings || !chrome.fontSettings.setFont) return;
  for (const script of SCRIPTS) {
    for (const b of BINDINGS) {
      chrome.fontSettings.setFont({
        genericFamily: b.genericFamily,
        script,
        fontId: b.fontId
      }, () => { void chrome.runtime.lastError; });
    }
  }
}

chrome.runtime.onInstalled.addListener(applyAJSeriesFontSettings);
chrome.runtime.onStartup.addListener(applyAJSeriesFontSettings);
