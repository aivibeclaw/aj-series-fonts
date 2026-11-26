/**
 * Supabase Edge Function (Deno / Web Fetch API) — Aaahhh Fonts Vibe ("Sound of Font" v3.0.0)
 * 100% self-contained single-file Deno Edge Function (zero external relative parent imports).
 * Provides <1ms phonetic conversion, numeric/currency guardrails (`1` / `Rs1` / `Rs 1u` vs `1u`/`onnu`/`ondru`),
 * spell & grammar auto-correction, and Leave-Letter / Invoice inline completions across all 24 languages.
 */

/**
 * Sound of Font TypeScript SDK (ES2018+, no dependencies).
 * Mirrors sound_of_font.py and multilingual_lexicon.py; keep them in sync.
 */

// ---------------------------------------------------------------- data

export const LANGUAGES = {
  en: "English", ta: "Tamil", "ta-sen": "Sen Tamil", hi: "Hindi",
  "hi-prathmic": "Prathmic Hindi", te: "Telugu", ml: "Malayalam",
  kn: "Kannada", bn: "Bengali", mr: "Marathi", pa: "Punjabi",
  ar: "Arabic", ur: "Urdu", sa: "Sanskrit", ja: "Japanese",
  ru: "Russian", es: "Spanish", fr: "French", de: "German",
  ms: "Malay", zh: "Chinese", th: "Thai", am: "Amharic", ko: "Korean",
} as const;

export type Lang = keyof typeof LANGUAGES;
export type Category = "leave_letter" | "official_email" | "invoice" | "greeting" | "erp_note";
export const CATEGORIES: Category[] = ["leave_letter", "official_email", "invoice", "greeting", "erp_note"];

const LATIN_LANGUAGES = ["en", "es", "fr", "de", "ms"];
const UNSPACED_LANGUAGES = ["zh", "ja", "th"];

const TA_NUMBERS: [string, string[]][] = [
  ["ஒன்று", ["1u", "onnu", "ondru"]], ["இரண்டு", ["2u", "rendu", "irandu"]],
  ["மூன்று", ["3u", "moonu", "moondru"]], ["நான்கு", ["4u", "naalu", "naangu"]],
  ["ஐந்து", ["5u", "anju", "aindhu"]], ["ஆறு", ["6u", "aaru"]], ["ஏழு", ["7u", "ezhu"]],
  ["எட்டு", ["8u", "ettu"]], ["ஒன்பது", ["9u", "onbadhu"]], ["பத்து", ["10u", "pathu"]],
];
const TA_NUMBER_MAP = new Map<string, string>();
for (const [native, aliases] of TA_NUMBERS) for (const a of aliases) TA_NUMBER_MAP.set(a, native);
const numberSound = (lang: string, word: string): string | undefined =>
  lang === "ta" || lang === "ta-sen" ? TA_NUMBER_MAP.get(word.toLowerCase()) : undefined;

const WORDS: Record<Lang, string> = {
  en: "hello thank thanks you please leave letter invoice payment greetings regards receive request application permission accommodate necessary government weird separate definitely business schedule document approval approved attached sincerely respectfully company customer service delivery balance account manager important information",
  ta: "வணக்கம்|vanakkam,vanakam,vannakkam,wanakkam நன்றி|nandri,nanri,nandree ஆம்|aam இல்லை|illai தயவுசெய்து|thayavuseithu விடுப்பு|viduppu விண்ணப்பம்|vinnappam,vinappam பணிவுடன்|panivudan நீங்கள்|neengal,ningal நான்|naan இன்று|indru,innikku சிங்கம்|singam இந்தியா|india,indhiya அன்பு|anbu அம்மா|amma அப்பா|appa தமிழ்|tamil,thamizh சென்னை|chennai பள்ளி|palli அலுவலகம்|aluvalagam வாழ்த்துக்கள்|vazhthukkal",
  "ta-sen": "வணக்கம்|vanakkam,vanakam,vannakkam,wanakkam நன்றி|nandri,nanri,nandree ஆம்|aam இல்லை|illai விடுப்பு|viduppu விண்ணப்பம்|vinnappam,vinappam பணிவுடன்|panivudan நீங்கள்|neengal,ningal நான்|naan இன்று|indru சிங்கம்|singam இந்தியா|india,indhiya அன்பு|anbu அன்னை|annai தந்தை|thandhai தமிழ்|tamil,thamizh வாழ்த்துகள்|vazhthugal அலுவலகம்|aluvalagam செந்தமிழ்|senthamizh",
  hi: "नमस्ते|namaste,namasthe नमस्कार|namaskar धन्यवाद|dhanyavad,dhanyawad कृपया|kripya हाँ|haan नहीं|nahin,nahi मैं|main,mai हैं|hain है|hai हूँ|hoon,hun आप|aap भारत|bharat,india आज|aaj कल|kal छुट्टी|chutti,chhutti सविनय|saviney,savinay आवेदन|aavedan शुभकामनाएँ|shubhkamnayen",
  "hi-prathmic": "नमस्ते|namaste,namasthe नमस्कार|namaskar धन्यवाद|dhanyavad कृपया|kripya हाँ|haan नहीं|nahin,nahi मैं|main,mai हैं|hain है|hai आप|aap भारत|bharat,india घर|ghar पानी|paani आज|aaj छुट्टी|chutti",
  te: "నమస్కారం|namaskaram ధన్యవాదాలు|dhanyavadalu అవును|avunu కాదు|kaadu సెలవు|selavu నేను|nenu మీరు|meeru భారత్|bharat,india ఈరోజు|eeroju దయచేసి|dayachesi శుభాకాంక్షలు|subhakankshalu",
  ml: "നമസ്കാരം|namaskaram നന്ദി|nandi അതെ|athe ഇല്ല|illa അവധി|avadhi ഞാൻ|njan നിങ്ങൾ|ningal ഭാരതം|bharat,india ഇന്ന്|innu ദയവായി|dayavaayi ആശംസകൾ|aashamsakal",
  kn: "ನಮಸ್ಕಾರ|namaskara ಧನ್ಯವಾದಗಳು|dhanyavadagalu ಹೌದು|haudu ಇಲ್ಲ|illa ರಜೆ|raje ನಾನು|naanu ನೀವು|neevu ಭಾರತ|bharat,india ಇಂದು|indu ದಯವಿಟ್ಟು|dayavittu ಶುಭಾಶಯಗಳು|shubhaashayagalu",
  bn: "নমস্কার|nomoskar,namaskar,nomoshkar ধন্যবাদ|dhonnobad,dhanyabad হ্যাঁ|hyan না|na ছুটি|chuti আমি|ami আপনি|apni ভারত|bharat,india আজ|aaj বাংলা|bangla শুভেচ্ছা|shubhechha",
  mr: "नमस्कार|namaskar धन्यवाद|dhanyavad होय|hoy नाही|nahi रजा|raja मी|mi तुम्ही|tumhi भारत|bharat,india आज|aaj कृपया|kripaya शुभेच्छा|shubhechha",
  pa: "ਸਤਿ_ਸ੍ਰੀ_ਅਕਾਲ|satsriakal ਧੰਨਵਾਦ|dhanvaad,dhannvad ਹਾਂ|haan ਨਹੀਂ|nahin ਛੁੱਟੀ|chhutti ਮੈਂ|main ਤੁਸੀਂ|tusi ਭਾਰਤ|bharat,india ਅੱਜ|ajj ਕਿਰਪਾ|kirpa ਪੰਜਾਬੀ|punjabi",
  ar: "مرحبا|marhaba,marhaban شكرا|shukran نعم|naam لا|laa إجازة|ijaza السلام_عليكم|assalamualaikum أهلا|ahlan من_فضلك|minfadlik اليوم|alyawm طلب|talab",
  ur: "سلام|salam آداب|adab,aadab شکریہ|shukriya ہاں|haan نہیں|nahin چھٹی|chutti میں|main آپ|aap ہیں|hain پاکستان|pakistan بھائی|bhai خوش_آمدید|khushamdeed مہربانی|mehrbani",
  sa: "नमस्कारः|namaskarah,namaskar नमस्ते|namaste धन्यवादः|dhanyavadah आम्|aam न|na अवकाशः|avakashah अहम्|aham भवान्|bhavaan भारतम्|bharatam अद्य|adya कृपया|kripayaa स्वागतम्|svaagatam",
  ja: "こんにちは|konnichiwa,konnichiha ありがとう|arigatou,arigato はい|hai いいえ|iie 休暇|kyuuka 日本|nihon,nippon 日本語|nihongo 東京|toukyou,tokyo 大阪|oosaka,osaka お願い|onegai 私|watashi",
  ru: "привет|privet спасибо|spasibo да|da нет|net,nyet отпуск|otpusk пожалуйста|pozhalujsta здравствуйте|zdravstvujte сегодня|segodnya заявка|zayavka хорошо|khorosho",
  es: "hola gracias adiós|adios sí|si señor|senor señora|senora mañana|manana día|dia días|dias permiso factura número|numero atención|atencion también|tambien más|mas cómo|como está|esta",
  fr: "bonjour merci très|tres congé|conge madame monsieur été|ete bientôt|bientot français|francais déjà|deja détail|detail détails|details pièce|piece reçu|recu vérifié|verifie",
  de: "hallo danke für|fur Grüße|grusse,gruesse schön|schon,schoen Urlaub|urlaub über|uber können|konnen,koennen möchte|mochte,moechte größer|grosser,groesser Straße|strasse,strase Prüfung|prufung,pruefung",
  ms: "helo terima_kasih|terimakasih selamat sila cuti saya anda hari_ini|hariini permohonan bayaran",
  zh: "我|wo 你|ni 好|hao 你好|nihao 谢谢|xiexie 不客气|bukeqi 请|qing 中国|zhongguo 再见|zaijian 申请|shenqing 批准|pizhun 是|shi 不|bu 请假|qingjia 非常|feichang 很|hen 常|chang 帮助|bangzhu 感谢|ganxie 今天|jintian 明天|mingtian",
  th: "สวัสดี|sawatdee,sawasdee ขอบคุณ|khopkhun ใช่|chai ไม่|mai ลา|laa ฉัน|chan คุณ|khun วันนี้|wanni กรุณา|karuna ลาหยุด|layut",
  am: "ሰላም|selam,salam አመሰግናለሁ|ameseginalehu አዎ|awo አይ|ay ፈቃድ|fekad እባክዎ|ebakwo ሥራ|sira ዓለም|alem ጨረቃ|chereqa ጸሐይ|tsehay ነፃ|netsa",
  ko: "안녕하세요|annyeonghaseyo,annyeong 감사합니다|gamsahamnida 네|ne 아니요|aniyo 휴가|hyuga 한국|hanguk 한국어|hangugeo 오늘|oneul 부탁|butak 신청|sincheong",
};

