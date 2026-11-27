-- AJ Series & Aaahhh Fonts Vibe (v3.1.0) — PostgreSQL & Supabase Phonetic Lexicon & Trigram Search Schema
-- Copyright (c) 2026 Aravind Jayamohan, India. Published by Aivibe Software Services Private Limited.

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS aivibe_sound_of_font_lexicon (
    id BIGSERIAL PRIMARY KEY,
    lang_code VARCHAR(16) NOT NULL,
    phonetic_key TEXT NOT NULL,
    sound_skeleton TEXT NOT NULL,
    native_word TEXT NOT NULL,
    context_domain VARCHAR(64) NOT NULL DEFAULT 'general',
    frequency_rank INTEGER NOT NULL DEFAULT 100,
    UNIQUE (lang_code, phonetic_key, context_domain)
);

CREATE INDEX IF NOT EXISTS idx_aivibe_sof_skeleton_trgm
    ON aivibe_sound_of_font_lexicon USING gin (sound_skeleton gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_aivibe_sof_lang_prefix
    ON aivibe_sound_of_font_lexicon (lang_code, phonetic_key text_pattern_ops);

-- Guard function ensuring standalone numbers ('1') and currency tokens ('Rs1') are never phonetically mutated
CREATE OR REPLACE FUNCTION aivibe_is_protected_numeric_token(tok TEXT)
RETURNS BOOLEAN LANGUAGE sql IMMUTABLE STRICT AS $$
    SELECT tok ~ '^(?:\d+(?:[.,]\d+)*|(?:Rs\.?|INR|USD|EUR|AED|SAR|SGD|MYR|₹|\$|€|£)\s*\d+(?:[.,]\d+)*)$';
$$;
