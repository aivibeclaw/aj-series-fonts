"""Sound of Font: phonetic, spell/grammar and context inline-helptext engine."""

from .engine.sound_of_font import (
    BackgroundFontMetadataIndexer,
    CommitResult,
    InlineSuggestion,
    SoundOfFontEngine,
    detect_default_language,
)

__all__ = [
    "BackgroundFontMetadataIndexer",
    "CommitResult",
    "InlineSuggestion",
    "SoundOfFontEngine",
    "detect_default_language",
]
__version__ = "1.0.0"
