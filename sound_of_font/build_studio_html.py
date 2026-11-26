"""Generate standalone 24-language Sound of Font Web Studio HTML from sound_of_font.ts."""
from __future__ import annotations

import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]

FAMILIES = [
    ("aaahhh-fonts-vibe", "Aaahhh Fonts Vibe", "AaahhhFontsVibe", True),
    ("aj-shresti", "AJ Shresti", "AJShresti", True),
    ("aj-sahasvi", "AJ Sahasvi", "AJSahasvi", False),
    ("aj-anushya", "AJ Anushya", "AJAnushya", True),
    ("aj-talin", "AJ Talin", "AJTalin", True),
]


def _compile_inline_engine() -> str:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [
                "npx", "tsc", "--target", "ES2020", "--module", "ES2020",
                "--strict", "--outDir", tmp,
                str(ROOT / "sound_of_font/engine/sound_of_font.ts"),
            ],
            check=True,
        )
        esm = (pathlib.Path(tmp) / "sound_of_font.js").read_text(encoding="utf-8")
    return re.sub(r"^export\s+", "", esm, flags=re.MULTILINE)


def _build_font_faces(local_mode: bool) -> str:
    rules = []
    for slug, fam, pfx, has_it in FAMILIES:
        styles = [("Regular", 400, "normal"), ("SemiBold", 600, "normal"), ("ExtraBold", 800, "normal")]
        if has_it:
            styles += [("Italic", 400, "italic"), ("SemiBoldItalic", 600, "italic"), ("ExtraBoldItalic", 800, "italic")]
        for sty, wt, fst in styles:
            url = f"../../dist/{slug}/woff2/{pfx}-{sty}.woff2" if local_mode else f"/fonts/{pfx}-{sty}.woff2"
            rules.append(
                f'@font-face {{ font-family: "{fam}"; font-weight: {wt}; font-style: {fst}; '
                f'font-display: swap; src: url("{url}") format("woff2"); }}'
            )
    return "\n".join(rules)


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aaahhh Fonts Vibe — Sound of Font Studio (All 24 Languages · v3.0.0)</title>
<meta name="description" content="Interactive Sound of Font smart typing studio powered by Aaahhh Fonts Vibe (v3.0.0) across all 24 languages, 5 document templates, automatic spell &amp; grammar correction, OS dictionary merge, and Default 3D Mild-Gradient Press.">
<link rel="canonical" href="https://fonts.aivibe.cloud/sound-of-font">
<link rel="icon" type="image/png" href="/favicon.png">
<meta property="og:title" content="Aaahhh Fonts Vibe — Sound of Font Studio (All 24 Languages · v3.0.0)">
<meta property="og:description" content="English-keyboard-to-24-language smart phonetic typing, spell &amp; grammar agreement, OS dictionary merge, and context-aware inline helptext.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://fonts.aivibe.cloud/sound-of-font">
<meta property="og:image" content="https://fonts.aivibe.cloud/favicon.png">
<style>
__FONT_FACES__
:root { --font: "Aaahhh Fonts Vibe"; --weight: 400; --fstyle: normal; --ink: #141c2b; --muted: #5c667a; --line: #d6dce8; --accent: #3b28cc; --bg: #f4f5fa; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--font), system-ui, sans-serif; font-weight: 400; line-height: 1.6; }
main { max-width: 1020px; margin: 0 auto; padding: 24px 16px 56px; }
header.top { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 16px; }
h1 { font-weight: 800; margin: 0 0 4px; font-size: clamp(24px, 4vw, 34px); }
h2 { font-weight: 600; font-size: 17px; margin: 0 0 10px; }
p.sub { color: var(--muted); margin: 0; max-width: 720px; font-size: 15px; }
.spark-badge { font-size: 12px; font-weight: 600; background: #e8edff; color: #283593; border: 1px solid #c5d1ff; border-radius: 999px; padding: 6px 12px; white-space: nowrap; }
section { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; margin-bottom: 16px; box-shadow: 0 4px 14px rgba(16, 24, 40, 0.03); }
.row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 10px; }
button, select, input[type="text"] { font: inherit; border: 1px solid var(--line); border-radius: 8px; padding: 7px 12px; background: #fff; color: inherit; font-size: 14px; }
button { cursor: pointer; border-radius: 999px; transition: border-color 0.12s, background 0.12s; }
button:hover { border-color: var(--accent); background: #f5f3ff; }
button.active-tpl { background: var(--accent); color: #fff; border-color: var(--accent); }
#heading { flex: 1; min-width: 210px; font-weight: 600; }
.editor { position: relative; }
.editor textarea, .editor .ghost { font-family: var(--font), system-ui, sans-serif; font-weight: var(--weight); font-style: var(--fstyle); font-size: 20px; line-height: 1.8; padding: 14px; border: 1px solid var(--line); border-radius: 10px; width: 100%; margin: 0; white-space: pre-wrap; overflow-wrap: break-word; letter-spacing: normal; }
.editor textarea { position: relative; background: transparent; color: var(--ink); height: 220px; resize: vertical; display: block; overflow-y: scroll; }
.editor .ghost { position: absolute; inset: 0; overflow-y: scroll; color: transparent; border-color: transparent; pointer-events: none; }
.ghost span.ghost-tip { color: #909ab0; }
.hint { color: var(--muted); font-size: 13.5px; }
output { display: block; margin-top: 10px; font-size: 21px; min-height: 34px; font-weight: var(--weight); font-style: var(--fstyle); }
.dict-bar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 8px; }
footer { text-align: center; color: var(--muted); font-size: 13px; margin-top: 20px; }
footer a { color: var(--accent); text-decoration: none; margin: 0 6px; }
</style>
</head>
<body>
<main>
  <header class="top">
    <div>
      <h1>Aaahhh Fonts Vibe · Sound of Font Studio</h1>
      <p class="sub">English-keyboard-to-24-language smart phonetic typing, automatic spell &amp; grammar agreement, OS/user dictionary fusion, and context-aware inline helptext. Press <b>Space</b> to commit word sound or <b>Tab</b> to accept full clause.</p>
    </div>
    <div class="spark-badge" id="sparkIndex">⚡ AI Metadata Indexer: booting…</div>
  </header>

  <section>
    <h2>1. Smart Context Writer &amp; Inline Helptext (All 24 Languages · 5 Document Contexts)</h2>
    <div class="row">
      <select id="lang" aria-label="Language"></select>
      <input type="text" id="heading" aria-label="Document heading" value="Leave Letter">
      <button type="button" data-template="Leave Letter" class="active-tpl">Leave Letter</button>
      <button type="button" data-template="Official Email">Official Email</button>
      <button type="button" data-template="FinTech Invoice">FinTech / Invoice</button>
      <button type="button" data-template="Greeting">Greeting</button>
      <button type="button" data-template="ERP Stock Note">ERP Note</button>
    </div>
    <div class="editor">
      <div class="ghost" id="ghost" aria-hidden="true"></div>
      <textarea id="body" aria-label="Document body" spellcheck="false" placeholder="Start typing 1+ letters (e.g. R + Space in English, m + Space in Tamil, s + Space in Hindi, or vanakkam / 1u / Rs1)..."></textarea>
    </div>
    <div class="row" id="next" style="margin-top:10px"></div>
    <div class="hint" id="status">Ready — auto-matched to your system/browser language or English default.</div>
  </section>

  <section>
    <h2>2. Sound, Number/Currency Guard &amp; Grammar Verification Pills</h2>
    <div class="row" id="pills"></div>
    <output id="result"></output>
  </section>

  <section>
    <h2>3. All 5 Canonical AJ Series Typefaces (27 Styles · Default 3D Mild-Gradient Press · OS/User Dictionary Merge)</h2>
    <div class="row">
      <select id="family" aria-label="Font family">
        <option value="Aaahhh Fonts Vibe">Aaahhh Fonts Vibe (Sound of Font · 5th Family)</option>
        <option value="AJ Shresti">AJ Shresti (Active OS UI &amp; Subtitles)</option>
        <option value="AJ Sahasvi">AJ Sahasvi (Bold Headings · Royal Small-Caps)</option>
        <option value="AJ Anushya">AJ Anushya (Zero-Stub Reading Clarity)</option>
        <option value="AJ Talin">AJ Talin (0° Connected Running Script)</option>
      </select>
      <select id="weight" aria-label="Font weight">
        <option value="400">Regular (400 — Full-Bodied)</option>
        <option value="600">SemiBold (600 — Crisp Step)</option>
        <option value="800">ExtraBold (800 — Commanding)</option>
      </select>
      <select id="fstyle" aria-label="Font style">
        <option value="normal">Upright (Roman)</option>
        <option value="italic">Italic</option>
      </select>
      <input type="color" id="inkcolor" value="#141c2b" title="Live 3D Pressed Ink Color">
      <label class="hint">Load custom font: <input type="file" id="fontfile" accept=".woff2,.woff,.ttf,.otf"></label>
    </div>
    <div class="dict-bar">
      <input type="text" id="customRoman" placeholder="Roman trigger (e.g. chennai)" style="width:190px">
      <input type="text" id="customNative" placeholder="Target word (e.g. சென்னை)" style="width:190px">
      <button type="button" id="addWordBtn">+ Add Dictionary Word</button>
      <label class="hint">Merge OS/Wordlist (.txt): <input type="file" id="dictfile" accept=".txt,.dic,.words"></label>
    </div>
    <div class="hint" id="fontstatus" style="margin-top:8px">All 5 AJ Series families (27 styles · 400 / 600 / 800 + Italics) pre-wired with Default 3D Mild-Gradient Press.</div>
  </section>

  <footer>
    <a href="/">AJ Series Foundry Home</a> ·
    <a href="/install">1-Click OS Installers (v3.0.0)</a> ·
    <a href="/api/v2/fonts.json">AI Agent Registry JSON</a> ·
    Exclusive Copyright Owner: <strong>Aravind Jayamohan, India</strong>
  </footer>
</main>

<script>
"use strict";
__INLINE_ENGINE__

const $ = (id) => document.getElementById(id);
const engine = new SoundOfFontEngine();
const body = $("body"), ghost = $("ghost"), heading = $("heading"), langSelect = $("lang");

const LANG_NATIVE_LABELS = {
  en: "English (Default)",
  ta: "Tamil · தமிழ்",
  "ta-sen": "Sen Tamil · செந்தமிழ்",
  hi: "Hindi · हिन्दी",
  "hi-prathmic": "Prathmic Hindi · प्राथमिक हिन्दी",
  te: "Telugu · తెలుగు",
  ml: "Malayalam · മലയാളം",
  kn: "Kannada · ಕನ್ನಡ",
  bn: "Bengali · বাংলা",
  mr: "Marathi · मराठी",
  pa: "Punjabi · ਪੰਜਾਬੀ",
  ar: "Arabic · العربية",
  ur: "Urdu · اردو",
  sa: "Sanskrit · संस्कृतम्",
  ja: "Japanese · 日本語",
  ru: "Russian · Русский",
  es: "Spanish · Español",
  fr: "French · Français",
  de: "German · Deutsch",
  ms: "Malay (SG / MY) · Bahasa Melayu",
  zh: "Chinese (CN / SG / MY) · 中文",
  th: "Thai · ไทย",
  am: "Amharic · አማርኛ",
  ko: "Korean · 한국어"
};

for (const code of Object.keys(LANGUAGES)) {
  const opt = document.createElement("option");
  opt.value = code;
  opt.textContent = LANG_NATIVE_LABELS[code] || LANGUAGES[code];
  langSelect.append(opt);
}
langSelect.value = engine.language;

// Background AI Metadata Auto-Indexer (zero main-thread jank)
const indexer = new BackgroundFontMetadataIndexer();
const allFiles = [];
for (const [slug, pfx, hasIt] of [
  ["aaahhh-fonts-vibe", "AaahhhFontsVibe", true],
  ["aj-shresti", "AJShresti", true],
  ["aj-sahasvi", "AJSahasvi", false],
  ["aj-anushya", "AJAnushya", true],
  ["aj-talin", "AJTalin", true]
]) {
  const stys = ["Regular", "SemiBold", "ExtraBold"].concat(hasIt ? ["Italic", "SemiBoldItalic", "ExtraBoldItalic"] : []);
  for (const s of stys) for (const ext of ["woff2", "woff", "ttf", "otf"]) allFiles.push(`${slug}/${ext}/${pfx}-${s}.${ext}`);
}
const dispatchMs = indexer.start(allFiles, {
  "aaahhh-fonts-vibe": 0.998, "aj-shresti": 0.995, "aj-sahasvi": 0.992, "aj-anushya": 0.999, "aj-talin": 0.985
});
indexer.done.then((idx) => {
  if (idx) {
    $("sparkIndex").textContent = `⚡ AI Metadata Indexed: ${idx.familyCount} families · ${idx.styleCount} styles · ${idx.languages.length} langs (${dispatchMs.toFixed(2)}ms dispatch)`;
  }
});

let pending = null;

function syncDir() {
  const rtl = langSelect.value === "ar" || langSelect.value === "ur";
  body.dir = rtl ? "rtl" : "ltr";
  ghost.dir = rtl ? "rtl" : "ltr";
}

function extractTrailingToken(str) {
  const unspaced = ["zh", "ja", "th"].includes(langSelect.value);
  const m = (unspaced ? /[\\x21-\\x7E]+$/ : /\\S*$/).exec(str);
  return m ? m[0] : "";
}

function dirArrow(langCode) {
  return (langCode === "ar" || langCode === "ur") ? " ← " : " → ";
}

function splitAtCaret() {
  const caret = body.selectionStart ?? body.value.length;
  const before = body.value.slice(0, caret);
  const after = body.value.slice(caret);
  const token = extractTrailingToken(before);
  return { prior: before.slice(0, before.length - token.length), token, before, after, caret };
}

function refresh() {
  ghost.textContent = "";
  $("next").textContent = "";
  pending = null;
  syncDir();
  const { prior, token, before, after } = splitAtCaret();
  if (after && !/^\\s*$/.test(after)) return;
  const lang = langSelect.value;
  const sug = engine.suggestInline(heading.value, prior, token, lang);
  const joiner = ["zh", "ja", "th"].includes(lang) ? "" : " ";
  const arrow = dirArrow(lang);
  if (sug.fullClauseSuggestion || sug.inlineGhostCompletion) {
    const core = splitPunct(token)[1];
    let tail = "";
    if (sug.fullClauseSuggestion) {
      const inline = core && sug.fullClauseSuggestion.toLowerCase().startsWith(core.toLowerCase());
      tail = inline ? sug.fullClauseSuggestion.slice(core.length) : (token ? arrow : "") + sug.fullClauseSuggestion;
      pending = { prior, clause: sug.fullClauseSuggestion, after, joiner };
    } else if (sug.inlineGhostCompletion) {
      tail = sug.inlineGhostCompletion;
      pending = { prior, clause: token + sug.inlineGhostCompletion, after, joiner };
    }
    if (tail) {
      const span = document.createElement("span");
      span.className = "ghost-tip";
      span.textContent = tail;
      ghost.append(before, span);
      ghost.scrollTop = body.scrollTop;
    }
  }
  for (const word of sug.nextWords) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = word;
    $("next").append(btn);
  }
}

function commitBeforeCaret(isNewline = false) {
  const caret = body.selectionStart;
  if (caret < 1) return;
  const beforeSep = body.value.slice(0, caret - 1);
  const afterSep = body.value.slice(caret);
  const token = extractTrailingToken(beforeSep);
  if (!token) return;
  const prior = beforeSep.slice(0, beforeSep.length - token.length);
  const lang = langSelect.value;
  const began = performance.now();
  const res = engine.onSpaceCommit(heading.value, prior, token, lang);
  let updatedLeft = isNewline ? res.text.replace(/[ \\t]+$/, "") + "\\n" : res.text;
  if (/[.!?।؟۔።]\\s*$/.test(updatedLeft)) {
    const trailing = /\\s*$/.exec(updatedLeft)[0];
    updatedLeft = engine.autoCorrectSentence(updatedLeft.trimEnd(), lang) + trailing;
  }
  const elapsed = performance.now() - began;
  body.value = updatedLeft + afterSep;
  body.setSelectionRange(updatedLeft.length, updatedLeft.length);
  $("status").textContent = `${token}${dirArrow(lang)}${res.committedWord} (${elapsed.toFixed(2)} ms · ${LANGUAGES[lang]})`;
}

body.addEventListener("input", (event) => {
  if (!event.isComposing && event.inputType === "insertText" && event.data === " ") commitBeforeCaret(false);
  else if (!event.isComposing && (event.inputType === "insertLineBreak" || (event.inputType === "insertText" && event.data === "\\n"))) commitBeforeCaret(true);
  refresh();
});
body.addEventListener("keydown", (event) => {
  if (event.key !== "Tab" || event.shiftKey || !pending) return;
  event.preventDefault();
  const nextLeft = pending.prior + pending.clause + pending.joiner;
  body.value = nextLeft + pending.after;
  body.setSelectionRange(nextLeft.length, nextLeft.length);
  refresh();
});
body.addEventListener("click", refresh);
body.addEventListener("keyup", (e) => { if (e.key.startsWith("Arrow")) refresh(); });
body.addEventListener("scroll", () => { ghost.scrollTop = body.scrollTop; });

$("next").addEventListener("click", (event) => {
  if (event.target.tagName !== "BUTTON") return;
  const { prior, token, after } = splitAtCaret();
  const lang = langSelect.value;
  const joiner = ["zh", "ja", "th"].includes(lang) ? "" : " ";
  const base = token ? engine.onSpaceCommit(heading.value, prior, token, lang).text : prior;
  const nextLeft = base + event.target.textContent + joiner;
  body.value = nextLeft + after;
  body.focus();
  body.setSelectionRange(nextLeft.length, nextLeft.length);
  refresh();
});

heading.addEventListener("input", refresh);
langSelect.addEventListener("change", () => {
  engine.language = langSelect.value;
  body.value = "";
  refresh();
});
document.querySelectorAll("[data-template]").forEach((btn) => btn.addEventListener("click", () => {
  document.querySelectorAll("[data-template]").forEach((b) => b.classList.remove("active-tpl"));
  btn.classList.add("active-tpl");
  heading.value = btn.dataset.template;
  body.value = "";
  body.focus();
  refresh();
}));

const SOUND_PILLS = [
  ["1", "ta", "convert"], ["Rs1", "ta", "convert"], ["Rs.1,250.50/-", "ta", "convert"],
  ["Rs 1u", "ta", "convert"], ["No. 1", "ta", "convert"], ["$10", "ta", "convert"],
  ["1u", "ta", "convert"], ["onnu", "ta", "convert"], ["ondru", "ta", "convert"],
  ["vanakam", "ta", "convert"], ["wanakkam", "ta", "convert"], ["namasthe", "hi", "convert"],
  ["namaskaram", "ml", "convert"], ["namaskara", "kn", "convert"], ["satsriakal", "pa", "convert"],
  ["marhaba", "ar", "convert"], ["shukriya", "ur", "convert"], ["konnichiwa", "ja", "convert"],
  ["privet", "ru", "convert"], ["nihao", "zh", "convert"], ["sawatdee", "th", "convert"],
  ["selam", "am", "convert"], ["terimakasih", "ms", "convert"],
  ["i recieve teh mail . he don't know.", "en", "grammar"],
  ["நான் வருகிறீர்கள்.", "ta", "grammar"],
  ["मैं ठीक है", "hi", "grammar"]
];
for (const [text, lang, mode] of SOUND_PILLS) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.textContent = `${text} (${lang})`;
  btn.addEventListener("click", () => {
    const t0 = performance.now();
    const out = mode === "grammar" ? engine.autoCorrectSentence(text, lang) : engine.convertText(text, lang);
    const dt = performance.now() - t0;
    $("result").textContent = `${text}${dirArrow(lang)}${out}  [${dt.toFixed(2)} ms]`;
  });
  $("pills").append(btn);
}

function updateFontVars() {
  const fam = $("family").value;
  const isSahasvi = fam === "AJ Sahasvi";
  if (isSahasvi && $("fstyle").value === "italic") $("fstyle").value = "normal";
  document.documentElement.style.setProperty("--font", `"${fam}"`);
  document.documentElement.style.setProperty("--weight", $("weight").value);
  document.documentElement.style.setProperty("--fstyle", $("fstyle").value);
  document.documentElement.style.setProperty("--ink", $("inkcolor").value);
}
$("family").addEventListener("change", updateFontVars);
$("weight").addEventListener("change", updateFontVars);
$("fstyle").addEventListener("change", updateFontVars);
$("inkcolor").addEventListener("input", updateFontVars);

$("fontfile").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const name = "Local " + file.name.replace(/[^\\w -]/g, " ");
  try {
    const face = new FontFace(name, await file.arrayBuffer());
    document.fonts.add(await face.load());
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = file.name;
    $("family").append(opt);
    $("family").value = name;
    updateFontVars();
    $("fontstatus").textContent = `Loaded custom font: ${file.name}`;
  } catch (err) {
    $("fontstatus").textContent = `Could not load ${file.name}: ${err.message}`;
  }
});

$("addWordBtn").addEventListener("click", () => {
  const r = $("customRoman").value.trim();
  const n = $("customNative").value.trim();
  if (!r || !n) return;
  engine.addUserWords({ [r]: n }, langSelect.value);
  $("fontstatus").textContent = `Added custom mapping [${langSelect.value}]: "${r}" → "${n}"`;
  $("customRoman").value = "";
  $("customNative").value = "";
  refresh();
});

$("dictfile").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const txt = await file.text();
  const total = await engine.mergeOsDictionary(txt);
  $("fontstatus").textContent = `Merged dictionary "${file.name}" (${total.toLocaleString()} active OS/dictionary words).`;
  refresh();
});

refresh();
</script>
</body>
</html>
"""


def main() -> None:
    inline_engine = _compile_inline_engine()
    for out_path, local_mode in [
        (ROOT / "sound_of_font/web/sound-of-font-studio.html", True),
        (ROOT / "hosting/public/sound-of-font.html", False),
    ]:
        html = (
            HTML_TEMPLATE
            .replace("__FONT_FACES__", _build_font_faces(local_mode))
            .replace("__INLINE_ENGINE__", inline_engine)
        )
        out_path.write_text(html, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(ROOT)} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
