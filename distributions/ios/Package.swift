// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AJSeriesFonts",
    platforms: [.iOS(.v15), .macOS(.v13), .visionOS(.v1)],
    products: [
        .library(name: "AJSeriesFonts", targets: ["AJSeriesFonts"])
    ],
    targets: [
        .target(
            name: "AJSeriesFonts",
            path: "Sources/AJSeriesFonts"
        )
    ]
)
