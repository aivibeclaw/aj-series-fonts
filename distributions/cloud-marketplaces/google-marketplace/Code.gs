/**
 * Google Workspace Marketplace Add-on — AJ Series & Aaahhh Fonts Vibe ("Sound of Font") v3.1.0
 * Supports Google Docs, Google Slides & Google Sheets across all 24 languages!
 * Copyright (c) 2026 Aravind Jayamohan, India. All Rights Reserved.
 * Authorized Publisher: Aivibe Software Services Private Limited, Chennai.
 * PLACEHOLDER: <Google Cloud project and Marketplace SDK listing configuration, set in the Apps Script console>
 */

var SOUND_LEXICON_24 = {
  "ta": { "vanakkam": "வணக்கம்", "vanakam": "வணக்கம்", "wanakkam": "வணக்கம்", "nandri": "நன்றி", "anbu": "அன்பு", "1u": "ஒன்று", "onnu": "ஒன்று", "ondru": "ஒன்று", "2u": "இரண்டு", "3u": "மூன்று", "4u": "நான்கு", "5u": "ஐந்து", "vinnappam": "விண்ணப்பம்", "panivudan": "பணிவுடன்", "india": "இந்தியா" },
  "ta-sen": { "vanakkam": "வணக்கம்", "vanakam": "வணக்கம்", "wanakkam": "வணக்கம்", "nandri": "நன்றி", "anbu": "அன்பு", "1u": "ஒன்று", "onnu": "ஒன்று", "ondru": "ஒன்று", "2u": "இரண்டு", "3u": "மூன்று", "vinnappam": "விண்ணப்பம்", "panivudan": "பணிவுடன்", "india": "இந்தியா" },
  "hi": { "namaste": "नमस्ते", "namasthe": "नमस्ते", "namaskar": "नमस्कार", "dhanyavad": "धन्यवाद", "bharat": "भारत", "main": "मैं", "hain": "हैं", "1u": "एक", "ek": "एक" },
  "hi-prathmic": { "namaste": "नमस्ते", "namaskar": "नमस्कार", "dhanyavad": "धन्यवाद", "bharat": "भारत", "main": "मैं", "hain": "हैं", "1u": "एक", "ek": "एक" },
  "te": { "namaskaram": "నమస్కారం", "dhanyavadalu": "ధన్యవాదాలు", "1u": "ఒకటి", "okati": "ఒకటి" },
  "ml": { "namaskaram": "നമസ്കാരം", "nanni": "നന്ദി", "sar": "സർ,", "1u": "ഒന്ന്", "onnu": "ഒന്ന്" },
  "kn": { "namaskara": "ನಮಸ್ಕಾರ", "dhanyavadagalu": "ಧನ್ಯವಾದಗಳು", "1u": "ಒಂದು", "ondu": "ಒಂದು" },
  "bn": { "nomoshkar": "নমস্কার", "nomoskar": "নমস্কার", "namaskar": "নমস্কার", "dhonnobad": "ধন্যবাদ", "1u": "এক", "ek": "এক" },
  "mr": { "namaskar": "नमस्कार", "dhanyavad": "धन्यवाद", "bharat": "भारत", "1u": "एक", "ek": "एक" },
  "pa": { "satsriakal": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "dhannvad": "ਧੰਨਵਾਦ", "1u": "ਇੱਕ", "ikk": "ਇੱਕ" },
  "ar": { "salam": "سلام", "marhaba": "مرحبا", "shukran": "شكرا", "1u": "واحد", "wahid": "واحد" },
  "ur": { "salam": "سلام", "adab": "آداب", "shukriya": "شکریہ", "1u": "ایک", "ek": "ایک" },
  "sa": { "namaste": "नमस्ते", "namah": "नमः", "dhanyavadah": "धन्यवादः", "1u": "एकम्", "ekam": "एकम्" },
  "ja": { "konnichiwa": "こんにちは", "arigatou": "ありがとう", "ohayou": "おはよう", "1u": "ひとつ", "ichi": "いち" },
  "ru": { "privet": "привет", "spasibo": "спасибо", "zdravstvuyte": "здравствуйте", "1u": "один", "odin": "один" },
  "es": { "hola": "hola", "gracias": "gracias", "manana": "mañana", "senor": "señor", "1u": "uno" },
  "fr": { "bonjour": "bonjour", "merci": "merci", "francais": "français", "coeur": "cœur", "1u": "un" },
  "de": { "hallo": "hallo", "danke": "danke", "fur": "für", "schon": "schön", "1u": "eins" },
  "ms": { "selamat": "selamat", "terimakasih": "terima kasih", "1u": "satu", "satu": "satu" },
  "zh": { "nihao": "你好", "ni": "你", "hao": "好", "wo": "我", "xiexie": "谢谢", "bukeqi": "不客气", "qing": "请", "zhongguo": "中国", "zaijian": "再见", "1u": "一", "yi": "一" },
  "th": { "sawatdee": "สวัสดี", "khobkhun": "ขอบคุณ", "1u": "หนึ่ง", "nueng": "หนึ่ง" },
  "am": { "selam": "ሰላም", "ameseginalehu": "አመሰግናለሁ", "sira": "ሥራ", "alem": "ዓለም", "1u": "አንድ", "and": "አንድ" },
  "ko": { "annyeong": "안녕", "annyeonghaseyo": "안녕하세요", "gamsahabnida": "감사합니다", "1u": "하나", "hana": "하나" }
};