// Each row follows CATEGORIES order.
const TEMPLATES: Record<Lang, [string, string, string, string, string]> = {
  en: [
    "Respected Sir/Madam, I am writing to request leave for two days due to a personal reason. Kindly grant me leave. Thank you.",
    "Dear Sir/Madam, I hope this email finds you well. Please find the details attached. Kind regards.",
    "Invoice for services rendered. Kindly process the payment before the due date. Thank you for your business.",
    "Warm greetings to you and your family. Wishing you joy and success.",
    "Stock has been received and verified. Please update the ledger.",
  ],
  ta: [
    "மதிப்பிற்குரிய|madhippirkuriya ஐயா,|aiya எனக்கு|enakku இரண்டு|irandu நாட்கள்|naatkal விடுப்பு|viduppu வழங்குமாறு|vazhangumaaru கேட்டுக்கொள்கிறேன்.|kettukkolgiren நன்றி.|nandri",
    "அன்புள்ள|anbulla ஐயா,|aiya விவரங்களை|vivarangalai இணைத்துள்ளேன்.|inaithullen நன்றி.|nandri",
    "சேவைக்கான|sevaikkaana விலைப்பட்டியல்.|vilaippattiyal தயவுசெய்து|thayavuseithu பணம்|panam செலுத்தவும்.|seluthavum",
    "உங்களுக்கும்|ungalukkum உங்கள்|ungal குடும்பத்தினருக்கும்|kudumbathinarukkum இனிய|iniya வாழ்த்துக்கள்.|vazhthukkal",
    "சரக்கு|sarakku பெறப்பட்டு|perappattu சரிபார்க்கப்பட்டது.|saripaarkkappattadhu",
  ],
  "ta-sen": [
    "மதிப்பிற்குரிய|madhippirkuriya ஐயா,|aiya அடியேனுக்கு|adiyenukku இரு|iru நாள்கள்|naalgal விடுப்பு|viduppu அளித்தருளுமாறு|alitharulumaaru பணிவுடன்|panivudan வேண்டுகிறேன்.|vendugiren நன்றி.|nandri",
    "பெருமதிப்பிற்குரியீர்,|perumadhippirkuriyeer விவரங்களை|vivarangalai இத்துடன்|ithudan இணைத்துள்ளேன்.|inaithullen நன்றி.|nandri",
    "ஆற்றிய|aatriya பணிக்கான|panikkaana விலைப்பட்டி.|vilaippatti தொகையைச்|thogaiyaich செலுத்த|selutha வேண்டுகிறோம்.|vendugirom",
    "தங்களுக்கும்|thangalukkum தங்கள்|thangal குடும்பத்தாருக்கும்|kudumbathaarukkum இனிய|iniya நல்வாழ்த்துகள்.|nalvazhthugal",
    "சரக்கு|sarakku பெறப்பெற்றுச்|perappetruch சரிபார்க்கப்பட்டது.|saripaarkkappattadhu",
  ],
  hi: [
    "सविनय|saviney निवेदन|nivedan है|hai कि|ki मुझे|mujhe दो|do दिन|din की|ki छुट्टी|chutti प्रदान|pradaan करें।|karen धन्यवाद।|dhanyavad",
    "आदरणीय|aadarniya महोदय,|mahoday विवरण|vivaran संलग्न|sanlagna है।|hai धन्यवाद।|dhanyavad",
    "सेवाओं|sevaon का|ka बिल।|bill कृपया|kripya भुगतान|bhugtaan करें।|karen",
    "आपको|aapko और|aur आपके|aapke परिवार|parivaar को|ko हार्दिक|haardik शुभकामनाएँ।|shubhkamnayen",
    "माल|maal प्राप्त|praapt और|aur सत्यापित|satyaapit हो|ho गया|gaya है।|hai",
  ],
  "hi-prathmic": [
    "श्रीमान|shriman जी,|ji मुझे|mujhe दो|do दिन|din की|ki छुट्टी|chutti दें।|den धन्यवाद।|dhanyavad",
    "प्रिय|priya महोदय,|mahoday जानकारी|jaankari साथ|saath में|mein है।|hai",
    "यह|yah आपका|aapka बिल|bill है।|hai कृपया|kripya पैसे|paise दें।|den",
    "आपको|aapko बहुत|bahut बधाई।|badhaai",
    "सामान|saamaan आ|aa गया|gaya है।|hai",
  ],
  te: [
    "గౌరవనీయులైన|gauravaneeyulaina అయ్యా,|ayya నాకు|naaku రెండు|rendu రోజులు|rojulu సెలవు|selavu మంజూరు|manjooru చేయగలరు.|cheyagalaru",
    "ప్రియమైన|priyamaina అయ్యా,|ayya వివరాలు|vivaraalu జతచేశాను.|jathachesaanu",
    "సేవల|sevala బిల్లు.|billu దయచేసి|dayachesi చెల్లించండి.|chellinchandi",
    "మీకు|meeku హృదయపూర్వక|hrudayapoorvaka శుభాకాంక్షలు.|subhakankshalu",
    "సరుకు|saruku అందింది.|andindi",
  ],
  ml: [
    "ബഹുമാനപ്പെട്ട|bahumaanappetta സർ,|sar എനിക്ക്|enikku രണ്ട്|randu ദിവസത്തെ|divasathe അവധി|avadhi അനുവദിക്കണം.|anuvadikkanam",
    "പ്രിയ|priya സർ,|sar വിശദാംശങ്ങൾ|vishadaamshangal ചേർക്കുന്നു.|cherkkunnu",
    "സേവനങ്ങളുടെ|sevanangalude ബിൽ.|bill ദയവായി|dayavaayi പണമടയ്ക്കുക.|panamadaykkuka",
    "നിങ്ങൾക്ക്|ningalkku ഹൃദയംനിറഞ്ഞ|hridayamniranja ആശംസകൾ.|aashamsakal",
    "ചരക്ക്|charakku ലഭിച്ചു.|labhichu",
  ],
  kn: [
    "ಮಾನ್ಯರೇ,|maanyare ನನಗೆ|nanage ಎರಡು|eradu ದಿನಗಳ|dinagala ರಜೆ|raje ಮಂಜೂರು|manjooru ಮಾಡಿ.|maadi",
    "ಆತ್ಮೀಯರೇ,|aatmeeyare ವಿವರಗಳನ್ನು|vivaragalannu ಲಗತ್ತಿಸಿದ್ದೇನೆ.|lagattisiddene",
    "ಸೇವೆಗಳ|sevegala ಬಿಲ್.|bill ದಯವಿಟ್ಟು|dayavittu ಪಾವತಿಸಿ.|paavatisi",
    "ನಿಮಗೆ|nimage ಹಾರ್ದಿಕ|haardika ಶುಭಾಶಯಗಳು.|shubhaashayagalu",
    "ಸರಕು|saraku ಸ್ವೀಕರಿಸಲಾಗಿದೆ.|sveekarisalaagide",
  ],
  bn: [
    "মাননীয়|mananiyo মহাশয়,|mohashoy আমাকে|amake দুই|dui দিনের|diner ছুটি|chuti মঞ্জুর|monjur করুন।|korun",
    "প্রিয়|priyo মহাশয়,|mohashoy বিবরণ|biboron সংযুক্ত|songjukto করা|kora হলো।|holo",
    "পরিষেবার|porishebar বিল।|bill অনুগ্রহ|onugroho করে|kore পরিশোধ|porishodh করুন।|korun",
    "আপনাকে|apnake আন্তরিক|antorik শুভেচ্ছা।|shubhechha",
    "মাল|maal গ্রহণ|grohon করা|kora হয়েছে।|hoyeche",
  ],
  mr: [
    "आदरणीय|aadarniya महोदय,|mahoday मला|mala दोन|don दिवसांची|divasanchi रजा|raja मंजूर|manjoor करावी.|karaavi",
    "प्रिय|priya महोदय,|mahoday तपशील|tapshil सोबत|sobat जोडला|jodla आहे.|aahe",
    "सेवांचे|sevanche बिल.|bill कृपया|kripya पैसे|paise भरा.|bhara",
    "आपणास|aapnaas हार्दिक|haardik शुभेच्छा.|shubhechha",
    "माल|maal मिळाला|milala आहे.|aahe",
  ],
  pa: [
    "ਸਤਿਕਾਰਯੋਗ|satkaaryog ਸ੍ਰੀਮਾਨ_ਜੀ,|shrimaanji ਮੈਨੂੰ|mainu ਦੋ|do ਦਿਨ|din ਦੀ|di ਛੁੱਟੀ|chhutti ਦਿੱਤੀ|ditti ਜਾਵੇ।|jaave",
    "ਪਿਆਰੇ|pyaare ਸ੍ਰੀਮਾਨ,|shrimaan ਵੇਰਵੇ|verve ਨੱਥੀ|natthi ਹਨ।|han",
    "ਸੇਵਾਵਾਂ|sevaavaan ਦਾ|da ਬਿੱਲ।|bill ਕਿਰਪਾ|kirpa ਕਰਕੇ|karke ਭੁਗਤਾਨ|bhugtaan ਕਰੋ।|karo",
    "ਤੁਹਾਨੂੰ|tuhaanu ਬਹੁਤ|bahut ਵਧਾਈਆਂ।|vadhaaiyaan",
    "ਸਮਾਨ|samaan ਮਿਲ|mil ਗਿਆ|gia ਹੈ।|hai",
  ],
  ar: [
    "السيد|alsayyid المحترم،|almuhtaram أرجو|arju منحي|manhi إجازة|ijaza لمدة|limuddat يومين.|yawmayn",
    "عزيزي|azizi السيد،|alsayyid تجدون|tajidun التفاصيل|altafasil مرفقة.|murfaqa",
    "فاتورة|fatura الخدمات.|alkhadamat يرجى|yurja سداد|sadad المبلغ.|almablagh",
    "أطيب|atyab التحيات|altahiyyat لكم.|lakum",
    "تم|tamma استلام|istilam البضاعة.|albidaa",
  ],
  ur: [
    "جناب|janab عالی،|aali مجھے|mujhe دو|do دن|din کی|ki چھٹی|chutti عنایت|inayat فرمائیں۔|farmaayen",
    "محترم|mohtaram جناب،|janab تفصیلات|tafseelat منسلک|munsalik ہیں۔|hain",
    "خدمات|khidmaat کا|ka بل۔|bill براہ|barah کرم|karam ادائیگی|adaaigi کریں۔|karen",
    "آپ|aap کو|ko دلی|dili مبارکباد۔|mubarakbad",
    "سامان|saamaan موصول|mausool ہو|ho گیا|gaya ہے۔|hai",
  ],
  sa: [
    "मान्यवर,|maanyavara मह्यं|mahyam दिनद्वयस्य|dinadvayasya अवकाशं|avakasham ददातु|dadaatu भवान्।|bhavaan",
    "प्रिय|priya महोदय,|mahodaya विवरणं|vivaranam संलग्नम्|samlagnam अस्ति।|asti",
    "सेवायाः|sevaayaah देयकम्।|deyakam कृपया|kripayaa धनं|dhanam ददातु।|dadaatu",
    "भवते|bhavate शुभकामनाः।|shubhakaamanaah",
    "वस्तूनि|vastooni प्राप्तानि।|praaptaani",
  ],
  ja: [
    "拝啓、|haikei 私用の|shiyouno ため|tame 二日間の|futsukakanno 休暇を|kyuukawo お願い|onegai いたします。|itashimasu",
    "お世話に|osewani なっております。|natteorimasu 詳細を|shousaiwo 添付します。|tenpushimasu",
    "ご請求書です。|goseikyuushodesu お支払いを|oshiharaiwo お願いします。|onegaishimasu",
    "ご家族の|gokazokuno 皆様に|minasamani ご多幸を|gotakouwo お祈りします。|oinorishimasu",
    "在庫を|zaikowo 受領しました。|juryoushimashita",
  ],
  ru: [
    "Уважаемый|uvazhaemyj руководитель,|rukovoditel прошу|proshu предоставить|predostavit мне|mne отпуск|otpusk на|na два|dva дня.|dnya",
    "Уважаемый|uvazhaemyj коллега,|kollega подробности|podrobnosti во|vo вложении.|vlozhenii",
    "Счёт|schet за|za услуги.|uslugi Просим|prosim произвести|proizvesti оплату.|oplatu",
    "Сердечно|serdechno поздравляем|pozdravlyaem вас.|vas",
    "Товар|tovar получен|poluchen и|i проверен.|proveren",
  ],
  es: [
    "Estimado señor, solicito un permiso de dos días por motivos personales. Muchas gracias.",
    "Estimado señor, adjunto encontrará los detalles. Saludos cordiales.",
    "Factura por servicios prestados. Por favor realice el pago.",
    "Un cordial saludo para usted y su familia.",
    "Mercancía recibida y verificada.",
  ],
  fr: [
    "Monsieur, je sollicite un congé de deux jours pour raison personnelle. Cordialement.",
    "Monsieur, veuillez trouver les détails en pièce jointe. Cordialement.",
    "Facture pour les services rendus. Merci de procéder au paiement.",
    "Meilleurs vœux à vous et à votre famille.",
    "Marchandise reçue et vérifiée.",
  ],
  de: [
    "Sehr geehrte Damen und Herren, ich bitte um zwei Tage Urlaub aus persönlichen Gründen. Vielen Dank.",
    "Sehr geehrte Damen und Herren, die Details finden Sie im Anhang. Mit freundlichen Grüßen.",
    "Rechnung für erbrachte Leistungen. Bitte überweisen Sie den Betrag.",
    "Herzliche Grüße an Sie und Ihre Familie.",
    "Ware erhalten und geprüft.",
  ],
  ms: [
    "Tuan yang dihormati, saya memohon cuti selama dua hari atas urusan peribadi. Terima kasih.",
    "Tuan yang dihormati, butiran dilampirkan bersama. Sekian, terima kasih.",
    "Invois untuk perkhidmatan. Sila jelaskan bayaran.",
    "Salam sejahtera buat anda sekeluarga.",
    "Stok telah diterima dan disahkan.",
  ],
  zh: [
    "尊敬的|zunjingde 领导，|lingdao 因个人原因|yingerenyuanyin 我想|woxiang 请假|qingjia 两天。|liangtian 谢谢。|xiexie",
    "您好，|ninhao 详情|xiangqing 请见|qingjian 附件。|fujian",
    "服务|fuwu 发票。|fapiao 请|qing 按时|anshi 付款。|fukuan",
    "祝您|zhunin 和家人|hejiaren 幸福安康。|xingfuankang",
    "货物|huowu 已收到|yishoudao 并核对。|binghedui",
  ],
  th: [
    "เรียน|rian หัวหน้า|huana ข้าพเจ้า|khaphachao ขอ|kho ลาหยุด|layut สองวัน|songwan",
    "เรียน|rian ท่าน|than รายละเอียด|railaiat ตามเอกสารแนบ|tamekkasannaep",
    "ใบแจ้งหนี้|baichaengni กรุณา|karuna ชำระเงิน|chamrangoen",
    "ขอให้|khohai ท่าน|than มีความสุข|mikhwamsuk",
    "ได้รับ|dairap สินค้า|sinkha แล้ว|laeo",
  ],
  am: [
    "ውድ|wid ኃላፊ፣|halafi ለሁለት|lehulet ቀናት|qenat ፈቃድ|fekad እንዲሰጠኝ|endiseten እጠይቃለሁ።|eteyqalehu",
    "ውድ|wid ጌታዬ፣|getaye ዝርዝሩ|zirziru ተያይዟል።|teyayzwal",
    "የአገልግሎት|yeageliglot ደረሰኝ።|deresegn እባክዎ|ebakwo ይክፈሉ።|yikfelu",
    "መልካም|melkam ምኞት|mignot ለእርስዎ።|lerswo",
    "እቃው|eqaw ደርሷል።|derswal",
  ],
  ko: [
    "존경하는|jongyeonghaneun 팀장님,|timjangnim 개인|gaein 사정으로|sajeongeuro 이틀|iteul 휴가를|hyugareul 신청합니다.|sincheonghamnida",
    "안녕하세요,|annyeonghaseyo 자세한|jasehan 내용을|naeyongeul 첨부합니다.|cheombuhamnida",
    "서비스|seobiseu 청구서입니다.|cheongguseoimnida 결제|gyeolje 부탁드립니다.|butakdeurimnida",
    "가정에|gajeonge 행복이|haengbogi 가득하길|gadeukhagil 바랍니다.|baramnida",
    "재고가|jaegoga 입고되었습니다.|ipgodoeeotseumnida",
  ],
};

