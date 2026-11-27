/**
 * Wix Velo Custom Element (`<aj-sound-input>`) — Aaahhh Fonts Vibe ("Sound of Font" v3.1.0)
 * Drop into Wix Site `public/custom-elements/wix-velo-sound-of-font.js` and bind tag `aj-sound-input`.
 * Provides real inline phonetic conversion across 24 languages, currency/number guards (`Rs 1u`, `$ 1u`, `No. 1u`, `1 -> 1`),
 * Tab ghost-completion, Space/Enter commit, and Leave-Letter / Invoice inline helptext!
 * PLACEHOLDER: <Wix site custom-element binding configuration>
 */

const AJ_WIX_LEXICON = {
  ta: { vanakkam: "வணக்கம்", vanakam: "வணக்கம்", wanakkam: "வணக்கம்", nandri: "நன்றி", anbu: "அன்பு", madhippirkuriya: "மதிப்பிற்குரிய", ayya: "ஐயா,", vinnappam: "விண்ணப்பம்", panivudan: "பணிவுடன்", "1u": "ஒன்று", onnu: "ஒன்று", ondru: "ஒன்று", "2u": "இரண்டு", "3u": "மூன்று" },
  hi: { namaste: "नमस्ते", namasthe: "नमस्ते", namaskar: "नमस्कार", dhanyavad: "धन्यवाद", mahoday: "महोदय,", savinay: "सविनय", nivedan: "निवेदन", bharat: "भारत", main: "मैं", hain: "हैं", "1u": "एक", ek: "एक" },
  te: { namaskaram: "నమస్కారం", dhanyavadalu: "ధన్యవాదాలు", gauravaniyulaina: "గౌరవనీయులైన", "1u": "ఒకటి", okati: "ఒకటి" },
  ml: { namaskaram: "നമസ്കാരം", nanni: "നന്ദി", bahumanappetta: "ബഹുമാനപ്പെട്ട", sar: "സർ,", "1u": "ഒന്ന്", onnu: "ഒന്ന്" },
  kn: { namaskara: "ನಮಸ್ಕಾರ", dhanyavadagalu: "ಧನ್ಯವಾದಗಳು", gauravaniya: "ಗೌರವನೀಯ", "1u": "ಒಂದು", ondu: "ಒಂದು" },
  bn: { nomoshkar: "নমস্কার", nomoskar: "নমস্কার", namaskar: "নমস্কার", dhonnobad: "ধন্যবাদ", "1u": "এক", ek: "এক" },
  pa: { satsriakal: "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", dhannvad: "ਧੰਨਵਾਦ", "1u": "ਇੱਕ", ikk: "ਇੱਕ" },
  ar: { salam: "سلام", marhaba: "مرحبا", shukran: "شكرا", "1u": "واحد", wahid: "واحد" },
  ur: { salam: "سلام", adab: "آداب", shukriya: "شکریہ", "1u": "ایک", ek: "ایک" },
  zh: { nihao: "你好", ni: "你", hao: "好", wo: "我", xiexie: "谢谢", bukeqi: "不客气", qing: "请", zhongguo: "中国", zaijian: "再见", "1u": "一" },
  ja: { konnichiwa: "こんにちは", arigatou: "ありがとう", ohayou: "おはよう", "1u": "ひとつ" },
  th: { sawatdee: "สวัสดี", khobkhun: "ขอบคุณ", "1u": "หนึ่ง" },
  am: { selam: "ሰላም", ameseginalehu: "አመሰግናለሁ", sira: "ሥራ", alem: "ዓለም", "1u": "አንድ" },
  ko: { annyeonghaseyo: "안녕하세요", gamsahabnida: "감사합니다", "1u": "하나" },
  ru: { privet: "привет", spasibo: "спасибо", "1u": "один" },
  es: { hola: "hola", gracias: "gracias", manana: "mañana", "1u": "uno" },
  fr: { bonjour: "bonjour", merci: "merci", coeur: "cœur", "1u": "un" },
  de: { hallo: "hallo", danke: "danke", fur: "für", "1u": "eins" },
  ms: { selamat: "selamat", terimakasih: "terima kasih", "1u": "satu" },
};

