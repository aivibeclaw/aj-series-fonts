import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sound_of_font import BackgroundFontMetadataIndexer, SoundOfFontEngine, detect_default_language
from sound_of_font.dictionaries import CATEGORIES, LANGUAGES, TEMPLATES
from sound_of_font.engine.sound_of_font import transliterate


class Base(unittest.TestCase):
    def setUp(self):
        self.engine = SoundOfFontEngine(language="en")


class GuardTests(Base):
    def test_empty_and_whitespace(self):
        for lang in LANGUAGES:
            self.assertEqual(self.engine.convert_token("", lang), "")
            self.assertEqual(self.engine.convert_text("   ", lang), "   ")
        self.assertEqual(self.engine.auto_correct_sentence("", "en"), "")
        result = self.engine.on_space_commit("Leave Letter", "", "", "en")
        self.assertEqual((result.committed_word, result.text, result.replaced), ("", "", False))

    def test_numbers_currency_and_ids_untouched(self):
        samples = ["1", "42", "Rs1", "Rs.1", "Rs 1", "₹1", "$10", "S$10", "RM10", "Rs.1,250.50/-",
                   "2026-11-26", "(1)", "INV-001", "No. 1", "https://example.com/a?b=1",
                   "(https://example.com/vanakkam)", "<someone@example.com>",
                   "www.example.com", "someone@example.com", "GST"]
        for lang in LANGUAGES:
            for sample in samples:
                with self.subTest(lang=lang, sample=sample):
                    self.assertEqual(self.engine.convert_text(sample, lang), sample)
        # Currency-prefixed number sounds ('Rs 1u', 'Rs. 1u') must keep '1u' unconverted!
        self.assertEqual(self.engine.convert_text("Rs 1u", "ta"), "Rs 1u")
        self.assertEqual(self.engine.convert_text("Rs. 1u", "ta"), "Rs. 1u")
        self.assertEqual(self.engine.on_space_commit("Invoice", "Rs ", "1u", "ta").committed_word, "1u")
        # Honorific abbreviations stay intact while names transliterate
        self.assertEqual(self.engine.convert_text("Mr. vanakkam", "ta"), "Mr. வணக்கம்")
        self.assertEqual(self.engine.convert_text("Dr. vanakkam", "ta"), "Dr. வணக்கம்")
        # Em-dash & en-dash compound boundaries convert both sides cleanly
        self.assertEqual(self.engine.convert_text("vanakkam—nandri", "ta"), "வணக்கம்—நன்றி")
        self.assertEqual(self.engine.convert_text("vanakkam–nandri", "ta"), "வணக்கம்–நன்றி")

    def test_space_commit_keeps_numbers(self):
        for token in ("1", "Rs1", "Rs.1"):
            self.assertEqual(self.engine.on_space_commit("Leave Letter", "", token, "ta").committed_word, token)

    def test_tamil_number_sounds(self):
        cases = {
            "ஒன்று": ("1u", "onnu", "ondru"), "இரண்டு": ("2u", "rendu", "irandu"),
            "மூன்று": ("3u", "moonu", "moondru"), "நான்கு": ("4u", "naalu", "naangu"),
            "ஐந்து": ("5u", "anju", "aindhu"),
        }
        for lang in ("ta", "ta-sen"):
            for native, sounds in cases.items():
                for sound in sounds:
                    with self.subTest(lang=lang, sound=sound):
                        self.assertEqual(self.engine.convert_token(sound, lang), native)
        self.assertEqual(self.engine.convert_token("1u", "hi"), "1u")


