import CoreText
import Foundation
import SwiftUI

/// Structured 5-Role Enterprise System Typography for iOS, iPadOS, macOS & visionOS (v3.0.0).
/// All 5 families render with native Default 3D Mild-Gradient Press and unified 25+ languages (incl. Korean Hangul & Sound of Font).
///
/// - **Level 1 · Headers (`header`)**: `AJ Sahasvi` (Sculpted Horizon Royal Small-Caps)
/// - **Level 2 · Sub-Headings (`subheading`)**: `AJ Shresti` (Architectural Geometric — Active OS Default)
/// - **Level 3 · 3rd-Level Text (`level3`)**: `AJ Talin` (0° Straight Connected Running Script)
/// - **Body Text (`body`)**: `AJ Anushya` (Zero-Tail Ultra-Clarity Reading Sans)
/// - **Sound of Font (`soundOfFont`)**: `Aaahhh Fonts Vibe` (Smart Phonetic Multilingual Sans)
public enum AJRole: Sendable {
    case header(size: CGFloat = 32, weight: AJWeight = .extraBold)
    case subheading(size: CGFloat = 22, weight: AJWeight = .semiBold, italic: Bool = false)
    case level3(size: CGFloat = 17, weight: AJWeight = .semiBold, italic: Bool = false)
    case body(size: CGFloat = 15, weight: AJWeight = .regular, italic: Bool = false)
    case soundOfFont(size: CGFloat = 16, weight: AJWeight = .regular, italic: Bool = false)
}

public enum AJWeight: String, Sendable {
    case regular = "Regular"
    case semiBold = "SemiBold"
    case extraBold = "ExtraBold"
}

public enum AJSystemTypography {
    public static func postScriptName(for role: AJRole) -> String {
        switch role {
        case .header(_, let w):
            return "AJSahasvi-\(w.rawValue)"
        case .subheading(_, let w, let italic):
            let suffix = italic ? (w == .regular ? "Italic" : "\(w.rawValue)Italic") : w.rawValue
            return "AJShresti-\(suffix)"
        case .level3(_, let w, let italic):
            let suffix = italic ? (w == .regular ? "Italic" : "\(w.rawValue)Italic") : w.rawValue
            return "AJTalin-\(suffix)"
        case .body(_, let w, let italic):
            let suffix = italic ? (w == .regular ? "Italic" : "\(w.rawValue)Italic") : w.rawValue
            return "AJAnushya-\(suffix)"
        case .soundOfFont(_, let w, let italic):
            let suffix = italic ? (w == .regular ? "Italic" : "\(w.rawValue)Italic") : w.rawValue
            return "AaahhhFontsVibe-\(suffix)"
        }
    }

    public static func font(for role: AJRole) -> Font {
        let size: CGFloat
        switch role {
        case .header(let s, _): size = s
        case .subheading(let s, _, _): size = s
        case .level3(let s, _, _): size = s
        case .body(let s, _, _): size = s
        case .soundOfFont(let s, _, _): size = s
        }
        return .custom(postScriptName(for: role), size: size)
    }

    public static func registerBundledFonts(in bundle: Bundle = .main) {
        guard let urls = bundle.urls(forResourcesWithExtension: "ttf", subdirectory: nil), !urls.isEmpty else {
            return
        }
        CTFontManagerRegisterFontURLs(urls as CFArray, .process, true) { _, _ in true }
    }
}

public extension View {
    func ajTypography(_ role: AJRole) -> some View {
        self.font(AJSystemTypography.font(for: role))
    }
}
