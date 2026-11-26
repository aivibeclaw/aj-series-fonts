/**
 * Sound of Font TypeScript SDK (ES2018+, no dependencies).
 * Mirrors sound_of_font.py and multilingual_lexicon.py; keep them in sync.
 */
export declare const LANGUAGES: {
    readonly en: "English";
    readonly ta: "Tamil";
    readonly "ta-sen": "Sen Tamil";
    readonly hi: "Hindi";
    readonly "hi-prathmic": "Prathmic Hindi";
    readonly te: "Telugu";
    readonly ml: "Malayalam";
    readonly kn: "Kannada";
    readonly bn: "Bengali";
    readonly mr: "Marathi";
    readonly pa: "Punjabi";
    readonly ar: "Arabic";
    readonly ur: "Urdu";
    readonly sa: "Sanskrit";
    readonly ja: "Japanese";
    readonly ru: "Russian";
    readonly es: "Spanish";
    readonly fr: "French";
    readonly de: "German";
    readonly ms: "Malay";
    readonly zh: "Chinese";
    readonly th: "Thai";
    readonly am: "Amharic";
    readonly ko: "Korean";
};
export type Lang = keyof typeof LANGUAGES;
export type Category = "leave_letter" | "official_email" | "invoice" | "greeting" | "erp_note";
export declare const CATEGORIES: Category[];
export declare function splitPunct(token: string): [string, string, string];
export declare function isProtected(token: string): boolean;
export declare function soundSkeleton(word: string): string;
export declare function acousticDistance(a: string, b: string): number;
export declare function transliterate(word: string, lang: string): string;
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
export declare function detectDefaultLanguage(systemLocale?: string): Lang;
export declare class SoundOfFontEngine {
    language: Lang;
    private user;
    private indexCache;
    private wordsExactCache;
    private templateCache;
    private convertCache;
    private osWords;
    private osSorted;
    constructor(options?: {
        language?: Lang;
        systemLocale?: string;
    });
    private lang;
    /**
     * Merge an OS/app word list. Browsers cannot read /usr/share/dict/words:
     * pass its text (Node/Electron: fs.promises.readFile) or an async loader.
     */
    mergeOsDictionary(source: string | Iterable<string> | (() => Promise<string>)): Promise<number>;
    addUserWords(words: string[] | Record<string, string>, lang?: Lang): void;
    isKnownWord(word: string, lang?: Lang): boolean;
    private template;
    private index;
    private matchSound;
    convertToken(token: string, lang?: Lang): string;
    private wordsExact;
    private isUpperPhonetic;
    private convertUncached;
    convertText(text: string, lang?: Lang): string;
    autoCorrectSentence(text: string, lang?: Lang): string;
    private correctEnglish;
    private perSentence;
    private agreeTamil;
    private agreeHindi;
    detectCategory(heading: string, priorText?: string): Category | null;
    private locate;
    private wordMatches;
    private body;
    suggestInline(heading: string, priorText: string, currentInput: string, lang?: Lang): InlineSuggestion;
    private complete;
    onSpaceCommit(heading: string, priorText: string, currentToken: string, lang?: Lang): CommitResult;
    private contextWord;
}
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
/** Browsers cannot list directories, so pass paths shaped `<family>/.../<Name>-<Style>.<ext>`. */
export declare class BackgroundFontMetadataIndexer {
    index: FontIndex | null;
    done: Promise<FontIndex | null>;
    /** Defers indexing to a later task; returns the dispatch time in ms. */
    start(files: string[], ocrConfidence?: Record<string, number>): number;
    private run;
}