class PhoneticTests(Base):
    def test_spelling_variants(self):
        for variant in ("vanakkam", "vanakam", "vannakkam", "wanakkam", "Vanakkam"):
            self.assertEqual(self.engine.convert_token(variant, "ta"), "வணக்கம்", variant)
        for variant in ("nandri", "nanri"):
            self.assertEqual(self.engine.convert_token(variant, "ta"), "நன்றி", variant)
        for variant in ("namasthe", "namaste"):
            self.assertEqual(self.engine.convert_token(variant, "hi"), "नमस्ते", variant)

    def test_punctuation_boundaries(self):
        self.assertEqual(self.engine.convert_token("vanakkam!", "ta"), "வணக்கம்!")
        self.assertEqual(self.engine.convert_token("(nandri)", "ta"), "(நன்றி)")
        self.assertEqual(self.engine.convert_token("1u,", "ta"), "ஒன்று,")
        self.assertEqual(self.engine.convert_token("...", "ta"), "...")
        self.assertEqual(self.engine.convert_text("vanakkam,  nandri.", "ta"), "வணக்கம்,  நன்றி.")

    def test_all_24_languages(self):
        cases = {
            "en": ("recieve", "receive"), "ta": ("vanakkam", "வணக்கம்"),
            "ta-sen": ("vanakkam", "வணக்கம்"), "hi": ("namaste", "नमस्ते"),
            "hi-prathmic": ("namaste", "नमस्ते"), "te": ("namaskaram", "నమస్కారం"),
            "ml": ("namaskaram", "നമസ്കാരം"), "kn": ("namaskara", "ನಮಸ್ಕಾರ"),
            "bn": ("nomoskar", "নমস্কার"), "mr": ("namaskar", "नमस्कार"),
            "pa": ("dhanvaad", "ਧੰਨਵਾਦ"), "ar": ("marhaba", "مرحبا"),
            "ur": ("shukriya", "شکریہ"), "sa": ("namaskarah", "नमस्कारः"),
            "ja": ("konnichiwa", "こんにちは"), "ru": ("privet", "привет"),
            "es": ("adios", "adiós"), "fr": ("tres", "très"), "de": ("fur", "für"),
            "ms": ("terimakasih", "terima kasih"), "zh": ("nihao", "你好"),
            "th": ("sawatdee", "สวัสดี"), "am": ("selam", "ሰላም"),
            "ko": ("annyeonghaseyo", "안녕하세요"),
        }
        self.assertEqual(len(LANGUAGES), 24)
        self.assertEqual(set(cases), set(LANGUAGES))
        for lang, (typed, expected) in cases.items():
            with self.subTest(lang=lang):
                self.assertEqual(self.engine.convert_token(typed, lang), expected)

    def test_transliteration_fallback(self):
        cases = [("kamal", "hi", "कमल"), ("kamal", "te", "కమల్"), ("dom", "ru", "дом"),
                 ("sakura", "ja", "さくら"), ("selam", "am", "ሰላም"), ("hana", "ko", "하나")]
        for typed, lang, expected in cases:
            with self.subTest(lang=lang):
                self.assertEqual(transliterate(typed, lang), expected)


class CorrectionTests(Base):
    def test_english(self):
        fix = lambda text: self.engine.auto_correct_sentence(text, "en")
        self.assertEqual(fix("i  recieve teh mail ."), "I receive the mail.")
        self.assertEqual(fix("he don't know. you is here."), "He doesn't know. You are here.")
        self.assertEqual(fix("pay Rs. 1 now"), "Pay Rs. 1 now")
        self.assertEqual(fix("visit https://example.com/teh today"), "Visit https://example.com/teh today")

    def test_tamil_agreement(self):
        self.assertEqual(self.engine.auto_correct_sentence("நான் வருகிறீர்கள்.", "ta"), "நான் வருகிறேன்.")
        self.assertEqual(self.engine.auto_correct_sentence("நீங்கள் வருகிறேன்", "ta"), "நீங்கள் வருகிறீர்கள்")
        self.assertEqual(self.engine.auto_correct_sentence("நீ வருகிறாய்", "ta-sen"), "நீங்கள் வருகிறீர்கள்")

    def test_hindi_agreement(self):
        self.assertEqual(self.engine.auto_correct_sentence("मैं ठीक है", "hi"), "मैं ठीक हूँ")
        self.assertEqual(self.engine.auto_correct_sentence("आप कैसे है?", "hi"), "आप कैसे हैं?")


