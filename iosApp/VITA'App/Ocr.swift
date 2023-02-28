//
//  Ocr.swift
//  VITA'App
//
//  Created by Son Pham-Ba on 28.02.23.
//  Copyright © 2023 ImTech. All rights reserved.
//

import Foundation
import UIKit
import Vision
import VisionKit


struct OcrRequest {
    var request: VNRecognizeTextRequest
    
    init(_ outputPath: URL) {
        request = VNRecognizeTextRequest { (request, error) in
            guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
        
            // Text shown in interface
            var ocrText = ""
            // Data to be exported
            var allDetected: [DetectedText] = []
            
            for observation in observations {
                guard let topCandidate = observation.topCandidates(1).first else { return }
                
                ocrText += topCandidate.string + "\n"
                var detectedText = DetectedText(text: topCandidate.string)
                
                // Create range for bounding box detection
                let startIndex = topCandidate.string.startIndex
                let endIndex = topCandidate.string.endIndex
                let range = startIndex ..< endIndex
                
                do {
                    let bbox: VNRectangleObservation = try topCandidate.boundingBox(for: range)!
                    
                    detectedText.bbox.bottomLeft  = Point(x: bbox.bottomLeft.x,  y: bbox.bottomLeft.y)
                    detectedText.bbox.bottomRight = Point(x: bbox.bottomRight.x, y: bbox.bottomRight.y)
                    detectedText.bbox.topLeft     = Point(x: bbox.topLeft.x,     y: bbox.topLeft.y)
                    detectedText.bbox.topRight    = Point(x: bbox.topRight.x,    y: bbox.topRight.y)
                } catch {
                    print("Could not retrieve bounding box for text \(topCandidate.string)")
                } // Cannot get bounding box
                
                allDetected.append(detectedText)
            }
            
            DispatchQueue.main.async {
                // Saving detected text into file text in local file system
                exportJson(data: allDetected, to: outputPath)
            }
        }
        
        request.recognitionLevel = .accurate
        request.recognitionLanguages = ["en-US", "en-GB", "fr-FR"]
        request.usesLanguageCorrection = true
    }
}


/** Save image, perform OCR and save OCR data */
func processImage(_ image: UIImage) {
    guard let cgImage = image.cgImage else { return }

    let filename = generateNewFilename()
    let imagePath = generatePath(filename, "png")
    let jsonPath = generatePath(filename, "json")
    saveImage(image, imagePath)

    let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    let ocrRequest = OcrRequest(jsonPath)
    do {
        try requestHandler.perform([ocrRequest.request])
    } catch {
        print(error)
    }
}