const AJ_WIX_TEMPLATES = {
  leave_letter: {
    en: [["Respected", "Respected"], ["Sir,", "Sir,"], ["I", "I"], ["am", "am"], ["unable", "unable"], ["to", "to"], ["attend", "attend"], ["work", "work"], ["today.", "today."]],
    ta: [["madhippirkuriya", "மதிப்பிற்குரிய"], ["ayya", "ஐயா,"], ["naan", "நான்"], ["indru", "இன்று"], ["viduppu", "விடுப்பு"], ["vendugiren.", "வேண்டுகிறேன்."]],
    hi: [["adarniya", "आदरणीय"], ["mahoday", "महोदय,"], ["savinay", "सविनय"], ["nivedan", "निवेदन"], ["hai.", "है।"]],
  },
  invoice: {
    en: [["Please", "Please"], ["find", "find"], ["attached", "attached"], ["Invoice", "Invoice"], ["for", "for"], ["payment.", "payment."]],
    ta: [["dayavuseydhu", "தயவுசெய்து"], ["indha", "இந்த"], ["pattiyalai", "பட்டியலை"], ["sarithirukka.", "சரிபார்க்கவும்."]],
  },
};

const CURRENCY_GUARD_RE = /(?:Rs\.?|INR|USD|EUR|GBP|RM|S\$|No\.?|#|[₹$€£¥₩฿₫৳])\s*$/i;

class AJSoundInputElement extends HTMLElement {
  static get observedAttributes() {
    return ["lang", "heading", "placeholder"];
  }

  attributeChangedCallback() {
    if (this._mounted) this._refreshHint();
  }

  get value() {
    return this._ta ? this._ta.value : "";
  }

  set value(v) {
    if (this._ta) {
      this._ta.value = String(v ?? "");
      this._refreshHint();
    }
  }

  connectedCallback() {
    if (this._mounted) return;
    this._mounted = true;
    const shadow = this.attachShadow({ mode: "open" });
    const style = document.createElement("style");
    style.textContent = `
      @import url("https://fonts.aivibe.cloud/css/index.css");
      :host { display: block; font-family: "Aaahhh Fonts Vibe", "AJ Shresti", sans-serif; }
      .wrap { display: flex; flex-direction: column; gap: 6px; }
      textarea {
        width: 100%; min-height: 120px; padding: 12px; box-sizing: border-box;
        font: 400 18px/1.6 "Aaahhh Fonts Vibe", "AJ Shresti", sans-serif;
        border: 1px solid #cbd5e1; border-radius: 10px; background: #ffffff; color: #0f172a;
      }
      .helptext {
        min-height: 24px; padding: 4px 10px; border-radius: 8px;
        background: #f1f5f9; color: #334155; font-size: 13px;
        display: flex; align-items: center; justify-content: space-between;
      }
      .ghost { color: #2563eb; font-weight: 600; }
    `;
    const wrap = document.createElement("div");
    wrap.className = "wrap";
    this._ta = document.createElement("textarea");
    this._ta.placeholder = this.getAttribute("placeholder") || "Type phonetically with Aaahhh Fonts Vibe…";
    this._hint = document.createElement("div");
    this._hint.className = "helptext";

    this._ta.addEventListener("keydown", (e) => {
      if (e.key === "Tab" && this._activeCompletion) {
        e.preventDefault();
        this._commitCurrentToken(this._activeCompletion + " ");
      } else if (e.key === "Enter") {
        this._commitBeforeDelimiter();
      }
    });

    this._ta.addEventListener("input", (e) => {
      const lang = this._lang();
      this._ta.dir = lang === "ar" || lang === "ur" ? "rtl" : "ltr";
      if (e.inputType === "insertText" && e.data === " ") {
        this._commitOnSpace();
      }
      this._refreshHint();
      this.dispatchEvent(new CustomEvent("change", { detail: { value: this._ta.value, lang } }));
    });

    wrap.append(this._ta, this._hint);
    shadow.append(style, wrap);
    this._refreshHint();
  }

  _lang() {
    return (this.getAttribute("lang") || "ta").toLowerCase();
  }

  _detectCategory(prior) {
    const h = `${this.getAttribute("heading") || ""} ${prior || ""}`.toLowerCase();
    if (/(leave|permission|application|request|sick|absence|viduppu)/.test(h)) return "leave_letter";
    if (/(invoice|bill|payment|receipt|gst)/.test(h)) return "invoice";
    return null;
  }

  _splitBeforeCaret(raw) {
    const lang = this._lang();
    const re = ["zh", "ja", "th"].includes(lang) ? /[\x21-\x7E]+$/ : /\S*$/;
    const m = re.exec(raw);
    const idx = m ? m.index : raw.length;
    return { prior: raw.slice(0, idx), token: raw.slice(idx) };
  }

  _convertToken(prior, token) {
    const lang = this._lang();
    if (!token || lang === "en") return token;
    if (/^\d+$/.test(token)) return token;
    if (CURRENCY_GUARD_RE.test(prior.trimEnd() + " ") && /^\d/.test(token)) return token;
    if (/^(?:Rs\.?|INR|USD|RM|No\.?|[₹$€£¥])\d/i.test(token)) return token;
    const m = /^([A-Za-z0-9]+)([.,!?;:]*)$/.exec(token);
    if (!m) return token;
    const [, core, punct] = m;
    const dict = AJ_WIX_LEXICON[lang] || {};
    const hit = dict[core.toLowerCase()];
    return hit ? hit + punct : token;
  }

  _commitOnSpace() {
    const caret = this._ta.selectionStart ?? this._ta.value.length;
    if (caret < 1 || this._ta.value[caret - 1] !== " ") return;
    const beforeSpace = this._ta.value.slice(0, caret - 1);
    const afterCaret = this._ta.value.slice(caret);
    const { prior, token } = this._splitBeforeCaret(beforeSpace);
    if (!token) return;
    const converted = this._convertToken(prior, token);
    if (converted !== token) {
      const nextBefore = prior + converted + " ";
      this._ta.value = nextBefore + afterCaret;
      this._ta.setSelectionRange(nextBefore.length, nextBefore.length);
    }
  }

  _commitBeforeDelimiter() {
    const caret = this._ta.selectionStart ?? this._ta.value.length;
    const before = this._ta.value.slice(0, caret);
    const after = this._ta.value.slice(caret);
    const { prior, token } = this._splitBeforeCaret(before);
    if (!token) return;
    const converted = this._convertToken(prior, token);
    if (converted !== token) {
      const nextBefore = prior + converted;
      this._ta.value = nextBefore + after;
      this._ta.setSelectionRange(nextBefore.length, nextBefore.length);
    }
  }

  _commitCurrentToken(replacement) {
    const caret = this._ta.selectionStart ?? this._ta.value.length;
    const before = this._ta.value.slice(0, caret);
    const after = this._ta.value.slice(caret);
    const { prior } = this._splitBeforeCaret(before);
    const nextBefore = prior + replacement;
    this._ta.value = nextBefore + after;
    this._ta.setSelectionRange(nextBefore.length, nextBefore.length);
    this._refreshHint();
  }

  _refreshHint() {
    if (!this._hint || !this._ta) return;
    const lang = this._lang();
    const arrow = lang === "ar" || lang === "ur" ? " ← " : " → ";
    const caret = this._ta.selectionStart ?? this._ta.value.length;
    const { prior, token } = this._splitBeforeCaret(this._ta.value.slice(0, caret));
    const cat = this._detectCategory(prior);
    const seq = (cat && AJ_WIX_TEMPLATES[cat] && (AJ_WIX_TEMPLATES[cat][lang] || AJ_WIX_TEMPLATES[cat].en)) || [];
    this._activeCompletion = "";

    if (token) {
      const conv = this._convertToken(prior, token);
      const tplHit = seq.find(([rom]) => rom.toLowerCase().startsWith(token.toLowerCase()));
      if (tplHit) {
        this._activeCompletion = tplHit[1];
        this._hint.innerHTML = `<span>Phonetic${arrow}<span class="ghost">${tplHit[1]}</span></span><span>Tab to complete · Space to commit</span>`;
        return;
      }
      if (conv !== token) {
        this._activeCompletion = conv;
        this._hint.innerHTML = `<span>${token}${arrow}<span class="ghost">${conv}</span></span><span>Space / Tab to commit</span>`;
        return;
      }
    }
    const priorCount = prior.trim() ? prior.trim().split(/\s+/).length : 0;
    if (seq[priorCount]) {
      this._activeCompletion = seq[priorCount][1];
      this._hint.innerHTML = `<span>Next (${cat.replace("_", " ")})${arrow}<span class="ghost">${seq[priorCount][1]}</span></span><span>Tab to insert</span>`;
    } else {
      this._hint.innerHTML = `<span>Aaahhh Fonts Vibe (${lang.toUpperCase()})</span><span>1 → 1 · Rs 1u → Rs 1u · phonetic on Space</span>`;
    }
  }
}

if (typeof customElements !== "undefined" && !customElements.get("aj-sound-input")) {
  customElements.define("aj-sound-input", AJSoundInputElement);
}