class ContextTests(Base):
    def test_heading_categories(self):
        for heading in ("Leave Letter", "Leave Application", "விண்ணப்பம்", "छुट्टी का आवेदन"):
            self.assertEqual(self.engine.detect_category(heading), "leave_letter", heading)
        self.assertEqual(self.engine.detect_category("Invoice"), "invoice")
        self.assertEqual(self.engine.detect_category("Official Email"), "official_email")
        self.assertEqual(self.engine.detect_category("ERP Note"), "erp_note")
        self.assertEqual(self.engine.detect_category("Greeting"), "greeting")
        self.assertIsNone(self.engine.detect_category("Shopping"))

    def test_one_letter_suggestion(self):
        cases = [("en", "R", "Respected"), ("en", "Res", "Respected"),
                 ("ta", "m", "மதிப்பிற்குரிய"), ("ta", "madhippirkuriya", "மதிப்பிற்குரிய"),
                 ("ta-sen", "m", "மதிப்பிற்குரிய"), ("hi", "s", "सविनय"), ("hi", "saviney", "सविनय")]
        for lang, typed, expected in cases:
            with self.subTest(lang=lang, typed=typed):
                suggestion = self.engine.suggest_inline("Leave Letter", "", typed, lang)
                self.assertEqual(suggestion.replacement_word, expected)
                self.assertTrue(suggestion.inline_ghost_completion)
                self.assertTrue(suggestion.next_words)
                self.assertTrue(suggestion.full_clause_suggestion.startswith(expected))
        suggestion = self.engine.suggest_inline("Leave Letter", "", "Res", "en")
        self.assertTrue(suggestion.inline_ghost_completion.startswith("pected Sir/Madam,"))

    def test_space_commit(self):
        result = self.engine.on_space_commit("Leave Letter", "", "R", "en")
        self.assertEqual((result.committed_word, result.text), ("Respected", "Respected "))
        self.assertTrue(result.replaced)
        self.assertEqual(result.next_words[0], "Sir/Madam,")
        result = self.engine.on_space_commit("Leave Letter", result.text, "S", "en")
        self.assertEqual(result.text, "Respected Sir/Madam, ")
        result = self.engine.on_space_commit("Leave Letter", "", "m", "ta")
        self.assertEqual(result.committed_word, "மதிப்பிற்குரிய")
        self.assertEqual(result.next_words[0], "ஐயா,")

    def test_whole_tamil_letter_by_sound(self):
        pairs = [part.split("|") for part in TEMPLATES["ta"]["leave_letter"].split()]
        text = ""
        for _, roman in pairs:
            text = self.engine.on_space_commit("விடுப்பு விண்ணப்பம்", text, roman, "ta").text
        self.assertEqual(text, " ".join(native for native, _ in pairs) + " ")

    def test_common_words_and_unrelated_text_not_expanded(self):
        self.assertEqual(self.engine.on_space_commit("Leave Letter", "", "a", "en").committed_word, "a")
        result = self.engine.on_space_commit("Leave Letter", "Something else ", "R", "en")
        self.assertEqual(result.committed_word, "R")

    def test_every_language_has_every_template(self):
        headings = {"leave_letter": "Leave Letter", "official_email": "Official Email",
                    "invoice": "Invoice", "greeting": "Greeting", "erp_note": "ERP Note"}
        for lang in LANGUAGES:
            for category in CATEGORIES:
                with self.subTest(lang=lang, category=category):
                    suggestion = self.engine.suggest_inline(headings[category], "", "", lang)
                    self.assertEqual(suggestion.category, category)
                    self.assertTrue(suggestion.full_clause_suggestion)
                    self.assertTrue(suggestion.next_words)