function onHomepage() {
  var card = CardService.newCardBuilder()
    .setHeader(
      CardService.newCardHeader()
        .setTitle("Aaahhh Fonts Vibe — Sound of Font")
        .setSubtitle("5 Handcrafted 3D-Pressed Fonts · All 24 Languages")
    )
    .addSection(
      CardService.newCardSection()
        .addWidget(
          CardService.newSelectionInput()
            .setType(CardService.SelectionInputType.DROPDOWN)
            .setTitle("Target Sound Language (24 Languages)")
            .setFieldName("lang")
            .addItem("English (Default)", "en", true)
            .addItem("Tamil (தமிழ்)", "ta", false)
            .addItem("Sen Tamil (செந்தமிழ்)", "ta-sen", false)
            .addItem("Hindi (हिन्दी)", "hi", false)
            .addItem("Prathmic Hindi", "hi-prathmic", false)
            .addItem("Telugu (తెలుగు)", "te", false)
            .addItem("Malayalam (മലയാളം)", "ml", false)
            .addItem("Kannada (ಕನ್ನಡ)", "kn", false)
            .addItem("Bengali (বাংলা)", "bn", false)
            .addItem("Marathi (मराठी)", "mr", false)
            .addItem("Punjabi (ਪੰਜਾਬੀ)", "pa", false)
            .addItem("Sanskrit (संस्कृतम्)", "sa", false)
            .addItem("Arabic (العربية)", "ar", false)
            .addItem("Urdu (اردو)", "ur", false)
            .addItem("Japanese (日本語)", "ja", false)
            .addItem("Russian (Русский)", "ru", false)
            .addItem("Spanish (Español)", "es", false)
            .addItem("French (Français)", "fr", false)
            .addItem("German (Deutsch)", "de", false)
            .addItem("Bahasa Melayu (MY/SG)", "ms", false)
            .addItem("Chinese / SG-MY Mandarin (中文)", "zh", false)
            .addItem("Thai (ไทย)", "th", false)
            .addItem("Amharic / Ethiopic (አማርኛ)", "am", false)
            .addItem("Korean (한국어)", "ko", false)
        )
        .addWidget(
          CardService.newTextInput()
            .setFieldName("phoneticInput")
            .setTitle("Type in English Sound Keys (e.g., vanakkam, 1u, Rs 1u)")
            .setMultiline(true)
        )
        .addWidget(
          CardService.newTextButton()
            .setText("Insert Smart Sound-of-Font Text")
            .setOnClickAction(CardService.newAction().setFunctionName("insertPhoneticText"))
        )
    );
  return card.build();
}

function insertPhoneticText(e) {
  var raw = (e && e.formInput && e.formInput.phoneticInput) || "";
  var lang = (e && e.formInput && e.formInput.lang) || "en";
  var converted = convertSoundPreview(raw, lang);
  var targetHost = "Workspace";

  try {
    var doc = DocumentApp.getActiveDocument();
    if (doc) {
      targetHost = "Google Docs";
      var cursor = doc.getCursor();
      if (cursor) {
        cursor.insertText(converted);
      } else {
        doc.getBody().appendParagraph(converted);
      }
      return buildSuccessNotification_(targetHost);
    }
  } catch (_) {}

  try {
    var pres = SlidesApp.getActivePresentation();
    if (pres) {
      targetHost = "Google Slides";
      var sel = pres.getSelection();
      var tr = sel ? sel.getTextRange() : null;
      if (tr) {
        tr.insertText(tr.getEndIndex() || 0, converted);
      } else {
        var slide = pres.getSlides()[0] || pres.appendSlide();
        slide.insertTextBox(converted, 48, 48, 520, 96);
      }
      return buildSuccessNotification_(targetHost);
    }
  } catch (_) {}

  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    if (ss) {
      targetHost = "Google Sheets";
      var cell = ss.getActiveCell();
      if (cell) {
        var existing = String(cell.getValue() || "");
        cell.setValue(existing ? existing + " " + converted : converted);
      }
      return buildSuccessNotification_(targetHost);
    }
  } catch (_) {}

  return buildSuccessNotification_(targetHost);
}

function buildSuccessNotification_(host) {
  return CardService.newActionResponseBuilder()
    .setNotification(CardService.newNotification().setText("Inserted into " + host + " via Aaahhh Fonts Vibe!"))
    .build();
}

function convertSoundPreview(text, lang) {
  if (!text || lang === "en") return text || "";
  var dict = SOUND_LEXICON_24[lang] || {};
  // Protect space-separated or compact currency/number prefixes (`Rs 1u`, `Rs. 1u`, `$ 1u`, `₹ 1u`, `No. 1u`, `Rs1`, `$100`)
  var guarded = text.replace(/(?:(?:Rs\.?|INR|USD|EUR|GBP|RM|S\$|No\.?|#|[₹$€£¥₩฿₫৳])\s*\d[\d,.]*[A-Za-z]*)/gi, function(m) {
    return "\u0000" + m + "\u0000";
  });
  var parts = guarded.split("\u0000");
  for (var i = 0; i < parts.length; i += 2) {
    parts[i] = parts[i].replace(/\b([A-Za-z0-9]+)\b/g, function(tok) {
      if (/^\d+$/.test(tok)) return tok;
      var low = tok.toLowerCase();
      if (Object.prototype.hasOwnProperty.call(dict, low)) {
        return dict[low];
      }
      return tok;
    });
  }
  return parts.join("");
}