const HEADING_KEYWORDS: [Category, string[]][] = [
  ["invoice", ["invoice", "bill", "payment", "receipt", "fintech", "விலைப்பட்டி", "बिल", "चालान", "فاتورة", "請求", "счёт", "factura", "facture", "rechnung", "invois", "发票", "청구"]],
  ["erp_note", ["erp", "stock", "inventory", "purchase order", "சரக்கு", "भंडार"]],
  ["official_email", ["email", "e-mail", "mail", "மின்னஞ்சல்", "ईमेल"]],
  ["greeting", ["greeting", "greetings", "wishes", "வாழ்த்து", "शुभकामना", "बधाई"]],
  ["leave_letter", ["leave", "application", "permission", "request", "விடுப்பு", "விண்ணப்பம்", "छुट्टी", "अवकाश", "आवेदन", "సెలవు", "അവധി", "ರಜೆ", "ছুটি", "रजा", "ਛੁੱਟੀ", "إجازة", "چھٹی", "休暇", "отпуск", "permiso", "vacaciones", "congé", "urlaub", "cuti", "请假", "申请", "ใบลา", "ลาหยุด", "ፈቃድ", "휴가"]],
];

const EN_CORRECTIONS = new Map<string, string>(Object.entries({
  i: "I", im: "I'm", recieve: "receive", recieved: "received", teh: "the",
  adress: "address", seperate: "separate", definately: "definitely", definitly: "definitely",
  accomodate: "accommodate", acommodate: "accommodate",
  neccessary: "necessary", necesary: "necessary",
  goverment: "government", governmant: "government",
  wierd: "weird", occurence: "occurrence", embarass: "embarrass",
  priviledge: "privilege", calender: "calendar", maintainance: "maintenance",
  buisness: "business", enviroment: "environment",
  occured: "occurred", untill: "until", becuase: "because", thier: "their",
  freind: "friend", beleive: "believe", acheive: "achieve",
  tommorow: "tomorrow", dont: "don't", doesnt: "doesn't", wont: "won't", cant: "can't",
  leav: "leave", requst: "request", pls: "please",
}));