class DictionaryAndLocaleTests(Base):
    def test_default_language(self):
        cases = {"ta_IN.UTF-8": "ta", "zh-Hans-CN": "zh", "ta-sen": "ta-sen", "id_ID": "ms",
                 "C": "en", "xx_YY": "en", "": "en"}
        for locale, expected in cases.items():
            self.assertEqual(detect_default_language(locale), expected, locale)
        self.assertEqual(SoundOfFontEngine(system_locale="hi_IN").language, "hi")

    def test_os_dictionary_merge(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "words"
            path.write_text("zyzzyva\nquokka\n", encoding="utf-8")
            self.assertTrue(self.engine.merge_os_dictionary(str(path), wait=True))
            self.assertTrue(self.engine.is_known_word("Quokka"))
            self.assertEqual(self.engine.suggest_inline("", "", "quok", "en").inline_ghost_completion, "ka")
            self.assertFalse(self.engine.merge_os_dictionary(str(Path(folder) / "missing")))

    def test_user_words(self):
        self.assertEqual(self.engine.convert_token("chennai", "en"), "chennai")
        self.engine.add_user_words({"chennai": "சென்னை"}, "ta")
        self.assertEqual(self.engine.convert_token("Chennai", "ta"), "சென்னை")
        self.engine.add_user_words(["AIVibe"])
        self.assertEqual(self.engine.convert_token("aivibe", "en"), "AIVibe")


class IndexerTests(unittest.TestCase):
    def test_background_index(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("fam-a/woff2/FamA-Regular.woff2", "fam-a/woff2/FamA-Bold.woff2",
                         "fam-b/ttf/FamB-Regular.ttf"):
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_bytes(b"")
            (root / "fam-b" / "metadata.json").write_text(json.dumps({"ocr_confidence": 0.9}))
            indexer = BackgroundFontMetadataIndexer(root)
            dispatch_ms = indexer.start()
            self.assertTrue(indexer.wait())
            self.assertLess(dispatch_ms, 50)  # loose bound: thread start jitters on busy machines
            self.assertIsNone(indexer.error)
            self.assertEqual(indexer.index["family_count"], 2)
            self.assertEqual(indexer.index["style_count"], 3)
            self.assertEqual(len(indexer.index["languages"]), 24)
            self.assertIsNone(indexer.index["families"]["fam-a"]["ocr_confidence"])
            self.assertEqual(indexer.index["families"]["fam-b"]["ocr_confidence"], 0.9)


class LatencyTests(Base):
    def test_under_one_ms_per_token(self):
        tokens = ["vanakkam", "vanakam", "nandri", "1u", "Rs.1", "madhippirkuriya", "chennai", "vazhthukal"]
        self.engine.convert_token("warmup", "ta")
        self.engine.suggest_inline("Leave Letter", "", "m", "ta")
        calls = 0
        began = time.perf_counter()
        for round_number in range(100):
            for token in tokens:
                # The suffix defeats the conversion cache on every round.
                suffix = "a" * (round_number % 5)
                self.engine.convert_token(token + suffix, "ta")
                self.engine.on_space_commit("Leave Letter", "", token, "ta")
                calls += 2
        average_ms = (time.perf_counter() - began) * 1000 / calls
        self.assertLess(average_ms, 1.0)


class WebStudioParityTests(unittest.TestCase):
    def test_web_studio_html_covers_all_24_languages_and_5_categories(self):
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "sound_of_font/web/sound-of-font-studio.html").exists())
        for rel in ("sound_of_font/web/sound-of-font-studio.html", "hosting/public/sound-of-font.html"):
            if rel.startswith("hosting/") and not (root / rel).exists():
                continue
            html = (root / rel).read_text(encoding="utf-8")
            for lang in LANGUAGES:
                self.assertIn(f"{lang}:", html if "-" not in lang else html.replace(f'"{lang}":', f"{lang}:"), f"{rel} missing {lang}")
            for cat in CATEGORIES:
                self.assertIn(f'"{cat}"', html, f"{rel} missing category {cat}")
            self.assertIn("BackgroundFontMetadataIndexer", html)
            self.assertIn("mergeOsDictionary", html)
            self.assertIn("autoCorrectSentence", html)

    def test_round3_engine_edge_cases_and_typescript_parity(self):
        import subprocess

        eng = SoundOfFontEngine(language="en")
        # 1. Currency regex fix: bare 'sar' (Malayalam 'സർ' / Leave Letter 'സർ,'), 'rm', 'inr', 'usd' convert cleanly
        self.assertEqual(eng.convert_token("sar", "ml"), "സർ")
        self.assertEqual(eng.on_space_commit("Leave Letter", "ബഹുമാനപ്പെട്ട ", "sar", "ml").committed_word, "സർ,")
        self.assertEqual(eng.convert_text("Rs 500", "ta"), "Rs 500")
        self.assertEqual(eng.convert_text("Rs 1u", "ta"), "Rs 1u")
        self.assertEqual(eng.convert_text("No. 1u", "ta"), "No. 1u")
        self.assertEqual(eng.on_space_commit("Invoice", "No. ", "1u", "ta").committed_word, "1u")
        self.assertEqual(eng.on_space_commit("Invoice", "# ", "1u", "ta").committed_word, "1u")
        self.assertEqual(eng.on_space_commit("Invoice", "$ ", "1u", "ta").committed_word, "1u")

        # 2. ALL-CAPS phonetic words convert when in WORDS[lang], while GST stays GST
        self.assertEqual(eng.convert_token("VANAKKAM", "ta"), "வணக்கம்")
        self.assertEqual(eng.convert_token("NAMASTE", "hi"), "नमस्ते")
        self.assertEqual(eng.convert_token("GST", "ta"), "GST")

        # 3. Punjabi Leave Letter advances past word 2 ('ਸ੍ਰੀਮਾਨ ਜੀ,') to word 3 ('ਮੈਨੂੰ')
        r0 = eng.on_space_commit("Leave Letter", "", "s", "pa")
        self.assertEqual(r0.committed_word, "ਸਤਿਕਾਰਯੋਗ")
        r1 = eng.on_space_commit("Leave Letter", r0.text, "s", "pa")
        self.assertEqual(r1.committed_word, "ਸ੍ਰੀਮਾਨ ਜੀ,")
        r2 = eng.on_space_commit("Leave Letter", r1.text, "m", "pa")
        self.assertEqual(r2.committed_word, "ਮੈਨੂੰ")

        # 4. detect_category scans prior_text + new keywords ('application', 'permission', 'request')
        self.assertEqual(eng.detect_category("", "Submitting leave permission application request"), "leave_letter")

        # 5. _context_word & suggest_inline parity after custom user sentences + English completions
        s_en = eng.suggest_inline("Leave Letter", "Respected Sir/Madam, I ", "a", "en")
        c_en = eng.on_space_commit("Leave Letter", "Respected Sir/Madam, I ", "a", "en")
        self.assertEqual(s_en.replacement_word, "am")
        self.assertEqual(c_en.committed_word, "am")
        s_ta = eng.suggest_inline("Leave Letter", "Custom opening line ", "vinn", "ta")
        c_ta = eng.on_space_commit("Leave Letter", "Custom opening line ", "vinn", "ta")
        self.assertEqual(s_ta.replacement_word, c_ta.committed_word)

        # 6. Tamil nasal clusters + Chinese Pinyin + expanded EN_CORRECTIONS
        self.assertEqual(eng.convert_token("singam", "ta"), "சிங்கம்")
        self.assertEqual(eng.convert_token("bukeqi", "zh"), "不客气")
        self.assertEqual(eng.convert_token("zaijian", "zh"), "再见")
        self.assertEqual(eng.convert_token("accomodate", "en"), "accommodate")
        self.assertEqual(eng.convert_token("definately", "en"), "definitely")

        # 7. TypeScript 1:1 parity via tsc + node
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    "tsc",
                    str(root / "sound_of_font/engine/sound_of_font.ts"),
                    "--target", "ES2020",
                    "--module", "commonjs",
                    "--outDir", tmp,
                ],
                check=True,
            )
            node_check = (
                f"const {{ SoundOfFontEngine }} = require({json.dumps(str(Path(tmp) / 'sound_of_font.js'))});\n"
                "const e = new SoundOfFontEngine({ language: 'en' });\n"
                "const assert = require('assert');\n"
                "assert.strictEqual(e.convertToken('sar', 'ml'), 'സർ');\n"
                "assert.strictEqual(e.onSpaceCommit('Leave Letter', 'ബഹുമാനപ്പെട്ട ', 'sar', 'ml').committedWord, 'സർ,');\n"
                "assert.strictEqual(e.convertText('Rs 500', 'ta'), 'Rs 500');\n"
                "assert.strictEqual(e.convertText('Rs 1u', 'ta'), 'Rs 1u');\n"
                "assert.strictEqual(e.convertText('No. 1u', 'ta'), 'No. 1u');\n"
                "assert.strictEqual(e.convertToken('VANAKKAM', 'ta'), 'வணக்கம்');\n"
                "assert.strictEqual(e.convertToken('GST', 'ta'), 'GST');\n"
                "const p0 = e.onSpaceCommit('Leave Letter', '', 's', 'pa');\n"
                "const p1 = e.onSpaceCommit('Leave Letter', p0.text, 's', 'pa');\n"
                "const p2 = e.onSpaceCommit('Leave Letter', p1.text, 'm', 'pa');\n"
                "assert.strictEqual(p0.committedWord, 'ਸਤਿਕਾਰਯੋਗ');\n"
                "assert.strictEqual(p1.committedWord, 'ਸ੍ਰੀਮਾਨ ਜੀ,');\n"
                "assert.strictEqual(p2.committedWord, 'ਮੈਨੂੰ');\n"
                "assert.strictEqual(e.detectCategory('', 'leave permission request'), 'leave_letter');\n"
                "assert.strictEqual(e.onSpaceCommit('Leave Letter', 'Respected Sir/Madam, I ', 'a', 'en').committedWord, 'am');\n"
                "assert.strictEqual(e.convertToken('bukeqi', 'zh'), '不客气');\n"
            )
            subprocess.run(["node", "-e", node_check], check=True)


if __name__ == "__main__":
    unittest.main()
