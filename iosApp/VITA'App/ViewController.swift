//
//  ViewController.swift
//  VITA'App
//
//  Created by Mikhael on 25/07/2022.
//  Copyright © 2022 ImTech. All rights reserved.
//

import UIKit
import Vision
import VisionKit

class ViewController: UIViewController {
    
    private var ocrTextView = OcrTextView(frame: .zero, textContainer: nil)
    private var scanButton = ScanButton(frame: .zero)
    private var scanImageView = ScanImageView(frame: .zero)
    private var ocrRequest = VNRecognizeTextRequest(completionHandler: nil)
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        configure()
        configureOCR()
    }

    
    private func configure() {
        view.addSubview(ocrTextView)
        view.addSubview(scanImageView)
        view.addSubview(scanButton)
        
        let padding: CGFloat = 16
        NSLayoutConstraint.activate([
            scanButton.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: padding),
            scanButton.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding),
            scanButton.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor, constant: -padding),
            scanButton.heightAnchor.constraint(equalToConstant: 50),
            
            ocrTextView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: padding),
            ocrTextView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding),
            ocrTextView.bottomAnchor.constraint(equalTo: scanButton.topAnchor, constant: -padding),
            ocrTextView.heightAnchor.constraint(equalToConstant: 500),
            
            scanImageView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: padding),
            scanImageView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: padding),
            scanImageView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -padding),
            scanImageView.bottomAnchor.constraint(equalTo: ocrTextView.topAnchor, constant: -padding),
            scanImageView.heightAnchor.constraint(equalToConstant: 600)
        ])
        
        scanButton.addTarget(self, action: #selector(scanDocument), for: .touchUpInside)
    }
    
    
    @objc private func scanDocument() {
        let scanVC = VNDocumentCameraViewController()
        scanVC.delegate = self
        present(scanVC, animated: true)
    }
    
    
    private func saveImage(_ image: UIImage) {
        // Save picture in local file system
        guard let png = image.pngData() else {
            print("Error: Could not get png data of image")
            return
        }
        
        do {
            let dir = getSaveDirectory()
            let path = dir.appendingPathComponent("cropped.png") // appendingPathComponent is deprecated!
            try png.write(to: path)
            print("Picture saved successfully")
        }
        catch {
            print("Error: could not save picture. \(error)")
        }
    }
    
    private func processImage(_ image: UIImage) {
        guard let cgImage = image.cgImage else { return }

        ocrTextView.text = ""
        scanButton.isEnabled = false
        
        let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        do {
            try requestHandler.perform([self.ocrRequest])
        } catch {
            print(error)
        }
    }

    
    private func configureOCR() {
        ocrRequest = VNRecognizeTextRequest { (request, error) in
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
                self.ocrTextView.text = ocrText
                self.scanButton.isEnabled = true
                
                // Saving detected text into file text in local file system
                let dir = getSaveDirectory()
                let path = dir.appendingPathComponent("detectedText.json") // appendingPathComponent is deprecated!
                exportJson(data: allDetected, to: path)
            }
        }
        
        ocrRequest.recognitionLevel = .accurate
        ocrRequest.recognitionLanguages = ["en-US", "en-GB", "fr-FR"]
        ocrRequest.usesLanguageCorrection = true
    }
}


extension ViewController: VNDocumentCameraViewControllerDelegate {
    func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFinishWith scan: VNDocumentCameraScan) {
        guard scan.pageCount >= 1 else {
            controller.dismiss(animated: true)
            return
        }
        
        let image = scan.imageOfPage(at: 0)
        scanImageView.image = image
        saveImage(image)
        processImage(image)
        controller.dismiss(animated: true)
    }
    
    func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFailWithError error: Error) {
        //Handle properly error
        controller.dismiss(animated: true)
    }
    
    func documentCameraViewControllerDidCancel(_ controller: VNDocumentCameraViewController) {
        controller.dismiss(animated: true)
    }
}


func getSaveDirectory() -> URL {
    return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
}