const EN_COMMON_WORDS = new Set(
  ("a i an the to of in on is am are my me we be as at by do he it no or so up us if " +
    "for and but not you can may was has had our all any get one two day per her his " +
    "its who how why now yes see let new out off own say she too use").split(" "),
);

// ---------------------------------------------------------------- text helpers

const LEAD_PUNCT = "([{\"'“‘¿¡«<";
const TRAIL_PUNCT = ".,;:!?)]}\"'”’…।॥»>。、，！？؟،؛۔።፣";
const SENTENCE_END = ".!?。！？।؟۔።";
const URL_OR_ID = /^(?:[a-z][a-z0-9+.\-]*:\/\/\S+|www\.\S+|[^\s@]+@[^\s@]+\.[^\s@]+|[@#]\S+|[\p{L}\p{N}_\-]+(?:\.[\p{L}\p{N}_\-]+)*\.(?:com|in|org|net|io|ai|co|dev|app|cloud)(?:\/\S*)?)$/iu;
const CURRENCY = /^(?:rs\.?|inr|usd|eur|gbp|aed|sar|sgd|myr|rm|s\$|jpy|krw|bdt|₹|\$|€|£|¥|₩|৳|௹|฿|⃁|⃃)\s*\d[\d,]*(?:\.\d+)?(?:\/-)?$/i;
const CURRENCY_WORDS = new Set([
  "rs", "rs.", "inr", "usd", "eur", "gbp", "aed", "sar", "sgd", "myr", "rm",
  "s$", "jpy", "krw", "bdt", "no", "no.", "#", "₹", "$", "€", "£", "¥", "₩", "৳", "௹", "฿", "⃁", "⃃",
]);
const LATIN_WORD = /^[A-Za-z]+(?:'[A-Za-z]+)?$/;
const ABBREVIATIONS = new Set(["rs", "mr", "mrs", "ms", "dr", "no", "etc", "e.g", "i.e", "st"]);

export function splitPunct(token: string): [string, string, string] {
  let start = 0;
  while (start < token.length && LEAD_PUNCT.includes(token[start])) start++;
  let end = token.length;
  while (end > start && TRAIL_PUNCT.includes(token[end - 1])) end--;
  return [token.slice(0, start), token.slice(start, end), token.slice(end)];
}

export function isProtected(token: string): boolean {
  if (URL_OR_ID.test(token) || CURRENCY.test(token) || /\p{Nd}/u.test(token)) return true;
  return token.length > 1 && /^[A-Z]+$/.test(token);
}

export function soundSkeleton(word: string): string {
  let s = word.toLowerCase();
  const rules: [string, string][] = [["zh", "l"], ["sh", "s"], ["th", "t"], ["dh", "d"], ["bh", "b"],
    ["ph", "p"], ["gh", "g"], ["kh", "k"], ["ch", "c"], ["jh", "j"], ["ee", "i"], ["oo", "u"],
    ["w", "v"], ["ck", "k"], ["q", "k"]];
  for (const [from, to] of rules) s = s.split(from).join(to);
  return s.replace(/(.)\1+/g, "$1");
}

const VOWELS = "aeiou";
const SIMILAR = new Set(["td", "kg", "pb", "cs", "cj", "sz", "vb", "fp", "nm", "iy", "uv", "lr"]);

export function acousticDistance(a: string, b: string): number {
  const indel = (c: string) => (VOWELS.includes(c) || c === "h" ? 0.6 : 1);
  let prev = [0];
  for (const c of b) prev.push(prev[prev.length - 1] + indel(c));
  for (const x of a) {
    const cur = [prev[0] + indel(x)];
    for (let j = 1; j <= b.length; j++) {
      const y = b[j - 1];
      const sub = x === y ? 0 : SIMILAR.has(x + y) || SIMILAR.has(y + x) ? 0.35
        : VOWELS.includes(x) && VOWELS.includes(y) ? 0.6 : 1;
      cur.push(Math.min(prev[j - 1] + sub, prev[j] + indel(x), cur[j - 1] + indel(y)));
    }
    prev = cur;
  }
  return prev[prev.length - 1];
}

// ---------------------------------------------------------------- transliteration

type Table = Map<string, string>;
const table = (keys: string, values: string): Table => {
  const v = values.split(" ");
  return new Map(keys.split(" ").map((k, i): [string, string] => [k, v[i]]));
};

function longest(t: { has(key: string): boolean }, s: string, i: number): string | null {
  for (let n = 4; n > 0; n--) {
    const chunk = s.slice(i, i + n);
    if (chunk.length === n && t.has(chunk)) return chunk;
  }
  return null;
}

const DEVA_KEYS = "k kh g gh ch chh j jh t th d dh n p ph f b bh m y r l v w s sh h c q z";
const DEVA_C = table(DEVA_KEYS, "क ख ग घ च छ ज झ त थ द ध न प फ फ ब भ म य र ल व व स श ह क क ज");
const TAMIL_C = table("ngk ngg njch njc ndr nth ndh ng nj k kh g gh c ch j t th d dh n p ph f b bh m y r l v w s sh h zh q z",
  "ங்க ங்க ஞ்ச ஞ்ச ன்ற ந்த ந்த ங்க ஞ்ச க க க க ச ச ஜ ட த ட த ந ப ப ப ப ப ம ய ர ல வ வ ச ஷ ஹ ழ க ஜ");
const VOWEL_KEYS = "a aa i ee ii u oo uu e ae ai o oa au".split(" ");
const vowelTable = (values: string[]): Table =>
  new Map(VOWEL_KEYS.map((k, i): [string, string] => [k, values[i]]));
const DEVA_V = "अ आ इ ई ई उ ऊ ऊ ए ए ऐ ओ ओ औ".split(" ");
const DEVA_M = ["", "ा", "ि", "ी", "ी", "ु", "ू", "ू", "े", "े", "ै", "ो", "ो", "ौ"];
const TAMIL_V = "அ ஆ இ ஈ ஈ உ ஊ ஊ எ ஏ ஐ ஒ ஓ ஔ".split(" ");
const TAMIL_M = ["", "ா", "ி", "ீ", "ீ", "ு", "ூ", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"];
const BLOCK_OFFSET: Record<string, number> = { bn: 0x80, pa: 0x100, te: 0x300, kn: 0x380, ml: 0x400 };
const DRAVIDIAN = ["ta", "ta-sen", "te", "ml", "kn"];

function brahmic(word: string, lang: string): string {
  const tamil = lang === "ta" || lang === "ta-sen";
  const cons = tamil ? TAMIL_C : DEVA_C;
  const vow = vowelTable(tamil ? TAMIL_V : DEVA_V);
  const mat = vowelTable(tamil ? TAMIL_M : DEVA_M);
  const virama = tamil ? "்" : "्";
  if (lang === "te" || lang === "ml" || lang === "kn") {
    vow.set("e", "ऎ").set("o", "ऒ");
    mat.set("e", "ॆ").set("o", "ॊ");
  }
  let out = "";
  let i = 0;
  while (i < word.length) {
    const c = longest(cons, word, i);
    if (c) {
      i += c.length;
      const glyph = tamil && c === "n" && i > 1 ? "ன" : cons.get(c)!;
      const v = longest(vow, word, i);
      if (v) {
        out += glyph + mat.get(v);
        i += v.length;
      } else out += i < word.length || (DRAVIDIAN.includes(lang) && glyph.length === 1) ? glyph + virama : glyph;
      continue;
    }
    const v = longest(vow, word, i);
    out += v ? vow.get(v) : word[i];
    i += v ? v.length : 1;
  }
  if (lang === "bn") out = out.split("व").join("ब");
  if (lang === "pa") out = out.split("ष").join("श");
  const offset = BLOCK_OFFSET[lang];
  return offset ? out.replace(/[ऀ-ॿ]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) + offset)) : out;
}

const CYRILLIC = table("shch zh kh ts ch sh yu ya yo a b v g d e z i j k l m n o p r s t u f h y c w x q",
  "щ ж х ц ч ш ю я ё а б в г д е з и й к л м н о п р с т у ф х ы к в кс к");
const KANA: Table = table("a i u e o", "あ い う え お");
Object.entries({ k: "かきくけこ", s: "さしすせそ", t: "たちつてと", n: "なにぬねの", h: "はひふへほ",
  m: "まみむめも", r: "らりるれろ", g: "がぎぐげご", z: "ざじずぜぞ", d: "だぢづでど",
  b: "ばびぶべぼ", p: "ぱぴぷぺぽ" }).forEach(([c, row]) => [..."aiueo"].forEach((v, i) => KANA.set(c + v, row[i])));
Object.entries({ ya: "や", yu: "ゆ", yo: "よ", wa: "わ", wo: "を", n: "ん", shi: "し", chi: "ち",
  tsu: "つ", fu: "ふ", ji: "じ" }).forEach(([k, v]) => KANA.set(k, v));
const ARABIC = table("sh kh th dh gh aa ee oo b t j h d r z s f q k l m n w y p g v c",
  "ش خ ث ذ غ ا ي و ب ت ج ه د ر ز س ف ق ك ل م ن و ي ب ج ف ك");
const URDU = table("sh kh ch gh aa ee oo b p t j h d r z s f q k g l m n w v y c",
  "ش کھ چ غ ا ی و ب پ ت ج ہ د ر ز س ف ق ک گ ل م ن و و ی ک");
const THAI_C = table("kh ch th ph ng k j d t n b p f m y r l w s h g",
  "ค ช ท พ ง ก จ ด ต น บ ป ฟ ม ย ร ล ว ส ห ก");
const THAI_V = new Map<string, [string, string]>([["a", ["", "า"]], ["i", ["", "ิ"]], ["u", ["", "ุ"]], ["e", ["เ", ""]], ["o", ["โ", ""]]]);
const ETHIOPIC = new Map<string, number>(Object.entries({ hh: 0x1210, chh: 0x1328, kh: 0x12b8, zh: 0x12e0,
  ts: 0x1338, tz: 0x1340, h: 0x1200, l: 0x1208, m: 0x1218, r: 0x1228,
  s: 0x1230, sh: 0x1238, q: 0x1240, b: 0x1260, v: 0x1268, t: 0x1270, ch: 0x1278, n: 0x1290, k: 0x12a8,
  w: 0x12c8, z: 0x12d8, y: 0x12e8, d: 0x12f0, j: 0x1300, g: 0x1308, f: 0x1348, p: 0x1350 }));
const ETHIOPIC_ORDER = new Map<string, number>([["e", 0], ["u", 1], ["i", 2], ["a", 3], ["ie", 4], ["o", 6]]);
const ETHIOPIC_ALONE = table("a u i e o", "አ ኡ ኢ እ ኦ");
const HANGUL_L = new Map<string, number>(Object.entries({ g: 0, kk: 1, n: 2, d: 3, tt: 4, r: 5, l: 5,
  m: 6, b: 7, pp: 8, s: 9, ss: 10, j: 12, jj: 13, ch: 14, k: 15, t: 16, p: 17, h: 18 }));
const HANGUL_V = new Map<string, number>(
  "a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i".split(" ").map((v, i): [string, number] => [v, i]));
const HANGUL_T = new Map<string, number>(Object.entries({ g: 1, n: 4, d: 7, l: 8, r: 8, m: 16, b: 17,
  s: 19, ng: 21, j: 22, ch: 23, k: 24, t: 25, p: 26, h: 27 }));

function greedy(word: string, t: Table): string {
  let out = "";
  for (let i = 0; i < word.length;) {
    const key = longest(t, word, i);
    out += key ? t.get(key) : word[i];
    i += key ? key.length : 1;
  }
  return out;
}

function arabicScript(word: string, t: Table): string {
  let out = "";
  for (let i = 0; i < word.length;) {
    const key = longest(t, word, i);
    if (key) {
      out += t.get(key);
      i += key.length;
    } else {
      if (i === 0 || (i === word.length - 1 && word[i] === "a")) out += "ا";
      i++;
    }
  }
  return out;
}

function japanese(word: string): string {
  let out = "";
  for (let i = 0; i < word.length;) {
    if (word[i] === word[i + 1] && !"aiueon".includes(word[i])) {
      out += "っ";
      i++;
      continue;
    }
    const key = longest(KANA, word, i);
    out += key ? KANA.get(key) : word[i];
    i += key ? key.length : 1;
  }
  return out;
}

function thai(word: string): string {
  let out = "";
  let i = 0;
  while (i < word.length) {
    const c = longest(THAI_C, word, i);
    const glyph = c ? THAI_C.get(c)! : "อ";
    i += c ? c.length : 0;
    const vowel = THAI_V.get(word[i]);
    if (vowel) {
      out += vowel[0] + glyph + vowel[1];
      i++;
    } else if (c) out += glyph;
    else out += word[i++];
  }
  return out;
}

function amharic(word: string): string {
  let out = "";
  for (let i = 0; i < word.length;) {
    const c = longest(ETHIOPIC, word, i);
    if (c) {
      i += c.length;
      const v = longest(ETHIOPIC_ORDER, word, i);
      out += String.fromCharCode(ETHIOPIC.get(c)! + (v ? ETHIOPIC_ORDER.get(v)! : 5));
      i += v ? v.length : 0;
    } else {
      out += ETHIOPIC_ALONE.get(word[i]) ?? word[i];
      i++;
    }
  }
  return out;
}

function hangul(word: string): string {
  let out = "";
  for (let i = 0; i < word.length;) {
    const onset = longest(HANGUL_L, word, i);
    let j = i + (onset ? onset.length : 0);
    const vowel = longest(HANGUL_V, word, j);
    if (!onset && !vowel) {
      out += word[i++];
      continue;
    }
    j += vowel ? vowel.length : 0;
    let coda = vowel ? longest(HANGUL_T, word, j) : null;
    if (coda && longest(HANGUL_V, word, j + coda.length)) coda = null;
    j += coda ? coda.length : 0;
    const lead = onset ? HANGUL_L.get(onset)! : 11;
    const mid = vowel ? HANGUL_V.get(vowel)! : 18;
    out += String.fromCharCode(0xac00 + lead * 588 + mid * 28 + (coda ? HANGUL_T.get(coda)! : 0));
    i = j;
  }
  return out;
}

export function transliterate(word: string, lang: string): string {
  const w = word.toLowerCase();
  if (["ta", "ta-sen", "hi", "hi-prathmic", "mr", "sa", "te", "ml", "kn", "bn", "pa"].includes(lang)) return brahmic(w, lang);
  if (lang === "ru") return greedy(w, CYRILLIC);
  if (lang === "ja") return japanese(w);
  if (lang === "ar" || lang === "ur") return arabicScript(w, lang === "ur" ? URDU : ARABIC);
  if (lang === "th") return thai(w);
  if (lang === "am") return amharic(w);
  if (lang === "ko") return hangul(w);
  return word;
}

// ---------------------------------------------------------------- engine

export interface InlineSuggestion {
  replacementWord: string;
  inlineGhostCompletion: string;
  nextWords: string[];
  fullClauseSuggestion: string;
  category: Category | null;
}

export interface CommitResult {
  committedWord: string;
  text: string;
  replaced: boolean;
  inlineGhostCompletion: string;
  nextWords: string[];
  fullClauseSuggestion: string;
}

const isLang = (value: unknown): value is Lang =>
  typeof value === "string" && Object.prototype.hasOwnProperty.call(LANGUAGES, value);

export function detectDefaultLanguage(systemLocale?: string): Lang {
  const g = globalThis as any;
  const locale: string | undefined = systemLocale ?? g.navigator?.languages?.[0] ?? g.navigator?.language
    ?? g.process?.env?.LC_ALL ?? g.process?.env?.LANG;
  if (!locale) return "en";
  const tag = locale.split(".")[0].split("@")[0].replace(/_/g, "-").toLowerCase();
  if (isLang(tag)) return tag;
  let base = tag.split("-")[0];
  if (base === "id" || base === "in") base = "ms";
  return isLang(base) ? base : "en";
}

type Pair = [native: string, roman: string];
interface Index {
  exact: Map<string, string>;
  skeletons: Map<string, string>;
  buckets: Map<string, [string, string][]>;
}

const normWord = (word: string) => splitPunct(word)[1].toLowerCase();
const stripMarks = (word: string) => word.normalize("NFD").replace(/\p{M}/gu, "");
const words_ = (text: string) => text.split(/\s+/).filter(Boolean);
const capitalise = (word: string) => word.charAt(0).toUpperCase() + word.slice(1);
const startsUpper = (word: string) => word.charAt(0) !== word.charAt(0).toLowerCase();

export class SoundOfFontEngine {
  language: Lang;
  private user = new Map<string, Map<string, string>>();
  private indexCache = new Map<string, Index>();
  private wordsExactCache = new Map<string, Set<string>>();
  private templateCache = new Map<string, Pair[]>();
  private convertCache = new Map<string, string>();
  private osWords = new Set<string>();
  private osSorted: string[] = [];

  constructor(options: { language?: Lang; systemLocale?: string } = {}) {
    this.language = isLang(options.language) ? options.language : detectDefaultLanguage(options.systemLocale);
    const g = globalThis as any;
    if (g.process?.versions?.node && typeof g.require === "function") {
      try {
        const fs = g.require("fs");
        if (fs.existsSync("/usr/share/dict/words")) {
          void this.mergeOsDictionary(() => fs.promises.readFile("/usr/share/dict/words", "utf8"));
        }
      } catch {
        // Browser or sandboxed runtime without /usr/share/dict/words
      }
    }
  }

  private lang(lang?: string): Lang {
    return isLang(lang) ? lang : this.language;
  }

  /**
   * Merge an OS/app word list. Browsers cannot read /usr/share/dict/words:
   * pass its text (Node/Electron: fs.promises.readFile) or an async loader.
   */
  async mergeOsDictionary(source: string | Iterable<string> | (() => Promise<string>)): Promise<number> {
    await Promise.resolve();
    const raw = typeof source === "function" ? await source() : source;
    const list = typeof raw === "string" ? raw.split(/\r?\n/) : raw;
    for (const word of list) if (word.trim()) this.osWords.add(word.trim().toLowerCase());
    this.osSorted = Array.from(this.osWords).sort();
    return this.osWords.size;
  }

  addUserWords(words: string[] | Record<string, string>, lang: Lang = "en"): void {
    const pairs: [string, string][] = Array.isArray(words) ? words.map((w) => [w, w]) : Object.entries(words);
    const bucket = this.user.get(lang) ?? new Map<string, string>();
    for (const [roman, native] of pairs) if (roman && native) bucket.set(roman.toLowerCase(), native);
    this.user.set(lang, bucket);
    this.convertCache.clear();
  }

  isKnownWord(word: string, lang: Lang = "en"): boolean {
    const low = word.toLowerCase();
    if (this.user.get(lang)?.has(low)) return true;
    if (lang === "en" && this.osWords.has(low)) return true;
    return this.index(lang).exact.has(low);
  }

  private template(category: Category, lang: Lang): Pair[] {
    const key = `${category}/${lang}`;
    let pairs = this.templateCache.get(key);
    if (!pairs) {
      pairs = words_(TEMPLATES[lang][CATEGORIES.indexOf(category)]).map((part): Pair => {
        const [raw, roman] = part.split("|");
        const native = raw.replace(/_/g, " ");
        return [native, roman || stripMarks(normWord(native))];
      });
      this.templateCache.set(key, pairs);
    }
    return pairs;
  }

  private index(lang: Lang): Index {
    let index = this.indexCache.get(lang);
    if (index) return index;
    const built: Index = { exact: new Map(), skeletons: new Map(), buckets: new Map() };
    const add = (roman: string, native: string) => {
      if (!built.exact.has(roman)) built.exact.set(roman, native);
      const key = soundSkeleton(roman);
      if (key && !built.skeletons.has(key)) {
        built.skeletons.set(key, native);
        const bucket = built.buckets.get(key[0]) ?? [];
        bucket.push([key, native]);
        built.buckets.set(key[0], bucket);
      }
    };
    for (const entry of words_(WORDS[lang])) {
      const [raw, aliases] = entry.split("|");
      const native = raw.replace(/_/g, " ");
      for (const roman of aliases ? aliases.split(",") : [native.toLowerCase()]) add(roman, native);
    }
    for (const category of CATEGORIES) {
      for (const [native, roman] of this.template(category, lang)) {
        if ((!LATIN_LANGUAGES.includes(lang) || roman.length >= 4) && LATIN_WORD.test(roman)) {
          add(roman.toLowerCase(), splitPunct(native)[1]);
        }
      }
    }
    index = built;
    this.indexCache.set(lang, index);
    return index;
  }

  private matchSound(core: string, lang: Lang): string {
    const low = core.toLowerCase();
    const own = this.user.get(lang)?.get(low);
    if (own) return own;
    if (lang === "en") {
      const fixed = EN_CORRECTIONS.get(low);
      return !fixed ? core : startsUpper(core) ? capitalise(fixed) : fixed;
    }
    const { exact, skeletons, buckets } = this.index(lang);
    if (LATIN_LANGUAGES.includes(lang)) {
      const native = exact.get(low);
      return !native ? core : startsUpper(core) ? capitalise(native) : native;
    }
    const direct = exact.get(low);
    if (direct) return direct;
    const key = soundSkeleton(low);
    if (key.length >= 3 && skeletons.has(key)) return skeletons.get(key)!;
    if (key.length >= 5) {
      let best = "";
      let bestScore = (key.length <= 6 ? 0.7 : 1.2) + 1e-9;
      for (const [candidate, native] of buckets.get(key[0]) ?? []) {
        if (Math.abs(candidate.length - key.length) > 2) continue;
        const score = acousticDistance(key, candidate);
        if (score < bestScore) {
          best = native;
          bestScore = score;
        }
      }
      if (best) return best;
    }
    return transliterate(low, lang);
  }

  convertToken(token: string, lang?: Lang): string {
    const l = this.lang(lang);
    if (!token) return token;
    if (/\s/.test(token)) return this.convertText(token, l);
    const key = `${l}\u0000${token}`;
    let result = this.convertCache.get(key);
    if (result === undefined) {
      result = this.convertUncached(token, l);
      if (this.convertCache.size >= 4096) this.convertCache.clear();
      this.convertCache.set(key, result);
    }
    return result;
  }

  private wordsExact(lang: Lang): Set<string> {
    let keys = this.wordsExactCache.get(lang);
    if (!keys) {
      keys = new Set<string>();
      for (const entry of words_(WORDS[lang])) {
        const [raw, aliases] = entry.split("|");
        for (const roman of aliases ? aliases.split(",") : [raw.toLowerCase()]) keys.add(roman.toLowerCase());
      }
      this.wordsExactCache.set(lang, keys);
    }
    return keys;
  }

  private isUpperPhonetic(core: string, lang: Lang): boolean {
    if (lang === "en" || core.length <= 1 || !/^[A-Z]+$/.test(core)) return false;
    const low = core.toLowerCase();
    return this.wordsExact(lang).has(low) || Boolean(this.user.get(lang)?.has(low));
  }

  private convertUncached(token: string, lang: Lang): string {
    if (URL_OR_ID.test(token) || CURRENCY.test(token)) return token;
    const [lead, core, trail] = splitPunct(token);
    if (!core) return token;
    if (URL_OR_ID.test(core) || CURRENCY.test(core) || core.toLowerCase() === "rs" || core.toLowerCase() === "s$") return token;
    if (trail.startsWith(".") && ABBREVIATIONS.has(core.toLowerCase())) return token;
    const sound = numberSound(lang, core);
    if (sound) return lead + sound + trail;
    if ((isProtected(core) && !this.isUpperPhonetic(core, lang)) || !LATIN_WORD.test(core)) return token;
    return lead + this.matchSound(core, lang) + trail;
  }

  convertText(text: string, lang?: Lang): string {
    const l = this.lang(lang);
    const parts = text.split(/(\s+|[—–])/);
    let prevTok = "";
    return parts.map((p, idx) => {
      if (!p || /^\s+$/.test(p) || p === "—" || p === "–") return p;
      const core = splitPunct(p)[1];
      let nextCore = "";
      for (let k = idx + 1; k < parts.length; k++) {
        const cand = parts[k];
        if (cand && !/^\s+$/.test(cand) && cand !== "—" && cand !== "–") {
          nextCore = splitPunct(cand)[1];
          break;
        }
      }
      const keepCurrPrefix = (CURRENCY_WORDS.has(p.toLowerCase()) || CURRENCY_WORDS.has(core.toLowerCase())) && /^\d/.test(nextCore);
      const keepNumSound = CURRENCY_WORDS.has(prevTok.toLowerCase()) && Boolean(numberSound(l, core));
      const out = (keepCurrPrefix || keepNumSound) ? p : this.convertToken(p, l);
      prevTok = p;
      return out;
    }).join("");
  }

  autoCorrectSentence(text: string, lang?: Lang): string {
    const l = this.lang(lang);
    const tidy = text.replace(/(\S)[ \t]{2,}/g, "$1 ").replace(/(\S)[ \t]+(?=[,;:!?.](?:\s|$))/g, "$1");
    if (l === "en") return this.correctEnglish(tidy);
    if (l === "ta" || l === "ta-sen") return this.perSentence(tidy, (w) => this.agreeTamil(w, l));
    if (l === "hi" || l === "hi-prathmic") return this.perSentence(tidy, (w) => this.agreeHindi(w));
    return tidy;
  }

  private correctEnglish(text: string): string {
    const parts = text.split(/(\s+)/);
    let start = true;
    parts.forEach((token, i) => {
      if (!token || /^\s+$/.test(token)) return;
      const [lead, original, trail] = splitPunct(token);
      let core = original;
      if (core && !isProtected(token) && LATIN_WORD.test(core)) {
        core = this.matchSound(core, "en");
        if (start) core = capitalise(core);
        parts[i] = lead + core + trail;
      }
      start = /^[.!?]/.test(trail) && !ABBREVIATIONS.has(core.toLowerCase());
    });
    return parts.join("")
      .replace(/\bI (?:is|are)\b/g, "I am")
      .replace(/\b([Yy]ou|[Tt]hey|[Ww]e) is\b/g, "$1 are")
      .replace(/\b([Hh]e|[Ss]he|[Ii]t) don't\b/g, "$1 doesn't");
  }

  private perSentence(text: string, fix: (words: string[]) => string[]): string {
    const chunks = text.split(/([.!?।\n]+)/);
    for (let i = 0; i < chunks.length; i += 2) {
      const parts = chunks[i].split(/(\s+)/);
      const positions = parts.map((p, j) => (p && !/^\s+$/.test(p) ? j : -1)).filter((j) => j >= 0);
      if (!positions.length) continue;
      const fixed = fix(positions.map((j) => parts[j]));
      positions.forEach((j, n) => (parts[j] = fixed[n]));
      chunks[i] = parts.join("");
    }
    return chunks.join("");
  }

  private agreeTamil(input: string[], lang: Lang): string[] {
    const formal = new Map([["ரொம்ப", "மிகவும்"], ["தேங்க்ஸ்", "நன்றி"], ["லீவு", "விடுப்பு"],
      ["ஆபீஸ்", "அலுவலகம்"], ["ஸ்கூல்", "பள்ளி"], ["நீ", "நீங்கள்"]]);
    const words = lang === "ta-sen" ? input.map((w) => formal.get(w) ?? w) : input.slice();
    const subjects = words.filter((w) => w === "நான்" || w === "நீங்கள்");
    if (subjects.length !== 1 || words.length < 2) return words;
    const wanted = subjects[0] === "நான்" ? "கிறேன்" : "கிறீர்கள்";
    const [lead, core, trail] = splitPunct(words[words.length - 1]);
    const ending = ["கிறீர்கள்", "கிறார்கள்", "கிறோம்", "கிறேன்", "கிறாய்", "கிறான்", "கிறாள்", "கிறார்"]
      .find((e) => core.endsWith(e));
    if (ending) words[words.length - 1] = lead + core.slice(0, -ending.length) + wanted + trail;
    return words;
  }

  private agreeHindi(input: string[]): string[] {
    const words = input.slice();
    const subjects = words.filter((w) => w === "मैं" || w === "आप");
    if (subjects.length !== 1 || words.length < 2) return words;
    const [lead, core, trail] = splitPunct(words[words.length - 1]);
    if (["है", "हैं", "हो", "हूँ", "हूं"].includes(core)) {
      words[words.length - 1] = lead + (subjects[0] === "मैं" ? "हूँ" : "हैं") + trail;
    }
    return words;
  }

  detectCategory(heading: string, priorText = ""): Category | null {
    for (const source of [heading, priorText]) {
      const low = (source || "").toLowerCase();
      if (!low) continue;
      for (const [category, keywords] of HEADING_KEYWORDS) {
        for (const keyword of keywords) {
          // Plain ASCII keywords need word boundaries; others match as substrings.
          const escaped = keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
          const hit = /^[\x20-\x7e]+$/.test(keyword)
            ? new RegExp(`\\b${escaped}\\b`).test(low)
            : low.includes(keyword);
          if (hit) return category;
        }
      }
    }
    return null;
  }

  private locate(prior: string, words: Pair[], lang: Lang): number | null {
    if (!prior.trim()) return 0;
    if (UNSPACED_LANGUAGES.includes(lang)) {
      const compact = words_(prior).join("");
      for (let k = words.length; k > 0; k--) {
        if (compact.endsWith(words.slice(0, k).map((w) => w[0]).join(""))) return k;
      }
      return null;
    }
    const typed = words_(prior).map(normWord).filter(Boolean);
    if (!typed.length) return 0;
    const flat: [string, number | null][] = [];
    words.forEach(([nStr], idx) => {
      const subs = words_(nStr).map(normWord).filter(Boolean);
      const parts = subs.length ? subs : [normWord(nStr)];
      parts.forEach((sub, k) => {
        flat.push([sub, k === parts.length - 1 ? idx + 1 : null]);
      });
    });
    let best = 0;
    let position: number | null = null;
    for (let j = 0; j < flat.length; j++) {
      const nextPos = flat[j][1];
      if (nextPos === null) continue;
      let n = 0;
      while (n < typed.length && n <= j && flat[j - n][0] === typed[typed.length - 1 - n]) n++;
      if (n > best) {
        best = n;
        position = nextPos;
      }
    }
    return position;
  }

  private wordMatches(typed: string, [native, roman]: Pair): boolean {
    const low = typed.toLowerCase();
    if (roman.toLowerCase().startsWith(low) || native.toLowerCase().startsWith(low)) return true;
    return low.length >= 3 && soundSkeleton(roman).startsWith(soundSkeleton(low));
  }

  private body(heading: string, prior: string): string {
    const head = (heading || "").trim();
    const start = prior.replace(/^\s+/, "");
    return head && start.startsWith(head) ? start.slice(head.length) : prior;
  }

  suggestInline(heading: string, priorText: string, currentInput: string, lang?: Lang): InlineSuggestion {
    const l = this.lang(lang);
    const category = this.detectCategory(heading, priorText);
    const typed = currentInput.trim();
    const core = splitPunct(typed)[1];
    const result: InlineSuggestion = {
      replacementWord: "", inlineGhostCompletion: "", nextWords: [], fullClauseSuggestion: "", category,
    };
    if (typed && (numberSound(l, core) || (isProtected(typed) && !this.isUpperPhonetic(core, l)))) {
      result.replacementWord = this.convertToken(typed, l);
      return result;
    }
    const joiner = UNSPACED_LANGUAGES.includes(l) ? "" : " ";
    if (category) {
      const words = this.template(category, l);
      const position = this.locate(this.body(heading, priorText || ""), words, l);
      let match = -1;
      if (position !== null && position < words.length && (!core || this.wordMatches(core, words[position]))) {
        match = position;
      }
      if (match < 0 && core.length >= 3) match = words.findIndex((w) => this.wordMatches(core, w));
      if (match >= 0) {
        let end = match;
        while (end < words.length - 1 && !SENTENCE_END.includes(words[end][0].slice(-1))) end++;
        const clause = words.slice(match, end + 1).map((w) => w[0]).join(joiner);
        const start = core ? match + 1 : match;
        result.replacementWord = core ? words[match][0] : "";
        result.inlineGhostCompletion =
          core && clause.toLowerCase().startsWith(core.toLowerCase()) ? clause.slice(core.length) : clause;
        result.nextWords = words.slice(start, start + 4).map((w) => w[0]);
        result.fullClauseSuggestion = clause;
        return result;
      }
    }
    result.replacementWord = typed ? this.convertToken(typed, l) : "";
    result.inlineGhostCompletion = core.length >= 3 ? this.complete(core, l) : "";
    return result;
  }

  private complete(prefix: string, lang: Lang): string {
    const low = prefix.toLowerCase();
    const pool = Array.from(this.user.get(lang)?.keys() ?? []);
    if (lang === "en") {
      pool.push(...Array.from(this.index("en").exact.keys()));
      pool.push(...Array.from(EN_COMMON_WORDS).sort());
    }
    const hit = pool.find((w) => w.startsWith(low) && w.length > low.length);
    if (hit) return hit.slice(low.length);
    if (lang !== "en") return "";
    let lo = 0;
    let hi = this.osSorted.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (this.osSorted[mid] <= low) lo = mid + 1;
      else hi = mid;
    }
    const next = this.osSorted[lo];
    return next && next.startsWith(low) ? next.slice(low.length) : "";
  }

  onSpaceCommit(heading: string, priorText: string, currentToken: string, lang?: Lang): CommitResult {
    const l = this.lang(lang);
    const prior = priorText || "";
    const token = currentToken.trim();
    if (!token) {
      return { committedWord: "", text: prior, replaced: false, inlineGhostCompletion: "", nextWords: [], fullClauseSuggestion: "" };
    }
    const joiner = UNSPACED_LANGUAGES.includes(l) ? "" : " ";
    const prevList = words_(prior);
    const prevLast = prevList.length ? prevList[prevList.length - 1].toLowerCase() : "";
    const coreTok = splitPunct(token)[1];
    const committedWord = CURRENCY_WORDS.has(prevLast) && numberSound(l, coreTok)
      ? token
      : (this.contextWord(heading, prior, token, l) ?? this.convertToken(token, l));
    const text = prior + (prior && !/\s$/.test(prior) ? joiner : "") + committedWord + joiner;
    const next = this.suggestInline(heading, text, "", l);
    return {
      committedWord,
      text,
      replaced: committedWord !== token,
      inlineGhostCompletion: next.inlineGhostCompletion,
      nextWords: next.nextWords,
      fullClauseSuggestion: next.fullClauseSuggestion,
    };
  }

  private contextWord(heading: string, prior: string, token: string, lang: Lang): string | null {
    const category = this.detectCategory(heading, prior);
    const [lead, core, trail] = splitPunct(token);
    const low = core.toLowerCase();
    if (!category || !core || (isProtected(core) && !this.isUpperPhonetic(core, lang)) || numberSound(lang, core)) return null;
    if (URL_OR_ID.test(token) || this.user.get(lang)?.has(low)) return null;
    if (lang === "en" && EN_CORRECTIONS.has(low) && low !== "i") return null;
    const words = this.template(category, lang);
    const position = this.locate(this.body(heading, prior), words, lang);
    let match = -1;
    if (position !== null && position < words.length) {
      const [nativeP, romanP] = words[position];
      if (lang === "en") {
        if (!(position === 0 && core.length === 1 && (low === "a" || low === "i") && romanP.toLowerCase() !== low)) {
          if (romanP.toLowerCase().startsWith(low) || nativeP.toLowerCase().startsWith(low)) match = position;
        }
      } else if (this.wordMatches(core, words[position])) {
        match = position;
      }
    }
    if (match < 0 && core.length >= 3 && !(lang === "en" && EN_COMMON_WORDS.has(low))) {
      match = words.findIndex((w) => this.wordMatches(core, w));
    }
    if (match < 0) return null;
    const [native, roman] = words[match];
    if (lang !== "en" && low !== roman.toLowerCase() && this.index(lang).exact.has(low)) return null;
    return lead + (trail ? splitPunct(native)[1] + trail : native);
  }
}

// ---------------------------------------------------------------- font metadata

export interface FamilyInfo {
  styles: string[];
  files: string[];
  ocrConfidence: number | null;
}

export interface FontIndex {
  families: Record<string, FamilyInfo>;
  familyCount: number;
  styleCount: number;
  languages: string[];
  scanMs: number;
}

const now = (): number => (globalThis as any).performance?.now() ?? Date.now();

/** Browsers cannot list directories, so pass paths shaped `<family>/.../<Name>-<Style>.<ext>`. */
export class BackgroundFontMetadataIndexer {
  index: FontIndex | null = null;
  done: Promise<FontIndex | null> = Promise.resolve(null);

  /** Defers indexing to a later task; returns the dispatch time in ms. */
  start(files: string[], ocrConfidence: Record<string, number> = {}): number {
    const began = now();
    const defer: (fn: () => void) => void =
      (globalThis as any).setTimeout
        ? (fn: () => void) => (globalThis as any).setTimeout(fn, 0)
        : (fn: () => void) => { void Promise.resolve().then(fn); };
    this.done = new Promise((resolve) => defer(() => resolve(this.run(files, ocrConfidence))));
    return now() - began;
  }

  private run(files: string[], ocr: Record<string, number>): FontIndex {
    const began = now();
    const families: Record<string, FamilyInfo> = {};
    for (const file of files) {
      const parts = file.split("/");
      const match = /^(.*)\.(woff2|woff|ttf|otf)$/i.exec(parts[parts.length - 1]);
      if (!match || parts.length < 2) continue;
      const info = (families[parts[0]] ??= { styles: [], files: [], ocrConfidence: ocr[parts[0]] ?? null });
      const dash = match[1].lastIndexOf("-");
      const style = dash >= 0 ? match[1].slice(dash + 1) : "Regular";
      if (!info.styles.includes(style)) info.styles.push(style);
      info.files.push(file);
    }
    const values = Object.values(families);
    this.index = {
      families,
      familyCount: values.length,
      styleCount: values.reduce((sum, f) => sum + f.styles.length, 0),
      languages: Object.keys(LANGUAGES),
      scanMs: now() - began,
    };
    return this.index;
  }
}

const engine = new SoundOfFontEngine({ language: "en" });

export async function handleSoundOfFontRequest(req: Request): Promise<Response> {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "authorization, content-type, x-client-info, apikey",
      },
    });
  }
  if (req.method === "GET") {
    return new Response(
      JSON.stringify({
        service: "Aaahhh Fonts Vibe — Sound of Font Edge API",
        version: "3.0.0",
        status: "ok",
        languages: LANGUAGES,
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Access-Control-Allow-Origin": "*",
        },
      },
    );
  }
  const body = (await req.json().catch(() => ({}))) as {
    lang?: Lang;
    heading?: string;
    priorText?: string;
    token?: string;
    text?: string;
  };
  const lang: Lang = body.lang && body.lang in LANGUAGES ? body.lang : "en";
  const heading = body.heading ?? "";
  const priorText = body.priorText ?? "";
  const token = body.token ?? "";

  const suggestion = engine.suggestInline(heading, priorText, token, lang);
  const committed = token ? engine.onSpaceCommit(heading, priorText, token, lang) : null;
  const convertedText = body.text ? engine.autoCorrectSentence(engine.convertText(body.text, lang), lang) : "";

  return new Response(
    JSON.stringify({
      version: "3.0.0",
      language: lang,
      suggestion,
      committed,
      convertedText,
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
      },
    },
  );
}

declare const Deno: { serve?: (handler: (req: Request) => Response | Promise<Response>) => unknown } | undefined;
if (typeof Deno !== "undefined" && Deno && typeof Deno.serve === "function") {
  Deno.serve(handleSoundOfFontRequest);
}
