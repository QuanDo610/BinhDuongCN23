import Foundation
import Vision
import AppKit
import PDFKit

func ocrCGImage(_ cgImage: CGImage) {
    let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    let request = VNRecognizeTextRequest { request, error in
        guard let observations = request.results as? [VNRecognizedTextObservation], error == nil else {
            if let err = error {
                fputs("OCR error: \(err.localizedDescription)\n", stderr)
            }
            return
        }
        
        // Sort observations top-to-bottom, left-to-right
        let sortedObservations = observations.sorted { obs1, obs2 in
            let y1 = obs1.boundingBox.origin.y
            let y2 = obs2.boundingBox.origin.y
            if abs(y1 - y2) > 0.015 {
                return y1 > y2 // Vision coordinates origin is bottom-left
            }
            return obs1.boundingBox.origin.x < obs2.boundingBox.origin.x
        }
        
        for observation in sortedObservations {
            if let candidate = observation.topCandidates(1).first {
                print(candidate.string)
            }
        }
    }
    
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["vi-VN", "en-US"]
    request.usesLanguageCorrection = true
    
    do {
        try requestHandler.perform([request])
    } catch {
        fputs("Failed to perform request: \(error.localizedDescription)\n", stderr)
    }
}

let args = CommandLine.arguments
guard args.count > 1 else {
    print("Usage: ocr_vision <file_path.pdf|png|jpg|jpeg|tiff>")
    exit(1)
}

let filePath = args[1]
let url = URL(fileURLWithPath: filePath)
let ext = url.pathExtension.lowercased()

if ext == "pdf" {
    guard let pdf = PDFDocument(url: url) else {
        fputs("Failed to load PDF at \(filePath)\n", stderr)
        exit(1)
    }
    
    let totalPages = pdf.pageCount
    for i in 0..<totalPages {
        guard let page = pdf.page(at: i) else { continue }
        print("=== TRANG \(i + 1)/\(totalPages) ===")
        let bounds = page.bounds(for: .mediaBox)
        let scale: CGFloat = 2.0 // 2x resolution for crisp OCR
        let targetSize = NSSize(width: bounds.width * scale, height: bounds.height * scale)
        let thumb = page.thumbnail(of: targetSize, for: .mediaBox)
        
        if let tiffData = thumb.tiffRepresentation,
           let bitmap = NSBitmapImageRep(data: tiffData),
           let cgImage = bitmap.cgImage {
            ocrCGImage(cgImage)
        }
    }
} else {
    guard let image = NSImage(contentsOf: url),
          let tiffData = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiffData),
          let cgImage = bitmap.cgImage else {
        fputs("Failed to load image at \(filePath)\n", stderr)
        exit(1)
    }
    ocrCGImage(cgImage)
}
